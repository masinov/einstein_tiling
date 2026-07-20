#!/usr/bin/env python
"""Prune the complete radius-seven colored Spectre parent alphabet."""

from __future__ import annotations

import ast
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json,
    colored_edge_index,
    colored_local_overlap_witnesses,
    colored_reciprocal_domains,
    colored_transition_graph,
    prune_colored_unsupported,
    strongly_connected_components,
)
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
FRONTIER = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-frontier.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-overlap.json"


def parse_counter(rows):
    return {ast.literal_eval(key): int(count) for key, count in rows.items()}


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def histogram(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def main():
    control = json.loads(CONTROL.read_text())
    frontier = json.loads(FRONTIER.read_text())
    generated_control = set(map(
        colored_corona_from_json, control["generated_one_sided_states"],
    ))
    radius7 = frontier["radius7"]
    generated_counts = parse_counter(radius7["generated_colored_states"])
    extra_counts = parse_counter(radius7["extra_colored_states"])
    generated_frontier = set(generated_counts)
    extra_frontier = set(extra_counts)
    states = tuple(sorted(
        generated_control | generated_frontier | extra_frontier,
        key=repr,
    ))
    state_to_index = {state: index for index, state in enumerate(states)}
    edge_index = colored_edge_index(states)
    domains = tuple(
        colored_reciprocal_domains(
            states, index, edge_index=edge_index,
        )
        for index in range(len(states))
    )
    reciprocal_supported = {
        index for index, row in enumerate(domains) if all(row)
    }
    locally_supported = {
        index for index in reciprocal_supported
        if colored_local_overlap_witnesses(
            states, index, limit=1, edge_index=edge_index,
        )
    }
    alive, rounds = prune_colored_unsupported(states)
    alive_set = set(alive)
    generated_indices = {
        state_to_index[state]
        for state in generated_control | generated_frontier
    }
    extra_indices = {state_to_index[state] for state in extra_frontier}
    transition = colored_transition_graph(states, allowed=alive)
    components = strongly_connected_components(transition, allowed=alive)
    closed_components = tuple(
        component for component in components
        if not (
            {neighbor for index in component for neighbor in transition[index]}
            - set(component)
        )
    )

    def ids(indices):
        return [state_id(states[index]) for index in sorted(indices)]

    extras_surviving = extra_indices & alive_set
    generated_removed = generated_indices - alive_set
    if not extras_surviving and not generated_removed:
        verdict = "COLORED_RADIUS1_OVERLAP_ELIMINATES_ALL_EXTRA_STATES"
    else:
        verdict = "COLORED_RADIUS1_OVERLAP_LEAVES_A_FRONTIER"
    artifact = {
        "schema": "einstein.w3.spectre-colored-overlap",
        "version": 1,
        "status": verdict,
        "provenance": {
            "control_source": str(CONTROL.relative_to(ROOT)),
            "control_sha256": file_sha256(CONTROL),
            "frontier_source": str(FRONTIER.relative_to(ROOT)),
            "frontier_sha256": file_sha256(FRONTIER),
        },
        "alphabet": {
            "combined_states": len(states),
            "generated_control_states": len(generated_control),
            "generated_radius7_states": len(generated_frontier),
            "extra_radius7_states": len(extra_frontier),
            "control_equals_radius7_generated": (
                generated_control == generated_frontier
            ),
            "generated_extra_intersection": len(
                generated_frontier & extra_frontier
            ),
            "generated_occurrences": sum(generated_counts.values()),
            "extra_occurrences": sum(extra_counts.values()),
        },
        "reciprocal_edge_stage": {
            "supported_states": len(reciprocal_supported),
            "unsupported_state_ids": ids(
                set(range(len(states))) - reciprocal_supported
            ),
            "directed_domain_size_histogram": histogram(
                len(domain) for row in domains for domain in row
            ),
        },
        "colored_parent_star_stage": {
            "supported_states": len(locally_supported),
            "unsupported_state_ids": ids(
                set(range(len(states))) - locally_supported
            ),
        },
        "fixed_point": {
            "rounds": [ids(round_) for round_ in rounds],
            "surviving_states": len(alive),
            "surviving_generated_states": len(generated_indices & alive_set),
            "surviving_extra_states": len(extras_surviving),
            "surviving_extra_state_ids": ids(extras_surviving),
            "removed_generated_state_ids": ids(generated_removed),
        },
        "transition_sccs": {
            "component_count": len(components),
            "component_sizes": [len(component) for component in components],
            "closed_component_count": len(closed_components),
            "closed_component_sizes": [
                len(component) for component in closed_components
            ],
            "components": [{
                "state_ids": ids(component),
                "generated_states": len(set(component) & generated_indices),
                "extra_states": len(set(component) & extra_indices),
                "closed": component in closed_components,
            } for component in components],
        },
        "state_index": [
            {
                "id": state_id(state),
                "kind": state[0],
                "source": (
                    "generated" if index in generated_indices else "extra"
                ),
                "radius7_occurrences": (
                    generated_counts.get(state, 0) + extra_counts.get(state, 0)
                ),
            }
            for index, state in enumerate(states)
        ],
        "claim_boundary": (
            "fixed-point deletion is a rigorous necessary-condition test on "
            "the complete radius-seven colored parent alphabet; a surviving "
            "state is not by itself globally realizable"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"states={len(states)} generated={len(generated_indices)} "
        f"extra={len(extra_indices)}; reciprocal={len(reciprocal_supported)} "
        f"local={len(locally_supported)} fixed={len(alive)} "
        f"extra-fixed={len(extras_surviving)}"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
