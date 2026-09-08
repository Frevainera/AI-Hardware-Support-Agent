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


if __name__ == "__main__":
    test_gpu_driver_change()
    print("TEST OK: cambio de driver detectado correctamente")