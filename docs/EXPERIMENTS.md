# Experiment registry

The ten experiments defined in the program (§8), with live status.
Rule from the program: **E1–E4 are validation gates — no verdict on a new
shape is publishable/trustable until they pass.** Every experiment run must
leave an entry here linking to its notebook session and artifacts.

| ID | Name | Kind | Status | Depends on | Evidence |
|---|---|---|---|---|---|
| E1 | Blind rediscovery of the hat | validation gate | **not started** | funnel A0–A4+A6 (M1–M5) | — |
| E2 | Exhaustive 12-fold sweep beyond known horizon | discovery | not started | E1 pass, scaled A0 | — |
| E3 | First hunts in 5-fold / 8-fold substrates | discovery | not started | E1 pass, new substrates | — |
| E4 | Diffraction fingerprint calibration | validation gate | not started | A4 (M4), reference library | — |
| E5 | ML allocation A/B | methodology | not started | funnel verdicts corpus | — |
| E6 | Inverse-design season (Pipeline B) | discovery | not started | B1–B3 build | — |
| E7 | Moduli prospecting season (Pipeline C) | discovery | not started | C1–C2 build | — |
| E8 | Convex exhaustion (negative program) | formalization | not started | Lean track | — |
| E9 | 3D pilot | moonshot | not started | 2D funnel mature | — |
| E10 | Certification & formalization track | continuous | not started | — | — |

## Pre-experiment validation log

Work that doesn't belong to a numbered experiment but gates them
(infrastructure correctness). Append-only.

| Date | What was validated | Method | Result | Where |
|---|---|---|---|---|
| 2026-07-15 | Kite substrate geometry & symmetry action | exact self-consistency tests (14 tests) | pass | `tests/test_kitegrid.py`, [notebook 01](notebook/2026-07-15-session-01.md) |
| 2026-07-15 | A0 free polykite counts n=1..12 | match vs OEIS A057786 (independent: B. Owen / J. Myers) | exact match | `tests/test_enumeration.py`, [notebook 01](notebook/2026-07-15-session-01.md) |
| 2026-07-15 | Hat embedding + recovery + membership in enumeration | Kaplan's hatviz outline (verbatim) end-to-end | pass | `tests/test_hat.py`, [assets/hat-recovered.svg](notebook/assets/hat-recovered.svg) |
| 2026-07-16 | A1 torus test: periodic-capable counts n=1..8 | match vs J. Myers' polykite census (independent, 2023; same grid-aligned scope) | exact match (1,1,4,5,1,71,55,39) | `tests/test_a1_vs_myers.py`, [notebook 02](notebook/2026-07-16-session-02.md) |
| 2026-07-16 | A1 soundness on the hat (proven aperiodic) | no certificate may exist; sweep k≤12 (also k≤8 in fast test) | pass (`no-periodic-at-budget`) | `tests/test_a1_torus.py`, DB shape 635 |
| 2026-07-16 | Certificate verifier rejects tampering | drop/duplicate placements must fail verification | pass | `tests/test_a1_torus.py` |
| 2026-07-16 | A2 corona engine: tilers grow, non-tilers halt | single kite + hat reach any cap; unique non-tiling 2-kite H_c=0 exact | pass | `tests/test_a2_heesch.py` |
| 2026-07-16 | A2 sharp prediction: only the hat grows unboundedly among n≤8 A1 survivors | full batch (1,087 shapes) + escalation to cap 4 | pass — hat unique at depth 4; all others exact H_c ≤ 2 | DB stage `A2-heesch`, [notebook 03](notebook/2026-07-16-session-03.md), `tests/test_a2_census.py` |
