#!/usr/bin/env python
"""Independent SAT verifier for pinned radius-two Spectre defect CSPs."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.geometry.cyclotomic import relative_pose
from einstein.tilings.spectre.colored_interfaces import (
    colored_corona_from_json, colored_local_overlap_witnesses,
)
from einstein.tilings.spectre.parent_constraints import ParentStateKernel
from einstein.tilings.spectre.parent_overlaps import parent_templates
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius2-defect.json"


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def sat_status(problem, kernel, extra_states):
    variables = {}
    next_variable = 1
    clauses = []
    for position, domain in enumerate(problem.domains):
        row = []
        for state in domain:
            variables[position, state] = next_variable
            row.append(next_variable)
            next_variable += 1
        clauses.append(row)
        for left, variable in enumerate(row):
            for other in row[:left]:
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
    position_index = {
        position: index for index, position in enumerate(problem.positions)
    }
    forbid_outer = [
        -variables[position_index[position], state]
        for position in problem.second_ring
        for state in problem.domains[position_index[position]]
        if state in extra_states
    ]
    with Cadical195(bootstrap_with=clauses) as solver:
        zero_outer_sat = solver.solve(assumptions=forbid_outer)
        assignments = 0
        forced_outer_types = None
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0}
            assignment = tuple(
                next(
                    state for state in problem.domains[position]
                    if variables[position, state] in positive
                )
                for position in range(len(problem.positions))
            )
            outer_types = {
                state for position, state in enumerate(assignment)
                if problem.positions[position] in set(problem.second_ring)
                and state in extra_states
            }
            forced_outer_types = (
                outer_types if forced_outer_types is None
                else forced_outer_types & outer_types
            )
            assignments += 1
            solver.add_clause([
                -variables[position, state]
                for position, state in enumerate(assignment)
            ])
    return assignments > 0, zero_outer_sat, assignments, forced_outer_types or set()


def main():
    artifact = json.loads(OUTPUT.read_text())
    provenance = artifact["provenance"]
    for prefix in ("a6", "control", "two_sided"):
        path = ROOT / provenance[f"{prefix}_source"]
        assert file_sha256(path) == provenance[f"{prefix}_sha256"]
    control = json.loads((ROOT / provenance["control_source"]).read_text())
    two_sided = json.loads(
        (ROOT / provenance["two_sided_source"]).read_text()
    )
    a6 = json.loads((ROOT / provenance["a6_source"]).read_text())
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
    extra_indices = {by_id[state_id(state)] for state in extras}
    kernel = ParentStateKernel(states, parent_templates(a6))
    checked = base_sat_count = 0
    for root in artifact["roots"]:
        root_index = by_id[root["root_state_id"]]
        witnesses = colored_local_overlap_witnesses(
            states, root_index, limit=1_000_000,
        )
        assert len(witnesses) == root["root_star_witnesses"]
        assert len(witnesses) == len(root["cases"])
        for case, witness in zip(root["cases"], witnesses):
            problem = kernel.build_radius_two(root_index, witness)
            base_sat, zero_outer_sat, assignments, forced_types = sat_status(
                problem, kernel, extra_indices,
            )
            assert base_sat == case["satisfiable"]
            assert not zero_outer_sat
            base_sat_count += base_sat
            checked += 1
            if base_sat:
                assert assignments == root["complete_assignment_count"]
                assert {
                    state_id(states[index]) for index in forced_types
                } == set(root["forced_outer_extra_state_ids"])
        assert root["minimum_outer_extras"] == 1
        assert root["satisfiable_witnesses"] == 1
        # The stored best assignment is a compact positive witness.
        best_case = root["cases"][root["best_witness_index"]]
        assert best_case["satisfiable"]
        assert sum(
            row["source"] == "extra" and row["ring"] == 2
            for row in root["best_assignment"]
        ) == 1
    assert checked == 131 and base_sat_count == 3
    assert artifact["conclusion"]["minimum_outer_extras"] == [1, 1, 1]
    print(
        "PASS radius-two defect CSP: 131 SAT instances; "
        "3 extend, 128 fail, all 131 reject a generated-only outer ring"
    )


if __name__ == "__main__":
    main()
