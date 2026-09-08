from datetime import datetime


# ==========================================
# AI Hardware Support Agent
# Incident Correlator v0.5
# ==========================================


CORRELATION_WINDOW_SECONDS = 10


def parse_event_time(event):
    """Convierte TimeCreated de un evento a datetime."""

    return datetime.strptime(
        event["TimeCreated"],
        "%Y-%m-%d %H:%M:%S"
    )


def correlate_events(events):
    """
    Agrupa eventos relacionados en incidentes.

    Actualmente busca:
    Kernel-Boot 29 seguido de Kernel-Power 41
    dentro de una ventana de tiempo determinada.
    """

    incidents = []

    boot_events = [
        event
        for event in events
        if event.get("Provider") == "Microsoft-Windows-Kernel-Boot"
        and event.get("Id") == 29
    ]

    power_events = [
        event
        for event in events
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
                    "events": [
                        boot_event,
                        power_event
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