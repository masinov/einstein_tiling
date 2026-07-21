# ST-M1.K3F — flag-carrier reduction

**Date:** 2026-07-21

**Status:** exact colored recoding in proof draft; no unmarked polygon,
geometric atlas, or novelty claim

## 1. Change of granularity

K2J asked one physical polygon occurrence to represent one triangular source
cell and expose three contextual corner potentials. That makes the six
potentials incident at a source vertex properties of six sectors of one
geometric junction. HC-09 found no shape making those sectors independently
visible.

K3F changes which object a physical occurrence represents. One source
triangle is subdivided into three congruent **flag carriers**, one per source
corner. The K2C corner potential is then a state of its own carrier
occurrence. Six source sectors at a source vertex are six distinct
occurrences, so K2V separation is physical at the combinatorial level rather
than a six-bit state assigned to one point.

This is not fixed fusion of the three source prototile types. Every source
cell, regardless of its contextual state, contains exactly three flag
carriers. Irrational source-state frequencies remain frequencies of contact
contexts, not rational component counts inside one macro.

## 2. Exact common support

Let `ABC` be an equilateral triangle, `O` its centroid and `M_AB`, `M_BC`,
`M_CA` its edge midpoints. The three closed quadrilaterals

```
K_A = A M_AB O M_CA,
K_B = B M_BC O M_AB,
K_C = C M_CA O M_BC
```

have disjoint interiors and union `ABC`. Rotation by 120 degrees permutes
them, so they are congruent. After scaling by `2`, their cyclic side lengths
are

```
1, 1/sqrt(3), 1/sqrt(3), 1
```

and their angles are `60,90,120,90` degrees. Call this support the corner
kite `K`.

The segment `O M_AB` is the internal interface between the `A` and `B`
flags. Thus every source edge has one corresponding internal flag interface
inside each incident source face. The half-segments `A M_AB` and `M_AB B`
are external interfaces to the adjacent source face.

## 3. Colored flag alphabet

Start with the finite K2V presentation. For a source face `F` with decoded
state `a`, side modes `x_AB,x_BC,x_CA`, branch/tag data and, on the base
branch, K2C potentials `q_A,q_B,q_C`, create three flag states

```
(F,A): (a,A,q_A-or-blank,x_CA,x_AB,branch/tag,source ports),
(F,B): (a,B,q_B-or-blank,x_AB,x_BC,branch/tag,source ports),
(F,C): (a,C,q_C-or-blank,x_BC,x_CA,branch/tag,source ports).
```

The fresh branch uses a blank potential and retains its common fresh tag.
Internal interface `O M_AB` requires the same face state and branch on its
two flags and, on the base branch,

```
q_B-q_A = parity(x_AB)  mod 2.
```

The other two internal interfaces carry the cyclic equations. The three
flags at `O` must have roles `A,B,C` in cyclic order and the same fresh tag
when on the fresh branch. This is exactly K2C.

Across a source edge, the two half-edge contacts transport the directed K1P
data of the adjacent source states. The four flags meeting at its midpoint
must describe one common source edge relation. At a source vertex, retain the
six incident flag states in cyclic order and apply the existing source vertex
rule. No equality is imposed between their six `q` values.

## 4. K3F theorem

**ST-M1.K3F.** The finite colored K2V triangular presentation and the colored
corner-kite presentation above are mutually locally derivable.

### Proof

Forward subdivision is local: split every source face by its centroid and
edge midpoints and copy the face, side and sector fields into the three
displayed flag records. K2C supplies all internal equations; source edge and
vertex legality supplies the midpoint and six-sector rules.

Conversely, the role/cyclic rule at every `120`-degree centroid groups exactly
three flags. Internal equality recovers one source face state and its three
side modes. The midpoint rule recovers one legal source edge, and the
six-sector rule recovers the source vertex word. Replacing every flag trimer
by its equilateral union gives the inverse local map. Both compositions are
the identity after forgetting the deterministic subdivision. \(\square\)

Consequently a shape-only realization of the complete flag language, plus
one lift, would still imply minimal ST-M1 by the already proved period-descent
chain.

## 5. What this removes

K3F removes two burdens specific to the one-triangle/one-polygon carrier.

1. The three K2C potentials are no longer three independently variable
   sectors of one rigid occurrence. They belong to three occurrences.
2. The six K2V sectors at a source vertex are no longer six colors that one
   geometric point must store. They are the ordinary cyclic states of six
   incident carriers.

The ternary parity condition is realized by a physical three-cycle of binary
variables and pairwise internal interfaces. This is the exact topological
factorization N5 allowed only after auxiliary variables were introduced.

## 6. What remains

K3F is still colored. One unmarked polygon `P`, congruent in every occurrence,
must force:

- the corner-kite scaffold and unique flag-trimer grouping;
- two finite internal-interface relations and the centroid cyclic rule;
- the paired external half-edge relation and complete four-flag midpoint
  rule;
- the six-flag source-vertex rule without identifying the six potentials;
- absence of sliding, alternate or unrecorded subdivisions/T-junctions,
  mixed-handed contacts and additional whole-plane components; and
- a lift of the fixed K1P witness.

Call this geometric obligation K3G. It is not solved merely by converting
colored edges to jigsaw profiles, because that conversion normally produces
one shape per colored flag state. The remaining problem is now an exact
**single-support contextual color-erasure** problem on a fixed four-interface
carrier, rather than a ternary state stored inside one polygon.

## 7. Compiler-aware inverse-geometry target

Any later search should take the K3F language as input rather than enumerate
polygons blindly. A candidate shape must provide a finite primitive-contact
atlas together with a map

```
primitive contacts/vertex stars -> K3F interfaces and vertices
```

that is total on the candidate's complete local closure, surjective on one
fixed witness, and compatible with the inverse K3F decoder. The cheap filters
are therefore, in order:

1. finite contact vocabulary and no continuous sliding;
2. forced corner-kite scaffold and trimer roles;
3. exact internal parity/branch relation;
4. midpoint and six-sector vertex completeness;
5. homochirality; and only then
6. whole-plane witness lifting.

This turns search into constrained inverse realization of a known finite
language. It does not make K3G finite or decidable until a bounded polygon
parameterization and a contact-completeness lemma are supplied.

## 8. HC-11 kill condition

Within HC-11, K3F may advance toward geometry only if an on-paper boundary
mechanism explains how one unmarked support realizes more than one flag state
and states a finite completeness proof. If no mechanism survives, freeze K3G
without a shape run and retain Section 7 only as the specification for a
future compiler-aware search.
