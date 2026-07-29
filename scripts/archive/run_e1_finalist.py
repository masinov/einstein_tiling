#!/usr/bin/env python
"""Reproduce the blind E1 rediscovery of the known Turtle control.

Legacy corpus label: n=10, candidate 2 / "E1 finalist".

Checks:
  * pose-free A3 disk cover at r2=50,000 (~9,000 tiles);
  * exact SAT torus search through index 100, parallel by quotient index;
  * matched-null A4 fingerprint at grid 2048;
  * patch and spectrum assets for human inspection.

The expensive A3 result may be reused after an interrupted documentation run:
  venv/bin/python scripts/archive/run_e1_finalist.py \
      --reuse-a3 /tmp/e1-finalist-r2-50000.json \
      --a3-wall-seconds 276.18
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import random
import subprocess
import time
from pathlib import Path

from einstein.e1_candidates import (
    SMALLEST_DEPTH3_KEYS,
    TURTLE_KEY,
    decode_compiled_key,
)
from einstein.funnel.a1_torus import find_periodic_tiling_sat
from einstein.funnel.a3_patch import (
    certificate_cells,
    sat_grow_patch,
    verify_patch_certificate,
)
from einstein.funnel.a4_diffraction import (
    class_power_sum,
    detect_peaks,
    fingerprint,
    save_spectrum_pgm,
)
from einstein.render.svg import hex_to_xy
from einstein.substrate.kitegrid import boundary_cycle

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "docs/notebook" / "assets"
OUTPUT = ASSETS / "e1-finalist-results.json"
PATCH_SVG = ASSETS / "e1-finalist-patch.svg"
SPECTRUM_PNG = ASSETS / "e1-finalist-spectrum.png"
KEY = SMALLEST_DEPTH3_KEYS[10][1]
assert KEY == TURTLE_KEY
SHAPE = decode_compiled_key(KEY)
COLORS = (
    "#f2c14e", "#f78154", "#4d9078", "#577590",
    "#9b5de5", "#43aa8b", "#f8961e", "#277da1",
    "#90be6d", "#f94144", "#b5179e", "#00b4d8",
)


def torus_index(k):
    certificate, exhausted = find_periodic_tiling_sat(
        SHAPE,
        k_min=k,
        k_max=k,
        conflict_budget=1_000_000,
    )
    return k, certificate, exhausted


def torus_sweep(k_max, jobs):
    indices = [k for k in range(1, k_max + 1) if (6 * k) % len(SHAPE) == 0]
    t0 = time.monotonic()
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(jobs, len(indices))
    ) as pool:
        rows = list(pool.map(torus_index, indices))
    certificates = [
        (k, certificate)
        for k, certificate, _ in rows
        if certificate is not None
    ]
    certificate = min(certificates)[1] if certificates else None
    return {
        "k_max": k_max,
        "indices_tested": indices,
        "certificate": certificate,
        "exhausted_indices": [
            k for k, _, exhausted in rows if exhausted
        ],
        "wall_seconds": round(time.monotonic() - t0, 3),
    }


def classes_from_certificate(certificate):
    rows = [
        (op, *hex_to_xy((tx, ty)))
        for op, tx, ty in certificate["placements"]
    ]
    cx = sum(x for _, x, _ in rows) / len(rows)
    cy = sum(y for _, _, y in rows) / len(rows)
    by_op = {}
    for op, x, y in rows:
        by_op.setdefault(op, []).append((x - cx, y - cy))
    return [points for points in by_op.values() if len(points) >= 8]


def diffraction(classes, radius, seed):
    rng = random.Random(seed)
    null = []
    for points in classes:
        random_points = []
        for _ in points:
            r = radius * math.sqrt(rng.random())
            angle = 2 * math.pi * rng.random()
            random_points.append((r * math.cos(angle), r * math.sin(angle)))
        null.append(random_points)
    power, dk, k0 = class_power_sum(null, grid=2048)
    peaks = detect_peaks(power, dk, k0, floor=1e-12, max_peaks=5)
    noise_ceiling = peaks[0][2] if peaks else 1e-12
    floor = 5 * noise_ceiling
    result = fingerprint(classes=classes, grid=2048, floor=floor)

    power, _, _ = class_power_sum(classes, grid=2048)
    quarter = power.shape[0] // 4
    core = power[quarter:-quarter, quarter:-quarter]
    pgm = Path("/tmp/e1-finalist-spectrum.pgm")
    save_spectrum_pgm(core, str(pgm), vmax=floor)
    subprocess.run(["convert", str(pgm), str(SPECTRUM_PNG)], check=True)
    return {"floor": floor, "result": result}


def render_patch(certificate):
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
    width, height, title = 1000, 1060, 60
    margin = 22
    scale = min(
        (width - 2 * margin) / (max(xs) - min(xs)),
        (height - title - 2 * margin) / (max(ys) - min(ys)),
    )
    x_shift = (width - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    y_shift = (
        title + margin
        + (height - title - 2 * margin - (max(ys) - min(ys)) * scale) / 2
        + max(ys) * scale
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
        (
            '<text x="500" y="27" fill="#f8f9fa" '
            'font-family="sans-serif" font-size="18" font-weight="700" '
            'text-anchor="middle">E1 blind rediscovery · known Turtle</text>'
        ),
        (
            '<text x="500" y="49" fill="#51cf66" '
            'font-family="sans-serif" font-size="13" text-anchor="middle">'
            f'pose-free A3 patch · r²={certificate["r2"]} · '
            f'{certificate["tiles"]} tiles</text>'
        ),
    ]
    radius = math.sqrt(certificate["r2"]) * scale
    parts.append(
        f'<circle cx="{x_shift:.2f}" cy="{y_shift:.2f}" r="{radius:.2f}" '
        'fill="none" stroke="#ffec99" stroke-opacity="0.90" '
        'stroke-width="2.2" stroke-dasharray="7 4"/>'
    )
    parts.append(
        '<text x="500" y="1042" fill="#ffec99" '
        'font-family="sans-serif" font-size="12" text-anchor="middle">'
        'exact coverage is certified inside the dashed circle; '
        'the exterior crown is unconstrained</text>'
    )
    for op, outline in outlines:
        points = " ".join(
            f"{x_shift + x * scale:.2f},{y_shift - y * scale:.2f}"
            for x, y in outline
        )
        parts.append(
            f'<polygon points="{points}" fill="{COLORS[op]}" '
            'fill-opacity="0.84" stroke="#f8f9fa" stroke-width="0.20" '
            'stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    PATCH_SVG.write_text("\n".join(parts) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-a3", type=Path)
    parser.add_argument("--a3-wall-seconds", type=float)
    parser.add_argument("--k-max", type=int, default=100)
    parser.add_argument("--jobs", type=int, default=10)
    args = parser.parse_args()

    if args.reuse_a3:
        a3 = json.loads(args.reuse_a3.read_text())
        a3_wall = args.a3_wall_seconds
    else:
        t0 = time.monotonic()
        a3 = {
            "shape": KEY,
            **sat_grow_patch(
                SHAPE,
                50_000,
                fix_seed=False,
                conflict_budget=10_000_000,
            ),
        }
        a3_wall = round(time.monotonic() - t0, 3)
    assert a3["shape"] == KEY
    assert a3["completed"] and not a3["refuted"] and not a3["exhausted"]
    assert verify_patch_certificate(SHAPE, a3["certificate"])

    a1 = torus_sweep(args.k_max, args.jobs)
    classes = classes_from_certificate(a3["certificate"])
    a4 = diffraction(classes, math.sqrt(a3["certificate"]["r2"]), 10302)
    prior = json.loads(
        (ASSETS / "a4-small-candidate-results.json").read_text()
    )
    prior_row = next(
        row for row in prior["results"]
        if row["n"] == 10 and row["index"] == 2
    )
    render_patch(a3["certificate"])

    payload = {
        "kind": "e1-turtle-control-escalation",
        "legacy_kind": "e1-smallest-corpus-finalist-escalation",
        "candidate": {
            "n": 10,
            "index": 2,
            "shape": KEY,
            "known_name": "turtle",
            "novel": False,
        },
        "a3": {
            "wall_seconds": a3_wall,
            "stats": a3["stats"],
            "certificate": a3["certificate"],
        },
        "a1_extended": a1,
        "a4_prior_r2_12800": prior_row["full_confirm"],
        "a4_r2_50000": a4,
        "patch_svg": PATCH_SVG.name,
        "spectrum_png": SPECTRUM_PNG.name,
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))
    print(PATCH_SVG.relative_to(ROOT))
    print(SPECTRUM_PNG.relative_to(ROOT))
    print(
        f"A1: {'periodic' if a1['certificate'] else 'no torus'} "
        f"through k={a1['k_max']}; "
        f"A3: {a3['tiles']} tiles; "
        f"A4: rank={a4['result']['rank']} "
        f"sym={a4['result']['symmetry']}"
    )


if __name__ == "__main__":
    main()
