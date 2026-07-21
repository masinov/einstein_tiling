# ST-M1.K1 — safe symbolic quotients before geometry

**Date:** 2026-07-21

**Status:** safety criterion proof-draft; natural three-role quotient refuted

**Scope:** minimal colored `sqrt(2)-1` source from ST-M1.S0; no polygonal
carrier or positive-entropy claim

The common-triangle construction has 38 raw macro-address states before
handedness, SAB, orientation, and vertex-collar refinement. Thirty-eight is a
safe presentation size, not a lower bound: a contextual decoder might merge
many states. This note states what such a merge must prove and tests the two
obvious reductions before any boundary geometry is considered.

## 1. Local closure is the adversary

Let `Y` be the proof-draft colored common-triangle source. Let `q` be a
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

- which of the two `2S+L` macro templates owns the cell;
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
The source coupling is the `2S+L` versus `M` macro composition. A different
coupling is allowed, but it must itself imply an irrational-only decoder on
the full local closure.

## 4. What may be merged safely

The 38 raw addresses split as `18+18+2`. The following distinctions have
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

The smallest **currently proved safe** symbolic presentation is the full
addressed, collared S0 alphabet. Its raw uncollared core has 38 states; the
actual collared cardinality has not been enumerated in the source or this
repository. No smaller quotient is currently proved safe.

Accordingly, K1 does not yet pass the pre-geometric gate. The next bounded
object is not a polygon but an explicit finite source table:

- list the 38 raw addresses and their internal directed ports;
- list the finite SAB/vertex collars needed by E-infinity;
- define candidate symmetry merges;
- prove future equivalence or retain the states separately.

Only after that table has a total decoder on its local closure can a contact-
star carrier be asked to realize it. A shape search performed earlier would
have no fixed symbolic specification and could only rediscover finite local
patches.

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
