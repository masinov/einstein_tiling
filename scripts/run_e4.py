#!/usr/bin/env python
"""E4 core -- diffraction fingerprint calibration (program section 8).

This runner covers the 12-fold/core subset of the full E4 gate.  Its
reference library is fed through the SAME per-orientation-class
pipeline (the mixed anchor set of a grid-aligned tiling is dominated by
substrate-lattice Bragg peaks; the aperiodic order lives in the
orientation-resolved densities -- program section 4 A4):

  random    uniform points in the hat patch's disk, split into 12 fake
            classes -> must be diffuse; calibrates the peak floor
  periodic  shape 392's A1 torus certificate unfolded over the plane,
            classes = the placements in the fundamental domain
            -> must be rank 2 ("crystal")
  hat       shape 635's A3 disk patch (11,514 anchors), classes = the 12
            symmetry ops -> aperiodic order: rank 4 expected
  spectre   vendored exact generator, level-6 Delta clipped to a centered
            disk, classes = (kind, rotation) -> rank 4, sixfold expected

The complete E4 gate additionally requires the Penrose, Ammann--Beenker,
Taylor--Socolar and random-tiling controls plus stability/false-positive
experiments listed in program section 8.  The pass criteria asserted here
therefore establish only the core sub-gate.  Spectrum images and a JSON
summary go to docs/notebook/assets/.

Usage: venv/bin/python scripts/run_e4.py <spectre-anchors.csv>
(generate the csv: cd vendor/spectre/spectre-core &&
 cargo run --release --bin anchors -- Delta 6 out.csv)
"""

import json
import math
import random
import subprocess
import sys

from einstein.db import ShapeDB
from einstein.funnel.a1_torus import lattice_to_cell
from einstein.funnel.a4_diffraction import (
    class_power_sum,
    detect_peaks,
    fingerprint,
    save_spectrum_pgm,
)
from einstein.render.svg import hex_to_xy
from einstein.substrate.module12 import to_xy as mod_to_xy

ASSETS = "docs/notebook/assets"


def hat_classes(db):
    v = db.latest_verdict(635, "A3-patch")
    cert = v["certificate"]
    assert cert["kind"] == "disk-patch" and cert["r2"] == 50000
    by_op: dict[int, list] = {}
    for op, tx, ty in cert["placements"]:
        by_op.setdefault(op, []).append(hex_to_xy((tx, ty)))
    return list(by_op.values()), cert["r2"]


def periodic_classes(db, radius):
    v = db.latest_verdict(392, "A1-torus")
    assert v["verdict"] == "periodic"
    cert = v["certificate"]
    a, b, d = cert["hnf"]
    classes = []
    reach = int(radius) + 4
    for _, tu, tv in cert["placements"]:
        pts = []
        for m in range(-reach, reach + 1):
            for n in range(-reach, reach + 1):
                u, vv = m * a + n * b + tu, n * d + tv
                cx, cy, _ = lattice_to_cell((u, vv, 0))
                x, y = hex_to_xy((cx, cy))
                if x * x + y * y <= radius * radius:
                    pts.append((x, y))
        classes.append(pts)
    return classes


def spectre_classes(csv_path):
    rows = []
    with open(csv_path) as f:
        next(f)
        for line in f:
            k, _s, r, t0, t1, t2, t3 = line.split(",")
            x, y = mod_to_xy((int(t0), int(t1), int(t2), int(t3)))
            rows.append((int(k), int(r), x, y))
    cx = sum(x for _, _, x, _ in rows) / len(rows)
    cy = sum(y for _, _, _, y in rows) / len(rows)
    xs = sorted(x for _, _, x, _ in rows)
    ys = sorted(y for _, _, _, y in rows)
    half = min(xs[-1] - xs[0], ys[-1] - ys[0]) / 2.0
    rad = 0.55 * half  # centered disk, away from the supertile boundary
    by_class: dict[tuple, list] = {}
    for k, r, x, y in rows:
        if (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad:
            by_class.setdefault((k, r), []).append((x - cx, y - cy))
    return list(by_class.values())


def random_classes(n, radius, k=12, seed=0):
    rng = random.Random(seed)
    classes = [[] for _ in range(k)]
    made = 0
    while made < n:
        x = rng.uniform(-radius, radius)
        y = rng.uniform(-radius, radius)
        if x * x + y * y <= radius * radius:
            classes[made % k].append((x, y))
            made += 1
    return classes


def render(classes, name, floor=0.03, out_size=1024):
    p, _, _ = class_power_sum(classes)
    # central half of k-space, max-pooled so 1-2 px Bragg peaks survive
    g = p.shape[0]
    q = g // 4
    core = p[q:g - q, q:g - q]
    f = core.shape[0] // out_size
    pooled = core.reshape(out_size, f, out_size, f).max(axis=(1, 3))
    pgm = f"/tmp/e4-{name}.pgm"
    save_spectrum_pgm(pooled, pgm, vmax=floor)
    png = f"{ASSETS}/e4-spectrum-{name}.png"
    subprocess.run(["convert", pgm, png], check=True)
    return png


def main(spectre_csv):
    db = ShapeDB("data/shapes.sqlite")
    hat, r2 = hat_classes(db)
    radius = math.sqrt(r2)
    n_hat = sum(len(c) for c in hat)
    refs = {
        "random": random_classes(n_hat, radius),
        "periodic": periodic_classes(db, radius),
        "hat": hat,
        "spectre": spectre_classes(spectre_csv),
    }
    db.close()

    # floor calibration on the random null (same pipeline)
    p, dk, k0 = class_power_sum(refs["random"])
    null_peaks = detect_peaks(p, dk, k0, floor=1e-12, max_peaks=5)
    noise_ceiling = null_peaks[0][2] if null_peaks else 1e-12
    floor = 5.0 * noise_ceiling
    print(f"noise ceiling (random null): {noise_ceiling:.3e} -> floor {floor:.3e}")

    results = {}
    for name, classes in refs.items():
        res = fingerprint(classes=classes, floor=floor)
        results[name] = res
        png = render(classes, name, floor=floor)
        print(f"{name:9s} n={res['n_points']:7d} classes={len(classes):3d} "
              f"peaks={res['n_peaks']:4d} rank={res['rank']} "
              f"sym={res['symmetry']:2d} unindexed={res['unindexed']} "
              f"verdict={res['verdict']}  [{png}]", flush=True)

    with open(f"{ASSETS}/e4-results.json", "w") as f:
        json.dump({"floor": floor, "results": results}, f, indent=1)

    # Pass criteria anchored to Baake-Gaehler-Sadun (arXiv 2502.03268):
    # hat and spectre are pure-point diffractive from 4:2 cut-and-project
    # schemes (Fourier module rank 4) with SIXFOLD symmetry about the
    # origin (chiral sixfold for the spectre; Friedel's law).
    ok = (results["random"]["verdict"] == "diffuse"
          and results["periodic"]["verdict"] == "crystal"
          and results["periodic"]["rank"] == 2
          and results["hat"]["verdict"] == "quasicrystal-candidate"
          and results["hat"]["rank"] == 4
          and results["hat"]["symmetry"] == 6
          and results["spectre"]["verdict"] == "quasicrystal-candidate"
          and results["spectre"]["rank"] == 4
          and results["spectre"]["symmetry"] == 6)
    print("E4 core:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
