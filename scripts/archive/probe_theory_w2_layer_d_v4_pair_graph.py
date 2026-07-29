#!/usr/bin/env python
"""Eliminate V4 potentials pairwise and inspect the placement conflict graph."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195

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


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def pair_graph(shape, hnf, row):
    twists = induced_v4_twists(tuple(row["base_twists"]), hnf)
    cnf, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(row["images"]), twists=twists, cover_mode="at-least"
    )
    instance, _, boundaries = quotient_boundary_data(shape, hnf)
    implication_cnf = CNF(
        from_clauses=cnf.clauses[metadata["cover_clauses"]:]
    )
    boundary_vertices = tuple(
        frozenset(vertex for edge in edges for vertex in (edge[0], edge[2]))
        for edges in boundaries
    )
    incompatible = []
    pairs_checked = 0
    with Cadical195(bootstrap_with=implication_cnf) as solver:
        for left, right in itertools.combinations(
            range(1, len(instance.placements) + 1), 2
        ):
            # Two individually consistent connected boundary systems sharing at
            # most one potential vertex can always be gauge-aligned there.
            if len(boundary_vertices[left - 1] & boundary_vertices[right - 1]) < 2:
                continue
            pairs_checked += 1
            if not solver.solve(assumptions=[left, right]):
                incompatible.append((left, right))
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = [tuple(-literal for literal in clause)
               for clause in collision_orbit_clauses(
                   shape, hnf, instance, target
               )]
    edges = tuple(sorted(set(incompatible) | set(packing)))
    degree = Counter(variable for edge in edges for variable in edge)

    bound = instance.n_cells // 12  # k/2 because n_cells = 6k
    graph_cnf = CNF(from_clauses=[[-left, -right] for left, right in edges])
    cardinality = CardEnc.atleast(
        lits=list(range(1, len(instance.placements) + 1)),
        bound=bound + 1,
        top_id=graph_cnf.nv,
        encoding=EncType.seqcounter,
    )
    graph_cnf.extend(cardinality.clauses)
    with Cadical195(bootstrap_with=graph_cnf) as solver:
        over_bound_sat = solver.solve()
        model = solver.get_model() if over_bound_sat else None
    selected = [] if model is None else [
        list(instance.placements[variable - 1][0])
        for variable in range(1, len(instance.placements) + 1)
        if model[variable - 1] > 0
    ]
    return {
        "hnf": list(hnf),
        "centers": hnf[0] * hnf[2],
        "placements": len(instance.placements),
        "mapping_index": row["mapping_index"],
        "twists": list(twists),
        "signature_pair_edges": len(incompatible),
        "signature_pairs_checked": pairs_checked,
        "packing_pair_edges": len(packing),
        "union_edges": len(edges),
        "degree_histogram": dict(sorted(Counter(degree.values()).items())),
        "tested_bound": bound,
        "graph_has_independent_set_over_bound": over_bound_sat,
        "over_bound_witness": selected,
    }


def main():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    for hnf in ((4, 0, 4), (6, 0, 6)):
        result = pair_graph(shape, hnf, row)
        print(json.dumps(result, indent=1), flush=True)


if __name__ == "__main__":
    main()
