# W3 — exact substitution certificates

W3 is the constructive branch of the program.  Its target theorem T3.1 says
that a finite C1--C5 certificate yields both a plane tiling and trivial
translation stabilizer for every legal tiling.  The first validation subject
is the vendored Spectre generator. The legacy “finalist” is now identified as
the known Turtle (ERR-003/D-0048); this gate supports the general certificate
method rather than a Turtle novelty claim.

> **Disposition (D-0070, 2026-07-21):** W3 is closed as a novelty branch.
> The exact finite results below are retained as a machine-readable partial
> reconstruction of the published Spectre hierarchy and as verifier controls.
> Reduced-patch pruning, forced grouping, all-whole-plane hierarchy,
> matching-rule encodings, and finite-state refinement all have controlling
> prior art. T3.1 has no authorized novelty claim without a generic
> soundness/completeness theorem and validation on structurally independent
> systems. The 80 D4 contexts will not be extended merely to finish this
> known-tile reconstruction. See
> `docs/literature/reviews/W3_CERTIFICATE_METHOD.md`.

## Literature crosswalk

W3's five clauses are repository certificate fields, not new names for an
uncited theorem. They must be compared explicitly with the controlling proof
architectures:

| W3 obligation | Literature control | Audit question |
|---|---|---|
| C1 legal recursive realization | SMKGS Hat/Spectre proofs; Chéritat cluster analysis | Are macro-boundaries and all child intersections proved legal at every level? |
| C2 finite rule closure | SMKGS forced metatiles; Tatham transducers | Is the state alphabet closed, and can transitions be represented without ambiguous hidden context? |
| C3 whole-plane existence and scale growth | substitution constructions; Akiyama--Araki Golden Hexes | Is there a nested/fixed construction with a certified divergent inradius? |
| C4 exhaustive recognisability | Walton Theorem 5.2/Corollary 5.5; Chéritat Corollary 63 | Does every admitted whole-plane tiling, not only generated samples, have the asserted preimage, and is the translation ambiguity eliminated without circularly assuming aperiodicity? |
| C5 global consistency | Labbé--Selinger SFT/Markov coding; local hierarchy proofs | Do all locally admitted parent overlaps glue, and does the finite language equal the intended hull? |

Catalog IDs and review status live in `docs/literature/SOURCES.json`; detailed
implementation gaps are in `docs/literature/METHODS_MATRIX.md`. The focused
Walton and Chéritat theorem audits are in `docs/literature/reviews/`. This
crosswalk is not a claim that W3 has instantiated either proof.

### Two recognisability routes that must not be conflated

Walton defines an `L`-sub pattern space using a **surjective local-derivation
subdivision** `S:LΩ→Ω`. Theorem 5.2 gives unique composition modulo
translation for every compact Hausdorff expansive `L`-sub space. In a
return-discrete tiling space, Corollary 5.5 strengthens this to strict
injectivity exactly when the hull contains no periodic tiling. Therefore
Walton is a powerful post-aperiodicity recognisability theorem and consistency
control, but invoking strict injectivity to prove the same hull-wide
nonperiodicity would be circular.

Chéritat supplies the non-circular control architecture. For every
whole-plane `Tile(1,1)` tiling without reflections, his finite cluster and
interface analysis gives a unique grouping, faithful intermediate
representations, and a parent description of the same kind; Corollary 63
iterates this indefinitely. Proposition 64 and Corollary 65 run the
construction backward to prove existence. W3 must reproduce this logical
scope, not necessarily the same pictures.

The version-2 certificate therefore emits two separate audits:

- Walton hypotheses `W1`--`W5`: compact/FLC hull, Hausdorff separation,
  Euclidean expansivity, surjective LD subdivision, and independent discrete
  nonperiodicity for strict injectivity;
- direct-composition obligations `D1`--`D7`: formal all-tilings domain,
  parent existence, unique grouping, faithful encodings, iterability, a
  uniform local inverse, and period descent with scale growth.

Only the direct route is eligible to become W3's standalone aperiodicity
proof. Every current row is derived by the verifier; the JSON has no
self-reported switch that can promote an unsupported claim.

The first Turtle-side literature control is now concrete. Exact standard words
and central-palindrome decompositions from Akiyama--Araki pass through level
24. Their independent Golden Ammann-bar count predicts minority handedness
`(3-sqrt(5))/6`; the existing 9,239-tile Turtle disk gives `1181/9239`. The
artifact and plot are `theory-w3-turtle-golden-sturmian.{json,svg}`. This
discharges only a combinatorial precursor and density-algebra control. It does
not discharge W3 C1, C3, C4, or C5 because the geometric Golden Hex induction
and forced-bar local cases have not been reconstructed.

## T3.0 — the finite combinatorial kernel

The A6 artifact recovers a deterministic, closed alphabet of 17 radius-one
collared states.  Its incidence matrix is primitive with least exponent 3.
These are exact finite facts, independently recomputed by
`substitution_certificate.py`; they discharge C2 but do not establish C1,
C3, C4 or C5.

In particular, A6's 309/309 unique composition instances are sampled from
interiors of generated Delta patches.  They are strong calibration evidence,
not the exhaustive legal language required by C4.

## Ancestry-blind physical-language prefix

The first direct C4/C5 experiment now starts from the exact straight
`Tile(1,1)` polygon, not from A6 labels or parent paths. Under one fixed
chirality, rotations and translations, and the edge-to-edge unit-edge contact
model, the central tile has 79 nonoverlapping neighboring poses and exactly
166 complete first coronas. Exact SAT ring completion contracts their
existential language as follows:

```text
complete first coronas                  166
extend through a complete second ring   30
extend through a complete third ring    21
seen in all level-3/4 substitution controls 18
```

The 18 generated types are stable across all nine root labels at both tested
levels and lie inside every finite survivor set. The three additional
radius-three types are corona indices 33, 44 and 155. Targeted exact SAT
witnesses extend all three through a fourth ring, so blind shallow-radius
growth does not distinguish the generated hull from every locally viable
branch.

The ownership test also falsifies an attractive shortcut. Of the 166 first
coronas, eight are compatible with exactly one recovered full/missing parent
occurrence, but all eight are dead ends by the second ring. Conversely none
of the 21 radius-three survivors is uniquely owned: 17 admit two compatible
central parents, three admit three, and one admits five. Therefore a valid
recognition certificate must coordinate grouping choices across neighboring
centers; isolated central-parent uniqueness is neither necessary nor
sufficient at this radius.

This is a complete **existential central-corona prefix through radius three**,
not a complete enumeration of all radius-three patches and not a whole-plane
extension theorem. It also assumes edge-to-edge contact; the reduction from
all geometrically admitted straight-Spectre tilings to that model remains an
explicit proof obligation. The artifact, figures, producer and cold verifier
are `theory-w3-spectre-physical-language.{json,svg}`,
`theory-w3-spectre-radius3-extra-survivors.svg`,
`run_theory_w3_spectre_patch_language.py`, and
`verify_theory_w3_spectre_patch_language.py`.

## Coordinated parent-overlap language

The next experiment replaces isolated ownership with a joint partial exact
partition. A parent variable is one translated/rotated occurrence of the
recovered full or missing 9/8-child template. Every **universally buffered**
inner tile—one for which all parent occurrences still compatible with the
visible physical patch lie inside the next-ring candidate universe—must be in
exactly one selected parent. Every other visible or candidate tile is in at
most one. Parent selection and exact physical next-ring completion are solved
in the same SAT instance.

The buffered definition is essential. Three radius-two branches of corona 44
and twelve of corona 155 initially have no safe target; they are expanded as
unrestricted physical branches rather than being misreported as grouping
UNSAT. In this run those branches have no physical third-ring completion, but
the guard is retained as part of the certificate semantics.

All 18 substitution-observed corona types have exact coordinated groupings in
generated graph-radius-four controls. The three extras exhaust as follows:

| corona | complete r2 branches | admissible r3 frontier | admissible r4 frontier | result |
|---:|---:|---:|---:|---|
| 33 | 2 | 200 | 0 | refuted by coordinated r4 |
| 44 | 27 | 0 | 0 | refuted before coordinated r4 |
| 155 | 60 | 24 | 0 | refuted by coordinated r4 |

Thus the finite central-corona language contracts conditionally from 21 to
the same 18 types seen in the substitution controls. This is a real closure
of the three explicit finite counterbranches, but the word “conditionally” is
not cosmetic: the test assumes that a whole-plane tiling is partitioned by
the recovered 9/8 parents. It does not prove that every geometrically admitted
tiling has such a partition, that the partition is unique, or that contraction
returns to the same all-tilings domain. Those remain D2, D3 and D5.

The artifact and figures are `theory-w3-spectre-parent-overlap.json`,
`theory-w3-spectre-parent-overlap.svg`, and
`theory-w3-spectre-grouping-witness.svg`. The producer and cold verifier are
`run_theory_w3_spectre_parent_overlap.py` and
`verify_theory_w3_spectre_parent_overlap.py`.

## Physical-to-parent transducer and unique L18 partition

The conditional direction can be removed **inside the L18 domain**. Exact
L18 completion gives 87 radius-two and 418 radius-three rooted physical
patches. Exhaustive buffered grouping of every radius-three case yields a
unique parent-anchor map. Forty-eight cases have multiple raw 8/9 group
choices, but every choice has the same anchor; the ambiguity is only the
optional ninth child at the finite boundary.

Applying this 418-entry local transducer throughout every exact extension to
radius six leaves 15,216 surviving patches. All have the complete canonical
eight-child core of the central anchor, and all eight children map back to
that anchor. The map's fibers are therefore exactly the common eight-child
component, with or without the one optional ninth child. This proves parent
existence and the unique full/missing partition for every whole-plane tiling
whose complete physical coronas all lie in L18. Parent variables are outputs
of the finite physical rule, not assumptions of the proof.

Contraction does not yet close. The 17 generated complete parent-corona states
coexist with non-generated finite branches. Once every central interface is
resolved at radius seven, the non-generated frontier evolves

```text
radius 7: 6280
radius 8: 1796
radius 9: 4482
```

The renewed radius-nine branching is not a whole-plane counterexample, but it
ends the blind-ring strategy: physical boundary fillings grow faster than the
small contracted state data that distinguish the cases. The next proof object
is the finite parent/interface overlap graph. It must either give a dead-SCC
certificate for every extra contracted state or expose a recurrent component
requiring an additional Chéritat-style interface label.

The first such quotient has now been tested. The physical frontier collapses
to nine non-generated uncolored parent coronas, giving 26 states together with
the 17 controls. Reciprocal-edge constraints, all triangle agreements visible
from neighboring radius-one coronas, and fixed-point support deletion leave
all 26 states alive. This proves that uncolored anchor coronas are insufficient.
The next alphabet must attach full/missing component type and the oriented
physical child-edge interface realizing each parent contact.

The artifact is `theory-w3-spectre-component-language.json`; its producer,
structural verifier and tests are the corresponding
`run_...component_language.py`, `verify_...component_language.py`, and
`test_spectre_component_language.py` files.

## Exact geometry is recurrent, not a fixed similarity

The generator's eight child frames have fixed reflection/rotation parts, but
their translations vary with level.  Four distinguished rank-four module
points form a 16-coordinate vector `q_n`.  A direct exact derivation gives one
integer matrix

```text
q_(n+1) = F q_n,       F in GL(16,Z),       det(F) = 1.
```

The verifier reconstructs `F` by applying the generator construction to the
16 coordinate basis vectors.  It checks the exact minimal-polynomial identity

```text
(F^2 - I)^2 (F^4 - 8 F^2 + I) = 0.
```

Thus the expanding linear root is `sqrt(4+sqrt(15))`, and the two-level
expansion factor is `4+sqrt(15)`.  All 256 child translations materialized in
the 32-level Rust table agree exactly with this recurrence.  This explains why
the recovered stationary *combinatorial* rules must not be interpreted as one
fixed Euclidean placement rule on the kite lattice.

## Current C1 exact checks

The verifier expands physical Spectre leaves in rank-four integer coordinates.
Its polygon kernel uses exact signs in `Z[sqrt(3)]`, checks pairwise interior
disjointness, unit-edge incidence at most two, and edge connectivity.  All
nine labels at levels zero and one pass (18 realized patches; level-one counts
are eight or nine physical tiles).

The nine named geometric rules collapse exactly to two support types at every
level: `full` for every non-Gamma label and `missing` for Gamma. This follows
inductively from the rule table, not from a finite sample. Both types have
abstract cell complexes with Euler characteristic one and one boundary cycle
through level four. Their boundary lengths through level six are:

```text
full:     14, 46, 182, 758, 3198, 13534, 57318
missing:  20, 44, 160, 652, 2736, 11564, 48960
```

For the boundary side joining distinguished vertices `q[2]` and `q[1]`, an
exact five-piece dihedral word recursion matches leaf-expanded boundaries
through level five. Its lengths `2, 8, 34, 144, 610, 2584` obey
`a_n=4a_(n-1)+a_(n-2)`, with dominant root `2+sqrt(5)`.

Tracing exterior edges by child owner yields a stable four-side macro grammar.
Its endpoint identities are now proved for **every** level: each identity is
integer-linear in `q_n`; the degree-eight annihilator above makes eight exact
initial checks sufficient for all `n`. The missing type uses the same A/B/C
sides and replaces the omitted slot-two long arc by that virtual child's
complementary C side. This is an all-level gluing skeleton, not merely an
observed prefix.

The two-type reduction and macro-side endpoint grammar are all-level theorems,
but endpoint chains alone do not prove that the recurrent paths are simple or
that nonadjacent children never cross. The complete direction-word formula is
still a finite falsification-tested conjecture. C1 remains
**partial** until a finite macro-boundary induction proves legality for every
level and connects those realized supports to all 17 collared states.  C3 also
remains partial: primitivity and exact algebraic expansion are proved, but a
certified inball-radius recurrence is still missing.

## Honest obligation table

| clause | current status | missing step |
|---|---|---|
| C1 legality | partial | exact macro-boundary/nonoverlap induction for all levels and collared supports |
| C2 closure | verified | — |
| C3 existence/growth | partial | inball center and divergent exact radius recurrence |
| C4 recognizability | partial | D1/D2/D3/D5/D6 are verified throughout the unrestricted fixed-chirality hull; D4's finite maps are exact but its 80 surviving radius-two state contexts have not been equated with the physical-derived hull; D7 also remains open |
| C5 global consistency | partial | unrestricted physical tilings enter L18 and contract to 17 states; the D4 17↔17 and scale round trips verify, but the abstract state SFT strictly over-approximates the faithful context language |

The versioned artifact is
`docs/notebook/assets/theory-w3-spectre-certificate-v0.json`.  The producer and
cold verifier are `run_theory_w3_spectre_certificate_audit.py` and
`verify_theory_w3_substitution_certificate.py`.

## Completed physical-language sequence

For the physical-language branch, parent existence and unique partition are
now established within L18. Extract full/missing component type and oriented
physical contact intervals from the complete radius-seven witnesses, build
the colored interface-overlap graph, and classify its recurrent strongly
connected components. Same-domain iteration requires eliminating every
non-generated recurrent component or refining the alphabet with the next
precise interface datum that separates it.

The first such refinement is now exhausted. Across all 57,589 resolved
radius-seven extensions, center full/missing type plus exact oriented
child-edge contacts produces 17 generated and five extra states. The 17 agree
exactly with an independent substitution control, but all 22 pass reciprocal,
colored triangle-star and fixed-point support and lie in one closed SCC.
Consequently this **one-sided** colored alphabet is a proved no-go for D5.
The minimal next experiment buffers two more physical rings so that the
full/missing type at both endpoints of each interface is observed rather than
left as a wildcard.

That two-sided experiment is also complete. The non-generated frontier follows
`6280→1796→4482`, all 4,482 final interfaces resolve, and they collapse to
three new full-component states. All three survive with the 17 controls in one
SCC, so radius-one two-sided interfaces are another finite no-go for D5.
Minimum-extra-neighbor optimization separates the obstruction: one state has
a generated-only surrounding star, while the other two have minimum cost one
and minimally require each other. The next exact object is therefore a pinned
radius-two state CSP, not a still wider radius-one color.

The pinned radius-two CSP closes that question. Of the `28+100+3` possible
extra-centered first stars, only one per root survives exact colored pair
agreement and exact nonoverlap of the represented 8/9-child supports. Their
complete assignment counts are 960, 432 and 840. Every one of the 131 cases is
UNSAT when the second ring is restricted to generated states, so all three
defects propagate. Intersecting defect types over every model gives the forced
map `A→C, B→C, C→A`. This proves that a defect cannot terminate inside two
parent rings, but repeated implications may revisit an earlier anchor; it does
not yet prove unbounded propagation, existence, or impossibility. Radius three
must test the alternating `A/C` branch against exact geometry or turn it into
a density or fault-line invariant.

Radius three eliminates the branch instead. Every one of the 2,232 complete
radius-two assignments was extended by all anchors named from ring two. The
three extra roots have `0,2,1` surviving CSPs. The first root is therefore
impossible in a whole-plane 20-state configuration, and every survivor of
either other root already contains that dead state in its fixed inner patch.
All three extras are excluded. Consequently D5 same-domain closure is now
verified **inside L18**: contraction yields only the 17 generated states.
That contracted-state calculation by itself does not discharge D1 entry of
every geometric Spectre tiling into L18, D4 faithful hull equivalence, C1
legality or C3 growth.

The ancestry-free physical continuation closes the D1 gap inside the declared
edge-to-edge contact model. Seed all three physical coronas outside L18 and
enumerate every exact nonoverlapping complete next ring. Their rooted patch
frontier is

```text
radius       1    2    3    4   5
patches      3   89  368  282   0
```

The radius-five frontier is empty: all 282 radius-four patches already have
an exposed edge with no candidate cover. Since a whole-plane occurrence would
restrict to one of these finite patches, types 33, 44 and 155 are impossible.
Together with the exhaustive `166→30→21` prefix, every complete corona in any
fixed-chirality edge-to-edge tiling is therefore in L18. An independent
one-hot CaDiCaL encoding reproduces all four frontiers. No parent template,
substitution state or generated control enters the ring constraints; the
generated control is used only to name the three physical types outside L18.

This verifies D1/D2/D3/D5/D6 throughout the edge-to-edge domain. It does not
yet prove that every unrestricted geometric straight-Spectre tiling is
edge-to-edge; T-junctions and other partial-edge contacts remain a separate
domain-reduction obligation. D4 faithful hull equivalence, C1 legality and C3
growth also remain open.

The unrestricted edge-patch bridge now closes that domain reduction. The 14
primitive unit edges merge into 13 maximal polygon sides with length histogram
`12×1 + 1×2`. Every interior angle is at least 90 degrees, and no maximal side
has right angles at both endpoints. Consequently any straight interface uses
at most two polygon sides per half-plane. There are exactly ten ordered
equal-length words of one or two parts from `{1,2}`; all ten split uniquely at
integer offsets into identical unit-edge words on both sides. Thus every
T-junction is already a vertex of the primitive 14-segment boundary.

Adjacency simultaneously locks every tile to one global 30-degree orientation
frame, and matching primitive endpoints puts every anchor in the rank-four
module. The independent verifier reconstructs the 13 sides and ten patterns
from the raw boundary and checks both exact even/odd `sqrt(3)` deformations.
Composing this bridge with the radius-five theorem verifies D1/D2/D3/D5/D6 on
the unrestricted fixed-chirality polygonal hull.

## D4 finite equivalence kernel

The forward and inverse maps are now explicit. The 17 child-edge-colored
component states project bijectively onto the 17 A6 radius-one collars; the
level-four control realizes all states in 310 complete occurrences, with no
many-to-one relation in either direction. Expanding each state into its 9/8
component and six neighboring components, then re-reading the interfaces,
returns the same state in all 17 cases. Each full/missing central boundary has
respectively 46/44 external primitive edges, and every one appears exactly
once in the interface colors.

The scale change is an exact phase-sensitive module map. There are two
determinant-one integer linear parts, exact integer inverses and six offsets per
chirality. Chirality toggles globally, rotation parity is retained, and a
translation `u` maps to `A_(chirality,parity) u`. One ordinary Spectre is
created for each first parent; states 10, 11 and 12 mark second-parent bases and
create one companion Spectre at relative pose `(0,1,(1,-3,-2,0))`. Forward and
inverse reconstruction gives the exact generated identities

```text
63 +   8 =   71
496 +  63 =  559
3905 + 496 = 4401
```

for level pairs 3→2, 4→3 and 5→4. Both two-level translation matrices have
characteristic polynomial `(x²-8x+1)²`, independently meeting the earlier
`4+sqrt(15)` recurrence.

This is a substantial D4 kernel, but not yet the hull theorem. The bare
17-state colored overlap SFT has 3,565 radius-one stars. Under the exact
next-phase map, 536 produce physical overlaps, 410 do not buffer the central
ordinary tile, and 2,619 give a valid buffered central corona. Thus radius-one
state consistency is strictly weaker than physical provenance. One additional
exact state ring kills 3,485 seed stars and leaves 80. D4 remains **partial**
until those 80 contexts are proved to be exactly the physical-derived
transition language (or the nonphysical remainder is finitely eliminated).

## Next proof obligation

Construct a pinned faithful-map CSP for the 80 radius-two seeds. It must carry
the next-phase ordinary/companion tiles together with the original physical
9/8 fibers, then prove that every whole-plane physical-derived center has one
of the nonoverlapping round-trip contexts and every other recurrent context is
impossible. Once that equality is established, promote D4 and use the exact
two-level matrices for D7 translational-period descent.

In parallel, use the all-level macro-side grammar to derive the complete
direction-word recursion, then prove its recurrent paths are simple and that
child interiors occupy disjoint sides of every glued arc. Such a noncrossing
lemma would upgrade the present C1 checks to an all-level induction and expose
the boundary data needed for C3 inballs.
