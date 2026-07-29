#!/usr/bin/env python
"""Cold verifier for the contracted parent-interface no-go artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.repository import repository_root
from einstein.tilings.spectre.certificates import file_sha256
from einstein.tilings.spectre.source_controls import analyze_parent_interfaces


ROOT = repository_root(Path(__file__))
A6_PATH = ROOT / "docs/notebook/assets/a6-spectre-results.json"


def verify(path):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-parent-interface"
        or artifact.get("version") != 1
        or artifact.get("status") != "ALL_26_UNCOLORED_STATES_SURVIVE"
    ):
        return False, "unsupported schema or status"
    provenance = artifact["provenance"]
    source = ROOT / provenance["component_source"]
    if file_sha256(source) != provenance["component_sha256"]:
        return False, "component source hash mismatch"
    expected = analyze_parent_interfaces(
        json.loads(source.read_text()), json.loads(A6_PATH.read_text())
    )
    if expected != artifact.get("analysis"):
        return False, "stored analysis differs from exact recomputation"
    if expected["surviving_extra_states"] != list(range(9)):
        return False, "an extra state was unexpectedly removed"
    return True, "all 17 generated and all 9 extra uncolored states survive"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    ok, message = verify(args.artifact)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
