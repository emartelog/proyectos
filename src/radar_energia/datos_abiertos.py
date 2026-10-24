"""Cliente del portal de datos abiertos de Colombia (datos.gov.co, plataforma Socrata).

Usa la API clásica (SODA 2.1), que no requiere token para volúmenes moderados:
- Metadatos: GET /api/views/<id>.json
- Registros: GET /resource/<id>.json?$limit=...&$offset=...&$order=:id
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from radar_energia._http import ClienteHttp, ErrorFuente

BASE_URL = "https://www.datos.gov.co"


@dataclass
class ClienteDatosAbiertos(ClienteHttp):
    base_url: str = BASE_URL
    tamano_pagina: int = 50_000

    def metadatos(self, dataset_id: str) -> dict:
        datos = self._solicitar("GET", f"{self.base_url}/api/views/{dataset_id}.json")
        if not isinstance(datos, dict) or "id" not in datos:
            raise ErrorFuente(f"Dataset {dataset_id} sin metadatos")
        return datos

    def registros(self, dataset_id: str, limite: int | None = None) -> Iterator[list[dict]]:
        """Entrega páginas de registros en orden estable hasta agotar o llegar a ``limite``."""
        offset = 0
        while limite is None or offset < limite:
            tamano = (
                self.tamano_pagina if limite is None else min(self.tamano_pagina, limite - offset)
            )
            pagina = self._solicitar(
                "GET",
                f"{self.base_url}/resource/{dataset_id}.json",
                params={"$limit": tamano, "$offset": offset, "$order": ":id"},
            )
            if not isinstance(pagina, list):
                raise ErrorFuente(f"Formato inesperado en {dataset_id}: {type(pagina).__name__}")
            if not pagina:
                return
            yield pagina
            if len(pagina) < tamano:
                return
            offset += len(pagina)
