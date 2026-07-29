"""Mechanical admission primitives shared by research command entry points."""

from __future__ import annotations

import re
from pathlib import Path


HEADINGS = (
    "Proposition",
    "Prior art and non-redundancy",
    "Outcome decisions",
    "Stop rule and finite justification",
    "Human checkpoint",
)
PLACEHOLDERS = ("[REPLACE", "TODO", "TBD", "Not run.")


def preregistration_sections(text: str) -> dict[str, str]:
    if "## Experiment pre-registration" not in text:
        return {}
    block = text.split("## Experiment pre-registration", 1)[1]
    block = block.split("\n## ", 1)[0]
    found: dict[str, str] = {}
    matches = list(re.finditer(r"^### (.+?)\s*$", block, re.MULTILINE))
    for index, match in enumerate(matches):
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(block)
        )
        found[match.group(1)] = block[match.end() : end].strip()
    return found


def validate_preregistration(path: Path) -> list[str]:
    """Return every mechanical admission error in one notebook."""

    found = preregistration_sections(path.read_text())
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


def tree_bytes(path: Path) -> int:
    """Total bytes in a file tree, treating an absent root as empty."""

    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
