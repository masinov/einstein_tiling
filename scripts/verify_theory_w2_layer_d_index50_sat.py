#!/usr/bin/env python
"""Verify explicit SAT witnesses for the non-obstructed index-50 pair orbits."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy_csp import build_boundary_holonomy_cnf, _cnf_sha256


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "docs/notebook/assets/theory-w2-layer-d-sat-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def verify_clause_model(cnf, true_variables):
    true_variables = frozenset(true_variables)
    if any(variable <= 0 or variable > cnf.nv for variable in true_variables):
        return False
    return all(any(
        literal in true_variables if literal > 0 else -literal not in true_variables
        for literal in clause
    ) for clause in cnf.clauses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witnesses", default=str(WITNESSES))
    args = parser.parse_args()
    path = Path(args.witnesses).resolve()
    payload = json.loads(path.read_text())
    matrix_path = ROOT / payload["provenance"]["matrix"]["path"]
    if sha256(matrix_path.read_bytes()).hexdigest() != payload["provenance"]["matrix"]["sha256"]:
        raise AssertionError("index-50 matrix dependency hash mismatch")
    matrix = json.loads(matrix_path.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in matrix["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    for completed, row in enumerate(payload["witnesses"], 1):
        hnf = tuple(row["hnf"])
        twists = tuple(tuple(value) for value in row["twists"])
        cnf, metadata = build_boundary_holonomy_cnf(
            shape, hnf, mappings[row["mapping_index"]], twists,
            cover_mode="at-least",
        )
        if metadata != row["canonical_metadata"]:
            raise AssertionError(f"metadata mismatch for pair orbit {row['pair_orbit']}")
        if _cnf_sha256(cnf) != row["cnf_sha256"]:
            raise AssertionError(f"CNF hash mismatch for pair orbit {row['pair_orbit']}")
        if not verify_clause_model(cnf, row["model_true_variables"]):
            raise AssertionError(f"invalid SAT witness for pair orbit {row['pair_orbit']}")
        print(
            f"[{completed:2d}/{len(payload['witnesses'])}] pair orbit "
            f"{row['pair_orbit']:02d} SAT witness VERIFIED",
            flush=True,
        )
    print(f"Layer-D SAT witnesses VERIFIED: {len(payload['witnesses'])}")


if __name__ == "__main__":
    main()
