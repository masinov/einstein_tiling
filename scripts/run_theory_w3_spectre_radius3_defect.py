#!/usr/bin/env python
"""Extend every pinned Spectre defect through parent radius three."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json, colored_local_overlap_witnesses,
)
from einstein.theory.spectre_parent_csp import ParentStateKernel
from einstein.theory.spectre_parent_overlap import parent_templates
from einstein.theory.spectre_patch_language import IDENTITY, pose_json
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
A6 = ROOT / "docs/notebook/assets/a6-spectre-results.json"
CONTROL = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
TWO_SIDED = ROOT / "docs/notebook/assets/theory-w3-spectre-two-sided-overlap.json"
RADIUS2 = ROOT / "docs/notebook/assets/theory-w3-spectre-radius2-defect.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius3-defect.json"


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def histogram(values):
    return {str(key): count for key, count in sorted(Counter(values).items())}


def main():
    control = json.loads(CONTROL.read_text())
    two_sided = json.loads(TWO_SIDED.read_text())
    radius2 = json.loads(RADIUS2.read_text())
    a6 = json.loads(A6.read_text())
    generated = set(map(
        colored_corona_from_json, control["generated_colored_states"],
    ))
    observed = {
        colored_corona_from_json(row["state"])
        for row in two_sided["alphabet"]["observed_radius9_state_records"]
    }
    extras = observed - generated
    states = tuple(sorted(generated | extras, key=repr))
    by_id = {state_id(state): index for index, state in enumerate(states)}
    extra_indices = {index for index, state in enumerate(states) if state in extras}
    kernel = ParentStateKernel(states, parent_templates(a6))
    roots = []
    for radius2_root in radius2["roots"]:
        root_index = by_id[radius2_root["root_state_id"]]
        root_witnesses = colored_local_overlap_witnesses(
            states, root_index, limit=1_000_000,
        )
        witness = root_witnesses[radius2_root["best_witness_index"]]
        problem2 = kernel.build_radius_two(root_index, witness)
        assignments2 = kernel.enumerate_assignments(problem2)
        if len(assignments2) != radius2_root["complete_assignment_count"]:
            raise ValueError("radius-two assignment count changed")
        cases = []
        survivors = []
        for assignment_index, assignment2 in enumerate(assignments2):
            problem3 = kernel.extend_fixed_assignment(problem2, assignment2)
            result = kernel.solve_radius_two(problem3, extra_indices)
            fixed_defects = [
                (position, state_index)
                for position, state_index in zip(problem2.positions, assignment2)
                if state_index in extra_indices
            ]
            cases.append({
                "radius2_assignment_index": assignment_index,
                "positions": len(problem3.positions),
                "third_ring": len(problem3.second_ring),
                "satisfiable": result.satisfiable,
                "minimum_third_ring_extras": result.minimum_outer_extras,
                "minimum_nonroot_extras": result.minimum_nonroot_extras,
                "fixed_defect_state_ids": sorted(
                    state_id(states[state_index])
                    for _, state_index in fixed_defects
                ),
                "search_nodes": result.search_nodes,
            })
            if not result.satisfiable:
                continue
            first = set(problem2.first_ring)
            second = set(problem2.second_ring)
            third = set(problem3.second_ring)
            survivors.append({
                "radius2_assignment_index": assignment_index,
                "minimum_third_ring_extras": result.minimum_outer_extras,
                "minimum_nonroot_extras": result.minimum_nonroot_extras,
                "fixed_defects": [{
                    "position": pose_json(position),
                    "ring": 0 if position == IDENTITY
                    else 1 if position in first else 2,
                    "state_id": state_id(states[state_index]),
                } for position, state_index in fixed_defects],
                "witness_assignment": [{
                    "position": pose_json(position),
                    "ring": 0 if position == IDENTITY
                    else 1 if position in first
                    else 2 if position in second
                    else 3 if position in third else None,
                    "state_id": state_id(states[state_index]),
                    "source": (
                        "extra" if state_index in extra_indices else "generated"
                    ),
                } for position, state_index in zip(
                    problem3.positions, result.assignment,
                )],
            })
        roots.append({
            "root_state_id": radius2_root["root_state_id"],
            "radius2_assignments": len(assignments2),
            "radius3_satisfiable": len(survivors),
            "position_count_histogram": histogram(
                case["positions"] for case in cases
            ),
            "third_ring_count_histogram": histogram(
                case["third_ring"] for case in cases
            ),
            "minimum_third_ring_extra_histogram": histogram(
                case["minimum_third_ring_extras"]
                for case in cases if case["satisfiable"]
            ),
            "survivors": survivors,
            "cases": cases,
        })

    dead_roots = {
        root["root_state_id"] for root in roots
        if root["radius3_satisfiable"] == 0
    }
    survivors_contain_dead = all(
        any(
            defect["state_id"] in dead_roots
            for defect in survivor["fixed_defects"]
        )
        for root in roots if root["root_state_id"] not in dead_roots
        for survivor in root["survivors"]
    )
    all_extras_eliminated = (
        len(dead_roots) >= 1
        and survivors_contain_dead
        and all(
            root["radius3_satisfiable"] > 0
            for root in roots if root["root_state_id"] not in dead_roots
        )
    )
    artifact = {
        "schema": "einstein.w3.spectre-radius3-defect",
        "version": 1,
        "status": (
            "RADIUS3_ELIMINATES_ALL_EXTRA_STATES_WITHIN_L18"
            if all_extras_eliminated else "RADIUS3_DEFECT_FRONTIER_REMAINS"
        ),
        "provenance": {
            "a6_source": str(A6.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6),
            "control_source": str(CONTROL.relative_to(ROOT)),
            "control_sha256": file_sha256(CONTROL),
            "two_sided_source": str(TWO_SIDED.relative_to(ROOT)),
            "two_sided_sha256": file_sha256(TWO_SIDED),
            "radius2_source": str(RADIUS2.relative_to(ROOT)),
            "radius2_sha256": file_sha256(RADIUS2),
        },
        "scope": {
            "state_alphabet": len(states),
            "generated_states": len(generated),
            "extra_states": len(extras),
            "radius2_assignments_checked": sum(
                root["radius2_assignments"] for root in roots
            ),
            "constraints": radius2["scope"]["constraints"],
        },
        "roots": roots,
        "elimination": {
            "dead_root_state_ids": sorted(dead_roots),
            "every_surviving_other_root_contains_a_dead_state": (
                survivors_contain_dead
            ),
            "all_extra_states_eliminated": all_extras_eliminated,
            "conditional_contraction_closure": all_extras_eliminated,
            "logic": (
                "a whole-plane occurrence restricts to a radius-three CSP; "
                "the dead root has none, and every survivor of either other "
                "root contains that dead state in its fixed inner patch"
            ),
        },
        "claim_boundary": (
            "closure is conditional on the fixed-chirality edge-to-edge L18 "
            "domain and its already proved unique 8/9 parent partition; entry "
            "of every geometric Spectre tiling into L18 remains unproved"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        "radius-three survivors:",
        [root["radius3_satisfiable"] for root in roots],
        "dead:", sorted(dead_roots),
        "closure:", all_extras_eliminated,
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
