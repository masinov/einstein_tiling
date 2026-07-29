#!/usr/bin/env python
"""Verify clause-level SAT witnesses for index-50 overlap at most two."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.constraints import _cnf_sha256
from einstein.holonomy.overlaps import build_bounded_overlap_holonomy_cnf
from verify_theory_w2_layer_d_index50_sat import verify_clause_model


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "docs/notebook/assets/theory-w2-layer-d-overlap2-sat-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    payload = json.loads(WITNESSES.read_text())
    dependencies = payload["provenance"]["dependencies"]
    for dependency in dependencies:
        path = ROOT / dependency["path"]
        if sha256(path.read_bytes()).hexdigest() != dependency["sha256"]:
            raise AssertionError(f"dependency hash mismatch: {path}")
    base = json.loads((ROOT / dependencies[1]["path"]).read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in base["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    for completed, row in enumerate(payload["witnesses"], 1):
        cnf, metadata = build_bounded_overlap_holonomy_cnf(
            shape, tuple(row["hnf"]), mappings[row["mapping_index"]],
            tuple(tuple(value) for value in row["twists"]), maximum_coverage=2,
        )
        if metadata != row["canonical_metadata"] or _cnf_sha256(cnf) != row["cnf_sha256"]:
            raise AssertionError(f"canonical CNF mismatch: {row['pair_orbit']}")
        if not verify_clause_model(cnf, row["model_true_variables"]):
            raise AssertionError(f"invalid witness: {row['pair_orbit']}")
        if completed % 10 == 0 or completed == len(payload["witnesses"]):
            print(f"[{completed:2d}/{len(payload['witnesses'])}] VERIFIED", flush=True)
    print(f"Overlap-2 SAT witnesses VERIFIED: {len(payload['witnesses'])}")


if __name__ == "__main__":
    main()
