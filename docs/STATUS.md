# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-16 (session 16)

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done through E1 n≤16 horizon, validated vs OEIS (sessions 01, 12) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 corona/Heesch engine | §4 A2 | ✅ done v0, hat = unique n≤8 anomaly (session 03) |
| M3 — A3 large-patch growth | §4 A3 | ✅ done v0, SAT backend; 22,940-tile hat patch, φ⁴ chirality anchor hit (sessions 04, 11) |
| M4 — A4 diffraction fingerprint | §4 A4 | ✅ done v0; 12-fold core calibration passed (session 05) |
| E4 — full fingerprint calibration gate | §8 E4 | ✅ passed (sessions 05–06) |
| M5 — A6 hierarchy mining | §4 A6 | ✅ done v0; recursive, stationary-collar and SAT forcing gate passed |
| **Gate G1 — E1 blind hat rediscovery** | §8 E1 | 🟨 in progress; hat A6 has one 3-type local rule family |
| Pipelines B, C; substrates n=5,8; scaling | §5, §6, §3.3 | ⬜ not started |

**No verdicts on new shapes are trusted before Gate G1 passes** (program §8).

## What exists and is verified

- Exact integer-arithmetic kite substrate (Laves [3.4.6.4]); A0 enumeration
  matches OEIS A057786 exactly n=1..16. The Rust production enumerator reaches
  19,035,075 free n=16 polykites in 364.48 s / 1.35 GiB and emits a compact
  fixed-width stream; Python remains the reference implementation.
- **A1 torus periodicity test** with machine-verified certificates
  (`src/einstein/funnel/a1_torus.py`): exact cover of quotient tori over all
  center-sublattices (HNF) up to index budget. Verdicts are three-valued:
  `periodic` (certificate), `no-periodic-at-budget`, `unknown-budget-exhausted`.
  The compiled streaming port reproduces the n=8 Myers split and screens
  n=9..16 with 60,477 independently re-verified positive certificates.
  At n=16, 29 are periodic at k≤12 and 19,035,046 survive; zero searches
  exhaust the node budget.
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
  exact code. Hat patches to 22,940 tiles (r2=100000, 551 s); reflected-hat
  density converges to the literature value 1/(1+φ⁴) — an external anchor
  A3 was never told about. Six H_c=2 shapes get pose-free disk-cover
  refutations at r2≤200. Periodic control patch (shape 392) stored for A4.
- **Compiled A2 first-corona filter:** exact vertex-ring cover plus hole-free
  exhaustion reproduces n=8 (720 H_c=0, 114 witnessed) and screens the actual
  n=9..16 corpus. At n=16 it proves 19,012,171 shapes H_c=0 and retains 22,875
  witnessed shapes. Across n=9..16 only 40,216 survive, every one with an
  independently verified corona; five initial budget cases all resolve under
  targeted escalation.
- **Compiled A2 recursive depth:** exact search enumerates all corona choices,
  not only one stored witness. The 40,216 first-corona survivors reduce to
  9,841 witnessed depth-2 shapes with no unknowns after escalation. On the
  complete n=8 universe, depth 3 leaves exactly one independently verified
  survivor—and its canonical form is the hat. This is the first direct blind
  rediscovery result.
- **Genuine new blind candidates:** depth 3 over n=9..16 yields 9,728
  independently verified chains, 105 exact H_c=2 shapes and eight conservative
  unknowns. The smallest complete witnessed sets—two n=10 and eight n=12
  shapes—are rendered in `a2-depth3-small-candidates.svg`. These are local
  growth candidates only; none is called an einstein or quasicrystal before
  A3/A4.
- **A4 diffraction fingerprint v0**
  (`src/einstein/funnel/a4_diffraction.py`): per-orientation Hann-windowed
  FFT powers on a shared grid, null-calibrated peak detection, sidelobe
  exclusion, bounded-integer module indexing, rotational-symmetry vote and
  crystal/quasicrystal-candidate/diffuse prioritization verdicts. Both stored
  hat patch sizes (11,514 and 22,940 anchors) recover rank 4 and symmetry 6;
  patch doubling calibrates the free coefficient bound at 8 (D-0018).
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
- **A6 hierarchy miner v0** (`src/einstein/funnel/a6_hierarchy.py`) uses
  exact rank-4 pose arithmetic and exact tile-edge adjacency. On pose-only
  Spectre patches it discovers a repeated 9-tile scaffold plus an 8-tile
  one-child exception. The selected rule uniquely covers all nine level-3
  root patches and recovers every withheld immediate parent in Delta levels
  1–4: 1/1, 8/8, 63/63 and 496/496. Physical counts
  9, 71, 559, 4,401 yield `T[n+1] = 8T[n] - T[n-1]` and dominant root
  `4 + sqrt(15)`. Artifact: `a6-spectre-results.json`; runner:
  `scripts/run_a6_spectre.py`.
- **A6 v1 recursive closure:** consecutive level-4/5 pose-only patches are
  contracted by exact scale-specific 8/7 rules. Colored physical-boundary
  adjacency graphs at equal abstract size become discrete after exact joint
  refinement, allowing partitions to transfer across scales. The level-4
  hierarchy closes `496 → 63 → 8 → 1`; every recovered cluster matches
  withheld ancestry at every depth. One exact oriented adjacency collar gives
  17 interior states that are 100% pure against all nine withheld labels
  (3,109 nodes), and all 17 states have one deterministic ordered child rule
  across 310 fully collared parents.
- **A6 v2 forcing gate:** the v1 parent and child collar numbers were found to
  be independently named rather than one stationary alphabet. Exact graph
  alignment now produces a closed, strongly connected 17-state substitution
  on normalized states `0..16`. Both locally exact physical phases enter the
  wider gate; only one closes recursively (`496→63→8→1`). Radius-1 physical
  collars stabilize at 32 states and 19 legal parent patterns: among 11,715
  occurrences from both phases, exactly the selected 3,905 groups remain
  legal. CaDiCaL proves all 19 physical patterns and all 17 metatile-state
  cases uniquely composable. Hidden ancestry and labels are still opened only
  after discovery and agree exactly.
- **E1 hat A6 screen:** A3 kite-grid placements now map exactly into module12,
  with candidate boundaries derived from their polykite cells. Disk cuts use
  an exact core-plus-halo SAT cover. On the 11,514-hat patch, 160 blind 8/7
  rules yield one full scaffold with two allowed exception positions. The
  ownership cover is non-unique (at least 20 solutions), but every sampled
  cover gives the same parent-anchor lattice and SAT forces all 141 safe-core
  anchors across every cover. Separate r2=50,000 and r2=100,000 SAT patches
  initially produced different patch-specific minimum libraries. A shared
  MaxSAT fit now requires 16 arity-7 patterns and forces both 430-parent cores
  to 71 and 72 groups respectively, with zero optional groups. The normalized
  16-state contractions admit one shared 15-pattern next-scale library
  (six arity 7, nine arity 8), forcing 43→8 and 41→8 with zero alternatives.
  Artifact:
  `a6-hat-screen-results.json`; inspection drawings:
  `a6-hat-candidate-{1,2}.svg`; runner: `scripts/run_a6_hat.py`.
- Test suite: **66 fast passed** (14 deselected, 49.81 s);
  **14 slow passed** (63 deselected, 111.33 s). Vendored Rust: **5 passed**.

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
(19–35 tiles max), while the hat covers r2=100000 (22,940 tiles).

## Known capacity limits (honest)

- Compiled A0 reaches E1 n=16, but its 19,035,075 records still require
  A3/A4 ranking. Depth 3 still leaves 9,728 witnessed n=9..16 shapes because
  raw depth is strongly size-dependent, especially at n=13 and n=16.
  Within-size ranking and large-patch/diffraction evidence are now mandatory.
  The fixed 16-cell key is intentionally scoped to E1; E2 n≈22–24 needs a
  wider key and likely external partitioning.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- A3 single-shot SAT: demonstrated at 22,940 tiles in 551 s;
  CNF building/solving scale roughly linearly but 10⁵-tile patches need an
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
- A6's current forcing certificate is verified finite computation over the
  recovered physical/collared languages, not a Lean theorem about arbitrary
  infinite tilings. The artifact contains the complete case counts and SAT
  results; a Lean wrapper is deferred to E10.
- Exact graph refinement becomes discrete on the calibrated Spectre patches;
  a general graph-isomorphism backtracker is not implemented. A future
  candidate whose refinement remains ambiguous must fail honestly or trigger
  that escalation.
- The traditional two-tile Gamma/Mystic fusion is not recovered uniquely, but
  the closed 9/8 hierarchy and its local forcing certificate do not require
  it. Recovering that named reference motif is optional validation archaeology.
- Hat A6 has a forced first parent-anchor lattice, but the next level is not a
  single Spectre-style full/deletion rule. Nearest 7/8 grouping cannot be made
  a deterministic function of geometry-only collars through radius 4; the
  recursive solver instead uses cover-invariant option states. Patch-specific
  minimum rulebooks do not transfer: the old 15-pattern library is globally
  UNSAT on the doubled patch, while its naive 17-pattern union introduces
  optional compositions. Joint fitting across both patches repairs this with
  forced shared libraries closing `430→71/72` and `43/41→8`. Eight terminal
  nodes are still too few to claim another independently replicated scale,
  and physical-hat ownership remains non-unique.

## Next actions (in order)

1. Run A3 disk growth on the complete ten-shape n=10/n=12 witnessed gallery,
   then use those outcomes to set the batch policy for n=13–16.
2. Run the complete n≤16 A0–A4 ranking, verify hat/turtle placement, and send
   the hat to A6 without identity-specific hints.
3. In parallel, seek a third shifted/independent hat window and stronger halo
   to challenge the shared 16/15-pattern A6 language and physical ownership.
4. Deferred: revisit the named Gamma/Mystic fusion if useful for comparison
   with the literature hierarchy; it is not a gate dependency.
5. Deferred: replace the bounded A4 indexer with LLL/PSLQ if future reference
   families or transformed controls break the E4 envelope.
6. Deferred: incremental SAT encoder for 10⁵-tile patches; corona-1 census
   feature; polyiamond substrate (external per-shape Heesch anchor from
   Kaplan's dataset).
