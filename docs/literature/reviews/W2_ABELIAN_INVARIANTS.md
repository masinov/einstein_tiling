# W2 abelian-invariant prior-art audit

**Audit date:** 2026-07-21
**Question:** do T2.C1/T2.C5 constitute a new theorem or method worth
developing, or a worked control inside established coloring theory?

## Result

W2's abelian layer is closed as a novelty branch. The general certificate
form is classical, and the Turtle conclusion is already a strict corollary of
published aperiodicity. The explicit support `W_k` was not located in the
audited Turtle sources or the dated targeted searches below, so it may be
retained as an independently derived worked example. It is not presented as
a new aperiodicity theorem, a new invariant framework, or a reason for more
quotient computation.

## Exact relationship to classical tile homology

For a finite quotient, let `M` be the cell-by-placement incidence matrix. A
W2 witness is a vector

```text
w^T M = 0,     w^T 1 != 0        over F_p.
```

This assigns an additive weight to every quotient cell, makes every legal
tile placement have weight zero, and gives the target region nonzero weight.
It is exactly a generalized coloring obstruction, expressed as finite linear
algebra.

Conway--Lagarias (`conway-lagarias-tiling-groups-1990`) make this relationship
structural. Section 5 defines generalized coloring maps into abelian groups,
identifies their maximal information with the tile homology group, and proves
in Theorem 5.2 that the resulting boundary condition is equivalent to the
existence of a signed tiling for simply connected planar regions. Their
nonabelian boundary invariant can be strictly stronger. Consequently:

- T2.C0 is a standard finite-field coloring/signed-tiling obstruction;
- T2.C2 is the corresponding ordinary integer-module membership question;
- Smith/Hermite normal form is an implementation technique, not a new tiling
  invariant;
- T2.C3 is a standard symmetry average plus conic Caratheodory reduction.

The surface setting is not a missing novelty. Lidjan--Baralic
(`lidjan-baralic-flat-surface-homology-2021`) define tile homology directly on
finite square grids on surfaces. Section 3 treats torus grids, and Theorems
3.1--3.3 give explicit non-tilability results whose proofs reduce to cell
relations and parity colorings on the quotient. Their substrate and tiles
differ from ours, but the logical certificate class—an abelian relation among
all quotient placements detecting the all-cells target—is the same.

## Comparison with published Turtle proofs

The following primary Turtle sources were searched in full text for parity,
modular coloring, homology, quotient-torus, and incidence obstructions:

- `smkgs-hat-2024`, especially Section 3, Section 6 and Appendix A;
- `akiyama-araki-turtle-2025`, especially the Golden Ammann bar proof;
- `james-smith-rhombic-2024`, especially Proposition 7 and the projection
  proof.

They prove much stronger statements by different mechanisms. The Hat paper
proves aperiodicity throughout the positive unequal `Tile(a,b)` family. The
Akiyama--Araki paper uses Golden Hex/Sturmian and Ammann-bar structure. James
Smith assumes a periodic Turtle tiling, passes to a finite rhombille
fundamental domain, and derives an irrational frequency equation from exact
counts. None of the audited texts states the displayed `W_k` formula or the
three thin HNF families.

That absence does not make T2.C1/T2.C5 a substantial new theorem. Published
aperiodicity already excludes *every* periodic quotient, while T2.C1/T2.C5
exclude only three D6-related, rank-one-thin quotient shapes. Their honest
value is pedagogical and computational: a compact positive control showing
that the verifier can turn an experimentally found null vector into a uniform
formula.

## Dated searches

On 2026-07-21, searches for combinations of `Turtle`, `Tile(sqrt(3),1)`,
`parity`, `coloring invariant`, `torus`, and `quotient` returned the published
Turtle hierarchy, Ammann-bar, rhombille-coloring and Sturmian proofs, but no
matching thin-support formula. Searches for finite-abelian/group-ring,
homology and torus coloring obstructions returned the classical algebraic
literature above and related polynomial/Groebner approaches. This is an
absence report, not a proof that the formula has never appeared.

## Claim permissions

Permitted:

- “an independently derived compact GF(2) coloring certificate for three
  infinite thin quotient families of the Turtle”;
- “a worked benchmark for certificate discovery and cold verification”;
- “the exact formula was not found in the audited sources as of 2026-07-21.”

Not permitted:

- “a new algebraic method for tilings”;
- “a new proof that the Turtle is aperiodic”;
- “a new substantive Turtle theorem” without external expert review and a
  materially broader theorem;
- any further radius, quotient-index, prime, or finite-group escalation under
  the W2 novelty claim.

## Disposition

Keep T2.C1/T2.C5 and the tiny regression verifier as a control example. Mark
T2.C0--T2.C5 as known-method or control results in the proof ledger. Archive
the large W2 finite-shell artifacts; do not extend them. The next research
decision moves to the classified-corpus funnel benchmark, whose proposition
must be defined before any ablation run is admitted.
