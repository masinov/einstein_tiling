# Determinism, periodicity, and the undecidable compiler boundary

**Date:** 2026-07-27
**Scope:** finite symbolic contact systems; the final shape-only one-polygon
subfamily is explicitly not claimed undecidable

Let `Y` be the nonempty aperiodic finite local system supplied by the
Akiyama--Hamada--Ito `sqrt(2)-1` construction. A geometric monotile solution
would induce a nonempty finite-local-complexity carrier system `X` together
with a finite-radius equivariant map `X -> Y` defined on every carrier tiling.

## 1. Root-deterministic carriers are impossible (N55)

Call a finite-alphabet `Z^2` carrier **root-deterministic** when the state at
one fixed cell determines at most one whole-plane configuration. This
includes a forced periodic scaffold whose complete side docking uniquely
propagates the neighbor pose in every direction.

### Theorem

Every nonempty root-deterministic carrier contains only periodic
configurations. Hence it admits no translation-equivariant map to `Y`.

### Proof

There are at most as many whole-plane configurations as rooted states, so
the carrier space `X` is finite. Translation acts on this finite set. For any
`x in X`, its stabilizer is a finite-index subgroup of `Z^2` and therefore
contains two linearly independent nonzero translations. Thus `x` is
periodic. If `pi:X->Y` were equivariant, every period of `x` would be a
period of `pi(x)`, contradicting aperiodicity of `Y`. QED.

This is the broad form of the repeated deterministic-docking failures. A
successful carrier must have contextual branching: the same rooted local
pose must extend in more than one way, while a larger finite neighborhood
still recovers the Sturmian state.

## 2. The unrestricted symbolic compiler problem is undecidable (U1)

Define `STURMIAN-COMPILER` as follows. The input is a finite two-dimensional
SFT `X` and a specified finite-radius block map `pi` to `Y`. Decide whether

1. `X` is nonempty; and
2. `pi` is total on `X` and has image in `Y`.

### Theorem

`STURMIAN-COMPILER` is undecidable, already when `pi` is a one-block
projection whose legality is immediate from the input presentation.

### Proof

Given an arbitrary Wang/SFT instance `W`, form the product SFT

```text
X_W = Y x W
```

and let `pi` be projection to the first coordinate. The map is a total
one-block map into `Y` by construction, and

```text
X_W is nonempty  <=>  W is nonempty.
```

An algorithm for `STURMIAN-COMPILER` would therefore decide the classical
domino problem, which is undecidable (and `Pi^0_1`-complete in the convention
used by Hellouin de Menibus--Lutfalla--Vanier, Theorem 2). QED.

The reduction survives standard higher-block recoding to one-support
**colored** square, triangular, or rhombus systems. It does not prove
undecidability after the additional restriction that the entire system be
the unrestricted tiling space of one connected unmarked polygon. No audited
source supplies that final geometrization, and claiming it would assume the
very monotile compiler under investigation.

## 3. The resulting dichotomy

The symbolic landscape has a sharp boundary.

- Deterministic pose propagation is decidable but necessarily periodic, so
  it cannot solve ST-M1.
- General contextual two-dimensional contact compilation is undecidable.
- A monotile construction must therefore occupy a structured middle class:
  enough contextual nondeterminism to avoid periodic propagation, but enough
  shape-forced synchronization to give a total decoder.

For the exact 31-state source, note 59 proves that this middle class begins
strictly beyond binary handedness and affine orientation residues. The next
constructive object is the source's actual corridor-width/contact-star
quotient. This dichotomy forbids a general synthesis search from being the
research plan; only source-specific structure can make the problem tractable.

## 4. Prior-art boundary

The undecidability reduction is standard symbolic dynamics, not a novelty
claim. The primary computational boundary used here is the classical domino
problem as restated in Hellouin de Menibus--Lutfalla--Vanier (2026), Theorem
2. Their Theorem 13 proves a stronger symbolic-geometric hardness statement
over every nonempty FLC potato-shape space using labels and forbidden
patterns. Their purely geometric theorem uses a finite machine-dependent
shapeset, not one connected unmarked polygon. That distinction is exactly
the open geometrization boundary retained above.
