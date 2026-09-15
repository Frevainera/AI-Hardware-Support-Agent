from src.recommendations import generate_recommendations


print("")
print("==========================================")
print(" PRUEBA DE RECOMENDACIONES")
print("==========================================")
print("")


test_results = [
    {
        "timestamp": "2026-09-10 15:00:20",

        "findings": [
            {
                "severity": "CRITICAL",
                "component": "CPU",
                "metric": "temperatura",
                "value": 94.0,
                "message": "CPU: temperatura crítica (94.0 °C).",
            },
            {
                "severity": "WARNING",
                "component": "GPU",
                "metric": "temperatura",
                "value": 86.0,
                "message": "GPU: temperatura elevada (86.0 °C).",
            },
            {
                "severity": "WARNING",
                "component": "GPU",
                "metric": "Hot Spot",
                "value": 101.0,
                "message": "GPU: Hot Spot elevada (101.0 °C).",
            },
            {
                "severity": "CRITICAL",
                "component": "RAM",
                "metric": "uso",
                "value": 94.0,
                "message": "RAM: uso crítico (94.0 %).",
            },
            {
                "severity": "CRITICAL",
                "component": "Disco",
                "metric": "espacio utilizado",
                "value": 96.8,
                "message": "Disco: espacio utilizado crítico (96.8 %).",
            },
        ],
    }
]


test_correlations = [
    {
        "type": "GPU_THERMAL",
        "severity": "WARNING",
        "consecutive_samples": 3,
    }
]


recommendations = generate_recommendations(
    test_results,
    test_correlations
)


for recommendation in recommendations:

    print(
        f"[{recommendation['priority']}] "
        f"{recommendation['component']}"
    )

    print(
        f"Causa: {recommendation['cause']}"
    )

    print("Acciones:")

    for action in recommendation["actions"]:
        print(f"  - {action}")

    print("")


print(
    f"Recomendaciones generadas: "
    f"{len(recommendations)}"
)