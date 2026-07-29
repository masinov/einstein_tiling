#!/usr/bin/env python
"""Isolate the 16 signature maps in the ``2 Lambda`` packing-family gate."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import (
    PACKING_COLLISION_SEED,
    area_admissible_2lambda_hnfs,
    coverage_summary,
)
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf
from einstein.holonomy.constraints import _cnf_sha256, quotient_boundary_data


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
FAMILY = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-family-index120.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-signature-index120.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _solve_hnf(arguments):
    shape, hnf, signature_rows = arguments
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing_clauses = collision_orbit_clauses(shape, hnf, instance, target)
    rows = []
    for layer_index, signature in enumerate(signature_rows):
        started = perf_counter()
        twists = induced_v4_twists(tuple(signature["base_twists"]), hnf)
        cnf, metadata = build_v4_coverability_cnf(
            shape, hnf, tuple(signature["images"]), twists
        )
        cnf.extend(packing_clauses)
        built = perf_counter()
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve()
            model = solver.get_model() if sat else None
            stats = solver.accum_stats()
        true_variables = sorted(literal for literal in model if literal > 0) if sat else []
        row = {
            "hnf": list(hnf),
            "index": hnf[0] * hnf[2],
            "layer_index": layer_index,
            "mapping_index": signature["mapping_index"],
            "images": signature["images"],
            "twists": list(twists),
            "packing_clauses": len(packing_clauses),
            "sat": sat,
            "verdict": "not-obstructed" if sat else "packing-obstructed",
            "canonical_cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "variables": cnf.nv,
            "clauses": len(cnf.clauses),
            "solver_conflicts": stats.get("conflicts"),
            "build_seconds": built - started,
            "solve_seconds": perf_counter() - built,
        }
        if sat:
            row["true_variables"] = true_variables
            row["coverage"] = coverage_summary(shape, hnf, true_variables)
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-index", type=int, default=120)
    parser.add_argument("--jobs", type=int, default=16)
    args = parser.parse_args()
    if args.maximum_index != 120:
        raise SystemExit("the tracked artifact is pinned to --maximum-index 120")
    base = json.loads(BASE.read_text())
    signature_rows = tuple(sorted(
        base["base_witnesses"], key=lambda row: row["mapping_index"]
    ))
    hnfs = area_admissible_2lambda_hnfs(args.maximum_index)
    if len(signature_rows) != 16 or len(hnfs) != 193:
        raise AssertionError("signature or HNF census changed")
    shape = decode_compiled_key(KEY)
    tasks = [(shape, hnf, signature_rows) for hnf in hnfs]
    print(
        f"packing signature-family cases: {len(hnfs)} HNFs x "
        f"{len(signature_rows)} maps; jobs={args.jobs}", flush=True,
    )
    checks = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_solve_hnf, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            rows = future.result()
            checks.extend(rows)
            obstructed = sum(not row["sat"] for row in rows)
            print(
                f"[{completed:3d}/{len(tasks)}] {tuple(rows[0]['hnf'])}: "
                f"{obstructed}/16 obstructed", flush=True,
            )
    checks.sort(key=lambda row: (row["mapping_index"], row["index"], row["hnf"]))
    by_mapping = []
    for signature in signature_rows:
        mapping_index = signature["mapping_index"]
        rows = [row for row in checks if row["mapping_index"] == mapping_index]
        by_mapping.append({
            "layer_index": next(row["layer_index"] for row in rows),
            "mapping_index": mapping_index,
            "images": signature["images"],
            "packing_obstructed": sum(not row["sat"] for row in rows),
            "not_obstructed": sum(row["sat"] for row in rows),
            "first_not_obstructed_hnf": next(
                (row["hnf"] for row in rows if row["sat"]), None
            ),
        })
    universal = [row["mapping_index"] for row in by_mapping if not row["not_obstructed"]]
    dependencies = (BASE, FAMILY)
    sources = (
        ROOT / "src/einstein/holonomy/alternating4/lifts.py",
        ROOT / "src/einstein/holonomy/alternating4/packing.py",
        ROOT / "src/einstein/holonomy/alternating4/packing_families.py",
        ROOT / "src/einstein/holonomy/alternating4/local_system.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-v4-single-signature-packing-family-scan",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "family": "area-admissible HNF sublattices of 2 Lambda",
            "maximum_index": args.maximum_index,
            "hnfs": len(hnfs),
            "signature_maps": len(signature_rows),
            "logical_cases": len(checks),
            "packing_collision_orbits": 1,
            "proof_status": "UNSAT search only; SAT assignments replayable",
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in dependencies
            ],
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "summary": {
            "universal_obstructors_in_finite_gate": universal,
            "universal_obstructor_count": len(universal),
            "total_packing_obstructed_cases": sum(not row["sat"] for row in checks),
            "total_not_obstructed_cases": sum(row["sat"] for row in checks),
        },
        "by_mapping": by_mapping,
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({"summary": payload["summary"], "by_mapping": by_mapping}, indent=1))


if __name__ == "__main__":
    main()
