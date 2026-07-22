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
