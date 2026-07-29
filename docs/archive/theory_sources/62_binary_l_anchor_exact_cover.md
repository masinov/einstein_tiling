# The binary `L`-anchor exact-cover normal form

## Scope

This note concerns only the exact Akiyama--Hamada--Ito Section 10.1 source
atlas reconstructed in SER1.  It does not claim that a polygon realizes the
atlas or that the two macro types are a new symbolic system.

## K53H — the role hexagons

In either 15-rhombus large template, restrict the exact internal-contact graph
to one role.  The three `L` vertices form one 3-clique.  The six `S` vertices
form two disjoint 3-cliques.  The union of the six primitive triangles carried
by any clique has six unit boundary edges and six boundary vertices, hence is
one regular unit hexagon.  The remaining six addresses have role `M`.

Thus each large macro is intrinsically

```text
one L hexagon + two S hexagons + six M connector rhombi.
```

This proves the source's stated `2S+L` hexagon composition directly in the
common-rhombus atlas and locates every one of its 15 addresses.

## K53B — exactly two rooted selector states

Use eighteen times the triangular-lattice coordinates of the `L`-hexagon
center as origin.  The unordered vectors to the two `S` centers are

```text
A: {(0,36),(36,0)},
B: {(36,36),(54,0)}.
```

Canonicalizing an unordered pair under all twelve lattice isometries gives

```text
A: {(-36,-36),(0,36)},
B: {(-54,-54),(-36,0)}.
```

They are different.  Since the source has exactly the two large templates,
macro type is therefore one binary rooted geometric relation rather than 30
unrelated address colors.

## K53E — exact-cover equivalence

Let a *rooted source block* be either of the two serialized 15-rhombus
stencils, rooted at its unique `L` hexagon, or the one-rhombus `M` block.
For the already-addressed source language, forgetting addresses and retaining
the rooted block cover is invertible:

1. every large source tile has one `L` anchor and selects exactly one of the
   two stencils by K53B;
2. source tiles have disjoint interiors and cover the plane, so the selected
   stencils and singleton `M` blocks form an exact cover; and
3. conversely, an exact cover by those stencils restores the macro name and
   every address from its position in the serialized stencil.

The statement is deliberately about the exact-cover enhancement of the
twelve-state rhombus field.  It does **not** say that arbitrary locally
plausible twelve-state rhombus tilings possess such a cover.  Proving that a
single unmarked polygon forces precisely this cover is the all-tilings burden.

## Construction consequence

The 31-state target has now separated into two source-native mechanisms:

```text
local cell state = SAB axis (3) x ordered corridor widths (2 x 2),
macro ownership  = one of two L-rooted exact-cover stencils.
```

A carrier need not display 31 colors.  It must make its two endpoint/contact
stars decode the twelve local states and must make the `L=11` cells act as
anchors for exactly one of the two finite stencils.  Failure of either property
on even one unrestricted tiling defeats total decoding.
