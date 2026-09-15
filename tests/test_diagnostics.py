from src.diagnostics import analyze_sample


test_sample = {
    "timestamp": "TEST",
    "cpu": {
        "load_percent": 95.0,
        "ram_percent": 92.0,
        "ram_total_gb": 15.77,
        "ram_available_gb": 1.2,
        "temperature_c": 92.0,
        "average_temperature_c": 85.0,
        "clock_average_mhz": 2500.0,
        "clock_max_mhz": 2500.0,
    },
    "gpu": {
        "load_percent": 99.0,
        "temperature_c": 92.0,
        "hotspot_temperature_c": 108.0,
        "memory_temperature_c": 97.0,
        "core_clock_mhz": 1500.0,
        "memory_clock_mhz": 1750.0,
        "vram_used_mb": 7500.0,
        "vram_free_mb": 676.0,
        "vram_total_mb": 8176.0,
    },
    "disk": {
        "total_gb": 446.08,
        "used_gb": 430.0,
        "free_gb": 16.08,
        "percent": 96.0,
    },
}


findings = analyze_sample(test_sample)


print("")
print("==========================================")
print(" PRUEBA DE ANOMALIA")
print("==========================================")
print("")

for finding in findings:
    print(
        f"[{finding['severity']}] "
        f"{finding['message']}"
    )

print("")
print(f"Total de hallazgos: {len(findings)}")
print("")