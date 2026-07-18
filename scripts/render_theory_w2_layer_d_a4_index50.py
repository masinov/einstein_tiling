#!/usr/bin/env python
"""Render the A4 closure of the W2.D index-50 shell."""

from __future__ import annotations

import json
from pathlib import Path

from render_theory_w2_layer_d import (
    BG, BORDER, COMPAT, GOLD, HOL, MUTED, PANEL, TEXT, W1,
    panel, rect, text,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/notebook/assets"
INPUT = ASSETS / "theory-w2-layer-d-a4-index50.json"
OUTPUT = ASSETS / "theory-w2-layer-d-a4-index50.svg"


def render(payload):
    rows = payload["finalist"]["by_hnf"]
    width, height = 1500, 1180
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        rect(0, 0, width, height, BG),
        text(40, 47, "W2.D · A4 closes the index-50 shell", 28, weight=700),
        text(40, 75,
             "A complementary finite quotient turns every former S3 survivor into a certified obstruction",
             16, MUTED),
    ]

    panel(parts, 40, 100, 1420, 165, "1 · Complete index-50 decomposition",
          "All 93 HNFs are assigned to an exact obstruction layer; colors record the first successful test.")
    x0, y0, step, side = 105, 178, 26, 18
    for index in range(93):
        fill = W1 if index < 75 else GOLD if index < 81 else HOL
        parts.append(rect(x0 + (index % 47) * step,
                          y0 + (index // 47) * 31,
                          side, side, fill, "#ffffff22", 0.7, 3))
    legends = ((W1, "75 · W1 period"), (GOLD, "6 · S3"), (HOL, "12 · A4"))
    for column, (fill, label) in enumerate(legends):
        x = 1050 + column * 130
        parts.append(rect(x, 233, 14, 14, fill, rx=2))
        parts.append(text(x + 22, 245, label, 12, MUTED))

    panel(parts, 40, 290, 1420, 500,
          "2 · Expanded 12 × 48 strong-A4 quotient matrix",
          "Magenta: every one of 48 commuting torus twists is UNSAT. Dark cells admit a relaxed model.")
    gx, gy, cw, ch, gap = 280, 390, 21, 24, 3
    for mapping_index in range(48):
        if mapping_index % 2 == 0:
            parts.append(text(gx + mapping_index * (cw + gap) + cw / 2,
                              gy - 14, mapping_index, 9, MUTED, "middle",
                              family="monospace", rotate=-55))
    for row_index, row in enumerate(rows):
        y = gy + row_index * 30
        parts.append(text(250, y + 17, str(tuple(row["hnf"])), 12,
                          TEXT, "end", 600, "monospace"))
        killers = set(row["killing_mapping_indices"])
        for mapping_index in range(48):
            parts.append(rect(gx + mapping_index * (cw + gap), y, cw, ch,
                              HOL if mapping_index in killers else COMPAT,
                              BORDER, 1, 3))
    parts.extend([
        rect(1115, 755, 15, 15, HOL, rx=2),
        text(1138, 768, "obstructed", 13, MUTED),
        rect(1260, 755, 15, 15, COMPAT, rx=2),
        text(1283, 768, "not obstructed", 13, MUTED),
    ])

    panel(parts, 40, 815, 690, 300, "3 · Why A4 adds information",
          "The strong kernels retain different quotients of the six boundary generators.")
    parts.extend([
        rect(85, 900, 260, 120, PANEL, GOLD, 2, 10),
        text(215, 935, "S3 target", 18, GOLD, "middle", 700),
        text(215, 970, "kernel A3", 15, TEXT, "middle"),
        text(215, 997, "residual quotient C2", 14, MUTED, "middle"),
        text(380, 963, "+", 32, MUTED, "middle", 700),
        rect(415, 900, 260, 120, PANEL, HOL, 2, 10),
        text(545, 935, "A4 target", 18, HOL, "middle", 700),
        text(545, 970, "kernel V4", 15, TEXT, "middle"),
        text(545, 997, "residual quotient C3", 14, MUTED, "middle"),
        text(380, 1063, "Neither target subsumes the other; together they separate the shell.",
             13, MUTED, "middle"),
    ])

    panel(parts, 755, 815, 705, 300, "4 · Certificate boundary",
          "Search results become theorems only after each generated core passes independent DRAT replay.")
    stages = (
        ("SEARCH", "48 pair orbits", COMPAT),
        ("COVER", "map 7 kills all 12 HNFs", GOLD),
        ("PROOF", "576/576 cold replay", HOL),
    )
    for index, (title, subtitle, fill) in enumerate(stages):
        x = 795 + index * 215
        parts.append(rect(x, 905, 180, 110, PANEL, fill, 2, 9))
        parts.append(text(x + 90, 940, title, 16, fill, "middle", 700))
        parts.append(text(x + 90, 972, subtitle, 12, MUTED, "middle"))
        if index < 2:
            parts.append(text(x + 197, 967, "→", 25, MUTED, "middle"))
    parts.append(text(1107, 1063,
                      "Certified prefix promoted: 45 → 50",
                      14, GOLD, "middle", 600))

    parts.append(text(750, 1152,
                      "Finite-quotient obstruction · exact torus logic · no claim of planar tiling existence",
                      13, MUTED, "middle"))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    OUTPUT.write_text(render(json.loads(INPUT.read_text())))
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
