#!/usr/bin/env python
"""Blind A6 candidate screen on the stored A3 hat disk patch.

This is the Gate-G1 adapter/screen, not yet a hierarchy certificate. It mines
exact nearest-anchor 8-tile scaffolds, expands one-child deletions, and asks
whether each rule covers an interior core using the surrounding disk as halo.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from einstein.db import ShapeDB, deserialize_cells
from einstein.funnel.a6_hierarchy import (
    deletion_variants,
    raw_hierarchy_level,
    template_occurrences,
)
from einstein.funnel.a6_polykite import (
    contract_typed_core_cover,
    cover_core_with_rule,
    enumerate_typed_core_covers,
    forced_typed_core_options,
    frequent_hex_nearest_templates,
    mine_option_state_recursive_library,
    placement_poses,
    polykite_boundary,
    typed_core_backbone,
)
from einstein.substrate.module12 import apply_sr, madd, to_xy

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"


def _template_json(template):
    return [[s, r, list(t)] for s, r, t in template]


def _render_candidate(
    candidate_number: int,
    candidate: dict,
    full,
    missing,
    boundary,
    out: Path,
) -> None:
    """Render aligned full/deletion panels with the removed hat ghosted."""
    embedded = template_occurrences(missing, full)
    if len(embedded) != 1:
        raise ValueError(
            f"candidate {candidate_number}: deletion embeds {len(embedded)} ways"
        )
    retained = embedded[0]
    polygons = []
    all_xy = []
    for child, (s, r, t) in enumerate(full):
        points = [
            to_xy(madd(t, apply_sr(s, r, vertex)))
            for vertex in boundary
        ]
        polygons.append(points)
        all_xy.extend(points)
    lo_x = min(x for x, _ in all_xy)
    hi_x = max(x for x, _ in all_xy)
    lo_y = min(y for _, y in all_xy)
    hi_y = max(y for _, y in all_xy)
    panel_width = hi_x - lo_x
    gap = 3.0
    offsets = [0.0, panel_width + gap]
    pad_x = 1.0
    pad_bottom = 1.0
    title_space = 3.2
    scale = 42.0
    width = (2 * panel_width + gap + 2 * pad_x) * scale
    height = (hi_y - lo_y + title_space + pad_bottom) * scale

    def screen(point, panel):
        x, y = point
        return (
            (x - lo_x + offsets[panel] + pad_x) * scale,
            (hi_y - y + title_space) * scale,
        )

    colors = [
        "#f2c14e", "#f78154", "#4d9078", "#577590",
        "#9b5de5", "#43aa8b", "#f94144", "#90be6d",
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.1f} {height:.1f}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        (
            f'<text x="{width / 2:.1f}" y="25" fill="#f8f9fa" '
            'font-family="sans-serif" font-size="18" font-weight="700" '
            f'text-anchor="middle">Hat A6 exception variant '
            f'{candidate_number}</text>'
        ),
        (
            f'<text x="{width / 2:.1f}" y="47" fill="#adb5bd" '
            'font-family="sans-serif" font-size="12" text-anchor="middle">'
            f'proposal rank {candidate["proposal_rank"]}, deletion '
            f'{candidate["deletion"]}, frequency '
            f'{candidate["proposal_frequency"]}; at least two core covers</text>'
        ),
    ]
    titles = ["full scaffold (8 hats)", "one-child exception (7 hats)"]
    for panel, title in enumerate(titles):
        center = (
            (offsets[panel] + panel_width / 2 + pad_x) * scale
        )
        lines.append(
            f'<text x="{center:.1f}" y="72" fill="#dee2e6" '
            'font-family="sans-serif" font-size="14" font-weight="600" '
            f'text-anchor="middle">{title}</text>'
        )
        for child, points in enumerate(polygons):
            ghost = panel == 1 and child not in retained
            coords = " ".join(
                f"{x:.2f},{y:.2f}"
                for x, y in (screen(point, panel) for point in points)
            )
            if ghost:
                style = (
                    'fill="#f94144" fill-opacity="0.10" '
                    'stroke="#f94144" stroke-width="2.2" '
                    'stroke-dasharray="7 5"'
                )
            else:
                style = (
                    f'fill="{colors[child]}" fill-opacity="0.78" '
                    'stroke="#f8f9fa" stroke-width="1.4"'
                )
            lines.append(
                f'<polygon points="{coords}" {style} stroke-linejoin="round"/>'
            )
            cx = sum(x for x, _ in points) / len(points)
            cy = sum(y for _, y in points) / len(points)
            sx, sy = screen((cx, cy), panel)
            lines.append(
                f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="9" '
                f'fill="#11151c" fill-opacity="0.82" '
                f'stroke="{colors[child]}" stroke-width="1.5"/>'
            )
            lines.append(
                f'<text x="{sx:.2f}" y="{sy + 4:.2f}" fill="#f8f9fa" '
                'font-family="sans-serif" font-size="11" font-weight="700" '
                f'text-anchor="middle">{child + 1}</text>'
            )
    lines.append("</svg>")
    out.write_text("\n".join(lines) + "\n")


def main() -> int:
    db = ShapeDB(ROOT / "data" / "shapes.sqlite")
    key = db.conn.execute(
        "SELECT key FROM shapes WHERE id = 635"
    ).fetchone()[0]
    shape = deserialize_cells(key)
    certificate = db.latest_verdict(635, "A3-patch")["certificate"]
    db.close()

    poses = placement_poses(certificate["placements"])
    boundary = polykite_boundary(shape)
    core_r2 = 10_000
    core = [
        i for i, pose in enumerate(poses)
        if pose[2][0] ** 2
        + pose[2][0] * pose[2][2]
        + pose[2][2] ** 2 <= core_r2
    ]
    histogram = frequent_hex_nearest_templates(
        poses, min_size=8, max_size=8, top=20
    )[8]
    ASSETS.mkdir(parents=True, exist_ok=True)
    candidates = []
    screened = 0
    for rank, (full, frequency) in enumerate(histogram, 1):
        full_occurrences = template_occurrences(full, poses)
        for deletion, missing in enumerate(deletion_variants(full)):
            screened += 1
            missing_occurrences = template_occurrences(missing, poses)
            covered = set().union(
                *(full_occurrences + missing_occurrences)
            )
            if not all(i in covered for i in core):
                continue
            cover = cover_core_with_rule(
                poses, core, full, missing
            )
            if cover.n_solutions:
                candidate_number = len(candidates) + 1
                svg = ASSETS / f"a6-hat-candidate-{candidate_number}.svg"
                candidates.append({
                    "proposal_rank": rank,
                    "deletion": deletion,
                    "proposal_frequency": frequency,
                    "full_occurrences": len(full_occurrences),
                    "missing_occurrences": len(missing_occurrences),
                    "core_cover": {
                        "full": cover.n_full,
                        "missing": cover.n_missing,
                        "solutions_capped_at_2": cover.n_solutions,
                    },
                    "full": _template_json(full),
                    "missing": _template_json(missing),
                    "svg": str(svg.relative_to(ROOT)),
                })
                _render_candidate(
                    candidate_number,
                    candidates[-1],
                    full,
                    missing,
                    boundary,
                    svg,
                )

    rule_family = None
    if (
        len(candidates) == 2
        and candidates[0]["full"] == candidates[1]["full"]
    ):
        templates = (
            tuple(
                (s, r, tuple(t))
                for s, r, t in candidates[0]["full"]
            ),
            tuple(
                (s, r, tuple(t))
                for s, r, t in candidates[0]["missing"]
            ),
            tuple(
                (s, r, tuple(t))
                for s, r, t in candidates[1]["missing"]
            ),
        )
        sampled_covers = enumerate_typed_core_covers(
            poses, core, templates, limit=20
        )
        contractions = [
            contract_typed_core_cover(
                raw_hierarchy_level(poses), templates, cover
            )
            for cover in sampled_covers
        ]
        anchor_sets_agree = (
            bool(contractions)
            and all(
                set(contraction.level.poses)
                == set(contractions[0].level.poses)
                for contraction in contractions[1:]
            )
        )
        rule_family = {
            "interpretation": (
                "one full scaffold with two allowed one-child "
                "exception variants"
            ),
            "template_types": [
                "full-8",
                "missing-child-2",
                "missing-child-1",
            ],
            "covers_sampled": len(sampled_covers),
            "cover_count_is_lower_bound": (
                len(sampled_covers) == 20
            ),
            "sampled_type_counts": [
                {
                    str(template_type): count
                    for template_type, count in sorted(
                        Counter(contraction.types).items()
                    )
                }
                for contraction in contractions
            ],
            "sampled_parent_anchor_sets_agree": anchor_sets_agree,
            "sampled_parent_anchors": (
                len(contractions[0].level.poses)
                if contractions else 0
            ),
            "interior_anchor_backbone": typed_core_backbone(
                poses, core, templates, base_r2=core_r2 // 2
            ),
        }
        recursive_physical_r2 = 30_000
        recursive_physical_core = [
            i for i, pose in enumerate(poses)
            if (
                pose[2][0] ** 2
                + pose[2][0] * pose[2][2]
                + pose[2][2] ** 2
            ) <= recursive_physical_r2
        ]
        option_states = forced_typed_core_options(
            poses,
            recursive_physical_core,
            templates,
            base_r2=22_000,
        )
        rule_family["recursive_probe"] = (
            mine_option_state_recursive_library(
                option_states,
                training_r2=15_000,
                forcing_r2=5_000,
            )
        )

    result = {
        "status": "RULE-FAMILY" if rule_family else (
            "CANDIDATES" if candidates else "NO-CANDIDATE"
        ),
        "scope": "blind local A6 screen; recursive closure not yet checked",
        "shape_id": 635,
        "patch_tiles": len(poses),
        "tile_boundary_vertices": len(boundary),
        "core_r2": core_r2,
        "core_tiles": len(core),
        "top_frequencies": [frequency for _, frequency in histogram],
        "rules_screened": screened,
        "candidates": candidates,
        "unique_candidates": sum(
            candidate["core_cover"]["solutions_capped_at_2"] == 1
            for candidate in candidates
        ),
        "ambiguous_candidates": sum(
            candidate["core_cover"]["solutions_capped_at_2"] == 2
            for candidate in candidates
        ),
        "rule_family": rule_family,
    }
    out = ASSETS / "a6-hat-screen-results.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"A6 hat screen: {len(candidates)} exception variants "
        f"({result['unique_candidates']} unique, "
        f"{result['ambiguous_candidates']} ambiguous) from "
        f"{screened} rules on {len(core)} core tiles"
    )
    if rule_family:
        backbone = rule_family["interior_anchor_backbone"]
        print(
            "  consolidated: one 3-type rule family; "
            f"{rule_family['covers_sampled']}+ covers sampled, "
            f"{backbone['forced_bases']} interior anchors forced"
        )
        recursive = rule_family["recursive_probe"]
        print(
            "  recursive probe: "
            f"{recursive['minimum_patterns']} typed patterns; "
            f"{recursive['forced_inner_groups']} inner groups forced, "
            f"{recursive['optional_inner_groups']} optional"
        )
    print(out.relative_to(ROOT))
    for candidate in candidates:
        print(candidate["svg"])
    return 0 if candidates else 1


if __name__ == "__main__":
    raise SystemExit(main())
