#!/usr/bin/env python
"""Wider E4: complete reference, stability and false-positive gates.

This expands the 12-fold core run with:
  - canonical Penrose (Z^5 projection) and Ammann--Beenker (Z^4 projection)
    vertex sets, expected Fourier-module rank 4 and symmetries 10 and 8;
  - patch-size doubling checks;
  - rotated and deliberately sheared copies (rank must remain 4);
  - 10,000 randomized Bravais-lattice parallelogram tilings, whose
    quasicrystal-candidate false-positive rate must be below 1e-3.
  - a Taylor--Socolar dyadic reciprocal hierarchy diagnostic;
  - an ensemble of genuine boundary-grown random square--triangle tilings,
    which must retain broad twelvefold order without narrow pure-point mass.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import math
import os
import random
import subprocess

import numpy as np

from einstein.analysis.diffraction import (
    class_power_sum,
    detect_peaks,
    dyadic_scale_depth,
    fingerprint,
    index_peaks,
    power_spectrum,
    rotational_symmetry,
    save_spectrum_pgm,
    sharp_peak_mass_fraction,
)
from einstein.analysis.benchmarks.limit_periodic import (
    TRIANGULAR_RECIPROCAL_RADIUS,
    taylor_socolar_hierarchy_classes,
)
from einstein.analysis.benchmarks.model_sets import (
    model_set_points,
    random_periodic_points,
    transform_points,
)
from einstein.analysis.benchmarks.square_triangle import random_square_triangle_patch

ASSETS = "docs/notebook/assets"


def random_disk(n, radius, seed):
    rng = random.Random(seed)
    points = []
    while len(points) < n:
        x, y = rng.uniform(-radius, radius), rng.uniform(-radius, radius)
        if x * x + y * y <= radius * radius:
            points.append((x, y))
    return points


def calibrated_floor(points, seed, grid=2048):
    radius = max(math.hypot(*p) for p in points)
    null = random_disk(len(points), radius, seed)
    power, dk, k0 = power_spectrum(null, grid=grid)
    peaks = detect_peaks(power, dk, k0, floor=1e-12, max_peaks=3)
    return 5.0 * peaks[0][2]


def analyze(points, seed, grid=2048):
    floor = calibrated_floor(points, seed, grid=grid)
    result = fingerprint(points=points, floor=floor, grid=grid)
    result["floor"] = floor
    return result


def render_power(power, name, floor, out_size=1024, crop_divisor=2):
    grid = power.shape[0]
    core_size = grid // crop_divisor
    lo = (grid - core_size) // 2
    core = power[lo:lo + core_size, lo:lo + core_size]
    factor = core.shape[0] // out_size
    pooled = core.reshape(out_size, factor, out_size, factor).max(axis=(1, 3))
    pgm = f"/tmp/e4-wide-{name}.pgm"
    save_spectrum_pgm(pooled, pgm, vmax=floor)
    png = f"{ASSETS}/e4-spectrum-{name}.png"
    subprocess.run(["convert", pgm, png], check=True)
    return png


def render(points, name, floor, grid=2048, out_size=1024):
    power, _, _ = power_spectrum(points, grid=grid)
    return render_power(power, name, floor, out_size=out_size)


def render_peak_map(peaks, name, k_max, out_size=1024):
    """Render detected low-k peaks without the dense lattice background."""
    image = np.zeros((out_size, out_size), dtype=np.float64)
    center = out_size // 2
    scale = 0.48 * out_size / k_max
    yy, xx = np.ogrid[-2:3, -2:3]
    disk = xx * xx + yy * yy <= 4
    for kx, ky, intensity in peaks:
        if math.hypot(kx, ky) > k_max:
            continue
        j = int(round(center + scale * kx))
        i = int(round(center + scale * ky))
        if i < 2 or j < 2 or i >= out_size - 2 or j >= out_size - 2:
            continue
        window = image[i - 2:i + 3, j - 2:j + 3]
        window[disk] = np.maximum(window[disk], intensity)
    pgm = f"/tmp/e4-wide-{name}.pgm"
    save_spectrum_pgm(image, pgm, vmax=0.25)
    png = f"{ASSETS}/e4-spectrum-{name}.png"
    subprocess.run(["convert", pgm, png], check=True)
    return png


def periodic_batch(args):
    start, count, grid = args
    rank_counts: dict[int, int] = {}
    false_positives = []
    ambiguous = 0
    for seed in range(start, start + count):
        points = random_periodic_points(seed)
        result = fingerprint(
            points=points, grid=grid, floor=0.04, k_min=0.3, top=60,
        )
        rank = result["rank"]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
        if result["verdict"] == "quasicrystal-candidate":
            false_positives.append(seed)
        elif result["verdict"] != "crystal":
            ambiguous += 1
    return rank_counts, false_positives, ambiguous


def periodic_false_positive_trial(total, workers, grid):
    chunk = math.ceil(total / workers)
    jobs = []
    for start in range(0, total, chunk):
        jobs.append((start, min(chunk, total - start), grid))
    rank_counts: dict[int, int] = {}
    false_positives = []
    ambiguous = 0
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for counts, bad, amb in pool.map(periodic_batch, jobs):
            for rank, count in counts.items():
                rank_counts[rank] = rank_counts.get(rank, 0) + count
            false_positives.extend(bad)
            ambiguous += amb
    screening_false_positives = sorted(false_positives)
    confirmed = []
    for seed in screening_false_positives:
        result = fingerprint(
            points=random_periodic_points(seed),
            grid=256, floor=0.04, k_min=0.3, top=60,
        )
        if result["verdict"] == "quasicrystal-candidate":
            confirmed.append(seed)
    return {
        "n": total,
        "screening_grid": grid,
        "confirmation_grid": 256,
        "rank_counts": {str(k): v for k, v in sorted(rank_counts.items())},
        "screening_false_positives": screening_false_positives,
        "screening_false_positive_rate": len(screening_false_positives) / total,
        "confirmed_false_positives": confirmed,
        "false_positive_rate": len(confirmed) / total,
        "ambiguous_noncrystal": ambiguous,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--periodic-count", type=int, default=10_000)
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument("--periodic-grid", type=int, default=192)
    parser.add_argument("--square-triangle-samples", type=int, default=4)
    parser.add_argument("--square-triangle-tiles", type=int, default=3_000)
    args = parser.parse_args()

    specs = {
        "penrose": {"bounds": (7, 11), "symmetry": 10},
        "ammann-beenker": {"bounds": (10, 18), "symmetry": 8},
    }
    references = {}
    stability = {}
    transforms = {}

    for ri, (name, spec) in enumerate(specs.items()):
        per_size = []
        for bound in spec["bounds"]:
            points = model_set_points(name, bound)
            result = analyze(points, seed=100 + ri * 10 + bound)
            per_size.append({"bound": bound, **result})
            print(
                f"{name:15s} bound={bound:2d} n={len(points):5d} "
                f"rank={result['rank']} sym={result['symmetry']:2d} "
                f"mass={result['peak_mass_fraction']:.3f}",
                flush=True,
            )
        references[name] = per_size[-1]
        stability[name] = {
            "sizes": per_size,
            "rank_stable": all(x["rank"] == 4 for x in per_size),
            "symmetry_stable": all(
                x["symmetry"] == spec["symmetry"] for x in per_size
            ),
        }

        full = model_set_points(name, spec["bounds"][-1])
        moved_results = []
        for label, angle, shear in (
            ("rotated", 0.37, 0.0),
            ("sheared", 0.61, -0.13),
        ):
            moved = transform_points(full, angle=angle, shear=shear)
            result = analyze(moved, seed=300 + ri * 10 + len(moved_results))
            moved_results.append({"kind": label, **result})
            print(
                f"{name:15s} {label:7s} rank={result['rank']} "
                f"sym={result['symmetry']:2d}",
                flush=True,
            )
        transforms[name] = {
            "cases": moved_results,
            "rank_stable": all(x["rank"] == 4 for x in moved_results),
        }
        render(full, name, per_size[-1]["floor"])

    ts_classes = taylor_socolar_hierarchy_classes()
    ts_power, ts_dk, ts_k0 = class_power_sum(ts_classes)
    ts_peaks = detect_peaks(ts_power, ts_dk, ts_k0, floor=0.02)
    ts_depth = dyadic_scale_depth(
        ts_peaks, TRIANGULAR_RECIPROCAL_RADIUS, tol=2.0 * ts_dk,
    )
    flat_power, flat_dk, flat_k0 = class_power_sum([
        [point for level in ts_classes for point in level]
    ])
    flat_peaks = detect_peaks(flat_power, flat_dk, flat_k0, floor=0.02)
    flat_depth = dyadic_scale_depth(
        flat_peaks, TRIANGULAR_RECIPROCAL_RADIUS, tol=2.0 * flat_dk,
    )
    ts_fingerprint = fingerprint(classes=ts_classes, floor=0.02)
    taylor_socolar = {
        "n_points": sum(len(level) for level in ts_classes),
        "level_counts": [len(level) for level in ts_classes],
        "symmetry": ts_fingerprint["symmetry"],
        "finite_rank_estimate": ts_fingerprint["rank"],
        "dyadic_depth": ts_depth,
        "erased_hierarchy_depth": flat_depth,
        "pass": ts_depth >= 5 and flat_depth == 1
                and ts_fingerprint["symmetry"] == 6,
    }
    render_peak_map(
        ts_peaks, "taylor-socolar",
        k_max=1.1 * TRIANGULAR_RECIPROCAL_RADIUS,
    )
    print(
        f"taylor-socolar  n={taylor_socolar['n_points']:5d} "
        f"dyadic-depth={ts_depth} erased={flat_depth} "
        f"sym={ts_fingerprint['symmetry']}",
        flush=True,
    )

    square_triangle_sets = []
    square_triangle_samples = []
    for seed in range(args.square_triangle_samples):
        patch = random_square_triangle_patch(
            10_000 + seed,
            target_tiles=args.square_triangle_tiles,
            mixing=0.75,
        )
        square_triangle_sets.append(patch.points)
        triangles = patch.tile_types.count(3)
        squares = patch.tile_types.count(4)
        square_triangle_samples.append({
            "seed": 10_000 + seed,
            "tiles": len(patch.polygons),
            "vertices": len(patch.points),
            "triangles": triangles,
            "squares": squares,
            "triangle_square_ratio": triangles / squares,
            "crop_center": patch.crop_center,
            "crop_radius": patch.crop_radius,
            "rejected_moves": patch.rejected_moves,
        })
    st_power, st_dk, st_k0 = class_power_sum(
        square_triangle_sets, grid=1024,
    )
    st_peaks = detect_peaks(
        st_power, st_dk, st_k0, floor=0.005, max_peaks=1000,
    )
    st_rank, _, st_unindexed = index_peaks(
        st_peaks, 2.0 * st_dk, top=150,
    )
    st_symmetry = rotational_symmetry(st_peaks, 2.0 * st_dk)
    st_sharp_mass = sharp_peak_mass_fraction(
        st_power, st_peaks, st_dk, st_k0,
    )
    square_triangle = {
        "samples": square_triangle_samples,
        "ensemble_grid": 1024,
        "n_peaks": len(st_peaks),
        "naive_rank": st_rank,
        "symmetry": st_symmetry,
        "unindexed": st_unindexed,
        "sharp_peak_mass_fraction": st_sharp_mass,
        "verdict": (
            "diffuse-ordered" if st_sharp_mass < 0.025
            else "false-pure-point"
        ),
        "pass": (
            st_rank == 4
            and st_symmetry == 12
            and st_sharp_mass < 0.025
        ),
    }
    render_power(
        st_power, "square-triangle-random", floor=0.025, out_size=512,
    )
    print(
        f"square-triangle samples={len(square_triangle_sets)} "
        f"rank={st_rank} sym={st_symmetry} "
        f"sharp-mass={st_sharp_mass:.4f} "
        f"verdict={square_triangle['verdict']}",
        flush=True,
    )

    print(
        f"periodic controls n={args.periodic_count} grid={args.periodic_grid} "
        f"workers={args.workers}",
        flush=True,
    )
    periodic = periodic_false_positive_trial(
        args.periodic_count, args.workers, args.periodic_grid,
    )
    print(
        f"periodic screen={len(periodic['screening_false_positives'])} "
        f"confirmed={len(periodic['confirmed_false_positives'])} "
        f"rate={periodic['false_positive_rate']:.3e} "
        f"ambiguous={periodic['ambiguous_noncrystal']}",
        flush=True,
    )

    phase2_pass = (
        all(x["rank"] == 4 for x in references.values())
        and references["penrose"]["symmetry"] == 10
        and references["ammann-beenker"]["symmetry"] == 8
        and all(x["rank_stable"] and x["symmetry_stable"]
                for x in stability.values())
        and all(x["rank_stable"] for x in transforms.values())
        and periodic["false_positive_rate"] < 1e-3
    )
    full_e4_pass = (
        phase2_pass
        and taylor_socolar["pass"]
        and square_triangle["pass"]
    )
    output = {
        "references": references,
        "stability": stability,
        "transforms": transforms,
        "periodic_trial": periodic,
        "taylor_socolar": taylor_socolar,
        "square_triangle_random": square_triangle,
        "phase2_pass": phase2_pass,
        "full_e4_pass": full_e4_pass,
        "remaining": [] if full_e4_pass else [
            name for name, passed in (
                ("phase2", phase2_pass),
                ("taylor-socolar", taylor_socolar["pass"]),
                ("random-square-triangle", square_triangle["pass"]),
            ) if not passed
        ],
    }
    with open(f"{ASSETS}/e4-wide-results.json", "w") as f:
        json.dump(output, f, indent=1)
    print("E4 wide:", "PASS" if full_e4_pass else "FAIL")
    return 0 if full_e4_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
