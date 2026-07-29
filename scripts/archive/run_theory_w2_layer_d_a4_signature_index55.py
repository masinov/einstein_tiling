#!/usr/bin/env python
"""Falsify the index-50 A4 map signature on the index-55 W1 frontier."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.combinatorics.finite_groups import alternating_group
from einstein.holonomy.constraints import _cnf_sha256
from einstein.holonomy.finite_constraints import (
    build_finite_boundary_holonomy_cnf,
    commuting_pairs,
)
from einstein.holonomy.quotients import pullback_images
from einstein.holonomy.symmetry import hnf_d6_image


ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "docs/notebook/assets/theory-w2-binary-families.json"
A4_MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
SIGNATURE = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature-index55.json"
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
    binary = json.loads(BINARY.read_text())
    matrix = json.loads(A4_MATRIX.read_text())
    signature = json.loads(SIGNATURE.read_text())
    group = alternating_group(4)
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    mapping_index = {images: index for index, images in enumerate(mappings)}
    signature_maps = frozenset(
        signature["finite_signature"]["killing_mapping_indices"]
    )
    if len(signature_maps) != 16:
        raise AssertionError("expected the 16-class distinct-V4-tail signature")

    shell = next(
        row for row in binary["admissible_horizon"]["by_index"]
        if row["index"] == 55
    )
    hnfs = tuple(sorted(
        tuple(row["hnf"]) for row in shell["results"]
        if row["certificate"] is None
    ))
    if len(hnfs) != 21:
        raise AssertionError(f"expected 21 index-55 W1 survivors, got {len(hnfs)}")

    unseen = {(hnf, index) for hnf in hnfs for index in signature_maps}
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
            raise AssertionError("signature scope is not closed under diagonal D6")
        unseen.difference_update(members)
        pair_orbits.append(members)
    if len(pair_orbits) != 28 or any(len(orbit) != 12 for orbit in pair_orbits):
        raise AssertionError("expected 28 free diagonal D6 pair orbits")

    representatives = {
        orbit_index: min(members)
        for orbit_index, members in enumerate(pair_orbits)
    }
    shape = decode_compiled_key(KEY)
    twists = commuting_pairs(group)
    print(
        f"A4 signature index 55: {len(hnfs)} HNFs x {len(signature_maps)} maps "
        f"= {len(hnfs) * len(signature_maps)} pairs; "
        f"{len(pair_orbits)} D6 representatives; {len(twists)} twists; "
        f"jobs={args.jobs}",
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
                task = (
                    shape, orbit_index, hnf, index, mappings[index], group,
                    twist_index, twist_pair,
                )
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
                f"unresolved={len(unresolved):2d}",
                flush=True,
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
    orbit_verdict = {row["pair_orbit"]: row["verdict"] for row in results}
    expanded = {
        pair: orbit_verdict[orbit_index]
        for orbit_index, members in enumerate(pair_orbits)
        for pair in members
    }
    by_hnf = []
    for hnf in hnfs:
        killers = sorted(
            index for index in signature_maps
            if expanded[(hnf, index)] == "holonomy-obstructed"
        )
        by_hnf.append({
            "hnf": list(hnf),
            "killing_signature_mapping_indices": killers,
            "verdict": "holonomy-obstructed" if killers else "not-obstructed",
        })
    covered_hnfs = sum(row["verdict"] == "holonomy-obstructed" for row in by_hnf)
    killing_pair_orbits = sum(
        row["verdict"] == "holonomy-obstructed" for row in results
    )
    print(
        f"complete: killing pair orbits={killing_pair_orbits}; "
        f"covered HNFs={covered_hnfs}/{len(hnfs)}",
        flush=True,
    )

    dependencies = (BINARY, A4_MATRIX, SIGNATURE)
    sources = (
        ROOT / "src/einstein/combinatorics/finite_groups.py",
        ROOT / "src/einstein/holonomy/quotients.py",
        ROOT / "src/einstein/holonomy/finite_constraints.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-a4-signature-index55-falsification",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "index": 55,
            "frontier_hnfs": len(hnfs),
            "signature_mapping_classes": len(signature_maps),
            "logical_pairs": len(expanded),
            "d6_pair_orbits": len(pair_orbits),
            "commuting_twists": len(twists),
            "proof_status": "search only; UNSAT cases require independent certificates",
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)),
                 "sha256": sha256(path.read_bytes()).hexdigest()}
                for path in dependencies
            ],
            "sources": [
                {"path": str(path.relative_to(ROOT)),
                 "sha256": sha256(path.read_bytes()).hexdigest()}
                for path in sources
            ],
        },
        "summary": {
            "killing_pair_orbits": killing_pair_orbits,
            "sat_pair_orbits": len(results) - killing_pair_orbits,
            "covered_hnfs": covered_hnfs,
            "surviving_hnfs": len(hnfs) - covered_hnfs,
        },
        "finalist": {
            "shape": KEY,
            "signature_mapping_indices": sorted(signature_maps),
            "hnfs": [list(hnf) for hnf in hnfs],
            "pair_orbits": [
                {"index": orbit_index, "members": [
                    {"hnf": list(hnf), "mapping_index": index}
                    for hnf, index in sorted(members)
                ]}
                for orbit_index, members in enumerate(pair_orbits)
            ],
            "representative_results": results,
            "by_hnf": by_hnf,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
