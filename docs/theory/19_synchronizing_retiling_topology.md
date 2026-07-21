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

## 9. Product-socket obstruction

The missing selector cannot be replaced by four independent guarded sockets.

### ST-M1.N16

Let the allowed corner tuples factor as

```
A = C_SW x C_SE x C_NE x C_NW,
```

with equality of the four incident corner modes at every macro-grid vertex.
Then the resulting corner language is empty or has a constant periodic
configuration.

### Proof

At any grid vertex, its color is simultaneously in `C_SW`, `C_SE`, `C_NE`
and `C_NW`, because it occupies those four roles in the four incident
macros. A whole-plane configuration therefore implies that the intersection
of the four sets is nonempty. Choose one color in the intersection and put it
at every vertex. Every macro then has an allowed tuple, giving a constant
doubly periodic configuration. □

Thus a fixed filler separating the four sockets destroys exactly the
coupling needed for aperiodicity.

## 10. Closed-corridor selector

There is a non-product topology that retains the K5S synchronization idea.
Let `T` be a fixed 11-tile, four-color Wang source and encode each color by
two bits. Since duplicate edge quadruples are irrelevant in a set, every
tile `t` has a distinct eight-bit word

```
b(t) = west(t) east(t) south(t) north(t).
```

Use a two-cell-wide **cyclic corridor** in one macrocell. Its abstract
adjacency graph is a cyclic ladder; an eventual Euclidean carrier must embed
it near the macro boundary. In a straight two-row piece, encode a bit by the
fixed-width exact domino word

```
E(0) = H VV,        E(1) = H H.             (3)
```

Both occupy a `2 x 4` rectangle and use four dominoes. Prefix the eight
encoded bits by

```
D = H VVVVVV H,                              (4)
```

which occupies `2 x 10` and uses ten dominoes. No payload contains a vertical
run longer than two, so (4) is the unique six-bar delimiter. The 11 selected
rooted cyclic words

```
z(t) = D E(b_1(t)) ... E(b_8(t))             (5)
```

all have longitudinal length 42 and use 42 congruent dominoes. Four fixed
two-bit windows, measured from `D`, expose the four Wang colors.

The finite set (5) has an explicit finite automaton: take the prefix trie of
the 11 rooted words, identify its accepting leaves with the root after the
closing contact, and omit every other transition. This is a constructive
finite object, although the source tuples still need serialization before a
cold table can be written.

### K5C geometric admission contract

One unmarked polygon realizes the closed-corridor selector only if:

1. its exact contacts force disjoint bounded cyclic ladders, rather than
   paths, merged cycles or a plane-spanning ladder;
2. the two exact bit blocks and delimiter are locally distinguishable before
   decoding a source state;
3. independently visible docking modes realize exactly the prefix-automaton
   transitions, not a label assigned after reading (5);
4. the unique delimiter roots four geometrically fixed readout windows;
5. contacts between neighboring cycles occur exactly when their exposed
   two-bit colors agree; and
6. the remaining area has a forced equal-count fill, with a complete
   full-isometry atlas and at least one whole-plane lift.

### ST-M1.K5C (conditional)

Any polygon satisfying K5C satisfies K4W and is an aperiodic monotile.

### Proof

Items 1--4 give a unique finite-radius macro partition and one of the 11
visible states (5). Item 5 makes the decoded macro configuration exactly a
valid `T`-tiling. Item 6 supplies tileability and covers every admitted
isometry. K4W period descent then excludes every translation period. □

K5C is the requested non-circular macro topology: one closed physical word,
not four independent labels, carries and couples all interfaces. It also
turns a future search into a compiler-aware problem—realize six finite contact
obligations—rather than blind polygon enumeration.

It is not a tile. The hardest step remains item 1 together with item 3: one
boundary must force finite rooted cycles and a multi-state automaton without
external colors. No such boundary word or completeness proof is supplied.

## 11. HC-13 disposition

The checkpoint's topology threshold is met by K5S and sharpened by K5C. N14,
N15 and N16 remove the three misleading cheap variants: a one-dimensional
ownership channel, independent binary quadrants and independent non-binary
sockets. The surviving exact-compiler search target is a rooted closed
corridor with an independently visible automaton.

No geometry run follows. HC-13 stops after its third session. Any next
checkpoint must first audit single-prototile simulation and geometric
synchronizing-frame prior art, then either propose one exact boundary
mechanism satisfying K5C.1--K5C.3 or close the cyclic-corridor route without
enumeration.
