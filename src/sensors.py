import requests
import statistics


LHM_URL = "http://localhost:8085/data.json"


def get_sensor_data():
    """Obtiene los datos de sensores desde LibreHardwareMonitor."""

    response = requests.get(LHM_URL, timeout=5)
    response.raise_for_status()

    return response.json()


def find_sensor(data, sensor_id):
    """Busca un sensor específico utilizando su SensorId."""

    if isinstance(data, dict):

        if data.get("SensorId") == sensor_id:
            return data.get("Value")

        for child in data.get("Children", []):
            result = find_sensor(child, sensor_id)

            if result is not None:
                return result

    elif isinstance(data, list):

        for item in data:
            result = find_sensor(item, sensor_id)

            if result is not None:
                return result

    return None


def parse_value(value):
    """
    Convierte valores de LibreHardwareMonitor a números.

    Ejemplos:
        '35,0 °C' -> 35.0
        '4393,0 MHz' -> 4393.0
        '6,7 %' -> 6.7
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    try:
        text = str(value)

        number = text.split()[0]
        number = number.replace(",", ".")

        return float(number)

    except (ValueError, IndexError):
        return None


def get_core_clocks(data):
    """Obtiene las frecuencias de los seis núcleos del CPU."""

    clocks = []

    for core_number in range(1, 7):

        sensor_id = f"/intelcpu/0/clock/{core_number}"

        value = find_sensor(data, sensor_id)
        value = parse_value(value)

        if value is not None:
            clocks.append(value)

    return clocks


def get_hardware_sensors():
    """Obtiene y normaliza las métricas principales de CPU y GPU."""

    data = get_sensor_data()

    core_clocks = get_core_clocks(data)

    cpu_clock_average = None
    cpu_clock_max = None

    if core_clocks:
        cpu_clock_average = round(
            statistics.mean(core_clocks),
            1
        )

        cpu_clock_max = round(
            max(core_clocks),
            1
        )

    sensors = {
        "cpu": {
            "load_percent": parse_value(
                find_sensor(
                    data,
                    "/intelcpu/0/load/0"
                )
            ),

            "temperature_c": parse_value(
                find_sensor(
                    data,
                    "/intelcpu/0/temperature/8"
                )
            ),

            "average_temperature_c": parse_value(
                find_sensor(
                    data,
                    "/intelcpu/0/temperature/1"
                )
            ),

            "clock_average_mhz": cpu_clock_average,

            "clock_max_mhz": cpu_clock_max,
        },

        "gpu": {
            "load_percent": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/load/0"
                )
            ),

            "temperature_c": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/temperature/0"
                )
            ),

            "hotspot_temperature_c": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/temperature/7"
                )
            ),

            "memory_temperature_c": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/temperature/1"
                )
            ),

            "core_clock_mhz": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/clock/0"
                )
            ),

            "memory_clock_mhz": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/clock/2"
                )
            ),

            "vram_used_mb": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/smalldata/0"
                )
            ),

            "vram_free_mb": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/smalldata/1"
                )
            ),

            "vram_total_mb": parse_value(
                find_sensor(
                    data,
                    "/gpu-amd/0/smalldata/2"
                )
            ),
        },
    }

    return sensors


def main():

    print("")
    print("==========================================")
    print(" HARDWARE SENSORS TEST")
    print("==========================================")
    print("")

    sensors = get_hardware_sensors()

    cpu = sensors["cpu"]
    gpu = sensors["gpu"]

    print("CPU")
    print("------------------------------------------")

    print(f"Uso:                  {cpu['load_percent']} %")
    print(f"Temperatura:          {cpu['temperature_c']} °C")
    print(
        f"Temperatura promedio: "
        f"{cpu['average_temperature_c']} °C"
    )
    print(
        f"Frecuencia promedio:  "
        f"{cpu['clock_average_mhz']} MHz"
    )
    print(
        f"Frecuencia máxima:    "
        f"{cpu['clock_max_mhz']} MHz"
    )

    print("")

    print("GPU")
    print("------------------------------------------")

    print(f"Uso:                  {gpu['load_percent']} %")
    print(f"Temperatura:          {gpu['temperature_c']} °C")
    print(f"Hot Spot:             {gpu['hotspot_temperature_c']} °C")
    print(f"Memoria:              {gpu['memory_temperature_c']} °C")
    print(f"Core Clock:           {gpu['core_clock_mhz']} MHz")
    print(f"Memory Clock:         {gpu['memory_clock_mhz']} MHz")
    print(f"VRAM usada:           {gpu['vram_used_mb']} MB")
    print(f"VRAM libre:           {gpu['vram_free_mb']} MB")
    print(f"VRAM total:           {gpu['vram_total_mb']} MB")

    print("")


if __name__ == "__main__":
    main()