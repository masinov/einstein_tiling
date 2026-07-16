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
