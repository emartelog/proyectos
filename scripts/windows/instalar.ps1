<#
.SYNOPSIS
  Instala el Radar de Energía en un PC con Windows.

.DESCRIPTION
  1. Verifica que Python 3.11 o superior esté instalado.
  2. Crea un entorno virtual (.venv) en la carpeta del proyecto e instala el paquete.
  3. Crea la carpeta de datos y guarda su ruta en la variable de usuario RADAR_DATOS.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\windows\instalar.ps1
  powershell -ExecutionPolicy Bypass -File scripts\windows\instalar.ps1 -Datos D:\RadarEnergia
#>
param(
    [string]$Datos = "C:\RadarEnergia\datos",
    [switch]$Desarrollo
)

$ErrorActionPreference = "Stop"
$Proyecto = Resolve-Path (Join-Path $PSScriptRoot "..\..")

function Buscar-Python {
    $candidatos = @(@{ Exe = "py"; Args = @("-3") }, @{ Exe = "python"; Args = @() })
    foreach ($c in $candidatos) {
        if (-not (Get-Command $c.Exe -ErrorAction SilentlyContinue)) { continue }
        $a = $c.Args
        $version = & $c.Exe @a -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $version) { continue }
        $mayor, $menor = "$version".Trim().Split(".") | ForEach-Object { [int]$_ }
        if ($mayor -gt 3 -or ($mayor -eq 3 -and $menor -ge 11)) { return $c }
        Write-Warning "Se encontró Python $version; se requiere 3.11 o superior."
    }
    throw "No se encontró Python 3.11+. Instálelo desde https://www.python.org/downloads/ (marque 'Add python.exe to PATH')."
}

Write-Host "== Radar de Energía: instalación ==" -ForegroundColor Cyan
$python = Buscar-Python
Write-Host "Python: $($python.Exe) $($python.Args -join ' ')"

$venv = Join-Path $Proyecto ".venv"
if (-not (Test-Path $venv)) {
    Write-Host "Creando entorno virtual en $venv"
    $a = $python.Args
    & $python.Exe @a -m venv $venv
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear el entorno virtual." }
}
$pythonVenv = Join-Path $venv "Scripts\python.exe"

Write-Host "Instalando dependencias..."
& $pythonVenv -m pip install --upgrade pip --quiet
$paquete = if ($Desarrollo) { "$Proyecto[dev]" } else { "$Proyecto" }
& $pythonVenv -m pip install -e $paquete --quiet
if ($LASTEXITCODE -ne 0) { throw "Falló la instalación del paquete." }

New-Item -ItemType Directory -Force -Path $Datos | Out-Null
[Environment]::SetEnvironmentVariable("RADAR_DATOS", $Datos, "User")
$env:RADAR_DATOS = $Datos

& $pythonVenv -c "import radar_energia, duckdb; print('Paquete OK, DuckDB', duckdb.__version__)"
if ($LASTEXITCODE -ne 0) { throw "La verificación del paquete falló." }

Write-Host ""
Write-Host "Instalación completa." -ForegroundColor Green
Write-Host "  Datos:  $Datos (variable de usuario RADAR_DATOS)"
Write-Host "  Correr: scripts\windows\ejecutar_mensual.ps1"
Write-Host "  Tarea:  scripts\windows\programar_tarea.ps1"
