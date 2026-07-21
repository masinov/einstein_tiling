# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-21 (session 68)

> **Identity correction (ERR-003/D-0048):** every current use of “the
> finalist” and every legacy `e1-finalist-*` artifact refers to the published
> ten-kite **Turtle**, not a new candidate. Its tilability and nonperiodicity
> are known. The preserved computations are Turtle-control and method results.
>
> **Horizon correction (ERR-004/D-0049):** the peer-reviewed Hat paper reports
> the exhaustive aperiodic-polykite horizon `n≤24`, not 21. E1 is entirely
> validation; frozen E2 (`n≈22–24`) is invalid as discovery. Promotion is
> fail-closed against both that horizon and the infinite polykite portion of
> `Tile(a,b)`. See the [literature baseline](literature/POLYKITE_BASELINE.md).

## Where we are

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done through E1 n≤16 horizon, validated vs OEIS (sessions 01, 12) |
| M1 — A1 periodicity rejection + shape DB | §4 A1, §7.4 | ✅ done v0, validated vs Myers (session 02) |
| M2 — A2 corona/Heesch engine | §4 A2 | ✅ done v0, hat = unique n≤8 anomaly (session 03) |
| M3 — A3 large-patch growth | §4 A3 | ✅ done v1; exact disk SAT plus required-placement nested-core extension (sessions 04, 11, 19) |
| M4 — A4 diffraction fingerprint | §4 A4 | ✅ done v0; 12-fold core calibration passed (session 05) |
| E4 — full fingerprint calibration gate | §8 E4 | ✅ passed (sessions 05–06) |
| M5 — A6 hierarchy mining | §4 A6 | ✅ done v0; recursive, stationary-collar and SAT forcing gate passed |
| T0/W1/W2 — exact theory foundations | theory program v0.2 | ⏸ frozen control branch; Turtle-control T1.2-36 and the finite S3/A4 holonomy prefix remain exact, but abelian methods are classical and all Turtle conclusions are subordinate to published aperiodicity (D-0067) |
| W3 — substitution certificates | theory program v0.2 | ✅ closed as a novelty branch; exact Spectre results retained as a machine-readable reconstruction/control, with no further radius or D4-context work authorized (D-0070) |
| **Gate G1 — E1 Hat/Turtle validation** | §8 E1 | ✅ closed as validation/postmortem; historical runs are not an unbiased global benchmark (D-0068) |
| ST-M1 — Sturmian monotile encoding | outside-horizon theorem branch | ⛔ S0/E-infinity blocked after the `18,18,2` source misread; Q0/N1/N2 survive conditionally; no K1 table exists (ERR-006/D-0076) |
| Pipelines B, C; substrates n=5,8; scaling | §5, §6, §3.3 | ⬜ not started |

**No verdicts on new shapes are trusted before Gate G1 passes** (program §8).

## What exists and is verified

- **Versioned literature subsystem:** 26 source records distinguish
  peer-reviewed theorems, computational methods, preprints, reviews and
  secondary evidence; 23 open PDFs plus text extracts are reproducibly cached
  outside Git. The state-of-the-art map, methods-to-code matrix, reading queue,
  and novelty protocol make exact shape novelty, tiling-system novelty,
  aperiodicity, and method novelty separate claims. Turtle is now a blinded
  positive control. See [`docs/literature/`](literature/README.md) and D-0050.
- **Golden-Sturmian Turtle control:** the Akiyama--Araki proof is now audited
  theorem by theorem. Exact code verifies its standard/central words through
  level 24 and both irrational density polynomials. The independently grown
  9,239-tile Turtle disk has minority handedness `1181/9239=0.127827687`, close
  to the published exact `(3-sqrt(5))/6=0.127322004`. Forced Ammann-bar and
  Golden Hex geometry remain external, so this is validation rather than a
  new aperiodicity proof (D-0051).
- **Isohedral-surround SAT control:** Kaplan's finite extendable-surround
  criterion is implemented with the full vertex halo. The complete `n<=8`
  counts `1,1,4,4,0,70,52,37` match Myers exactly; all 169 positive surrounds
  cold-verify. It separates periodic anisohedral shapes for A1 and rejects Hat
  and Turtle. This is a portable early filter, not an aperiodicity test
  (D-0052).
- **Recognisability theorem crosswalk:** Walton's compact-Hausdorff expansive
  `L`-sub theorem and Chéritat's all-whole-plane Spectre hierarchy are now
  mapped to separate W1--W5 and D1--D7 machine obligations. The distinction
  prevents a circular proof: in return-discrete tiling spaces Walton's strict
  injectivity is equivalent to already excluding periodic hull elements,
  whereas Chéritat directly proves total unique grouping for every tiling.
  Certificate v2 cold-verifies and honestly remains partial (D-0053).
- **W3 method-novelty audit:** the reduced-patch/overlap-deletion/forced-parent
  architecture is already explicit in the original Spectre proof, Chéritat
  supplies the all-whole-plane equivalence, and the matching-rule and
  finite-state literature covers the general encoding ideas. A new July 2026
  Hat paper also publishes exact JSON retiling certificates and a verifier.
  W3 is therefore an exact reproducibility/control implementation, not a new
  aperiodicity theorem or established general method. The 80 abstract D4
  contexts will not be extended (D-0070).
- **ST-M1 theorem design:** minimal aperiodicity is separated from the
  surjective positive-entropy strengthening. A coupled contact-star carrier
  is the only retained mechanism; independent finite-state rails admit a
  periodic product. The full-isometry theorem requires geometric
  homochirality and a reflected global decoder. The source's
  `kappa=infinity` remark was not itself a complete system theorem, motivating
  the explicit S0 derivation below; no unmarked contact kernel has yet been
  derived (D-0071).
- **ST-M1 equal-support compiler:** a finite connected macrotiling system over
  one congruent periodic cell is MLD with a finite colored one-support system
  by explicit internal-address ports. This closes only the conditional
  compiler S0C. The source's `kappa=infinity` remark does not provide the
  common-cell subdivision or preserve the complete Section 10.1 language
  (D-0072, ERR-006).
- **ST-M1 source correction:** primary Table 1 gives the optimized
  `sqrt(2)-1` large templates composition `12S+6M+6L`, not bare `2S+L`.
  The one-support `kappa=infinity` sentence belongs to the separate Turtle
  subsection. The session-65 `18,18,2` specialization, its all-`M` exclusion,
  and the resulting S0 closure are withdrawn. S0C remains a valid conditional
  compiler, but S0/E-infinity are blocked (ERR-006/D-0076).
- **ST-M1 corrected composition skeleton:** in the source convention the
  actual large templates are `[12:12:6]` and the small template is
  `M=[0:2:0]`. Their segment meets the Sturmian parabola exactly at
  `beta=sqrt(2)-1`, with positive mixture coefficients. This proves P0 and
  retains the irrational-slope arithmetic target. The source SAB language,
  not composition alone, excludes all-`M`; E-infinity remains blocked
  (D-0077).
- **ST-M1 symbolic quotient boundary:** Q0 correctly requires safety on the
  full finite local closure. Erasing ownership to unrestricted `S/M/L`
  restores rational periodic tilings, and independent corridor rails admit
  periodic products. These conditional no-go results survive, but there is no
  established raw S0 alphabet to quotient and no K1 collar table to write.
- **Primary-source polykite baseline and enforced novelty gate:** the positive
  unequal `Tile(a,b)` continuum is completely classified; it contains
  infinitely many polykites; the three degenerate similarity classes are
  periodic; `Tile(1,1)` is only weakly chiral aperiodic; and suitable edge
  modifications give families of strict Spectres. The finite search report is
  `n≤24`. Code now distinguishes an unregistered key from a discovery-eligible
  shape and blocks all promotions until the full family audit passes.
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
- **Blind local-growth survivors:** depth 3 over n=9..16 yields 9,728
  independently verified chains, 105 exact H_c=2 shapes and eight conservative
  unknowns. The smallest complete witnessed sets—two n=10 and eight n=12
  shapes—are rendered in `a2-depth3-small-candidates.svg`. These are local
  growth candidates only; known-shape classification is mandatory before
  novelty promotion. In the smallest gallery, n=10 candidate 2 is the Turtle.
- **Blind Turtle rediscovery (formerly “new-shape finalist”):** the complete
  smallest-survivor batch passed A3/A4 and an extended exact A1 audit. One n=10 shape
  is disk-refuted; all eight n=12 shapes are exact periodic tilers at torus
  index 16. The remaining n=10 candidate 2 has no torus certificate through
  index 215 (plus several larger spot refutations), covers an independently
  verified r²=50,000 disk with 9,239
  tiles, and retains a rank-4, sixfold diffraction signature after patch
  enlargement. These independently reproduce expected Turtle behavior; the
  published Turtle proofs, not these finite tests, establish aperiodicity.
- **Turtle robustness audit (legacy finalist assets):** the apparent crown gaps are outside A3's
  certified disk (zero missing cells inside). Four independently phase-biased
  r²=12,800 patches share at most 6.7% exact placements but all retain
  estimated rank≥4 at 1024² and 2048². The first large patch contains one
  exact period-47 stripe domain; it does not recur as an exact period across
  the independent patches. Symmetry votes vary at small size/resolution, so
  the robust signal is rank≥4, not universally sixfold symmetry (D-0025).
- **A3 crown correction:** the preceding gap audit addressed coverage, not
  continuability. All five complete r²=12,800 crowns are exact dead ends.
  After measured collar rewrites, however, a literal nested chain preserves
  growing cores r²=9,000 then r²=30,000 inside outer patches r²=50,000 and
  r²=100,000 (18,386 tiles). Candidate status now rests on nested core growth,
  with collar depth reported explicitly; independent disk covers alone no
  longer count as growth evidence (ERR-002, D-0026).
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
- **W3 ancestry-blind physical language:** exact straight-`Tile(1,1)`
  geometry produces all 166 fixed-chirality edge-to-edge first coronas.
  Exact SAT ring completion contracts the existential central-corona prefix
  `166→30→21`; the generated level-3/4 controls contain 18 stable types.
  The three extras `[33,44,155]` all have radius-four witnesses. None of the
  21 radius-three survivors has unique isolated parent ownership
  (`2:17,3:3,5:1`), while all eight superficially unique radius-one types die
  at radius two. C5 became partial rather than proved; this result supplies
  the input language for the coordinated experiment below.
- **W3 coordinated parent-overlap language:** physical ring variables and
  recovered 9/8-parent variables now share one exact SAT problem on a
  universally buffered core. All 18 generated corona controls group. The
  extras exhaust as `33: 2→200→0`, `44: 27→0`, and `155: 60→24→0`, so the
  conditional finite language equals those 18 controls. Empty-buffer branches
  are expanded physically, never called UNSAT. The result assumes the parent
  language; it does not prove all physical tilings have a parent partition or
  that the partition is unique and iterable.
- **W3 L18 physical-to-parent transducer:** the 18-type language has 87
  radius-two and 418 radius-three rooted cases. Exhaustive grouping gives one
  parent-anchor map in every case; 48 raw 8/9 ambiguities retain the same
  anchor. Among all 15,216 radius-six survivors, the complete canonical eight
  children map to that anchor, proving the unique full/missing partition for
  every whole-plane L18 tiling. Contraction is not closed: non-generated
  complete parent coronas have frontiers `6280→1796→4482` at radii 7–9.
  Further blind rings are replaced by a contracted parent/interface graph.
- **W3 contracted-interface no-go:** the frontier compresses to nine extra
  uncolored parent coronas beside the 17 generated states. Exact reciprocal
  edge and triangle-overlap CSPs leave all 26 states alive; fixed-point support
  pruning removes none. Parent type and physical interface color are therefore
  necessary state, not optional detail.
- **W3 one-sided colored-interface no-go:** all 57,589 resolved radius-seven
  extensions collapse to 17 generated and five extra states after retaining
  the center full/missing type and exact oriented child-edge contacts. The
  generated set exactly matches the independent substitution control, but all
  22 states survive colored star pruning and form one closed SCC. The next
  finite alphabet must buffer the neighbor component types as well.
- **W3 two-sided defect frontier:** exhaustive continuation gives
  `6280→1796→4482`; every radius-nine interface has all six endpoint types
  physically buffered. The branches collapse to three new full-component
  states, and all three survive beside the 17 controls in one SCC. Their exact
  minimum extra-neighbor costs are `[1,0,1]`: one state is locally absorbable,
  while the other two require an extra neighbor and minimally point to each
  other. The next proof object is a pinned radius-two defect CSP.
- **W3 pinned radius-two defect propagation:** only one of each defect's
  `28,100,3` colored root stars survives exact pair agreement and physical
  8/9-child support nonoverlap. The three surviving problems have
  `960,432,840` complete assignments, but all 131 are UNSAT with a
  generated-only second ring. The forced type map is `A→C, B→C, C→A`, so the
  apparently absorbable defect enters the alternating `A/C` pair. This is a
  finite propagation theorem, not yet contraction closure or a plane-tiling
  counterexample.
- **W3 radius-three conditional closure:** all `960+432+840=2,232`
  radius-two assignments were extended with exact colored pair and physical
  support constraints. The three roots have `0,2,1` survivors. The dead root
  `288…` cannot occur in a whole-plane 20-state configuration, and every
  survivor of either other root contains `288…` in its fixed inner patch.
  Hence all extras are eliminated and contraction closes to the 17 generated
  states inside L18. Entry of every geometric Spectre tiling into L18 remains
  the recognisability blocker.
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
- **Theory dossier v0.2 adopted:** `docs/theory/` now separates roadmap,
  theorem text, stable-ID proof status, experiment evidence and monograph
  structure. The dossier's historical “finalist” identifier now means the
  Turtle control (D-0048). T0.1 gives a proof draft that singly periodic grid-aligned
  tilability implies doubly periodic tilability; W1's auditable transfer
  certificate contract is specified. No new-tile verdict is claimed.
- **W1.a exact reference implementation:** the new cylinder engine enumerates
  all whole-tile crossing-state unions, searches the entire graph, and converts
  cycles to independently verified A1 certificates. Eight unit controls pass,
  including a four-kite example that has period (2,0) but not (1,0), preventing
  primitive-only vector collapse. The archived phase-0 matrix adds 28 n≤3
  census/vector cases and 102 independent bounded-torus checks: 25 verified
  cycles, four cycle-free hat vectors, zero disagreements/exhaustions. Those
  phase-0 graph hashes motivated the complete certificate gate below.
- **W1 negative gate and first Turtle-control theorem:** cycle-free results now carry
  complete graph manifests checked by a separate geometry/state/transition
  verifier. Five negative controls pass tamper-resistant verification. For the
  Turtle, 11 D6 representatives cover every one of the 90 nonzero vectors
  with Q(v)≤25, including nonprimitive vectors; all are independently verified
  cycle-free with zero exhaustions. Thus T1.2-25 exactly excludes every such
  grid-aligned period. Larger vectors and unconditional geometry remain open.
- **W1 exact extension through Q=36:** four incremental shell certificates
  cover 36 more vectors, with complete graphs up to 159,860 states. Combined
  with T1.2-25, all 126 nonzero vectors in 15 D6 orbits through Q=36 are
  independently verified cycle-free. The 51 MB shell artifact makes proof-size
  scaling explicit; it contains zero resource exhaustions.
- **W2 Layer A and B audit:** exact area and prime-sector coloring witnesses
  have zero false exclusions on all 60,477 materialized periodic certificates.
  For the Turtle, sector coloring adds nothing beyond k≡0 mod 5. The proposed
  isolated nontrivial-character Layer B is mathematically vacuous because its
  projected target is zero; T2.B0 retires it and redirects W2 to integer SNF.
- **W2.C modular cokernel:** quotient-wide GF(2) witnesses pass all 60,477
  periodic controls with zero false exclusions and kill 36/742 area-admissible
  Turtle HNFs through index 60. A closed odd-weight support annihilates both
  thin placement profiles for HNF (1,0,k), producing proof draft T2.C1 for all
  k≥4—W2's first infinite quotient-family exclusion.
- **W2.C exact integer normal forms:** pinned FLINT 0.9.0 and SymPy 1.14.0
  independently agree on Smith controls; canonical FLINT row-HNF completes all
  742 Turtle quotients through index 60. It finds exactly the same 36 rank
  obstructions as GF(2), 706 unrestricted integer solutions, and zero
  torsion-index obstructions. Thus the bare integer relaxation is exhausted at
  this horizon; integer compatibility is not a 0/1 cover.
- **W2.C nonnegative rational no-go:** translation averaging reduces the full
  incidence LP exactly to a six-sector cone. Exact compact witnesses verify
  that all 706 integer-compatible Turtle quotients through index 60 are also
  nonnegative-rational compatible; the same 36 rank cases are obstructed.
  Ordinary positivity therefore adds zero kills. Binary exact-cover structure
  or nonabelian holonomy is the remaining algebraic target.
- **W2.C binary quotient families:** T1.2-36 composes with exact HNF vector
  membership into 126 infinite congruence families. They exclude every HNF
  through index 36 and 2,941/8,864 Turtle area-admissible HNFs through index
  215. Exact D6 maps promote the thin proof to all three families `(1,0,k)`,
  `(k,0,1)`, `(k,k-1,1)` for every k≥4. Missing family membership is unknown.
- **W2 prior-art disposition:** additive incidence/cokernel witnesses are
  classical generalized coloring/tile homology, including on finite tori.
  The explicit Turtle thin support was not found in the audited Turtle papers,
  but is only a small corollary of published aperiodicity. W2 is frozen as a
  control branch (D-0067), not a method- or Turtle-novelty claim.
- **W2.D phase 0:** an exact p3 Cayley model reproduces Conway--Lagarias'
  three-in-line boundary invariant. The Turtle has 2,556 S3 boundary-group
  surjections, but exhaustive zero-displacement analysis yields no commuting-
  coset obstruction: 2,322 kernels have order 6 and 234 have order 3. A sound
  torus certificate must couple group potentials to the selected binary tile-
  boundary network; no Layer-D Turtle quotient is yet excluded at this phase.
- **W2.D binary-coupled result:** the at-least-cover/S3-potential CSP passes
  one-kite and nontrivial shape-392 periodic controls. The 234 strong Turtle
  surjections reduce to 39 inner-conjugacy classes. Exhaustive class search
  kills all three W1-family survivors at index 40—`(10,3,4)`, `(40,11,1)`,
  `(40,28,1)`—with six killing classes each, while their placement-only
  relaxations are SAT. All 54 selected map/twist core CNFs and DRAT proofs
  replay under independent `drat-trim`; together with area and T2.C4-36 this
  excludes every HNF through index 40. The later bullets extend this finite
  prefix; O1 remains open.
- **W2.D index-45 extension:** all 39 strong S3 quotient classes are classified
  on the nine W1-surviving HNFs. Nine effective maps form three exact
  same-signature triples; every HNF is killed by at least six maps. One
  deterministic map per HNF supplies 162/162 independently replayed DRAT
  cores (377,474,096 compressed bytes). The shell splits 69 W1-family plus 9
  Layer-D exclusions, closing every grid-aligned quotient through index 45.
  Exact diagonal D6 covariance explains the triple pattern: 4,212/4,212
  transformed matrix entries agree. It is not an infinite-family theorem and
  O1 stays open.
- **W2.D index-50 complementary closure:** S3 excludes one six-HNF orbit, then
  an exact small-group census selects A4 with V4 displacement kernel and
  residual C3 information. On the 12 S3 survivors, 48 strong A4 classes reduce
  to 48 diagonal pair orbits: 16 are obstructed and cover every HNF, while
  32/32 relaxed SAT witnesses verify clausewise. Fixing map 7 yields 576/576
  cold-replayed DRAT cores (2,166,298,658 compressed bytes). The complete shell
  splits 75 W1 + 6 S3 + 12 A4, closing the certified quotient prefix through
  50. The shared killer signature is three distinct V4 values on the final
  three generators; this is finite evidence for a symbolic family theorem,
  not O1.
- **Interrupted overnight Turtle campaign recovered (legacy finalist logs):** checksummed parsing of
  the append-only logs records 9,099 completed generic HNF quotient executions
  plus 36 targeted executions, all reporting exact UNSAT, with zero periodic
  certificates. The count includes deliberate reruns; jobs lacking completion
  lines remain unknown. The completed blind hierarchy
  screen retained two non-unique first-composition rules out of 22,094 but no
  stationary recognizable recursion. Artifact: `e1-overnight-recovered.json`.
- Test suite: **222 fast passed** (17 deselected, 145.42 s, session 68);
  **17 slow passed** previously (192 deselected, 389.36 s).
  Vendored Rust: **5 passed**.

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
mini-E1 positive-control result: Heesch depth alone ranks it #1 in its size
class. This is not a new census. Kaplan's public 2023 eight-kite artifact has
exactly the same 108 `H_c=1` and five `H_c=2` counts; its three inconclusive
cases are the two periodic anisohedral shapes removed by A1 and the Hat.
Our structurally independent A2 engine therefore supplies an exact 116/116
per-shape reproduction and cold-verifiable benchmark; session 58 maps the two
periodic-anisohedral controls to IDs 506/793 and the Hat to ID 635. See ERR-005 and
`docs/literature/reviews/KAPLAN_HEESCH_POLYKITES.md`. A3 sharpens the
internal ranking: all six `H_c=2` shapes are pose-free refuted on disks of
`r2<=200` (19–35 tiles max), while the Hat covers `r2=100000` (22,940 tiles);
that separation is finite benchmark evidence, not a novelty claim.

## Known capacity limits (honest)

- Compiled A0 reaches E1 n=16, but its 19,035,075 records still require
  A3/A4 ranking. Depth 3 still leaves 9,728 witnessed n=9..16 shapes because
  raw depth is strongly size-dependent, especially at n=13 and n=16. The
  first complete ten-shape promotion blindly rediscovered the Turtle, but
  9,718 witnessed shapes plus eight unknowns remain outside A3. Within-size
  ranking and batched large-patch/diffraction evidence are now mandatory.
  The next complete *validation/corpus* batch would be all 29 n=14/n=15
  depth-3 witnesses; the much larger n=13 and n=16 sets follow after its
  measured yield. None can be a new aperiodic polykite under the published
  `n≤24` classification. Frozen E2 is invalidated rather than awaiting a
  wider key.
- A1 torus budget k ≤ 12 proven sufficient for n ≤ 8 only (by Myers
  agreement); larger n may need larger tori — revalidate per horizon.
- A3 single-shot SAT: demonstrated at 22,940 tiles in 551 s, but an
  independently covered disk is not continuation evidence. Required-placement
  nested cores now provide the sound growth feature; optimizing retained-core
  radius across many scales still needs an incremental encoder
  (assumption-based collar growth) or compiled encoding.
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

Research is under the 2026-07-21 reset recorded in
`docs/literature/RESEARCH_RETURN_AUDIT.md`.

1. The T2.C1/T2.C5 audit is **closed**: the method class is classical tile
   homology and the explicit Turtle formula is retained only as a worked
   control. W2 escalation is frozen.
2. The E1 benchmark assessment is **closed no-go** for new ablations. Package
   the exact reproduction fixtures and postmortem during release work only.
3. Human checkpoint `HC-2026-07-21-04` was explicitly authorized after review
   of sessions 64--66. Sessions 67--68 used two slots for the primary-source
   correction and corrected projective-composition lemma; no experiment or
   large artifact was produced.
4. Keep all polykite discovery work through `n=24`, all Turtle quotient-shell
   escalation, and all Spectre radius escalation frozen.
5. **ST-M1 remains upstream of K1.** P0 proves that the corrected template
   segment selects only `sqrt(2)-1`, so the arithmetic target survives. The
   final HC-04 session may inspect the actual isometric-cell supports for a
   plausible common refinement; no table, shape search, or radius escalation
   is authorized.
6. The `Tile(a,b)` recognizer remains required infrastructure before any
   future polykite novelty promotion, but is not itself the next research
   result.
