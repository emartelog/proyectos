"""Cliente HTTP base con reintentos exponenciales, compartido por todas las fuentes."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import requests

log = logging.getLogger(__name__)


class ErrorFuente(RuntimeError):
    """Error al consultar una fuente de datos."""


class _Reintentable(Exception):
    """Falla transitoria (5xx, 429): se reintenta con espera exponencial."""


@dataclass
class ClienteHttp:
    reintentos: int = 4
    espera_base: float = 2.0
    timeout: int = 180
    sesion: requests.Session = field(default_factory=requests.Session)

    def __post_init__(self) -> None:
        self.sesion.headers.setdefault("User-Agent", "radar-energia/0.1 (+github)")

    def _solicitar(self, metodo: str, url: str, **kwargs):
        ultimo_error: Exception | None = None
        for intento in range(self.reintentos + 1):
            try:
                resp = self.sesion.request(metodo, url, timeout=self.timeout, **kwargs)
                if resp.status_code == 429 or resp.status_code >= 500:
                    raise _Reintentable(f"HTTP {resp.status_code} en {url}")
                if resp.status_code >= 400:
                    # Un 4xx indica una solicitud mal formada: reintentar no ayuda.
                    raise ErrorFuente(f"HTTP {resp.status_code} en {url}: {resp.text[:300]}")
                return resp.json()
            except (_Reintentable, requests.RequestException, ValueError) as e:
                ultimo_error = e
            if intento < self.reintentos:
                espera = self.espera_base * 2**intento
                log.warning("Fallo (%s). Reintento %d en %.0fs", ultimo_error, intento + 1, espera)
                time.sleep(espera)
        raise ErrorFuente(
            f"Sin respuesta válida tras {self.reintentos + 1} intentos: {ultimo_error}"
        )
