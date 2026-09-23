import json
from pathlib import Path

from src import recommendations
from src.anomaly_detection import detect_persistent_anomalies
from src.correlation import analyze_correlations
from src.config import THRESHOLDS
from src.recommendations import generate_recommendations

BASE_DIR = Path(__file__).resolve().parent.parent
MONITORING_PATH = BASE_DIR / "data" / "monitoring_history.json"


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


def get_vram_usage_percent(gpu):
    """Calcula el porcentaje de VRAM utilizada."""

    total = gpu.get("vram_total_mb")
    used = gpu.get("vram_used_mb")

    if not total or used is None:
        return None

    return (used / total) * 100


def check_temperature(
    value,
    warning,
    critical,
    component,
    metric
):
    """Evalúa una temperatura."""

    if value is None:
        return None

    if value >= critical:
        return {
            "severity": "CRITICAL",
            "component": component,
            "metric": metric,
            "value": value,
            "message": (
                f"{component}: {metric} crítica "
                f"({value} °C)."
            ),
        }

    if value >= warning:
        return {
            "severity": "WARNING",
            "component": component,
            "metric": metric,
            "value": value,
            "message": (
                f"{component}: {metric} elevada "
                f"({value} °C)."
            ),
        }

    return None


def check_percentage(
    value,
    warning,
    critical,
    component,
    metric
):
    """Evalúa un porcentaje."""

    if value is None:
        return None

    if value >= critical:
        return {
            "severity": "CRITICAL",
            "component": component,
            "metric": metric,
            "value": value,
            "message": (
                f"{component}: {metric} crítica "
                f"({value:.1f} %)."
            ),
        }

    if value >= warning:
        return {
            "severity": "WARNING",
            "component": component,
            "metric": metric,
            "value": value,
            "message": (
                f"{component}: {metric} elevada "
                f"({value:.1f} %)."
            ),
        }

    return None


def analyze_sample(sample):
    """Analiza una muestra de monitoreo."""

    findings = []

    cpu = sample.get("cpu", {})
    gpu = sample.get("gpu", {})
    storage = sample.get("storage", {})
    disk = sample.get("disk", {})

    # CPU temperature
    finding = check_temperature(
        cpu.get("temperature_c"),
        THRESHOLDS["cpu_temperature_warning"],
        THRESHOLDS["cpu_temperature_critical"],
        "CPU",
        "temperatura"
    )

    if finding:
        findings.append(finding)

    # GPU temperature
    finding = check_temperature(
        gpu.get("temperature_c"),
        THRESHOLDS["gpu_temperature_warning"],
        THRESHOLDS["gpu_temperature_critical"],
        "GPU",
        "temperatura"
    )

    if finding:
        findings.append(finding)

    # GPU Hot Spot
    finding = check_temperature(
        gpu.get("hotspot_temperature_c"),
        THRESHOLDS["gpu_hotspot_warning"],
        THRESHOLDS["gpu_hotspot_critical"],
        "GPU",
        "Hot Spot"
    )

    if finding:
        findings.append(finding)

    # GPU memory temperature
    finding = check_temperature(
        gpu.get("memory_temperature_c"),
        THRESHOLDS["gpu_memory_temperature_warning"],
        THRESHOLDS["gpu_memory_temperature_critical"],
        "GPU",
        "temperatura de memoria"
    )

    if finding:
        findings.append(finding)

    # RAM
    finding = check_percentage(
        cpu.get("ram_percent"),
        THRESHOLDS["ram_warning"],
        THRESHOLDS["ram_critical"],
        "RAM",
        "uso"
    )

    if finding:
        findings.append(finding)

    # VRAM
    vram_percent = get_vram_usage_percent(gpu)

    finding = check_percentage(
        vram_percent,
        THRESHOLDS["vram_warning"],
        THRESHOLDS["vram_critical"],
        "VRAM",
        "uso"
    )

    if finding:
        findings.append(finding)

    # Disk
    finding = check_percentage(
        disk.get("percent"),
        THRESHOLDS["disk_warning"],
        THRESHOLDS["disk_critical"],
        "Disco",
        "espacio utilizado"
    )

    if finding:
        findings.append(finding)

    # SSD temperature
    finding = check_temperature(
        storage.get("ssd", {}).get("temperature_c"),
        THRESHOLDS["ssd_temperature_warning"],
        THRESHOLDS["ssd_temperature_critical"],
        "SSD",
        "temperatura"
    )

    if finding:
        findings.append(finding)

    # HDD temperature
    finding = check_temperature(
        storage.get("hdd", {}).get("temperature_c"),
        THRESHOLDS["hdd_temperature_warning"],
        THRESHOLDS["hdd_temperature_critical"],
        "HDD",
        "temperatura"
    )

    if finding:
        findings.append(finding)

    return findings


def analyze_history(history):
    """Analiza todas las muestras del historial."""

    results = []

    for sample in history:

        findings = analyze_sample(sample)

        results.append({
            "timestamp": sample.get("timestamp"),
            "sample": sample,
            "findings": findings
        })

    return results


def print_results(results):
    """Muestra los resultados del diagnóstico."""

    print("")
    print("==========================================")
    print(" DIAGNOSTICO DEL SISTEMA")
    print("==========================================")
    print("")

    total_findings = 0

    for result in results:

        timestamp = result["timestamp"]
        findings = result["findings"]

        print(f"Fecha: {timestamp}")

        if not findings:
            print("Estado: OK")

        else:

            for finding in findings:

                print(
                    f"[{finding['severity']}] "
                    f"{finding['message']}"
                )

                total_findings += 1

        print("")

    persistent_anomalies = detect_persistent_anomalies(
        results,
        minimum_samples=3
    )

    correlations = analyze_correlations(results)

    recommendations = generate_recommendations(
        results,
        correlations
    )

    print("------------------------------------------")
    print(f"Hallazgos: {total_findings}")
    print("------------------------------------------")
    print("")

    print("ANOMALIAS PERSISTENTES")
    print("------------------------------------------")

    if not persistent_anomalies:

        print("Ninguna anomalía persistente detectada.")

    else:

        for anomaly in persistent_anomalies:

            print(
                f"[{anomaly['severity']}] "
                f"{anomaly['message']}"
            )

    print("")

    print("CORRELACIONES")
    print("------------------------------------------")

    if not correlations:

        print("Ninguna correlación anómala detectada.")

    else:

        for correlation in correlations:

            print(
                f"[{correlation['severity']}] "
                f"{correlation['message']}"
            )

    print("")
    print("RECOMENDACIONES")
    print("------------------------------------------")

    if not recommendations:

        print("No se requieren recomendaciones.")

    else:

        for recommendation in recommendations:

            print(
                f"[{recommendation['priority']}] "
                f"{recommendation['component']}"
            )

            print(
                f"Causa: "
                f"{recommendation['cause']}"
            )

            print("Acciones:")

            for action in recommendation["actions"]:

                print(
                    f"  - {action}"
                )


            print("")

    print("")

def main():

    history = load_history()

    if not history:
        print("")
        print("No hay datos de monitoreo disponibles.")
        print("")
        return

    results = analyze_history(history)

    print_results(results)

if __name__ == "__main__":
    main()