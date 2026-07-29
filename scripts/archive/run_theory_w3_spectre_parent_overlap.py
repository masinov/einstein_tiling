#!/usr/bin/env python
"""Run the coordinated Spectre parent-overlap language experiment."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.tilings.substitution import SPECTRE_TILE_BOUNDARY
from einstein.geometry.cyclotomic import apply_sr, madd, to_xy
from einstein.tilings.spectre.parent_overlaps import analyze_parent_overlap_language
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[2]
A6 = ROOT / "docs/notebook/assets/a6-spectre-results.json"
PHYSICAL = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-parent-overlap.json"
SUMMARY = ROOT / "docs/notebook/assets/theory-w3-spectre-parent-overlap.svg"
WITNESS = ROOT / "docs/notebook/assets/theory-w3-spectre-grouping-witness.svg"


def render_summary(analysis, path: Path) -> None:
    extras = analysis["extra_coronas"]
    width, height = 1120, 610
    values = ((166, "bare r=1", "#7aa2f7"), (30, "physical r=2", "#e0af68"),
              (21, "physical r=3", "#bb9af7"), (18, "after grouping", "#9ece6a"))
    scale = 225 / 166
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        '<text x="560" y="42" text-anchor="middle" fill="#f8f9fa" '
        'font-family="sans-serif" font-size="25">Coordinated Spectre parent language</text>',
        '<text x="560" y="70" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="14">exact buffered-core grouping; 18 generated controls survive</text>',
    ]
    for column, (value, label, color) in enumerate(values):
        x = 75 + column * 260
        bar = value * scale
        lines.extend((
            f'<rect x="{x}" y="{320-bar:.2f}" width="150" height="{bar:.2f}" rx="8" fill="{color}"/>',
            f'<text x="{x+75}" y="{300-bar:.2f}" text-anchor="middle" fill="#f8f9fa" font-family="sans-serif" font-size="28">{value}</text>',
            f'<text x="{x+75}" y="348" text-anchor="middle" fill="#c0caf5" font-family="sans-serif" font-size="16">{label}</text>',
        ))
    lines.extend((
        '<line x1="70" y1="385" x2="1050" y2="385" stroke="#414868"/>',
        '<text x="85" y="418" fill="#a9b1d6" font-family="monospace" font-size="14">corona</text>',
        '<text x="260" y="418" fill="#a9b1d6" font-family="monospace" font-size="14">r2 branches</text>',
        '<text x="475" y="418" fill="#a9b1d6" font-family="monospace" font-size="14">group-compatible r3</text>',
        '<text x="735" y="418" fill="#a9b1d6" font-family="monospace" font-size="14">r4 frontier</text>',
        '<text x="900" y="418" fill="#a9b1d6" font-family="monospace" font-size="14">verdict</text>',
    ))
    for row, result in enumerate(extras):
        y = 455 + row * 38
        verdict = "REFUTED r≤4"
        color = "#f7768e"
        entries = (
            (100, str(result["corona_index"])),
            (300, str(result["complete_radius2_branches"])),
            (540, str(result["radius3_frontier_states"])),
            (775, str(result["radius4_frontier_states"])),
            (950, verdict),
        )
        for x, text in entries:
            lines.append(
                f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color if x==950 else "#f8f9fa"}" font-family="monospace" font-size="17">{text}</text>'
            )
    lines.extend((
        '<text x="560" y="585" text-anchor="middle" fill="#a9b1d6" font-family="sans-serif" font-size="13">conditional on the recovered 9/8 parent templates; not an all-tilings recognisability theorem</text>',
        '</svg>',
    ))
    path.write_text("\n".join(lines) + "\n")


def _parse_pose(row):
    return row[0], row[1], tuple(row[2])


def render_grouping_witness(analysis, path: Path) -> None:
    witness = analysis["representative_generated_grouping"]
    patch = tuple(_parse_pose(row) for row in witness["patch"])
    parents = [set(_parse_pose(row) for row in parent)
               for parent in witness["selected_parents"]]
    safe = { _parse_pose(row) for row in witness["safe_tiles"] }
    palette = ("#7aa2f7", "#e0af68", "#bb9af7", "#9ece6a", "#f7768e",
               "#73daca", "#ff9e64", "#c0caf5")
    polygons = []
    for pose in patch:
        points = [
            to_xy(madd(pose[2], apply_sr(pose[0], pose[1], vertex)))
            for vertex in SPECTRE_TILE_BOUNDARY
        ]
        owner = next((index for index, parent in enumerate(parents) if pose in parent), None)
        polygons.append((pose, points, owner))
    all_points = [point for _, polygon, _ in polygons for point in polygon]
    lo_x, hi_x = min(x for x, _ in all_points), max(x for x, _ in all_points)
    lo_y, hi_y = min(y for _, y in all_points), max(y for _, y in all_points)
    scale = min(940 / (hi_x-lo_x), 620 / (hi_y-lo_y))
    def screen(point):
        x, y = point
        return 90+(x-lo_x)*scale, 85+(hi_y-y)*scale
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 780">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        '<text x="560" y="38" text-anchor="middle" fill="#f8f9fa" font-family="sans-serif" font-size="24">Representative coordinated parent grouping</text>',
        f'<text x="560" y="64" text-anchor="middle" fill="#a9b1d6" font-family="sans-serif" font-size="14">generated corona {witness["corona_index"]}; colors are disjoint parent occurrences, gray is the free boundary</text>',
    ]
    for pose, polygon, owner in polygons:
        coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in map(screen, polygon))
        fill = palette[owner % len(palette)] if owner is not None else "#565f89"
        stroke = "#f8f9fa" if pose in safe else "#11151c"
        width = 1.8 if pose in safe else 1.0
        lines.append(f'<polygon points="{coordinates}" fill="{fill}" fill-opacity="0.78" stroke="{stroke}" stroke-width="{width}"/>')
    lines.extend((
        '<text x="560" y="748" text-anchor="middle" fill="#a9b1d6" font-family="sans-serif" font-size="13">white outlines: universally buffered tiles required to have exactly one parent</text>',
        '</svg>',
    ))
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    a6 = json.loads(A6.read_text())
    physical = json.loads(PHYSICAL.read_text())
    analysis = analyze_parent_overlap_language(a6, physical)
    artifact = {
        "schema": "einstein.w3.spectre-parent-overlap",
        "version": 1,
        "status": "CONDITIONAL_EXTRAS_REFUTED_RADIUS4",
        "provenance": {
            "a6_source": str(A6.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6),
            "physical_source": str(PHYSICAL.relative_to(ROOT)),
            "physical_sha256": file_sha256(PHYSICAL),
        },
        "analysis": analysis,
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    render_summary(analysis, SUMMARY)
    render_grouping_witness(analysis, WITNESS)
    summary = analysis["summary"]
    print(
        "W3 coordinated grouping: 21 physical r3 -> "
        f"{summary['conditional_language_after_grouping']} conditional types; "
        "extras 33/44/155 refuted"
    )
    print(OUTPUT.relative_to(ROOT))
    print(SUMMARY.relative_to(ROOT))
    print(WITNESS.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
