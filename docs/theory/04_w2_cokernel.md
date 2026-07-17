# W2.C — quotient incidence cokernels

## Modular certificate

For a quotient lattice (L), let (M(L)) be the cell-by-placement incidence
matrix. Any exact cover, and even any integer relaxation, must satisfy

\[
M(L)x=\mathbf1.
\]

> **T2.C0 (modular cokernel obstruction).** If there are a prime (p) and a
> cell-weight vector (w\in\mathbb F_p^{6[\Lambda:L]}) such that
> (w^T M(L)=0) but (w^T\mathbf1\ne0), then the quotient has no integer or
> 0/1 exact-cover solution.

*Proof.* Multiplying a putative equation by (w^T) gives zero on the left and
a nonzero value on the right modulo (p). ∎

The implemented first slice uses (p=2). A certificate stores the HNF and the
support of (w). The verifier reconstructs every legal quotient placement and
checks even intersection with the support, then checks that the support itself
has odd cardinality. A missing mod-2 witness has no positive polarity: it does
not imply an integer solution or a tiling.

The zero-false-exclusion gate passes all 60,477 materialized verified periodic
certificates. For the finalist, 742 area-admissible HNFs at indices 5,10,...,60
were tested; 36 are killed, exactly three per index. Artifact:
`docs/notebook/assets/theory-w2-layer-c-gf2.json`.

## T2.C1 — an infinite thin-quotient family

Consider the finalist on HNF (L_k=(1,0,k)), with cells labelled
((v,s)\in\mathbb Z/k\mathbb Z\times\{0,\ldots,5\}). For every (k\ge4),
the only non-self-overlapping placement profiles, up to translation (t), are:

\[
\begin{aligned}
A_t={}&\{(t,s):0\le s<6\}\cup
\{(t+1,4),(t+1,5),(t-1,1),(t-1,2)\},\\
B_t={}&\{(t,s):0\le s<6\}\cup
\{(t+1,0),(t+1,5),(t-1,2),(t-1,3)\}.
\end{aligned}
\]

All first coordinates are modulo (k).

Define a mod-2 weight support (W_k) as follows. If (k) is even,

\[
W_k=\{(0,3),(2,4),(2,5),(-1,1),(-1,3)\}.
\]

If (k) is odd,

\[
W_k=\{(0,1),(2,4),(-1,2)\}
\cup\{(v,5):3\le v\le k-1\}.
\]

> **T2.C1 (thin-family obstruction).** For every (k\ge4), the finalist does
> not tile the quotient with HNF ((1,0,k)).

*Proof.* In the even case (W_k) has five cells. In the odd case it has
(3+(k-3)=k) cells, also odd. Thus its dot product with the all-ones target is
one modulo two.

For either parity, substitute the displayed weights into the two placement
profiles. Away from the marked columns, (A_t) and (B_t) meet the support in
zero or two cells. At the marked columns (0,2,-1) (and at the two endpoints
of the sector-5 interval in the odd case), the full six-sector contribution at
(t) and the four offset cells again pair exactly. Hence
(|A_t\cap W_k|\equiv|B_t\cap W_k|\equiv0\pmod2) for every (t).
T2.C0 gives the contradiction. ∎

The formulas are pinned by `finalist_thin_gf2_support`; tests reconstruct and
independently verify them for every (4\le k\le100). The proof is uniform in
(k); the finite range is regression coverage, not the theorem's bound.

The other two killed HNFs at each tested index are D6-related thin directions,
but their uniform orbit identification is not yet used in the theorem. T2.C1
already excludes one infinite area-admissible quotient family (k=5m).

## T2.C2 — exact integral membership

Let (L_M) be the integer column lattice of (M), and let
(L_+=L_M+\mathbb Z\mathbf1). Then

> **T2.C2 (integer incidence criterion).** The equation
> (Mx=\mathbf1) has an unrestricted integer solution exactly when
> (L_M=L_+). Equivalently, the canonical row Hermite forms of (M^T) and
> the matrix obtained by adjoining (\mathbf1^T) agree. In Smith language,
> this holds exactly when adjoining (\mathbf1) changes neither the rank nor
> the top determinantal divisor.

*Proof.* The equation has an integer solution precisely when
(\mathbf1\in L_M), which is precisely (L_M=L_+). Transposition presents these
column lattices as row lattices, for which Hermite normal form is canonical.
For the Smith formulation, a rank increase means
(\mathbf1\notin L_M\otimes\mathbb Q). At equal rank the index
([L_+:L_M]) is the ratio of the top determinantal divisors, so the index is one
exactly when the lattices agree. ∎

The implementation has two exact paths. FLINT 0.9.0 computes canonical row
HNF for the production census. FLINT and SymPy 1.14.0 independently compute
Smith invariant factors for pinned rank, torsion-index and compatible controls.
Both Smith implementations and HNF agree on the finalist control HNFs
`(1,0,5)` and `(5,1,1)`. The HNF route is used at scale because full Smith
diagonalization exhibited severe coefficient swell on some index-30/60
incidence matrices; this changes performance, not the membership theorem.

All 742 area-admissible finalist HNFs through index 60 have now been decided in
the unrestricted integer relaxation. Exactly 36 are `obstructed-rank`; these
are exactly the 36 quotients already killed by independently verified GF(2)
witnesses. The remaining 706 are `integer-compatible`. There are zero
same-rank `obstructed-index` cases, so odd or prime-power torsion adds no kill at
this horizon. `integer-compatible` is not a 0/1 exact cover and does not advance
O1. Artifact: `docs/notebook/assets/theory-w2-layer-c-snf.json`.

This negative result closes bare integral cokernel membership as the next
finite discriminator. Layer C should now add the inequalities discarded by
integer relaxation—nonnegative/0–1 feasibility, preferably via quotient-family
certificates—or advance to the proposed nonabelian holonomy Layer D.

## T2.C3 — translation-averaged nonnegative feasibility

> **T2.C3 (six-sector cone reduction).** On a fixed torus quotient, the full
> system (Mx=\mathbf1, x\ge0) over the rationals is feasible exactly when the
> all-ones vector in (\mathbb Q^6) belongs to the nonnegative cone generated by
> the six-sector profiles of legal placements. If feasible, at most six
> profiles are needed.

*Proof.* The quotient translation group permutes placements and is transitive
on the spatial cells within each sector. Average any feasible (x) over this
group. The result remains nonnegative and feasible and is constant on each
placement orbit. For all placements with a given sector profile (p), their
aggregate incidence is spatially constant; if there are (N_p) such placements
on an index-(k) quotient, assigning each weight (c_p k/N_p) contributes
(c_p p_s) at every cell of sector (s). Thus a full averaged cover is equivalent
to nonnegative coefficients satisfying (\sum_p c_p p=\mathbf1). The converse
is the displayed weight assignment. Conic Carathéodory in dimension six gives
a representation using at most six generators. ∎

The producer searches all linearly independent profile subsets of size at most
six with exact SymPy rationals. The verifier reconstructs all placements,
expands the compact profile coefficients to per-placement weights, and checks
coverage one at every quotient cell using `Fraction` arithmetic.

For the finalist through index 60, the result again matches the rank/GF(2)
table exactly: 36 fractionally obstructed and 706 fractionally compatible.
Every positive result has a full-incidence witness; every negative result has
an independent GF(2) obstruction. Hence ordinary LP/Farkas positivity adds no
new kill at this horizon. The remaining finite distinction is genuinely the
binary exact-cover constraint. Artifact:
`docs/notebook/assets/theory-w2-layer-c-nonnegative.json`.
