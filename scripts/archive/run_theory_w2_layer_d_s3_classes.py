#!/usr/bin/env python
"""Exhaust the 39 inner-conjugacy classes of strong finalist S3 quotients."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.polykites.database import code_version
from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.boundary import (
    s3_boundary_surjections,
    verify_s3_boundary_quotient,
)
from einstein.holonomy.constraints import scan_boundary_holonomy


ROOT = Path(__file__).resolve().parents[2]
PHASE1 = ROOT / "docs/notebook/assets/theory-w2-layer-d-coupled.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-classes.json"
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
    parser.add_argument("--indices", type=int, nargs="+", default=[40])
    args = parser.parse_args()

    phase1 = json.loads(PHASE1.read_text())
    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(
        shape,
        displacement_kernel_order=3,
        conjugacy_reduced=True,
    )
    if len(mappings) != 39:
        raise AssertionError("expected 39 inner-conjugacy classes")
    if not all(
        verify_s3_boundary_quotient(shape, images, require_surjective=True)
        for images in mappings
    ):
        raise AssertionError("invalid S3 boundary quotient representative")

    hnfs = sorted({
        tuple(row["hnf"])
        for row in phase1["finalist"]["results"]
        if row["index"] in args.indices
        and row["cascade_verdict"] == "survives-tested-stack"
    })
    if not hnfs:
        raise AssertionError("no phase-1 frontier HNFs selected")
    tasks = [
        (shape, hnf, mapping_index, images)
        for hnf in hnfs
        for mapping_index, images in enumerate(mappings)
    ]
    print(
        f"S3 class matrix: {len(hnfs)} HNFs x {len(mappings)} maps "
        f"= {len(tasks)} scans; jobs={args.jobs}",
        flush=True,
    )
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(_scan, task): task[1:3] for task in tasks}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            if completed % 5 == 0 or result["scan"]["verdict"] == "holonomy-obstructed":
                print(
                    f"[{completed:3d}/{len(tasks)}] {tuple(result['hnf'])} "
                    f"map={result['mapping_index']:02d}: "
                    f"{result['scan']['verdict']} "
                    f"({result['scan']['twist_pairs_checked']} twists, "
                    f"{result['wall_seconds']:.2f}s)",
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

    sources = (
        ROOT / "src/einstein/holonomy/boundary.py",
        ROOT / "src/einstein/holonomy/constraints.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-s3-conjugacy-class-exhaustion",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "indices": sorted(args.indices),
            "displacement_kernel_order": 3,
            "surjections_before_inner_conjugacy": 234,
            "inner_conjugacy_classes": 39,
            "equivalence": (
                "simultaneous inner conjugation of generator images, vertex "
                "potentials, and the exhaustive commuting twist pairs is a "
                "CNF-model bijection"
            ),
            "positive_polarity": (
                "one class obstructing all 18 twists excludes that HNF"
            ),
            "negative_polarity": (
                "compatibility for all 39 S3 classes does not imply tileability"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "phase1": {
                "path": str(PHASE1.relative_to(ROOT)),
                "sha256": sha256(PHASE1.read_bytes()).hexdigest(),
            },
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
            "mapping_representatives": [
                {
                    "index": index,
                    "id": _mapping_id(images),
                    "generator_images": images,
                }
                for index, images in enumerate(mappings)
            ],
            "by_hnf": by_hnf,
            "results": results,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(by_hnf, indent=1))


if __name__ == "__main__":
    main()
