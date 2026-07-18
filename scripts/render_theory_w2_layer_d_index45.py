#!/usr/bin/env python
"""Render the W2.D index-45 quotient-class matrix and signature triples."""

from __future__ import annotations

import json
from pathlib import Path

from render_theory_w2_layer_d import (
    BG, BORDER, COMPAT, GOLD, HOL, MUTED, PANEL, TEXT, W1,
    panel, rect, text,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
INPUT = ASSETS / "theory-w2-layer-d-s3-index45.json"
OUTPUT = ASSETS / "theory-w2-layer-d-index45.svg"


def render(payload):
    rows = payload["finalist"]["by_hnf"]
    width, height = 1400, 1090
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG),
        text(40, 47, "W2.D · index-45 shell and S3 signature triples", 28,
             weight=700),
        text(40, 75, "Finalist, grid-aligned torus quotients · 162 independently replayed proof cores",
             16, MUTED),
    ]

    panel(parts, 40, 100, 1320, 160, "1 · Complete index-45 shell",
          "All 78 HNF lattices are excluded: 69 by short-period families, 9 by nonabelian holonomy.")
    x0, y0, step, side = 100, 184, 29, 19
    for index in range(78):
        fill = W1 if index < 69 else HOL
        parts.append(rect(x0 + (index % 39) * step, y0 + (index // 39) * 31,
                          side, side, fill, "#ffffff22", 0.7, 3))
    parts.extend([
        rect(1035, 239, 14, 14, W1, rx=2),
        text(1057, 251, "69 · period family", 12, MUTED),
        rect(1205, 239, 14, 14, HOL, rx=2),
        text(1227, 251, "9 · Layer D", 12, MUTED),
    ])

    panel(parts, 40, 285, 1320, 535,
          "2 · Complete 9 × 39 strong-S3 quotient matrix",
          "Magenta: all 18 commuting twists UNSAT. Gold outline: deterministic map retained for proof replay.")
    gx, gy, cw, ch, gap = 300, 392, 24, 31, 3
    selected = {tuple(row["hnf"]): min(row["killing_mapping_indices"])
                for row in rows}
    for mapping_index in range(39):
        if mapping_index % 3 == 0:
            parts.append(text(gx + mapping_index * (cw + gap) + cw / 2,
                              gy - 15, mapping_index, 10, MUTED, "middle",
                              family="monospace", rotate=-55))
    for row_index, row in enumerate(rows):
        hnf = tuple(row["hnf"])
        y = gy + row_index * 42
        parts.append(text(274, y + 21, f"{hnf}", 13, TEXT, "end", 600,
                          "monospace"))
        killers = set(row["killing_mapping_indices"])
        for mapping_index in range(39):
            x = gx + mapping_index * (cw + gap)
            parts.append(rect(
                x, y, cw, ch,
                HOL if mapping_index in killers else COMPAT,
                GOLD if mapping_index == selected[hnf] else BORDER,
                3 if mapping_index == selected[hnf] else 1,
                3,
            ))
    parts.extend([
        rect(1030, 785, 15, 15, HOL, rx=2),
        text(1053, 798, "killing map", 13, MUTED),
        rect(1160, 783, 18, 18, "none", GOLD, 3, 2),
        text(1187, 798, "stored proof map", 13, MUTED),
    ])

    panel(parts, 40, 845, 1320, 205, "3 · Three exact map-signature families",
          "Within each triple, all maps kill the same seven HNFs. Columns H1--H9 follow the matrix row order.")
    triples = ((9, 15, 18), (21, 24, 27), (30, 33, 36))
    triple_kills = []
    for triple in triples:
        triple_kills.append({
            tuple(row["hnf"])
            for row in rows
            if triple[0] in row["killing_mapping_indices"]
        })
    sx, sy, sw, sh = 335, 930, 101, 30
    for column, _ in enumerate(rows):
        parts.append(text(sx + column * sw + 45, sy - 11,
                          f"H{column + 1}", 11, MUTED, "middle", 700,
                          family="monospace"))
    for line, (triple, killed) in enumerate(zip(triples, triple_kills)):
        y = sy + line * 38
        parts.append(text(292, y + 20, str(triple), 13, TEXT, "end", 700,
                          "monospace"))
        for column, row in enumerate(rows):
            hnf = tuple(row["hnf"])
            parts.append(rect(sx + column * sw, y, 90, sh,
                              HOL if hnf in killed else COMPAT,
                              BORDER, 1, 4))
            parts.append(text(sx + column * sw + 45, y + 20,
                              "KILL" if hnf in killed else "miss",
                              10, TEXT if hnf in killed else MUTED, "middle",
                              700, "monospace"))

    parts.append(text(700, 1075,
                      "Finite exact pattern—not yet an infinite HNF-family theorem · larger indices remain open",
                      12, GOLD, "middle", 600))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    OUTPUT.write_text(render(json.loads(INPUT.read_text())))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
