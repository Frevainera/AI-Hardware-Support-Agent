import json
import time
from datetime import datetime
from pathlib import Path

import psutil

from sensors import get_hardware_sensors


BASE_DIR = Path(__file__).resolve().parent.parent
MONITORING_PATH = BASE_DIR / "data" / "monitoring_history.json"


def get_disk_metrics():
    """Obtiene información del disco principal."""

    disk = psutil.disk_usage("C:\\")

    return {
        "total_gb": round(disk.total / (1024 ** 3), 2),
        "used_gb": round(disk.used / (1024 ** 3), 2),
        "free_gb": round(disk.free / (1024 ** 3), 2),
        "percent": disk.percent,
    }


def collect_metrics():
    """Recolecta métricas generales y sensores de hardware."""

    memory = psutil.virtual_memory()
    hardware = get_hardware_sensors()

    metrics = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "cpu": {
            "load_percent": psutil.cpu_percent(interval=1),
            "ram_percent": memory.percent,
            "ram_total_gb": round(
                memory.total / (1024 ** 3),
                2
            ),
            "ram_available_gb": round(
                memory.available / (1024 ** 3),
                2
            ),
            "temperature_c": hardware["cpu"]["temperature_c"],
            "average_temperature_c": hardware["cpu"][
                "average_temperature_c"
            ],
            "clock_average_mhz": hardware["cpu"][
                "clock_average_mhz"
            ],
            "clock_max_mhz": hardware["cpu"][
                "clock_max_mhz"
            ],
        },

        "gpu": {
            "load_percent": hardware["gpu"]["load_percent"],
            "temperature_c": hardware["gpu"]["temperature_c"],
            "hotspot_temperature_c": hardware["gpu"][
                "hotspot_temperature_c"
            ],
            "memory_temperature_c": hardware["gpu"][
                "memory_temperature_c"
            ],
            "core_clock_mhz": hardware["gpu"][
                "core_clock_mhz"
            ],
            "memory_clock_mhz": hardware["gpu"][
                "memory_clock_mhz"
            ],
            "vram_used_mb": hardware["gpu"]["vram_used_mb"],
            "vram_free_mb": hardware["gpu"]["vram_free_mb"],
            "vram_total_mb": hardware["gpu"]["vram_total_mb"],
        },

        "disk": get_disk_metrics(),
    }

    return metrics


def load_history():
    """Carga el historial de monitoreo."""

    if not MONITORING_PATH.exists():
        return []

    try:
        with open(
            MONITORING_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    """Guarda el historial de métricas."""

    MONITORING_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        MONITORING_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def collect_sample():
    """Recolecta y guarda una muestra."""

    history = load_history()
    metrics = collect_metrics()

    history.append(metrics)

    save_history(history)

    return metrics


def monitor(interval_seconds=10, samples=5):
    """Ejecuta el monitoreo durante una cantidad determinada de muestras."""

    print("")
    print("==========================================")
    print(" MONITOREO AUTOMATICO")
    print("==========================================")
    print("")
    print(f"Intervalo: {interval_seconds} segundos")
    print(f"Muestras: {samples}")
    print("")

    for sample_number in range(1, samples + 1):

        metrics = collect_sample()

        cpu = metrics["cpu"]
        gpu = metrics["gpu"]
        disk = metrics["disk"]

        print(
            f"[{sample_number}/{samples}] "
            f"CPU: {cpu['load_percent']}% | "
            f"CPU: {cpu['temperature_c']} °C | "
            f"Freq: {cpu['clock_average_mhz']} MHz | "
            f"RAM: {cpu['ram_percent']}% | "
            f"GPU: {gpu['load_percent']}% | "
            f"GPU Temp: {gpu['temperature_c']} °C | "
            f"Hot Spot: {gpu['hotspot_temperature_c']} °C | "
            f"VRAM: {gpu['vram_used_mb']}/"
            f"{gpu['vram_total_mb']} MB | "
            f"Disco: {disk['percent']}% usado"
        )

        if sample_number < samples:
            time.sleep(interval_seconds)


def main():

    print("")
    print("==========================================")
    print(" AI HARDWARE SUPPORT AGENT")
    print(" System Monitoring v0.6.2")
    print("==========================================")
    print("")

    monitor(
        interval_seconds=10,
        samples=5
    )

    print("")
    print(
        f"Historial guardado en: "
        f"{MONITORING_PATH}"
    )


if __name__ == "__main__":
    main()