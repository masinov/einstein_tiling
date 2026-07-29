#!/usr/bin/env python
"""Validate and extend the map-7 two-bit coverability SFT through index 60."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.local_system import (
    V4_TWIST_PAIRS,
    build_map7_v4_coverability_cnf,
)


ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "docs/notebook/assets/theory-w2-binary-families.json"
FACTOR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-factor.json"
A4_INDEX55 = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature-index55.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-sft-index60.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _solve(arguments):
    shape, hnf, twist_index, twists = arguments
    started = perf_counter()
    cnf, metadata = build_map7_v4_coverability_cnf(shape, hnf, twists)
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    return {
        "hnf": list(hnf),
        "twist_index": twist_index,
        "twists": list(twists),
        "sat": sat,
        "cnf_sha256": sha256("".join(
            " ".join(map(str, clause)) + " 0\n" for clause in cnf.clauses
        ).encode()).hexdigest(),
        "metadata": metadata,
        "conflicts": stats.get("conflicts"),
        "wall_seconds": perf_counter() - started,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    args = parser.parse_args()
    binary = json.loads(BINARY.read_text())
    a4_index55 = json.loads(A4_INDEX55.read_text())
    shells = {}
    for index in (55, 60):
        shell = next(
            row for row in binary["admissible_horizon"]["by_index"]
            if row["index"] == index
        )
        shells[index] = tuple(sorted(
            tuple(row["hnf"]) for row in shell["results"]
            if row["certificate"] is None
        ))
    if len(shells[55]) != 21 or len(shells[60]) != 45:
        raise AssertionError("W1 frontier changed")
    if a4_index55["summary"]["covered_hnfs"] != 21:
        raise AssertionError("index-55 A4 control is not closed")

    shape = decode_compiled_key(KEY)
    tasks = [
        (shape, hnf, twist_index, twists)
        for index in (55, 60) for hnf in shells[index]
        for twist_index, twists in enumerate(V4_TWIST_PAIRS)
    ]
    print(f"V4 SFT tasks: {len(tasks)}; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_solve, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            row = future.result()
            results.append(row)
            if completed % 24 == 0 or completed == len(tasks):
                print(f"[{completed:4d}/{len(tasks)}] complete", flush=True)
    results.sort(key=lambda row: (row["hnf"][0] * row["hnf"][2], row["hnf"], row["twist_index"]))

    by_index = []
    for index in (55, 60):
        hnf_rows = []
        for hnf in shells[index]:
            checks = [
                row for row in results
                if tuple(row["hnf"]) == hnf
            ]
            checks.sort(key=lambda row: row["twist_index"])
            if len(checks) != len(V4_TWIST_PAIRS):
                raise AssertionError("incomplete HNF/twist product")
            sat_twists = [row["twist_index"] for row in checks if row["sat"]]
            hnf_rows.append({
                "hnf": list(hnf),
                "sat_twist_indices": sat_twists,
                "verdict": "holonomy-obstructed" if not sat_twists else "not-obstructed",
                "checks": checks,
            })
        obstructed = sum(row["verdict"] == "holonomy-obstructed" for row in hnf_rows)
        by_index.append({
            "index": index,
            "frontier_hnfs": len(hnf_rows),
            "obstructed_hnfs": obstructed,
            "surviving_hnfs": len(hnf_rows) - obstructed,
            "results": hnf_rows,
        })
    if by_index[0]["obstructed_hnfs"] != 21:
        raise AssertionError("two-bit factor disagrees with the index-55 control")

    dependencies = (BINARY, FACTOR, A4_INDEX55)
    sources = (
        ROOT / "src/einstein/holonomy/alternating4/group.py",
        ROOT / "src/einstein/holonomy/alternating4/local_system.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-map7-v4-local-sft-index60",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "indices": [55, 60],
            "map": 7,
            "twists": len(V4_TWIST_PAIRS),
            "logical_cases": len(tasks),
            "proof_status": "search only; index-55 has independent full-A4 certificates",
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
        "reduction": {
            "potential": "two bits per quotient vertex (V4 = GF(2)^2)",
            "c3_normalization": "q(vertex) = 2*x+y mod 3",
            "local_rule": (
                "every cell has a covering placement whose boundary obeys "
                "v_end=v_deck+v_start+M^q_start*v_label"
            ),
            "exact_cover_polarity": (
                "sound necessary condition via connected boundary skeleton"
            ),
        },
        "by_index": by_index,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps([
        {key: row[key] for key in (
            "index", "frontier_hnfs", "obstructed_hnfs", "surviving_hnfs"
        )}
        for row in by_index
    ], indent=1))


if __name__ == "__main__":
    main()
