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

## 7. Two different quotient obligations

Let `F:Y -> K_full` be K1C. Let `q` be a finite symbol map from the full
contact records to a smaller alphabet `Q`, extended equivariantly to
configurations. For a fixed presentation radius `rho`, define

```
Z_rho(q) = {z : every radius-rho patch of z occurs in q(K_full)}.
```

There are two logically separate questions.

1. **Image resolving:** does `q(x)` determine `x` for configurations already
   known to lie in `q(K_full)`?
2. **Local-closure totality:** does every `z in Z_rho(q)`, including a
   configuration assembled from compatible intended patches but absent from
   the image, decode to `Y`?

The first question is a conjugacy question. The second is Q0's
no-spurious-configurations obligation. Passing the first does not imply the
second because a two-dimensional factor image need not equal any prescribed
finite local closure.

## 8. ST-M1.K1R — compact image-resolving criterion

The restriction `q:K_full -> q(K_full)` has a finite-radius inverse if and
only if it is injective on whole-plane configurations.

### Proof

A finite-radius inverse implies injectivity. Conversely, `K_full` is compact
and its finite-alphabet image is Hausdorff. A continuous bijection from
`K_full` to `q(K_full)` therefore has a continuous inverse. Continuity at the
center cylinder gives, for every source state, a finite quotient
neighborhood deciding that state. Compactness and finiteness of the source
alphabet give one uniform radius. Translation equivariance transports the
center rule to every cell. \(\square\)

Equivalently, failure occurs when two distinct full configurations have the
same quotient image. If ambiguity can be produced at arbitrarily large
radii by globally extendable paired patches, compactness extracts such a
whole-plane pair. Thus a proposed merge needs a **uniform context-separation
proof**, not agreement through several sampled radii.

K1R supplies no decision procedure for injectivity. In dimension two that
would be an unjustified leap. It identifies the exact infinite proposition a
finite proof must establish.

## 9. ST-M1.K1T — finite local-closure certificate

Fix `rho`. The quotient presentation is safe with an exact source lift if and
only if there are a radius `R` and a map `delta` from centered radius-`R`
patches occurring in `Z_rho(q)` to the addressed source alphabet `A` such
that the following finite-local identities hold on every sufficiently large
patch occurring in `Z_rho(q)`:

1. applying `delta` at neighboring centers satisfies every source edge and
   vertex rule of `Y`;
2. rebuilding the lossless contacts with `F` and applying `q` reproduces the
   centered quotient contact data.

### Proof

If such `delta` exists, apply it at every cell of any `z in Z_rho(q)`.
Condition 1 puts the resulting configuration in `Y`; condition 2 says
`q(F(delta(z)))=z`. Hence `delta` is a total finite-radius right inverse on
the entire quotient SFT.

Conversely, any finite-radius right inverse supplies its centered local rule
`delta`. Membership of its output in the finite-type source and the right-
inverse identity are checked on a bounded enlargement of its radius, giving
conditions 1 and 2. \(\square\)

K1T is the finite certificate contract for a future quotient. “Finite” here
describes the logical witness once `q`, `rho`, `R`, and the patch-domain are
given; it does not authorize enumerating those objects or increasing `R`
until a merge appears.

By Q0, any nonempty quotient satisfying K1T is aperiodic. K1R is necessary
for K1T but not sufficient: K1R controls only the intended image, whereas K1T
controls all of `Z_rho(q)`.

## 10. ST-M1.N3 — the one-symbol frame quotient fails

If all contact records and corner data are erased, the remaining system is
the uncolored edge-to-edge equilateral-triangle frame. It has the standard
periodic triangular tiling. Therefore it cannot admit a total equivariant map
to the irrational S0 source.

This does not rule out one unmarked geometric carrier. Such a carrier may
have several relative contact modes arising from different offsets or poses.
N3 says those modes—or some equally strong contextual data—cannot all be
erased at the symbolic stage.

## 11. Present K1 status

The lossless K1C presentation and the exact K1R/K1T contract are established
as proof drafts. No nontrivial map `q` has been proposed, and no merge is
known safe. The source alphabet is still defined functorially rather than
serialized, so even a bounded merge table would currently lack an auditable
domain.

The next on-paper question is structural: determine which source information
must remain invariant under every K1T-safe quotient, and whether those
invariants already require explicit macro identity. Failure would close the
selected contextual-carrier route before geometry. No enumeration is
authorized.
