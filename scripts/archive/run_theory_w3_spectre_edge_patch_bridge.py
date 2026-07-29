#!/usr/bin/env python
"""Package the unrestricted Spectre edge-patch to primitive-contact bridge."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.tilings.spectre.edge_contacts import analyze_edge_patch_bridge


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-edge-patch-bridge.json"


def main():
    analysis = analyze_edge_patch_bridge()
    if not analysis["theorem"][
        "unrestricted_contacts_reduce_to_primitive_edge_to_edge"
    ]:
        raise ValueError("unrestricted contact bridge did not close")
    artifact = {
        "schema": "einstein.w3.spectre-edge-patch-bridge",
        "version": 1,
        "status": "UNRESTRICTED_EDGE_PATCH_BRIDGE_PROVED",
        "subject": "straight Tile(1,1), one fixed chirality",
        "scope": {
            "motions": ["translation", "rotation"],
            "reflections_allowed": False,
            "input_contact_model": (
                "arbitrary locally finite polygon tilings, including vertices "
                "on sides and T-junctions"
            ),
            "output_contact_model": "full primitive unit-edge contacts",
        },
        "published_crosscheck": {
            "source": "smkgs-chiral-2024",
            "results": ["Lemma 2.3", "Theorem 3.1"],
            "role": (
                "independent unrestricted edge-patch and even/odd deformation "
                "route to aligned hat-turtle tilings"
            ),
        },
        "analysis": analysis,
        "claim": {
            "verdict": (
                "every fixed-chirality straight-Spectre tiling is represented "
                "by the exact 14-segment primitive contact model"
            ),
            "logic": (
                "the angle hypotheses bound each maximal straight interface "
                "to two sides per half-plane; all ten equal-length words have "
                "one common integer unit subdivision; adjacency locks one "
                "30-degree frame and matched endpoints lock all anchors to the "
                "rank-four module"
            ),
        },
        "claim_boundary": (
            "fixed chirality only; mixed reflected/unreflected Tile(1,1) "
            "tilings are outside the W3 Spectre domain"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        "edge-patch bridge: 13 maximal sides, 10 interface patterns -> PASS"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
