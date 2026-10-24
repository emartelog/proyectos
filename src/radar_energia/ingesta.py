"""Ingesta: descarga cada dataset por mes, lo guarda en crudo/ y lo carga al almacén.

Si la huella (hash) del contenido no cambió desde la última captura, no se recarga.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import logging
from dataclasses import dataclass

import pandas as pd

from radar_energia.almacen import Almacen
from radar_energia.especificaciones import Especificacion
from radar_energia.simem import ClienteSimem

log = logging.getLogger(__name__)


@dataclass
class ResultadoIngesta:
    dataset: str
    mes: dt.date
    filas: int
    estado: str  # "cargado" | "sin cambios" | "vacío" | "error"
    detalle: str = ""


def fin_de_mes(mes: dt.date) -> dt.date:
    siguiente = dt.date(mes.year + mes.month // 12, mes.month % 12 + 1, 1)
    return siguiente - dt.timedelta(days=1)


def huella(df: pd.DataFrame) -> str:
    """Hash estable del contenido, independiente del orden de filas y columnas."""
    if df.empty:
        return "vacio"
    ordenado = df[sorted(df.columns)].astype(str)
    ordenado = ordenado.sort_values(list(ordenado.columns)).reset_index(drop=True)
    return hashlib.sha256(ordenado.to_csv(index=False).encode()).hexdigest()


class Ingestor:
    def __init__(self, almacen: Almacen, cliente: ClienteSimem | None = None) -> None:
        self.almacen = almacen
        self.cliente = cliente or ClienteSimem()
        self._granularidad: dict[str, str] = {}

    def granularidad(self, dataset: str) -> str:
        if dataset not in self._granularidad:
            meta = self.cliente.metadatos(dataset)
            self._granularidad[dataset] = (meta.get("metadata") or {}).get("granularity", "Diaria")
        return self._granularidad[dataset]

    def descargar(self, esp: Especificacion, mes: dt.date) -> pd.DataFrame:
        registros: list[dict] = []
        for _, lote in self.cliente.registros(
            esp.dataset, mes, fin_de_mes(mes), self.granularidad(esp.dataset)
        ):
            registros.extend(lote)
        return pd.DataFrame.from_records(registros)

    def ingerir(self, esp: Especificacion, mes: dt.date) -> ResultadoIngesta:
        df = self.descargar(esp, mes)
        faltantes = [c for c in esp.columnas_origen if c not in df.columns]
        if not df.empty and faltantes:
            raise ValueError(f"{esp.dataset}: faltan columnas {faltantes}")

        firma = huella(df)
        if firma == self.almacen.huella_registrada(esp.dataset, mes):
            return ResultadoIngesta(esp.dataset, mes, len(df), "sin cambios")

        carpeta = self.almacen.crudo / esp.dataset
        carpeta.mkdir(parents=True, exist_ok=True)
        archivo = carpeta / f"{mes:%Y-%m}.parquet"
        df.to_parquet(archivo, index=False)
        self.almacen.cargar_mes(esp, mes, archivo, firma, len(df))
        estado = "cargado" if len(df) else "vacío"
        log.info("%s %s: %d filas (%s)", esp.dataset, f"{mes:%Y-%m}", len(df), estado)
        return ResultadoIngesta(esp.dataset, mes, len(df), estado)
