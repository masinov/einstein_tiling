#!/usr/bin/env python
"""Exhaust the 39 strong S3 quotient classes on the index-45 frontier."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy import (
    s3_boundary_surjections,
    verify_s3_boundary_quotient,
)
from einstein.theory.holonomy_csp import scan_boundary_holonomy


ROOT = Path(__file__).resolve().parents[2]
PHASE1 = ROOT / "docs/notebook/assets/theory-w2-layer-d-coupled.json"
INDEX40 = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-classes.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index45.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _mapping_id(images):
    encoded = json.dumps(images, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()[:16]


def _scan(arguments):
    shape, hnf, mapping_index, images = arguments
    started = perf_counter()
    result = scan_boundary_holonomy(
        shape,
        hnf,
        images,
        cover_mode="at-least",
        stop_on_sat=True,
    )
    return {
        "hnf": list(hnf),
        "mapping_index": mapping_index,
        "mapping_id": _mapping_id(images),
        "wall_seconds": perf_counter() - started,
        "scan": result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=16)
    args = parser.parse_args()

    phase1 = json.loads(PHASE1.read_text())
    index40 = json.loads(INDEX40.read_text())
    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(
        shape,
        displacement_kernel_order=3,
        conjugacy_reduced=True,
    )
    if len(mappings) != 39 or not all(
        verify_s3_boundary_quotient(shape, images, require_surjective=True)
        for images in mappings
    ):
        raise AssertionError("strong S3 conjugacy-class enumeration changed")

    hnfs = sorted({
        tuple(row["hnf"])
        for row in phase1["finalist"]["results"]
        if row["index"] == 45
        and row["cascade_verdict"] == "survives-tested-stack"
    })
    if len(hnfs) != 9:
        raise AssertionError(f"expected nine index-45 frontier HNFs, got {len(hnfs)}")

    high_yield = sorted({
        mapping_index
        for row in index40["finalist"]["by_hnf"]
        for mapping_index in row["killing_mapping_indices"]
    })
    remaining = [index for index in range(len(mappings)) if index not in high_yield]
    mapping_order = high_yield + remaining
    tasks = [
        (shape, hnf, mapping_index, mappings[mapping_index])
        for mapping_index in mapping_order
        for hnf in hnfs
    ]
    print(
        f"index 45: {len(hnfs)} HNFs x {len(mappings)} maps = "
        f"{len(tasks)} scans; jobs={args.jobs}; priority maps={high_yield}",
        flush=True,
    )
    results = []
    first_kills = {}
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(_scan, task): task[1:3] for task in tasks}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            if result["scan"]["verdict"] == "holonomy-obstructed":
                first_kills.setdefault(tuple(result["hnf"]), result["mapping_index"])
                print(
                    f"[{completed:3d}/{len(tasks)}] KILL {tuple(result['hnf'])} "
                    f"map={result['mapping_index']:02d} "
                    f"({result['wall_seconds']:.1f}s)",
                    flush=True,
                )
            elif completed % 20 == 0:
                print(
                    f"[{completed:3d}/{len(tasks)}] {len(first_kills)}/{len(hnfs)} "
                    "HNFs killed so far",
                    flush=True,
                )
    results.sort(key=lambda row: (row["hnf"], row["mapping_index"]))

    by_hnf = []
    for hnf in hnfs:
        subset = [row for row in results if tuple(row["hnf"]) == hnf]
        killed = [
            row["mapping_index"]
            for row in subset
            if row["scan"]["verdict"] == "holonomy-obstructed"
        ]
        by_hnf.append({
            "hnf": list(hnf),
            "mappings_tested": len(subset),
            "killing_mapping_indices": killed,
            "verdict": "holonomy-obstructed" if killed else "not-obstructed",
        })

    by_mapping = []
    for mapping_index in range(len(mappings)):
        killed = [
            row["hnf"]
            for row in results
            if row["mapping_index"] == mapping_index
            and row["scan"]["verdict"] == "holonomy-obstructed"
        ]
        by_mapping.append({
            "mapping_index": mapping_index,
            "mapping_id": _mapping_id(mappings[mapping_index]),
            "hnfs_killed": killed,
        })

    sources = (
        ROOT / "src/einstein/theory/holonomy.py",
        ROOT / "src/einstein/theory/holonomy_csp.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-s3-index45-exhaustion",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "index": 45,
            "frontier_hnfs": len(hnfs),
            "displacement_kernel_order": 3,
            "inner_conjugacy_classes": len(mappings),
            "matrix_complete": len(results) == len(hnfs) * len(mappings),
            "positive_polarity": (
                "one verified boundary quotient obstructing all 18 commuting "
                "twists excludes that HNF, subject to independent proof replay"
            ),
            "proof_status": (
                "search matrix only; DRAT core production is the next gate for kills"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "dependencies": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in (PHASE1, INDEX40)
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
            "priority_mapping_indices": high_yield,
            "mapping_representatives": [
                {
                    "index": index,
                    "id": _mapping_id(images),
                    "generator_images": images,
                }
                for index, images in enumerate(mappings)
            ],
            "by_hnf": by_hnf,
            "by_mapping": by_mapping,
            "results": results,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(by_hnf, indent=1))


if __name__ == "__main__":
    main()
