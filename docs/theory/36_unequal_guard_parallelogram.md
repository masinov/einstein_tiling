# Unequal-guard parallelogram transfer

**Date:** 2026-07-23

**Status:** HC-30 secondary symbolic assessment; exact conditional family,
no contact-role proof, solver, polygon, patch or candidate

**Scope:** K22R's equal internal spokes and symmetric sharp-angle assignment,
but with two independent guard-lens side lengths

## 1. K28G: the conditional parallelogram family

Put `phi=pi-gamma`, `g=exp(i*phi)`, and choose positive guard-side lengths
`e,f`. Normalize

```text
R=0,
Gamma=e,
Q=e+f*g.                                         (1.1)
```

Half-turn about `Q/2` sends `Gamma` to `Q-Gamma=f*g`; the two guard paths
therefore bound the parallelogram

```text
P={alpha*e+beta*f*g: 0<=alpha,beta<=1}.          (1.2)
```

Retain K22R's internal equal-spoke length `d`, turn
`q=exp(i*(pi+gamma)/2)`, and relative partial sums

```text
w_0=0,
w_1=a,
w_2=a+d*q,
w_3=a+d*q+b*q^2,
w_4=a+d*q+b*q^2+d*q^3,
w_5=w_4+c*q^4,
w_6=w_5+d*q^5.                                   (1.3)
```

For a unit terminal direction `z`, let `(alpha_k,beta_k)` be the unique
coefficients satisfying

```text
z*w_k=alpha_k*e+beta_k*f*g.                      (1.4)
```

### ST-M1.K28G

Conditional on the distinct guard sides `e,f` being legitimate intrinsic
roles in the K9A/K9T contact language, the complete carrier-spine obligation
is

```text
0<alpha_k<1,   0<beta_k<1,       k=1,...,6,

|Q-2*z*w_6|^2=(a+b+c)^2,                         (1.5)
```

together with disjointness of the same 66 nonadjacent segment pairs as
K22S. Central inversion gives the paired vertices. Setting `e=f=d`
recovers K22S exactly.

### Proof

Equations (1.1)--(1.2) are the unequal-side version of K22R's guard lens.
The internal boundary word and turns are unchanged, giving (1.3). A point
is in the open parallelogram exactly when both coefficients in (1.4) lie in
`(0,1)`. Half-turn pairing and the central host edge are unchanged except
for the new diagonal `Q`. This proves (1.5) and its converse at the
carrier-spine level. □

K28G is conditional because changing the two guard-side occurrences from
the old common length `d` to new intrinsic lengths changes role recognition
and complete cover tables. Geometry alone does not prove that every tiling
uses them as the intended guard path.

## 2. K28T: K25X transfers but N37 does not

For a unit displacement written in the unit oblique basis as

```text
u_0=r+s*g,                                        (2.1)
```

a length-`d` translate has normalized parallelogram-coordinate changes

```text
d*r/e,    d*s/f.                                  (2.2)
```

Thus an isolated length-`d` spoke translates strictly inside (1.2) exactly
when

```text
d*|r|<e,    d*|s|<f.                              (2.3)
```

K25X is internal to the spine and is unchanged:

```text
u=b/(2*d*sin(gamma/2)),   t=1-u.                 (2.4)
```

### ST-M1.K28T

N37's containment-versus-crossing squeeze does not transfer to independent
`e,f`. Conditions (2.3) scale with the guard sides, while the simplicity
threshold

```text
b>2*d*sin(gamma/2)                               (2.5)
```

depends only on the internal spoke length.

### Exact separation control

Take the non-right rational trigonometric data

```text
cos(gamma/2)=4/5,   sin(gamma/2)=3/5,
d=1,                b=2,
e=10,               f=11.                        (2.6)
```

Here `sin(phi)=sin(gamma)=24/25`. Formula (8.8) of the K23I analysis bounds
the absolute oblique coefficient of every unit direction by `25/24`.
Therefore each internal spoke has coordinate changes below `25/24`, and a
length-`b` code edge has changes at most `25/12`; all are strictly below
both guard scales `10,11`. Meanwhile

```text
b=2>6/5=2*d*sin(gamma/2),                         (2.7)
```

so the K25X pair does not intersect. This is an exact local separation of
containment from the crossing threshold, not a K28G spine or tile witness.

## 3. HC-30 secondary disposition

Unequal guard legs are a genuinely live hypothesis at the symbolic geometry
level: K25X transfers, but the theorem that closed K22S does not. The next
missing statement is upstream of coordinates:

### ST-M1.K28W

Prove that the two new intrinsic guard-side roles `e,f`, their intended
half-turn docking, and every competing complete or subdivided contact are
compatible with the K9A/K9T selector and recognizable in the full local
closure. Only then derive or decide the complete K28G system (1.5).

K28W is open and frozen. A solver run on (1.5), an angle sample or a drawing
before the role/cover-table theorem would repeat the color-as-geometry error
that the earlier K2J/K3G gates prohibit.

## HC-38 supersession

Theory note 49 supplies the missing upstream role theorem and refutes the
route. In the unchanged boundary word, every `B,C` endpoint is flanked by an
internal side of length `d`. The selected `(B,C)` and `(C,B)` primary stars
therefore force both complete guard sides to equal `d` (N44). Genuinely
unequal `e,f` cannot enter K9A/K9T; the collapsed case `e=f=d` is K22S and is
already refuted by N37 (N45). Thus K28W is closed for complete clean spokes.
Partial, multi-edge or contextual guard contacts are not silently included.
