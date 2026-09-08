import json
from pathlib import Path


# ==========================================
# AI Hardware Support Agent
# Change Detector v0.3
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_PATH = BASE_DIR / "data" / "diagnostics_history.json"


def load_history():
    """Carga el historial de diagnósticos."""

    if not HISTORY_PATH.exists():
        print("ERROR: No existe diagnostics_history.json")
        return []

    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("ERROR: El historial JSON no es válido.")
        return []

    except OSError as error:
        print(f"ERROR al leer el historial: {error}")
        return []


def compare_value(changes, component, previous, current):
    """Compara un valor y registra un cambio si existe."""

    if previous != current:
        changes.append({
            "component": component,
            "previous": previous,
            "current": current
        })

def classify_change_severity(change):
    """Clasifica la severidad de un cambio detectado."""

    component = change.get("component")
    change_type = change.get("type")

    # Cambios de driver
    if change_type == "DRIVER_CHANGE":
        return "LOW"

    # Hardware agregado
    if change_type == "HARDWARE_ADDED":

        if component == "GPU":
            return "MEDIUM"

        if component == "Disco":
            return "MEDIUM"

        return "MEDIUM"

    # Hardware eliminado
    if change_type == "HARDWARE_REMOVED":

        if component == "GPU":
            return "HIGH"

        if component == "Disco":
            return "HIGH"

        return "HIGH"

    # Cambios críticos de hardware
    if component == "CPU - Modelo":
        return "HIGH"

    if component == "Motherboard - Fabricante":
        return "HIGH"

    if component == "Motherboard - Modelo":
        return "HIGH"

    if component == "BIOS - Versión":
        return "HIGH"

    # Cambios de RAM
    if component == "RAM":
        return "MEDIUM"

    return "LOW"

def compare_hardware_list(changes, component, previous_items, current_items, key):
    """Detecta hardware agregado o eliminado."""

    previous_names = {
        item.get(key)
        for item in previous_items
        if item.get(key)
    }

    current_names = {
        item.get(key)
        for item in current_items
        if item.get(key)
    }

    added = current_names - previous_names
    removed = previous_names - current_names

    for name in sorted(added):
        changes.append({
            "component": component,
            "type": "HARDWARE_ADDED",
            "previous": None,
            "current": name
        })

    for name in sorted(removed):
        changes.append({
            "component": component,
            "type": "HARDWARE_REMOVED",
            "previous": name,
            "current": None
        })

def compare_hardware(previous, current):
    """Compara los principales componentes del hardware."""

    changes = []

    # CPU
    previous_cpu = previous.get("CPU", {})
    current_cpu = current.get("CPU", {})

    compare_value(
        changes,
        "CPU - Modelo",
        previous_cpu.get("Name"),
        current_cpu.get("Name")
    )

    compare_value(
        changes,
        "CPU - Núcleos",
        previous_cpu.get("Cores"),
        current_cpu.get("Cores")
    )

    compare_value(
        changes,
        "CPU - Procesadores lógicos",
        previous_cpu.get("LogicalProcessors"),
        current_cpu.get("LogicalProcessors")
    )

    # RAM
    previous_ram = previous.get("RAM", {})
    current_ram = current.get("RAM", {})

    compare_value(
        changes,
        "RAM",
        previous_ram.get("TotalGB"),
        current_ram.get("TotalGB")
    )

    # Motherboard
    previous_board = previous.get("Motherboard", {})
    current_board = current.get("Motherboard", {})

    compare_value(
        changes,
        "Motherboard - Fabricante",
        previous_board.get("Manufacturer"),
        current_board.get("Manufacturer")
    )

    compare_value(
        changes,
        "Motherboard - Modelo",
        previous_board.get("Product"),
        current_board.get("Product")
    )

    # BIOS
    previous_bios = previous.get("BIOS", {})
    current_bios = current.get("BIOS", {})

    compare_value(
        changes,
        "BIOS - Versión",
        previous_bios.get("Version"),
        current_bios.get("Version")
    )

    # GPU
    previous_gpus = previous.get("GPU", [])
    current_gpus = current.get("GPU", [])

    compare_hardware_list(
        changes,
        "GPU",
        previous_gpus,
        current_gpus,
        "Name"
    )

    # Comparar versiones de drivers
    compare_gpu_drivers(
        changes,
        previous_gpus,
        current_gpus
    )

    # Discos
    previous_disks = previous.get("Disks", [])
    current_disks = current.get("Disks", [])

    compare_hardware_list(
        changes,
        "Disco",
        previous_disks,
        current_disks,
        "Model"
    )

    return changes

def compare_gpu_drivers(changes, previous_gpus, current_gpus):
    """Compara las versiones de drivers de las GPU."""

    previous_drivers = {
        gpu.get("Name"): gpu.get("DriverVersion")
        for gpu in previous_gpus
    }

    current_drivers = {
        gpu.get("Name"): gpu.get("DriverVersion")
        for gpu in current_gpus
    }

    # Buscar GPUs presentes en ambas ejecuciones
    for gpu_name in current_drivers:

        if gpu_name in previous_drivers:

            previous_driver = previous_drivers[gpu_name]
            current_driver = current_drivers[gpu_name]

            if previous_driver != current_driver:

                changes.append({
                    "component": f"GPU - Driver ({gpu_name})",
                    "type": "DRIVER_CHANGE",
                    "previous": previous_driver,
                    "current": current_driver
                })

def main():

    print("")
    print("==========================================")
    print(" AI HARDWARE SUPPORT AGENT")
    print(" Change Detector v0.3")
    print("==========================================")
    print("")

    history = load_history()

    if len(history) < 2:
        print("No hay suficientes ejecuciones para comparar.")
        print("Se necesitan al menos 2 registros.")
        return

    # Buscar las últimas ejecuciones que tengan snapshot de hardware
    compatible_entries = [
        entry for entry in history
        if "hardware" in entry
    ]

    if len(compatible_entries) < 2:
        print("No hay suficientes snapshots de hardware compatibles.")
        print("Se necesitan al menos 2 ejecuciones compatibles.")
        return

    previous_entry = compatible_entries[-2]
    current_entry = compatible_entries[-1]

    previous_hardware = previous_entry.get("hardware", {})
    current_hardware = current_entry.get("hardware", {})

    print("Comparando:")
    print(f"Anterior → {previous_entry.get('timestamp')}")
    print(f"Actual   → {current_entry.get('timestamp')}")
    print("")

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    print(f"CAMBIOS DETECTADOS: {len(changes)}")
    print("")

    if not changes:

        print("CPU          → SIN CAMBIOS")
        print("RAM          → SIN CAMBIOS")
        print("Motherboard  → SIN CAMBIOS")
        print("BIOS         → SIN CAMBIOS")
        print("GPU          → SIN CAMBIOS")
        print("Discos       → SIN CAMBIOS")
        print("")
        print("Estado: SISTEMA ESTABLE")

    else:

        print("CAMBIOS ENCONTRADOS:")
        print("")

    for change in changes:

        severity = classify_change_severity(change)

        change["severity"] = severity

        print(f"Componente: {change['component']}")
        print(f"Tipo:       {change.get('type', 'HARDWARE_CHANGE')}")
        print(f"Severidad:  {severity}")
        print(f"Anterior:   {change['previous']}")
        print(f"Actual:     {change['current']}")
        print("-" * 50)


if __name__ == "__main__":
    main()