#!/usr/bin/env python
"""Falsify the candidate ``selected <= k/2`` packing-density theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.density import build_signature_density_bound_cnf
from einstein.holonomy.alternating4.packing_families import area_admissible_2lambda_hnfs
from einstein.holonomy.constraints import _cnf_sha256


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"
SIGNATURES = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-index", type=int, default=120)
    parser.add_argument("--mapping-index", type=int, default=7)
    parser.add_argument(
        "--output",
        default="docs/notebook/assets/theory-w2-layer-d-v4-density-index120.json",
    )
    args = parser.parse_args()

    shape = decode_compiled_key(KEY)
    signatures = json.loads(SIGNATURES.read_text())
    try:
        row = next(
            row for row in signatures["base_witnesses"]
            if row["mapping_index"] == args.mapping_index
        )
    except StopIteration:
        raise SystemExit(f"mapping index {args.mapping_index} is not a signature row")

    results = []
    started = time.monotonic()
    for hnf in area_admissible_2lambda_hnfs(args.maximum_index):
        cnf, metadata = build_signature_density_bound_cnf(shape, hnf, row)
        then = time.monotonic()
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
            model = solver.get_model() if sat else None
        selected = None
        if model is not None:
            selected = sum(
                model[variable - 1] > 0
                for variable in range(1, metadata["placements"] + 1)
            )
        result = {
            "hnf": list(hnf),
            "index": hnf[0] * hnf[2],
            "sat_above_bound": sat,
            "selected_placements": selected,
            "cnf_sha256": _cnf_sha256(cnf),
            "seconds": time.monotonic() - then,
            "conflicts": stats.get("conflicts"),
            "metadata": metadata,
        }
        results.append(result)
        print(
            f"hnf={hnf!s:16s} "
            f"{'COUNTERMODEL' if sat else 'bounded'} "
            f"selected={selected} conflicts={result['conflicts']} "
            f"seconds={result['seconds']:.3f}",
            flush=True,
        )

    countermodels = sum(row["sat_above_bound"] for row in results)
    payload = {
        "experiment": "T2.D7 single-signature packing-density falsification",
        "claim_under_test": (
            "For every area-admissible HNF L <= 2 Lambda, V4 signature "
            "compatibility plus the six-kite collision orbit implies "
            "selected placements <= [Lambda:L]/2."
        ),
        "scope": {
            "maximum_index": args.maximum_index,
            "mapping_index": args.mapping_index,
            "hnfs": len(results),
            "indices": dict(sorted(Counter(row["index"] for row in results).items())),
        },
        "summary": {
            "bounded": len(results) - countermodels,
            "countermodels": countermodels,
            "candidate_survives_finite_gate": countermodels == 0,
            "proof_status": "UNSAT search only; no infinite theorem claimed",
        },
        "provenance": {
            "candidate_key": KEY,
            "signature_source": str(SIGNATURES.relative_to(ROOT)),
            "signature_source_sha256": digest(SIGNATURES),
            "implementation": "src/einstein/holonomy/alternating4/density.py",
            "implementation_sha256": digest(
                ROOT / "src/einstein/holonomy/alternating4/density.py"
            ),
        },
        "elapsed_seconds": time.monotonic() - started,
        "results": results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=1) + "\n")
    print(
        f"summary: {len(results) - countermodels}/{len(results)} bounded; "
        f"{countermodels} countermodels; wrote {output}",
        flush=True,
    )
    return 1 if countermodels else 0


if __name__ == "__main__":
    raise SystemExit(main())
