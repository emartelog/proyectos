"""Publicación del dato maestro: archivos de salida, historia acumulada y bitácora."""

from __future__ import annotations

import datetime as dt
import json
import logging
from pathlib import Path

import duckdb

from radar_energia.agregados import TABLAS_AGREGADAS
from radar_energia.calidad import Resultado
from radar_energia.ingesta import ResultadoIngesta

log = logging.getLogger(__name__)

TABLAS_MAESTRAS = ["dim_agente", "dim_planta", "dim_mes_liquidacion"]


def incorporar_historico(con: duckdb.DuckDBPyConnection, historico: Path) -> list[str]:
    """Agrega a cada tabla agregada los meses publicados antes que no se recalcularon.

    Sirve cuando el pipeline corre sin estado (p. ej. en GitHub Actions): se descarga la
    publicación anterior y se conservan sus meses, reemplazando solo los recalculados.
    """
    notas = []
    for tabla in TABLAS_AGREGADAS:
        archivo = historico / f"{tabla}.parquet"
        if not archivo.exists():
            notas.append(f"{tabla}: sin publicación anterior")
            continue
        ruta = str(archivo).replace("'", "''")
        try:
            antes = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
            con.execute(
                f"""
                INSERT INTO {tabla} BY NAME
                SELECT * FROM read_parquet('{ruta}')
                WHERE mes NOT IN (SELECT DISTINCT mes FROM {tabla})
                """
            )
            despues = con.execute(f"SELECT count(*) FROM {tabla}").fetchone()[0]
            notas.append(f"{tabla}: {despues - antes} filas históricas conservadas")
        except duckdb.Error as e:  # esquema distinto: se recalcula desde cero la próxima vez
            log.warning("No se pudo incorporar el histórico de %s: %s", tabla, e)
            notas.append(f"{tabla}: histórico incompatible, omitido ({e})")
    return notas


def exportar(con: duckdb.DuckDBPyConnection, salida: Path) -> list[Path]:
    salida.mkdir(parents=True, exist_ok=True)
    archivos = []
    for tabla in TABLAS_AGREGADAS + TABLAS_MAESTRAS:
        for formato, opciones in (("parquet", "FORMAT parquet"), ("csv", "HEADER, DELIMITER ','")):
            destino = salida / f"{tabla}.{formato}"
            ruta = str(destino).replace("'", "''")
            orden = "ORDER BY mes" if tabla.startswith("agg_") else ""
            con.execute(f"COPY (SELECT * FROM {tabla} {orden}) TO '{ruta}' ({opciones})")
            archivos.append(destino)
    return archivos


def _gwh(kwh) -> str:
    return "—" if kwh is None else f"{kwh / 1e6:,.1f} GWh"


def _pct(x) -> str:
    return "—" if x is None else f"{x:.1%}"


def _cop(x) -> str:
    return "—" if x is None else f"{x:,.1f} COP/kWh"


def escribir_bitacora(
    con: duckdb.DuckDBPyConnection,
    salida: Path,
    meses: list[dt.date],
    ingesta: list[ResultadoIngesta],
    calidad: list[Resultado],
    notas_historico: list[str],
) -> Path:
    salida.mkdir(parents=True, exist_ok=True)
    lineas = [
        "# Bitácora del dato maestro",
        "",
        f"Generado: {dt.datetime.now(dt.UTC):%Y-%m-%d %H:%M} UTC",
        f"Meses procesados: {', '.join(f'{m:%Y-%m}' for m in meses)}",
        "",
        "## Resumen del mercado",
        "",
        "| Mes | Demanda | Exposición a bolsa | Precio bolsa (pond. compras) "
        "| Precio escasez | Aportes vs. media | Estado |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    filas = con.execute(
        """
        SELECT mes, demanda_kwh, exposicion_bolsa_pct, precio_bolsa_ponderado_compras,
               precio_escasez, aportes_vs_media_historica_pct, es_preliminar
        FROM agg_mercado_mensual ORDER BY mes DESC LIMIT 13
        """
    ).fetchall()
    for mes, dem, expo, pb, esc, ap, prel in filas:
        estado = "preliminar" if prel else "liquidado"
        lineas.append(
            f"| {mes:%Y-%m} | {_gwh(dem)} | {_pct(expo)} | {_cop(pb)} | {_cop(esc)} "
            f"| {_pct(ap)} | {estado} |"
        )

    lineas += [
        "",
        "## Controles de calidad",
        "",
        "| Control | Nivel | Resultado | Detalle |",
        "|---|---|---|---|",
    ]
    for r in calidad:
        icono = "✅" if r.ok else ("⛔" if r.nivel == "bloquea" else "⚠️")
        lineas.append(f"| {r.control} | {r.nivel} | {icono} | {r.detalle} |")

    lineas += [
        "",
        "## Estado de liquidación (calendario XM)",
        "",
        "| Mes | Versión máxima | Última publicación |",
        "|---|---|---|",
    ]
    for mes, version, publicada in con.execute(
        "SELECT mes, version_maxima, ultima_publicacion FROM dim_mes_liquidacion "
        "ORDER BY mes DESC LIMIT 13"
    ).fetchall():
        lineas.append(f"| {mes:%Y-%m} | {version} | {publicada} |")

    lineas += ["", "## Ingesta", "", "| Dataset | Mes | Filas | Estado |", "|---|---|---:|---|"]
    for r in ingesta:
        detalle = f" — {r.detalle}" if r.detalle else ""
        lineas.append(f"| {r.dataset} | {r.mes:%Y-%m} | {r.filas:,} | {r.estado}{detalle} |")

    if notas_historico:
        lineas += ["", "## Histórico", ""] + [f"- {n}" for n in notas_historico]

    archivo = salida / "bitacora.md"
    archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (salida / "calidad.json").write_text(
        json.dumps([r.a_dict() for r in calidad], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return archivo
