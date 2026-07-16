# Experiment registry

The ten experiments defined in the program (§8), with live status.
Rule from the program: **E1–E4 are validation gates — no verdict on a new
shape is publishable/trustable until they pass.** Every experiment run must
leave an entry here linking to its notebook session and artifacts.

| ID | Name | Kind | Status | Depends on | Evidence |
|---|---|---|---|---|---|
| E1 | Blind rediscovery of the hat | validation gate | **in progress** — funnel complete; n≤16 scaling next | funnel A0–A4+A6 (M1–M5) | sessions 01–09 infrastructure |
| E2 | Exhaustive 12-fold sweep beyond known horizon | discovery | not started | E1 pass, scaled A0 | — |
| E3 | First hunts in 5-fold / 8-fold substrates | discovery | not started | E1 pass, new substrates | — |
| E4 | Diffraction fingerprint calibration | validation gate | **PASSED** (2026-07-16) | A4 (M4), full reference library | `scripts/run_e4.py`, `scripts/run_e4_wide.py`; [notebook 05](notebook/2026-07-16-session-05.md), [notebook 06](notebook/2026-07-16-session-06.md); assets `e4-results.json`, `e4-wide-results.json`, `e4-spectrum-*.png` |
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
| 2026-07-16 | A3 hat-patch chirality vs literature: reflected density must approach 1/(1+φ⁴) ≈ 0.12732 (from the H7/H8 substitution of arXiv 2303.10798, an input A3 never sees) | SAT-grown disks, 130 → 11,514 tiles | pass — 13.85% → 12.81%, monotone | DB stage `A3-patch` (shape 635), [notebook 04](notebook/2026-07-16-session-04.md), `tests/test_a3_patch.py` |
| 2026-07-16 | A3 internal consistency: engines agree (greedy vs SAT) and A2 finite-H_c shapes must hit disk-cover ceilings | 2-kite refuted by both engines; six H_c=2 shapes pose-free UNSAT at r2≤200 while the hat covers r2=50000 | pass | DB stage `A3-patch`, [notebook 04](notebook/2026-07-16-session-04.md) |
| 2026-07-16 | Vendored spectre generator (user-provided) + our rank-4 module port | three-way agreement: upstream reference float leaves == Rust exact traversal == our module12 projection (N=3 Delta, 559 leaves); tile-count recurrence; single chirality | pass | `tests/test_spectre_vendor.py`, `vendor/spectre/VENDOR.md` |
| 2026-07-16 | A6 v0 blind immediate-composition recovery on Spectre | pose-only exact local mining on Delta N=3, confirmation on N=4 and all nine N=3 root labels; hidden ancestry opened afterward | pass — repeated 9/8 scaffolds; unique cover per selected rule; withheld parents recovered exactly at N=1..4 (1, 8, 63, 496); recurrence `(8,-1)` | `scripts/run_a6_spectre.py`, `a6-spectre-results.json`, [notebook 07](notebook/2026-07-16-session-07.md) |
| 2026-07-16 | A6 v1 recursive and collared closure on Spectre | exact contraction of pose-only N=4/5 patches; cross-scale colored adjacency-graph transfer; withheld paths/labels opened afterward | pass — N=4 closes `496→63→8→1`, all depths match ancestry; radius-1 gives 17 pure states covering 9 labels; 17/17 deterministic child rules on 310 interior parents | `scripts/run_a6_spectre.py`, `a6-spectre-results.json`, [notebook 08](notebook/2026-07-16-session-08.md) |
| 2026-07-16 | A6 v2 stationary language and forcing gate on Spectre | align parent/child collars to one alphabet; test both exact physical phases by recursive closure; enumerate physical and metatile collar languages; SAT-block the known parent in every finite case | pass — 2 local phases → 1 recursive survivor; 32 physical states/19 legal parent patterns reject 7,810 competing occurrences; 17-state substitution closed and strongly connected; all 19 physical and all 17 metatile cases uniquely composable | `scripts/run_a6_spectre.py`, `a6-spectre-results.json`, [notebook 09](notebook/2026-07-16-session-09.md) |
| 2026-07-16 | E1 hat A6 first blind hierarchy screen | exact A3-placement/module adapter; exact accelerated nearest-anchor mining; core-plus-halo SAT cover; cover-invariant option states; MaxSAT recursive library | in progress — one 8/7 scaffold family with two exception positions; ≥20 ownership covers but one parent-anchor lattice; all 141 safe-core anchors forced; next level uses a minimum 15-pattern, arity-7 library and forces 27/27 inner groups | `scripts/run_a6_hat.py`, `a6-hat-screen-results.json`, `a6-hat-candidate-{1,2}.svg`, [notebook 10](notebook/2026-07-16-session-10.md) |

## E4 phase-1 record (2026-07-16, first numbered experiment run)

Pipeline: per-orientation-class anchor sets → Hann-windowed FFT power
spectra, incoherently averaged → peak detection (floor = 5× the strongest
local max of the random null, exclusion zones against window sidelobes)
→ greedy bounded-integer module indexing → verdict.

| reference | points | classes | rank | sym | verdict | literature target |
|---|---|---|---|---|---|---|
| random null | 11,514 | 12 | 0 | — | diffuse | diffuse ✓ |
| periodic (A1 cert of shape 392, unfolded) | 11,341 | 3 | 2 | 6 | crystal | rank 2 ✓ |
| hat (A3 SAT patch, shape 635) | 11,514 | 12 | 4 | 6 | quasicrystal-candidate | rank 4, sixfold (Baake–Gähler–Sadun arXiv 2502.03268) ✓ |
| spectre (vendored generator, level-6 Delta disk) | 106,905 | 60 | 4 | 6 | quasicrystal-candidate | rank 4, chiral sixfold (ibid.) ✓ |

Calibration iterations (recorded honestly): (1) mixed anchor sets are
dominated by substrate-lattice peaks → per-orientation classes per the
spec; (2) window sidelobes poisoned indexing → exclusion zones;
(3) coefficient bound too small for lattice peaks → split pair/free
bounds; (4) my initial 12-fold expectation for the spectre was wrong —
the literature value is chiral sixfold, which is what we measure.

**Gate status: still open.** This run establishes the detector's 12-fold
core behavior, but the full E4 criteria in program §8 also require Penrose,
Ammann–Beenker, Taylor–Socolar and square-triangle random-tiling references;
exact module-rank recovery across that library; a false-positive measurement
over 10⁴ random periodic tilers; patch-size-doubling stability; and deliberately
rotated/sheared indexer controls. Those are carried forward rather than
silently treating this narrower calibration as the complete gate.

## E4 wider/final record (2026-07-16)

The second run closes every remaining criterion from program §8. Canonical
projection references use a projected centered-hypercube window; the
Taylor–Socolar case uses its published dyadic reciprocal hierarchy because
its limit-periodic Fourier module is not finitely generated. The random
square–triangle control implements the published boundary-gap growth rule
and averages independent interior crops before measuring narrow-peak mass.

| check | result | target |
|---|---|---|
| Penrose, 561 → 1,307 vertices | rank 4, symmetry 10 at both sizes | exact rank; size stability ✓ |
| Ammann–Beenker, 869 → 2,617 vertices | rank 4, symmetry 8 at both sizes | exact rank; size stability ✓ |
| rotated references | rank 4; symmetry retained | covariance ✓ |
| sheared references | rank 4; rotational vote drops to 2 | module rank affine-stable ✓ |
| Taylor–Socolar, 59,407 sites | five dyadic reciprocal levels; hierarchy-erased control has one | limit-periodic hierarchy ✓ |
| random square–triangle ensemble | rank-4 substrate, twelvefold broad order, narrow-peak mass below calibrated 0.025 cutoff | diffuse/random order distinguished from pure point ✓ |
| randomized periodic tilers | 10,000 screened; 9 coarse candidates; 0 confirmed at the second resolution | confirmed false-positive rate 0 < 10⁻³ ✓ |

The coarse periodic screen also returned 149 rank-3 ambiguous cases. They are
not false quasicrystal positives, but are retained in the JSON rather than
hidden. D-0011 accepts the bounded indexer for A4 v0 inside this measured
envelope and makes second-resolution confirmation mandatory when the
high-throughput coarse screen reports rank ≥ 4.
