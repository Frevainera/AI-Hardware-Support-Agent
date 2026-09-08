from src.change_detector import (
    compare_hardware,
    classify_change_severity
)


def test_gpu_driver_change():

    previous_hardware = {
        "GPU": [
            {
                "Name": "AMD Radeon RX 5700 XT",
                "DriverVersion": "32.0.21045.5002"
            }
        ]
    }

    current_hardware = {
        "GPU": [
            {
                "Name": "AMD Radeon RX 5700 XT",
                "DriverVersion": "32.0.21050.5002"
            }
        ]
    }

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    assert len(changes) == 1
    assert changes[0]["type"] == "DRIVER_CHANGE"
    assert changes[0]["previous"] == "32.0.21045.5002"
    assert changes[0]["current"] == "32.0.21050.5002"


def test_gpu_added():

    previous_hardware = {
        "GPU": []
    }

    current_hardware = {
        "GPU": [
            {
                "Name": "AMD Radeon RX 5700 XT",
                "DriverVersion": "32.0.21045.5002"
            }
        ]
    }

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    assert len(changes) == 1
    assert changes[0]["component"] == "GPU"
    assert changes[0]["type"] == "HARDWARE_ADDED"
    assert changes[0]["previous"] is None
    assert changes[0]["current"] == "AMD Radeon RX 5700 XT"


def test_gpu_removed():

    previous_hardware = {
        "GPU": [
            {
                "Name": "AMD Radeon RX 5700 XT",
                "DriverVersion": "32.0.21045.5002"
            }
        ]
    }

    current_hardware = {
        "GPU": []
    }

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    assert len(changes) == 1
    assert changes[0]["component"] == "GPU"
    assert changes[0]["type"] == "HARDWARE_REMOVED"
    assert changes[0]["previous"] == "AMD Radeon RX 5700 XT"
    assert changes[0]["current"] is None


def test_disk_added():

    previous_hardware = {
        "Disks": []
    }

    current_hardware = {
        "Disks": [
            {
                "Model": "Samsung SSD 1TB"
            }
        ]
    }

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    assert len(changes) == 1
    assert changes[0]["component"] == "Disco"
    assert changes[0]["type"] == "HARDWARE_ADDED"
    assert changes[0]["previous"] is None
    assert changes[0]["current"] == "Samsung SSD 1TB"


def test_disk_removed():

    previous_hardware = {
        "Disks": [
            {
                "Model": "Samsung SSD 1TB"
            }
        ]
    }

    current_hardware = {
        "Disks": []
    }

    changes = compare_hardware(
        previous_hardware,
        current_hardware
    )

    assert len(changes) == 1
    assert changes[0]["component"] == "Disco"
    assert changes[0]["type"] == "HARDWARE_REMOVED"
    assert changes[0]["previous"] == "Samsung SSD 1TB"
    assert changes[0]["current"] is None

def test_severity_driver_change():

    change = {
        "component": "GPU - Driver (AMD Radeon RX 5700 XT)",
        "type": "DRIVER_CHANGE"
    }

    assert classify_change_severity(change) == "LOW"


def test_severity_gpu_added():

    change = {
        "component": "GPU",
        "type": "HARDWARE_ADDED"
    }

    assert classify_change_severity(change) == "MEDIUM"


def test_severity_gpu_removed():

    change = {
        "component": "GPU",
        "type": "HARDWARE_REMOVED"
    }

    assert classify_change_severity(change) == "HIGH"


def test_severity_disk_added():

    change = {
        "component": "Disco",
        "type": "HARDWARE_ADDED"
    }

    assert classify_change_severity(change) == "MEDIUM"


def test_severity_disk_removed():

    change = {
        "component": "Disco",
        "type": "HARDWARE_REMOVED"
    }

    assert classify_change_severity(change) == "HIGH"


def test_severity_cpu_change():

    change = {
        "component": "CPU - Modelo",
        "type": "HARDWARE_CHANGE"
    }

    assert classify_change_severity(change) == "HIGH"


def test_severity_bios_change():

    change = {
        "component": "BIOS - Versión",
        "type": "HARDWARE_CHANGE"
    }

    assert classify_change_severity(change) == "HIGH"


def test_severity_ram_change():

    change = {
        "component": "RAM",
        "type": "HARDWARE_CHANGE"
    }

    assert classify_change_severity(change) == "MEDIUM"

if __name__ == "__main__":
    test_gpu_driver_change()
    test_gpu_added()
    test_gpu_removed()
    test_disk_added()
    test_disk_removed()

    test_severity_driver_change()
    test_severity_gpu_added()
    test_severity_gpu_removed()
    test_severity_disk_added()
    test_severity_disk_removed()
    test_severity_cpu_change()
    test_severity_bios_change()
    test_severity_ram_change()

    print("TODOS LOS TESTS OK")