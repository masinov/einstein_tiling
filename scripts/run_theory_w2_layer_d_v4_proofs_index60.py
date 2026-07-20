#!/usr/bin/env python
"""Produce checked twist-union proofs for the 42 map-7 index-60 kills."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from time import perf_counter

from pysat.solvers import Solver

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_sft import V4_TWIST_PAIRS
from einstein.theory.a4_v4_twist_union import (
    build_map7_v4_coverability_union_cnf,
)
from run_theory_w2_layer_d_proofs import (
    _clause_hash,
    _gzip_deterministic,
    _read_dimacs_clauses,
)


ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-sft-index60.json"
FACTOR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-factor.json"
PACKING = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-packing.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-map7.json"
CERT_DIR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-map7"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _prove_one(arguments):
    shape, hnf, checker = arguments
    started = perf_counter()
    cnf, metadata = build_map7_v4_coverability_union_cnf(shape, hnf)
    generated = Counter(tuple(sorted(clause)) for clause in cnf.clauses)
    stem = f"hnf-{hnf[0]}-{hnf[1]}-{hnf[2]}-map7-v4-twist-union"
    with tempfile.TemporaryDirectory(prefix="layer-d-index60-map7-", dir="/tmp") as name:
        temp = Path(name)
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
            raise AssertionError(f"Glucose failed to prove UNSAT: {stem}")
        raw_proof.write_text("\n".join(proof) + "\n")
        trim = subprocess.run(
            [checker, original_cnf, raw_proof, "-c", core_cnf, "-l", core_proof],
            check=True, text=True, capture_output=True,
        )
        if "s VERIFIED" not in trim.stdout:
            raise AssertionError(f"raw proof failed: {stem}")
        checked = subprocess.run(
            [checker, core_cnf, core_proof], check=True, text=True,
            capture_output=True,
        )
        if "s VERIFIED" not in checked.stdout:
            raise AssertionError(f"core proof failed: {stem}")
        core = Counter(tuple(sorted(clause)) for clause in _read_dimacs_clauses(core_cnf))
        if any(count > generated[clause] for clause, count in core.items()):
            raise AssertionError(f"core contains a non-generated clause: {stem}")
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        cnf_target = CERT_DIR / f"{stem}.cnf.gz"
        proof_target = CERT_DIR / f"{stem}.drat.gz"
        _gzip_deterministic(core_cnf, cnf_target)
        _gzip_deterministic(core_proof, proof_target)
        return {
            "hnf": list(hnf),
            "canonical_cnf_clause_hash": _clause_hash(cnf),
            "canonical_metadata": metadata,
            "core_clauses": sum(core.values()),
            "core_subset_verified": True,
            "glucose_stats": stats,
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
                "raw_proof": "VERIFIED", "trimmed_core": "VERIFIED",
            },
            "wall_seconds": perf_counter() - started,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")
    scan = json.loads(SCAN.read_text())
    shell = next(row for row in scan["by_index"] if row["index"] == 60)
    obstructed = []
    survivors = []
    for row in shell["results"]:
        hnf = tuple(row["hnf"])
        if row["verdict"] == "holonomy-obstructed":
            if len(row["checks"]) != len(V4_TWIST_PAIRS) or any(
                check["sat"] for check in row["checks"]
            ):
                raise AssertionError(f"incomplete obstructed search row: {hnf}")
            obstructed.append(hnf)
        else:
            survivors.append(hnf)
    if len(obstructed) != 42 or sorted(survivors) != [
        (10, 2, 6), (30, 6, 2), (30, 22, 2)
    ]:
        raise AssertionError("index-60 map-7 frontier changed")
    shape = decode_compiled_key(KEY)
    tasks = [(shape, hnf, checker) for hnf in sorted(obstructed)]
    print(f"index-60 map-7 union proofs: {len(tasks)}; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_prove_one, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            row = future.result()
            results.append(row)
            print(
                f"[{completed:2d}/{len(tasks)}] {tuple(row['hnf'])} VERIFIED "
                f"({row['wall_seconds']:.1f}s, "
                f"{row['certificate']['drat_gz_bytes']/1048576:.2f} MiB)",
                flush=True,
            )
    results.sort(key=lambda row: row["hnf"])
    checker_root = Path(checker).parent
    checker_commit = subprocess.run(
        ["git", "-C", checker_root, "rev-parse", "HEAD"], check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    dependencies = (SCAN, FACTOR, PACKING)
    sources = (
        ROOT / "src/einstein/theory/a4_v4_sft.py",
        ROOT / "src/einstein/theory/a4_v4_twist_union.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-index60-map7-v4-twist-union-certificates",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "index": 60,
            "hnfs": [row["hnf"] for row in results],
            "hnfs_certified": len(results),
            "map": 7,
            "v4_twists_per_union": len(V4_TWIST_PAIRS),
            "direct_logical_cases": len(results) * len(V4_TWIST_PAIRS),
            "union_equivalence": (
                "shared cover/potential variables; selector activates each "
                "twist suffix; at least one selector is true"
            ),
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in dependencies
            ],
            "producer": "Glucose 4 via python-sat",
            "checker": {"name": "drat-trim", "git_commit": checker_commit},
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "conclusion": {
            "all_42_map7_frontier_hnfs_unsat": True,
            "three_residual_hnfs_closed_by_companion_packing_manifest": True,
            "complete_index60_shell_closed": True,
            "not_a_general_aperiodicity_proof": True,
        },
        "summary": {
            "certificates": len(results),
            "independently_verified": len(results),
            "compressed_certificate_bytes": sum(
                row["certificate"]["cnf_gz_bytes"]
                + row["certificate"]["drat_gz_bytes"] for row in results
            ),
        },
        "results": results,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
