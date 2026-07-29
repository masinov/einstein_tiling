# Walton: recognisability for generalised FLC pattern spaces

**Catalog ID:** `walton-recognisability-2026`  
**Audited version:** arXiv:2509.21001v2, revised 2026-05-28  
**Audit date:** 2026-07-20  
**Status:** theorem and hypothesis audit completed; examples and every
auxiliary proof were not independently rederived.

## Exact framework

Walton works with translation-invariant pattern spaces in the local topology.
The definitions controlling W3 are:

- **Definition 3.12:** finite local complexity (FLC) for a pattern space;
  Corollary 3.16 identifies FLC with compactness.
- **Definitions 3.25 and 3.27:** return discreteness and well-separation;
  Proposition 3.32 identifies compact Hausdorff spaces with FLC,
  well-separated spaces.
- **Definition 4.1:** an `L`-substitutional pattern space has a *surjective
  local-derivation* subdivision map `S:LΩ→Ω`; substitution is
  `sigma=S∘L`.
- **Definition 4.5 and Proposition 4.6:** if subdivision is not surjective,
  the theorem applies only after restriction to the hierarchical/eventual
  range. It does not automatically cover the full geometrically admitted
  hull.
- **Definition 5.1:** unique composition modulo translation means any two
  preimages of the same pattern differ by a translation.

The linear map `L` must be expansive: every eigenvalue has modulus greater
than one. A combinatorial incidence matrix with exponential growth is not, by
itself, this Euclidean hypothesis.

## Main theorem and consequences

**Theorem 5.2.** Every compact Hausdorff expansive `L`-sub pattern space has
unique composition modulo translation.

This is stronger in generality than the primitive stone-substitution theorem:
minimality, repetitivity and primitivity are not assumed. It is also weaker
than strict uniqueness when the image pattern has translational periods.

**Proposition 5.3** gives the exact fibre size

```text
# sigma^-1(P) = [K_P : L K_P'] < infinity,
```

where `P'` is a preimage and `K_P` is the translational period group.
Consequently, a nonperiodic pattern has one preimage.

**Corollary 5.5.** Substitution is injective iff every pattern is discretely
nonperiodic. For return-discrete tiling spaces this is equivalent to the hull
containing no periodic tiling. When injective, inverse subdivision is itself a
local derivation, so a finite recognition radius exists.

**Corollary 5.6** gives the individual-pattern form: for an FLC,
return-discrete, expansive `L`-sub pattern, inverse local derivability is
equivalent to *aperiodicity of the whole hull*, not merely nonperiodicity of
one generated tiling.

## The circularity boundary for W3

Walton cannot be used as follows:

```text
claim no periodic tilings -> invoke injectivity -> claim aperiodicity proved.
```

For the return-discrete tile spaces relevant here, absence of periodic hull
elements is precisely the hypothesis equivalent to injectivity. The theorem
is therefore an excellent recognisability and consistency control after an
independent aperiodicity proof, but not a standalone route to that proof.

There is one useful non-circular conclusion available earlier: if W3 encodes
a compact Hausdorff expansive `L`-sub space, Theorem 5.2 gives composition
uniqueness *modulo translation*. A separate argument must still eliminate the
translation ambiguity.

## Mapping to W3

| Walton hypothesis/result | W3 clauses | Current Spectre state |
|---|---|---|
| formal compact/FLC pattern space | C1, C5 | missing: generated states are not the full legal hull |
| Hausdorff/well-separated or return-discrete | C1, C5 | missing as encoded evidence |
| expansive Euclidean `L` | C3 | partial: exact recurrent module expansion is not yet one map on the hull |
| surjective LD subdivision `S:LΩ→Ω` | C2, C4, C5 | missing on all admitted tilings |
| no discrete periods, for strict injectivity | C4 and target theorem | missing and cannot be assumed circularly |
| inverse subdivision is LD | C4 | conclusion only after the preceding rows |

The machine-readable version of this table is emitted by
`recognisability_crosswalk()` in
`src/einstein/tilings/substitution.py`.

## Repository impact

The former C4 phrase “exhaustive legal collar language” was directionally
correct but underspecified. W3 now distinguishes:

1. a **Walton route**, which requires an actual compact Hausdorff expansive
   `L`-sub hull and an independent period exclusion for strict uniqueness;
2. a **direct local-composition route**, which proves total and unique parent
   grouping on every admitted tiling and then derives period exclusion.

Only the second route can presently serve as W3's independent aperiodicity
proof architecture. Chéritat is its concrete Spectre control.
