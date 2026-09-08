from src.change_detector import compare_hardware


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


if __name__ == "__main__":
    test_gpu_driver_change()
    test_gpu_added()
    test_gpu_removed()
    test_disk_added()
    test_disk_removed()

    print("TODOS LOS TESTS OK")