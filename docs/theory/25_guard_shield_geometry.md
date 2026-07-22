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
