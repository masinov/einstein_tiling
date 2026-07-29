#!/usr/bin/env python
"""Independent-solution robustness audit for the E1 n=10 finalist.

Four deterministic SAT phase seeds produce independent r2=12,800 patches.
The audit compares exact placement overlap, exact/approximate translation
repetitions, and matched-null A4 fingerprints.

Usage:
  venv/bin/python scripts/run_e1_finalist_robustness.py
  venv/bin/python scripts/run_e1_finalist_robustness.py --reuse-dir /tmp
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import json
import math
import random
import time
from pathlib import Path

from einstein.db import ShapeDB
from einstein.e1_candidates import (
    SMALLEST_DEPTH3_KEYS,
    decode_compiled_key,
)
from einstein.funnel.a1_torus import cell_to_lattice, lattice_to_cell
from einstein.funnel.a3_patch import (
    certificate_cells,
    disk_region,
    sat_grow_patch,
    verify_patch_certificate,
)
from einstein.funnel.a4_diffraction import (
    class_power_sum,
    detect_peaks,
    fingerprint,
    index_peaks,
)
from einstein.render.svg import hex_to_xy
from einstein.substrate.kitegrid import (
    boundary_cycle,
    cell_centroid4,
    norm2,
)

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/notebook/assets"
OUTPUT = ASSETS / "e1-finalist-robustness.json"
GALLERY = ASSETS / "e1-finalist-independent-patches.svg"
KEY = SMALLEST_DEPTH3_KEYS[10][1]
SHAPE = decode_compiled_key(KEY)
SEEDS = (1, 2, 3, 4)
COLORS = (
    "#f2c14e", "#f78154", "#4d9078", "#577590",
    "#9b5de5", "#43aa8b", "#f8961e", "#277da1",
    "#90be6d", "#f94144", "#b5179e", "#00b4d8",
)


def solve(seed):
    started = time.monotonic()
    result = sat_grow_patch(
        SHAPE,
        12_800,
        fix_seed=False,
        conflict_budget=10_000_000,
        phase_seed=seed,
    )
    if not result["completed"]:
        raise RuntimeError(f"phase seed {seed} did not complete: {result}")
    return seed, result["certificate"], result["stats"], round(
        time.monotonic() - started, 3
    )


def load_or_solve(reuse_dir):
    if reuse_dir is not None:
        rows = []
        for seed in SEEDS:
            certificate = json.loads(
                (reuse_dir / f"e1-finalist-seed-{seed}.json").read_text()
            )
            rows.append((seed, certificate, {"phase_seed": seed}, None))
        return rows
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(SEEDS)) as pool:
        return list(pool.map(solve, SEEDS))


def translation_profile(certificate, inner_r2=6_400):
    poses = []
    for op, tx, ty in certificate["placements"]:
        u, v, _ = cell_to_lattice((tx, ty, 0))
        x, y = hex_to_xy((tx, ty))
        poses.append((op, u, v, x, y))
    pose_set = {(op, u, v) for op, u, v, _, _ in poses}
    central = sorted(poses, key=lambda row: row[3] ** 2 + row[4] ** 2)[:60]
    candidates = set()
    for op, u, v, _, _ in central:
        for other_op, other_u, other_v, _, _ in poses:
            if other_op != op:
                continue
            du, dv = other_u - u, other_v - v
            if (
                (du > 0 or (du == 0 and dv > 0))
                and abs(du) <= 80
                and abs(dv) <= 80
            ):
                candidates.add((du, dv))
    rows = []
    for du, dv in candidates:
        dx, dy = hex_to_xy((2 * du - 2 * dv, 2 * du + 4 * dv))
        eligible = matched = 0
        for op, u, v, x, y in poses:
            shifted_x, shifted_y = x + dx, y + dy
            if (
                x * x + y * y <= inner_r2
                and shifted_x * shifted_x + shifted_y * shifted_y <= inner_r2
            ):
                eligible += 1
                matched += (op, u + du, v + dv) in pose_set
        if eligible >= 50:
            rows.append({
                "du": du,
                "dv": dv,
                "length": math.hypot(dx, dy),
                "matched": matched,
                "eligible": eligible,
                "fraction": matched / eligible,
            })
    rows.sort(
        key=lambda row: (row["fraction"], row["matched"]),
        reverse=True,
    )
    return rows[:10]


def diffraction(certificate, seed, grid=1024, seed_offset=20_000):
    by_op = collections.defaultdict(list)
    for op, tx, ty in certificate["placements"]:
        by_op[op].append(hex_to_xy((tx, ty)))
    classes = [points for points in by_op.values() if len(points) >= 8]
    rng = random.Random(seed_offset + seed)
    radius = math.sqrt(certificate["r2"])
    null = []
    for points in classes:
        random_points = []
        for _ in points:
            r = radius * math.sqrt(rng.random())
            angle = 2 * math.pi * rng.random()
            random_points.append((r * math.cos(angle), r * math.sin(angle)))
        null.append(random_points)
    power, dk, k0 = class_power_sum(null, grid=grid)
    peaks = detect_peaks(power, dk, k0, floor=1e-12, max_peaks=5)
    floor = 5 * (peaks[0][2] if peaks else 1e-12)
    return floor, fingerprint(classes=classes, grid=grid, floor=floor)


def render_gallery(results):
    panel = 500
    width = 2 * panel
    height = 2 * (panel + 55)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    for panel_index, result in enumerate(results):
        ox = (panel_index % 2) * panel
        oy = (panel_index // 2) * (panel + 55)
        certificate = result["certificate"]
        groups = certificate_cells(SHAPE, certificate)
        outlines = [
            (
                placement[0],
                [hex_to_xy(vertex) for vertex in boundary_cycle(group)],
            )
            for placement, group in zip(certificate["placements"], groups)
        ]
        xs = [x for _, outline in outlines for x, _ in outline]
        ys = [y for _, outline in outlines for _, y in outline]
        margin = 15
        scale = min(
            (panel - 2 * margin) / (max(xs) - min(xs)),
            (panel - 2 * margin) / (max(ys) - min(ys)),
        )
        x_shift = ox + (panel - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
        y_shift = oy + margin + (
            panel - 2 * margin - (max(ys) - min(ys)) * scale
        ) / 2 + max(ys) * scale
        for op, outline in outlines:
            points = " ".join(
                f"{x_shift + x * scale:.2f},{y_shift - y * scale:.2f}"
                for x, y in outline
            )
            parts.append(
                f'<polygon points="{points}" fill="{COLORS[op]}" '
                'fill-opacity="0.84" stroke="#f8f9fa" stroke-width="0.28" '
                'stroke-linejoin="round"/>'
            )
        fp = result["a4"]
        confirm = result["a4_confirm"]
        parts.extend([
            (
                f'<text x="{ox + panel / 2}" y="{oy + panel + 22}" '
                'fill="#f8f9fa" font-family="sans-serif" font-size="15" '
                f'font-weight="700" text-anchor="middle">phase seed '
                f'{result["phase_seed"]} · {certificate["tiles"]} tiles</text>'
            ),
            (
                f'<text x="{ox + panel / 2}" y="{oy + panel + 43}" '
                'fill="#51cf66" font-family="sans-serif" font-size="12" '
                f'text-anchor="middle">1024² r{fp["rank"]}/s{fp["symmetry"]} '
                f'· 2048² r{confirm["rank"]}/s{confirm["symmetry"]} · '
                f'best translation '
                f'{result["translations"][0]["fraction"]:.1%}</text>'
            ),
        ])
    parts.append("</svg>")
    GALLERY.write_text("\n".join(parts) + "\n")


def boundary_audit(certificate):
    covered = {
        cell
        for group in certificate_cells(SHAPE, certificate)
        for cell in group
    }
    region = set(disk_region(certificate["r2"]))
    annuli = []
    for extra_r2 in (1_000, 2_500, 5_000, 10_000):
        outer = set(disk_region(certificate["r2"] + extra_r2))
        annulus = outer - region
        uncovered = annulus - covered
        annuli.append({
            "extra_r2": extra_r2,
            "cells": len(annulus),
            "uncovered": len(uncovered),
            "uncovered_fraction": len(uncovered) / len(annulus),
        })
    return {
        "certified_region_cells": len(region),
        "covered_cells_total": len(covered),
        "missing_inside_certified_disk": len(region - covered),
        "overhang_cells": sum(
            norm2(cell_centroid4(cell)) > 16 * certificate["r2"]
            for cell in covered
        ),
        "exterior_annuli": annuli,
    }


def periodic_control_classes(db, radius):
    verdict = db.latest_verdict(392, "A1-torus")
    certificate = verdict["certificate"]
    a, b, d = certificate["hnf"]
    reach = int(radius) + 4
    classes = []
    for _, tu, tv in certificate["placements"]:
        points = []
        for m in range(-reach, reach + 1):
            for n in range(-reach, reach + 1):
                u, v = m * a + n * b + tu, n * d + tv
                cx, cy, _ = lattice_to_cell((u, v, 0))
                x, y = hex_to_xy((cx, cy))
                if x * x + y * y <= radius * radius:
                    points.append((x, y))
        classes.append(points)
    return classes


def rank_top_profile(classes, floor):
    power, dk, k0 = class_power_sum(classes, grid=2048)
    peaks = detect_peaks(
        power, dk, k0, floor=floor, max_peaks=5_000
    )
    profile = {}
    for top in (20, 30, 40, 60, 100, 150, 250, 400, 800):
        rank, _, _ = index_peaks(
            peaks,
            2 * dk,
            max_rank=6,
            coeff_bound=8,
            top=top,
            pair_bound=384,
        )
        profile[str(top)] = rank
    return {"detected_peaks": len(peaks), "rank_by_top": profile}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-dir", type=Path)
    args = parser.parse_args()
    solved = load_or_solve(args.reuse_dir)
    results = []
    placement_sets = {}
    for seed, certificate, stats, wall_seconds in sorted(solved):
        assert verify_patch_certificate(SHAPE, certificate)
        floor, a4 = diffraction(certificate, seed)
        confirm_floor, a4_confirm = diffraction(
            certificate, seed, grid=2048, seed_offset=30_000
        )
        result = {
            "phase_seed": seed,
            "wall_seconds": wall_seconds,
            "stats": stats,
            "certificate": certificate,
            "translations": translation_profile(certificate),
            "a4_floor": floor,
            "a4": a4,
            "a4_confirm_floor": confirm_floor,
            "a4_confirm": a4_confirm,
        }
        results.append(result)
        placement_sets[seed] = {
            tuple(placement) for placement in certificate["placements"]
        }
    overlaps = []
    for left_index, left in enumerate(SEEDS):
        for right in SEEDS[left_index + 1:]:
            intersection = placement_sets[left] & placement_sets[right]
            union = placement_sets[left] | placement_sets[right]
            overlaps.append({
                "left": left,
                "right": right,
                "intersection": len(intersection),
                "jaccard": len(intersection) / len(union),
            })
    original_certificate = json.loads(
        (ASSETS / "e1-finalist-results.json").read_text()
    )["a3"]["certificate"]
    db = ShapeDB(
        ROOT / "tests/fixtures/polykites-n8.sqlite",
        read_only=True,
    )
    raw_hat = db.conn.execute(
        """
        SELECT certificate
        FROM verdicts
        WHERE shape_id = 635 AND stage = 'A3-patch'
          AND json_extract(certificate, '$.r2') = 50000
        """
    ).fetchone()[0]
    hat_certificate = json.loads(raw_hat)
    hat_by_op = collections.defaultdict(list)
    for op, tx, ty in hat_certificate["placements"]:
        hat_by_op[op].append(hex_to_xy((tx, ty)))
    periodic_classes = periodic_control_classes(db, math.sqrt(50_000))
    db.close()
    candidate_classes = collections.defaultdict(list)
    for op, tx, ty in original_certificate["placements"]:
        candidate_classes[op].append(hex_to_xy((tx, ty)))
    core_floor = json.loads(
        (ASSETS / "e4-results.json").read_text()
    )["floor"]
    candidate_floor = json.loads(
        (ASSETS / "e1-finalist-results.json").read_text()
    )["a4_r2_50000"]["floor"]
    payload = {
        "kind": "independent-sat-phase-robustness",
        "candidate": {"n": 10, "index": 2, "shape": KEY},
        "r2": 12_800,
        "results": results,
        "pairwise_overlaps": overlaps,
        "original_large_patch_boundary_audit": boundary_audit(
            original_certificate
        ),
        "original_large_patch_translation_profile": translation_profile(
            original_certificate,
            inner_r2=16_000,
        ),
        "rank_top_sensitivity": {
            "periodic_control": rank_top_profile(
                periodic_classes, core_floor
            ),
            "hat_control": rank_top_profile(
                list(hat_by_op.values()), core_floor
            ),
            "candidate": rank_top_profile(
                list(candidate_classes.values()), candidate_floor
            ),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    render_gallery(results)
    print(OUTPUT.relative_to(ROOT))
    print(GALLERY.relative_to(ROOT))


if __name__ == "__main__":
    main()
