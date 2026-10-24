import datetime as dt

import pytest
import requests

from radar_energia.simem import ClienteSimem, ErrorSimem, Filtro, ventanas_consulta

D = dt.date


def test_ventanas_diarias_parten_por_mes_calendario():
    assert ventanas_consulta(D(2026, 1, 15), D(2026, 3, 10), "Horaria") == [
        (D(2026, 1, 15), D(2026, 1, 31)),
        (D(2026, 2, 1), D(2026, 2, 28)),
        (D(2026, 3, 1), D(2026, 3, 10)),
    ]


def test_ventanas_mensuales_agrupan_24_meses():
    ventanas = ventanas_consulta(D(2023, 1, 1), D(2026, 6, 30), "Mensual")
    assert ventanas == [
        (D(2023, 1, 1), D(2024, 12, 31)),
        (D(2025, 1, 1), D(2026, 6, 30)),
    ]


def test_ventanas_rango_invertido_vacio():
    assert ventanas_consulta(D(2026, 2, 1), D(2026, 1, 1), "Diaria") == []


def test_filtro_a_api():
    assert Filtro("CodigoVariable", "in", ["PPBO", "PPBOGReal"]).a_api() == {
        "Fd": "CodigoVariable",
        "Op": "in",
        "Vl": "PPBO,PPBOGReal",
        "Lg": "and",
    }
    with pytest.raises(ValueError):
        Filtro("x", "~", "1").a_api()


class _Resp:
    def __init__(self, status, payload):
        self.status_code = status
        self._payload = payload
        self.text = str(payload)

    def json(self):
        return self._payload


class _SesionFalsa(requests.Session):
    def __init__(self, respuestas):
        super().__init__()
        self.respuestas = list(respuestas)
        self.llamadas = []

    def request(self, metodo, url, **kwargs):
        self.llamadas.append((metodo, url, kwargs.get("json")))
        r = self.respuestas.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def _cliente(respuestas):
    return ClienteSimem(sesion=_SesionFalsa(respuestas), espera_base=0)


def test_registros_por_ventana_y_formatos_de_respuesta():
    cliente = _cliente(
        [
            _Resp(200, [{"Valor": 1}]),
            _Resp(200, {"result": {"records": [{"Valor": 2}, {"Valor": 3}]}}),
        ]
    )
    salida = list(
        cliente.registros(
            "96D56E",
            D(2026, 1, 20),
            D(2026, 2, 5),
            "Diaria",
            [Filtro("CodigoVariable", "=", "PPBO")],
        )
    )
    assert [len(r) for _, r in salida] == [1, 2]
    metodo, url, cuerpo = cliente.sesion.llamadas[0]
    assert metodo == "POST"
    assert "startDate=2026-01-20&endDate=2026-01-31&datasetId=96D56E" in url
    assert cuerpo == [{"Fd": "CodigoVariable", "Op": "eq", "Vl": "PPBO", "Lg": "and"}]


def test_reintenta_fallas_transitorias():
    cliente = _cliente(
        [
            requests.ConnectionError("caída"),
            _Resp(503, {}),
            _Resp(200, {"result": {"name": "Precio", "metadata": {"granularity": "Diaria"}}}),
        ]
    )
    assert cliente.metadatos("96D56E")["name"] == "Precio"
    assert len(cliente.sesion.llamadas) == 3


def test_no_reintenta_error_de_cliente():
    cliente = _cliente([_Resp(400, {"message": "mal"}), _Resp(200, {})])
    with pytest.raises(ErrorSimem, match="HTTP 400"):
        cliente.metadatos("XXXXXX")
    assert len(cliente.sesion.llamadas) == 1


def test_agota_reintentos():
    cliente = _cliente([_Resp(500, {})] * 5)
    with pytest.raises(ErrorSimem, match="5 intentos"):
        cliente.metadatos("96D56E")
