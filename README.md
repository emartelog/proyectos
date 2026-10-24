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
| Cliente de la API de SIMEM con reintentos y partición por ventanas | ✅ `src/radar_energia/simem.py` |
| Registro de fuentes por configuración | ✅ `config/fuentes.yml` |
| Reconocimiento y perfilamiento de fuentes | ✅ `src/radar_energia/reconocimiento.py` · workflow `reconocimiento.yml` |
| Pruebas y estilo en CI | ✅ workflow `ci.yml` |
| Modelo del dato maestro (maestros + hechos con versiones de liquidación) | ⏳ tras el reconocimiento |
| Workflow mensual con controles de calidad y publicación por Release | ⏳ |
| Panel y primera nota estratégica | ⏳ |

Las decisiones de diseño están en [`docs/decisiones.md`](docs/decisiones.md) y la propuesta del
dato maestro en [`docs/modelo-dato-maestro.md`](docs/modelo-dato-maestro.md).

## Uso local

```bash
pip install -e ".[dev]"
pytest -q
python -m radar_energia.reconocimiento --config config/fuentes.yml
```

## Fuentes

Datos públicos de SIMEM / XM. Este repositorio no usa información privada de ningún agente
del mercado.
