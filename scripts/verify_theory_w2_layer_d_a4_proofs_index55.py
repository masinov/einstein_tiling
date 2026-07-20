#!/usr/bin/env python
"""Cold-replay the stored A4 index-55 Layer-D certificates."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_semidirect import canonical_a4_semidirect
from einstein.theory.finite_groups import alternating_group
from einstein.theory.holonomy_finite_csp import (
    build_finite_boundary_holonomy_cnf,
    commuting_pairs,
)
from run_theory_w2_layer_d_proofs import _clause_hash
from verify_theory_w2_layer_d_proofs import _dimacs_clauses


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index55.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _verify_one(arguments):
    row, images, checker = arguments
    group = alternating_group(4)
    shape = decode_compiled_key(KEY)
    cnf, metadata = build_finite_boundary_holonomy_cnf(
        shape, tuple(row["hnf"]), images, tuple(row["twists"]), group,
    )
    if (metadata != row["canonical_metadata"]
            or _clause_hash(cnf) != row["canonical_cnf_clause_hash"]):
        raise AssertionError(f"canonical CNF mismatch: {row['hnf']}")
    certificate = row["certificate"]
    cnf_gz = (ROOT / certificate["cnf_gz"]).read_bytes()
    proof_gz = (ROOT / certificate["drat_gz"]).read_bytes()
    if (sha256(cnf_gz).hexdigest() != certificate["cnf_gz_sha256"]
            or sha256(proof_gz).hexdigest() != certificate["drat_gz_sha256"]):
        raise AssertionError("compressed certificate hash mismatch")
    core_cnf, core_proof = gzip.decompress(cnf_gz), gzip.decompress(proof_gz)
    if sha256(core_cnf).hexdigest() != certificate["cnf_uncompressed_sha256"]:
        raise AssertionError("uncompressed core-CNF hash mismatch")
    if sha256(core_proof).hexdigest() != certificate["drat_uncompressed_sha256"]:
        raise AssertionError("uncompressed DRAT hash mismatch")
    generated = Counter(tuple(sorted(clause)) for clause in cnf.clauses)
    core = Counter(_dimacs_clauses(core_cnf))
    if any(count > generated[clause] for clause, count in core.items()):
        raise AssertionError("core is not a canonical-CNF subset")
    with tempfile.TemporaryDirectory(prefix="verify-a4-index55-", dir="/tmp") as name:
        cnf_path, proof_path = Path(name)/"core.cnf", Path(name)/"core.drat"
        cnf_path.write_bytes(core_cnf)
        proof_path.write_bytes(core_proof)
        checked = subprocess.run(
            [checker, cnf_path, proof_path], check=True,
            text=True, capture_output=True,
        )
    if "s VERIFIED" not in checked.stdout:
        raise AssertionError("DRAT replay failed")
    return tuple(row["hnf"]), row["twist_index"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")
    payload = json.loads(MANIFEST.read_text())
    if payload["kind"] != "theory-w2-layer-d-a4-index55-independent-drat-certificates":
        raise AssertionError("unexpected certificate-manifest kind")
    for dependency_kind in ("sources", "dependencies"):
        for source in payload["provenance"][dependency_kind]:
            source_path = ROOT / source["path"]
            if sha256(source_path.read_bytes()).hexdigest() != source["sha256"]:
                raise AssertionError(f"source hash mismatch: {source['path']}")
    matrix_path = ROOT / next(
        row["path"] for row in payload["provenance"]["dependencies"]
        if row["path"].endswith("a4-index50.json")
    )
    matrix = json.loads(matrix_path.read_text())
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    group = alternating_group(4)
    coordinates = canonical_a4_semidirect()
    twists = commuting_pairs(group)
    v4_indices = tuple(
        index for index, pair in enumerate(twists)
        if all(coordinates.coordinate(element).q == 0 for element in pair)
    )
    if list(v4_indices) != payload["scope"]["twist_indices"]:
        raise AssertionError("V4 twist reduction changed")
    expected_hnfs = {tuple(hnf) for hnf in payload["scope"]["hnfs"]}
    expected_cases = {
        (hnf, twist_index) for hnf in expected_hnfs for twist_index in v4_indices
    }
    actual_cases = {
        (tuple(row["hnf"]), row["twist_index"])
        for row in payload["results"]
    }
    if actual_cases != expected_cases or len(payload["results"]) != len(expected_cases):
        raise AssertionError("manifest is not the complete HNF/V4-twist product")
    tasks = []
    for row in payload["results"]:
        if row["mapping_index"] != payload["scope"]["selected_mapping_index"]:
            raise AssertionError("unexpected selected A4 map")
        if tuple(row["twists"]) != twists[row["twist_index"]]:
            raise AssertionError("twist index/value mismatch")
        tasks.append((row, mappings[row["mapping_index"]], checker))
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_verify_one, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            future.result()
            if completed % 24 == 0 or completed == len(tasks):
                print(f"[{completed:3d}/{len(tasks)}] VERIFIED", flush=True)
    print(f"A4 index-55 Layer-D certificates VERIFIED: {len(payload['results'])}")


if __name__ == "__main__":
    main()
