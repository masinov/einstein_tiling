#!/usr/bin/env python
"""Render the representative radius-nine L18 contraction frontier."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.substitution import SPECTRE_TILE_BOUNDARY
from einstein.geometry.cyclotomic import apply_sr, madd, to_xy
from einstein.tilings.spectre.patches import IDENTITY, patch_edge_incidence


ROOT = repository_root(Path(__file__))
SOURCE = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.svg"


def pose(row):
    return int(row[0]), int(row[1]), tuple(map(int, row[2]))


def main():
    artifact = json.loads(SOURCE.read_text())
    patch = tuple(pose(row) for row in artifact[
        "representative_radius9_frontier"
    ]["patch"])
    incidence, _ = patch_edge_incidence(patch)
    adjacency = {tile: set() for tile in patch}
    for owners in incidence.values():
        if len(owners) == 2:
            left, right = owners
            adjacency[left].add(right)
            adjacency[right].add(left)
    distance = {IDENTITY: 0}
    queue = deque((IDENTITY,))
    while queue:
        tile = queue.popleft()
        for neighbor in adjacency[tile]:
            if neighbor not in distance:
                distance[neighbor] = distance[tile] + 1
                queue.append(neighbor)

    polygons = []
    for tile in patch:
        s, r, translation = tile
        points = [to_xy(madd(translation, apply_sr(s, r, vertex)))
                  for vertex in SPECTRE_TILE_BOUNDARY]
        polygons.append((tile, points))
    points = [point for _, polygon in polygons for point in polygon]
    lo_x, hi_x = min(x for x, _ in points), max(x for x, _ in points)
    lo_y, hi_y = min(y for _, y in points), max(y for _, y in points)
    scale = min(790 / (hi_x - lo_x), 720 / (hi_y - lo_y))

    def screen(point):
        x, y = point
        return 35 + (x - lo_x) * scale, 80 + (hi_y - y) * scale

    colors = (
        "#f7768e", "#ff9e64", "#e0af68", "#9ece6a", "#73daca",
        "#7dcfff", "#7aa2f7", "#bb9af7", "#c0caf5", "#565f89",
    )
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 850">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        '<text x="580" y="38" text-anchor="middle" fill="#f8f9fa" '
        'font-family="sans-serif" font-size="24">L18 contraction frontier: radius-nine witness</text>',
        '<text x="580" y="63" text-anchor="middle" fill="#a9b1d6" '
        'font-family="sans-serif" font-size="14">296 exact physical Tile(1,1) copies; color is graph radius</text>',
    ]
    for tile, polygon in polygons:
        coordinates = " ".join(
            f"{x:.2f},{y:.2f}" for x, y in map(screen, polygon)
        )
        depth = distance[tile]
        stroke = "#ffffff" if tile == IDENTITY else "#11151c"
        width = 2.2 if tile == IDENTITY else 0.75
        lines.append(
            f'<polygon points="{coordinates}" fill="{colors[depth]}" '
            f'fill-opacity="0.78" stroke="{stroke}" stroke-width="{width}"/>'
        )
    records = artifact["contraction_audit"]["radius_records"][-3:]
    lines.extend((
        '<rect x="865" y="110" width="260" height="250" rx="10" fill="#1a1f2b" stroke="#414868"/>',
        '<text x="995" y="145" text-anchor="middle" fill="#f8f9fa" font-family="sans-serif" font-size="18">non-generated frontier</text>',
    ))
    for index, record in enumerate(records):
        y = 195 + 58 * index
        lines.append(
            f'<text x="900" y="{y}" fill="#a9b1d6" font-family="monospace" font-size="17">r={record["radius"]}</text>'
        )
        lines.append(
            f'<text x="1090" y="{y}" text-anchor="end" fill="#f7768e" font-family="monospace" font-size="20">{record["continued_frontier_patches"]:,}</text>'
        )
    lines.extend((
        '<text x="995" y="410" text-anchor="middle" fill="#e0af68" font-family="sans-serif" font-size="16">unique parent partition: proved</text>',
        '<text x="995" y="440" text-anchor="middle" fill="#f7768e" font-family="sans-serif" font-size="16">contraction closure: open</text>',
        '<text x="995" y="490" text-anchor="middle" fill="#a9b1d6" font-family="sans-serif" font-size="13">finite witness only</text>',
        '<text x="995" y="512" text-anchor="middle" fill="#a9b1d6" font-family="sans-serif" font-size="13">not a plane tiling</text>',
        '</svg>',
    ))
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
