#!/usr/bin/env python
"""Certify the single-orbit packing refinement on the index-60 escapes."""

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
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    collision_overlap,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_product import build_v4_product_coverability_cnf
from einstein.theory.holonomy_csp import quotient_boundary_data
from run_theory_w2_layer_d_proofs import (
    _clause_hash,
    _gzip_deterministic,
    _read_dimacs_clauses,
)


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-product.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-packing.json"
CERT_DIR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index60-packing"
KEY = "010001010104010502f002f1030b030c04fa04fb"
COLLISION_SEED = ((3, 0, 0), (5, 0, 1))


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _build_case(shape, witness, lift):
    hnf = tuple(lift["hnf"])
    layers = tuple(
        (tuple(images), tuple(twists))
        for images, twists in zip(witness["images"], lift["induced_twists"])
    )
    cnf, metadata = build_v4_product_coverability_cnf(shape, hnf, layers)
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, COLLISION_SEED[0]),
        placement_lattice_cells(shape, COLLISION_SEED[1]),
    )
    clauses = collision_orbit_clauses(shape, hnf, instance, target)
    if len(clauses) != 12 * hnf[0] * hnf[2]:
        raise AssertionError("collision orbit is not free under translation and D6")
    if any(not (instance.placements[-clause[0] - 1][1]
                & instance.placements[-clause[1] - 1][1]) for clause in clauses):
        raise AssertionError("packing orbit contains a non-collision")
    cnf.extend(clauses)
    packing = {
        "kind": "single-D6-collision-orbit-nonoverlap",
        "seed_placements": [list(row) for row in COLLISION_SEED],
        "overlap_cells": collision_overlap(target),
        "orbit_clauses": len(clauses),
        "is_subset_of_exact_nonoverlap": True,
    }
    return cnf, metadata, packing


def _prove_one(arguments):
    shape, witness, lift, checker = arguments
    started = perf_counter()
    cnf, metadata, packing = _build_case(shape, witness, lift)
    generated = Counter(tuple(sorted(clause)) for clause in cnf.clauses)
    hnf = tuple(lift["hnf"])
    stem = f"hnf-{hnf[0]}-{hnf[1]}-{hnf[2]}-full16-overlap6-orbit"
    with tempfile.TemporaryDirectory(prefix="layer-d-index60-packing-", dir="/tmp") as name:
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
            "packing_refinement": packing,
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
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")
    product = json.loads(PRODUCT.read_text())
    witness = product["base_witness"]
    lifts = product["index60_lifts"]
    if len(lifts) != 3:
        raise AssertionError("expected the three index-60 D6-orbit escapes")
    shape = decode_compiled_key(KEY)
    tasks = [(shape, witness, lift, checker) for lift in lifts]
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_prove_one, task) for task in tasks]
        for future in as_completed(futures):
            row = future.result()
            results.append(row)
            print(
                f"{tuple(row['hnf'])}: VERIFIED ({row['wall_seconds']:.1f}s, "
                f"{row['certificate']['drat_gz_bytes']/1048576:.2f} MiB)",
                flush=True,
            )
    results.sort(key=lambda row: row["hnf"])
    checker_root = Path(checker).parent
    checker_commit = subprocess.run(
        ["git", "-C", checker_root, "rev-parse", "HEAD"], check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    sources = (
        ROOT / "src/einstein/theory/a4_v4_sft.py",
        ROOT / "src/einstein/theory/a4_v4_product.py",
        ROOT / "src/einstein/theory/a4_v4_packing.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-index60-single-orbit-packing-certificates",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "hnfs": [row["hnf"] for row in results],
            "signature_layers": 16,
            "packing_axiom": (
                "forbid one exact D6 orbit of two-tile collisions sharing six kites"
            ),
            "logical_polarity": (
                "sound relaxation of exact cover: all omitted collision orbits remain allowed"
            ),
        },
        "provenance": {
            "dependencies": [{
                "path": str(PRODUCT.relative_to(ROOT)), "sha256": _digest(PRODUCT),
            }],
            "producer": "Glucose 4 via python-sat",
            "checker": {"name": "drat-trim", "git_commit": checker_commit},
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "conclusion": {
            "all_three_index60_escapes_unsat": True,
            "full_nonoverlap_used": False,
            "collision_orbits_used": 1,
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
