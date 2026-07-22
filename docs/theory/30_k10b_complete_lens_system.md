# Complete K10B square-lens feasibility system

**Status:** HC-24 exact proof draft; no polygon, placement patch or candidate

**Scope:** unchanged K10B boundary word, square lens and five sharp
`pi/4` spine angles; positive weights `a,b,c,d` and `h=a+b+c`

## 1. Orientation correction

The K10B data do not fix the terminal angle `ell_A`; they require only
`ell_A!=pi/4`. Consequently the first `A` edge need not have a direction in
`Q(sqrt(2))`. What is true is more precise:

- relative to the first edge, every spine offset has coefficients in
  `Q(sqrt(2))`; and
- complete feasibility is a finite exact semialgebraic system in one unit
  direction `(C,S)`.

Thus a purely linear system in `(a,b,c,d)` would silently fix an angle which
K9A/K10B left free. HC-24 retains the free angle and derives the exact finite
system instead.

## 2. The first half of the spine

Use the square coordinates of K14R, put `R=(0,0)`, `Q=(d,d)`, and write

```text
r=d/sqrt(2),              C=cos(x), S=sin(x).          (2.1)
```

The five `pi/4` convex spine angles have signed exterior turn
`3*pi/4`. Reversing all signs reflects the square, so it suffices to take the
positive sign. Before the final rotation by `x`, the first six partial sums
are

```text
w_0 = (0,0),
w_1 = (a,0),
w_2 = (a-r, r),
w_3 = (a-r, r-b),
w_4 = (a, sqrt(2)*d-b),
w_5 = (a-c, sqrt(2)*d-b),
w_6 = (a-c+r, r-b).                                  (2.2)
```

Indeed the successive edge directions are

```text
0, 3*pi/4, 3*pi/2, pi/4, pi, 7*pi/4,                (2.3)
```

with lengths `a,d,b,d,c,d`. Every coordinate in (2.2) belongs to the
`Q(sqrt(2))`-linear span of the weights.

Let

```text
M(C,S) = [[C,-S],[S,C]].                              (2.4)
```

Central spine pairing gives every vertex, not only the first half:

```text
p_k       = M*w_k,
p_(13-k)  = (d,d)-M*w_k,            0<=k<=6.         (2.5)
```

The central edge is therefore

```text
e_H=(d,d)-2*M*w_6.                                   (2.6)
```

Equations (2.2)--(2.6) are the complete spine coordinates conditional only
on the free terminal direction.

## 3. K15S: exact lens system

### ST-M1.K15S

The centrally paired K10B spine has its relative interior in the open square
lens if and only if there are real `C,S` satisfying

```text
C^2+S^2=1,       C>0, S>0,                            (3.1)

0 < C*x_k-S*y_k < d,
0 < S*x_k+C*y_k < d,             k=1,...,6,           (3.2)
```

where `w_k=(x_k,y_k)` is the explicit table (2.2), together with the central
length equation

```text
(d-2*(C*x_6-S*y_6))^2
 +(d-2*(S*x_6+C*y_6))^2 = h^2.                       (3.3)
```

The reflected turn choice is obtained by exchanging the square axes and
adds no feasibility class.

### Proof

The first `A` edge has relative interior in the square exactly when its unit
direction lies strictly inside the tangent quadrant at `R`, giving (3.1).
Equations (3.2) say precisely that the six nonterminal first-half vertices
are in the open square. Equation (2.5) then puts all six paired vertices in
the open square too. Convexity of the square puts every open segment between
successive vertices inside it. Finally (3.3) is exactly `|e_H|=h`.

Conversely, an admitted spine supplies its first-edge direction `(C,S)`;
the five fixed turns give (2.2), central pairing gives (2.5), open
containment gives (3.1)--(3.2), and the prescribed host length gives (3.3).
□

K15S is exact lens containment and closure. Simplicity of the full polyline
is a separate finite condition: for the thirteen explicitly known segments,
every nonadjacent pair must fail the standard closed-segment intersection
test (orientation determinants plus collinear interval tests). No claim below
silently infers simplicity from containment.

## 4. Closure is one line on the unit circle

Write

```text
X=a-c+r,        Y=r-b,        R_6=X^2+Y^2,
U=X+Y=a-b-c+sqrt(2)*d,
V=X-Y=a+b-c.                                         (4.1)
```

Expanding (3.3) gives the single exact linear equation in the orientation:

```text
U*C+V*S = T,
T = (2*d^2+4*R_6-h^2)/(4*d).                         (4.2)
```

Hence fixed weights have at most two closure orientations, except in the
degenerate identity case. Before quadrant and containment restrictions, a
closure orientation exists exactly when

```text
T^2 <= U^2+V^2 = 2*R_6.                              (4.3)
```

The square root used to intersect (4.2) with (3.1) need not lie in
`Q(sqrt(2))`. This is why the exact full problem is semialgebraic rather than
linear in the weights alone.

## 5. N32: the complete prefix creates a narrow weight wedge

### ST-M1.N32

Every open-lens K10B spine satisfying K15S necessarily obeys

```text
d < sqrt(2)*a,
h < sqrt(2)*d,
b > (sqrt(2)-1)*d,                                  (5.1)
```

and therefore

```text
b+c < a < (1+sqrt(2))*b-c,
b > sqrt(2)*c.                                      (5.2)
```

### Proof

The strict forms of N31's prefix and diameter arguments give the first two
inequalities in (5.1), because all nonterminal spine vertices lie in the
open square.

For the third, put `Y_4=sqrt(2)*d-b`, so `w_4=(a,Y_4)`. If `Y_4<=0`, then
`b>=sqrt(2)d>(sqrt(2)-1)d`. If `Y_4>0`, the first inequality for `w_4` in
(3.2) gives

```text
a*C-Y_4*S>0,       so tan(x)<a/Y_4.                  (5.3)
```

On this interval the function

```text
f(x)=a*sin(x)+Y_4*cos(x)
```

is strictly increasing from `Y_4`. Its value is the second coordinate of
`M*w_4`, which is strictly below `d`. Hence `Y_4<d`, proving
`b>(sqrt(2)-1)d`.

Combining the first two inequalities gives `h<2a`, hence `b+c<a`. Combining
the last two gives

```text
b > (1-1/sqrt(2))*(a+b+c),
```

which rearranges to `a<(1+sqrt(2))b-c`. For this open interval in `a` to be
nonempty one needs `2c<sqrt(2)b`, equivalently `b>sqrt(2)c`. □

The illustrative tuple `(a,b,c,h)=(11,4,6,21)` passes N31 but fails N32's
`b>sqrt(2)c`. It therefore does not survive the complete fixed-turn prefix.
The original `(1,2,4,7)` fails for the same reason independently of U1.

## 6. K15D: exact arithmetic exclusion of `d` host covers

K15S gives `d>h/sqrt(2)`, so `2d>h`. Under cover-side alignment V, a
full-side partition of the host can therefore contain at most one `d` side.
It contains one exactly when

```text
h-d in <a,b,c>                                       (6.1)
```

with nonnegative remainder; if `d>h`, the remainder is negative and the
condition automatically fails. Thus the exact replacement for the old
`d>h` shortcut is

```text
h-d notin <a,b,c>.                                   (6.2)
```

This is a finite semigroup test for rational weights and a finite bounded
exact-equality test in a fixed real algebraic field. It excludes arithmetic
`d` covers only; vertex alignment, transitions, sliding and geometric
contacts remain separate obligations.

## 7. HC-24 intermediate disposition

K15S supplies the full finite lens system, N32 sharply narrows its possible
weight cone, and K15D closes the requested arithmetic formulation of the
`d`-cover burden. No new tuple is selected in session 126. Session 127 must
solve K13A U1/U2 jointly with (3.1)--(3.3), (5.2) and (6.2), analytically;
it may not turn this exact system into a numerical parameter search.
