#!/usr/bin/env python
"""Independent SAT replay of the radius-three Spectre defect elimination."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.substrate.module12 import relative_pose
from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json, colored_local_overlap_witnesses,
)
from einstein.theory.spectre_parent_csp import ParentStateKernel
from einstein.theory.spectre_parent_overlap import parent_templates
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius3-defect.json"


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def is_satisfiable(problem, kernel):
    variables = {}
    clauses = []
    next_variable = 1
    for position, domain in enumerate(problem.domains):
        row = []
        for state in domain:
            variables[position, state] = next_variable
            row.append(next_variable)
            next_variable += 1
        clauses.append(row)
        for offset, variable in enumerate(row):
            for other in row[:offset]:
                clauses.append([-variable, -other])
    for left in range(len(problem.positions)):
        for right in range(left):
            relative = relative_pose(
                problem.positions[left], problem.positions[right],
            )
            for a in problem.domains[left]:
                for b in problem.domains[right]:
                    if not kernel.compatible(relative, a, b):
                        clauses.append([
                            -variables[left, a], -variables[right, b],
                        ])
    with Cadical195(bootstrap_with=clauses) as solver:
        return solver.solve()


def main():
    artifact = json.loads(OUTPUT.read_text())
    provenance = artifact["provenance"]
    for prefix in ("a6", "control", "two_sided", "radius2"):
        path = ROOT / provenance[f"{prefix}_source"]
        assert file_sha256(path) == provenance[f"{prefix}_sha256"]
    a6 = json.loads((ROOT / provenance["a6_source"]).read_text())
    control = json.loads((ROOT / provenance["control_source"]).read_text())
    two_sided = json.loads(
        (ROOT / provenance["two_sided_source"]).read_text()
    )
    radius2 = json.loads((ROOT / provenance["radius2_source"]).read_text())
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
    kernel = ParentStateKernel(states, parent_templates(a6))
    replay = {}
    fixed_defects_by_survivor = {}
    checked = 0
    for stored_root, radius2_root in zip(artifact["roots"], radius2["roots"]):
        assert stored_root["root_state_id"] == radius2_root["root_state_id"]
        root_index = by_id[stored_root["root_state_id"]]
        witness = colored_local_overlap_witnesses(
            states, root_index, limit=1_000_000,
        )[radius2_root["best_witness_index"]]
        problem2 = kernel.build_radius_two(root_index, witness)
        assignments2 = kernel.enumerate_assignments(problem2)
        assert len(assignments2) == stored_root["radius2_assignments"]
        survivors = []
        for case, assignment2 in zip(stored_root["cases"], assignments2):
            problem3 = kernel.extend_fixed_assignment(problem2, assignment2)
            sat = is_satisfiable(problem3, kernel)
            assert sat == case["satisfiable"]
            if sat:
                survivors.append(case["radius2_assignment_index"])
                fixed_defects_by_survivor[
                    stored_root["root_state_id"], case["radius2_assignment_index"]
                ] = set(case["fixed_defect_state_ids"])
            checked += 1
        replay[stored_root["root_state_id"]] = survivors
        assert len(survivors) == stored_root["radius3_satisfiable"]

    dead = {root for root, survivors in replay.items() if not survivors}
    assert dead == set(artifact["elimination"]["dead_root_state_ids"])
    assert len(dead) == 1
    for (root, _), fixed_defects in fixed_defects_by_survivor.items():
        if root not in dead:
            assert fixed_defects & dead
    assert artifact["elimination"]["all_extra_states_eliminated"]
    assert artifact["status"] == "RADIUS3_ELIMINATES_ALL_EXTRA_STATES_WITHIN_L18"
    print(
        f"PASS radius-three defect elimination: {checked} SAT replays; "
        f"survivors={[len(replay[root]) for root in replay]}; "
        f"dead={sorted(dead)}"
    )


if __name__ == "__main__":
    main()
