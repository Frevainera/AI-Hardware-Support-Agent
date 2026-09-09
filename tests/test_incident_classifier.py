from src.incident_classifier import classify_incident


def test_hardware_classification():
    incident = {
        "type": "UNEXPECTED_RESTART",
        "events": [
            {
                "provider": "Microsoft-Windows-WHEA-Logger"
            }
        ]
    }

    classifications = classify_incident(incident)

    hardware = next(
        item for item in classifications
        if item["cause"] == "POSSIBLE_HARDWARE_ERROR"
    )

    assert hardware["confidence"] == 80


def test_storage_classification():
    incident = {
        "type": "UNEXPECTED_RESTART",
        "events": [
            {
                "provider": "Disk"
            }
        ]
    }

    classifications = classify_incident(incident)

    storage = next(
        item for item in classifications
        if item["cause"] == "POSSIBLE_STORAGE_ERROR"
    )

    assert storage["confidence"] == 75


def test_filesystem_classification():
    incident = {
        "type": "UNEXPECTED_RESTART",
        "events": [
            {
                "provider": "Ntfs"
            }
        ]
    }

    classifications = classify_incident(incident)

    filesystem = next(
        item for item in classifications
        if item["cause"] == "POSSIBLE_FILESYSTEM_ERROR"
    )

    assert filesystem["confidence"] == 70


def test_no_additional_hardware_evidence():
    incident = {
        "type": "UNEXPECTED_RESTART",
        "events": [
            {
                "provider": "Microsoft-Windows-Kernel-Boot"
            },
            {
                "provider": "Microsoft-Windows-Kernel-Power"
            }
        ]
    }

    classifications = classify_incident(incident)

    assert len(classifications) == 1
    assert classifications[0]["cause"] == "CAUSE_NOT_DETERMINED"
    assert classifications[0]["confidence"] == 40


if __name__ == "__main__":
    test_hardware_classification()
    test_storage_classification()
    test_filesystem_classification()
    test_no_additional_hardware_evidence()

    print("")
    print("==========================================")
    print(" INCIDENT CLASSIFIER TESTS")
    print("==========================================")
    print("")
    print("TODOS LOS TESTS OK")