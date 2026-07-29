#!/usr/bin/env python
"""Render the symmetry-reduced W2.D index-50 result and S3 saturation."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.holonomy.symmetry import hnf_d6_image, orbit
from render_theory_w2_layer_d import (
    BG, BORDER, COMPAT, GOLD, HOL, MUTED, PANEL, TEXT, W1,
    panel, rect, text,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
INPUT = ASSETS / "theory-w2-layer-d-s3-index50.json"
OUTPUT = ASSETS / "theory-w2-layer-d-index50.svg"


def render(payload):
    rows = payload["finalist"]["by_hnf"]
    hnfs = tuple(tuple(row["hnf"]) for row in rows)
    hnf_orbits = orbit(hnfs, hnf_d6_image)
    width, height = 1500, 1210
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG),
        text(40, 47, "W2.D · index-50 symmetry reduction and S3 saturation", 28,
             weight=700),
        text(40, 75,
             "Finalist, grid-aligned torus quotients · 702 logical pairs from 81 exact D6 representatives",
             16, MUTED),
    ]

    panel(parts, 40, 100, 1420, 155, "1 · Index-50 shell",
          "75 HNFs fall to W1 period families; Layer D kills 6; 12 survive every strong S3 map.")
    x0, y0, step, side = 105, 178, 26, 18
    for index in range(93):
        fill = W1 if index < 75 else HOL if index < 81 else COMPAT
        parts.append(rect(x0 + (index % 47) * step,
                          y0 + (index // 47) * 30,
                          side, side, fill, "#ffffff22", 0.7, 3))
    parts.extend([
        rect(1080, 229, 14, 14, W1, rx=2),
        text(1102, 241, "75 · period", 12, MUTED),
        rect(1200, 229, 14, 14, HOL, rx=2),
        text(1222, 241, "6 · S3 kill", 12, MUTED),
        rect(1320, 229, 14, 14, COMPAT, rx=2),
        text(1342, 241, "12 · survive", 12, MUTED),
    ])

    panel(parts, 40, 280, 1420, 650,
          "2 · Expanded 18 × 39 strong-S3 quotient matrix",
          "Magenta: all 18 commuting twists UNSAT. Dark cells: a relaxed model exists; they are not tilings.")
    gx, gy, cw, ch, gap = 335, 380, 25, 23, 3
    for mapping_index in range(39):
        if mapping_index % 3 == 0:
            parts.append(text(gx + mapping_index * (cw + gap) + cw / 2,
                              gy - 15, mapping_index, 10, MUTED, "middle",
                              family="monospace", rotate=-55))
    for row_index, row in enumerate(rows):
        hnf = tuple(row["hnf"])
        y = gy + row_index * 28
        parts.append(text(307, y + 17, f"{hnf}", 12, TEXT, "end", 600,
                          "monospace"))
        killers = set(row["killing_mapping_indices"])
        for mapping_index in range(39):
            parts.append(rect(
                gx + mapping_index * (cw + gap), y, cw, ch,
                HOL if mapping_index in killers else COMPAT,
                BORDER, 1, 3,
            ))
    parts.extend([
        rect(1120, 899, 15, 15, HOL, rx=2),
        text(1143, 912, "obstructed", 13, MUTED),
        rect(1260, 899, 15, 15, COMPAT, rx=2),
        text(1283, 912, "not obstructed", 13, MUTED),
    ])

    panel(parts, 40, 955, 1420, 205, "3 · Three HNF symmetry orbits",
          "Only orbit C is excluded. Orbits A and B are the exact S3 saturation frontier.")
    labels = ("A · survives", "B · survives", "C · excluded")
    for column, (label, members) in enumerate(zip(labels, hnf_orbits)):
        x = 85 + column * 465
        killed = all(
            next(row for row in rows if tuple(row["hnf"]) == hnf)["killing_mapping_indices"]
            for hnf in members
        )
        parts.append(rect(x, 1025, 420, 102,
                          "#35224b" if killed else PANEL,
                          HOL if killed else BORDER, 2, 8))
        parts.append(text(x + 18, 1052, label, 15,
                          HOL if killed else TEXT, weight=700))
        for line in range(2):
            chunk = members[line * 3:(line + 1) * 3]
            parts.append(text(x + 18, 1080 + line * 25,
                              "  ".join(map(str, chunk)), 11, MUTED,
                              family="monospace"))

    parts.append(text(
        750, 1190,
        "Mixed finite result · complete certified prefix remains index 45 · stronger target required",
        13, GOLD, "middle", 600,
    ))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    OUTPUT.write_text(render(json.loads(INPUT.read_text())))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
