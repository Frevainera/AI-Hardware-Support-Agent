from typing import List, Dict, Any
from src.config import THRESHOLDS


def analyze_gpu_thermal_behavior(
    results: List[Dict[str, Any]],
    minimum_samples: int = 3
) -> List[Dict[str, Any]]:
    """
    Detecta un posible problema térmico de GPU cuando
    existe carga elevada y temperatura elevada durante
    varias muestras consecutivas.

    La correlación considera:

    - Carga de GPU
    - Temperatura del núcleo
    - Hot Spot
    - Temperatura de memoria
    """

    if not results:
        return []

    consecutive = 0

    for result in reversed(results):

        sample = result.get("sample", {})
        gpu = sample.get("gpu", {})

        gpu_load = gpu.get("load_percent")
        gpu_temperature = gpu.get("temperature_c")
        gpu_hotspot = gpu.get("hotspot_temperature_c")
        gpu_memory_temperature = gpu.get(
            "memory_temperature_c"
        )

        thermal_problem = (
            (
                gpu_temperature is not None
                and gpu_temperature >= THRESHOLDS[
                    "gpu_temperature_warning"
                ]
            )
            or
            (
                gpu_hotspot is not None
                and gpu_hotspot >= THRESHOLDS[
                    "gpu_hotspot_warning"
                ]
            )
            or
            (
                gpu_memory_temperature is not None
                and gpu_memory_temperature >= THRESHOLDS[
                    "gpu_memory_temperature_warning"
                ]
            )
        )

        if (
            gpu_load is not None
            and gpu_load >= THRESHOLDS["gpu_load_correlation"]
            and thermal_problem
        ):
            consecutive += 1

        else:
            break

    if consecutive < minimum_samples:
        return []

    latest_sample = results[-1].get("sample", {})
    gpu = latest_sample.get("gpu", {})

    return [
        {
            "type": "GPU_THERMAL",
            "severity": "WARNING",
            "timestamp": latest_sample.get("timestamp"),
            "consecutive_samples": consecutive,
            "gpu_load_percent": gpu.get("load_percent"),
            "gpu_temperature_c": gpu.get("temperature_c"),
            "gpu_hotspot_temperature_c": gpu.get(
                "hotspot_temperature_c"
            ),
            "gpu_memory_temperature_c": gpu.get(
                "memory_temperature_c"
            ),
            "message": (
                "Posible problema térmico de GPU: "
                "carga elevada y comportamiento térmico "
                "anómalo detectados de forma persistente."
            ),
        }
    ]


def analyze_correlations(
    results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Ejecuta las reglas de correlación disponibles.
    """

    correlations = []

    correlations.extend(
        analyze_gpu_thermal_behavior(results)
    )

    return correlations