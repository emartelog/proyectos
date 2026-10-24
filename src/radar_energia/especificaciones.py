"""Cómo se transforma cada dataset de SIMEM en una tabla del dato maestro.

Cada especificación dice qué columnas se conservan y con qué nombre, cuál es la clave
natural y cómo se versiona el dato:

- ``liquidacion``: columna ``Version`` (TX1, TX2, TXR, TXF, TX3 … TX10). Vigente = mayor orden.
- ``publicacion``: una fecha de publicación. Vigente = la más reciente.
- ``None``: sin versión (la descarga más reciente reemplaza a la anterior).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Orden oficial de las versiones de liquidación (TX1 es la primera; TX10 la última).
ORDEN_VERSIONES = ["TX1", "TX2", "TXR", "TXF"] + [f"TX{i}" for i in range(3, 11)]
# Las versiones diarias previas a la liquidación mensual se consideran preliminares.
VERSIONES_PRELIMINARES = {"TX1", "TX2"}


@dataclass(frozen=True)
class Especificacion:
    dataset: str
    tabla: str
    tiempo: tuple[str, str]  # (columna origen, columna destino: fecha | fecha_hora)
    dimensiones: dict[str, str]  # columna origen -> destino
    medidas: dict[str, str] = field(default_factory=dict)
    tipo_version: str | None = "liquidacion"
    columna_version: str = "Version"

    @property
    def columna_tiempo(self) -> str:
        return self.tiempo[1]

    @property
    def clave(self) -> list[str]:
        """Clave natural, sin la versión."""
        return [self.columna_tiempo, *self.dimensiones.values()]

    @property
    def columnas_origen(self) -> list[str]:
        cols = [self.tiempo[0], *self.dimensiones, *self.medidas]
        if self.tipo_version:
            cols.append(self.columna_version)
        return cols


_H = ("FechaHora", "fecha_hora")
_D = ("Fecha", "fecha")

ESPECIFICACIONES: list[Especificacion] = [
    # --- Maestros (instantáneas diarias que se convierten en historia SCD2) ---
    Especificacion(
        "24914F",
        "m_version",
        ("FechaInicio", "fecha"),
        {
            "Version": "version",
            "FechaFin": "fecha_fin",
            "FechaPublicacion": "fecha_publicacion",
            "esMaximaVersion": "es_maxima",
        },
        tipo_version=None,
    ),
    Especificacion(
        "972263",
        "m_agente_diario",
        _D,
        {"CodigoSICAgente": "agente", "NombreAgente": "nombre", "ActividadAgente": "actividad"},
        tipo_version=None,
    ),
    Especificacion(
        "0BFC9D",
        "m_planta_diario",
        _D,
        {
            "CodigoPlanta": "planta",
            "NombrePlanta": "nombre",
            "CodigoSICAgente": "agente",
            "TipoGeneracion": "tipo_generacion",
            "TipoClasificacion": "clasificacion",
            "TipoDespachoRecurso": "tipo_despacho",
            "CodigoAreaOperativa": "area",
            "CodigoSubAreaOperativa": "subarea",
        },
        {"CapEfectivaNeta": "capacidad_efectiva_neta"},
        tipo_version="publicacion",
        columna_version="FechaPublicacion",
    ),
    # --- Hechos ---
    Especificacion(
        "EC6945",
        "h_precio_bolsa_hora",
        _H,
        {"CodigoVariable": "variable"},
        {"Valor": "precio_cop_kwh"},
    ),
    Especificacion(
        "96D56E",
        "h_precio_bolsa_dia",
        _D,
        {"CodigoVariable": "variable"},
        {"Valor": "precio_cop_kwh"},
    ),
    Especificacion(
        "D55202",
        "h_demanda",
        _H,
        {"CodigoSICAgente": "agente", "TipoMercado": "mercado"},
        {"Valor": "kwh"},
    ),
    Especificacion("42EDC9", "h_compra_bolsa", _H, {"CodigoSICAgente": "agente"}, {"Valor": "kwh"}),
    Especificacion("E14D70", "h_venta_bolsa", _H, {"CodigoSICAgente": "agente"}, {"Valor": "kwh"}),
    Especificacion(
        "C8381F",
        "h_contrato_cantidad",
        _H,
        {"CodigoSICAgente": "agente", "TipoMercado": "mercado"},
        {"Valor": "kwh"},
    ),
    Especificacion(
        "E60CE2",
        "h_contrato_venta",
        _H,
        {"CodigoSICAgente": "agente", "TipoMercado": "mercado"},
        {"Valor": "kwh"},
    ),
    Especificacion(
        "D31647",
        "h_contrato_precio",
        _D,
        {
            "CodigoAgenteComprador": "agente",
            "TipoMercado": "mercado",
            "Mecanismo": "mecanismo",
            "NormatividadRelacionada": "norma",
        },
        {"Valor": "precio_cop_kwh"},
    ),
    Especificacion(
        "43D616",
        "h_escasez",
        ("FechaInicio", "fecha"),
        {"CodigoVariable": "variable"},
        {"Valor": "precio_cop_kwh"},
    ),
    Especificacion(
        "BA1C55",
        "h_aportes",
        _D,
        {"CodigoSerieHidrologica": "serie", "RegionHidrologica": "region"},
        {
            "AportesHidricosEnergia": "aportes_energia",
            "MediaHistoricaEnergia": "media_historica_energia",
            "PromedioAcumuladoEnergia": "promedio_acumulado_energia",
        },
        tipo_version="publicacion",
        columna_version="FechaPublicacion",
    ),
    Especificacion("8E7F3C", "h_generacion", _H, {"CodigoPlanta": "planta"}, {"Valor": "kwh"}),
]

POR_DATASET = {e.dataset: e for e in ESPECIFICACIONES}
POR_TABLA = {e.tabla: e for e in ESPECIFICACIONES}
