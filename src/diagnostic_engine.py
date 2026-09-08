import json
from pathlib import Path


# ==========================================
# AI Hardware Support Agent
# Diagnostic Engine v0.1
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = BASE_DIR / "data" / "hardware_report.json"


def load_hardware_report():
    """Carga el informe generado por PowerShell."""

    with open(REPORT_PATH, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def add_diagnostic(diagnostics, status, problem, evidence, severity, explanation, recommendation):
    """Agrega un diagnóstico al resultado."""

    diagnostics.append({
        "status": status,
        "problem": problem,
        "evidence": evidence,
        "severity": severity,
        "explanation": explanation,
        "recommended_action": recommendation
    })
def analyze_system_status(data, diagnostics):
    """Analiza el uso actual de CPU y memoria RAM."""

    system_status = data.get("SystemStatus", {})

    cpu_usage = system_status.get("CPUUsagePercent")
    memory_usage = system_status.get("MemoryUsagePercent")

    # -------------------------
    # CPU
    # -------------------------

    if cpu_usage is not None:

        if cpu_usage > 95:
            add_diagnostic(
                diagnostics,
                "CRITICAL",
                "Uso de CPU extremadamente alto",
                f"Uso de CPU: {cpu_usage}%",
                "ALTA",
                "El procesador presenta una utilización extremadamente elevada en el momento de la medición.",
                "Identificar los procesos que están utilizando CPU y comprobar si el consumo persiste."
            )

        elif cpu_usage >= 80:
            add_diagnostic(
                diagnostics,
                "WARNING",
                "Uso elevado de CPU",
                f"Uso de CPU: {cpu_usage}%",
                "MEDIA",
                "El procesador presenta una utilización elevada en el momento de la medición.",
                "Comprobar procesos activos y realizar varias mediciones para determinar si el consumo es persistente."
            )

        else:
            add_diagnostic(
                diagnostics,
                "NORMAL",
                "Uso de CPU dentro de parámetros normales",
                f"Uso de CPU: {cpu_usage}%",
                "BAJA",
                "No se observa una utilización elevada del procesador en esta medición.",
                "No se requiere ninguna acción."
            )

    # -------------------------
    # RAM
    # -------------------------

    if memory_usage is not None:

        if memory_usage > 95:
            add_diagnostic(
                diagnostics,
                "CRITICAL",
                "Uso de memoria RAM extremadamente alto",
                f"Uso de RAM: {memory_usage}%",
                "ALTA",
                "La memoria disponible es muy limitada y podría provocar degradación del rendimiento.",
                "Identificar procesos con alto consumo de memoria y evaluar la ampliación de RAM si el problema persiste."
            )

        elif memory_usage >= 80:
            add_diagnostic(
                diagnostics,
                "WARNING",
                "Uso elevado de memoria RAM",
                f"Uso de RAM: {memory_usage}%",
                "MEDIA",
                "La memoria RAM presenta una utilización elevada en el momento de la medición.",
                "Comprobar procesos activos y observar si el consumo elevado es persistente."
            )

        else:
            add_diagnostic(
                diagnostics,
                "NORMAL",
                "Uso de memoria RAM dentro de parámetros normales",
                f"Uso de RAM: {memory_usage}%",
                "BAJA",
                "La utilización de memoria RAM no es elevada en esta medición.",
                "No se requiere ninguna acción."
            )

def analyze_cpu(data, diagnostics):
    """Analiza el procesador."""

    cpu = data.get("CPU", {})

    cores = cpu.get("Cores")
    logical_processors = cpu.get("LogicalProcessors")

    if cores is None or logical_processors is None:
        add_diagnostic(
            diagnostics,
            "WARNING",
            "Información incompleta del CPU",
            str(cpu),
            "MEDIA",
            "No se pudieron determinar correctamente los núcleos o procesadores lógicos.",
            "Verificar la información del procesador mediante CIM/WMI."
        )
        return

    if logical_processors < cores:
        add_diagnostic(
            diagnostics,
            "WARNING",
            "Cantidad de procesadores lógicos inconsistente",
            f"Núcleos: {cores} | Lógicos: {logical_processors}",
            "MEDIA",
            "La cantidad de procesadores lógicos no debería ser inferior a la cantidad de núcleos físicos.",
            "Revisar configuración de BIOS/UEFI y configuración de arranque de Windows."
        )
    else:
        add_diagnostic(
            diagnostics,
            "NORMAL",
            "Procesador detectado correctamente",
            f"Núcleos: {cores} | Procesadores lógicos: {logical_processors}",
            "BAJA",
            "La información básica del procesador es consistente.",
            "No se requiere ninguna acción."
        )


def analyze_ram(data, diagnostics):
    """Analiza la memoria RAM."""

    ram = data.get("RAM", {})
    total_gb = ram.get("TotalGB")

    if total_gb is None:
        add_diagnostic(
            diagnostics,
            "WARNING",
            "Información de RAM incompleta",
            str(ram),
            "MEDIA",
            "No se pudo determinar la cantidad de memoria RAM.",
            "Verificar la memoria mediante CIM/WMI."
        )
        return

    if total_gb < 8:
        status = "WARNING"
        severity = "MEDIA"
        explanation = "La cantidad de memoria detectada puede ser insuficiente para cargas de trabajo modernas."
        recommendation = "Considerar ampliar la memoria RAM."
    else:
        status = "NORMAL"
        severity = "BAJA"
        explanation = "La cantidad de memoria detectada es adecuada para un sistema de uso general."
        recommendation = "No se requiere ninguna acción."

    add_diagnostic(
        diagnostics,
        status,
        "Memoria RAM",
        f"RAM detectada: {total_gb} GB",
        severity,
        explanation,
        recommendation
    )


def analyze_gpu(data, diagnostics):
    """Analiza las GPU detectadas."""

    gpus = data.get("GPU", [])

    if not gpus:
        add_diagnostic(
            diagnostics,
            "WARNING",
            "No se detectaron GPU",
            "Lista de GPU vacía",
            "MEDIA",
            "El sistema no informó ningún adaptador gráfico.",
            "Verificar dispositivos gráficos y controladores."
        )
        return

    for gpu in gpus:
        name = gpu.get("Name", "GPU desconocida")
        driver = gpu.get("DriverVersion", "Desconocido")

        add_diagnostic(
            diagnostics,
            "NORMAL",
            "GPU detectada",
            f"{name} | Driver: {driver}",
            "BAJA",
            "El adaptador gráfico fue detectado correctamente.",
            "No se requiere ninguna acción."
        )


def analyze_disks(data, diagnostics):
    """Analiza los discos físicos."""

    disks = data.get("Disks", [])

    if not disks:
        add_diagnostic(
            diagnostics,
            "CRITICAL",
            "No se detectaron discos físicos",
            "Lista de discos vacía",
            "ALTA",
            "El sistema no informó ningún dispositivo de almacenamiento físico.",
            "Verificar conexiones, BIOS/UEFI y estado del almacenamiento."
        )
        return

    for disk in disks:
        model = disk.get("Model", "Disco desconocido")
        size_gb = disk.get("SizeGB", 0)

        add_diagnostic(
            diagnostics,
            "NORMAL",
            "Dispositivo de almacenamiento detectado",
            f"{model} | Capacidad: {size_gb} GB",
            "BAJA",
            "El dispositivo de almacenamiento fue detectado correctamente.",
            "No se requiere ninguna acción."
        )

def save_diagnostics_history(data, diagnostics, overall_status):
    """Guarda un snapshot completo del sistema y sus diagnósticos."""

    history_path = BASE_DIR / "data" / "diagnostics_history.json"

    history = []

    # Cargar historial existente
    if history_path.exists():
        try:
            with open(history_path, "r", encoding="utf-8") as file:
                history = json.load(file)
        except (json.JSONDecodeError, OSError):
            history = []

    # Crear snapshot completo
    entry = {
        "timestamp": __import__("datetime").datetime.now().isoformat(
            timespec="seconds"
        ),
        "hardware": data,
        "overall_status": overall_status,
        "diagnostics": diagnostics
    }

    history.append(entry)

    # Guardar historial actualizado
    with open(history_path, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

    return history_path
def calculate_overall_status(diagnostics):
    """Calcula el estado general del equipo."""

    normal = 0
    warning = 0
    critical = 0

    for diagnostic in diagnostics:
        status = diagnostic.get("status")

        if status == "NORMAL":
            normal += 1
        elif status == "WARNING":
            warning += 1
        elif status == "CRITICAL":
            critical += 1

    if critical > 0:
        overall_status = "CRITICAL"
        risk = "ALTO"
    elif warning > 0:
        overall_status = "WARNING"
        risk = "MEDIO"
    else:
        overall_status = "NORMAL"
        risk = "BAJO"

    return {
        "overall_status": overall_status,
        "risk": risk,
        "total_diagnostics": len(diagnostics),
        "normal": normal,
        "warning": warning,
        "critical": critical
    }

def run_diagnostics(data):
    """Ejecuta todas las reglas de diagnóstico."""

    diagnostics = []

    analyze_cpu(data, diagnostics)
    analyze_system_status(data, diagnostics)
    analyze_ram(data, diagnostics)
    analyze_gpu(data, diagnostics)
    analyze_disks(data, diagnostics)

    return diagnostics


def main():

    print("")
    print("==========================================")
    print(" AI HARDWARE SUPPORT AGENT")
    print(" Diagnostic Engine v0.1")
    print("==========================================")
    print("")

    try:
        data = load_hardware_report()
    except FileNotFoundError:
        print("ERROR: No se encontró hardware_report.json")
        return
    except json.JSONDecodeError:
        print("ERROR: El archivo JSON no es válido.")
        return

    diagnostics = run_diagnostics(data)

    overall_status = calculate_overall_status(diagnostics)

    history_path = save_diagnostics_history(
    data,
    diagnostics,
    overall_status
)

    print(f"Diagnósticos generados: {len(diagnostics)}")
    print("")
    print("ESTADO GENERAL DEL EQUIPO")
    print(f"Estado: {overall_status['overall_status']}")
    print(f"Riesgo: {overall_status['risk']}")
    print(f"Normal: {overall_status['normal']}")
    print(f"Warnings: {overall_status['warning']}")
    print(f"Críticos: {overall_status['critical']}")
    print("")
    print(f"Historial guardado en: {history_path}")
    print("")

    for number, diagnostic in enumerate(diagnostics, start=1):

        print(f"[{number}] {diagnostic['status']}")
        print(f"Problema: {diagnostic['problem']}")
        print(f"Evidencia: {diagnostic['evidence']}")
        print(f"Severidad: {diagnostic['severity']}")
        print(f"Explicación: {diagnostic['explanation']}")
        print(f"Acción recomendada: {diagnostic['recommended_action']}")
        print("-" * 50)


if __name__ == "__main__":
    main()