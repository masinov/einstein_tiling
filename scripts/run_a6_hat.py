#!/usr/bin/env python
"""Blind A6 candidate screen on the stored A3 hat disk patch.

This is the Gate-G1 adapter/screen, not yet a hierarchy certificate. It mines
exact nearest-anchor 8-tile scaffolds, expands one-child deletions, and asks
whether each rule covers an interior core using the surrounding disk as halo.
"""

from __future__ import annotations

import json
from pathlib import Path

from einstein.db import ShapeDB, deserialize_cells
from einstein.funnel.a6_hierarchy import (
    deletion_variants,
    template_occurrences,
)
from einstein.funnel.a6_polykite import (
    cover_core_with_rule,
    frequent_hex_nearest_templates,
    placement_poses,
    polykite_boundary,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"


def _template_json(template):
    return [[s, r, list(t)] for s, r, t in template]


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
                })

    result = {
        "status": "CANDIDATES" if candidates else "NO-CANDIDATE",
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
    }
    ASSETS.mkdir(parents=True, exist_ok=True)
    out = ASSETS / "a6-hat-screen-results.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"A6 hat screen: {len(candidates)} candidates "
        f"({result['unique_candidates']} unique, "
        f"{result['ambiguous_candidates']} ambiguous) from "
        f"{screened} rules on {len(core)} core tiles"
    )
    print(out.relative_to(ROOT))
    return 0 if candidates else 1


if __name__ == "__main__":
    raise SystemExit(main())
