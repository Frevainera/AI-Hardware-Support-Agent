# ==========================================
# AI Hardware Support Agent
# Windows Event Collector v0.2
# ==========================================

$report = [ordered]@{}

# ==========================================
# Configuración
# ==========================================

$days = 7
$startTime = (Get-Date).AddDays(-$days)

# ==========================================
# Obtener eventos del registro System
# ==========================================

$events = Get-WinEvent -FilterHashtable @{
    LogName   = "System"
    StartTime = $startTime
    Level     = 1, 2, 3
} -ErrorAction SilentlyContinue

# ==========================================
# Fuentes relevantes
# ==========================================

$relevantProviders = @(
    "Microsoft-Windows-Kernel-Power",
    "Microsoft-Windows-Kernel-Boot",
    "Microsoft-Windows-WHEA-Logger",
    "Disk",
    "Ntfs"
)

# ==========================================
# Filtrar eventos relevantes
# ==========================================

$relevantEvents = @(
    $events | Where-Object {
        $_.ProviderName -in $relevantProviders
    } | Select-Object -First 100 | ForEach-Object {

        [ordered]@{
            TimeCreated = $_.TimeCreated.ToString("yyyy-MM-dd HH:mm:ss")
            Id          = $_.Id
            Level       = $_.LevelDisplayName
            Provider    = $_.ProviderName
            Message     = $_.Message
        }
    }
)

# ==========================================
# Resumen general
# ==========================================

$report.Summary = [ordered]@{
    AnalysisPeriodDays = $days
    TotalEvents        = $events.Count

    CriticalEvents     = @(
        $events | Where-Object Level -eq 1
    ).Count

    ErrorEvents        = @(
        $events | Where-Object Level -eq 2
    ).Count

    WarningEvents      = @(
        $events | Where-Object Level -eq 3
    ).Count

    RelevantEvents     = $relevantEvents.Count
}

# ==========================================
# Contadores específicos
# ==========================================

$report.EventCounts = [ordered]@{

    KernelPower41 = @(
        $events | Where-Object {
            $_.ProviderName -eq "Microsoft-Windows-Kernel-Power" -and
            $_.Id -eq 41
        }
    ).Count

    KernelBoot29 = @(
        $events | Where-Object {
            $_.ProviderName -eq "Microsoft-Windows-Kernel-Boot" -and
            $_.Id -eq 29
        }
    ).Count

    WHEA = @(
        $events | Where-Object {
            $_.ProviderName -eq "Microsoft-Windows-WHEA-Logger"
        }
    ).Count

    Disk = @(
        $events | Where-Object {
            $_.ProviderName -eq "Disk"
        }
    ).Count

    Ntfs = @(
        $events | Where-Object {
            $_.ProviderName -eq "Ntfs"
        }
    ).Count
}

# ==========================================
# Eventos relevantes
# ==========================================

$report.RelevantEvents = $relevantEvents

# ==========================================
# Fecha de recolección
# ==========================================

$report.CollectionTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

# ==========================================
# Guardar JSON
# ==========================================

$json = $report | ConvertTo-Json -Depth 6

$outputPath = Join-Path $PSScriptRoot "..\data\event_log_report.json"

$json | Out-File -FilePath $outputPath -Encoding utf8

# ==========================================
# Resultado en consola
# ==========================================

Write-Host ""
Write-Host "=========================================="
Write-Host " AI HARDWARE SUPPORT AGENT"
Write-Host " Windows Event Collector v0.2"
Write-Host "=========================================="
Write-Host ""

Write-Host "Periodo analizado: $days dias"
Write-Host "Eventos encontrados: $($events.Count)"
Write-Host "Eventos relevantes: $($relevantEvents.Count)"
Write-Host ""

Write-Host "Kernel-Power 41: $($report.EventCounts.KernelPower41)"
Write-Host "Kernel-Boot 29:  $($report.EventCounts.KernelBoot29)"
Write-Host "WHEA:           $($report.EventCounts.WHEA)"
Write-Host "Disk:           $($report.EventCounts.Disk)"
Write-Host "Ntfs:           $($report.EventCounts.Ntfs)"
Write-Host ""

Write-Host "Informe generado:"
Write-Host $outputPath
Write-Host ""