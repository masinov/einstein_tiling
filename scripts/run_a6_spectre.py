#!/usr/bin/env python
"""Blind A6 v0 calibration against the user-owned Spectre generator.

Discovery reads exact physical tile poses only. Hidden substitution paths are
generated to separate files and opened strictly after the rule is fixed.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from einstein.funnel.a6_hierarchy import (
    SPECTRE_TILE_BOUNDARY,
    cluster_adjacency,
    cover_with_rule,
    discover_composition,
    read_anchor_poses,
    read_hidden_parent_groups,
    recover_order2_recurrence,
    validate_against_hidden,
)
from einstein.substrate.module12 import apply_sr, madd, to_xy

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "vendor" / "spectre" / "spectre-core"
ASSETS = ROOT / "docs" / "notebook" / "assets"
LABELS = ["Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi"]


def _run(binary: str, label: str, level: int, out: Path) -> None:
    subprocess.run(
        [CORE / "target" / "release" / binary, label, str(level), out],
        check=True,
    )


def _template_json(template):
    return [[s, r, list(t)] for s, r, t in template]


def _render_metatiles(full, missing, out: Path) -> None:
    panels = [("full scaffold (9)", full), ("one-child exception (8)", missing)]
    polygons = []
    all_xy = []
    offsets = [0.0, 18.0]
    for panel, ((title, template), dx) in enumerate(zip(panels, offsets)):
        for i, (s, r, t) in enumerate(template):
            points = [
                to_xy(madd(t, apply_sr(s, r, vertex)))
                for vertex in SPECTRE_TILE_BOUNDARY
            ]
            shifted = [(x + dx, y) for x, y in points]
            all_xy.extend(shifted)
            polygons.append((panel, i, shifted))
    lo_x = min(x for x, _ in all_xy) - 1
    hi_x = max(x for x, _ in all_xy) + 1
    lo_y = min(y for _, y in all_xy) - 2
    hi_y = max(y for _, y in all_xy) + 2
    scale = 30
    width, height = (hi_x - lo_x) * scale, (hi_y - lo_y) * scale

    def screen(point):
        x, y = point
        return ((x - lo_x) * scale, (hi_y - y) * scale)

    colors = ["#f2c14e", "#f78154", "#4d9078", "#577590", "#9b5de5"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    for panel, i, points in polygons:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in map(screen, points))
        lines.append(
            f'<polygon points="{coords}" fill="{colors[i % len(colors)]}" '
            'fill-opacity="0.82" stroke="#f8f9fa" stroke-width="1"/>'
        )
    panel_centers = []
    for panel in range(len(panels)):
        panel_points = [
            point for p, _, points in polygons if p == panel for point in points
        ]
        panel_centers.append(
            (min(x for x, _ in panel_points) + max(x for x, _ in panel_points)) / 2
        )
    for (title, _), center in zip(panels, panel_centers):
        x, y = screen((center, hi_y - 0.7))
        lines.append(
            f'<text x="{x:.2f}" y="{y:.2f}" fill="#f8f9fa" '
            f'font-family="sans-serif" font-size="14" text-anchor="middle">{title}</text>'
        )
    lines.append("</svg>")
    out.write_text("\n".join(lines) + "\n")


def main() -> int:
    subprocess.run(["cargo", "build", "--release", "--bins"], cwd=CORE, check=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="a6-spectre-") as raw_tmp:
        tmp = Path(raw_tmp)
        anchors = {}
        hidden_paths = {}
        for level in range(1, 5):
            ap = tmp / f"Delta-n{level}-anchors.csv"
            hp = tmp / f"Delta-n{level}-hierarchy.csv"
            _run("anchors", "Delta", level, ap)
            _run("hierarchy", "Delta", level, hp)
            anchors[level] = read_anchor_poses(ap)
            hidden_paths[level] = hp

        # Training and confirmation are both pose-only. The ancestry files
        # above remain unopened until the rule and partitions are fixed.
        rule, _, diagnostics = discover_composition(
            anchors[3],
            confirmation_poses=anchors[4],
            tile_boundary=SPECTRE_TILE_BOUNDARY,
        )

        levels = {}
        physical_counts = []
        all_exact = True
        for level in range(1, 5):
            cover = cover_with_rule(anchors[level], rule.full, rule.missing)
            hidden = read_hidden_parent_groups(hidden_paths[level], anchors[level])
            validation = validate_against_hidden(cover.groups, hidden)
            all_exact &= cover.n_solutions == 1 and validation["exact"]
            physical_counts.append(len(anchors[level]))
            levels[str(level)] = {
                "physical_tiles": len(anchors[level]),
                "parents": len(cover.groups),
                "full": cover.n_full,
                "missing": cover.n_missing,
                "unique_exact_cover": cover.n_solutions == 1,
                "hidden_validation": validation,
            }

        # Immediate-rule robustness: the same pose-only templates must compose
        # every root label, not just the Delta patch used for discovery.
        roots = {}
        for label in LABELS:
            ap = tmp / f"{label}-n3-anchors.csv"
            _run("anchors", label, 3, ap)
            poses = read_anchor_poses(ap)
            cover = cover_with_rule(poses, rule.full, rule.missing)
            roots[label] = {
                "physical_tiles": len(poses),
                "parents": len(cover.groups),
                "full": cover.n_full,
                "missing": cover.n_missing,
                "unique_exact_cover": cover.n_solutions == 1,
            }
            all_exact &= cover.n_solutions == 1

        recurrence = recover_order2_recurrence(physical_counts)
        full_adj = cluster_adjacency(rule.full, SPECTRE_TILE_BOUNDARY)
        missing_adj = cluster_adjacency(rule.missing, SPECTRE_TILE_BOUNDARY)
        result = {
            "status": "PASS" if all_exact else "FAIL",
            "scope": "A6 v0 immediate composition; recognizability not yet proved",
            "blind_inputs": "exact (s,r,t0..t3) physical poses only; kind ignored",
            "selected_rule": {
                "full": _template_json(rule.full),
                "missing": _template_json(rule.missing),
                "full_adjacency": {
                    "degrees": list(full_adj[0]),
                    "internal_edges": full_adj[1],
                    "exposed_edges": full_adj[2],
                },
                "missing_adjacency": {
                    "degrees": list(missing_adj[0]),
                    "internal_edges": missing_adj[1],
                    "exposed_edges": missing_adj[2],
                },
            },
            "discovery": diagnostics,
            "delta_levels": levels,
            "all_root_labels_level3": roots,
            "physical_tile_counts": physical_counts,
            "recurrence": recurrence,
            "inflation_area": "dominant root 4 + sqrt(15)",
        }
        out_json = ASSETS / "a6-spectre-results.json"
        out_json.write_text(json.dumps(result, indent=2) + "\n")
        out_svg = ASSETS / "a6-spectre-metatiles.svg"
        _render_metatiles(rule.full, rule.missing, out_svg)

    print(
        f"A6 v0: {result['status']} — size {rule.full_size}; "
        f"levels 1–4 hidden recovery exact; recurrence "
        f"T[n+1]={recurrence['a']}T[n] - T[n-1]"
    )
    print(out_json.relative_to(ROOT))
    print(out_svg.relative_to(ROOT))
    return 0 if all_exact else 1


if __name__ == "__main__":
    raise SystemExit(main())
