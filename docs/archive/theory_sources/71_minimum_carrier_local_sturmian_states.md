# Minimum carrier-local Sturmian state theorem

**Date:** 2026-07-28  
**Scope:** one common-rhombus carrier whose decoded Section 10.1 macrotiles do
not cross carrier boundaries; arbitrary finite contextual state library is
allowed inside the carrier

## 1. Exact composition coordinates

Measure area in common `60/120` rhombi.  A large Section 10.1 macro has area
`15`; the singleton `M` macro has area `1`.  A carrier-local decoded state has
an integer composition

```text
(k,m),                  15*k + m = A,                  (1.1)
```

where `A` is the fixed carrier area, `k` is the total number of large macros
of either type, and `m` is the number of singleton macros.

P0 gives the target singleton-to-large occurrence ratio

```text
r = 6*(sqrt(2)-1),             2 < r < 3.              (1.2)
```

The equality follows from its positive homogeneous coefficients:

```text
b/a = beta*(1-2*beta)/(beta^2/6) = 6*beta,
beta=sqrt(2)-1,
```

because `1-2*beta=beta^2`.

For state frequencies `delta_s`, every carrier has the same area, so a
necessary frequency equation is

```text
sum_s delta_s*m_s = r * sum_s delta_s*k_s.             (1.3)
```

This is N60C specialized to the exact `15/1` source areas.

## 2. K64A — the sub-30 area classification

### Theorem

If a carrier-local state library satisfies (1.3) and `A<30`, then

```text
A in {15,16,17}.                                       (2.1)
```

Moreover its essential state library must contain both

```text
(1,A-15)        and        (0,A).                       (2.2)
```

Thus the only sub-30 composition mechanisms are

| area | large-containing state | second state |
|---:|---|---|
| 15 | `1 large` | `15 M` |
| 16 | `1 large + 1 M` | `16 M` |
| 17 | `1 large + 2 M` | `17 M` |

### Proof

For `A<15`, equation (1.1) forces `k=0` in every state, contradicting the
positive large-macro density.  For `15<=A<30`, one has `k in {0,1}`.  All
states with `k=1` have the same value `m=A-15`.  If no `k=0` state occurs,
(1.3) would give the rational integer ratio `A-15`, not the irrational `r`.
Hence both compositions in (2.2) must occur.

As the frequency of `(1,A-15)` ranges from zero to one, the aggregate ratio
in (1.3) ranges strictly from infinity down to `A-15`.  It contains `r` if
and only if

```text
A-15 < r.
```

Since `2<r<3` and `A` is integral, this is equivalent to `A<=17`.  Combining
with `A>=15` proves (2.1) and the table.  QED.

The next arithmetically possible area is `30`: the compositions `(2,0)` and
`(1,15)` already bracket `r`.  Therefore a complete exclusion at areas
`15,16,17` would prove a genuine minimum-area jump from `17` to `30`, not
merely failure of one support.

## 3. K64B — the all-singleton parity gate

Any state `(0,A)` is a lozenge subdivision of the carrier into singleton `M`
macros.  Each singleton carries unequal ordered corridor bits.  When two
singleton long diagonals meet at a source gap, endpoint continuation equates
the corresponding bit.  Consequently the graph formed by the long
diagonals of the subdivision must be bipartite.

Equivalently, every odd cycle in that graph is a local source-language
certificate against the all-singleton state.  N60V applied this criterion to
the one P17 support and found an odd cycle in all 60 subdivisions.  For a new
support, bipartiteness is necessary but not by itself a complete compiler
certificate: its boundary endpoint germs must also equal those of the
large-containing state and all source vertex stars must close.

## 4. Exact finite construction target

K64A turns the smallest carrier-local question into one bounded
classification, not an open-ended polygon search:

1. normalize one `large_A` or `large_B` macro;
2. attach exactly `0`, `1`, or `2` source-legal singleton rhombi, retaining a
   connected disk;
3. enumerate every lozenge subdivision of the same support;
4. reject it on an odd long-diagonal cycle, unequal exposed SAB germs, or an
   illegal source vertex star; and
5. retain any survivor as an exact two-state carrier alphabet satisfying the
   composition equation.

Every item is finite because the large macro and attachment budget are
fixed.  K64C/N64S now complete this list: all `997` supports and all `29,443`
lozenge subdivisions fail the necessary bipartite continuation condition.
Thus no carrier-local Sturmian compiler of area below `30` exists.  See
theory note 72 and its cold-rebuilt exact certificate.

This target directly compiles the fixed source.  It does not reopen arbitrary
carrier geometry or weaken the all-tilings obligation.
