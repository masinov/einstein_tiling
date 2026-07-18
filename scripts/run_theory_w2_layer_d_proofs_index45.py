#!/usr/bin/env python
"""Produce independently checked DRAT cores for all nine index-45 kills."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy import s3_boundary_surjections
from einstein.theory.holonomy_csp import commuting_s3_pairs
import run_theory_w2_layer_d_proofs as proof_tools


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index45.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-proof-index45.json"
CERT_DIR = ROOT / "docs/notebook/assets/theory-w2-layer-d-proof-index45"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _prove_one(arguments):
    proof_tools.CERT_DIR = CERT_DIR
    return proof_tools._prove_one(arguments)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--drat-trim", default="/tmp/drat-trim/drat-trim")
    args = parser.parse_args()
    checker = str(Path(args.drat_trim).resolve())
    if not Path(checker).is_file():
        raise SystemExit(f"missing proof checker: {checker}")

    search = json.loads(SEARCH.read_text())
    if not search["scope"]["matrix_complete"]:
        raise AssertionError("index-45 search matrix is incomplete")
    selected = {
        tuple(row["hnf"]): min(row["killing_mapping_indices"])
        for row in search["finalist"]["by_hnf"]
    }
    if len(selected) != 9 or any(not value for value in selected.values()):
        raise AssertionError("index-45 kill cover changed")

    shape = decode_compiled_key(KEY)
    mappings = s3_boundary_surjections(shape, displacement_kernel_order=3)
    twists = commuting_s3_pairs()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    tasks = [
        (shape, hnf, mapping_index, mappings[mapping_index], twist_index, pair, checker)
        for hnf, mapping_index in sorted(selected.items())
        for twist_index, pair in enumerate(twists)
    ]
    print(f"index-45 proof tasks: {len(tasks)}; jobs={args.jobs}", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(_prove_one, task): task[1:6] for task in tasks}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(
                f"[{completed:3d}/{len(tasks)}] {tuple(result['hnf'])} "
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
        ROOT / "src/einstein/theory/holonomy.py",
        ROOT / "src/einstein/theory/holonomy_csp.py",
        ROOT / "scripts/run_theory_w2_layer_d_proofs.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-index45-independent-drat-certificates",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "hnfs": [list(hnf) for hnf in sorted(selected)],
            "selected_mapping_rule": "lowest killing conjugacy-class index per HNF",
            "selected_mappings": [
                {"hnf": list(hnf), "mapping_index": mapping_index}
                for hnf, mapping_index in sorted(selected.items())
            ],
            "twists_per_hnf": len(twists),
            "certificate_logic": (
                "each stored core CNF is a multiplicity-respecting subset of "
                "the canonical generated CNF; drat-trim independently verifies "
                "the stored DRAT core; all 18 commuting twists are covered"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "search": {
                "path": str(SEARCH.relative_to(ROOT)),
                "sha256": _digest(SEARCH),
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
