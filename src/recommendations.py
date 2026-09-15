from typing import List, Dict, Any


def generate_recommendations(
    results: List[Dict[str, Any]],
    correlations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Genera recomendaciones técnicas a partir de los
    hallazgos y correlaciones detectados.
    """

    recommendations = []

    if not results:
        return recommendations

    latest_result = results[-1]
    findings = latest_result.get("findings", [])

    checked = set()

    for finding in findings:

        component = finding.get("component")
        metric = finding.get("metric")

        key = (component, metric)

        if key in checked:
            continue

        checked.add(key)

        if component == "CPU" and metric == "temperatura":

            recommendations.append({
                "component": "CPU",
                "priority": finding.get("severity"),
                "cause": (
                    "Temperatura elevada del procesador."
                ),
                "actions": [
                    "Verificar el funcionamiento del cooler.",
                    "Comprobar el flujo de aire del gabinete.",
                    "Limpiar disipador y ventiladores.",
                    "Comprobar la temperatura bajo carga.",
                ],
            })

        elif component == "GPU" and metric == "temperatura":

            recommendations.append({
                "component": "GPU",
                "priority": finding.get("severity"),
                "cause": (
                    "Temperatura elevada de la GPU."
                ),
                "actions": [
                    "Verificar los ventiladores de la GPU.",
                    "Comprobar el flujo de aire del gabinete.",
                    "Limpiar disipador y ventiladores.",
                    "Comprobar la temperatura bajo carga.",
                ],
            })

        elif component == "GPU" and metric == "Hot Spot":

            recommendations.append({
                "component": "GPU",
                "priority": finding.get("severity"),
                "cause": (
                    "Hot Spot elevado en la GPU."
                ),
                "actions": [
                    "Comparar temperatura GPU vs Hot Spot.",
                    "Verificar distribución térmica del disipador.",
                    "Comprobar ventilación y flujo de aire.",
                    "Revisar pasta térmica y pads si corresponde.",
                ],
            })

        elif (
            component == "GPU"
            and metric == "temperatura de memoria"
        ):

            recommendations.append({
                "component": "GPU",
                "priority": finding.get("severity"),
                "cause": (
                    "Temperatura elevada de la memoria de video."
                ),
                "actions": [
                    "Verificar refrigeración de la VRAM.",
                    "Comprobar flujo de aire.",
                    "Limpiar el sistema de refrigeración.",
                    "Revisar pads térmicos si corresponde.",
                ],
            })

        elif component == "RAM" and metric == "uso":

            recommendations.append({
                "component": "RAM",
                "priority": finding.get("severity"),
                "cause": (
                    "Uso elevado de memoria RAM."
                ),
                "actions": [
                    "Identificar procesos con alto consumo de memoria.",
                    "Cerrar aplicaciones innecesarias.",
                    "Comprobar el consumo durante carga.",
                    "Evaluar si la capacidad instalada es suficiente.",
                ],
            })

        elif component == "VRAM" and metric == "uso":

            recommendations.append({
                "component": "GPU",
                "priority": finding.get("severity"),
                "cause": (
                    "Uso elevado de memoria de video."
                ),
                "actions": [
                    "Reducir la calidad de texturas si es necesario.",
                    "Reducir resolución o escala de renderizado.",
                    "Cerrar aplicaciones que utilicen GPU.",
                    "Comprobar el consumo de VRAM durante carga.",
                ],
            })

        elif (
            component == "Disco"
            and metric == "espacio utilizado"
        ):

            recommendations.append({
                "component": "Disco",
                "priority": finding.get("severity"),
                "cause": (
                    "Espacio de almacenamiento insuficiente."
                ),
                "actions": [
                    "Eliminar archivos innecesarios.",
                    "Vaciar archivos temporales.",
                    "Revisar aplicaciones y juegos instalados.",
                    "Mantener espacio libre para el correcto funcionamiento del sistema.",
                ],
            })

    # Recomendaciones derivadas de correlaciones
    for correlation in correlations:

        if correlation.get("type") == "GPU_THERMAL":

            recommendations.append({
                "component": "GPU",
                "priority": correlation.get("severity"),
                "cause": (
                    "Comportamiento térmico anómalo "
                    "durante carga elevada."
                ),
                "actions": [
                    "Verificar refrigeración de la GPU.",
                    "Comprobar ventiladores y flujo de aire.",
                    "Limpiar disipador y gabinete.",
                    "Realizar una prueba bajo carga controlada.",
                ],
            })

    return recommendations