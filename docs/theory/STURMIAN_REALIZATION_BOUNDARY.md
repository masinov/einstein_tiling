# The Sturmian monotile realization boundary

**Status:** canonical research statement, 2026-07-29
**Goal:** construction, nonexistence or undecidability for a precisely defined
connected-unmarked realization family

This document states the project-level Sturmian problem after consolidating
the AHI-specific branch.  It separates established general theory, one exact
source benchmark and the genuinely unresolved geometric theorem.

## 1. The problem

Let `S` be a computably presented, nonempty, aperiodic planar FLC tiling
system.  Determine whether there exists a compact connected unmarked
polygonal disk `P`, placed under the declared Euclidean isometry convention,
such that:

1. `P` tiles the plane;
2. a finite-radius translation-equivariant map

   ```text
   pi:X(P)->X(S)                                         (1.1)
   ```

   is defined on every tiling by `P`; and
3. the output of every tiling is a legal point of `X(S)`.

By Theorem 2.1 of `GENERAL_REALIZATION_THEOREMS.md`, these conditions make `P`
an aperiodic monotile.  Injectivity and surjectivity are unnecessary for
aperiodicity.

Surjectivity is a distinct stronger target.  If `X(S)` has positive entropy
and `pi` is onto, entropy monotonicity gives

```text
h(X(P)) >= h(X(S)).                                      (1.2)
```

Without surjectivity, the image may be a zero-entropy subsystem.

The project accepts three meaningful terminal outcomes:

- construct such a `P` for a Sturmian source;
- prove nonexistence for an architecture-independent realization class; or
- prove undecidability for a clearly specified computable family of connected
  unmarked supports while identifying meaningful decidable subfamilies.

## 2. Why the source is not the hard part

Akiyama--Hamada--Ito construct finite colored aperiodic tile sets from
quadratic Sturmian lattices.  Their Section 10.1 system at

```text
beta=sqrt(2)-1
```

uses three disk-like physical prototiles and has positive topological entropy.
The source explicitly leaves the monotile question open.  Its supports, color
rules and Ammann-bar-like data do not become an unmarked monotile by forgetting
the colors.

More generally, every finite colored local system already has routine Wang,
atlas and finite-state presentations.  `GENERAL_REALIZATION_THEOREMS.md`
shows that rooted T-junction chains can express every finite local relation.
Thus source alphabet size and local rule expressivity are not the bottleneck.

The hard quantifier is:

```text
every unrestricted tiling by one unmarked support.       (2.1)
```

## 3. Current logical boundary

| Realization category | Status | Qualification |
|---|---|---|
| Finite colored SFT with a fixed aperiodic factor | available | Standard finite presentation |
| Arbitrary symbolic compiler nonemptiness | undecidable | Product with a fixed nonempty aperiodic source |
| One connected polygon plus finite edge rules | undecidable, conditional | Product reduction plus Stade's unrefereed all-tilings weave converse |
| Two connected unmarked polygonal supports | undecidable, conditional | Stade's geometric staple construction |
| One connected unmarked polygon | open here | No audited construction, impossibility theorem or undecidability reduction |

The last row is not a cosmetic removal of markings.  Independent two-body
jigsaw erasure realizes only biclique relations, and the complete Stade stick
relation lies outside that class.  Contact-complete physical weakening still
preserves an explicit periodic stick tiling.

## 4. The exact AHI benchmark retained by the repository

The repository independently reconstructed one finite presentation of the
AHI Section 10.1 system.  The finite, cold-verifiable facts are:

- physical template sizes `30,30,2` in primitive triangles;
- common-rhombus component counts `15,15,1`;
- 31 addressed rhombus roles and 44 internal contacts;
- a twelve-state quotient

  ```text
  Z/3 x {0,1} x {0,1};
  ```

- one `L` hexagon, two `S` hexagons and six `M` connectors in each large
  macro; and
- two full-isometry classes of the rooted large-macro arrangement.

These facts establish a precise benchmark source.  They do not establish one
unmarked carrier or transfer the source's entropy.

The canonical fixtures are under `data/sturmian-source/`; the primary source
and reconstruction boundary are documented in the literature catalog.

## 5. What the AHI branch actually excluded

Under explicit hypotheses, the branch closed:

1. binary domain-wall and affine pose-local encodings of the reconstructed
   source;
2. root-deterministic finite carriers;
3. independent complete two-participant port erasure;
4. contact-complete separable erasure of the Stade stick;
5. carrier-local P17 decoding;
6. carrier-local AHI decoding below and at area 30;
7. carrier-local boundary-neutral count-changing trades at every area;
8. an ordinary participant-separable sector star for the AHI parity relation;
9. fixed-topology participant-wise torsion-free additive parity tests; and
10. the unbroken convex-flank realization of one parity zipper.

Only items 2--4 and 8--9 contain source-independent statements.  The other
items are benchmark facts about one source or one realization family.

None excludes:

- arbitrary connected unmarked polygons;
- decoders whose source macrotiles cross carrier boundaries;
- nonseparable contact hyperedges;
- context distributed across several boundary arcs;
- a larger-radius whole-plane exclusion with a proved total decoder; or
- a different Sturmian source presentation.

## 6. Local expressivity is already solved

The reusable hierarchy is:

```text
independent two-body profiles    -> biclique relations only
ordinary/additive joint tests    -> cannot detect ternary parity
rooted hidden-state T-junctions  -> every finite local relation
```

The final line subsumes the former AHI parity zipper: it is simply the
`Z/2`, length-three automaton instance.  More local states, delimiters, combs,
reset vertices or source addresses therefore do not reduce the distance to
the monotile theorem.

The unresolved step is not compiling a relation after roles are granted.  It
is forcing the roles, contact topology and grouping by the shape of one
support in all tilings.

## 7. Positive construction contract

Any future polygon proposal must be accompanied from inception by all of the
following obligations.

### 7.1 Exact support and existence

- exact algebraic or rational coordinates for one connected topological disk;
- at least one complete whole-plane tiling or a finite construction theorem;
- declared allowed isometries and treatment of reflections/mixed handedness.

### 7.2 Intrinsic roles

- every compiler role is recoverable from a bounded neighborhood of the bare
  unmarked boundary;
- roles are not colors renamed after observing an intended patch;
- congruent copies realize every required state.

### 7.3 Complete contact language

- all full-edge, partial-edge, T-junction, point, reflected and
  non-edge-to-edge contacts are classified;
- sliding, overhang and maximal-segment subdivision are included;
- unintended contacts either decode legally or are proved absent.

### 7.4 Total grouping and decoder

- every whole-plane tiling has a bounded grouping into compiler complexes;
- grouping ambiguity, if allowed, does not change the decoded source;
- every admitted local patch decodes, source adjacencies are legal and
  re-encoding reproduces the input language.

### 7.5 Periodicity gate

- every proposed support is tested immediately against exact positive
  periodicity criteria;
- a local encoded patch is never treated as evidence for aperiodicity;
- period exclusion is claimed only through the total map (1.1) or another
  complete theorem.

This contract intentionally places the no-spurious-tilings theorem before
shape optimization.  The retired hinge octagon passed local role and closure
checks but admitted a periodic two-copy fundamental domain that never used its
intended compiler state.

## 8. Negative and undecidability programs

A meaningful impossibility theorem must quantify over an architecture that
is recognizable outside this repository.  Examples of viable scopes are:

- all separable complete two-participant collar erasures;
- all ordinary sector-star realizations of a specified relation;
- all carrier-local fixed-area fusion decoders;
- all one-support realizations whose contact complex has a stated bounded
  arity or decomposition property; or
- a computably presented unmarked family broad enough to support an
  undecidability reduction.

The theorem must state which hypothesis an arbitrary polygon may violate.
Closing another hand-chosen boundary word is not a family theorem.

For undecidability, the exact missing bridge is a **shape-only self-stapling
reduction**: geometrize a sufficiently rich marked relation using one
connected unmarked support while proving the all-tilings converse.  Theorem
4.1 of the general synthesis shows that independent two-body collars cannot
provide this bridge for nonrectangular relations.  A successful reduction
must therefore use nonseparable multi-port context, a third participant,
carrier--verifier fusion or a global redundancy theorem.

## 9. Decidable islands

The known undecidable classes contain useful decidable restrictions:

- directed-graph auxiliary layers reduce to directed-cycle existence;
- fixed-width cylinder layers reduce to a finite transfer graph;
- rectangular two-body relations are decided by row-neighborhood equality;
- physical separable erasure is decided by biclique closure avoiding the
  forbidden physical graph; and
- finite carrier-local composition libraries admit exact frequency-cone
  rejection certificates.

These are genuine family classifications.  A larger research program may ask
whether the one-unmarked-polygon boundary decomposes into analogous decidable
islands around an undecidable core.

## 10. Research disposition

The AHI-specific zipper, comb, reset, thin-lens and carrier-size ladders are
closed as active research directions.  Their exact proofs remain historical
case studies and verifier fixtures.

Reopening the constructive branch requires one of:

1. a source-independent one-support erasure theorem;
2. a scoped unmarked undecidability reduction;
3. a complete polygon satisfying Section 7; or
4. a new source theorem that changes the global realization problem rather
   than merely changing its finite presentation.

The project should measure future work by which obligation in Sections 1, 7
or 8 it closes—not by the number of local lemmas or candidate families it
produces.

## 11. Evidence and claim boundary

The exact AHI artifacts are benchmark evidence.  The general proofs are
internal proof drafts and mostly instances of established symbolic, jigsaw or
finite-state ideas.  The marked undecidability result is explicitly
conditional on an unrefereed preprint.  No repository result currently
establishes:

- a Sturmian aperiodic monotile;
- nonexistence of all Sturmian monotiles;
- undecidability for one connected unmarked polygon;
- surjectivity onto the positive-entropy AHI hull; or
- novelty of the finite-state contact compiler.

The detailed AHI branch provenance remains in `83_ahi_branch_closure.md` and
the row-level statuses remain in `PROOF_LEDGER.md`.
