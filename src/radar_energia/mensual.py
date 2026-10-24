"""Actualización mensual del dato maestro.

Uso típico (día 12 de cada mes, en el PC o en GitHub Actions):
    python -m radar_energia.mensual

Carga histórica inicial (una sola vez, en el PC):
    python -m radar_energia.mensual --desde 2021-01 --hasta 2026-09

Pasos: calendario de versiones → selección de meses → ingesta → agregados → histórico
(opcional) → controles de calidad → publicación. Código de salida 0 si se publicó, 2 si un
control que bloquea falló (la bitácora se escribe igual) y 1 ante errores de ejecución.
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys
from pathlib import Path

from radar_energia import agregados, calidad, publicacion
from radar_energia.almacen import Almacen
from radar_energia.especificaciones import ESPECIFICACIONES, POR_DATASET
from radar_energia.ingesta import Ingestor, ResultadoIngesta

log = logging.getLogger("mensual")

VENTANA_MESES = 10  # TX5 llega 8–9 meses después del mes de operación
MESES_SIEMPRE = 2  # los meses más recientes aún reciben versiones diarias (TX1/TX2)
DATASET_VERSIONES = "24914F"


def mes(texto: str) -> dt.date:
    return dt.date.fromisoformat(f"{texto}-01")


def sumar_meses(m: dt.date, n: int) -> dt.date:
    total = m.year * 12 + m.month - 1 + n
    return dt.date(total // 12, total % 12 + 1, 1)


def rango_meses(desde: dt.date, hasta: dt.date) -> list[dt.date]:
    meses, actual = [], desde
    while actual <= hasta:
        meses.append(actual)
        actual = sumar_meses(actual, 1)
    return meses


def meses_a_procesar(almacen: Almacen, ventana: list[dt.date]) -> list[dt.date]:
    """Meses de la ventana que hay que (re)procesar.

    Un mes entra si nunca se ha cargado, si XM publicó una versión después de la última
    captura, o si está entre los ``MESES_SIEMPRE`` más recientes.
    """
    recientes = set(ventana[-MESES_SIEMPRE:])
    filas = almacen.con.execute(
        """
        SELECT l.mes, l.ultima_publicacion, min(m.fecha_captura)::DATE AS captura
        FROM dim_mes_liquidacion l
        LEFT JOIN ingesta_manifiesto m ON m.mes = l.mes AND m.dataset <> ?
        GROUP BY l.mes, l.ultima_publicacion
        """,
        [DATASET_VERSIONES],
    ).fetchall()
    estado = {m: (pub, cap) for m, pub, cap in filas}
    seleccion = []
    for m in ventana:
        publicacion_, captura = estado.get(m, (None, None))
        if m in recientes or captura is None or (publicacion_ and publicacion_ >= captura):
            seleccion.append(m)
    return seleccion


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--desde", type=mes, help="Primer mes (AAAA-MM). Fuerza el rango.")
    parser.add_argument("--hasta", type=mes, help="Último mes (AAAA-MM). Por defecto, el anterior.")
    parser.add_argument("--ventana", type=int, default=VENTANA_MESES)
    parser.add_argument("--raiz", type=Path, help="Carpeta de datos (por defecto RADAR_DATOS).")
    parser.add_argument("--salida", type=Path, default=Path("salida"))
    parser.add_argument("--historico", type=Path, help="Carpeta con la publicación anterior.")
    parser.add_argument("--datasets", nargs="*", help="Limitar a estos datasets (pruebas).")
    parser.add_argument(
        "--sin-descarga",
        action="store_true",
        help="No descarga: recalcula agregados con lo ya almacenado.",
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    hoy = dt.date.today()
    hasta = args.hasta or sumar_meses(dt.date(hoy.year, hoy.month, 1), -1)
    if args.desde:
        ventana = rango_meses(args.desde, hasta)
    else:
        ventana = rango_meses(sumar_meses(hasta, -(args.ventana - 1)), hasta)

    especificaciones = [
        e for e in ESPECIFICACIONES if not args.datasets or e.dataset in args.datasets
    ]
    resultados_ingesta: list[ResultadoIngesta] = []

    with Almacen(args.raiz) as almacen:
        meses = ventana
        if not args.sin_descarga:
            ingestor = Ingestor(almacen)
            # 1. Calendario de versiones de toda la ventana (es liviano y define el resto).
            for m in ventana:
                resultados_ingesta.append(ingestor.ingerir(POR_DATASET[DATASET_VERSIONES], m))
            # 2. Meses que cambiaron. Con --desde se procesa todo el rango pedido.
            meses = ventana if args.desde else meses_a_procesar(almacen, ventana)
            log.info("Meses a procesar: %s", ", ".join(f"{m:%Y-%m}" for m in meses))
            # 3. Ingesta del resto de datasets. Un fallo no detiene a los demás.
            for esp in especificaciones:
                if esp.dataset == DATASET_VERSIONES:
                    continue
                for m in meses:
                    try:
                        resultados_ingesta.append(ingestor.ingerir(esp, m))
                    except Exception as e:
                        log.exception("Fallo en %s %s", esp.dataset, f"{m:%Y-%m}")
                        resultados_ingesta.append(
                            ResultadoIngesta(esp.dataset, m, 0, "error", str(e)[:200])
                        )

        # 4. Agregados sobre toda la historia almacenada.
        agregados.calcular(almacen.con)
        notas = (
            publicacion.incorporar_historico(almacen.con, args.historico) if args.historico else []
        )

        # 5. Calidad sobre los meses procesados.
        resultados_calidad = calidad.ejecutar(almacen.con, meses)
        errores_ingesta = [r for r in resultados_ingesta if r.estado == "error"]
        if errores_ingesta:
            resultados_calidad.append(
                calidad.Resultado(
                    "ingesta:errores",
                    "bloquea",
                    False,
                    f"{len(errores_ingesta)} descargas fallaron: "
                    + ", ".join(f"{r.dataset} {r.mes:%Y-%m}" for r in errores_ingesta[:5]),
                )
            )
        bloqueos = calidad.bloqueantes(resultados_calidad)

        # 6. Publicación (la bitácora se escribe siempre).
        bitacora = publicacion.escribir_bitacora(
            almacen.con, args.salida, meses, resultados_ingesta, resultados_calidad, notas
        )
        log.info("Bitácora: %s", bitacora)
        if bloqueos:
            for r in bloqueos:
                log.error("Control bloqueante: %s — %s", r.control, r.detalle)
            return 2
        archivos = publicacion.exportar(almacen.con, args.salida)
        log.info("Publicados %d archivos en %s", len(archivos), args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
