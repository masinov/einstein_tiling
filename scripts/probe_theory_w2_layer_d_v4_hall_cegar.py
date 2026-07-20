#!/usr/bin/env python
"""Search exactly for a Hall-deficient V4-compatible T2.D6 packing.

The SAT master chooses placements and quotient centers satisfying

    2 * selected_tiles - used_centers >= 1.

Thus every master model is a strict obstruction to assigning two distinct
centers per tile.  Packing conflicts and all affine pair circuits are seeded;
higher affine circuits are learned from the exact XOR union-find oracle, one
complete translation orbit at a time.  UNSAT is a finite hypergraph proof of
the density-half implication on the requested quotient.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuit_hypergraph import (
    affine_pair_circuit_orbits,
    packing_circuit_orbits,
)
from einstein.theory.a4_v4_circuits import (
    affine_compatible,
    build_v4_equation_system,
    minimal_affine_circuit,
    translation_orbit,
)
from einstein.theory.a4_v4_hall import (
    hall_witness_profile,
    minimal_hall_witness,
    placement_center_supports,
    two_center_matching,
    verify_two_matching,
)
from einstein.theory.a4_v4_lift import induced_v4_twists


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _master(shape, system, seed_pairs=True):
    placement_count = len(system.placements)
    a, _b, d = system.hnf
    centers = tuple((u, v) for u in range(a) for v in range(d))
    center_variables = {
        center: placement_count + index
        for index, center in enumerate(centers, 1)
    }
    supports = placement_center_supports(shape, system)
    cnf = CNF()

    packing_orbits = packing_circuit_orbits(shape, system)
    for orbit in packing_orbits:
        cnf.extend([[-variable for variable in circuit]
                    for circuit in orbit.translates])

    pair_orbits = affine_pair_circuit_orbits(system) if seed_pairs else ()
    for orbit in pair_orbits:
        cnf.extend([[-variable for variable in circuit]
                    for circuit in orbit.translates])

    # A selected placement forces all four centers in its geometric support to
    # be counted.  Unforced center variables may stay false, so satisfiability
    # of the inequality below is equivalent to a genuine Hall deficiency.
    for variable, support in enumerate(supports, 1):
        for center in support:
            cnf.append([-variable, center_variables[center]])

    k = len(centers)
    # Coefficients are only 2 and 1, so duplicate each placement literal and
    # use a cardinality network.  This is exactly the pseudo-Boolean row
    # 2*sum(x) + sum(not y) >= k+1; the duplicate-wire equivalence is pinned
    # exhaustively in the regression tests.
    hall = CardEnc.atleast(
        lits=(list(range(1, placement_count + 1)) * 2
              + [-center_variables[center] for center in centers]),
        bound=k + 1,
        top_id=max(cnf.nv, placement_count + k),
        encoding=EncType.cardnetwrk,
    )
    cnf.extend(hall.clauses)
    return cnf, supports, centers, packing_orbits, pair_orbits


def learn(shape, system, maximum_iterations=100000, seed_pairs=True):
    cnf, supports, centers, packing_orbits, pair_orbits = _master(
        shape, system, seed_pairs=seed_pairs
    )
    placement_count = len(system.placements)
    learned_orbits = []
    learned_clauses = set()
    print(
        f"master placements={placement_count} centers={len(centers)} "
        f"packing_orbits={len(packing_orbits)} "
        f"affine_pair_orbits={len(pair_orbits)} variables={cnf.nv} "
        f"clauses={len(cnf.clauses)}",
        flush=True,
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        for iteration in range(1, maximum_iterations + 1):
            if not solver.solve():
                return {
                    "status": "NO_HALL_DEFICIENCY",
                    "iterations": iteration - 1,
                    "packing_orbits": len(packing_orbits),
                    "affine_pair_orbits": len(pair_orbits),
                    "learned_orbits": learned_orbits,
                    "learned_clauses": len(learned_clauses),
                    "master_variables": cnf.nv,
                    "initial_master_clauses": len(cnf.clauses),
                }
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(
                variable for variable in range(1, placement_count + 1)
                if variable in positive
            )
            matching = two_center_matching(supports, selected)
            if matching.saturated or not verify_two_matching(supports, matching):
                raise AssertionError("SAT Hall inequality and matching disagree")
            matching = minimal_hall_witness(supports, matching.deficient_tiles)
            profile = hall_witness_profile(supports, matching)

            if affine_compatible(system, matching.deficient_tiles):
                return {
                    "status": "HALL_DEFICIENT_COUNTERMODEL",
                    "iterations": iteration - 1,
                    "packing_orbits": len(packing_orbits),
                    "affine_pair_orbits": len(pair_orbits),
                    "learned_orbits": learned_orbits,
                    "learned_clauses": len(learned_clauses),
                    "selected": [list(system.placements[v - 1]) for v in selected],
                    "selected_count": len(selected),
                    "deficient_tiles": [
                        list(system.placements[v - 1])
                        for v in matching.deficient_tiles
                    ],
                    "deficient_tile_count": len(matching.deficient_tiles),
                    "deficient_centers": [list(c) for c in matching.deficient_centers],
                    "deficient_center_count": len(matching.deficient_centers),
                    "witness_profile": profile,
                }

            core = minimal_affine_circuit(system, matching.deficient_tiles)
            if not core:
                raise AssertionError("incompatible selection yielded no circuit")
            orbit = translation_orbit(system, core)
            added = 0
            for circuit in orbit:
                clause = tuple(-variable for variable in circuit)
                if clause in learned_clauses:
                    continue
                solver.add_clause(list(clause))
                learned_clauses.add(clause)
                added += 1
            learned_orbits.append({
                "size": len(core),
                "orbit_size": len(orbit),
                "clauses_added": added,
                "hall_witness_profile": profile,
                "placements": [list(system.placements[v - 1]) for v in core],
            })
            if iteration <= 20 or iteration % 100 == 0:
                histogram = Counter(row["size"] for row in learned_orbits)
                print(
                    f"iteration={iteration} selected={len(selected)} "
                    f"minimal_Hall={profile['center_count']}/"
                    f"{2 * profile['tile_count']} core={len(core)} "
                    f"added={added} histogram={dict(sorted(histogram.items()))}",
                    flush=True,
                )
    raise AssertionError("unreachable")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hnf", nargs=3, type=int, default=(4, 0, 4))
    parser.add_argument("--mapping-index", type=int)
    parser.add_argument("--maximum-iterations", type=int, default=100000)
    parser.add_argument("--no-seed-pairs", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    hnf = tuple(args.hnf)
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    rows = payload["base_witnesses"]
    if args.mapping_index is None:
        row = dict(rows[0])
    else:
        row = dict(next(item for item in rows
                        if item["mapping_index"] == args.mapping_index))
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    result = learn(
        shape, system, args.maximum_iterations,
        seed_pairs=not args.no_seed_pairs,
    )
    result.update({
        "hnf": list(hnf),
        "centers": hnf[0] * hnf[2],
        "mapping_index": row["mapping_index"],
        "learned_core_size_histogram": dict(sorted(Counter(
            item["size"] for item in result["learned_orbits"]
        ).items())),
    })
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"] == "HALL_DEFICIENT_COUNTERMODEL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
