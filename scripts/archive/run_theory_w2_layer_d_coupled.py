#!/usr/bin/env python
"""Run W2.D's binary-coupled S3 torus-holonomy experiment.

The default horizon is the first five area-admissible indices beyond W1's
complete quotient prefix.  Earlier exact certificate classes are applied
first; only their survivors enter the more expensive coupled CSP.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.funnel.a1_torus import sublattices
from einstein.theory.binary_families import (
    quotient_period_obstruction,
    verify_quotient_period_obstruction,
)
from einstein.theory.holonomy import (
    s3_boundary_quotients,
    verify_s3_boundary_quotient,
)
from einstein.theory.holonomy_csp import (
    scan_boundary_holonomy,
    solve_cover_control,
)
from einstein.theory.invariants import (
    gf2_cokernel_obstruction,
    verify_gf2_cokernel_obstruction,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-coupled.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"
W1_FILES = (
    ROOT / "docs/notebook/assets/theory-w1-finalist-norm25.json",
    ROOT / "docs/notebook/assets/theory-w1-finalist-norm26-36.json",
)


def _sha(path):
    return sha256(path.read_bytes()).hexdigest()


def _load_period_vectors():
    vectors = set()
    dependencies = []
    for path in W1_FILES:
        payload = json.loads(path.read_text())
        if not payload["summary"]["complete_requested_range"]:
            raise AssertionError(f"incomplete W1 dependency: {path}")
        if payload["summary"]["resource_exhaustions"]:
            raise AssertionError(f"exhausted W1 dependency: {path}")
        for orbit in payload["orbits"]:
            if orbit["verdict"] != "cycle-free" or not orbit["independently_verified"]:
                raise AssertionError(f"unverified W1 orbit in {path}")
            vectors.update(tuple(vector) for vector in orbit["orbit"])
        dependencies.append({
            "path": str(path.relative_to(ROOT)),
            "sha256": _sha(path),
        })
    if len(vectors) != 126:
        raise AssertionError("expected the 126-vector W1 norm ball")
    return tuple(sorted(vectors)), dependencies


def _scan_one(arguments):
    shape, hnf, images = arguments
    started = perf_counter()
    base = solve_cover_control(shape, hnf, cover_mode="at-least")
    if not base["sat"]:
        raise AssertionError(f"placement-only relaxation unexpectedly UNSAT: {hnf}")
    coupled = scan_boundary_holonomy(
        shape,
        hnf,
        images,
        cover_mode="at-least",
        stop_on_sat=True,
    )
    return {
        "hnf": list(hnf),
        "base": base,
        "coupled": coupled,
        "wall_seconds": perf_counter() - started,
    }


def _periodic_controls():
    controls = []
    single = ((0, 0, 0),)
    single_images = s3_boundary_quotients(single, keep=0)[
        "sample_surjections_by_displacement_kernel"
    ]["3"]
    for hnf in ((1, 0, 1), (2, 0, 1), (2, 1, 1)):
        controls.append({
            "name": "single-kite",
            "hnf": list(hnf),
            "result": scan_boundary_holonomy(
                single, hnf, single_images, cover_mode="exact", stop_on_sat=True
            ),
        })

    shape392 = (
        (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3),
        (0, 0, 4), (0, 0, 5), (2, -4, 0), (2, -4, 1),
    )
    images392 = s3_boundary_quotients(shape392, keep=0)[
        "sample_surjections_by_displacement_kernel"
    ]["3"]
    controls.append({
        "name": "stored-periodic-shape-392",
        "hnf": [2, 0, 2],
        "known_tiles_per_domain": 3,
        "result": scan_boundary_holonomy(
            shape392,
            (2, 0, 2),
            images392,
            cover_mode="exact",
            stop_on_sat=True,
        ),
    })
    if any(row["result"]["verdict"] != "not-obstructed" for row in controls):
        raise AssertionError("coupled CSP falsely excluded a periodic control")
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--max-index", type=int, default=60)
    args = parser.parse_args()
    if args.max_index < 40 or args.max_index % 5:
        raise SystemExit("--max-index must be a multiple of five and at least 40")

    shape = decode_compiled_key(KEY)
    quotient_data = s3_boundary_quotients(shape, keep=0)
    images = quotient_data["sample_surjections_by_displacement_kernel"]["3"]
    if not verify_s3_boundary_quotient(shape, images, require_surjective=True):
        raise AssertionError("selected S3 boundary quotient failed verification")
    vectors, w1_dependencies = _load_period_vectors()

    rows = []
    frontier = []
    for index in range(40, args.max_index + 1, 5):
        for hnf in sublattices(index):
            period = quotient_period_obstruction(hnf, vectors)
            if period:
                if not verify_quotient_period_obstruction(period):
                    raise AssertionError(f"invalid period-family certificate: {hnf}")
                rows.append({
                    "index": index,
                    "hnf": list(hnf),
                    "cascade_verdict": "killed-period-family",
                    "period_certificate": period,
                })
                continue
            gf2 = gf2_cokernel_obstruction(shape, hnf)
            if gf2:
                if not verify_gf2_cokernel_obstruction(shape, gf2):
                    raise AssertionError(f"invalid GF(2) certificate: {hnf}")
                rows.append({
                    "index": index,
                    "hnf": list(hnf),
                    "cascade_verdict": "killed-mod2",
                    "gf2_certificate": gf2,
                })
                continue
            frontier.append(tuple(hnf))

    print(f"coupled frontier: {len(frontier)} HNFs; jobs={args.jobs}", flush=True)
    coupled = {}
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(_scan_one, (shape, hnf, images)): hnf
            for hnf in frontier
        }
        for completed, future in enumerate(as_completed(futures), 1):
            hnf = futures[future]
            result = future.result()
            coupled[hnf] = result
            print(
                f"[{completed:3d}/{len(frontier)}] {hnf}: "
                f"{result['coupled']['verdict']} "
                f"({result['coupled']['twist_pairs_checked']} twists, "
                f"{result['wall_seconds']:.2f}s)",
                flush=True,
            )

    for hnf in frontier:
        result = coupled[hnf]
        verdict = result["coupled"]["verdict"]
        rows.append({
            "index": hnf[0] * hnf[2],
            "hnf": list(hnf),
            "cascade_verdict": (
                "killed-holonomy" if verdict == "holonomy-obstructed"
                else "survives-tested-stack"
            ),
            "period_certificate": None,
            "gf2_certificate": None,
            "layer_d": result,
        })
    rows.sort(key=lambda row: (row["index"], row["hnf"]))

    by_index = {}
    for row in rows:
        summary = by_index.setdefault(str(row["index"]), {
            "hnfs": 0,
            "killed_period_family": 0,
            "killed_mod2": 0,
            "tested_layer_d": 0,
            "killed_holonomy": 0,
            "survives_tested_stack": 0,
        })
        summary["hnfs"] += 1
        verdict = row["cascade_verdict"].replace("-", "_")
        if verdict in summary:
            summary[verdict] += 1
        if row["cascade_verdict"] in {"killed-holonomy", "survives-tested-stack"}:
            summary["tested_layer_d"] += 1

    source_paths = (
        ROOT / "src/einstein/theory/holonomy.py",
        ROOT / "src/einstein/theory/holonomy_csp.py",
        Path(__file__),
    )
    dependencies = (
        ROOT / "docs/notebook/assets/theory-w2-layer-d-phase0.json",
        ROOT / "docs/notebook/assets/theory-w2-binary-families.json",
        ROOT / "docs/notebook/assets/theory-w2-layer-c-gf2.json",
    )
    payload = {
        "kind": "theory-w2-layer-d-binary-coupled-s3",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "geometric_scope": "grid-aligned finalist torus quotients",
            "horizon": [40, args.max_index, 5],
            "cover_relaxation": (
                "every quotient cell has at least one selected placement; "
                "overlap is allowed, so every exact cover remains feasible"
            ),
            "positive_polarity": (
                "all 18 commuting S3 twist pairs UNSAT proves that the HNF "
                "admits no exact cover for the selected verified boundary quotient"
            ),
            "negative_polarity": (
                "one satisfying relaxed twisted model is only failure of this "
                "certificate class, not a tiling"
            ),
            "proof_status": (
                "CaDiCaL UNSAT results and canonical CNF hashes are retained; "
                "independently checked DRAT traces are a separate next gate"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _sha(path)}
                for path in source_paths
            ],
            "dependencies": [
                {"path": str(path.relative_to(ROOT)), "sha256": _sha(path)}
                for path in dependencies
            ] + w1_dependencies,
        },
        "selected_boundary_quotient": {
            "target": "S3",
            "selection_rule": (
                "phase-0 deterministic sample among surjections whose "
                "zero-displacement kernel has order 3"
            ),
            "generator_images": images,
            "verified_surjective": True,
            "tile_relators": quotient_data["relators"],
        },
        "validation": {
            "periodic_controls": _periodic_controls(),
            "false_exclusions": 0,
        },
        "finalist": {
            "shape": KEY,
            "by_index": by_index,
            "results": rows,
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(by_index, indent=1))


if __name__ == "__main__":
    main()
