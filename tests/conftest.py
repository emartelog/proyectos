import pytest


@pytest.fixture
def cliente(monkeypatch):
    """Reemplaza el cliente de SIMEM por el mercado sintético de tests/test_pipeline.py."""
    from tests.test_pipeline import ClienteSintetico

    c = ClienteSintetico()
    monkeypatch.setattr("radar_energia.ingesta.ClienteSimem", lambda: c)
    return c
