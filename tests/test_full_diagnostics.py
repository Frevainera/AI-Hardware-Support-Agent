from src.diagnostics import analyze_history
from src.anomaly_detection import detect_persistent_anomalies
from src.correlation import analyze_correlations
from src.recommendations import generate_recommendations


def build_test_history():
    return [
        {
            "timestamp": "2026-09-10 15:00:00",
            "cpu": {
                "temperature_c": 92,
                "load_percent": 95,
                "ram_percent": 92,
            },
            "gpu": {
                "temperature_c": 82,
                "hotspot_temperature_c": 97,
                "memory_temperature_c": 88,
                "load_percent": 95,
                "vram_used_mb": 7500,
                "vram_total_mb": 8176,
            },
            "disk": {
                "percent": 96,
            },
        },
        {
            "timestamp": "2026-09-10 15:00:10",
            "cpu": {
                "temperature_c": 93,
                "load_percent": 96,
                "ram_percent": 93,
            },
            "gpu": {
                "temperature_c": 84,
                "hotspot_temperature_c": 99,
                "memory_temperature_c": 90,
                "load_percent": 97,
                "vram_used_mb": 7550,
                "vram_total_mb": 8176,
            },
            "disk": {
                "percent": 96.4,
            },
        },
        {
            "timestamp": "2026-09-10 15:00:20",
            "cpu": {
                "temperature_c": 94,
                "load_percent": 97,
                "ram_percent": 94,
            },
            "gpu": {
                "temperature_c": 86,
                "hotspot_temperature_c": 101,
                "memory_temperature_c": 92,
                "load_percent": 98,
                "vram_used_mb": 7600,
                "vram_total_mb": 8176,
            },
            "disk": {
                "percent": 96.8,
            },
        },
    ]


def main():
    history = build_test_history()

    results = analyze_history(history)

    total_findings = sum(
        len(result["findings"])
        for result in results
    )

    assert len(results) == 3
    assert total_findings == 21

    print("OK: 21 hallazgos detectados.")

    persistent = detect_persistent_anomalies(
        results,
        minimum_samples=3
    )

    assert len(persistent) == 7

    print("OK: 7 anomalías persistentes detectadas.")

    correlations = analyze_correlations(results)

    assert len(correlations) == 1
    assert correlations[0]["type"] == "GPU_THERMAL"

    print("OK: correlación térmica de GPU detectada.")

    recommendations = generate_recommendations(
        results,
        correlations
    )

    assert len(recommendations) == 8

    print("OK: 8 recomendaciones generadas.")

    components = [
        recommendation["component"]
        for recommendation in recommendations
    ]

    assert "CPU" in components
    assert "GPU" in components
    assert "RAM" in components
    assert "Disco" in components

    for recommendation in recommendations:
        assert recommendation.get("cause")
        assert recommendation.get("actions")

    print("OK: todas las recomendaciones contienen causa y acciones.")

    print("")
    print("==========================================")
    print(" TEST DE INTEGRACION: OK")
    print("==========================================")


if __name__ == "__main__":
    main()
