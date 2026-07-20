#!/usr/bin/env python
"""Prove L18 corona entry for fixed-chirality edge-to-edge Spectre tilings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.spectre_d1_entry import analyze_d1_entry
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-d1-entry.json"
PLOT = ROOT / "docs/notebook/assets/theory-w3-spectre-d1-entry.svg"


def render(analysis, path):
    records = analysis["radius_records"]
    values = [(1, analysis["initial_frontier_patches"])] + [
        (row["radius"], row["surviving_patches"]) for row in records
    ]
    width, height = 1000, 470
    left, right, top, bottom = 105, 55, 90, 90
    chart_w = width - left - right
    chart_h = height - top - bottom
    maximum = max(value for _, value in values)
    points = []
    for index, (radius, value) in enumerate(values):
        x = left + chart_w * index / (len(values) - 1)
        y = top + chart_h * (1 - value / maximum)
        points.append((x, y, radius, value))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        '<text x="500" y="38" text-anchor="middle" fill="#f8f9fa" '
        'font-family="sans-serif" font-size="24">D1 physical entry: non-L18 corona frontier</text>',
        '<text x="500" y="65" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="14">exact fixed-chirality edge-to-edge rings; no parent or substitution constraints</text>',
        f'<line x1="{left}" y1="{top+chart_h}" x2="{width-right}" '
        f'y2="{top+chart_h}" stroke="#565f89" stroke-width="2"/>',
        '<polyline points="' + " ".join(
            f"{x:.1f},{y:.1f}" for x, y, _, _ in points
        ) + '" fill="none" stroke="#7aa2f7" stroke-width="4"/>',
    ]
    for x, y, radius, value in points:
        lines.extend((
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#bb9af7"/>',
            f'<text x="{x:.1f}" y="{y-16:.1f}" text-anchor="middle" '
            f'fill="#f8f9fa" font-family="sans-serif" font-size="20">{value}</text>',
            f'<text x="{x:.1f}" y="{top+chart_h+34:.1f}" text-anchor="middle" '
            f'fill="#c0caf5" font-family="sans-serif" font-size="16">radius {radius}</text>',
        ))
    lines.extend((
        '<text x="500" y="442" text-anchor="middle" fill="#9ece6a" '
        'font-family="sans-serif" font-size="16">all three extra coronas are excluded by the empty radius-five frontier</text>',
        '</svg>',
    ))
    path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=24)
    args = parser.parse_args()
    physical = json.loads(PHYSICAL.read_text())
    prefix = physical["analysis"]
    extras = prefix["radius3"]["unobserved_survivor_indices"]
    if extras != [33, 44, 155]:
        raise ValueError("physical-prefix extra-corona set changed")
    analysis = analyze_d1_entry(target_radius=5, workers=args.workers)
    if not analysis["all_extra_coronas_eliminated"]:
        raise ValueError("non-L18 physical frontier did not close")
    artifact = {
        "schema": "einstein.w3.spectre-d1-entry",
        "version": 1,
        "status": "EDGE_TO_EDGE_L18_ENTRY_PROVED_RADIUS5",
        "provenance": {
            "physical_language_source": str(PHYSICAL.relative_to(ROOT)),
            "physical_language_sha256": file_sha256(PHYSICAL),
        },
        "scope": {
            "tile": "straight-edged Tile(1,1)",
            "chirality": "one fixed handedness",
            "motions": ["translation", "rotation"],
            "contact_model": "edge-to-edge unit-edge tilings",
            "ancestry_or_parent_data_used_in_ring_enumeration": False,
            "target_selection": (
                "the three exact physical corona types outside L18"
            ),
        },
        "physical_prefix": {
            "complete_first_coronas": prefix["radius1"]["complete_coronas"],
            "radius2_surviving_types": prefix["radius2"][
                "surviving_first_coronas"
            ],
            "radius3_surviving_types": prefix["radius3"][
                "surviving_first_coronas"
            ],
            "L18_corona_types": prefix["substitution_control"][
                "observed_first_coronas"
            ],
            "non_L18_radius3_types": extras,
        },
        "elimination": analysis,
        "theorem": {
            "verdict": (
                "every complete tile corona in any whole-plane tiling in the "
                "declared edge-to-edge domain belongs to L18"
            ),
            "logic": (
                "a whole-plane occurrence of any non-L18 corona restricts to "
                "one of the exhaustively enumerated finite ring patches, but "
                "their complete radius-five frontier is empty"
            ),
        },
        "claim_boundary": (
            "this discharges D1 inside the fixed-chirality edge-to-edge model; "
            "a separate theorem must exclude non-edge-to-edge straight-Spectre "
            "tilings before claiming the unrestricted geometric hull"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    render(analysis, PLOT)
    print(
        "D1 edge-to-edge entry: frontier",
        [analysis["initial_frontier_patches"], *(
            row["surviving_patches"] for row in analysis["radius_records"]
        )],
        "-> PASS",
    )
    print(OUTPUT.relative_to(ROOT))
    print(PLOT.relative_to(ROOT))


if __name__ == "__main__":
    main()
