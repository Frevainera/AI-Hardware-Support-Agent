# ==========================================
# AI Hardware Support Agent
# Hardware Collector v0.2
# ==========================================

$report = [ordered]@{}

# Sistema operativo
$os = Get-CimInstance Win32_OperatingSystem

$report.OS = [ordered]@{
    Name         = $os.Caption
    Version      = $os.Version
    Architecture = $os.OSArchitecture
}

# Procesador
$cpu = Get-CimInstance Win32_Processor

$report.CPU = [ordered]@{
    Name                    = $cpu.Name
    Cores                   = $cpu.NumberOfCores
    LogicalProcessors       = $cpu.NumberOfLogicalProcessors
    MaxClockMHz             = $cpu.MaxClockSpeed
}

# Memoria RAM
$computer = Get-CimInstance Win32_ComputerSystem

$report.RAM = [ordered]@{
    TotalBytes = $computer.TotalPhysicalMemory
    TotalGB    = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
}

# Motherboard
$board = Get-CimInstance Win32_BaseBoard

$report.Motherboard = [ordered]@{
    Manufacturer = $board.Manufacturer
    Product      = $board.Product
}

# BIOS
$bios = Get-CimInstance Win32_BIOS

$report.BIOS = [ordered]@{
    Manufacturer = $bios.Manufacturer
    Version      = $bios.SMBIOSBIOSVersion
    ReleaseDate  = $bios.ReleaseDate
}

# GPU
$gpus = Get-CimInstance Win32_VideoController

$report.GPU = @(
    $gpus | ForEach-Object {
        [ordered]@{
            Name          = $_.Name
            DriverVersion = $_.DriverVersion
        }
    }
)

# Discos
$disks = Get-CimInstance Win32_DiskDrive

$report.Disks = @(
    $disks | ForEach-Object {
        [ordered]@{
            Model      = $_.Model
            Interface  = $_.InterfaceType
            SizeBytes  = $_.Size
            SizeGB     = [math]::Round($_.Size / 1GB, 2)
        }
    }
)
# ==========================================
# Estado actual del sistema
# ==========================================

# Uso de CPU
$cpuLoad = Get-CimInstance Win32_Processor |
    Measure-Object -Property LoadPercentage -Average

# Memoria disponible
$osMemory = Get-CimInstance Win32_OperatingSystem

$usedMemory = $computer.TotalPhysicalMemory - $osMemory.FreePhysicalMemory * 1KB
$memoryUsagePercent = ($usedMemory / $computer.TotalPhysicalMemory) * 100

$report.SystemStatus = [ordered]@{
    CPUUsagePercent    = [math]::Round($cpuLoad.Average, 2)
    MemoryUsagePercent = [math]::Round($memoryUsagePercent, 2)
    FreeMemoryGB       = [math]::Round(($osMemory.FreePhysicalMemory * 1KB) / 1GB, 2)
}

# Fecha de recopilación
$report.CollectionTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

# Convertir a JSON
$json = $report | ConvertTo-Json -Depth 5

# Guardar informe
$outputPath = Join-Path $PSScriptRoot "..\data\hardware_report.json"

$json | Out-File -FilePath $outputPath -Encoding utf8

Write-Host ""
Write-Host "======================================"
Write-Host " AI HARDWARE SUPPORT AGENT"
Write-Host " Hardware Collector v0.2"
Write-Host "======================================"
Write-Host ""
Write-Host "Informe generado:"
Write-Host $outputPath
Write-Host ""