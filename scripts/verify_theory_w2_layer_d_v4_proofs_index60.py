#!/usr/bin/env python
"""Cold-replay the 42 map-7 V4 twist-union index-60 certificates."""

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
from einstein.theory.a4_v4_twist_union import (
    build_map7_v4_coverability_union_cnf,
)
from run_theory_w2_layer_d_proofs import _clause_hash
from verify_theory_w2_layer_d_proofs import _dimacs_clauses


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-map7.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _verify_one(arguments):
    row, checker = arguments
    shape = decode_compiled_key(KEY)
    cnf, metadata = build_map7_v4_coverability_union_cnf(shape, tuple(row["hnf"]))
    if (metadata != row["canonical_metadata"]
            or _clause_hash(cnf) != row["canonical_cnf_clause_hash"]):
        raise AssertionError(f"canonical twist-union mismatch: {row['hnf']}")
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
    with tempfile.TemporaryDirectory(prefix="verify-index60-map7-", dir="/tmp") as name:
        cnf_path, proof_path = Path(name) / "core.cnf", Path(name) / "core.drat"
        cnf_path.write_bytes(core_cnf)
        proof_path.write_bytes(core_proof)
        checked = subprocess.run(
            [checker, cnf_path, proof_path], check=True,
            text=True, capture_output=True,
        )
    if "s VERIFIED" not in checked.stdout:
        raise AssertionError("DRAT replay failed")
    return tuple(row["hnf"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    payload = json.loads(MANIFEST.read_text())
    if payload["kind"] != "theory-w2-layer-d-index60-map7-v4-twist-union-certificates":
        raise AssertionError("unexpected index-60 map-7 manifest kind")
    for section in ("sources", "dependencies"):
        for source in payload["provenance"][section]:
            path = ROOT / source["path"]
            if sha256(path.read_bytes()).hexdigest() != source["sha256"]:
                raise AssertionError(f"provenance mismatch: {source['path']}")
    expected = {tuple(hnf) for hnf in payload["scope"]["hnfs"]}
    actual = {tuple(row["hnf"]) for row in payload["results"]}
    if len(expected) != 42 or actual != expected or len(payload["results"]) != 42:
        raise AssertionError("manifest does not contain exactly 42 unique HNFs")
    tasks = [(row, checker) for row in payload["results"]]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_verify_one, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            future.result()
            if completed % 6 == 0 or completed == len(tasks):
                print(f"[{completed:2d}/{len(tasks)}] VERIFIED", flush=True)
    print(f"index-60 map-7 twist-union certificates VERIFIED: {len(tasks)}")


if __name__ == "__main__":
    main()
