#!/usr/bin/env python
"""Cold-check A4 SAT witnesses for all non-obstructed index-50 pair orbits."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.combinatorics.finite_groups import alternating_group
from einstein.holonomy.constraints import _cnf_sha256
from einstein.holonomy.finite_constraints import build_finite_boundary_holonomy_cnf


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-sat-index50.json"
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
    payload = json.loads(WITNESSES.read_text())
    for source in payload["provenance"]["sources"]:
        source_path = ROOT / source["path"]
        if sha256(source_path.read_bytes()).hexdigest() != source["sha256"]:
            raise AssertionError(f"source hash mismatch: {source['path']}")
    matrix_path = ROOT / payload["provenance"]["matrix"]["path"]
    matrix_bytes = matrix_path.read_bytes()
    if sha256(matrix_bytes).hexdigest() != payload["provenance"]["matrix"]["sha256"]:
        raise AssertionError("A4 index-50 matrix dependency hash mismatch")
    matrix = json.loads(matrix_bytes)
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    expected_orbits = {
        row["pair_orbit"]
        for row in matrix["finalist"]["representative_results"]
        if row["sat_twist_index"] is not None
    }
    actual_orbits = {row["pair_orbit"] for row in payload["witnesses"]}
    if actual_orbits != expected_orbits or len(payload["witnesses"]) != len(expected_orbits):
        raise AssertionError("SAT witness artifact is not the complete survivor set")
    shape = decode_compiled_key(KEY)
    group = alternating_group(4)
    for completed, row in enumerate(payload["witnesses"], 1):
        cnf, metadata = build_finite_boundary_holonomy_cnf(
            shape, tuple(row["hnf"]), mappings[row["mapping_index"]],
            tuple(row["twists"]), group,
        )
        if metadata != row["canonical_metadata"]:
            raise AssertionError(f"metadata mismatch for pair orbit {row['pair_orbit']}")
        if _cnf_sha256(cnf) != row["cnf_sha256"]:
            raise AssertionError(f"CNF hash mismatch for pair orbit {row['pair_orbit']}")
        if not verify_clause_model(cnf, row["model_true_variables"]):
            raise AssertionError(f"invalid SAT witness for pair orbit {row['pair_orbit']}")
        if completed % 8 == 0 or completed == len(payload["witnesses"]):
            print(f"[{completed:2d}/{len(payload['witnesses'])}] VERIFIED", flush=True)
    print(f"A4 Layer-D SAT witnesses VERIFIED: {len(payload['witnesses'])}")


if __name__ == "__main__":
    main()
