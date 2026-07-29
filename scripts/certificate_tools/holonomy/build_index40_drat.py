#!/usr/bin/env python
"""Produce independently checked DRAT cores for the three Layer-D index-40 kills."""

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
from time import perf_counter

from pysat.solvers import Solver

from einstein.polykites.database import code_version
from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.boundary import s3_boundary_surjections
from einstein.holonomy.constraints import (
    build_boundary_holonomy_cnf,
    commuting_s3_pairs,
)
from einstein.solvers.cnf_certificates import (
    clause_hash,
    gzip_deterministic,
    read_dimacs_clauses,
)


ROOT = repository_root(Path(__file__))
PHASE2 = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-classes.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-proof-index40.json"
CERT_DIR = ROOT / "docs/notebook/assets/theory-w2-layer-d-proof-index40"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _prove_one(arguments):
    shape, hnf, mapping_index, images, twist_index, twists, checker = arguments
    started = perf_counter()
    cnf, metadata = build_boundary_holonomy_cnf(
        shape, hnf, images, twists, cover_mode="at-least"
    )
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    generated_clauses = Counter(tuple(sorted(clause)) for clause in cnf.clauses)
    stem = f"hnf-{hnf[0]}-{hnf[1]}-{hnf[2]}-map-{mapping_index}-twist-{twist_index:02d}"
    with tempfile.TemporaryDirectory(prefix="layer-d-proof-", dir="/tmp") as temp_name:
        temp = Path(temp_name)
        original_cnf = temp / "original.cnf"
        raw_proof = temp / "raw.drat"
        core_cnf = temp / "core.cnf"
        core_proof = temp / "core.drat"
        cnf.to_file(original_cnf)
        with Solver(name="glucose4", bootstrap_with=cnf, with_proof=True) as solver:
            sat = solver.solve()
            stats = solver.accum_stats()
            proof = solver.get_proof()
        if sat or not proof or proof[-1] != "0":
            raise AssertionError(f"Glucose did not emit a complete UNSAT proof: {stem}")
        raw_proof.write_text("\n".join(proof) + "\n")

        trim = subprocess.run(
            [checker, original_cnf, raw_proof, "-c", core_cnf, "-l", core_proof],
            check=True,
            text=True,
            capture_output=True,
        )
        if "s VERIFIED" not in trim.stdout:
            raise AssertionError(f"raw proof did not verify: {stem}")
        check = subprocess.run(
            [checker, core_cnf, core_proof],
            check=True,
            text=True,
            capture_output=True,
        )
        if "s VERIFIED" not in check.stdout:
            raise AssertionError(f"trimmed core did not verify: {stem}")

        core_clauses = Counter(
            tuple(sorted(clause))
            for clause in read_dimacs_clauses(
                core_cnf, sort_literals=False
            )
        )
        if any(count > generated_clauses[clause] for clause, count in core_clauses.items()):
            raise AssertionError(f"core contains a non-generated clause: {stem}")
        cnf_target = CERT_DIR / f"{stem}.cnf.gz"
        proof_target = CERT_DIR / f"{stem}.drat.gz"
        gzip_deterministic(core_cnf, cnf_target)
        gzip_deterministic(core_proof, proof_target)
        return {
            "hnf": list(hnf),
            "mapping_index": mapping_index,
            "twist_index": twist_index,
            "twists": [list(twists[0]), list(twists[1])],
            "canonical_cnf_sha256": sha256(original_cnf.read_bytes()).hexdigest(),
            "canonical_cnf_clause_hash": clause_hash(cnf),
            "canonical_metadata": metadata,
            "core_clauses": sum(core_clauses.values()),
            "core_subset_verified": True,
            "glucose_stats": stats,
            "raw_proof_bytes": raw_proof.stat().st_size,
            "certificate": {
                "cnf_gz": str(cnf_target.relative_to(ROOT)),
                "cnf_gz_sha256": _digest(cnf_target),
                "cnf_uncompressed_sha256": _digest(core_cnf),
                "cnf_gz_bytes": cnf_target.stat().st_size,
                "drat_gz": str(proof_target.relative_to(ROOT)),
                "drat_gz_sha256": _digest(proof_target),
                "drat_uncompressed_sha256": _digest(core_proof),
                "drat_gz_bytes": proof_target.stat().st_size,
            },
            "independent_verification": {
                "raw_proof": "VERIFIED",
                "trimmed_core": "VERIFIED",
            },
            "wall_seconds": perf_counter() - started,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")

    phase2 = json.loads(PHASE2.read_text())
    selected = {
        tuple(row["hnf"]): min(row["killing_mapping_indices"])
        for row in phase2["finalist"]["by_hnf"]
    }
    expected = {(10, 3, 4), (40, 11, 1), (40, 28, 1)}
    if set(selected) != expected:
        raise AssertionError("phase-2 index-40 kill set changed")

    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(shape, displacement_kernel_order=3)
    twists = commuting_s3_pairs()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [
        (shape, hnf, mapping_index, mappings[mapping_index], twist_index, pair, checker)
        for hnf, mapping_index in sorted(selected.items())
        for twist_index, pair in enumerate(twists)
    ]
    print(f"proof tasks: {len(tasks)}; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(_prove_one, task): task[1:6] for task in tasks}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(
                f"[{completed:2d}/{len(tasks)}] {tuple(result['hnf'])} "
                f"twist={result['twist_index']:02d} VERIFIED "
                f"({result['wall_seconds']:.1f}s, "
                f"{result['certificate']['drat_gz_bytes'] / 1048576:.2f} MiB)",
                flush=True,
            )
    results.sort(key=lambda row: (row["hnf"], row["twist_index"]))

    checker_root = Path(checker).parent
    checker_commit = subprocess.run(
        ["git", "-C", checker_root, "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    sources = (
        ROOT / "src/einstein/holonomy/boundary.py",
        ROOT / "src/einstein/holonomy/constraints.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-index40-independent-drat-certificates",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "hnfs": [list(hnf) for hnf in sorted(selected)],
            "selected_mapping_rule": "lowest killing conjugacy-class index per HNF",
            "twists_per_hnf": len(twists),
            "certificate_logic": (
                "each stored core CNF is a multiplicity-respecting subset of "
                "the canonical generated CNF; drat-trim independently verifies "
                "the stored DRAT core; all 18 commuting twists are covered"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "phase2": {
                "path": str(PHASE2.relative_to(ROOT)),
                "sha256": _digest(PHASE2),
            },
            "producer": "Glucose 4 via python-sat",
            "checker": {
                "name": "drat-trim",
                "git_commit": checker_commit,
                "source": "https://github.com/marijnheule/drat-trim",
            },
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "summary": {
            "certificates": len(results),
            "independently_verified": sum(
                row["independent_verification"]["trimmed_core"] == "VERIFIED"
                for row in results
            ),
            "compressed_certificate_bytes": sum(
                row["certificate"]["cnf_gz_bytes"]
                + row["certificate"]["drat_gz_bytes"]
                for row in results
            ),
        },
        "results": results,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
