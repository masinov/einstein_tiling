"""Cold structural checks for the Kaplan eight-kite benchmark crosswalk."""

import importlib.util
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "docs/notebook/assets/kaplan-8kite-crosswalk.json"


def load_runner():
    path = ROOT / "scripts" / "run_kaplan_8kite_crosswalk.py"
    spec = importlib.util.spec_from_file_location("kaplan_crosswalk", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_exact_cell_coordinate_conversion():
    runner = load_runner()
    for direction, point in enumerate(runner.ORIGINS):
        assert runner.kaplan_point_to_cell(point) == (0, 0, direction)


def test_crosswalk_is_a_database_bijection_with_expected_roles():
    payload = json.loads(ARTIFACT.read_text())
    records = payload["records"]
    assert payload["unique_bijection"] is True
    assert payload["source_pages"] == 116
    assert payload["counts"] == {
        "hc1": 108,
        "hc2": 5,
        "periodic_anisohedral": 2,
        "hat": 1,
    }
    assert len(records) == len({record["key"] for record in records}) == 116
    assert [
        (record["page"], record["shape_id"], record["role"])
        for record in records
        if record["kaplan_status"] == "inconclusive"
    ] == [
        (32, 506, "periodic-anisohedral"),
        (47, 793, "periodic-anisohedral"),
        (50, 635, "hat"),
    ]

    fixture = ROOT / "tests/fixtures/polykites-n8.sqlite"
    conn = sqlite3.connect(f"{fixture.resolve().as_uri()}?mode=ro", uri=True)
    for record in records:
        row = conn.execute(
            "SELECT key, n FROM shapes WHERE id=?", (record["shape_id"],)
        ).fetchone()
        assert row == (record["key"], 8)
    conn.close()
