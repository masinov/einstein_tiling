#!/usr/bin/env python
"""Sample torus pair-graph extremizers and test their literal planar lifts."""

from __future__ import annotations

import argparse
from collections import Counter
import itertools
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
    hall_deficiency,
    hall_witness_profile,
    minimal_hall_witness,
    two_center_matching,
)
from einstein.theory.a4_v4_lift import induced_v4_twists
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    placement_lattice_cells,
    torus_conflicting_pairs,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED
from einstein.theory.holonomy_csp import quotient_boundary_data


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _torus_sources(shape, row, count, packing_mode):
    hnf = (4, 0, 4)
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    cnf = CNF()
    packing_orbits = (() if packing_mode == "full"
                      else packing_circuit_orbits(shape, system))
    for orbit in packing_orbits + affine_pair_circuit_orbits(system):
        cnf.extend([[-variable for variable in circuit]
                    for circuit in orbit.translates])
    if packing_mode == "full":
        instance, _, _ = quotient_boundary_data(shape, hnf)
        cnf.extend([[-left, -right]
                    for left, right in torus_conflicting_pairs(instance)])
    exactly = CardEnc.equals(
        lits=list(range(1, len(system.placements) + 1)),
        bound=9,
        top_id=cnf.nv,
        encoding=EncType.cardnetwrk,
    )
    cnf.extend(exactly.clauses)
    sources = []
    with Cadical195(bootstrap_with=cnf) as solver:
        while len(sources) < count and solver.solve():
            truth = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(variable for variable in range(
                1, len(system.placements) + 1
            ) if variable in truth)
            if len(selected) != 9:
                raise AssertionError("source cardinality encoding failed")
            sources.append(tuple(system.placements[v - 1] for v in selected))
            # One representative per quotient-translation orbit.
            for translated in translation_orbit(system, selected):
                solver.add_clause([-variable for variable in translated])
    return tuple(sources)


def _supports(shape, placements):
    return tuple(frozenset(
        (u, v) for u, v, _sector in placement_lattice_cells(shape, placement)
    ) for placement in placements)


def _first_lifted_witness(shape, source, maximum_periods):
    rectangles = sorted(
        itertools.product(range(1, maximum_periods + 1), repeat=2),
        key=lambda pair: (pair[0] * pair[1], max(pair), pair),
    )
    for width, height in rectangles:
        placements = tuple(
            (operation, u + 4 * i, v + 4 * j)
            for i in range(width)
            for j in range(height)
            for operation, u, v in source
        )
        supports = _supports(shape, placements)
        matching = two_center_matching(supports, range(1, len(placements) + 1))
        if matching.saturated:
            continue
        witness = minimal_hall_witness(supports, matching.deficient_tiles)
        return width, height, placements, supports, witness
    return None


def _ambient_system(shape, row, maximum_periods, margin=5):
    side = 4 * maximum_periods + 2 * margin + 2
    side += side % 2
    hnf = side, 0, side
    row = dict(row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    return build_v4_equation_system(shape, hnf, row), margin


def catalog(shape, row, samples=20, maximum_periods=7, packing_mode="single"):
    if packing_mode not in ("single", "full"):
        raise ValueError("packing_mode must be 'single' or 'full'")
    sources = _torus_sources(shape, row, samples, packing_mode)
    ambient, shift = _ambient_system(shape, row, maximum_periods)
    lookup = {placement: variable for variable, placement in enumerate(
        ambient.placements, 1
    )}
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    rows = []
    countermodel = None
    for source_index, source in enumerate(sources):
        lifted = _first_lifted_witness(shape, source, maximum_periods)
        if lifted is None:
            rows.append({
                "source_index": source_index,
                "source": [list(p) for p in source],
                "status": "NO_HALL_CORE_IN_SEARCH",
            })
            continue
        width, height, placements, supports, witness = lifted
        literal = tuple(placements[v - 1] for v in witness.deficient_tiles)
        shifted = tuple((operation, u + shift, v + shift)
                        for operation, u, v in literal)
        global_variables = tuple(lookup[p] for p in shifted)
        cells = tuple(placement_lattice_cells(shape, placement)
                      for placement in shifted)
        packing_conflicts = sum(
            bool(cells[left] & cells[right])
            and canonical_collision_type(cells[left], cells[right]) == target
            for left, right in itertools.combinations(range(len(cells)), 2)
        )
        actual_overlap_pairs = sum(
            bool(cells[left] & cells[right])
            for left, right in itertools.combinations(range(len(cells)), 2)
        )
        affine_pair_conflicts = sum(
            not affine_compatible(
                ambient, (global_variables[left], global_variables[right])
            )
            for left, right in itertools.combinations(
                range(len(global_variables)), 2
            )
        )
        if packing_conflicts or affine_pair_conflicts:
            raise AssertionError("source lift lost pairwise admissibility")
        if packing_mode == "full" and actual_overlap_pairs:
            raise AssertionError("full-packing torus source overlapped after lift")
        core = minimal_affine_circuit(ambient, global_variables)
        profile = hall_witness_profile(supports, witness)
        item = {
            "source_index": source_index,
            "source": [list(p) for p in source],
            "status": ("PLANAR_HALL_COUNTERMODEL" if not core
                       else "BLOCKED_BY_AFFINE_CIRCUIT"),
            "first_period_rectangle": [width, height],
            "whole_set_deficiency": hall_deficiency(
                supports, range(1, len(placements) + 1)
            ),
            "minimal_hall_profile": profile,
            "packing_pair_conflicts": packing_conflicts,
            "actual_overlap_pairs": actual_overlap_pairs,
            "affine_pair_conflicts": affine_pair_conflicts,
            "minimal_affine_circuit_size": len(core),
        }
        rows.append(item)
        print(
            f"source={source_index} rectangle={width}x{height} "
            f"Hall={profile['center_count']}/{2 * profile['tile_count']} "
            f"circuit={len(core)}",
            flush=True,
        )
        if not core:
            countermodel = {
                **item,
                "placements": [list(p) for p in literal],
                "centers": [list(c) for c in witness.deficient_centers],
            }
            break
    return {
        "status": ("PLANAR_HALL_COUNTERMODEL" if countermodel
                   else "NO_COUNTERMODEL_IN_CATALOG"),
        "source_hnf": [4, 0, 4],
        "source_target_count": 9,
        "requested_samples": samples,
        "enumerated_sources": len(sources),
        "maximum_periods": maximum_periods,
        "mapping_index": row["mapping_index"],
        "packing_mode": packing_mode,
        "rows": rows,
        "circuit_size_histogram": dict(sorted(Counter(
            item.get("minimal_affine_circuit_size")
            for item in rows if "minimal_affine_circuit_size" in item
        ).items())),
        "countermodel": countermodel,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--maximum-periods", type=int, default=7)
    parser.add_argument("--packing-mode", choices=("single", "full"),
                        default="single")
    parser.add_argument("--output")
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    result = catalog(
        shape, payload["base_witnesses"][0], args.samples, args.maximum_periods,
        args.packing_mode,
    )
    text = json.dumps(result, indent=1) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
    return 1 if result["status"] == "PLANAR_HALL_COUNTERMODEL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
