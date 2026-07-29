# Rooted binary reflection hinge

**Date:** 2026-07-27

**Status:** HC-40 exact symbolic-star theorem and admission contract; no
polygon, placement witness, local converse or monotile

## 1. The unrooted star carries no bit

K45H has two angle roles `alpha!=beta`, each occurring twice. Ignoring any
distinction between the two opposite mirror-axis contact rays, the two
possible cyclic assignments are

```text
alpha,beta,beta,alpha     and     beta,alpha,alpha,beta.       (1.1)
```

### ST-M1.N50

The two assignments in (1.1) are congruent under a half-turn about the hinge
point. Sector angles alone therefore carry no unmarked binary state.

### Proof

Rotation through `pi` exchanges the two opposite axis rays and shifts the
cyclic sequence by two places, sending the first word in (1.1) to the second.
With no intrinsic ray label, this is an allowed Euclidean isometry. □

## 2. Two intrinsic axis roots

Now require the two opposite axis contacts to have distinct unmarked geometric
germs `H` and `D`. Every admitted patch isometry must preserve their roles;
for example, a later carrier may use different complete side lengths or
different finite endpoint contexts. The names are hypotheses until such a
carrier is constructed.

### ST-M1.K46S

Assume K45H, `alpha!=beta`, and intrinsically distinct opposite roots `H,D`.
Up to reflection in the hinge axis, there are exactly two rooted sector stars:

```text
state 0: the pair adjacent to H has angle alpha;
state 1: the pair adjacent to H has angle beta.       (2.1)
```

They are not equivalent under the full Euclidean group, and the defining
reflection preserves each state.

### Proof

K45H forces each pair adjacent to one axis ray to share its angle role and
forces the opposite pair to use the complementary role. There are therefore
exactly the two choices (2.1). Reflection exchanges the two occurrences
within each pair but fixes both axis rays, hence preserves the choice.

Any isometry between the two rooted stars must map the unique `H` germ to
`H`. It would then have to map an `alpha` sector adjacent to `H` to a `beta`
sector adjacent to `H`, impossible because Euclidean isometries preserve
angles and `alpha!=beta`. The half-turn from N50 is unavailable because it
exchanges `H` and `D`. □

The exact values `alpha=pi/3`, `beta=2*pi/3` satisfy every sector equation and
the strict inequality.

## 3. K46J finite admission contract

A single unmarked polygon realizes the rooted binary hinge only if it meets
all six clauses below.

### ST-M1.K46J

1. **Intrinsic roles.** The polygon is symmetry-free and contains locally
   recoverable `alpha`, `beta`, `H`, and `D` boundary roles with
   `alpha!=beta`, `H!=D`.
2. **Sector algebra.** `alpha+beta=pi`, and both values lie in `(0,pi)`.
3. **Two placements.** Four congruent occurrences realize each state in
   (2.1), with exact contacts on both axis rays and the two reflected off-axis
   rays and with disjoint interiors in a full neighborhood.
4. **Finite termination.** Every ray contact extends to a named finite common
   boundary arc whose remote endpoint star is included; no dangling contact
   or unspecified continuation is allowed.
5. **Local totality.** Every legal completion involving an `H` or `D` root is
   locally one of the two selected states; spurious mixed angle/root stars are
   excluded geometrically.
6. **Decoder.** A finite-radius map reads state 0/1 from the `H`-adjacent angle
   pair and exports it to the selected compiler relation.

Clauses 1--6 are jointly sufficient for a local two-state junction gadget.
They do not prove a monotile: whole-plane tilability, grouping, and absence of
other tilings remain separate global obligations.

## 4. Logical boundary

K46S proves state capacity, not physical storage. In particular, declaring
`H,D` as labels would make the result a marked-tile construction. The next
step must derive their distinction from one boundary word and must realize
both angle roles at each root context; otherwise N50 applies.
