#!/usr/bin/env python
"""Cold verifier for the one-star Spectre defect-cost certificate."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from einstein.tilings.spectre.colored_interfaces import (
    colored_corona_from_json, minimum_colored_neighbor_cost,
)
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-defect-propagation.json"


def main():
    artifact = json.loads(OUTPUT.read_text())
    provenance = artifact["provenance"]
    for prefix in ("control", "two_sided"):
        path = ROOT / provenance[f"{prefix}_source"]
        assert file_sha256(path) == provenance[f"{prefix}_sha256"]
    control = json.loads((ROOT / provenance["control_source"]).read_text())
    two_sided = json.loads(
        (ROOT / provenance["two_sided_source"]).read_text()
    )
    generated = set(map(
        colored_corona_from_json, control["generated_colored_states"],
    ))
    observed = {
        colored_corona_from_json(row["state"])
        for row in two_sided["alphabet"]["observed_radius9_state_records"]
    }
    extras = observed - generated
    states = tuple(sorted(generated | extras, key=repr))
    extra_indices = {index for index, state in enumerate(states) if state in extras}
    costs = {index: int(index in extra_indices) for index in range(len(states))}
    verified = {}
    for index in sorted(extra_indices):
        cost, witness = minimum_colored_neighbor_cost(states, index, costs)
        assert witness is not None
        verified[sha256(repr(states[index]).encode()).hexdigest()[:16]] = cost
    recorded = {
        row["state_id"]: row["minimum_extra_neighbors"]
        for row in artifact["analysis"]["states"]
    }
    assert recorded == verified
    assert sorted(verified.values()) == [0, 1, 1]
    print("PASS defect propagation: exact one-star costs [0, 1, 1]")


if __name__ == "__main__":
    main()
