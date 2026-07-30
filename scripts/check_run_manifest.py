#!/usr/bin/env python3
"""Cold-verify a supervisor-owned research execution manifest."""

from __future__ import annotations

import sys
from pathlib import Path

from einstein.repository import repository_root
from einstein.repository.research import validate_run_manifest


ROOT = repository_root(Path(__file__))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_run_manifest.py <run-manifest.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        print(f"missing run manifest: {path}", file=sys.stderr)
        return 2
    errors = validate_run_manifest(path, root=ROOT)
    if errors:
        for error in errors:
            print(f"manifest: {error}", file=sys.stderr)
        return 1
    print(f"run manifest: PASS [{path.relative_to(ROOT)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
