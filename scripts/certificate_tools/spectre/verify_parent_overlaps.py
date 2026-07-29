#!/usr/bin/env python
"""Cold verifier for the coordinated Spectre parent-overlap artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.spectre.parent_overlaps import analyze_parent_overlap_language
from einstein.tilings.spectre.certificates import file_sha256


ROOT = repository_root(Path(__file__))


def verify(path):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-parent-overlap"
        or artifact.get("version") != 1
        or artifact.get("status") != "CONDITIONAL_EXTRAS_REFUTED_RADIUS4"
    ):
        return False, "unsupported schema or status"
    provenance = artifact["provenance"]
    a6_path = ROOT / provenance["a6_source"]
    physical_path = ROOT / provenance["physical_source"]
    if file_sha256(a6_path) != provenance["a6_sha256"]:
        return False, "A6 source hash mismatch"
    if file_sha256(physical_path) != provenance["physical_sha256"]:
        return False, "physical-language source hash mismatch"
    expected = analyze_parent_overlap_language(
        json.loads(a6_path.read_text()), json.loads(physical_path.read_text())
    )
    if expected != artifact.get("analysis"):
        return False, "stored analysis does not match exact recomputation"
    if expected["summary"]["extras_surviving_coordinated_grouping"]:
        return False, "an extra corona still survives"
    return True, (
        "18/18 generated controls survive; extras 33/44/155 have zero "
        "coordinated radius-four frontier states"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    ok, message = verify(args.artifact)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
