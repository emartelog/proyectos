"""Prueba de humo del panel con los agregados de un pipeline sintético."""

import pytest

from tests.test_pipeline import _correr

pytest.importorskip("streamlit")
pytest.importorskip("plotly")


def test_panel_renderiza_sin_errores(tmp_path, cliente, monkeypatch):
    from streamlit.testing.v1 import AppTest

    assert _correr(tmp_path) == 0
    monkeypatch.setenv("RADAR_PANEL_DATOS", str(tmp_path / "salida"))
    app = AppTest.from_file("../panel/app.py", default_timeout=60).run()
    assert not app.exception, app.exception
    assert app.title[0].value == "Radar de Energía"
    assert len(app.tabs) == 4
    assert len(app.metric) == 4
    assert len(app.dataframe) >= 2  # una tabla de escenarios por simulador
