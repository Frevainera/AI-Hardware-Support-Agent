from src.event_analyzer import (
    analyze_events,
    classify_event_severity
)


def test_severity_classification():

    assert classify_event_severity("Kernel-Power") == "HIGH"
    assert classify_event_severity("Kernel-Boot") == "MEDIUM"
    assert classify_event_severity("WHEA") == "HIGH"
    assert classify_event_severity("Disk") == "HIGH"
    assert classify_event_severity("Ntfs") == "MEDIUM"


def test_no_hardware_errors():

    report = {
        "EventCounts": {
            "KernelPower41": 0,
            "KernelBoot29": 0,
            "WHEA": 0,
            "Disk": 0,
            "Ntfs": 0
        }
    }

    diagnostics = analyze_events(report)

    assert len(diagnostics) == 5

    for diagnostic in diagnostics:
        assert diagnostic["status"] == "NORMAL"


def test_unexpected_restarts():

    report = {
        "EventCounts": {
            "KernelPower41": 2,
            "KernelBoot29": 2,
            "WHEA": 0,
            "Disk": 0,
            "Ntfs": 0
        },
        "RelevantEvents": [
            {
                "TimeCreated": "2026-09-05 11:17:01",
                "Id": 29,
                "Provider": "Microsoft-Windows-Kernel-Boot",
                "Level": "Error",
                "Message": "Fast Startup error"
            },
            {
                "TimeCreated": "2026-09-05 11:17:05",
                "Id": 41,
                "Provider": "Microsoft-Windows-Kernel-Power",
                "Level": "Critical",
                "Message": "Unexpected restart"
            },
            {
                "TimeCreated": "2026-09-04 05:53:08",
                "Id": 29,
                "Provider": "Microsoft-Windows-Kernel-Boot",
                "Level": "Error",
                "Message": "Fast Startup error"
            },
            {
                "TimeCreated": "2026-09-04 05:53:11",
                "Id": 41,
                "Provider": "Microsoft-Windows-Kernel-Power",
                "Level": "Critical",
                "Message": "Unexpected restart"
            }
        ]
    }

    diagnostics = analyze_events(report)

    incidents = [
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "Incident-Correlator"
    ]

    kernel_power = [
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "Kernel-Power"
    ]

    kernel_boot = [
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "Kernel-Boot"
    ]

    assert len(incidents) == 2

    assert "Confianza: 80%" in incidents[0]["evidence"]
    assert "Confianza: 80%" in incidents[1]["evidence"]
    assert len(kernel_power) == 0
    assert len(kernel_boot) == 0


def test_hardware_events():

    report = {
        "EventCounts": {
            "KernelPower41": 0,
            "KernelBoot29": 0,
            "WHEA": 1,
            "Disk": 1,
            "Ntfs": 1
        }
    }

    diagnostics = analyze_events(report)

    whea = next(
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "WHEA"
    )

    disk = next(
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "Disk"
    )

    ntfs = next(
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["component"] == "Ntfs"
    )

    assert whea["severity"] == "HIGH"
    assert disk["severity"] == "HIGH"
    assert ntfs["severity"] == "MEDIUM"


if __name__ == "__main__":

    test_severity_classification()
    test_no_hardware_errors()
    test_unexpected_restarts()
    test_hardware_events()

    print("")
    print("==========================================")
    print(" EVENT ANALYZER TESTS")
    print("==========================================")
    print("")
    print("TODOS LOS TESTS OK")