from datetime import datetime


CORRELATION_WINDOW_SECONDS = 10


def parse_event_time(event):
    return datetime.strptime(
        event["TimeCreated"],
        "%Y-%m-%d %H:%M:%S"
    )


def build_event_summary(event):
    """Genera un resumen legible de un evento."""

    return {
        "provider": event.get("Provider", "Desconocido"),
        "event_id": event.get("Id", "Desconocido"),
        "time": event.get("TimeCreated", "Desconocido"),
        "level": event.get("Level", "Desconocido"),
        "message": event.get("Message", "")
    }

def calculate_incident_confidence(
    time_difference_seconds,
    whea_count=0,
    disk_count=0,
    ntfs_count=0
):
    """Calcula la confianza del diagnóstico de reinicio inesperado."""

    confidence = 60

    # Correlación temporal fuerte
    if time_difference_seconds <= 5:
        confidence += 20
    elif time_difference_seconds <= 10:
        confidence += 10

    # Evidencia adicional
    if whea_count > 0:
        confidence += 10

    if disk_count > 0:
        confidence += 5

    if ntfs_count > 0:
        confidence += 5

    return min(confidence, 100)

def correlate_events(events):
    """Correlaciona eventos relacionados temporalmente."""

    incidents = []

    boot_events = [
        event for event in events
        if event.get("Provider") == "Microsoft-Windows-Kernel-Boot"
        and event.get("Id") == 29
    ]

    power_events = [
        event for event in events
        if event.get("Provider") == "Microsoft-Windows-Kernel-Power"
        and event.get("Id") == 41
    ]

    used_power_events = set()

    for boot_event in boot_events:

        boot_time = parse_event_time(boot_event)

        for index, power_event in enumerate(power_events):

            if index in used_power_events:
                continue

            power_time = parse_event_time(power_event)

            time_difference = (
                power_time - boot_time
            ).total_seconds()

            if 0 <= time_difference <= CORRELATION_WINDOW_SECONDS:

                incidents.append({
                    "type": "UNEXPECTED_RESTART",
                    "severity": "HIGH",
                    "confidence": calculate_incident_confidence(
                        time_difference
                    ),

                    "events": [
                        build_event_summary(boot_event),
                        build_event_summary(power_event)
                    ],

                    "time_difference_seconds": time_difference,

                    "explanation": (
                        "Kernel-Boot 29 y Kernel-Power 41 "
                        "ocurrieron en la misma secuencia temporal."
                    )
                })

                used_power_events.add(index)

                break

    return incidents