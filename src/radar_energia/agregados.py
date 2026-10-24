"""Agregados mensuales del dato maestro, calculados en SQL sobre las vistas vigentes.

Reglas de cálculo (ver docs/modelo-dato-maestro.md):
- El costo en bolsa se calcula hora a hora: Σ (compra en bolsa_h × precio de bolsa_h).
- El precio de contrato se pondera por energía. D31647 trae el precio por día y mecanismo,
  sin cantidad. C8381F trae la cantidad por hora, sin mecanismo. Por eso se toma el precio
  medio del día (promedio simple entre mecanismos) y se pondera con la cantidad de ese día.
- La compra en bolsa no viene separada por mercado. La porción regulada se reporta como
  "implícita" (demanda regulada − contratos regulados), nunca como dato observado.
- Varios comercializadores también revenden energía. Su balance es
  demanda + ventas (contratos y bolsa) = compras (contratos y bolsa), y la exposición de su
  demanda se mide con la posición neta en bolsa: max(compras − ventas en bolsa, 0) / demanda.
"""

from __future__ import annotations

import duckdb

VARIABLE_PRECIO_BOLSA = "PB_Nal"
RANGOS_EXPOSICION = [0, 0.10, 0.25, 0.50, 0.75, 1.0001]

SQL_EXPOSICION = f"""
CREATE OR REPLACE TABLE agg_exposicion_mensual AS
WITH precio AS (
    SELECT fecha_hora, precio_cop_kwh FROM v_precio_bolsa_hora
    WHERE variable = '{VARIABLE_PRECIO_BOLSA}'
),
demanda AS (
    SELECT date_trunc('month', fecha_hora)::DATE AS mes, agente,
           sum(kwh) AS demanda_kwh,
           sum(kwh) FILTER (WHERE mercado = 'Regulado') AS demanda_regulada_kwh,
           bool_or(es_preliminar) AS es_preliminar
    FROM v_demanda GROUP BY ALL
),
venta_bolsa AS (
    SELECT date_trunc('month', fecha_hora)::DATE AS mes, agente, sum(kwh) AS ventas_bolsa_kwh
    FROM v_venta_bolsa GROUP BY ALL
),
venta_contratos AS (
    SELECT date_trunc('month', fecha_hora)::DATE AS mes, agente,
           sum(kwh) AS ventas_contratos_kwh
    FROM v_contrato_venta GROUP BY ALL
),
bolsa AS (
    SELECT date_trunc('month', b.fecha_hora)::DATE AS mes, b.agente,
           sum(b.kwh) AS bolsa_kwh,
           sum(b.kwh * p.precio_cop_kwh) AS costo_bolsa_cop,
           sum(b.kwh) FILTER (WHERE p.precio_cop_kwh IS NULL) AS bolsa_sin_precio_kwh
    FROM v_compra_bolsa b LEFT JOIN precio p USING (fecha_hora)
    GROUP BY ALL
),
contrato_dia AS (
    SELECT fecha_hora::DATE AS fecha, agente, mercado, sum(kwh) AS kwh
    FROM v_contrato_cantidad GROUP BY ALL
),
precio_contrato_dia AS (
    SELECT fecha, agente, mercado, avg(precio_cop_kwh) AS precio_cop_kwh
    FROM v_contrato_precio WHERE precio_cop_kwh > 0 GROUP BY ALL
),
contratos AS (
    SELECT date_trunc('month', c.fecha)::DATE AS mes, c.agente,
           sum(c.kwh) AS contratos_kwh,
           sum(c.kwh) FILTER (WHERE c.mercado = 'Regulado') AS contratos_regulado_kwh,
           sum(c.kwh * p.precio_cop_kwh) AS costo_contratos_cop,
           sum(c.kwh) FILTER (WHERE p.precio_cop_kwh IS NOT NULL) AS contratos_con_precio_kwh
    FROM contrato_dia c LEFT JOIN precio_contrato_dia p USING (fecha, agente, mercado)
    GROUP BY ALL
),
escasez AS (
    SELECT date_trunc('month', fecha)::DATE AS mes, avg(precio_cop_kwh) AS precio_escasez
    FROM v_escasez GROUP BY ALL
),
agentes AS (
    SELECT agente, arg_max(nombre, vigente_hasta) AS nombre_agente
    FROM dim_agente GROUP BY agente
)
SELECT d.mes, d.agente, a.nombre_agente,
       d.demanda_kwh,
       coalesce(d.demanda_regulada_kwh, 0) AS demanda_regulada_kwh,
       coalesce(c.contratos_kwh, 0) AS contratos_kwh,
       coalesce(c.contratos_regulado_kwh, 0) AS contratos_regulado_kwh,
       coalesce(b.bolsa_kwh, 0) AS bolsa_kwh,
       coalesce(vc.ventas_contratos_kwh, 0) AS ventas_contratos_kwh,
       coalesce(vb.ventas_bolsa_kwh, 0) AS ventas_bolsa_kwh,
       coalesce(b.bolsa_kwh, 0) - coalesce(vb.ventas_bolsa_kwh, 0) AS bolsa_neta_kwh,
       greatest(coalesce(b.bolsa_kwh, 0) - coalesce(vb.ventas_bolsa_kwh, 0), 0)
           / nullif(d.demanda_kwh, 0) AS exposicion_bolsa_pct,
       coalesce(vc.ventas_contratos_kwh, 0) + coalesce(vb.ventas_bolsa_kwh, 0)
           > 0.05 * d.demanda_kwh
           AS revende_energia,
       greatest(coalesce(d.demanda_regulada_kwh, 0) - coalesce(c.contratos_regulado_kwh, 0), 0)
           / nullif(d.demanda_regulada_kwh, 0) AS exposicion_regulada_implicita_pct,
       b.costo_bolsa_cop,
       b.costo_bolsa_cop / nullif(b.bolsa_kwh, 0) AS precio_medio_bolsa,
       c.costo_contratos_cop,
       c.costo_contratos_cop / nullif(c.contratos_con_precio_kwh, 0) AS precio_medio_contrato,
       c.contratos_con_precio_kwh / nullif(c.contratos_kwh, 0) AS cobertura_precio_contrato_pct,
       e.precio_escasez,
       b.costo_bolsa_cop / nullif(b.bolsa_kwh, 0) - e.precio_escasez AS brecha_vs_escasez,
       coalesce(b.bolsa_sin_precio_kwh, 0) AS bolsa_sin_precio_kwh,
       d.es_preliminar OR coalesce(l.es_preliminar, true) AS es_preliminar
FROM demanda d
LEFT JOIN bolsa b USING (mes, agente)
LEFT JOIN contratos c USING (mes, agente)
LEFT JOIN venta_contratos vc USING (mes, agente)
LEFT JOIN venta_bolsa vb USING (mes, agente)
LEFT JOIN escasez e USING (mes)
LEFT JOIN agentes a USING (agente)
LEFT JOIN dim_mes_liquidacion l USING (mes)
WHERE d.demanda_kwh > 0
ORDER BY d.mes, d.agente
"""

SQL_MERCADO = f"""
CREATE OR REPLACE TABLE agg_mercado_mensual AS
WITH precio AS (
    SELECT date_trunc('month', fecha_hora)::DATE AS mes,
           avg(precio_cop_kwh) AS precio_bolsa_promedio_simple
    FROM v_precio_bolsa_hora WHERE variable = '{VARIABLE_PRECIO_BOLSA}' GROUP BY ALL
),
ppbo AS (
    SELECT date_trunc('month', fecha)::DATE AS mes, avg(precio_cop_kwh) AS ppbo_promedio_diario
    FROM v_precio_bolsa_dia WHERE variable = 'PPBO' GROUP BY ALL
),
expo AS (
    SELECT mes, sum(demanda_kwh) AS demanda_kwh,
           sum(demanda_regulada_kwh) AS demanda_regulada_kwh,
           sum(contratos_kwh) AS contratos_kwh, sum(bolsa_kwh) AS bolsa_kwh,
           sum(greatest(bolsa_neta_kwh, 0)) AS bolsa_neta_positiva_kwh,
           sum(costo_bolsa_cop) / nullif(sum(bolsa_kwh), 0) AS precio_bolsa_ponderado_compras,
           avg(precio_escasez) AS precio_escasez,
           bool_or(es_preliminar) AS es_preliminar
    FROM agg_exposicion_mensual GROUP BY mes
),
generacion AS (
    SELECT date_trunc('month', g.fecha_hora)::DATE AS mes,
           sum(g.kwh) AS generacion_kwh,
           sum(g.kwh) FILTER (WHERE p.tipo_generacion = 'Hidraulica') AS gen_hidraulica_kwh,
           sum(g.kwh) FILTER (WHERE p.tipo_generacion = 'Termica') AS gen_termica_kwh,
           sum(g.kwh) FILTER (WHERE p.tipo_generacion = 'Solar') AS gen_solar_kwh,
           sum(g.kwh) FILTER (WHERE p.tipo_generacion = 'Eolica') AS gen_eolica_kwh,
           sum(g.kwh) FILTER (WHERE p.tipo_generacion IS NULL) AS gen_sin_clasificar_kwh
    FROM v_generacion g
    LEFT JOIN (SELECT * FROM dim_planta WHERE es_actual) p USING (planta)
    GROUP BY ALL
),
aportes AS (
    SELECT date_trunc('month', fecha)::DATE AS mes,
           sum(aportes_energia) / nullif(sum(media_historica_energia), 0)
               AS aportes_vs_media_historica_pct
    FROM v_aportes WHERE region = 'Colombia' GROUP BY ALL
)
SELECT x.mes, x.demanda_kwh, x.demanda_regulada_kwh, x.contratos_kwh, x.bolsa_kwh,
       x.bolsa_neta_positiva_kwh / nullif(x.demanda_kwh, 0) AS exposicion_bolsa_pct,
       p.precio_bolsa_promedio_simple, x.precio_bolsa_ponderado_compras, pp.ppbo_promedio_diario,
       x.precio_escasez, a.aportes_vs_media_historica_pct,
       g.generacion_kwh, g.gen_hidraulica_kwh, g.gen_termica_kwh, g.gen_solar_kwh,
       g.gen_eolica_kwh, g.gen_sin_clasificar_kwh,
       x.es_preliminar
FROM expo x
LEFT JOIN precio p USING (mes)
LEFT JOIN ppbo pp USING (mes)
LEFT JOIN generacion g USING (mes)
LEFT JOIN aportes a USING (mes)
ORDER BY x.mes
"""


def _sql_distribucion() -> str:
    casos = []
    for bajo, alto in zip(RANGOS_EXPOSICION, RANGOS_EXPOSICION[1:], strict=False):
        etiqueta = f"{bajo:.0%}–{min(alto, 1):.0%}"
        casos.append(
            f"WHEN exposicion_bolsa_pct >= {bajo} AND exposicion_bolsa_pct < {alto} "
            f"THEN '{etiqueta}'"
        )
    return f"""
CREATE OR REPLACE TABLE agg_distribucion_exposicion AS
WITH base AS (
    SELECT mes, demanda_kwh, CASE {" ".join(casos)} ELSE 'sin dato' END AS rango_exposicion,
           es_preliminar
    FROM agg_exposicion_mensual
)
SELECT mes, rango_exposicion,
       count(*) AS comercializadores,
       sum(demanda_kwh) AS demanda_kwh,
       sum(demanda_kwh) / sum(sum(demanda_kwh)) OVER (PARTITION BY mes)
           AS participacion_demanda_pct,
       bool_or(es_preliminar) AS es_preliminar
FROM base GROUP BY mes, rango_exposicion
ORDER BY mes, rango_exposicion
"""


TABLAS_AGREGADAS = ["agg_exposicion_mensual", "agg_mercado_mensual", "agg_distribucion_exposicion"]


def calcular(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(SQL_EXPOSICION)
    con.execute(SQL_MERCADO)
    con.execute(_sql_distribucion())
