#!/usr/bin/env python
"""Run one frozen HC-38 tangent cell with cvc5/CAC."""

from __future__ import annotations

from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

import cvc5

from einstein.db import code_version
from einstein.theory.cvc5_models import exact_real_payload
from einstein.theory.k16w_exact import HC34_CELLS


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
FORMULA_MANIFEST = ASSETS / "k16w-hc38-tangent-formulas.json"
MEMORY_MIB = 16 * 1024
ASSERTION_COUNT = 190


def load_frozen_solver(cell: str) -> tuple[cvc5.Solver, dict[str, cvc5.Term], dict]:
    manifest = json.loads(FORMULA_MANIFEST.read_text())
    records = {record["cell"]: record for record in manifest.get("records", [])}
    if not manifest.get("complete") or manifest.get("cell_order") != list(HC34_CELLS):
        raise RuntimeError("cold tangent formula manifest is incomplete or reordered")
    if manifest.get("cvc5_version") != importlib.metadata.version("cvc5"):
        raise RuntimeError("cvc5 version drift")
    if cell not in records:
        raise RuntimeError(f"cold tangent formula record missing for {cell}")
    record = records[cell]
    formula = ROOT / record["path"]
    data = formula.read_bytes()
    if record.get("bytes") != len(data):
        raise RuntimeError(f"formula byte-count drift for {cell}")
    if record.get("sha256") != sha256(data).hexdigest():
        raise RuntimeError(f"formula hash drift for {cell}")

    solver = cvc5.Solver()
    for name, value in manifest["cvc5_options"].items():
        solver.setOption(name, value)
    parser = cvc5.InputParser(solver)
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, str(formula))
    while not parser.done():
        command = parser.nextCommand()
        if command.isNull():
            break
        if command.getCommandName() == "check-sat":
            continue
        command.invoke(solver, parser.getSymbolManager())
    if len(solver.getAssertions()) != ASSERTION_COUNT:
        raise RuntimeError(f"formula assertion-count drift for {cell}")
    terms = {str(term): term for term in parser.getSymbolManager().getDeclaredTerms()}
    expected = set(record["solver_variables"])
    if set(terms) != expected:
        raise RuntimeError(f"declared-variable drift for {cell}: {sorted(terms)}")
    return solver, terms, record


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) != 2 or argv[1] not in HC34_CELLS:
        print(f"usage: {argv[0]} {{{'|'.join(HC34_CELLS)}}}", file=sys.stderr)
        return 2
    cell = argv[1]
    resource.setrlimit(
        resource.RLIMIT_AS,
        (MEMORY_MIB * 1024 * 1024, MEMORY_MIB * 1024 * 1024),
    )
    stem = f"k16w-hc38-tangent-{cell}"
    result_path = ASSETS / f"{stem}-result.json"
    verify_path = ASSETS / f"{stem}-result-verification.json"
    solver, terms, formula_record = load_frozen_solver(cell)

    started = time.monotonic()
    answer = solver.checkSat()
    elapsed = time.monotonic() - started
    status = str(answer)
    payload = {
        "kind": "k16w-hc38-tangent-cell-result",
        "schema_version": 1,
        "date": "2026-07-24",
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "memory_limit_mib": MEMORY_MIB,
        "cvc5_version": importlib.metadata.version("cvc5"),
        "cvc5_options": json.loads(FORMULA_MANIFEST.read_text())["cvc5_options"],
        "code_version": code_version(),
        "formula": {
            "path": formula_record["path"],
            "sha256": formula_record["sha256"],
            "constraint_counts": formula_record["constraint_counts"],
            "normalization": "u=1; all physical points scaled by K35T T>0",
            "simplicity": "all 120 exact closed-segment predicates retained",
        },
        "claim_boundary": {
            "sat": "carrier geometry only; requires admitted-field cold verification",
            "unsat": "cvc5/CAC evidence only; no independent proof certificate",
            "unknown": "cell remains open; no rerun or option change",
        },
        "model": None,
        "model_field_supported": None,
        "statistics": str(solver.getStatistics()),
    }
    if status == "sat":
        payload["model"] = {
            name: exact_real_payload(solver, solver.getValue(terms[name]))
            for name in formula_record["solver_variables"]
        }
        payload["model_field_supported"] = all(
            entry.get("kind") in {"rational", "q_sqrt2"}
            for entry in payload["model"].values()
        )
    result_path.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({
        "cell": cell,
        "status": status,
        "elapsed_seconds": elapsed,
        "model_field_supported": payload["model_field_supported"],
        "formula_sha256": formula_record["sha256"],
    }, indent=1), flush=True)

    if status == "sat":
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_k16w_exact.py"),
             str(result_path), cell],
            cwd=ROOT,
            check=False,
        )
        if not verify_path.exists() or completed.returncode != 0:
            print("cold verification did not certify the SAT model", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
