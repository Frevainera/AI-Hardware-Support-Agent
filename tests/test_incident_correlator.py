from src.incident_correlator import correlate_events


def test_correlate_kernel_boot_and_power():

    events = [
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
        }
    ]

    incidents = correlate_events(events)

    assert len(incidents) == 1

    incident = incidents[0]

    assert incident["type"] == "UNEXPECTED_RESTART"
    assert incident["severity"] == "HIGH"
    assert incident["time_difference_seconds"] == 4


def test_two_separate_incidents():

    events = [
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
        },
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
        }
    ]

    incidents = correlate_events(events)

    assert len(incidents) == 2


def test_events_outside_correlation_window():

    events = [
        {
            "TimeCreated": "2026-09-05 11:17:01",
            "Id": 29,
            "Provider": "Microsoft-Windows-Kernel-Boot",
            "Level": "Error",
            "Message": "Fast Startup error"
        },
        {
            "TimeCreated": "2026-09-05 11:17:30",
            "Id": 41,
            "Provider": "Microsoft-Windows-Kernel-Power",
            "Level": "Critical",
            "Message": "Unexpected restart"
        }
    ]

    incidents = correlate_events(events)

    assert len(incidents) == 0


if __name__ == "__main__":

    test_correlate_kernel_boot_and_power()
    test_two_separate_incidents()
    test_events_outside_correlation_window()

    print("")
    print("==========================================")
    print(" INCIDENT CORRELATOR TESTS")
    print("==========================================")
    print("")
    print("TODOS LOS TESTS OK")