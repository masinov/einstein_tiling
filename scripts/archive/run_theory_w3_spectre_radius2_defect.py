#!/usr/bin/env python
"""Minimize extra states in radius-two stars around each Spectre defect."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.geometry.cyclotomic import relative_pose
from einstein.tilings.spectre.colored_interfaces import (
    colored_corona_from_json, colored_local_overlap_witnesses,
)
from einstein.tilings.spectre.parent_constraints import ParentStateKernel
from einstein.tilings.spectre.parent_overlaps import parent_templates
from einstein.tilings.spectre.patches import pose_json
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[2]
A6 = ROOT / "docs/notebook/assets/a6-spectre-results.json"
CONTROL = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
TWO_SIDED = ROOT / "docs/notebook/assets/theory-w3-spectre-two-sided-overlap.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-radius2-defect.json"


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def histogram(values):
    return {str(key): count for key, count in sorted(Counter(values).items())}


def enumerate_assignments(problem, kernel, extra_indices):
    """Enumerate every state assignment with an independent SAT backend."""
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
    outer = {
        problem.positions.index(position) for position in problem.second_ring
    }
    signatures = Counter()
    assignments = 0
    forced_types = None
    with Cadical195(bootstrap_with=clauses) as solver:
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0}
            assignment = tuple(
                next(
                    state for state in problem.domains[position]
                    if variables[position, state] in positive
                )
                for position in range(len(problem.positions))
            )
            outer_extras = tuple(sorted(
                state for position, state in enumerate(assignment)
                if position in outer and state in extra_indices
            ))
            signatures[outer_extras] += 1
            types = set(outer_extras)
            forced_types = types if forced_types is None else forced_types & types
            assignments += 1
            solver.add_clause([
                -variables[position, state]
                for position, state in enumerate(assignment)
            ])
    return assignments, signatures, forced_types or set()


def main():
    control = json.loads(CONTROL.read_text())
    two_sided = json.loads(TWO_SIDED.read_text())
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
    templates = parent_templates(json.loads(A6.read_text()))
    kernel = ParentStateKernel(states, templates)
    roots = []
    for root_index in sorted(extra_indices):
        root_witnesses = colored_local_overlap_witnesses(
            states, root_index, limit=1_000_000,
        )
        cases = []
        best = None
        best_problem = best_result = None
        best_witness_index = None
        for witness_index, witness in enumerate(root_witnesses):
            problem = kernel.build_radius_two(root_index, witness)
            result = kernel.solve_radius_two(problem, extra_indices)
            cases.append({
                "witness_index": witness_index,
                "positions": len(problem.positions),
                "first_ring": len(problem.first_ring),
                "second_ring": len(problem.second_ring),
                "satisfiable": result.satisfiable,
                "minimum_outer_extras": result.minimum_outer_extras,
                "minimum_nonroot_extras": result.minimum_nonroot_extras,
                "search_nodes": result.search_nodes,
                "constraint_arcs": result.constraint_arcs,
            })
            if not result.satisfiable:
                continue
            objective = (
                result.minimum_outer_extras,
                result.minimum_nonroot_extras,
                witness_index,
            )
            if best is None or objective < best:
                best = objective
                best_problem = problem
                best_result = result
                best_witness_index = witness_index
        if best_problem is None or best_result is None:
            raise ValueError("one defect has no radius-two extension")
        assignment_count, outer_signatures, forced_outer_types = (
            enumerate_assignments(best_problem, kernel, extra_indices)
        )
        first = set(best_problem.first_ring)
        second = set(best_problem.second_ring)
        assignment = []
        for position, state_index in zip(
            best_problem.positions, best_result.assignment,
        ):
            assignment.append({
                "position": pose_json(position),
                "ring": 0 if position == (0, 0, (0, 0, 0, 0))
                else 1 if position in first else 2 if position in second
                else None,
                "state_id": state_id(states[state_index]),
                "source": (
                    "extra" if state_index in extra_indices else "generated"
                ),
            })
        roots.append({
            "root_state_id": state_id(states[root_index]),
            "root_star_witnesses": len(root_witnesses),
            "satisfiable_witnesses": sum(
                case["satisfiable"] for case in cases
            ),
            "position_count_histogram": histogram(
                case["positions"] for case in cases
            ),
            "minimum_outer_extras": best_result.minimum_outer_extras,
            "minimum_nonroot_extras": best_result.minimum_nonroot_extras,
            "best_witness_index": best_witness_index,
            "complete_assignment_count": assignment_count,
            "outer_extra_signature_histogram": {
                ",".join(state_id(states[index]) for index in signature): count
                for signature, count in sorted(outer_signatures.items())
            },
            "forced_outer_extra_state_ids": [
                state_id(states[index]) for index in sorted(forced_outer_types)
            ],
            "best_assignment": assignment,
            "cases": cases,
        })
    artifact = {
        "schema": "einstein.w3.spectre-radius2-defect",
        "version": 1,
        "status": "RADIUS2_FORCES_TYPED_OUTER_DEFECT_FOR_ALL_THREE_STATES",
        "provenance": {
            "a6_source": str(A6.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6),
            "control_source": str(CONTROL.relative_to(ROOT)),
            "control_sha256": file_sha256(CONTROL),
            "two_sided_source": str(TWO_SIDED.relative_to(ROOT)),
            "two_sided_sha256": file_sha256(TWO_SIDED),
        },
        "scope": {
            "states": len(states),
            "generated_states": len(generated),
            "extra_states": len(extras),
            "constraints": [
                "exact reciprocal endpoint types and child-edge contacts",
                "agreement on adjacency/nonadjacency for every represented anchor pair",
                "exact nonoverlap of all canonical 8/9-child physical supports",
            ],
            "objective": (
                "lexicographically minimize extra states on ring two, then "
                "on all nonroot positions"
            ),
        },
        "roots": roots,
        "conclusion": {
            "minimum_outer_extras": [
                root["minimum_outer_extras"] for root in roots
            ],
            "all_zero_outer_problems_unsatisfiable": all(
                root["minimum_outer_extras"] > 0 for root in roots
            ),
            "forced_type_map": {
                root["root_state_id"]: root["forced_outer_extra_state_ids"]
                for root in roots
            },
            "interpretation": (
                "no extra state can be surrounded by a radius-two parent "
                "patch whose outer ring is entirely generated; the forced "
                "type map sends the absorbable state into the alternating "
                "pair and maps the pair into each other"
            ),
        },
        "claim_boundary": (
            "this is a finite two-ring propagation theorem in the 20-state "
            "colored parent language; it neither proves an infinite defect "
            "configuration exists nor yet eliminates all three defects"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        "radius-two outer minima:",
        [root["minimum_outer_extras"] for root in roots],
        "nonroot minima:",
        [root["minimum_nonroot_extras"] for root in roots],
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
