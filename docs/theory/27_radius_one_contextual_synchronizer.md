# Radius-one contextual synchronization of the multiplexed host side

**Status:** proof-draft design; no polygon, candidate, or total decoder

**Checkpoint:** HC-21, fixed radius one

## 1. Fixed neighborhood

For an occurrence `P_0` and its intrinsic `H` side, define the closed
**radius-one H-star** `Star_1(H)` to contain:

1. `P_0`;
2. every tile occurrence whose closed support meets any point of the closed
   segment `H`, including occurrences meeting it only at a subdivision or
   endpoint vertex; and
3. the exact common boundary arcs, cyclic sector orders and intrinsic rooted
   side germs of those occurrences at points of `H`.

It contains no occurrence solely because it meets one of those neighbors
away from `H`.  Thus remote guard--shield terminal contacts are radius two or
larger and are unavailable in HC-21.

This radius is fixed before the theorem attempt.  If the data in
`Star_1(H)` do not distinguish all legal root contexts, HC-21 closes radius
one; it does not enlarge the neighborhood.

Under local finiteness, the compact segment `H` meets finitely many tile
occurrences.  A proposed finite certificate must additionally exclude
sliding families or serialize them honestly; finiteness is not inferred from
the desired three words.

## 2. The three intended classes

The desired radius-one decoder has codomain

```text
W = {shield, host_0, host_1}.                              (2.1)
```

Its first observable is the ordered cover word of `relint(H)`:

```text
shield  : [H]
host_0  : [A,B,C]
host_1  : [A,C,B].                                        (2.2)
```

The labels `host_0,host_1` are contextual states, not markings on the
polygon.  Reflections reverse rooted words in the usual way; the two selected
classes are the non-reversal states retained by K9A.

## 3. K12C: the radius-one certificate contract

### ST-M1.K12C

A finite radius-one contextual synchronizer for K10B consists of the
following exact data and proofs.

1. **Complete star language.** Every `Star_1(H)` admitted by any unrestricted
   tiling belongs to one of three finite star classes `S_H,S_0,S_1`, and their
   cover words are respectively those in (2.2).
2. **Disjoint decoding.** No rooted star belongs to two classes, including
   after every allowed reflection or intrinsic symmetry.
3. **Shield pose.** In class `S_H`, the full `H--H` contact fixes the K10B
   half-turn mate and its exact intersection with the root is the complete
   spine `S` with disjoint interiors.
4. **Host legality.** In `S_0,S_1`, every subdivision and point participant
   satisfies the K9A/K9T sector equations and decodes to the corresponding
   selected word.
5. **No hidden fourth class.** Partial covers, other length words,
   overhanging/sliding sides, different endpoint correspondences and extra
   point participants are all excluded within this same radius-one language.
6. **Lift.** Each of the three classes occurs in at least one globally legal
   source lift; absence is not used to fake completeness.

If these six clauses hold, the map reading the class of `Star_1(H)` is a
bounded, equivariant, total contextual decoder.  It accepts the deliberately
multiplexed `H` side without requiring atomicity.

### Proof

Clause 1 gives totality on the full radius-one local closure, not only on
intended patches. Clause 2 makes the value single-valued and compatible with
the full isometry convention. Clauses 3--4 give soundness of each decoded
value. Clause 5 prevents an unclassified tiling from entering through a
fourth local cover. Clause 6 prevents a vacuous symbolic language. All data
are contained in `Star_1(H)`, so the decoder is local and translation
equivariant. □

K12C is a certificate contract, not evidence that K10B meets it.

## 4. Admission questions and stop

Sessions 119--120 ask only:

1. What cover words are forced or permitted by the exact K9A length and
   adjacent-sector algebra at radius one?
2. Does that algebra already produce a fourth class?
3. If so, does any already-proved radius-one interaction exclude it without
   importing remote K9T terminal contacts or coordinates?

If a fourth locally compatible word survives and no current radius-one
theorem excludes it, K12C remains open and HC-21 closes radius one.  A larger
context, a coordinate search, or a new boundary word requires a later human
checkpoint.

## 5. Forced transition closure

K9A gives

```text
ell_B=ell_C=theta,
rho_A=rho_B=rho_C=pi-gamma-theta.                    (5.1)
```

Therefore the same four-sector equation used for every selected adjacency
also holds for `B|B`:

```text
rho_B+gamma+ell_B
  =(pi-gamma-theta)+gamma+theta
  =pi.                                               (5.2)
```

This is not one of the four selected transitions, but it is inseparable from
them by the existing angle data.  The clean-spoke equations also assign the
same right and left spoke lengths to every `B` occurrence.  K9T's terminal
sector classes admit every left role in `{A,B,C}` and every right role in
`{B,C}`, so they do not distinguish a `B|B` guard complex either.

Transitions into `A` remain forbidden because `ell_A!=theta`.  Hence a
code-only cover of `H=7` must begin with its sole `A=1`; the remaining length
six is a word in `B=2,C=4`.  The nonnegative solutions of

```text
2*n_B+4*n_C=6
```

give exactly

```text
[A,B,C],       [A,C,B],       [A,B,B,B].             (5.3)
```

up to no reordering beyond that displayed.  Covers involving `d` would add
possibilities for special choices of `d`; they cannot remove (5.3).

## 6. N29: factorized radius-one algebra admits a fourth class

### ST-M1.N29

Any radius-one acceptance proof which factors into:

1. the K10B side-length sum;
2. independent K9A primary-junction angle and clean-spoke equations; and
3. the K9T left/right terminal angle classes,

accepts the additional cover word `[A,B,B,B]` whenever it accepts both
`[A,B,C]` and `[A,C,B]`.

### Proof

The length identity is `1+2+2+2=7`.  Its three directed adjacencies are
`A|B,B|B,B|B`.  The first is selected, while (5.2) proves the other two have
the same exact sector sum; the common clean-spoke length equations apply.
The word begins with allowed left role `A` and ends with allowed right role
`B`, so the factorized K9T terminal classes also accept it.  Every listed
factor therefore accepts the word. □

N29 establishes algebraic local compatibility, not a polygonal star.  Full
occurrences placed at its three subdivision points might still overlap away
from `H`; such a collision lies inside `Star_1(H)` and could provide the
non-factorized geometric exclusion K12C needs.  No existing coordinate-free
lemma proves that collision.

## 7. Exact remaining radius-one alternatives

After N29, a K12C proof must supply at least one new radius-one fact:

- the intrinsic `B|G|B` primary star is geometrically impossible despite its
  exact sector and spoke equations;
- two or more individually legal primary complexes in `[A,B,B,B]` force an
  overlap among their full occurrences; or
- another feature already visible on `H` couples the subdivision count and
  permits exactly three code occurrences.

Declaring “three pieces” as a rule is not a geometric proof.  Remote K9T
terminal contacts are outside the fixed radius and cannot close HC-21.
