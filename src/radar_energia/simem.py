"""Cliente mínimo y explícito para la API pública de SIMEM (XM).

Se basa en el contrato que usa la librería oficial ``pydataxm`` (v0.3.19), pero con
control propio sobre reintentos, partición de fechas y trazabilidad de cada descarga.

Endpoints:
- Metadatos de un dataset: GET  ``/detalle-datos-publicos?datasetId=...``
- Datos de un dataset:      POST ``/datos-publicos?startDate=...&endDate=...&datasetId=...``
- Catálogos:                GET  ``/PublicData?startdate=...&enddate=...&datasetId=...``
"""

from __future__ import annotations

import datetime as dt
import logging
import time
from collections.abc import Iterator
from dataclasses import dataclass, field

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://www.simem.co/backend-files/api"
FECHA_REFERENCIA = "1990-01-01"

# Máximo de meses por consulta según la granularidad del dataset (regla de pydataxm).
MESES_POR_CONSULTA = {"Horaria": 1, "Diaria": 1, "Semanal": 24, "Mensual": 24, "Anual": 60}

OPERADORES = {
    "=": "eq",
    "!=": "neq",
    "like": "ct",
    "!like": "dnc",
    "in": "in",
    "!in": "nin",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
    "between": "btw",
    "!between": "nbtw",
}


class ErrorSimem(RuntimeError):
    """Error al consultar la API de SIMEM."""


class _Reintentable(Exception):
    """Falla transitoria (5xx, 429): se reintenta con espera exponencial."""


@dataclass(frozen=True)
class Filtro:
    """Filtro de la API: columna, operador (ver ``OPERADORES``) y valor(es)."""

    columna: str
    operador: str
    valor: str | list[str]

    def a_api(self) -> dict:
        if self.operador not in OPERADORES:
            raise ValueError(f"Operador no soportado: {self.operador}")
        valor = ",".join(self.valor) if isinstance(self.valor, list) else self.valor
        return {"Fd": self.columna, "Op": OPERADORES[self.operador], "Vl": valor, "Lg": "and"}


def ventanas_consulta(
    inicio: dt.date, fin: dt.date, granularidad: str
) -> list[tuple[dt.date, dt.date]]:
    """Parte [inicio, fin] en ventanas que respetan el límite de la API.

    Las ventanas se alinean a meses calendario para que cada consulta sea reproducible
    (la misma ventana siempre pide exactamente el mismo rango).
    """
    if inicio > fin:
        return []
    meses = MESES_POR_CONSULTA.get(granularidad, 1)
    ventanas = []
    actual = inicio
    while actual <= fin:
        mes_destino = actual.month - 1 + meses
        siguiente = dt.date(actual.year + mes_destino // 12, mes_destino % 12 + 1, 1)
        cierre = min(siguiente - dt.timedelta(days=1), fin)
        ventanas.append((actual, cierre))
        actual = siguiente
    return ventanas


@dataclass
class ClienteSimem:
    """Cliente HTTP con reintentos exponenciales para SIMEM."""

    base_url: str = BASE_URL
    reintentos: int = 4
    espera_base: float = 2.0
    timeout: int = 180
    sesion: requests.Session = field(default_factory=requests.Session)

    def __post_init__(self) -> None:
        self.sesion.headers.setdefault("User-Agent", "radar-energia/0.1 (+github)")

    # --- HTTP ---------------------------------------------------------------
    def _solicitar(self, metodo: str, url: str, **kwargs):
        ultimo_error: Exception | None = None
        for intento in range(self.reintentos + 1):
            try:
                resp = self.sesion.request(metodo, url, timeout=self.timeout, **kwargs)
                if resp.status_code == 429 or resp.status_code >= 500:
                    raise _Reintentable(f"HTTP {resp.status_code} en {url}")
                if resp.status_code >= 400:
                    # Un 4xx indica una solicitud mal formada: reintentar no ayuda.
                    raise ErrorSimem(f"HTTP {resp.status_code} en {url}: {resp.text[:300]}")
                return resp.json()
            except (_Reintentable, requests.RequestException, ValueError) as e:
                ultimo_error = e
            if intento < self.reintentos:
                espera = self.espera_base * 2**intento
                log.warning("Fallo (%s). Reintento %d en %.0fs", ultimo_error, intento + 1, espera)
                time.sleep(espera)
        raise ErrorSimem(
            f"Sin respuesta válida tras {self.reintentos + 1} intentos: {ultimo_error}"
        )

    # --- Metadatos y catálogos --------------------------------------------
    def metadatos(self, dataset_id: str) -> dict:
        """Nombre, granularidad, columnas y demás metadatos de un dataset."""
        url = f"{self.base_url}/detalle-datos-publicos?datasetId={dataset_id}"
        datos = self._solicitar("GET", url)
        resultado = datos.get("result") or {}
        if not resultado:
            raise ErrorSimem(f"Dataset {dataset_id} sin metadatos: {datos.get('message')}")
        return resultado

    def catalogo(self, catalogo_id: str) -> list[dict]:
        """Registros de un catálogo (datasets o variables)."""
        hoy = dt.date.today().isoformat()
        url = (
            f"{self.base_url}/PublicData?startdate={FECHA_REFERENCIA}&enddate={hoy}"
            f"&datasetId={catalogo_id}"
        )
        datos = self._solicitar("GET", url)
        return (datos.get("result") or {}).get("records", [])

    # --- Datos ----------------------------------------------------------------
    def registros(
        self,
        dataset_id: str,
        inicio: dt.date,
        fin: dt.date,
        granularidad: str,
        filtros: list[Filtro] | None = None,
    ) -> Iterator[tuple[tuple[dt.date, dt.date], list[dict]]]:
        """Descarga [inicio, fin] ventana por ventana. Entrega (ventana, registros)."""
        cuerpo = [f.a_api() for f in filtros] if filtros else None
        for desde, hasta in ventanas_consulta(inicio, fin, granularidad):
            url = (
                f"{self.base_url}/datos-publicos?startDate={desde.isoformat()}"
                f"&endDate={hasta.isoformat()}&datasetId={dataset_id}"
            )
            datos = self._solicitar("POST", url, json=cuerpo)
            yield (desde, hasta), _extraer_registros(datos)


def _extraer_registros(datos) -> list[dict]:
    """La API devuelve una lista de registros; algunas respuestas vienen envueltas."""
    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict):
        resultado = datos.get("result", datos)
        if isinstance(resultado, dict):
            return resultado.get("records", [])
        if isinstance(resultado, list):
            return resultado
    raise ErrorSimem(f"Formato de respuesta inesperado: {type(datos).__name__}")
