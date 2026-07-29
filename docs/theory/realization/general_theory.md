# General realization theorems for planar tiling compilers

**Status:** canonical internal synthesis, 2026-07-29
**Scope:** source-independent statements extracted across the chronological
theory corpus; exact note coverage is recorded in
`../reference/SOURCE_MAP.json`
**Novelty:** no general method-novelty claim is made

This document consolidates the reusable mathematics produced by the project.
It deliberately excludes the geometry and address tables of the particular
Akiyama--Hamada--Ito (AHI) source.  Those appear only as applications in
`../research/sturmian_realization.md`.

The central distinction is between two problems:

1. **local compilation:** express a finite symbolic relation using a finite
   contact complex; and
2. **shape-only realization:** force that complex in every unrestricted
   tiling by one connected unmarked polygon.

The first problem is elementary once a rooted multi-participant topology is
granted.  The second is the unresolved monotile problem.

## 1. Definitions

### 1.1 Tiling systems and local maps

A planar tiling system `X` is a translation-invariant set of tilings with
finite local complexity (FLC).  Its translation action is written

```text
T_v(x) = x+v.
```

A map `pi:X->Y` is **finite-radius local** when the output in a bounded
neighborhood of the origin is determined by an input neighborhood of one
fixed finite radius.  It is **translation equivariant** when

```text
pi(x+v)=pi(x)+v.                                         (1.1)
```

The map is **total** when it is defined and produces a legal point of `Y` for
every `x in X`, including tilings that were not part of the intended encoding
construction.

### 1.2 Realization levels

The following levels must not be conflated.

- A **colored local presentation** uses finitely many roles, colors or
  forbidden local patterns.
- A **marked one-support presentation** uses one connected support but retains
  a finite matching relation on its boundary roles.
- An **unmarked finite shapeset** uses shape alone but may contain several
  noncongruent supports.
- An **unmarked monotile realization** uses one connected support, admits all
  Euclidean placements allowed by the claim, and has no external matching
  rule.

Passing from one level to the next is a theorem obligation, not a change of
terminology.

### 1.3 Port-erasure families

For a connected carrier with a finite set of directed boundary ports, write

```text
R subset E_plus x E_minus                              (1.2)
```

for the marked compatibility relation.

A **separable two-participant collar erasure** replaces each complete rooted
port `e` independently by a polygonal profile `p_e` in a collar disjoint from
all other port collars.  Port endpoints and corner sectors stay fixed; exactly
two occurrences enter the collar; and two profiles cover it gaplessly with
disjoint interiors precisely on the relation being realized.

An **ordinary sector star** is a punctured disk partitioned into one connected
sector per incident participant.  It contains no T-junction, terminated edge,
overlap, repeated participant sector or hidden completion state.

These definitions are hypotheses of the theorems below.  They do not describe
all possible polygon contacts.

## 2. Period transfer and periodic completion

### Theorem 2.1 — total decoder period descent (Q0)

Let `X` be a nonempty planar tiling system and `Y` a tiling system with no
nonzero translational periods.  If a total translation-equivariant local map

```text
pi:X->Y                                                   (2.1)
```

exists, then no tiling in `X` has a nonzero translational period.

#### Proof

If `x+v=x`, equivariance gives

```text
pi(x)+v=pi(x+v)=pi(x).
```

Thus every period of `x` is a period of `pi(x)`, contradicting the hypothesis
on `Y` when `v` is nonzero. ∎

The proof is trivial; totality is not.  Agreement on a selected encoded image
does not rule out a second, possibly periodic, component of the full tiling
hull.

### Certificate contract 2.2 — full-local-closure decoding (K1T)

For a finite quotient rule system `X_Q`, a proposed bounded decoder `d` is a
valid total source decoder exactly when every admitted radius-`R` patch:

1. receives a source state from `d`;
2. maps adjacent patches to legal source contacts; and
3. re-encodes to the original quotient patch on every overlap.

Because the alphabets and radii are fixed and finite, these are finite
extensional checks.  Checking only patches observed in one generated tiling is
strictly weaker.

### Theorem 2.3 — periodic completion for grid-aligned finite tiles (T0.1)

Let `T` be a fixed finite polykite on a rank-two lattice `Lambda`.  If a
grid-aligned tiling by `T` has a nonzero lattice period `v`, then another
tiling by `T` has two linearly independent periods, one of which is `v`.

#### Proof

Encode a tiling by the finite set of oriented tile anchors at each lattice
site.  Exact coverage is a finite-range condition, so legal encodings form a
two-dimensional SFT `X_T` and preserve translation periods.

Write `v=g p` with `p` primitive, and complete `p` to a lattice basis `(p,u)`.
Then

```text
Lambda/<v> = Z u + (Z/gZ) p.                            (2.2)
```

A `v`-periodic point of `X_T` is therefore a bi-infinite sequence of finite
columns.  The finite-range constraints make these sequences a nonempty
one-dimensional SFT.  Present that SFT by a finite higher-block directed
graph.  A bi-infinite path contains a directed cycle; repeating the cycle
gives a periodic column sequence.  Its lift is invariant under `v` and under
a vector `m u+j p` with `m>0`, which is independent of `v`. ∎

Consequently weak and strong translational aperiodicity coincide for fixed
grid-aligned finite polykites.  The upgrade from arbitrary Euclidean periodic
polykite tilings to aligned periodic tilings is external, supplied by Appendix
A of Smith--Myers--Kaplan--Goodman-Strauss.

### Theorem 2.4 — common-support colored compiler (S0C)

Let a finite macrotiling system consist of connected patches of one congruent
periodic cell.  Assume every exposed cell edge has one of finitely many
matching roles and every internal cell address is unique within its macro.
Then the macrotiling system is mutually locally derivable with a finite
colored tileset whose members all have the one cell support.

#### Proof

Color each cell by its macro type, internal address and exposed-edge roles.
Adjacent address colors enforce the internal macro adjacency graph; exposed
roles enforce the macro matching rule.  Connectedness makes every legal
colored component one complete macro, and unique addresses make grouping
local and unique.  Forgetting the internal subdivisions recovers the macro
tiling, while subdividing a macro gives the colored tiling. ∎

The theorem compiles finite macro structure into colors, not into unmarked
shape.

### Theorem 2.5 — lossless incidence recoding and compact inverse (K1C/K1R)

Every finite edge-and-vertex SFT has a finite contact-incidence presentation:
directed half-contacts name both endpoint states and their directed edge, all
half-contacts incident to one cell agree on its center state, and cyclic
corner words enforce the old vertex rule.  Encoding and decoding are inverse
radius-one maps on the complete rule space.

For any finite quotient of this presentation, a finite-radius inverse exists
on the intended image exactly when the quotient map is injective on
whole-plane configurations.

#### Proof

The incidence presentation explicitly retains every datum needed by the old
rule, so its radius-one inverse is immediate.  For the quotient statement,
injectivity gives a continuous bijection from a compact shift space to its
Hausdorff image, hence a homeomorphism.  Continuity of the inverse at the
finitely many center cylinders gives one uniform finite decoding radius.
The converse is immediate. ∎

Neither image injectivity nor lossless recoding supplies Contract 2.2 on
additional configurations admitted by a coarser quotient.

## 3. Determinism and undecidability

### Theorem 3.1 — root-deterministic finite carriers are periodic (N55)

Let `X` be a nonempty finite-alphabet `Z^2` carrier system in which the state
at one fixed root determines at most one whole-plane configuration.  Then
every point of `X` is periodic.

#### Proof

There are no more points of `X` than rooted states, so `X` is finite.
Translation acts on this finite set.  The stabilizer of every point has finite
index in `Z^2`, hence contains two linearly independent nonzero translations.
Every point is rank-two periodic. ∎

By Theorem 2.1, no such nonempty carrier can map equivariantly to an aperiodic
target.  A successful carrier therefore needs contextual branching: the same
rooted local state must have more than one global extension.

### Theorem 3.2 — unrestricted symbolic compiler nonemptiness is undecidable

Fix any nonempty aperiodic two-dimensional SFT `Y`.  Given a finite SFT `X`
and a specified local map `pi:X->Y`, deciding whether `X` is nonempty while
`pi` is total is undecidable, even when `pi` is a one-block projection whose
legality is immediate.

#### Proof

For an arbitrary Wang/SFT instance `W`, form

```text
X_W=Y x W
```

and project to the first coordinate.  The projection is total and

```text
X_W is nonempty  iff  W is nonempty.
```

A decision algorithm would solve the domino problem. ∎

This remains a colored symbolic theorem.  Standard higher-block recoding does
not make it a theorem about unrestricted tilings by one unmarked polygon.

### Theorem 3.3 — marked connected-polygon realization is undecidable (U2)

Fix a finite Wang presentation `Y` of a nonempty aperiodic target.  There is a
computable family of one connected polygonal supports with finite edge
matching rules and specified total local decoders to `Y` whose tileability is
undecidable.  Every tileable member is aperiodic.

#### Dependency qualification

This statement is conditional on the all-tilings weave converse, Wang-to-AB
recoding and stick construction in Jack Stade's unrefereed preprint *Two
Tiling is Undecidable* (especially Lemmas 4--5 and Theorem 15).  The repository
has audited the relevant proof chain and pinned its fixed rule table, but this
dependency is not peer reviewed.

#### Proof, conditional on that construction

Given a Wang system `W`, form `Z_W=Y x W`.  Apply the effective Wang-to-AB and
AB-to-stick conversions.  Stade's converse makes every marked stick tiling
locally decode to a tiling of `Z_W`, not merely the intended examples.  Hence

```text
stick(W) tiles  iff  Z_W is nonempty  iff  W is nonempty.
```

Projection to `Y` is a total finite-radius map.  By Theorem 2.1 every
tileable instance is aperiodic, and deciding tileability would decide the
domino problem. ∎

This theorem retains finite matching rules.  Stade's shape-only conversion
uses a second, noncongruent staple support.  Therefore neither construction
settles the one-connected-unmarked-polygon case.

### Decidable subfamilies

The same marked construction has nontrivial decidable restrictions.

- If the auxiliary Wang layer is a finite directed graph copied in every row,
  nonemptiness is equivalent to existence of a directed cycle.
- At any supplied finite cylinder width, legal cyclic rows form a finite
  transfer graph; nonemptiness is again directed-cycle existence.

Thus undecidability is caused by unrestricted two-dimensional contextual
compilation, not by the fixed aperiodic factor alone.

## 4. Complete classification of independent two-body erasure

Call a finite bipartite relation `R` **rectangular** when

```text
R(e,f), R(e',f), R(e',f')  imply  R(e,f').              (4.1)
```

Equivalently, any two nonempty row neighborhoods are equal or disjoint, so
each nontrivial compatibility component is a biclique.

### Theorem 4.1 — biclique classification (K61R)

A finite directed port relation admits a separable two-participant collar
erasure if and only if it is rectangular.  Positive instances have effective
rational polygonal profiles.

#### Necessity

Place every rooted unit port in one canonical position.  There is one fixed
endpoint-reversing isometry `J` placing a mate on the opposite side.  Gapless
two-participant coverage requires

```text
p_e=J(p_f).                                              (4.2)
```

If `R(e,f)` and `R(e',f)`, then `p_e=p_e'`.  If additionally
`R(e',f')`, equation (4.2) gives `p_f=p_f'`, and therefore `R(e,f')`.
So `R` is rectangular.

#### Sufficiency

For each biclique component choose a distinct shallow asymmetric rational
zigzag `q_C`.  Give its left roles `q_C` and its right roles `J(q_C)`; use
distinct unmatched profiles for isolated roles.  Disjoint collars permit all
replacements simultaneously.  Distinct tooth words and endpoint asymmetry
prevent unintended component or reflection matches.  Compatibility is
exactly `R`. ∎

This is the usual jigsaw-color construction stated as a necessary-and-
sufficient classification.

### Theorem 4.2 — physical graph sandwich (K62P)

Suppose only a required physically possible graph `A` must be retained and a
physically possible forbidden graph `F` must be avoided.  Let `cl(A)` be the
union of complete bipartite graphs on the nontrivial connected components of
`A`.  Then an independent two-participant collar relation `B` satisfying

```text
A subset B,             B intersect F is empty          (4.3)
```

exists exactly when `cl(A) intersect F` is empty.

#### Proof

Equation (4.2) propagates profile equality along every path of `A`; hence any
realization containing `A` also contains `cl(A)`.  The component-wise zigzag
construction from Theorem 4.1 realizes `cl(A)` itself.  It avoids `F` exactly
under the stated test. ∎

This finite closure test is the correct weakening when some marked contacts
are geometrically impossible because the carriers overlap.

### Theorem 4.3 — connected required contacts preserve a periodic carrier

Let a carrier admit an edge-to-edge periodic tiling.  If its independent
collar erasure must preserve a required physical-contact graph that is
connected and spans all directed port roles occurring in that periodic
tiling, then the modified polygon also admits a periodic tiling.

#### Proof

Theorem 4.2 forces one complete compatibility component on all those roles.
Replace every carrier occurrence in the periodic tiling by the modified
polygon.  Each old full-edge contact now uses complementary profiles; fixed
endpoints and corner sectors preserve gapless vertex coverage.  The original
translation lattice remains. ∎

The Stade stick application proves its required physical graph is spanning
for every length `n>=5`, so every contact-complete separable self-stapling of
that support retains an explicit periodic row tiling.  This application uses
the published port table but not Stade's weave-converse theorem.

## 5. Limits of ordinary and additive joint tests

Let

```text
E_3={000,011,101,110}                                   (5.1)
```

be ternary even parity.  Every unary and binary projection of `E_3` is full.

### Theorem 5.1 — ordinary sector stars cannot realize parity (K69A)

No ordinary sector star with three binary participant roles and any fixed
passive sectors has exact visible relation `E_3`.

#### Proof

Full unary and binary projections prevent every unary or adjacent-pair germ
condition from rejecting an odd triple.  Let the active sector angles be
`A_x,B_y,C_z` and let the passive total be `Gamma`.  Acceptance of the four
even words gives

```text
A_0+B_0+C_0+Gamma=2pi,
A_0+B_1+C_1+Gamma=2pi,
A_1+B_0+C_1+Gamma=2pi,
A_1+B_1+C_0+Gamma=2pi.
```

Writing `d_A=A_1-A_0` and similarly for `B,C`, subtraction gives

```text
d_B+d_C=d_A+d_C=d_A+d_B=0.
```

Therefore all three differences vanish.  The angle equation, like the unary
and pairwise rules, accepts the entire binary cube. ∎

### Theorem 5.2 — torsion-free additive tests cannot realize parity (K70A)

Let `G` be an abelian group with no nonzero element of order two.  For maps
`f_A,f_B,f_C:{0,1}->G`, if

```text
f_A(x)+f_B(y)+f_C(z)=g_*                                (5.2)
```

holds on `E_3`, it holds on all eight triples.

#### Proof

Subtract the `000` equation from the other three even equations.  The state
differences satisfy the same three equations as above, so
`d_A=d_B` and `2d_A=0`.  Two-torsion-freeness forces all differences to zero.
∎

Taking a product group proves the result for any finite family of additive
tests.  It includes real or algebraic lengths, angles, areas, displacements
and vector-closure budgets.  The result does not cover order-sensitive
topology, collision selection, a two-torsion hidden state or a larger-radius
whole-plane exclusion.

## 6. Rooted T-junctions compile every finite relation

The negative results above concern separable or additive tests.  Once a
rooted three-participant subdivision topology and finite role set are granted,
local expressivity is complete.

### Theorem 6.1 — finite-automaton T-junction compiler (K74A)

For any finite nondeterministic automaton

```text
A=(Q,Sigma,E,I,F)
```

and fixed word length `n`, there is a finite rooted three-participant
T-junction contact complex whose legal covers are in bijection with the
length-`n` accepting paths of `A`.

#### Construction and proof

Enumerate `Q={q_1,...,q_m}` and choose distinct angles

```text
lambda(q_j)=pi/3+j*pi/(6(m+1)).                         (6.1)
```

For transition `(q,a,r)` create a unit code-side role with left endpoint
angle `lambda(q)` and right endpoint angle `pi-lambda(r)`.  A straight host
contributes angle `pi`.  Consecutive transitions ending at `r` and starting
at `s` fill their subdivision point exactly when

```text
pi+(pi-lambda(r))+lambda(s)=2pi,
```

which, by distinctness, is equivalent to `r=s`.  Rooted left and right
delimiters use the complementary initial and final angles.  Thus every legal
cover is an accepting path, and every accepting path satisfies every sector
equation. ∎

### Corollary 6.2 — every finite fixed-arity relation (K74R)

For finite alphabets `Sigma_1,...,Sigma_n` and finite relation

```text
R subset Sigma_1 x ... x Sigma_n,
```

apply Theorem 6.1 to the deterministic prefix trie of `R`.  After projecting
transition roles to visible symbols, the legal covers are exactly `R`, and
each accepted word has a unique lifted trie path.

### Corollary 6.3 — finite-group word constraints (K74G)

For a finite group `G`, use states `G`, identity as the initial/final state,
and transitions `q --g--> qg`.  The compiler accepts exactly words whose
product is the identity.  The three-bit parity zipper is merely the case
`G=Z/2`, `n=3`.

These are colored, role-labelled contact-complex theorems.  The rooted host,
word order, alignment, participant count, delimiter roles and reflected
semantics are hypotheses.  Nothing here proves that one unmarked polygon
forces them.

## 7. Finite weighted subdivision languages

Let a finite directed graph have an initial set `I`, terminal set `F`, exact
positive vertex weights `w`, and target host length `h`.

### Theorem 7.1 — finite weighted-path criterion (K13W)

Put `delta=min w(v)`.  The complete accepted host language is the finite set
of `I`--`F` paths with at most `floor(h/delta)` vertices and total weight
`h`.  Therefore equality with a proposed finite word set is decidable by
exact finite path enumeration, even when the transition graph has cycles.

#### Proof

An accepted path of `k` vertices has weight at least `k delta`, so
`k<=floor(h/delta)`.  A finite graph has finitely many paths at bounded
length.  Exact endpoint, transition and weight checks are necessary and
sufficient. ∎

The transition graph must be the closure forced by the geometry, not the
adjacency list one hoped to realize.  The theorem detects repetition and
alternative subdivision words before coordinate synthesis.

## 8. Topology of polygonal contact interfaces

These results concern arbitrary compact polygonal disks and do not depend on
a source alphabet.

### Theorem 8.1 — two-participant interfaces cannot terminate alone (N23)

Let two polygonal disk occurrences have disjoint interiors, share a
nondegenerate boundary segment ending at `q`, and together cover a
neighborhood of `q`.  If no third occurrence contains `q`, their common
boundary continues through `q` along a second nondegenerate segment.

#### Proof

In a sufficiently small circle around `q`, the two open interiors are the
only regions.  Transitions between two regions on a circle occur in pairs.
The incoming shared segment gives one separator branch; hence another branch
must leave `q`.  Polygonality makes it a straight segment of positive
length. ∎

### Corollary 8.2 — positive point participants propagate (N24)

A maximal two-participant polygonal contact arc terminates at a third
participant.  It cannot close as a common Jordan boundary component of two
compact disks with disjoint interiors, because one complementary side is
unbounded.  Thus a positive sector introduced at one contact cannot be
treated as a point decoration; its adjacent boundary interfaces require a
bounded completion or propagate through the tiling.

### Theorem 8.3 — copy-exchanging involutions and reflection parity

Let a polygonal disk have trivial Euclidean symmetry.

1. An isometry exchanging two occurrences has order two and is therefore a
   half-turn or a reflection.
2. Reflection acts freely on the occurrences of every invariant finite local
   star.  Hence the number of participants is even.
3. A reflection-invariant star with two occurrence orbits has sector order
   `alpha,beta,beta,alpha` and fills a neighborhood exactly when
   `alpha+beta=pi`.

#### Proof

For (1), exchanging twice stabilizes the support; trivial symmetry makes the
square of the isometry the identity.  For (2), a fixed occurrence would give
the support a reflection symmetry.  The orbit count follows.  The mirror has
two opposite fixed rays; freeness forces both to be sector boundaries, giving
the stated order, and the angle equation follows by summing sectors. ∎

### Theorem 8.4 — clean off-axis reflection docking is impossible (N48)

Two symmetry-free polygon occurrences exchanged by reflection cannot have
disjoint interiors and one clean invariant two-copy interface arc outside
the mirror axis.

#### Proof

Reflection reverses the interface interval and has one fixed point.  A fixed
irredundant vertex would require angle `pi`, so the point lies inside a
central side perpendicular to the mirror.  Reflection preserves each local
half-plane of that side.  The two reflected interiors therefore occupy the
same half-plane and overlap. ∎

The theorem deliberately excludes an axis-contained side, T-junctions and
third participants.

## 9. Boundary alphabets versus simultaneous realization

### Theorem 9.1 — finite convex side-germ embedding (K71B)

Any finite collection of triples

```text
(positive side length, left convex angle, right convex angle)
```

can occur as pairwise nonadjacent, intrinsically distinguishable directed
boundary germs of one connected symmetry-free simple polygon.  Algebraic
input data can be realized over the same ordered algebraic field.

#### Proof

Make every prescribed side the outer edge of a shallow trapezoidal tab with
the required flank directions.  Put the finitely many tabs in disjoint boxes
along a large carrier and join their bases with short polygonal chains.
Choose distinct spacings and one unique asymmetric marker.  Shallow disjoint
tabs ensure simplicity; the marker destroys every nontrivial symmetry. ∎

The theorem isolates an important boundary: storing finitely many local
roles on one polygon is easy.  Proving simultaneous congruent packing,
complete contact termination and the absence of unintended tilings is the
hard part.

## 10. Consolidated expressivity boundary

The source-independent local hierarchy is now:

| Realization mechanism | Exact expressive power established here |
|---|---|
| Independent complete two-body profiles | Biclique/rectangular relations |
| Independent physically required profiles | Biclique closure of required-contact components |
| Ordinary sector stars | Cannot realize ternary parity |
| Finite torsion-free additive tests | Cannot realize ternary parity |
| Rooted hidden-state T-junction chains | Every finite fixed-arity relation |

Therefore another local automaton, parity gadget, delimiter, zipper or larger
finite role alphabet does not approach the monotile theorem.  The remaining
question is whether one connected unmarked support can force the required
roles and topology, exclude all alternative contacts and admit a total
whole-plane decoder.

## 11. Claim and literature boundary

All proofs above are internal proof drafts unless explicitly marked external
or conditional.  Their general ideas lie in standard symbolic dynamics,
jigsaw matching, finite-state recoding and edge-patch machinery.  In
particular:

- Theorems 2.1, 3.1 and 3.2 are standard dynamical/finite-state arguments.
- Theorems 4.1--4.2 are the familiar jigsaw-color principle sharpened into a
  stated classification.
- Theorems 5.1--5.2 are elementary algebra.
- Theorem 6.1 is standard automaton state propagation expressed by angles.
- Theorem 3.3 is a product corollary conditional on Stade's preprint.

The audited literature does not supply the conjunction required for one
connected unmarked Euclidean polygon in unrestricted gapless tilings.  That
is a dated absence report, not a novelty or impossibility theorem.

## 12. Provenance

The row-level IDs, qualifications and dependencies remain in
`../reference/proof_ledger.md`.  The extracted source notes remain available
under `docs/archive/theory_sources/`.  Controlling reviews are:

- `docs/literature/reviews/MARKED_STURMIAN_UNDECIDABILITY.md`;
- `docs/literature/reviews/FINITE_AUTOMATON_CONTACT_COMPILER.md`;
- `docs/literature/reviews/TJUNCTION_CONTACT_COMPLEX.md`; and
- `docs/literature/reviews/K5C_SINGLE_TILE_SIMULATION.md`.
