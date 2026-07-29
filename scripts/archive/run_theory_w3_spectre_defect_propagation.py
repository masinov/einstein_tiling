#!/usr/bin/env python
"""Classify local propagation of the three two-sided extra states."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json, minimum_colored_neighbor_cost,
)
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
TWO_SIDED = ROOT / "docs/notebook/assets/theory-w3-spectre-two-sided-overlap.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-defect-propagation.json"


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def main():
    control = json.loads(CONTROL.read_text())
    two_sided = json.loads(TWO_SIDED.read_text())
    generated = set(map(
        colored_corona_from_json, control["generated_colored_states"],
    ))
    records = two_sided["alphabet"]["observed_radius9_state_records"]
    observed = {colored_corona_from_json(row["state"]) for row in records}
    extras = observed - generated
    states = tuple(sorted(generated | extras, key=repr))
    extra_indices = {index for index, state in enumerate(states) if state in extras}
    costs = {index: int(index in extra_indices) for index in range(len(states))}
    rows = []
    for index in sorted(extra_indices):
        cost, witness = minimum_colored_neighbor_cost(states, index, costs)
        if cost is None or witness is None:
            raise ValueError("fixed-point survivor has no colored star")
        rows.append({
            "state_id": state_id(states[index]),
            "kind": states[index][0],
            "minimum_extra_neighbors": cost,
            "generated_only_star": cost == 0,
            "minimum_witness": [{
                "state_id": state_id(states[neighbor]),
                "source": (
                    "extra" if neighbor in extra_indices else "generated"
                ),
            } for neighbor in witness],
        })
    propagating = [row for row in rows if row["minimum_extra_neighbors"] > 0]
    absorbable = [row for row in rows if row["generated_only_star"]]
    artifact = {
        "schema": "einstein.w3.spectre-defect-propagation",
        "version": 1,
        "status": "LOCAL_DEFECT_SPLIT_ONE_ABSORBABLE_TWO_PROPAGATING",
        "provenance": {
            "control_source": str(CONTROL.relative_to(ROOT)),
            "control_sha256": file_sha256(CONTROL),
            "two_sided_source": str(TWO_SIDED.relative_to(ROOT)),
            "two_sided_sha256": file_sha256(TWO_SIDED),
        },
        "analysis": {
            "generated_states": len(generated),
            "extra_states": len(extras),
            "locally_absorbable_extra_states": len(absorbable),
            "locally_propagating_extra_states": len(propagating),
            "states": rows,
        },
        "claim_boundary": (
            "minimum cost is exact for one colored parent star; an absorbable "
            "star need not extend globally, while positive cost proves only "
            "that the defect cannot terminate at that single parent"
        ),
        "next_experiment": (
            "pin each extra at the root of a radius-two parent-state CSP and "
            "minimize extra states on the outer parent ring"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"extras={len(extras)} absorbable={len(absorbable)} "
        f"propagating={len(propagating)}; costs="
        f"{[row['minimum_extra_neighbors'] for row in rows]}"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
