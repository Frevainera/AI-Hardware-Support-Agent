import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MONITORING_PATH = BASE_DIR / "data" / "monitoring_history.json"


def load_monitoring_history():
    """Carga el historial de monitoreo."""

    if not MONITORING_PATH.exists():
        return []

    try:
        with open(MONITORING_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def calculate_statistics(history):
    """Calcula estadísticas básicas del historial."""

    if not history:
        return {}

    cpu_values = [
        sample["cpu_percent"]
        for sample in history
    ]

    ram_values = [
        sample["ram_percent"]
        for sample in history
    ]

    return {
        "samples": len(history),
        "cpu_average": round(sum(cpu_values) / len(cpu_values), 2),
        "cpu_min": min(cpu_values),
        "cpu_max": max(cpu_values),
        "ram_average": round(sum(ram_values) / len(ram_values), 2),
        "ram_min": min(ram_values),
        "ram_max": max(ram_values),
    }


def calculate_trend(values):
    """Determina si una métrica sube, baja o permanece estable."""

    if len(values) < 2:
        return "INSUFFICIENT_DATA"

    first = values[0]
    last = values[-1]

    difference = last - first

    if difference > 5:
        return "INCREASING"

    if difference < -5:
        return "DECREASING"

    return "STABLE"


def analyze_trends(history):
    """Analiza las tendencias de CPU y RAM."""

    if not history:
        return {}

    cpu_values = [
        sample["cpu_percent"]
        for sample in history
    ]

    ram_values = [
        sample["ram_percent"]
        for sample in history
    ]

    return {
        "cpu_trend": calculate_trend(cpu_values),
        "ram_trend": calculate_trend(ram_values),
    }


def generate_diagnostics(statistics, trends):
    """Genera diagnósticos basados en estadísticas y tendencias."""

    diagnostics = []

    if not statistics:
        return diagnostics

    if statistics["cpu_average"] >= 80:
        diagnostics.append({
            "component": "CPU",
            "status": "WARNING",
            "severity": "MEDIUM",
            "message": "El uso promedio de CPU es elevado.",
            "evidence": (
                f"Promedio: {statistics['cpu_average']}%"
            )
        })

    if statistics["ram_average"] >= 80:
        diagnostics.append({
            "component": "RAM",
            "status": "WARNING",
            "severity": "MEDIUM",
            "message": "El uso promedio de RAM es elevado.",
            "evidence": (
                f"Promedio: {statistics['ram_average']}%"
            )
        })

    if trends.get("cpu_trend") == "INCREASING":
        diagnostics.append({
            "component": "CPU",
            "status": "WARNING",
            "severity": "MEDIUM",
            "message": "Se observa una tendencia creciente en el uso de CPU.",
            "evidence": "La diferencia entre la primera y última muestra supera 5 puntos porcentuales."
        })

    if trends.get("ram_trend") == "INCREASING":
        diagnostics.append({
            "component": "RAM",
            "status": "WARNING",
            "severity": "MEDIUM",
            "message": "Se observa una tendencia creciente en el uso de RAM.",
            "evidence": "La diferencia entre la primera y última muestra supera 5 puntos porcentuales."
        })

    return diagnostics


def analyze_monitoring():
    """Ejecuta el análisis completo del historial."""

    history = load_monitoring_history()

    if not history:
        print("No hay datos de monitoreo disponibles.")
        return

    statistics = calculate_statistics(history)
    trends = analyze_trends(history)
    diagnostics = generate_diagnostics(statistics, trends)

    print("")
    print("==========================================")
    print(" MONITORING ANALYZER v0.6.1")
    print("==========================================")
    print("")

    print(f"Muestras analizadas: {statistics['samples']}")
    print("")
    print("CPU")
    print(f"  Promedio: {statistics['cpu_average']}%")
    print(f"  Mínimo:  {statistics['cpu_min']}%")
    print(f"  Máximo:  {statistics['cpu_max']}%")
    print(f"  Tendencia: {trends['cpu_trend']}")

    print("")
    print("RAM")
    print(f"  Promedio: {statistics['ram_average']}%")
    print(f"  Mínimo:  {statistics['ram_min']}%")
    print(f"  Máximo:  {statistics['ram_max']}%")
    print(f"  Tendencia: {trends['ram_trend']}")

    print("")
    print("DIAGNOSTICOS")

    if not diagnostics:
        print("  No se detectaron tendencias preocupantes.")
    else:
        for diagnostic in diagnostics:
            print(
                f"  [{diagnostic['severity']}] "
                f"{diagnostic['component']}: "
                f"{diagnostic['message']}"
            )
            print(f"  Evidencia: {diagnostic['evidence']}")


if __name__ == "__main__":
    analyze_monitoring()