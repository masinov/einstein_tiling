#!/usr/bin/env python
"""Scan the index-50 D6 pair orbits with cell multiplicity bounded by two."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy_overlap import scan_bounded_overlap_holonomy


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index50.json"
MODELS = ROOT / "docs/notebook/assets/theory-w2-layer-d-models-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-overlap2-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _scan(arguments):
    shape, orbit_index, hnf, mapping_index, images = arguments
    started = perf_counter()
    scan = scan_bounded_overlap_holonomy(
        shape, hnf, images, maximum_coverage=2, stop_on_sat=True
    )
    return {
        "pair_orbit": orbit_index,
        "representative": {
            "hnf": list(hnf),
            "mapping_index": mapping_index,
        },
        "wall_seconds": perf_counter() - started,
        "scan": scan,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    args = parser.parse_args()
    base = json.loads(BASE.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in base["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    pair_orbits = base["finalist"]["pair_orbits"]
    old_results = {
        row["pair_orbit"]: row for row in base["finalist"]["representative_results"]
    }
    tasks = []
    for item in pair_orbits:
        representative = old_results[item["index"]]["representative"]
        hnf = tuple(representative["hnf"])
        mapping_index = representative["mapping_index"]
        tasks.append((shape, item["index"], hnf, mapping_index, mappings[mapping_index]))
    print(f"index-50 overlap<=2: {len(tasks)} D6 pair orbits; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_scan, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            if result["scan"]["verdict"] == "holonomy-obstructed":
                print(
                    f"[{completed:2d}/{len(tasks)}] KILL orbit "
                    f"{result['pair_orbit']:02d} "
                    f"({result['wall_seconds']:.1f}s)",
                    flush=True,
                )
            elif completed % 10 == 0:
                print(f"[{completed:2d}/{len(tasks)}]", flush=True)
    results.sort(key=lambda row: row["pair_orbit"])
    verdict = {row["pair_orbit"]: row["scan"]["verdict"] for row in results}
    expanded = {}
    for item in pair_orbits:
        for member in item["members"]:
            expanded[(tuple(member["hnf"]), member["mapping_index"])] = verdict[item["index"]]
    hnfs = sorted({hnf for hnf, _ in expanded})
    by_hnf = []
    for hnf in hnfs:
        killers = [
            index for index in range(len(mappings))
            if expanded[(hnf, index)] == "holonomy-obstructed"
        ]
        by_hnf.append({
            "hnf": list(hnf),
            "killing_mapping_indices": killers,
            "verdict": "holonomy-obstructed" if killers else "not-obstructed",
        })
    sources = (
        ROOT / "src/einstein/theory/holonomy_overlap.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-index50-overlap2-exhaustion",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "maximum_coverage": 2,
            "frontier_hnfs": len(hnfs),
            "mapping_classes": len(mappings),
            "logical_pairs": len(expanded),
            "d6_pair_orbits": len(results),
            "representative_scans_complete": len(results) == len(pair_orbits),
            "soundness": (
                "every exact cover satisfies coverage at most two; UNSAT over "
                "all commuting twists therefore excludes an exact cover"
            ),
            "proof_status": "search only; independent DRAT required for new kills",
        },
        "provenance": {
            "dependencies": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in (BASE, MODELS)
            ],
            "sources": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in sources
            ],
        },
        "finalist": {
            "shape": KEY,
            "representative_results": results,
            "by_hnf": by_hnf,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(by_hnf, indent=1))


if __name__ == "__main__":
    main()
