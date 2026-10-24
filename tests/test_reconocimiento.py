import datetime as dt

import pandas as pd

from radar_energia.perfil import perfilar
from radar_energia.reconocimiento import mes_anterior, ventanas_muestra

D = dt.date


def test_mes_anterior_cruza_anio():
    assert mes_anterior(D(2026, 1, 15)) == (D(2025, 12, 1), D(2025, 12, 31))
    assert mes_anterior(D(2026, 3, 31), 1) == (D(2026, 2, 1), D(2026, 2, 28))


def test_ventanas_muestra_por_rol():
    hoy = D(2026, 10, 24)
    hecho = ventanas_muestra({"id": "96D56E", "rol": "hecho"}, hoy, 4)
    assert hecho == [
        ("mes_reciente", D(2026, 9, 1), D(2026, 9, 30)),
        ("mes_maduro", D(2026, 5, 1), D(2026, 5, 31)),
    ]
    assert len(ventanas_muestra({"id": "0BFC9D", "rol": "maestro"}, hoy, 4)) == 1
    assert ventanas_muestra({"id": "24914f", "rol": "maestro"}, hoy, 4) == [
        ("ultimo_anio", D(2025, 10, 1), D(2026, 9, 30)),
    ]


def test_perfilar():
    df = pd.DataFrame(
        {
            "Fecha": ["2026-09-01", "2026-09-02", "2026-09-02"],
            "Version": ["TX1", "TX2", "TX2"],
            "Valor": [100.0, None, None],
        }
    )
    p = perfilar(df)
    assert p["filas"] == 3 and p["filas_duplicadas"] == 1
    assert p["columnas"]["Fecha"]["min"].startswith("2026-09-01")
    assert p["columnas"]["Version"]["valores"] == {"TX2": 2, "TX1": 1}
    assert p["columnas"]["Valor"]["nulos"] == 2 and p["columnas"]["Valor"]["suma"] == 100.0


def test_catalogo_tolera_nulos(tmp_path):
    from radar_energia.reconocimiento import reconocer_catalogos

    class Cliente:
        def catalogo(self, _):
            return [
                {"idDataset": "C8381F", "nombre": "Cantidad en contratos", "finDato": None},
                {"idDataset": "AAA111", "nombre": "Otro", "finDato": "2026-10-01"},
            ]

    config = {"catalogos": {"datasets": "e007fb"}, "busqueda_catalogo": ["contrato"]}
    candidatos = reconocer_catalogos(Cliente(), config, tmp_path)
    assert [c["idDataset"] for c in candidatos] == ["C8381F"]


def test_registro_de_fuentes_valido():
    from pathlib import Path

    import yaml

    config = yaml.safe_load(Path("config/fuentes.yml").read_text())
    ids = [d["id"] for d in config["datasets"]] + list(config["catalogos"].values())
    assert all(isinstance(i, str) and len(i) == 6 and i.isalnum() for i in ids), ids
    assert len(set(ids)) == len(ids)
    assert all(d["rol"] in {"maestro", "hecho"} for d in config["datasets"])
