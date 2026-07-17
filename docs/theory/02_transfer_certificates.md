# T1.1–T1.2 — exact cylinder transfer certificates

## Fixed-vector theorem

Let (T) be a finite grid-aligned polykite and let (v\in\Lambda\setminus
\{0\}). Write (v=g p), with (p) primitive, and choose (u) such that
`det(p,u)=1`.

> **T1.1 (Fixed-Vector Transfer Theorem).** The complete transfer graph
> constructed by `src/einstein/theory/transfer.py` contains a directed cycle
> if and only if some grid-aligned tiling by (T) has period (v).

### State completeness

Modulo (v), one transverse column has exactly (6g) kite cells. Normalize
each legal oriented tile placement so its least (u)-coordinate is zero. Its
finite list of column masks is a **placement pattern**. Placements identifying
two of their own cells modulo (v) are discarded.

At a cut, every already occupied future cell belongs to a whole placement
whose least column lies strictly before the cut. Each such placement contributes
one of the finitely enumerated crossing masks. Exact tilings contain no overlap,
so their cut state is a nonoverlapping union of these contributions. The state
enumerator forms every such union. It may include unions whose unseen past
cannot be tiled, but it cannot omit a state induced by a tiling.

This is why enumeration is not seeded only from an empty cut. A tiling can have
whole tiles crossing every possible cut.

### Transition completeness and soundness

For a state at column (j), a transition chooses normalized placements whose
least column is (j). The choices must be disjoint from the incoming state and
from one another and must cover every unoccupied cell of column (j) exactly
once. Dropping the completed column gives the successor state.

Every tiling therefore produces a bi-infinite path in the graph. Conversely,
the placement witnesses along any bi-infinite path cover each column exactly
once. A directed cycle repeats to give such a path and hence a cylinder tiling.
The repeated placement witnesses also give a rank-2 torus cover with periods
(v) and (m u), where (m) is the cycle length; the existing A1 verifier
independently checks that exact cover.

Because the graph is finite, it has a bi-infinite path only if it contains a
directed cycle. Thus an acyclic complete graph proves that no tiling has period
(v). ∎

## Negative certificate

A `cylinder-cycle-free-certificate` contains:

1. the exact shape, vector and unimodular cylinder basis;
2. the complete normalized placement-pattern list;
3. every crossing contribution and every nonoverlapping union state;
4. every exact-cover transition, with a placement witness;
5. a permutation of all states that topologically orders every edge;
6. canonical counts and a graph hash.

`src/einstein/theory/transfer_verify.py` does not invoke the producer's graph
enumerator. It recompiles patterns from kite geometry, independently rebuilds
the contribution/state sets and transition targets, checks every supplied edge
witness, and verifies the topological order. Deleting a state or edge, changing
an ordering, or submitting a cyclic graph is rejected by tests.

## Bounded-norm corollary

Use the center-lattice norm

\[
Q(x,y)=x^2+xy+y^2,
\]

whose physical squared length is (12Q) in the repository's coordinates.
The allowed placement group contains (D_6), so applying any substrate
symmetry maps a (v)-periodic tiling to a tiling of the same free shape with
period in the exact (D_6)-orbit of (v).

> **T1.2-25 (Finalist bounded-norm exclusion).** The n=10 finalist admits no
> grid-aligned tiling with a nonzero translation period (v) satisfying
> (Q(v)\le 25).

The finite norm ball consists of 90 nonzero vectors in 11 (D_6)-orbits,
including all nonprimitive vectors. The artifact
`docs/notebook/assets/theory-w1-finalist-norm25.json` contains one complete,
independently verified cycle-free certificate for every orbit representative.
There were no resource exhaustions.

This theorem does not prove aperiodicity: vectors with (Q(v)>25) remain. It
also has grid-aligned scope; W4 is required for arbitrary Euclidean placements.

### Certified extension through Q=36

Four additional orbit representatives `(3,3)`, `(4,2)`, `(5,1)` and `(6,0)`
cover the 36 vectors in the shell (25<Q(v)\le36). Their independently
verified acyclic graphs have respectively 74,489; 91,570; 120,621; and 159,860
states. Combined with T1.2-25 this establishes:

> **T1.2-36.** The n=10 finalist admits no grid-aligned tiling with a nonzero
> translation period (v) satisfying (Q(v)\le36).

The combined norm ball contains 126 vectors in 15 exact (D_6)-orbits. The
incremental proof archive is
`docs/notebook/assets/theory-w1-finalist-norm26-36.json`.

## Review status

- The finite T1.2-25 computation is machine-verified.
- The T1.1 mathematical argument is a complete internal proof draft pending
  adversarial review and preferred literature citations.
- Positive cycles retain a second verification path through A1.
- Negative certificates are deliberately larger than hashes: completeness and
  acyclicity are both independently recomputable from their contents.
