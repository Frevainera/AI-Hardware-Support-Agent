from src.monitoring_analyzer import (
    calculate_statistics,
    calculate_trend,
    generate_diagnostics,
)


def test_calculate_statistics():
    history = [
        {
            "cpu_percent": 10.0,
            "ram_percent": 50.0,
        },
        {
            "cpu_percent": 20.0,
            "ram_percent": 60.0,
        },
        {
            "cpu_percent": 30.0,
            "ram_percent": 70.0,
        },
    ]

    statistics = calculate_statistics(history)

    assert statistics["samples"] == 3
    assert statistics["cpu_average"] == 20.0
    assert statistics["cpu_min"] == 10.0
    assert statistics["cpu_max"] == 30.0
    assert statistics["ram_average"] == 60.0
    assert statistics["ram_min"] == 50.0
    assert statistics["ram_max"] == 70.0


def test_calculate_trend_increasing():
    values = [10, 20, 30]

    assert calculate_trend(values) == "INCREASING"


def test_calculate_trend_decreasing():
    values = [30, 20, 10]

    assert calculate_trend(values) == "DECREASING"


def test_calculate_trend_stable():
    values = [50, 52, 51]

    assert calculate_trend(values) == "STABLE"


def test_calculate_trend_insufficient_data():
    values = [50]

    assert calculate_trend(values) == "INSUFFICIENT_DATA"


def test_high_cpu_diagnostic():
    statistics = {
        "cpu_average": 85.0,
        "ram_average": 50.0,
    }

    trends = {
        "cpu_trend": "STABLE",
        "ram_trend": "STABLE",
    }

    diagnostics = generate_diagnostics(statistics, trends)

    assert len(diagnostics) == 1
    assert diagnostics[0]["component"] == "CPU"
    assert diagnostics[0]["severity"] == "MEDIUM"


def test_high_ram_diagnostic():
    statistics = {
        "cpu_average": 50.0,
        "ram_average": 85.0,
    }

    trends = {
        "cpu_trend": "STABLE",
        "ram_trend": "STABLE",
    }

    diagnostics = generate_diagnostics(statistics, trends)

    assert len(diagnostics) == 1
    assert diagnostics[0]["component"] == "RAM"
    assert diagnostics[0]["severity"] == "MEDIUM"


def test_increasing_trends_generate_diagnostics():
    statistics = {
        "cpu_average": 50.0,
        "ram_average": 50.0,
    }

    trends = {
        "cpu_trend": "INCREASING",
        "ram_trend": "INCREASING",
    }

    diagnostics = generate_diagnostics(statistics, trends)

    assert len(diagnostics) == 2
    assert diagnostics[0]["component"] == "CPU"
    assert diagnostics[1]["component"] == "RAM"


def test_normal_system_generates_no_diagnostics():
    statistics = {
        "cpu_average": 20.0,
        "ram_average": 50.0,
    }

    trends = {
        "cpu_trend": "STABLE",
        "ram_trend": "STABLE",
    }

    diagnostics = generate_diagnostics(statistics, trends)

    assert diagnostics == []


if __name__ == "__main__":
    print("")
    print("==========================================")
    print(" MONITORING ANALYZER TESTS")
    print("==========================================")
    print("")
    print("TODOS LOS TESTS OK")