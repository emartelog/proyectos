"""Controles de calidad del dato maestro.

Cada control devuelve un ``Resultado``. Un control de nivel ``bloquea`` que falle detiene la
publicación; uno de nivel ``advierte`` queda registrado en la bitácora.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass

import duckdb

from radar_energia.especificaciones import ESPECIFICACIONES

TOLERANCIA_BALANCE = 0.02  # |demanda − (contratos + bolsa)| / demanda
PRECIO_BOLSA_MAX = 3_000.0  # COP/kWh; por encima se revisa
TOLERANCIA_PPBO = 0.01
MESES_MIN_VARIACION = 6


@dataclass
class Resultado:
    control: str
    nivel: str  # "bloquea" | "advierte"
    ok: bool
    detalle: str

    def a_dict(self) -> dict:
        return asdict(self)


def _meses_sql(meses: list[dt.date]) -> str:
    return ", ".join(f"DATE '{m.isoformat()}'" for m in meses) or "NULL"


def unicidad(con, meses) -> list[Resultado]:
    resultados = []
    for esp in ESPECIFICACIONES:
        clave = ", ".join(f'"{c}"' for c in esp.clave + (["version"] if esp.tipo_version else []))
        duplicados = con.execute(
            f"""
            SELECT count(*) FROM (
                SELECT {clave} FROM {esp.tabla}
                WHERE date_trunc('month', "{esp.columna_tiempo}") IN ({_meses_sql(meses)})
                GROUP BY ALL HAVING count(*) > 1)
            """
        ).fetchone()[0]
        resultados.append(
            Resultado(
                f"unicidad:{esp.tabla}",
                "bloquea",
                duplicados == 0,
                f"{duplicados} claves duplicadas" if duplicados else "sin duplicados",
            )
        )
    return resultados


def cobertura_horaria(con, meses) -> list[Resultado]:
    """Cada mes de un dataset horario debe tener todas sus horas (días × 24)."""
    resultados = []
    for esp in ESPECIFICACIONES:
        if esp.columna_tiempo != "fecha_hora":
            continue
        vista = "v_" + esp.tabla.removeprefix("h_")
        filas = con.execute(
            f"""
            WITH meses AS (SELECT unnest([{_meses_sql(meses)}]) AS mes)
            SELECT m.mes,
                   count(DISTINCT v.fecha_hora) AS horas,
                   datediff('hour', m.mes, m.mes + INTERVAL 1 MONTH) AS esperadas,
                   coalesce(l.es_preliminar, true) AS preliminar
            FROM meses m
            LEFT JOIN {vista} v ON date_trunc('month', v.fecha_hora) = m.mes
            LEFT JOIN dim_mes_liquidacion l ON l.mes = m.mes
            GROUP BY m.mes, l.es_preliminar ORDER BY m.mes
            """
        ).fetchall()
        for mes, horas, esperadas, preliminar in filas:
            completo = horas == esperadas
            resultados.append(
                Resultado(
                    f"cobertura:{esp.tabla}:{mes:%Y-%m}",
                    "advierte" if preliminar else "bloquea",
                    completo,
                    f"{horas}/{esperadas} horas" + (" (mes preliminar)" if preliminar else ""),
                )
            )
    return resultados


def balance(con, meses) -> Resultado:
    fuera = con.execute(
        f"""
        SELECT mes, agente,
               abs(demanda_kwh - contratos_kwh - bolsa_kwh) / demanda_kwh AS desvio
        FROM agg_exposicion_mensual
        WHERE mes IN ({_meses_sql(meses)})
          AND abs(demanda_kwh - contratos_kwh - bolsa_kwh) / demanda_kwh > {TOLERANCIA_BALANCE}
        ORDER BY desvio DESC
        """
    ).fetchall()
    total = con.execute(
        f"SELECT count(*) FROM agg_exposicion_mensual WHERE mes IN ({_meses_sql(meses)})"
    ).fetchone()[0]
    ejemplos = ", ".join(f"{a} {m:%Y-%m} ({d:.1%})" for m, a, d in fuera[:5])
    return Resultado(
        "balance:demanda=contratos+bolsa",
        "advierte",
        not fuera,
        f"{len(fuera)} de {total} agente-mes fuera de ±{TOLERANCIA_BALANCE:.0%}"
        + (f". Mayores: {ejemplos}" if fuera else ""),
    )


def precio_bolsa(con, meses) -> list[Resultado]:
    fuera = con.execute(
        f"""
        SELECT count(*) FROM v_precio_bolsa_hora
        WHERE variable = 'PB_Nal'
          AND date_trunc('month', fecha_hora) IN ({_meses_sql(meses)})
          AND (precio_cop_kwh < 0 OR precio_cop_kwh > {PRECIO_BOLSA_MAX})
        """
    ).fetchone()[0]
    # El PPBO diario publicado debe coincidir con el ponderado que calculamos.
    difiere = con.execute(
        f"""
        WITH calc AS (
            SELECT b.fecha_hora::DATE AS fecha,
                   sum(b.kwh * p.precio_cop_kwh) / nullif(sum(b.kwh), 0) AS ppbo_calc
            FROM v_compra_bolsa b
            JOIN v_precio_bolsa_hora p ON p.fecha_hora = b.fecha_hora AND p.variable = 'PB_Nal'
            WHERE date_trunc('month', b.fecha_hora) IN ({_meses_sql(meses)})
            GROUP BY ALL
        )
        SELECT count(*), count(*) FILTER (
            WHERE abs(c.ppbo_calc - d.precio_cop_kwh) / d.precio_cop_kwh > {TOLERANCIA_PPBO})
        FROM calc c JOIN v_precio_bolsa_dia d ON d.fecha = c.fecha AND d.variable = 'PPBO'
        """
    ).fetchone()
    dias, dias_dif = difiere
    return [
        Resultado(
            "precio_bolsa:rango",
            "advierte",
            fuera == 0,
            f"{fuera} horas fuera de [0, {PRECIO_BOLSA_MAX:,.0f}] COP/kWh",
        ),
        Resultado(
            "precio_bolsa:ppbo_reproducible",
            "advierte",
            dias > 0 and dias_dif == 0,
            f"{dias_dif} de {dias} días con PPBO calculado ≠ publicado (±{TOLERANCIA_PPBO:.0%})",
        ),
    ]


def _huerfanos(con, meses, vista: str, columna: str, dimension: str) -> list[str]:
    return [
        f[0]
        for f in con.execute(
            f"""
            SELECT DISTINCT {columna} FROM {vista}
            WHERE date_trunc('month', fecha_hora) IN ({_meses_sql(meses)})
              AND {columna} NOT IN (SELECT {columna} FROM {dimension})
            ORDER BY 1
            """
        ).fetchall()
    ]


def integridad(con, meses) -> list[Resultado]:
    resultados = []
    for nombre, vista, columna, dimension in (
        ("agentes", "v_demanda", "agente", "dim_agente"),
        ("plantas", "v_generacion", "planta", "dim_planta"),
    ):
        huerfanos = _huerfanos(con, meses, vista, columna, dimension)
        ejemplos = f". Ej.: {', '.join(huerfanos[:10])}" if huerfanos else ""
        resultados.append(
            Resultado(
                f"integridad:{nombre}",
                "advierte",
                not huerfanos,
                f"{len(huerfanos)} {nombre} de {vista.removeprefix('v_')} sin maestro{ejemplos}",
            )
        )
    return resultados


def cobertura_precio_contratos(con, meses) -> Resultado:
    filas = con.execute(
        f"""
        SELECT mes, sum(contratos_kwh * cobertura_precio_contrato_pct) / sum(contratos_kwh)
        FROM agg_exposicion_mensual WHERE mes IN ({_meses_sql(meses)})
        GROUP BY mes HAVING sum(contratos_kwh) > 0 ORDER BY mes
        """
    ).fetchall()
    if not filas:
        return Resultado("contratos:cobertura_precio", "advierte", False, "sin contratos")
    detalle = ", ".join(f"{m:%Y-%m}: {c or 0:.1%}" for m, c in filas)
    return Resultado(
        "contratos:cobertura_precio",
        "advierte",
        all((c or 0) >= 0.95 for _, c in filas),
        f"energía en contratos con precio por mes: {detalle}. "
        "XM publica los precios de contratos con rezago.",
    )


def variacion_demanda(con, meses) -> Resultado:
    filas = con.execute("SELECT mes, demanda_kwh FROM agg_mercado_mensual ORDER BY mes").fetchall()
    alertas = []
    for i, (mes, demanda) in enumerate(filas):
        previos = [d for _, d in filas[max(0, i - 12) : i] if d]
        if mes not in meses or len(previos) < MESES_MIN_VARIACION:
            continue
        media = sum(previos) / len(previos)
        desv = (sum((d - media) ** 2 for d in previos) / len(previos)) ** 0.5
        if desv and abs(demanda - media) > 3 * desv:
            alertas.append(f"{mes:%Y-%m}")
    return Resultado(
        "variacion:demanda_nacional",
        "advierte",
        not alertas,
        f"meses atípicos (>3σ): {', '.join(alertas)}" if alertas else "sin meses atípicos",
    )


def ejecutar(con: duckdb.DuckDBPyConnection, meses: list[dt.date]) -> list[Resultado]:
    resultados = unicidad(con, meses) + cobertura_horaria(con, meses)
    resultados.append(balance(con, meses))
    resultados += precio_bolsa(con, meses)
    resultados += integridad(con, meses)
    resultados.append(cobertura_precio_contratos(con, meses))
    resultados.append(variacion_demanda(con, meses))
    return resultados


def bloqueantes(resultados: list[Resultado]) -> list[Resultado]:
    return [r for r in resultados if r.nivel == "bloquea" and not r.ok]
