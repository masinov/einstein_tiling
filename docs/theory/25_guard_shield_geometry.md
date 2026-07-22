# K10 — guard-and-shield geometry

**Date:** 2026-07-22

**Status:** exact admission and obstruction draft; no polygonal witness,
whole-plane forcing or monotile claim

## 1. HC-19 role inventory

HC-19 attempts exact geometry for K9T. The single congruence class must make
six occurrence roles locally recoverable; role names are not colors:

| occurrence role | intrinsic feature used in that pose | recognition burden |
|---|---|---|
| host `H` | one straight side of length `h` | distinguish it from every code and docking side |
| code `A` | straight side of length `a` | `a,b,c` pairwise distinct and `a+b+c=h` |
| code `B` | straight side of length `b` | directed endpoint/adjacent-arc type recoverable |
| code `C` | straight side of length `c` | directed endpoint/adjacent-arc type recoverable |
| guard `G` | vertex `Gamma` of angle `gamma` and its two incident contact arcs | identify the guard pose, including which arc faces left/right |
| shield `W` | one contact arc joining the two terminal stars | distinguish its two terminal endpoint roles |

The terminal vertices `Q,R` and the arcs `G--X`, `G--W`, `G--Y` must also be
recognizable from the unmarked contact patch. A valid proposal must enumerate
every repeated length/angle and explain why it does not permute the six
roles. Pairwise-distinct `a,b,c,h` recognizes the host word but is not by
itself a recognition proof for `G,W`.

HC-19 first takes K9V's convex role-reuse branch. Only after that branch is
proved impossible may it consider one explicitly named nonconvex skeleton.
Failure to supply one exact polygon and both shield patches by session 114
closes K9T without a coordinate search or larger atlas.

## 2. Complete clean-spoke hypotheses

Retain K9A's angles

```text
ell_B=ell_C=theta,
rho_A=rho_B=rho_C=pi-gamma-theta,                    (2.1)
```

and K9's complete clean guard spokes. If the guard sides at `Gamma` have
lengths `u,v`, then

```text
u_A=u_B=u_C=u,       v_B=v_C=v.                      (2.2)
```

Here `u_X` is the complete boundary side leaving the right endpoint of code
side `X`, and `v_X` leaves its left endpoint. The code sides `B,C` have
distinct lengths. These hypotheses are precisely the fixed-pose geometry
retained by K9T; allowing partial spokes or contextual guard poses would be a
different route.

## 3. N25: the convex role-reuse branch is empty

K9V already proves that a convex carrier must make `B,C` adjacent and must
identify `Gamma` with one of the three vertices incident to their union.

### ST-M1.N25

No irredundant convex polygon satisfies K9A, the complete clean-spoke
conditions (2.2), pairwise-distinct code lengths, and the K9V guard-role reuse
condition.

### Proof

Let `V` be the shared endpoint of adjacent sides `B,C`.

**Case 1: `Gamma=V`.** Its angle `gamma` is one of the two endpoint values
`theta,rho` of both code sides.

- If `gamma=theta` and `theta!=rho`, `V` is the directed left endpoint of
  both `B,C`. The only other polygon side leaving that endpoint of `B` is
  `C`, and conversely the side leaving `C` is `B`. Hence
  `v_B=c` and `v_C=b`. Equation (2.2) forces `b=c`, contrary to role
  recognition.
- If `gamma=rho` and `theta!=rho`, the same argument at the common directed
  right endpoint gives `u_B=c`, `u_C=b`, again forcing `b=c`.
- If `gamma=theta=rho`, (2.1) gives `3*gamma=pi`. K9V then leaves
  `pi-3*gamma=0` exterior turn for the required `A,H` boundary, contradicting
  irredundancy.

**Case 2: `Gamma` is an outer endpoint of `B union C`.** Without loss it is
an outer endpoint of `B`; write `alpha` for the interior angle at `V`.
The two endpoint angles of `B` sum to `pi-gamma` by (2.1). Since one is the
guard angle `gamma`, the other is

```text
alpha = pi-2*gamma.
```

But K9V requires the strict inequality `alpha+2*gamma<pi`, while this identity
gives equality. If the two endpoint values coincide, then
`theta=rho=gamma=pi/3` and the same zero-remainder contradiction results.
The outer endpoint of `C` is symmetric.

All possible reused vertices are exhausted. □

## 4. Consequence

The cheaper side of K9V's dichotomy is now closed, not merely unsuccessful:

```text
K9T + fixed complete spokes + distinct code roles  =>  carrier nonconvex.
```

The obstruction is structural. It does not depend on coordinates, a search
budget or a guessed boundary word. It also identifies exactly which
hypothesis a future alternative must change: permit contextual guard poses,
partial/multi-edge spokes, or abandon distinct side-length role recognition.
HC-19 changes none of those silently.

The remaining two sessions may study one nonconvex right-angle shield
skeleton, with all six roles retained. Local sector closure alone will not be
accepted as a polygonal witness.

## 5. K10B: one fixed nonconvex boundary skeleton

The only nonconvex topology admitted for sessions 113--114 fixes

```text
gamma=pi/2,       theta=rho_X=pi/4,       ell_A!=pi/4,
a=1,              b=2,                    c=4,
h=a+b+c=7.                                         (5.1)
```

Let every complete guard spoke have one further length `d>0`, distinct from
`1,2,4,7`. The intrinsic cyclic side-length word of the proposed carrier is

```text
d, A, d, B, d, C, d, H, d, C, d, B, d, A, d.       (5.2)
```

The first and last `d` sides meet at the unique guard vertex `Gamma`; the
middle thirteen sides form the **shield spine** `S`. The unique `H` side
roots the spine. The two occurrences of each of `A,B,C` are one intrinsic
role exchanged by reversal. Every used code side has a `d` side on the
required endpoint, so (2.2) holds with `u=v=d`.

The angle requirements on one half of (5.2) are

```text
angle(Gamma)=pi/2,
angle(A|d)=angle(d|B)=angle(B|d)
             =angle(d|C)=angle(C|d)=pi/4,           (5.3)
```

while the unused guard-leg/`A` endpoint has `ell_A!=pi/4`. The reversed half
inherits the corresponding reflected roles. Angles at `d|H|d` are free apart
from simplicity and the polygon angle sum; this is where nonconvex turn must
occur.

## 6. Exact guard--shield isometry

Place the spine endpoints at `R=-Q` and require vertices
`p_0=R,...,p_13=Q` with

```text
p_(13-i) = -p_i.                                    (6.1)
```

The edge labels from `R` to `Q` are

```text
A,d,B,d,C,d,H,d,C,d,B,d,A.                          (6.2)
```

Condition (6.1) makes `S` invariant as a set under the half-turn
`J(x)=-x`, with its endpoints exchanged. Choose `Gamma` on one side of the
chord so

```text
|Gamma-R|=|Gamma-Q|=d,
angle(R,Gamma,Q)=pi/2.                              (6.3)
```

Thus `|R-Q|=d*sqrt(2)`. Define the carrier boundary as the two guard sides
`Gamma--R`, `Q--Gamma` plus `S`. Its half-turned occurrence has guard vertex
`-Gamma`, shares the complete spine `S`, and uses the opposite side of it.

### ST-M1.K10B

If the spine is simple, meets the two guard sides only at `R,Q`, and lies in
the closed lens bounded by the upper broken path
`R--Gamma--Q` and its half-turn, then the carrier and its half-turn have
disjoint interiors and share exactly `S`. The relative guard--shield
isometry is the exact half-turn `J`; no docking choice remains.

### Proof

The two broken paths and the simple spine divide the lens into the two closed
regions bounded respectively by `S` and each broken path. Half-turn `J`
exchanges the broken paths and reverses `S`, hence exchanges the two regions.
Their interiors are disjoint and their common boundary is exactly `S`. □

K10B is conditional on the three explicit geometric predicates in its first
sentence. It is not a coordinate construction.

## 7. Role-recognition audit of the skeleton

The boundary word (5.2) addresses the HC-18 audit burden without silently
assuming six colors:

- `H` is the unique side of length `7`;
- `A,B,C` are the length classes `1,2,4`, respectively;
- `Gamma` is the unique `pi/2` vertex whose two incident sides both have
  length `d` and whose opposite boundary arc contains the unique `H`;
- the guard pose is rooted by `Gamma` and the ordered `A,B,C,H` progression;
- the shield pose is the unique full-spine contact rooted by `H`; and
- the two occurrences of each code length are declared the same role under
  reversal, which is already the quotient used by K6O.

This audit assumes every other `d|d` or repeated-angle context is excluded by
the final coordinate list. If such a context appears, guard recognition
fails. Likewise, the length word alone does not force another occurrence to
cover the entire spine; K10B supplies one exact docking, not the all-tilings
converse.

## 8. The remaining coordinate system

An HC-19 witness is now a finite list `p_0,...,p_13,Gamma` satisfying:

1. the side lengths and central pairing (5.2), (6.1);
2. the five `pi/4` endpoint angles and `ell_A!=pi/4` in (5.3);
3. the right-angle equal-leg guard equations (6.3);
4. simplicity and the K10B lens containment inequalities;
5. no unlisted repeated guard context; and
6. exact placements of the remaining host/code/guard occurrences for both
   `ABC` and `ACB`, with all pairwise interiors disjoint.

Conditions 1--5 construct only the guard/shield pair. Condition 6 is still
the decisive patch obligation. Session 114 may not replace it with a sketch
or an optimizer.
