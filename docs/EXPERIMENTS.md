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
| 2026-07-16 | E1 hat A6 first blind hierarchy screen | exact A3-placement/module adapter; exact accelerated nearest-anchor mining; core-plus-halo SAT cover; cover-invariant option states; MaxSAT recursive libraries | in progress — one 8/7 scaffold family with two exception positions; ≥20 ownership covers but one parent-anchor lattice; all 141 safe-core anchors forced; first finite patch exposed a patch-specific 15/8-pattern recursive fit | `scripts/run_a6_hat.py`, `a6-hat-screen-results.json`, `a6-hat-candidate-{1,2}.svg`, [notebook 10](notebook/2026-07-16-session-10.md) |
| 2026-07-16 | E1 hat A6 patch-doubling challenge | grow exact r²=100,000 disk; freeze old rulebook; joint MaxSAT over r²=50,000 and r²=100,000 patches; shared-alphabet SAT verification | pass for two recursive finite scales — exact 8/7 scaffold unchanged; old 15-pattern optimum correctly rejected as patch-specific; shared 16-pattern library forces 430→71/72, then shared 15-pattern library forces 43/41→8, with zero optional groups | `scripts/run_a6_hat.py`, `a6-hat-screen-results.json`, DB shape 635 A3 certificates, [notebook 11](notebook/2026-07-16-session-11.md) |
| 2026-07-16 | E4 hat patch-doubling regression | run the A4 fingerprint on both stored hat disks; parameter-isolate a spurious fifth generator on the doubled patch | pass after calibrated free coefficient bound 6→8 — both 11,514- and 22,940-hat patches recover rank 4, symmetry 6 | `tests/test_a4_diffraction.py`, D-0018, [notebook 11](notebook/2026-07-16-session-11.md) |
| 2026-07-16 | E1 A0 horizon scaling | exact compiled breadth-first enumeration; same D6 canonical form as Python; fixed-width streaming output | pass — all OEIS A057786 counts through n=16; 19,035,075 shapes in 364.48 s, 1.35 GiB; full corpus materialized as reproducible stream | `tools/a0_polykites.rs`, `scripts/run_a0_fast.py`, `tests/test_a0_compiled.py`, [notebook 12](notebook/2026-07-16-session-12.md) |
| 2026-07-16 | E1 compiled A1 horizon screen | exact HNF torus cover over A0 streams; record-range parallelism; Python certificate verification | pass — n=8 reproduces 39/834 Myers split; all 60,477 certificates at n=9..16 independently verify; n=16 completes in 673.06 s with 29 periodic and 19,035,046 survivors, zero exhaustions | `tools/a1_torus.rs`, `scripts/run_a1_fast.py`, `tests/test_a1_compiled.py`, [notebook 13](notebook/2026-07-16-session-13.md) |
| 2026-07-16 | E1 compiled A2 first-corona screen | exact vertex-ring cover, nonoverlap and hole-free test over A1 streams; dynamic chunks; targeted budget escalation | pass — n=8 reproduces 720 H_c=0 / 114 survivors; n=16 reduces 19,035,046→22,875 in 889.09 s; 40,216 total n=9..16 survivors, every one with a Python-verified corona and no unresolved budget cases | `tools/a2_corona.rs`, `scripts/run_a2_fast.py`, `tests/test_a2_compiled.py`, [notebook 14](notebook/2026-07-16-session-14.md) |
| 2026-07-16 | E1 compiled A2 recursive depth | exhaustive recursive corona chains with dynamic ring coverage; targeted 10M-node escalation; independent chain verification | pass — 40,216 first-corona shapes reduce to 9,841 witnessed depth-2 shapes with no unknowns; blind n=8 depth 3 leaves exactly one verified survivor, canonically the hat | `tools/a2_corona.rs`, `tests/test_a2_compiled.py`, [notebook 15](notebook/2026-07-16-session-15.md) |
| 2026-07-16 | E1 blind depth-3 candidate screen | parallel recursive depth-3 search on all 9,841 depth-2 survivors; full independent chain verification; smallest-candidate gallery | in progress — 9,728 witnessed H_c≥3, 105 exact H_c=2, 8 execution/budget unknowns retained; genuine new n=10/n=12 candidates rendered for inspection, A3/A4 next | `a2-depth3-small-candidates.svg`, `scripts/render_a2_candidates.py`, [notebook 16](notebook/2026-07-16-session-16.md) |
| 2026-07-16 | E1 smallest-candidate promotion | pose-free A3 ladder on complete n=10/n=12 depth-3 sets; exact A1 extension; two-size matched-null A4; finalist escalation | one high-priority finalist — 1/10 A3-refuted, all 8 n=12 exact-periodic at torus index 16, n=10 candidate 2 survives exact A1 through index 100, grows a verified 9,239-tile r²=50,000 disk and retains rank-4/sixfold diffraction | `e1-finalist-results.json`, `e1-finalist-{patch.svg,spectrum.png}`, `scripts/run_e1_finalist.py`, [notebook 17](notebook/2026-07-16-session-17.md) |
| 2026-07-16 | E1 finalist robustness audit | exact boundary coverage; four independent SAT phase solutions; exact translation overlap; matched-null A4 at 1024² and 2048²; extended/targeted exact tori | pass as a ranking robustness check — zero missing certified disk cells; independent patches share <6.7% placements yet all retain rank≥4 at both resolutions; exact A1 contiguous through index 215; period-47 cylinders through transverse width 25 are UNSAT; symmetry remains size-sensitive | `e1-finalist-robustness.json`, `e1-finalist-periodicity.json`, `e1-finalist-independent-patches.svg`, [notebook 18](notebook/2026-07-16-session-18.md) |
| 2026-07-17 | E1 finalist nested-crown audit | freeze complete patches, then thaw measured collars while enlarging; independently verify literal placement inclusion | correction/pass — all five complete crowns are dead; extendable-core depth varies strongly; one verified nested chain grows protected cores r²=9,000→30,000 while outer patches grow r²=12,800→50,000→100,000 (18,386 tiles) | `e1-finalist-nested.json`, `scripts/record_e1_finalist_nested.py`, [notebook 19](notebook/2026-07-17-session-19.md), D-0026 |

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
