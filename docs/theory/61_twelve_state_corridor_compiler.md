# The exact twelve-state corridor compiler

**Date:** 2026-07-27

## 1. Source quotient (K52Q)

Every common rhombus has one long-diagonal SAB axis and two ordered
transverse corridor widths. Write narrow as `0` and wide as `1`. The local
alphabet is exactly

```text
(axis, left_bit, right_bit) in Z/3 x {0,1} x {0,1}.
```

The source roles are recovered without an additional color:

```text
S = 00,       M = 01 or 10,       L = 11.
```

For an `M` cell the published bent SAB has direction word `r,(r+1),r` or
`r,(r-1),r`; its signed bend distinguishes `01` from `10`. Reflection swaps
the two bits. The exact vector lift gives one ordered-bit embedding for each
large template. The singleton `M` has exactly the two reflected embeddings.
Across the three templates, every one of the twelve states occurs.

The artifact `data/sturmian-source/ahi-corridor-quotient.json` records the
31 address states, both reflected singleton states, and the complete action
of the twelve triangular-frame isometries. Its cold verifier re-extracts the
signed SAB bends from the pinned source archive.

## 2. Pure pose is impossible (N56)

The action on the twelve source states has three orbits:

```text
{axis} x {00}       size 3,
{axis} x {01,10}    size 6,
{axis} x {11}       size 3.
```

The pose set of one symmetry-free polygon on one triangular frame is a
transitive `D6`-set. The image of an equivariant map from a transitive set is
transitive. Therefore no radius-zero pose code can cover the complete
twelve-state source alphabet. The numerical equality `|D6|=12` is
misleading: role must arise from contact context, not from orientation alone.

## 3. Source-native geometric contract (K52E)

A connected unmarked polygon `P` realizes the twelve-state compiler if every
unrestricted tiling by `P` satisfies all of the following.

1. **Frame and axis.** A finite-radius rule recovers a triangular rhombus
   frame and one of its three axes for every occurrence.
2. **Two contextual bits.** Two ordered, intrinsically rooted contact stars
   on an occurrence recover values in `{0,1}`; reflection exchanges them.
3. **Complete local state.** Exactly the twelve K52Q states occur; no
   additional mixed-handed or non-frame state survives.
4. **Macro totality.** The resulting state field has a unique finite-radius
   exact cover by the two 15-address templates and the singleton template in
   the serialized kernel K50C.
5. **Source contacts.** Every recovered macro boundary and contracted vertex
   satisfies the source edge/SAB rule, including reflections.
6. **Existence.** At least one source tiling lifts to a `P` tiling.

Under clauses 1--6, the macro decoder maps every `P` tiling to the irrational
AHI source. Equivariance transfers every period, so `P` is an aperiodic
monotile. This is a direct specialization of C0/Q0 to the exact source, not a
new general compiler theorem.

## 4. The remaining construction problem

Clause 4 is now the decisive symbolic question: do the twelve contextual
states force the 31-address macro ownership, or what additional bounded star
state is necessary? Clauses 1--3 identify the geometric mechanism to seek: a
rhombus-like carrier whose orientation gives the SAB axis and whose two
rooted endpoint stars each have exactly two legal completions. Boundary
synthesis before macro-totality is proved would repeat the earlier drift.

The construction will therefore work in this order:

1. decide the exact twelve-state-to-31-address macro cover on its full local
   closure;
2. if safe, realize the two endpoint bits by one polygon and prove the
   complete contact atlas;
3. if unsafe, preserve the smallest spurious periodic configuration and add
   only the bounded contextual state that distinguishes it.
