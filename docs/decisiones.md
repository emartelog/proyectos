# Decisiones de diseño

## 1. Las liquidaciones del MEM se revisan: el dato maestro guarda versiones

XM liquida cada día de operación varias veces: TX1/TX2 en los días siguientes, luego
TXR y TXF, y reliquidaciones posteriores (TX3 … TX10) semanas o meses después. Un mismo
(fecha, agente, variable) puede tener varios valores válidos según la versión.

**Implicación.** Una carga incremental del tipo "pedir desde la última fecha guardada"
nunca recoge las reliquidaciones de días ya descargados. Es el caso del script de ejemplo
del taller SIMEM–Power BI (nov. 2025). Por eso:

- Cada corrida mensual **reprocesa una ventana hacia atrás**, cuyo tamaño se fijará con el
  calendario oficial de versiones (dataset `24914F`).
- Los hechos se guardan con su **versión de liquidación y su fecha de captura**. Así se
  puede consultar el dato vigente o el que se conocía en una fecha dada.
- La "versión vigente" se determina con el orden oficial de versiones, no con la fecha
  de descarga.

## 2. Promedios ponderados, no simples

Los precios mensuales (bolsa y contratos) se calculan **ponderando por energía**: el costo
de compra en bolsa es la suma horaria de cantidad × precio. Promediar precios diarios, o el
precio de cada contrato sin ponderar por cantidad, sesga el costo cuando el consumo y el
precio se mueven juntos.

## 3. Variables separadas

`PPBO` (precio de bolsa) y `PPBOGReal` son variables distintas. Nunca se agregan juntas.

## 4. Fuentes por configuración

Cada dataset se registra en `config/fuentes.yml`. Agregar una fuente no requiere cambiar el
pipeline.

## 5. Reconocimiento antes de modelar

Antes de fijar el esquema del dato maestro, un workflow descarga muestras reales: el último
mes cerrado y un mes maduro con reliquidaciones. Las perfila (columnas, tipos, nulos,
duplicados y versiones presentes) y deja el resultado versionado en
`datos/reconocimiento/`.

## 6. Alcance del análisis

El análisis es de mercado y agregado, sin centrarse en agentes individuales.
