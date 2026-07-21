# K5S — a synchronizing twelve-state retiling topology

**Date:** 2026-07-22

**Status:** exact combinatorial topology and conditional unique-grouping lemma;
no unmarked polygon, boundary-color transducer or aperiodicity result

## 1. Target

K4W strategy A asks first for a bounded macrocell topology with at least 11
rooted exact retilings by congruent copies of one support. It also needs a
local invariant that could identify macrocell boundaries in every admitted
tiling. The present note supplies those two *topological* ingredients. It
does not claim that an unmarked polygon forces the admitted language.

Use the ordinary `1 x 2` domino as the exact support and a rooted `2 x 16`
rectangle as the macrocell. Write

```
V = one vertical domino, width 1,
H = two horizontal dominoes filling a 2 x 2 block, width 2.
```

A word in `V,H` is a composition of its total width into parts `1,2` and
specifies one exact domino retiling of a two-row rectangle.

## 2. Twelve selected retilings

Let `W_6` be the composition words of width 6 and let

```
W*_6 = W_6 minus {VVVVVV}.
```

For every `w in W*_6`, define the rooted macro retiling

```
R(w) = VVV H w H VVV.                         (1)
```

The first-piece recurrence

```
d_0 = d_1 = 1,       d_n = d_(n-1) + d_(n-2)
```

counts compositions by `1,2`. Hence `|W_6|=d_6=13` and `|W*_6|=12`.
Every word in (1) has width `3+2+6+2+3=16` and every retiling uses exactly
16 congruent dominoes: six in the two `VVV` collars, four in the two `H`
blocks, and six in the width-six middle. The 12 rooted words are distinct.
Thus this topology clears the 11-state count with one spare state and without
a component-frequency obstruction.

This is a selected subfamily of the rectangle's domino tilings. Geometry
would have to exclude every other retiling; selection on paper is not a
matching rule.

## 3. The delimiter

Concatenate two admitted words in the same two-row band. The terminal `VVV`
of the left macro and initial `VVV` of the right macro form

```
... H VVV | VVV H ... = ... H VVVVVV H ... .  (2)
```

Call the maximal run of six vertical dominoes in (2) a **six-bar**. No
six-bar occurs inside an admitted macro: each collar run has length three and
is isolated by `H`, while a width-six middle word other than `VVVVVV` has
every vertical run of length at most five. Consequently the six-bars occur
exactly at macro seams, and the seam is the unique midpoint between their
third and fourth columns.

## 4. Conditional unique grouping

Define the guarded strip language `G_16` by four extensional conditions on a
plane domino tiling.

1. Every tile belongs to a two-row band containing bi-infinite six-bars.
2. Consecutive six-bars in a band have seam midpoints 16 units apart, and the
   interval between them has form (1).
3. Six-bars in vertically adjacent bands have the same seam coordinates.
4. No other contact admitted by the eventual geometric carrier can imitate a
   vertical domino or a six-bar.

### ST-M1.K5S

Every tiling in `G_16` has a unique radius-16 partition into rooted `2 x 16`
macrocells, and every macrocell carries one of 12 locally visible states.

### Proof

A six-bar consists of six dominoes spanning one and the same pair of rows, so
it identifies that band without a chosen lattice origin. Maximality and (2)
identify the seam at its midpoint. Conditions 1 and 2 give the unique
sequence of width-16 intervals in each band. Condition 3 aligns these
intervals between bands, producing one rectangular macro grid. The word
between consecutive seams is read within distance 16 and recovers `w`.
Condition 4 prevents a second geometric interpretation of the marker.
Therefore grouping and state decoding are finite-radius and unique. □

## 5. What this does and does not buy

The six-bar is a genuine synchronization invariant, not an absolute lattice
residue: it is a bounded configuration of physical occurrences, and its
midpoint is recovered equivariantly from the tiling. It avoids the gauge
failure of N8/N9.

The bare domino does **not** enforce `G_16`. It admits many other tilings,
including periodic ones, and the selected words expose only a one-dimensional
composition channel. Their left and right collars are fixed, while the top
and bottom ownership words are correlated. Nothing here realizes the four
independently checked Wang interfaces.

The remaining geometric burden is finite and explicit:

- force precisely `G_16` with one connected unmarked polygon under full
  isometries;
- make the six-bar recognizable without external marks;
- route the four edge colors of 11 selected Jeandel--Rao states to four
  macro interfaces; and
- prove a complete contact atlas and one whole-plane lift.

Failure of the first two items closes this synchronized-domino
parameterization. It does not close other K4W inverse dissections.

## 6. One-channel no-go

Suppose an ordinary Wang presentation reads its interface colors only from
the boundary ownership pattern of (1). The west and east collars are fixed.
The two rows use the same `V/H` composition, so the north and south ownership
words are the same function `c(w)` of the state.

### ST-M1.N14

Every nonempty ordinary Wang shift obtained in this way has a periodic point.

### Proof

If the fixed east and west interfaces do not match, the shift is empty. If
they do, choose any admitted state `w`. Its north color is its south color
`c(w)`, so the constant configuration filled by `w` satisfies both horizontal
and vertical matching. It is doubly periodic. □

This no-go concerns the unaugmented ownership channel. Independently visible
docking states or a geometric transducer reaching the other sides are outside
its scope, but would be new obligations rather than consequences of K5S.

## 7. Why four independent square flips also fail

Partition a rooted `4 x 4` square into four rooted `2 x 2` quadrants. Each
quadrant has two domino retilings, horizontal and vertical, so independent
choices give 16 exact rooted retilings. The two quadrant bits incident to a
macro side form its boundary signature. Adjacent macros match precisely when
the two endpoint bits of their shared side agree.

### ST-M1.N15

No nonempty selection of these 16 four-flip states, with only the induced
side-overlap rule, is strongly aperiodic.

### Proof

The four quadrant bits are exactly colors on the four macro corners. A
selected macro retiling is therefore one allowed binary `2 x 2` corner block,
and side matching is the usual overlap of the two corner colors. The complete
macro language is a binary corner-coloring SFT. Hu--Lin Theorem 2.3, already
recorded as N11, says every nonempty such SFT has a periodic point. □

N15 is useful because the topology looks two-dimensional and clears the
11-state count, yet it has added no arity beyond the refuted B0 language.

## 8. A non-binary corner-carrier target

The preceding no-gos suggest a more natural source geometry. A macro can
carry one locally visible mode at each of its four corners; neighboring
macros literally share the corner mode, and an internal exact-cover gadget
admits only a fixed relation `A subset C^4`. This is corner coloring rather
than edge routing.

### ST-M1.K5Q (conditional)

Assume one unmarked polygon forces:

1. a unique finite-radius square macro partition;
2. one of `q` visible modes at each macro corner, shared consistently by all
   incident macros;
3. exactly the macro tuples in a fixed strongly aperiodic corner relation
   `A subset C^4`;
4. complete full-isometry contacts and one whole-plane lift.

Then it is an aperiodic monotile.

The proof is the same lift and period-descent argument as K4W, with the local
map reading corner tuples instead of edge colors.

Hu--Lin's introduction reports an earlier 44-tile aperiodic corner system on
six colors, but that source has not been audited here and is not yet a branch
dependency. If verified, its arity matches K5Q better than forcing the
11-state Jeandel--Rao edge presentation through a one-dimensional strip.

An exact finite carrier scaffold is easy to state but not yet to enforce. A
`20 x 20` domino macro can reserve four disjoint `2 x 5` corner sockets. Each
socket has eight exact retilings by the same recurrence, so six rooted modes
can be selected at each corner. Fixed domino-filled rectangles occupy the
remainder, including a two-row synchronization rail

```
VVV H H H H H H H VVV
```

of width 20. Adjacent rails create the same locally visible six-bar seam as
K5S. Thus the scaffold has ample exact retilings, four non-binary physical
ports and a credible synchronization invariant.

What is missing is decisive: an uncolored domino exact cover allows all
socket products and many non-scaffold tilings. A central gadget must realize
exactly `A`, and one polygon must force both it and the rail. Until that
coupling is constructed, the `20 x 20` object is a compiler-aware search
topology, not a tile candidate or a solution of K5Q.
