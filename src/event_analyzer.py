import json
from pathlib import Path


# ==========================================
# AI Hardware Support Agent
# Event Analyzer v0.4.1
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
EVENT_LOG_PATH = BASE_DIR / "data" / "event_log_report.json"


def load_event_report():
    """Carga el informe de eventos de Windows."""

    if not EVENT_LOG_PATH.exists():
        print("ERROR: No existe event_log_report.json")
        return {}

    try:
        with open(
            EVENT_LOG_PATH,
            "r",
            encoding="utf-8-sig"
        ) as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("ERROR: El informe de eventos no es válido.")
        return {}

    except OSError as error:
        print(f"ERROR al leer el informe: {error}")
        return {}

def classify_event_severity(component):
    """Clasifica la severidad de un tipo de evento."""

    severity_map = {
        "Kernel-Power": "HIGH",
        "Kernel-Boot": "MEDIUM",
        "WHEA": "HIGH",
        "Disk": "HIGH",
        "Ntfs": "MEDIUM"
    }

    return severity_map.get(component, "LOW")

def add_event_diagnostic(
    diagnostics,
    component,
    status,
    severity,
    message,
    evidence
):
    """Agrega un diagnóstico basado en eventos."""

    diagnostics.append({
        "component": component,
        "status": status,
        "severity": severity,
        "message": message,
        "evidence": evidence
    })


def analyze_kernel_power(report, diagnostics):
    """Analiza eventos Kernel-Power 41."""

    count = report.get(
        "EventCounts",
        {}
    ).get("KernelPower41", 0)

    if count > 0:

        add_event_diagnostic(
            diagnostics,
            "Kernel-Power",
            "WARNING",
            "HIGH",
            "Se detectaron reinicios inesperados del sistema.",
            f"Kernel-Power ID 41 detectado {count} veces en los últimos 7 días."
        )

    else:

        add_event_diagnostic(
            diagnostics,
            "Kernel-Power",
            "NORMAL",
            "LOW",
            "No se detectaron reinicios inesperados.",
            "Kernel-Power ID 41: 0 eventos."
        )


def analyze_kernel_boot(report, diagnostics):
    """Analiza eventos Kernel-Boot 29."""

    count = report.get(
        "EventCounts",
        {}
    ).get("KernelBoot29", 0)

    if count > 0:

        add_event_diagnostic(
            diagnostics,
            "Kernel-Boot",
            "WARNING",
            "MEDIUM",
            "Se detectaron errores relacionados con Windows Fast Startup.",
            f"Kernel-Boot ID 29 detectado {count} veces."
        )

    else:

        add_event_diagnostic(
            diagnostics,
            "Kernel-Boot",
            "NORMAL",
            "LOW",
            "No se detectaron errores Kernel-Boot ID 29.",
            "Kernel-Boot ID 29: 0 eventos."
        )


def analyze_whea(report, diagnostics):
    """Analiza eventos WHEA."""

    count = report.get(
        "EventCounts",
        {}
    ).get("WHEA", 0)

    if count > 0:

        add_event_diagnostic(
            diagnostics,
            "WHEA",
            "WARNING",
            "HIGH",
            "Se detectaron eventos relacionados con errores de hardware.",
            f"WHEA-Logger: {count} eventos detectados."
        )

    else:

        add_event_diagnostic(
            diagnostics,
            "WHEA",
            "NORMAL",
            "LOW",
            "No se detectaron errores WHEA.",
            "WHEA-Logger: 0 eventos."
        )


def analyze_disk(report, diagnostics):
    """Analiza eventos Disk."""

    count = report.get(
        "EventCounts",
        {}
    ).get("Disk", 0)

    if count > 0:

        add_event_diagnostic(
            diagnostics,
            "Disk",
            "WARNING",
            "HIGH",
            "Se detectaron eventos relacionados con discos.",
            f"Disk: {count} eventos detectados."
        )

    else:

        add_event_diagnostic(
            diagnostics,
            "Disk",
            "NORMAL",
            "LOW",
            "No se detectaron errores del controlador de disco.",
            "Disk: 0 eventos."
        )


def analyze_ntfs(report, diagnostics):
    """Analiza eventos NTFS."""

    count = report.get(
        "EventCounts",
        {}
    ).get("Ntfs", 0)

    if count > 0:

        add_event_diagnostic(
            diagnostics,
            "Ntfs",
            "WARNING",
            "MEDIUM",
            "Se detectaron eventos relacionados con el sistema de archivos.",
            f"Ntfs: {count} eventos detectados."
        )

    else:

        add_event_diagnostic(
            diagnostics,
            "Ntfs",
            "NORMAL",
            "LOW",
            "No se detectaron errores NTFS.",
            "Ntfs: 0 eventos."
        )


def analyze_events(report):
    """Ejecuta todos los análisis de eventos."""

    diagnostics = []

    analyze_kernel_power(
        report,
        diagnostics
    )

    analyze_kernel_boot(
        report,
        diagnostics
    )

    analyze_whea(
        report,
        diagnostics
    )

    analyze_disk(
        report,
        diagnostics
    )

    analyze_ntfs(
        report,
        diagnostics
    )

    return diagnostics


def main():

    print("")
    print("==========================================")
    print(" AI HARDWARE SUPPORT AGENT")
    print(" Event Analyzer v0.4.1")
    print("==========================================")
    print("")

    report = load_event_report()

    if not report:
        return

    diagnostics = analyze_events(report)

    print(
        f"Diagnósticos de eventos generados: "
        f"{len(diagnostics)}"
    )

    print("")

    for diagnostic in diagnostics:

        print(
            f"[{diagnostic['severity']}] "
            f"{diagnostic['component']}"
        )

        print(
            f"Estado: {diagnostic['status']}"
        )

        print(
            f"Mensaje: {diagnostic['message']}"
        )

        print(
            f"Evidencia: {diagnostic['evidence']}"
        )

        print("-" * 50)


if __name__ == "__main__":
    main()