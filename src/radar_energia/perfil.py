"""Perfilamiento de datos: qué columnas trae un dataset, con qué calidad y qué valores."""

from __future__ import annotations

import pandas as pd

MAX_CATEGORIAS = 30  # Si una columna tiene hasta este número de valores distintos, se listan.


def perfilar(df: pd.DataFrame) -> dict:
    """Resume estructura y calidad de un DataFrame en un dict serializable a JSON."""
    perfil: dict = {
        "filas": int(len(df)),
        "filas_duplicadas": int(df.duplicated().sum()) if len(df) else 0,
        "columnas": {},
    }
    for col in df.columns:
        serie = df[col]
        info: dict = {
            "tipo": str(serie.dtype),
            "nulos": int(serie.isna().sum()),
            "distintos": int(serie.nunique(dropna=True)),
        }
        if col.lower().startswith("fecha"):
            fechas = pd.to_datetime(serie, errors="coerce")
            if fechas.notna().any():
                info["min"] = str(fechas.min())
                info["max"] = str(fechas.max())
        elif pd.api.types.is_numeric_dtype(serie) and serie.notna().any():
            info["min"] = float(serie.min())
            info["max"] = float(serie.max())
            info["suma"] = float(serie.sum())
        if 0 < info["distintos"] <= MAX_CATEGORIAS:
            conteos = serie.astype(str).value_counts(dropna=True)
            info["valores"] = {str(k): int(v) for k, v in conteos.items()}
        perfil["columnas"][col] = info
    return perfil
