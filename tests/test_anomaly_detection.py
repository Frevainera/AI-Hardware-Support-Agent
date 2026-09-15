from src.anomaly_detection import detect_persistent_anomalies


test_results = [
    {
        "timestamp": "2026-09-10 14:00:00",
        "findings": [
            {
                "severity": "WARNING",
                "component": "GPU",
                "metric": "temperatura",
                "value": 82.0,
                "message": "GPU: temperatura elevada (82.0 °C)."
            }
        ]
    },
    {
        "timestamp": "2026-09-10 14:00:10",
        "findings": [
            {
                "severity": "WARNING",
                "component": "GPU",
                "metric": "temperatura",
                "value": 84.0,
                "message": "GPU: temperatura elevada (84.0 °C)."
            }
        ]
    },
    {
        "timestamp": "2026-09-10 14:00:20",
        "findings": [],
    },
]


persistent = detect_persistent_anomalies(
    test_results,
    minimum_samples=3
)


print("")
print("==========================================")
print(" PRUEBA DE ANOMALIA PERSISTENTE")
print("==========================================")
print("")

for anomaly in persistent:

    print(
        f"[{anomaly['severity']}] "
        f"{anomaly['message']}"
    )

print("")
print(
    f"Anomalías persistentes: "
    f"{len(persistent)}"
)
print("")