# Minimal Sturmian targets eliminate source-language pruning

**Date:** 2026-07-28  
**Scope:** separable finite-port realizations whose total decoder targets the
irrational Sturmian-lattice hull; no claim about nonseparable junctions or
carrier--verifier fusion

## 1. The right target space

The positive-entropy patch-tile hull of Section 10.1 is not the smallest
aperiodic object that a monotile needs to decode.  Forget the interchangeable
patch choice and retain the three indexed line families.  For fixed irrational
`alpha`, let `L_alpha` be the translation hull of all triples of mechanical
words in source Theorem 1, with intercepts

```text
(rho_0,rho_1,rho_2) in (R/Z)^3,       rho_0+rho_1+rho_2=0.       (1.1)
```

The lower/upper choices at a discontinuity are included by taking the orbit
closure.  Every element is an irrational Sturmian lattice and therefore has no
nonzero translation period.

For ST-M1, a total local map to `L_alpha` is sufficient: any period of the
unmarked tiling would descend to a period of its lattice image.  Surjectivity
onto the decorated positive-entropy patch hull is not required.

## 2. K63M — the irrational lattice hull is minimal

### Theorem

For irrational `alpha`, the `Z^2` translation action on `L_alpha` is minimal.
Consequently `L_alpha` has no proper nonempty closed translation-invariant
subsystem.

### Proof

Use `(rho_0,rho_1)` as coordinates on the phase torus in (1.1).  Translating
the lattice indices by `(m,n,-m-n)` acts by

```text
(rho_0,rho_1) -> (rho_0+m alpha, rho_1+n alpha) mod 1.          (2.1)
```

Because `alpha` is irrational, `{m alpha mod 1:m in Z}` is dense in the
circle.  The product action (2.1) is therefore dense on the two-torus.

A finite lattice patch prescribes finitely many lower/upper mechanical-word
inequalities in the phases.  Whenever it occurs away from a discontinuity,
its phase set contains a nonempty half-open rectangle.  A patch at a
discontinuity is a limit of one of the adjacent lower/upper choices and occurs
in the same language; its cylinder is reached from a one-sided phase
neighborhood.  Density of (2.1) therefore makes every finite patch recur in
the orbit of every phase.  Every orbit is dense in the coded hull, proving
minimality.  This is the standard minimality proof for a Sturmian shift,
applied independently in two phase coordinates with the third fixed by
(1.1).  QED.

### Decoder corollary

Let `X` be any nonempty compact tiling space and let

```text
pi:X -> L_alpha
```

be continuous and translation-equivariant.  Its image is nonempty, compact
and translation-invariant, hence equals `L_alpha` by K63M.  Thus **totality
already forces surjectivity onto the minimal lattice target**.

This does not imply positive entropy: `L_alpha` is the zero-entropy lattice
factor, not the interchangeable Section 10.1 decoration hull.

## 3. K63D — finite component decomposition of every separable realization

Fix a marked finite-port carrier presentation `Y` with a local factor

```text
lambda:Y -> L_alpha.
```

For an independent two-participant profile assignment, K62P partitions the
directed ports into finitely many paired biclique components.  Call this
finite datum a **component scheme** `C`, and write `B_C` for its complete
profile-compatibility relation.

Define

```text
Y_C = {y in Y : every physical port contact of y lies in B_C}. (3.1)
```

This is a closed translation-invariant subsystem because violation is visible
at one contact.

### Theorem

Every nonempty separable finite-port realization with a total decoder to
`L_alpha` determines a component scheme `C` satisfying

```text
Y_C is nonempty,              lambda(Y_C)=L_alpha.             (3.2)
```

Conversely, every separable construction must begin with one of the finitely
many schemes satisfying (3.2); K62P realizes its two-body profile relation,
but whole-plane totality and exclusion of spurious unmarked tilings remain
separate obligations.

### Proof

The profiles of a proposed unmarked tile induce `C`.  Decoding a tiling gives
a marked configuration whose every contact is geometrically compatible, so
the image lies in `Y_C`.  Nonemptiness of the unmarked hull makes `Y_C`
nonempty.  The composite map to `L_alpha` has compact invariant image and is
therefore surjective by K63M, proving (3.2).

There are finitely many component schemes on a finite port set.  K62P gives
the exact rational profile construction for any fixed scheme.  That
construction alone does not prove that all its tilings lie in `Y_C`, so no
converse monotile claim is made.  QED.

K63D is the promised decomposition of the entire separable branch.  It
replaces the vague phrase “choose a smaller aperiodic subsystem” by finitely
many exact component schemes, each of which must still cover the **whole**
minimal Sturmian-lattice hull.

## 4. N63R — every rail-separable scheme is periodic

Let `w` be a mechanical Sturmian word of slope

```text
alpha=sqrt(2)-1 < 1/2.
```

Its complete length-two language is

```text
00, 01, 10,                                                   (4.1)
```

and `11` does not occur.  Indeed, two consecutive ones would make the height
over a length-two interval equal two although `2 alpha<1`.  Each word in
(4.1) occurs because the corresponding interval of the irrational circle
rotation has positive length.

The bipartite adjacency graph of (4.1) is connected:

```text
L:1 -- R:0 -- L:0 -- R:1.                                    (4.2)
```

By K62P, any independent two-body profile realization preserving the whole
Sturmian rail must also accept the missing corner `11`.  It therefore accepts
the constant-one periodic rail.  Applying the same completion independently
to the three line families gives a periodic triangular-frame configuration,
so no such rail-separable presentation has a total decoder to `L_alpha`.

For an irrational slope above `1/2`, exchange zero and one: `11,10,01` force
the missing periodic corner `00`.  Thus the conclusion holds for every
irrational binary Sturmian slope.

### Corollary

Language pruning cannot rescue:

1. one independent profile alphabet per Sturmian rail;
2. a product of three independently enforced rail languages; or
3. any component scheme whose only state is a single rail's adjacent width
   pair.

K63M is load-bearing here: a nonempty decoder image cannot omit one of the
three essential bigrams in (4.1).  N63R strengthens the earlier 1D-SFT
periodic-point observation N1 by identifying the exact profile-component
collapse.

## 5. What remains for the exact AHI/Stade compiler

### K63E — factor-visible contacts cannot be pruned

Call a marked contact cylinder `U subset Y` **lattice-visible** when membership
in `U` is the inverse image, under `lambda`, of a nonempty finite-patch
cylinder in `L_alpha`.  Every such contact is essential in every total
realization.

Indeed, the decoder corollary gives `lambda(Y_C)=L_alpha`.  Choose a lattice
configuration in the finite cylinder defining `U`; it has a preimage in
`Y_C`, so that preimage contains the contact.  Equivalently, minimality makes
the contact recur in the decoded image of every nonempty realization.  A
language-pruned component scheme may therefore delete only contacts that
distinguish points in one fiber of `lambda`.  It cannot delete a corridor
width, a finite three-rail patch, or any other datum already determined by the
Sturmian lattice.

This is stronger than the statement that the three rails themselves cannot be
pruned.  It moves the whole loophole into the auxiliary decoration fiber.

### K63F — the published entropy flips do not change boundary components

Suppose two finite marked patches have the same geometric support and the
same complete exposed port data.  Replacing one by the other changes no
external contact in a separable component scheme: every boundary port and
every physically possible mate is literally unchanged.  Restricting which
member of such a pair is used can change the decorated subsystem, but cannot
disconnect its external required-contact graph.

The two Figure 45 relations reconstructed in K55I have exactly this form.
Their two sides have congruent common support and are local interchangeable
pairs in the source matching language.  Consequently the explicit
positive-entropy choices presently known for Section 10.1 cannot rescue a
separable erasure by contact pruning.  They are fiber choices, but they are
**boundary-invisible** fiber choices.

This does not assert that K55I exhausts the complete fiber of the Section
10.1 factor map.  It does show that the source's stated reason for positive
entropy supplies no missing profile alphabet.

## 6. U3 — no algorithm classifies all finite marked extensions

There is a precise computability boundary behind the remaining fixed-instance
question.  Define `COMPONENT-COVER_alpha` as follows.  An input consists of

1. a finite two-dimensional SFT `Y`;
2. a specified finite-radius factor `lambda:Y -> L_alpha`; and
3. a finite component scheme `C` on the presentation's contacts.

The question is whether `Y_C` from (3.1) is nonempty.  This problem is
undecidable, even with `alpha` and the Sturmian factor fixed.

To prove it, fix one nonempty finite presentation `Y_0 -> L_alpha`.  Given an
arbitrary Wang shift `W`, take

```text
Y = Y_0 x W
```

and use the universal component scheme, so `Y_C=Y`.  Then

```text
Y_C is nonempty  <=>  W is nonempty.
```

The right side is the domino problem.  The reduction is the symbolic core of
U2 and does not claim undecidability for one unmarked polygon.  Its role here
is different: it proves that a theorem which accepts an arbitrary finite
Sturmian extension and decides all of its component schemes cannot exist.
Any complete positive result must exploit the special structure of the fixed
AHI presentation, or restrict the auxiliary layer as D3 does.

## 7. The reduced fixed-instance problem

The universal component scheme is already periodic by N62S.  N63R now removes
every nonuniversal scheme that merely separates the three narrow/wide rails.
K63E removes every scheme that deletes a factor-visible contact, and K63F
shows that pruning the published interchangeable-pair entropy does not alter
external components.  Any surviving separable scheme must therefore encode a
**joint multi-rail fiber context not generated by the known boundary-neutral
flips**, while remaining surjective onto `L_alpha`.

There is also a source-specific finite alphabet reduction.  P0's positive
mixture coefficients force every decoded Section 10.1 tiling to contain the
singleton `small_M` type with positive frequency and at least one of the two
large types with positive frequency.  Since `large_A` and `large_B` have the
same composition vector, composition alone does not force each one
separately.  Up to deletion of an entire macro type, the only possible
essential alphabets are therefore

```text
{large_A, small_M},
{large_B, small_M},
{large_A, large_B, small_M}.                              (7.1)
```

The third is the contact-complete source already covered by N62S after the
Stade conversion.  Thus a genuinely new separable source restriction must
live over one of the first two alphabets, or must retain all three while
forbidding a proper subset of boundary-distinct fiber contacts.  Equation
(7.1) is not a nonemptiness claim for either two-type subsystem; deciding
their existence is part of the remaining source theorem.

For the Stade carrier this becomes one finite, source-specific question:

> Which intrinsic port contacts occur in the marked stick tilings over every
> phase cylinder of `L_alpha`, and is there a nonuniversal biclique component
> scheme containing all of them?

Answering it requires the port-to-source-cylinder map for one fixed AHI
presentation.  The generic Stade rule table and the finite contact quotient
are serialized, as are the reconstructed `31` AHI addresses, but the complete
extensional AHI edge/vertex table and its Wang-to-stick instance are not.  The
functorial D0 proof does not substitute for that table.  K63E/K63F permit this
map to quotient out all rail-visible cylinders and the two known Figure 45
flip pairs first; only genuinely boundary-distinct fiber states need separate
rows.

The next constructive datum is therefore **SER2**, not a polygon: serialize
the finite map

```text
Stade port contact -> AHI source state/side/vertex cylinder              (5.1)
```

and prove it covers every phase in `L_alpha`.  Then each component scheme has
an exact outcome:

- its restricted source is empty;
- it misses a phase cylinder and cannot be a total decoder;
- or it covers `L_alpha`, in which case it is the only legitimate separable
  profile alphabet to geometrize and must still pass the no-spurious-tilings
  converse.

No further separable boundary synthesis is justified before (5.1) exists.
