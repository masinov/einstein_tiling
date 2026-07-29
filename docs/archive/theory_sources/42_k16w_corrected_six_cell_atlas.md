# K16W corrected six-cell atlas

**Date:** 2026-07-23

**Status:** HC-33 theorem draft; one strand order and two bridge-chart pairs
refuted, six complete bounded cells remain, no solver verdict or candidate

**Scope:** complete K16W after ERR-013 and corrected N42, normalized by `u=1`

Put

```text
L=sqrt(v^2-1),       delta=v-L,
M=sqrt(h^2-1),       D=sqrt(v^2+1),
h=a+b+c.                                             (0.1)
```

Corrected N42 fixes the five long-strand traversal to

```text
B east, C west, H east, C' west, B' east.            (0.2)
```

## 1. K33M: the open spine has exactly five midline crossings

Let `ell` be `x=v/2`.  K32S already proves that each long strand crosses
`ell` once.  We now exclude every additional crossing by the six intervening
short subpaths.

### The B--C and C'--B' connectors

The B terminal endpoint and C initial endpoint both have horizontal
coordinate strictly above `L`.  If their `b,1` connector touched `ell`, its
length would exceed

```text
2*L-v.                                                (1.1)
```

Host diameter and `a+c>3/sqrt(2)` give

```text
b+1<D-3/sqrt(2)+1.                                   (1.2)
```

N39's positive function `F(v)` is exactly the comparison

```text
D-3/sqrt(2)+1<2*L-v.                                 (1.3)
```

Thus this connector cannot touch `ell`.  Central pairing gives the same
conclusion for C'--B'.

### The C--H and H--C' connectors

The C terminal endpoint obeys `p_(6,x)<delta`.  Since H points east and has
horizontal span above `M`,

```text
p_(8,x)<(v-M)/2.                                     (1.4)
```

If the `c,1` connector from `p_6` to `p_8` touched `ell`, its length would
exceed

```text
(v/2-delta)+M/2=(v+M)/2-delta.                       (1.5)
```

The exact comparisons retained from corrected N42 give

```text
(v+M)/2-delta>19/6,
c+1<U_0+1<19/6.                                     (1.6)
```

Contradiction.  Central pairing treats H--C'.

### The two terminal subpaths

The initial `a,1` path joins `p_0` to the B initial endpoint `p_2`, both left
of `ell`.  Touching `ell` would require length above `v-delta=L`.  But K31C
gives

```text
a+1<5/2<3<L.                                        (1.7)
```

The terminal path is its central mate.

### ST-M1.K33M

The open K16W spine meets `ell` exactly at the five interiors of
`B,C,H,C',B'`, in that traversal order and with directions `E,W,E,W,E`.

**Admitted form:** necessary-condition implication from complete K16W.

The proof above uses strict inequalities throughout, so a short edge tangent
to `ell` is excluded as well as a transverse crossing.

## 2. N43: strand order S4 is impossible

Between consecutive long-strand crossings, K33M puts the B--C and H--C'
subarcs wholly in the right open half-plane.  Two disjoint arcs in a
half-plane cannot join alternating endpoint pairs on its boundary line.
This is the standard Jordan separation criterion for noncrossing chords.

In K32S order S4 the bottom-to-top order is

```text
C', B, H, B', C.                                    (2.1)
```

The two right-half-plane pairs are `(B,C)` and `(H,C')`; their endpoints in
(2.1) alternate

```text
C' [pair 2], B [pair 1], H [pair 2], C [pair 1].    (2.2)
```

They must intersect, contradicting spine simplicity.

### ST-M1.N43

No complete K16W point belongs to K32S cell S4.  Cells S1, S2 and S3 pass
this necessary topological test; no nonemptiness claim is made for them.

**Admitted form:** necessary-condition implication from complete K16W.

## 3. K33C: the first bridge lies on the left semicircle

Write the first-quadrant terminal direction as `Z=C+iS`, put
`k=1/sqrt(2)`, and retain

```text
q=(-k,k),       r_b=Z*q*z_1=(x_b,y_b).             (3.1)
```

In the surviving polarity cell `x_b,y_b>0`; N38 gives `y_b<x_b`.  For
`s=Z*q`,

```text
s_x=-k(C+S)<0,
s_y= k(C-S),       |s_y|<-s_x.                     (3.2)
```

Since `z_1=conj(s)*r_b`,

```text
Re(z_1)=s_x*x_b+s_y*y_b
       <=s_x*x_b+|s_y|*y_b<0.                     (3.3)
```

### ST-M1.K33C

In K32A's bounded atlas, the first bridge has sign `sigma_1=-1`.  Both chart
pairs with `sigma_1=+1` are empty.  The vertical chart seams have zero real
part and are also excluded by the strict sign (3.3).

**Admitted form:** necessary-condition implication plus restriction of the
exact K32A cover.

No sign of the second bridge is fixed by this argument.

## 4. Corrected HC-33 disposition

N43 leaves three exact strand orders and K33C leaves two exact chart pairs:

```text
S_1, S_2, S_3
    x
(sigma_1,sigma_2)=(-,-),(-,+).                    (4.1)
```

Thus complete K16W has an exact bounded cover by six cells.  Every cell keeps
corrected N42's H-east sign, closure, all 32 containment bounds, all 120
nonadjacent-pair predicates and K32R's discriminant/boundary obligations.

HC-33 is exhausted at session 150.  No solver formula or research command is
activated: serialization, cold equivalence checks, preregistration and any
externally supervised decision require a new checkpoint.  The six cells are
not six candidates; they are six unresolved semialgebraic cases for one
conditional carrier topology.
