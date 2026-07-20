#!/usr/bin/env python
"""Cold finite-state verifier for the two-sided Spectre interface result."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json, colored_transition_graph,
    prune_colored_unsupported, strongly_connected_components,
)
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-two-sided-overlap.json"


def main():
    artifact = json.loads(OUTPUT.read_text())
    provenance = artifact["provenance"]
    for prefix in ("component", "control"):
        path = ROOT / provenance[f"{prefix}_source"]
        assert file_sha256(path) == provenance[f"{prefix}_sha256"]
    control = json.loads(
        (ROOT / provenance["control_source"]).read_text()
    )
    generated = set(map(
        colored_corona_from_json, control["generated_colored_states"],
    ))
    records = artifact["alphabet"]["observed_radius9_state_records"]
    observed = {colored_corona_from_json(row["state"]) for row in records}
    assert sum(row["occurrences"] for row in records) == (
        artifact["alphabet"]["radius9_occurrences"]
    )
    states = tuple(sorted(generated | observed, key=repr))
    alive, rounds = prune_colored_unsupported(states)
    transition = colored_transition_graph(states, allowed=alive)
    components = strongly_connected_components(transition, allowed=alive)
    fixed = artifact["fixed_point"]
    assert len(states) == fixed["combined_states"]
    assert len(alive) == fixed["surviving_states"]
    assert len(rounds) == len(fixed["rounds"])
    assert [len(component) for component in components] == [
        row["size"] for row in artifact["transition_sccs"]
    ]
    extra = observed - generated
    alive_states = {states[index] for index in alive}
    assert len(extra & alive_states) == fixed["surviving_extra_states"]
    extension = artifact["extension"]
    complete = (
        extension["two_sided_unresolved"] == 0
        and extension["nongenerated_branch_contracts_to_generated"] == 0
    )
    assert complete
    expected = (
        "TWO_SIDED_OVERLAP_ELIMINATES_ALL_EXTRA_STATES"
        if not (extra & alive_states) and generated <= alive_states
        else "TWO_SIDED_OVERLAP_LEAVES_A_FRONTIER"
    )
    assert artifact["status"] == expected
    print(
        f"PASS two-sided overlap: {len(states)} states, "
        f"{len(extra & alive_states)} surviving extras"
    )


if __name__ == "__main__":
    main()
