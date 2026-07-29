#!/usr/bin/env python
"""Run W2.C's full-quotient GF(2) incidence-cokernel experiment.

This is an exact modular slice of the integer/SNF layer, not a full Smith
normal form implementation. Positive witnesses prove quotient UNSAT; a missing
witness has no SAT polarity.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.funnel.a1_torus import sublattices
from einstein.theory.invariants import (
    area_allows_index,
    gf2_cokernel_obstruction,
    verify_gf2_cokernel_obstruction,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "notebook" / "assets" / "theory-w2-layer-c-gf2.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    paths = sorted((ROOT / "data" / "a1-compiled").glob("periodic-*.jsonl"))
    if not paths:
        raise RuntimeError("compiled periodic corpus is not materialized")
    corpus = []
    checked = false_exclusions = 0
    for path in paths:
        rows = 0
        for line in path.read_text().splitlines():
            if not line:
                continue
            row = json.loads(line)
            shape = decode_compiled_key(row["shape"])
            obstruction = gf2_cokernel_obstruction(shape, row["hnf"])
            false_exclusions += obstruction is not None
            checked += 1
            rows += 1
        corpus.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "certificates": rows,
            }
        )
    if false_exclusions:
        raise AssertionError("GF(2) cokernel falsely excluded a periodic certificate")

    shape = decode_compiled_key(KEY)
    results = []
    for index in range(1, 61):
        if not area_allows_index(len(shape), index):
            continue
        for hnf in sublattices(index):
            certificate = gf2_cokernel_obstruction(shape, hnf)
            if certificate and not verify_gf2_cokernel_obstruction(shape, certificate):
                raise AssertionError(f"GF(2) witness failed verification for {hnf}")
            results.append(
                {
                    "index": index,
                    "hnf": list(hnf),
                    "verdict": "killed-mod2" if certificate else "not-killed-mod2",
                    "certificate": certificate,
                }
            )
    killed = [row for row in results if row["certificate"]]
    by_index = {}
    for row in results:
        summary = by_index.setdefault(
            str(row["index"]), {"hnfs": 0, "killed_mod2": 0}
        )
        summary["hnfs"] += 1
        summary["killed_mod2"] += row["certificate"] is not None

    source = ROOT / "src" / "einstein" / "theory" / "invariants.py"
    payload = {
        "kind": "theory-w2-layer-c-gf2",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "modulus": 2,
            "integer_snf_complete": False,
            "positive_polarity": (
                "a verified witness proves the quotient has no integer or "
                "0/1 exact-cover solution"
            ),
            "negative_polarity": (
                "not-killed-mod2 is unknown, not evidence of a tiling"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "periodic_corpus": corpus,
        },
        "validation": {
            "verified_periodic_certificates": checked,
            "false_exclusions": false_exclusions,
        },
        "finalist": {
            "shape": KEY,
            "area_admissible_indices": [5, 60, 5],
            "quotients_tested": len(results),
            "quotients_killed_mod2": len(killed),
            "by_index": by_index,
            "results": results,
            "conclusion": (
                "GF(2) gives exact quotient-specific kills beyond area, but "
                "does not decide the surviving HNFs and is not full SNF."
            ),
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "validation": payload["validation"],
        "finalist": {
            "quotients_tested": len(results),
            "quotients_killed_mod2": len(killed),
            "by_index": by_index,
        },
    }, indent=1))


if __name__ == "__main__":
    main()
