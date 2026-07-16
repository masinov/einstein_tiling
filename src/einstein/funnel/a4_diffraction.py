"""A4 -- diffraction fingerprinting (program section 4 A4, milestone M4).

The "new eye": detect aperiodic *order* (not just non-periodicity) in a
large patch, with zero proof effort.  Pipeline:

  anchor points -> Hann-weighted density -> FFT power spectrum
  -> Bragg peak detection (subpixel-refined local maxima above a floor)
  -> module rank estimation (smallest set of generators whose small
     integer combinations reproduce every strong peak)
  -> verdict: rank 2 => crystal; rank >= 4 with many sharp peaks =>
     quasicrystal candidate; no peaks above floor => diffuse.

Floats are permitted here by D-0010: A4 is spectral *analysis*, not
search-path geometry; its output is a prioritization signal gated by the
E4 calibration experiment.  The periodic, random, funnel-grown hat and
vendored spectre patches are the 12-fold/core calibration; the wider E4
reference and robustness suite remains required before any verdict on a
new shape is trusted.

Rank estimation notes: peaks live in the 2D plane, so "rank" means the
rank of the Z-module the peak vectors generate.  We fit greedily: process
strong peaks by increasing |k|; a peak joins the generator set iff no
bounded-integer combination of the current generators reproduces it
within tolerance.  Bounded brute force (|coeff| <= coeff_bound) replaces
LLL/PSLQ at this scale -- strong peaks of real quasicrystals carry small
indices; the E4 controls calibrate the tolerance.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


def power_spectrum(points, grid: int = 2048, pad: float = 1.02,
                   extent=None):
    """Hann-windowed FFT power spectrum of a 2D point set.

    Returns (P, dk, k0): P is the fftshifted power grid normalized so the
    DC (k=0) value is 1; a pixel (i, j) has wavevector
    k = (j - k0) * dk, (i - k0) * dk (angular, radians per length unit).
    `extent` = (center_xy, half_width) pins the window/grid so several
    point sets (orientation classes) share identical k-space sampling.
    """
    pts = np.asarray(points, dtype=np.float64)
    if extent is None:
        lo = pts.min(axis=0)
        hi = pts.max(axis=0)
        center = (lo + hi) / 2.0
        half = float(np.max(hi - lo)) / 2.0 * pad
    else:
        center = np.asarray(extent[0], dtype=np.float64)
        half = float(extent[1]) * pad
    # Hann taper on the disk-normalized radius kills edge ringing
    rel = (pts - center) / half
    w = 0.5 * (1.0 + np.cos(np.pi * np.clip(np.hypot(rel[:, 0], rel[:, 1]), 0, 1)))
    span = 2.0 * half
    ij = np.floor((pts - center + half) / span * grid).astype(np.int64)
    ij = np.clip(ij, 0, grid - 1)
    dens = np.zeros((grid, grid), dtype=np.float64)
    np.add.at(dens, (ij[:, 1], ij[:, 0]), w)
    f = np.fft.fftshift(np.fft.fft2(dens))
    p = np.abs(f) ** 2
    p /= p[grid // 2, grid // 2]
    dk = 2.0 * math.pi / span
    return p, dk, grid // 2


def class_power_sum(point_sets, grid: int = 2048, pad: float = 1.02):
    """Incoherent (power) average of per-class spectra on a shared grid.

    The program's sharpening trick: anchors of a grid-aligned tiling live
    on the substrate lattice, so the mixed point set is dominated by
    lattice Bragg peaks; the aperiodic order sits in the per-orientation
    densities.  Summing per-class powers makes those peaks add while
    class-incoherent noise averages down.  Each class spectrum is
    DC-normalized before averaging, so the result's DC is 1.
    """
    allpts = np.concatenate([np.asarray(p, dtype=np.float64)
                             for p in point_sets if len(p)])
    lo = allpts.min(axis=0)
    hi = allpts.max(axis=0)
    extent = ((lo + hi) / 2.0, float(np.max(hi - lo)) / 2.0)
    acc = None
    dk = k0 = None
    n_used = 0
    for pts in point_sets:
        if len(pts) < 8:
            continue
        p, dk, k0 = power_spectrum(pts, grid=grid, pad=pad, extent=extent)
        acc = p if acc is None else acc + p
        n_used += 1
    return acc / n_used, dk, k0


def detect_peaks(p, dk, k0, k_min: float = 0.15, floor: float = 1e-4,
                 max_peaks: int = 1000, excl_pixels: int = 4):
    """Bragg peak candidates: local maxima of the power grid above
    `floor` (relative to DC), at |k| >= k_min, subpixel-refined by
    parabolic interpolation.  Maxima within `excl_pixels` of a stronger
    accepted peak are suppressed (window sidelobes ring in that zone and
    would otherwise poison the module indexing).  Returns
    [(kx, ky, intensity)] sorted by intensity, strongest first."""
    grid = p.shape[0]
    m = p >= floor
    for ax, sh in itertools.product((0, 1), (1, -1)):
        m &= p >= np.roll(p, sh, axis=ax)
    m &= (p >= np.roll(np.roll(p, 1, 0), 1, 1))
    m &= (p >= np.roll(np.roll(p, 1, 0), -1, 1))
    m &= (p >= np.roll(np.roll(p, -1, 0), 1, 1))
    m &= (p >= np.roll(np.roll(p, -1, 0), -1, 1))
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    ii, jj = np.nonzero(m)
    kx = (jj - k0) * dk
    ky = (ii - k0) * dk
    keep = np.hypot(kx, ky) >= k_min
    ii, jj = ii[keep], jj[keep]
    # exclusion zone, strongest-first
    order = np.argsort(-p[ii, jj])
    taken_i: list[int] = []
    taken_j: list[int] = []
    sel = []
    e2 = excl_pixels * excl_pixels
    for idx in order:
        i, j = int(ii[idx]), int(jj[idx])
        ok = True
        for ti, tj in zip(taken_i, taken_j):
            if (ti - i) ** 2 + (tj - j) ** 2 <= e2:
                ok = False
                break
        if ok:
            taken_i.append(i)
            taken_j.append(j)
            sel.append((i, j))
            if len(sel) >= max_peaks:
                break
    out = []
    tiny = 1e-300
    for i, j in sel:
        # parabolic subpixel refinement, per axis, in log intensity
        c = math.log(max(p[i, j], tiny))
        num_x = math.log(max(p[i, j - 1], tiny)) - math.log(max(p[i, j + 1], tiny))
        den_x = math.log(max(p[i, j - 1], tiny)) + math.log(max(p[i, j + 1], tiny)) - 2 * c
        num_y = math.log(max(p[i - 1, j], tiny)) - math.log(max(p[i + 1, j], tiny))
        den_y = math.log(max(p[i - 1, j], tiny)) + math.log(max(p[i + 1, j], tiny)) - 2 * c
        dx = 0.5 * num_x / den_x if den_x < 0 else 0.0
        dy = 0.5 * num_y / den_y if den_y < 0 else 0.0
        dx = min(max(dx, -0.5), 0.5)
        dy = min(max(dy, -0.5), 0.5)
        out.append(((j + dx - k0) * dk, (i + dy - k0) * dk, float(p[i, j])))
    out.sort(key=lambda t: -t[2])
    return out[:max_peaks]


def index_peaks(peaks, tol: float, max_rank: int = 6, coeff_bound: int = 6,
                top: int = 60, pair_bound: int = 48):
    """Estimate the rank of the Z-module generated by the strongest peak
    vectors.  Greedy: shortest-first among the `top` strongest peaks, a
    peak becomes a new generator iff no bounded integer combination of
    existing generators lands within `tol`.

    Two coefficient bounds: the best-conditioned generator *pair* is
    solved exactly (2x2 system) and allowed indices up to `pair_bound` --
    a periodic patch has lattice peaks with large indices in view --
    while the enumerated coefficients of generators beyond the pair are
    bounded by `coeff_bound` (genuine extra generators of a quasicrystal
    module carry small indices on strong peaks).  This bounded search
    replaces LLL/PSLQ at this scale; the E4 controls calibrate `tol`.

    Returns (rank, generators, unindexed) where unindexed counts peaks
    that neither matched nor were accepted (rank cap hit)."""
    cand = sorted(peaks[:top], key=lambda t: math.hypot(t[0], t[1]))
    gens: list[tuple[float, float]] = []
    unindexed = 0

    def representable(v):
        """Is v within tol of a bounded-integer combination of gens?
        Peaks live in 2D, so only (rank-2) coefficients are free: pick the
        best-conditioned generator pair as the 2x2 solve, enumerate the
        rest, round the solved pair to nearby integers."""
        r = len(gens)
        if r == 0:
            return False
        if r == 1:
            g = gens[0]
            n2 = g[0] * g[0] + g[1] * g[1]
            a = (v[0] * g[0] + v[1] * g[1]) / n2
            for na in (math.floor(a), math.ceil(a)):
                if abs(na) <= pair_bound and math.hypot(
                        v[0] - na * g[0], v[1] - na * g[1]) <= tol:
                    return True
            return False
        # best-conditioned pair -> the solved coordinates
        bi, bj, bdet = 0, 1, 0.0
        for i in range(r):
            for j in range(i + 1, r):
                d = abs(gens[i][0] * gens[j][1] - gens[i][1] * gens[j][0])
                if d > bdet:
                    bi, bj, bdet = i, j, d
        if bdet < 1e-12:
            return False
        gi, gj = gens[bi], gens[bj]
        free = [g for k, g in enumerate(gens) if k not in (bi, bj)]
        rng = range(-coeff_bound, coeff_bound + 1)
        for coeffs in itertools.product(rng, repeat=len(free)):
            rx = v[0] - sum(c * g[0] for c, g in zip(coeffs, free))
            ry = v[1] - sum(c * g[1] for c, g in zip(coeffs, free))
            det = gi[0] * gj[1] - gi[1] * gj[0]
            a = (rx * gj[1] - ry * gj[0]) / det
            b = (gi[0] * ry - gi[1] * rx) / det
            for na in (math.floor(a), math.ceil(a)):
                for nb in (math.floor(b), math.ceil(b)):
                    if abs(na) > pair_bound or abs(nb) > pair_bound:
                        continue
                    dx = rx - na * gi[0] - nb * gj[0]
                    dy = ry - na * gi[1] - nb * gj[1]
                    if math.hypot(dx, dy) <= tol:
                        return True
        return False

    for kx, ky, _ in cand:
        if representable((kx, ky)):
            continue
        if len(gens) < max_rank:
            gens.append((kx, ky))
        else:
            unindexed += 1
    # reduction pass: drop generators representable by the others
    changed = True
    while changed:
        changed = False
        for i in range(len(gens) - 1, -1, -1):
            g = gens.pop(i)
            if not representable(g):
                gens.insert(i, g)
            else:
                changed = True
    return len(gens), gens, unindexed


def rotational_symmetry(peaks, tol: float, top: int = 30):
    """Largest m in {12, 10, 8, 6, 5, 4, 3, 2} such that rotating the `top`
    strongest peaks by 2*pi/m lands on SOME detected peak (within tol);
    1 if none.  Matching against the full detected set (not the top
    slice) keeps intensity noise from breaking the vote."""
    cand = [(kx, ky) for kx, ky, _ in peaks[:top]]
    allp = [(kx, ky) for kx, ky, _ in peaks]
    if not cand:
        return 1
    for m in (12, 10, 8, 6, 5, 4, 3, 2):
        a = 2.0 * math.pi / m
        c, s = math.cos(a), math.sin(a)
        ok = all(
            any(math.hypot(c * x - s * y - qx, s * x + c * y - qy) <= tol
                for qx, qy in allp)
            for x, y in cand
        )
        if ok:
            return m
    return 1


def peak_mass_fraction(p, peaks, dk, k0, radius_pixels: int = 2,
                       dc_pixels: int = 4):
    """Fraction of non-DC spectral power concentrated near detected peaks.

    This is a finite-patch proxy for the pure-point fraction requested by
    A4/E4, not a mathematical Lebesgue-decomposition claim.  We integrate
    disks of `radius_pixels` around the detected maxima and divide by all
    power outside a small DC disk.  The E4 reference/null suite calibrates
    its interpretation.
    """
    grid = p.shape[0]
    yy, xx = np.ogrid[:grid, :grid]
    dc = (xx - k0) ** 2 + (yy - k0) ** 2 <= dc_pixels * dc_pixels
    total = float(p[~dc].sum())
    if total <= 0.0 or not peaks:
        return 0.0
    mask = np.zeros_like(p, dtype=bool)
    r2 = radius_pixels * radius_pixels
    for kx, ky, _ in peaks:
        j = int(round(kx / dk + k0))
        i = int(round(ky / dk + k0))
        i0, i1 = max(0, i - radius_pixels), min(grid, i + radius_pixels + 1)
        j0, j1 = max(0, j - radius_pixels), min(grid, j + radius_pixels + 1)
        sy, sx = np.ogrid[i0:i1, j0:j1]
        mask[i0:i1, j0:j1] |= (sx - j) ** 2 + (sy - i) ** 2 <= r2
    mask &= ~dc
    return float(p[mask].sum()) / total


def sharp_peak_mass_fraction(p, peaks, dk, k0, top: int = 100,
                             radius_pixels: int = 2,
                             background_inner: int = 5,
                             background_outer: int = 8,
                             dc_pixels: int = 4):
    """Background-subtracted mass in the strongest narrow peaks.

    This is the E4 random-tiling discriminator.  A finite-window Bragg peak
    concentrates power in a small core above its local annular background;
    broad diffuse maxima do not.  The value is a calibration statistic and
    must only be compared at a shared FFT grid and rendering extent.
    """
    p = np.asarray(p)
    grid = p.shape[0]
    yy, xx = np.ogrid[
        -background_outer:background_outer + 1,
        -background_outer:background_outer + 1,
    ]
    rr = xx * xx + yy * yy
    core = rr <= radius_pixels * radius_pixels
    annulus = (
        (rr >= background_inner * background_inner)
        & (rr <= background_outer * background_outer)
    )
    used = np.zeros_like(p, dtype=bool)
    excess = 0.0
    for kx, ky, _ in peaks[:top]:
        j = int(round(kx / dk + k0))
        i = int(round(ky / dk + k0))
        r = background_outer
        if i < r or j < r or i >= grid - r or j >= grid - r:
            continue
        window = p[i - r:i + r + 1, j - r:j + r + 1]
        background = float(np.median(window[annulus]))
        fresh = core & ~used[i - r:i + r + 1, j - r:j + r + 1]
        excess += float(np.maximum(window[fresh] - background, 0.0).sum())
        used[i - r:i + r + 1, j - r:j + r + 1][core] = True
    total_mask = np.ones_like(p, dtype=bool)
    total_mask[
        k0 - dc_pixels:k0 + dc_pixels + 1,
        k0 - dc_pixels:k0 + dc_pixels + 1,
    ] = False
    total = float(p[total_mask].sum())
    return excess / total if total else 0.0


def dyadic_scale_depth(peaks, base_radius: float, tol: float,
                       max_depth: int = 12):
    """Number of consecutively halved reciprocal scales in a peak set.

    Taylor--Socolar order is limit-periodic: its level-n triangular pattern
    has real-space lattice constant 2^n a0 and reciprocal scale 2^-n b0.
    Starting on the known base reciprocal shell, count how many vectors
    k, k/2, k/4, ... are detected.  A plain triangular lattice stops at one.
    """
    vectors = [(kx, ky) for kx, ky, _ in peaks]
    best = 0
    for kx, ky in vectors:
        if abs(math.hypot(kx, ky) - base_radius) > 3.0 * tol:
            continue
        depth = 0
        for level in range(max_depth):
            tx, ty = kx / (2 ** level), ky / (2 ** level)
            if any(math.hypot(tx - qx, ty - qy) <= tol
                   for qx, qy in vectors):
                depth += 1
            else:
                break
        best = max(best, depth)
    return best


def fingerprint(points=None, classes=None, grid: int = 2048,
                k_min: float = 0.15, floor: float = 1e-4,
                tol_pixels: float = 2.0, max_rank: int = 6,
                coeff_bound: int = 6, top: int = 150):
    """Full A4 fingerprint.  Pass either one point set (`points`) or a
    list of per-orientation-class point sets (`classes`, preferred for
    grid-aligned tilings -- the mixed set is dominated by substrate
    lattice peaks; the per-class powers carry the aperiodic order).
    Returns a dict (power spectrum left out; recompute for rendering):

      n_points, n_peaks, rank, generators, unindexed, symmetry,
      peak_mass_fraction, sharp_peak_mass_fraction,
      strongest (top-10 peaks), verdict
    """
    if classes is not None:
        p, dk, k0 = class_power_sum(classes, grid=grid)
        n_points = sum(len(c) for c in classes)
    else:
        p, dk, k0 = power_spectrum(points, grid=grid)
        n_points = len(points)
    peaks = detect_peaks(p, dk, k0, k_min=k_min, floor=floor)
    tol = tol_pixels * dk
    if not peaks:
        return {"n_points": n_points, "n_peaks": 0, "rank": 0,
                "generators": [], "unindexed": 0, "symmetry": 1,
                "peak_mass_fraction": 0.0,
                "sharp_peak_mass_fraction": 0.0, "strongest": [],
                "verdict": "diffuse"}
    rank, gens, unindexed = index_peaks(
        peaks, tol, max_rank=max_rank, coeff_bound=coeff_bound, top=top)
    sym = rotational_symmetry(peaks, tol)
    if rank <= 2:
        verdict = "crystal"
    elif rank >= 4:
        verdict = "quasicrystal-candidate"
    else:
        verdict = f"rank-{rank}"
    return {
        "n_points": n_points,
        "n_peaks": len(peaks),
        "rank": rank,
        "generators": [[g[0], g[1]] for g in gens],
        "unindexed": unindexed,
        "symmetry": sym,
        "peak_mass_fraction": peak_mass_fraction(p, peaks, dk, k0),
        "sharp_peak_mass_fraction": sharp_peak_mass_fraction(
            p, peaks, dk, k0,
        ),
        "strongest": [[kx, ky, v] for kx, ky, v in peaks[:10]],
        "verdict": verdict,
    }


def save_spectrum_pgm(p, path: str, vmax: float = 0.03,
                      gamma: float = 0.5):
    """Grayscale dump of a power grid (render only): values at or above
    `vmax` (typically the peak floor) saturate white; the noise
    background stays near black."""
    img = np.power(np.clip(p / vmax, 0.0, 1.0), gamma)
    img = (img * 255).astype(np.uint8)
    with open(path, "wb") as f:
        f.write(f"P5\n{img.shape[1]} {img.shape[0]}\n255\n".encode())
        f.write(img[::-1].tobytes())
