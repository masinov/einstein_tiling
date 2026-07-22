# Unequal-spoke right-angle guard

**Status:** HC-25 topology proof draft; no polygon, coordinates or candidate

**Retained data:** K9A/K9T complete clean spokes, `gamma=pi/2`,
`theta=rho_X=pi/4`, central guard--shield half-turn and full Euclidean
isometries

**Changed datum:** outgoing spoke length `u` and incoming spoke length `v`
may differ

## 1. Directed spoke roles

At a selected primary transition `X|Y`, K9A's guard has two complete sides:

```text
right endpoint of X -- length u -- guard,
guard -- length v -- left endpoint of Y.              (1.1)
```

Equivalently, the intrinsic side immediately leaving the right endpoint of
each left role `X in {A,B,C}` has length `u`, while the side immediately
leaving the left endpoint of each right role `Y in {B,C}` has length `v`.
These are directed boundary roles, not two names for an unmeasured port.

## 2. N34: the old connector forces equal legs

### ST-M1.N34

K10B's original 15-edge boundary word cannot realize the complete clean-
spoke equations with `u!=v`.

### Proof

In the old word, the boundary segment between the intrinsic `A` and `B`
sides is one complete side. At its `A` endpoint it is the outgoing spoke
`u_A`, hence has length `u`. At its `B` endpoint the same segment is the
incoming spoke `v_B`, hence has length `v`. A polygonal side has one length,
so `u=v`. The one-side connector between `B` and `C` gives the same identity.
The paired half of the spine repeats both identities. □

Thus unequal guard legs are not a numerical variation of K10B. They require
a changed boundary topology. N33 cannot be evaded merely by replacing some
printed `d` labels with `u` and others with `v` on the old word.

## 3. K16B: minimal split-spoke lift

Each incompatible `A--B` and `B--C` connector needs at least one new boundary
vertex so an outgoing `u` side and incoming `v` side can be distinct. The
minimal centrally paired split replaces each such connector by the ordered
two-side path `u,v`. It leaves the outgoing `C--H` side as `u`, because `H`
has no K9A incoming-`v` role.

The first half-spine is therefore

```text
A,u,v,B,u,v,C,u,                                      (3.1)
```

and central pairing fixes the complete spine as

```text
A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A.                  (3.2)
```

Choose the guard path from `R` to `Q` to have consecutive lengths `v,u`.
The resulting cyclic carrier word is

```text
v,A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A,u.              (3.3)
```

It has 19 sides. Relative to K10B, the four added sides are forced by the two
split connectors and their centrally paired copies. Up to cyclic reversal,
(3.3) is the unique edge-count-minimal split of those four one-side
connectors while leaving every other K10B adjacency unchanged.

### Angle inventory

The five retained sharp vertices on the first half are

```text
A|u,  v|B,  B|u,  v|C,  C|u,                        (3.4)
```

each with carrier angle `pi/4`. The new bridge vertices `u|v` have
irredundant angles `delta_1,delta_2 in (0,2*pi)\{pi}`, to be derived rather
than guessed. The
`u|H` angle and terminal `v|A` angle remain free under the earlier K10B
contract, and the paired half has complementary shield contexts.

### Status

K16B is a finite combinatorial carrier topology, not a realization theorem.
In particular it has not proved:

- that the two new bridge angles can be recognized without markings;
- that the many repeated `u` and `v` sides have complete cover tables;
- simplicity or containment of its spine;
- either complete `ABC/ACB` placement patch; or
- the all-tilings converse.

## 4. Rectangular guard lens

Put

```text
R=(0,0),       Gamma=(v,0),       Q=(v,u).           (4.1)
```

The half-turn about `(v/2,u/2)` sends `Gamma` to `(0,u)`. The two guard paths
therefore bound the exact rectangle

```text
L(u,v)=[0,v] x [0,u].                                (4.2)
```

This is the sole geometric gain admitted by HC-25: the square has become a
rectangle, and the incompatible connector has become the explicit `u|v`
bridge. No additional junction participant or contact radius is introduced.

## 5. Next exact obligation

Let the signed exterior bridge turns be

```text
sigma_i=pi-delta_i,       i=1,2.                     (5.1)
```

Session 129 must apply the fixed turn sequence

```text
3*pi/4, sigma_1, 3*pi/4, 3*pi/4,
sigma_2, 3*pi/4, 3*pi/4                              (5.2)
```

to (3.1), derive every first-half partial sum, impose central host closure
and all rectangle inequalities, and determine whether the free bridge angles
are genuine geometric degrees of freedom or merely unmarked colors. No
coordinate fitting or angle enumeration is admitted.

## 6. K17S: complete rectangular-lens system

Put

```text
q=(-1+i)/sqrt(2),
z_j=cos(sigma_j)+i*sin(sigma_j),       j=1,2.         (6.1)
```

Before the terminal rotation, the first-half partial sums of (3.1) are

```text
w_0 = 0,
w_1 = a,
w_2 = a+u*q,
w_3 = a+u*q+v*q*z_1,
w_4 = w_3+b*q^2*z_1,
w_5 = w_4+u*q^3*z_1,
w_6 = w_5+v*q^3*z_1*z_2,
w_7 = w_6+c*q^4*z_1*z_2,
w_8 = w_7+u*q^5*z_1*z_2.                         (6.2)
```

These are exactly the edge directions obtained from (5.2). Let

```text
Z=C+i*S,       C^2+S^2=1,       C>0, S>0,            (6.3)
```

and write `D=v+i*u` for the rectangle diagonal. Central pairing gives all
spine vertices:

```text
p_k       = Z*w_k,
p_(17-k)  = D-Z*w_k,                 0<=k<=8.         (6.4)
```

The central host edge is `D-2*Z*w_8`.

### ST-M1.K17S

The K16B spine has relative interior in the open rectangular lens and central
edge length `h=a+b+c` if and only if there are unit variables `Z,z_1,z_2`,
with `z_j notin {1,-1}`, satisfying

```text
0 < Re(Z*w_k) < v,
0 < Im(Z*w_k) < u,                    k=1,...,8,       (6.5)

|D-2*Z*w_8|^2 = h^2.                                 (6.6)
```

The exclusions remove the zero/`2*pi` degenerate angle and the reducible
straight angle. The opposite global turn orientation is the reflected system.

### Proof

Equation (6.2) is the complete turn recursion. Conditions (6.3) and (6.5)
put the first edge and every first-half vertex strictly inside the tangent
rectangle. Equation (6.4) puts the paired vertices inside as well, and
convexity of the rectangle contains every intervening open segment. Equation
(6.6) is exactly the prescribed central length. The converse reads the same
three unit directions from any admitted spine. □

As before, lens containment does not imply spine simplicity. The finite
nonintersection predicates for the seventeen explicit segments remain a
separate condition.

## 7. Closure remains a line in the terminal orientation

Write `w_8=X+iY` and `R_8=X^2+Y^2`. Expanding (6.6) gives

```text
(v*X+u*Y)*C + (u*X-v*Y)*S
  = (u^2+v^2+4*R_8-h^2)/4.                           (7.1)
```

Thus fixed weights and bridge angles again leave at most two terminal
orientations, unless the line degenerates identically. Before the strict
rectangle inequalities, an orientation exists exactly when the squared
right side of (7.1) does not exceed

```text
(v*X+u*Y)^2+(u*X-v*Y)^2=(u^2+v^2)*R_8.              (7.2)
```

Equations (6.1)--(7.2) are a finite exact semialgebraic system. No angle or
coordinate grid is being sampled.

## 8. K17G: bridge angles are geometry, not colors

### ST-M1.K17G

For `u!=v`, each K16B bridge angle is locally recoverable from the unmarked
polygon boundary germ consisting of its ordered incident side lengths
`(u,v)` and its interior angle. Consequently fixed values
`delta_1,delta_2` are genuine shape parameters, not per-occurrence symbolic
states.

### Proof

A Euclidean isometry preserves side lengths, their incidence and the
interior angle. Since `u!=v`, the ordered pair distinguishes the two rays up
to the declared reflection. If the two bridge angles differ, their numerical
values distinguish their intrinsic roles directly. If they agree, the
neighboring distinct code-side contexts in (3.3) distinguish their boundary
positions. In either case, one polygon fixes the values once; an occurrence
cannot choose a different `delta_j` without ceasing to be congruent. □

K17G does not prove that either bridge is forced to participate in an
intended contact. It proves only that retaining the variables in K17S does
not smuggle markings into the carrier.

## 9. Session-130 stop

The unequal-spoke relaxation now has one exact bounded question. Session 130
must eliminate or instantiate the two bridge directions analytically and
either:

1. give one exact simple open-rectangle spine satisfying K17S, together with
   its fixed bridge angles and all segment nonintersection proofs; or
2. prove a scoped incompatibility theorem for K16B.

Failure to do either closes HC-25 without coordinates. A numerical fit,
angle enumeration, extra bridge edge, changed guard angle, placement-patch
claim, SVG or candidate promotion is not an accepted outcome.
