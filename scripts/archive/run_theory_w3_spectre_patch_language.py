#!/usr/bin/env python
"""Enumerate the ancestry-blind straight-Spectre corona language through r=3."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.theory.spectre_patch_language import analyze_physical_patch_language
from einstein.theory.substitution_certificate import file_sha256
from einstein.funnel.a6_hierarchy import SPECTRE_TILE_BOUNDARY
from einstein.substrate.module12 import apply_sr, madd, to_xy


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/notebook/assets/a6-spectre-results.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
PLOT = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.svg"
GALLERY = ROOT / "docs/notebook/assets/theory-w3-spectre-radius3-extra-survivors.svg"


def render(report, path: Path) -> None:
    radius1 = report["radius1"]["complete_coronas"]
    radius2 = report["radius2"]["surviving_first_coronas"]
    radius3 = report["radius3"]["surviving_first_coronas"]
    observed = report["substitution_control"]["observed_first_coronas"]
    extra = report["substitution_control"]["unobserved_radius3_survivors"]
    values = (
        ("bare r=1", radius1, "#7aa2f7"),
        ("survive r=2", radius2, "#e0af68"),
        ("survive r=3", radius3, "#bb9af7"),
        ("substitution-observed", observed, "#9ece6a"),
    )
    width, height = 1120, 500
    base_y = 370
    scale = 260 / radius1
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        '<text x="560" y="48" text-anchor="middle" fill="#f8f9fa" '
        'font-family="sans-serif" font-size="25">Physical Spectre patch language</text>',
        '<text x="560" y="78" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="15">exact, same-chirality, edge-to-edge; no ancestry in enumeration</text>',
    ]
    for index, (label, value, color) in enumerate(values):
        x = 70 + index * 270
        bar_height = value * scale
        lines.extend((
            f'<rect x="{x}" y="{base_y-bar_height:.2f}" width="160" '
            f'height="{bar_height:.2f}" rx="8" fill="{color}"/>',
            f'<text x="{x+80}" y="{base_y-bar_height-14:.2f}" '
            f'text-anchor="middle" fill="#f8f9fa" font-family="sans-serif" '
            f'font-size="30">{value}</text>',
            f'<text x="{x+80}" y="{base_y+30}" text-anchor="middle" '
            f'fill="#c0caf5" font-family="sans-serif" font-size="17">{label}</text>',
        ))
    lines.extend((
        f'<text x="560" y="440" text-anchor="middle" fill="#f7768e" '
        f'font-family="sans-serif" font-size="17">{extra} radius-three survivors remain outside the observed substitution language; all reach radius four</text>',
        '<text x="560" y="468" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="14">finite contraction, not a whole-plane extension theorem</text>',
        '</svg>',
    ))
    path.write_text("\n".join(lines) + "\n")


def render_survivor_gallery(report, path: Path) -> None:
    indices = report["radius3"]["unobserved_survivor_indices"]
    panels = []
    for index in indices:
        record = report["records"][index]

        def parse(rows):
            return [(s, r, tuple(translation)) for s, r, translation in rows]

        rings = (
            [(0, 0, (0, 0, 0, 0))],
            parse(record["neighbors"]),
            parse(record["third_ring_second_ring_poses"]),
            parse(record["third_ring_extension_poses"]),
        )
        polygons = []
        for ring, poses in enumerate(rings):
            for s, rotation, translation in poses:
                polygons.append((ring, [
                    to_xy(madd(translation, apply_sr(s, rotation, vertex)))
                    for vertex in SPECTRE_TILE_BOUNDARY
                ]))
        panels.append((index, record, polygons))

    panel_width, panel_height = 390, 410
    width, height = panel_width * len(panels), 500
    colors = ("#f7768e", "#7aa2f7", "#e0af68", "#bb9af7")
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        f'<text x="{width/2:.1f}" y="35" text-anchor="middle" fill="#f8f9fa" '
        'font-family="sans-serif" font-size="23">Unobserved radius-three survivors</text>',
        f'<text x="{width/2:.1f}" y="60" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="14">central / first / second / third rings; finite witnesses, not plane tilings</text>',
    ]
    for panel, (index, record, polygons) in enumerate(panels):
        points = [point for _, polygon in polygons for point in polygon]
        lo_x, hi_x = min(x for x, _ in points), max(x for x, _ in points)
        lo_y, hi_y = min(y for _, y in points), max(y for _, y in points)
        scale = min(340 / (hi_x - lo_x), 315 / (hi_y - lo_y))
        offset_x = panel * panel_width + (panel_width - (hi_x - lo_x) * scale) / 2
        offset_y = 88 + (330 - (hi_y - lo_y) * scale) / 2

        def screen(point):
            x, y = point
            return offset_x + (x - lo_x) * scale, offset_y + (hi_y - y) * scale

        for ring, polygon in polygons:
            coordinates = " ".join(
                f"{x:.2f},{y:.2f}" for x, y in map(screen, polygon)
            )
            lines.append(
                f'<polygon points="{coordinates}" fill="{colors[ring]}" '
                'fill-opacity="0.72" stroke="#11151c" stroke-width="1.1"/>'
            )
        center = panel * panel_width + panel_width / 2
        lines.extend((
            f'<text x="{center:.1f}" y="445" text-anchor="middle" fill="#f8f9fa" '
            f'font-family="sans-serif" font-size="18">corona {index}</text>',
            f'<text x="{center:.1f}" y="470" text-anchor="middle" fill="#a9b1d6" '
            f'font-family="sans-serif" font-size="13">r2 completions '
            f'{record["second_ring_total_solutions"]}; compatible parents '
            f'{record["compatible_central_parents"]}</text>',
        ))
    lines.append('</svg>')
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    source = json.loads(SOURCE.read_text())
    analysis = analyze_physical_patch_language(source)
    artifact = {
        "schema": "einstein.w3.spectre-physical-patch-language",
        "version": 1,
        "status": "COMPLETE_RADIUS3_PREFIX",
        "provenance": {
            "a6_source": str(SOURCE.relative_to(ROOT)),
            "a6_sha256": file_sha256(SOURCE),
        },
        "analysis": analysis,
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    render(analysis, PLOT)
    render_survivor_gallery(analysis, GALLERY)
    print(
        "W3 physical language: "
        f"{analysis['radius1']['complete_coronas']} r1 -> "
        f"{analysis['radius2']['surviving_first_coronas']} r2; "
        f"{analysis['radius3']['surviving_first_coronas']} r3; "
        f"{analysis['substitution_control']['observed_first_coronas']} observed, "
        f"{analysis['substitution_control']['unobserved_radius3_survivors']} extra"
    )
    print(OUTPUT.relative_to(ROOT))
    print(PLOT.relative_to(ROOT))
    print(GALLERY.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
