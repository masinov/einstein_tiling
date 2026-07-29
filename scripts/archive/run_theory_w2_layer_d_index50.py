#!/usr/bin/env python
"""Exhaust index 50 modulo the exact diagonal D6 covariance (T2.D3)."""

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
from einstein.holonomy.symmetry import hnf_d6_image, pullback_s3_images


ROOT = Path(__file__).resolve().parents[2]
PHASE1 = ROOT / "docs/notebook/assets/theory-w2-layer-d-coupled.json"
SYMMETRY = ROOT / "docs/notebook/assets/theory-w2-layer-d-symmetry.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"
PRIORITY_MAPS = frozenset((9, 15, 18, 21, 24, 27, 30, 33, 36))


def _mapping_id(images):
    encoded = json.dumps(images, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()[:16]


def _scan(arguments):
    shape, orbit_index, hnf, mapping_index, images = arguments
    started = perf_counter()
    result = scan_boundary_holonomy(
        shape, hnf, images, cover_mode="at-least", stop_on_sat=True
    )
    return {
        "pair_orbit": orbit_index,
        "representative": {
            "hnf": list(hnf),
            "mapping_index": mapping_index,
            "mapping_id": _mapping_id(images),
        },
        "wall_seconds": perf_counter() - started,
        "scan": result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=16)
    args = parser.parse_args()

    phase1 = json.loads(PHASE1.read_text())
    symmetry = json.loads(SYMMETRY.read_text())
    if not symmetry["scope"]["all_checks_passed"]:
        raise AssertionError("T2.D3 covariance artifact is not verified")
    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(
        shape, displacement_kernel_order=3, conjugacy_reduced=True
    )
    if len(mappings) != 39 or not all(
        verify_s3_boundary_quotient(shape, images, require_surjective=True)
        for images in mappings
    ):
        raise AssertionError("strong S3 conjugacy-class enumeration changed")
    mapping_index = {images: index for index, images in enumerate(mappings)}
    hnfs = sorted({
        tuple(row["hnf"])
        for row in phase1["finalist"]["results"]
        if row["index"] == 50
        and row["cascade_verdict"] == "survives-tested-stack"
    })
    if len(hnfs) != 18:
        raise AssertionError(f"expected 18 index-50 frontier HNFs, got {len(hnfs)}")

    unseen = {(hnf, index) for hnf in hnfs for index in range(len(mappings))}
    pair_orbits = []
    while unseen:
        seed = min(unseen)
        members = frozenset(
            (
                hnf_d6_image(seed[0], op),
                mapping_index[pullback_s3_images(mappings[seed[1]], op)],
            )
            for op in range(12)
        )
        if not members <= unseen:
            raise AssertionError("diagonal D6 action did not partition frontier")
        unseen.difference_update(members)
        pair_orbits.append(members)

    representatives = []
    for orbit_index, members in enumerate(pair_orbits):
        hnf, index = min(
            members,
            key=lambda pair: (pair[1] not in PRIORITY_MAPS, pair[1], pair[0]),
        )
        representatives.append((orbit_index, hnf, index))
    representatives.sort(
        key=lambda row: (row[2] not in PRIORITY_MAPS, row[2], row[1])
    )
    tasks = [
        (shape, orbit_index, hnf, index, mappings[index])
        for orbit_index, hnf, index in representatives
    ]
    print(
        f"index 50: {len(hnfs)} HNFs x {len(mappings)} maps = "
        f"{len(hnfs) * len(mappings)} logical pairs; "
        f"{len(tasks)} D6-orbit representatives; jobs={args.jobs}",
        flush=True,
    )

    results = []
    covered_hnfs = set()
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(_scan, task): task[1:4] for task in tasks}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            if result["scan"]["verdict"] == "holonomy-obstructed":
                members = pair_orbits[result["pair_orbit"]]
                covered_hnfs.update(hnf for hnf, _ in members)
                print(
                    f"[{completed:2d}/{len(tasks)}] KILL orbit "
                    f"{result['pair_orbit']:02d} rep="
                    f"{tuple(result['representative']['hnf'])}/"
                    f"m{result['representative']['mapping_index']:02d}; "
                    f"covered HNFs={len(covered_hnfs)}/{len(hnfs)} "
                    f"({result['wall_seconds']:.1f}s)",
                    flush=True,
                )
            elif completed % 10 == 0:
                print(
                    f"[{completed:2d}/{len(tasks)}] covered HNFs="
                    f"{len(covered_hnfs)}/{len(hnfs)}",
                    flush=True,
                )
    results.sort(key=lambda row: row["pair_orbit"])
    orbit_verdict = {
        row["pair_orbit"]: row["scan"]["verdict"] for row in results
    }
    expanded = {
        pair: orbit_verdict[orbit_index]
        for orbit_index, members in enumerate(pair_orbits)
        for pair in members
    }
    if len(expanded) != len(hnfs) * len(mappings):
        raise AssertionError("expanded matrix is incomplete")

    by_hnf = []
    for hnf in hnfs:
        killed = [
            index for index in range(len(mappings))
            if expanded[(hnf, index)] == "holonomy-obstructed"
        ]
        by_hnf.append({
            "hnf": list(hnf),
            "killing_mapping_indices": killed,
            "verdict": "holonomy-obstructed" if killed else "not-obstructed",
        })

    sources = (
        ROOT / "src/einstein/holonomy/boundary.py",
        ROOT / "src/einstein/holonomy/constraints.py",
        ROOT / "src/einstein/holonomy/symmetry.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-s3-index50-d6-exhaustion",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "index": 50,
            "frontier_hnfs": len(hnfs),
            "inner_conjugacy_classes": len(mappings),
            "logical_matrix_entries": len(expanded),
            "d6_pair_orbits": len(pair_orbits),
            "representative_scans_complete": len(results) == len(pair_orbits),
            "expansion_theorem": "T2.D3",
            "proof_status": "search matrix; DRAT production required for kills",
        },
        "provenance": {
            "code_version": code_version(),
            "dependencies": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in (PHASE1, SYMMETRY)
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
            "mapping_representatives": [
                {
                    "index": index,
                    "id": _mapping_id(images),
                    "generator_images": images,
                }
                for index, images in enumerate(mappings)
            ],
            "pair_orbits": [
                {
                    "index": orbit_index,
                    "members": [
                        {"hnf": list(hnf), "mapping_index": index}
                        for hnf, index in sorted(members)
                    ],
                }
                for orbit_index, members in enumerate(pair_orbits)
            ],
            "representative_results": results,
            "by_hnf": by_hnf,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(by_hnf, indent=1))


if __name__ == "__main__":
    main()
