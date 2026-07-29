# Exact source contact kernel and pose-local no-gos

**Date:** 2026-07-27

## 1. The extensional kernel (K50C)

Pairing the primitive triangles along the reconstructed SABs gives 31 rooted
rhombus addresses. Their complete macro-internal edge incidence consists of
22 contacts in `large_A`, 22 in `large_B`, and none in the singleton
`small_M`; 24 address states meet a macro boundary. Every rhombus side has
exactly one endpoint of its long-diagonal SAB.

The exact artifact is
`data/sturmian-source/ahi-section10-contact-kernel.json`. It records every
address, role, diagonal axis, four side germs, internal contact, and exposed
address. Its cold verifier rebuilds it from the source atlas rather than
trusting serialized counts.

## 2. Binary handedness cannot encode ownership (N53)

Consider the source-specific carrier family in which each occurrence has one
handedness bit and every macro-internal contact must join opposite bits. The
three `large_A` addresses

```text
large_A:0, large_A:1, large_A:2
```

are pairwise adjacent. The three internal equations are

```text
x0 + x1 = 1,
x0 + x2 = 1,
x1 + x2 = 1                 (mod 2).
```

The first two imply `x1=x2`, contradicting the third. Therefore the internal
source graph itself is not bipartite. No binary domain-wall compiler can
realize the published macro ownership, regardless of how its external
contacts are treated.

All 44 internal contacts join *different* long-diagonal axes. The obstruction
triangle uses all three axes. Consequently three geometric orientations are
the first natural state space, but orientation alone is not yet a decoder.

## 3. Affine orientation laws are insufficient (N54)

Let a primitive triangle be `(u,v,o)`, with `o` its up/down orientation, and
suppose its paired-rhombus axis is

```text
A(u,v,o) = a*u + b*v + c*[o=D] + d  (mod 3).
```

Requiring the selected adjacent triangle to select the same axis back is a
finite condition on the `3 x 3 x 2` residue classes. Exhausting the 81 exact
coefficient tuples leaves only

```text
(a,b,c,d) = (0,0,0,0), (0,0,0,1), (0,0,0,2).
```

These are the three constant-axis periodic lozenge matchings. Neither large
source template lies in any one of them. Thus the source pairing cannot be
recovered from a one-cell affine lattice residue. This does not exclude a
non-affine periodic scaffold or a contextual finite-radius decoder.

## 4. Construction consequence

The exact source has now ruled out both cheap erasures:

1. one binary tile-level phase cannot encode macro ownership;
2. one affine three-axis lattice phase cannot encode the rhombus pairing.

A viable unmarked carrier must expose a genuinely joint side or vertex state.
In particular, the state cannot be assigned independently to a tile before
its contact star is known. The next source task is to serialize the finite
`S/M/L` corridor-width state on each of the 31 addresses and determine the
smallest context that recovers macro ownership on the complete local closure.
This is source-specific quotienting, not another free carrier family.
