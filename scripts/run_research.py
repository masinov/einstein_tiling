#!/usr/bin/env python3
"""Launch a pre-registered research command within checkpoint budgets."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from check_experiment_gate import validate


ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS = ROOT / "docs" / "HUMAN_CHECKPOINTS.json"


def tree_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def main(argv: list[str]) -> int:
    if len(argv) < 4 or argv[2] != "--":
        print("usage: run_research.py <session-notebook.md> -- <command> ...", file=sys.stderr)
        return 2

    notebook = Path(argv[1])
    if not notebook.is_absolute():
        notebook = ROOT / notebook
    errors = validate(notebook)
    if errors:
        for error in errors:
            print(f"gate: {error}", file=sys.stderr)
        return 1

    match = re.search(r"session-(\d+)\.md$", notebook.name)
    if not match:
        print("gate: notebook filename must contain session-NN.md", file=sys.stderr)
        return 1
    session = int(match.group(1))

    checkpoint = json.loads(CHECKPOINTS.read_text())
    policy = checkpoint["policy"]
    latest = checkpoint["latest"]
    distance = session - latest["through_session"]
    if distance < 1 or distance > policy["max_research_sessions"]:
        print(
            f"gate: session {session} is outside checkpoint {latest['id']} "
            f"allowance 1..{policy['max_research_sessions']}",
            file=sys.stderr,
        )
        return 1

    current = sum(tree_bytes(ROOT / root) for root in policy["artifact_roots"])
    baseline = sum(latest["artifact_bytes"].values())
    growth = max(0, current - baseline)
    if growth >= policy["max_new_artifact_bytes"]:
        print(
            f"gate: artifact growth {growth} reached checkpoint limit "
            f"{policy['max_new_artifact_bytes']}",
            file=sys.stderr,
        )
        return 1

    print(
        f"research gate: PASS [{latest['id']}; session +{distance}; "
        f"artifact growth {growth} bytes]",
        flush=True,
    )
    return subprocess.run(argv[3:], cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
