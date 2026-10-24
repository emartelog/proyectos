# Bitácora del dato maestro

Generado: 2026-10-24 18:50 UTC
Meses procesados: 2026-08, 2026-09

## Resumen del mercado

| Mes | Demanda | Exposición a bolsa | Precio bolsa (pond. compras) | Precio escasez | Aportes vs. media | Estado |
|---|---:|---:|---:|---:|---:|---|
| 2026-09 | 7,481.3 GWh | 18.9% | 706.7 COP/kWh | 891.4 COP/kWh | 65.5% | liquidado |
| 2026-08 | 7,608.9 GWh | 15.2% | 960.0 COP/kWh | 838.8 COP/kWh | 75.1% | liquidado |

## Controles de calidad

| Control | Nivel | Resultado | Detalle |
|---|---|---|---|
| unicidad:m_version | bloquea | ✅ | sin duplicados |
| unicidad:m_agente_diario | bloquea | ✅ | sin duplicados |
| unicidad:m_planta_diario | bloquea | ✅ | sin duplicados |
| unicidad:h_precio_bolsa_hora | bloquea | ✅ | sin duplicados |
| unicidad:h_precio_bolsa_dia | bloquea | ✅ | sin duplicados |
| unicidad:h_demanda | bloquea | ✅ | sin duplicados |
| unicidad:h_compra_bolsa | bloquea | ✅ | sin duplicados |
| unicidad:h_venta_bolsa | bloquea | ✅ | sin duplicados |
| unicidad:h_contrato_cantidad | bloquea | ✅ | sin duplicados |
| unicidad:h_contrato_venta | bloquea | ✅ | sin duplicados |
| unicidad:h_contrato_precio | bloquea | ✅ | sin duplicados |
| unicidad:h_escasez | bloquea | ✅ | sin duplicados |
| unicidad:h_aportes | bloquea | ✅ | sin duplicados |
| unicidad:h_generacion | bloquea | ✅ | sin duplicados |
| cobertura:h_precio_bolsa_hora:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-09 | bloquea | ✅ | 720/720 horas |
| balance:demanda+ventas=compras | advierte | ✅ | 2 de 130 agente-mes fuera de ±2%, con 0.0% de la demanda. De mayor demanda: SCEC 2026-08 (6.9%), SCEC 2026-09 (2.5%) |
| precio_bolsa:rango | advierte | ✅ | 0 horas fuera de [0, 3,000] COP/kWh |
| precio_bolsa:ppbo_reproducible | advierte | ✅ | 0 de 61 días con PPBO calculado ≠ publicado (±1%) |
| integridad:agentes | advierte | ✅ | 0 agentes de demanda sin maestro |
| integridad:plantas | advierte | ✅ | 187 plantas sin maestro, con 2.3% de la energía generada. Ej.: 2S8G, 2TYI, 2VJS, 2YB9, 2ZHY, 2ZP9, 3A44, 3ACC, 3AL6, 3B4L |
| contratos:cobertura_precio | advierte | ⚠️ | energía en contratos con precio por mes: 2026-08: 100.0%, 2026-09: 3.4%. XM publica los precios de contratos con rezago. |
| variacion:demanda_nacional | advierte | ✅ | sin meses atípicos |

## Estado de liquidación (calendario XM)

| Mes | Versión máxima | Última publicación |
|---|---|---|
| 2026-09 | TXF | 2026-10-10 |
| 2026-08 | TX3 | 2026-10-23 |

## Ingesta

| Dataset | Mes | Filas | Estado |
|---|---|---:|---|
| 24914F | 2026-08 | 3 | cargado |
| 24914F | 2026-09 | 2 | cargado |
| 972263 | 2026-08 | 11,407 | cargado |
| 972263 | 2026-09 | 11,029 | cargado |
| 0BFC9D | 2026-08 | 70,647 | cargado |
| 0BFC9D | 2026-09 | 69,813 | cargado |
| EC6945 | 2026-08 | 11,160 | cargado |
| EC6945 | 2026-09 | 8,640 | cargado |
| 96D56E | 2026-08 | 279 | cargado |
| 96D56E | 2026-09 | 210 | cargado |
| D55202 | 2026-08 | 276,768 | cargado |
| D55202 | 2026-09 | 203,040 | cargado |
| 42EDC9 | 2026-08 | 705,192 | cargado |
| 42EDC9 | 2026-09 | 520,008 | cargado |
| E14D70 | 2026-08 | 705,192 | cargado |
| E14D70 | 2026-09 | 520,008 | cargado |
| C8381F | 2026-08 | 516,816 | cargado |
| C8381F | 2026-09 | 380,136 | cargado |
| E60CE2 | 2026-08 | 690,792 | cargado |
| E60CE2 | 2026-09 | 508,896 | cargado |
| D31647 | 2026-08 | 28,898 | cargado |
| D31647 | 2026-09 | 233 | cargado |
| 43D616 | 2026-08 | 155 | cargado |
| 43D616 | 2026-09 | 120 | cargado |
| BA1C55 | 2026-08 | 1,364 | cargado |
| BA1C55 | 2026-09 | 1,320 | cargado |
| 8E7F3C | 2026-08 | 2,383,512 | cargado |
| 8E7F3C | 2026-09 | 1,904,616 | cargado |

## Histórico

- agg_exposicion_mensual: sin publicación anterior
- agg_mercado_mensual: sin publicación anterior
- agg_distribucion_exposicion: sin publicación anterior
