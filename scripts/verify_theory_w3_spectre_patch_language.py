#!/usr/bin/env python
"""Cold verifier for the exact radius-three physical Spectre prefix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.tilings.spectre.patches import analyze_physical_patch_language
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[1]


def verify(path):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-physical-patch-language"
        or artifact.get("version") != 1
    ):
        return False, "unsupported schema"
    source_path = ROOT / artifact["provenance"]["a6_source"]
    if file_sha256(source_path) != artifact["provenance"]["a6_sha256"]:
        return False, "A6 source hash mismatch"
    expected = analyze_physical_patch_language(json.loads(source_path.read_text()))
    if expected != artifact.get("analysis"):
        return False, "stored analysis does not match exact recomputation"
    if artifact.get("status") != "COMPLETE_RADIUS3_PREFIX":
        return False, "artifact status overstates or understates the finite scope"
    return True, (
        f"166 r1, {expected['radius2']['surviving_first_coronas']} r2, "
        f"{expected['radius3']['surviving_first_coronas']} r3; "
        "18 substitution-observed"
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
