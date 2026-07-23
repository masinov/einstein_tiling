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

## 8. K23I: three full spokes force one angle interval

Write

```text
phi=pi-gamma                                             (8.1)
```

for the angle between the two rhombus basis vectors.  Normalize `d=1`.
If a unit displacement is

```text
u=r+s*exp(i*phi),                                       (8.2)
```

then a translate of its closed segment has both endpoints strictly inside
the unit rhombus only if

```text
|r|<1,       |s|<1.                                    (8.3)
```

Indeed the two endpoint differences in oblique coordinates are exactly
`(r,s)`.  Conversely, (8.3) lets the isolated segment be translated into the
open unit square in oblique coordinates.  Thus (8.3) is exact for an isolated
spoke, although it does not couple the three spokes into one spine.

Modulo an unoriented angle `pi`, successive spoke directions differ by

```text
2*tau=pi+gamma=-phi (mod pi).                          (8.4)
```

### ST-M1.K23I (corrected by ERR-012)

If all three `d` spokes of a K22S spine have their endpoints in the open
rhombus, then

```text
pi/3 < gamma < 2*pi/3.                                 (8.5)
```

For the non-right HC-28 family the right-angle point is treated separately by
N33, so the surviving domain is

```text
(pi/3,2*pi/3) minus {pi/2}.                            (8.6)
```

On the lower branch `pi/3<gamma<pi/2`, write the first `A` direction as

```text
delta=phi/2-epsilon.
```

The three isolated-spoke conditions force

```text
0 < epsilon < min(3*gamma-pi, phi/2).                 (8.7)
```

### Proof

For a unit vector at projective angle `psi`, its oblique coefficients are

```text
r=sin(phi-psi)/sin(phi),
s=sin(psi)/sin(phi).                                  (8.8)
```

First take the obtuse-lens range `0<gamma<pi/2`. Formula (8.8) shows that the
complete set of projective directions satisfying (8.3) is

```text
(-gamma,0) union (pi-2*gamma,gamma),                  (8.9)
```

where empty intervals are discarded and angles are read modulo `pi`.  Three
directions separated by `gamma` fit in (8.9) only if
`3*gamma>pi`; equality puts one of them on a rhombus side and violates the
strict inequality.  This proves the lower bound in (8.5).

The first code edge leaves `R` into the lens, so `0<delta<phi`.  Reflection
about the rhombus bisector changes `delta-phi/2` to its negative; choose the
representative `delta-phi/2=-epsilon`.  The first spoke line then has angle
`-epsilon`, and the other two have projective angles
`gamma-epsilon` and `2*gamma-epsilon`.  Membership in (8.9) gives
`epsilon<3*gamma-pi`; `delta>0` gives `epsilon<phi/2`.
All inequalities reverse directly to show these are the exact isolated-spoke
orientation conditions on this lower branch.

Now take the acute-lens range `0<phi<pi/2`, equivalently
`pi/2<gamma<pi`. Solving both strict sine inequalities in (8.8) gives the
complete projective direction set

```text
(0,phi) union (pi-phi,2*phi),                         (8.10)
```

where the second interval is nonempty exactly when `phi>pi/3`. The three
spoke directions differ by `phi` up to reversal in projective angle. If
`phi<=pi/3`, only the first interval survives and three successive directions
cannot all fit strictly. Thus `phi>pi/3`, or `gamma<2*pi/3`.

The omitted band is real. At `gamma=3*pi/5` and `phi=2*pi/5`, take the three
projective directions `pi/10`, `3*pi/10`, and `7*pi/10` (the same set as
the reflected-turn progression `54,126,198` degrees). Their six
oblique coefficients have absolute values

```text
sin(pi/10)/sin(2*pi/5)
or
sin(3*pi/10)/sin(2*pi/5),                             (8.11)
```

both strictly below one because
`0<pi/10<3*pi/10<2*pi/5<pi/2`. Hence the upper branch cannot be discarded.
Combining the two branches proves (8.5). □

K23I is a necessary family reduction.  It does not prove that the three
translated segments share compatible intermediate code edges.

## 9. Exact rational containment control

The surviving interval is not vacuous at the level of the 24 containment
inequalities.  Choose

```text
cos(gamma/2)=4/5,       sin(gamma/2)=3/5,
z=(4+3*i)/5,            d=1,
(a,b,c)=(19/20,17/20,1/2).                           (9.1)
```

Then

```text
cos(gamma)=7/25,        sin(gamma)=24/25,
q=(-3+4*i)/5,           g=(-7+24*i)/25.              (9.2)
```

In the rhombic basis `(1,g)`, the six unit direction increments
`z*q^j`, `0<=j<=5`, are

```text
( 39/40,          5/8),
(-527/600,        7/24),
( 79/1000,      -39/40),
(11753/15000,   527/600),
(-25481/25000,  -79/1000),
(164833/375000,-11753/15000).                        (9.3)
```

After multiplying alternately by `a,1,b,1,c,1`, the six partial sums are

```text
(741/800,              19/32),
(23/480,               85/96),
(863/7500,             17/300),
(4493/5000,           187/200),
(19449/50000,        1791/2000),
(621401/750000,      3359/30000).                    (9.4)
```

Every numerator in (9.4) is strictly between `0` and its denominator, so all
first-half and centrally paired vertices satisfy (4.1) exactly.  This control
does **not** satisfy closure: `h=23/10`, while the rhombus diameter is

```text
2*cos(gamma/2)=8/5.                                  (9.5)
```

It proves only that containment is nonempty inside K23I's surviving interval.
Consequently a family closure must couple containment to the host chord; it
cannot dismiss the interval as an isolated-spoke or prefix artifact.

## 10. Session-136 disposition

K23I closes every non-right guard angle outside
`(pi/3,2*pi/3) minus {pi/2}`. The exact rational control (9.1)--(9.5) lies on
the lower branch and shows why the surviving domain is a real coupled
problem. The original session-136 text incorrectly omitted the acute-lens
band; ERR-012 is controlling. HC-28's later exact controls remain on the
lower branch and are unaffected.

## 11. K24C: exact containment and closure coexist

The proposed containment-to-diameter implication is false.  Retain the exact
non-right angle and turn from (9.2), but choose

```text
z=(24+7*i)/25,        d=1,
a=3/4,                b=1/2.                        (11.1)
```

The six unit increments in rhombic coordinates are now

```text
( 25/24,    7/24),
( -5/8,      5/8),
( -7/24,  -25/24),
( 39/40,     5/8),
(-527/600,  7/24),
( 79/1000, -39/40).                                  (11.2)
```

Let

```text
c_* = 11377/7500 - 2*sqrt(1586086)/1875.            (11.3)
```

The exact comparison

```text
1/6 < c_* < 7/40                                      (11.4)
```

follows equivalently from the sign change below.  The six partial sums are

```text
p_1 = (25/32, 7/32),
p_2 = ( 5/32,27/32),
p_3 = ( 1/96,31/96),
p_4 = (473/480,91/96),
p_5 = (473/480-527*c_*/600, 91/96+7*c_*/24),
p_6 = (12773/12000-527*c_*/600, -13/480+7*c_*/24).
                                                               (11.5)
```

Every coordinate in (11.5) lies strictly between zero and one.  For the last
two points this follows directly from (11.4); the closest endpoint checks are

```text
91/96+(7/24)*(7/40)=959/960<1,
-13/480+(7/24)*(1/6)=31/1440>0.                     (11.6)
```

The other bounds are weaker rational comparisons.

For variable `c`, direct exact expansion of the central-edge condition gives

```text
|Q-2*z*w_6|^2-(a+b+c)^2
  = (150000*c^2-455080*c+74471)/50000.              (11.7)
```

Its values at the two rational endpoints are

```text
F(1/6)=2791/50000>0,
F(7/40)=-2297/200000<0.                              (11.8)
```

The smaller quadratic root is exactly (11.3), while the other root exceeds
`2`.  Hence (11.4) holds and `F(c_*)=0`.

### ST-M1.K24C

The exact data (9.2), (11.1), and (11.3) satisfy every K22S open-rhombus
containment inequality and the exact host closure equation, with

```text
h=5/4+c_* < 57/40 < 8/5.                             (11.9)
```

Thus changing the guard angle genuinely escapes N33 at the coupled
containment-and-closure level.  This is still not a carrier witness because
simplicity has not been imposed.

## 12. N36: the exact closed control self-intersects

The failure of simplicity is exact and occurs before the algebraic coordinate
`c_*` enters.  In oblique coordinates, segment `p_1 p_2` and the nonadjacent
segment `p_3 p_4` meet because

```text
p_1+(7/12)*(p_2-p_1)
 = p_3+(5/12)*(p_4-p_3)
 = (5/12,7/12).                                     (12.1)
```

Both parameters lie strictly between zero and one.  The four orientation
determinants, in the same order, are

```text
5/12, -7/12, -7/12, 5/12,                           (12.2)
```

so this is a transverse interior crossing.  The rhombic coordinate map is
invertible, hence the physical spine crosses at the corresponding physical
point as well.

### ST-M1.N36

K24C is an exact self-crossing containment-and-closure control, not a simple
K22S carrier.  It disproves the proposed family-wide diameter obstruction but
proves neither existence nor nonexistence of another simple point in the same
semialgebraic family.

## 13. HC-28 disposition

The three sessions have produced a complete family, the sharp necessary angle
interval, and an exact proof that non-right geometry escapes N33 through
closure.  They have not produced a simple spine or a family-wide simplicity
obstruction.  HC-28's third terminal outcome therefore fires:

### ST-M1.K24W

Determine whether the K22S family has a point in

```text
(pi/3,2*pi/3) minus {pi/2}                            (13.1)
```

satisfying all 66 nonadjacent-segment predicates. This is open and
**frozen**. Reopening requires either complete exact simple data or a
separately authorized decision procedure for this already serialized family;
another angle sample, guessed central direction, or weakened intersection
list is not admissible. Any decomposition must cover both connected
non-right subintervals.

No polygon, two-patch placement, all-tilings decoder, aperiodicity theorem or
candidate has been obtained.

### HC-29 supersession

The freeze above is the historical HC-28 disposition. K25X and N37 in
`34_nonright_spoke_crossing.md` subsequently prove that `p_1p_2` and
`p_3p_4` cross throughout the complete corrected K23I domain. K24W is
therefore closed/refuted for this fixed family; no decision run was needed.
