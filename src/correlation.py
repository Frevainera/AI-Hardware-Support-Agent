from typing import List, Dict, Any
from src.config import THRESHOLDS


def analyze_gpu_thermal_behavior(
    results: List[Dict[str, Any]],
    minimum_samples: int = 3
) -> List[Dict[str, Any]]:
    """
    Detecta un posible problema térmico de GPU cuando
    existe alta carga y temperatura elevada durante
    varias muestras consecutivas.
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

        if (
            gpu_load is not None
            and gpu_temperature is not None
            and gpu_hotspot is not None
            and gpu_load >= THRESHOLDS["gpu_load_correlation"]
            and (
                gpu_temperature >= THRESHOLDS["gpu_temperature_warning"]
                or gpu_hotspot >= THRESHOLDS["gpu_hotspot_warning"]
            )
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
            "message": (
                "Posible problema térmico de GPU: "
                "carga elevada y temperatura alta "
                "detectadas de forma persistente."
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