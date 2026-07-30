#!/usr/bin/env python3
"""Validate an admitted sustained-program or experiment proposal."""

from __future__ import annotations

import sys
from pathlib import Path

from einstein.repository import repository_root
from einstein.repository.research import validate_research_proposal


ROOT = repository_root(Path(__file__))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_research_proposal.py <proposal.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        print(f"missing proposal: {path}", file=sys.stderr)
        return 2
    errors = validate_research_proposal(
        path,
        root=ROOT,
        require_admitted=True,
    )
    if errors:
        for error in errors:
            print(f"gate: {error}", file=sys.stderr)
        return 1
    print(f"research proposal: PASS [{path.relative_to(ROOT)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
