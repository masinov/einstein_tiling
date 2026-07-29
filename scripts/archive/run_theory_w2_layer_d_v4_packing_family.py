#!/usr/bin/env python
"""Falsify the proposed single-orbit packing theorem across ``2 Lambda``."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_packing_family import (
    area_admissible_2lambda_hnfs,
    build_signature_packing_cnf,
    coverage_summary,
)
from einstein.theory.holonomy_csp import _cnf_sha256


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
PACKING60 = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-packing.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-family-index120.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _solve(arguments):
    shape, hnf, signature_rows = arguments
    started = perf_counter()
    cnf, metadata = build_signature_packing_cnf(shape, hnf, signature_rows)
    built = perf_counter()
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        stats = solver.accum_stats()
    true_variables = sorted(literal for literal in model if literal > 0) if sat else []
    row = {
        "hnf": list(hnf),
        "index": hnf[0] * hnf[2],
        "sat": sat,
        "verdict": "not-obstructed" if sat else "packing-obstructed",
        "canonical_cnf_sha256": _cnf_sha256(cnf),
        "metadata": metadata,
        "solver_conflicts": stats.get("conflicts"),
        "build_seconds": built - started,
        "solve_seconds": perf_counter() - built,
    }
    if sat:
        row["true_variables"] = true_variables
        row["coverage"] = coverage_summary(shape, hnf, true_variables)
    return row


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
    if len(signature_rows) != 16:
        raise AssertionError("expected all 16 distinct-tail signature maps")
    hnfs = area_admissible_2lambda_hnfs(args.maximum_index)
    if len(hnfs) != 193:
        raise AssertionError("area-admissible 2-Lambda HNF census changed")
    shape = decode_compiled_key(KEY)
    tasks = [(shape, hnf, signature_rows) for hnf in hnfs]
    print(f"2-Lambda packing-family cases: {len(tasks)}; jobs={args.jobs}", flush=True)
    rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_solve, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            row = future.result()
            rows.append(row)
            print(
                f"[{completed:3d}/{len(tasks)}] {tuple(row['hnf'])} "
                f"{'SAT' if row['sat'] else 'UNSAT'} "
                f"({row['solve_seconds']:.2f}s)", flush=True,
            )
    rows.sort(key=lambda row: (row["index"], row["hnf"]))
    by_index = []
    for index in sorted({row["index"] for row in rows}):
        current = [row for row in rows if row["index"] == index]
        by_index.append({
            "index": index,
            "hnfs": len(current),
            "packing_obstructed": sum(not row["sat"] for row in current),
            "not_obstructed": sum(row["sat"] for row in current),
        })
    sat_rows = [row for row in rows if row["sat"]]
    dependencies = (BASE, PACKING60)
    sources = (
        ROOT / "src/einstein/theory/a4_v4_lift.py",
        ROOT / "src/einstein/theory/a4_v4_packing.py",
        ROOT / "src/einstein/theory/a4_v4_product.py",
        ROOT / "src/einstein/theory/a4_v4_packing_family.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-v4-single-orbit-packing-family-falsification",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "family": "HNF sublattices of 2 Lambda",
            "area_admissible_only": True,
            "maximum_index": args.maximum_index,
            "indices": [row["index"] for row in by_index],
            "hnfs": len(rows),
            "signature_layers": len(signature_rows),
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
            "packing_obstructed": len(rows) - len(sat_rows),
            "not_obstructed": len(sat_rows),
            "first_not_obstructed_index": min(
                (row["index"] for row in sat_rows), default=None
            ),
            "candidate_infinite_family_survives_falsification": not sat_rows,
        },
        "by_index": by_index,
        "results": rows,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({"summary": payload["summary"], "by_index": by_index}, indent=1))


if __name__ == "__main__":
    main()
