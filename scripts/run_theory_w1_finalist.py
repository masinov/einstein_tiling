#!/usr/bin/env python
"""Certify bounded-norm W1 period exclusions for the n=10 finalist.

The default run covers every D6 orbit of nonzero center-lattice vectors with
Q(x,y)=x^2+xy+y^2 <= 25, including nonprimitive vectors.  Every negative
result includes the complete graph and is checked by the independent verifier.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.db import code_version, serialize_cells
from einstein.e1_candidates import decode_compiled_key
from einstein.funnel.a1_torus import verify_certificate
from einstein.theory.transfer import (
    CylinderTransfer,
    decide_period_vector,
    vector_norm2,
    vector_orbit,
    vector_orbit_representatives,
)
from einstein.theory.transfer_verify import verify_cycle_free_manifest


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-norm2", type=int, default=25)
    parser.add_argument(
        "--min-norm2",
        type=int,
        default=0,
        help="exclude vectors at or below this already-certified norm",
    )
    args = parser.parse_args()
    if args.min_norm2 < 0 or args.min_norm2 >= args.max_norm2:
        parser.error("require 0 <= min-norm2 < max-norm2")
    shape = decode_compiled_key(KEY)
    rows = []
    complete = True
    periodic = None
    for representative in vector_orbit_representatives(args.max_norm2):
        if vector_norm2(representative) <= args.min_norm2:
            continue
        started = perf_counter()
        result = decide_period_vector(shape, representative)
        row = {
            "representative": list(representative),
            "orbit": [list(vector) for vector in vector_orbit(representative)],
            "norm2": vector_norm2(representative),
            "verdict": result.verdict,
            "profile": result.summary(),
        }
        if result.verdict == "cycle":
            if not verify_certificate(shape, result.certificate):
                raise AssertionError("finalist transfer cycle failed A1 verification")
            row["a1_certificate"] = result.certificate
            periodic = row
            complete = False
        elif result.verdict == "cycle-free":
            manifest = CylinderTransfer(shape, representative).cycle_free_manifest()
            if not verify_cycle_free_manifest(manifest):
                raise AssertionError(
                    f"independent verifier rejected finalist vector {representative}"
                )
            row["certificate"] = manifest
            row["independently_verified"] = True
        else:
            complete = False
        elapsed = perf_counter() - started
        rows.append(row)
        print(
            representative,
            f"Q={row['norm2']}",
            row["verdict"],
            f"states={result.state_count}",
            f"edges={result.edge_count}",
            f"time={elapsed:.3f}s",
            flush=True,
        )
        if periodic is not None:
            break

    producer = ROOT / "src" / "einstein" / "theory" / "transfer.py"
    verifier = ROOT / "src" / "einstein" / "theory" / "transfer_verify.py"
    payload = {
        "kind": "theory-w1-finalist-bounded-norm",
        "schema_version": 1,
        "date": "2026-07-17",
        "candidate": {"n": 10, "index": 2, "shape": KEY},
        "scope": {
            "coordinate_norm": "Q(x,y)=x^2+x*y+y^2 (physical norm squared / 12)",
            "max_norm2": args.max_norm2,
            "min_norm2_exclusive": args.min_norm2,
            "all_nonzero_vectors": True,
            "includes_nonprimitive_vectors": True,
            "orbit_reduction": "exact D6 action; full orbit listed per certificate",
            "geometric_scope": "grid-aligned tilings only",
        },
        "provenance": {
            "code_version": code_version(),
            "shape_key": serialize_cells(shape),
            "producer": str(producer.relative_to(ROOT)),
            "producer_sha256": sha256(producer.read_bytes()).hexdigest(),
            "verifier": str(verifier.relative_to(ROOT)),
            "verifier_sha256": sha256(verifier.read_bytes()).hexdigest(),
        },
        "orbits": rows,
        "summary": {
            "orbit_representatives": len(rows),
            "vectors_covered": sum(len(row["orbit"]) for row in rows),
            "cycle_free_certificates": sum(
                row["verdict"] == "cycle-free" for row in rows
            ),
            "independently_verified": sum(
                row.get("independently_verified", False) for row in rows
            ),
            "periodic_certificate_found": periodic is not None,
            "resource_exhaustions": sum(
                row["verdict"] == "resource-exhausted" for row in rows
            ),
            "complete_requested_range": complete,
            "complete_through_bound": complete and args.min_norm2 == 0,
            "claim": (
                f"No grid-aligned finalist tiling has a nonzero translation "
                f"period v with {args.min_norm2}<Q(v)<={args.max_norm2}."
                if complete
                else "The requested bounded-norm classification did not complete."
            ),
        },
    }
    suffix = (
        f"norm{args.max_norm2}"
        if args.min_norm2 == 0
        else f"norm{args.min_norm2 + 1}-{args.max_norm2}"
    )
    out = ROOT / "docs" / "notebook" / "assets" / f"theory-w1-finalist-{suffix}.json"
    out.write_text(json.dumps(payload, indent=1) + "\n")
    print(out.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))
    return 0 if complete or periodic is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
