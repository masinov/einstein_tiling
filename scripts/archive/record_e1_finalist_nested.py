#!/usr/bin/env python
"""Record and verify the executed nested-core audit for the E1 finalist.

The expensive SAT extensions are supplied as generated certificates. This
script independently verifies them and proves the required inner placements
are literal subsets of each larger patch.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.patches import (
    certificate_cells,
    verify_patch_certificate,
)
from einstein.analysis.diffraction import (
    class_power_sum,
    detect_peaks,
    fingerprint,
)
from einstein.visualization.kite_svg import hex_to_xy
from einstein.geometry.kite_grid import boundary_cycle, cell_centroid4, norm2

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "docs/notebook/assets"
OUTPUT = ASSETS / "e1-finalist-nested.json"
SVG = ASSETS / "e1-finalist-nested-cores.svg"


def frozen(shape, certificate, cutoff_r2):
    groups = certificate_cells(shape, certificate)
    return [
        placement
        for placement, group in zip(certificate["placements"], groups)
        if max(norm2(cell_centroid4(cell)) for cell in group)
        <= 16 * cutoff_r2
    ]


def diffraction(certificate):
    by_op = {}
    for op, tx, ty in certificate["placements"]:
        by_op.setdefault(op, []).append(hex_to_xy((tx, ty)))
    classes = [points for points in by_op.values() if len(points) >= 8]
    rng = random.Random(41_000)
    radius = math.sqrt(certificate["r2"])
    null = []
    for points in classes:
        random_points = []
        for _ in points:
            r = radius * math.sqrt(rng.random())
            angle = 2 * math.pi * rng.random()
            random_points.append((r * math.cos(angle), r * math.sin(angle)))
        null.append(random_points)
    power, dk, k0 = class_power_sum(null, grid=2048)
    peaks = detect_peaks(power, dk, k0, floor=1e-12, max_peaks=5)
    floor = 5 * (peaks[0][2] if peaks else 1e-12)
    return {
        "floor": floor,
        "result": fingerprint(classes=classes, grid=2048, floor=floor),
    }


def render_panel(parts, shape, certificate, preserved, panel_index, label):
    panel = 600
    ox = panel_index * panel
    groups = certificate_cells(shape, certificate)
    outlines = [
        [hex_to_xy(vertex) for vertex in boundary_cycle(group)]
        for group in groups
    ]
    xs = [x for outline in outlines for x, _ in outline]
    ys = [y for outline in outlines for _, y in outline]
    margin, title = 18, 55
    scale = min(
        (panel - 2 * margin) / (max(xs) - min(xs)),
        (panel - title - 2 * margin) / (max(ys) - min(ys)),
    )
    x_shift = ox + (panel - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    y_shift = title + margin + (
        panel - title - 2 * margin - (max(ys) - min(ys)) * scale
    ) / 2 + max(ys) * scale
    parts.extend([
        (
            f'<text x="{ox + panel / 2}" y="24" fill="#f8f9fa" '
            'font-family="sans-serif" font-size="17" font-weight="700" '
            f'text-anchor="middle">{label}</text>'
        ),
        (
            f'<text x="{ox + panel / 2}" y="44" fill="#f8f9fa" '
            'font-family="sans-serif" font-size="13" text-anchor="middle">'
            f'{certificate["tiles"]} tiles · green = frozen from prior scale'
            '</text>'
        ),
    ])
    preserved = {tuple(row) for row in preserved}
    for placement, outline in zip(certificate["placements"], outlines):
        points = " ".join(
            f"{x_shift + x * scale:.2f},{y_shift - y * scale:.2f}"
            for x, y in outline
        )
        keep = tuple(placement) in preserved
        parts.append(
            f'<polygon points="{points}" '
            f'fill="{"#51cf66" if keep else "#577590"}" '
            f'fill-opacity="{0.95 if keep else 0.58}" '
            'stroke="#f8f9fa" stroke-width="0.18" stroke-linejoin="round"/>'
        )


def render_nested(shape, outer_50000, outer_100000,
                  first_frozen, second_frozen):
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    render_panel(
        parts, shape, outer_50000, first_frozen, 0,
        'nested step 1 · outer r²=50,000',
    )
    render_panel(
        parts, shape, outer_100000, second_frozen, 1,
        'nested step 2 · outer r²=100,000',
    )
    parts.append('</svg>')
    SVG.write_text("\n".join(parts) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outer_50000", type=Path)
    parser.add_argument("outer_100000", type=Path)
    args = parser.parse_args()

    robustness = json.loads(
        (ASSETS / "e1-finalist-robustness.json").read_text()
    )
    base = next(
        row["certificate"] for row in robustness["results"]
        if row["phase_seed"] == 1
    )
    key = robustness["candidate"]["shape"]
    shape = decode_compiled_key(key)
    outer_50000 = json.loads(args.outer_50000.read_text())
    outer_100000 = json.loads(args.outer_100000.read_text())
    for certificate in (base, outer_50000, outer_100000):
        assert verify_patch_certificate(shape, certificate)

    first_frozen = frozen(shape, base, 9_000)
    second_frozen = frozen(shape, outer_50000, 30_000)
    assert {tuple(row) for row in first_frozen} <= {
        tuple(row) for row in outer_50000["placements"]
    }
    assert {tuple(row) for row in second_frozen} <= {
        tuple(row) for row in outer_100000["placements"]
    }

    payload = {
        "kind": "nested-core-extension-audit",
        "candidate": robustness["candidate"],
        "full_crown_extension": {
            "from_r2": 12_800,
            "to_r2": 16_000,
            "patches_tested": 5,
            "refuted": 5,
            "unknown": 0,
        },
        "first_collar_profiles": [
            {"patch": "production", "pass_cutoff_r2": 10_000,
             "fail_cutoff_r2": 10_250},
            {"patch": "phase-1", "pass_cutoff_r2": 9_000,
             "fail_cutoff_r2": 10_000},
            {"patch": "phase-2", "pass_cutoff_r2": 5_000,
             "fail_cutoff_r2": 6_400},
            {"patch": "phase-3", "pass_cutoff_r2": 9_000,
             "fail_cutoff_r2": 10_000},
            {"patch": "phase-4", "pass_cutoff_r2": 5_000,
             "fail_cutoff_r2": 6_400},
        ],
        "nested_chain": [
            {
                "source_r2": 12_800,
                "frozen_cutoff_r2": 9_000,
                "frozen_placements": len(first_frozen),
                "target_r2": 50_000,
                "target_tiles": outer_50000["tiles"],
                "certificate": outer_50000,
            },
            {
                "source_r2": 50_000,
                "frozen_cutoff_r2": 30_000,
                "frozen_placements": len(second_frozen),
                "target_r2": 100_000,
                "target_tiles": outer_100000["tiles"],
                "certificate": outer_100000,
            },
        ],
        "second_collar_profile": {
            "full_crown_to_r2_60000": "refuted",
            "target_r2": 100_000,
            "pass_cutoff_r2": 30_000,
            "fail_cutoff_r2": 35_000,
        },
        "nested_outer_diffraction": diffraction(outer_100000),
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    render_nested(
        shape, outer_50000, outer_100000, first_frozen, second_frozen
    )
    print(OUTPUT.relative_to(ROOT))
    print(SVG.relative_to(ROOT))


if __name__ == "__main__":
    main()
