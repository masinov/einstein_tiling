# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-16 (session 06)

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done, validated vs OEIS (session 01) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 corona/Heesch engine | §4 A2 | ✅ done v0, hat = unique n≤8 anomaly (session 03) |
| M3 — A3 large-patch growth | §4 A3 | ✅ done v0, SAT backend; 11,514-tile hat patch, φ⁴ chirality anchor hit (session 04) |
| M4 — A4 diffraction fingerprint | §4 A4 | ✅ done v0; 12-fold core calibration passed (session 05) |
| E4 — full fingerprint calibration gate | §8 E4 | ✅ passed (sessions 05–06) |
| M5 — A6 hierarchy mining | §4 A6 | ⬜ after E4 |
| **Gate G1 — E1 blind hat rediscovery** | §8 E1 | ⬜ blocked by E4 + M5 |
| Pipelines B, C; substrates n=5,8; scaling | §5, §6, §3.3 | ⬜ not started |

**No verdicts on new shapes are trusted before Gate G1 passes** (program §8).

## What exists and is verified

- Exact integer-arithmetic kite substrate (Laves [3.4.6.4]); A0 enumeration
  matches OEIS A057786 exactly n=1..12. (Session 01.)
- **A1 torus periodicity test** with machine-verified certificates
  (`src/einstein/funnel/a1_torus.py`): exact cover of quotient tori over all
  center-sublattices (HNF) up to index budget. Verdicts are three-valued:
  `periodic` (certificate), `no-periodic-at-budget`, `unknown-budget-exhausted`.
- **Shape database** (`src/einstein/db.py`, `data/shapes.sqlite`): 1,264
  shapes (all free polykites n≤8), one A1 verdict each, with budget + code
  version stamps. Batch runner `scripts/run_a1.py` is resumable.
- **A1 validated against Myers' independent census** (same grid-aligned
  scope): periodic-capable counts n=1..8 = 1, 1, 4, 5, 1, 71, 55, 39 —
  exact match at every n; the hat correctly survives as
  `no-periodic-at-budget`. Regression: `tests/test_a1_vs_myers.py`.
- **A2 corona/Heesch engine** (`src/einstein/funnel/a2_heesch.py`): full
  exact H_c census n≤8; the hat is the unique unbounded-corona anomaly
  (session 03).
- **A3 large-patch construction** (`src/einstein/funnel/a3_patch.py`):
  disk exact-cover; SAT (CaDiCaL) workhorse + pure-Python greedy for the
  growth-profile feature (D-0009). All certificates re-verified by our own
  exact code. Hat patches to 11,514 tiles (r2=50000, 220 s); reflected-hat
  density converges to the literature value 1/(1+φ⁴) — an external anchor
  A3 was never told about. Six H_c=2 shapes get pose-free disk-cover
  refutations at r2≤200. Periodic control patch (shape 392) stored for A4.
- **A4 diffraction fingerprint v0**
  (`src/einstein/funnel/a4_diffraction.py`): per-orientation Hann-windowed
  FFT powers on a shared grid, null-calibrated peak detection, sidelobe
  exclusion, bounded-integer module indexing, rotational-symmetry vote and
  crystal/quasicrystal-candidate/diffuse prioritization verdicts.
- **Vendored spectre reference generator** (`vendor/spectre/`) with an exact
  rank-4 anchor dump and independent Python module projection
  (`substrate/module12.py`). Its N=3 Delta output agrees three ways: upstream
  float leaves, Rust exact traversal and our projection; recurrence and
  chirality pins are tested.
- **E4 full calibration gate passed:** the phase-1 random/periodic/hat/spectre
  core is joined by canonical Penrose and Ammann–Beenker cut-and-project
  patches, Taylor–Socolar dyadic hierarchy, and genuine boundary-grown random
  square–triangle tilings. Known ranks/symmetries are recovered; ranks survive
  patch doubling and invertible rotations/shears; 10,000 randomized periodic
  tilers produce zero confirmed quasicrystal false positives. The
  square–triangle ensemble retains broad twelvefold order but is separated
  from pure-point references by background-subtracted narrow-peak mass.
- Wider artifacts: `scripts/run_e4_wide.py`,
  `docs/notebook/assets/e4-wide-results.json`, and
  `e4-spectrum-{penrose,ammann-beenker,taylor-socolar,square-triangle-random}.png`.
- Test suite: **50 fast passed** (12 deselected, 5.65 s);
  **12 slow passed** (50 deselected, 79.45 s).

## Funnel state (polykites, grid-aligned scope — D-0006)

| n | shapes | A1: periodic | A2: H=0 | H=1 | H=2 | grows (anomaly) |
|---|---|---|---|---|---|---|
| 1–3 | 7 | 6 | 1 | — | — | — |
| 4 | 10 | 5 | 4 | 1 | — | — |
| 5 | 27 | 1 | 12 | 14 | — | — |
| 6 | 85 | 71 | 13 | 1 | — | — |
| 7 | 262 | 55 | 165 | 41 | 1 | — |
| 8 | 873 | 39 | 720 | 108 | 5 | **1 — the hat** |

All H values exact by exhaustion (D-0008). **The hat is the unique
unbounded-corona anomaly among all 1,264 free polykites n ≤ 8** — a
mini-E1: Heesch depth alone ranks it #1 in its size class. The six H_c=2
shapes (gallery in notebook 03 assets) are likely novel data — no published
polykite Heesch census exists (Kaplan's covers other polyforms). A3
sharpens the separation: all six are pose-free refuted on disks of r2≤200
(19–35 tiles max), while the hat covers r2=50000 (11,514 tiles).

## Known capacity limits (honest)

- Pure-Python A0: wall at n≈14–15 (E1 needs 16, E2 needs 22–24) — streaming/
  compiled enumerator required before those sweeps.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- A3 single-shot SAT: ~10⁴ tiles (~10⁵ cells, ~10⁷ clauses, ~4 min);
  CNF building/solving scale linearly-ish but 10⁵-tile patches need an
  incremental encoder (assumption-based ring growth) or compiled encoding.
- A3 greedy engine (growth profile): useful to ~10² tiles on hard shapes.
- Funnel v0 sees grid-aligned tilings only (D-0006) — sound positives,
  incomplete negatives; matches the external census scope.
- A4's module indexer remains a bounded greedy numerical estimator rather
  than a general LLL/PSLQ solver (D-0011). E4 supports it for the current
  prioritization role: every known finite-rank reference is correct under
  patch doubling and affine transforms, and the two-resolution periodic
  control gives 0/10,000 confirmed false positives. It is not a proof tool.
- The narrow-peak mass used to distinguish random square–triangle order is
  grid/extent dependent and may only be compared at the shared E4 calibration
  settings. A4 verdicts remain prioritization signals, never spectral-type
  certificates.
- The Spectre source is user-owned and was explicitly supplied for integration
  here. It has no separate license declaration; that matters only if explicit
  third-party reuse terms are wanted later, not for work in this repository.

## Next actions (in order)

1. M5 / A6 hierarchy mining, using the vendored spectre substitution as the
   known answer the reverse-discovery pipeline must recover.
2. Gate G1 planning, then A0 scaling (streaming/compiled enumerator) and the
   A2 performance port required for the n≤16 E1 blind sweep.
3. Deferred: replace the bounded A4 indexer with LLL/PSLQ if future reference
   families or transformed controls break the E4 envelope.
4. Deferred: incremental SAT encoder for 10⁵-tile patches; corona-1 census
   feature; polyiamond substrate (external per-shape Heesch anchor from
   Kaplan's dataset).
