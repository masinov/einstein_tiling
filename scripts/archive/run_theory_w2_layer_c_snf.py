#!/usr/bin/env python
"""Run W2.C's exact integer incidence-lattice normal-form census.

The 60,477 positive controls are all rechecked as explicit exact covers.  A
deterministic cross-section is additionally sent through the Smith code; doing
60,477 redundant Smith decompositions is intentionally not the default because
the explicit 0/1 solutions are stronger compatibility witnesses.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import json
from pathlib import Path

import flint
import sympy

from einstein.polykites.database import code_version
from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.periodic_quotients import sublattices, verify_certificate
from einstein.periodicity.invariants import (
    area_allows_index,
    integer_cokernel_hnf,
    integer_cokernel_snf,
    verify_gf2_cokernel_obstruction,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "notebook" / "assets" / "theory-w2-layer-c-snf.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def periodic_controls(sample_count):
    paths = sorted((ROOT / "data" / "a1-compiled").glob("periodic-*.jsonl"))
    if not paths:
        raise RuntimeError("compiled periodic corpus is not materialized")
    controls = []
    provenance = []
    checked = 0
    for path in paths:
        count = 0
        for line in path.read_text().splitlines():
            if not line:
                continue
            row = json.loads(line)
            shape = decode_compiled_key(row["shape"])
            certificate = {"hnf": row["hnf"], "placements": row["placements"]}
            if not verify_certificate(shape, certificate):
                raise AssertionError(f"invalid positive control in {path}")
            digest = sha256(line.encode()).hexdigest()
            controls.append((digest, shape, row["hnf"]))
            checked += 1
            count += 1
        provenance.append({
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "certificates": count,
        })
    spot = []
    for digest, shape, hnf in sorted(controls)[:sample_count]:
        result = integer_cokernel_snf(shape, hnf)
        if result["verdict"] != "integer-compatible":
            raise AssertionError(f"Smith false exclusion for periodic {hnf}")
        spot.append({"selector_sha256": digest, "hnf": hnf, "result": result})
    return {
        "explicit_solutions_verified": checked,
        "false_exclusions": 0,
        "smith_spot_checks": len(spot),
        "spot_results": spot,
        "corpus": provenance,
    }


def _smith_worker(task):
    shape, hnf = task
    return hnf, integer_cokernel_hnf(shape, hnf)


def finalist_census(max_index, jobs):
    shape = decode_compiled_key(KEY)
    rows = []
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        for index in range(1, max_index + 1):
            if not area_allows_index(len(shape), index):
                continue
            tasks = [(shape, hnf) for hnf in sublattices(index)]
            for hnf, result in pool.map(_smith_worker, tasks):
                witness = result.get("modular_witness")
                if witness is not None and not verify_gf2_cokernel_obstruction(
                    shape, witness
                ):
                    raise AssertionError(f"modular witness failed for {hnf}")
                rows.append({"index": index, "hnf": list(hnf), "result": result})
            counts = Counter(row["result"]["verdict"] for row in rows)
            print(index, len(rows), dict(counts), flush=True)
    by_index = {}
    for row in rows:
        summary = by_index.setdefault(str(row["index"]), Counter())
        summary["hnfs"] += 1
        summary[row["result"]["verdict"]] += 1
    verdicts = Counter(row["result"]["verdict"] for row in rows)
    modular = sum("modular_witness" in row["result"] for row in rows)
    return {
        "shape": KEY,
        "maximum_index": max_index,
        "area_admissible_step": 5,
        "quotients_tested": len(rows),
        "verdicts": dict(verdicts),
        "obstructions_with_independent_mod2_witness": modular,
        "by_index": {index: dict(counts) for index, counts in by_index.items()},
        "results": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-index", type=int, default=60)
    parser.add_argument("--periodic-snf-samples", type=int, default=16)
    parser.add_argument("--jobs", type=int, default=12)
    args = parser.parse_args()

    source = ROOT / "src" / "einstein" / "theory" / "invariants.py"
    payload = {
        "kind": "theory-w2-layer-c-integer-smith",
        "schema_version": 1,
        "date": "2026-07-17",
        "method": {
            "production_dependency": f"python-flint=={flint.__version__}",
            "reference_dependency": f"sympy=={sympy.__version__}",
            "criterion": (
                "compare canonical row-HNF bases of transpose(M) before and "
                "after adjoining 1; equality is equivalent to 1 belonging "
                "to the integer column lattice"
            ),
            "smith_crosscheck": (
                "FLINT and SymPy Smith rank/determinantal-divisor tests agree "
                "on pinned unit and finalist controls"
            ),
            "positive_polarity": "obstructed-rank/index proves quotient UNSAT",
            "negative_polarity": (
                "integer-compatible only proves an unrestricted integer solution; "
                "it does not prove a 0/1 cover"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
        },
        "validation": periodic_controls(args.periodic_snf_samples),
        "finalist": finalist_census(args.max_index, args.jobs),
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "validation": {
            key: value for key, value in payload["validation"].items()
            if key not in {"spot_results", "corpus"}
        },
        "finalist": {
            key: value for key, value in payload["finalist"].items()
            if key not in {"results", "by_index"}
        },
    }, indent=1))


if __name__ == "__main__":
    main()
