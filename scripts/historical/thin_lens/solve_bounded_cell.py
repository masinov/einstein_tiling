#!/usr/bin/env python
"""Run one preregistered bounded HC-34 K16W cell."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.repository import repository_root
import subprocess
import sys
import time

import z3

from einstein.polykites.database import code_version
from einstein.historical.thin_lens.exact import HC34_CELLS
from einstein.solvers.algebraic_models import exact_z3_payload


ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs/notebook/assets"
TIMEOUT_MS = 3 * 60 * 60 * 1000
MEMORY_MIB = 32 * 1024
FORMULA_MANIFEST = ASSETS / "k16w-hc34-formulas.json"


def load_frozen_solver(cell: str) -> tuple[z3.Solver, dict]:
    """Load and authenticate the frozen formula without rebuilding it.

    Z3's generated ``let`` identifiers depend on construction history, so two
    equivalent calls to the Python builder need not be byte-identical.  The
    launch contract is the opposite: solve the exact bytes pinned in the cold
    manifest.  Authenticate those bytes, parse them, then attach resource
    parameters to the parsed solver.
    """

    formula_path = ASSETS / f"k16w-hc34-{cell}.smt2"
    manifest = json.loads(FORMULA_MANIFEST.read_text())
    records = {record["cell"]: record for record in manifest.get("records", [])}
    if not manifest.get("complete") or manifest.get("cell_order") != list(HC34_CELLS):
        raise RuntimeError("cold formula manifest is incomplete or reordered")
    if cell not in records:
        raise RuntimeError(f"cold formula record missing for {cell}")
    record = records[cell]
    data = formula_path.read_bytes()
    if record.get("path") != str(formula_path.relative_to(ROOT)):
        raise RuntimeError(f"formula path drift for {cell}")
    if record.get("bytes") != len(data):
        raise RuntimeError(f"formula byte-count drift for {cell}")
    if record.get("sha256") != sha256(data).hexdigest():
        raise RuntimeError(f"formula hash drift for {cell}")

    solver = z3.SolverFor("QF_NRA")
    solver.from_file(str(formula_path))
    if len(solver.assertions()) != 187:
        raise RuntimeError(f"formula assertion-count drift for {cell}")
    solver.set(timeout=TIMEOUT_MS)
    return solver, record


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) != 2 or argv[1] not in HC34_CELLS:
        print(f"usage: {argv[0]} {{{'|'.join(HC34_CELLS)}}}", file=sys.stderr)
        return 2
    cell = argv[1]
    stem = f"k16w-hc34-{cell}"
    formula_path = ASSETS / f"{stem}.smt2"
    result_path = ASSETS / f"{stem}-result.json"
    verify_path = ASSETS / f"{stem}-result-verification.json"

    z3.set_param("memory_max_size", MEMORY_MIB)
    solver, formula_record = load_frozen_solver(cell)

    started = time.monotonic()
    answer = solver.check()
    elapsed = time.monotonic() - started
    status = str(answer)
    payload = {
        "kind": "k16w-hc34-cell-result",
        "schema_version": 1,
        "date": "2026-07-23",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "timeout_ms": TIMEOUT_MS,
        "memory_limit_mib": MEMORY_MIB,
        "z3_version": z3.get_version_string(),
        "code_version": code_version(),
        "formula": {
            "path": str(formula_path.relative_to(ROOT)),
            "sha256": sha256(formula_path.read_bytes()).hexdigest(),
            "constraint_counts": formula_record["constraint_counts"],
            "normalization": "u=1",
            "cell_theorems": "N38/K29O + K31C + corrected N42 + K32S/K32A + N43/K33C",
            "simplicity": "all 120 exact closed-segment predicates retained",
        },
        "claim_boundary": {
            "sat": "requires exact cold verification; carrier geometry only",
            "unsat": "solver evidence only without replayable exact certificate",
            "unknown": "cell remains open/frozen; no rerun or escalation",
        },
        "model": None,
        "statistics": str(solver.statistics()),
        "reason_unknown": solver.reason_unknown() if status == "unknown" else None,
    }
    if status == "sat":
        model = solver.model()
        payload["model"] = {
            name: exact_z3_payload(
                model.eval(z3.Real(name), model_completion=True)
            )
            for name in ("a", "b", "c", "v", "t0", "t1", "t2", "sqrt_half")
        }
    result_path.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "formula_sha256": payload["formula"]["sha256"],
    }, indent=1), flush=True)

    if status == "sat":
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/historical/thin_lens/verify_model.py"),
             str(result_path), cell],
            cwd=ROOT,
            check=False,
        )
        if not verify_path.exists() or completed.returncode != 0:
            print("cold verification did not certify the SAT model", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
