# Every carrier-local Sturmian compiler requires a count-changing AHI trade

**Date:** 2026-07-28  
**Scope:** every finite-area carrier-local realization of the exact AHI source;
no bound on carrier size

## 1. K66A — the complete arithmetic phase diagram

Let the common-rhombus carrier area be

```text
A=15q+s,             q>=1, 0<=s<15.                    (1.1)
```

A state containing `k` large macros has the unique composition

```text
v_k=(k,A-15k),       0<=k<=q.                          (1.2)
```

For `k>0`, its singleton-to-large slope is

```text
r_k=A/k-15,                                             (1.3)
```

strictly decreasing in `k`; `k=0` is the infinite-slope state.  The target
slope is the irrational number

```text
r=6(sqrt(2)-1).
```

### Theorem

Area `A` passes the composition cone if and only if

```text
s/q < r.                                                (1.4)
```

Equivalently, if

```text
h=floor(A/(15+r)),                                      (1.5)
```

then every viable state library contains at least one composition with
`k<=h` and at least one with `k>=h+1`.  Conversely, any pair straddling this
cut has a positive frequency mixture of slope `r`.

### Proof

For a state-frequency vector `delta_k`, divide the total singleton count by
the total large count.  After weighting each `r_k` by `k delta_k`, the result
is a convex combination of the finite slopes, with any `k=0` frequency adding
only to the numerator.  Since every `r_k` is rational and `r` is irrational,
the target is attained exactly when used states occur on both sides of `r`.
Equation (1.3) gives `r_k>r` precisely when `k<A/(15+r)` and `r_k<r`
precisely when `k>A/(15+r)`.  The threshold is irrational and hence never an
integer, proving (1.5).

There is a low-side state exactly when `r_q=s/q<r`, which proves (1.4).
Conversely the states immediately on either side of (1.5) bracket `r`, and a
positive two-point mixture realizes it.  QED.

The first arithmetically admitted bands are therefore

```text
15--17,
30--34,
45--52,
60--69,
75--87,
and every A>=90.                                        (1.6)
```

N64S closes the first band, and N65S closes area 30.  Formula (1.6), not an
area-by-area search, is the permanent arithmetic classifier.

## 2. K66T — the count-changing trade theorem

### Definition

An **AHI carrier trade** is a pair of finite source-macro patches with

1. the same connected geometric support;
2. source macrotiles wholly inside that support; and
3. different numbers of large macros.

The exposed marked boundary data may differ: a contextual unmarked carrier is
allowed to recover its state from neighboring carriers.  Thus this definition
does not smuggle in separable or radius-zero erasure.

### Theorem

Every carrier-local finite-state compiler to the exact AHI source contains an
AHI carrier trade.  If two states contain `k_1` and `k_2` large macros, their
singleton counts differ by

```text
m_1-m_2=15(k_2-k_1).                                    (2.1)
```

### Proof

All states are decompositions of the same carrier support and have the form
(1.2).  K66A forces one used state on each side of the threshold (1.5), so
their large counts differ.  They are the required same-support trade, and
subtracting their equal-area equations gives (2.1).  QED.

This is the general object that the small classifications were testing:

- sub-30 trades would exchange one large macro with 15 singleton cells;
- area-30 `H/G` trades do the same;
- area-30 `H/Z` trades exchange two large macros with 30 singleton cells.

## 3. K66C — the corridor-cut formulation

Expand every large macro into its exact 15 common rhombi.  Each rhombus has a
long diagonal whose endpoints carry the two ordered corridor bits:

```text
S=00,       L=11,       M in {01,10}.                   (3.1)
```

Let `V` be the equivalence classes of corridor-bit occurrences under the
exact AHI endpoint-continuation relation.  (For an all-singleton subdivision
these are the long-diagonal endpoints used by K64B; for a mixed macro patch
the addressed source port/vertex data, not geometric coincidence alone,
defines the classes.)  Continuation makes the labels a single map

```text
c: V -> {0,1}                                             (3.2)
```

on the resulting continuation graph.  Consequently the `M`-labelled edges are
exactly the cut edges of `c`; every cycle contains an even number of them.
Conversely, on each connected component, any edge labelling with even `M`
parity around every cycle integrates to (3.2), uniquely up to a global bit
flip.  This is the graph-theoretic content of the ordered-corridor rule used
in K64B.  It does not identify the participant sectors at a geometric vertex
unless the exact source rule does so.

Therefore the local part of the infinite carrier question is exactly:

> Does one finite triangular-lattice support admit two exact covers by the
> published large stencils and singleton rhombi, with different large counts,
> such that both induced `S/M/L` long-diagonal labellings are cuts and the
> remaining AHI vertex/SAB rules close?

This is a count-changing cut-admissible exact-cover problem.  It includes
contextual boundary states and does not assume the two marked boundaries are
equal.  The sub-30 and area-30 certificates prove that it has no witness in
their complete size ranges.

## 4. N66R — the all-area closure criterion

If the fixed AHI source admits no count-changing cut-admissible carrier trade,
then no carrier-local Sturmian monotile exists at **any** area.

This is immediate from K66T, but it changes the research target.  The next
work is not an area-31 carrier census.  It is one of:

1. derive a conserved source boundary/height charge that forbids every
   count-changing trade;
2. construct one exact trade, then test its complete AHI vertex/SAB legality;
   or
3. prove a computability boundary for this fixed trade problem.

Even a positive trade is not a monotile: whole-plane tilability, contextual
state recovery, grouping, total decoding, and periodicity rejection remain.
But without a trade the entire carrier-local branch is closed permanently.
