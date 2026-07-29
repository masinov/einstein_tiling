#!/usr/bin/env python
"""Independently replay the stored W2.D index-40 DRAT certificates."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path

from einstein.repository import repository_root
import subprocess
import tempfile

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.boundary import s3_boundary_surjections
from einstein.holonomy.constraints import build_boundary_holonomy_cnf
from einstein.solvers.cnf_certificates import clause_hash, parse_dimacs_clauses


ROOT = repository_root(Path(__file__))
MANIFEST = ROOT / "docs/notebook/assets/theory-w2-layer-d-proof-index40.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _sha_bytes(value):
    return sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    parser.add_argument("--manifest", default=str(MANIFEST))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")

    manifest = Path(args.manifest).resolve()
    payload = json.loads(manifest.read_text())
    results = payload["results"]
    if args.limit is not None:
        results = results[:args.limit]
    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(shape, displacement_kernel_order=3)
    for index, row in enumerate(results, 1):
        hnf = tuple(row["hnf"])
        images = mappings[row["mapping_index"]]
        twists = tuple(tuple(value) for value in row["twists"])
        canonical, metadata = build_boundary_holonomy_cnf(
            shape, hnf, images, twists, cover_mode="at-least"
        )
        if metadata != row["canonical_metadata"]:
            raise AssertionError(f"metadata mismatch: {hnf}, twist {row['twist_index']}")
        if clause_hash(canonical) != row["canonical_cnf_clause_hash"]:
            raise AssertionError(f"canonical clause hash mismatch: {hnf}")

        certificate = row["certificate"]
        cnf_path = ROOT / certificate["cnf_gz"]
        proof_path = ROOT / certificate["drat_gz"]
        cnf_gz = cnf_path.read_bytes()
        proof_gz = proof_path.read_bytes()
        if _sha_bytes(cnf_gz) != certificate["cnf_gz_sha256"]:
            raise AssertionError(f"compressed CNF hash mismatch: {cnf_path}")
        if _sha_bytes(proof_gz) != certificate["drat_gz_sha256"]:
            raise AssertionError(f"compressed proof hash mismatch: {proof_path}")
        core_cnf = gzip.decompress(cnf_gz)
        core_proof = gzip.decompress(proof_gz)
        if _sha_bytes(core_cnf) != certificate["cnf_uncompressed_sha256"]:
            raise AssertionError(f"core CNF hash mismatch: {cnf_path}")
        if _sha_bytes(core_proof) != certificate["drat_uncompressed_sha256"]:
            raise AssertionError(f"core proof hash mismatch: {proof_path}")

        generated = Counter(tuple(sorted(clause)) for clause in canonical.clauses)
        core = Counter(parse_dimacs_clauses(core_cnf))
        if any(count > generated[clause] for clause, count in core.items()):
            raise AssertionError(f"core is not a canonical-CNF subset: {hnf}")
        with tempfile.TemporaryDirectory(prefix="verify-layer-d-", dir="/tmp") as name:
            temp = Path(name)
            cnf_file, proof_file = temp / "core.cnf", temp / "core.drat"
            cnf_file.write_bytes(core_cnf)
            proof_file.write_bytes(core_proof)
            checked = subprocess.run(
                [checker, cnf_file, proof_file],
                check=True,
                text=True,
                capture_output=True,
            )
        if "s VERIFIED" not in checked.stdout:
            raise AssertionError(f"DRAT verification failed: {hnf}")
        print(
            f"[{index:2d}/{len(results)}] {hnf} twist={row['twist_index']:02d} VERIFIED",
            flush=True,
        )
    print(f"Layer-D certificates VERIFIED: {len(results)}")


if __name__ == "__main__":
    main()
