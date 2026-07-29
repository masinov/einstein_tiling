# K16W crossing cells

**Date:** 2026-07-23

**Status:** HC-30 theorem draft; no solver, polygon, patch or candidate

**Scope:** the fixed K16B 19-edge unequal-spoke rectangular carrier, with
both bridge angles symbolic

## 1. K26X: the bridge-independent hook crossing

Use K18H's local hook

```text
s_0=0,
s_1=v*r,
s_2=v*r+w*q*r,
s_3=v*r+w*q*r+u*q^2*r,             w in {b,c},       (1.1)
```

where `|r|=1`, `q=(-1+i)/sqrt(2)`, and `q^2=-i`. The first and third
segments are nonadjacent.

### ST-M1.K26X

Their supporting lines meet at the unique parameters

```text
t = 1-w/(sqrt(2)*v),
s = w/(sqrt(2)*u),                                (1.2)
```

measured from `s_0` on the first segment and from `s_2` on the third.
Consequently the hook crosses transversely when

```text
w<sqrt(2)*u and w<sqrt(2)*v.                     (1.3)
```

At `w=sqrt(2)*min(u,v)`, the intersection reaches an endpoint while the
other parameter remains in `[0,1]`, so the two closed nonadjacent segments
still meet. A simple hook therefore requires

```text
w>sqrt(2)*min(u,v).                              (1.4)
```

### Proof

An intersection satisfies

```text
t*v*r=v*r+w*q*r+s*u*q^2*r.
```

Divide by `r`. The imaginary part gives `s=w/(sqrt(2)*u)` and the real
part gives `t=1-w/(sqrt(2)*v)`. The first and third directions differ by
`pi/2`, so an interior intersection is transverse. The remaining claims
follow from the closed parameter interval `[0,1]`. □

For K20L, `u=1`, `v=2`, and `w=1/10`, so (1.2) lies strictly in the
unit square. The old decoupled containment control is therefore
self-crossing, as expected from its deliberate omission of simplicity.

## 2. K26P: the first corner fixes the aspect orientation

K19P uses a first-edge unit direction `(x,y)` with `x,y>0`. Its first two
horizontal coordinates satisfy

```text
0 < a*x-u*(x+y)/sqrt(2) < a*x < v.              (2.1)
```

### ST-M1.K26P

Every K17S point satisfies

```text
v>u/sqrt(2).                                     (2.2)
```

### Proof

Equation (2.1) gives
`v>a*x>u*(x+y)/sqrt(2)`. A first-quadrant unit vector has
`x+y>1`, proving (2.2). □

## 3. N38: only an extreme wide rectangle survives

The central host edge joins two points in the open `v`-by-`u` rectangle.
Therefore K17S implies the strict diameter bound

```text
h=a+b+c<sqrt(u^2+v^2).                           (3.1)
```

### ST-M1.N38

Every simple K17S spine must satisfy

```text
v/u > sqrt(23/2),
b>sqrt(2)*u,
c>sqrt(2)*u.                                     (3.2)
```

### Proof

Apply K26X to both hooks. If `v<u`, K26P gives `v>u/sqrt(2)`, while

```text
h=a+b+c>u/sqrt(2)+2*sqrt(2)*v
             >u/sqrt(2)+2*u
             >sqrt(u^2+v^2),
```

contradicting (3.1). Thus `v>=u`; equality is excluded by K16B. Now
K26X gives `b,c>sqrt(2)*u`, and K19P gives `a>u/sqrt(2)`. Hence

```text
sqrt(u^2+v^2)>h>5*u/sqrt(2).
```

Squaring positive quantities gives `v^2>23*u^2/2`, proving (3.2). □

This eliminates the entire small-aspect cell left by the coarser
host-diameter calculation. It does not prove that the extreme wide cell is
nonempty.

## 4. Bridge-phase polarity in the surviving cone

Let `r_w=(x_w,y_w)` be the direction of the length-`v` edge in either
hook. Containment of that edge and the intervening code edge gives

```text
v*|y_w|<u,
w*|x_w-y_w|/sqrt(2)<u.                          (4.1)
```

By (3.2), the second inequality makes `|x_w-y_w|<1`. Since `r_w` is
unit, `x_w*y_w<=0` would instead give
`(x_w-y_w)^2>=x_w^2+y_w^2=1`. Therefore

```text
x_w*y_w>0.                                      (4.2)
```

Moreover (3.2) and the first inequality in (4.1) give

```text
y_w^2<2/23,
x_w^2>21/23.                                    (4.3)
```

For the complete K17S phases,

```text
r_b=Z*q*z_1,
r_c=Z*q^3*z_1*z_2.                              (4.4)
```

Thus every surviving point lies in one of four exact open polarity cells,
according to the signs of `(x_b,x_c)`; each `y` has the same sign as its
corresponding `x`. The next obligation is to determine which relative-phase
cells survive the intersection of the two long `v` segments.

## 5. K27X: exact bridge-dependent long-spoke cells

The first long spoke begins at `p_2` in direction `r_b`; the second begins
at `p_5` in direction `r_c`. From K19E,

```text
p_5-p_2=H_b*r_b,
H_b=v+b*q+u*q^2=A+i*B,                           (5.1)

A=v-b/sqrt(2),
B=b/sqrt(2)-u.                                   (5.2)
```

N38 makes `B>0`. Also `b<h<sqrt(u^2+v^2)<sqrt(2)*v`, so `A>0` and
`B<v`. Put

```text
R=r_c/r_b=q^2*z_2=X+i*Y,
X^2+Y^2=1.                                       (5.3)
```

The bridge variable `z_1` and terminal orientation cancel: this pair reads
only the relative second bridge phase.

### ST-M1.K27X

For `Y!=0`, the supporting lines of the two length-`v` spokes meet at

```text
s = -B/(v*Y),
t = (A*Y-B*X)/(v*Y),                             (5.4)
```

where `t` is measured on `p_2p_3` and `s` on `p_5p_6`. The two closed
segments intersect exactly when

```text
v*Y+B <= 0,
A*Y-B*X <= 0,
(A-v)*Y-B*X >= 0.                                (5.5)
```

When `Y=0`, the directions are parallel and the nonzero normal offset
`B` makes the two supporting lines distinct, so this pair is disjoint.

### Proof

An intersection satisfies

```text
p_2+t*v*r_b=p_5+s*v*r_c.
```

Divide by `r_b` and use (5.1):

```text
t*v=A+i*B+s*v*(X+i*Y).
```

Real and imaginary parts give (5.4). Because `B>0`, the condition
`0<=s<=1` is equivalent to `vY+B<=0`. Its denominator `vY` is then
negative. The conditions `t>=0` and `t<=1` consequently become the second
and third inequalities in (5.5), respectively. If `Y=0`, the imaginary
offset between the parallel lines is `B`, proving the last statement. □

### Exact disjoint safe cells

The complement of the closed intersection cell (5.5) is the following
disjoint union:

```text
C_0: v*Y+B > 0;

C_1: v*Y+B <= 0,
     A*Y-B*X > 0;

C_2: v*Y+B <= 0,
     A*Y-B*X <= 0,
     (A-v)*Y-B*X < 0.                            (5.6)
```

Every simple K16W point belongs to exactly one of `C_0,C_1,C_2`, in
addition to one of the four polarity cells in Section 4. Conversely, (5.6)
is necessary and sufficient for this named long-spoke pair to be disjoint.
The remaining non-spoke pairs retain their existing exact K21Q predicates;
they are not silently discarded by this reduction.

## 6. Primary HC-30 disposition

K26X handles both bridge-independent hook pairs completely. N38 reduces
their simple complement to one extreme aspect cone and four bridge-polarity
cells. K27X then handles the only pair formed by the two long spokes and
partitions its safe complement into three exact cells. Thus the three
critical spoke-pair patterns are fully decomposed into at most twelve named
semialgebraic cells before the other K21Q constraints are read.

This is the admitted decomposition outcome, not a K16W decision. K16W
remains open/frozen because none of the twelve cells has yet been proved
empty or supplied a complete witness satisfying the other 117 pair
predicates and host closure. Any future exact decision must use N38 and the
K27X cells rather than rerun the monolithic unrestricted formula.
