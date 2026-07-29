#!/usr/bin/env python
"""Test all strong A4 maps on the twelve S3-surviving index-50 HNFs."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.finite_groups import alternating_group
from einstein.theory.holonomy_csp import _cnf_sha256
from einstein.theory.holonomy_finite_csp import (
    build_finite_boundary_holonomy_cnf,
    commuting_pairs,
)
from einstein.theory.holonomy_quotients import pullback_images
from einstein.theory.holonomy_symmetry import hnf_d6_image


ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / "docs/notebook/assets/theory-w2-layer-d-small-groups.json"
S3 = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _solve_twist(arguments):
    shape, orbit_index, hnf, mapping_index, images, group, twist_index, twists = arguments
    started = perf_counter()
    cnf, metadata = build_finite_boundary_holonomy_cnf(
        shape, hnf, images, twists, group
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        stats = solver.accum_stats()
    return {
        "pair_orbit": orbit_index,
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
    census = json.loads(CENSUS.read_text())
    s3 = json.loads(S3.read_text())
    group = alternating_group(4)
    target = next(row for row in census["results"] if row["target"] == "A4")
    mappings = tuple(
        tuple(images) for images in target["representatives_by_kernel"]["4"]
    )
    if len(mappings) != 48:
        raise AssertionError("A4 strong-map census changed")
    mapping_index = {images: index for index, images in enumerate(mappings)}
    hnfs = sorted(
        tuple(row["hnf"]) for row in s3["finalist"]["by_hnf"]
        if row["verdict"] == "not-obstructed"
    )
    if len(hnfs) != 12:
        raise AssertionError("expected twelve S3-surviving HNFs")

    unseen = {(hnf, index) for hnf in hnfs for index in range(len(mappings))}
    pair_orbits = []
    while unseen:
        seed = min(unseen)
        members = frozenset(
            (
                hnf_d6_image(seed[0], op),
                mapping_index[pullback_images(mappings[seed[1]], op, group)],
            )
            for op in range(12)
        )
        if not members <= unseen:
            raise AssertionError("A4 diagonal action failed to partition scope")
        unseen.difference_update(members)
        pair_orbits.append(members)
    if len(pair_orbits) != 48:
        raise AssertionError(f"expected 48 pair orbits, got {len(pair_orbits)}")
    representatives = {}
    shape = decode_compiled_key(KEY)
    for orbit_index, members in enumerate(pair_orbits):
        hnf, index = min(members)
        representatives[orbit_index] = (hnf, index)
    twists = commuting_pairs(group)
    print(
        f"A4 index 50: {len(hnfs)} HNFs x {len(mappings)} maps = 576 pairs; "
        f"{len(representatives)} D6 representatives; 48 twists; jobs={args.jobs}",
        flush=True,
    )
    results = {
        orbit_index: {
            "pair_orbit": orbit_index,
            "representative": {"hnf": list(hnf), "mapping_index": index},
            "sat_twist_index": None,
            "checks": [],
        }
        for orbit_index, (hnf, index) in representatives.items()
    }
    unresolved = set(representatives)
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        for twist_index, twist_pair in enumerate(twists):
            if not unresolved:
                break
            futures = []
            for orbit_index in sorted(unresolved):
                hnf, index = representatives[orbit_index]
                task = (shape, orbit_index, hnf, index, mappings[index], group,
                        twist_index, twist_pair)
                futures.append(executor.submit(_solve_twist, task))
            resolved = []
            for future in as_completed(futures):
                check = future.result()
                orbit_index = check["pair_orbit"]
                results[orbit_index]["checks"].append(check)
                if check["sat"]:
                    results[orbit_index]["sat_twist_index"] = twist_index
                    resolved.append(orbit_index)
            unresolved.difference_update(resolved)
            print(
                f"twist {twist_index:02d}/47: SAT={len(resolved):2d}; "
                f"unresolved={len(unresolved):2d}", flush=True,
            )
    for row in results.values():
        row["checks"].sort(key=lambda check: check["twist_index"])
        row["twist_pairs_checked"] = len(row["checks"])
        row["verdict"] = (
            "holonomy-obstructed"
            if row["sat_twist_index"] is None else "not-obstructed"
        )
        row["worker_seconds"] = sum(
            check["wall_seconds"] for check in row["checks"]
        )
    results = sorted(results.values(), key=lambda row: row["pair_orbit"])
    killed_orbits = [row["pair_orbit"] for row in results
                     if row["verdict"] == "holonomy-obstructed"]
    covered = {hnf for orbit_index in killed_orbits
               for hnf, _ in pair_orbits[orbit_index]}
    print(
        f"complete: killing pair orbits={len(killed_orbits)}; "
        f"HNFs={len(covered)}/{len(hnfs)}",
        flush=True,
    )
    verdict = {row["pair_orbit"]: row["verdict"] for row in results}
    expanded = {
        pair: verdict[orbit_index]
        for orbit_index, members in enumerate(pair_orbits)
        for pair in members
    }
    by_hnf = []
    for hnf in hnfs:
        killers = [index for index in range(len(mappings))
                   if expanded[(hnf, index)] == "holonomy-obstructed"]
        by_hnf.append({
            "hnf": list(hnf), "killing_mapping_indices": killers,
            "verdict": "holonomy-obstructed" if killers else "not-obstructed",
        })
    sources = (
        ROOT / "src/einstein/theory/finite_groups.py",
        ROOT / "src/einstein/theory/holonomy_quotients.py",
        ROOT / "src/einstein/theory/holonomy_finite_csp.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-a4-index50-exhaustion",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "target": "A4", "target_order": 12,
            "displacement_kernel_order": 4,
            "frontier_hnfs": len(hnfs), "mapping_classes": len(mappings),
            "logical_pairs": len(expanded), "d6_pair_orbits": len(pair_orbits),
            "commuting_twists": 48,
            "proof_status": "search only; independent certificates required for kills",
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)),
                 "sha256": sha256(path.read_bytes()).hexdigest()}
                for path in (CENSUS, S3)
            ],
            "sources": [
                {"path": str(path.relative_to(ROOT)),
                 "sha256": sha256(path.read_bytes()).hexdigest()}
                for path in sources
            ],
        },
        "finalist": {
            "shape": KEY,
            "mapping_representatives": [list(images) for images in mappings],
            "pair_orbits": [
                {"index": index, "members": [
                    {"hnf": list(hnf), "mapping_index": mapping_index}
                    for hnf, mapping_index in sorted(members)
                ]} for index, members in enumerate(pair_orbits)
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
