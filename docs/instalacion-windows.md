# Instalación en Windows

Requisitos: Windows 10/11, [Python 3.11 o superior](https://www.python.org/downloads/)
(al instalarlo, marque **Add python.exe to PATH**) y [Git](https://git-scm.com/download/win).

## 1. Descargar el proyecto

```powershell
git clone -b radar-energia https://github.com/emartelog/proyectos.git
cd proyectos
```

## 2. Instalar

```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows\instalar.ps1
```

Crea el entorno `.venv`, instala el paquete y define la carpeta de datos
`C:\RadarEnergia\datos` (variable de usuario `RADAR_DATOS`). Para usar otra carpeta:
`... instalar.ps1 -Datos D:\RadarEnergia`.

## 3. Carga histórica (una sola vez)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows\ejecutar_mensual.ps1 -Desde 2021-01
```

Descarga desde enero de 2021 hasta el último mes cerrado (~800 MB). Puede tardar varias
horas. Si se interrumpe, al volver a correrlo solo recarga lo que cambió.

## 4. Programar la actualización mensual

```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows\programar_tarea.ps1
```

Crea la tarea `\RadarEnergia\Mensual` en el Programador de tareas: el día 12 de cada mes a
las 07:00. Si el PC está apagado a esa hora, corre apenas se encienda. Para quitarla:
`programar_tarea.ps1 -Eliminar`.

## Qué queda en la carpeta de datos

| Ruta | Contenido |
|---|---|
| `crudo\<DATASET>\<AAAA-MM>.parquet` | Respuesta de SIMEM, tal cual |
| `maestro.duckdb` | Base con maestros, hechos versionados y agregados |
| `salida\` | Agregados y maestros en Parquet y CSV, `bitacora.md`, `calidad.json` |
| `logs\` | Un log por corrida |

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | Actualización publicada en `salida\` |
| 2 | Un control de calidad que bloquea falló. Revise `salida\bitacora.md` |
| 1 | Error de ejecución. Revise el log |
