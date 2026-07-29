# K16W polarity elimination

**Date:** 2026-07-23

**Status:** HC-31 theorem draft; two exact cells survive, no solver verdict,
polygon, patch or candidate

**Scope:** K16B inside the N38 extreme-aspect cone

## 1. N39: equal polarity cannot fit

Put

```text
L=sqrt(v^2-u^2),
D=sqrt(v^2+u^2).                                  (1.1)
```

N38 gives `v/u>sqrt(23/2)`. For either long-spoke unit direction
`r=(x,y)`, containment gives `v*|y|<u`, hence

```text
v*|x|=v*sqrt(1-y^2)>L.                           (1.2)
```

### ST-M1.N39

The two length-`v` spokes of a simple K17S spine have opposite horizontal
polarities.

### Proof

Suppose first that both point east. A length-`v` segment with horizontal
displacement above `L` and both endpoints in `(0,v)` starts left of `v-L`
and ends right of `L`. Thus the end `p_3` of the first spoke lies right of
`L`, while the start `p_5` of the second lies left of `v-L`. The intervening
two-edge path from `p_3` to `p_5` must therefore move left by more than

```text
2*L-v.                                           (1.3)
```

Its total length is `b+u`, so `b+u>2L-v`. If both spokes point west, the
start/end inequalities reverse and the same necessary bound follows.

On the other hand, host closure, K26P and K26X give

```text
b+u
 < D-a-c+u
 < D-(3/sqrt(2)-1)*u.                            (1.4)
```

It remains to compare (1.3) and (1.4). Normalize `r=v/u` and define

```text
F(r)=2*sqrt(r^2-1)-r-sqrt(r^2+1)+3/sqrt(2)-1.    (1.5)
```

At `r_0=sqrt(23/2)`,

```text
F(r_0)=sqrt(42)-sqrt(46)/2-sqrt(2)-1>0:          (1.6)
```

indeed `sqrt(42)>6`, `sqrt(46)/2<7/2`, and `sqrt(2)<3/2`.
Moreover

```text
F'(r)=2r/sqrt(r^2-1)-1-r/sqrt(r^2+1)>0,          (1.7)
```

because the first term exceeds `2` while the last two sum to less than
`2`. Hence `F(r)>0` throughout N38, so the upper bound (1.4) is strictly
below `2L-v`, contradicting the necessary reset length. □

Only the two opposite-polarity cells remain.

## 2. K29O: K27X collapses to one sign

Retain K27X's

```text
R=r_c/r_b=X+iY,
A=v-b/sqrt(2)>0,
B=b/sqrt(2)-u>0.                                 (2.1)
```

In either opposite-polarity cell, `X<0`. More sharply, put `t=u/v`.
Each long-spoke line makes an angle of magnitude below `arcsin(t)` with its
horizontal polarity, so

```text
-X>sqrt(1-t^2)>1-t>A/v.                          (2.2)
```

The last inequality uses `b>sqrt(2)u`.

### ST-M1.K29O

On either opposite-polarity cell, the two long spokes intersect as closed
segments exactly when

```text
A*Y-B*X <= 0.                                    (2.3)
```

They are disjoint exactly when the reverse strict inequality holds.

### Proof

K27X proves that intersection implies (2.3). Conversely, suppose (2.3).
Since `X<0`, it reads

```text
A*Y+B*(-X)<=0,
```

so `Y<0` and `-Y>=B*(-X)/A>B/v` by (2.2). This is K27X's first
intersection inequality. Its third left side is

```text
(A-v)*Y-B*X=(-b/sqrt(2))*Y+B*(-X)>0,             (2.4)
```

which is the remaining K27X inequality. Thus all three hold. Negating (2.3)
gives the exact disjointness condition. □

## 3. Fixed surviving cells

The critical-pair decomposition now has exactly two cells:

```text
P_+-: x_b>0, y_b>0, x_c<0, y_c<0, AY-BX>0;
P_-+: x_b<0, y_b<0, x_c>0, y_c>0, AY-BX>0.       (3.1)
```

Both also carry N38, all K17S containment and closure constraints, and the
117 noncritical segment-disjointness predicates. No theorem here asserts
that either cell is nonempty. If an exact decision is authorized, these two
cells are the complete fixed instance list; same-polarity or three-way K27X
subcases must not be reintroduced.
