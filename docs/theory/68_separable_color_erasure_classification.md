# Separable two-body color erasure is completely classified

**Date:** 2026-07-28  
**Scope:** one-support erasures obtained by replacing marked ports independently
inside disjoint collars; every decoded interface has exactly two participants
and uses the complete rooted port

## 1. The realization family

Let `T` be one connected polygonal carrier with a finite set `E` of directed,
unit-length boundary ports and a finite allowed relation

```text
R subset E_plus x E_minus.
```

The two copies of `E` record the two sides of an oriented interface.  If
reflections are admitted, first take the directed reflection double cover, so
endpoint reversal and handedness are part of a port role.

A **separable collar erasure** replaces each marked port `e` by a rooted simple
polygonal profile `p_e` inside a collar disjoint from every other port collar.
It must satisfy all of the following.

1. The two endpoints and the carrier's corner sectors are unchanged.
2. An intended port contact has the unique endpoint-to-endpoint alignment
   inherited from `T`.
3. The relative interior of the collar has exactly two tile participants; no
   third occurrence or other boundary arc enters it.
4. After the two carrier interiors are put on opposite sides, their collars
   cover gaplessly with disjoint interiors exactly for the pairs in `R`.

Clause 4 is relation-exact, not merely correct on a selected list of known
whole-plane tilings.  This is the most general independent two-body jigsaw
replacement of a finite marked edge relation.  The profiles may have any
finite polygonal complexity and arbitrarily small rational coordinates.

Call a bipartite relation **rectangular** when

```text
R(e,f), R(e',f), R(e',f')  =>  R(e,f').                (1.1)
```

Equivalently, any two nonempty row neighborhoods are equal or disjoint.

## 2. K61R — exact classification

### Theorem

A finite directed port relation has a separable collar erasure if and only if
it is rectangular.  Equivalently, every nontrivial connected component of its
bipartite compatibility graph is a complete bipartite graph.

The criterion is decidable by a finite row-intersection test, and every
positive instance has an effective rational polygonal-profile construction.

### Necessity

Put a rooted unit port in canonical coordinates, with endpoints `(0,0)` and
`(1,0)` and carrier interior above it.  There is one fixed endpoint-reversing
isometry `J` that puts a second carrier on the opposite side.  Two profiles
meet gaplessly in the declared two-body collar precisely when

```text
p_e = J(p_f).                                           (2.1)
```

Thus a rooted profile has exactly one complementary rooted profile.  If
`R(e,f)` and `R(e',f)`, then `p_e=p_e'`.  If also `R(e',f')`, equation (2.1)
gives `p_f=p_f'`, hence `R(e,f')`.  This proves (1.1).

Another useful form follows immediately.  If two row neighborhoods intersect,
use (1.1) in both orders to show that each contains the other.  They are equal;
therefore the compatibility graph is a disjoint union of bicliques.  QED.

### Sufficiency

For every nontrivial biclique component `C`, choose a distinct asymmetric
rooted rational zigzag `q_C` in an arbitrarily shallow unit collar.  Assign
`q_C` to all plus-side roles of `C` and its exact complement `J(q_C)` to all
minus-side roles.  Choose the zigzags with different finite tooth words and
with an endpoint-asymmetry marker, so profiles belonging to different
components or reversed directed roles cannot coincide.  Give isolated roles
unmatched profiles.  Because the collars are disjoint, all replacements can
be made simultaneously without changing connectivity or corner sectors.

The resulting profile pairs coincide exactly on the bicliques, proving
sufficiency.  All vertices can be rational.  QED.

This is the familiar jigsaw-color construction stated as a classification,
not a novelty claim.

## 3. N61S — Stade's marked stick is outside the class

The fixed weave rules in Stade's construction already violate (1.1), before
any input-dependent `A/B` constraints are added.  For every stick length
`n>=5`, consider the four port roles

```text
e  = z1,      e' = a1,      f = a2,      f' = b1.
```

Rules 1--11 allow

```text
R(z1,a2),       R(a1,a2),       R(a1,b1),
```

but rule 9 forbids `R(z1,b1)`.  The later arrow and triangle rules add
forbiddances only among `a-y`, `c-y`, `a-x1` and `b-z2` pairs, so none of
these four facts changes.  They are exactly the three true corners and one
false corner of (1.1).

### Corollary

No member of the factor-preserving marked Sturmian stick family U2 can have
its complete matching relation erased by independent two-participant port
profiles on the same connected support.  This holds for every simulated Wang
system, including the fixed AHI product family.

The second staple in Stade's geometric conversion is therefore not an
inessential filler within this class.  Its third-party occupation of the
dent--dent cavities is what escapes rectangularity.

## 4. What this closes, and what it forces next

The theorem closes the entire **separable two-body self-stapling family**, not
one profile word or one polygon.  Testing membership is finite: compare every
pair of row neighborhoods, or find a forbidden `3-of-4` rectangle such as the
one above.

It does not prove that one unmarked Sturmian polygon is impossible.  Any such
polygon derived from U2 must violate at least one family hypothesis.  Hence it
must use one of the following genuinely different mechanisms:

1. a third tile occurrence or a T-junction inside a rule-checking interface;
2. a context-dependent port whose state is jointly fixed by more than one
   boundary arc of the same occurrence;
3. a fusion construction in which a copy simultaneously occupies carrier and
   verifier regions rather than modifying ports independently; or
4. a proof that the missing corner of a nonrectangular local relation can
   never occur in any whole-plane carrier tiling, so relation-exactness can be
   weakened without admitting a spurious tiling.

The fourth option still needs an all-tilings theorem; checking only intended
weave tilings is insufficient.  Thus the next constructive target is no
longer an unspecified boundary profile.  It is a nonseparable, multi-port or
multi-participant self-stapling theorem with a total decoder.
