# Decision log

Append-only. Each entry: context → decision → consequences. Reversals get a
new entry referencing the old one, never an edit.

## D-0001 (2026-07-15) — Repository layout

Docs (program spec, status, experiments, decisions, notebook) under `docs/`;
exact-arithmetic library under `src/einstein/` (installable package);
validation in `tests/`; bulk artifacts under `data/` (gitignored when large).
The program document is the *specification*; it is never edited to match
reality — discrepancies go to `docs/program/ERRATA.md`.

## D-0002 (2026-07-15) — Python first, compiled kernel later

The program's performance targets (§7.1: tens of millions of tiles/second)
need compiled code, but correctness and auditability come first: v0 is pure
Python with exact integer arithmetic, validated against external anchors
(OEIS, Kaplan's hat coordinates). The compiled port happens only after the
Python reference implementation exists to test it against. Measured Python
capacity: A0 to n=12 in 40 s (see STATUS "capacity limits").

## D-0003 (2026-07-15) — Integer hex coordinates; rank-4 module deferred

All polykite-substrate geometry lives on the triangular lattice
(basis e1=(1,0), e2=(1/2,√3/2), hexagon side 2): every kite vertex is an
integer pair, squared length is x²+xy+y², and the full grid symmetry group
acts by integer maps. The program's rank-4 ℤ[ζ₁₂] module (§3.3) is *not
needed* for polykites (only 6-fold directions occur) and is deferred until
12-fold rotations actually appear (module polygons, spectre substitution,
diffraction indexing). Scale matches Kaplan's hatviz `hexPt`, so published
hat data embeds verbatim — chosen deliberately for external validation.

## D-0004 (2026-07-15) — Kite cell encoding and canonical forms

Cell = (hex-center x, hex-center y, sector d∈0..5); kite quad
[C, M_{d−1}, V_d, M_d]. Free-polyform canonical form = lex-min over the 12
point-group images of the translation-normalized sorted cell tuple.
Enumeration = grow-by-one-neighbor BFS with canonical dedup (every connected
(n+1)-form contains a connected n-form). Validated: OEIS A057786 exact match
n=1..12.

## D-0005 (2026-07-15) — External anchors before trust

Standing rule (instance of program §8's gate philosophy): every new component
must be validated against data we did not produce — OEIS sequences, published
coordinates, literature values — before its output is used downstream. A
component with no external anchor available gets exact self-consistency tests
plus a note in EXPERIMENTS.md "pre-experiment validation log".

## D-0006 (2026-07-16) — Funnel v0 scope: grid-aligned tilings only

A1 (and later funnel stages as currently designed) consider only placements
in the kite grid's symmetry group p6m. Polyform tilings that break grid
alignment exist in general and are invisible to this machinery. Consequence:
"periodic" verdicts are sound (a certificate is a real periodic tiling), but
survival of A1 does not exclude off-grid periodic tilings. This matches the
scope of Myers' published census (he states the same restriction), which is
what makes his numbers usable as our external anchor. Lifting this
restriction is a recorded open problem for the certification track — any
eventual aperiodicity *proof* must handle off-grid placements (the hat paper
does).

## D-0007 (2026-07-16) — A1 v0 = torus exact-cover only; SQLite for the DB

The program's A1 battery (Conway criterion, BLD factorization, isohedral-type
search, torus search) is ordered by cost, but at current scale (n ≤ 12,
~10⁵ shapes) the torus test alone is fast enough (~30 ms/shape) and is the
only sub-test that both certifies and covers all periodic cases; the others
are deferred as optimizations for the n ≥ 16 sweeps. Shape DB v0 is a single
SQLite file under `data/` (committed while small): zero services, standard
tooling, resumable batch jobs keyed by canonical form.

## D-0008 (2026-07-16) — A2 corona conventions: Kaplan's H_c

Corona of a patch = congruent copies with disjoint interiors, each touching
the patch, covering every empty cell that shares at least a vertex with the
patch; holes (bounded empty edge-connected regions) forbidden at every
level — this is H_c of Kaplan arXiv:2105.09438, chosen so that a future
polyiamond substrate can validate directly against his published data.
Depth claims: "H ≥ k" carries a machine-verified certificate (the corona
chain); "H = k" is an exhaustion result valid only when no budget was hit,
like UNSAT — it carries the budget stamp instead. Latest verdict per shape
in the DB is the operative one (escalations append, never overwrite).

## D-0009 (2026-07-16) — A3 = disk exact cover; SAT (CaDiCaL) is the workhorse

A3 patches are posed as exact cover of a disk-shaped cell region (copies
may overhang; enclosed empty cells are uncovered region cells, so
hole-freeness needs no separate check). Measured on the hat: greedy
most-constrained-first filling with backtracking and restarts walls near
~250 tiles — wrong early commitments hide beyond chronological
backtracking; the A2 corona engine is worse as a grower. The spec's SAT
prescription is therefore adopted now rather than later: `python-sat`
(CaDiCaL 1.9.5) is the project's first external solver dependency. Trust
boundary: solver models are decoded and re-verified by our own exact
verifier before storage, and UNSAT results are recorded as exhaustion
verdicts ("disk-cover-refuted", pose-free when no seed is pinned), so no
claim ever rests on the solver alone. The pure-Python greedy grower is
kept for the growth-profile feature and as fallback. Known limit: CNF
size (~11M clauses at 9×10⁴ cells) caps single-shot patches around 10⁴
tiles; incremental encoding is the recorded escalation path.

## D-0010 (2026-07-16) — Vendored spectre generator; float scope for A4

Two related decisions for M4.

**Vendored reference generator.** The user-provided exact spectre /
Tile(1,1) substitution generator is vendored source-only at
`vendor/spectre/` (Rust crate + `gen_tables.py`; our initial addition is an
anchor-dump binary; A6 later adds a validation-only ancestry dump). Role:
E4/A4 calibration source with exact rank-4
module ground truth, and later the known answer A6 hierarchy mining must
re-discover (program §4 A6 cites `gen_tables.py`'s loop explicitly). It
is a *generator* for one known tiling: it never produces evidence about
candidate shapes, so D-0005 requires only that its output be
cross-validated (done three ways: upstream's own suite, our Python
module12 port reproducing the reference float leaves, tile-count
recurrence + single-chirality checks in `tests/test_spectre_vendor.py`).
The rank-4 module math (deferred in D-0003) enters the codebase now as
`substrate/module12.py`, validated against the same reference.

**Floats in A4.** The "exact arithmetic in the search path" rule
(D-0003) is scoped: A4's spectral analysis (FFT power spectra, peak
detection, module-rank indexing; numpy) is numerical by nature and runs
on floats. This is acceptable because A4 emits *prioritization signals*,
never certificates or exactness claims, and its trustworthiness is
established empirically by the E4 gate (reference patches must reproduce
literature signatures) rather than by arithmetic exactness. All geometry
feeding A4 (patch certificates, module coordinates) remains exact; the
float boundary is the projection to Cartesian points at analysis time.

## D-0011 (2026-07-16) — E4 reference semantics; bounded indexer accepted for A4 v0

**Reference semantics.** Penrose and Ammann–Beenker calibration patches are
canonical cut-and-project vertex sets from Z⁵ and Z⁴ with projected-cube
windows. Taylor–Socolar is limit-periodic, so forcing a finite module-rank
answer would be wrong; E4 instead requires consecutive reciprocal scales
`b_n = 2^-n b_0` and verifies that erasing level labels collapses the signal
to the ordinary triangular lattice. Random square–triangle tilings use the
published stochastic boundary-growth rule, collision-checked before
insertion, followed by interior-disk cropping and incoherent ensemble power.
Their twelvefold short-range peaks are expected; the negative control is the
small background-subtracted mass in *narrow* peaks, measured only on a shared
grid/extent. None of these numerical diagnostics is a certificate.

**Indexer decision.** Do not add fpylll/PSLQ yet. The existing bounded
integer indexer recovers the exact known finite ranks across the complete E4
library, survives patch doubling and deliberately rotated/sheared inputs,
and yields zero confirmed quasicrystal false positives over 10,000 randomized
periodic tilers. Nine coarse-grid periodic cases initially reached rank 4;
all fell back below rank 4 at the fixed confirmation grid. Therefore A4 v0
adopts mandatory second-resolution confirmation for rank ≥ 4 emitted by a
reduced-resolution/high-throughput screen, and accepts the bounded indexer
for prioritization. LLL/PSLQ remains the escalation path if a future
reference, transform, or control falls outside this empirical envelope.

## D-0012 (2026-07-16) — A6 blind/validation split; exact local mining

**Data separation.** A6 discovery may read only physical tile geometry and
poses. The vendored `hierarchy` dump is a validation oracle: it is generated
to a separate file and opened only after a rule and complete partition have
been fixed. Rows are joined to the ordinary anchor dump by exact pose, never
by traversal order. Tile kind and child path are ignored by the miner.

**Exactness.** Local neighborhoods are ordered by squared module distance in
`Q(sqrt(3))`, canonicalized by exact dihedral pose arithmetic, matched by exact
pose lookup, and accepted only through an exact disjoint cover of the whole
patch. No floating-point geometry enters discovery or verification; Cartesian
projection is used only for the SVG artifact.

**Phase ambiguity.** Pose-only exact cover does not by itself make the
immediate composition recognizable: two one-deletion phases survive on both
the training and larger confirmation patch. A6 v0 ranks this exact-cover tie
by adjacency cohesion (maximize shared tile edges, then minimize exposed
edges), which selects the phase that afterward matches withheld ancestry
exactly at levels 1–4. This is a calibrated mining heuristic, not a forcing
proof. M5 remains open until recursive labelled closure and collared
unique-composition checks remove reliance on that ranking.

## D-0013 (2026-07-16) — A6 recursive graph transfer and collared states

**Scale-specific rules.** Spectre's exact child translations are constructed
from the previous supertile boundary and vary by level; A6 must not pretend
there is one stationary integer-module inflation map. Instead, recover one
exact 8/7 pose rule per scale. A locally mined rule on the smaller patch is
applied to the next larger patch; equal-sized abstract contractions are then
aligned by exact colored adjacency-graph isomorphism, and the known partition
is transferred to expose the next scale's rule.

The current isomorphism engine is joint one-dimensional color refinement over
exceptional/nonexceptional node colors and physical-boundary adjacency. It is
accepted only when refinement is discrete and the resulting bijection exactly
preserves every edge. Ambiguous refinement is an honest failure; no arbitrary
node matching is allowed.

**Collared states, not forced names.** Unlabelled Spectre supertile interiors
form only two congruence classes, so the supplied nine labels cannot be
recovered from interior shape alone. A6 therefore retains exact oriented
radius-1 collar states. On the calibration patch these give 17 interior states;
withheld labels are opened afterward and every state is label-pure. Each state
also has one exact ordered child-collar pattern on all fully collared samples.
This 17-state table is the operative blind substitution candidate. It is not a
recognizability certificate until all legal collars—not only observed
collars—are enumerated and unique composition is checked by SAT.

**Scaling exact cover.** Candidate occurrence hypergraphs are decomposed into
independent overlap components before search. This preserves exact solution
counting while avoiding recursion depth proportional to thousands of
independent parents.

## D-0014 (2026-07-16) — A6 stationary state alignment and finite forcing gate

**One alphabet, not two arbitrary colorings.** A6 v1 numbered radius-1 collar
signatures independently on the child and parent contractions. Both sides had
17 classes, but their integer IDs denoted different scale-local signatures, so
the recorded table was not itself a stationary substitution. A6 v2 aligns the
equal-sized parent contraction with the previous patch's child contraction by
the exact graph isomorphism from D-0013, and matches same-scale child signatures
directly. The resulting normalized states `0..16` occur on both sides, every
state has one rule, the child alphabet is exactly the parent alphabet, and the
transition graph is strongly connected.

**Recursive closure replaces the phase heuristic.** The immediate physical
miner honestly returns two exact 9/8 phases on both training and confirmation
patches. The old edge-cohesion score chose the correct one, but is no longer a
trust dependency: only one phase admits the recursively unique exceptional-
child hierarchy `496→63→8→1`; the other leaves two incompatible next-level
compositions. The score is retained only as a diagnostic and agrees with the
closure result.

**Finite local forcing certificate.** Radius-1 physical edge neighborhoods
stabilize at 32 states between the level-4 and level-5 patches. They induce 19
legal parent patterns for the recursively closing phase. When all 11,715
geometric occurrences from both phases are offered, exactly the selected
3,905-parent cover remains legal; the other 7,810 occurrences are rejected.
CaDiCaL checks all 19 pattern cases and finds no alternative composition.
At the next scale, the two visible 8/7 metatile types already force grouping
(310/310 complete contexts); the radius-1 17-state refinement additionally
rejects every competing fully colored occurrence and is SAT-unique on all 17
state cases (309 complete finite-patch representatives).

This closes M5's computational calibration gate and unblocks E1. The JSON
artifact is the verified case table; emitting a Lean wrapper around it belongs
to E10, not to the runtime funnel. The traditional two-tile Gamma/Mystic fusion
is not needed by this recovered 9/8 hierarchy certificate and remains optional
reference-structure archaeology rather than a gate blocker.

## D-0015 (2026-07-16) — Disk patches use exact core-plus-halo A6 covers

Generated reference supertiles can be covered completely by parent clusters;
A3 candidate patches are disk cuts and generally cannot. For E1, A6 therefore
requires every tile in a fixed interior core to belong to exactly one parent,
permits a parent to use tiles from the surrounding halo, enforces at-most-one
use of every halo tile, and does not require the outer halo itself to compose.
CaDiCaL enumerates composition multiplicity up to two. This is an exact
finite-region statement and avoids either discarding boundary-crossing parents
or pretending the disk boundary follows a substitution boundary.

Kite-grid placements embed without approximation in the existing module:
hex `(x,y) → (x,0,y,0)`; rotations advance by two module steps; the reflected
D6 operations use the matching module reflection/rotation pair. Exact nearest
anchor mining is accelerated by expanding hex-lattice boxes whose omitted
points have a proved quadratic-distance lower bound.

## D-0016 (2026-07-16) — Hat A6 composes to unique anchors before unique ownership

The first hat screen initially described two candidate rules and “two
compositions.” Both phrasings were too coarse. The solver count was capped at
two (there are at least twenty covers), and the two rules share the same
eight-hat scaffold: they are two allowed one-child exception positions in one
three-type family (`full-8`, exception A, exception B).

Different exact covers reassign a small number of physical hats between
neighboring parents, but the contracted parent poses are invariant. On the
current disk, twenty sampled covers give the same 315 parent anchors. A
separate SAT backbone query—not sampling—proves all 141 anchors in the safer
inner core occur in every cover: 97 allow only `full-8`, 22 allow full/A and
22 allow full/B. Thus A6 should distinguish **anchor recognizability** from
**ownership recognizability**. The former is enough to continue mining the
abstract hierarchy; the latter remains an additional forcing obligation.

This correction is recorded rather than silently replacing the earlier
artifact semantics. “Candidate” in this A6 context means a hierarchy
hypothesis for the already-known hat, never a new monotile.

**Recursive state is the option set, not an arbitrary ownership choice.**
The invariant parent alphabet is the three allowed-type sets `[full]`,
`[full,A]`, `[full,B]`. Mining exact nearest 7/8 groups colored by those
states, then minimizing the finite pattern library by MaxSAT, yields 15
patterns on a 430-parent training core; every selected pattern has arity 7.
Fixing that library makes the complete 430-parent training cover unique:
71 groups and 71 distinct anchors are SAT-forced (zero optional alternatives).
Treating those pattern IDs as the next scale's states gives a second exact
contraction on a 43-anchor nested core: a minimum eight-pattern library
(six arity-7, two arity-8) forces nine groups with zero alternatives. This is
accepted as recursive closure evidence, but the small disk cut does not yet
contain enough halo to close the final nine anchors to one root.

## D-0017 (2026-07-16) — Recursive libraries are shared cross-patch objects

A minimum finite pattern set learned on one disk is not itself a substitution
language. On the first hat disk, 15 arity-7 patterns force a complete
contraction. A separately solved doubled disk also has a 15-pattern optimum,
but only 13 patterns coincide; freezing the first optimum makes the second
exact cover UNSAT. Taking the 17-pattern union is also invalid because it
admits optional compositions.

A6 therefore fits recursive libraries jointly across calibration patches:
pattern-presence variables are shared, while each patch has independent
exact-cover constraints. The accepted first-level optimum is 16 arity-7
patterns and forces both patches (`430→71` and `430→72`). Applying the same
rule to their contractions yields a shared 15-pattern library (six arity 7,
nine arity 8) forcing `43→8` and `41→8`.

Pattern states are the normalized indices of the selected shared patterns,
ordered canonically. They are not IDs from the larger patch-local catalogue
of every observed pattern. Verification must also use the shared option-state
alphabet: locally renumbering a subset changes colored pattern semantics.

This finite two-patch result is stronger than count stability but remains a
calibration certificate, not a theorem for every infinite hat tiling.
Physical-hat ownership ambiguity is unchanged, and an eight-node terminal
layer is not counted as another replicated recursive scale.

## D-0018 (2026-07-16) — A4 free coefficient bound follows patch doubling

Making the r²=100,000 hat certificate the default exposed rank 5 in the
bounded module indexer, despite the r²=50,000 patch giving the literature
rank 4. The issue was not the peak floor, tolerance or symmetry vote. Past the
100 strongest peaks, a true module relation needed a coefficient of magnitude
7 or 8; the calibrated free-generator enumeration stopped at 6.

The A4 default `coeff_bound` is raised from 6 to 8. The separately solved
generator pair retains `pair_bound=48`. Both stored hat sizes now give rank 4
and sixfold symmetry in one slow regression. A larger representation bound
makes more integer relations available rather than declaring new generators;
the wider reference and null suite remains green. It is still a bounded
empirical indexer under D-0011, not a general exact integer-relation
algorithm.

## D-0019 (2026-07-16) — A0 compiled fixed-key stream for E1 scale

The Python breadth-first enumerator remains the readable reference, but its
tuple/set representation reaches n=12 in 53.48 s and becomes impractical near
the E1 horizon. A0's production path is therefore a standalone exact Rust
tool using the identical cell adjacency and twelve-operation canonical form.

For n≤16, canonical shapes are fixed 32-byte keys. Coordinates are packed only
after translating the lexicographically first transformed cell to the origin;
range and parity invariants are asserted. Counts match OEIS A057786 through
n=16, including 19,035,075 shapes at the required horizon in 364.48 s and
1.35 GiB peak RSS.

Downstream stages consume a versioned fixed-width binary stream (`A0PK`).
Stream order is unspecified because it comes from a hash set. Generated files
under `data/a0-compiled/` are ignored reproducible artifacts; source code,
format reader and cross-implementation tests are committed. This closes A0
capacity only. A1/A2 must gain compiled streaming filters before the complete
19-million-shape E1 sweep is operational.

## D-0020 (2026-07-16) — A1 compiled torus screen is a sound retirement filter

The Python A1 torus implementation is ported exactly to Rust for `A0PK`
streams: the same HNF sublattices, quotient placements, exact-cover branching,
node budget and independently checkable certificates. Shapes are removed only
when a cover is found. Refuted and budget-exhausted cases both remain in the
survivor stream, so parallel screening cannot discard an aperiodic candidate
without positive periodic evidence.

The n=8 Myers anchor is reproduced exactly (39 periodic, 834 survivors, zero
exhaustions), and Python independently verifies every one of the 60,477
certificates emitted at n=9..16. Sixteen record-range workers screen the full
n=16 level in 673.06 s.

This stage is not expected to reduce uniformly. The quotient must contain an
integer number of n-cell tiles, so the frozen k≤12 budget depends strongly on
n: n=13 has no admissible index, while n=16 tests only k=8 (three tiles per
domain). Such shapes remain survivors rather than receiving stronger negative
claims. A2 still needs a compiled local-corona filter before the E1 sweep is
practical.

## D-0021 (2026-07-16) — A2 first-corona exhaustion is the compiled bulk filter

The first A2 production filter asks only whether one hole-free corona exists.
It ports the Python definitions exactly: every empty kite sharing a vertex
with the seed must be covered; congruent placements may extend outward but
must not overlap; the completed patch must have no bounded edge-connected
empty component.

A shape is rejected as H_c=0 only after exhausting every exact-cover branch.
A witnessed corona survives with a compact `(op, tx, ty)` certificate, and a
node-budget exhaustion also survives in a separate stream. The n=8 result is
exactly the established census: 720 H_c=0 and 114 survivors. All 40,216
final witnesses at n=9..16 independently pass the Python verifier.

Sixteen workers consume many 25,000-record ranges dynamically. At the
100,000-node budget, five shapes initially exhaust; rerunning only those at
10,000,000 nodes resolves three as H_c=0 and two as witnessed. Thus the final
n=9..16 first-corona corpus has no unknowns. In particular n=16 contracts
from 19,035,046 A1 survivors to 22,875 witnessed A2 survivors in 889.09 s.

This is an exact local refutation and witness stage, not a tiling verdict.
Deeper corona levels are run only on the resulting 40,216-shape stream.

## D-0022 (2026-07-16) — Recursive corona search preserves exact finite depth

Deeper A2 cannot extend only one stored first-corona witness when making a
negative claim: a different first corona might admit another layer. The
compiled solver therefore recursively enumerates every valid corona cover at
each level. A shape is classified below depth d only after all chains fail;
positive chains and budget exhaustions survive.

Coverage uses dynamic state rather than the first-level `u128` shortcut,
because second-corona rings exceed 128 cells on larger shapes. At n=8 the
compiled depth-2 result reproduces the established census: six shapes reach
two coronas, 827 stop below, and one hard H_c=1 case exhausts at 100,000
nodes; 10,000,000 nodes resolves it negatively. At depth 3, exactly one of
the seven conservative inputs survives. Its three-corona chain independently
verifies and its canonical shape is the hat.

Across n=9..16, targeted escalation resolves every depth-2 budget case. The
final 9,841 two-corona survivors all carry Python-verified chains. Depth 3
requires a separate performance design: positive extension is often cheap,
while exhaustive H_c=2 refutation can consume the full million-node budget.
Future runs should try stored-chain extension first, then reserve exhaustive
fallback for within-size ranking and exact negatives.

## D-0023 (2026-07-16) — Depth-3 survivors are candidates, not einstein claims

The recursive A2 bulk run reaches depth 3 on 9,728 n=9..16 shapes and proves
105 exact H_c=2 negatives. Eight additional shapes exhaust the million-node
budget and are conservatively retained. All 9,728 positive chains pass the
independent Python verifier.

Raw depth is strongly size-dependent: 7,371 of the 7,409 n=16 depth-2
survivors reach depth 3, whereas no n=9 or n=11 shape does. Therefore
“candidate” at this point means a within-size local-growth anomaly suitable
for A3/A4, not evidence of aperiodicity or quasicrystalline order. The eight
10M-node audit attempts experienced a process/session transport failure and
produced no result; they remain explicitly unknown rather than being inferred
from empty output.

Human inspection starts with the complete smallest new witnessed sets: both
n=10 candidates and all eight n=12 candidates are rendered in one SVG. These
are genuinely new shapes from the exhaustive blind corpus, unlike the earlier
hat A6 drawings, which showed two hierarchy exception variants of the same
known hat.

## D-0024 (2026-07-16) — One smallest-corpus shape earns finalist status

The ten smallest witnessed depth-3 shapes were promoted together, without
visual preselection, through pose-free A3. One n=10 shape is exactly refuted
at r²=800. The other nine initially grow through r²=12,800, but an exact A1
audit beyond the production k≤12 budget finds torus certificates for all
eight n=12 shapes at index 16. Those are periodic budget escapes and are
retired regardless of their finite-patch A4 estimates.

The remaining shape is n=10 candidate 2, canonical compiled key
`010001010104010502f002f1030b030c04fa04fb`. It has:

- no exact torus certificate through index 100, with no SAT budget
  exhaustions over the 20 arithmetically admissible quotient indices;
- a pose-free, independently verified r²=50,000 disk patch of 9,239 tiles;
- rank-4 diffraction at both 2,404 and 9,239 anchors, with sixfold symmetry
  recovered on the larger patch.

This earns **high-priority E1 finalist** status, not an einstein verdict.
Finite disk growth does not prove an infinite tiling; a bounded torus search
does not prove aperiodicity; and A4 is a prioritization signal. The next
obligations are independent large-patch solutions, a deeper/structurally
different periodicity attack, and blind A6 hierarchy/forcing analysis.

The exact SAT torus audit subsequently extends the contiguous no-certificate
range through index 215 with no budget exhaustions. Additional completed
indices 225, 230, 235, 245 and 265 are also UNSAT, but the requested 105–300
parallel run was interrupted because unreturned HNF-heavy indices formed an
hour-scale tail. They remain unclassified; no contiguous claim beyond 215 is
made. All targeted period-47 cylinders through transverse width 25 (quotient
indices 235–1,175) are UNSAT.

## D-0025 (2026-07-16) — A4 promotion requires independent patch robustness

The first finalist's deterministic r²=50,000 patch contains an exact
period-47 translation across a central 706-tile comparison region, and its
rendered exterior crown appears gapped. The two observations require separate
treatment:

- the A3 certificate has zero missing kite cells among all 90,714 required
  disk cells; the visible gaps lie outside the certified disk, where tile
  overhang is allowed but coverage is not required;
- a single SAT model may contain periodic approximant domains, so a global
  rank-4 FFT is not sufficient promotion evidence.

A4 promotion now requires independently biased A3 solutions. Four phase-seed
patches at r²=12,800 have pairwise placement Jaccard overlap below 0.067, yet
all retain estimated Fourier-module rank at least 4 at both 1024² and 2048²
resolution. The exact period-47 stripe does not persist across them; their
strong approximate translations instead recur at 18- and 29-step scales.
Symmetry votes are less stable at 2048² (2, 3 or 6), so “sixfold” remains a
large-patch observation rather than a patch-independent invariant.

The finalist remains prioritized because rank≥4 survives independent
solutions, not because one visually regular patch was labeled
“quasicrystal-candidate.” A4's rank and symmetry remain numerical ranking
features, never proof.

A coefficient-bound and peak-depth stress test further separates the
candidate from the periodic control. Raising the solved-pair coefficient
bound from 48 to 384 does not reduce its rank. Both the calibrated hat and
the candidate are rank 2 on the strongest 20–40 substrate peaks and rank 4
when the satellite set reaches 60–400 peaks; the periodic control remains
rank 2 throughout 20–400. The candidate therefore reproduces the calibrated
quasicrystal control's rank-transition profile, while still requiring exact
periodicity and hierarchy follow-up.

## D-0026 (2026-07-17) — A3 promotion is based on nested cores, not disk covers

The user's "crown gaps" observation concerned continuability, not uncovered
cells. Re-testing with exact required-placement clauses confirms the issue:
all five r²=12,800 finalist patches are UNSAT when frozen in full and enlarged
even to r²=16,000. Their final crowns are dead ends. The earlier response that
only checked zero missing cells inside the disk answered the wrong question.

Progressively thawing the boundary finds extendable cores, but with substantial
solution dependence. For enlargement to r²=16,000, two patches preserve cores
through r²=9,000, one through 10,000, and two require retreat to r²=5,000.
Thus roughly 36–73% of placements survive, with collars about 2–6 tile
diameters deep.

The candidate nevertheless has a machine-verified nested chain:

1. 1,576 placements of a phase-seed-1 r²=12,800 patch, wholly inside the
   r²=9,000 core, remain literal placements in an r²=50,000 patch;
2. 5,317 placements of that r²=50,000 patch, wholly inside r²=30,000, remain
   literal placements in an r²=100,000 patch of 18,386 tiles.

Full crowns at both scales remain non-extendable. Consequently independent
disk size and tile count are demoted to diagnostics. A3 promotion requires a
growing sequence of frozen cores and reports retained-core radius, placement
fraction and collar depth. Two nested steps are stronger evidence but still
not an infinite-tiling proof.

The genuinely nested r²=100,000 outer patch retains the A4 rank-4/sixfold
signature at 18,386 anchors. Spectral prioritization therefore survives the
nested-growth correction, although the collar instability lowers confidence.

## D-0027 (2026-07-17) — Adopt theory program v0.2 and claim governance

The theorem-producing track in
`docs/program/theory_research_plan.md` v0.2 is adopted. It runs alongside the
computational funnel through four coordinated workstreams: W1 exact transfer
automata, W2 algebraic obstructions, W3 substitution certificates and W4 grid
rigidity. Finite-patch, numerical and budget-limited results remain evidence
for prioritization; none is promoted to a theorem without satisfying the
explicit proof obligations.

Within the grid-aligned scope, the periodic-completion theorem T0.1 collapses
weak and strong aperiodicity: if any tiling has a nonzero translation period,
the associated one-dimensional finite-type quotient has a periodic point and
therefore yields a rank-2 periodic plane tiling. Accordingly O1, O2 and O4 are
one obligation, while existence O3 and geometric scope O5 remain separate.
T0.1 is initially recorded as a proof draft pending independent audit and a
literature check.

Claim status is governed by `docs/theory/PROOF_LEDGER.md`. Stable theorem and
obligation IDs link the roadmap, proof text, implementations, tests,
experiments and final exposition. Chronological notebooks and raw artifacts
remain append-only evidence; they do not override the ledger.

W1 starts with a pure-Python higher-block reference engine. It must cover every
nonzero period vector, including nonprimitive vectors and their quotient
torsion, reconstruct positive A1-compatible certificates, and attach a finite
completeness/exhaustion witness to every negative result. Empty-frontier-only
reachability is explicitly insufficient because it can miss a closed recurrent
component. Budgeted cylinder SAT sweeps remain useful controls but cease to be
the intended proof mechanism once W1 passes its validation anchors.

The W3 hat gate extends G1 to theory claims: no new finalist substitution or
forcing certificate is trusted before the same blind pipeline closes on the
hat. The dossier organization and paper extraction map live in `docs/theory/`.

## D-0028 (2026-07-17) — W1 negatives require complete independently verified graphs

A W1 `cycle-free` claim is accepted only with a complete finite manifest:
geometry-derived placement patterns, all crossing contributions, every state
and transition, transition witnesses, and a topological ordering of all states.
A graph hash alone is a reproducibility fingerprint, not a certificate.

The verifier must recompile geometry and independently re-enumerate the state
and transition relations without calling the producer's graph routines. It
must reject missing states, missing edges, invalid topological orders and
cyclic instances. This gate now passes on the Myers-validated two-kite
non-tiler and four hat vectors.

Under that standard, the finalist's 11 exact D6 orbit representatives cover
all 90 nonzero center-lattice vectors with Q(v)=x²+xy+y²≤25, including
nonprimitive vectors. Every complete graph is independently verified acyclic,
with no resource exhaustion. We therefore accept the scoped theorem T1.2-25:
no grid-aligned finalist tiling has a translation period in that norm ball.
This does not close O1 outside the finite bound or O5 outside grid alignment.

## D-0029 (2026-07-17) — W1 norm proofs use incremental shell archives

Complete negative manifests grow much faster than their graph summaries. The
four certificates for 25<Q≤36 occupy 51 MB even though graph production remains
easy. Bounded-norm theorems will therefore be archived as independently
verified shells, each listing its exact D6 orbit coverage and source hashes,
rather than repeatedly embedding every lower-norm certificate.

The new shell covers 36 vectors in four orbits with zero cycles/exhaustions.
Together with T1.2-25 it establishes T1.2-36 for the grid-aligned finalist.

## D-0030 (2026-07-17) — Retire isolated-character Layer B; proceed to integral SNF

W2 Layer A is accepted after zero false exclusions on all 60,477 materialized
periodic certificates. For the finalist its prime sector coloring reproduces
the area class k≡0 mod 5 and adds no further kills.

The roadmap's proposed nontrivial single-character infeasibility test is
retired. The Fourier transform of the constant torus target vanishes at every
nontrivial character, making each isolated projected system homogeneous and
always solvable by zero amplitudes (T2.B0). Characters remain computational
decomposition tools, but the next obstruction experiment is the full integer
incidence module via Smith normal form, where cross-character integrality is
retained.

## D-0031 (2026-07-17) — Layer C starts with modular cokernels; full SNF stays separate

No exact Smith-normal-form library is installed (SymPy, FLINT/python-flint,
Sage and PARI interfaces are absent). Layer C therefore starts with compact
finite-field cokernel witnesses rather than adding an unreviewed dependency.
A positive witness wᵀM=0, wᵀ1≠0 mod p is exact quotient UNSAT; failure to find
one is unknown and never reported as feasibility.

The GF(2) slice passes zero-false-exclusion validation on all 60,477 compiled
periodic certificates. For the finalist it kills 36 of 742 area-admissible HNFs
through index 60. A uniform support formula proves, subject to proof review,
that HNF (1,0,k) is impossible for every k≥4, giving the first W2 infinite
quotient family. Full integer SNF remains a distinct unfinished milestone and
requires either an audited local algorithm or an explicitly adopted exact
dependency.

## D-0032 (2026-07-17) — Adopt exact normal-form dependencies; HNF at scale

The user authorized project-local dependency installation. We pin SymPy 1.14.0
and python-flint 0.9.0 for W2 Layer C. SymPy and FLINT independently agree on
Smith rank, top determinantal divisor and membership for rank, torsion-index
and compatible controls. FLINT is the production backend.

Full Smith diagonalization suffers severe coefficient swell on some larger
finalist incidence matrices. The census therefore uses the mathematically
equivalent canonical row-Hermite test: transpose the placement matrix and ask
whether adjoining the all-ones row changes its canonical integer row lattice.
Smith remains the reference derivation and control implementation. This is an
exact backend choice, not a relaxation.

Across all 742 area-admissible finalist HNFs through index 60, integral normal
forms kill exactly the 36 quotients already killed modulo two and find no
same-rank torsion-index obstruction. The other 706 admit unrestricted integer
solutions, not 0/1 covers. W2 therefore moves to positivity/integrality-aware
family certificates or nonabelian holonomy rather than extending the same bare
integer-cokernel calculation.

## D-0033 (2026-07-17) — Retire ordinary LP positivity via translation averaging

Before adopting a numerical LP dependency, we proved that nonnegative rational
incidence feasibility on a torus is exactly a six-dimensional sector-profile
cone problem. Translation averaging makes a feasible cover constant on
placement orbits, and conic Carathéodory bounds a witness by six profiles. The
producer solves these systems over exact rationals; the verifier expands each
compact result and checks every full incidence row with `Fraction` arithmetic.

Across the 742 finalist HNFs through index 60, the cone test obstructs exactly
the same 36 rank/GF(2) cases and gives verified fractional covers for all 706
others. Ordinary nonnegative LP therefore contributes no additional finalist
discrimination at this horizon. We will not add SciPy/HiGHS for this layer.
Further W2 work must retain binary exact-cover combinatorics or use nonabelian
holonomy; a fractional cover is never reported as a tiling.

## D-0034 (2026-07-17) — Binary family certificates compose W1 with HNF membership

The first binary family layer reuses W1's complete cycle-free transfer
certificates instead of inventing a second SAT proof format. If an HNF lattice
contains a certified-impossible vector, any quotient exact cover would lift to
a tiling having that vector as a period. Exact membership is the two-congruence
test `d|y` and `a|(x-(y/d)b)`.

The 126 vectors through Q=36 therefore define 126 infinite quotient families.
They cover every HNF through index 36 and 2,941 of the 8,864 area-admissible
HNFs through index 215. Separately, exact D6 lattice maps extend T2.C1 from
`(1,0,k)` to all three thin families for every k≥4. Missing certificates retain
unknown polarity.

## D-0035 (2026-07-17) — Layer D requires binary boundary-network coupling

We audited Conway--Lagarias (1990) directly and reproduced their p3 Cayley
winding proof control with exact Eisenstein-affine arithmetic. This primary
anchor is mandatory before finalist use.

The finalist boundary presentation has 2,556 surjections to S3, so nonabelian
targets exist. Nevertheless exhaustive displacement-kernel analysis finds zero
commutator obstruction: most maps lose all zero-displacement information and
the rest retain only A3 parity, for which every pair of cosets has commuting
representatives. A canonical displacement word may also cross tile interiors,
so treating it as a boundary holonomy would be unsound.

Layer D will therefore use the connected boundary skeleton of the selected
binary exact cover. Its certificate/CSP must jointly encode placement choices,
active tile-boundary edges, finite-group potentials and commuting twisted torus
conditions. The uncoupled displacement-commutator shortcut is retired, and no
Layer-D finalist exclusion is currently claimed.

## D-0036 (2026-07-17) — Accept coupled S3 cores; index 40 is closed

Layer D now uses an at-least-cover relaxation coupled to finite-group boundary
potentials. Overlap is permitted deliberately: every genuine exact cover is a
model of the placement clauses, so UNSAT for all commuting twists is a sound
torus exclusion while SAT remains unknown. One-kite tori and the independent
three-tile shape-392 torus pass in both relaxed and exact modes.

The finalist's 234 order-3-kernel S3 surjections reduce to 39 classes under
simultaneous inner conjugacy. The first fixed map adds no exclusions among the
96 W1-family survivors at admissible indices 40--60, but exhaustive class
search at index 40 finds six killing classes for each of its three survivors:
`(10,3,4)`, `(40,11,1)`, and `(40,28,1)`. Their placement-only relaxations are
SAT. Thus the separation is genuinely nonabelian rather than ordinary cover
UNSAT.

Solver UNSAT is accepted only after proof replay. PySAT's CaDiCaL-1.9.5 proof
stream failed `drat-trim` because it omitted a checkable terminal conflict, so
it is retained only as the search solver. Glucose 4 produced the certificate
traces. For one killing map per HNF, all 18 twists (54 instances) have stored
compressed core CNFs and DRAT proofs independently verified by `drat-trim`;
the standalone verifier regenerates the canonical CNF and checks each core is
a clause subset before proof replay.

Together with area and T2.C4-36 this proves the finite grid-aligned quotient
prefix through index 40. It does not prove O1 or aperiodicity: larger period
lattices remain open.

## D-0037 (2026-07-17) — Promote the index-45 shell after 162 proof replays

The nine index-45 HNFs surviving the W1 period families were tested against
all 39 order-3-kernel S3 conjugacy classes. Every HNF has at least six killing
maps. Only nine maps kill anything, and they split into three triples with
identical within-triple HNF signatures. This is recorded as a finite exact
pattern, not extrapolated into an infinite HNF-family theorem.

One killing map per HNF was selected by the deterministic lowest-index rule.
All 18 twists for all nine HNFs have stored Glucose/core-DRAT certificates:
162/162 independently verify through `drat-trim`, canonical-CNF regeneration,
core-subset checking and hash replay. The 377,474,096-byte compressed payload
is accepted despite its size because it upgrades the shell from solver output
to an independently replayable finite theorem.

At index 45 the certificate split is 69 period-family kills plus nine Layer-D
kills, exhausting all 78 HNFs. With area and the prior shells, the complete
grid-aligned quotient prefix is therefore closed through index 45. O1 remains
open. The next research priority is to explain the three map signatures
symbolically before scaling the same brute-force matrix to index 50.

## D-0038 (2026-07-17) — Quotient Layer D by exact diagonal D6 symmetry

The index-45 signature pattern is the visible projection of an exact diagonal
point-group action. A geometric operation moves the HNF lattice covariantly
and pulls the six-generator S3 boundary map back by its inverse. Model
transport gives a bijection of placements, potentials and commuting twists,
so Layer-D satisfiability is constant on these pair orbits (T2.D3).

The machine certificate checks all 351 matrix entries under all 12 operations
(4,212 comparisons). The nine HNFs form orbits of sizes three and six; the 39
maps form seven orbits; and the nine effective maps are exactly two entire map
orbits. The raw matrix reduces to 43 diagonal pair orbits.

Future finite Layer-D shells will scan one representative per diagonal orbit
and record the complete orbit expansion. This is an exact logical reduction,
not a heuristic pruning rule. Positive exclusions still require independently
replayed UNSAT proofs; symmetry does not change certificate polarity.

## D-0039 (2026-07-17) — Record S3 saturation at index 50; keep prefix at 45

The exact D6 reduction turns the index-50 18x39 matrix into 81 representative
scans. Four are UNSAT over all twists and 77 are SAT. After orbit expansion,
one six-HNF orbit is excluded and two six-HNF orbits survive every strong S3
boundary map.

The positive side is accepted: one lowest killing map per excluded HNF gives
108 Glucose/core-DRAT pairs, all independently replayed from regenerated
canonical CNFs. The negative/saturation side is also made auditable: all 77
SAT pair-orbit representatives have explicit truth assignments checked clause
by clause against regenerated CNFs. These assignments witness only the relaxed
at-least-cover holonomy systems, never tilings.

Therefore the six exclusions are promoted as finite theorems, but index 50 is
not closed and the complete quotient prefix remains 45. Re-running the same
39 S3 classes at larger indices is no longer the main path. Next inspect the
surviving model structure and then enlarge or refine the nonabelian target.

## D-0040 (2026-07-17) — Retire connectivity and overlap-two as S3 repairs

All 77 verified relaxed survivor models have connected active tile-boundary
networks, so adding connectivity would not separate them. Every original model
overlaps, but the complete experiment with cell multiplicity capped at two
reproduces exactly the same 77 SAT / four UNSAT pair-orbit matrix and the same
six-HNF exclusion orbit. Explicit assignments for all 77 bounded-overlap SAT
instances verify clause by clause.

We therefore reject both easy repairs as explanations of index-50 saturation.
The at-most-two encoding remains available as a diagnostic and proof-strength
ladder, but it adds no finite exclusion here. Layer D should next seek a richer
finite quotient of the boundary presentation, or a different invariant that
couples selected placements beyond local coverage multiplicity.

## D-0041 (2026-07-18) — Select A4 as the complementary target; close index 50

The exact small-nonabelian-target census selects A4 over D4 and Q8 for the
first controlled escalation. A4 has only 48 proper-kernel inner classes,
versus 1,824 for each order-eight target, and its normal displacement kernel
is V4. The residual C3 quotient is complementary to the C2 information in the
strong S3 maps rather than merely making the same target larger.

This choice closes the finite shell. Sixteen of 48 symmetry-reduced HNF/map
pairs are UNSAT for all 48 commuting twists, and their D6 expansions cover all
12 HNFs that survived S3. The complementary 32 pairs have explicit models
checked against every regenerated clause. For promotion, map 7 was fixed on
all 12 HNFs and all 576 direct twist instances received independently checked
DRAT cores; a separate cold process rebuilt and replayed 576/576.

We therefore promote T2.D2-50 and the complete grid-aligned quotient prefix
through index 50. This is not O1 and is not evidence of tiling existence. The
shared killing-map signature—three distinct V4 values on the final three
generators—should be attacked symbolically before an indiscriminate larger
finite-shell census; index 55 is the next finite control for any proposed
family theorem.
