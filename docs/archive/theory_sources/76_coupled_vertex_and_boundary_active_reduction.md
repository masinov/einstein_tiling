# Coupled three-rail algebra and the boundary-active reduction

**Date:** 2026-07-29  
**Scope:** arbitrary finite carrier-local patches of the exact AHI
Section 10.1 source; source macrotiles remain wholly inside each carrier  
**Status:** exact local vertex algebra and an all-area boundary-neutral no-go;
contextual boundary-active compilers remain open

This note answers the question left by K67G/N67C at the correct two levels.
The coupled binary vertex algebra does **not** contain a new additive charge
capable of excluding an even trade.  The global rail continuation rule does,
however, prove that no count-changing trade can be invisible on the complete
marked carrier boundary.  Thus every surviving carrier-local compiler must
export its state through joint, boundary-active rail context.

No novelty claim is made for the elementary parity or propagation arguments.

## 1. K68V — the exact coupled vertex code

Fix a source index triple `i+j+k=0` and write the three corridor-width bits

```text
x_a=a_i,                    x_b=b_j,                    x_c=c_k.
```

The three cyclic rectangular cells incident to the indexed tiny triangle use
the transverse pairs `(x_b,x_c)`, `(x_c,x_a)`, and `(x_a,x_b)`.  By source
Definition 4 and the exact twelve-state quotient, a cell is mixed precisely
when its two bits differ.  Its coupled mixedness vector is therefore

```text
mu(x_a,x_b,x_c)
   = (x_b xor x_c, x_c xor x_a, x_a xor x_b).          (1.1)
```

Consequently

```text
mu_0 xor mu_1 xor mu_2 = 0,                            (1.2)
```

and the image is exactly

```text
E_3 = {000, 110, 101, 011}.                            (1.3)
```

Every element has exactly two lifts, exchanged by complementing all three
bits.  This is the coupled form of the three-axis contradiction used by
N60V: `111` is not a possible mixedness star.

The four types in (1.3) are not merely formal binary assignments.  They
occur in genuine irrational source lattices at
`alpha=sqrt(2)-1`.  Away from mechanical-word discontinuities, the bit at a
phase `rho` is one exactly when its fractional part exceeds

```text
q=1-alpha=2-sqrt(2).
```

The phase triples with fractional parts

```text
(1/3,1/3,1/3),
(1/5,1/5,3/5) and its permutations,
(2/3,2/3,2/3)
```

have representatives whose real sum is zero, as required by source Theorem
1.  The exact inequalities

```text
1/5 < 1/3 < q < 3/5 < 2/3
```

follow respectively from `sqrt(2)<5/3`, `sqrt(2)>7/5`, and
`sqrt(2)>4/3`.  They witness `000`, the three weight-two vectors, and again
`000` through the complementary `111` bit state.

### Integral consequence

The three nonzero incidence vectors

```text
v_0=(1,1,0),       v_1=(1,0,1),       v_2=(0,1,1)
```

generate the index-two lattice

```text
Lambda = {z in Z^3 : z_0+z_1+z_2 is even}.             (1.4)
```

Indeed their determinant has absolute value two and all three have even
coordinate sum.  Hence the only additive quotient of the local coupled
mixedness algebra is the parity already seen by K67G.  In particular,

```text
3(v_0+v_1+v_2)=(6,6,6),                                (1.5)
```

so the synchronized mixed-cell change required by `Delta k=2` lies in the
local incidence lattice.  Equation (1.5) is a method ceiling, not a legal
finite trade: macro exact cover, SAB geometry, and global rail continuation
have not yet been imposed.

## 2. Complete marked boundary data

A finite source patch has **complete marked boundary data** when every source
datum used by a local replacement is fixed on its interface:

- the common-rhombus frame and oriented corridor-bit germs;
- the continued SAB endpoint germs;
- the source edge and vertex stars crossing the interface; and
- the macro-address termination data.

Two same-support patches are **boundary-neutral** when these data agree.
This is stronger than having the same unmarked polygonal outline.  It is the
right notion because either member may then replace the other inside any
complete source tiling containing the first, without changing the exterior.
K66T deliberately did not assume boundary neutrality: contextual carrier
states may have different marked interfaces.

## 3. N68H — no count-changing boundary-neutral trade exists

### Theorem

No two globally admissible, same-support, boundary-neutral AHI source patches
have different numbers of large macros.  This holds at every carrier area.

### Proof

Let `P` and `Q` be such patches.  Since they are globally admissible, place
`P` in a complete source tiling `T`.  Complete marked boundary equality lets
us replace `P` by `Q`; the local source rules give another complete tiling
`T'` with exactly the same exterior.  The two corridor fields therefore
coincide outside one bounded set.

Fix any `a`-corridor bit `a_i`.  The strip between the indexed lines
`a=a(i)` and `a=a(i+1)` is unbounded.  It participates in infinitely many
cyclic cabinet cells obtained by varying a transverse index.  Choose one
whose support misses the bounded replacement region.  Its ordered
twelve-state label explicitly contains `a_i`, so exterior agreement gives
the same value of `a_i` in `T` and `T'`.  Repeat for every `i`, and cyclically
for every `b_j` and `c_k`.  Thus all three global rail words agree.

The ordered role of every common rhombus is determined by the appropriate
pair of these rail bits: `00` is `S`, `11` is `L`, and `01/10` is the signed
`M` state.  Hence the directional mixed-cell counts inside the common
support agree in `P` and `Q`.  K67D gives, on any axis `r`,

```text
M_r=N_r-3k_P=N_r-3k_Q,
```

where `N_r` is fixed by the support.  Therefore `k_P=k_Q`, contrary to a
count-changing trade.  QED.

This theorem is consistent with the source's positive-entropy Figure 45
interchanges.  Those replace one macro cover of a fixed corridor field by
another and preserve macro composition; N68H does not assert uniqueness of
the cover.

## 4. K68R — exact residual carrier-local class

Combine K66T, K68V, N68H, N63R, and K63F.  Every carrier-local compiler must
contain a count-changing pair of carrier states.  Such a pair cannot have the
same complete marked boundary by N68H.  Its state therefore changes
factor-visible corridor data exported to neighboring carriers.  That export
cannot be a product of three independently enforced rail languages, because
N63R then admits a periodic constant rail.  Nor can it be supplied solely by
the known boundary-neutral entropy flips, by K63F.

Thus the only surviving carrier-local realization class is

```text
boundary-active + joint multi-rail + contextual.                       (4.1)
```

This is an exhaustive reduction of the carrier-local architecture, not an
impossibility theorem for (4.1).  It also explains why another carrier-area
census cannot settle the problem: a viable state is not a compact defect in
one fixed source lattice.  It transports the Sturmian phase across carrier
interfaces.

## 5. What remains

The next theorem object is the finite phase-transport relation induced at a
carrier junction.  It must answer whether a boundary-active joint multi-rail
state can be enforced by one unmarked carrier while every whole-plane tiling
still decodes to the minimal irrational lattice hull.  There are three honest
outcomes:

1. a general periodicity/no-go theorem for all finite joint phase-transport
   relations in a specified contact family;
2. an exact nonseparable relation that remains total on the fixed AHI source,
   which becomes constructive input for shape synthesis; or
3. an undecidability boundary for a clearly defined class broad enough to
   include those relations.

Local additive vertex charges are exhausted by K68V.  Boundary-neutral
carrier states are exhausted by N68H.  The fixed residual class (4.1), rather
than a new polygon or a larger carrier area, is the remaining carrier-local
problem.
