# T0.1 — Periodic completion for grid-aligned finite tiles

## Statement

Let `K` be the kite complex with translation lattice
\(\Lambda\cong\mathbb Z^2\), and let \(T\) be a fixed finite polykite. Let
\(\Omega_T\) be the space of grid-aligned exact tilings of `K` by translated,
rotated, and optionally reflected copies of \(T\).

> **T0.1 (Periodic Completion Theorem).** If some
> \(\omega\in\Omega_T\) has a nonzero translation period
> \(v\in\Lambda\), then there is an \(\omega'\in\Omega_T\) whose translation
> stabilizer has rank two. Moreover, \(v\) is a period of \(\omega'\).

The vector \(v\) need not be primitive in the ambient lattice.

## Finite-type encoding

Choose one translation anchor at every lattice site and one of the finitely
many point-group images of \(T\). At site \(p\in\Lambda\), record the subset
of orientation types whose tile copies are anchored at \(p\). This gives a
finite alphabet: only finitely many orientations exist, and exact coverage
forbids duplicate copies.

Whether every kite cell is covered exactly once depends only on anchor
symbols within the diameter of \(T\). Thus the legal encodings form a
two-dimensional subshift of finite type \(X_T\). Reading anchors reconstructs
the tiling, and reading a tiling reconstructs its anchors, so translational
periods are preserved by the encoding.

This encoding is used only for the theorem. Implementations may use smaller
frontier-germ states, but they must prove equivalence to this finite-range
model.

## Proof

Assume \(x\in X_T\) is invariant under a nonzero vector \(v\). Write
\(v=g p\), where \(p\) is primitive in \(\Lambda\) and \(g\geq 1\). Choose
\(u\in\Lambda\) such that \((p,u)\) is a lattice basis. Then

\[
\Lambda/\langle v\rangle \cong \mathbb Z\,u\oplus\mathbb Z/g\mathbb Z\,p.
\]

A \(v\)-periodic configuration is therefore a bi-infinite sequence of
finite columns: each column contains the \(g\) torsion positions in the
\(p\)-direction and their finite anchor alphabet. Because the original
constraints have finite range, the legal column sequences form a
one-dimensional subshift of finite type \(Y_v\). The assumed configuration
shows that \(Y_v\neq\varnothing\).

Present \(Y_v\) as a finite directed higher-block graph. A bi-infinite path
in a finite directed graph repeats a vertex in the forward direction. The
path segment between two repetitions is a directed cycle. Repeating that
cycle in both directions gives a periodic point \(y'\in Y_v\).

Lift \(y'\) to \(X_T\). It is invariant under \(v\) and under a second
translation of the form \(m u+j p\), where \(m>0\) is the cycle length and
the possible torsion shift \(j p\) records the column convention. This second
vector is linearly independent of \(v\). The lifted tiling is therefore fully
periodic. ∎

## Corollaries

> **C0.1.** For fixed finite grid-aligned polykites, weak translational
> aperiodicity (existence and no rank-2 periodic tiling) is equivalent to
> strong translational aperiodicity (existence and no nonzero period in any
> tiling).

> **C0.2.** A proof that no fully periodic grid-aligned tiling exists closes
> the entire periodicity obligation. A separate universal exclusion of
> singly periodic tilings is unnecessary.

> **C0.3.** A vector-specific search must include nonprimitive vectors. A
> configuration can have period \(2p\) without having period \(p\).

## Constructive content

The proof is effective. A directed cycle in the exact transfer graph for
\(K/\langle v\rangle\) reconstructs a rank-2 torus certificate accepted by
the A1 verifier. Conversely, a complete cycle-free transfer graph is a finite
certificate that no tiling has period \(v\).

The theorem does not prove that the transfer graph is computationally small.
That engineering and certificate contract is specified in
`W1_TRANSFER_SPEC.md`.

## Scope and review obligations

- The theorem itself concerns grid-aligned tilings. For finite polykite sets,
  the upgrade needed for periodicity is already external: Appendix A,
  Lemmas A.1, A.3 and A.5 of Smith--Myers--Kaplan--Goodman-Strauss,
  *An aperiodic monotile*, show that any weakly or strongly periodic
  geometric polykite tiling has an aligned counterpart with the same listed
  property. Combining that reduction with T0.1 means exclusion of all aligned
  rank-two tori excludes every nonzero translational period under arbitrary
  Euclidean placements. W4 concerns only stronger all-tilings rigidity or
  extensions outside the polykite hypotheses.
- The proof relies only on finite local complexity and finite-range exact
  coverage, not on the candidate's diffraction or hierarchy.
- Before theorem-ready status, verify the terminology and preferred citation
  against the standard periodic-point result for one-dimensional SFTs.
- The implementation must handle \(\Lambda/\langle v\rangle\)'s torsion when
  \(v\) is nonprimitive.
