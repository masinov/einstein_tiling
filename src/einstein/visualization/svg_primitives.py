"""Small dependency-free SVG primitives shared by report renderers."""

from __future__ import annotations

import html


BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#f0f6fc"
MUTED = "#9da7b3"
W1 = "#3b82b8"
HOL = "#d05ce3"
COMPAT = "#3a424d"
GOLD = "#f2c14e"


def text(
    x,
    y,
    value,
    size=18,
    fill=TEXT,
    anchor="start",
    weight=400,
    family="sans-serif",
    rotate=None,
):
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate else ""
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"'
        f'{transform}>{html.escape(str(value))}</text>'
    )


def rect(x, y, width, height, fill, stroke="none", stroke_width=1, rx=0):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'rx="{rx}"/>'
    )


def panel(parts, x, y, width, height, title_value, subtitle=None):
    parts.append(rect(x, y, width, height, PANEL, BORDER, 1.5, 12))
    parts.append(text(x + 24, y + 34, title_value, 20, weight=700))
    if subtitle:
        parts.append(text(x + 24, y + 58, subtitle, 13, MUTED))
