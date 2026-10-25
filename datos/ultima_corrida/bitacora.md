# Bitácora del dato maestro

Generado: 2026-10-24 20:53 UTC
Meses procesados: 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06, 2026-07, 2026-08, 2026-09

## Resumen del mercado

| Mes | Demanda | Exposición a bolsa | Precio bolsa (pond. compras) | Precio escasez | Aportes vs. media | Estado |
|---|---:|---:|---:|---:|---:|---|
| 2026-09 | 7,481.3 GWh | 18.9% | 706.7 COP/kWh | 891.4 COP/kWh | 65.5% | liquidado |
| 2026-08 | 7,608.9 GWh | 15.2% | 960.0 COP/kWh | 838.8 COP/kWh | 75.1% | liquidado |
| 2026-07 | 7,640.9 GWh | 14.3% | 812.9 COP/kWh | 929.1 COP/kWh | 79.0% | liquidado |
| 2026-06 | 7,247.6 GWh | 10.3% | 605.7 COP/kWh | 991.0 COP/kWh | 75.9% | liquidado |
| 2026-05 | 7,605.3 GWh | 11.8% | 549.8 COP/kWh | 1,006.0 COP/kWh | 75.5% | liquidado |
| 2026-04 | 7,166.5 GWh | 13.5% | 293.2 COP/kWh | 1,080.5 COP/kWh | 95.0% | liquidado |
| 2026-03 | 7,417.9 GWh | 16.6% | 229.2 COP/kWh | 803.7 COP/kWh | 110.3% | liquidado |
| 2026-02 | 6,551.2 GWh | 11.3% | 125.6 COP/kWh | 790.2 COP/kWh | 181.3% | liquidado |
| 2026-01 | 7,105.9 GWh | 9.9% | 218.6 COP/kWh | 798.8 COP/kWh | 139.2% | liquidado |
| 2025-12 | 7,145.9 GWh | 9.1% | 288.9 COP/kWh | 833.4 COP/kWh | 92.6% | liquidado |
| 2025-11 | 7,022.7 GWh | 8.3% | 238.0 COP/kWh | 806.0 COP/kWh | 85.6% | liquidado |
| 2025-10 | 7,158.1 GWh | 8.3% | 183.9 COP/kWh | 832.4 COP/kWh | 94.0% | liquidado |
| 2025-09 | 7,059.6 GWh | 10.3% | 318.6 COP/kWh | 868.9 COP/kWh | 95.3% | liquidado |

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
| cobertura:h_precio_bolsa_hora:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_precio_bolsa_hora:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_precio_bolsa_hora:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_precio_bolsa_hora:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_precio_bolsa_hora:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_demanda:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_demanda:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_demanda:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_demanda:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_compra_bolsa:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_compra_bolsa:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_compra_bolsa:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_compra_bolsa:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_venta_bolsa:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_venta_bolsa:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_venta_bolsa:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_venta_bolsa:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_contrato_cantidad:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_contrato_cantidad:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_cantidad:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_cantidad:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_contrato_venta:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_contrato_venta:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_contrato_venta:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_contrato_venta:2026-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2025-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_generacion:2025-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2025-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2025-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-09 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2025-10 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2025-11 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2025-12 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-01 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-02 | bloquea | ✅ | 672/672 horas |
| cobertura:h_generacion:2026-03 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-04 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2026-05 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-06 | bloquea | ✅ | 720/720 horas |
| cobertura:h_generacion:2026-07 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-08 | bloquea | ✅ | 744/744 horas |
| cobertura:h_generacion:2026-09 | bloquea | ✅ | 720/720 horas |
| balance:demanda+ventas=compras | advierte | ✅ | 7 de 1363 agente-mes fuera de ±2%, con 0.0% de la demanda |
| precio_bolsa:rango | advierte | ✅ | 0 horas fuera de [0, 3,000] COP/kWh |
| precio_bolsa:ppbo_reproducible | advierte | ✅ | 0 de 638 días con PPBO calculado ≠ publicado (±1%) |
| integridad:agentes | advierte | ✅ | 0 agentes de demanda sin maestro |
| integridad:plantas | advierte | ✅ | 123 plantas sin maestro, con 0.6% de la energía generada. Ej.: 2S8G, 2YB9, 3EE4, 3EXH, 3H2U, 3PKH, 3PKN, 3PXJ, 4QPJ, 4SO6 |
| contratos:cobertura_precio | advierte | ⚠️ | energía en contratos con precio por mes: 2025-01: 100.0%, 2025-02: 100.0%, 2025-03: 100.0%, 2025-04: 100.0%, 2025-05: 100.0%, 2025-06: 100.0%, 2025-07: 100.0%, 2025-08: 100.0%, 2025-09: 100.0%, 2025-10: 100.0%, 2025-11: 100.0%, 2025-12: 100.0%, 2026-01: 100.0%, 2026-02: 100.0%, 2026-03: 100.0%, 2026-04: 100.0%, 2026-05: 100.0%, 2026-06: 100.0%, 2026-07: 100.0%, 2026-08: 100.0%, 2026-09: 3.4%. XM publica los precios de contratos con rezago. |
| variacion:demanda_nacional | advierte | ✅ | sin meses atípicos |

## Estado de liquidación (calendario XM)

| Mes | Versión máxima | Última publicación |
|---|---|---|
| 2026-09 | TXF | 2026-10-10 |
| 2026-08 | TX3 | 2026-10-23 |
| 2026-07 | TX3 | 2026-09-23 |
| 2026-06 | TX3 | 2026-08-24 |
| 2026-05 | TX3 | 2026-07-09 |
| 2026-04 | TX4 | 2026-10-23 |
| 2026-03 | TX4 | 2026-09-22 |
| 2026-02 | TX5 | 2026-10-22 |
| 2026-01 | TX5 | 2026-09-22 |
| 2025-12 | TX5 | 2026-08-08 |
| 2025-11 | TX5 | 2026-07-01 |
| 2025-10 | TX4 | 2026-04-23 |
| 2025-09 | TX4 | 2026-03-22 |

## Ingesta

| Dataset | Mes | Filas | Estado |
|---|---|---:|---|
| 24914F | 2025-01 | 4 | cargado |
| 24914F | 2025-02 | 5 | cargado |
| 24914F | 2025-03 | 4 | cargado |
| 24914F | 2025-04 | 5 | cargado |
| 24914F | 2025-05 | 4 | cargado |
| 24914F | 2025-06 | 3 | cargado |
| 24914F | 2025-07 | 5 | cargado |
| 24914F | 2025-08 | 4 | cargado |
| 24914F | 2025-09 | 4 | cargado |
| 24914F | 2025-10 | 4 | cargado |
| 24914F | 2025-11 | 5 | cargado |
| 24914F | 2025-12 | 5 | cargado |
| 24914F | 2026-01 | 5 | cargado |
| 24914F | 2026-02 | 5 | cargado |
| 24914F | 2026-03 | 4 | cargado |
| 24914F | 2026-04 | 4 | cargado |
| 24914F | 2026-05 | 3 | cargado |
| 24914F | 2026-06 | 4 | cargado |
| 24914F | 2026-07 | 3 | cargado |
| 24914F | 2026-08 | 3 | cargado |
| 24914F | 2026-09 | 2 | cargado |
| 972263 | 2025-01 | 10,085 | cargado |
| 972263 | 2025-02 | 9,170 | cargado |
| 972263 | 2025-03 | 10,168 | cargado |
| 972263 | 2025-04 | 9,812 | cargado |
| 972263 | 2025-05 | 10,191 | cargado |
| 972263 | 2025-06 | 9,936 | cargado |
| 972263 | 2025-07 | 10,372 | cargado |
| 972263 | 2025-08 | 10,580 | cargado |
| 972263 | 2025-09 | 10,444 | cargado |
| 972263 | 2025-10 | 10,976 | cargado |
| 972263 | 2025-11 | 10,715 | cargado |
| 972263 | 2025-12 | 11,173 | cargado |
| 972263 | 2026-01 | 11,160 | cargado |
| 972263 | 2026-02 | 10,080 | cargado |
| 972263 | 2026-03 | 11,129 | cargado |
| 972263 | 2026-04 | 10,846 | cargado |
| 972263 | 2026-05 | 11,331 | cargado |
| 972263 | 2026-06 | 10,985 | cargado |
| 972263 | 2026-07 | 11,339 | cargado |
| 972263 | 2026-08 | 11,407 | cargado |
| 972263 | 2026-09 | 11,029 | cargado |
| 0BFC9D | 2025-01 | 35,064 | cargado |
| 0BFC9D | 2025-02 | 33,211 | cargado |
| 0BFC9D | 2025-03 | 37,480 | cargado |
| 0BFC9D | 2025-04 | 38,051 | cargado |
| 0BFC9D | 2025-05 | 40,659 | cargado |
| 0BFC9D | 2025-06 | 40,378 | cargado |
| 0BFC9D | 2025-07 | 43,772 | cargado |
| 0BFC9D | 2025-08 | 45,323 | cargado |
| 0BFC9D | 2025-09 | 45,458 | cargado |
| 0BFC9D | 2025-10 | 49,111 | cargado |
| 0BFC9D | 2025-11 | 49,757 | cargado |
| 0BFC9D | 2025-12 | 53,413 | cargado |
| 0BFC9D | 2026-01 | 55,642 | cargado |
| 0BFC9D | 2026-02 | 52,228 | cargado |
| 0BFC9D | 2026-03 | 60,675 | cargado |
| 0BFC9D | 2026-04 | 60,567 | cargado |
| 0BFC9D | 2026-05 | 64,314 | cargado |
| 0BFC9D | 2026-06 | 64,424 | cargado |
| 0BFC9D | 2026-07 | 68,792 | cargado |
| 0BFC9D | 2026-08 | 70,647 | cargado |
| 0BFC9D | 2026-09 | 69,813 | cargado |
| EC6945 | 2025-01 | 13,248 | cargado |
| EC6945 | 2025-02 | 11,952 | cargado |
| EC6945 | 2025-03 | 13,248 | cargado |
| EC6945 | 2025-04 | 14,976 | cargado |
| EC6945 | 2025-05 | 13,248 | cargado |
| EC6945 | 2025-06 | 10,656 | cargado |
| EC6945 | 2025-07 | 15,480 | cargado |
| EC6945 | 2025-08 | 13,224 | cargado |
| EC6945 | 2025-09 | 12,816 | cargado |
| EC6945 | 2025-10 | 13,248 | cargado |
| EC6945 | 2025-11 | 15,120 | cargado |
| EC6945 | 2025-12 | 15,624 | cargado |
| EC6945 | 2026-01 | 15,624 | cargado |
| EC6945 | 2026-02 | 14,112 | cargado |
| EC6945 | 2026-03 | 13,392 | cargado |
| EC6945 | 2026-04 | 12,960 | cargado |
| EC6945 | 2026-05 | 11,160 | cargado |
| EC6945 | 2026-06 | 10,728 | cargado |
| EC6945 | 2026-07 | 11,088 | cargado |
| EC6945 | 2026-08 | 11,160 | cargado |
| EC6945 | 2026-09 | 8,640 | cargado |
| 96D56E | 2025-01 | 273 | cargado |
| 96D56E | 2025-02 | 252 | cargado |
| 96D56E | 2025-03 | 275 | cargado |
| 96D56E | 2025-04 | 208 | cargado |
| 96D56E | 2025-05 | 327 | cargado |
| 96D56E | 2025-06 | 267 | cargado |
| 96D56E | 2025-07 | 335 | cargado |
| 96D56E | 2025-08 | 341 | cargado |
| 96D56E | 2025-09 | 327 | cargado |
| 96D56E | 2025-10 | 334 | cargado |
| 96D56E | 2025-11 | 327 | cargado |
| 96D56E | 2025-12 | 403 | cargado |
| 96D56E | 2026-01 | 403 | cargado |
| 96D56E | 2026-02 | 364 | cargado |
| 96D56E | 2026-03 | 341 | cargado |
| 96D56E | 2026-04 | 330 | cargado |
| 96D56E | 2026-05 | 279 | cargado |
| 96D56E | 2026-06 | 268 | cargado |
| 96D56E | 2026-07 | 278 | cargado |
| 96D56E | 2026-08 | 279 | cargado |
| 96D56E | 2026-09 | 210 | cargado |
| D55202 | 2025-01 | 326,808 | cargado |
| D55202 | 2025-02 | 297,240 | cargado |
| D55202 | 2025-03 | 333,552 | cargado |
| D55202 | 2025-04 | 388,752 | cargado |
| D55202 | 2025-05 | 266,448 | cargado |
| D55202 | 2025-06 | 257,712 | cargado |
| D55202 | 2025-07 | 334,152 | cargado |
| D55202 | 2025-08 | 337,824 | cargado |
| D55202 | 2025-09 | 326,784 | cargado |
| D55202 | 2025-10 | 269,376 | cargado |
| D55202 | 2025-11 | 331,200 | cargado |
| D55202 | 2025-12 | 410,688 | cargado |
| D55202 | 2026-01 | 342,240 | cargado |
| D55202 | 2026-02 | 309,120 | cargado |
| D55202 | 2026-03 | 343,800 | cargado |
| D55202 | 2026-04 | 267,840 | cargado |
| D55202 | 2026-05 | 276,768 | cargado |
| D55202 | 2026-06 | 265,608 | cargado |
| D55202 | 2026-07 | 276,768 | cargado |
| D55202 | 2026-08 | 276,768 | cargado |
| D55202 | 2026-09 | 203,040 | cargado |
| 42EDC9 | 2025-01 | 785,496 | cargado |
| 42EDC9 | 2025-02 | 717,264 | cargado |
| 42EDC9 | 2025-03 | 805,200 | cargado |
| 42EDC9 | 2025-04 | 918,768 | cargado |
| 42EDC9 | 2025-05 | 790,032 | cargado |
| 42EDC9 | 2025-06 | 621,912 | cargado |
| 42EDC9 | 2025-07 | 794,904 | cargado |
| 42EDC9 | 2025-08 | 800,352 | cargado |
| 42EDC9 | 2025-09 | 787,608 | cargado |
| 42EDC9 | 2025-10 | 828,480 | cargado |
| 42EDC9 | 2025-11 | 816,336 | cargado |
| 42EDC9 | 2025-12 | 1,027,440 | cargado |
| 42EDC9 | 2026-01 | 1,041,792 | cargado |
| 42EDC9 | 2026-02 | 947,328 | cargado |
| 42EDC9 | 2026-03 | 873,192 | cargado |
| 42EDC9 | 2026-04 | 852,576 | cargado |
| 42EDC9 | 2026-05 | 708,168 | cargado |
| 42EDC9 | 2026-06 | 692,280 | cargado |
| 42EDC9 | 2026-07 | 703,128 | cargado |
| 42EDC9 | 2026-08 | 705,192 | cargado |
| 42EDC9 | 2026-09 | 520,008 | cargado |
| E14D70 | 2025-01 | 785,496 | cargado |
| E14D70 | 2025-02 | 717,264 | cargado |
| E14D70 | 2025-03 | 805,200 | cargado |
| E14D70 | 2025-04 | 918,768 | cargado |
| E14D70 | 2025-05 | 790,032 | cargado |
| E14D70 | 2025-06 | 621,912 | cargado |
| E14D70 | 2025-07 | 794,904 | cargado |
| E14D70 | 2025-08 | 800,352 | cargado |
| E14D70 | 2025-09 | 787,608 | cargado |
| E14D70 | 2025-10 | 828,480 | cargado |
| E14D70 | 2025-11 | 816,336 | cargado |
| E14D70 | 2025-12 | 1,027,440 | cargado |
| E14D70 | 2026-01 | 1,041,792 | cargado |
| E14D70 | 2026-02 | 788,544 | cargado |
| E14D70 | 2026-03 | 873,192 | cargado |
| E14D70 | 2026-04 | 852,576 | cargado |
| E14D70 | 2026-05 | 708,168 | cargado |
| E14D70 | 2026-06 | 692,280 | cargado |
| E14D70 | 2026-07 | 703,128 | cargado |
| E14D70 | 2026-08 | 705,192 | cargado |
| E14D70 | 2026-09 | 520,008 | cargado |
| C8381F | 2025-01 | 590,976 | cargado |
| C8381F | 2025-02 | 537,096 | cargado |
| C8381F | 2025-03 | 601,704 | cargado |
| C8381F | 2025-04 | 576,120 | cargado |
| C8381F | 2025-05 | 475,272 | cargado |
| C8381F | 2025-06 | 463,680 | cargado |
| C8381F | 2025-07 | 599,256 | cargado |
| C8381F | 2025-08 | 598,584 | cargado |
| C8381F | 2025-09 | 596,280 | cargado |
| C8381F | 2025-10 | 622,200 | cargado |
| C8381F | 2025-11 | 604,200 | cargado |
| C8381F | 2025-12 | 757,296 | cargado |
| C8381F | 2026-01 | 744,336 | cargado |
| C8381F | 2026-02 | 575,400 | cargado |
| C8381F | 2026-03 | 633,912 | cargado |
| C8381F | 2026-04 | 615,000 | cargado |
| C8381F | 2026-05 | 513,984 | cargado |
| C8381F | 2026-06 | 511,032 | cargado |
| C8381F | 2026-07 | 523,800 | cargado |
| C8381F | 2026-08 | 516,816 | cargado |
| C8381F | 2026-09 | 380,136 | cargado |
| E60CE2 | 2025-01 | 722,784 | cargado |
| E60CE2 | 2025-02 | 661,824 | cargado |
| E60CE2 | 2025-03 | 296,112 | cargado |
| E60CE2 | 2025-04 | 144,864 | cargado |
| E60CE2 | 2025-05 | 664,176 | cargado |
| E60CE2 | 2025-06 | 578,592 | cargado |
| E60CE2 | 2025-07 | 736,800 | cargado |
| E60CE2 | 2025-08 | 446,328 | cargado |
| E60CE2 | 2025-09 | 292,944 | cargado |
| E60CE2 | 2025-10 | 462,312 | cargado |
| E60CE2 | 2025-11 | 457,056 | cargado |
| E60CE2 | 2025-12 | 967,680 | cargado |
| E60CE2 | 2026-01 | 961,488 | cargado |
| E60CE2 | 2026-02 | 902,448 | cargado |
| E60CE2 | 2026-03 | 837,192 | cargado |
| E60CE2 | 2026-04 | 812,160 | cargado |
| E60CE2 | 2026-05 | 676,800 | cargado |
| E60CE2 | 2026-06 | 669,624 | cargado |
| E60CE2 | 2026-07 | 694,608 | cargado |
| E60CE2 | 2026-08 | 690,792 | cargado |
| E60CE2 | 2026-09 | 508,896 | cargado |
| D31647 | 2025-01 | 29,012 | cargado |
| D31647 | 2025-02 | 26,608 | cargado |
| D31647 | 2025-03 | 29,224 | cargado |
| D31647 | 2025-04 | 28,324 | cargado |
| D31647 | 2025-05 | 36,735 | cargado |
| D31647 | 2025-06 | 21,330 | cargado |
| D31647 | 2025-07 | 29,629 | cargado |
| D31647 | 2025-08 | 29,949 | cargado |
| D31647 | 2025-09 | 29,086 | cargado |
| D31647 | 2025-10 | 30,258 | cargado |
| D31647 | 2025-11 | 29,516 | cargado |
| D31647 | 2025-12 | 30,336 | cargado |
| D31647 | 2026-01 | 28,984 | cargado |
| D31647 | 2026-02 | 33,355 | cargado |
| D31647 | 2026-03 | 28,217 | cargado |
| D31647 | 2026-04 | 34,175 | cargado |
| D31647 | 2026-05 | 28,016 | cargado |
| D31647 | 2026-06 | 27,545 | cargado |
| D31647 | 2026-07 | 17,303 | cargado |
| D31647 | 2026-08 | 28,898 | cargado |
| D31647 | 2026-09 | 233 | cargado |
| 43D616 | 2025-01 | 62 | cargado |
| 43D616 | 2025-02 | 56 | cargado |
| 43D616 | 2025-03 | 62 | cargado |
| 43D616 | 2025-04 | 60 | cargado |
| 43D616 | 2025-05 | 93 | cargado |
| 43D616 | 2025-06 | 135 | cargado |
| 43D616 | 2025-07 | 183 | cargado |
| 43D616 | 2025-08 | 186 | cargado |
| 43D616 | 2025-09 | 173 | cargado |
| 43D616 | 2025-10 | 186 | cargado |
| 43D616 | 2025-11 | 177 | cargado |
| 43D616 | 2025-12 | 217 | cargado |
| 43D616 | 2026-01 | 217 | cargado |
| 43D616 | 2026-02 | 196 | cargado |
| 43D616 | 2026-03 | 186 | cargado |
| 43D616 | 2026-04 | 180 | cargado |
| 43D616 | 2026-05 | 155 | cargado |
| 43D616 | 2026-06 | 149 | cargado |
| 43D616 | 2026-07 | 154 | cargado |
| 43D616 | 2026-08 | 155 | cargado |
| 43D616 | 2026-09 | 120 | cargado |
| BA1C55 | 2025-01 | 1,395 | cargado |
| BA1C55 | 2025-02 | 1,260 | cargado |
| BA1C55 | 2025-03 | 1,395 | cargado |
| BA1C55 | 2025-04 | 1,350 | cargado |
| BA1C55 | 2025-05 | 1,395 | cargado |
| BA1C55 | 2025-06 | 1,350 | cargado |
| BA1C55 | 2025-07 | 1,364 | cargado |
| BA1C55 | 2025-08 | 1,364 | cargado |
| BA1C55 | 2025-09 | 1,320 | cargado |
| BA1C55 | 2025-10 | 1,364 | cargado |
| BA1C55 | 2025-11 | 1,320 | cargado |
| BA1C55 | 2025-12 | 1,364 | cargado |
| BA1C55 | 2026-01 | 1,364 | cargado |
| BA1C55 | 2026-02 | 1,232 | cargado |
| BA1C55 | 2026-03 | 1,364 | cargado |
| BA1C55 | 2026-04 | 1,320 | cargado |
| BA1C55 | 2026-05 | 1,364 | cargado |
| BA1C55 | 2026-06 | 1,320 | cargado |
| BA1C55 | 2026-07 | 1,363 | cargado |
| BA1C55 | 2026-08 | 1,364 | cargado |
| BA1C55 | 2026-09 | 1,320 | cargado |
| 8E7F3C | 2025-01 | 1,643,616 | cargado |
| 8E7F3C | 2025-02 | 1,524,552 | cargado |
| 8E7F3C | 2025-03 | 1,717,632 | cargado |
| 8E7F3C | 2025-04 | 1,961,856 | cargado |
| 8E7F3C | 2025-05 | 1,743,192 | cargado |
| 8E7F3C | 2025-06 | 1,436,856 | cargado |
| 8E7F3C | 2025-07 | 1,844,760 | cargado |
| 8E7F3C | 2025-08 | 1,881,216 | cargado |
| 8E7F3C | 2025-09 | 1,857,984 | cargado |
| 8E7F3C | 2025-10 | 1,976,640 | cargado |
| 8E7F3C | 2025-11 | 1,988,712 | cargado |
| 8E7F3C | 2025-12 | 2,151,480 | cargado |
| 8E7F3C | 2026-01 | 2,640,408 | cargado |
| 8E7F3C | 2026-02 | 2,094,216 | cargado |
| 8E7F3C | 2026-03 | 2,382,816 | cargado |
| 8E7F3C | 2026-04 | 2,377,128 | cargado |
| 8E7F3C | 2026-05 | 2,105,400 | cargado |
| 8E7F3C | 2026-06 | 2,123,208 | cargado |
| 8E7F3C | 2026-07 | 2,266,368 | cargado |
| 8E7F3C | 2026-08 | 2,383,512 | cargado |
| 8E7F3C | 2026-09 | 1,904,616 | cargado |

## Histórico

- agg_exposicion_mensual: 2998 filas históricas conservadas
- agg_mercado_mensual: 48 filas históricas conservadas
- agg_distribucion_exposicion: 271 filas históricas conservadas
