def classify_incident(incident):
    """
    Clasifica posibles causas de un incidente utilizando
    únicamente la evidencia asociada al propio incidente.

    No determina una causa raíz definitiva.
    Genera hipótesis basadas en evidencia disponible.
    """

    classifications = []

    incident_type = incident.get("type")

    if incident_type != "UNEXPECTED_RESTART":
        return classifications

    events = incident.get("events", [])

    providers = {
        event.get("provider")
        for event in events
    }

    has_whea = "Microsoft-Windows-WHEA-Logger" in providers
    has_disk = "Disk" in providers
    has_ntfs = "Ntfs" in providers

    if has_whea:
        classifications.append({
            "cause": "POSSIBLE_HARDWARE_ERROR",
            "confidence": 80,
            "evidence": (
                "Se detectó un evento WHEA asociado al incidente."
            ),
            "explanation": (
                "La presencia de WHEA proporciona evidencia "
                "adicional de un posible problema de hardware."
            )
        })

    if has_disk:
        classifications.append({
            "cause": "POSSIBLE_STORAGE_ERROR",
            "confidence": 75,
            "evidence": (
                "Se detectó un evento Disk asociado al incidente."
            ),
            "explanation": (
                "La presencia de eventos Disk proporciona evidencia "
                "de un posible problema relacionado con almacenamiento."
            )
        })

    if has_ntfs:
        classifications.append({
            "cause": "POSSIBLE_FILESYSTEM_ERROR",
            "confidence": 70,
            "evidence": (
                "Se detectó un evento Ntfs asociado al incidente."
            ),
            "explanation": (
                "La presencia de eventos NTFS proporciona evidencia "
                "de un posible problema del sistema de archivos."
            )
        })

    if not classifications:
        classifications.append({
            "cause": "CAUSE_NOT_DETERMINED",
            "confidence": 40,
            "evidence": (
                "El incidente contiene Kernel-Boot 29 y "
                "Kernel-Power 41, pero no presenta evidencia "
                "adicional de WHEA, Disk o Ntfs."
            ),
            "explanation": (
                "El sistema sufrió un reinicio inesperado, "
                "pero los eventos disponibles no permiten "
                "determinar la causa raíz. Una pérdida de "
                "alimentación, bloqueo del sistema u otra causa "
                "siguen siendo posibilidades."
            )
        })

    return classifications