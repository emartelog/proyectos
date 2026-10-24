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

if ($Hora -notmatch '^([01]\d|2[0-3]):[0-5]\d$') { throw "Hora inválida: use HH:mm (24 h)." }

$script = Resolve-Path (Join-Path $PSScriptRoot "ejecutar_mensual.ps1")
$argumentos = [System.Security.SecurityElement]::Escape(
    "-NoProfile -ExecutionPolicy Bypass -File `"$script`"")
$meses = "January February March April May June July August September October November December"
$xmlMeses = ($meses.Split(" ") | ForEach-Object { "<$_ />" }) -join ""

# Se registra con una definición XML: es la forma confiable de crear un disparador mensual
# con "ejecutar lo antes posible si se omitió" (New-ScheduledTaskTrigger no tiene mensual).
$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Radar de Energía: actualización mensual del dato maestro (SIMEM).</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-01-01T$($Hora):00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByMonth>
        <DaysOfMonth><Day>$Dia</Day></DaysOfMonth>
        <Months>$xmlMeses</Months>
      </ScheduleByMonth>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <ExecutionTimeLimit>PT6H</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>$argumentos</Arguments>
    </Exec>
  </Actions>
</Task>
"@

Register-ScheduledTask -Xml $xml -TaskPath $Ruta -TaskName $Nombre -Force | Out-Null

$info = Get-ScheduledTaskInfo -TaskPath $Ruta -TaskName $Nombre
Write-Host "Tarea programada: $Ruta$Nombre (día $Dia de cada mes, $Hora)" -ForegroundColor Green
Write-Host "Próxima ejecución: $($info.NextRunTime)"
Write-Host "La tarea corre con su sesión iniciada; si el PC estaba apagado, corre al encenderlo."
