import json
import time
from datetime import datetime
from pathlib import Path

import psutil


BASE_DIR = Path(__file__).resolve().parent.parent
MONITORING_PATH = BASE_DIR / "data" / "monitoring_history.json"


def collect_metrics():
    """Recolecta métricas básicas del sistema."""

    memory = psutil.virtual_memory()

    metrics = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": memory.percent,
        "ram_available_gb": round(memory.available / (1024 ** 3), 2),
    }

    return metrics


def load_history():
    """Carga el historial de monitoreo."""

    if not MONITORING_PATH.exists():
        return []

    try:
        with open(MONITORING_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    """Guarda el historial de métricas."""

    with open(MONITORING_PATH, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


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

        print(
            f"[{sample_number}/{samples}] "
            f"CPU: {metrics['cpu_percent']}% | "
            f"RAM: {metrics['ram_percent']}% | "
            f"Disponible: {metrics['ram_available_gb']} GB"
        )

        if sample_number < samples:
            time.sleep(interval_seconds)


def main():
    print("")
    print("==========================================")
    print(" AI HARDWARE SUPPORT AGENT")
    print(" System Monitoring v0.6")
    print("==========================================")
    print("")

    monitor(interval_seconds=10, samples=5)

    print("")
    print(f"Historial guardado en: {MONITORING_PATH}")


if __name__ == "__main__":
    main()