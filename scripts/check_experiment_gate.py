#!/usr/bin/env python3
"""Validate the mandatory research-experiment pre-registration block."""

from __future__ import annotations

import sys
from pathlib import Path

from einstein.repository.research import validate_preregistration


validate = validate_preregistration


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_experiment_gate.py <session-notebook.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"missing notebook: {path}", file=sys.stderr)
        return 2
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"gate: {error}", file=sys.stderr)
        return 1
    print(f"experiment gate: PASS [{path}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
