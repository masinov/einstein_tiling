# K16W bridge elimination

**Status:** HC-26 theorem draft; no polygon, placement patch or candidate

This note makes one bounded theorem-only attempt to settle the rectangular
split-spoke carrier K16B.  The admission is deliberately terminal: HC-26 must
end with either a complete exact K16W witness, a scoped K16B incompatibility
theorem, or a freeze at K16W.  A partial analysis is not a successful fourth
outcome.

No numerical angle search, coordinate fitting, experiment, SVG, extra edge,
additional participant or enlarged contact atlas is admitted.

## 1. First target: one rigid hook

Both bridge-independent subchains have the form

```text
v, w, u,          w in {b,c},                       (1.1)
```

with signed exterior turns `3*pi/4` at both internal vertices.  Normalize
the first edge direction to the unit vector

```text
r=(x,y),             x^2+y^2=1.                    (1.2)
```

Relative to the first endpoint, the four hook vertices are

```text
s_0 = (0,0),
s_1 = v*(x,y),
s_2 = s_1 + (w/sqrt(2))*(-x-y, x-y),
s_3 = s_2 + u*(y,-x).                              (1.3)
```

The six directed pair differences are

```text
d_01 = (v*x, v*y),
d_12 = (w/sqrt(2))*(-x-y, x-y),
d_23 = (u*y, -u*x),
d_02 = ((v-w/sqrt(2))*x-(w/sqrt(2))*y,
        (w/sqrt(2))*x+(v-w/sqrt(2))*y),
d_13 = (-(w/sqrt(2))*x+(u-w/sqrt(2))*y,
        (w/sqrt(2)-u)*x-(w/sqrt(2))*y),
d_03 = ((v-w/sqrt(2))*x+(u-w/sqrt(2))*y,
        (w/sqrt(2)-u)*x+(v-w/sqrt(2))*y).           (1.4)
```

## 2. K18H: exact rigid-hook cone

### ST-M1.K18H

The hook (1.1) can be translated so that all four vertices, and hence all
three open segments, lie strictly inside a `v`-by-`u` rectangle if and only
if there is a unit vector `(x,y)` such that

```text
|Re(d_ij)| < v,       |Im(d_ij)| < u
for 0 <= i < j <= 3.                              (2.1)
```

Thus (1.2), (1.4) and (2.1) are an exact bridge-independent semialgebraic
cone: six vector bounds, or twelve two-sided coordinate bounds (24 scalar
strict inequalities).

### Proof

A finite planar point set can be translated into the open rectangle
`(0,v) x (0,u)` exactly when its horizontal span is less than `v` and its
vertical span is less than `u`.  Each span condition is equivalent to the
corresponding coordinate bound on every pair difference.  This gives (2.1).
The rectangle is convex, so containing the four endpoints contains all three
open segments.  Conversely, any contained translated hook has both spans
strictly below the rectangle dimensions.  Formula (1.4) is the direct
expansion of (1.3).  □

Every K17S spine therefore supplies one solution of K18H with `w=b` and one
with `w=c`; their unit vectors may differ because the bridge angles separate
the hooks.  K18H is necessary for the complete carrier, not sufficient for
coupling the two hooks, host closure or simplicity.

Two immediate scalar consequences are

```text
b^2 < u^2+v^2,       c^2 < u^2+v^2.                (2.2)
```

They follow by applying (2.1) to `d_12` and summing the squared coordinate
bounds.  They are weaker than K17S's central-chord condition
`h=a+b+c<sqrt(u^2+v^2)`, but the full directional cone (2.1) retains more
information.

## 3. The rigid hooks do not give a cheap no-go

The cone is nonempty even when `u!=v`.  Take

```text
v=1,       u=1001/1000,       w=1,
r=(3/5,4/5).                                      (3.1)
```

Then

```text
s_1=(3/5,4/5),
s_2=(3/5-7/(5*sqrt(2)), 4/5-1/(5*sqrt(2))),
s_3=s_2+(1001/1250,-3003/5000).                   (3.2)
```

Here `s_2` has negative first coordinate, while `s_1` is the rightmost
vertex.  The horizontal span is exactly

```text
7/(5*sqrt(2)) = 7*sqrt(2)/10 < 1                  (3.3)
```

because `98<100`.  Both intermediate vertical coordinates and both
coordinates of `s_3` have the signs displayed in (3.2); for the only close
case,

```text
997/5000 - 1/(5*sqrt(2)) > 0
```

because `997*sqrt(2)>1000`.  The vertical span is consequently `4/5`, below
`1001/1000`.  The remaining order comparisons follow from
`1001*sqrt(2)<1750`.  All claims reduce after squaring to strict positive
integer inequalities.  Hence (3.1) satisfies K18H exactly.

This is only a local three-edge control, not a K16W witness.  It proves that
the audit's requested first cone cannot by itself close K16B.

## 4. N35: the closure line never degenerates in K17S

Write `w_8=X+iY`.  Equation (7.1) of the rectangular-lens note is

```text
A*C+B*S=T,
A=v*X+u*Y,
B=u*X-v*Y,
T=(u^2+v^2+4*(X^2+Y^2)-h^2)/4.                  (4.1)
```

### ST-M1.N35

The line (4.1) cannot be identically satisfied in the terminal unit
direction `(C,S)` by any K17S solution.

### Proof

It is an identity in `(C,S)` only if `A=B=T=0`.  The linear map from `(X,Y)`
to `(A,B)` has determinant `-(u^2+v^2)`, which is nonzero for positive
`u,v`.  Thus `A=B=0` if and only if `w_8=0`.  But K17S includes the strict
`k=8` bounds

```text
0 < Re(Z*w_8) < v,       0 < Im(Z*w_8) < u,
```

which immediately exclude `w_8=0`.  If strict containment is dropped, the
remaining equality `T=0` would additionally force `h^2=u^2+v^2`; that is the
corner-to-corner central chord, not an omitted K17S case.  □

Hence every admitted bridge choice leaves an honest nonzero line cutting the
terminal unit circle in at most two points.

## 5. K18R: reflected global orientation is not lost

### ST-M1.K18R

The positive- and negative-turn K16B systems are isometric.  It is sufficient
to eliminate one sign provided the reflected sign is carried explicitly by
complex conjugation; feasibility, strict containment, simplicity and all
length equations are preserved.

### Proof

For a global turn sign `epsilon in {+1,-1}`, replace

```text
q by exp(epsilon*3*pi*i/4)
```

and use bridge units with the same sign convention.  Complex conjugation
sends the complete positive recursion to the negative recursion because all
edge lengths are real.  Reflect the whole geometric configuration and then
choose axes adapted to the reflected rectangular guard lens; this restores
the normalization `R=(0,0), Gamma=(v,0), Q=(v,u)`.  A Euclidean reflection
preserves every distance, intersection and strict inside/outside relation.
Thus a solution or contradiction for one sign transfers to the other.  □

This is an explicit quantifier reduction, not an assumption of chirality.

## 6. Remaining HC-26 obligation

K18H closes the requested rigid-hook analysis but does not settle K16W.  N35
and K18R remove the two exceptional quantifier cases named at admission.  The
remaining sessions must couple the two hook cones through the two bridge
units and the nondegenerate closure line, and then reach exactly one admitted
terminal outcome.  If neither a complete exact simple witness nor a scoped
K16B incompatibility theorem is proved, K16W freezes and the proposed next
checkpoint pivots to `gamma!=pi/2`.

