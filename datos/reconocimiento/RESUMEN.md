# Reconocimiento de fuentes SIMEM

Ejecutado: 2026-10-24 17:31 UTC · fecha de referencia 2026-10-24

| ID | Dataset | Granularidad | Filas | Duplicadas | Versiones | Estado |
|---|---|---|---:|---:|---|---|
| 24914F | Versiones de factura para la liquidación mensual | Diaria | 47 | 0 | TX3:12, TX4:7, TX5:4, TXF:12, TXR:12 | ok |
| 0BFC9D | Parámetros técnicos de las plantas de generación | Diaria | 69,813 | 0 | — | ok |
| 96D56E | Precio de bolsa ponderado | Diaria | 489 | 0 | TX1:61, TX2:122, TX3:62, TXF:122, TXR:122 | ok |
| D55202 | Demanda comercial nacional | Horaria | 479,808 | 0 | TX2:136872, TX3:69192, TXF:136872, TXR:136872 | ok |
| 42EDC9 | Magnitud energía en bolsa nacional a cargo | Horaria | 1,228,176 | 0 | TX2:349344, TX3:177312, TXF:350760, TXR:350760 | ok |
| E14D70 | Magnitud ventas en bolsa nacional en energía | Horaria | 1,228,176 | 0 | TX2:349344, TX3:177312, TXF:350760, TXR:350760 | ok |
| D31647 | Precios en contratos de energía del Mercado Mayorista por comprador | Diaria | 28,249 | 0 | TX2:6886, TX3:7121, TXF:7121, TXR:7121 | ok |
| 8E7F3C | Generación ideal nacional por planta | Horaria | 4,010,016 | 0 | TX1:896928, TX2:897048, TX3:421080, TXF:897480, TXR:897480 | ok |
| catalogos | — | — | — | — | — | ERROR: sequence item 6: expected str instance, float found |

## Columnas por dataset

- **24914F**: Version, FechaInicio, FechaFin, FechaPublicacion, esMaximaVersion
- **0BFC9D**: Fecha, CodigoDuracion, FechaPublicacion, CodigoPlanta, NombrePlanta, CodigoSICAgente, CapEfectivaNeta, FPO, CodigoSubAreaOperativa, CodigoAreaOperativa, TipoDespachoRecurso, TipoClasificacion, TipoGeneracion
- **96D56E**: CodigoVariable, Fecha, CodigoDuracion, UnidadMedida, Version, Valor
- **D55202**: CodigoVariable, FechaHora, CodigoSICAgente, TipoMercado, Version, Valor, UnidadMedida, CodigoDuracion
- **42EDC9**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, Version, Valor
- **E14D70**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, Version, Valor
- **D31647**: Fecha, CodigoAgenteComprador, TipoMercado, Mecanismo, NormatividadRelacionada, Valor, Version, CodigoVariable
- **8E7F3C**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoPlanta, Version, Valor

## Candidatos en el catálogo (0)

