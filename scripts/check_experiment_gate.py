#!/usr/bin/env python3
"""Validate the mandatory research-experiment pre-registration block."""

from __future__ import annotations

import re
import sys
from pathlib import Path


HEADINGS = (
    "Proposition",
    "Prior art and non-redundancy",
    "Outcome decisions",
    "Stop rule and finite justification",
    "Human checkpoint",
)
PLACEHOLDERS = ("[REPLACE", "TODO", "TBD", "Not run.")


def sections(text: str) -> dict[str, str]:
    if "## Experiment pre-registration" not in text:
        return {}
    block = text.split("## Experiment pre-registration", 1)[1]
    block = block.split("\n## ", 1)[0]
    found: dict[str, str] = {}
    matches = list(re.finditer(r"^### (.+?)\s*$", block, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        found[match.group(1)] = block[match.end():end].strip()
    return found


def validate(path: Path) -> list[str]:
    found = sections(path.read_text())
    errors = []
    for heading in HEADINGS:
        body = found.get(heading, "")
        if not body:
            errors.append(f"missing or empty section: {heading}")
        elif len(body) < 40:
            errors.append(f"section is too short to be auditable: {heading}")
        elif any(marker.lower() in body.lower() for marker in PLACEHOLDERS):
            errors.append(f"placeholder remains in section: {heading}")
    outcomes = found.get("Outcome decisions", "")
    if len(re.findall(r"^[-*] ", outcomes, re.MULTILINE)) < 2:
        errors.append("Outcome decisions must contain at least two explicit branches")
    return errors


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
