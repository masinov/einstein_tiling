#!/usr/bin/env python
"""Two-scale A4 diffraction screen for A3-grown blind candidates.

Uses a deterministic random null with the same orientation-class populations
as each patch.  The central crop and full patch are fingerprinted at grid
1024; full patches provisionally ranked >=4 are confirmed at grid 2048.
Full-patch spectra are rendered for human inspection.

Usage:
  venv/bin/python scripts/archive/run_a4_candidates.py
"""

from __future__ import annotations

import json
import math
import random
import subprocess
from pathlib import Path

from einstein.analysis.diffraction import (
    class_power_sum,
    detect_peaks,
    fingerprint,
    save_spectrum_pgm,
)
from einstein.polykites.known_shapes import (
    PUBLISHED_APERIODIC_POLYKITE_HORIZON,
    aperiodic_discovery_status,
)
from einstein.visualization.kite_svg import hex_to_xy

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "docs" / "notebook" / "assets"
A3_RESULTS = ASSETS / "a3-small-candidate-results.json"
OUTPUT = ASSETS / "a4-small-candidate-results.json"
GALLERY = ASSETS / "a4-small-candidate-spectra.svg"


def placement_classes(cert, crop_r2=None):
    rows = [
        (op, *hex_to_xy((tx, ty)))
        for op, tx, ty in cert["placements"]
    ]
    cx = sum(x for _, x, _ in rows) / len(rows)
    cy = sum(y for _, _, y in rows) / len(rows)
    by_op = {}
    for op, x, y in rows:
        x -= cx
        y -= cy
        if crop_r2 is None or x * x + y * y <= crop_r2:
            by_op.setdefault(op, []).append((x, y))
    return [points for points in by_op.values() if len(points) >= 8]


def matched_null(classes, radius, seed):
    rng = random.Random(seed)
    out = []
    for points in classes:
        random_points = []
        for _ in points:
            r = radius * math.sqrt(rng.random())
            angle = 2 * math.pi * rng.random()
            random_points.append((r * math.cos(angle), r * math.sin(angle)))
        out.append(random_points)
    return out


def calibrated_fingerprint(classes, radius, seed, grid):
    null = matched_null(classes, radius, seed)
    power, dk, k0 = class_power_sum(null, grid=grid)
    null_peaks = detect_peaks(
        power, dk, k0, floor=1e-12, max_peaks=5
    )
    noise_ceiling = null_peaks[0][2] if null_peaks else 1e-12
    floor = 5 * noise_ceiling
    result = fingerprint(classes=classes, grid=grid, floor=floor)
    return floor, result


def render_spectrum(classes, floor, name):
    power, _, _ = class_power_sum(classes, grid=2048)
    grid = power.shape[0]
    quarter = grid // 4
    core = power[quarter:grid - quarter, quarter:grid - quarter]
    pgm = Path("/tmp") / f"{name}.pgm"
    save_spectrum_pgm(core, str(pgm), vmax=floor)
    png = ASSETS / f"{name}.png"
    subprocess.run(["convert", str(pgm), str(png)], check=True)
    return png


def write_gallery(rows):
    panel = 360
    columns = 3
    width = columns * panel
    height = math.ceil(len(rows) / columns) * (panel + 48)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#11151c"/>',
    ]
    for i, row in enumerate(rows):
        shape_label = (
            f'known {row["known_name"].title()}'
            if row.get("known_name")
            else f'candidate {row["index"]}'
        )
        x = (i % columns) * panel
        y = (i // columns) * (panel + 48)
        confirm = row["full_confirm"]
        periodic = row["exact_a1"]["verdict"] == "periodic"
        color = (
            "#74c0fc" if periodic
            else "#51cf66" if confirm["rank"] >= 4
            else "#ffd43b"
        )
        verdict = (
            f'exact periodic · torus index '
            f'{row["exact_a1"]["certificate_index"]}'
            if periodic
            else f'rank {confirm["rank"]} · sym {confirm["symmetry"]} · '
                 f'{confirm["verdict"]}'
        )
        parts.extend([
            (
                f'<image x="{x}" y="{y}" width="{panel}" height="{panel}" '
                f'href="{row["spectrum_png"]}" '
                f'xlink:href="{row["spectrum_png"]}"/>'
            ),
            (
                f'<text x="{x + panel / 2}" y="{y + panel + 19}" '
                'fill="#f8f9fa" font-family="sans-serif" font-size="14" '
                f'font-weight="700" text-anchor="middle">n={row["n"]} '
                f'{shape_label}</text>'
            ),
            (
                f'<text x="{x + panel / 2}" y="{y + panel + 38}" '
                f'fill="{color}" font-family="sans-serif" font-size="12" '
                f'text-anchor="middle">{verdict}</text>'
            ),
        ])
    parts.append("</svg>")
    GALLERY.write_text("\n".join(parts) + "\n")


def main():
    source = json.loads(A3_RESULTS.read_text())
    exact_source = json.loads(
        (ASSETS / "a1-extended-small-candidate-results.json").read_text()
    )
    exact = {
        (row["n"], row["index"]): row
        for row in exact_source["results"]
    }
    rows = []
    for candidate in source["results"]:
        final = candidate["ladder"][-1]
        if final["status"] != "grown":
            continue
        cert = candidate["largest_certificate"]
        full = placement_classes(cert)
        crop = placement_classes(cert, crop_r2=3200)
        seed = 1000 * candidate["n"] + candidate["index"]
        crop_floor, crop_result = calibrated_fingerprint(
            crop, math.sqrt(3200), seed, grid=1024
        )
        full_floor, full_result = calibrated_fingerprint(
            full, math.sqrt(cert["r2"]), seed + 100, grid=1024
        )
        confirm_floor, confirm_result = calibrated_fingerprint(
            full, math.sqrt(cert["r2"]), seed + 200, grid=2048
        )
        name = (
            f"a4-candidate-n{candidate['n']:02}-"
            f"{candidate['index']:02}-spectrum"
        )
        png = render_spectrum(full, confirm_floor, name)
        discovery_status = aperiodic_discovery_status(
            candidate["n"], candidate["shape"]
        )
        row = {
            "n": candidate["n"],
            "index": candidate["index"],
            "shape": candidate["shape"],
            "known_name": candidate.get("known_name"),
            "novel_key": candidate.get(
                "novel_key", candidate.get("known_name") is None
            ),
            "aperiodic_discovery_status": discovery_status,
            "novel": discovery_status == "eligible",
            "patch_r2": cert["r2"],
            "patch_tiles": cert["tiles"],
            "crop_classes": [len(points) for points in crop],
            "full_classes": [len(points) for points in full],
            "crop_floor": crop_floor,
            "full_floor": full_floor,
            "confirm_floor": confirm_floor,
            "crop": crop_result,
            "full": full_result,
            "full_confirm": confirm_result,
            "exact_a1": {
                "verdict": exact[
                    (candidate["n"], candidate["index"])
                ]["verdict"],
                "certificate_index": (
                    exact[(candidate["n"], candidate["index"])]
                    ["certificate"]["index"]
                    if exact[(candidate["n"], candidate["index"])]
                    ["certificate"] is not None
                    else None
                ),
            },
            "spectrum_png": png.name,
        }
        rows.append(row)
        print(
            f"n={row['n']} candidate {row['index']}: "
            f"crop rank={crop_result['rank']} sym={crop_result['symmetry']}; "
            f"full rank={full_result['rank']} sym={full_result['symmetry']}; "
            f"confirm rank={confirm_result['rank']} "
            f"sym={confirm_result['symmetry']}",
            flush=True,
        )

    payload = {
        "kind": "matched-null-two-scale-a4-candidate-screen",
        "literature_scope": {
            "published_aperiodic_polykite_horizon": (
                PUBLISHED_APERIODIC_POLYKITE_HORIZON
            ),
            "all_rows_are_validation_not_discovery": True,
            "controlling_correction": "ERR-004/D-0049",
        },
        "screen_grid": 1024,
        "confirm_grid": 2048,
        "crop_r2": 3200,
        "results": rows,
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    write_gallery(rows)
    print(OUTPUT.relative_to(ROOT))
    print(GALLERY.relative_to(ROOT))


if __name__ == "__main__":
    main()
