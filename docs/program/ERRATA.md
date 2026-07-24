# Errata and clarifications to the program document

The program document (`einstein_search_program.md`) is kept verbatim as the
specification. Factual errors found while implementing are recorded here,
with sources. Append-only.

## ERR-001 (2026-07-15) — "The hat being a 13-polykite" (§3.3)

The hat is an **8-kite** polykite on the Laves [3.4.6.4] grid; **13 is its
number of sides** (a tridecagon), not its cell count. Confirmed against the
SMKG paper ("An aperiodic monotile", arXiv:2303.10798) and verified
computationally in this repo: Kaplan's published hat outline contains exactly
8 kite cells (`tests/test_hat.py`). The document's later uses of polykite
horizons (§8 E1 "polykites n ≤ 16", E2 "n ≈ 22–24") are unaffected and remain
sensible budgets.

## ERR-002 (2026-07-17) — Independent disk covers are not patch growth (§4 A3)

The implementation initially treated a SAT cover of each larger disk as
evidence that a candidate "grew." That is weaker than the program's intended
frontier extension: independently solved disks may use incompatible interior
phases and sacrificial boundary crowns that cannot continue.

A3 evidence must therefore be nested. Exact placements from a smaller patch
are frozen inside a protected core while a larger region is solved. The
reported feature is the largest preserved core (and the discarded collar
depth), not merely the largest independently coverable circle. A complete
finite crown being non-extendable does not refute the tile; it refutes that
particular finite patch as a fragment of an infinite tiling.

## ERR-003 (2026-07-20) — The n=10 “finalist” is the known Turtle (§8 E1)

The shape historically promoted as “n=10 candidate 2” or the “E1 finalist,”
with compiled key
`010001010104010502f002f1030b030c04fa04fb`, is **exactly the Turtle** of
Smith--Myers--Kaplan--Goodman-Strauss, up to the canonical translation and
dihedral normalization already used by the enumerator. It is not a new shape.

This was checked without visual judgement. The primary paper's exact
`rawtileB` outline (arXiv:2303.10798 source, `00_macros.tex`) contains ten kite
cells; applying this repository's `cells_in_polygon` and `canonical_form`
produces the finalist key byte-for-byte. The identity is pinned by
`tests/test_turtle.py` and registered in `src/einstein/e1_candidates.py`.

The error was in promotion-time known-shape deduplication, not enumeration or
certificate verification. E1's specification explicitly expected the blind
funnel to surface both Hat and Turtle. The disk, diffraction, transfer,
cokernel, holonomy, and packing artifacts remain valid finite computations,
but their subject is now a **known aperiodic Turtle control**. Legacy filenames
containing `finalist` are retained for reproducibility and must be read as
aliases for Turtle.

Tilability and nonperiodicity are already established externally. In
particular, arXiv:2403.01911 gives a recursive Bricks-and-Mortar construction
and an Ammann-bar contradiction: periodicity would force rational `k/n` to
satisfy `q(1-q)=1/5`, hence `q=(5±sqrt(5))/10`. Internal W1--W3 work may seek
independent finite certificates for those known facts, but it is no longer a
proof obligation for a new-einstein claim. Novelty promotion must henceforth
classify every canonical key against the registered known-polykite anchors
before assigning candidate status.

## ERR-004 (2026-07-20) — E2 is not beyond the known polykite horizon (§8)

The program calls E2's `n≈22--24` polykite sweep “beyond the known horizon.”
That is false. Smith--Myers--Kaplan--Goodman-Strauss, *An aperiodic
monotile*, Section 6, explicitly report an exhaustive computer search with no
aperiodic `n`-kites other than Hat and Turtle for **`n≤24`**. This supersedes
ERR-001's statement that the original E2 horizon remained sensible.

The same section completely classifies the positive `Tile(a,b)` continuum:
every positive unequal pair is aperiodic and combinatorially equivalent to
Hat tilings; the three exceptional similarity classes `a=0`, `b=0`, and
`a=b` admit periodic tilings. It also identifies infinitely many polykites in
that continuum, namely `Tile(1,k√3)` and `Tile(k√3,1)` for every positive odd
integer `k`. Therefore named Hat/Turtle key comparison alone is not a
complete prior-art check even above `n=24`.

Appendix A also proves the periodic-alignment reduction the theory plan had
assigned to W4: if a polykite admits a periodic tiling under arbitrary
Euclidean placements, it admits a grid-aligned periodic tiling (Lemmas A.1,
A.3, A.5). Lemma A.6 proves the stronger statement that every Hat tiling is
aligned. W4 may still investigate stronger all-tilings rigidity or other
substrates, but it is not a missing bridge for polykite periodicity.

Consequences:

- E1 remains a validation experiment; none of its `n≤16` shapes can be a new
  aperiodic polykite under the published classification.
- E2, as frozen, is invalidated before launch and must be redesigned. Merely
  moving to `n=25` is not an adequate research justification: Kaplan's 2025
  review reports a later search of roughly 500 billion polykites with no
  other unusual behavior.
- New-polykite promotion is fail-closed pending both the finite-horizon check
  and recognition of the infinite polykite part of `Tile(a,b)`.

The controlling claim matrix and source tiers are recorded in
`docs/literature/POLYKITE_BASELINE.md`.

## ERR-005 (2026-07-21) — The A2 `n<=8` Heesch census is a reproduction

Session 03 stated that polykite Heesch numbers appeared uncharted and called
the six `H_c=2` cases through eight kites possibly novel. That prior-art claim
is withdrawn.

Kaplan's public `heesch-sat` implementation explicitly supports the polykite
grid. In an August 2023 comment on his official project page, he stated that
he had computed Heesch numbers of non-tiling polykites through roughly 16 or
17 cells. He also published a 116-page eight-kite artifact containing every
non-tiling 8-kite with positive Heesch number and three inconclusive cases.
Its aggregate counts are 108 with `H_c=1`, five with `H_c=2`, and three
inconclusive. Kaplan identifies the latter as two periodic anisohedral shapes
and the Hat. These numbers exactly match our A1+A2 partition.

The A2 implementation remains independent: it uses recursive exact-cover DFS
and cold-verifiable nested-corona certificates rather than Kaplan's monolithic
SAT encoding. Its result is therefore a useful exact reproduction and
pipeline benchmark, but not new census data. The source/algorithm crosswalk
and evidence tiers are recorded in
`docs/literature/reviews/KAPLAN_HEESCH_POLYKITES.md`.

Session 58 subsequently derived the exact coordinate conversion and verified
a 116/116 per-shape bijection, including identical individual `H_c` values and
the three inconclusive identities. This strengthens the reproduction claim;
it does not restore any novelty claim.

## ERR-006 (2026-07-21) — The ST-M1 38-address source was misread

Sessions 65--66 claimed that the optimized `sqrt(2)-1` construction in
Akiyama--Hamada--Ito had two connected large templates of composition
`2S+L`, hence `18,18,2` common-triangle addresses. That claim is withdrawn.

The primary TeX distinguishes two constructions with the same slope. The
general construction in Section 9 has Type I composition `2S+L` and 26
possible large patch-tiles. The optimized three-prototile construction in
Section 10.1 instead has two Type I patch-tiles of composition
`12S+6M+6L`, plus one Type II `M`; this is stated explicitly in Table 1. The
six attached `M` cells in each connected large prototile were omitted when
the repository inferred `18,18,2` from the visible `2S+L` ratio.

More importantly, the later statement that cell supports can coincide at
`kappa=infinity` occurs in the separate Smith Turtle subsection. The source
does not apply that specialization to the optimized Section 10.1 system, give
a common-cell subdivision for its `12S+6M+6L` templates, or prove equivalence
of the resulting complete local languages. Replacing 38 by another guessed
integer would therefore not repair the proof.

Consequences:

- ST-M1.E-infinity and the instantiated ST-M1.S0 return to **blocked**;
- the conditional common-cell compiler ST-M1.S0C remains valid;
- the quotient criterion Q0 and the role-only/independent-rail no-go results
  N2/N1 remain valid as conditional symbolic statements;
- no raw addressed alphabet, collar/port table, or all-`M` exclusion has been
  established for the optimized system;
- the radius-one table authorized in D-0075 is halted before enumeration.

The affected historical notebooks are retained with correction notices. The
stable theory notes and proof ledger use this erratum as the controlling
status.

Session 69 subsequently resolved the geometry without undoing this erratum:
the centroid formulas give `30,30,2` common-triangle addresses after splitting
the six embedded `M` rhombi in each large template and the small `M` rhombus.
This is ST-M1.G0. Complete SAB/vertex-language transport remains open as L0,
so the withdrawn `18,18,2` proof and S0 closure remain withdrawn.

## ERR-007 (2026-07-22) — K7C settles the host footprint, not the whole strip

Theory note 22 originally claimed that K7C made the three neighbor interiors
in the entire strip `-d<y<0` exactly the three rectangles below the host.
That is false at the reflex endpoint of role `A`. With its code side directed
along positive `x`, interior below, and `ell_A=3*pi/2`, the `A` occurrence
contains a third-quadrant germ (`x<0,y<0`) outside the host footprint.

K7C proves exactly what the tail reduction needs: inside
`(0,L) x (-d,0)`, the open footprint below the host, the three interiors are
the disjoint rectangles below their code intervals. The reflex spillover is
part of the rooted tail `Q_A` and must be included in the tail-pair and
host-versus-tail intersection checks. References to the “complete strip” are
withdrawn and replaced by “host-footprint collar.”

At the same endpoint, if exactly the host and `A` occur and the neighborhood
is gaplessly covered, angle sum forces the host interior angle to be
`2*pi-3*pi/2=pi/2`. Any future K7W witness either has that right-angle host
corner or explicitly admits another participant there. K7A's selector and
K7C's stem equalities are otherwise unchanged.

## ERR-008 (2026-07-22) — Half-turn spine copies have complementary angles

Session 113's K10B role audit said that the paired copies of each `A,B,C`
length on the centrally symmetric shield spine were “the same role under
reversal.” That is false for the polygonal contact geometry being proposed.

If a carrier and its half-turn share the complete spine with disjoint
interiors, then at every paired spine vertex `p,-p` their two interior angles
sum to `2*pi`. Hence a convex intended code endpoint of angle `alpha` is
paired with a reflex auxiliary endpoint of angle `2*pi-alpha`, not another
copy of the same directed endpoint type. Length reflection alone therefore
does not recognize `A,B,C`.

Consequences:

- K10B's conditional half-turn docking lemma remains valid;
- the three mirror sides are auxiliary same-length sides, not declared code
  roles;
- intended code roles require length **and** convex endpoint context;
- the reflex copies cannot occupy an intended internal host junction because
  the host already contributes `pi` and their angle exceeds `pi`; and
- every future contact-completeness proof must nevertheless exclude other
  uses of those same-length auxiliary sides.

No coordinate or polygon claim depended on the incorrect role sentence.
The session-114 stop fires before the skeleton is promoted.

## ERR-009 (2026-07-22) — N26 does not apply at terminal spine vertices

ERR-008 and the original N26 proof correctly derive complementary carrier
angles at every **nonterminal** vertex of the shared K10B spine, where the two
half-turn occurrences locally fill a disk. They then incorrectly apply that
identity to both endpoints of all three paired code sides.

The `A` sides are the first and last edges of the spine. At their terminal
vertices `R,Q`, the two occurrences fill only the corner of the right-angle
guard lens. With `R=(-d/sqrt(2),0)` and
`Gamma=(0,d/sqrt(2))`, the vectors from `R` to `Gamma` and `-Gamma` are
perpendicular, so the paired terminal carrier angles sum to `pi/2`, not
`2*pi`. The internal endpoint of each paired `A` side still satisfies N26.
Both endpoints of `B,C` are nonterminal and still satisfy N26.

Consequences:

- K10B's half-turn docking and K11S's general atomic-root theorem survive;
- paired `B,C` sides are reflex at both endpoints when their intended mates
  are convex;
- paired `A` has one reflex internal endpoint and one convex terminal
  lens-corner endpoint, so it cannot be treated as a two-reflex atomic root;
- N27 remains valid endpoint by endpoint, but does not by itself settle the
  terminal `A` context; and
- K10B must be tested against K11S using complete root-cover data rather than
  the discarded shortest-reflex-side shortcut.

No polygon, coordinate or tiling claim had been promoted. The error was found
while applying the synchronization theorem, before any coordinate work.

## ERR-010 (2026-07-22) — K20L's printed hook direction was not a unit vector

Theory note 32 §10 and session 133 originally asserted that
`(120/121,11/121)` was a unit vector because
`120^2+11^2=121^2`.  This is false:

```text
120^2+11^2=14521,       121^2=14641.
```

The defect is material to that printed control.  Normalizing the vector
increases its horizontal span past the rectangle width, so equations
(10.1)--(10.4) in their original form do not prove K18H.  The session-133
verification line claiming the false Pythagorean identity is withdrawn.

K20L itself survives with the exact replacement

```text
r=(544/545,33/545),       544^2+33^2=545^2.
```

For `(u,v,w)=(1,2,1/10)`, the corrected hook has horizontal order

```text
0 < Re(s_2) < Re(s_3) < Re(s_1)=1088/545 < 2
```

and vertical span `544/545<1`.  The close comparison
`Re(s_3)<Re(s_1)` is `330*sqrt(2)<577`, whose squared form is
`217800<332929`.  Thus the corrected direction proves the same isolated
K18H control for `b=c=1/10`.

Consequences:

- K20L's separation conclusion survives with corrected exact data;
- K18H, K19P, K19E and the HC-26 freeze are unchanged;
- no downstream theorem, polygon or candidate depended on the invalid vector;
  and
- the original equations and verification statement must not be cited.

## ERR-011 (2026-07-23) — HC-28 used one forbidden transient angle diagnostic

HC-28 was explicitly authorized as theorem-first with no numerical angle
sweep. During session 137, while testing whether a proposed analytic lower
bound could hold, a transient read-only Python diagnostic evaluated that
lower-bound expression at a small table of floating-point angle pairs. This
was outside D-0151's admitted method even though it created no file, runner,
certificate or governed artifact.

The diagnostic output is discarded and is not evidence for any ledger row.
K23I predates it and is an exact symbolic interval proof. K24C and N36 are
rederived independently from the single exact rational choice
`cos(gamma/2)=4/5`, `sin(gamma/2)=3/5`, using rational arithmetic and one
explicit quadratic root. Their statements and verifications do not cite or
depend on the sampled table.

Consequences:

- no empirical claim about the family is permitted;
- HC-28 consumes its final session and closes immediately at K24W;
- no further angle, orientation or coordinate exploration is authorized; and
- any future family decision must receive a new checkpoint and, if
  computational, pass the experiment gate before implementation.

## ERR-012 (2026-07-23) — K23I omitted the acute-lens direction band

Theory note 33 §8 originally asserted that, when
`phi=pi-gamma<pi/2`, the isolated unit-spoke conditions `|r|<1,|s|<1`
confine the projective direction to `(0,phi)`. This is false. Solving both
sine inequalities in (8.8) gives

```text
(0,phi) union (pi-phi,2*phi).
```

The second band is nonempty exactly for `phi>pi/3`. An exact control is
`gamma=3*pi/5`, `phi=2*pi/5`: the three required projective directions can be
taken as `pi/10,3*pi/10,7*pi/10`, and every oblique coefficient has absolute
value either `sin(pi/10)/sin(2*pi/5)` or
`sin(3*pi/10)/sin(2*pi/5)`, both strictly below one.

Consequently the correct necessary isolated-spoke interval is

```text
pi/3 < gamma < 2*pi/3,
```

not `pi/3<gamma<pi/2`. The orientation window (8.7) remains correct only on
the lower branch `pi/3<gamma<pi/2`.

Consequences:

- K23I is replaced by its corrected two-branch statement;
- ERR-011's description of the pre-existing K23I interval proof as exact is
  itself superseded here; ERR-011's process correction remains valid;
- K24W is widened to
  `(pi/3,2*pi/3) minus {pi/2}`;
- D-0152 and D-0153's narrower interval statements are superseded by
  D-0154;
- sessions 136--137 and STATUS carry explicit correction notices;
- K23C, K24C and N36 are unchanged because their exact angle lies in the
  lower branch; and
- no future theorem or decision run may close the family without covering
  both non-right subintervals.

## ERR-013 (2026-07-23) — N42 reversed a centrally paired traversal vector

Theory note 41 and session 148 originally claimed that the centrally paired
mate C' of the westward C strand was traversed eastward.  This is false.
Central pairing is

```text
p_(17-k)=D-p_k.
```

For the paired C and B edges this gives exactly

```text
p_12-p_11=p_6-p_5,
p_15-p_14=p_3-p_2.
```

The half-turn negates an undirected geometric vector, but reversing the paired
vertex indices negates it again.  Thus C' is westward like C and B' is
eastward like B.  The original H-east branch joined the terminal endpoint of
H to the **terminal**, not initial, endpoint of C'; the directed reset lemma
does not apply.

The arithmetic budget in note 41 is correct and the H-west branch survives.
It proves only the corrected N42:

```text
v-2*p_(8,x)>0,
```

so every K16W central H edge must point east.  The long-strand traversal is
therefore `E,W,E,W,E`.  No K32S strand order or K32A chart pair is eliminated
by this result.

Consequences:

- the all-cell empty table and the K16W refutation are withdrawn;
- D-0169 is superseded by D-0170;
- K16W returns to open/frozen with the H-east sign added;
- session 148's terminal-outcome statement is withdrawn; and
- directed-strand claims must henceforth be pinned by exact symbolic edge-
  vector identities, not inferred from the carrier's half-turn alone.

## ERR-014 (2026-07-24) — Sandbox process visibility falsely closed HC-34

Session 152 and D-0174 asserted that the HC-34 screen and its first solver
process had died.  That conclusion was false.  The diagnostic `screen -ls`
and `ps` calls ran inside a managed process namespace that could not see or
contact the host-owned screen process, reporting `Dead ???` and no matching
PID.  A host-level check on 2026-07-24 showed the original screen detached and
the complete process chain still live:

```text
SCREEN -> run_research.py -> run_k16w_hc34.py
       -> timeout 10800 -> run_k16w_hc34_cell.py S1--
```

The S1-- cell had been consuming CPU continuously since the original launch.
The two other first-batch cells did abort before solving on the textual-drift
guard, as their logs state.  Thus HC-34 produced no verdict *yet*, but it was
not a completed failed launch and its active cell was never killed.

Consequences:

- D-0174's claims that screen died, no solver survived and HC-34 closed are
  withdrawn;
- D-0175/HC-35's premise of zero active HC-34 work is withdrawn, and HC-35 is
  halted before any research launch;
- the original HC-34 supervisor remains the only authorized solver process;
- after S1-- terminates, the original supervisor may continue its untouched
  second batch under D-0172; the repaired loader changes provenance handling,
  not formula bytes, constraints, ordering or budgets;
- S1-+ and S2-- remain pre-solver failures and are not retried; and
- no future screen/process conclusion may rely solely on the sandbox
  namespace when the process was launched into the host namespace.

## ERR-015 (2026-07-24) — HC-34 pre-solver failures inherit batch wall time

The HC-34 aggregate records `elapsed_seconds` near 10,800 for the two cells
that failed immediately on formula-text drift.  This is not solver time.  The
supervisor launched all three first-batch children together, then waited for
S1-- before it reaped and recorded its already-exited siblings.  The field is
therefore elapsed wall time from batch launch to result recording.

The exception logs and return code 1 establish that S1-+ and S2-- never
entered Z3.  Their disposition is `no_result`, not `resource_stop`.  No timing
comparison or resource-consumption claim may use their recorded elapsed
values.  The four return-code-124 cells are genuine externally supervised
three-hour resource stops.
