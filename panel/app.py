"""Radar de Energía: panel para comercializadoras y grandes consumidores.

Lee los agregados del dato maestro. Por defecto usa los de la última corrida publicada en el
repositorio (``datos/ultima_corrida``); con la variable ``RADAR_PANEL_DATOS`` se puede apuntar
a la carpeta ``salida`` del PC.

    streamlit run panel/app.py

El panel no muestra nombres de agentes: solo agregados del mercado y rangos.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
DATOS = Path(os.environ.get("RADAR_PANEL_DATOS", RAIZ / "datos" / "ultima_corrida"))

# Paleta validada (skill dataviz): 3 categóricos all-pairs y rampa ordinal azul.
PALETA = {
    "light": {
        "superficie": "#fcfcfb",
        "tinta": "#0b0b0b",
        "tinta2": "#52514e",
        "tenue": "#898781",
        "rejilla": "#e1e0d9",
        "base": "#c3c2b7",
        "serie": ["#2a78d6", "#eb6834", "#1baf7a"],
        "ordinal": ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"],
    },
    "dark": {
        "superficie": "#1a1a19",
        "tinta": "#f0efec",
        "tinta2": "#c3c2b7",
        "tenue": "#898781",
        "rejilla": "#2c2c2a",
        "base": "#383835",
        "serie": ["#3987e5", "#d95926", "#199e70"],
        "ordinal": ["#184f95", "#256abf", "#3987e5", "#6da7ec", "#b7d3f6"],
    },
}
COLUMNAS_ESPERADAS = {
    "agg_mercado_mensual": [
        "precio_bolsa_ponderado_compras",
        "precio_bolsa_p10",
        "precio_bolsa_p90",
        "precio_contrato_regulado",
        "precio_contrato_no_regulado",
        "precio_escasez",
        "exposicion_bolsa_pct",
        "aportes_vs_media_historica_pct",
        "es_preliminar",
    ],
}
RANGOS = ["0%–10%", "10%–25%", "25%–50%", "50%–75%", "75%–100%"]


# --- Datos -----------------------------------------------------------------------
@st.cache_data(ttl=3600)
def cargar(nombre: str) -> pd.DataFrame:
    for ext in ("parquet", "csv"):
        archivo = DATOS / f"{nombre}.{ext}"
        if archivo.exists():
            df = pd.read_parquet(archivo) if ext == "parquet" else pd.read_csv(archivo)
            df["mes"] = pd.to_datetime(df["mes"])
            # Publicaciones anteriores pueden no traer columnas nuevas: quedan vacías.
            faltantes = [c for c in COLUMNAS_ESPERADAS.get(nombre, []) if c not in df]
            df = df.assign(**{c: float("nan") for c in faltantes})
            return df.sort_values("mes")
    return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_calidad() -> list[dict]:
    archivo = DATOS / "calidad.json"
    return json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else []


# --- Formato -----------------------------------------------------------------------
def cop(x: float | None, dec: int = 0) -> str:
    if x is None or pd.isna(x):
        return "—"
    texto = f"{abs(x):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-${texto}" if x < 0 else f"${texto}"


def pct(x: float | None) -> str:
    return "—" if x is None or pd.isna(x) else f"{x:.1%}".replace(".", ",")


def gwh(x: float | None) -> str:
    return "—" if x is None or pd.isna(x) else f"{x / 1e6:,.0f} GWh".replace(",", ".")


def mes_txt(m: pd.Timestamp) -> str:
    meses = "ene feb mar abr may jun jul ago sep oct nov dic".split()
    return f"{meses[m.month - 1]} {m.year}"


def etiquetas(meses: pd.Series) -> list[str]:
    """Meses como etiquetas en español; el eje es categórico y conserva el orden."""
    return [mes_txt(m) for m in meses]


def md(texto: str) -> str:
    """Escapa el signo $ para que Streamlit no lo interprete como fórmula."""
    return texto.replace("$", r"\$")


def mostrar(fig: go.Figure, meses: pd.Series) -> None:
    """Dibuja la figura con marcas de eje legibles: con historia larga, solo ene y jul."""
    etiquetas_mes = etiquetas(meses)
    if len(etiquetas_mes) > 24:
        marcas = [e for e, m in zip(etiquetas_mes, meses, strict=True) if m.month in (1, 7)]
        fig.update_xaxes(tickmode="array", tickvals=marcas, ticktext=marcas)
    st.plotly_chart(fig, use_container_width=True)


def tema() -> dict:
    tipo = getattr(getattr(st.context, "theme", None), "type", None)
    return PALETA["dark" if tipo == "dark" else "light"]


def _alfa(hex_color: str, alfa: float) -> str:
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alfa})"


def figura(t: dict, titulo_y: str, formato_y: str = ",.0f") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=360,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color=t["tinta2"]),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=t["superficie"], font_color=t["tinta"]),
        legend=dict(orientation="h", y=1.1, x=0, font=dict(color=t["tinta2"]), traceorder="normal"),
        separators=",.",
    )
    fig.update_xaxes(
        type="category",
        showgrid=False,
        linecolor=t["base"],
        tickfont=dict(color=t["tenue"]),
        tickangle=0,
    )
    fig.update_yaxes(
        title=titulo_y,
        gridcolor=t["rejilla"],
        zeroline=False,
        tickfont=dict(color=t["tenue"]),
        tickformat=formato_y,
        title_font=dict(color=t["tenue"]),
    )
    return fig


def linea(fig, meses, y, nombre, color, formato="%{y:,.0f}"):
    fig.add_trace(
        go.Scatter(
            x=etiquetas(meses),
            y=y,
            name=nombre,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=8, color=color),
            hovertemplate=formato,
        )
    )


# --- Escenarios ----------------------------------------------------------------
def escenarios_bolsa(mercado: pd.DataFrame) -> pd.DataFrame:
    """Precios de bolsa de referencia, tomados de la historia mensual (ponderado por compras)."""
    serie = mercado["precio_bolsa_ponderado_compras"].dropna()
    ultimo = mercado.dropna(subset=["precio_bolsa_ponderado_compras"]).iloc[-1]
    filas = [
        ("Mes húmedo (percentil 10 histórico)", serie.quantile(0.10)),
        ("Mes típico (mediana histórica)", serie.quantile(0.50)),
        ("Mes seco (percentil 90 histórico)", serie.quantile(0.90)),
        (f"Último mes ({mes_txt(ultimo['mes'])})", ultimo["precio_bolsa_ponderado_compras"]),
    ]
    if pd.notna(ultimo.get("precio_escasez")):
        filas.append(("Precio de escasez vigente", ultimo["precio_escasez"]))
    return pd.DataFrame(filas, columns=["escenario", "precio_bolsa"])


def costo_mezcla(
    energia_kwh: float, fraccion_bolsa: float, precio_contrato: float, escenarios: pd.DataFrame
) -> pd.DataFrame:
    df = escenarios.copy()
    df["costo_total"] = energia_kwh * (
        fraccion_bolsa * df["precio_bolsa"] + (1 - fraccion_bolsa) * precio_contrato
    )
    df["costo_unitario"] = df["costo_total"] / energia_kwh
    df["vs_100_contratos"] = df["costo_total"] - energia_kwh * precio_contrato
    return df


def tabla_escenarios(df: pd.DataFrame) -> None:
    st.dataframe(
        pd.DataFrame(
            {
                "Escenario de bolsa": df["escenario"],
                "Precio de bolsa ($/kWh)": df["precio_bolsa"].map(cop),
                "Costo unitario ($/kWh)": df["costo_unitario"].map(cop),
                "Costo del mes": df["costo_total"].map(cop),
                "Diferencia vs. 100 % en contratos": df["vs_100_contratos"].map(cop),
            }
        ),
        hide_index=True,
        use_container_width=True,
    )


# --- Secciones -------------------------------------------------------------------
def seccion_mercado(mercado: pd.DataFrame, t: dict) -> None:
    ultimo = mercado.iloc[-1]
    previo = mercado.iloc[-2] if len(mercado) > 1 else None

    def delta(col, fmt):
        if previo is None or pd.isna(previo[col]) or pd.isna(ultimo[col]):
            return None
        return fmt(ultimo[col] - previo[col])

    def pp(d):
        return f"{d * 100:+.1f} pp".replace(".", ",")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Precio de bolsa pagado",
        f"{cop(ultimo['precio_bolsa_ponderado_compras'])}/kWh",
        delta("precio_bolsa_ponderado_compras", lambda d: f"{cop(d)} vs. mes anterior"),
        delta_color="inverse",
    )
    c2.metric(
        "Demanda comprada en bolsa",
        pct(ultimo["exposicion_bolsa_pct"]),
        delta("exposicion_bolsa_pct", pp),
        delta_color="inverse",
    )
    c3.metric("Precio de escasez", f"{cop(ultimo['precio_escasez'])}/kWh")
    c4.metric(
        "Aportes hídricos vs. media",
        pct(ultimo["aportes_vs_media_historica_pct"]),
        delta("aportes_vs_media_historica_pct", pp),
    )

    st.markdown("#### Precio de la energía: bolsa frente a contratos y escasez")
    st.caption(
        "$/kWh por mes. La franja muestra el rango del precio de bolsa horario "
        "(percentiles 10 a 90)."
    )
    fig = figura(t, "$/kWh")
    x = etiquetas(mercado["mes"])
    fig.add_trace(
        go.Scatter(
            x=x,
            y=mercado["precio_bolsa_p10"],
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=mercado["precio_bolsa_p90"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor=_alfa(t["serie"][0], 0.15),
            name="Rango horario de bolsa (p10–p90)",
            hoverinfo="skip",
        )
    )
    linea(
        fig,
        mercado["mes"],
        mercado["precio_bolsa_ponderado_compras"],
        "Bolsa (pagado por compradores)",
        t["serie"][0],
    )
    linea(
        fig,
        mercado["mes"],
        mercado["precio_contrato_regulado"],
        "Contratos, mercado regulado",
        t["serie"][1],
    )
    linea(
        fig,
        mercado["mes"],
        mercado["precio_contrato_no_regulado"],
        "Contratos, mercado no regulado",
        t["serie"][2],
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=mercado["precio_escasez"],
            name="Precio de escasez",
            mode="lines",
            line=dict(color=t["tenue"], width=2, dash="dash"),
            hovertemplate="%{y:,.0f}",
        )
    )
    mostrar(fig, mercado["mes"])

    st.markdown("#### Hidrología: aportes frente a la media histórica")
    fig = figura(t, "% de la media", ".0%")
    fig.add_trace(
        go.Bar(
            x=x,
            y=mercado["aportes_vs_media_historica_pct"],
            name="Aportes",
            marker=dict(color=t["serie"][0], cornerradius=4),
            hovertemplate="%{y:.0%}",
        )
    )
    fig.add_hline(
        y=1,
        line=dict(color=t["tenue"], width=1, dash="dot"),
        annotation_text="Media histórica",
        annotation_font_color=t["tenue"],
    )
    fig.update_layout(showlegend=False, bargap=0.25)
    mostrar(fig, mercado["mes"])


def seccion_comercializadoras(mercado, distribucion, t) -> None:
    st.markdown("#### ¿Qué parte de la demanda se compra en bolsa?")
    st.caption("Compra neta en bolsa / demanda comercial, total del mercado.")
    fig = figura(t, "% de la demanda", ".0%")
    linea(
        fig,
        mercado["mes"],
        mercado["exposicion_bolsa_pct"],
        "Exposición a bolsa",
        t["serie"][0],
        "%{y:.1%}",
    )
    fig.update_layout(showlegend=False)
    fig.update_yaxes(rangemode="tozero")
    mostrar(fig, mercado["mes"])

    st.markdown("#### ¿Cómo se reparte esa exposición?")
    st.caption(
        "Participación en la demanda nacional según el rango de exposición a bolsa de "
        "cada comercializador. Sin nombres de agentes."
    )
    fig = figura(t, "% de la demanda", ".0%")
    for i, rango in enumerate(RANGOS):
        datos = distribucion[distribucion["rango_exposicion"] == rango]
        fig.add_trace(
            go.Bar(
                x=etiquetas(datos["mes"]),
                y=datos["participacion_demanda_pct"],
                name=f"Expuestos {rango}",
                marker=dict(color=t["ordinal"][i], line=dict(color=t["superficie"], width=2)),
                customdata=datos["comercializadores"],
                hovertemplate="%{y:.1%} de la demanda · %{customdata} comercializadores",
            )
        )
    fig.update_layout(barmode="stack", bargap=0.2, legend_traceorder="normal")
    fig.update_xaxes(categoryorder="array", categoryarray=etiquetas(mercado["mes"]))
    mostrar(fig, mercado["mes"])

    st.markdown("#### Simulador: ¿cuánto cuesta cada punto de exposición?")
    con_precio = mercado.dropna(subset=["precio_contrato_regulado"])
    referencia = con_precio["precio_contrato_regulado"].iloc[-1] if len(con_precio) else 300.0
    c1, c2, c3 = st.columns(3)
    demanda = c1.number_input("Demanda mensual (GWh)", 1.0, 2_000.0, 100.0, 10.0, format="%.0f")
    exposicion = c2.slider("Demanda sin cubrir con contratos (%)", 0, 100, 20) / 100
    precio_contrato = c3.number_input(
        "Precio de sus contratos ($/kWh)",
        50.0,
        2_000.0,
        float(round(referencia)),
        5.0,
        format="%.0f",
    )
    df = costo_mezcla(demanda * 1e6, exposicion, precio_contrato, escenarios_bolsa(mercado))
    tabla_escenarios(df)
    seco, humedo = df.iloc[2], df.iloc[0]
    st.info(
        md(
            f"Con {pct(exposicion)} de la demanda en bolsa, pasar de un mes húmedo a uno seco "
            f"cambia el costo de compra en **{cop(seco['costo_total'] - humedo['costo_total'])}** "
            "al mes. Cada punto adicional de exposición en un mes seco vale "
            f"**{cop(demanda * 1e6 * 0.01 * (seco['precio_bolsa'] - precio_contrato))}**."
        )
    )


def seccion_consumidores(mercado, t) -> None:
    st.markdown("#### Contratos no regulados frente a la bolsa")
    st.caption(
        "$/kWh por mes. Un precio de bolsa por encima del contrato es el costo de no "
        "haberse cubierto."
    )
    fig = figura(t, "$/kWh")
    linea(fig, mercado["mes"], mercado["precio_bolsa_ponderado_compras"], "Bolsa", t["serie"][0])
    linea(
        fig,
        mercado["mes"],
        mercado["precio_contrato_no_regulado"],
        "Contratos, mercado no regulado",
        t["serie"][2],
    )
    mostrar(fig, mercado["mes"])

    st.markdown("#### Simulador: contrato fijo o exposición a bolsa")
    referencia = mercado["precio_contrato_no_regulado"].dropna()
    c1, c2, c3 = st.columns(3)
    consumo = c1.number_input(
        "Consumo mensual (MWh)", 10.0, 500_000.0, 5_000.0, 100.0, format="%.0f"
    )
    en_bolsa = c2.slider("Consumo comprado a precio de bolsa (%)", 0, 100, 30) / 100
    precio = c3.number_input(
        "Precio ofrecido en contrato ($/kWh)",
        50.0,
        2_000.0,
        float(round(referencia.iloc[-1])) if len(referencia) else 350.0,
        5.0,
        format="%.0f",
    )
    df = costo_mezcla(consumo * 1e3, en_bolsa, precio, escenarios_bolsa(mercado))
    tabla_escenarios(df)
    serie = mercado["precio_bolsa_ponderado_compras"].dropna()
    meses_caros = (serie > precio).mean() if len(serie) else float("nan")
    st.info(
        md(
            f"En la historia disponible, la bolsa estuvo por encima de {cop(precio)}/kWh en "
            f"**{pct(meses_caros)}** de los meses. Es la frecuencia con que el contrato ofrecido "
            "habría sido más barato que comprar en bolsa."
        )
    )


def seccion_metodologia(calidad: list[dict], mercado: pd.DataFrame) -> None:
    st.markdown(
        """
**Fuente:** datos abiertos de SIMEM (XM). Dato maestro mensual con todas las versiones de
liquidación; se usa siempre la versión vigente.

**Definiciones**
- *Precio de bolsa pagado*: costo horario de las compras en bolsa / energía comprada
  (reproduce el PPBO publicado por XM).
- *Exposición a bolsa*: compra neta en bolsa / demanda comercial.
- *Precio de contratos*: precio diario por comprador ponderado por la energía contratada.
  XM publica los precios con rezago: el último mes puede estar incompleto.
- *Escenarios del simulador*: percentiles del precio de bolsa mensual en la historia
  disponible. No son pronósticos.

Código y documentación: rama `radar-energia` del repositorio.
        """
    )
    if calidad:
        advertencias = [c for c in calidad if not c["ok"]]
        st.markdown(
            f"**Controles de calidad de la última corrida:** {len(calidad)} ejecutados, "
            f"{len(advertencias)} con advertencia."
        )
        for c in advertencias:
            st.markdown(f"- ⚠️ `{c['control']}`: {c['detalle']}")
    with st.expander("Ver datos del mercado"):
        st.dataframe(mercado, hide_index=True, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Radar de Energía", page_icon="⚡", layout="wide")
    mercado = cargar("agg_mercado_mensual")
    distribucion = cargar("agg_distribucion_exposicion")
    if mercado.empty:
        st.error(f"No hay datos en {DATOS}. Ejecute el pipeline o defina RADAR_PANEL_DATOS.")
        st.stop()

    t = tema()
    ultimo = mercado.iloc[-1]
    st.title("Radar de Energía")
    st.caption(
        f"Mercado de Energía Mayorista de Colombia · {mes_txt(mercado['mes'].iloc[0])} a "
        f"{mes_txt(ultimo['mes'])} · "
        + ("último mes preliminar" if ultimo["es_preliminar"] else "último mes liquidado")
        + " · Fuente: SIMEM (XM)"
    )
    pestanas = st.tabs(["Mercado", "Comercializadoras", "Grandes consumidores", "Metodología"])
    with pestanas[0]:
        seccion_mercado(mercado, t)
    with pestanas[1]:
        seccion_comercializadoras(mercado, distribucion, t)
    with pestanas[2]:
        seccion_consumidores(mercado, t)
    with pestanas[3]:
        seccion_metodologia(cargar_calidad(), mercado)


main()
