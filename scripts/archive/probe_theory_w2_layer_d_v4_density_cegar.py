#!/usr/bin/env python
"""Learn finite V4 gluing hyperedges until the packing density is decided."""

from __future__ import annotations

import argparse
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


def learn(shape, hnf, row, maximum_iterations=100000):
    twists = induced_v4_twists(tuple(row["base_twists"]), hnf)
    covered, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(row["images"]), twists=twists, cover_mode="at-least"
    )
    instance, _, boundaries = quotient_boundary_data(shape, hnf)
    placement_count = len(instance.placements)
    k = hnf[0] * hnf[2]
    target_count = k // 2 + 1
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = collision_orbit_clauses(shape, hnf, instance, target)
    implications = covered.clauses[metadata["cover_clauses"]:]
    learned = []
    learned_clauses = set()
    placement_lookup = {
        placement: variable
        for variable, (placement, _) in enumerate(instance.placements, 1)
    }

    def translated_core(core, shift_u, shift_v):
        a, b, d = hnf
        out = []
        for variable in core:
            operation, u, v = instance.placements[variable - 1][0]
            qv, rv = divmod(v + shift_v, d)
            ru = (u + shift_u - qv * b) % a
            out.append(placement_lookup[(operation, ru, rv)])
        return tuple(sorted(out))

    boundary_vertices = tuple(
        frozenset(vertex for edge in edges for vertex in (edge[0], edge[2]))
        for edges in boundaries
    )
    with Cadical195(bootstrap_with=implications) as checker:
        # Seed the master with all local binary incompatibilities.  Without
        # this pass the CEGAR loop merely rediscovers thousands of pair edges.
        pair_edges = []
        for left, right in itertools.combinations(
            range(1, placement_count + 1), 2
        ):
            shared = boundary_vertices[left - 1] & boundary_vertices[right - 1]
            if len(shared) < 2:
                continue
            if not checker.solve(assumptions=[left, right]):
                pair_edges.append((left, right))
        master = CNF(from_clauses=[list(clause) for clause in packing])
        master.extend([[-left, -right] for left, right in pair_edges])
        exactly = CardEnc.equals(
            lits=list(range(1, placement_count + 1)),
            bound=target_count,
            top_id=max(master.nv, covered.nv),
            encoding=EncType.cardnetwrk,
        )
        master.extend(exactly.clauses)
        print(f"prelearned binary incompatibilities={len(pair_edges)}", flush=True)
        with Cadical195(bootstrap_with=master) as chooser:
            for iteration in range(1, maximum_iterations + 1):
                if not chooser.solve():
                    return {
                        "status": "BOUND_VERIFIED_BY_LEARNED_HYPERGRAPH",
                        "iterations": iteration - 1,
                        "prelearned_pair_edges": len(pair_edges),
                        "learned_clauses": len(learned_clauses),
                        "learned": learned,
                    }
                model = chooser.get_model()
                selected = [
                    variable for variable in range(1, placement_count + 1)
                    if model[variable - 1] > 0
                ]
                if len(selected) != target_count:
                    raise AssertionError("master cardinality encoding failed")
                if checker.solve(assumptions=selected):
                    return {
                        "status": "COUNTERMODEL",
                        "iterations": iteration - 1,
                        "prelearned_pair_edges": len(pair_edges),
                        "learned_clauses": len(learned_clauses),
                        "selected": [
                            list(instance.placements[variable - 1][0])
                            for variable in selected
                        ],
                        "learned": learned,
                    }
                core = checker.get_core()
                if not core:
                    raise AssertionError("checker returned no assumption core")
                # Cadical cores are not guaranteed deletion-minimal.
                core = list(core)
                changed = True
                while changed:
                    changed = False
                    for variable in list(core):
                        trial = [item for item in core if item != variable]
                        if not checker.solve(assumptions=trial):
                            core = trial
                            changed = True
                            break
                orbit_added = 0
                for shift_u in range(hnf[0]):
                    for shift_v in range(hnf[2]):
                        shifted = translated_core(core, shift_u, shift_v)
                        clause = tuple(-variable for variable in shifted)
                        if clause in learned_clauses:
                            continue
                        if checker.solve(assumptions=list(shifted)):
                            raise AssertionError(
                                "translation did not preserve gluing circuit"
                            )
                        chooser.add_clause(list(clause))
                        learned_clauses.add(clause)
                        orbit_added += 1
                learned.append({
                    "size": len(core),
                    "translation_orbit_clauses_added": orbit_added,
                    "placements": [
                        list(instance.placements[variable - 1][0])
                        for variable in core
                    ],
                })
                if iteration <= 20 or iteration % 100 == 0:
                    print(
                        f"iteration={iteration} core={len(core)} "
                        f"histogram={dict(Counter(row['size'] for row in learned))}",
                        flush=True,
                    )
    raise AssertionError("unreachable")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hnf", nargs=3, type=int, default=(4, 0, 4))
    parser.add_argument("--maximum-iterations", type=int, default=100000)
    parser.add_argument("--output")
    args = parser.parse_args()
    hnf = tuple(args.hnf)
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    result = learn(shape, hnf, row, args.maximum_iterations)
    result.update({
        "hnf": list(hnf),
        "centers": hnf[0] * hnf[2],
        "tested_selected": hnf[0] * hnf[2] // 2 + 1,
        "mapping_index": row["mapping_index"],
        "core_size_histogram": dict(sorted(Counter(
            item["size"] for item in result["learned"]
        ).items())),
    })
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"] == "COUNTERMODEL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
