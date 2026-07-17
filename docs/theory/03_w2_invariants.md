# W2 exact invariants — Layer A result and Layer B correction

## T2.A — area and sector-count obstructions

For an index-(k) quotient of the center lattice, the torus contains exactly
(6k) kite cells. A tile of (n) kites can cover it only if

\[
n\mid 6k,
\]

or equivalently (k\equiv0\pmod{n/\gcd(n,6)}). The certificate records the
nonzero remainder and is independently recomputable.

A refinement assigns weights (w_0,\ldots,w_5\in\mathbb F_p) to the six kite
sectors. Let (c_o\in\mathbb Z^6) be the sector-count profile of orientation
(o\in D_6). If

\[
c_o\cdot w=0\quad\text{for every allowed orientation},
\]

then any quotient tiling requires

\[
k(1,1,1,1,1,1)\cdot w=0\pmod p.
\]

A nonzero target residue is therefore an exact coloring obstruction. The code
computes the right nullspace of the orientation-profile matrix over prime
fields and emits the weights, profiles and target residue.

The zero-false-exclusion gate passes all 60,477 materialized A1 periodic
certificates for n=9..16. For the n=10 finalist, a modulus-5 sector witness
excludes exactly the indices not divisible by 5. It adds no exclusions beyond
area. This negative finding is preserved in
`docs/notebook/assets/theory-w2-layer-a.json`.

## T2.B0 — no-go for isolated nontrivial character blocks

The roadmap proposed testing each character of the finite quotient
(A=\Lambda/L) separately. Write (x_o(a)) for the indicator/relaxation of a
tile of orientation (o) anchored at (a\in A). Exact coverage has six sector
equations. Fourier transform at a character \(\chi\in\widehat A\) gives

\[
\sum_o P_{s,o}(\chi)\,\widehat{x_o}(\chi)
= \widehat{1}(\chi),\qquad s=0,\ldots,5.
\]

> **T2.B0 (Single-character linear no-go).** For every nontrivial character
> \(\chi\ne1\), the isolated Fourier-projected linear system cannot be
> infeasible: its right-hand side is zero and the zero vector
> \(\widehat{x_o}(\chi)=0\) is always a solution.

*Proof.* The Fourier transform of the constant function on a finite group is
zero at every nontrivial character. The projected equations are homogeneous,
so the zero amplitude vector solves all six equations. ∎

The trivial character is not new Layer B information: it is precisely the
orientation-count/area relaxation in Layer A.

Consequently the roadmap's claim that infeasibility of one nontrivial
six-dimensional character block could kill a quotient was incorrect. Character
factorization remains useful for computation and for understanding the
incidence module, but not as an isolated rational infeasibility test.

## Redirect to Layer C

The full integer equation

\[
M(L)^T x=\mathbf1
\]

can still fail even when every rational character block is compatible. Smith
normal form detects integral cokernel torsion that isolated complex Fourier
blocks discard. Layer C therefore becomes the next algebraic experiment:

1. build the complete placement-by-cell incidence matrix for small quotients;
2. determine whether \(\mathbf1\) lies in its integer column lattice;
3. emit a compact modular/cokernel witness when it does not;
4. validate zero false exclusions against verified A1 periodic certificates;
5. measure whether it kills any finalist quotient already admissible by area.

If Layer C also adds no kills, W2 should proceed to nonabelian torus holonomy
rather than multiplying equivalent coloring tests.
