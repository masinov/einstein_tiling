# Binary plaquette and finite-radius audit for ST-M1.B0

**Date:** 2026-07-21

**Status:** primary-source audit in progress under HC-12; no experiment or
geometric construction

## Question and radius vocabulary

The K3B square-diagonal mechanism assigns one bit to each forced square
macrocell.  Three distinct radii must not be conflated:

1. **rule support**: the finite set of bit positions inspected by one allowed
   pattern;
2. **decoder radius**: the finite neighborhood needed to recover a colored
   source state; and
3. **geometric visibility**: the macrocells whose bits one contact or vertex
   gadget of the unmarked polygon can jointly constrain.

An arbitrary large decoder radius does not help when the complete geometric
language enforces only nearest-neighbor or one-corner rules.  Conversely, a
large rectangular rule support can remain binary and need not introduce more
physical prototile shapes.

## Exact substrate identification

The K3F flag carrier is exactly the repository's primitive kite cell after a
uniform scale, not merely a qualitatively similar quadrilateral.

For a cell `(C,M_{d-1},V_d,M_d)`, `substrate/kitegrid.py` gives angles
`60,90,120,90` and cyclic side lengths

```
sqrt(3), 1, 1, sqrt(3).
```

K3F gives angles `60,90,120,90` and lengths

```
1, 1/sqrt(3), 1/sqrt(3), 1.
```

Multiplication by `sqrt(3)` makes the two ordered metric polygons identical.
The existing integer hex-coordinate substrate, its full `D6` action and its
published-coordinate anchors therefore apply directly to the undeformed flag
scaffold.

This observation has two opposite consequences.  It makes later exact
geometry cheap, but any candidate that remains a union of at most 24 such
kites lies inside the published finite polykite horizon.  A free boundary
deformation or contextual retiling gadget is not automatically a polykite and
is not excluded by that horizon.

## Sources admitted to the audit

- `hu-lin-two-color-square-2011`: the peer-reviewed two-color corner- and
  edge-coloring nonemptiness theorem;
- `kari-moutot-low-complexity-2023`: the peer-reviewed binary rectangular
  recoding theorem and its exact local-closure lemma;
- `jeandel-rao-wang-2021`: the sharp 11-tile/four-edge-color Wang lower bound,
  used only to distinguish ordinary edge-colored Wang systems from binary
  corner plaquettes.

The theorem consequences and HC-12 decision are completed in the following
sessions.  No enumeration of the `2^16` binary plaquette rule sets is needed:
Hu--Lin already settle that class.
