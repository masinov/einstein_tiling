#!/usr/bin/env python
"""Test all 16 distinct-tail A4 maps on the map-7 index-60 escapes."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_sft import (
    V4_TWIST_PAIRS,
    build_v4_coverability_cnf,
)
from einstein.theory.holonomy_csp import _cnf_sha256


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
SIGNATURE = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature.json"
MAP7_SCAN = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-sft-index60.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-signature-index60.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _solve(arguments):
    shape, hnf, mapping_index, images, twist_index, twists = arguments
    started = perf_counter()
    cnf, metadata = build_v4_coverability_cnf(shape, hnf, images, twists)
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    return {
        "hnf": list(hnf),
        "mapping_index": mapping_index,
        "twist_index": twist_index,
        "twists": list(twists),
        "sat": sat,
        "cnf_sha256": _cnf_sha256(cnf),
        "metadata": metadata,
        "conflicts": stats.get("conflicts"),
        "wall_seconds": perf_counter() - started,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    args = parser.parse_args()
    matrix = json.loads(MATRIX.read_text())
    signature = json.loads(SIGNATURE.read_text())
    map7_scan = json.loads(MAP7_SCAN.read_text())
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    signature_maps = tuple(signature["finite_signature"]["killing_mapping_indices"])
    if len(signature_maps) != 16:
        raise AssertionError("distinct-tail signature changed")
    shell60 = next(row for row in map7_scan["by_index"] if row["index"] == 60)
    hnfs = tuple(sorted(
        tuple(row["hnf"]) for row in shell60["results"]
        if row["verdict"] == "not-obstructed"
    ))
    if hnfs != ((10, 2, 6), (30, 6, 2), (30, 22, 2)):
        raise AssertionError("map-7 index-60 escape orbit changed")

    shape = decode_compiled_key(KEY)
    tasks = [
        (shape, hnf, mapping_index, mappings[mapping_index], twist_index, twists)
        for hnf in hnfs for mapping_index in signature_maps
        for twist_index, twists in enumerate(V4_TWIST_PAIRS)
    ]
    print(f"index-60 residual signature tasks: {len(tasks)}; jobs={args.jobs}", flush=True)
    checks = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_solve, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            checks.append(future.result())
            if completed % 24 == 0 or completed == len(tasks):
                print(f"[{completed:3d}/{len(tasks)}] complete", flush=True)
    checks.sort(key=lambda row: (row["hnf"], row["mapping_index"], row["twist_index"]))

    by_hnf = []
    pair_results = []
    for hnf in hnfs:
        killers = []
        for mapping_index in signature_maps:
            rows = [
                row for row in checks
                if tuple(row["hnf"]) == hnf and row["mapping_index"] == mapping_index
            ]
            if len(rows) != len(V4_TWIST_PAIRS):
                raise AssertionError("incomplete map/twist product")
            sat_twists = [row["twist_index"] for row in rows if row["sat"]]
            if not sat_twists:
                killers.append(mapping_index)
            pair_results.append({
                "hnf": list(hnf),
                "mapping_index": mapping_index,
                "sat_twist_indices": sat_twists,
                "verdict": "holonomy-obstructed" if not sat_twists else "not-obstructed",
                "checks": rows,
            })
        by_hnf.append({
            "hnf": list(hnf),
            "killing_mapping_indices": killers,
            "verdict": "holonomy-obstructed" if killers else "not-obstructed",
        })
    covered = sum(row["verdict"] == "holonomy-obstructed" for row in by_hnf)

    dependencies = (MATRIX, SIGNATURE, MAP7_SCAN)
    sources = (
        ROOT / "src/einstein/theory/a4_semidirect.py",
        ROOT / "src/einstein/theory/a4_v4_sft.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-v4-signature-index60-residual",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "index": 60,
            "map7_escape_hnfs": len(hnfs),
            "signature_maps": len(signature_maps),
            "v4_twists": len(V4_TWIST_PAIRS),
            "logical_cases": len(tasks),
            "proof_status": "search only",
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
            "covered_escape_hnfs": covered,
            "surviving_escape_hnfs": len(hnfs) - covered,
            "killing_hnf_map_pairs": sum(
                row["verdict"] == "holonomy-obstructed" for row in pair_results
            ),
        },
        "by_hnf": by_hnf,
        "pair_results": pair_results,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({"summary": payload["summary"], "by_hnf": by_hnf}, indent=1))


if __name__ == "__main__":
    main()
