# Full-side rooted hinge compiler

**Date:** 2026-07-27

**Status:** HC-40 exact port-incidence theorem and candidate template; no
closed polygon, complete placements or monotile

## 1. Root endpoint roles

Let the intrinsic complete root sides `H,D` be distinct. For both K46S states
to use the same unmarked polygon, each root side must offer both angle roles:

```text
endpoints(H)={alpha,beta},       endpoints(D)={alpha,beta}.   (1.1)
```

At each rooted endpoint, denote the other incident complete side by
`x_(alpha,H)`, `x_(beta,H)`, `x_(alpha,D)`, or `x_(beta,D)`.

### ST-M1.K47P

The two rooted hinge states have complete full-side germ placements if and
only if, after choosing orientations of `H,D`,

```text
x_(alpha,H) = x_(beta,D) = X,
x_(beta,H)  = x_(alpha,D) = Y.                       (1.2)
```

Here equality means congruent unmarked side germs, including length and any
already-intrinsic endpoint context. `X` and `Y` may be distinct.

### Proof

In state 0, the `alpha` occurrence adjacent to `H` meets the `beta` occurrence
adjacent to `D` along each reflected off-axis ray. Complete full-side contact
forces the first equality in (1.2). State 1 similarly pairs `beta` at `H` with
`alpha` at `D`, forcing the second.

Conversely, align reflected copies along the two root rays and use the equal
side germs from (1.2) on the off-axis rays. K45H's sector equation fills the
neighborhood without overlap, giving both boundary-germ placements. □

The converse is local: it does not say the four complete polygons remain
disjoint beyond the matched side germs.

## 2. Sector totality is automatic

### ST-M1.K47T

Inside the K45H reflection-invariant four-participant topology, if
`alpha+beta=pi` and `alpha!=beta`, the only gapless rooted sector stars are
the two K46S states.

### Proof

The selected stars contain two `alpha` and two `beta` sectors and sum to
`2*pi`. The two mixed alternatives put the same role at both roots, producing
four `alpha` or four `beta` sectors. The first would require
`4*alpha=2*pi`, hence `alpha=pi/2`; then `alpha+beta=pi` gives
`beta=pi/2`, contrary to `alpha!=beta`. The second is identical. □

Thus K46J's local-totality clause is discharged at sector level once the
reflection-hinge topology and intrinsic roots are established. Other contact
topologies at the same polygon vertices remain a later atlas obligation.

## 3. Exact rooted boundary template

Orient `H` from its `alpha` endpoint to its `beta` endpoint, and orient `D`
the same way. Equations (1.1)--(1.2) force the rooted fragments

```text
X -(alpha)- H -(beta)- Y,
Y -(alpha)- D -(beta)- X.                            (3.1)
```

Let `P,Q` be the two residual boundary arcs connecting the remote ends of
the two `Y` sides and the two `X` sides respectively.

### ST-M1.K47B

Every full-side carrier satisfying K47P has, up to reversal, the cyclic
rooted template

```text
H, Y, P, Y, D, X, Q, X,                             (3.2)
```

with the four root endpoint angles fixed as in (3.1). Conversely any simple
irredundant polygon with template (3.2), intrinsic distinct roles, and the
K45H angles realizes K47P at boundary-germ level.

If `P,Q` are required nonempty and contain at least one side each, the carrier
has at least eight sides. Equality is the smallest unresolved template.

### Proof

Starting along `H`, its `beta` endpoint forces the first `Y`; the other `Y`
must terminate at the `alpha` endpoint of `D`, with the residual arc `P`
between their remote ends. Traversing `D` reaches its `beta` endpoint and the
first `X`; residual arc `Q` joins it to the `X` ending at the `alpha` endpoint
of `H`. This is exactly (3.2). Reversing traversal gives the only alternate
rooted reading. The converse is direct from the four incidences. Counting
`H,D`, two `X`, two `Y`, and one side in each residual arc gives eight. □

## 4. Search value and remaining obligations

K47B converts arbitrary polygon generation into a word-constrained family:

1. choose `alpha in (0,pi)\{pi/2}` and set `beta=pi-alpha`;
2. choose distinct intrinsic side germs `H,D,X,Y`;
3. choose finite residual arcs `P,Q`;
4. solve global polygon closure and simplicity; then
5. test complete four-copy placements and finite contact termination.

No candidate may skip steps 4--5. In particular, the eight-side lower bound
is not an eight-gon existence result and is unrelated to the published
polykite size horizon.
