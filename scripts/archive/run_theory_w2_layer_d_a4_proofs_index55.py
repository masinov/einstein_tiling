#!/usr/bin/env python
"""Produce independently checked A4 proofs for the index-55 closure.

Only twists in the Klein-four kernel are required.  T2.D4 proves that the
C3 coordinate of a period twist vanishes for an exact cover; the producer
nevertheless builds every one of the resulting 21 HNF x 16 V4-twist CNFs
and stores independently verified DRAT cores.
"""

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
from einstein.theory.a4_semidirect import canonical_a4_semidirect
from einstein.theory.finite_groups import alternating_group
from einstein.theory.holonomy_finite_csp import (
    build_finite_boundary_holonomy_cnf,
    commuting_pairs,
)
from run_theory_w2_layer_d_proofs import (
    _clause_hash,
    _gzip_deterministic,
    _read_dimacs_clauses,
)


ROOT = Path(__file__).resolve().parents[2]
SEARCH = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature-index55.json"
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
FACTOR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-factor.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index55.json"
CERT_DIR = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-proof-index55"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _v4_twists(group):
    coordinates = canonical_a4_semidirect()
    return tuple(
        (index, pair)
        for index, pair in enumerate(commuting_pairs(group))
        if all(coordinates.coordinate(element).q == 0 for element in pair)
    )


def _prove_one(arguments):
    shape, hnf, mapping_index, images, twist_index, twists, group, checker = arguments
    started = perf_counter()
    cnf, metadata = build_finite_boundary_holonomy_cnf(
        shape, hnf, images, twists, group
    )
    generated = Counter(tuple(sorted(clause)) for clause in cnf.clauses)
    stem = (
        f"hnf-{hnf[0]}-{hnf[1]}-{hnf[2]}-map-{mapping_index}-"
        f"twist-{twist_index:02d}"
    )
    with tempfile.TemporaryDirectory(prefix="layer-d-a4-index55-proof-", dir="/tmp") as name:
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
            "mapping_index": mapping_index,
            "twist_index": twist_index,
            "twists": list(twists),
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
    parser.add_argument("--jobs", type=int, default=24)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")
    search = json.loads(SEARCH.read_text())
    selected = {
        tuple(row["hnf"]): min(row["killing_signature_mapping_indices"])
        for row in search["finalist"]["by_hnf"]
        if row["killing_signature_mapping_indices"]
    }
    if len(selected) != 21 or set(selected.values()) != {7}:
        raise AssertionError("A4 index-55 deterministic kill cover changed")
    matrix = json.loads(MATRIX.read_text())
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    group = alternating_group(4)
    v4_twists = _v4_twists(group)
    if len(v4_twists) != 16:
        raise AssertionError("expected all 16 ordered V4 twist pairs")
    shape = decode_compiled_key(KEY)
    tasks = [
        (shape, hnf, mapping_index, mappings[mapping_index], twist_index,
         pair, group, checker)
        for hnf, mapping_index in sorted(selected.items())
        for twist_index, pair in v4_twists
    ]
    print(f"A4 index-55 proof tasks: {len(tasks)}; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_prove_one, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            row = future.result()
            results.append(row)
            print(
                f"[{completed:3d}/{len(tasks)}] {tuple(row['hnf'])} "
                f"twist={row['twist_index']:02d} VERIFIED "
                f"({row['wall_seconds']:.1f}s, "
                f"{row['certificate']['drat_gz_bytes']/1048576:.2f} MiB)",
                flush=True,
            )
    results.sort(key=lambda row: (row["hnf"], row["twist_index"]))
    checker_root = Path(checker).parent
    checker_commit = subprocess.run(
        ["git", "-C", checker_root, "rev-parse", "HEAD"], check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    dependencies = (SEARCH, MATRIX, FACTOR)
    sources = (
        ROOT / "src/einstein/theory/finite_groups.py",
        ROOT / "src/einstein/theory/holonomy_finite_csp.py",
        ROOT / "src/einstein/theory/a4_semidirect.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-a4-index55-independent-drat-certificates",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "hnfs": [list(hnf) for hnf in sorted(selected)],
            "selected_mapping_rule": "lowest killing A4 signature class per HNF",
            "selected_mapping_index": 7,
            "twist_indices": [index for index, _ in v4_twists],
            "twists_per_hnf": len(v4_twists),
            "twist_reduction": (
                "T2.D4: exact-cover period twists have zero C3 coordinate"
            ),
            "certificate_logic": (
                "every exact-cover-relevant twist has a generated canonical "
                "CNF, independently verified DRAT core, and "
                "multiplicity-respecting subset check"
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
        "summary": {
            "certificates": len(results),
            "independently_verified": sum(
                row["independent_verification"]["trimmed_core"] == "VERIFIED"
                for row in results
            ),
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
