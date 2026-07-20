#!/usr/bin/env python
"""Independent verifier for the colored parent-overlap certificate."""

from __future__ import annotations

import ast
import json
from hashlib import sha256
from pathlib import Path

from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json, colored_transition_graph,
    prune_colored_unsupported, strongly_connected_components,
)
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-overlap.json"


def parse_states(rows):
    return {ast.literal_eval(key) for key in rows}


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def main():
    artifact = json.loads(OUTPUT.read_text())
    provenance = artifact["provenance"]
    control_path = ROOT / provenance["control_source"]
    frontier_path = ROOT / provenance["frontier_source"]
    assert file_sha256(control_path) == provenance["control_sha256"]
    assert file_sha256(frontier_path) == provenance["frontier_sha256"]
    control = json.loads(control_path.read_text())
    frontier = json.loads(frontier_path.read_text())["radius7"]
    generated_control = set(map(
        colored_corona_from_json, control["generated_one_sided_states"],
    ))
    generated = parse_states(frontier["generated_colored_states"])
    extra = parse_states(frontier["extra_colored_states"])
    states = tuple(sorted(generated_control | generated | extra, key=repr))
    alive, rounds = prune_colored_unsupported(states)
    transition = colored_transition_graph(states, allowed=alive)
    components = strongly_connected_components(transition, allowed=alive)
    generated_all = generated_control | generated
    alive_states = {states[index] for index in alive}
    alphabet = artifact["alphabet"]
    fixed = artifact["fixed_point"]
    assert alphabet["combined_states"] == len(states)
    assert alphabet["control_equals_radius7_generated"] == (
        generated_control == generated
    )
    assert alphabet["generated_extra_intersection"] == len(generated & extra)
    assert fixed["surviving_states"] == len(alive)
    assert fixed["surviving_generated_states"] == len(
        generated_all & alive_states
    )
    assert fixed["surviving_extra_states"] == len(extra & alive_states)
    assert set(fixed["surviving_extra_state_ids"]) == {
        state_id(state) for state in extra & alive_states
    }
    assert len(fixed["rounds"]) == len(rounds)
    assert artifact["transition_sccs"]["component_sizes"] == [
        len(component) for component in components
    ]
    expected = (
        "COLORED_RADIUS1_OVERLAP_ELIMINATES_ALL_EXTRA_STATES"
        if not (extra & alive_states) and generated_all <= alive_states
        else "COLORED_RADIUS1_OVERLAP_LEAVES_A_FRONTIER"
    )
    assert artifact["status"] == expected
    print(
        "PASS colored overlap: "
        f"{len(states)} states -> {len(alive)} fixed-point survivors; "
        f"extra survivors={len(extra & alive_states)}"
    )


if __name__ == "__main__":
    main()
