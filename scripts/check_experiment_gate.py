#!/usr/bin/env python3
"""Compatibility name for the proposal-based experiment admission gate."""

from __future__ import annotations

import sys
from pathlib import Path

from einstein.repository import repository_root
from einstein.repository.research import validate_research_proposal


ROOT = repository_root(Path(__file__))


def validate(
    path: Path,
    *,
    root: Path = ROOT,
    admission_path: Path | None = None,
) -> list[str]:
    return validate_research_proposal(
        path,
        root=root,
        require_admitted=True,
        require_experiment=True,
        admission_path=admission_path,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_experiment_gate.py <research-proposal.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        print(f"missing proposal: {path}", file=sys.stderr)
        return 2
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"gate: {error}", file=sys.stderr)
        return 1
    print(f"experiment gate: PASS [{path.relative_to(ROOT)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
