#!/usr/bin/env python
"""Blind A6 v1 calibration against the user-owned Spectre generator.

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
    collar_label_validation,
    collared_composition_sat_certificate,
    collared_substitution_rules,
    cluster_adjacency,
    contracted_adjacency,
    contract_level,
    cover_with_rule,
    discover_composition,
    enumerate_composition_candidates,
    oriented_collar_colors,
    physical_edge_contacts,
    physical_composition_sat_certificate,
    read_anchor_poses,
    read_hidden_node_labels,
    read_hidden_parent_groups,
    raw_hierarchy_level,
    recover_order2_recurrence,
    recover_recursive_hierarchy,
    validate_against_hidden,
)
from einstein.substrate.module12 import apply_sr, madd, to_xy

ROOT = Path(__file__).resolve().parent.parent.parent
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


def _rule_json(rule):
    return {
        "full": _template_json(rule.full),
        "missing": _template_json(rule.missing),
        "full_size": rule.full_size,
        "proposal_frequency": rule.proposal_frequency,
    }


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
        for level in range(1, 6):
            ap = tmp / f"Delta-n{level}-anchors.csv"
            hp = tmp / f"Delta-n{level}-hierarchy.csv"
            _run("anchors", "Delta", level, ap)
            _run("hierarchy", "Delta", level, hp)
            anchors[level] = read_anchor_poses(ap)
            hidden_paths[level] = hp

        # Training and confirmation are both pose-only. The ancestry files
        # above remain unopened until the rule and partitions are fixed.
        ranked_rule, _, diagnostics = discover_composition(
            anchors[3],
            confirmation_poses=anchors[4],
            tile_boundary=SPECTRE_TILE_BOUNDARY,
        )
        phase_candidates = enumerate_composition_candidates(
            anchors[3], confirmation_poses=anchors[4]
        )
        phase_results = []
        recursive_survivors = []
        for candidate, _ in phase_candidates:
            try:
                candidate_recursive = recover_recursive_hierarchy(
                    anchors[4],
                    anchors[5],
                    candidate,
                    SPECTRE_TILE_BOUNDARY,
                )
            except ValueError as exc:
                phase_results.append({
                    "rule": _rule_json(candidate),
                    "missing_adjacency": {
                        "internal_edges": cluster_adjacency(
                            candidate.missing, SPECTRE_TILE_BOUNDARY
                        )[1],
                        "exposed_edges": cluster_adjacency(
                            candidate.missing, SPECTRE_TILE_BOUNDARY
                        )[2],
                    },
                    "recursive_closure": False,
                    "failure": str(exc),
                })
            else:
                recursive_survivors.append((candidate, candidate_recursive))
                phase_results.append({
                    "rule": _rule_json(candidate),
                    "missing_adjacency": {
                        "internal_edges": cluster_adjacency(
                            candidate.missing, SPECTRE_TILE_BOUNDARY
                        )[1],
                        "exposed_edges": cluster_adjacency(
                            candidate.missing, SPECTRE_TILE_BOUNDARY
                        )[2],
                    },
                    "recursive_closure": True,
                    "level_counts": [
                        len(level.poses)
                        for level in candidate_recursive.levels
                    ],
                })
        if len(recursive_survivors) != 1:
            raise ValueError(
                "expected one recursively closing physical phase, found "
                f"{len(recursive_survivors)}"
            )
        rule, recursive = recursive_survivors[0]
        physical_forcing = physical_composition_sat_certificate(
            anchors[4],
            anchors[5],
            rule,
            [candidate for candidate, _ in phase_candidates],
            SPECTRE_TILE_BOUNDARY,
            radius=1,
        )

        levels = {}
        physical_counts = []
        all_exact = (
            rule == ranked_rule
            and physical_forcing["unique_composition"]
        )
        for level in range(1, 6):
            cover = cover_with_rule(anchors[level], rule.full, rule.missing)
            hidden = read_hidden_parent_groups(
                hidden_paths[level], anchors[level]
            )
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

        recursive_validation = {}
        for depth, level in enumerate(recursive.levels, 1):
            hidden = read_hidden_parent_groups(
                hidden_paths[4], anchors[4], levels_up=depth
            )
            validation = validate_against_hidden(level.leaves, hidden)
            recursive_validation[str(depth)] = validation
            all_exact &= validation["exact"]

        upper_immediate = contract_level(raw_hierarchy_level(anchors[5]), rule)
        lower_immediate = recursive.levels[0]
        lower_contacts = physical_edge_contacts(
            anchors[4], SPECTRE_TILE_BOUNDARY
        )
        upper_contacts = physical_edge_contacts(
            anchors[5], SPECTRE_TILE_BOUNDARY
        )
        upper_adjacency = contracted_adjacency(
            upper_contacts, upper_immediate
        )
        collar_colors = oriented_collar_colors(
            upper_immediate, upper_adjacency, radius=1
        )
        hidden_labels = read_hidden_node_labels(
            hidden_paths[5], anchors[5], upper_immediate, levels_up=1
        )
        interior = [
            i for i, neighbors in enumerate(upper_adjacency)
            if len(neighbors) == 6
        ]
        collar_validation = collar_label_validation(
            collar_colors, hidden_labels, interior
        )
        all_exact &= (
            collar_validation["pure"]
            and collar_validation["collar_classes"] == 17
            and collar_validation["labels"] == 9
        )
        first_recursive_rule = recursive.rules[0]
        first_recursive_cover = cover_with_rule(
            upper_immediate.poses,
            first_recursive_rule.full,
            first_recursive_rule.missing,
        )
        upper_parent = contract_level(
            upper_immediate, first_recursive_rule, first_recursive_cover
        )
        uncollared_rules = collared_substitution_rules(
            lower_immediate,
            upper_immediate,
            upper_parent,
            first_recursive_cover,
            lower_contacts,
            upper_contacts,
            radius=0,
        )
        uncollared_composition = collared_composition_sat_certificate(
            lower_immediate,
            upper_immediate,
            upper_parent,
            first_recursive_cover,
            lower_contacts,
            upper_contacts,
            uncollared_rules,
            radius=0,
        )
        collared_rules = collared_substitution_rules(
            lower_immediate,
            upper_immediate,
            upper_parent,
            first_recursive_cover,
            lower_contacts,
            upper_contacts,
            radius=1,
        )
        collared_composition = collared_composition_sat_certificate(
            lower_immediate,
            upper_immediate,
            upper_parent,
            first_recursive_cover,
            lower_contacts,
            upper_contacts,
            collared_rules,
            radius=1,
        )
        all_exact &= (
            collared_rules["deterministic"]
            and collared_rules["closed"]
            and collared_rules["state_count"] == 17
            and collared_composition["all_states_checked"]
            and collared_composition["unique_composition"]
        )

        recurrence = recover_order2_recurrence(physical_counts)
        full_adj = cluster_adjacency(rule.full, SPECTRE_TILE_BOUNDARY)
        missing_adj = cluster_adjacency(rule.missing, SPECTRE_TILE_BOUNDARY)
        result = {
            "status": "PASS" if all_exact else "FAIL",
            "scope": (
                "A6 v2 recursive phase selection, physical radius-1 forcing, "
                "closed collared substitution, and SAT-checked composition"
            ),
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
            "physical_phase_closure": {
                "candidates": len(phase_candidates),
                "recursive_survivors": len(recursive_survivors),
                "heuristic_selection_agrees": rule == ranked_rule,
                "results": phase_results,
            },
            "physical_radius1_composition_sat": physical_forcing,
            "delta_levels": levels,
            "all_root_labels_level3": roots,
            "recursive_hierarchy": {
                "level_counts": [
                    len(level.poses) for level in recursive.levels
                ],
                "covers": [
                    {
                        "full": cover.n_full,
                        "missing": cover.n_missing,
                        "unique": cover.n_solutions == 1,
                    }
                    for cover in recursive.covers
                ],
                "rules": [_rule_json(found) for found in recursive.rules],
                "refinement_rounds": list(recursive.refinement_rounds),
                "hidden_validation": recursive_validation,
            },
            "radius1_collar_validation": collar_validation,
            "radius0_collared_substitution": uncollared_rules,
            "radius0_composition_sat": uncollared_composition,
            "radius1_collared_substitution": collared_rules,
            "radius1_composition_sat": collared_composition,
            "physical_composition_forcing_radius": 1,
            "composition_forcing_radius_in_metatile_language": 0,
            "substitution_collar_state_radius": 1,
            "physical_tile_counts": physical_counts,
            "recurrence": recurrence,
            "inflation_area": "dominant root 4 + sqrt(15)",
        }
        out_json = ASSETS / "a6-spectre-results.json"
        out_json.write_text(json.dumps(result, indent=2) + "\n")
        out_svg = ASSETS / "a6-spectre-metatiles.svg"
        _render_metatiles(rule.full, rule.missing, out_svg)

    print(
        f"A6 v2: {result['status']} — recursive "
        f"{' -> '.join(map(str, result['recursive_hierarchy']['level_counts']))}; "
        f"{physical_forcing['unique_patterns']} physical collar patterns forced; "
        f"{collared_rules['state_count']} closed radius-1 states, "
        f"{collared_composition['unique_instances']}/"
        f"{collared_composition['complete_context_instances']} complete "
        f"contexts SAT-unique; "
        f"recurrence "
        f"T[n+1]={recurrence['a']}T[n] - T[n-1]"
    )
    print(out_json.relative_to(ROOT))
    print(out_svg.relative_to(ROOT))
    return 0 if all_exact else 1


if __name__ == "__main__":
    raise SystemExit(main())
