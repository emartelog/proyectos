# Propuesta: dato maestro y workflow mensual

Estado: **propuesta para revisión**. Se basa en el reconocimiento del 24-oct-2026
(`datos/reconocimiento/RESUMEN.md`), que cubrió 12 fuentes de SIMEM.

## 1. Pregunta que debe responder

> ¿Qué parte de la energía que compran los comercializadores se expone al precio de bolsa,
> cuánto cuesta esa exposición frente a los contratos y al precio de escasez, y cómo cambia
> con la hidrología?

Con nivel de detalle **comercializador × mes × mercado (regulado / no regulado)**, a partir de
datos horarios.

## 2. Dónde vive cada capa

```
                 ┌──────────────── PC de escritorio (o runner de GitHub) ────────────────┐
SIMEM (API) ───► │ crudo/        estandar/          maestro.duckdb                         │
                 │ (tal cual,    (tipado, formato   (maestros + hechos versionados          │
                 │  inmutable)    largo, versión)    + agregados mensuales)                 │
                 └──────────────────────────────────────────────┬──────────────────────────┘
                                                                │ solo agregados (MB)
                                                                ▼
                                      GitHub Release mensual  ──► Power BI / panel / notas
```

| Capa | Contenido | Tamaño estimado | Ubicación |
|---|---|---|---|
| `crudo/` | Respuesta de la API por dataset y ventana, con huella (hash) y fecha de captura | ~11 MB/mes (Parquet, medido en el reconocimiento) | PC (ruta configurable `RADAR_DATOS`) |
| `estandar/` | Mismo dato tipado, en formato largo y con columnas normalizadas | similar | PC |
| `maestro.duckdb` | Maestros, hechos versionados y agregados | < 1 GB en varios años | PC |
| Release mensual | Agregados mensuales + maestros (Parquet y CSV) + bitácora | < 5 MB por versión | GitHub |

El mismo paquete corre en el PC o en GitHub Actions. Solo cambia `RADAR_DATOS`. **Los datos
crudos nunca entran a git.**

## 3. Maestros

| Tabla | Fuente | Clave | Columnas principales | Historia |
|---|---|---|---|---|
| `dim_agente` | 972263 | `codigo_sic` | nombre, actividad (Generador, Comercializador, Distribuidor, Transportador) | SCD2: `vigente_desde` / `vigente_hasta` |
| `dim_planta` | 0BFC9D | `codigo_planta` | nombre, `codigo_sic` del agente, tipo de generación, clasificación, despacho, capacidad efectiva neta, área | SCD2 |
| `dim_version` | 24914F | `mes`, `version` | fecha de publicación, `es_maxima`, orden (TX1 < TX2 < TXR < TXF < TX3 … TX10) | Se reemplaza cada corrida (es el calendario oficial) |
| `dim_calendario` | generada | `fecha` | año, mes, día hábil/festivo (Colombia), hora | — |

**SCD2** quiere decir que un cambio no sobrescribe. Si una planta cambia de agente o de
capacidad, queda una fila nueva con su fecha de vigencia. Es la base para auditar.

## 4. Hechos (versionados)

Todas las tablas de hechos llevan `version` y `fecha_captura`. La clave natural más
`version` es única. Así se puede reconstruir cualquier mes "como se conocía" en una fecha
dada.

| Tabla | Fuente | Grano | Medida |
|---|---|---|---|
| `h_precio_bolsa_hora` | **EC6945** (nueva) | hora | `PB_Nal` (COP/kWh) |
| `h_precio_bolsa_dia` | 96D56E | día × variable | `PPBO` (ponderado con compras en bolsa), `PPBOGReal` (ponderado con generación real), **siempre separados** |
| `h_demanda` | D55202 | hora × agente × mercado | demanda comercial (kWh) |
| `h_compra_bolsa` | 42EDC9 | hora × agente | energía en bolsa a cargo (kWh) |
| `h_venta_bolsa` | E14D70 | hora × agente | ventas en bolsa (kWh) |
| `h_contrato_cantidad` | C8381F | hora × agente × mercado | compra despachada en contratos de largo plazo (kWh) |
| `h_contrato_precio` | D31647 | día × comprador × mercado × mecanismo | precio de contrato de largo plazo (COP/kWh) |
| `h_escasez` | 43D616 | día | precio de escasez ponderado |
| `h_aportes` | BA1C55 | día × región hidrológica | aportes (kWh), media histórica |
| `h_generacion` | 8E7F3C | hora × planta | generación ideal (kWh) |

**Vista vigente.** `v_<hecho>_vigente` toma, para cada mes, la versión marcada `es_maxima`
en `dim_version`. Los días sin versión mensual todavía (TX1/TX2) se marcan como
**preliminares**.

## 5. Agregado principal: `agg_exposicion_mensual`

Grano: **mes × comercializador × mercado**.

| Indicador | Cálculo |
|---|---|
| `demanda_kwh` | Σ demanda horaria |
| `contratos_kwh` | Σ compra en contratos |
| `bolsa_kwh` | Σ compra en bolsa |
| `exposicion_bolsa_pct` | bolsa_kwh / demanda_kwh |
| `costo_bolsa_cop` | Σ_h (compra bolsa_h × PB_Nal_h): **ponderado horario** |
| `precio_medio_bolsa` | costo_bolsa_cop / bolsa_kwh |
| `precio_medio_contrato` | precio de contrato ponderado por cantidad (ver nota) |
| `brecha_vs_escasez` | precio_medio_bolsa − precio de escasez del mes |
| `es_preliminar` | true si el mes aún no tiene versión TXR |

**Nota sobre el precio de contrato.** D31647 trae el precio por comprador, día, mercado y
mecanismo, pero sin cantidad. C8381F trae la cantidad por agente, hora y mercado, pero sin
mecanismo. Se cruzan en **agente × día × mercado**: si en un día hay varios mecanismos, se
usa el promedio de esos precios ponderado por la cantidad de ese día. Es una aproximación
y queda documentada así en las salidas.

**Además, agregados de contexto:** `agg_mercado_mensual` (totales nacionales, mezcla de
generación por tecnología, aportes frente a la media histórica) y `agg_distribucion_exposicion`
(cuántos comercializadores caen en cada rango de exposición: 0–10 %, 10–25 % …). Este
último es el que se publica en las notas, sin nombres.

## 6. Controles de calidad

| Control | Regla | Si falla |
|---|---|---|
| Esquema | Columnas y tipos esperados por dataset | **Bloquea** la publicación |
| Unicidad | Clave natural + versión sin duplicados | **Bloquea** |
| Cobertura | 24 horas por día y todos los días del mes en datasets horarios | Bloquea si el mes es TXR o posterior; advierte si es preliminar |
| Balance | demanda ≈ contratos + bolsa por agente y mes (tolerancia inicial 2 %, a calibrar) | Advierte y lista los agentes fuera de tolerancia |
| Mercados | regulado + no regulado = total por agente | Advierte |
| Precio | PB_Nal dentro de [0, 3.000] COP/kWh; PPBO diario ≈ ponderado de PB_Nal horario | Advierte |
| Variación | Cambio de un mes a otro > 3 desviaciones estándar en demanda nacional | Advierte |
| Rezago de contratos | El último mes de D31647 viene incompleto (233 filas en sep. vs. ~28.000 en may.) | Se marca preliminar; no bloquea |
| Integridad referencial | Todo agente o planta de los hechos existe en su maestro | Advierte y lista los huérfanos |

El balance demanda ≈ contratos + bolsa **no está verificado todavía**. Es una hipótesis que
el primer run confirmará o corregirá. La definición de D55202 incluye la participación en
pérdidas del STN y los consumos propios, así que puede haber diferencias sistemáticas.

## 7. Workflow mensual

**Cuándo:** el día **12 de cada mes**. XM publica TXF del mes anterior hacia el día 10, según
el calendario 24914F. También puede correrse a mano para un rango de meses.

**Ventana de reproceso:** los **10 meses anteriores**. TX5 aparece entre 8 y 9 meses después
del mes de operación. La ventana se recalcula leyendo `dim_version`: se reprocesa todo mes
cuya versión máxima cambió desde la última corrida. Normalmente son 3 o 4 meses, no 10.

```
1. versiones   → descargar 24914F; detectar meses con versión nueva
2. ingesta     → por dataset y mes afectado: descargar a crudo/ (con hash);
                 si el hash no cambió, saltar (idempotente)
3. estandar    → tipar, normalizar nombres, formato largo
4. maestros    → actualizar dim_agente y dim_planta (SCD2)
5. hechos      → upsert por (clave, versión)
6. calidad     → controles de la sección 6; si un control que bloquea falla, se detiene
7. agregados   → recalcular los meses afectados
8. publicación → Release "maestro-AAAA-MM" con agregados + maestros + bitácora.md
                 (meses revisados, versiones nuevas, alertas de calidad)
9. alerta      → si falla: issue en GitHub con el detalle (y correo de GitHub Actions)
```

**En el PC:** la misma secuencia con `python -m radar_energia.mensual`, programada con el
Programador de tareas (Windows) o cron (Linux/Mac). **En GitHub:** el workflow
`mensual.yml` como respaldo. Procesa en el runner y publica solo los agregados.

**Carga histórica inicial:** desde enero de 2021 (unos 70 meses, ~800 MB en crudo). Se corre
una sola vez en el PC.

## 8. Lo que queda abierto

1. Validar la regla de balance con el primer run real (sección 6).
2. Confirmar si C8381F y D31647 cruzan bien por código de agente: 152 frente a 149 agentes.
3. Evaluar la fuente de datos.gov.co `ytme-6qnu` (sin revisar: el dominio está bloqueado
   desde el entorno de desarrollo).
4. Sistema operativo del PC, para el instalador y la tarea programada.
