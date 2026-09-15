from src.correlation import analyze_correlations


test_results = [
    {
        "timestamp": "2026-09-10 14:00:00",
        "sample": {
            "gpu": {
                "load_percent": 95.0,
                "temperature_c": 82.0,
                "hotspot_temperature_c": 97.0,
            }
        },
        "findings": []
    },
    {
        "timestamp": "2026-09-10 14:00:10",
        "sample": {
            "gpu": {
                "load_percent": 97.0,
                "temperature_c": 84.0,
                "hotspot_temperature_c": 99.0,
            }
        },
        "findings": []
    },
    {
        "timestamp": "2026-09-10 14:00:20",
        "sample": {
            "gpu": {
                "load_percent": 98.0,
                "temperature_c": 86.0,
                "hotspot_temperature_c": 101.0,
            }
        },
        "findings": []
    },
]


correlations = analyze_correlations(test_results)


print("")
print("==========================================")
print(" PRUEBA DE CORRELACION")
print("==========================================")
print("")

for correlation in correlations:

    print(
        f"[{correlation['severity']}] "
        f"{correlation['message']}"
    )

    print(
        f"Carga GPU: "
        f"{correlation['gpu_load_percent']} %"
    )

    print(
        f"Temperatura GPU: "
        f"{correlation['gpu_temperature_c']} °C"
    )

    print(
        f"Hot Spot: "
        f"{correlation['gpu_hotspot_temperature_c']} °C"
    )

    print(
        f"Muestras consecutivas: "
        f"{correlation['consecutive_samples']}"
    )

print("")
print(f"Correlaciones detectadas: {len(correlations)}")
print("")