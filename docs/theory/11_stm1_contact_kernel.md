# ST-M1.K1 — contact-incidence kernel before quotienting

**Date:** 2026-07-21

**Status:** lossless compiler K1C proved in draft; every nontrivial quotient
and every geometric realization remain open

**Scope:** the full addressed minimal colored source S0 from theory note 10;
no polygon, boundary teeth, collar enumeration, or positive-entropy claim

## 1. Why the first kernel must be lossless

The role-only and independent-rail quotients fail. It would therefore be
circular to begin K1 by guessing which of the addressed source states can be
erased. The safe baseline is instead a lossless change of presentation: move
the source state from the interior of a colored triangle to its complete
contact incidence, prove an inverse on the entire local-rule space, and only
then ask whether any incidence distinctions are future-equivalent.

This baseline is not yet an unmarked tile. Its contact modes and vertex-star
relation remain symbolic matching data that a later polygon would have to
enforce by geometry alone.

## 2. Finite source presentation

Let `Y` be the S0 system on the standard triangular frame. Write `A` for its
finite addressed triangle alphabet. A state in `A` includes the macro type
and address, split-`M` half, source edge/SAB data, restricted order class and
gap symbols described in theory note 10.

Let `E` be the three directed sides of a rooted triangle. For every legal
oriented adjacency in `Y`, introduce a half-contact record

```
h = (a, e; b, e')
```

meaning that side `e` of source state `a` meets side `e'` of state `b`. Its
involution is `h_bar=(b,e';a,e)`. Retain also the finite allowed cyclic words
of corner records around a lattice vertex. These words include the I0 order
state and any O0 participant order used by S0.

The data are finite because `A`, `E`, the source edge rule and the source
vertex rule are finite. No occurrence census is used.

## 3. Kernel configurations

A `K_full` configuration is an edge-to-edge triangular-frame tiling in which:

1. the two half-contacts on every shared edge are involutes;
2. all three half-contacts incident with one triangle have the same first
   component `a`;
3. their side components are the three distinct sides of that rooted
   triangle;
4. every cyclic corner word is one of the transported legal source vertex
   words.

Condition 2 is the two-dimensional coupler. It prevents choosing the three
corridor directions independently: all incident directional contacts must
name one common addressed source state.

## 4. ST-M1.K1C — lossless contact-incidence compiler

There is a radius-one conjugacy between `Y` and `K_full`.

### Proof

Given `y in Y`, label each shared edge by the ordered pair of its two source
states and sides. Source vertex legality supplies condition 4. This defines a
radius-one map `F:Y -> K_full`.

Conversely, in a `K_full` configuration, condition 2 makes the first component
of the three incident half-contacts independent of the chosen side. Assign
that state `a` to the triangle. Edge involution gives exactly the neighboring
state named by each record, and the cyclic corner rule restores every source
vertex condition. The resulting configuration lies in `Y`. This inverse
`D` has radius one (indeed the center state is visible on its incident
contacts), and `D F` and `F D` are identities.

Rotations and reflections act simultaneously on `a`, the directed side and
the cyclic corner word, so the construction includes every source isometry
state without making the inverse multivalued. Translation equivariance is
immediate. \(\square\)

Since `Y` is nonempty and aperiodic in the minimal S0 proof draft, `K_full`
is likewise nonempty and aperiodic. More importantly for K1, the conclusion
holds on **every** configuration admitted by the stated contact rules, not
only on images chosen from `Y`.

## 5. What K1C does and does not accomplish

K1C supplies a finite, coupled contact-star language with a total decoder.
It is a universal recoding of the addressed source, not a novel reduction and
not a nontrivial quotient. The source state `a` is still written explicitly
inside every half-contact record.

A genuine K1 quotient must erase some of this information while retaining a
finite-radius inverse on its **full local closure**. In particular, it must
not merely preserve the intended image `q(K_full)`. It must prove that every
configuration satisfying the quotient contact and vertex rules decodes to
S0. This is exactly Q0's adversarial domain.

Nor does K1C imply geometric realizability. A single unmarked polygon has one
fixed boundary; it does not carry a freely chosen symbolic half-contact on
each occurrence. Later geometry must realize the permitted contact modes as
relative placements and must make every forbidden edge or vertex star
physically impossible, including T-junctions, sliding contacts and mixed
determinant classes.

## 6. Next bounded question

Before any table or shape is drawn, define a future-equivalence relation on
`K_full` contact records and prove the local inverse criterion:

> a proposed quotient is safe exactly when some fixed-radius quotient
> neighborhood determines the unique centered `A` state in every
> configuration of the quotient local-rule space.

The next session may prove this criterion and derive necessary invariants for
any merge. It may not guess a radius, enumerate collars, or infer safety from
source samples.
