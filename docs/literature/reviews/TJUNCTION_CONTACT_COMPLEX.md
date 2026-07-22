# T-junction and subdivision-order contact complexes

**Audit date:** 2026-07-22

**Question:** is an intentional non-edge-to-edge contact, in which several
whole neighbor sides partition one host side, already a published route from
finite symbolic states to one unrestricted unmarked polygon?

## Decision

The general language is prior art, but the proposed geometric erasure step is
not supplied by the audited sources.

Smith--Myers--Kaplan--Goodman-Strauss already treat arbitrary finite **edge
patches**: several tiles may surround a connected common arc, vertices may
have three or more participants, and a complete locally consistent edge-patch
correspondence transports an entire tiling.  Thus neither T-junction atlases,
maximal-segment subdivision nor local contact-complex decoding is new.

Hellouin de Menibus--Lutfalla--Vanier show that finite local complexity lets
one simulate arbitrary symbolic rules over geometric tilings.  Their main
simulation adds labels and forbidden patterns to a pre-existing geometric
tiling space.  Their purely geometric undecidability construction uses a
finite machine-dependent shapeset.  Neither theorem compiles the states into
one congruence class whose unrestricted gapless tilings all decode.

Sugimoto proves that a single convex polygon admitting an edge-to-edge
monohedral tiling also admits a periodic one.  This preprint is used only as a
scope boundary: a shape-only aperiodicity mechanism cannot remain inside the
convex edge-to-edge class.  It says nothing against nonconvex tiles or
intentional subdivisions of one side by several neighbors.

No audited source states the narrower **subdivision-order carrier** proposed
for HC-15: one fully occupied host side is partitioned by unequal whole sides
of congruent neighbors, and the order of the unequal lengths is read as a
finite local state.  This dated absence report is not a novelty claim.  HC-15
may derive its exact capacity and obstruction lemmas, but may not call the
use of edge patches, T-junctions, FLC recodings or Wang simulation new.

## Primary-source anchors

### Spectre edge patches

In `smkgs-chiral-2024`, Section 2.2 defines an edge patch around a connected
component `e` of the intersection of two tiles, with every other participant
containing an endpoint of `e`.  A vertex is an interior point shared by at
least three participants.  Lemma 2.3 says that complete, locally consistent
edge-patch correspondences give combinatorially equivalent tiling spaces and
preserve translational periodicity.

This is broader than an edge-to-edge pair atlas and already includes the
topological object needed for a T-junction compiler.  The lemma is
conditional on having the complete edge-patch correspondence; it does not
construct one support that realizes a prescribed finite code.

The Hat paper's Appendix A likewise organizes arbitrary polygon contacts by
maximal boundary segments and aligned components.  Its result is specific to
the polykite alignment problem, not a general state-erasure construction.

### Wang potatoes and FLC

`hellouin-lutfalla-vanier-geometric-2026` carefully separates shapes from
symbolic-geometric tiles.  Definition 6 calls the all-tilings space of a
shapeset with no extra rules *purely geometric*.  Definition 10 gives FLC and
notes its equivalence to finiteness of two-tile patterns.

Theorem 13 makes the domino problem hard over any nonempty FLC geometric
tiling space by adding finitely many labels and forbidden patterns.  The
construction deliberately avoids geometric triple points when laying its
auxiliary grid; it does not exploit T-junctions as shape-only states.
Theorem 22 encodes computation into a finite purely geometric shapeset and
uses shear lines to make FLC undecidable.  This confirms that boundary
geometry and partial alignment can carry formidable symbolic structure, but
the construction has several machine-dependent shapes and does not provide a
single connected polygon or an all-tilings monotile decoder.

Cached PDF SHA-256:
`ec348a6bef3efea7da1affa2e7a756b632b52b3d0819ea1f13ac44a84ec8b252`.

### Convex edge-to-edge boundary

`sugimoto-convex-edge-2015`, Theorem 2, states that no single convex polygon
is an aperiodic prototile when edge-to-edge incidence is the only matching
condition.  The paper derives this from the periodic tilings available to
triangles, quadrilaterals, the classified edge-to-edge pentagons and
monohedral hexagons, together with the impossibility of a monohedral convex
polygon with seven or more sides.

HC-15 does not depend on this theorem for a positive conclusion.  It records
why an intentional non-edge-to-edge or nonconvex mechanism is not a cosmetic
variant of the simplest polygon class.

Cached PDF SHA-256:
`ad7a4486ebef1cedff14172e301c88453db58d485d70e39abe5266e65322c88f`.

## Exact residue admitted for HC-15

Fix one occurrence as a **host** and one of its straight boundary sides as a
closed interval.  A `k`-piece subdivision word is a contact patch in which:

1. exactly `k` other occurrences meet the host side in positive-length
   intervals with disjoint relative interiors;
2. those intervals cover the host side exactly;
3. each interval is one complete, intrinsically identifiable side of its
   neighbor; and
4. the `k-1` interior division points are ordinary T-junctions with no slide.

HC-15 may answer only the following bounded questions.

- How many order states can such a contact word distinguish under full
  Euclidean isometry?
- What endpoint-angle equations are forced at its internal T-junctions?
- Is there one explicit congruent-polygon patch realizing more than one
  state with disjoint interiors and exact coverage of the host side?

The result remains a local contact kernel.  It does not satisfy K5C or K4W
unless a later theorem forces every whole-plane tiling into a complete finite
atlas, supplies compatible interfaces, proves a lift and excludes periodic
fault tilings.

## Permitted and forbidden claims

Permitted:

- complete edge-patch and T-junction atlases are established proof objects;
- FLC geometric tilings support finite local symbolic recodings;
- a subdivision-order lemma may give a new repository search primitive or a
  scoped proof-draft if it survives a later targeted novelty review;
- the exact one-support all-tilings erasure problem remains unresolved by the
  sources audited here.

Forbidden:

- “T-junction matching is new”;
- “FLC makes a shape-only compiler automatic”;
- “a local junction with several states is an aperiodic monotile”;
- “absence from this audit proves the subdivision-order mechanism is novel”;
- any polygon search before the local lemma and its complete contact scope
  are written down.

## Dated searches

Primary-source searches on 2026-07-22 included:

- `aperiodic tiling T-junction edge subdivision permutation matching rules polygon`;
- `single polygon Wang tiles T junction partial edge contacts simulation`;
- `non-edge-to-edge tiling matching rules subdivided edge aperiodic monotile`;
- `tiling encode permutation order subdivided edge Wang tiles geometry`;
- `Decision problems on geometric tilings Wang potatoes`.

They recovered the sources above, the already-audited one-puzzle-piece,
atlas, marked-tile and jigsaw conversions, and secondary uses of T-junctions.
No primary theorem located in this search supplies the exact congruent-
polygon subdivision-order carrier and an unrestricted all-tilings converse.

## Stop rule

Session 100 is audit-only.  Sessions 101--102 may use on-paper exact geometry
only.  By the end of session 102 the fixed subdivision-word class must have
either:

1. one explicit polygonal contact patch with exact coordinates, disjoint
   interiors, more than one isometry class of fully occupied host-side
   states, and a complete statement of what remains unforced; or
2. a scoped theorem proving that the fixed class cannot carry an exclusive
   state under full Euclidean isometries.

No enumeration, SAT search, coordinate optimizer, SVG or candidate promotion
is admitted in HC-15.

## HC-15 outcome

Theory note 21 proves the interval-complex capacity `k!/2`, closes the
two-neighbor apparent bit by reflection, and derives the exact endpoint-angle
equation. It then proves N21: no convex complementary-port polygon realizes
the surviving three- or four-neighbor universal order channel. No exact
nonconvex witness was obtained, so the stop rule fired at session 102 without
an experiment. This outcome does not change the prior-art decision above and
does not establish novelty for the scoped lemmas.
