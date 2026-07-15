# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-16 (session 02)

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done, validated vs OEIS (session 01) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 SAT Heesch engine | §4 A2 | ⬜ next |
| M3 — A3 large-patch growth | §4 A3 | ⬜ |
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

| n | shapes | A1: periodic | A1 survivors (candidates ∪ non-tilers) |
|---|---|---|---|
| 1–3 | 7 | 6 | 1 |
| 4 | 10 | 5 | 5 |
| 5 | 27 | 1 | 26 |
| 6 | 85 | 71 | 14 |
| 7 | 262 | 55 | 207 |
| 8 | 873 | 39 | 834 (hat among them) |

Separating einstein candidates from plain non-tilers within the survivors is
A2's job (Heesch depth / corona growth).

## Known capacity limits (honest)

- Pure-Python A0: wall at n≈14–15 (E1 needs 16, E2 needs 22–24) — streaming/
  compiled enumerator required before those sweeps.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- Funnel v0 sees grid-aligned tilings only (D-0006) — sound positives,
  incomplete negatives; matches the external census scope.

## Next actions (in order)

1. M2 / A2: SAT-driven corona growth (Heesch engine). First decision: SAT
   dependency (python-sat vs kissat subprocess vs keep exact-cover core for
   corona-1 and profile). Validation anchors: known Heesch numbers for
   non-tiling polykites (Myers lists Heesch data), hat coronas must grow
   indefinitely (test to some depth).
2. A2 output feeds anomaly stats: corona-1 census + Heesch depth per A1
   survivor into the DB.
3. Then A3/A4 per program order.
