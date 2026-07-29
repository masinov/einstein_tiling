#!/usr/bin/env python
"""Render a review figure for the W2.D index-40 holonomy result."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.holonomy.constraints import commuting_s3_pairs
from einstein.visualization.svg_primitives import (
    BG, BORDER, COMPAT, GOLD, HOL, MUTED, PANEL, TEXT, W1,
    panel, rect, text,
)


ROOT = repository_root(Path(__file__))
ASSETS = ROOT / "docs/notebook/assets"
INPUT = ASSETS / "theory-w2-layer-d-s3-classes.json"
OUTPUT = ASSETS / "theory-w2-layer-d-index40.svg"

def render(payload):
    rows = payload["finalist"]["by_hnf"]
    width, height = 1400, 930
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG),
        text(40, 47, "W2.D · nonabelian torus-holonomy certificate", 28,
             weight=700),
        text(40, 75, "Finalist, grid-aligned HNF quotients at index 40", 16,
             MUTED),
    ]

    # Panel 1: all 90 HNFs at index 40.
    panel(
        parts, 40, 100, 1320, 190,
        "1 · Complete index-40 quotient shell",
        "Each square is one HNF lattice. All 90 are excluded, by two independent certificate classes.",
    )
    x0, y0, step, side = 92, 183, 26, 18
    for index in range(90):
        column, line = index % 45, index // 45
        fill = W1 if index < 87 else HOL
        parts.append(rect(x0 + column * step, y0 + line * 31, side, side,
                          fill, "#ffffff22", 0.7, 3))
    parts.extend([
        rect(1040, 244, 16, 16, W1, rx=2),
        text(1064, 258, "87 · short-period family", 13, MUTED),
        rect(1235, 244, 16, 16, HOL, rx=2),
        text(1259, 258, "3 · Layer D", 13, MUTED),
    ])

    # Panel 2: 39 quotient maps by 3 surviving HNFs.
    panel(
        parts, 40, 315, 1320, 300,
        "2 · Exhaustive strong S3 boundary-quotient classes",
        "Magenta means that this quotient map obstructs all 18 commuting twists. Gold outlines mark the stored proof maps.",
    )
    gx, gy, cell_w, cell_h, gap = 302, 425, 24, 42, 3
    selected = {tuple(rows[0]["hnf"]): 21,
                tuple(rows[1]["hnf"]): 9,
                tuple(rows[2]["hnf"]): 9}
    for mapping_index in range(39):
        if mapping_index % 3 == 0:
            parts.append(text(
                gx + mapping_index * (cell_w + gap) + cell_w / 2,
                gy - 16,
                mapping_index,
                10,
                MUTED,
                "middle",
                family="monospace",
                rotate=-55,
            ))
    for row_index, row in enumerate(rows):
        hnf = tuple(row["hnf"])
        y = gy + row_index * 57
        parts.append(text(275, y + 27, f"HNF {hnf}", 14, TEXT, "end",
                          600, "monospace"))
        killers = set(row["killing_mapping_indices"])
        for mapping_index in range(39):
            x = gx + mapping_index * (cell_w + gap)
            fill = HOL if mapping_index in killers else COMPAT
            stroke = GOLD if mapping_index == selected[hnf] else BORDER
            stroke_width = 3 if mapping_index == selected[hnf] else 1
            parts.append(rect(x, y, cell_w, cell_h, fill, stroke,
                              stroke_width, 3))
    parts.extend([
        rect(1012, 387, 15, 15, HOL, rx=2),
        text(1035, 400, "6 killing classes per HNF", 13, MUTED),
        rect(1215, 385, 18, 18, "none", GOLD, 3, 2),
        text(1242, 400, "proof map", 13, MUTED),
    ])

    # Panel 3: the 18 commuting twist choices for a representative proof map.
    panel(
        parts, 40, 640, 650, 250,
        "3 · Representative proof bundle",
        "HNF (10,3,4), quotient class 21 · every admissible twist is UNSAT",
    )
    labels = ("e", "(12)", "(01)", "(012)", "(021)", "(02)")
    pairs = set(commuting_s3_pairs())
    perms = tuple(sorted({value for pair in pairs for value in pair}))
    tx, ty, tw, th = 232, 720, 49, 23
    for index, label in enumerate(labels):
        parts.append(text(tx + index * tw + 19, ty - 10, label, 10, MUTED,
                          "middle", family="monospace"))
        parts.append(text(tx - 12, ty + index * th + 16, label, 10, MUTED,
                          "end", family="monospace"))
    for left_index, left in enumerate(perms):
        for right_index, right in enumerate(perms):
            commuting = (left, right) in pairs
            x, y = tx + right_index * tw, ty + left_index * th
            parts.append(rect(x, y, 41, 18, HOL if commuting else "#252b33",
                              BORDER, 0.7, 2))
            parts.append(text(x + 20.5, y + 13, "U" if commuting else "×",
                              10, TEXT if commuting else "#59636f", "middle",
                              700, "monospace"))
    parts.append(text(553, 866, "18 U = independently verified UNSAT cores",
                      12, MUTED, "middle"))

    # Panel 4: logical reading of the result.
    panel(
        parts, 715, 640, 645, 250,
        "4 · How to read the certificate",
        "The holonomy constraint adds information beyond placement coverage.",
    )
    bx, by, bw, bh = 750, 728, 165, 62
    parts.append(rect(bx, by, bw, bh, "#203142", W1, 2, 8))
    parts.append(text(bx + bw / 2, by + 25, "At-least cover", 15, TEXT,
                      "middle", 700))
    parts.append(text(bx + bw / 2, by + 47, "SAT", 16, "#78c6f0",
                      "middle", 700, "monospace"))
    parts.append(text(947, by - 10, "+ boundary holonomy", 11, MUTED,
                      "middle"))
    parts.append(text(947, by + 39, "→", 24, TEXT, "middle"))
    parts.append(rect(975, by, bw, bh, "#3b2042", HOL, 2, 8))
    parts.append(text(975 + bw / 2, by + 25, "All 18 twists", 15, TEXT,
                      "middle", 700))
    parts.append(text(975 + bw / 2, by + 47, "UNSAT", 16, "#ef9cff",
                      "middle", 700, "monospace"))
    parts.append(text(1170, by + 38, "⇒", 25, TEXT, "middle"))
    parts.append(rect(1200, by, 125, bh, "#3b2042", HOL, 2, 8))
    parts.append(text(1262.5, by + 25, "No exact", 14, TEXT, "middle", 700))
    parts.append(text(1262.5, by + 47, "HNF cover", 14, TEXT, "middle", 700))
    parts.append(text(1038, 847,
                      "This visualizes an exclusion—not a tiling. Larger indices remain open.",
                      13, GOLD, "middle", 600))

    parts.append(text(700, 915,
                      "Source: theory-w2-layer-d-s3-classes.json · 54 stored CNF/DRAT cores",
                      12, MUTED, "middle", family="monospace"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    payload = json.loads(INPUT.read_text())
    OUTPUT.write_text(render(payload))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
