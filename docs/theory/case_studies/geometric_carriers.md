# Geometric carrier results and counterexamples

**Status:** integrated case-study dossier
**Scope:** exact local geometry and explicitly defined carrier families
**Global claim:** no monotile construction and no universal polygon
nonexistence theorem

This chapter condenses source notes 15--57 and 79--81.  Those notes contain
many architecture-specific calculations; the consolidation retains their
mathematical value in three forms:

1. source-independent topology and geometry lemmas;
2. exact classifications or no-go theorems for named families; and
3. explicit controls and counterexamples that guard future constructions.

Complete coordinate recursions, inequality systems and corrected derivations
remain byte-preserved under `docs/archive/theory_sources/`.

## 1. Why these are case studies

All families in this chapter granted some combination of a rooted host, named
port roles, a selected cyclic boundary word, a fixed docking involution or a
prescribed participant count.  Those hypotheses are not automatic for one
unmarked polygon.  A family result is nevertheless useful when it:

- classifies every geometry under those hypotheses;
- gives a reusable necessary condition;
- supplies a counterexample to a tempting inference; or
- identifies exactly which hypothesis a future construction must change.

The family names are retained only as stable references to the proof ledger.

## 2. Transferable lemmas

### Lemma G.1 — positive weighted host languages are finite

Let a finite directed graph have positive exact vertex weights, initial set
`S`, terminal set `T`, and target weight `h`.  If

```text
delta = min_v w(v),
```

then every accepted path has at most `floor(h/delta)` vertices.  Hence the
complete accepted host language is decidable by finite exact path
enumeration.  A proposed word set is complete iff it contains every
`S`--`T` path of weight `h` within that bound.

This is `K13W`.  It prevents the common error of checking only intended words
while ignoring repetitions introduced by transition closure.

### Lemma G.2 — two-tile interfaces cannot end alone

Let two polygonal disks with disjoint interiors share a nondegenerate boundary
segment ending at `Q`.  If they cover a neighborhood of `Q` and no third tile
contains `Q`, their common boundary continues through `Q` along a second
nondegenerate segment.

#### Proof

On a sufficiently small circle around `Q`, the two open interiors alternate
an even number of times.  The incoming shared segment provides one transition
branch.  A separator cannot terminate inside the disk, so a second branch
leaves `Q`; polygonality makes it a straight segment of positive length.
This is `N23`. ∎

### Corollary G.3 — positive point participants propagate

Follow a two-participant common-boundary arc maximally.  It either reaches a
third participant or continues.  It cannot close as a common Jordan boundary
of two compact disks with disjoint interiors, since one complementary side is
unbounded.  Thus an occurrence contributing a positive sector at a junction
cannot disappear as a point decoration; each incident interface must be
absorbed by a finite contact complex or propagate through the tiling (`N24`).

### Lemma G.4 — prescribed convex side germs coexist

Any finite list of positive side lengths and convex endpoint-angle pairs can
be embedded as pairwise nonadjacent, intrinsically distinguishable directed
sides of one connected symmetry-free simple polygon.  If the data lie in an
ordered algebraic field, so can all coordinates.

#### Construction

Realize each germ as the outer side of a shallow trapezoidal tab.  Place the
tabs far apart on a large asymmetric carrier, join their bases by short
connector chains, and use one unique marker tab to destroy symmetry.  Small
depths and disjoint bounding boxes ensure simplicity.  This is `K71B`. ∎

The lemma proves that a finite boundary alphabet is cheap.  It does not prove
that congruent copies can pack simultaneously or that unintended contacts are
absent.

### Lemma G.5 — copy-exchanging involutions

If a symmetry-free polygon occurrence `P` is exchanged with another
occurrence `P'` by one isometry `g`, then `g` is a half-turn or a reflection.
Indeed `g^2(P)=P`, so trivial tile symmetry gives `g^2=id`; the only
nonidentity plane isometries of order two are those two types (`K43I`).

### Lemma G.6 — reflection-orbit parity

In a reflection-invariant finite star of congruent copies of a symmetry-free
polygon, reflection acts freely on occurrences.  Every orbit has size two,
so the participant count is even.  In particular no invariant
three-participant hinge exists (`K45O`, `N49`).

A four-participant star has, up to reversal, sector sequence

```text
alpha, beta, beta, alpha
```

and is locally complete exactly when `alpha+beta=pi` (`K45H`).

### Lemma G.7 — clean off-axis reflection docking is impossible

Suppose two symmetry-free polygon occurrences are exchanged by reflection,
have disjoint interiors, and share one clean two-copy arc not contained in
the mirror.  The reflection reverses that interval, so it has a unique fixed
point.  Irredundancy puts the point inside a central side perpendicular to
the mirror.  Reflection preserves each local half-plane of that side, so both
tile interiors occupy the same half-plane and overlap.  Contradiction
(`K43R`, `N48`).

This does not cover an axis-contained side, a T-junction, or a third
participant.

### Lemma G.8 — local role recognition from boundary words

Distinct side lengths, endpoint-angle contexts, and asymmetric cyclic
adjacency words are Euclidean invariants.  If each named role has a unique
rooted boundary germ under these invariants, every placement recovers the
role locally.  Repeated length alone is never sufficient; terminal and
internal occurrences may have different angle contexts (`K41R`, ERR-008,
ERR-009).

## 3. Retiling and synchronization families

The first construction route subdivided a colored triangular source into
three congruent `60/90/120/90` flag kites (`K3F`).  The subdivision is MLD as
a colored system.  Its exact rigidity control says that three convex flag
kites tile their equilateral macrotriangle only in the standard edge-to-edge
placement (`N10`).

Trying to store state solely in the two diagonal retilings of a square leads
to a binary `2x2` corner-plaquette SFT.  Hu--Lin's classification implies
every nonempty such system has a doubly periodic configuration (`N11`).  This
closes the immediate two-state route, not larger binary block encodings.

Jeandel--Rao's bound shows that an ordinary aperiodic edge-Wang macro compiler
requires at least 11 states and four interface colors (`N13`).  A 12-state
two-row domino band with a maximal six-bar delimiter gives unique grouping
only after explicit guards are assumed (`K5S`).  Three natural channels then
fail:

| Channel | Exact outcome |
|---|---|
| north/south ownership only | empty or constant periodic (`N14`) |
| four independent quadrant flips | Hu--Lin periodicity (`N15`) |
| four Cartesian corner sockets | empty or constant periodic (`N16`) |

A cyclic corridor can symbolically compile an aperiodic finite source, but
its unmarked boundary forcing remains the missing theorem (`K5C`).

## 4. Subdivision-word and host-language results

For a selected pair of rooted words `ABC` and `ACB`, local junction equations
can enlarge the transition graph.  With old weights `(1,2,4,7)`, the spurious
word `ABBB` survives every factorized radius-one test (`N29`) and even has an
exact disjoint collar (`N30`).

The weighted-path theorem gives the complete arithmetic repair.  Under the
forced transition closure, `ABC` and `ACB` are the only host words exactly
when:

1. `b+c` has only the representation `(1,1)` over `b,c`; and
2. `a+b+c` is outside the numerical semigroup generated by `b,c`.

This is the necessary-and-sufficient criterion `K13A`.  The infinite family

```text
(a,b,c,h)=(1,n,n+2,2n+3),   n>=4
```

satisfies it (`K13F`).  The result is a reusable boundary-language theorem;
it does not solve polygon packing.

## 5. Equal-spoke lens classification

The selected half-turn shield word first produced a 15-edge square-lens
family.  Its complete containment and closure reduce to six exact partial
sums, one unit direction, and one central edge equation (`K15S`).

### Theorem G.9 — square-lens no-go

No positive weights with `h=a+b+c` satisfy the complete unchanged square-lens
system (`N33`).  Normalized containment bounds force one orientation
parameter simultaneously above and below two disjoint rational functions.
The final difference factors as a strictly positive polynomial on the
admitted interval.

The result closes every weight choice for that topology, including the
arithmetic family above.

Changing the right guard angle gives an equal-leg rhombic lens.  Three long
spokes can fit only for

```text
pi/3 < gamma < 2pi/3.
```

For the critical nonadjacent spoke pair, the exact intersection parameters
are `1-u,u` with

```text
u = b/(2d sin(gamma/2)).
```

Simplicity requires `b>2d sin(gamma/2)`, while containment forces the strict
opposite inequality on both angle branches.  Therefore no equal-spoke
non-right rhombic spine is simple (`K25X`, `N37`).

Unequal outer guard lengths do not create a third clean-spoke family: the
required endpoint incidences force both guards back to the common spoke
length, reducing to the refuted equal-leg case (`N44`, `N45`).

### Classification G.10 — edge-minimal clean spokes

With fixed role order `A-B-C-H-C-B-A`, complete full-side ports, and
half-turn docking, the edge-minimal word is:

- the 15-edge equal-port word when incoming and outgoing ports agree; or
- the 19-edge split-port word when they differ.

There is no third intermediate word (`K42P`, `K42M`, `N46`).

## 6. Unequal-spoke rectangular lens

Splitting each dual-role connector yields the 19-edge `K16B` word and a
rectangular lens.  This is the one analyzed family not decided by theorem.

The exact reduction established:

- 8 partial sums and 32 scalar containment inequalities (`K17S`);
- 120 nonadjacent segment predicates and one closure equation (`K21Q`);
- a necessary extreme aspect ratio
  `v/u>sqrt(23/2)` with `b,c>sqrt(2)u` (`N38`);
- opposite horizontal polarity for the two long spokes (`N39`);
- a compact normalized box with `v<13`, `a<3/2`, and
  `b,c<98/43` (`K31C`);
- exactly four strand orders before intersection filtering (`K32S`), then
  six bounded cells after direction and chord exclusions (`N43`, `K33C`);
- an exact tangent-stratum reduction from eight to seven variables (`K35T`);
  and
- radical-free conjugate-root selector identities (`K36P`, `K38N`, `K40H`).

One attempted strand-reset closure was retracted: central pairing preserves
the directed traversal vector, so the east-pointing case survives
(ERR-013).  The corrected theorem only forces the central `H` strand east.

Two exact solver families reached resource limits without SAT or UNSAT:
Z3/NLSAT by time and cvc5/CAC by memory.  Thus `K16W` remains open in six
bounded cells.  Resource stops are evidence about methods, not geometry.

## 7. Reflection and hinge families

Clean reflection docking is impossible by Lemma G.7.  A reflection-fixed
hinge must instead have four participants by Lemma G.6.  Rooting one of the
two reflected sector pairs can distinguish two local states when
`alpha!=beta`; without the root the states are half-turn congruent (`N50`,
`K46S`).

The full-side rooted hinge forces the boundary template

```text
H, Y, P, Y, D, X, Q, X,
```

so eight sides are minimal under that word (`K47B`).  An exact symmetry-free
octagon realizes the local lengths, angles, closure and role recovery
(`K48R`, `K48C`, `K49W`).

### Counterexample G.11 — the hinge octagon is periodic

The octagon and its half-turn image share the `X-Q-X` chain.  Their union is a
simple 10-gon whose opposite boundary chains are translates by

```text
(19,0)  and  (2,4sqrt(3)).
```

Its area is `76sqrt(3)`, equal to the lattice covolume.  The union therefore
tiles by lattice translation, and the octagon itself tiles periodically
(`N52`).

The periodic assembly never uses the intended hinge state.  This is the
canonical warning that local compiler correctness does not address the
unrestricted tiling language.

## 8. Parity zipper family

The AHI rail parity relation admits an exact rooted two-phase T-junction
zipper (`K70Z`).  Asymmetric length-four delimiters force phase zero at both
ends, making the three visible unit roles project exactly to even parity
(`K71T`).  Bending the host preserves the language whenever endpoint angles
sum to the same phase-dependent constant (`K72F`).

Two exact host chains were constructed:

- a `30`-degree convergent fan at `C=5pi/6` (`K72S`); and
- a strictly convex outward fan at `C=7pi/6` (`K73F`).

The remaining one-polygon step fails for every unbroken convex-flank
realization of all six required ports: their distinct required hull turns sum
to at least `14pi/3>2pi` (`N73W`).  Pairwise-nonadjacent ports require at
least four reflex vertices; allowing the only compatible adjacency still
requires at least three (`K73R`).

The subsequent finite-automaton theorem shows that the zipper is just the
`Z/2`, length-three instance of a general local compiler.  More zipper states
do not approach the all-tilings support theorem.

## 9. Family disposition

| Family | Status | Scope of conclusion |
|---|---|---|
| binary diagonal retiling | closed | immediate `2x2` bit language |
| independent synchronized sockets | closed | product channels |
| equal-spoke square lens | closed | all positive weights |
| equal-spoke rhombic lens | closed | all nondegenerate guard angles |
| unequal-guard clean spokes | closed | collapses to equal-spoke family |
| unequal-spoke rectangle | open/frozen | six exact bounded cells |
| clean reflection spine | impossible | two-copy off-axis interface |
| four-participant reflection hinge | locally realizable; global candidate periodic | fixed eight-side template |
| parity zipper convex-flank carrier | closed | unbroken convex port flanks |

These results are useful admissions filters and counterexamples.  None
classifies arbitrary connected polygons or arbitrary Sturmian realizations.

## 10. Proof provenance

The exact theorem IDs, hypotheses, errata and artifacts remain in
`../reference/proof_ledger.md`.  The source map assigns notes 15--57 and
79--81 to this chapter.  A future paper may extract a family theorem from the
source notes without reviving the corresponding construction as an active
monotile route.
