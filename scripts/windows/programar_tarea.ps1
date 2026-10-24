<#
.SYNOPSIS
  Programa la actualización mensual en el Programador de tareas de Windows.

.DESCRIPTION
  Crea la tarea \RadarEnergia\Mensual: el día 12 de cada mes a las 07:00. Si el PC estaba
  apagado a esa hora, la tarea corre apenas se encienda (StartWhenAvailable).

.EXAMPLE
  scripts\windows\programar_tarea.ps1
  scripts\windows\programar_tarea.ps1 -Dia 14 -Hora 20:00
  scripts\windows\programar_tarea.ps1 -Eliminar
#>
param(
    [ValidateRange(1, 28)][int]$Dia = 12,
    [string]$Hora = "07:00",
    [switch]$Eliminar
)

$ErrorActionPreference = "Stop"
$Ruta = "\RadarEnergia\"
$Nombre = "Mensual"

if ($Eliminar) {
    Unregister-ScheduledTask -TaskPath $Ruta -TaskName $Nombre -Confirm:$false
    Write-Host "Tarea eliminada."
    exit 0
}

$script = Resolve-Path (Join-Path $PSScriptRoot "ejecutar_mensual.ps1")
$accion = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$script`""

# New-ScheduledTaskTrigger no admite frecuencia mensual; se usa schtasks y luego se ajusta.
schtasks.exe /Create /F /TN "$Ruta$Nombre" /SC MONTHLY /D $Dia /ST $Hora /TR $accion | Out-Null
if ($LASTEXITCODE -ne 0) { throw "schtasks no pudo crear la tarea." }

$tarea = Get-ScheduledTask -TaskPath $Ruta -TaskName $Nombre
$tarea.Settings.StartWhenAvailable = $true
$tarea.Settings.ExecutionTimeLimit = "PT6H"
Set-ScheduledTask -InputObject $tarea | Out-Null

$info = Get-ScheduledTaskInfo -TaskPath $Ruta -TaskName $Nombre
Write-Host "Tarea programada: $Ruta$Nombre (día $Dia de cada mes, $Hora)" -ForegroundColor Green
Write-Host "Próxima ejecución: $($info.NextRunTime)"
