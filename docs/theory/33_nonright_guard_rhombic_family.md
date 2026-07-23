# Symbolic non-right guard rhombus

**Date:** 2026-07-23

**Status:** HC-28 exact family derivation; no polygon, placement patch or
candidate

**Scope:** K10B's unchanged equal-spoke 15-edge boundary word, equal guard
legs, central half-turn docking and the symmetric K9A specialization
`theta=rho=(pi-gamma)/2`, with `0<gamma<pi`

## 1. The hypothesis changed from N33

N33 closes the right-angle equal-leg guard: its lens is a square and the five
sharp spine angles are `pi/4`.  HC-28 changes the guard angle itself while
retaining the topology and K9A selector.  Put

```text
lambda = theta = rho = (pi-gamma)/2,
tau    = pi-lambda = (pi+gamma)/2.                  (1.1)
```

Then every sharp vertex on the first half of the shield spine has interior
angle `lambda` and signed exterior turn `tau`.  K9A still selects exactly the
two reversal classes `ABC` and `ACB` provided the unused endpoint satisfies

```text
ell_A != lambda.                                    (1.2)
```

The cyclic side word is unchanged:

```text
d,A,d,B,d,C,d,H,d,C,d,B,d,A,d,                     (1.3)
```

and the middle shield spine, from `R` to `Q`, remains

```text
A,d,B,d,C,d,H,d,C,d,B,d,A.                         (1.4)
```

This is a one-parameter family of the topology closed by N33, not a change to
the frozen unequal-spoke K16B topology.

## 2. The guard lens is an exact rhombus

Use complex coordinates.  Place

```text
R=0,                  Gamma=d,
g=(-cos(gamma), sin(gamma)),
Q=d*(1+g).                                             (2.1)
```

The two guard sides have length `d`, and the angle between `Gamma->R=-d`
and `Gamma->Q=d*g` is `gamma`.  Half-turn about `Q/2` sends `Gamma` to
`Q-Gamma=d*g`.  Hence the guard path and its half-turn bound the
parallelogram

```text
P_gamma={d*(alpha+beta*g): 0<=alpha,beta<=1},        (2.2)
```

which is a rhombus because both spanning vectors have length `d`.  Since
`0<gamma<pi`, `Im(g)>0` and the lens is nondegenerate.  At
`gamma=pi/2`, `g=i` and (2.2) is exactly K15S's square.

For a point `p=(p_x,p_y)`, define its two unscaled oblique-coordinate
numerators

```text
B_gamma(p) = p_y,
A_gamma(p) = Im(g)*p_x-Re(g)*p_y.                   (2.3)
```

Solving `p=d*(alpha+beta*g)` gives

```text
beta  = B_gamma(p)/(d*Im(g)),
alpha = A_gamma(p)/(d*Im(g)).                       (2.4)
```

Therefore `p` is in the open lens if and only if

```text
0 < A_gamma(p) < d*Im(g),
0 < B_gamma(p) < d*Im(g).                           (2.5)
```

This is the exact containment test; it does not approximate a curved region
or sample the angle.

## 3. K22R: complete relative spine

Let

```text
q=exp(i*tau).                                       (3.1)
```

Before the free terminal rotation, the first-half partial sums are

```text
w_0 = 0,
w_1 = a,
w_2 = a+d*q,
w_3 = a+d*q+b*q^2,
w_4 = a+d*q+b*q^2+d*q^3,
w_5 = a+d*q+b*q^2+d*q^3+c*q^4,
w_6 = a+d*q+b*q^2+d*q^3+c*q^4+d*q^5.              (3.2)
```

### ST-M1.K22R

For the family (1.1)--(1.4), equations (3.1)--(3.2) are the complete relative
first-half spine.  If `z=C+iS` is the free unit direction of the first `A`
edge, all fourteen spine vertices are

```text
p_k      = z*w_k,                  0<=k<=6,
p_(13-k) = Q-z*w_k,                0<=k<=6.          (3.3)
```

The central `H` edge is

```text
e_H=Q-2*z*w_6.                                      (3.4)
```

### Proof

Successive first-half edge directions differ by the fixed signed exterior
turn `tau`; their lengths are `a,d,b,d,c,d`, giving (3.2).  The fixed
half-turn exchanges the two guard paths and reverses the shield spine, so it
sends every first-half point `p` to `Q-p`.  This gives (3.3) and leaves the
single middle edge (3.4).  Conversely, (3.2)--(3.4) have precisely the side
word, five sharp turns and central pairing required by (1.3).  □

Changing every turn sign complex-conjugates the construction and reflects the
rhombus, so it adds no feasibility class under full Euclidean isometry.

## 4. K22S: complete exact family

### ST-M1.K22S

Let `h=a+b+c`.  A centrally paired spine of the fixed HC-28 family has every
nonterminal spine vertex in the open rhombus if and only if there are positive
`a,b,c,d`, a guard angle `0<gamma<pi`, and a unit `z` such that

```text
0 < A_gamma(z*w_k) < d*Im(g),
0 < B_gamma(z*w_k) < d*Im(g),       k=1,...,6,       (4.1)

|Q-2*z*w_6|^2 = h^2.                                (4.2)
```

It is a **simple** open-lens shield spine exactly when, in addition, every
nonadjacent pair among its thirteen closed segments is disjoint.  There are
`binom(13,2)-12=66` such pairs, and each predicate is the standard exact
orientation/collinear-interval segment test applied to the vertices (3.3).

### Proof

Equation (2.5) applied to the first six vertices is exactly (4.1).  Central
inversion in `Q/2` sends oblique coordinates `(alpha,beta)` to
`(1-alpha,1-beta)`, so (4.1) simultaneously places their six paired vertices
in the open lens.  Convexity of the rhombus contains every open segment
between successive contained vertices.  Equation (4.2) is exactly the
prescribed central length.  These implications reverse directly.  A polygonal
chain is simple precisely when no two nonadjacent closed segments intersect;
the thirteen-segment count gives 66.  □

K22S is the complete finite carrier-spine obligation.  It is not yet the two
complete host patches, role-recognition proof or all-tilings converse.

## 5. Polynomial half-angle form

Put

```text
x=cos(gamma/2),       y=sin(gamma/2).               (5.1)
```

The nondegenerate non-right parameter domain is

```text
x>0, y>0, x^2+y^2=1, x^2!=y^2.                     (5.2)
```

In these variables

```text
q=(-y,x),
g=(y^2-x^2, 2*x*y).                                (5.3)
```

Thus every `q^j`, every partial sum (3.2), both forms (2.3), closure (4.2),
and all segment determinants are polynomial expressions in

```text
a,b,c,d,x,y,C,S,
```

with only the two unit-circle equations
`x^2+y^2=C^2+S^2=1`.  K22S is therefore one exact finite semialgebraic
family.  Formula (5.3) is a representation theorem, not authorization for a
QE, SMT, CAD or numerical search run.

## 6. Right-angle specialization recovers K15S exactly

Set `gamma=pi/2`, so `x=y=1/sqrt(2)`, `g=i`, and

```text
q=(-1+i)/sqrt(2).                                   (6.1)
```

The powers in (3.2) give

```text
w_1=(a,0),
w_2=(a-d/sqrt(2), d/sqrt(2)),
w_3=(a-d/sqrt(2), d/sqrt(2)-b),
w_4=(a, sqrt(2)*d-b),
w_5=(a-c, sqrt(2)*d-b),
w_6=(a-c+d/sqrt(2), d/sqrt(2)-b).                  (6.2)
```

These are K15S (2.2) term for term.  Since `g=(0,1)`, (4.1) becomes
`0<Re(z*w_k),Im(z*w_k)<d`, and (4.2) becomes K15S (3.3).  The non-right
family therefore changes exactly the angle/lens hypothesis named at
admission; it neither loses nor silently alters the closed square case.

## 7. Session-135 disposition

K22R and K22S close the complete symbolic-family derivation and its required
N33 specialization control.  They are a reduction, not a terminal HC-28
outcome.  The remaining sessions must either prove this entire non-right
family empty, exhibit exact data satisfying K22S including all 66 simplicity
predicates, or fire the predeclared freeze at one named surviving obligation.
