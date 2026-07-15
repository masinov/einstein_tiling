# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-16 (session 03)

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done, validated vs OEIS (session 01) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 corona/Heesch engine | §4 A2 | ✅ done v0, hat = unique n≤8 anomaly (session 03) |
| M3 — A3 large-patch growth | §4 A3 | ⬜ next |
| M4 — A4 diffraction fingerprint + E4 calibration | §4 A4, E4 | ⬜ |
| M5 — A6 hierarchy mining | §4 A6 | ⬜ |
| **Gate G1 — E1 blind hat rediscovery** | §8 E1 | ⬜ blocked by M2–M5 |
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
- Test suite: 23 tests. Fast ~2 s; `-m slow` ~40 s (OEIS n=10 + Myers n=8).

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
polykite Heesch census exists (Kaplan's covers other polyforms).

## Known capacity limits (honest)

- Pure-Python A0: wall at n≈14–15 (E1 needs 16, E2 needs 22–24) — streaming/
  compiled enumerator required before those sweeps.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- Funnel v0 sees grid-aligned tilings only (D-0006) — sound positives,
  incomplete negatives; matches the external census scope.

## Next actions (in order)

1. M3 / A3: large-patch growth for anomalies (SAT seed + frontier extension
   per §4 A3) — needed to give A4 its 10⁵+-point input. The hat is the
   pilot anomaly.
2. M4 / A4: diffraction fingerprint + E4 calibration (reference library:
   at minimum hat patches + a periodic control + a random control).
3. A0 scaling (streaming/compiled enumerator) + A2 performance port —
   prerequisites for the n≤16 E1 blind sweep.
4. Deferred: corona-1 census feature; polyiamond substrate (would add an
   external per-shape Heesch anchor from Kaplan's dataset).
