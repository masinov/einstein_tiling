#!/usr/bin/env python
"""Cold-check positive witnesses in the n<=8 isohedral control artifact."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.db import deserialize_cells
from einstein.funnel.a1_isohedral import (
    find_isohedral_surround,
    verify_isohedral_surround,
)
from einstein.funnel.a1_torus import verify_certificate


ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "docs/notebook/assets/a1-isohedral-control.json"


def main() -> None:
    payload = json.loads(ARTIFACT.read_text())
    assert payload["kind"] == "a1-isohedral-surround-control"
    assert payload["source_id"] == "kaplan-isohedral-sat-2024"
    assert payload["verdict"] == "pass"
    assert [row["isohedral"] for row in payload["rows"]] == [
        1, 1, 4, 4, 0, 70, 52, 37
    ]
    for record in payload["positive_certificates"]:
        shape = deserialize_cells(record["key"])
        assert verify_isohedral_surround(shape, record["certificate"])

    control = payload["periodic_anisohedral_control_n4"]
    shape = deserialize_cells(control["key"])
    assert verify_certificate(shape, control["periodic_certificate"])
    assert find_isohedral_surround(shape)["isohedral"] is False

    for control in payload["aperiodic_controls"].values():
        shape = deserialize_cells(control["key"])
        assert find_isohedral_surround(shape)["isohedral"] is False
    print("PASS: 169 isohedral witnesses, anisohedral split, Hat/Turtle controls")


if __name__ == "__main__":
    main()
