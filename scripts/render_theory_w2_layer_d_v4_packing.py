#!/usr/bin/env python
"""Render the representative six-kite collision used by the packing gate."""

from pathlib import Path

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.periodic_quotients import lattice_to_cell
from einstein.visualization.kite_svg import hex_to_xy
from einstein.geometry.kite_grid import boundary_cycle, cell_vertices
from einstein.holonomy.alternating4.packing import placement_lattice_cells


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-packing-overlap6.svg"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    shape = decode_compiled_key(KEY)
    left = placement_lattice_cells(shape, (3, 0, 0))
    right = placement_lattice_cells(shape, (5, 0, 1))
    overlap = left & right
    left_hex = {lattice_to_cell(cell) for cell in left}
    right_hex = {lattice_to_cell(cell) for cell in right}
    all_hex = left_hex | right_hex
    polygons = {
        cell: tuple(hex_to_xy(vertex) for vertex in cell_vertices(cell))
        for cell in all_hex
    }
    outlines = [
        tuple(hex_to_xy(vertex) for vertex in boundary_cycle(cells))
        for cells in (left_hex, right_hex)
    ]
    xs = [x for polygon in polygons.values() for x, _ in polygon]
    ys = [y for polygon in polygons.values() for _, y in polygon]
    scale, pad = 48.0, 0.7
    x0, y0 = min(xs) - pad, min(ys) - pad
    geometry_width = (max(xs) - min(xs) + 2 * pad) * scale
    geometry_height = (max(ys) - min(ys) + 2 * pad) * scale
    width = max(620.0, geometry_width)
    height = geometry_height + 125.0
    x_shift = (width - geometry_width) / 2.0

    def point(value):
        x, y = value
        return f"{x_shift+(x-x0)*scale:.2f},{geometry_height-(y-y0)*scale:.2f}"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.2f} {height:.2f}">',
        '<rect width="100%" height="100%" fill="#fbfaf7"/>',
    ]
    overlap_hex = {lattice_to_cell(cell) for cell in overlap}
    for cell, polygon in sorted(polygons.items()):
        if cell in overlap_hex:
            fill = "#d1495b"
        elif cell in left_hex:
            fill = "#6baed6"
        else:
            fill = "#f2b134"
        parts.append(
            f'<polygon points="{" ".join(map(point, polygon))}" fill="{fill}" '
            'stroke="#ffffff" stroke-width="1.4"/>'
        )
    for outline, stroke in zip(outlines, ("#185a7d", "#9a6500")):
        parts.append(
            f'<polygon points="{" ".join(map(point, outline))}" fill="none" '
            f'stroke="{stroke}" stroke-width="3.2" stroke-linejoin="round"/>'
        )
    baseline = geometry_height + 25
    parts.extend([
        f'<rect x="18" y="{baseline-12}" width="18" height="18" fill="#6baed6"/>',
        f'<text x="43" y="{baseline+3}" font-family="sans-serif" font-size="16">placement (3,0,0)</text>',
        f'<rect x="18" y="{baseline+18}" width="18" height="18" fill="#f2b134"/>',
        f'<text x="43" y="{baseline+33}" font-family="sans-serif" font-size="16">placement (5,0,1)</text>',
        f'<rect x="18" y="{baseline+48}" width="18" height="18" fill="#d1495b"/>',
        f'<text x="43" y="{baseline+63}" font-family="sans-serif" font-size="16">six shared kites; entire D6 orbit forbidden</text>',
        '</svg>',
    ])
    OUT.write_text("\n".join(parts) + "\n")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
