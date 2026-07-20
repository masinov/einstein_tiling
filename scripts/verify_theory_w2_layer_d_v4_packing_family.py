#!/usr/bin/env python
"""Cold-check SAT witnesses in the ``2 Lambda`` packing-family scan."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_packing_family import (
    area_admissible_2lambda_hnfs,
    build_signature_packing_cnf,
    coverage_summary,
)
from einstein.theory.holonomy_csp import _cnf_sha256


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-family-index120.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _verify_sat(arguments):
    shape, signature_rows, row = arguments
    hnf = tuple(row["hnf"])
    cnf, metadata = build_signature_packing_cnf(shape, hnf, signature_rows)
    truth = set(row["true_variables"])
    if (metadata != row["metadata"]
            or _cnf_sha256(cnf) != row["canonical_cnf_sha256"]
            or any(variable < 1 or variable > cnf.nv for variable in truth)
            or any(not any((literal > 0) == (abs(literal) in truth)
                           for literal in clause) for clause in cnf.clauses)
            or coverage_summary(shape, hnf, truth) != row["coverage"]):
        raise AssertionError(f"SAT witness replay failed: {hnf}")
    return hnf


def main():
    payload = json.loads(ARTIFACT.read_text())
    if payload["kind"] != "theory-w2-layer-d-v4-single-orbit-packing-family-falsification":
        raise AssertionError("unexpected packing-family artifact kind")
    for section in ("dependencies", "sources"):
        for source in payload["provenance"][section]:
            path = ROOT / source["path"]
            if sha256(path.read_bytes()).hexdigest() != source["sha256"]:
                raise AssertionError(f"provenance mismatch: {source['path']}")
    expected = set(area_admissible_2lambda_hnfs(payload["scope"]["maximum_index"]))
    actual = {tuple(row["hnf"]) for row in payload["results"]}
    if expected != actual or len(actual) != payload["scope"]["hnfs"]:
        raise AssertionError("packing-family HNF census mismatch")
    base_path = ROOT / payload["provenance"]["dependencies"][0]["path"]
    signature_rows = tuple(sorted(
        json.loads(base_path.read_text())["base_witnesses"],
        key=lambda row: row["mapping_index"],
    ))
    shape = decode_compiled_key(KEY)
    sat_rows = [row for row in payload["results"] if row["sat"]]
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(_verify_sat, (shape, signature_rows, row))
            for row in sat_rows
        ]
        for completed, future in enumerate(as_completed(futures), 1):
            future.result()
            if completed % 16 == 0 or completed == len(futures):
                print(f"[{completed:3d}/{len(futures)}] SAT witnesses VERIFIED", flush=True)
    print(
        f"packing-family scan census VERIFIED: {len(actual)} HNFs; "
        f"SAT witnesses replayed: {len(sat_rows)}"
    )


if __name__ == "__main__":
    main()
