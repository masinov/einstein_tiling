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

Human inspection starts with the complete smallest witnessed sets: both n=10
shapes and all eight n=12 shapes are rendered in one SVG. **Correction
(D-0048/ERR-003):** n=10 candidate 2 is exactly the known Turtle. The gallery
is therefore a blind-survivor gallery, not a gallery of ten novel shapes.

## D-0024 (2026-07-16) — Blind promotion rediscovers the Turtle

> **Superseded classification (D-0048/ERR-003):** this experiment's numerical
> results stand, but “finalist” is a legacy alias for the known Turtle and not
> a novelty classification.

The ten smallest witnessed depth-3 shapes were promoted together, without
visual preselection, through pose-free A3. One n=10 shape is exactly refuted
at r²=800. The other nine initially grow through r²=12,800, but an exact A1
audit beyond the production k≤12 budget finds torus certificates for all
eight n=12 shapes at index 16. Those are periodic budget escapes and are
retired regardless of their finite-patch A4 estimates.

The remaining shape is n=10 candidate 2, now identified exactly as the Turtle,
with canonical compiled key
`010001010104010502f002f1030b030c04fa04fb`. It has:

- no exact torus certificate through index 100, with no SAT budget
  exhaustions over the 20 arithmetically admissible quotient indices;
- a pose-free, independently verified r²=50,000 disk patch of 9,239 tiles;
- rank-4 diffraction at both 2,404 and 9,239 anchors, with sixfold symmetry
  recovered on the larger patch.

At the time this earned **high-priority E1 finalist** status. D-0048 retracts
that status: the computations are instead a blind Turtle rediscovery and a
known-aperiodic control. Finite disk growth, bounded torus searches, and A4
remain only internal evidence; the Turtle's tilability and nonperiodicity come
from the published proofs.

The exact SAT torus audit subsequently extends the contiguous no-certificate
range through index 215 with no budget exhaustions. Additional completed
indices 225, 230, 235, 245 and 265 are also UNSAT, but the requested 105–300
parallel run was interrupted because unreturned HNF-heavy indices formed an
hour-scale tail. They remain unclassified; no contiguous claim beyond 215 is
made. All targeted period-47 cylinders through transverse width 25 (quotient
indices 235–1,175) are UNSAT.

## D-0025 (2026-07-16) — A4 promotion requires independent patch robustness

The Turtle control's deterministic r²=50,000 patch contains an exact
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

The Turtle control passed this robustness check because rank≥4 survives
independent solutions, not because one visually regular patch was labelled
“quasicrystal-candidate.” A4's rank and symmetry remain numerical validation
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
all five r²=12,800 Turtle-control patches are UNSAT when frozen in full and enlarged
even to r²=16,000. Their final crowns are dead ends. The earlier response that
only checked zero missing cells inside the disk answered the wrong question.

Progressively thawing the boundary finds extendable cores, but with substantial
solution dependence. For enlargement to r²=16,000, two patches preserve cores
through r²=9,000, one through 10,000, and two require retreat to r²=5,000.
Thus roughly 36–73% of placements survive, with collars about 2–6 tile
diameters deep.

The Turtle control nevertheless has a machine-verified nested chain:

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

## D-0042 (2026-07-18) — Factor A4; promote the certified prefix through 55

The canonical A4 obstruction is no longer treated as an opaque permutation
table. Exact coordinates `A4 = GF(2)^2 semidirect C3` reproduce every group
operation and Layer-D edge equation. For the killing maps, the C3 projection
is the geometric character `±(2x+y) mod 3`. It vanishes on every center-period
translation, so an exact cover can realize only the 16 ordered V4 twist pairs,
not all 48 commuting A4 pairs. We adopt this T2.D4 reduction for later proof
production while retaining all-twist scans as falsification controls.

At index 55, the 21 HNFs not excluded by W1 cross the 16 distinct-V4-tail map
classes into 336 logical pairs and 28 exact diagonal-D6 orbits. Every orbit is
UNSAT for all 48 twists; hence every signature map obstructs every frontier
HNF. For promotion, map 7 was fixed and all 21 x 16 theorem-relevant direct
CNFs received independently verified DRAT cores. A separate cold verifier
regenerated and replayed 336/336 certificates. The 3,021,269,794-byte payload
remains ignored locally; its tracked manifest pins all hashes and provenance.

We therefore promote T2.D2-55. The shell decomposition is 51 W1 exclusions
plus 21 A4 exclusions, with indices 51--54 removed by area. This remains a
finite grid-aligned periodicity theorem, not O1, O3, or O5. The next theory
target is an infinite-family derivation of the persistent V4-tail obstruction,
not merely another larger finite shell.

## D-0043 (2026-07-18) — Record the 2-Lambda blind family; require packing

Factoring out the geometric C3 character turns each distinct-tail A4 map into
a two-bit local coverability SFT. This exact reduction reproduces the complete
index-55 proof matrix cheaply. At index 60 it gives the required
falsification: map 7 obstructs 42 of 45 W1 survivors, while one three-HNF D6
orbit survives all 16 signature maps. No index-60 theorem is promoted.

The escape is explained, not merely observed. Each signature map has an
explicit rank-two-twist model on HNF `(2,0,2)`, and every HNF sublattice of
`2 Lambda` inherits it by covering pullback. Sixteen base assignments and
3,024 finite pullbacks cold-check clausewise. More finite quotient data does
not repair the issue: all 16 maps simultaneously admit one shared three-
placement model. It covers 18 base cells once and six twice, so even the
overlap-at-most-two strengthening passes; its index-60 lifts also verify.

We therefore retire both indiscriminate multiplication of the present finite
boundary quotients and overlap-two as the next Layer-D escalation. The missing
condition is nonoverlap/packing, or a genuinely equivalent density constraint.
These SAT assignments are overlapping pseudo-covers, not tilings, and do not
refute O1. The certified prefix remains 55. The next implementation should
either derive a packing-sensitive invariant from the local V4 colours or move
to W1/W3 recognizability, where packing is native.

## D-0044 (2026-07-18) — Adopt the single-orbit packing refinement

The missing packing information is much smaller than full exact cover on the
three index-60 escapes. Their lifted full-product witness has 45 placements
and exactly 15 colliding pairs; every collision is a translate of placements
`(3,0,0)` and `(5,0,1)`, sharing six kites. Exact geometric classification
partitions all 22,680 torus collision pairs into 40 D6 orbits. We add only the
720 clauses in this one orbit, leaving the other 39 overlap types permitted.

The full 16-signature product plus that single sound orbit is UNSAT on all
three escape HNFs. Glucose proofs were checked and trimmed by `drat-trim`;
a separate cold verifier rebuilt the exact orbit, checked that every added
pair truly overlaps, checked core inclusion and hashes, and replayed 3/3
proofs. The compressed payload is 4,337,057 bytes.

We adopt this as T2.D6 and as the packing-sensitive Layer-D primitive. It
proves that the `2 Lambda` countermodels fail for a sharply local reason rather
than requiring the complete nonoverlap relation. It closes the three hard
index-60 residual HNFs, but T2.D2-60 remains unpromoted until the other 42
map-7 exclusions receive the same independent proof treatment. The result is
finite and does not establish O1, O3, or O5.

## D-0045 (2026-07-18) — Promote the certified quotient prefix through 60

The 42 index-60 HNFs killed by the map-7 V4 SFT now have independently
checkable proof bundles. To avoid 672 separate files, each HNF uses an exact
selector union of its 16 twist components: common cover and potential
variables, guarded component suffixes, and an at-least-one selector clause.
The union is satisfiable exactly when one direct twist component is
satisfiable.

Glucose proved all 42 unions UNSAT. `drat-trim` checked every raw proof and
trimmed core during production; a separate cold run regenerated every union,
checked source, dependency, compressed and uncompressed hashes, verified core
inclusion, and replayed 42/42 certificates. The bundle represents 672 direct
twist cases and occupies 694,971,396 compressed bytes.

The full index-60 shell is now 123 W1 period-family exclusions, 42 map-7
twist-union exclusions, and the three T2.D6 one-orbit packing exclusions.
Indices 56--59 fail area. We therefore promote T2.D2-60: no grid-aligned
finalist exact cover exists on any HNF torus through index 60.

This is still a finite theorem and does not establish O1. The next theoretical
advance should seek an infinite packing/holonomy family theorem or return to
W1/W3 recognizability, not treat another finite shell as evidence by
accumulation.

## D-0046 (2026-07-19) — Retire the planar Hall branch; return to W3

The adaptive two-center proposal has received its required structural
falsification test. A translation-distinct 4x4 full-packing pair-graph
extremizer was lifted literally to the plane. Inside a 3x4 period rectangle it
contains a deletion-minimal set of 63 placements touching 125 substrate
centers. The placements are mutually nonoverlapping and share a consistent V4
potential, yet two unit-capacity centers per tile would require 126 centers.

A standalone cold verifier reconstructs all kite cells, checks zero overlaps,
recomputes and deletion-minimizes the Hall witness, guards every V4 equation
away from quotient seams, checks the packed-XOR integration, and independently
replays the potential implications with CaDiCaL. The artifact passes.

We therefore retire T2.D7-H and any binary-matroid or discharging proof whose
conclusion is that same two-center matching. The elementary minimal-Hall-core
lemma (connectedness, deficiency 1 or 2, private-center bound, curvature
identity) remains useful but does not imply the conjecture. The running
radius-two taper is retained as a no-go/optimization artifact only. Per the
predeclared branch point in D-0045, primary theorem development returns to W3's
substitution-certificate schema and Spectre validation gate rather than
inventing a third local-density ansatz immediately.

## D-0047 (2026-07-19) — Separate stationary combinatorics from recurrent geometry in W3

The recovered A6 collared substitution is stationary as a finite state rule,
but the Spectre child translations are not one fixed Euclidean similarity on
the kite/module substrate. Treating the representative A6 poses as an
iterable fixed geometric substitution would therefore be unsound.

W3 certificates will encode these layers separately: a stationary collared
state transition kernel and an exact finite-dimensional recurrence for its
scale-dependent realization. For the Spectre control the latter is a
unimodular 16-by-16 integer matrix on four rank-four module points, with exact
minimal polynomial `(x^2-1)^2(x^4-8x^2+1)` and agreement with all 32 generated
table levels. Exact expansion alone does not discharge legality or inball
growth: C1 awaits macro-boundary induction and C3 awaits a divergent certified
inradius. The verifier keeps both clauses partial until those checks exist.

## D-0048 (2026-07-20) — Reclassify the E1 finalist as the known Turtle

An exact primary-source comparison proves that canonical n=10 candidate 2,
key `010001010104010502f002f1030b030c04fa04fb`, is the published ten-kite
Turtle. The primary `rawtileB` outline canonicalizes to the same ten-cell tuple
and compiled key. We therefore retract the “genuinely new” and “new-shape
finalist” classifications in D-0023/D-0024; ERR-003 is controlling.

No computational artifact is discarded. Existing `e1-finalist-*` and
`theory-*-finalist-*` paths are stable legacy identifiers for Turtle-control
experiments. Their exact finite claims remain valid, but their logical use is
method validation or independent Turtle certification—not evidence for a new
monotile. The externally known Turtle theorems close tilability and
nonperiodicity; internal O1/O3 rows now describe optional independent proof
recovery rather than open mathematical status.

Promotion now has a mandatory canonical known-shape identity gate. The Turtle
outline/key is registered in production code and independently reconstructed
in `tests/test_turtle.py`. Search resumes only after Hat and Turtle are removed
from novelty rankings. Historical notebook entries remain unchanged as an
audit trail and are superseded by this decision wherever they call the Turtle
new or its aperiodicity unknown.

## D-0049 (2026-07-20) — Install a fail-closed literature and family gate

ERR-003 was not merely a missing alias. The frozen program already named the
Turtle and `Tile(a,b)`, yet implementation promoted Turtle as new and proposed
`n≈22--24` as a discovery horizon even though the peer-reviewed Hat paper
reports the exhaustive classified horizon `n≤24`. This is a research-process
failure: canonical-key novelty was allowed to stand in for a primary-source
prior-art audit.

`docs/literature/POLYKITE_BASELINE.md` is now the controlling polykite claim
matrix. Evidence classes are explicit: peer-reviewed theorem, published
exhaustive-computation report, author review, or dated search snapshot.
Promotion requires exact identity, size-horizon, infinite-family, motion-group
and current-literature checks. Absence from `KNOWN_POLYKITE_KEYS` means only
“unregistered key.”

The production gate is deliberately fail-closed. All `n≤24` polykites are
ineligible for an aperiodic-discovery label. An unregistered `n>24` key is
also ineligible until a `Tile(a,b)` family classifier has explicitly rejected
membership. Historical artifacts retain their data, but future payloads use
`novel_key` separately from `aperiodic_discovery_status`; the legacy `novel`
boolean means the latter is literally `eligible`.

E2 is paused for redesign rather than shifted mechanically to `n=25`.
Kaplan's reported 500-billion-polykite follow-up means a credible next search
must target a theoretically distinguished family, a different substrate, or
a demonstrably new invariant—not merely repeat an undocumented larger census.

For periodicity theory, the published Appendix-A alignment reduction
supersedes W4 as a required bridge: arbitrary periodic polykite tileability
implies aligned periodic tileability. W4 survives only as optional work on the
stronger “every tiling is aligned” property or on substrate classes outside
the theorem.

## D-0050 (2026-07-20) — Make literature a versioned, testable subsystem

The Turtle misidentification cannot be prevented by adding one more named
shape. The repository now treats prior art as part of the research apparatus:
`docs/literature/SOURCES.json` is a machine-readable catalog; the tracked
state-of-the-art, methods matrix, reading queue, and novelty protocol state
what is known, how deeply it has been reviewed, where it affects the code, and
what remains unimplemented. Structural tests require the controlling sources
and route every catalog entry into the review documents.

Open PDFs and text extracts are cached under ignored `data/literature/` paths,
with SHA-256 hashes in an ignored local lock. This keeps roughly 90 MiB of
third-party source material out of Git while retaining reproducible metadata
and a one-command fetcher. Publication status and repository review depth are
orthogonal: an abstract-verified peer-reviewed paper cannot support a detailed
internal claim until its relevant theorem and assumptions are audited.

Candidate records must distinguish exact shape identity, tiling-system
identity, proof of aperiodicity, and method novelty. The current Turtle result
is formally a blinded positive control for the funnel and certificate
machinery. Future promotion fails closed until the novelty dossier covers
named and parameterized families, finite census scope, motion convention,
dated current searches, proof obligations, and comparison with known tiling
systems. No new search workstream begins without a source map and an explicit
statement of which known search it does not repeat.

## D-0051 (2026-07-20) — Adopt the Golden-Sturmian Turtle density control

The full Akiyama--Araki alternative Turtle proof has been audited at theorem
level. Its two proof halves remain logically separate in this repository:
Golden Hex patch-tiles establish existence, while forced dispensable Golden
Ammann bars establish universal nonperiodicity through an irrational density.

The exact internal control reproduces standard words, central palindromes and
both decomposition identities through level 24. It also verifies symbolically
that the bar frequencies solve `q^2-q+1/5=0` and that the induced minority
handedness density is `(3-sqrt(5))/6 = 1/(1+phi^4)`, the root of
`9f^2-9f+1=0`. The existing independently generated 9,239-tile Turtle disk has
minority D6 count `1181/9239 = 0.127827687`, within `5.06e-4` of the exact
infinite-volume value `0.127322004`. This is an external structural validation
that the patch generator was not fitted to reproduce.

The claim boundary is strict. The repository has not yet reconstructed the
geometric Golden Sturmian Patches, arbitrary-inball Golden Hex induction,
forced GAB continuation, Kagome lemma, or crossing bijection. The published
paper, not the new finite artifact, supplies Turtle tileability and
aperiodicity. The next internal proof step is exact GAB endpoint geometry and
local continuation enumeration; the next literature workstream remains
Kaplan's isohedral SAT control.

## D-0052 (2026-07-20) — Adopt the isohedral-surround SAT prefilter

Kaplan's Proposition-1 criterion is now an exact grid-aligned A1 prefilter:
a simply connected first surround is accepted iff every neighbour can carry
the congruent surround without conflict. The implementation combines halo
exact cover, inverse closure, direct composition-conflict clauses and lazy
hole cuts. Every positive result carries a finite surround independently
checked from geometry.

The external benchmark was essential. An initial edge-neighbour halo returned
54 isohedral seven-kites instead of Myers's 52 because it could leave an
uncovered angular sector at a vertex. Reusing A2's full vertex halo corrected
the complete `n<=8` counts to `1,1,4,4,0,70,52,37`, exactly matching Myers at
all eight orders. The artifact contains 169 cold-verified positive surrounds,
the unique periodic-but-anisohedral four-kite as an A1-positive/isohedral-
negative control, and negative Hat/Turtle controls.

The filter is complete only for isohedral tilings in the alignment model. A1
remains necessary for periodic tilings with multiple transitivity classes.
Neither negative result proves aperiodicity. This closes a portable method
control; it does not reopen or justify rerunning the settled `n<=24` polykite
classification. Primary literature work now moves to W3 recognisability.

## D-0053 (2026-07-20) — Separate theorem-import and direct recognisability routes

Walton's general theorem and Chéritat's Spectre proof have different logical
roles and may not be cited interchangeably. Walton Theorem 5.2 applies to a
compact Hausdorff expansive `L`-sub pattern space, where `L`-sub means that a
surjective local-derivation subdivision `S:LΩ→Ω` is already defined. It
gives unique composition modulo translation. For return-discrete tiling
spaces, Corollary 5.5 gives strict injectivity exactly when the hull contains
no periodic element. Consequently, Walton is a consistency theorem and a
post-aperiodicity recognisability route for W3; using its injectivity
conclusion to establish that same absence of periodic tilings would be
circular.

Chéritat Corollary 63 is the appropriate non-circular control: a whole-plane
Spectre tiling without reflections passes through a finite chain of faithful
cluster/interface/triangle/pack representations, has one unique grouping, and
returns to the same class so the grouping iterates. The existence direction is
separate (Proposition 64 and Corollary 65). W3 now records this as direct-route
obligations D1--D7 alongside Walton hypotheses W1--W5.

The version-2 substitution certificate computes these statuses rather than
accepting self-reported theorem flags. The recovered 17-state artifact remains
valid but partial: Walton's compact-hull, separation, surjective-LD and
no-periodic-hull hypotheses are unproved; the direct route has only sampled
parent uniqueness, finite state closure and partial expanding geometry. The
next proof experiment must enumerate a physical legal Spectre patch language
independently of the vendor ancestry and test total, unique parent ownership
at increasing finite radii.

## D-0054 (2026-07-20) — Replace isolated ownership by coordinated grouping

The first physical Spectre language experiment is ancestry-blind: it uses the
exact straight `Tile(1,1)` polygon, one fixed chirality, rotations and
translations, and edge-to-edge unit-edge contacts. It enumerates all 166
complete first coronas and uses exact SAT cover plus exact polygon nonoverlap
to decide existential completion through successive rings. Thirty central
corona types reach radius two and 21 reach radius three. All 18 types observed
stably in every level-3/4 generated control lie in that set. Three additional
types (indices 33, 44 and 155) remain, and targeted exact witnesses extend all
three through radius four.

The proposed shortcut “find a radius where each viable central tile has one
parent” is rejected. All eight first coronas with one locally compatible
recovered parent are refuted at radius two. None of the 21 radius-three
survivors is uniquely owned: their parent-count histogram is `2:17, 3:3,
5:1`. Parent grouping is a joint constraint across overlapping centers, not
an independent label attached to one central corona.

W3 C5 advances from missing to partial, but C4 is not proved. The exact scope
is an existential central-corona prefix through three rings in an edge-to-edge
model; it is neither the full radius-three patch language nor a theorem that a
finite survivor reaches the plane. Further blind radius growth is
deprioritized. The next experiment constructs the translation-compatible
parent-overlap constraint language and tests the three extra branches against
global grouping consistency and Chéritat's component/interface cases.

## D-0055 (2026-07-20) — Adopt buffered coordinated grouping; keep it conditional

Parent grouping is encoded as a joint partial exact partition by translated
and rotated occurrences of the recovered full/missing 9/8-child templates.
Every universally buffered inner tile must have exactly one selected parent;
every other visible or candidate tile has at most one. Exact physical
next-ring completion and parent selection share one SAT instance.

“Universally buffered” means that every parent occurrence still geometrically
compatible with the fixed inner patch lies in the union of that patch and all
legal next-ring candidates. A branch with no buffered target is expanded by
ordinary physical exact cover and is never counted as grouping UNSAT. This
guard caught 3 such radius-two branches for corona 44 and 12 for corona 155;
all 15 later die physically, but the distinction is part of the soundness
contract.

All 18 substitution-observed corona types admit exact groupings on generated
graph-radius-four controls. The three extra physical types do not survive:
corona 33 has 200 admissible radius-three frontier states and corona 155 has
24, but both have zero radius-four successors; corona 44 has zero admissible
radius-three states after all 27 second-ring branches. Thus the conditional
central-corona language is exactly the 18 generated types.

The result is deliberately conditional on the recovered 9/8 parent language.
It proves that types 33, 44 and 155 cannot occur in a whole-plane tiling that
admits that grouping, not that arbitrary physical tilings admit the grouping.
It also does not prove unique partition or same-domain iteration. W3 therefore
remains a valid partial certificate; D2, D3 and D5 are not promoted. The next
step is to derive parent/component existence from the 18 physical cases and
then exclude ambiguous overlap domains, following Chéritat's logical order.

## D-0056 (2026-07-20) — Promote L18 parent partition; reject blind-ring closure

Treat the 18 substitution-observed physical coronas as an ancestry-blind local
language `L18`. Exact local completion gives 87 radius-two and 418 radius-three
rooted cases. Every radius-three case has a buffered parent grouping and all
groupings induce the same parent **anchor** on every safe tile. The 48 cases
with more than one raw grouping differ only by the optional ninth child; their
anchor maps agree.

The resulting 418-entry radius-three transducer is a local map from physical
geometry to a parent anchor. Exhaustive `L18` extension through radius six
leaves 15,216 patches. In every survivor, the eight canonical core children
of the central anchor are present and carry that same anchor. Since any tile
mapped to an anchor belongs to its canonical nine-child support, the fibers
are exactly the common eight children with or without the optional ninth.
Thus, within the fixed-chirality edge-to-edge `L18` domain, parent existence
and the unique full/missing partition are finite theorems rather than assumed
variables.

Contraction closure is not promoted. Complete contracted interfaces first
appear at radius six. Generated parent-corona states coexist with finite
non-generated states; after exact continuation the latter have frontier sizes
6,280 at radius seven, 1,796 at radius eight, and 4,482 at radius nine. The
radius-nine states are finite witnesses, not plane tilings, but their renewed
branching makes larger blind rings the wrong proof object. D2 and D3 are now
verified conditional on `L18`; D5 remains open. The next experiment contracts
the frontier to a parent/interface state graph and tests that graph for dead
components or globally recurrent counterlanguages.

## D-0057 (2026-07-20) — Require colored interfaces beyond parent coronas

The complete contracted frontier has only nine non-generated uncolored corona
signatures. Together with the 17 generated signatures this gives a 26-state
parent-anchor alphabet. Reciprocal-edge support and every triangle consistency
constraint expressible from those radius-one anchor coronas were enumerated
exactly. All 26 states survive; iterative support deletion removes none.

Therefore uncolored parent-corona overlap is retired as a possible closure
proof. The failure is informative: the abstraction forgets whether an anchor
is a full or missing parent and which physical boundary interface realizes a
parent-parent contact. The next state refinement must carry those component
types and interface colors. This is the smallest natural refinement aligned
with Chéritat's faithful component/interface representations; adding more
blind physical rings or more constraints derived from the same uncolored
coronas would repeat an already falsified method.

## D-0058 (2026-07-20) — One-sided physical colors are necessary but insufficient

The complete radius-seven L18 census contains 51,309 extensions whose
contracted corona is generated and 6,280 whose contracted corona is not.
Recording the center's full/missing component type and every exact oriented
child-edge contact compresses these to 17 generated and five extra states.
The generated set agrees exactly with the independent level-five substitution
control. Missing types are accepted from a finite patch only when the optional
child is mapped to another component or an adjacent core child's complete
physical corona witnesses the alternative contact; mere boundary absence is
never interpreted as a missing child.

This one-sided alphabet deliberately leaves the six neighbor component types
unknown. All 22 states have reciprocal colored edges, colored triangle-star
support, and fixed-point support. Their transition graph is one closed
strongly connected component containing all 17 generated and all five extra
states. Thus exact contact intervals plus the center type still cannot prove
contraction closure. This is a finite no-go theorem for that abstraction, not
a counterexample tiling.

The next minimal refinement is two-sided: extend the five extra interface
states until the full/missing type at both ends of every contact is physically
buffered. Large intermediate frontiers are resumable local checkpoints under
`data/w3-frontiers/` and are git-ignored; only small census/certificate
artifacts are versioned.

## D-0059 (2026-07-20) — Two-sided colors leave three defect states

The 6,280 non-generated radius-seven branches were exhaustively extended.
Exactly 1,796 radius-eight patches survive and yield 4,482 radius-nine
extensions, reproducing the earlier contraction audit. Every radius-nine
extension buffers the center and all six neighbor component types: there are
zero unresolved two-sided interfaces and zero contractions back into the 17
generated uncolored coronas.

The 4,482 extensions collapse to three new two-sided colored states, all full
components, with occurrence counts 776, 2,410 and 1,296. Combined with the 17
generated controls, all 20 states survive reciprocal/colored-star fixed-point
pruning and form one strongly connected component. Thus even full/missing
types at both ends plus exact child-edge contacts do not by themselves prove
D5 contraction closure.

The failure has internal structure. Exact minimum-cost enumeration of each
extra state's six-neighbor star gives extra-neighbor costs `[1,0,1]`. One
state can be surrounded entirely by generated states. The other two cannot
terminate locally: a minimum witness for either contains the other. This
turns the next experiment from another undirected state refinement into a
small pinned-defect propagation problem. Build radius-two parent-state CSPs,
pin each extra at the root, and minimize extra states on the outer ring.

## D-0060 (2026-07-20) — Radius two forces typed defect propagation

For each of the three two-sided extra states, every colored radius-one star
was pinned at the root: 28, 100 and 3 cases respectively. The radius-two CSP
adds a state at every parent anchor named by the six first-ring coronas and
requires exact reciprocal type/contact agreement, agreement on adjacency or
nonadjacency for every represented anchor pair, and exact nonoverlap of their
canonical 8/9-child physical supports.

Only one first-ring star per root survives these radius-two constraints; 128
of 131 are UNSAT. The three surviving CSPs have 960, 432 and 840 complete
assignments. Exhaustive model enumeration and an independent CaDiCaL encoding
agree that every case becomes UNSAT when all second-ring extras are forbidden.
The minimum number of outer defects is `[1,1,1]` and the minimum nonroot totals
are `[3,2,3]`.

More strongly, intersecting the second-ring defect types across **all** models
gives the forced map

```text
288091b49587a4b2 -> 2f1d7f0fac5b9704
2fb5d0cf9a68ffe2 -> 2f1d7f0fac5b9704
2f1d7f0fac5b9704 -> 288091b49587a4b2
```

Thus the state previously absorbable at radius one feeds into a mutually
propagating pair, and no defect can terminate within two parent rings. This
does not yet imply unbounded propagation: iterating the local implication may
revisit an earlier anchor and close a finite cycle. It also does not prove that
a whole-plane configuration exists or contradict planar packing. The next
experiment grows the forced defect relation to radius three and tests whether
exact geometry closes it, creates a cycle/fault line, or yields a quantitative
density bound.

## D-0061 (2026-07-20) — Radius three eliminates the contracted defect alphabet

Every complete radius-two assignment from D-0060 was extended by adding all
anchors named by its second-ring states and solving the same exact colored and
physical-support CSP. This gives 2,232 independently replayable radius-three
instances.

The three pinned root types have respectively 0 of 960, 2 of 432 and 1 of 840
radius-three survivors. The first state, `288091b49587a4b2`, is therefore
impossible in any whole-plane configuration over the 20-state alphabet. Every
survivor of either other root already contains that dead state in its fixed
inner radius-two patch. Hence those roots are impossible as well. This is a
finite elimination proof, not an inference from failed random growth.

Consequently, within the fixed-chirality edge-to-edge L18 domain, the unique
8/9 parent partition contracts only to the 17 generated colored states. D5
same-domain closure is verified under the L18 hypothesis. The larger W3
recognisability claim remains partial because D1—proving that every admitted
geometric straight-Spectre tiling has only L18 coronas—has not been proved.
Nor does this repair the separate C1 all-level geometric legality or C3
inradius-growth obligations.

## D-0062 (2026-07-20) — Physical radius five proves L18 entry edge-to-edge

The three non-L18 physical corona types `33`, `44` and `155` were returned to
the ancestry-blind polygon engine: no parent templates, substitution states or
generated-patch filters entered the ring constraints (the generated control is
used only to identify which physical types are outside L18). Every exposed edge
was covered by every possible exact nonoverlapping next ring. The complete
rooted frontier is

```text
radius       1    2    3    4   5
patches      3   89  368  282   0
```

The roots split as `2/27/60` at radius two, `200/144/24` at radius three and
`72/18/192` at radius four. All 282 radius-four patches fail at radius five;
each already has an exposed edge with no admissible candidate cover, so no SAT
model is entered at the decisive layer. An independent one-hot CaDiCaL
encoding reproduces the full frontier and digests.

Together with the earlier exhaustive `166→30→21` physical-corona prefix, this
proves that every complete corona in any whole-plane fixed-chirality
**edge-to-edge** straight-Spectre tiling belongs to L18. Thus D1 entry, and by
composition D2/D3/D5/D6, are verified throughout that declared contact model.
The unrestricted geometric claim remains partial: a separate local theorem
must rule out T-junctions or other non-edge-to-edge contacts. D4 faithful hull
equivalence also remains open.

## D-0063 (2026-07-20) — Ten edge-patch patterns close unrestricted D1

The exact 14-segment `Tile(1,1)` boundary uses all twelve 30-degree directions
and merges into thirteen maximal polygon sides: twelve of primitive length one
and one of length two. Its interior angles are all at least 90 degrees, and no
maximal side has 90-degree corners at both ends.

At a junction on one side of a straight tiling interface, two distinct incident
tiles must therefore contribute `90+90=180` degrees; an additional point-only
tile is impossible. Three consecutive sides would make the middle tile's side
have right angles at both ends, which the exact boundary excludes. Hence every
maximal interface has at most two polygon sides on either side. Enumerating
words of one or two lengths from `{1,2}` leaves exactly ten ordered equal-length
patterns, with total lengths one through four. Splitting the length-two side at
its existing 180-degree boundary vertex sends every pattern bijectively to the
same unit subdivision on both sides. All apparent T-junctions are primitive
vertices.

The boundary direction word also locks adjacent copies to one common
30-degree frame, and matched primitive endpoints propagate every anchor into
the exact rank-four module. Independent arithmetic reconstruction verifies all
ten patterns and both even/odd `sqrt(3)` deformation controls. Consequently
every unrestricted fixed-chirality straight-Spectre tiling belongs to the
primitive contact model used by the radius-five D1 certificate. D1/D2/D3/D5/D6
are now verified on the full fixed-chirality hull. D4 and D7 remain open, as do
C1 and C3.

## D-0064 (2026-07-20) — D4 finite equivalence kernel; context equality stays open

The physical child-edge-colored component alphabet and A6's oriented
radius-one collar alphabet are exactly the same finite information. Across 310
complete level-four component occurrences, both have 17 states and the
relation is one-to-one in both directions. Expanding each colored state into
its central 9/8 component plus six neighboring components, then recomputing
the physical interfaces, returns the identical state in all 17 cases. Every
one of the central component's 46 (full) or 44 (missing) external primitive
edges has exactly one recorded owner across an interface.

Successive phases are related by two explicit determinant-one integer matrices
(one per chirality), orientation-dependent integer offsets and exact inverse
maps. The map toggles the entire chirality phase without mixing handednesses
and sends translations through the corresponding module matrix. Every first
parent contributes one normalized ordinary Spectre; every second-parent marker
(exactly collar states 10, 11 or 12) contributes a companion at relative pose
`(0,1,(1,-3,-2,0))`. This forward/inverse construction reproduces the complete
generated level pairs `3→2`, `4→3` and `5→4` exactly, with counts
`63+8=71`, `496+63=559` and `3905+496=4401`. The two-level translation matrices
both have characteristic polynomial `(x²-8x+1)²`, matching the previously
derived factor `4+sqrt(15)`.

D4 is not promoted to verified. Exhausting the abstract 17-state colored
radius-one overlap language gives 3,565 stars; 536 map to overlapping next-phase
Spectres and 410 do not yet buffer the central output tile. These are states of
an over-approximation, not counterexamples in the physical hull. Exact
radius-two state completion kills 3,485 seeds and leaves 80. The next D4 proof
object is therefore the physical-origin/context correspondence for those 80
survivors, not another change to the already exact coordinate maps.

## D-0065 (2026-07-21) — Experiments require admission and human checkpoints

ERR-003 through ERR-005 exposed a process failure: decisive prior-art facts
were acknowledged but did not halt the next computational continuation. The
research protocol is therefore executable policy rather than advisory prose.

Every nontrivial research computation now requires a notebook
pre-registration stating its proposition, primary-source/non-redundancy audit,
outcome-dependent decisions, finite stop rule and current human checkpoint.
The record must pass `scripts/check_experiment_gate.py`, and the command must
be launched through `scripts/run_research.py`. Ordinary unit tests and
read-only diagnostics are exempt.

The launcher refuses work beyond three numbered research sessions or 1 GiB of
new material under the declared artifact roots since the last explicit human
checkpoint. At that boundary the agent must present a decision summary and
obtain explicit continuation; available RAM or unattended time is not a reason
to extend the budget.

Finally, a user-supplied prior-art fact, scope constraint or contradiction is
a halt condition for the affected branch. It must be recorded in ERRATA or
DECISIONS, checked against primary sources and propagated into STATUS before
work resumes. This specifically prevents a known finite classification from
being absorbed as context while the same catalog continues running.

## D-0066 (2026-07-21) — Kaplan eight-kite reproduction closes per shape

Kaplan's 116-page public eight-kite artifact uses a different but exactly
convertible cell representation. His point `p` represents the unique kite
`(p-origin[d], d)` for which the translated point is a legal hex center.
Converting and canonicalizing every page gives 116 distinct keys, each present
in the repository database with the same individual classification: 108 at
`H_c=1`, five at `H_c=2`, two periodic-anisohedral inconclusive controls and
the Hat.

This closes the bounded comparison proposed by ERR-005. It strengthens the
claim from aggregate agreement to an exact per-shape independent reproduction.
It does not make the census new, authorize a larger census, or alter the
published `n<=24` discovery boundary.

## D-0067 (2026-07-21) — Close W2 abelian invariants as a control branch

The adversarial prior-art audit of T2.C1/T2.C5 is complete. Conway--Lagarias
already identify additive cell weights with generalized coloring maps and
tile homology; later flat-surface work applies the same relation/parity logic
directly to finite torus grids. W2's GF(2) left-null witnesses and integer
cokernels are instances of that classical certificate class.

No audited Turtle source states our exact parity support for the three thin
HNF families. Nevertheless, the published theorem that every Turtle tiling is
nonperiodic already excludes every torus quotient, so the thin-family result
is only a small independently derived corollary. It is retained as a compact
producer/verifier control, not claimed as a new method, a new Turtle theorem,
or an aperiodicity proof. No further W2 quotient index, prime, group, or shell
run is authorized under this branch. The next research decision is whether
the blind Hat/Turtle funnel supports a publishable classified-corpus benchmark
after comparison and ablations are specified on paper.

## D-0068 (2026-07-21) — E1 is a validation postmortem, not a clean benchmark

The historical E1 runs do not support unbiased rank, recall or ablation
claims. Hat was the explicit development and calibration target; Turtle was
named in the program's expected outcome even though its canonical key was not
registered; thresholds and budgets changed in response to observations; and
the expensive A3/A4 stages were run only on the ten smallest depth-three
survivors. There is no frozen global score over the complete corpus.

The exact outputs still form a useful public reproduction package: the
116-shape Kaplan crosswalk, cold-verifiable certificates, a disclosed
ten-shape retrospective bracket, and the identity/prior-art failure
postmortem. They must be described as validation and research-governance
evidence, not as a blind discovery-method benchmark.

A clean `n<=12` replay could freeze labels, baselines and rank metrics, but it
would contain only two positives, one already used during method development.
Its expected research return does not justify another run. No E1 ablation
campaign is authorized. E1 is closed as validation/postmortem, and the next
research branch must begin outside the classified polykite catalog after a
primary-source go/no-go audit.

## D-0069 (2026-07-21) — Sturmian monotile encoding survives only as ST-M1

The full Akiyama--Hamada--Ito construction gives quadratic-slope aperiodic
finite tile sets with colors/Ammann-bar matching rules; it does not give a new
monotile family. Its optimized `sqrt(2)-1` system has three disk-like
prototiles and positive entropy, while its open-problem section explicitly
asks whether another monotile and disk-like general constructions can be
obtained.

Nearby general results do not silently close this gap. Geometric matching
rules preserve multiple tile types; atlas reduction retains external legal
patch rules; the poly-`K` correspondence preserves tileset cardinality and may
change the acting group. Accordingly, the only authorized continuation is the
on-paper theorem candidate ST-M1: construct one connected unmarked disk whose
every tiling has a translation-equivariant finite-radius factor onto the
`sqrt(2)-1` Sturmian system. The central obligations are congruence encoding
and exclusion of all spurious unmarked tilings. No runner, search, or generated
patch is authorized until a plausible proof plan for both obligations exists.

This decision and its dated permitted/forbidden claims are recorded in
`docs/literature/reviews/STURMIAN_MONOTILE_ENCODING.md`. The adversarial W3
method-novelty audit remains next, as required by the human checkpoint review.

## D-0070 (2026-07-21) — Close W3 as a novelty branch

The adversarial W3 audit finds no current method-novelty proposition. The
original chiral-Spectre proof already uses computer-generated reduced patch
lists, iterative overlap-based deletion, reduced 5-patches and forced unique
supertile assignment. Chéritat proves the complete all-whole-plane faithful
component/interface chain and iterable unique hierarchy. Walton supplies the
general recognisability framework, while Goodman--Strauss/Vereshchagin and
Tatham cover finite local matching-rule and finite-state substitution
encodings.

W3's exact JSON schemas, independent cold verifiers, tamper tests and explicit
obligation ledger remain useful reproducibility engineering. They do not yet
form a new general method: only the published Spectre system has been treated,
there is no generic soundness/completeness theorem for the schema, and the
remaining 80 D4 contexts belong to an abstract over-approximation rather than
the physical hull. Eliminating them would complete another executable
reconstruction of a known theorem.

A July 2026 adjacent preprint by Batle and Bednorz also publishes exact JSON
certificates and a Python verifier for finite Hat retiling. It does not solve
Spectre recognisability, but independently forbids broad novelty claims about
machine-readable certificates in Hat/Spectre computation.

No further W3 radius, seed, corona or context computation is authorized.
Reopening requires an on-paper generic theorem over a stated class, a proved
certificate soundness map to whole-plane conclusions, explicit control of
spurious abstract states, and validation on at least two structurally
independent systems. Permitted and forbidden claims are fixed in
`docs/literature/reviews/W3_CERTIFICATE_METHOD.md`.

## D-0071 (2026-07-21) — ST-M1 stops at a coupled-carrier design

The first ST-M1 theorem-design pass selects the minimal aperiodicity theorem
before the positive-entropy strengthening. A total finite-radius map into any
aperiodic irrational Sturmian subsystem suffices for period descent; positive
entropy requires the separate and stronger claim that the map is surjective
onto the complete Section 10.1 three-prototile system.

The source's `kappa=infinity` suggestion of one support up to color is not
silently identified with its proved positive-entropy example. The former is
now a named source-extraction obligation, ST-M1.S0. Until its complete finite
alphabet, contacts and all-tilings aperiodicity are derived, it is not an
available target system.

The chosen candidate mechanism is a coupled contact-star carrier: finite
relative boundary offsets encode contextual states, while corner relations
couple all three Sturmian directions. Independent one-dimensional sofic rails
are ruled out because they contain compatible periodic points under the
product hypothesis. Full Euclidean isometries are controlling; an ordinary
monotile proof must geometrically exclude mixed-handed contacts and propagate
one chirality across every plane tiling, or be downgraded in advance to an
orientation-preserving claim.

No polygon, contact search or patch experiment is authorized. Geometry may
begin only after the equal-support source lemma and a total, unambiguous
three-state symbolic contact kernel are proved on paper. Session 63 exhausts
the three-session allowance under `HC-2026-07-21-02`; further research needs a
new explicit human checkpoint.

## D-0072 (2026-07-21) — S0 splits into a compiler and E-infinity

The user authorized checkpoint `HC-2026-07-21-03` for bounded on-paper S0/K1
work. The first source derivation finds that the `kappa=infinity` sentence does
not itself define the colored equal-support target needed by ST-M1. Section
8.1's equidistanced model is introduced for bounded-displacement calculations,
and the one-support suggestion occurs later in the distinct Turtle
subsection. No common-cell subdivision or language equivalence is stated for
the optimized positive-entropy `sqrt(2)-1` system.

The formal reduction does close. ST-M1.S0C proves that finite connected
macrotiles over one congruent periodic cell can be compiled into finitely
colored copies of that cell with unique local regrouping and preservation of
periods. This is an elementary colored-macro compiler, not a monotile result or
a method-novelty claim.

ST-M1.S0 now depends on the new exact lemma E-infinity: construct the
nondegenerate common cell for all three Section 10.1 templates and prove that
the complete SAB/boundary language and irrational symbolic sequences survive
the transport. K1 remains blocked because its true alphabet is the full set of
addressed constituent-cell colors, generally larger than the three visible
macro types. In accordance with the dependency stop rule, no contact kernel,
shape or experiment was started in session 64.

## D-0073 (2026-07-21) — Minimal colored S0 closes in proof draft

The E-infinity derivation closes the source-specific colored stage for the
minimal aperiodicity target. At equal corridor width, every cabinet/isometric
rectangle is the same trigonal rhombus. Cutting `S` and `L` as in Definition 4
and also cutting `M` along the marked diagonal—consistent with the paper's
`2M` bookkeeping—produces one equilateral-triangle support.

The two connected `2S+L` templates contain 18 primitive triangles each and
the `M` diamond contains two. A finite higher-block collar records macro
address, handedness, primitive cell type, `M` half, SAB continuation and the
source vertex star. The S0C compiler then gives unique local regrouping and
prevents equidistancing from adding new combinatorial vertex cycles.

The colored system is minimally aperiodic: any translational period lies in
the trigonal lattice and periodically shifts at least one virtual corridor
word, which would have rational slope, contrary to the source composition
restriction to `sqrt(2)-1` (or its admitted irrational conjugate). This is our
proof-draft derivation, not a theorem stated by the source and not an unmarked
monotile.

Positive-entropy transport remains unproved. K1 is now admissible, but the
input is a collared refinement of 38 raw macro-address states rather than
three colors. The next on-paper step must first seek an
aperiodicity-preserving quotient of that alphabet; direct geometric encoding
of an unspecified collar expansion is not authorized.

## D-0074 (2026-07-21) — The natural K1 three-state quotient is unsafe

A symbolic quotient must be judged on the complete shift defined by its
finite local rules, not merely on recoded intended source tilings. ST-M1.Q0
records the sufficient condition: the entire local closure must have a total
finite-radius map to an irrational-only Sturmian system.

The natural reduction to primitive `S/M/L` roles fails this test. Once macro
ownership, internal addresses and completion ports are forgotten, the rule is
the source's unrestricted `{S,M,L}` cabinet system. Remark 7 explicitly says
that system forms Sturmian lattices of every slope; rational slopes supply
periodic points. Keeping the three corridor families as independent
finite-state rails also fails by ST-M1.N1.

This refutes only the obvious source-role quotient, not every possible
three-symbol coding. No nontrivial quotient is currently proved safe. The
smallest safe presentation remains the full addressed/collared S0 alphabet,
with a 38-state raw core and an as-yet unwritten finite collar expansion.

K1 remains blocked before geometry. A future checkpoint must first authorize
an explicit finite collar/port table and require each proposed state merge to
preserve overlap transitions and a total irrational-corridor decoder on the
full local closure. Session 66 exhausts `HC-2026-07-21-03`; no polygon or
contact search follows automatically.

## D-0075 (2026-07-21) — K1 table admitted at fixed contact radius one

Independent review identified two controlling qualifications and the user
authorized their resolution under checkpoint `HC-2026-07-21-04`.

First, the source explicitly says that Theorem 4 requires at least two tiles
to realize a quadratic-slope Sturmian lattice, immediately before suggesting
one support at `kappa=infinity` “up to color.” This is a lower bound inside the
paper's category: a tile is `(support,color)`, and contextual states count as
different colored tile types. ST-M1 does not contradict it. ST-M1 seeks one
unmarked support whose states are recovered from a surrounding contact star;
those states are not prototile colors in the admitted geometric tiling. The
finite-radius map is applied only after the shape-only tiling exists. The
source's next section still asks whether another aperiodic monotile can be
obtained, confirming that this category change is the open step rather than a
claimed one-colored-tile corollary.

Second, the proof-draft all-`M` exclusion currently depends on the unwritten
transported collar table. It remains an explicit IOU until that table shows
which `M` stars and completions are legal; the projective endpoint argument
alone does not instantiate the finite local rule.

The admitted table uses **contact-corona radius 1**, where contact means any
nonempty intersection, so one corona contains the complete vertex stars of a
triangular cell. Raw internal ports may name cells elsewhere in their fixed
finite macro template, but no radius-2/3 collar escalation is allowed. If a
radius-1 table cannot prove overlap consistency, exclude the all-`M` branch,
or support a future-equivalence merge, that failure is the session result.
Any code needed to construct or check the table is a gated research run under
D-0065; no polygonal carrier work is authorized.

## D-0076 (2026-07-21) — Withdraw E-infinity and halt the 38-address table

The source check required before constructing D-0075's table found that its
premise is false. Table 1 of the primary Akiyama--Hamada--Ito TeX lists the
optimized Section 10.1 large prototiles as `12S+6M+6L`, not bare `2S+L`.
The latter describes the earlier 27-tile construction at the same slope.
Sessions 65--66 therefore omitted the attached `M` cells and did not derive
the asserted `18,18,2` addressed templates.

The error is deeper than the count. The `kappa=infinity` one-support sentence
is made in the separate Turtle subsection, after a different cell
construction. The source gives no common-cell specialization or complete
language transport for the optimized `sqrt(2)-1` example. Consequently
ST-M1.E-infinity and the instantiated colored source S0 are again blocked;
the all-`M` exclusion and every cardinality attributed to their collar
alphabet are unavailable.

ST-M1.S0C survives as a conditional common-cell compiler. Q0, N1 and N2 also
survive at their stated conditional scope and continue to rule out unsafe
quotient strategies. They do not supply the missing source. The admitted
radius-one classification is stopped before any enumeration, script, or
artifact is produced. Reopening requires an exact source-independent
common-support construction for the actual `12S+6M+6L`, `12S+6M+6L`, `M`
templates, including their SAB and vertex language; a revised address count
alone is insufficient. See ERR-006.

## D-0077 (2026-07-21) — Retain the actual-composition projective skeleton

The user authorized the replacement on-paper task after ERR-006. Before any
common-support construction, the actual optimized compositions were checked
against the source's projective convention. A patch composition
`xS+yM+zL` represents `[x:2y:z]`; hence each optimized large type
`12S+6M+6L` is the point `[12:12:6]`, while the small type is
`M=[0:2:0]`.

ST-M1.P0 proves that their projective segment intersects the Sturmian
parabola

`[(1-beta)^2 : 2 beta (1-beta) : beta^2]`

at exactly `beta=sqrt(2)-1`. Every non-`M` point of the segment has first to
third coordinate ratio `2`, forcing
`(1-beta)^2/beta^2=2`; the positive solution is unique. The intersection is
genuine because its segment coefficients can be chosen
`a=beta^2/6` for the combined large-type density and
`b=beta(1-2 beta)>0` for the pure-`M` density.

This retains the arithmetic core of the withdrawn proof and improves its
scope: it is the source's exact `T_A intersect T_C` argument, not an argument
that first assumes a periodic fundamental domain. At the original colored
source level, the SAB matching rule is what places every tiling on the
Sturmian parabola and therefore excludes the all-`M` endpoint. A future
common-support or unmarked system cannot borrow that conclusion until it has
a total decoder into the complete source language. P0 does not close
E-infinity/S0, define an address alphabet, or authorize an atlas run.

## D-0078 (2026-07-21) — Correct common-support geometry is `30,30,2`

The final HC-04 session derives the support geometry directly from the
source's centroid definition instead of reading it from a figure. In cabinet
coordinates, the centroid of the triangle bounded by `a=A`, `b=B`, `c=C` is

`((2B-A-C)/3, (2C-A-B)/3)`.

For adjacent `b` and `c` gaps `p` and `q`, the four centroids defining an
isometric cell therefore form a parallelogram with edge vectors
`p(2,-1)/3` and `q(-1,2)/3`. The fixed map to isometric coordinates sends the
unit vectors to equal-length vectors at 120 degrees. After rescaling by
`1/kappa`, both possible gaps `kappa` and `kappa+1` tend to one. Every
`S/M/L` isometric-cell support consequently tends to the same
`60/120` rhombus, cyclic orientations included.

The source cuts `S` and `L` along the diagonal not parallel to the omitted
line family. In the limiting rhombus this is the short diagonal, producing
two equilateral triangles. Splitting each `M` rhombus along the corresponding
marked diagonal therefore gives the same triangle support. The actual large
composition `12S+6M+6L` becomes `12+2*6+6=30` triangles, and the small `M`
becomes two. Thus the two large and one small templates have corrected raw
address counts `30,30,2` (62 total).

This closes only the support-and-template geometry lemma ST-M1.G0. It does
not close E-infinity: the normalized limit collapses tiny line-arrangement
triangles to vertices and can create new point contacts. A finite transported
SAB/vertex language must still prove that every equal-support colored tiling
decodes to the original source and excludes spurious recombinations. No atlas
was enumerated, and no radius escalation is authorized. HC-04 is exhausted.

## D-0079 (2026-07-21) — Separate auxiliary overlaps from physical tilings

The user authorized HC-05 for on-paper L0 work, with the review's
overlap-to-point warning as a mandatory obligation. Reading the cited source
sentence in its full construction context corrects its scope.

The objects permitted to overlap on tiny triangles are the auxiliary
first-order Sturmian-triangle patches `P1,P2,P3` used to prove the bounded-
displacement correspondence between the `S` and `L` hexagon centers. They are
introduced after the physical isometric cells, which the source explicitly
says “provide a tiling,” and before the conclusion that the resulting tile
set in Figure 37 admits tilings of the plane. Thus the final three physical
patch-tiles are ordinary unions of a cellulation; the cited sentence does not
say that their interiors overlap.

The warning remains mathematically relevant. The auxiliary overlaps certify
coordination of the BD assignment, and their tiny triangular supports shrink
to vertices under normalized equidistancing. ST-M1.O0 records the correct
bridge: contract each locally finite, interior-disjoint tiny overlap disk to
a vertex while retaining its participant set and cyclic order as a finite
vertex decoration. The quotient is again a plane, auxiliary patch interiors
become disjoint, and the decorated vertex star retains exactly the collapsed
incidence.

L0 is therefore split into: O0 auxiliary overlap contraction; I0 transport
of the final physical edge/vertex incidence; and D0 a total finite local
decoder on the full limiting language. This is a proof design, not an atlas
enumeration. Failure of any component closes the current equal-support route;
it may not be answered by silently weakening the physical/source distinction.

## D-0080 (2026-07-21) — Physical limiting vertices retain unique provenance

The exact line-index calculation closes ST-M1.I0 without an atlas. For a
triangle bounded in cabinet coordinates by indexed lines `a_r,b_j,c_k`, let
`s=r+j+k`. In the normalized equidistant limit its centroid is

`(j-s/3, k-s/3)`.

Every physical isometric cell `H^a_{j,k}` uses `r=i-1` with `i+j+k=0` and
the four choices `(j+epsilon,k+eta)`. Their orders are
`s=-1+epsilon+eta`, hence `-1,0,0,1`. The three possible vertex classes lie
in the disjoint cosets

`Z^2+(1/3,1/3)`, `Z^2`, and `Z^2-(1/3,1/3)`.

The coset determines `s`, then the coordinates determine `j,k`, and
`r=s-j-k`. Thus two distinct indexed source triangles never acquire the same
physical centroid. The limiting triangle edges have primitive differences
`(2,-1)/3`, `(-1,2)/3`, or `(1,1)/3`; none contains another vertex in its
relative interior. Consequently the G0 complex is a genuine simplicial
triangulation with no new physical T-junction or vertex identification.

The vanished narrow/wide metric information remains in the transported
`S/M/L`, address and SAB colors. With these colors, every limiting physical
star has exactly one prelimit source-star provenance. Reflections act on the
whole decorated star and do not create a second lift. I0 is therefore a
proof-draft lemma at the colored stage. D0—the global total decoder from the
finite local rules—remains open; no atlas was enumerated.

## D-0081 (2026-07-21) — Close minimal colored S0 by an index-cocycle decoder

The last HC-05 session closes D0 and L0 at proof-draft level without a collar
enumeration. The limiting alphabet retains finite macro addresses and
internal ports, source boundary/SAB data, line family and order coset,
narrow/wide gap symbols, and O0 vertex decorations. Its rules are direct
address equalities, source boundary matches, I0 vertex incidence, and equality
of repeated descriptions of one indexed corridor gap.

Every edge-to-edge tiling by the common equilateral triangle has one global
triangular frame. Choose an arbitrary vertex as index origin and integrate the
fixed `(r,j,k)` increment across primitive edges. The sum around every
triangular face is zero; since the plane cellulation is simply connected, the
sum around every closed path is zero. Thus local index data have no global
holonomy. Gap equalities produce three global narrow/wide sequences, and
transported edge/SAB rules produce exactly the indexed Section 10.1 source
matching system. S0C ports group the `30,30,2` constituents uniquely into
complete macros. The source theorem and P0 force slope `sqrt(2)-1`, excluding
the spurious all-`M` endpoint.

Flattening one physical source tiling by its line indices proves existence.
A period of a limiting colored tiling is a triangular-lattice translation and
would, through the finite-radius decoder, periodize its irrational source
configuration. Therefore the minimal equal-support colored system is
aperiodic. ST-M1.D0, L0, E-infinity and S0 close as proof drafts.

The conclusion is deliberately weaker than the withdrawn claim in one
respect: no MLD or topological conjugacy between the finite-`kappa` Euclidean
hull and the equidistant Euclidean hull is asserted. The proved object is a
finite, period-reflecting symbolic decoder, which is sufficient for minimal
ST-M1 but not for the positive-entropy strengthening. No unmarked monotile,
carrier, collar quotient or geometric contact atlas has been constructed.
K1 is the next theorem blocker and requires a new human checkpoint.

## D-0082 (2026-07-21) — Make I0's order restriction and D0's slope branch explicit

Post-checkpoint audit identified two hypotheses that were used correctly but
not stated at their load-bearing locations.

First, the centroid map is not injective on arbitrary index triples:
`(r,j,k)` and `(r+1,j+1,k+1)` have the same centroid. Their orders differ by
three. I0 applies only to the physical generating vertices of an isometric
cell, whose orders are exactly `{-1,0,1}`. The three centroid cosets determine
the order modulo three, and on this restricted set that residue determines the
integer order itself. I0's statement and ledger dependencies now include this
restriction explicitly.

Second, source Theorem 4(2) allows a quadratic slope or its algebraic
conjugate when that conjugate also lies in `(0,1)`. For
`beta=sqrt(2)-1`, the conjugate is `-1-sqrt(2)`, outside the Sturmian slope
interval. Hence it supplies no second branch; this is also immediate from
P0's unique intersection with the parabola on `[0,1]`.

Neither clarification changes the O0/I0/D0 conclusions or reopens S0. They
are recorded before K1 because its decoder inherits the restricted-order
argument. “Bent SAB” is also marked as repository shorthand for the
isometric-cell construction in source Figure 41. HC-05 remains exhausted and
K1 remains unauthorized pending HC-06.

## D-0083 (2026-07-21) — Start K1 from a lossless incidence compiler

The user explicitly authorized HC-06 for on-paper K1 work. The first step
does not guess a quotient. ST-M1.K1C moves every full addressed S0 state into
finite directed half-contact records `(a,e;b,e')` and retains the legal cyclic
corner words. The three incident contacts of a triangle must share the same
center state `a`; opposite half-contacts are involutes.

Encoding a source tiling by these records and reading their common center
state are inverse radius-one maps on the complete stated contact-rule space.
This gives a finite coupled contact-star baseline and keeps Q0's
no-spurious-configurations obligation explicit. It is a standard lossless
recoding, not a novelty claim or a nontrivial quotient.

K1C is not a geometric result. Its contact modes are still symbolic colors,
whereas one unmarked carrier has one fixed boundary. K1 remains open until a
quotient erases explicit source identities while retaining a finite-radius
decoder on its full local closure. HC-06 does not authorize a collar census,
carrier drawing, contact search or experiment.

## D-0084 (2026-07-21) — Separate image resolving from local-closure totality

A contact quotient has two distinct obligations. K1R proves, by compactness,
that a finite quotient of K1C has a finite-radius inverse on its intended
image exactly when it is injective on complete configurations. Arbitrarily
large ambiguities made from globally extendable source patches therefore
converge to a whole-plane ambiguous pair.

This is not enough for a carrier. Its finite matching rules define an SFT
`Z_rho(q)` that may strictly contain the intended factor image. K1T is the
exact safety contract: one fixed-radius local decoder must send every
configuration of `Z_rho(q)` to S0, satisfy all source edge/vertex rules, and
reproduce the quotient contacts when re-encoded. These bounded local
identities are necessary and sufficient for a total right inverse.

Erasing all contact and corner modes fails immediately (N3), because it
leaves the periodic equilateral-triangle frame. This does not refute an
unmarked carrier with several geometrically realized relative contact modes.
No specific quotient, radius or collar table was chosen.

## D-0085 (2026-07-21) — Distributed contact code closes symbolic K1 only

K1D gives a nontrivial safe quotient without guessing source-state merges.
Choose an injective three-coordinate code for the essential addressed S0
states and place one coordinate on each incident directed contact. The legal
tile-star rule admits exactly complete codewords; decoded neighbors and
vertex cycles must satisfy S0. The three modes recover the source state and
re-encoding returns the quotient configuration, so K1T holds on the complete
stated local-rule space.

This redistributes information rather than reducing the number of decoded
source star types. With `n` essential states, an immediate three-contact
decoder needs at least `ceil(n^(1/3))` modes per directed side. P0 guarantees
positive total large and small macro coefficients, so one 30-address large
macro and the 2-address small macro give `n>=32` and a lower bound of four
modes. The argument does not assume that both 30-address large types are
essential.

N4 records the new obstruction: independent side-mode choices admit a
Cartesian product and cannot enforce a non-Cartesian codeword set. A geometric
carrier therefore needs a genuine corner/tile-star coupler. The purely
symbolic K1 obligation closes in proof draft; the full monotile route remains
blocked at K2G, which must realize the coupled modes with one fixed unmarked
boundary while excluding illegal mixed stars, sliding, T-junctions and
opposite-handed faults. HC-06 is exhausted and no geometry is authorized.

## D-0086 (2026-07-21) — Repair N4 with a selected parity code, not an unproved 62-state lemma

Independent review found that D-0085 applied the conditional N4 obstruction
without proving its premise. At the conservative count `n=32`, a Cartesian
codeword image of size `4*4*2` is numerically possible. P0 also does not imply
that both large macro types are essential: it forces positive total large
density and small density, which guarantees 30 addresses of one occurring
large type plus two small addresses, but not `30+30+2=62`.

The repair chooses the code rather than strengthening the occurrence claim.
Map a guaranteed 32-state subset bijectively to the even-parity half of
`{0,1,2,3}^3`. Map every remaining state to a fresh diagonal triple. The
result is injective, every individual coordinate forgets identity, and the
image is non-Cartesian because `(0,0,1)` belongs to the product of the three
coordinate projections but not to the image. Thus N4 applies unconditionally
to this selected K1P compiler.

Allowed claim: one explicit safe distributed compiler requires joint
tile-star or corner coupling. Forbidden claims: every safe distributed code
requires such coupling; both large macro types occur; the essential alphabet
has 62 states; or four modes per side suffice for the selected code. The user
authorized HC-07 for on-paper K2G design after this loophole was identified.
No contact census, carrier search, generated geometry or experiment is
authorized.

## D-0087 (2026-07-21) — Exact K2G parity needs ternary information

K2G is defined as an exact realization of the selected K1P compiler, a
stronger target than minimal ST-M1. Its G1--G6 contract requires a complete
geometric contact normal form, mode extraction, equality with the extendable
K1P star language, overlap legality, homochirality and one lift. This strength
is what makes K1P/N4 relevant; it is not claimed necessary for every possible
Sturmian monotile factor.

The even-parity core has full unary and binary projections. Hence no
conjunction of constraints seeing at most two incident side modes can realize
it exactly: every such constraint accepting all legal words is trivial on its
scope. N5 therefore rules out not only independent side keys but also
ordinary binary corner checks for this compiler.

A viable exact carrier must name a genuine ternary exact-cover junction, a
locally recoverable auxiliary phase, or a proved larger-radius geometric
exclusion. No polygon, atlas or existence claim is made. The remaining HC-07
session is restricted to analyzing the auxiliary-phase option on paper.

## D-0088 (2026-07-21) — K1P parity has exact four-state hidden-phase cost

The N5 arity obstruction is not fatal symbolically. With hidden phase
`h=(p,q) in (Z/2)^2`, three pairwise relations can require
`p=parity(x)`, `q=parity(y)` and `parity(z)=p+q`. Eliminating `h` gives exactly
the even-parity K1P core.

Four hidden values are minimal. Any hidden value in a star factorization
contributes a product box. A box contained in even parity fixes all three
coordinate parities and covers at most one of the four even Boolean patterns;
four boxes are necessary, and the displayed construction attains the bound.

This is a symbolic factorization, not a carrier. The hidden phase must be a
locally recoverable geometric pose/contact-star class. A phase defined only
by integrating edge increments is ambiguous up to global additive constant
and is invalid unless all uses are gauge-invariant or a bounded geometric
landmark fixes it without an external origin. K2G remains open at realizing
four such local phase classes together with G1--G6. HC-07 is exhausted.

## D-0089 (2026-07-21) — Pure pose fails by orbit weight, not group non-embedding

The user's HC-08 authorization carries an audit suggestion that
`(Z/2)^2` cannot be represented by pure rotations because it does not embed
in a cyclic group. That is not the right obstruction: four poses can be
labeled by four states without the label map preserving a group law.

For one fixed intrinsic three-side boundary pattern, however, rotations and
reflections only permute the side parities and therefore preserve Hamming
weight. K2H needs `000` together with `011,101,110`; these lie in weights zero
and two. N7 proves that no orbit of one intrinsic pattern realizes the four
states. Pure pose is closed, while contextual docking states remain open.

The K1P core is also fixed explicitly: choose one source witness `y_0` and
one large type `tau` occurring in it, map its 30 address types and the two
small types onto the parity core, and require G6's lift to contain `tau`.
This answers the audit's quantifier note without asserting universal
occurrence of either large type.

## D-0090 (2026-07-21) — `L/2L` is a gauge, not a carrier state, without a local anchor

The triangular lattice quotient `L/2L` has the desired four-element structure
but the bare frame cannot select its absolute cosets locally. Every primitive
`L` translation fixes the unmarked frame. Translation equivariance forces any
local output to inherit that period, whereas the coset coloring is changed by
the translation and has period lattice `2L`. N8 records the contradiction.

Integrating quotient-valued edge increments gives the same result: vertex
phases are determined only up to a global additive element. A future carrier
may use `L/2L` only if additional bounded contact geometry anchors the coset
and prevents gauge-related distinct source decodings of the same unmarked
tiling. Without that anchor, the quotient is bookkeeping and does not enforce
K1P parity. The unanchored translation-phase option is closed; contextual
stars and genuine ternary junctions remain open.

## D-0091 (2026-07-21) — Close unanchored pose action; require a physical shared state

N9 combines the HC-08 results. If a proposed hidden state uses only carrier
orientation and an absolute `L/2L` residue in the bare frame, translation
equivariance makes it invariant under every residue shift. It therefore
depends only on orientation, and N7's Hamming-weight orbit obstruction applies.
The combined unanchored frame-pose shortcut fails.

K2H's existential variable reduces geometric arity only if one bounded,
locally visible carrier feature is shared by all three interface constraints.
If the variable is reconstructed only after reading the three modes, its
existence is simply the original parity relation and N5 is not bypassed.

K2G is frozen. It may reopen only with an on-paper candidate for a four-class
contextual star map or a genuine ternary/larger-radius exact-cover junction,
together with a noncircular shape-enforcement argument. Pure pose, bare
`L/2L`, radius escalation and unmotivated notch search are closed. HC-08 is
exhausted.

## D-0092 (2026-07-21) — Reopen K2G on an exact boundary-cocycle candidate

The user authorized HC-09 with a three-session kill condition. K2C provides a
concrete mechanism surviving N7--N9. Treat K1P's codebook as the union of its
32 base even-parity words and its remaining fresh diagonal tags. A corner
constraint forces one branch consistently around the carrier. On the base
branch, contextual bits at the three corners have successive differences
equal to the side-mode parities; closed-boundary holonomy is zero exactly for
the even words. On the fresh branch, cyclic tag equality gives exactly one
diagonal word.

The corner potentials are defined only up to simultaneous flip and every
constraint uses differences, so no absolute lattice phase is introduced.
They are contextual vertex-sector states, not pure poses. K2C is an exact
symbolic factorization of the complete K1P star relation, not a polygon.

The candidate survives admission. It fails unless a shared six-valent
geometric vertex can expose separate sector states for its incident carriers,
side contacts can enforce the difference relation, and the resulting atlas
has no additional contacts. No drawing or search is authorized.

## D-0093 (2026-07-21) — K2C needs sector-separated six-valent vertices

Identifying all six carrier-corner potentials at one frame vertex would force
the two directed half-mode parities on every shared edge to agree. K1P's
center-state code and source edge rule do not establish that property. A
single common vertex bit is therefore forbidden unless a later code theorem
proves half-mode parity matching.

K2V gives the exact alternative. Integrate each carrier face's even word
independently and retain at every shared vertex the six participant bits with
their cyclic sector identities. This always lifts a K1P configuration and has
a finite raw base alphabet of at most 64 sector words. It is symbolic, not a
geometric atlas.

The remaining HC-09 question is whether one fixed unmarked boundary can make
those sector records locally visible and transport their differences along
sides without merely reintroducing painted colors. Failure of that
noncircular junction contract closes the selected route.

## D-0094 (2026-07-21) — HC-09 kill condition closes active K2G geometry

K2J states the exact admission contract for K2C/K2V geometry: a bounded
unmarked sector invariant, same-corner sharing, an exact finite side
transducer, complete six-sector vertex/contact classification, frame and
chirality forcing, and a lift of the fixed G6 witness.

No candidate meets it. “Two-phase zipper” and “forked corner” descriptions
do not provide one exact polygon, exclude unintended offsets and contacts,
prove rigid three-side compatibility, classify vertices, or lift a whole
plane. Naming their hypothetical local state `q` would merely reintroduce an
external color.

The HC-09 kill condition therefore fires. K2C and K2V remain valid symbolic
reductions, but the selected exact-compiler K2G route closes as active
research. Reopening requires an exact on-paper polygon or general geometric
gadget lemma satisfying J1--J6. Shape search, notch drawing, collar
escalation, or finite patches are explicitly insufficient. HC-09 is exhausted.

## D-0095 (2026-07-21) — Define SER0; do not digitize source figures as tables

HC-10 consolidates the symbolic ST-M1 chain. SER0 specifies the complete
machine-readable source object: exact `30,30,2` templates and addresses,
state fields, oriented edges, cyclic vertex words, decoder data, fixed K1P
code and cold-verifier obligations.

The arXiv v3 source archive was audited. Its TeX supplies formulas and prose;
the relevant construction figures are standalone Adobe Illustrator PDFs.
There is no constituent-address list, bent-SAB table, vertex atlas or figure-
generating coordinate source. Visual/path extraction would therefore be an
independent reconstruction with semantic choices, not direct serialization.

No producer run is admitted. SER0 is blocked pending author data or a
separately preregistered, independently validated reconstruction. The
self-contained theory write-up may use an abstract finite S0 presentation but
must expose SER0 as the reproducibility gap.

## D-0096 (2026-07-21) — Consolidate ST-M1 as a conditional symbolic dossier

Theory note 14 replaces the need to reconstruct the ST-M1 argument from
sessions 63--85. It states P0, S0, Q0/K1T, K1P, N5--N9 and K2C/K2V in one
dependency chain, then isolates the conditional K2J-to-monotile implication.

The dossier is a proof draft and carries no method-novelty claim. It states
that no polygon, monotile, surjectivity or entropy result exists. SER0 and
K2J remain independent blockers: missing source tables cannot be repaired by
prose consolidation, and symbolic boundary holonomy cannot be promoted to
geometry.

## D-0097 (2026-07-21) — Freeze ST-M1 at the consolidated two-blocker boundary

The HC-10 adversarial integration audit accepts theory note 14 only at
proof-draft level. SER0 and K2J are logically independent: SER0 asks for the
extensional colored source presentation needed for cold verification; K2J
asks for one unmarked geometric carrier whose complete tiling language
realizes the symbolic compiler. Closing either does not close the other.

HC-10 is exhausted without an experiment or generated artifact. Active ST-M1
work remains frozen. Reopening requires author-supplied exact source data, a
separately preregistered and independently validated source reconstruction,
or an exact on-paper polygon/gadget lemma meeting every K2J obligation. A
larger patch, radius escalation, or suggestive drawing is not a reopening
input.

## D-0098 (2026-07-21) — Reopen geometry at flag-carrier granularity

The user declines the author-contact route and authorizes HC-11 to pursue a
new geometric idea, with compiler-aware search as a secondary outcome. The
checkpoint is idea-first and inherits a three-session kill condition; no
shape run is authorized merely because the branch reopened.

K3F replaces one polygon per source triangle by three congruent corner-kite
flag carriers per triangle. K2C's three potentials then live on three
physical occurrences joined in a cycle, and K2V's six source-vertex sectors
remain six occurrences. The colored flag system is MLD with K2V. This is not
fixed fusion of source types and does not impose rational source-state
frequencies.

The remaining K3G problem is still shape-only color erasure: one unmarked
polygon must force the flag scaffold, internal cycle, paired midpoint and
six-sector source-vertex rules, frame, chirality and a witness lift. If no
boundary mechanism supplies both contextual state variation and a finite
contact-completeness proof within HC-11, K3G freezes without a geometric run.

## D-0099 (2026-07-21) — Search retilings, not isolated shapes

N10 shows that the convex K3F corner kite has a unique edge-to-edge
three-copy dissection of its equilateral macrotriangle. A uniquely aligned
full-side deformation likewise fixes the rooted contact star and supplies no
contextual alphabet. The undeformed flag scaffold is therefore a symbolic
support, not a candidate tile.

K3R replaces blind shape enumeration by inverse retiling. Seek one polygon
with multiple exact retilings of a fixed macrocell; retiling choices and their
boundary subdivisions are the symbols. The conditional R1--R5 theorem keeps
unique macro grouping, contact completeness, source decoding, chirality and
one lift separate.

No run is admitted yet. The final HC-11 session must give a bounded macrocell,
multiplicity, retiling template, unique-grouping marker and finite
contact-completeness argument. Otherwise K3R freezes as a search
specification. Intentional T-junctions are no longer forbidden categorically;
they must be exhaustively classified.

## D-0100 (2026-07-21) — Retain the binary retiling kernel; fire the HC-11 kill

Two right-isosceles copies tile one square along either diagonal. If a
polygonal deformation forces exclusive full hypotenuse pairing and a complete
leg/corner atlas, its tilings group uniquely into binary square macrocells.
The diagonal choice changes boundary ownership and corner valence, providing
a concrete contextual-state channel with two-dimensional plaquette coupling.

This is not a tile candidate. No guard is known that proves contact
completeness for unrestricted plane tilings, and no binary plaquette language
has been proved to decode totally to K3F/S0. B0 records the latter symbolic
question. Both results are required before boundary synthesis.

HC-11's kill condition therefore fires after session 90. No geometry run is
admitted; K3G remains frozen. The next admissible action is a primary-source
and on-paper audit of B0. Only a positive audit can justify a later fixed-`N`,
preregistered inverse boundary-word experiment.

## D-0101 (2026-07-21) — Identify the K3F flag with the exact kite substrate

The K3F flag carrier and the primitive cell of `substrate/kitegrid.py` have
the same ordered angles `60,90,120,90`.  Scaling K3F by `sqrt(3)` changes its
ordered sides from `1,1/sqrt(3),1/sqrt(3),1` to the repository cell's
`sqrt(3),1,1,sqrt(3)`.  They are the same metric kite up to scale.

Consequently the undeformed flag scaffold inherits the existing exact
hex-coordinate and `D6` machinery.  This is computational infrastructure, not
a candidate result.  A support made from at most 24 whole substrate cells is
inside the published polykite horizon; a free boundary deformation or
contextual retiling gadget need not be a polykite and is not classified by
that statement.

HC-12 is audit-only.  It distinguishes binary rule support, decoder radius
and the neighborhood a physical contact gadget can jointly see.  No binary
rule census or boundary synthesis is authorized.

## D-0102 (2026-07-21) — Refute `2x2` B0; retain larger binary support

Hu--Lin's peer-reviewed Theorem 2.3 is exactly about allowed subsets of the
sixteen binary `2x2` corner patterns.  It proves that every nonempty such
whole-plane language contains a doubly periodic configuration.  Therefore the
immediate K3B binary square-plaquette language cannot be strongly aperiodic
and cannot map totally and period-reflectingly to S0.  ST-M1.N11 refutes that
version of B0 without enumerating 65,536 rule sets.

This does not close binary encodings.  Kari--Moutot Theorem 9 and Lemma 25
effectively encode any Wang SFT into binary `n x m` rectangular rules whose
complete closure is exactly the translates of valid sparse encodings and
whose periodic-point existence agrees with the source.  Corollary 12 permits
fixed height `m=2` and sufficiently large width.  ST-M1.N12 therefore retains
a generalized finite-radius binary route, conditional on the still-missing
extensional S0 presentation.

No smallest surviving width is claimed.  Jeandel--Rao's 11-tile/four-color
minimum concerns ordinary edge-colored Wang tiles and does not by itself
settle binary corner plaquettes; it is Hu--Lin's corner theorem that supplies
the exact no-go.

## D-0103 (2026-07-21) — Replace bit-only B0 by the K4W retiling compiler

The visible diagonal map of a finite physical contact SFT is generally a
sofic projection, not automatically the `2x2` SFT formed from its observed bit
blocks. Hu--Lin closes the bit-complete K3B route but leaves independently
visible hidden docking states open. Such states must be recovered from
bounded unmarked geometry before source legality is invoked.

For an ordinary edge-Wang macro presentation, Jeandel--Rao force at least 11
macrostates and four interface colors. Two diagonal retilings with at most
`h` docking modes each therefore require `h>=6` (N13). This is a scoped
search lower bound, not a universal bound for vertex or larger-range systems.

K4W is the direct sufficient contract: one polygon must force unique square
macro grouping, locally visible states realizing a fixed aperiodic Wang set,
exact complete interfaces under full isometries, and one lift. Period descent
then proves aperiodicity. The preferred design specializes to the minimal
11-state/four-color Jeandel--Rao set and seeks at least 11 rooted exact
retilings of one macrocell rather than Kari--Moutot's enormous generic binary
strip.

HC-12 ends after session 93. No polygon or run is authorized. A future K4W
checkpoint must first produce on paper one exact macrocell topology supporting
11 rooted retilings and a plausible unique-grouping invariant; failure within
three sessions closes that parameterization without computation.

## D-0104 (2026-07-22) — Repair HC-12 provenance before HC-13

The HC-12 independent audit found one source-cache defect and one
non-load-bearing transcription error. The Hu--Lin catalog entry now points to
the Internet Archive snapshot of the AMS primary PDF. The repository fetcher
cached a 535,019-byte PDF whose SHA-256 is
`3f46f0e8f483f87a852f90bc28c0a51a0c798682ff1b4de4e50b1af09b7d5bbd`,
exactly matching the independently supplied digest; extracted text contains
Theorem 2.3's 17 corner cycle generators and 56 maximal noncycle generators.
The zero-byte failed temporary download was removed.

Kari--Moutot define `S={2^j-1 : 0<=j<=t-1}` and then `s=2^(t-1)`, not
`2^t-1`; hence their explicit sufficient width is `N=3*2^(t-1)`. N12 used
only finiteness and sufficiently large width, so its conclusion survives.
The correction is recorded before inverse-dissection work.

The user explicitly authorized `HC-2026-07-22-13`: at most three on-paper
sessions to exhibit one exact macrocell topology with at least 11 rooted
retilings and a credible unique-grouping invariant, or close that
parameterization without a shape run.

## D-0105 (2026-07-22) — A twelve-state synchronizing domino kernel

A rooted `2 x 16` macrorectangle has 12 selected equal-area domino retilings
of the form `VVV H w H VVV`, where `w` ranges over the width-six composition
words other than `VVVVVV`. The Fibonacci recurrence gives 13 width-six
words, hence 12 selected states; every state uses 16 congruent dominoes.

When admitted macros concatenate, the two three-column collars form a
maximal six-column vertical-domino bar. Because no selected macro contains
such a run, its midpoint identifies the seam locally. With vertically
aligned bars and a complete no-imitation contact rule, ST-M1.K5S proves a
unique radius-16 macro partition and state decoder. This is an exact
topological carrier and synchronization lemma, not an unmarked polygon:
ordinary dominoes do not enforce the guarded language, and the topology does
not yet route four Wang colors to four interfaces.

## D-0106 (2026-07-22) — Independent flips do not supply aperiodic arity

K5S clears the state-count threshold but its raw boundary ownership has one
variable channel: east/west are fixed and north/south are the same state
word. N14 proves any nonempty ordinary Wang language read only from those
signatures has a constant periodic tiling.

The obvious two-dimensional repair also fails. Four independent binary
domino flips in a `4 x 4` macro provide 16 rooted states and a pair of bits on
each side, but those bits are exactly four shared binary corner colors. N15
identifies the complete language with Hu--Lin's corner SFT, so every nonempty
selection has a periodic point. Independent local choices do not evade N11.

K5Q records the surviving compiler shape: four visible non-binary corner
modes plus an internal exact-cover relation. A `20 x 20` domino scaffold with
four `2 x 5` sockets supplies at least six exact modes per corner and can
carry a K5S-style synchronization rail. It does not enforce a relation among
the sockets. Hu--Lin mention a 44-tile six-color aperiodic corner system, but
that controlling source must be audited before use. No novelty, polygon or
aperiodicity claim is attached to K5Q.

## D-0107 (2026-07-22) — Couple all ports on one rooted closed corridor

N16 proves that four sockets separated by forced filler cannot impose an
aperiodic corner relation: their Cartesian-product language is empty or has a
constant periodic configuration. A real central constraint is mandatory.

K5C supplies a non-product exact topology. Encode the four two-bit colors of
each of the 11 source Wang tiles as one length-42 cyclic domino word. Fixed-
width `H VV`/`H H` bit blocks keep component count constant; a unique
`H VVVVVV H` delimiter roots the cycle and its four readout windows. The
prefix trie of the 11 words is a finite automaton accepting exactly the source
states. One physical cycle therefore couples all four interfaces rather than
allowing independent socket choices.

This meets HC-13's on-paper topology target and yields a compiler-aware
geometric admission contract. It does not solve the monotile problem. No
unmarked polygon is known to force bounded disjoint cycles, make the automaton
states independently visible, exclude all unintended contacts and lift the
source. HC-13 is exhausted at session 96; no shape run is authorized.

## D-0108 (2026-07-22) — Downgrade K5C to a test instance; retain only the gapless geometric residue

The HC-14 primary-source audit finds that K5C's symbolic architecture is
established prior art. Ollinger already concatenates all Wang codes, selects
one with a jaw, propagates its four interfaces by wires and proves an
all-tilings converse using five functional polyomino supports. Demaine et al.
compile plane tiling systems into one rotatable polygon, but in a prescribed
lattice “nearly-plane” model whose copies leave gaps. Greenfeld--Tao compile a
finite system of translational tiling equations into one equation by adding a
finite cyclic fibre. Fletcher, Socolar--Taylor, Akiyama and
Lagae--Kari--Dutre cover atlas, marked-boundary, unique-composition and
edge/corner recodings. The `44/6` corner system is a construction from the
16-Wang-tile/six-color source, not a lower bound.

Therefore K5C's trie, delimiter, selector, wire and corner-source conversions
carry no method-novelty claim. The only retained target is the conjunction not
supplied by those sources: one connected unmarked planar polygon, ordinary
gapless coverage without an imposed lattice/atlas/seed/fibre, full declared
isometries, and a total decoder on every shape-only tiling.

HC-14 may test one exact boundary mechanism against K5C.1--K5C.3. Failure to
prove bounded cycles, independently visible transition states and complete
contacts within sessions 98--99 closes the cyclic-corridor route without
enumeration. No symbolic redesign qualifies as progress on that residue.

## D-0109 (2026-07-22) — Refute the fixed-successor rosette

The first exact HC-14 mechanism gives one polygon an intrinsic head and tail
whose keyed fit fixes a relative isometry `g`. Requiring one predecessor and
successor per occurrence and taking `g` to have order 42 seems to force a
closed K5C corridor.

N17 proves the conflict. A finite component of length greater than two is an
orbit of a finite-order rotation. The successor rotation is transitive on the
unmarked ring, so no Euclidean-equivariant local decoder using that component
alone can select one delimiter or assign a nonconstant cyclic word. External
contacts may break the symmetry only by becoming the missing state/root
carrier themselves.

Thus one fixed docking transform cannot satisfy K5C.2--K5C.3. HC-14's final
session tests only the several-full-arc-mode escape; failure closes K5C without
geometry enumeration.

## D-0110 (2026-07-22) — Fire the HC-14 kill; freeze K5C geometry

N18 proves the gapless boundary-coverage obstruction: every nondegenerate
boundary port is contacted, so disjoint “optional” keys cannot encode a choice
by leaving all but one unused. Neutral caps would be additional roles whose
complete organization remains to be forced.

N19 bounds one specified full polygonal arc pair to at most four Euclidean
docking isometries (at most two after fixing which local sides face). This
prevents treating one full arc as an arbitrary automaton-state bank. A
two-mode endpoint flip could in principle feed a holonomy word test, but no
explicit boundary, length-42 component theorem, exact eleven-word acceptance
or pre-decoding state is supplied. It does not satisfy K5C.1--K5C.3.

HC-14's predeclared failure outcome therefore applies after session 99. K5C
is retained only as a conditional test instance and the cyclic-corridor route
is frozen. Reopening requires an explicit boundary with complete full-contact
modes, exclusive bounded closure, non-circular state/holonomy, exclusion of
partial/sliding/vertex faults and one gapless plane lift before any run.

## D-0111 (2026-07-22) — Admit only the subdivision-order T-junction residue

The HC-15 primary-source audit finds that multi-tile edge patches,
T-junction atlases and locally consistent contact-complex transport are
already explicit in the Spectre proof. Hellouin de Menibus--Lutfalla--Vanier
show that arbitrary symbolic rules can be superimposed on any nonempty FLC
geometric tiling space, but their construction uses labels and forbidden
patterns; their purely geometric undecidability theorem uses a finite
machine-dependent shapeset. Sugimoto's convex edge-to-edge theorem supplies
only a scope boundary: that class always has a periodic monohedral
realization.

HC-15 therefore makes no general T-junction, FLC-recoding or compiler-novelty
claim. It admits one narrower object: a host side fully partitioned by
unequal complete sides of congruent neighbors, with the order of their
lengths proposed as a locally visible state. Sessions 101--102 may derive
exact order-capacity and endpoint-angle lemmas and must either give one exact
nonoverlapping polygonal contact witness with multiple full-isometry states,
or close the fixed class by a scoped no-go. No enumeration or candidate
promotion is authorized.

## D-0112 (2026-07-22) — Subdivision order starts at three states, not one bit

K6O counts the fixed interval contact complex exactly. With `k` pairwise
distinct complete neighbor-side lengths summing to one host side, full
Euclidean isometry identifies precisely a word and its reversal, leaving
`k!/2` order states. N20 therefore refutes the smallest three-occurrence
binary idea: the two orders of two unequal neighbors are mirror images and
form one state. Three neighbors give three states; four give twelve.

At each ordinary internal T-junction, J0 forces the two neighbor endpoint
angles to sum to `pi`. Right-angle ports are a universal sufficient local
vocabulary. These results concern abstract interval contact complexes and do
not prove that congruent copies of one polygon realize multiple orders.
Session 102 retains exactly that geometric obligation for the host-plus-three
class. Failure closes the class under HC-15's stop rule.

## D-0113 (2026-07-22) — Close convex subdivision ports; fire the HC-15 stop

N21 applies the convex exterior-turn budget to the natural complementary-port
realization of K6O. Every code side whose endpoint interior angles sum to
`pi` consumes exactly `pi` across its two exterior turns. Three or more such
sides cannot form a proper subset of a convex boundary: multiple blocks or a
block of length at least four exceed total turn `2*pi`; one block of three
forces a quadrilateral, whose host-length equality is degenerate.

Thus right-angle ports and all convex fixed-directed-pose universal-order
carriers are impossible. This is a scoped no-go, not a theorem against
nonconvex supports, contextual reflection choices, extra participants or
selected non-complementary words.

No exact nonconvex polygonal witness was found on paper. HC-15 is exhausted
at session 102 and its stop rule fires without an experiment. K6O is retained
only as an exact compiler-aware search primitive. Reopening requires exact
coordinates and two hand-verifiable non-reversal patches before any contact
classification run.

## D-0114 (2026-07-22) — Admit HC-16's selected-word route; derive K7A

After independent review of HC-15, the user authorizes one three-session
on-paper checkpoint. The escape route is fixed in advance: a nonconvex
support, two selected non-reversal three-neighbor words, fixed directed poses,
ordinary three-participant internal junctions, no contextual handedness and
no extra junction participant. Failure to give exact coordinates with
hand-checkable coverage and disjointness freezes that named route; it does not
authorize enumeration or an optimizer.

K7A classifies the endpoint equations before any polygon is drawn. Up to
reversal and relabeling, two classes are `ABC` and `ACB`. J0 forces
`ell_B=ell_C=theta` and `rho_A=rho_B=rho_C=pi-theta`; only `ell_A` remains
free. Choosing `ell_A != theta` admits exactly those two classes and excludes
the third, where `A` would become the middle role. The orthogonal choice
`theta=pi/2`, `ell_A=3*pi/2` therefore gives an exact two-state selector and
forces genuine nonconvexity.

This is local-angle feasibility only. No polygon, contact patch, all-tilings
decoder or monotile is claimed. The zero-byte literature-fetch remnant named
in the review was removed; the verified source PDF and hash-bearing catalog
entry remain unchanged.

## D-0115 (2026-07-22) — Reduce HC-16 to one common collar and two tail packings

K7C strengthens the selected-word selector without proposing a shape. If an
internal neighbor--neighbor stem is required to be one complete clean contact
with no extra participant, the four junction equations for `ABC` and `ACB`
force all five used leaving sides to have one common length `d`. In the
orthogonal specialization, both words then have an automatically disjoint
rectangular collar of depth `d` below the host.

All remaining overlap is captured by six exact intersections among three
rooted tails at the offsets written in theory note 22. A shorter/longer stem
mismatch would introduce another partial contact or junction and is outside
the route fixed at HC-16 admission. This is a reduction, not a polygonal
witness: the tails and the host-versus-tail inequalities remain open, and no
coordinate search is authorized.

## D-0116 (2026-07-22) — Fire the HC-16 stop at exact tail packing

No exact orthogonal polygonal disk was found on paper whose three rooted
tails satisfy both K7C offset triples and remain disjoint from the host.
Local angle closure and a valid common collar are not promoted into a patch:
the unresolved intersections begin immediately below that collar.

HC-16 is exhausted at session 105, so its predeclared stop fires. K7A and
K7C remain exact proof-draft primitives, but the selected-word polygon route
is frozen without a coordinate search, optimizer, SVG or candidate. This is
not a no-go theorem for arbitrary nonconvex carriers. Reopening the same
route requires an exact polygon and both complete hand-verified placement
lists before computation; unequal stems, contextual handedness or extra
participants constitute different routes requiring new admission.

## D-0117 (2026-07-22) — Correct K7C and admit one unequal-stem cap route

The HC-16 review identifies ERR-007: K7C settles only the open footprint
below the host, not the whole horizontal strip. The `3*pi/2` endpoint of `A`
has a third-quadrant spillover germ, which remains in `Q_A`; with no third
participant there, the host corner is forced to `pi/2`. The theory note is
corrected before downstream work. The reviewed zero-byte Conway--Lagarias
fetch remnant is removed while its intact source PDF remains unchanged.

The user authorizes HC-17. It fixes the smallest different mechanism:
ordinary K7A primary junctions, one deliberate unequal first stem, and
exactly one secondary congruent cap occurrence per mismatch. N22 proves that
some secondary participant is necessary in every gapless realization and
gives its angle equation. Sessions 107--108 may solve the finite length/cap
closure and either exhibit an exact finite contact complex or freeze the
route. Contextual handedness, unbounded junction cascades, a contact atlas,
coordinate search and candidate promotion are not authorized.

## D-0118 (2026-07-22) — Uniform unequal stems have one exact length family

K8U solves the HC-17 length algebra. Up to reflecting the complete patch,
every used right stem has one length `s` and the used left stems of `B,C`
have length `s+Delta`. These equalities are necessary and sufficient for all
four adjacencies in `ABC,ACB` to expose the same directed excess `Delta`.
The unused left stem of `A` remains free.

Thus each selected word creates two identical secondary sockets, and a cap
that occupies the complete exposed segment needs a side of length `Delta`
and a right-angle entry. This is a finite symbolic/contact result, not a
polygon. The lower endpoint must close through a finite exact contact cycle
among the admitted occurrences; otherwise N22 recurs and the forbidden
participant cascade begins. Session 108 is the final HC-17 session and may
not replace that missing cycle with coordinates, search or an unspecified
atlas.

## D-0119 (2026-07-22) — One cap side transports the mismatch; fire HC-17

At the lower endpoint of the K8U socket, a cap can pair its K7A reflex
`3*pi/2` endpoint with a convex `pi/2` endpoint of the longer neighbor. The
angles fill `2*pi`, but N23 proves that this does not end their contact. With
only those two occurrences covering a neighborhood, their common polygonal
boundary must continue through the vertex along another positive-length
side. Unequal next sides recreate N22; equal next sides only move the same
obligation forward.

No finite multi-edge interface returning both cap branches to the original
shorter occurrence was derived. HC-17 is exhausted at session 108, so its
stop fires without coordinates, enumeration, SVG or candidate promotion.
This closes only the one-edge/unserialized-cap route. An exact finite cyclic
boundary word supplied before computation may reopen unequal stems; arbitrary
unequal-stem carriers are not refuted.

## D-0120 (2026-07-22) — Admit HC-18 and derive the four-sector selector

The user authorizes HC-18 after independent review. Before research, all five
zero-byte literature download remnants are removed in one sweep after their
intact source PDFs are confirmed. Three older empty compiled streams are
classified rather than deleted: the n=13 A1 certificate stream records zero
admissible scheduled quotient cases, while the n=9 depth-2 and n=11 depth-3
positive-witness streams agree with zero-count survivor/exhausted headers and
the original exact result tables. File emptiness alone is not used as a
verdict.

HC-18 then admits one mechanism outside J0/K7C/K8U: a fourth congruent
occurrence contributes a fixed positive angle `gamma` between the two code
neighbors at every primary host subdivision. K9A solves the four sector
equations. The selected words `ABC,ACB` require common
`ell_B=ell_C=theta` and common
`rho_A=rho_B=rho_C=pi-gamma-theta`; the third reversal class is excluded
exactly when `ell_A!=theta`. Thus the primary selector can be locally convex,
but no guard occurrence or polygon has yet been realized. HC-18 remains
on-paper and must close a finite residual topology within three sessions or
freeze without a shape run.

## D-0121 (2026-07-22) — Curvature forces guard-role reuse or nonconvexity

K9V applies the total exterior-turn budget before any coordinates. Each of
the `B,C` code sides consumes endpoint turns summing to `pi+gamma`; therefore
the two sides must be adjacent in every convex carrier. If their common
interior angle is `alpha`, all remaining vertices receive only
`pi-alpha-2*gamma` exterior turn. A separate guard vertex alone needs
`pi-gamma`, which never fits. Thus a convex realization must reuse the guard
vertex as a `B/C` endpoint, while a carrier with a distinct guard feature is
necessarily nonconvex. The symmetric three-`pi/3` primary star is eliminated
convexly.

N24 independently closes the point-plug interpretation. The positive guard
sector creates two nondegenerate guard--neighbor interfaces, and N23 forces a
secondary participant at the terminal point of each maximal interface. A
surviving route must therefore provide a bounded contact complex, not merely
an extra angle label. Session 111 may state that complex and its complete
sector algebra; otherwise the HC-18 stop fires.

## D-0122 (2026-07-22) — Retain the bounded guard-and-shield topology

K9T supplies the finite residue required by HC-18. The guard's complete
boundary is divided into three arcs contacted cyclically by the left code
neighbor, one shield occurrence and the right code neighbor. The host touches
the guard at the primary point. The two guard interfaces terminate at exact
three-sector stars with that same shield, so no guard boundary is left to an
unnamed continuation.

Fixed guard/shield poses force one common terminal angle on left roles
`A,B,C` and another on right roles `B,C`. Together with K9A these conditions
are necessary and sufficient for the sector algebra of all four selected
adjacencies. Restriction to the recognizable host interval preserves the two
non-reversal word states. An explicit rational-angle example proves local
consistency but is not a polygon angle list.

HC-18 therefore closes positively at its declared level: a finite
state-bearing contact topology with bounded residue exists on paper. No
polygonal support, placement patch, forcing theorem, monotile or method
novelty is claimed. A later geometry checkpoint must preselect either
nonconvexity or convex guard/code-vertex reuse, state every intrinsic role
identification, and give exact coordinates and both complete shield patches
before any computation. Failure closes this topology; it does not authorize
a larger atlas.

## D-0123 (2026-07-22) — Enumerate HC-19 roles and close convex guard reuse

The user authorizes HC-19 with explicit recognition obligations for the six
occurrence roles `H,A,B,C,G,W`. Distinct host/code lengths recover only the
host word; guard pose, shield arc, terminal vertices and every repeated
length/angle also require intrinsic or contact-context recognition before a
polygon could be admitted.

N25 closes the cheaper convex branch completely under K9T's fixed complete
spokes. K9V forces the guard vertex onto the adjacent `B/C` block. At their
shared vertex, the two sides leaving that endpoint have swapped lengths
`b,c`, while the clean-spoke equations require equality. At an outer endpoint,
the other endpoint angle is `pi-2gamma`, making K9V's strict curvature
inequality an equality and leaving no turn for `A,H`. Equal endpoint angles
reduce to the already excluded `gamma=pi/3` zero-remainder case.

Thus fixed-pose, distinct-length K9T geometry is necessarily nonconvex. This
is a theorem for the named branch, not a failed coordinate attempt. Sessions
113--114 may examine one right-angle shield skeleton and must still provide a
complete polygon and both exact patches or close K9T without search.

## D-0124 (2026-07-22) — Fix one 15-edge nonconvex shield skeleton

K10B is the sole nonconvex geometry admitted after N25. Its cyclic length
word is
`d,A,d,B,d,C,d,H,d,C,d,B,d,A,d`, with exact code lengths
`1,2,4`, host length `7`, a right-angle equal-leg guard tip, and five fixed
`pi/4` code/spoke endpoints. The thirteen-edge shield spine is centrally
paired around the unique host side. Half-turn about its midpoint gives the
shield occurrence and, conditional on simplicity and lens containment,
proves exact full-spine contact and disjoint interiors.

The role audit is explicit: `H,A,B,C` are recovered by length; `Gamma` by its
angle, equal incident spokes and opposite rooted word; guard orientation by
the code progression; and shield by the complete spine rooted at `H`. Paired
copies of each code side are the same reversal role. Any other occurrence of
the guard context invalidates recognition.

This is a finite coordinate system and exact relative isometry, not yet a
polygon. Session 114 must solve all spine coordinates, simplicity/lens
inequalities and both eight-occurrence shield patches. Failure closes K9T;
no second boundary word or coordinate search is admitted.

## D-0125 (2026-07-22) — Correct K10B role pairing and fire HC-19

ERR-008 corrects the session-113 claim that equal-length sides paired across
the half-turn spine are the same reversal role. Opposite-side full-spine
docking makes their carrier angles complementary to `2*pi`; intended convex
code sides are paired with reflex auxiliary sides. Length plus endpoint
context recovers the intended role locally, and a reflex endpoint cannot fit
beside the host's `pi` sector at an internal division. The auxiliary sides
remain an explicit all-tilings contact-completeness burden.

No exact 15-edge coordinate list closes K10B's simultaneous simplicity,
lens, recognition and both-patch disjointness obligations. The half-turn
guard/shield pair is insufficient by itself, and no approximate spine is
promoted. HC-19 is exhausted at session 114, so its stop fires without a
polygon, SVG, coordinate search or candidate. N25 and N26 are retained as
exact filters and K10B as a conditional reduction. K10T/K10W are frozen;
reopening this exact word requires complete coordinates and both placement
tables before computation.

## D-0126 (2026-07-22) — Open HC-20 and separate duplication from control

The user authorizes HC-20 after independent review, with correction of the
stale K10B sentence as a precondition. Theory note 25 now says that paired
`A,B,C` occurrences share a length class but have distinct intended-convex
and auxiliary-reflex contexts, consistently with ERR-008/N26.

N27 proves the first control layer exactly. At an internal subdivision of a
straight host side, the host already contributes angle `pi`; an N26 reflex
auxiliary endpoint contributes more than `pi`, so the two interiors cannot be
disjoint. Length plus convex endpoint context therefore recovers the intended
code role at every primary host junction.

This does not control auxiliary contacts elsewhere. HC-20 has at most three
on-paper sessions to derive a finite synchronization condition and apply it
to the fixed K10B word. K10W may reopen only with its pre-existing complete
exact coordinate list and both placement tables. Otherwise the checkpoint
must state the failed condition and retain the freeze. No experiment,
alternative spine, contact-atlas enlargement or approximate geometry is
admitted.

## D-0127 (2026-07-22) — A finite atomic root controls duplicated shield arcs

K11S answers HC-20's general theorem question positively but conditionally.
Assume one selected root side has vertex-aligned contacts and its complete
finite cover table consists of one full intrinsic mate side. Aligning that
mate across the root fixes the neighboring congruent polygon. If this exact
pose has disjoint interior and shares the selected complete arc, every
auxiliary side on the arc belongs to that one forced shield pair.

The certificate is bounded: one root-side cover table, one rooted mate and
one exact two-copy intersection proof. It is not a full contact atlas. Vertex
alignment is an explicit hypothesis, so sliding or overhanging contacts are
not hidden. K11S proves that N26 duplication is not inherently uncontrollable;
it does not prove that K10B has an atomic root.

K10B's only plausible synchronizer is its unique `H` side. Session 117 must
test every root cover word of `H`, including T-junction subdivisions. A
unique single-side length does not establish atomicity.

## D-0128 (2026-07-22) — Correct the terminal scope and close HC-20

ERR-009 corrects N26 before K11S is applied. The two half-turn occurrences
fill a complete disk only at nonterminal spine vertices. At terminal `R,Q`
they fill the right-angle lens corner, so paired terminal `A` angles sum to
`pi/2`, not `2*pi`. Paired `B,C` remain reflex at both endpoints; paired `A`
has one reflex internal endpoint and one convex terminal endpoint. N27 is
therefore an endpoint-polarity theorem, not a proof for every endpoint of
every code side.

This also retracts D-0127's sentence calling `H` the only plausible
synchronizer. It was merely the first proposed root. N28 proves that `H`
itself cannot be atomic: the shield requires cover `[H]`, while the two
compiler states require `[A,B,C]` and `[A,C,B]`, with `7=1+2+4`. The other
intrinsic sides have no complete vertex-alignment and root-cover certificate;
length alone does not close them.

HC-20 therefore closes at its declared boundary. K11S is retained as a
general finite sufficient theorem showing that auxiliary duplication is not
intrinsically uncontrollable. K10B does not yet meet it and K10W remains
frozen. No coordinates, placement tables, polygon, SVG, experiment or
candidate were produced. Reopening requires either a complete atomic-root
certificate for another named side together with the existing exact K10W
geometry, or a stronger finite contextual synchronizer that safely accepts
the multiplexed `H` cover words.

## D-0129 (2026-07-22) — Fix radius one before contextual synchronization

The user authorizes HC-21 after independent review. Its context radius is
fixed before work: `Star_1(H)` contains the root occurrence, every occurrence
meeting any point of its closed `H` side (including point-only subdivision and
endpoint participants), and only the incidences, sectors and rooted boundary
germs based at that side. Occurrences meeting those neighbors only away from
`H` are outside the radius.

K12C states the complete finite certificate required for a contextual
decoder with values `shield,host_0,host_1`. The three intended cover words are
`[H]`, `[A,B,C]` and `[A,C,B]`. Totality is on the full unrestricted
radius-one local closure: partial/sliding covers, other words, symmetries and
extra point participants must be excluded, and every retained class needs a
source lift.

Sessions 119--120 may use only the existing exact K9A/K9T length and sector
algebra to test this contract. If another locally compatible word survives
without an already-proved radius-one exclusion, radius one closes. No radius
escalation, coordinate work, alternative boundary, experiment, atlas
enumeration or candidate promotion is authorized.

## D-0130 (2026-07-22) — K9A forces a fourth radius-one cover algebraically

The selected K9A transitions force common
`ell_B=ell_C=theta` and
`rho_A=rho_B=rho_C=pi-gamma-theta`. Consequently `B|B` satisfies the same
four-sector equation and clean-spoke lengths as the selected transitions.
Together with `H=7`, `A=1`, `B=2`, this produces the exact additional cover
`[A,B,B,B]`. K9T's factorized terminal classes accept its left `A` and right
`B` roles.

N29 therefore closes every radius-one proof built only from independent
length, primary-sector, spoke and terminal equations. It does not assert that
the complete polygonal `ABBB` star is overlap-free. A surviving K12C route
must prove within the already fixed `Star_1(H)` that the `B|G|B` star is
geometrically impossible, that several such complexes collide, or that a
visible joint feature forces exactly three code occurrences. Merely imposing
the intended part count is not a shape proof, and remote shield contacts are
outside HC-21's radius.

## D-0131 (2026-07-22) — The fourth word survives an exact collar; close HC-21

N30 strengthens N29 without overclaiming a polygonal patch. Partition the
host at `1,3,5,7`. At its `A|B,B|B,B|B` junctions, the host's lower `pi`
sector and the upper `rho_X,gamma,ell_B` sectors cover disjoint
neighborhoods exactly. The junctions are separated, so these neighborhoods
and thin side collars combine without overlap. The left endpoint is the
accepted `A` role and the right endpoint is the accepted `B` role.

Thus no independent endpoint or primary-sector argument can reject `ABBB`.
An exclusion must use complete occurrence geometry away from `H`: a
`B|G|B` same-role collision or a multi-junction overlap/coupling. No such
coordinate-free theorem exists in the current chain, and K10B has no exact
polygon or placement table on which to verify it. N30 is not a complete-star
existence proof.

HC-21's predeclared stop therefore fires at radius one. K12C remains an open
frozen contract, and factorized angle/contact synchronization is closed for
K10B. No radius escalation, coordinates, alternative boundary, experiment,
SVG or candidate follows. Reopening requires an exact collision theorem or a
complete K10B polygon and full radius-one tables supplied before work.

## D-0132 (2026-07-22) — Admit joint weighted-language design

The user authorizes HC-22 after independent review. Lengths and selected
words are one joint design object: the transition graph is the complete
closure forced by their local equations, not the desired edge list. K13W
proves that exact positive weights bound every host word to at most
`floor(h/min w)` roles. The desired language is complete exactly when its
words have weight `h` and every other bounded directed start-to-terminal path
has different weight.

This is a finite arithmetic criterion and a standard weighted-automaton
argument; no method novelty is claimed. Sessions 122--123 must derive a
necessary-and-sufficient symbolic specialization for the K9A words
`ABC,ACB`, then prove either a reusable passing family or nonexistence. A
triple search, coordinate work, polygon, boundary synthesis, experiment, SVG,
radius escalation or candidate promotion is not authorized.

## D-0133 (2026-07-22) — Characterize the K9A host language exactly

The equations forced jointly by `ABC,ACB` close the transition graph to
`{A,B,C} x {B,C}`: every edge into `B,C` is legal and every edge into `A` is
illegal. K13A splits accepted host words into an optional unique initial `A`
and a word over `B,C`.

The desired two-word language is complete if and only if `b+c` has the unique
nonnegative `(b,c)` representation `(1,1)` and `h=a+b+c` is not in the
semigroup `<b,c>`. The first condition is equivalently that neither ratio
`b/c,c/b` is a positive integer; the second is a finite bounded membership
test. This is necessary and sufficient, not a heuristic.

The criterion explains two distinct traps. `(1,2,4)` fails uniqueness and
admits `ABBB`; `(1,2,3)` passes that test but has `h=6=3b=2c`, admitting
`BBB` and `CC`. Session 123 must prove a reusable passing family or close the
class. No enumeration or geometry is authorized.

## D-0134 (2026-07-22) — Retain an infinite arithmetic design family

K13F proves that every integer `n>=4` with

```text
(a,b,c,h)=(1,n,n+2,2n+3)
```

satisfies both K13A conditions. For representations over `b,c`, the total
coefficient count is forced to two; U1 then forces one copy of each, while U2
fails by parity between `2n,2n+2,2n+4` and `2n+3`. Thus the complete
code-only host language is exactly `ABC,ACB`. This is an infinite symbolic
family proved without a triple search.

Under the separate cover-side alignment hypothesis V, choosing `d=3n>h`
also prevents a full `d` side from entering an `H` partition, leaving exactly
`[H]` and the two code words at the arithmetic level. Sliding and overhangs
are not excluded by this inequality.

HC-22 closes positively as an arithmetic boundary-design result. It does not
repair the original `(1,2,4)` skeleton or establish any polygon, coordinate,
patch, full local language, tiling, aperiodicity, candidate, or novelty claim.
Those geometric and literature gates remain explicit. No computation or
artifact was produced.

## D-0135 (2026-07-22) — Fix HC-23 geometry and redo every length role

The user authorizes HC-23 after independent review for the smallest K13F
weights `(a,b,c,h)=(1,4,6,11)` with `d=12` and the unchanged K10B word. The
role audit is redone rather than inherited. `A,B,C` each have intended and
ERR-008/ERR-009 auxiliary contexts, `H` is intrinsically unique, and eight
`d` sides require ordered local context.

Beyond `H`, HC-23 explicitly tracks the full-side arithmetic cover tables of
`A,B,C,d`. K14R records every coefficient solution over lengths
`{1,4,6,11,12}`; the many coincidences show why length alone cannot prove
contact completeness. These tables are conditional on cover-side alignment
and do not enumerate geometric contacts.

The guard and its half-turn bound a square lens of side `d`. The spine starts
with lengths `a,d` meeting at interior angle `pi/4`. Session 125 must derive
the exact prefix and central-edge containment inequalities before closure
coordinates. Failure closes this fixed instance by theorem; no alternative
tuple, `d`, word, computation, SVG or candidate is admitted.

## D-0136 (2026-07-22) — Close the K13F/K10B square-lens pairing

N31 proves a necessary condition before any coordinate fitting. Put the
K10B square lens in orthonormal coordinates at its endpoint `R`. The first
`A` edge lies in the square's tangent quadrant. Turning by the prescribed
`+/-3*pi/4` into the following `d` edge makes one coordinate at most
`a-d/sqrt(2)`. Containment therefore requires `d<=sqrt(2)a`. The central
host edge is a segment in the same square, so `h<=sqrt(2)d`. Together,
`h<=2a`, or `b+c<=a` when `h=a+b+c`.

The fixed tuple `(1,4,6,11;d=12)` violates both the prefix bound and the
combined bound. Every K13F member `(1,n,n+2,2n+3)`, `n>=4`, also violates
`b+c<=a`, independent of `d`. HC-23's predeclared stop therefore fires in
session 125 without coordinates or computation.

This closes only the unchanged K10B square-lens word/angle topology paired
with K13F. K13F's arithmetic language remains proved. A different boundary
word, guard geometry or first-angle assignment requires a new checkpoint and
must name which N31 hypothesis it changes; no such branch is admitted here.

## D-0137 (2026-07-22) — Admit the complete K10B feasibility system

After independent review, the user explicitly authorizes HC-24. The branch
keeps K10B's square lens, boundary word, first `A,d` prefix and angle
assignment, but no longer fixes K13F's weights. It must derive every spine
vertex exactly over `Q(sqrt(2))` and reduce complete lens containment to a
finite exact system before choosing a new tuple.

That geometric system is solved jointly with K13A's U1/U2 arithmetic
conditions. The old shortcut `d>h` is not inherited: exclusion of unintended
`d`-side host covers must be handled by exact semigroup arithmetic. Any
surviving tuple must also redo the complete role and side-cover audit from
zero rather than inherit K14R.

HC-24 has at most three sessions to prove a viable exact family or a scoped
incompatibility theorem. Numerical search, approximate coordinate fitting,
experiment, SVG, candidate promotion and an enlarged boundary/contact atlas
are not authorized.

## D-0138 (2026-07-22) — Retain the exact semialgebraic lens system

K10B fixes five relative `pi/4` turns but not the terminal `A` angle. Thus
the relative spine offsets lie in the `Q(sqrt(2))`-linear span of the
weights, while the absolute orientation remains one unit variable `(C,S)`.
K15S records all partial sums, every strict square inequality, and the exact
central host-length equation. The latter reduces to one line on the unit
circle, so the problem is finite and exact but not linear in the weights
alone. No angle is silently fixed to satisfy the audit prompt.

The fourth partial sum strengthens N31. N32 proves every feasible fixed-order
spine needs

```text
b+c<a<(1+sqrt(2))*b-c,       b>sqrt(2)*c.
```

In particular the review's illustrative `(11,4,6,21)` tuple fails the
complete prefix even though it passes N31. K15D handles the changed `d`
burden: because K15S implies `2d>h`, an arithmetic host cover involving `d`
exists exactly when `h-d` is a nonnegative member of `<a,b,c>`.

Session 126 selects no tuple. The next session must solve K15S, N32, K13A
and K15D jointly by exact analysis, not parameter enumeration or approximate
fitting.

## D-0139 (2026-07-22) — Close every unchanged K10B square-lens weight

N33 solves K15S before the K13A arithmetic is needed. Normalize `d=1` and
write the strict N32 slack as positive margins `alpha,beta,mu`; positivity of
`c` makes their sum smaller than `1-1/sqrt(2)`. The fourth and sixth exact
partial sums then impose opposing bounds `beta>L(t)` and `beta<U(t)` on the
free orientation `t=tan(x)`, with `0<t<1`.

The inequality `L(t)>U(t)` is exact: after clearing the positive denominator
and squaring positive sides, its difference factors as

```text
(1-t)*(t^3+5*t^2+5*t+1)/2 > 0.
```

Thus no positive weights `(a,b,c,d)`, with `h=a+b+c`, satisfy the unchanged
K10B square-lens system. HC-24 closes one session early without tuple
selection, coordinate fitting or computation. U1/U2 and K15D remain valid
arithmetic tools, but their joint K10B feasible set is empty.

This decision does not close K13A, unequal/non-square guards, changed
boundary prefixes, changed sharp angles or other monotile mechanisms. A
future checkpoint must name which N33 hypothesis it changes; varying weights
alone is closed.

## D-0140 (2026-07-22) — Admit unequal right-angle guard spokes

The user explicitly authorizes HC-25 to change the equal-leg hypothesis of
N33 while retaining K9A/K9T's right-angle guard and complete clean-spoke
semantics. The first obligation is combinatorial: determine whether K10B's
old one-edge connectors can simultaneously realize outgoing spoke length
`u` and incoming spoke length `v` when `u!=v`.

If that is impossible, HC-25 may introduce only the minimal split connector
needed to place one `u` side and one `v` side between selected code roles. It
must fix the resulting boundary topology and derive the exact rectangular-
lens system before any coordinates. At most three sessions may produce a
viable exact mechanism or a scoped no-go.

No numerical search, approximate fitting, experiment, SVG, larger contact
atlas, polygon promotion or candidate claim is authorized. Adding further
junction participants or changing the right angle is outside this checkpoint.

## D-0141 (2026-07-22) — Split the unequal spoke connector minimally

N34 proves that K10B's original one-side connectors cannot carry unequal
clean-spoke lengths: the same `A--B` side is both `u_A` and `v_B`, and the
same identity occurs at `B--C`. Thus unequal spokes necessarily change the
boundary word; relabeling the old `d` sides is invalid.

K16B introduces exactly one new vertex at each incompatible connector and
its central partner. The first half becomes `A,u,v,B,u,v,C,u`, the complete
spine is its reversal around `H`, and unequal perpendicular guard legs close
the 19-edge cyclic word (3.3). Their half-turn lens is a `v`-by-`u`
rectangle. This is edge-count-minimal only within the declared split of the
old connectors; it is not a polygonal realization or uniqueness theorem over
all possible topologies.

The two new `u|v` bridge angles are explicit unknowns. Session 129 must derive
the full exact rectangular-lens system and test whether those angles are
geometrically determined or merely reintroduced colors. No angle choice,
coordinate fitting or added participant is authorized in session 128.

## D-0142 (2026-07-22) — Retain the finite bridge-angle system

K17S gives the complete K16B rectangular-lens model: eight explicit
first-half partial sums in two bridge-turn units, sixteen two-sided rectangle
bounds (32 scalar inequalities), central reversal and one host-length equation. For fixed bridge
angles and weights, closure is again a line in the terminal unit direction.
Simplicity remains a separate finite segment-intersection obligation.

K17G establishes that the bridge angles are not symbolic colors. Each lies
between the ordered unequal intrinsic lengths `(u,v)`, so it is a measurable
boundary feature fixed once by the polygon. This does not force intended
contacts, but it permits the angles to remain honest geometric parameters in
the final HC-25 question.

Session 130 must either give one exact simple open-rectangle spine with fixed
bridge angles and hand-checkable nonintersection, or prove K16B incompatible.
Failure closes HC-25. Numerical fitting, angle enumeration, extra edges,
changed guard angle, SVG and candidate promotion remain forbidden.

## D-0143 (2026-07-22) — Freeze unequal spokes at K16W

HC-25 reaches its three-session stop without an exact simple K17S spine or a
general incompatibility proof. The straight-bridge specialization is
reducible and therefore not K16B. Reusing `pi/4` at both bridges gives the
exact eight-direction expression (10.2), but neither proves nor refutes all
rectangle and central-closure predicates. Opposed width chords remain coupled
through the fixed hooks and host equation.

The finite unresolved obligation is named K16W: fixed exact positive weights,
two fixed irredundant bridge angles, one exact terminal orientation, all
K17S inequalities and host closure, and a complete nonintersection proof.
No such witness, polygon, patch or candidate is claimed, and no no-go theorem
for the free-angle topology is claimed.

The branch is frozen. Reopening requires a complete exact K16W witness
supplied before computation or a theorem eliminating the bridge variables.
Angle enumeration, numerical fitting, added edges, a larger contact atlas and
SVG-led promotion are not authorized continuations.

## D-0144 (2026-07-22) — Admit one theorem-only K16W elimination checkpoint

After independent review of HC-24 and HC-25, the user explicitly authorizes
HC-26 as one theorem-only attempt on K16W. It has exactly three admissible
terminal outcomes:

1. an exact simple witness satisfying every predicate in (11.1);
2. a scoped incompatibility theorem for K16B; or
3. a freeze at K16W, with the next proposed pivot fixed in advance as the
   non-right guard angle `gamma!=pi/2`.

A partial angle or inequality analysis does not count as success. The first
mathematical target is the exact necessary cone of the two bridge-independent
rigid chains `v,B,u` and `v,C,u`. Any subsequent elimination must treat both
global turn orientations and the exceptional case in which the closure line
(7.1) is identically satisfied. HC-26 stops within three sessions.

No numerical angle or coordinate search, experiment, SVG, extra edge,
additional participant, larger contact atlas, polygon promotion or candidate
claim is authorized.

## D-0145 (2026-07-22) — Retain the exact hook cones; close exceptional cases

K18H classifies each bridge-independent `v,w,u` hook by six explicit pair
differences and twelve two-sided coordinate-span bounds. Every K17S solution
must satisfy this cone once for `w=b` and once for `w=c`. The exact control
`(u,v,w)=(1001/1000,1,1)`, `r=(3/5,4/5)` lies strictly in the cone, so the
requested first target does not supply a hook-only incompatibility theorem.

N35 proves that the terminal closure line cannot degenerate identically under
K17S: vanishing of its two coefficients forces `w_8=0`, contradicting strict
containment at the eighth vertex. K18R handles the opposite global turn sign
by complex conjugation and reflection, preserving every metric, containment
and nonintersection predicate.

HC-26 therefore remains open for two sessions. They must couple both hook
cones through the bridge variables and closure and reach the existing exact
trichotomy; the local cone is not a successful terminal result.

## D-0146 (2026-07-22) — Retain prefix and closure eliminations without promotion

K19P derives the complete first-corner cone and the necessary bound
`a>u/sqrt(2)`. K19E independently eliminates all three endpoint phases from
host closure: the relaxed equation is exactly an annulus/circle radial-
interval intersection. Both derivations handle continuous bridge angles
without sampling.

Exact unequal-leg controls show that neither relaxation is contradictory.
The tuple `(u,v,a)=(1,2,1)` with first direction `(24/25,7/25)` passes K19P;
adding `b=c=1/10` passes K19E. The tuple is not asserted to pass the two
rigid-hook cones or simultaneous containment and is not a K16W witness.

HC-26 has one session left. The prefix and closure results do not satisfy the
terminal trichotomy; only a complete exact simple witness or scoped K16B
incompatibility theorem prevents the predeclared freeze.

## D-0147 (2026-07-22) — Fire the HC-26 freeze; retain K16W only as an exact obligation

K20L proves that `(u,v,a,b,c,h)=(1,2,1,1/10,1/10,6/5)` passes
K19P, both isolated K18H cones and K19E separately, with exact rational unit
directions. This rules out a contradiction derived only from the weights and
those decoupled projections. It does not combine their phases into one spine
and is not a compatibility or candidate claim.

The last authorized session obtains neither a complete exact simple K16W
witness nor a scoped incompatibility theorem for every bridge choice.
Therefore HC-26's predeclared third outcome fires. K16W remains open but
frozen; no angle enumeration, coordinate fitting, extra bridge, SVG or
candidate promotion follows.

The next proposed branch is fixed as the non-right guard-angle mechanism
`gamma!=pi/2`. It changes a named K9A/K9T hypothesis rather than modifying
K16B again and requires a new human checkpoint before work begins.

## D-0148 (2026-07-22) — Repair K20L and admit one exact K16W decision

Independent audit found that K20L's printed vector was not unit. ERR-010 is
the controlling correction: `(544/545,33/545)` replaces it and exactly
restores the isolated-hook control. The false session-133 Pythagorean check is
withdrawn. No downstream result changes.

The user explicitly authorizes HC-27 to replace the hand-only K16W freeze by
one preregistered decision of the complete normalized existential-polynomial
sentence. The formula must include positivity, `u=1` scale normalization,
`u!=v`, three rationally parameterized unit directions, all K17S strict
containment bounds, exact host closure, bridge irredundancy and exact
nonintersection of every nonadjacent spine-segment pair. The latter may use
existential strict separating lines, which are equivalent for disjoint compact
segments.

SAT reopens K16W only after a separate exact verifier checks the original
geometric predicates. UNSAT closes K16B only if accompanied by a replayable,
independently checked exact certificate; a bare solver answer is solver
evidence, not a theorem. Unknown or the fixed resource stop retains the
freeze. No second variable ordering, larger budget, weakened simplicity
condition, extra edge or topology escalation is authorized. The symbolic
`gamma!=pi/2` family is the proposed follow-on, not part of this run.

## D-0149 (2026-07-22) — Fix the complete K16W decision sentence

K21Q serializes exactly one scale-normalized K16W formula. Tangent-half-angle
parameters cover the terminal first-quadrant direction and every admitted
bridge direction; the omitted bridge point `(-1,0)` is already the forbidden
reducible case. The formula contains 13 base constraints, 32 scalar strict
containment bounds, one exact host-closure equation and exact closed-segment
nonintersection for all 120 nonadjacent pairs among the 17 spine segments.
Strict interior containment separately keeps the spine off the two guard
edges.

The generated SMT-LIB formula is therefore equivalent to K16W's carrier
geometry, not a sufficient monotone or sampled subclass. The separate cold
verifier does not import the solver formulation: for rational solver models it
reconstructs the original coordinates over `Q(sqrt(2))`, checks all bounds and
closure, and recomputes the 120 segment intersections. Non-rational models are
rejected rather than approximated.

The session-134 experiment gate passes before the runner is written. The
single fixed run must be launched through `scripts/run_research.py`; D-0148's
claim boundaries remain controlling.

## D-0150 (2026-07-23) — K16W exact decision reaches the resource stop

The complete fixed K21Q formula ran in screen `k16w_hc27` from 23:04 on July
22 until host inspection at 08:31 on July 23. It consumed 9h26m33s of CPU and
emitted no SAT, UNSAT or `unknown` verdict. Z3 5.0.0.0 did not return control
at its requested eight-hour internal timeout, so the preregistered wall-clock
stop was enforced externally at 9h27m27s observed wall time.

This is a `resource_stop`, not a mathematical result. K16W remains open and
frozen; there is no model to cold-verify and no UNSAT certificate. D-0148
forbids a second ordering, enlarged budget, weakened simplicity condition or
rerun. The exact 386,654-byte SMT-LIB formula and a result manifest are
retained for audit.

Future native solver jobs with a wall-clock stop must be launched beneath an
external process supervisor. An internal solver timeout alone does not satisfy
the experiment stop rule. The next proposed branch remains the symbolic
non-right guard-angle family, requiring a new explicit authorization.

## D-0151 (2026-07-23) — Admit the symbolic non-right rhombic family

The user explicitly authorizes HC-28 after the K16W resource stop. The new
question changes one named hypothesis upstream of the closed square-lens
theorem N33: the guard angle is symbolic, with `0<gamma<pi` and
`gamma!=pi/2`. It does not rerun or relax K16W.

The topology is fixed before derivation. Retain K10B's equal-spoke 15-edge
centrally paired word, use equal guard legs and the corresponding rhombic
half-turn lens, and take the symmetric sharp-endpoint specialization
`theta=rho=(pi-gamma)/2`. The five fixed spine turns are therefore
`(pi+gamma)/2`. The first session must derive the complete exact containment,
closure and simplicity obligations and recover the N33 square system at
`gamma=pi/2` as an internal control.

HC-28 has exactly three terminal outcomes: an exact simple non-right carrier
witness, a scoped incompatibility theorem for the entire fixed family, or a
freeze at one explicitly named surviving obligation. Merely writing the
family is not success. No numerical angle sweep, QE/CAD/SMT run, topology
change, extra participant, SVG, placement-patch claim or candidate promotion
is authorized.

## D-0152 (2026-07-23) — Reduce the non-right family to one open interval

K23I applies exact rhombic-coordinate chord conditions to the three full
`d` spokes. Up to reflection, they can all fit only when
`pi/3<gamma<=pi/2`, with the global first-edge direction in the explicit
interval (8.7). Since HC-28 excludes the right angle already closed by N33,
only `pi/3<gamma<pi/2` survives.

This necessary reduction is not a family no-go. K23C gives one exact rational
angle, orientation and positive weight tuple whose six first-half vertices
all lie strictly inside the rhombus. Its host length exceeds the rhombus
diameter, so it is deliberately not a closure or candidate claim. The final
HC-28 obligation is now exact: decide whether complete containment anywhere
in the surviving interval can coexist with `h` below the rhombus diameter
and the central host equation. If neither a proof nor a complete simple
witness is obtained in session 137, freeze at that implication without a
search or solver run.

## D-0153 (2026-07-23) — Non-right closure exists; freeze at simplicity

K24C refutes the proposed containment-to-diameter obstruction by exact
construction. At the rational non-right angle
`(cos(gamma/2),sin(gamma/2))=(4/5,3/5)`, rational orientation
`z=(24+7i)/25`, weights `a=3/4`, `b=1/2`, and the explicit smaller quadratic
root (11.3), all twelve oblique coordinate pairs are strictly internal and
the central edge has length `h=a+b+c` exactly.

The control is not a carrier. N36 proves two nonadjacent spoke segments cross
transversely at the exact oblique point `(5/12,7/12)`. Therefore the
non-right angle genuinely escapes N33's containment/closure obstruction, but
no simple polygonal spine has been constructed.

HC-28's third terminal outcome fires at K24W: existence of a point satisfying
all 66 simplicity predicates in `pi/3<gamma<pi/2` remains open and frozen.
The three-session budget is exhausted. ERR-011 separately records and
discards one transient floating-angle diagnostic that violated the
checkpoint's method restriction; no theorem or exact control depends on it.
No polygon, placement patch, decoder, aperiodicity result or candidate is
claimed.

## D-0154 (2026-07-23) — Correct K23I and widen K24W

Independent audit found that K23I's acute-lens proof omitted a second
projective direction band. ERR-012 is controlling. The correct necessary
isolated-spoke interval is

```text
pi/3 < gamma < 2*pi/3.
```

The right angle remains separately closed by N33 for the unchanged square
topology, so the frozen simplicity obligation K24W now ranges over
`(pi/3,2*pi/3) minus {pi/2}`. Equation (8.7) parameterizes only the lower
branch. D-0152 and D-0153 remain historical records but their narrower
interval language is superseded here.

K23C, K24C and N36 survive unchanged: their exact guard angle lies in the
lower branch and their arithmetic has been independently recomputed. No
HC-29 theorem or experiment is admitted by this correction. Any future
decomposition or decision procedure must cover both non-right subintervals
from the outset.

## D-0155 (2026-07-23) — Admit HC-29 crossing analysis before any decision run

The user explicitly authorizes HC-29 after ERR-012 widens K24W. The first
question is theorem-only: derive the exact intersection parameters of the
two nonadjacent `d` spokes that cross in N36, then determine whether complete
rhombus containment forces those parameters into the open unit interval on
each of the lower and upper non-right guard-angle branches.

If this proves a family-wide crossing, K24W closes and no exact-decision run
is logically admissible. If a domain survives, a later HC-29 session may
preregister a decomposition by subinterval and crossing pattern before any
runner is written. Such a run must cover every surviving cell, use an
external wall-clock supervisor from launch, and retain the exact-verification
boundaries of D-0148. A monolithic fallback, missing branch, second ordering,
or post hoc budget increase is not authorized.

## D-0156 (2026-07-23) — Close K24W by a family-wide spoke crossing

K25X solves exactly the intersection of the two nonadjacent full-length
spokes already seen in N36. Their segment parameters are `u` and `1-u`, with

```text
u = b/(2*d*sin(gamma/2)).
```

On the corrected upper K23I branch, the rhombus diameter and strict interior
containment force `b<2*d*sin(gamma/2)`. On the lower branch, the corrected
orientation window (8.7) and one exact oblique-coordinate chord bound force
the same strict inequality. Thus `0<u<1` in both cases and the nonadjacent
spokes cross transversely. The interval endpoints violate K23I strict
containment; the same diameter argument also covers the right-angle point.

N37 therefore refutes K24W throughout its complete ERR-012 domain. HC-29
closes after one theorem session. D-0155's solver branch is not activated:
there is no surviving semialgebraic cell to decide, so no runner, solver or
artifact is written. This closes only the K22R/K22S equal-spoke rhombic
topology and does not close K16W or the wider monotile program.

## D-0157 (2026-07-23) — Admit HC-30 K16W crossing analysis

The user explicitly authorizes the independent-review recommendation for
HC-30. The primary question is theorem-only: apply K25X's exact line-
intersection method to the critical nonadjacent segment pairs of K16B's
fixed 19-edge unequal-spoke rectangle, retaining both bridge angles as
symbolic variables.

The admitted primary outcomes are either a scoped incompatibility theorem
closing K16W, or an exact finite semialgebraic decomposition of every
surviving crossing pattern suitable for a later, separately preregistered
decision. A partial angle calculation is not success. No solver, search,
sampling, coordinate fit, new edge, extra participant, SVG or candidate
promotion is authorized. The unequal-guard parallelogram transfer is
secondary: it may be assessed only after the K16W analysis reaches one of
the two terminal outcomes and only within the three-session HC-30 budget.

## D-0158 (2026-07-23) — Reduce K16W to one extreme aspect cone

K26X transfers K25X's line-intersection method to each fixed K16B
`v,w,u` hook. Simplicity forces `w>sqrt(2)*min(u,v)` for both `w=b,c`.
K26P sharpens the first-corner constraint to `v>u/sqrt(2)`. Together with
the strict host-chord diameter bound, N38 eliminates `v<u` and leaves only

```text
v/u>sqrt(23/2),   b,c>sqrt(2)*u.
```

In that cone, both long-spoke directions have equal-sign coordinates,
vertical square below `2/23`, and horizontal square above `21/23`. Thus four
explicit bridge-polarity cells remain. This is a strict family reduction,
not a K16W decision or witness.

## D-0159 (2026-07-23) — Partition the bridge-dependent long-spoke pair

K27X solves the intersection of K16B's two length-`v` spokes using only their
relative bridge phase `R=X+iY`. The exact closed intersection region is the
conjunction (5.5); its complement is the disjoint three-cell union C0--C2.
Together with K26X's complete treatment of both rigid-hook pairs, every
critical spoke-pair pattern is now assigned to at most twelve named
semialgebraic cells: one N38 aspect cone, four polarity choices and three
long-spoke safe cells.

This satisfies HC-30's admitted primary decomposition outcome but does not
decide K16W. The remaining 117 segment predicates, containment and closure
stay conjunctive. K16W therefore remains open/frozen; any future decision
must start from N38/K27X rather than rerunning the monolithic K21Q instance.
No solver or research artifact was produced.

## D-0160 (2026-07-23) — Unequal guard legs survive only conditionally

With HC-30's primary K16W decomposition complete, the final authorized
session assesses independent guard-lens lengths `e,f`. K28G gives the exact
parallelogram version of K22R/K22S: the relative spine and K25X intersection
formula are unchanged, while containment coordinates scale independently by
`e` and `f`.

K28T proves that N37 does not transfer. An exact non-right local control has
`(cos(gamma/2),sin(gamma/2))=(4/5,3/5)` and
`(d,b,e,f)=(1,2,10,11)`: all isolated spoke/code displacements fit strictly
in oblique coordinates, while `b>2d sin(gamma/2)` avoids the K25X crossing.
This is not a complete carrier witness.

The new lengths also create new intrinsic boundary roles and contact cover
tables. K28W therefore freezes the family upstream of coordinates: a full-
local-closure role/recognizability theorem is required before any solver,
angle sample, drawing or candidate claim. HC-30 is exhausted at three
theorem sessions with no artifact growth.

## D-0161 (2026-07-23) — Admit HC-31 theorem-first K16W cell elimination

The user explicitly authorizes the independent-review recommendation for
HC-31. Session 142 must first apply exact segment-intersection and span
arguments to the remaining K16W cells inside N38. No solver or runner is
admitted until that theorem session reaches either a family no-go or a fixed
surviving-cell list.

If cells survive, a later session may preregister one decomposed exact
decision whose complete cell list, formula options, outcome branches and
wall/memory stops are fixed before the runner is written. D-0150 external
supervision applies from launch. A monolithic fallback, added cell, alternate
ordering, relaxed predicate, second budget or post hoc escalation is not
authorized. K28W remains secondary and may be touched only after a terminal
K16W outcome and with checkpoint capacity remaining.

## D-0162 (2026-07-23) — Reduce K16W to two cells and preregister both

N39 proves that two same-polarity length-`v` spokes cannot fit inside the
N38 rectangle. Each spans horizontally more than
`sqrt(v^2-u^2)`, forcing the intervening `b,u` path to reset by more than its
strict host-derived length budget. K29O then shows that on either remaining
opposite-polarity cell, K27X's complete closed-intersection conjunction is
equivalent to the single sign `AY-BX<=0`. Simplicity is `AY-BX>0`.

Thus exactly two cells remain: `P_+-` and `P_-+`. Session 143 preregisters
those two complete K21Q subinstances, passes the experiment gate, and fixes
their order and resources before the runner is written: four internal and
externally supervised wall hours per cell, 96 GiB, one ordering, maximum
eight solver-hours. All 120 segment predicates remain. No monolithic
fallback, third cell, alternate ordering, weakened formula or budget
increase is authorized.

## D-0163 (2026-07-23) — Both HC-31 cells reach the external resource stop

The supervised `P_+-` and `P_-+` processes each run for exactly the fixed
four-hour wall budget and exit through GNU `timeout` with return code 124.
Neither returns SAT, UNSAT, `unknown` or a model.  Both 174-assertion formulas
and their SHA-256 values are preserved with one complete manifest tied to
code version `d30342f`.

This is a resource stop, not evidence for feasibility or infeasibility.
K16W remains open/frozen.  The two formulas may not be rerun with another
ordering, timeout or weakened predicate set.  HC-31 is exhausted at session
144 with 784,680 bytes of artifact growth.

## D-0164 (2026-07-23) — Admit theorem-only HC-32 conservative reduction

After reviewing the HC-31 duration, the user explicitly authorizes HC-32.
Its three-session budget contains no solver or coordinate search.  It must
adjudicate five conservative reductions: exact host-component budgets and
the `b,c` window; terminal-orientation elimination with actual
variable/degree accounting; a proof or no-go for a two-cell isometry; the
`lambda=1/v` boundary system including limiting self-contacts; and only then
an exhaustive strand-order decomposition if justified.

Every new ledger row must label its admitted form: either a necessary
condition proved from the complete K16W system, or an exact
bijection/equisatisfiable substitution.  Compactness alone does not license
ordinary interval subdivision as a complete decision method.  A later run
would require exact CAD/NLSAT certificates, a certified finite cover, or a
proved regularity condition such as an interval-Newton/Krawczyk criterion,
and belongs to a later checkpoint.

## D-0165 (2026-07-23) — Carry only conservative session-145 reductions

K30W proves the strict K16W window
`sqrt(2)<b,c<sqrt(2)/(sqrt(1-v^-2)-v^-1)`, whose endpoint decreases to
`sqrt(2)`.  K30B rewrites host closure as two exact component budgets plus a
unit direction, but is analytic only because serializing that direction adds
variables.

The proposed cheap cell quotient fails: N40 proves the intrinsic K16B cyclic
word has trivial dihedral automorphism group, with the anchored reflection
first mismatching `u` and `v`.  K30E gives the exact two-branch line--circle
elimination but rejects it computationally.  K21Q already uses one terminal
tangent variable; the radical form leaves the variable count at eight and
raises the cleared degree ceiling from 28 to 84.  HC-32 therefore carries
K30W/K30B into compactification, retains both cells, and does not rewrite or
run the formula.

## D-0166 (2026-07-23) — Replace asymptotic blow-up by an explicit bound

N41 proves the `P_-+` cell empty: its westward first length-`v` spoke forces
the prefix endpoint beyond `sqrt(v^2-1)`, while host diameter and
`b,c>sqrt(2)` put the complete prefix norm strictly below that value.

For `P_+-`, K31C applies the same endpoint margin
`delta=v-sqrt(v^2-1)` at both long spokes.  It bounds `a` from the first
prefix, bounds `p_8` after the second spoke, and combines that with the host
component budget.  Every surviving point has
`sqrt(23/2)<v<V_*<13`, `a<3/2`, and `b,c<98/43`.

This is stronger than the planned `lambda=1/v` analysis and blocks limiting
self-contact at infinity by strict finite inequalities.  It compactifies the
weights but does not close the open boundary strata or prove interval
subdivision complete.  No formula or solver run is authorized.

## D-0167 (2026-07-23) — Close HC-32 with a 16-cell bounded exact atlas

K32S uses the fixed symmetry line, central half-turn and the positive K27X
hook offset to prove `y_C>y_B`.  The five long-strand heights therefore have
exactly four possible strict central-symmetric orders.  This is an exhaustive
partition, not a selected isotopy class.

K32A replaces each unbounded bridge tangent parameter by two bounded
semicircle charts.  The four chart pairs are an exact cover of both bridge
directions and preserve variable count and degree.  K32R separately partitions
closure into negative-discriminant, tangent and transverse strata; it names
where interval Newton may apply but does not claim interval completeness.

Together with N41/K31C, the one surviving K16W obligation has an exact cover
by 16 bounded cells, each retaining all original predicates.  HC-32 is
exhausted at three theorem sessions with no artifact growth or solver run.
A later decision requires separate authorization and an exact certificate
contract for all cells and boundary strata.

## D-0168 (2026-07-23) — Admit HC-33 theorem-first all-cell decision

After independent verification of HC-32, the user explicitly authorizes
HC-33.  The first session must derive exact inequalities for each of K32S's
four strand orders across all four K32A bridge-chart pairs and attempt
theorem-level eliminations.  A cell may be removed only by a proved necessary
condition from complete K16W or by an exact equivalence recorded in the proof
ledger.

Only cells that survive that pass may enter a serialized decision package.
Before any solver launch, the package must retain closure, all 32 containment
bounds and all 120 nonadjacent-pair predicates; cold construction tests must
establish equivalence to the admitted cells; and a notebook preregistration
must pass `scripts/check_experiment_gate.py`.  D-0150 external supervision
applies.  Negative-discriminant, tangent and transverse closure strata and
all strict-boundary cases must receive explicit exact dispositions.  No
dropped predicate, chosen strand order, heuristic angle/coordinate sample,
alternate ordering, timeout increase, polygon, SVG or candidate promotion is
authorized.

## D-0169 (2026-07-23) — Refute K16W by the thin-lens reset theorem

N42 observes that the central H strand must point either west with C or east
with C'.  In either case two same-polarity segments of horizontal spans above
`sqrt(v^2-1)` and `sqrt(h^2-1)` are separated by exactly the `c,1` path.
Open-strip containment forces that path to have length above
`sqrt(h^2-1)-delta(v)`.

K30W/K31C give the opposite exact budget:
`sqrt(h^2-1)>10/3`, while
`c+1+delta(v)<13/6+1+1/6=10/3`.  Thus every one of the sixteen K32S/K32A
cells is empty.  K16W is closed/refuted for the fixed K16B 19-edge topology.
No HC-33 formula or solver run is activated, and the prior resource stops
remain resource stops rather than computational evidence.

This is not a general monotile, guard-and-shield or unequal-leg no-go.
Reopening requires changing a named topological or thin-lens hypothesis, not
increasing a solver budget.

## D-0170 (2026-07-23) — Supersede D-0169; retain only H-east

ERR-013 identifies a directed-edge error in D-0169.  Central pairing preserves
the traversed C and B vectors because its half-turn and reversed indexing
contribute two sign changes.  C' is westward, not eastward, so the short
`p_9`--`p_11` path does not reset between terminal and initial endpoints of
two eastward segments.  The H-east half of the claimed contradiction is
invalid.

The H-west branch and every radical comparison survive.  They prove the
corrected N42: complete K16W forces `v-2*p_(8,x)>0`, so H points east and the
five long strands are traversed `E,W,E,W,E`.  K16W is open/frozen, all sixteen
K32S/K32A cells remain, and D-0168's theorem-first HC-33 authorization resumes
with this exact sign added.  No formula or solver is launched by this repair.

## D-0171 (2026-07-23) — Close HC-33 with six corrected K16W cells

K33M combines the N39 connector margin, corrected N42 and K31C budgets to
prove that none of the six short spine subpaths touches `x=v/2`.  The five
long strands are therefore the complete ordered crossing list.  N43 applies
Jordan separation to this exact list and refutes K32S order S4: its B--C and
H--C' right-half-plane arcs have alternating boundary endpoints.

Independently, K33C rewrites the first bridge as
`z_1=conj(Z*q)*r_b`.  The first-quadrant frame and N38 component bounds force
`Re(z_1)<0`, so K32A's two positive-first chart pairs are empty.  The exact
remaining cover has three strand orders times two chart pairs, or six cells.

Every original closure, containment and nonintersection predicate remains.
HC-33 is exhausted at session 150 without a formula or solver.  A later
decision requires new authorization, serialization and cold equivalence
tests for exactly these six cells, a passing experiment gate and D-0150
external supervision.

## D-0172 (2026-07-23) — Admit HC-34 fixed six-cell decision

The user explicitly authorizes HC-34 after the corrected HC-33 disposition.
The instance list is fixed before implementation:

```text
S1--, S1-+, S2--, S2-+, S3--, S3-+,
```

where the first bridge sign is K33C's forced negative sign and the final sign
is the second bridge chart.  Session 151 must preregister, serialize and
cold-check those exact cells before launch.  Each formula retains complete
K21Q, N38/K29O, N41/K31C, corrected N42, its full K32S signs, K32A's bounded
charts and all 120 pair predicates.

If validation passes, run two printed batches of three cells.  Each cell gets
one Z3 5.0 QF_NRA ordering, a three-hour internal timeout, an independent
external 10,800-second supervisor with 60-second kill grace, and a 32-GiB
process memory parameter.  Maximum solver work is eighteen cell-hours and
maximum elapsed solver time is six hours.  No alternate ordering, additional
cell, weakened predicate, sequential fallback, timeout increase or post hoc
escalation is authorized.  SAT requires exact cold model verification; bare
UNSAT is solver evidence only; resource stop/unknown/unverifiable output
leaves the named cell open.

## D-0173 (2026-07-23) — Freeze the six HC-34 formulas before launch

The experiment gate passes before implementation.  From stable revision
`a984181`, the cold serializer writes exactly the six D-0172 cells.  Every
formula has 187 top-level assertions: 13 base constraints, 32 containment
bounds, one closure equation, all 120 nonadjacent-pair predicates and 21
admitted theorem/chart/strand constraints.

The manifest fixes cell order, SHA-256, byte size, constraint counts and code
version.  Regression tests recompute all of them independently.  The rational
model verifier separately reconstructs the selected charts and strand signs
before checking the original geometry.  The formulas are now immutable for
the HC-34 launch; any drift, reordering or missing manifest record aborts the
runner rather than regenerating a different instance.

## D-0174 (2026-07-23) — Record the failed HC-34 launch; forbid silent retry

The first fixed-batch launch passed the research gate, then failed before a
solver verdict.  The single-cell runner rebuilt a semantically identical Z3
formula and compared its generated SMT-LIB text byte-for-byte with the frozen
file.  Z3's internal `let` identifiers depend on construction history, so two
cells correctly aborted on textual drift even though no mathematical
constraint had changed.  The first cell matched by construction order and
entered `check()`, but the enclosing screen process died immediately; no
solver or supervisor process survived and no result file was written.

This is a launch-wrapper failure, not SAT, UNSAT, `unknown`, or mathematical
evidence.  The six formulas and their hashes remain exactly those frozen by
D-0173.  The runner is repaired to authenticate the manifest path, byte count
and SHA-256, parse those frozen bytes directly, verify 187 assertions, and
only then attach the pre-registered resource parameters.  It no longer
reconstructs a formula at launch.

D-0172's stop rule explicitly says a killed process leaves its cell open and
does not authorize a rerun.  Therefore HC-34 closes as a failed launch with
all six cells open.  A retry requires a new explicit human checkpoint that
names the same six immutable formulas and resources; neither this repair nor
the unused HC-34 session allowance silently grants it.

## D-0175 (2026-07-24) — Admit HC-35 as the first effective six-cell run

After independent review of corrected HC-33 and failed HC-34, the user
explicitly authorizes one HC-35 run of the same six D-0173 files.  This does
not waive the prior stop rule retroactively: it is a new checkpoint decision,
made after disclosure that zero solver evidence existed.  Formula hashes,
cell order, two batches, Z3 ordering, three-hour internal and external limits,
60-second kill grace, 32-GiB per-cell parameter and all claim boundaries are
unchanged.

The launch must be fail-isolated.  The research supervisor runs as a
host-native transient user service rather than as a child of screen.  Every
cell process starts a new session, so a cell exception cannot signal siblings.
Screen runs independently and is only a viewport on append-only logs; losing
it cannot terminate the supervisor or cells.

The prior screen death is classified as an infrastructure-lifecycle failure,
not a batch exception cascade.  The managed command returned while the screen
daemon and its still-running solver were descendants of that launch scope;
all were reaped, while the two pre-solver exceptions merely returned nonzero
inside a parent that was coded to wait for every sibling.  No screen exit
status survived, so the exact signal is unavailable.  A harmless transient
user-service probe persisted and exited successfully, validating the
replacement ownership boundary before research launch.

## D-0176 (2026-07-24) — Supersede D-0174/D-0175; HC-34 is still live

ERR-014 corrects the process-visibility premise.  Host-level `screen` and
process inspection finds the original HC-34 supervisor and S1-- solver alive
under the original external timeout.  The sandbox had reported only that it
could not see the host process; it did not establish process death.

HC-35 is therefore cancelled before launch.  Its preregistration, tested
fail-isolated runner and transient-service probe remain infrastructure, not
research evidence.  No HC-35 solver unit, screen viewport or result manifest
was started.

The original HC-34 process is left undisturbed.  Its two textual-drift
failures remain failures and are not retried.  When S1-- finishes, the same
supervisor may launch its pre-registered second batch.  Those children will
consume the D-0173 frozen bytes through the repaired loader; no formula,
ordering, cell, timeout or memory parameter changes.  Final disposition waits
for that original supervisor.  Any work after its manifest is known requires
a new human decision based on the actual per-cell outcomes.

## D-0177 (2026-07-24) — Close HC-34/HC-35 with no solver verdict

The original HC-34 supervisor completed at 05:55:22 Europe/Madrid.  Cold
manifest replay authenticates all six D-0173 formula hashes, cell order,
187-assertion counts, batch membership, result links and null models.

The exact disposition is:

```text
S1--  resource_stop       S1-+  no_result
S2--  no_result           S2-+  resource_stop
S3--  resource_stop       S3-+  resource_stop
```

Every resource stop has external return code 124 after the fixed 10,800
seconds.  The two `no_result` cells have return code 1 and preserved
pre-solver formula-drift exceptions.  ERR-015 clarifies that their displayed
10,800-second elapsed values are batch recording time, not solver time.

There is no SAT, UNSAT, `unknown`, model, exact witness or replayable
infeasibility certificate.  K16W and all six cells remain open/frozen.  The
run shows that the current single Z3/NLSAT ordering does not decide even the
theorem-bounded cells at this budget; it supplies no geometric evidence.
No cell may be rerun, reordered or given a larger budget under HC-34/35.

HC-35 was cancelled before launch and contributes no solver output.  Sessions
153--155 exhaust its checkpoint allowance.  Further K16W work requires a new
human checkpoint and a method change justified against these resource stops,
not another timeout extension.

## D-0178 (2026-07-24) — Admit HC-36 exact discriminant theory

After independent review of the HC-34/35 closure and the certificate boundary
of alternative real-algebraic solvers, the user explicitly authorizes one
three-session theorem-only checkpoint.  HC-36 must analyze K32R's exact
closure discriminant before any new decision procedure is considered:

1. split every surviving K16W cell into `Delta=0` and `Delta>0` strata;
2. on `Delta=0`, either derive a simplicity obstruction or an exact
   lower-dimensional presentation;
3. on `Delta>0`, test whether first-quadrant terminal orientation and N42's
   eastward host select one of the two closure roots; and
4. apply K25X-style chord/intersection identities inside the retained strand
   cells.

No solver, CAS, floating-point reconnaissance, experiment runner, coordinate
search, polygon, SVG or candidate promotion is authorized.  A successful
reduction must be measured, not described impressionistically: the proof
ledger must record a strict decrease in continuous variables, closure roots,
live cells or cleared polynomial degree, together with its admitted form
(necessary implication or exact equivalence).  If neither an exact cell
elimination nor such a quantified reduction is proved by session 158, the
checkpoint stops and K16W remains frozen.  A solver pivot or another carrier
family requires a new human decision.

## D-0179 (2026-07-24) — Reduce the K16W tangent stratum exactly

K35D identifies K32R's radical sign with the side of the rectangle diagonal
containing `p_8`.  On `Delta=0`, corrected N42 selects the internal tangency:
`p_8=lambda*(v,1)` with `0<lambda<1/2`, and the central host is the remaining
diagonal segment.  K35T reconstructs the unique terminal direction by
`(C,S)=(A/T,B/T)` and its tangent chart by `t_0=B/(T+A)`.

Substituting these identities while retaining every K34Q predicate gives an
exact tangent presentation with seven rather than eight solver real variables
(six rather than seven geometric variables, plus the fixed `sqrt_half`
auxiliary).  This is HC-36's first measured success.  No degree reduction or
tangent-cell emptiness is claimed.

K35F separately proves that closure, first-quadrant terminal pose, strict
`p_8` containment and H-east alone can admit both transverse roots.  Therefore
any root elimination in the remaining sessions must consume a genuine strand
or nonintersection predicate; treating the cheap filters as a selector is
forbidden.

## D-0180 (2026-07-24) — Reduce transverse root selection to exact strand signs

K36W rotates the two transverse closure roots into the fixed relative spine
frame.  K36M then rewrites each B/C midline-order test as the sign of
`F_j-epsilon*sqrt(Delta)*Q_j`; no endpoint or strand predicate is dropped.
The conjugate product

```text
F_j^2-Delta*Q_j^2
```

is therefore an exact root selector: if it is negative throughout a complete
cell, that strand's required K32S sign retains at most one of the two closure
roots.  No such uniform cell sign is proved in session 157, so the conditional
`2 -> <=1` count is not booked as an HC-36 reduction and all six transverse
cells remain two-root obligations.  Evaluated points, sampled angles or a
replacement of the full simplicity table by this condition remain forbidden.

## D-0181 (2026-07-24) — Close HC-36 with tangent reduction only

K37O orders the two transverse terminal directions counterclockwise.  K37Q
proves `Q_B>0>Q_C`, so K36M's B and C strand tests can only move from below H
to above H as the radical sign changes from minus to plus.  If both roots are
complete, K37S reduces their abstract ordered strand-cell transitions from
nine to six.

This transition-table reduction is not one of HC-36's admitted complexity
metrics: it removes no live K34Q cell or closure root and lowers no variable or
degree count.  Neither conjugate selector product is proved negative on a
complete cell.  Therefore the only booked HC-36 success is K35T's exact
tangent presentation:

```text
solver variables 8 -> 7; geometric variables 7 -> 6.
```

All six cells and both transverse roots remain open; no tangent cell is proved
empty.  Sessions 156--158 exhaust HC-36.  No result licenses a solver run,
timeout increase, predicate deletion, polygon or candidate claim.  A certified
stratified decision, another named-pair theorem, or a carrier pivot requires a
new human checkpoint.

## D-0182 (2026-07-24) — Admit HC-37 selector-polynomial theory

Following independent verification of every HC-36 identity, the user directs
the work to continue.  HC-37 takes the review's first recommendation: attack
K36P's two named polynomials

```text
P_B=F_B^2-Delta*Q_B^2,
P_C=F_C^2-Delta*Q_C^2
```

with the cell-specific information not consumed by HC-36, especially
K33C's `sigma_1=-1` and the two exact `sigma_2` bridge charts.  The admitted
outcomes are a uniform negative selector on a complete cell, an exact
cell/root elimination, or a strict decrease in continuous variables or
cleared polynomial degree.  Every result must keep its implication/equivalence
form explicit in the proof ledger.

Sessions 159--161 are theorem-only.  No solver, CAS, floating-point
reconnaissance, experiment runner, coordinate search, polygon, SVG or
candidate promotion is authorized.  A conditional selector, evaluated point,
heuristic sign or smaller unmeasured region does not satisfy the stop.  If no
admitted count decreases by session 161, the thin-lens carrier freezes and a
new human decision chooses between a separately preregistered tangent
cvc5/CAD attempt and a carrier pivot.

## D-0183 (2026-07-24) — Put the selector in line--chord normal form

K38N factors each K36P polynomial as

```text
P_j=|w_8|^2*((T-2*n_j*m_j)^2
             -Q_j^2*(d^2-4*m_j^2)).
```

This is the exact condition that K36W's two-center root chord crosses the
named B or C supporting line.  The reformulation changes no admitted count.

For B, K38B expands the line offset throughout K33C's fixed left-semicircle
chart.  Except on the slice `a=sqrt(2)`, its sign changes within that one
chart; therefore `sigma_1=-1` alone cannot force the selector.  This is a
scoped shortcut obstruction, not a counterexample to complete K16W and not a
claim that `P_B` changes sign inside a live strand cell.  Session 160 must add
the complete cell constraints and the second bridge chart; no sampled point
or chart-only argument counts as HC-37 progress.

## D-0184 (2026-07-24) — Narrow, but do not promote, selector attacks

K39C expresses the C support-line offset as `dot(z_2,U)`.  Each fixed second
bridge semicircle contains both offset signs whenever `U_y` is nonzero; in the
exceptional `U_y=0` slice, the vertical seams have zero offset.  Therefore the
second chart sign alone no more forces `P_C` than the first chart forces
`P_B`.

K39O combines the exact root order with the complete S1--S3 signs.  Six of
twelve root-labelled strand attacks have selector product strictly positive;
only

```text
S1+: B,C;  S2-: B,C;  S3-: B;  S3+: C
```

can still be negative.  This `12 -> 6` bookkeeping reduction removes no live
root or cell and is not booked under D-0182's success rule.  Session 161 gets
one final theorem attempt on those six expressions and the S3 sum; absent an
admitted count reduction, the thin-lens carrier freezes.

## D-0185 (2026-07-24) — Freeze the thin-lens selector route

K40E shows that K39O's six residual attacks are exactly the three possible
same-cell conjugate-root transitions `S1->S1`, `S2->S2`, and `S3->S3`.
K40H derives a separate affine-radical expression for S3's sum sign and the
radical-free conjugate selector `H_0^2-Delta*H_1^2`.

No complete cell forces any of `P_B`, `P_C`, or the S3 sum selector negative.
Consequently HC-37 reduces only auxiliary bookkeeping (`12 -> 6 -> 3`), not
an admitted metric:

```text
variables unchanged; degree unchanged; six cells; two transverse roots.
```

The predeclared stop fires after sessions 159--161.  Further algebraic
refinement of the same thin-lens selectors is frozen.  No solver run, timeout
increase, polygon or candidate is authorized.  Reopening requires a new human
decision for either a separately preregistered certified decision of K35T's
seven-variable tangent stratum or a pivot to a different carrier geometry.
