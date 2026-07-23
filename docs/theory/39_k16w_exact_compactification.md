# K16W exact compactification

**Date:** 2026-07-23

**Status:** HC-32 theorem draft; one polarity cell refuted and the other
weight-compactified, no solver, coordinates, polygon or candidate

**Normalization:** `u=1`

Put

```text
v_0=sqrt(23/2),
L(v)=sqrt(v^2-1),
delta(v)=v-L(v)=1/(v+L(v)),                       (0.1)
U(v)=sqrt(2)/(sqrt(1-v^(-2))-v^(-1)).             (0.2)
```

N38/K30W give `v>v_0` and `sqrt(2)<b,c<U(v)`.  Both `delta` and `U` are
strictly decreasing.

## 1. N41: the west--east cell is empty

In `P_-+`, the first length-`v` spoke points west.  Its endpoints `p_2,p_3`
are in the open rectangle, so

```text
p_(2,x)>v*|x_b|>sqrt(v^2-1)=L(v).                 (1.1)
```

On the other hand `p_2=Z*(a+q)`, hence

```text
p_(2,x)<=|p_2|=sqrt(a^2-sqrt(2)*a+1).             (1.2)
```

Host diameter and N38 give

```text
a+b+c<sqrt(v^2+1)=D,
a<D-2*sqrt(2).                                    (1.3)
```

### ST-M1.N41

The complete `P_-+` K16W cell is empty.

**Admitted form:** necessary-condition implication, ending in contradiction.

### Proof

Since `a>1/sqrt(2)`, the square in (1.2) is strictly increasing with `a`.
At the upper value in (1.3),

```text
(D-2*sqrt(2))^2-sqrt(2)*(D-2*sqrt(2))+1
  =v^2+14-5*sqrt(2)*D.                            (1.4)
```

N38 gives `D>5/sqrt(2)>3/sqrt(2)`, so the final expression is below
`v^2-1=L(v)^2`.  Equations (1.1)--(1.2) demand the reverse strict order.
Contradiction.  □

This is a mathematical refutation of one HC-31 cell, not a reinterpretation
of its resource stop.

## 2. Prefix control in the east--west cell

In `P_+-`, the first length-`v` spoke points east.  Containment gives

```text
0<p_(2,x)<v-v*x_b<delta(v).                       (2.1)
```

Also `0<p_(2,y)<1`.  Since `|p_2|^2=a^2-sqrt(2)a+1`,

```text
a^2-sqrt(2)*a<delta(v)^2.                         (2.2)
```

Define the positive root

```text
A(v)=(sqrt(2)+sqrt(2+4*delta(v)^2))/2.            (2.3)
```

Then `a<A(v)`, and `A` is strictly decreasing.

## 3. K31C: an explicit global upper bound

The second length-`v` spoke points west.  Its endpoint `p_6` therefore obeys

```text
0<p_(6,x)<delta(v).                               (3.1)
```

Only the length-`c` code edge and the final unit edge remain before `p_8`.
The triangle inequality in the horizontal component gives

```text
0<p_(8,x)<delta(v)+c+1<delta(v)+U(v)+1.           (3.2)
```

Set

```text
delta_0=(sqrt(46)-sqrt(42))/2,
U_0=sqrt(46)/(sqrt(21)-sqrt(2)),
A_0=(sqrt(2)+sqrt(2+4*delta_0^2))/2,
V_*=A_0+4*U_0+2*delta_0+2.                        (3.3)
```

### ST-M1.K31C

Every K16W solution belongs to `P_+-` and satisfies

```text
sqrt(23/2)<v<V_*<13,
1/sqrt(2)<a<A_0<3/2,
sqrt(2)<b,c<U_0<98/43.                            (3.4)
```

**Admitted form:** necessary-condition implication from complete K16W.

### Proof

N41 leaves only `P_+-`.  If

```text
v<=2*(delta(v)+U(v)+1),                           (3.5)
```

monotonicity immediately puts `v` below `V_*`.  Otherwise (3.2) makes the
horizontal component of the central host edge positive.  Closure and
`h=a+b+c` give

```text
v-2*p_(8,x)<h<A(v)+2*U(v),
v<A(v)+4*U(v)+2*delta(v)+2<V_*.                   (3.6)
```

The first three bounds in (3.4) follow from (2.2), K30W and monotonicity.
For the simple rational estimates, `delta_0<1/6` because
`sqrt(46)+sqrt(42)>12`; `sqrt(2)<10/7` then gives `A_0<3/2` by evaluating
the quadratic in (2.2) at `3/2`.  Also

```text
sqrt(21)>9/2,       sqrt(2)<10/7,       sqrt(46)<7,
```

so `U_0<7/(9/2-10/7)=98/43`.  Consequently

```text
V_*<3/2+4*(98/43)+1/3+2=3341/258<13.              (3.7)
```

□

## 4. Boundary and regularity scope

K31C is an exact compactification of the **weights** and eliminates the only
unbounded aspect direction.  It does not make the strict feasible set closed:

- tangent bridge variables can approach the omitted straight direction;
- open containment can approach the rectangle boundary;
- disjoint segments can approach endpoint contact or tangency; and
- the closure equality can become singular.

The proof does not ignore those limits.  N41 and K31C use strict finite
inequalities before any limit, so an unbounded sequence cannot escape by
converging to a self-contact.  For a later complete interval method, however,
the remaining finite boundary strata still require exact treatment through a
finite circle atlas plus a certified cover or a proved nonsingularity
criterion.  Compact weights alone are not an UNSAT algorithm.

## 5. Session-146 disposition

The planned `lambda=1/v` blow-up is unnecessary: its only purpose was to
decide whether the aspect direction could escape to infinity, and K31C gives
the stronger explicit bound.  Session 147 may now study finite strand/order
data, but only if it supplies an exhaustive theorem rather than a selected
ordering.  No solver run is authorized.
