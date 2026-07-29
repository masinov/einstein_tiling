# Non-right spoke-crossing closure

**Date:** 2026-07-23

**Status:** HC-29 proof-draft family no-go; no solver run, polygon, placement
patch, or candidate

**Scope:** the equal-spoke, equal-leg K22S rhombic family of
`33_nonright_guard_rhombic_family.md`, including both corrected K23I branches

## 1. The N36 crossing is symbolic

Retain the notation of K22R:

```text
q=exp(i*(pi+gamma)/2),
p_1=z*a,
p_2=p_1+z*d*q,
p_3=p_2+z*b*q^2,
p_4=p_3+z*d*q^3.                              (1.1)
```

Here `a,b,d>0`, `0<gamma<pi`, and `|z|=1`. The first and third
segments in (1.1) are nonadjacent. Their possible intersection is

```text
p_1+t*z*d*q = p_3+u*z*d*q^3.                  (1.2)
```

### ST-M1.K25X (exact spoke-pair criterion)

The two supporting lines in (1.2) meet at the unique parameters

```text
u = b/(2*d*sin(gamma/2)),
t = 1-u.                                      (1.3)
```

Consequently:

- if `0<b<2*d*sin(gamma/2)`, the two segments cross transversely in
  their interiors;
- if `b=2*d*sin(gamma/2)`, their nonadjacent endpoints coincide,
  `p_1=p_4`;
- a simple K22S spine therefore requires

```text
b>2*d*sin(gamma/2).                            (1.4)
```

The same criterion holds for the reflected global turn orientation.

### Proof

Subtract `p_1` in (1.2) and divide by the nonzero number `z*d*q`:

```text
t = 1+(b/d)*q+u*q^2.                           (1.5)
```

Write `x=cos(gamma/2)` and `y=sin(gamma/2)`. Since

```text
Im(q)=x,
Im(q^2)=-sin(gamma)=-2*x*y,
```

the imaginary part of (1.5) gives `u=b/(2*d*y)`. Its real part then
gives `t=1-u`. The two directions are nonparallel because their angle
modulo `pi` is `gamma`, strictly between zero and `pi`, so the line
intersection is unique and every interior intersection is transverse.
At equality, `(t,u)=(0,1)`, which is exactly `p_1=p_4`. Complex
conjugation proves the reflected statement. □

For K24C, `b=1/2`, `d=1`, and `sin(gamma/2)=3/5`; (1.3) gives
`u=5/12`, `t=7/12`, recovering N36 without using the algebraic value
`c_*`.

## 2. The upper branch cannot satisfy simplicity

Suppose

```text
pi/2 <= gamma < 2*pi/3.                        (2.1)
```

In the notation `x=cos(gamma/2)`, `y=sin(gamma/2)`, one has `y>=x`.
The two diagonals of the side-`d` rhombus have lengths `2*d*x` and
`2*d*y`; hence its diameter is `2*d*y`.

K22S places `p_2` and `p_3` strictly inside this rhombus. Their
distance is the intervening code-edge length `b`, so strict interior
containment gives

```text
b < 2*d*y.                                     (2.2)
```

K25X now puts the intersection parameters strictly in `(0,1)`. Thus
the two nonadjacent spokes cross.

The strictness in (2.2) does not hide a boundary case: the diameter of
a compact parallelogram is attained at a pair of opposite vertices,
whereas both K22S points are in its open interior.

## 3. The lower branch cannot satisfy simplicity

Now suppose

```text
pi/3 < gamma < pi/2.                            (3.1)
```

Put `phi=pi-gamma`. By the corrected lower-branch K23I
parameterization, after reflecting if necessary the first `A` direction is

```text
delta=phi/2-epsilon,
0<epsilon<min(3*gamma-pi,phi/2).                (3.2)
```

The code edge `p_2p_3` has direction `z*q^2`, whose physical angle in
the rhombic basis is

```text
delta-phi = -phi/2-epsilon.                     (3.3)
```

For a unit vector at that angle, the absolute change of its second
oblique coordinate is

```text
A = sin(phi/2+epsilon)/sin(phi)
  = cos(gamma/2-epsilon)/(2*x*y).               (3.4)
```

Since `gamma>pi/3`,

```text
epsilon < phi/2 < gamma,
```

and therefore `|gamma/2-epsilon|<gamma/2`. Cosine is even and strictly
decreasing on `[0,pi]`, so (3.4) gives

```text
A > cos(gamma/2)/(2*x*y) = 1/(2*y).             (3.5)
```

The endpoints `p_2,p_3` are strictly inside the side-`d` rhombus.
Their second normalized oblique coordinates therefore differ by strictly
less than one. Equations (3.4)--(3.5) imply

```text
(b/d)*A < 1,
b < d/A < 2*d*y.                                (3.6)
```

K25X again forces a transverse interior crossing of the two nonadjacent
spokes.

## 4. ST-M1.N37: family-wide simplicity no-go

No K22S point has a simple spine.

### Proof

K23I restricts three strictly contained full spokes to

```text
pi/3 < gamma < 2*pi/3.                           (4.1)
```

Section 2 forces a transverse spoke crossing on the upper branch, including
the right-angle point, and Section 3 forces the same crossing on the lower
branch. The endpoints of (4.1) are already excluded by K23I's strict
containment. These cases exhaust the K22S family. □

N37 uses only K22S containment, not the host-closure equation or any of the
other 65 nonintersection predicates. It is therefore stronger than an
UNSAT result for the complete K24W sentence: one named segment pair already
contradicts simplicity.

## 5. HC-29 disposition

K24W is **closed** by N37. The exact K24C data remain useful as a sharp
lower-branch control: K25X specializes to the previously reported N36
intersection parameters.

No semialgebraic cell survives the theorem-first step. Under D-0155, an
SMT/CAD/QE runner would now have no logically live domain and is not
admissible. HC-29 therefore closes after one theorem session with no
research computation and no artifact growth.

This result closes only the fixed K22R/K22S equal-spoke, equal-leg,
centrally-paired rhombic carrier. It does not close K16W's unequal-spoke
rectangle, different side words, unequal guard legs, additional hinges or
participants, or the broader K4W monotile contract. No tile has been found.
