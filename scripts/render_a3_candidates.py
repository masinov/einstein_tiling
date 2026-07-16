#!/usr/bin/env python
"""Render central views of the ten smallest candidates' largest A3 patches."""

from __future__ import annotations

import json
import math
from pathlib import Path

from einstein.e1_candidates import decode_compiled_key
from einstein.funnel.a3_patch import certificate_cells
from einstein.render.svg import hex_to_xy
from einstein.substrate.kitegrid import boundary_cycle, cell_centroid4, norm2

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"
RESULTS = ASSETS / "a3-small-candidate-results.json"
OUTPUT = ASSETS / "a3-small-candidate-patches.svg"

COLORS = (
    "#f2c14e", "#f78154", "#4d9078", "#577590",
    "#9b5de5", "#43aa8b", "#f8961e", "#277da1",
    "#90be6d", "#f94144", "#b5179e", "#00b4d8",
)


def render(payload, display_r2=800):
    columns = 2
    panel_w, panel_h = 480, 390
    margin, title_h = 28, 70
    width = columns * panel_w
    height = math.ceil(len(payload["results"]) / columns) * panel_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    for panel, result in enumerate(payload["results"]):
        column, row = panel % columns, panel // columns
        ox, oy = column * panel_w, row * panel_h
        cert = result["largest_certificate"]
        shape = decode_compiled_key(result["shape"])
        groups = certificate_cells(shape, cert)
        shown_r2 = min(display_r2, cert["r2"])
        selected = [
            (placement[0], group)
            for placement, group in zip(cert["placements"], groups)
            if any(norm2(cell_centroid4(cell)) <= 16 * shown_r2
                   for cell in group)
        ]
        outlines = [
            (op, [hex_to_xy(vertex) for vertex in boundary_cycle(group)])
            for op, group in selected
        ]
        xs = [x for _, outline in outlines for x, _ in outline]
        ys = [y for _, outline in outlines for _, y in outline]
        available_w = panel_w - 2 * margin
        available_h = panel_h - title_h - margin
        patch_w = max(xs) - min(xs)
        patch_h = max(ys) - min(ys)
        scale = min(available_w / patch_w, available_h / patch_h)
        x_shift = ox + (panel_w - patch_w * scale) / 2 - min(xs) * scale
        y_shift = (
            oy + title_h + (available_h - patch_h * scale) / 2
            + max(ys) * scale
        )
        final = result["ladder"][-1]
        status = (
            f"refuted at r²={final['r2']}"
            if final["status"] == "refuted"
            else f"grown through r²={final['r2']}"
        )
        status_color = "#ff6b6b" if final["status"] == "refuted" else "#51cf66"
        parts.extend([
            (
                f'<rect x="{ox + 8}" y="{oy + 8}" '
                f'width="{panel_w - 16}" height="{panel_h - 16}" '
                'rx="10" fill="#1c2430" stroke="#394555"/>'
            ),
            (
                f'<text x="{ox + panel_w / 2}" y="{oy + 30}" '
                'fill="#f8f9fa" font-family="sans-serif" font-size="16" '
                f'font-weight="700" text-anchor="middle">n={result["n"]} '
                f'candidate {result["index"]}</text>'
            ),
            (
                f'<text x="{ox + panel_w / 2}" y="{oy + 50}" '
                f'fill="{status_color}" font-family="sans-serif" '
                f'font-size="12" text-anchor="middle">{status}; '
                f'{cert["tiles"]} tiles</text>'
            ),
            (
                f'<text x="{ox + panel_w / 2}" y="{oy + 65}" '
                'fill="#adb5bd" font-family="sans-serif" font-size="10" '
                f'text-anchor="middle">central r²≤{shown_r2} view · '
                f'{len(selected)} intersecting tiles</text>'
            ),
        ])
        radius = math.sqrt(shown_r2) * scale
        parts.append(
            f'<circle cx="{x_shift:.2f}" cy="{y_shift:.2f}" r="{radius:.2f}" '
            'fill="none" stroke="#ffffff" stroke-opacity="0.18" '
            'stroke-width="1.2" stroke-dasharray="4 4"/>'
        )
        for op, outline in outlines:
            points = " ".join(
                f"{x_shift + x * scale:.2f},{y_shift - y * scale:.2f}"
                for x, y in outline
            )
            parts.append(
                f'<polygon points="{points}" fill="{COLORS[op]}" '
                'fill-opacity="0.82" stroke="#f8f9fa" stroke-width="0.65" '
                'stroke-linejoin="round"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    payload = json.loads(RESULTS.read_text())
    OUTPUT.write_text(render(payload))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
