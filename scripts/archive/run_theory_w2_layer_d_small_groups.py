#!/usr/bin/env python
"""Census the first genuinely new finite holonomy targets beyond S3."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.finite_groups import SMALL_NONABELIAN_TARGETS, symmetric_group
from einstein.theory.holonomy_quotients import boundary_quotient_census


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-small-groups.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    shape = decode_compiled_key(KEY)
    groups = (symmetric_group(3), *(factory() for factory in SMALL_NONABELIAN_TARGETS))
    results = []
    for group in groups:
        started = perf_counter()
        result = boundary_quotient_census(shape, group)
        result["wall_seconds"] = perf_counter() - started
        results.append(result)
        print(
            group.name,
            f"hom={result['homomorphisms']} surj={result['surjections']} "
            f"kernels={result['surjective_displacement_kernel_orders']} "
            f"classes={result['inner_conjugacy_classes_by_kernel']} "
            f"({result['wall_seconds']:.1f}s)",
            flush=True,
        )
    sources = (
        ROOT / "src/einstein/theory/finite_groups.py",
        ROOT / "src/einstein/theory/holonomy_quotients.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-small-finite-group-census",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "shape": KEY,
            "targets": [result["target"] for result in results],
            "selection_rule": (
                "choose a target with surjective boundary maps and a proper "
                "nontrivial zero-displacement kernel not explained by S3"
            ),
        },
        "provenance": {
            "sources": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in sources
            ],
        },
        "results": results,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
