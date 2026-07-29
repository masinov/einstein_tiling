#!/usr/bin/env python
"""Cold-replay the stored A4 index-50 Layer-D certificates."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
from hashlib import sha256
import json
from pathlib import Path

from einstein.repository import repository_root
import subprocess
import tempfile

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.combinatorics.finite_groups import alternating_group
from einstein.holonomy.finite_constraints import (
    build_finite_boundary_holonomy_cnf,
    commuting_pairs,
)
from einstein.solvers.cnf_certificates import (
    clause_hash as _clause_hash,
    parse_dimacs_clauses as _dimacs_clauses,
)


ROOT = repository_root(Path(__file__))
MANIFEST = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _verify_one(arguments):
    row, images, checker = arguments
    group = alternating_group(4)
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
    with tempfile.TemporaryDirectory(prefix="verify-a4-layer-d-", dir="/tmp") as name:
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
    args = parser.parse_args()
    payload = json.loads(MANIFEST.read_text())
    if payload["kind"] != "theory-w2-layer-d-a4-index50-independent-drat-certificates":
        raise AssertionError("unexpected certificate-manifest kind")
    for source in payload["provenance"]["sources"]:
        source_path = ROOT / source["path"]
        if sha256(source_path.read_bytes()).hexdigest() != source["sha256"]:
            raise AssertionError(f"source hash mismatch: {source['path']}")
    search_path = ROOT / payload["provenance"]["search"]["path"]
    search_bytes = search_path.read_bytes()
    if sha256(search_bytes).hexdigest() != payload["provenance"]["search"]["sha256"]:
        raise AssertionError("search artifact hash mismatch")
    search = json.loads(search_bytes)
    mappings = tuple(tuple(images) for images in search["finalist"]["mapping_representatives"])
    shape = decode_compiled_key(KEY)
    group = alternating_group(4)
    twists = commuting_pairs(group)
    expected_hnfs = {tuple(hnf) for hnf in payload["scope"]["hnfs"]}
    expected_cases = {
        (hnf, twist_index) for hnf in expected_hnfs
        for twist_index in range(len(twists))
    }
    actual_cases = {
        (tuple(row["hnf"]), row["twist_index"])
        for row in payload["results"]
    }
    if actual_cases != expected_cases or len(payload["results"]) != len(expected_cases):
        raise AssertionError("certificate manifest is not the complete HNF/twist product")
    checker = "/tmp/drat-trim/drat-trim"
    tasks = []
    for row in payload["results"]:
        if row["mapping_index"] != 7:
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
    print(f"A4 Layer-D certificates VERIFIED: {len(payload['results'])}")


if __name__ == "__main__":
    main()
