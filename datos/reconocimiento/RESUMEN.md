# Reconocimiento de fuentes

Ejecutado: 2026-10-25 01:25 UTC · fecha de referencia 2026-10-25

| ID | Dataset | Granularidad | Filas | Duplicadas | Versiones | Estado |
|---|---|---|---:|---:|---|---|
| 24914F | Versiones de factura para la liquidación mensual | Diaria | 47 | 0 | TX3:12, TX4:7, TX5:4, TXF:12, TXR:12 | ok |
| 0BFC9D | Parámetros técnicos de las plantas de generación | Diaria | 69,813 | 0 | — | ok |
| 972263 | Listado de agentes registrados | Diaria | 11,029 | 0 | — | ok |
| EC6945 | Precio de bolsa horario | Horaria | 19,800 | 0 | TX1:4392, TX2:4392, TX3:2232, TXF:4392, TXR:4392 | ok |
| 96D56E | Precio de bolsa ponderado | Diaria | 489 | 0 | TX1:61, TX2:122, TX3:62, TXF:122, TXR:122 | ok |
| D55202 | Demanda comercial nacional | Horaria | 479,808 | 0 | TX2:136872, TX3:69192, TXF:136872, TXR:136872 | ok |
| 42EDC9 | Magnitud energía en bolsa nacional a cargo | Horaria | 1,228,176 | 0 | TX2:349344, TX3:177312, TXF:350760, TXR:350760 | ok |
| E14D70 | Magnitud ventas en bolsa nacional en energía | Horaria | 1,228,176 | 0 | TX2:349344, TX3:177312, TXF:350760, TXR:350760 | ok |
| D31647 | Precios en contratos de energía del Mercado Mayorista por comprador | Diaria | 28,249 | 0 | TX2:6886, TX3:7121, TXF:7121, TXR:7121 | ok |
| C8381F | Cantidad de compra despachada en contratos de largo plazo en kWh | Horaria | 894,120 | 0 | TX2:255192, TX3:128496, TXF:255216, TXR:255216 | ok |
| E60CE2 | Venta en contratos bilaterales de largo plazo por vendedor en energía | Horaria | 1,185,696 | 0 | TX2:338832, TX3:169200, TXF:338832, TXR:338832 | ok |
| 43D616 | Precio de escasez ponderado | Diaria | 275 | 0 | TX1:61, TX2:61, TX3:31, TXF:61, TXR:61 | ok |
| BA1C55 | Aportes Hídricos en Energía | Diaria | 2,684 | 0 | — | ok |
| 8E7F3C | Generación ideal nacional por planta | Horaria | 4,010,016 | 0 | TX1:896928, TX2:897048, TX3:421080, TXF:897480, TXR:897480 | ok |
| datos.gov.co/ytme-6qnu | Tarifas y Costos de Energía Eléctrica para el Mercado Regulado (E.S.P. Empresas Públicas de Medellín - EPM, Antioquia) | — | 415 | 0 | — | ok |

## Columnas por dataset

- **24914F**: Version, FechaInicio, FechaFin, FechaPublicacion, esMaximaVersion
- **0BFC9D**: Fecha, CodigoDuracion, FechaPublicacion, CodigoPlanta, NombrePlanta, CodigoSICAgente, CapEfectivaNeta, FPO, CodigoSubAreaOperativa, CodigoAreaOperativa, TipoDespachoRecurso, TipoClasificacion, TipoGeneracion
- **972263**: Fecha, CodigoDuracion, CodigoSICAgente, NombreAgente, ActividadAgente
- **EC6945**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, Version, Valor
- **96D56E**: CodigoVariable, Fecha, CodigoDuracion, UnidadMedida, Version, Valor
- **D55202**: CodigoVariable, FechaHora, CodigoSICAgente, TipoMercado, Version, Valor, UnidadMedida, CodigoDuracion
- **42EDC9**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, Version, Valor
- **E14D70**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, Version, Valor
- **D31647**: Fecha, CodigoAgenteComprador, TipoMercado, Mecanismo, NormatividadRelacionada, Valor, Version, CodigoVariable
- **C8381F**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, TipoMercado, Version, Valor
- **E60CE2**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoSICAgente, TipoMercado, Version, Valor
- **43D616**: CodigoVariable, FechaInicio, CodigoDuracion, UnidadMedida, Version, Valor
- **BA1C55**: FechaPublicacion, Fecha, CodigoSerieHidrologica, RegionHidrologica, AportesHidricosEnergia, PromedioAcumuladoEnergia, MediaHistoricaEnergia
- **8E7F3C**: CodigoVariable, FechaHora, CodigoDuracion, UnidadMedida, CodigoPlanta, Version, Valor
- **datos.gov.co/ytme-6qnu**: a_o, periodo, operador_de_red, nivel, cu_total, costo_compra_gm_i, cargo_transporte_stn_tm, cargo_transporte_sdl_dn_m, margen_comercializaci_n_cvm, costo_g_t_p_rdidas_prn_m, restricciones_rm, cot, cfm_j_fact

## Candidatos en el catálogo (142)

- 2106b8 · Precios y estadísticas de los contratos de convocatorias del SICEP entre agentes integrados verticalmente para el mercado regulado por comercializador · 2023-09-30T10:35:01.19 · 2026-10-24T07:37:40.883
- 7AEE6F · Nivel embalse reportado menos compromisos EVE embalsados por planta · 2023-09-28T20:27:03.407 · 2026-10-24T06:42:21.813
- F3A83B · Estadísticas de contratos de Demanda Desconectable Voluntaria (DDV) · 2023-09-30T11:09:06.763 · 2026-10-24T08:25:05.76
- bf41fe · Histórico Posición abierta por contrato II Open interest II · 2025-03-10T23:00:12.1 · 2026-10-08T15:14:42.453
- ae3f23 · Precios de escasez del Cargo por Confiabilidad · 2023-09-25T23:36:51.263 · 2026-10-01T13:54:37.347
- 5106B9 · Declaración de respaldo horaria para cada planta y/o unidad · 2023-09-28T20:27:03.407 · 2026-10-24T06:34:58.167
- 8d3ccd · Proyección de embalse agregado de corto plazo · 2024-09-06T08:42:12.99 · 2026-10-18T19:18:11.053
- d31647 · Precios en contratos de energía del Mercado Mayorista por comprador · 2024-10-08T14:18:52.303 · 2026-10-24T06:36:06.613
- 0fa2ac · Datos soporte del proceso de Demandas por Recurso, versión y horaria · 2024-11-06T16:25:40.203 · 2026-06-11T21:22:50.337
- 8d10e6 · Proyecciones de las cantidades y precios en contratos de energía del Mercado Mayorista por comercializador · 2025-01-20T14:01:10.267 · 2026-10-01T19:31:50.98
- 0bfc9d · Parámetros técnicos de las plantas de generación · 2025-02-07T14:10:00.743 · 2026-10-24T11:23:30.43
- f138b6 · Aportes Hídricos en Caudal del Informe Diario · 2023-07-12T21:50:47.92 · 2026-10-24T08:30:10.66
- 972263 · Listado de agentes registrados · 2023-09-29T23:27:37.013 · 2026-10-24T08:20:26.46
- 969fbb · Cumplimiento de reporte de facturación entre agentes y usuarios del mercado no regulado · 2026-05-22T08:30:41.32 · 2026-10-19T03:19:17.637
- AB7D7F · Generación Ideal por planta · 2023-09-28T20:27:03.407 · 2026-10-24T06:53:03.12
- 0c5948 · Precios y estadísticas de los contratos de convocatorias del SICEP entre agentes integrados verticalmente para el mercado regulado · 2023-09-30T13:24:31.503 · 2026-10-24T07:36:54.587
- 48e773 · Precios futuros y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado · 2023-09-30T11:49:21.447 · 2026-10-02T08:17:57.317
- 7F18B1 · Listado de plantas de generación en pruebas · 2024-05-14T18:43:59.563 · 2026-10-23T08:31:27.383
- 86d298 · Proyecciones de energía de los contratos no realizados a través del SICEP con destino al mercado regulado por comercializador y contrato · 2023-09-29T16:12:29.493 · 2026-10-14T09:58:12.73
- A8F4C0 · Costo promedio ponderado en contratos de largo plazo MC · 2025-06-04T11:20:33.287 · 2026-10-24T06:41:57.123
- EEDA4A · Cantidad ventas en contratos del SICEP · 2025-06-04T09:15:17.89 · 2026-10-24T06:40:55.403
- 7b756b · Precios promedios horarios mensuales de contratos con UNR para el total del SIN · 2023-09-29T17:44:07.12 · 2026-10-21T08:29:00.207
- 75f675 · Aportes Energético Largo Plazo · 2023-10-11T09:04:06.687 · 2026-10-15T18:20:45.723
- A0CF2A · Listado de Embalses que sirven al Sistema Interconectado Nacional · 2024-02-03T16:29:38.633 · 2026-10-23T07:13:06.42
- 7e704d · Meteorología local en Plantas Solares · 2023-07-13T15:04:35.627 · 2026-10-24T07:23:12.16
- b08986 · Registro de contratos de usuarios no regulados y reporte de facturación · 2023-09-29T00:14:41.41 · 2026-10-02T07:12:58.54
- 5fc353 · Datos soporte del proceso de liquidación por Recurso, Tipo combustible, versión y mensual · 2023-09-28T22:28:52.387 · 2026-06-11T21:25:36.263
- 12c7fd · Generación Programada Redespacho por Planta · 2023-09-30T12:57:24.763 · 2026-10-24T07:26:22.057
- 178428 · Precios futuros y estadísticas de los contratos entre agentes · 2023-09-30T16:17:54.693 · 2026-10-02T08:24:32.803
- 60fed4 · Precios futuros y estadísticas de los contratos entre agentes por comercializador y generador · 2023-09-29T16:22:51.08 · 2026-10-02T08:25:22.833
- b1189f · Precio de oferta de la planta en el proceso del despacho ideal, en COP/kWh · 2023-09-29T06:03:49.34 · 2026-10-11T06:44:43.21
- 8F2AFC · Reconciliación negativa para plantas que no realizan AGC · 2023-09-28T20:27:03.407 · 2026-10-24T06:43:27.93
- FADED0 · Capacidad efectiva neta por planta en potencia · 2025-06-03T11:15:29.603 · 2026-10-24T07:03:23.51
- f21bd1 · Cantidades horarias de energía por comercializador de contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T13:18:02.727 · 2026-10-24T07:38:01.103
- 705468 · Estadísticas horarias de precios por comercializador de los contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T17:48:16.177 · 2026-10-24T07:38:27.05
- ac9492 · Precios futuros horarios mensuales de contratos con UNR para el total del SIN · 2023-09-29T09:01:20.01 · 2026-10-19T03:24:28.37
- 39726d · Bandera de parada de plantas · 2025-10-10T16:24:11.14 · 2026-10-24T06:41:02.503
- 1eee63 · Aportes Energético Mediano Plazo · 2023-10-09T19:37:22.45 · 2026-10-18T19:25:07.313
- 013220 · Precios y estadísticas mensuales de contratos entre agentes por generador · 2023-10-02T10:42:36.153 · 2026-10-24T07:42:11.97
- 15df39 · Proyecciones de energía de los contratos no realizados a través del SICEP con destino al mercado regulado por comercializador · 2023-09-29T16:14:11.113 · 2026-10-02T08:32:55.63
- a38a5c · Agentes MEM inscritos en el mecanismo Derivex · 2025-03-10T22:53:57.687 · 2026-10-08T15:14:03.763
- 61ccc8 · Precios horarios y estadísticas de los contratos entre agentes por generador · 2023-09-29T14:08:33.097 · 2026-10-24T07:38:57.78
- c10ec7 · Cobertura de la demanda de contratos realizados fuera del SICEP · 2023-09-28T22:58:37.917 · 2026-10-05T13:15:51.747
- 305a36 · Energía promedio de los contratos de convocatorias del SICEP con destino al mercado regulado del Sistema Interconectado Nacional · 2023-09-27T02:45:30.963 · 2026-10-24T07:41:12.2
- 9e2844 · Precios horarios y estadísticas de los contratos entre agentes por comercializador · 2023-09-29T11:49:51.217 · 2026-10-24T07:38:48.943
- f776db · Proyecciones de las cantidades en contratos de energía del Mercado Mayorista por comprador · 2026-05-11T10:55:21.57 · 2026-10-05T09:01:08.337
- 531ba3 · Informe anual de auditoría de costos de combustible para el cálculo del precio marginal de escasez · 2023-09-29T00:08:29.2 · 2026-05-20T16:47:31.277
- d0d746 · Pérdidas Energía Asignadas Agente · 2023-09-30T11:55:24.757 · 2026-10-24T06:37:04.373
- 06bb49 · Energía promedio mensual de contratos con UNR para el total del SIN · 2023-09-29T10:33:12.15 · 2026-10-20T20:16:17.19
- 926542 · AGC Planta oferta nacional · 2026-05-25T08:42:53.84 · 2026-10-23T10:14:16.943
- 5f4e97 · Precios promedios horarios mensuales por comercializador de contratos con UNR para el total del SIN · 2023-10-04T17:29:41.413 · 2026-10-21T08:28:47.2
- 5f246a · Precios horarios y estadísticas de los contratos entre agentes · 2023-10-04T18:54:35.76 · 2026-10-24T07:43:03.27
- 300D5C · Costo de operación y mantenimiento para el precio de escasez · 2025-07-07T11:08:26.243 · 2026-10-24T06:28:24.797
- 4f9fe7 · Precios horarios futuros y estadísticas de los contratos entre agentes · 2023-09-30T20:55:20.39 · 2026-10-02T08:21:30.173
- e5be73 · Precios horarios y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado · 2023-09-29T14:29:06.6 · 2026-10-24T07:39:41.193
- 6d9c07 · Proyecciones de precios de los contratos no realizados a través del SICEP con destino al mercado regulado por comercializador y contrato · 2023-09-29T17:40:45.37 · 2026-10-14T09:58:09.39
- 842296 · Energía calculada para plantas hidráulicas por reconciliación positiva asociada a la exportación hacia Ecuador · 2023-09-28T20:27:03.407 · 2026-10-24T06:36:27.14
- FB23CF · Valor contratos convocatorias públicas SICEP · 2025-06-04T09:15:19.95 · 2026-10-24T06:37:45.99
- f0be2a · Precios y estadísticas mensuales de contratos de convocatorias del SICEP para el mercado regulado por comercializador · 2023-09-30T10:31:00.427 · 2026-10-24T07:34:15.59
- 42f98c · Meteorología local en Plantas Eólicas · 2024-01-18T07:12:12.557 · 2026-10-24T07:20:59.09
- ec8596 · Aportes Hídricos en Porcentaje del Informe Diario · 2023-07-13T20:30:00.537 · 2026-10-24T08:30:12.39
- 629B6D · Oportunidad en la entrega de información por parte de los agentes de contratos largo plazo · 2024-05-16T16:02:07.16 · 2026-01-06T19:52:21.073
- 6bac48 · Precios y estadísticas de los contratos entre agentes integrados verticalmente para el mercado no regulado · 2023-09-30T15:57:42.133 · 2026-10-24T07:38:16.733
- a6dcc1 · Precios futuros mensuales de contratos con UNR por mercado de comercialización · 2023-09-29T09:59:00.523 · 2026-10-19T03:25:38.74
- d943d5 · Proyecciones de precios de los contratos no realizados a través del SICEP con destino al mercado regulado por comercializador · 2023-09-30T11:35:45.557 · 2026-10-02T08:19:38.093
- 69736c · Precios y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado, por año de suscripción · 2023-09-30T10:27:30.433 · 2026-10-24T07:40:07.423
- cebe60 · Precios y estadísticas mensuales de los contratos de convocatorias del SICEP para el mercado regulado · 2023-09-30T10:28:43.44 · 2026-10-24T07:36:55.413
- d528cb · Precios horarios y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado por comercializador · 2023-09-29T10:47:45.553 · 2026-10-24T07:40:53.15
- 2bff14 · Aportes Hídricos en Energía del Informe Diario de Operación · 2023-07-17T20:15:44.973 · 2026-10-24T08:30:12.04
- fbfafd · Precios y estadísticas mensuales de contratos entre agentes por comercializador · 2023-09-30T13:44:43.43 · 2026-10-24T07:43:53.5
- c0e18d · Estado de cobertura contractual de las fronteras del MNR durante los períodos de representación de los agentes · 2026-07-30T09:58:07.14 · 2026-10-24T06:17:25.787
- 379022 · Bandera de arranque Planta térmica para el Despacho Ideal · 2025-02-12T14:04:42.12 · 2026-10-24T06:48:17.433
- 40d2d3 · Estadísticas horarias de precios de los contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T16:22:04.163 · 2026-10-24T07:25:54.04
- 48eb33 · Valor acumulado bolsa de recursos a la fecha · 2026-10-06T13:59:53.333 · 2026-10-24T08:24:21.727
- 43D616 · Precio de escasez ponderado · 2025-03-07T16:09:33.467 · 2026-10-24T06:41:38.87
- 68a95b · Estadísticas de precios de los contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T15:59:16.633 · 2026-10-24T07:39:21.843
- 30a827 · Precios futuros mensuales de contratos con UNR para el total del SIN · 2023-09-29T09:11:24.397 · 2026-10-19T03:22:03.643
- F37316 · Magnitud de reconciliación positiva para plantas que prestan servicio de AGC · 2023-09-28T20:27:03.407 · 2026-10-24T06:38:46.997
- 2d5afe · Datos soporte del proceso de liquidación por Recurso, versión y horaria · 2023-09-28T20:27:03.407 · 2026-06-11T21:21:41.67
- 2a301d · Datos soporte del proceso de Despacho Ideal por Recurso, versión y horaria · 2024-06-28T14:57:09.533 · 2026-04-27T14:23:29.01
- bb4a0a · Precios y estadísticas mensuales de contratos entre agentes · 2023-09-30T11:11:22.53 · 2026-10-24T07:49:32.983
- b1ccc4 · Precios promedios mensuales de contratos con UNR por mercado de comercialización · 2023-09-29T18:01:51.973 · 2026-10-21T08:29:16.39
- 8E7F3C · Generación ideal nacional por planta · 2025-08-22T16:01:58.893 · 2026-10-24T06:50:35.4
- 560280 · Precios horarios futuros y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado por comercializador · 2023-10-06T00:00:42.34 · 2026-10-02T10:55:06.113
- 110a9e · Proyecciones de los precios en contratos de energía del Mercado Mayorista por vendedor · 2026-05-11T14:42:24.43 · 2026-10-05T09:04:45.763
- f09333 · --- Deprecated --- Datos soporte del proceso de liquidación por Código sic agente, Recurso, Unidad, versión y horaria · 2023-09-28T02:17:41.99 · 2026-09-10T13:19:18.923
- a51857 · Generación Real por Agente Comercializador · 2026-08-11T19:22:57.47 · 2026-10-24T08:21:12.973
- C8381F · Cantidad de compra despachada en contratos de largo plazo en kWh · 2025-06-04T09:16:10.08 · 2026-10-24T06:53:20.25
- B8EDC1 · Tarifa de aportes ley 99 de 1993 para plantas térmicas e hidráulicas · 2025-07-19T11:24:31.913 · 2026-08-26T21:09:07.233
- 7580FA · Participación en Convocatorias de Participación en Subasta de Cierre de agentes registrados · 2023-09-29T01:01:31.177 · 2026-10-08T15:11:44.907
- 51201b · Proyecciones de los precios en contratos de energía del Mercado Mayorista por comprador · 2026-05-11T14:38:38.143 · 2026-10-05T09:07:46.143
- ff027b · Despacho programado recursos de generación · 2023-09-30T10:52:26.017 · 2026-10-24T16:20:52.06
- ea45fe · Precios y estadísticas de los contratos entre agentes, agrupados por año de suscripción · 2023-09-30T09:44:00.963 · 2026-10-24T07:41:36.947
- 6B9E0C · Generación ideal internacional Venezuela por recurso planta · 2023-09-28T20:27:03.407 · 2026-10-24T06:59:57.953
- 860bc8 · Duración promedio de los contratos producto de convocatorias del SICEP para el mercado regulado · 2023-09-30T07:18:23.033 · 2026-10-05T13:18:10.997
- dac3c5 · Precios futuros y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado por comercializador · 2023-09-30T09:41:24.683 · 2026-10-02T08:24:55.53
- 42d664 · Cantidades de energía por comercializador de contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T13:04:16.843 · 2026-10-24T07:37:58.8
- 9a1b87 · Insumos para el Precio Marginal de Escasez · 2025-10-30T10:16:39.22 · 2026-10-24T06:50:39.423
- f9d42a · Precios horarios futuros y estadísticas de los contratos entre agentes por comercializador y generador · 2023-09-29T11:16:13.64 · 2026-10-02T08:24:21.47
- 1237df · Bandera de arranque de plantas · 2025-10-10T15:45:15.53 · 2026-10-24T06:49:05.45
- BD26DC · Nivel de embalse declarado por el agente diariamente · 2023-09-28T22:04:50.36 · 2026-10-24T06:49:36.84
- B53464 · Reconciliación negativa para planta que realiza AGC · 2023-09-28T20:27:03.407 · 2026-10-24T06:41:53.18
- 5f8082 · Precios promedios mensuales de contratos con UNR para el total del SIN · 2023-09-29T18:04:28.427 · 2026-10-21T08:18:50.783
- da2c83 · Estadísticas de precios por comercializador de los contratos adjudicados en subastas del Ministerio (MME) · 2023-09-18T17:17:33.267 · 2026-10-24T07:37:21.493
- 0810d0 · Cumplimiento de reporte de contratos entre agentes y usuarios del mercado no regulado · 2026-06-26T16:05:42.117 · 2026-10-19T03:14:51.8
- 9a387a · Porcentaje estimado de cobertura con contratos de convocatorias del SICEP para el mercado regulado · 2023-09-29T10:21:07.233 · 2026-10-05T13:16:50.31
- 34FFDA · Aportes Hídricos en Porcentaje · 2023-09-29T12:21:44.29 · 2026-10-24T08:22:56.407
- 90b78a · Porcentaje Estimado de cobertura con contratos entre agentes · 2023-09-29T09:41:31.13 · 2026-10-05T13:17:29.98
- d760bb · Precios y estadísticas de los contratos entre agentes, por año de suscripción y por comercializador · 2023-09-29T16:16:08.363 · 2026-10-24T07:43:44.013
- 8b732d · Duración promedio de los contratos entre agentes · 2023-09-30T07:32:56.903 · 2026-10-05T13:16:01.047
- cf0167 · Costo Restricciones Asignadas al Agente · 2023-09-26T08:53:41.753 · 2026-10-24T06:28:09.29
- 02B289 · Aportes Hídricos en Caudal · 2023-09-29T11:55:05.173 · 2026-10-24T08:31:47.94
- 086d86 · Energía promedio de los contratos entre agentes del Sistema Interconectado Nacional · 2023-09-28T17:44:50.007 · 2026-10-24T07:41:01.92
- 1cdd5f · Precios y estadísticas de los contratos entre agentes integrados verticalmente por generador · 2023-09-30T18:08:06.57 · 2026-10-24T07:38:33.757
- 48C79B · Precios de escasez promedio ponderado por agente · 2023-09-28T23:09:41.523 · 2026-10-24T06:43:44.61
- 909809 · Precio de Oferta de Arranque y Parada por recurso USD · 2023-09-29T18:04:08.527 · 2026-10-07T16:58:50.8
- c6f395 · Procedimiento de retiro de agentes según la Res. CREG 156 de 2011 · 2023-09-29T22:02:02.67 · 2026-10-24T07:12:03.13
- b73e3c · Energía promedio mensual de contratos con UNR por mercado de comercialización · 2023-09-30T16:28:19.18 · 2026-10-19T03:25:34.723
- 3cf0d1 · Precios horarios futuros y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado · 2023-09-30T11:37:18.793 · 2026-10-02T08:29:17.593
- e5437f · Precios promedios horarios mensuales por comercializador y mercado de comercialización de contratos con UNR · 2023-10-04T14:30:03.077 · 2026-10-21T08:15:46.063
- BA1C55 · Aportes Hídricos en Energía · 2023-09-29T12:08:14.157 · 2026-10-24T08:30:20.71
- E17D25 · Generación Real y Programada en las Plantas de Generación · 2023-09-29T10:59:40.38 · 2026-10-23T11:18:40.87
- b461cf · Tipo de Combustible con el que arrancó la planta · 2025-12-12T11:26:52.683 · 2026-10-24T06:42:07.98
- 58d1c7 · Proyecciones de las cantidades en contratos de energía del Mercado Mayorista por vendedor · 2026-05-11T11:30:39.87 · 2026-10-16T17:09:17.39
- 1e543e · Energía promedio de los contratos del SICEP para el mercado regulado por comercializador · 2023-09-28T21:14:22.5 · 2026-10-24T07:40:50.233
- 52341b · Precios y Energía de los contratos no realizados a través del SICEP con destino al mercado regulado · 2023-09-26T22:48:16.893 · 2026-10-24T07:44:40.087
- E60CE2 · Venta en contratos bilaterales de largo plazo por vendedor en energía · 2025-06-04T09:15:18.49 · 2026-10-24T06:47:29.137
- AE2DD3 · Promedio aritmético anual de la participación en Convocatorias de agentes registrados · 2023-09-29T13:16:05.353 · 2026-10-08T15:10:38.1
- 38a251 · Precios y estadísticas de los contratos entre agentes, por año de suscripción y por generador · 2023-09-29T18:32:09.887 · 2026-10-24T07:41:38.03
- CDD16E · Generación ideal internacional Ecuador por planta · 2023-09-28T20:27:03.407 · 2026-10-24T06:51:19.777
- d66c25 · Precios promedios horarios mensuales de contratos con UNR por mercado de comercialización · 2023-09-29T17:07:26.833 · 2026-10-21T08:25:04.11
- 781422 · Precios y estadísticas de los contratos entre agentes integrados verticalmente por comercializador · 2023-09-30T10:01:33.457 · 2026-10-24T07:43:26.86
- 331979 · Precios y estadísticas de los contratos de convocatorias del SICEP para el mercado regulado, por año de suscripción y por comercializador · 2023-09-29T16:21:42.3 · 2026-10-24T07:36:19.627
- b18005 · Precio de oferta de la planta para cada configuración ofertada en el proceso del despacho ideal, en COP/kWh · 2023-09-29T05:56:49.153 · 2026-10-24T06:41:44.653
- 8ae7da · Combustibles y Heat Rate de plantas térmicas del SIN · 2023-10-09T21:11:08.803 · 2026-10-24T09:19:03.12
- 05f977 · Precios futuros horarios mensuales de contratos con UNR por mercado de comercialización · 2023-09-29T08:02:36.687 · 2026-10-19T03:22:36.71
- 24F4EC · Disponibilidad comercial por planta · 2025-09-16T10:57:37.927 · 2026-10-24T06:54:32.267
- 9E77E5 · Disponibilidad real por planta · 2025-03-07T11:17:46.28 · 2026-10-24T07:04:10.943
- 1be05d · Precios y Energía de los contratos no realizados a través del SICEP que atienden el mercado de usuarios regulados · 2023-09-27T01:10:05.013 · 2026-10-24T07:44:13.397
- 230a9d · Registro de contratos de largo plazo entre agentes · 2023-09-29T00:12:51.487 · 2026-10-02T07:14:58.833
- 8DA3D8 · Magnitud de reconciliación positiva para plantas que no realizan AGC · 2023-09-28T20:27:03.407 · 2026-10-24T06:48:22.19
- 8DECCA · Estadísticas de contratos del mercado secundario · 2023-09-30T11:35:39.21 · 2026-10-24T08:27:56.033
