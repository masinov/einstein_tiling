"""Minimal SVG rendering of kite-grid patches for human inspection.

The program (docs/program, section 10) requires every anomaly to ship as a
visual artifact -- trained human eyes are a detection channel, not decoration.
Floating point appears here only, at output time; all upstream geometry is
exact.
"""

from __future__ import annotations

import math

from einstein.geometry.kite_grid import cell_vertices

SQRT3_2 = math.sqrt(3) / 2


def hex_to_xy(p: tuple[int, int]) -> tuple[float, float]:
    x, y = p
    return (x + y / 2, y * SQRT3_2)


def cells_to_svg(cells, scale: float = 40.0, fill: str = "#7aa6c2",
                 stroke: str = "#1c2b36") -> str:
    polys = [[hex_to_xy(v) for v in cell_vertices(c)] for c in cells]
    xs = [x for poly in polys for x, _ in poly]
    ys = [y for poly in polys for _, y in poly]
    pad = 0.5
    x0, y0 = min(xs) - pad, min(ys) - pad
    w = (max(xs) - min(xs) + 2 * pad) * scale
    h = (max(ys) - min(ys) + 2 * pad) * scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.2f} {h:.2f}">'
    ]
    for poly in polys:
        pts = " ".join(
            f"{(x - x0) * scale:.2f},{h - (y - y0) * scale:.2f}" for x, y in poly
        )
        parts.append(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{scale * 0.04:.2f}" stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def groups_to_svg(groups, fills, scale: float = 40.0,
                  stroke: str = "#1c2b36") -> str:
    """Render a list of cell groups (e.g. one group per tile placement),
    each filled with fills[i % len(fills)].  Outlines only the group
    boundary, so individual tiles read as tiles."""
    from einstein.geometry.kite_grid import boundary_cycle

    outlines = [[hex_to_xy(v) for v in boundary_cycle(g)] for g in groups]
    xs = [x for o in outlines for x, _ in o]
    ys = [y for o in outlines for _, y in o]
    pad = 0.5
    x0, y0 = min(xs) - pad, min(ys) - pad
    w = (max(xs) - min(xs) + 2 * pad) * scale
    h = (max(ys) - min(ys) + 2 * pad) * scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.2f} {h:.2f}">'
    ]
    for i, o in enumerate(outlines):
        pts = " ".join(
            f"{(x - x0) * scale:.2f},{h - (y - y0) * scale:.2f}" for x, y in o
        )
        parts.append(
            f'<polygon points="{pts}" fill="{fills[i % len(fills)]}" '
            f'stroke="{stroke}" stroke-width="{scale * 0.04:.2f}" '
            f'stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def save_svg(cells, path: str, **kw) -> None:
    with open(path, "w") as f:
        f.write(cells_to_svg(cells, **kw))
