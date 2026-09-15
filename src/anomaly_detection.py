from typing import List, Dict, Any
from src.config import THRESHOLDS


def count_consecutive_findings(
    results: List[Dict[str, Any]],
    component: str,
    metric: str
) -> int:
    """
    Cuenta cuántas muestras consecutivas presentan
    un hallazgo para un componente y métrica determinados.

    El conteo se realiza desde la muestra más reciente
    hacia atrás.
    """

    consecutive = 0

    for result in reversed(results):

        findings = result.get("findings", [])

        found = any(
            finding.get("component") == component
            and finding.get("metric") == metric
            for finding in findings
        )

        if found:
            consecutive += 1
        else:
            break

    return consecutive


def detect_persistent_anomalies(
    results: List[Dict[str, Any]],
    minimum_samples: int = None
) -> List[Dict[str, Any]]:
    """
    Detecta anomalías que permanecen durante varias
    muestras consecutivas.
    """

    persistent = []

    if not results:
        return persistent

    if minimum_samples is None:
        minimum_samples = THRESHOLDS["persistent_samples"]

    latest_findings = results[-1].get("findings", [])

    checked = set()

    for finding in latest_findings:

        component = finding.get("component")
        metric = finding.get("metric")

        key = (component, metric)

        if key in checked:
            continue

        checked.add(key)

        consecutive = count_consecutive_findings(
            results,
            component,
            metric
        )

        if consecutive >= minimum_samples:

            persistent.append({
                "component": component,
                "metric": metric,
                "severity": finding.get("severity"),
                "consecutive_samples": consecutive,
                "message": (
                    f"{component}: {metric} "
                    f"persiste durante "
                    f"{consecutive} muestras consecutivas."
                )
            })

    return persistent