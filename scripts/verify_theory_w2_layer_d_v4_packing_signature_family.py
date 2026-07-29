#!/usr/bin/env python
"""Cold-check SAT witnesses in the single-signature packing-family scan."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import (
    PACKING_COLLISION_SEED,
    area_admissible_2lambda_hnfs,
    coverage_summary,
)
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf
from einstein.holonomy.constraints import _cnf_sha256, quotient_boundary_data


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-signature-index120.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _verify_sat(arguments):
    shape, signature, row = arguments
    hnf = tuple(row["hnf"])
    twists = induced_v4_twists(tuple(signature["base_twists"]), hnf)
    cnf, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(signature["images"]), twists
    )
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    clauses = collision_orbit_clauses(shape, hnf, instance, target)
    cnf.extend(clauses)
    truth = set(row["true_variables"])
    if (metadata != row["metadata"]
            or list(twists) != row["twists"]
            or len(clauses) != row["packing_clauses"]
            or _cnf_sha256(cnf) != row["canonical_cnf_sha256"]
            or any(not any((literal > 0) == (abs(literal) in truth)
                           for literal in clause) for clause in cnf.clauses)
            or coverage_summary(shape, hnf, truth) != row["coverage"]):
        raise AssertionError(f"single-signature SAT replay failed: {hnf}")
    return row["mapping_index"], hnf


def main():
    payload = json.loads(ARTIFACT.read_text())
    if payload["kind"] != "theory-w2-layer-d-v4-single-signature-packing-family-scan":
        raise AssertionError("unexpected signature-family artifact kind")
    for section in ("dependencies", "sources"):
        for source in payload["provenance"][section]:
            path = ROOT / source["path"]
            if sha256(path.read_bytes()).hexdigest() != source["sha256"]:
                raise AssertionError(f"provenance mismatch: {source['path']}")
    expected_hnfs = set(area_admissible_2lambda_hnfs(payload["scope"]["maximum_index"]))
    expected_maps = {row["mapping_index"] for row in payload["by_mapping"]}
    actual = {(row["mapping_index"], tuple(row["hnf"])) for row in payload["checks"]}
    if actual != {(mapping, hnf) for mapping in expected_maps for hnf in expected_hnfs}:
        raise AssertionError("single-signature scan matrix is incomplete")
    base_path = ROOT / payload["provenance"]["dependencies"][0]["path"]
    signatures = {
        row["mapping_index"]: row
        for row in json.loads(base_path.read_text())["base_witnesses"]
    }
    shape = decode_compiled_key(KEY)
    sat_rows = [row for row in payload["checks"] if row["sat"]]
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(_verify_sat, (shape, signatures[row["mapping_index"]], row))
            for row in sat_rows
        ]
        for completed, future in enumerate(as_completed(futures), 1):
            future.result()
            if completed % 32 == 0 or completed == len(futures):
                print(f"[{completed:4d}/{len(futures)}] SAT witnesses VERIFIED", flush=True)
    print(
        f"single-signature packing matrix VERIFIED: {len(actual)} cases; "
        f"SAT witnesses replayed: {len(sat_rows)}"
    )


if __name__ == "__main__":
    main()
