"""Prueba de punta a punta del pipeline mensual con un mercado sintético de resultado conocido.

Mercado de prueba (por hora):
- Precio de bolsa: 200 COP/kWh de 00 a 11 h y 400 de 12 a 23 h.
- A1C (regulado): demanda 30; compra en bolsa 10 solo de 12 a 23 h; el resto en contratos.
  → exposición 120/720 = 1/6; precio medio de bolsa 400 (el promedio simple sería 300).
- A2C (no regulado): demanda 20; bolsa 5 todas las horas; contratos 15.
  → exposición 25 %; precio medio de bolsa 300.
- Contratos: A1C dos mecanismos a 250 y 350 (promedio diario 300); A2C a 280.
- Agosto liquidado (TX2 y TXR; TXR es la vigente). Septiembre solo TX2 (preliminar).
"""

import datetime as dt

import duckdb
import pytest

from radar_energia import mensual

AGO, SEP = dt.date(2026, 8, 1), dt.date(2026, 9, 1)


def _horas(inicio: dt.date, fin: dt.date):
    actual = dt.datetime.combine(inicio, dt.time())
    while actual.date() <= fin:
        yield actual
        actual += dt.timedelta(hours=1)


def _dias(inicio: dt.date, fin: dt.date):
    actual = inicio
    while actual <= fin:
        yield actual
        actual += dt.timedelta(days=1)


def _versiones(mes_ini: dt.date):
    # Agosto: TX2 (valores errados ×2) y TXR (valores correctos). Septiembre: solo TX2.
    return [("TX2", 2.0), ("TXR", 1.0)] if mes_ini == AGO else [("TX2", 1.0)]


def _registros(dataset: str, inicio: dt.date, fin: dt.date) -> list[dict]:
    r: list[dict] = []
    versiones = _versiones(dt.date(inicio.year, inicio.month, 1))
    if dataset == "24914F":
        if inicio <= AGO <= fin:
            r += [
                {
                    "Version": "TXR",
                    "FechaInicio": "2026-08-01",
                    "FechaFin": "2026-08-31",
                    "FechaPublicacion": "2026-09-05",
                    "esMaximaVersion": 0,
                },
                {
                    "Version": "TXF",
                    "FechaInicio": "2026-08-01",
                    "FechaFin": "2026-08-31",
                    "FechaPublicacion": "2026-09-10",
                    "esMaximaVersion": 1,
                },
            ]
        return r
    for d in _dias(inicio, fin):
        f = d.isoformat()
        if dataset == "972263":
            r += [
                {
                    "Fecha": f,
                    "CodigoSICAgente": a,
                    "NombreAgente": n,
                    "ActividadAgente": t,
                    "CodigoDuracion": "P1D",
                }
                for a, n, t in [
                    ("A1C", "Agente uno", "Comercializador"),
                    ("A2C", "Agente dos", "Comercializador"),
                    ("G1G", "Generador", "Generador"),
                ]
            ]
        elif dataset == "0BFC9D":
            for p, tipo in [("P1", "Hidraulica"), ("P2", "Solar")]:
                r.append(
                    {
                        "Fecha": f,
                        "FechaPublicacion": "2026-10-05",
                        "CodigoPlanta": p,
                        "NombrePlanta": p,
                        "CodigoSICAgente": "G1G",
                        "CapEfectivaNeta": 100.0,
                        "TipoGeneracion": tipo,
                        "TipoClasificacion": "GENERADOR",
                        "TipoDespachoRecurso": "Despachado Centralmente",
                        "CodigoAreaOperativa": "A",
                        "CodigoSubAreaOperativa": "S",
                    }
                )
        elif dataset == "96D56E":
            # PPBO = (120×400 + 60×200 + 60×400) / 240 = 350
            r += [
                {"CodigoVariable": "PPBO", "Fecha": f, "Version": v, "Valor": 350.0 * k}
                for v, k in versiones
            ]
        elif dataset == "D31647":
            for v, k in versiones:
                r += [
                    {
                        "Fecha": f,
                        "CodigoAgenteComprador": "A1C",
                        "TipoMercado": "Regulado",
                        "Mecanismo": "Subasta MME",
                        "NormatividadRelacionada": "MME",
                        "Valor": 250.0 * k,
                        "Version": v,
                        "CodigoVariable": "PrecioContratoLP",
                    },
                    {
                        "Fecha": f,
                        "CodigoAgenteComprador": "A1C",
                        "TipoMercado": "Regulado",
                        "Mecanismo": "SICEP",
                        "NormatividadRelacionada": "CREG",
                        "Valor": 350.0 * k,
                        "Version": v,
                        "CodigoVariable": "PrecioContratoLP",
                    },
                    {
                        "Fecha": f,
                        "CodigoAgenteComprador": "A2C",
                        "TipoMercado": "No Regulado",
                        "Mecanismo": "Negociación Bilateral",
                        "NormatividadRelacionada": "CREG",
                        "Valor": 280.0 * k,
                        "Version": v,
                        "CodigoVariable": "PrecioContratoLP",
                    },
                ]
        elif dataset == "43D616":
            r += [
                {
                    "CodigoVariable": "PrecioEscasezPonderado",
                    "FechaInicio": f,
                    "Version": v,
                    "Valor": 900.0,
                }
                for v, _ in versiones
            ]
        elif dataset == "BA1C55":
            r.append(
                {
                    "Fecha": f,
                    "FechaPublicacion": f,
                    "CodigoSerieHidrologica": "COL",
                    "RegionHidrologica": "Colombia",
                    "AportesHidricosEnergia": 80.0,
                    "MediaHistoricaEnergia": 100.0,
                    "PromedioAcumuladoEnergia": 90.0,
                }
            )
    for h in _horas(inicio, fin):
        fh = h.isoformat()
        tarde = h.hour >= 12
        for v, k in versiones:
            if dataset == "EC6945":
                r.append(
                    {
                        "CodigoVariable": "PB_Nal",
                        "FechaHora": fh,
                        "Version": v,
                        "Valor": (400.0 if tarde else 200.0) * k,
                    }
                )
            elif dataset == "D55202":
                r += [
                    {
                        "CodigoVariable": "DdaCom",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A1C",
                        "TipoMercado": "Regulado",
                        "Version": v,
                        "Valor": 30.0 * k,
                    },
                    {
                        "CodigoVariable": "DdaCom",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A2C",
                        "TipoMercado": "No Regulado",
                        "Version": v,
                        "Valor": 20.0 * k,
                    },
                ]
            elif dataset == "42EDC9":
                r += [
                    {
                        "CodigoVariable": "MgCB",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A1C",
                        "Version": v,
                        "Valor": (10.0 if tarde else 0.0) * k,
                    },
                    {
                        "CodigoVariable": "MgCB",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A2C",
                        "Version": v,
                        "Valor": 5.0 * k,
                    },
                ]
            elif dataset == "E14D70":
                r.append(
                    {
                        "CodigoVariable": "MgVB",
                        "FechaHora": fh,
                        "CodigoSICAgente": "G1G",
                        "Version": v,
                        "Valor": 15.0 * k,
                    }
                )
            elif dataset == "C8381F":
                r += [
                    {
                        "CodigoVariable": "x",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A1C",
                        "TipoMercado": "Regulado",
                        "Version": v,
                        "Valor": (20.0 if tarde else 30.0) * k,
                    },
                    {
                        "CodigoVariable": "x",
                        "FechaHora": fh,
                        "CodigoSICAgente": "A2C",
                        "TipoMercado": "No Regulado",
                        "Version": v,
                        "Valor": 15.0 * k,
                    },
                ]
            elif dataset == "8E7F3C":
                r += [
                    {
                        "CodigoVariable": "GIdealNal",
                        "FechaHora": fh,
                        "CodigoPlanta": "P1",
                        "Version": v,
                        "Valor": 50.0 * k,
                    },
                    {
                        "CodigoVariable": "GIdealNal",
                        "FechaHora": fh,
                        "CodigoPlanta": "P2",
                        "Version": v,
                        "Valor": 10.0 * k,
                    },
                ]
    return r


class ClienteSintetico:
    def __init__(self):
        self.solicitudes = 0

    def metadatos(self, dataset):
        return {"name": dataset, "metadata": {"granularity": "Diaria"}}

    def registros(self, dataset, inicio, fin, granularidad, filtros=None):
        self.solicitudes += 1
        yield (inicio, fin), _registros(dataset, inicio, fin)


@pytest.fixture
def cliente(monkeypatch):
    c = ClienteSintetico()
    monkeypatch.setattr("radar_energia.ingesta.ClienteSimem", lambda: c)
    return c


def _correr(tmp_path, *extra, raiz="datos"):
    return mensual.main(
        [
            "--desde",
            "2026-08",
            "--hasta",
            "2026-09",
            "--raiz",
            str(tmp_path / raiz),
            "--salida",
            str(tmp_path / "salida"),
            *extra,
        ]
    )


def _exposicion(tmp_path, carpeta="salida"):
    con = duckdb.connect()
    ruta = tmp_path / carpeta / "agg_exposicion_mensual.parquet"
    return {
        (m, a): fila
        for m, a, *fila in con.execute(
            f"""SELECT mes, agente, exposicion_bolsa_pct, precio_medio_bolsa,
                       precio_medio_contrato, es_preliminar, demanda_kwh, nombre_agente
                FROM '{ruta}'"""
        ).fetchall()
    }


def test_pipeline_calcula_indicadores_ponderados(tmp_path, cliente):
    assert _correr(tmp_path) == 0
    expo = _exposicion(tmp_path)

    a1 = expo[(AGO, "A1C")]
    assert a1[0] == pytest.approx(1 / 6)
    assert a1[1] == pytest.approx(400)  # ponderado horario, no el promedio simple (300)
    assert a1[2] == pytest.approx(300)  # promedio diario de 250 y 350, ponderado por energía
    assert a1[3] is False  # agosto liquidado: TXR vigente
    assert a1[4] == pytest.approx(30 * 24 * 31)  # usa TXR, no TX2 (que vale el doble)
    assert a1[5] == "Agente uno"

    a2 = expo[(AGO, "A2C")]
    assert a2[0] == pytest.approx(0.25)
    assert a2[1] == pytest.approx(300)
    assert a2[2] == pytest.approx(280)

    assert expo[(SEP, "A1C")][3] is True  # septiembre solo con TX2: preliminar

    bitacora = (tmp_path / "salida" / "bitacora.md").read_text()
    assert "balance:demanda=contratos+bolsa | advierte | ✅" in bitacora
    assert "precio_bolsa:ppbo_reproducible | advierte | ✅" in bitacora


def test_mercado_y_distribucion(tmp_path, cliente):
    assert _correr(tmp_path) == 0
    con = duckdb.connect()
    salida = tmp_path / "salida"
    mercado = con.execute(
        f"""SELECT exposicion_bolsa_pct, precio_bolsa_ponderado_compras,
                   precio_bolsa_promedio_simple, aportes_vs_media_historica_pct,
                   gen_hidraulica_kwh, gen_solar_kwh
            FROM '{salida}/agg_mercado_mensual.parquet' WHERE mes = DATE '2026-08-01'"""
    ).fetchone()
    horas = 24 * 31
    assert mercado[0] == pytest.approx((10 * 12 * 31 + 5 * horas) / (50 * horas))
    assert mercado[1] == pytest.approx(350)
    assert mercado[2] == pytest.approx(300)
    assert mercado[3] == pytest.approx(0.8)
    assert mercado[4] == pytest.approx(50 * horas)
    assert mercado[5] == pytest.approx(10 * horas)

    rangos = dict(
        con.execute(
            f"""SELECT rango_exposicion, comercializadores
                FROM '{salida}/agg_distribucion_exposicion.parquet'
                WHERE mes = DATE '2026-08-01'"""
        ).fetchall()
    )
    assert rangos == {"10%–25%": 1, "25%–50%": 1}


def test_reproceso_es_idempotente(tmp_path, cliente):
    assert _correr(tmp_path) == 0
    antes = _exposicion(tmp_path)
    assert _correr(tmp_path) == 0
    assert _exposicion(tmp_path) == antes
    bitacora = (tmp_path / "salida" / "bitacora.md").read_text()
    assert "sin cambios" in bitacora


def test_historico_conserva_meses_no_recalculados(tmp_path, cliente):
    assert _correr(tmp_path) == 0
    # Corrida "sin estado" (como en GitHub Actions) que solo recalcula septiembre.
    codigo = mensual.main(
        [
            "--desde",
            "2026-09",
            "--hasta",
            "2026-09",
            "--raiz",
            str(tmp_path / "limpio"),
            "--salida",
            str(tmp_path / "nueva"),
            "--historico",
            str(tmp_path / "salida"),
        ]
    )
    assert codigo == 0
    expo = _exposicion(tmp_path, "nueva")
    assert (AGO, "A1C") in expo and (SEP, "A1C") in expo


def test_meses_a_procesar(tmp_path, cliente):
    assert _correr(tmp_path) == 0
    from radar_energia.almacen import Almacen

    with Almacen(tmp_path / "datos") as almacen:
        ventana = mensual.rango_meses(dt.date(2026, 6, 1), SEP)
        # Junio y julio nunca se cargaron; agosto y septiembre son los más recientes.
        assert mensual.meses_a_procesar(almacen, ventana) == ventana
        ventana_larga = mensual.rango_meses(AGO, dt.date(2026, 11, 1))
        # Agosto ya capturado después de su última publicación: no se reprocesa.
        assert AGO not in mensual.meses_a_procesar(almacen, ventana_larga)


def test_columnas_faltantes_se_reportan(tmp_path, monkeypatch):
    class ClienteRoto(ClienteSintetico):
        def registros(self, dataset, inicio, fin, granularidad, filtros=None):
            filas = _registros(dataset, inicio, fin)
            if dataset == "D55202":
                filas = [{k: v for k, v in f.items() if k != "TipoMercado"} for f in filas]
            yield (inicio, fin), filas

    monkeypatch.setattr("radar_energia.ingesta.ClienteSimem", ClienteRoto)
    assert _correr(tmp_path) == 2  # la ingesta falla y bloquea la publicación
    bitacora = (tmp_path / "salida" / "bitacora.md").read_text()
    assert "faltan columnas" in bitacora
    assert not (tmp_path / "salida" / "agg_exposicion_mensual.parquet").exists()
