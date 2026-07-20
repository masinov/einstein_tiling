#!/usr/bin/env python
"""Probe local placement-density bounds for the Layer-D packing invariant."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_lift import induced_v4_twists
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED
from einstein.theory.a4_v4_sft import build_v4_coverability_cnf
from einstein.theory.holonomy_csp import quotient_boundary_data


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def local_optimum(
    shape, hnf, row, width=None, height=None, origin=(0, 0), potential_bit=None
):
    """Maximize placements anchored in one rectangle; disable all others."""
    twists = induced_v4_twists(tuple(row["base_twists"]), hnf)
    cnf, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(row["images"]), twists=twists, cover_mode="at-least"
    )
    instance, vertices, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = collision_orbit_clauses(shape, hnf, instance, target)
    left, bottom = origin
    if width is None or height is None:
        objective = tuple(range(1, len(instance.placements) + 1))
        block = None
    else:
        objective = tuple(
            variable
            for variable, ((_, u, v), _) in enumerate(instance.placements, 1)
            if left <= u < left + width and bottom <= v < bottom + height
        )
        block = [left, bottom, width, height]
    objective_set = set(objective)
    implications = cnf.clauses[metadata["cover_clauses"]:]
    if potential_bit is not None:
        if potential_bit not in (0, 1):
            raise ValueError("potential_bit must be 0, 1, or None")
        placement_count = len(instance.placements)
        implications = [
            clause for clause in implications
            if all(
                (abs(literal) - placement_count - 1) % 2 == potential_bit
                for literal in clause if abs(literal) > placement_count
            )
        ]
    hard = implications + list(packing)
    hard.extend(
        [-variable]
        for variable in range(1, len(instance.placements) + 1)
        if variable not in objective_set
    )
    formula = WCNF()
    for clause in hard:
        formula.append(clause)
    for variable in objective:
        formula.append([variable], weight=1)
    with RC2(formula, adapt=True, exhaust=True, incr=True) as solver:
        model = solver.compute()
        cost = solver.cost
    truth = {literal for literal in model if literal > 0}
    selected = [
        list(instance.placements[variable - 1][0])
        for variable in objective if variable in truth
    ]
    selected_anchor_histogram = Counter((u, v) for _, u, v in selected)
    center_state_histogram = None
    if potential_bit is None:
        colors = {}
        base = len(instance.placements) + 1
        for index, vertex in enumerate(vertices):
            colors[vertex] = (
                int(base + 2 * index in truth)
                | (int(base + 2 * index + 1 in truth) << 1)
            )
        by_center = {}
        kinds = sorted({vertex[:2] for vertex in vertices})
        for u in range(hnf[0]):
            for v in range(hnf[2]):
                values = tuple(colors[(*kind, u, v)] for kind in kinds)
                by_center[(u, v)] = tuple(value ^ values[0] for value in values)
        center_state_histogram = dict(
            sorted((str(state), count)
                   for state, count in Counter(by_center.values()).items())
        )
    return {
        "hnf": list(hnf),
        "mapping_index": row["mapping_index"],
        "potential_bit": potential_bit,
        "twists": list(twists),
        "block": block,
        "objective_placements": len(objective),
        "maximum_selected": len(objective) - cost,
        "selected": selected,
        "selected_anchor_histogram": {
            str(anchor): count
            for anchor, count in sorted(selected_anchor_histogram.items())
        },
        "center_state_histogram": center_state_histogram,
    }


def main():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    rows = payload["base_witnesses"]
    probes = []
    for bit in (0, 1, None):
        for hnf in ((2, 0, 2), (4, 0, 2), (2, 0, 10)):
            result = local_optimum(shape, hnf, rows[0], potential_bit=bit)
            probes.append(result)
            print(
                f"bit={bit} hnf={hnf} map={rows[0]['mapping_index']:2d} "
                f"max={result['maximum_selected']}",
                flush=True,
            )
    print(json.dumps(probes, indent=1))


if __name__ == "__main__":
    main()
