# K6R — boundary forcing for the K5C corridor

**Date:** 2026-07-22

**Status:** on-paper mechanism test; the fixed-successor rosette is refuted;
no polygon, computation or monotile result

## 1. The admitted mechanism

The HC-14 audit leaves only a geometric question.  A finite automaton,
delimiter and interface wires are already standard.  One boundary must make
those data unavoidable in every ordinary gapless tiling by one connected
unmarked polygon.

The simplest exact candidate is a **keyed successor rosette**.  Give the
polygon one intrinsically distinguishable head contact and one tail contact.
Their full-arc fit fixes one relative isometry `g`.  Require every occurrence
to use its head once and its tail once.  If `g` is a rotation through
`2*pi/42`, the tempting conclusion is that the contact components are
42-cycles and therefore realize K5C.1.

The following formulation separates what that idea really proves from the
root and state information it does not carry.

## 2. Fixed-successor model

Let `P` be a compact polygonal topological disk with trivial Euclidean
stabilizer.  In a locally finite tiling by congruent copies of `P`, suppose a
locally recognizable directed contact relation `s` satisfies:

1. every occurrence has exactly one successor and one predecessor;
2. if an occurrence is placed by `f in E(2)`, its successor is placed by
   `f g`, for one fixed intrinsic isometry `g`; and
3. the proposed K5C root and word are functions only of the resulting directed
   contact component, not of additional contacts to another structure.

The trivial-stabilizer hypothesis merely avoids treating two poses of `P` as
the same rooted occurrence.  It is natural for a tile whose head and tail are
intrinsically directed.  A symmetric support can be handled in the quotient
by its finite stabilizer, with the same conclusion for a freely acted-on
component.

## 3. N17: a fixed successor cannot carry a rooted word

### ST-M1.N17

In the fixed-successor model, a finite component of `m>2` distinct
occurrences is a rotationally symmetric `m`-cycle.  No Euclidean-equivariant
local decoder from that component can select exactly one root or assign a
nonconstant cyclic word.  In particular the proposed order-42 rosette cannot
satisfy K5C.2--K5C.3.

### Proof

Starting from an occurrence `f(P)`, repeated successors are

```text
f(P), f g(P), f g^2(P), ... .
```

If these first return after exactly `m` distinct occurrences, then
`f g^m(P)=f(P)`.  Trivial stabilizer gives `g^m=id`, while exact length gives
no smaller positive power equal to the identity.

A finite-order Euclidean isometry is either the identity, a reflection of
order two, or a rotation.  Since `m>2`, `g` is a rotation of exact order `m`.
In global coordinates the conjugate `h=f g f^{-1}` leaves the unmarked
directed component invariant, moves each occurrence to its successor and acts
transitively on the `m` occurrences.

Let a Euclidean-equivariant local decoder select a unique root occurrence.
Applying `h` leaves the input component unchanged as an unmarked set and must
move the selected root to its successor.  Uniqueness also requires the root
to remain the selected root.  The action is free on occurrences, a
contradiction.  The same transitivity makes every occurrence's intrinsic
rooted neighborhood congruent, so any equivariantly assigned symbol is
constant around the cycle.  A unique delimiter and eleven distinct rooted
K5C words are therefore impossible.  □

## 4. Scope

N17 does not say that finite contact cycles are impossible.  It says that one
repeated docking transform supplies closure but erases the asymmetry K5C needs
for a root and a state.  External contacts could break the rosette symmetry,
but then the root/state is carried by those contacts and condition 3 no longer
holds.  Such a proposal must specify that second structure and prove its
gapless contact completeness; calling it a keyed rosette does not discharge
K5C.2--K5C.3.

The theorem also does not cover a successor relation with several
independently visible docking transforms.  That is the only surviving variant
for the final HC-14 analysis.

## 5. Interim decision

The one-head/one-tail boundary mechanism fails before any coordinates are
drawn.  The order-42 turn can force a symmetric ring only under the already
strong one-successor hypotheses, and that very symmetry forbids the delimiter
and nonconstant code it was meant to support.

The remaining question is whether several full-arc docking modes can be
exclusive in a gapless one-polygon tiling.  Session 99 resolves that bounded
question below.

## 6. N18: every boundary port must be filled

The first multiplexing attempt puts several disjoint keyed head arcs and
several matching tail arcs on `P`, intending a tile to choose exactly one pair
and leave the other options unused.

### ST-M1.N18

Let a locally finite family of compact topological disks tile the plane with
pairwise disjoint interiors.  Every point in the relative interior of a tile's
polygonal boundary edge belongs to the boundary of another tile.  Therefore
every nondegenerate arc in a disjoint option-port bank is contacted in every
tiling; “choose one port and leave the others unused” is impossible in an
ordinary gapless tiling.

### Proof

Let `x` be in the relative interior of a boundary edge of a tile `T`.  There
are points outside `T` arbitrarily close to `x`.  The tiling covers them, and
local finiteness lets us pass to a sequence covered by one fixed neighboring
tile `U`.  Since tiles are closed, `x` belongs to `U`.  It cannot lie in the
interior of `U`: an open disk there would meet the interior side of `T`,
contradicting disjoint interiors.  Hence `x` lies on `boundary(U)`.  □

N18 permits several neighbors to subdivide one port and permits neutral caps.
But those are additional contact roles whose complete arrangement must be
forced.  They do not make the unused options disappear.  In particular a
diagram showing one selected key while leaving the other key arcs exposed is
not a tiling mechanism.

## 7. N19: one full arc is not an arbitrary mode bank

The only immediate escape from N18 is to multiplex alternatives on the same
full contact arc.

### ST-M1.N19

Fix two nondegenerate compact polygonal boundary arcs `A` and `B`, each with
two distinct endpoints.  There are at most four Euclidean isometries taking
`A` onto `B` and its endpoint set onto the endpoint set of `B`.  Thus one
fixed full-arc pair cannot directly expose an arbitrary finite transition
alphabet.

### Proof

There are two bijections between the two endpoint sets.  For either ordered
endpoint assignment, an isometry of the plane has at most two choices: the
orientation-preserving rigid motion and its composition with reflection in
the line through the two target endpoints.  Requiring the whole arc to map
onto `B` can only remove choices.  Hence at most four remain.  If the local
interior sides are also prescribed to be opposite across the contact, at most
one of the two side choices for each endpoint order survives, but the
conservative bound four is sufficient here.  □

The bound is deliberately scoped to one specified full-arc pair.  Multiple
arc pairs return to N18.  Partial contacts, offsets and T-junctions are outside
N19, but they require an extensional contact atlas proving that no slide,
branch, overlap or unintended cap occurs—the very K5C completeness burden.

## 8. The two-mode holonomy residue is not a mechanism yet

An endpoint-reversing full-arc pair can plausibly expose two local docking
modes.  A chain could then spell a binary word, and the product of its relative
isometries could act as a closure test.  This is the strongest variant left by
N17--N19, but it does not meet the admitted contract:

- no arcs `A,B` or two placement isometries have been constructed;
- no proof makes every component a simple cycle of length 42 rather than a
  path, branch, other cycle or collision;
- no product calculation accepts exactly the eleven K5C words and rejects
  every other admitted word; and
- the two local modes reveal a bit, not the prefix-automaton state required by
  K5C.3.  Recovering a state after reading the completed word would be the
  circular labeling the contract forbids.

It could become a different exact holonomy mechanism only after all four
items are proved from one explicit boundary.  Naming the two alignments is not
such a proof.

## 9. HC-14 disposition

The admitted mechanism attempt has exhausted its variants:

1. one fixed successor transform yields a symmetric unrooted rosette (N17);
2. disjoint optional ports are all contacted in a gapless tiling (N18); and
3. one full-arc pair has at most four rigid alignments and supplies no finite
   selector by itself (N19).

No concrete boundary survives with K5C.1--K5C.3 proved.  The predeclared
HC-14 kill therefore fires.  K5C remains a useful conditional test instance,
but the cyclic-corridor route is frozen: no polygon search, contact-radius
escalation or drawing is authorized.

Reopening requires an explicit polygonal boundary and, before computation, a
proof draft giving: (R1) its complete full-contact modes; (R2) exclusive
bounded component closure; (R3) an independently visible accepting state or
an exact non-circular holonomy replacement; (R4) exclusion of every partial,
sliding and vertex contact; and (R5) one gapless whole-plane lift.  These are
geometric data, not a new symbolic compiler.
