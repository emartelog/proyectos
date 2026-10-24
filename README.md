# Radar de Energía · Mercado de Energía Mayorista de Colombia

Dato maestro **mensual, versionado y reproducible** del Mercado de Energía Mayorista (MEM),
construido a partir de los datos abiertos de [SIMEM](https://www.simem.co/) (administrado por XM),
y análisis estratégicos que se apoyan en él.

> **Primera pregunta de análisis:** *Exposición a bolsa: ¿qué tan expuesta está la
> comercialización de energía al precio spot, y qué implica para coberturas, tarifas y regulación?*
> El análisis es de nivel de mercado y agregado.

## Arquitectura

```
SIMEM (API pública) ──► Ingesta ──► Crudo ──► Estandarizado ──► Dato maestro ──► Análisis / panel
                        (GitHub      (tal      (tipos, claves,   (maestros +       (notas
                        Actions)     cual)     versiones)        hechos, mensual)  estratégicas)
```

| Componente | Estado |
|---|---|
| Cliente de la API de SIMEM y de datos.gov.co, con reintentos | ✅ `simem.py`, `datos_abiertos.py` |
| Registro de fuentes por configuración (13 datasets) | ✅ `config/fuentes.yml` |
| Reconocimiento y perfilamiento de fuentes | ✅ `reconocimiento.py` · workflow `reconocimiento.yml` |
| Almacén DuckDB: hechos versionados, versión vigente, maestros con historia (SCD2) | ✅ `almacen.py`, `especificaciones.py` |
| Agregados: exposición a bolsa, mercado, distribución | ✅ `agregados.py` |
| Controles de calidad (bloqueantes y de advertencia) | ✅ `calidad.py` |
| Actualización mensual incremental y publicación por Release | ✅ `mensual.py` · workflow `mensual.yml` |
| Carga histórica desde 2021 en tramos | ✅ workflow `carga-historica.yml` · `config/carga_historica.yml` |
| Instalación y tarea programada en Windows | ✅ `scripts/windows/` · [guía](docs/instalacion-windows.md) |
| Pruebas en Linux y Windows (CI) | ✅ workflow `ci.yml` |
| Panel en Streamlit: mercado, comercializadoras y grandes consumidores, con simuladores | ✅ `panel/app.py` |
| Primera nota estratégica | ⏳ |

Las decisiones de diseño están en [`docs/decisiones.md`](docs/decisiones.md) y la propuesta del
dato maestro en [`docs/modelo-dato-maestro.md`](docs/modelo-dato-maestro.md).

## Uso local

```bash
pip install -e ".[dev]"
pytest -q
python -m radar_energia.mensual                      # actualización mensual
python -m radar_energia.mensual --desde 2021-01      # carga histórica
pip install -e ".[panel]" && streamlit run panel/app.py   # panel
```

En Windows, ver la [guía de instalación](docs/instalacion-windows.md).

## Fuentes

Datos públicos de SIMEM / XM. Este repositorio no usa información privada de ningún agente
del mercado.
