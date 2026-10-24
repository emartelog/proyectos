"""Almacén local del dato maestro en DuckDB.

Estructura en disco (raíz configurable con la variable de entorno ``RADAR_DATOS``):

    <raiz>/crudo/<DATASET>/<AAAA-MM>.parquet   respuesta de la API, tal cual
    <raiz>/maestro.duckdb                      tablas estandarizadas, vistas y agregados

Cada carga reemplaza la partición mensual completa de una tabla. Como la API entrega todas
las versiones publicadas de un mes, el reemplazo conserva la historia de versiones y la
carga es idempotente: cargar dos veces el mismo archivo deja el mismo resultado.
"""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import duckdb

from radar_energia.especificaciones import (
    ESPECIFICACIONES,
    ORDEN_VERSIONES,
    VERSIONES_PRELIMINARES,
    Especificacion,
)

RAIZ_POR_DEFECTO = Path("datos/local")


def raiz_datos() -> Path:
    return Path(os.environ.get("RADAR_DATOS", RAIZ_POR_DEFECTO))


def _q(nombre: str) -> str:
    """Identificador SQL entre comillas."""
    return '"' + nombre.replace('"', '""') + '"'


class Almacen:
    def __init__(self, raiz: Path | None = None) -> None:
        self.raiz = Path(raiz or raiz_datos())
        self.crudo = self.raiz / "crudo"
        self.raiz.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(self.raiz / "maestro.duckdb"))
        self._crear_esquema()

    def cerrar(self) -> None:
        self.con.close()

    def __enter__(self) -> Almacen:
        return self

    def __exit__(self, *_) -> None:
        self.cerrar()

    # --- Esquema -------------------------------------------------------------
    def _crear_esquema(self) -> None:
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS ingesta_manifiesto (
                dataset VARCHAR, mes DATE, filas BIGINT, huella VARCHAR,
                fecha_captura TIMESTAMP, archivo VARCHAR,
                PRIMARY KEY (dataset, mes)
            )
            """
        )
        self.con.execute("CREATE OR REPLACE TABLE orden_version (version VARCHAR, orden INT)")
        self.con.executemany(
            "INSERT INTO orden_version VALUES (?, ?)",
            [(v, i) for i, v in enumerate(ORDEN_VERSIONES, start=1)],
        )
        for esp in ESPECIFICACIONES:
            self.con.execute(f"CREATE TABLE IF NOT EXISTS {esp.tabla} ({_definicion(esp)})")
            self._crear_vista_vigente(esp)
        self._crear_dimensiones()

    def _crear_vista_vigente(self, esp: Especificacion) -> None:
        """v_<tabla>: una fila por clave natural, con la versión vigente."""
        nombre = f"v_{esp.tabla.removeprefix('h_').removeprefix('m_')}"
        if esp.tipo_version is None:
            self.con.execute(f"CREATE OR REPLACE VIEW {nombre} AS SELECT * FROM {esp.tabla}")
            return
        particion = ", ".join(_q(c) for c in esp.clave)
        if esp.tipo_version == "liquidacion":
            preliminares = ", ".join(f"'{v}'" for v in sorted(VERSIONES_PRELIMINARES))
            self.con.execute(
                f"""
                CREATE OR REPLACE VIEW {nombre} AS
                SELECT t.*, t.version IN ({preliminares}) AS es_preliminar
                FROM {esp.tabla} t LEFT JOIN orden_version o USING (version)
                QUALIFY row_number() OVER (
                    PARTITION BY {particion} ORDER BY o.orden DESC NULLS LAST) = 1
                """
            )
        else:  # publicacion: gana la fecha de publicación más reciente
            self.con.execute(
                f"""
                CREATE OR REPLACE VIEW {nombre} AS
                SELECT * FROM {esp.tabla}
                QUALIFY row_number() OVER (PARTITION BY {particion} ORDER BY version DESC) = 1
                """
            )

    def _crear_dimensiones(self) -> None:
        # SCD2 por "islas": períodos consecutivos con los mismos atributos.
        self.con.execute(
            """
            CREATE OR REPLACE VIEW dim_agente AS
            WITH marcado AS (
                SELECT *, fecha - CAST(row_number() OVER (
                    PARTITION BY agente, nombre, actividad ORDER BY fecha) AS INT) AS isla
                FROM (SELECT DISTINCT fecha, agente, nombre, actividad FROM m_agente_diario)
            )
            SELECT agente, nombre, actividad,
                   min(fecha) AS vigente_desde, max(fecha) AS vigente_hasta,
                   max(fecha) = (SELECT max(fecha) FROM m_agente_diario) AS es_actual
            FROM marcado GROUP BY agente, nombre, actividad, isla
            """
        )
        self.con.execute(
            """
            CREATE OR REPLACE VIEW dim_planta AS
            WITH diario AS (SELECT * FROM v_planta_diario),
            marcado AS (
                SELECT *, fecha - CAST(row_number() OVER (
                    PARTITION BY planta, nombre, agente, tipo_generacion, clasificacion,
                                 tipo_despacho, capacidad_efectiva_neta
                    ORDER BY fecha) AS INT) AS isla
                FROM diario
            )
            SELECT planta, nombre, agente, tipo_generacion, clasificacion, tipo_despacho,
                   area, subarea, capacidad_efectiva_neta,
                   min(fecha) AS vigente_desde, max(fecha) AS vigente_hasta,
                   max(fecha) = (SELECT max(fecha) FROM m_planta_diario) AS es_actual
            FROM marcado
            GROUP BY planta, nombre, agente, tipo_generacion, clasificacion, tipo_despacho,
                     area, subarea, capacidad_efectiva_neta, isla
            """
        )
        # Estado de liquidación de cada mes según el calendario oficial (24914F).
        self.con.execute(
            """
            CREATE OR REPLACE VIEW dim_mes_liquidacion AS
            SELECT date_trunc('month', fecha)::DATE AS mes,
                   arg_max(version, o.orden) AS version_maxima,
                   max(fecha_publicacion) AS ultima_publicacion,
                   count(*) FILTER (WHERE version = 'TXR') = 0 AS es_preliminar
            FROM m_version LEFT JOIN orden_version o USING (version)
            GROUP BY 1
            """
        )

    # --- Carga ---------------------------------------------------------------
    def huella_registrada(self, dataset: str, mes: dt.date) -> str | None:
        fila = self.con.execute(
            "SELECT huella FROM ingesta_manifiesto WHERE dataset = ? AND mes = ?",
            [dataset, mes],
        ).fetchone()
        return fila[0] if fila else None

    def cargar_mes(
        self, esp: Especificacion, mes: dt.date, archivo: Path, huella: str, filas: int
    ) -> None:
        """Reemplaza la partición ``mes`` de la tabla con el contenido de ``archivo``."""
        tiempo = _q(esp.columna_tiempo)
        select = _select_estandar(esp, archivo)
        self.con.execute("BEGIN TRANSACTION")
        try:
            self.con.execute(
                f"DELETE FROM {esp.tabla} WHERE date_trunc('month', {tiempo}) = ?", [mes]
            )
            if filas:
                self.con.execute(
                    f"INSERT INTO {esp.tabla} SELECT * FROM ({select}) "
                    f"WHERE date_trunc('month', {tiempo}) = ?",
                    [mes],
                )
            self.con.execute(
                "INSERT OR REPLACE INTO ingesta_manifiesto VALUES (?, ?, ?, ?, now(), ?)",
                [esp.dataset, mes, filas, huella, str(archivo)],
            )
            self.con.execute("COMMIT")
        except Exception:
            self.con.execute("ROLLBACK")
            raise


def _tipo(destino: str) -> str:
    if destino == "fecha_hora":
        return "TIMESTAMP"
    if destino in ("fecha", "fecha_fin", "fecha_publicacion"):
        return "DATE"
    return "VARCHAR"


def _definicion(esp: Especificacion) -> str:
    cols = [f"{_q(esp.columna_tiempo)} {_tipo(esp.columna_tiempo)}"]
    cols += [f"{_q(d)} {_tipo(d)}" for d in esp.dimensiones.values()]
    cols += [f"{_q(m)} DOUBLE" for m in esp.medidas.values()]
    if esp.tipo_version:
        cols.append("version VARCHAR")
    cols.append("fecha_captura TIMESTAMP")
    return ", ".join(cols)


def _select_estandar(esp: Especificacion, archivo: Path) -> str:
    """SELECT que lleva el crudo al esquema estándar (tipos y nombres)."""
    origen, destino = esp.tiempo
    partes = [f"CAST({_q(origen)} AS {_tipo(destino)}) AS {_q(destino)}"]
    partes += [f"CAST({_q(o)} AS {_tipo(d)}) AS {_q(d)}" for o, d in esp.dimensiones.items()]
    partes += [f"TRY_CAST({_q(o)} AS DOUBLE) AS {_q(d)}" for o, d in esp.medidas.items()]
    if esp.tipo_version:
        partes.append(f"CAST({_q(esp.columna_version)} AS VARCHAR) AS version")
    partes.append("now()::TIMESTAMP AS fecha_captura")
    ruta = str(archivo).replace("'", "''")
    return f"SELECT {', '.join(partes)} FROM read_parquet('{ruta}')"
