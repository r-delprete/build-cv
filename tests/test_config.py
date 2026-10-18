import importlib
import sys
from pathlib import Path


def test_load_current_config(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["pytest", ".", "assets", "output.pdf"],
    )

    import config

    importlib.reload(config)

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    loaded_config = config.load_config(config_path)

    assert loaded_config.layout.page_size == "A4"
    assert loaded_config.typography.font_family == "Carlito"


def test_reject_unsupported_page_size(monkeypatch, tmp_path):
    import json

    import pytest

    monkeypatch.setattr(
        sys,
        "argv",
        ["pytest", ".", "assets", "output.pdf"],
    )

    import config

    importlib.reload(config)

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))

    data["layout"]["page_size"] = "INVALID"

    invalid_path = tmp_path / "invalid_config.json"
    invalid_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Page format not supported"):
        config.load_config(invalid_path)


def test_reject_missing_config_section(monkeypatch, tmp_path):
    import json

    import pytest

    monkeypatch.setattr(
        sys,
        "argv",
        ["pytest", ".", "assets", "output.pdf"],
    )

    import config

    importlib.reload(config)

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))

    del data["typography"]

    invalid_path = tmp_path / "missing_section.json"
    invalid_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing sections: typography"):
        config.load_config(invalid_path)


def test_reject_negative_margin(monkeypatch, tmp_path):
    import json

    import pytest

    monkeypatch.setattr(
        sys,
        "argv",
        ["pytest", ".", "assets", "output.pdf"],
    )

    import config

    importlib.reload(config)

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))

    data["layout"]["margin_left_mm"] = -1

    invalid_path = tmp_path / "negative_margin.json"
    invalid_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        config.load_config(invalid_path)


def test_reject_invalid_margin_type(monkeypatch, tmp_path):
    import json

    import pytest

    monkeypatch.setattr(
        sys,
        "argv",
        ["pytest", ".", "assets", "output.pdf"],
    )

    import config

    importlib.reload(config)

    config_path = Path(__file__).resolve().parents[1] / "config.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))

    data["layout"]["left_margin_mm"] = "invalid"

    invalid_path = tmp_path / "invalid_margin_type.json"
    invalid_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    with pytest.raises(TypeError):
        config.load_config(invalid_path)
