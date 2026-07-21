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
exclusive in a gapless one-polygon tiling.  Session 99 must resolve that
bounded question or fire HC-14's kill for K5C.
