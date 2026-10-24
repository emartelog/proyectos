<#
.SYNOPSIS
  Ejecuta la actualización mensual del dato maestro y deja un log por corrida.

.EXAMPLE
  scripts\windows\ejecutar_mensual.ps1
  scripts\windows\ejecutar_mensual.ps1 -Desde 2021-01 -Hasta 2026-09   # carga histórica
#>
param(
    [string]$Desde,
    [string]$Hasta,
    [switch]$SinDescarga,
    [string]$Datos = $(if ($env:RADAR_DATOS) { $env:RADAR_DATOS }
                       else { [Environment]::GetEnvironmentVariable("RADAR_DATOS", "User") })
)

$ErrorActionPreference = "Stop"
$Proyecto = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$pythonVenv = Join-Path $Proyecto ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonVenv)) { throw "Falta el entorno. Ejecute primero scripts\windows\instalar.ps1" }
if (-not $Datos) { throw "RADAR_DATOS no está definido. Ejecute primero scripts\windows\instalar.ps1" }

$env:RADAR_DATOS = $Datos
$env:PYTHONUTF8 = "1"  # tildes y símbolos de la bitácora en UTF-8
$logs = Join-Path $Datos "logs"
$salida = Join-Path $Datos "salida"
New-Item -ItemType Directory -Force -Path $logs, $salida | Out-Null
$log = Join-Path $logs ("mensual_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date))

$argumentos = @("-m", "radar_energia.mensual", "--salida", $salida)
if ($Desde) { $argumentos += @("--desde", $Desde) }
if ($Hasta) { $argumentos += @("--hasta", $Hasta) }
if ($SinDescarga) { $argumentos += "--sin-descarga" }

Write-Host "Ejecutando: python $($argumentos -join ' ')"
Write-Host "Log: $log"
Push-Location $Proyecto
try {
    # Python escribe el log en stderr; se redirige todo al archivo y a la consola.
    $ErrorActionPreference = "Continue"
    & $pythonVenv @argumentos 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath $log
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

switch ($codigo) {
    0 { Write-Host "Listo. Resultados en $salida" -ForegroundColor Green }
    2 { Write-Warning "Un control de calidad bloqueó la publicación. Revise $salida\bitacora.md" }
    default { Write-Error "La actualización falló (código $codigo). Revise $log" }
}
exit $codigo
