import json

from src.monitoring import (
    collect_metrics,
    load_history,
    save_history,
)


def test_collect_metrics():
    metrics = collect_metrics()

    assert "timestamp" in metrics
    assert "cpu_percent" in metrics
    assert "ram_percent" in metrics
    assert "ram_available_gb" in metrics

    assert 0 <= metrics["cpu_percent"] <= 100
    assert 0 <= metrics["ram_percent"] <= 100
    assert metrics["ram_available_gb"] >= 0


def test_save_and_load_history(tmp_path, monkeypatch):
    test_path = tmp_path / "monitoring_history.json"

    import src.monitoring as monitoring

    monkeypatch.setattr(
        monitoring,
        "MONITORING_PATH",
        test_path
    )

    history = [
        {
            "timestamp": "2026-09-08 15:00:00",
            "cpu_percent": 20.0,
            "ram_percent": 50.0,
            "ram_available_gb": 8.0,
        }
    ]

    save_history(history)

    loaded_history = load_history()

    assert loaded_history == history


def test_load_history_when_file_does_not_exist(tmp_path, monkeypatch):
    test_path = tmp_path / "nonexistent.json"

    import src.monitoring as monitoring

    monkeypatch.setattr(
        monitoring,
        "MONITORING_PATH",
        test_path
    )

    history = load_history()

    assert history == []


def test_load_history_when_json_is_invalid(tmp_path, monkeypatch):
    test_path = tmp_path / "invalid.json"

    test_path.write_text(
        "JSON INVALIDO",
        encoding="utf-8"
    )

    import src.monitoring as monitoring

    monkeypatch.setattr(
        monitoring,
        "MONITORING_PATH",
        test_path
    )

    history = load_history()

    assert history == []


if __name__ == "__main__":
    test_collect_metrics()

    print("")
    print("==========================================")
    print(" MONITORING TESTS")
    print("==========================================")
    print("")
    print("TODOS LOS TESTS OK")