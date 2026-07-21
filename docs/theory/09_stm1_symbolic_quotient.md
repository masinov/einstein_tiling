# ST-M1.K1 — safe symbolic quotients before geometry

**Date:** 2026-07-21

**Status:** conditional safety criterion proof-draft; natural three-role
quotient refuted; application blocked by ERR-006

**Scope:** any future minimal colored `sqrt(2)-1` source satisfying
ST-M1.S0; no polygonal carrier or positive-entropy claim

ERR-006 withdraws the claimed 38-state common-triangle construction. This
note's quotient criterion and no-go results do not depend on that count, but
there is currently no proved S0 alphabet to merge. They specify tests for any
future valid source before boundary geometry is considered.

## 1. Local closure is the adversary

Let `Y` be a colored equal-support source satisfying S0. Let `q` be a
finite-radius recoding of `Y` to a smaller alphabet `Q`. Merely inspecting the
image `q(Y)` is insufficient. A geometric carrier will enforce some finite
local rules, so the relevant object is the local closure

```
Z(q,r) = {Q-configurations whose every radius-r patch occurs in q(Y)}.
```

Even when every configuration in `q(Y)` is aperiodic, `Z(q,r)` can contain a
periodic configuration assembled from locally legal patches. This is the
symbolic version of the no-spurious-tilings obligation.

### ST-M1.Q0 (safe-quotient criterion)

A quotient `(q,r)` is safe for minimal ST-M1 if:

1. `Z(q,r)` is nonempty; and
2. there is a total finite-radius, translation-equivariant decoder
   `d:Z(q,r)->Y_irr`, where every tiling in `Y_irr` carries an irrational
   Sturmian corridor system.

Then every configuration in `Z(q,r)` is nonperiodic.

**Proof.** If `z+v=z`, equivariance gives `d(z)+v=d(z+v)=d(z)`. The target has
no nonzero translational period, so `v=0`. Nonemptiness supplies existence.
This is period descent, but its domain is the entire finite local closure, not
only the intended image. \(\square\)

For a carrier realization, one must additionally prove that every shape-only
tiling decodes into `Z(q,r)`. Q0 separates that geometric obligation from the
symbolic quotient question.

## 2. The natural three-role quotient fails

The tempting quotient keeps only the primitive cabinet role `S`, `M`, or `L`
and the unrestricted SAB continuation rule, while forgetting:

- which source macro template owns the cell;
- the cell's address inside that macro;
- the internal/boundary ports enforcing completion of the macro;
- the two halves of the small `M` diamond as one forced component.

This is precisely the structural information that selected the quadratic
slope. Remark 7 of the source gives the controlling counterexample:
`A={S,M,L}` forms Sturmian lattices with every slope in `[0,1]`. Rational
slopes give periodic configurations.

### ST-M1.N2 (role-only no-go)

The finite presentation consisting only of the unrestricted `S/M/L` cabinet
roles and SAB continuation is not a safe quotient for ST-M1.Q0.

**Proof.** Choose any rational slope admitted by the source's
`{S,M,L}` system. Theorem 2 and Remark 7 give a periodic Sturmian lattice and
hence a periodic role/SAB configuration satisfying the unrestricted local
rules. Thus its local-rule space contains a periodic point and cannot admit a
total decoder to an irrational-only target. \(\square\)

This does not prove that every three-symbol recoding is impossible. It proves
that the obvious source-role recoding—the one suggested by “encode the three
states”—destroys the aperiodicity mechanism.

## 3. Independent corridor states also fail

Another reduction keeps finite states on each of the three corridor families
but drops the macro coupling among their intersections. It falls under
ST-M1.N1: each nonempty one-dimensional sofic rail has a periodic point, and
the product of compatible periodic rails gives a periodic plane
configuration.

Therefore a safe quotient must retain a genuinely two-dimensional coupling.
The source construction uses projective patch-tile composition to select its
irrational slope. A different coupling is allowed, but it must itself imply an
irrational-only decoder on the full local closure.

## 4. What may be merged safely

For any valid addressed S0 presentation, the following distinctions have
different logical roles:

- `S/M/L` and SAB data reconstruct the virtual corridor system;
- macro ownership and internal ports force the composition classes that give
  `(1-beta)^2/beta^2=2`;
- vertex collars prevent equidistancing from adding new flat cycles;
- handedness records the full-isometry branch;
- absolute address names may contain redundancy from template symmetries.

Only the last category is presumptively mergeable. Define two collared states
to be **future-equivalent** when every finite compatible exterior has a lift
with one state exactly when it has a lift with the other, and the two lifts
produce the same virtual corridor output. Quotienting by a proved finite-index
future equivalence preserves the decoder. Equality of radius-one stars, graph
degree, or frequency is not enough; those tests ignore larger completion
obligations.

This is analogous to minimising a right-resolving finite presentation, but the
objects are two-dimensional collared macro states. A proposed merge must
supply:

1. a finite equivalence table on the complete collared alphabet;
2. overlap well-definedness of every quotient transition;
3. total lifting or a direct irrational-corridor decoder on the quotient local
   closure;
4. a periodic-point exclusion proof independent of the intended source
   samples.

## 5. Present K1 boundary

K1 does not pass the pre-geometric gate because S0/E-infinity is blocked. The
next object is not a collar table or polygon but a proof of the equal-support
source for the actual optimized templates. Only after that proof fixes a
finite addressed alphabet may one list internal ports and SAB/vertex collars,
define symmetry merges, and prove future equivalence. A shape search or table
enumeration performed earlier would have no valid symbolic specification.

## 6. Claim boundary

Established here:

- the safe-quotient criterion Q0;
- the source-backed failure N2 of the natural role-only quotient;
- the applicability of the independent-rail no-go N1;
- the exact information classes that any later quotient must preserve.

Not established:

- a minimal alphabet or a nontrivial safe merge;
- the complete collar table or its cardinality;
- a one-shape realization;
- homochirality under the full Euclidean group;
- positive entropy of any unmarked system.
