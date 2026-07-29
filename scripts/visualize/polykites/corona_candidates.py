#!/usr/bin/env python
"""Render the smallest blind depth-3 A2 survivors, labelling known shapes.

Writes:
  docs/notebook/assets/a2-depth3-small-candidates.svg
"""

from __future__ import annotations

from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import (
    TURTLE_KEY,
    known_polykite_name,
    novel_smallest_depth3_candidates,
    smallest_depth3_candidates,
    unregistered_smallest_depth3_candidates,
)
from einstein.visualization.kite_svg import hex_to_xy
from einstein.geometry.kite_grid import cell_vertices

ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs" / "notebook" / "assets"


def render(rows):
    columns = 2
    panel_w, panel_h = 340, 250
    margin, title_h = 24, 60
    width = columns * panel_w
    height = ((len(rows) + columns - 1) // columns) * panel_h
    colors = [
        "#f2c14e", "#f78154", "#4d9078", "#577590",
        "#9b5de5", "#43aa8b",
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    for index, (n, local_index, key, cells) in enumerate(rows):
        known_name = known_polykite_name(key)
        known_suffix = f" · known {known_name.title()}" if known_name else ""
        column, line = index % columns, index // columns
        ox, oy = column * panel_w, line * panel_h
        polygons = [
            [hex_to_xy(vertex) for vertex in cell_vertices(cell)]
            for cell in cells
        ]
        xs = [x for polygon in polygons for x, _ in polygon]
        ys = [y for polygon in polygons for _, y in polygon]
        shape_w = max(xs) - min(xs)
        shape_h = max(ys) - min(ys)
        available_w = panel_w - 2 * margin
        available_h = panel_h - title_h - margin
        scale = min(
            available_w / max(shape_w, 1),
            available_h / max(shape_h, 1),
        )
        x_shift = ox + (panel_w - shape_w * scale) / 2 - min(xs) * scale
        y_shift = (
            oy + title_h + (available_h - shape_h * scale) / 2
            + max(ys) * scale
        )
        parts.extend([
            (
                f'<rect x="{ox + 8}" y="{oy + 8}" '
                f'width="{panel_w - 16}" height="{panel_h - 16}" '
                'rx="10" fill="#1c2430" stroke="#394555"/>'
            ),
            (
                f'<text x="{ox + panel_w / 2}" y="{oy + 31}" '
                'fill="#f8f9fa" font-family="sans-serif" font-size="16" '
                f'font-weight="700" text-anchor="middle">n={n} candidate '
                f'{local_index}{known_suffix}</text>'
            ),
            (
                f'<text x="{ox + panel_w / 2}" y="{oy + 50}" '
                'fill="#adb5bd" font-family="monospace" font-size="10" '
                f'text-anchor="middle">Hc ≥ 3 · {key[:16]}…</text>'
            ),
        ])
        for cell, polygon in zip(cells, polygons):
            points = " ".join(
                f"{x_shift + x * scale:.2f},{y_shift - y * scale:.2f}"
                for x, y in polygon
            )
            parts.append(
                f'<polygon points="{points}" fill="{colors[cell[2]]}" '
                'fill-opacity="0.88" stroke="#f8f9fa" stroke-width="1.4" '
                'stroke-linejoin="round"/>'
            )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    rows = list(smallest_depth3_candidates())
    assert len(rows) == 10
    ASSETS.mkdir(parents=True, exist_ok=True)
    output = ASSETS / "a2-depth3-small-candidates.svg"
    output.write_text(render(rows))
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
