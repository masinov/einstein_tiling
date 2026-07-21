# K4W — a retiling compiler for a minimal aperiodic Wang source

**Date:** 2026-07-21

**Status:** sufficient theorem and search contract in proof draft; no polygon,
retiling family, contact atlas or novelty claim

## 1. Why the binary projection was the wrong complete state

Suppose a guarded polygon tiling uniquely groups into square macrocells and
each square has one of the two K3B diagonals. Let `Y` be the finite local
language of all locally visible macro contact states and let

```
b : Y -> {slash, backslash}
```

forget everything except the diagonal. If `Y` is an SFT, `b(Y)` is a sofic
shift. It need not be the SFT obtained by allowing all `2x2` bit blocks seen
in `b(Y)`. Hidden docking phases can enforce consistency over arbitrarily
long visible-bit distances.

Hu--Lin N11 kills the special case where the bit is the complete state and
leg/corner legality is exactly a set of allowed `2x2` bit blocks. It does not
kill a finite hidden cover `Y`. The hidden state must be independently
recoverable from bounded unmarked geometry; adding it after decoding the bits
would merely rename a color and prove nothing.

## 2. A lower bound for an edge-Wang realization

Jeandel--Rao prove that an aperiodic ordinary Wang set has at least 11 tile
states and at least four edge colors.

### ST-M1.N13

Assume the complete square-macro language is an ordinary edge-matching Wang
shift and each macrostate is determined by one of the two diagonal retilings
and at most `h` independently visible docking modes for that diagonal. If the
macro language is aperiodic, then

```
2h >= 11, hence h >= 6,
```

and its interfaces use at least four distinguishable colors.

This is immediate because the resulting Wang alphabet has at most `2h`
states, while Jeandel--Rao's lower bounds apply to every aperiodic Wang set.
The result is deliberately scoped: vertex constraints, larger-range rules or
a non-Wang finite cover need not obey the `h>=6` statement.

The bound is a search filter. A boundary family offering only two diagonal
states and fewer than six rooted modes per diagonal cannot realize an
aperiodic edge-Wang compiler, no matter how persuasive a finite patch looks.

## 3. Direct sufficient contract

The Sturmian source is not essential to the geometric idea. Let `T` be any
published aperiodic Wang set; the 11-state Jeandel--Rao set is minimal and
gives the tightest exact target. Let `P` be one connected unmarked polygon,
admitted under the full Euclidean isometry group.

### K4W contract

1. **Unique grouping.** Every `P`-tiling has a unique finite-radius partition
   into congruent rooted square macrocells `M`.
2. **Visible states.** Each `M` has one state in the fixed Wang alphabet `T`,
   recovered from its exact internal retiling and/or independently visible
   docking geometry. No external mark or chosen origin enters the decoder.
3. **Exact interfaces.** Two macrocell sides meet in a `P`-tiling if and only
   if the corresponding Wang edge colors match. All partial contacts,
   T-junctions, slides and alternative subdivisions belong to a finite
   complete atlas and decode within this rule.
4. **Full-isometry safety.** Reflected and rotated occurrences either enter
   the same decoder coherently or are excluded geometrically; mixed-handed
   fault components do not exist.
5. **Lift.** At least one valid whole-plane `T`-tiling lifts to a `P`-tiling.

### ST-M1.K4W

Any polygon satisfying K4W is an aperiodic monotile.

### Proof

The lift proves whole-plane tileability. Suppose a `P`-tiling had a nonzero
translation period. Unique finite-radius grouping makes that translation
preserve and permute its macrocell partition. The local visible-state map is
translation equivariant, so it sends the period to the decoded valid
`T`-tiling. This contradicts the aperiodicity of `T`. Full-isometry safety
ensures the argument covers every tiling allowed in the ordinary monotile
definition. \(\square\)

The theorem is a standard factor/period-descent composition specialized to a
single-support retiling compiler. No novelty is claimed for the theorem
schema. Novelty would reside in an exact polygon and complete atlas meeting
K4W.

## 4. Two admissible realization strategies

### A. Internal multi-retiling

Use one macrocell with at least 11 rooted exact retilings by congruent copies
of `P`, assign them bijectively to the Jeandel--Rao tiles, and make their macro
boundary subdivisions display the four Wang colors. Because each macrocell
uses the same number of congruent copies, this introduces no fixed-fusion
frequency obstruction. The binary diagonal square is the two-state control
for this stronger inverse-dissection problem.

### B. Contextual hidden docking

Keep the two diagonal retilings but require at least 11 locally distinguishable
combined `(diagonal,docking)` macrostates and four interface modes. The state
must be visible before the Wang rule is invoked. This is more economical in
internal dissections but harder to protect against circular state assignment.

Kari--Moutot's long binary strip is a third symbolic existence route, but its
large rectangular support is not naturally read by one K3B edge or corner.
It is a correctness control, not the preferred geometric compiler.

## 5. Search architecture, not a run authorization

A later inverse-geometry search should take the 11 Wang states and four colors
as fixed input and search only parameterized macrocell dissections or docking
atlases. Every proposed parameterization must predeclare:

- the macrocell `M`, component count and maximum segment count;
- how the 11 states and four colors are read from exact incidences;
- a finite lemma making the contact atlas complete under full isometries;
- the exact lift certificate; and
- a fixed failure outcome that closes that parameterization.

No polygon enumeration follows from this note. In particular, searching
ordinary polykites of size at most 24 would remain inside the classified
horizon, and increasing a contact radius after failure would violate the
experiment gate.

## 6. HC-12 disposition

The bit-only K3B route is closed by N11. Binary symbolic aperiodicity survives
at larger range by N12, but the direct geometric route should use the tighter
K4W compiler target rather than reproduce a huge generic encoding. HC-12
ends with a theorem and explicit state/interface lower bounds, not a shape.

The next checkpoint, if authorized, should be on-paper inverse-dissection
design for K4W strategy A. Its kill condition should require one exact
macrocell topology supporting at least 11 rooted retilings and a plausible
unique-grouping invariant within three sessions; otherwise K4W returns to the
frozen specification without a search run.
