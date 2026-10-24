"""Reconocimiento de fuentes: descarga muestras de SIMEM y documenta qué traen.

Uso:
    python -m radar_energia.reconocimiento --config config/fuentes.yml

Para cada dataset del registro descarga dos meses de muestra:
- el último mes cerrado (datos recientes, versiones tempranas de liquidación), y
- un mes "maduro" varios meses atrás (para observar las reliquidaciones posteriores).

Salidas (versionadas en git, livianas):
    datos/reconocimiento/RESUMEN.md
    datos/reconocimiento/catalogo_datasets.csv | catalogo_variables.csv
    datos/reconocimiento/<ID>/metadatos.json | perfil.json | muestra.csv
Datos completos (no versionados, se publican como artefacto del workflow):
    datos/_crudo/<ID>.parquet
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

from radar_energia.perfil import perfilar
from radar_energia.simem import ClienteSimem

log = logging.getLogger("reconocimiento")

FILAS_MUESTRA = 500
MESES_HISTORIA_VERSIONES = 12


def mes_anterior(fecha: dt.date, meses: int = 1) -> tuple[dt.date, dt.date]:
    """Primer y último día del mes que está ``meses`` antes del mes de ``fecha``."""
    total = fecha.year * 12 + fecha.month - 1 - meses
    inicio = dt.date(total // 12, total % 12 + 1, 1)
    sig = total + 1
    fin = dt.date(sig // 12, sig % 12 + 1, 1) - dt.timedelta(days=1)
    return inicio, fin


def ventanas_muestra(
    dataset: dict, hoy: dt.date, meses_maduro: int
) -> list[tuple[str, dt.date, dt.date]]:
    """Ventanas a descargar por dataset, con una etiqueta legible."""
    if dataset["id"].upper() == "24914F":  # calendario de versiones: un año completo
        inicio, _ = mes_anterior(hoy, MESES_HISTORIA_VERSIONES)
        _, fin = mes_anterior(hoy, 1)
        return [("ultimo_anio", inicio, fin)]
    reciente = ("mes_reciente", *mes_anterior(hoy, 1))
    if dataset.get("rol") == "maestro":
        return [reciente]
    return [reciente, ("mes_maduro", *mes_anterior(hoy, 1 + meses_maduro))]


def reconocer_dataset(
    cliente: ClienteSimem,
    dataset: dict,
    hoy: dt.date,
    meses_maduro: int,
    salida: Path,
    crudo: Path,
) -> dict:
    ds_id = dataset["id"].upper()
    carpeta = salida / ds_id
    carpeta.mkdir(parents=True, exist_ok=True)

    meta = cliente.metadatos(ds_id)
    (carpeta / "metadatos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    granularidad = (meta.get("metadata") or {}).get("granularity", "Diaria")

    marcos = []
    for etiqueta, inicio, fin in ventanas_muestra(dataset, hoy, meses_maduro):
        for (desde, hasta), registros in cliente.registros(ds_id, inicio, fin, granularidad):
            log.info("%s %s %s..%s: %d registros", ds_id, etiqueta, desde, hasta, len(registros))
            if registros:
                df = pd.DataFrame.from_records(registros)
                df["_ventana"] = etiqueta
                marcos.append(df)
    df = pd.concat(marcos, ignore_index=True) if marcos else pd.DataFrame()

    perfil = perfilar(df.drop(columns="_ventana", errors="ignore"))
    perfil["filas_por_ventana"] = (
        df["_ventana"].value_counts().to_dict() if "_ventana" in df else {}
    )
    perfil["granularidad"] = granularidad
    (carpeta / "perfil.json").write_text(json.dumps(perfil, ensure_ascii=False, indent=2))

    if not df.empty:
        crudo.mkdir(parents=True, exist_ok=True)
        df.to_parquet(crudo / f"{ds_id}.parquet", index=False)
        muestra = df.sample(n=min(FILAS_MUESTRA, len(df)), random_state=0).sort_index()
        muestra.to_csv(carpeta / "muestra.csv", index=False)

    versiones = (perfil["columnas"].get("Version") or {}).get("valores", {})
    return {
        "id": ds_id,
        "nombre": meta.get("name", dataset.get("nombre")),
        "granularidad": granularidad,
        "filas": perfil["filas"],
        "duplicadas": perfil["filas_duplicadas"],
        "columnas": list(perfil["columnas"]),
        "versiones": versiones,
        "estado": "ok" if perfil["filas"] else "sin datos",
    }


def reconocer_catalogos(cliente: ClienteSimem, config: dict, salida: Path) -> list[dict]:
    """Guarda los catálogos y devuelve los datasets que coinciden con las palabras clave."""
    candidatos: list[dict] = []
    for nombre, cat_id in config["catalogos"].items():
        df = pd.DataFrame.from_records(cliente.catalogo(cat_id))
        df.to_csv(salida / f"catalogo_{nombre}.csv", index=False)
        log.info("Catálogo %s: %d registros", nombre, len(df))
        if nombre != "datasets" or df.empty:
            continue
        texto = df.fillna("").astype(str).agg(" ".join, axis=1).str.lower()
        patron = "|".join(re.escape(p) for p in config.get("busqueda_catalogo", []))
        if patron:
            candidatos = df[texto.str.contains(patron)].to_dict(orient="records")
    return candidatos


def escribir_resumen(
    salida: Path, hoy: dt.date, resultados: list[dict], candidatos: list[dict], errores: dict
) -> None:
    lineas = [
        "# Reconocimiento de fuentes SIMEM",
        "",
        f"Ejecutado: {dt.datetime.now(dt.UTC):%Y-%m-%d %H:%M} UTC · fecha de referencia {hoy}",
        "",
        "| ID | Dataset | Granularidad | Filas | Duplicadas | Versiones | Estado |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for r in resultados:
        versiones = ", ".join(f"{k}:{v}" for k, v in sorted(r["versiones"].items())) or "—"
        lineas.append(
            f"| {r['id']} | {r['nombre']} | {r['granularidad']} | {r['filas']:,} "
            f"| {r['duplicadas']:,} | {versiones} | {r['estado']} |"
        )
    for ds_id, error in errores.items():
        lineas.append(f"| {ds_id} | — | — | — | — | — | ERROR: {error[:120]} |")
    lineas += ["", "## Columnas por dataset", ""]
    for r in resultados:
        lineas.append(f"- **{r['id']}**: {', '.join(r['columnas']) or '—'}")
    lineas += ["", f"## Candidatos en el catálogo ({len(candidatos)})", ""]
    for c in candidatos:
        resumen = " · ".join(str(v) for v in list(c.values())[:4])
        lineas.append(f"- {resumen}")
    (salida / "RESUMEN.md").write_text("\n".join(lineas) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=Path("config/fuentes.yml"))
    parser.add_argument("--salida", type=Path, default=Path("datos/reconocimiento"))
    parser.add_argument("--crudo", type=Path, default=Path("datos/_crudo"))
    parser.add_argument("--hoy", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument(
        "--meses-maduro",
        type=int,
        default=4,
        help="Meses antes del mes reciente para la muestra madura.",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = yaml.safe_load(args.config.read_text())
    args.salida.mkdir(parents=True, exist_ok=True)
    cliente = ClienteSimem()

    errores: dict[str, str] = {}
    try:
        candidatos = reconocer_catalogos(cliente, config, args.salida)
    except Exception as e:  # el reconocimiento debe continuar aunque falle una fuente
        log.exception("Fallo en catálogos")
        errores["catalogos"] = str(e)
        candidatos = []

    resultados = []
    for dataset in config["datasets"]:
        try:
            resultados.append(
                reconocer_dataset(
                    cliente, dataset, args.hoy, args.meses_maduro, args.salida, args.crudo
                )
            )
        except Exception as e:
            log.exception("Fallo en %s", dataset["id"])
            errores[dataset["id"].upper()] = str(e)

    escribir_resumen(args.salida, args.hoy, resultados, candidatos, errores)
    log.info("Listo: %d datasets ok, %d con error", len(resultados), len(errores))
    return 0 if resultados else 1


if __name__ == "__main__":
    sys.exit(main())
