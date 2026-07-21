# Sturmian tile-set to monotile prior-art audit

**Audit date:** 2026-07-21
**Question:** can the quadratic-slope Sturmian-lattice tile sets be faithfully
encoded by one connected, unmarked Euclidean-plane tile, and is such an
encoding already supplied by general matching-rule or poly-`K` theory?

## Decision

**Go, but only for a narrowly stated theorem-design branch.** No audited
source supplies a shape-only, single-prototile encoding of the new Sturmian
tile sets. Several nearby results remove colors, reduce the number of supports,
or transfer a geometric tile to a group tile, but each stops short of the
ordinary monotile claim in a precisely identifiable way.

The admissible target is not “collapse any aperiodic tile set.” Its minimal
aperiodicity form is:

> For one explicit non-golden quadratic slope, construct a connected unmarked
> topological-disk tile whose every Euclidean tiling has a translation-equivariant
> finite-radius map into the corresponding irrational Sturmian-lattice
> tiling system.

Surjectivity onto the complete Sturmian system is a separate, stronger target.
It is not needed to exclude periods, but it is needed if the construction is
also meant to transfer the source system's positive entropy.

The first control should be `alpha = sqrt(2)-1`, because the source paper gives
an optimized three-prototile realization by topological disks and reports
positive topological entropy for its tiling space. No experiment or geometric
construction is authorized by this audit alone.

## What the Sturmian papers actually prove

The controlling source is the full version
`akiyama-hamada-ito-sturmian-2026`, not the seven-page announcement
`akiyama-hamada-ito-announcement-2026`.

- Section 6 defines a tile as a compact support **plus a color**. Ammann bars
  and their adjacency conditions are part of the finite-color matching rule.
- Theorem 4 constructs an aperiodic finite tile set for every quadratic
  irrational slope. Its abstract pair of density classes unfolds through
  bounded-displacement correspondences into finitely many actual patch-tile
  types.
- Remark 7 explicitly says that Theorem 4 does not exclude a one-patch-tile
  realization; it does not construct one.
- Theorem 5 gives a linear-in-expansion-factor upper bound on the number of
  tile types, not a monotile theorem.
- Section 10.1 constructs a three-prototile example for
  `alpha = sqrt(2)-1`; the prototiles are homeomorphic to disks, and local
  interchangeable pairs give positive topological entropy.
- Section 10.2 recovers the already known Turtle mechanism at the golden
  slope.
- Section 11 asks whether another aperiodic monotile can be obtained. It also
  says that all supports can be made connected in the general construction,
  while connected interiors and elimination or simplification of the Ammann
  bars remain open.

The July announcement repeats the finite-tile-set theorem. Its Nut-and-Bolt
presentation explicitly allows disconnected supports and displays a
29-patch-tile example as disjoint unions of disks. It does not strengthen the
result to an unmarked monotile.

At the formal limit `kappa = infinity`, Section 10.2 says supports can be
reduced to one *up to color*. Removing the words “up to color” is not valid:
forgetting colors and Ammann-bar rules enlarges the tiling hull and can admit
periodic tilings. The Turtle is exceptional precisely because its geometry
forces the bars; the general construction contains no analogous theorem.

## Why nearby general machinery does not close the problem

### Local matching rules

Goodman--Strauss (`goodman-strauss-matching-1998`) constructs finite local
rules forcing broad classes of substitution tilings. The theorem concerns
decorated/local-rule prototile sets, not reduction to one shape. The recent
FLC extension (`vereshchagin-matching-2026`) likewise states that substitution
or hierarchical tiling families are sofic through decorations; it does not
erase tile types or external rules. Moreover, the positive-entropy Sturmian
example is not presented as a single deterministic substitution hull.

Standard colored-edge-to-jigsaw conversions can replace colors by boundary
geometry. They ordinarily produce one distinct geometric prototile for each
tile type. Thus they can help obtain an unmarked **finite tile set**, but they
do not solve congruence of all supports.

The positive-entropy source cannot simply be treated as the zero-entropy,
uniquely deterministic substitution hull familiar from Hat/Turtle/Spectre,
and the paper supplies no unique-parent hierarchy. That strategy therefore
cannot merely be reused for the no-spurious-tilings lemma. The natural proof
target is arithmetic: shape-forced Ammann bars or an equivalent local coding
whose line sequences are Sturmian for every admitted tiling.

### Atlas reduction

Fletcher (`fletcher-atlas-2010`) proves that congruent supports can encode
tile types through their symmetry orientations when a finite atlas of legal
coronas is imposed. The theorem preserves MLD and can reduce 13 planar Wang
squares to two squares; it reduces 21 Wang cubes to one cube in three
dimensions. The constraint is still an external atlas rule. The paper
explicitly distinguishes this from a monotile determined by shape alone.

The Hat paper makes the same logical boundary vivid: with arbitrary finite
atlas rules, even a rectangle can be called an aperiodic monotile. That is not
the paper's—and not this repository's—ordinary unmarked geometric notion.

### Poly-`K` and group monotiles

Theorem 7 of `coulbois-et-al-groups-2026` gives a bijection between poly-`K`
tilesets and finite tilesets of `G x K`, preserving cotilers and the **number
of tile types**. Its monotile corollary starts with a geometric poly-`K`
monotile. The Hat-to-Cucaracha construction therefore transfers an existing
monotile into a virtually `Z^2` group; it does not convert an arbitrary
Euclidean finite tile set into one Euclidean shape. The paper also warns that
enlarging the allowed isometry group can create additional tilings.

### Literal fusion is not enough

Gluing one fixed multiset of the source prototiles into a repeating macro-tile
would impose fixed rational component ratios. The Sturmian construction uses
irrational pattern frequencies. A successful monotile must therefore encode
source types contextually—through locally recoverable environments or
orientations—not merely bundle one fixed copy of every source tile.

## Precise theorem candidate ST-M1

Let `alpha = sqrt(2)-1`, and let `X_alpha` be the complete decorated
Sturmian-lattice tiling space from Section 10.1 of
`akiyama-hamada-ito-sturmian-2026`.

Construct a compact polygonal topological disk `P_alpha` such that copies may
be placed by the full Euclidean isometry group and:

1. at least one tiling of the plane by `P_alpha` exists;
2. there is a finite-radius, translation-equivariant map
   `pi : X(P_alpha) -> X_alpha` defined on **every** `P_alpha` tiling;
3. a translational period of a `P_alpha` tiling is a period of its image under
   `pi`.

Item 3 follows from ordinary equivariance once `pi` is a genuine local map.
Since every tiling in `X_alpha` realizes an irrational Sturmian lattice and has
no nonzero translational period, items 1--3 prove that `P_alpha` is an
aperiodic monotile. Neither injectivity, MLD, nor surjectivity is needed for
this minimal period-exclusion theorem.

There is a distinct strengthened target:

4. `pi` is surjective onto the complete positive-entropy space `X_alpha`.

If item 4 is proved, monotonicity of topological entropy under factors gives
`h(X(P_alpha)) >= h(X_alpha) > 0`, even if `pi` is not injective. Without
surjectivity, the image of `pi` might be a zero-entropy subsystem, so positive
entropy of the monotile hull remains unproved. The design must state whether
it seeks only ST-M1's aperiodicity conclusion or this stronger
positive-entropy monotile conclusion.

The actual mathematical burden is concentrated in two lemmas:

- **congruence encoding:** represent the three decorated source types by
  locally distinguishable states of one support;
- **no-spurious-tilings:** prove that every shape-only tiling decodes to a
  legal source tiling, with no periodic branch created by forgotten colors,
  reflections, non-edge-to-edge contacts, or alternative orientations.

The second lemma is the analogue of the decisive all-tilings step in the Hat,
Turtle, and Spectre proofs. Producing one attractive encoded patch does not
address it.

Because the intended mechanism is arithmetic rather than a deterministic
substitution hierarchy, a proposed proof must identify the geometric local
data that force the Sturmian line sequences and prove that the forcing works
simultaneously in every lattice direction used by the source construction.

## Novelty and characterization boundary

A solution of ST-M1 would give a Sturmian-derived monotile mechanism outside
the golden Hat--Turtle parameter family at the level of construction. Calling
the resulting tiling system genuinely independent requires a separate audit.
The source system's positive entropy and its `Q(sqrt(2))` arithmetic are
promising discriminants, but neither is promoted here as a proved MLD or
topological-conjugacy obstruction. That belongs to a later characterization
theorem.

## Dated searches

Primary-source searches run on 2026-07-21 included:

- `aperiodic tile set single connected unmarked monotile encoding Wang tiles`;
- `tile set monotile encoding` and `tileset monotile aperiodic`;
- `single prototile Wang tiles plane matching rules`;
- `2025 2026 Sturmian lattice monotile`;
- `2025 2026 aperiodic monotile construction tile sets`;
- `matching rules substitution tilings theorem finite prototiles`.

They returned the sources audited above, marked/atlas monotiles,
finite-prototile matching-rule theorems, Hat-family follow-up work, and group
monotiles. No source located in this search states ST-M1 or a generic
shape-only Euclidean tile-set-to-monotile conversion. This is a dated absence
report, not a proof that no such theorem exists.

## Claim permissions

Permitted:

- “Akiyama--Hamada--Ito construct infinitely many quadratic-slope aperiodic
  finite tile sets, not an infinite monotile family.”
- “Their `sqrt(2)-1` example uses three disk-like prototiles and has positive
  entropy.”
- “A faithful unmarked-monotile factor construction is explicitly left open
  by the source and was not supplied by the audited matching-rule, atlas, or
  poly-`K` theorems.”
- “ST-M1 is a source-backed open theorem candidate as of the dated audit.”

Not permitted:

- “The Sturmian paper already constructs new monotiles.”
- “One support up to color is an ordinary monotile.”
- “Boundary notches, atlas rules, or groupification automatically reduce a
  finite Euclidean tile set to one unmarked Euclidean shape.”
- “A local construction or one generated tiling proves ST-M1.”
- “Positive entropy or a different quadratic field alone proves system
  novelty.”

## Stop rule and next action

No runner is authorized. Before drawing or searching for shapes, write a
theorem-design note that (i) declares whether it targets minimal ST-M1 or the
surjective positive-entropy strengthening, (ii) chooses one arithmetic
congruence-encoding mechanism, and (iii) proves on paper why it can express
three states without external colors. If that note cannot state a plausible
no-spurious-tilings lemma forcing the required Sturmian line systems, close
the branch without computation.

## Design follow-up (session 63)

The requested on-paper design is now recorded in
`docs/theory/07_stm1_sturmian_monotile_design.md`. It selects minimal ST-M1
before the surjective positive-entropy strengthening and makes the full
Euclidean motion convention explicit. Reflected and mixed-handed placements
cannot be omitted: the proposed carrier would need a geometric chirality
separator making every whole-plane tiling homochiral, with a reflected decoder
on the opposite global branch.

The design also corrects a tempting source conflation. Section 10.1 proves
positive entropy for the three-prototile system; the `kappa=infinity` passage
only suggests one support up to color. No bridge between those statements is
presently proved. Extracting the complete colored equal-support source is now
the named source lemma ST-M1.S0.

Finally, an elementary no-go shows that three independent finite-state line
encoders cannot suffice: each nonempty one-dimensional sofic shift contains a
periodic point, and compatible independent periodic rails yield a periodic
plane configuration. Cross-direction intersection constraints are therefore
mandatory. The coupled contact-star architecture remains blocked because no
complete three-state symbolic kernel has yet been derived. No shape drawing
or computation is authorized by this follow-up.

## Equal-support follow-up (session 64)

The `kappa=infinity` passage has now been checked against the complete source
context. It does not close the equal-support source lemma for the optimized
`sqrt(2)-1` example. Section 8.1 uses the equidistanced trigonal model for BD
calculations; the later one-support suggestion occurs in the Turtle
subsection. The paper does not give a transported alphabet or an all-tilings
equivalence with the Section 10.1 three-prototile system.

`docs/theory/08_stm1_equal_support_compiler.md` proves the conditional part:
connected macrotiles over one congruent cell can be compiled into finitely
colored copies of that cell with unique local regrouping. The remaining
source-specific statement E-infinity must construct the common cell and prove
that the SAB/boundary language and irrational symbolic sequences survive.
Until then S0 stays blocked and K1 has no correct alphabet to encode.
