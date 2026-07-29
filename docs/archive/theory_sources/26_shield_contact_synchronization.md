# Shield contact synchronization after N26

**Status:** proof draft; no polygon, candidate, or contact-completeness theorem
for K10B

**Scope:** unrestricted locally finite gapless tilings by one irredundant
polygonal disk, allowing the full Euclidean isometry group

## 1. HC-20 question

N26 shows that a two-copy full-spine docking necessarily creates a second
boundary side of each code length.  At nonterminal spine vertices, intended
convex angles are paired with reflex angles.  ERR-009 corrects the terminal
`A` endpoint: the two carrier sectors there fill the lens corner rather than
a full disk.  HC-20 separates two claims which must not be conflated:

1. the auxiliary same-length sides are **unavoidable** in this docking; and
2. those sides admit **uncontrollable alternative contacts** in every tiling.

Only the first statement follows from N26.  This note asks for a finite local
criterion sufficient for controlling the second.  It then tests K10B against
that criterion before any coordinate work can resume.

The HC-19 correction remains a precondition: the two copies belong to one
length class but are not the same directed role.  It is now scoped separately
to internal and terminal spine vertices by ERR-009.

## 2. Boundary germs and angle polarity

For an oriented boundary side `e` of a polygon `P`, its rooted boundary germ
records

```text
(length(e), left endpoint angle, right endpoint angle,
 predecessor length, successor length).                         (2.1)
```

The predecessor and successor entries are intrinsic boundary data, not
colors.  A germ is **convex** when both endpoint angles lie in `(0,pi)` and
**reflex** when both lie in `(pi,2*pi)`.

Consider two congruent occurrences which share a polygonal arc and whose
interiors lie on opposite sides of that arc.  At an internal vertex of the
shared arc, if those two occurrences alone fill a neighborhood, their
interior angles sum to `2*pi`.  Thus the contact pairs an angle `alpha` with
the complementary angle `2*pi-alpha`.

## 3. N27: the primary host reads angle polarity

### ST-M1.N27

Let an intended code side have a convex endpoint assigned to an internal
host subdivision, and let its full-arc docking partner have the N26
complementary reflex angle at the corresponding endpoint. At that subdivision
the reflex partner cannot replace the intended directed endpoint in any
interior-disjoint gapless patch. Consequently endpoint polarity locally
rejects every such auxiliary endpoint. For K10B this covers both ends of
`B,C` and the internal-spine end of `A`, not `A`'s terminal lens endpoint.

### Proof

The host occupies a straight sector of angle `pi` at an internal subdivision
point.  A reflex auxiliary occurrence contributes an angle strictly greater
than `pi` at the same point.  Their sector sum is therefore strictly greater
than `2*pi`, so their interiors overlap.  An intended convex endpoint is not
excluded by this argument and is the endpoint used in the K9A sector
equation.  This applies independently at every complementary reflex endpoint
and makes no claim at a terminal endpoint outside N26.  □

## 4. What N27 does not prove

N27 is a local polarity filter, not an all-tilings contact theorem.  An
auxiliary reflex side might still:

- meet a different concave or subdivided boundary away from a host;
- begin a partial common arc which branches at its next vertex;
- participate in a junction with a third or fourth occurrence; or
- initiate a complete alternative docking not present in the intended patch.

Therefore auxiliary duplication is not yet classified as controllable or
uncontrollable.  Session 116 must derive a finite, boundary-intrinsic
synchronization criterion.  It may not assume that a shared side forces the
rest of the shield arc merely because one intended placement does so.

## 5. HC-20 admission and stop

The remaining checkpoint has one fixed decision tree:

1. prove a finite sufficient condition under which one matched auxiliary
   germ propagates to one complete rooted docking arc;
2. test the fixed K10B word against that condition; and
3. resume coordinates only if the existing K10W reopening rule is already
   met: a complete exact coordinate list and both exact placement tables
   before computation.

If K10B fails the condition and no stronger theorem controls the failed
contact, K10W remains frozen.  HC-20 does not admit another spine, an atlas
enumeration, numerical fitting, or an SVG.

## 6. Root-side cover words

Let `r` be a distinguished side of `P`.  A **root cover word** is the ordered
list of intrinsic boundary-side germs of neighboring occurrences whose full
sides partition `relint(r)` in a locally legal patch.  Endpoint order is read
from one fixed orientation of `r`.

The following hypotheses make this a finite object.

- **V (cover-side vertex alignment):** every maximal common boundary segment
  on `r` is one full intrinsic side of the neighboring occurrence, with both
  of that side's vertices on `r`; no neighbor side overhangs an endpoint of
  `r`.  An internal endpoint may lie in `relint(r)`, so ordinary T-junction
  subdivisions remain in the table.
- **F (finite cover table):** `P` has finitely many positive side lengths and
  the tiling is locally finite.  If `lambda` is the shortest side, a cover of
  `r` has at most `floor(|r|/lambda)` entries.  Hence all length-compatible
  words and their endpoint angle contexts form a finite table.

Condition V is substantive.  Without it a longer side can slide continuously
past an endpoint or only a proper subsegment of a neighbor side can cover a
piece of `r`, and a finite word table is not complete.  A proposed polygon
must prove V from its angles/guards or include those sliding edge patches in
its contact analysis.

Call `r` **atomic with mate `r*`** when its complete finite cover table has
one entry only:

```text
[r*],                                                       (6.1)
```

up to intrinsic symmetries of `P` which produce the same placed disk.  This
means that every use of `r` in every admitted tiling is covered by one full
side `r*` of one neighboring occurrence, with the endpoint correspondence
fixed.

## 7. K11S: one atomic root synchronizes a complete arc

### ST-M1.K11S

Let `S` be a selected boundary arc of `P` containing a side `r`.  Suppose:

1. vertex alignment V holds on `r`;
2. `r` is atomic with mate `r*`;
3. mapping `r*` onto `r` with interiors on opposite sides determines one
   occurrence `Q` (modulo intrinsic symmetries producing the same disk); and
4. in that forced pose, `P intersect Q=S`, their interiors are disjoint, and
   their union contains a neighborhood of every internal vertex of `S`.

Then in every locally finite gapless tiling containing an occurrence of `P`,
its side `r` belongs to exactly one `P--Q` pair sharing the complete arc `S`.
Every auxiliary side on that copy of `S` is thereby controlled by the same
bounded root decision.  The pair is locally recognizable in the bounded
neighborhood of the root cover.

### Proof

Gapless coverage supplies a cover word on `r`.  Hypotheses 1--2 make it the
single full side `r*` of one neighbor `Q`.  A Euclidean isometry of a polygon
is fixed by the images of the two distinct endpoints of `r*` together with
the choice of the opposite half-plane for its interior; hypothesis 3 removes
any residual intrinsic duplicate.  Hence `Q` has the selected pose.

Hypothesis 4 now gives equality along all of `S`, not just `r`, and excludes
another occurrence from either side of an internal point of that common arc.
Thus all paired auxiliary germs belong to this one forced neighbor.  If two
different neighbors claimed the root, their interiors would occupy the same
open half-neighborhood of `r`, contradicting interior disjointness.  The
root cover is bounded data, so the pairing is locally recognizable.  □

## 8. Interpretation

K11S answers the general HC-20 dichotomy at the appropriate strength:

```text
auxiliary duplication is not intrinsically uncontrollable;
one finite atomic root can synchronize the entire duplicated arc.       (8.1)
```

This is a sufficient theorem, not a claim that every duplicated arc has such
a root.  It does not construct an atomic side, prove vertex alignment for an
unspecified polygon, or serialize a full contact atlas.  Its certificate is
strictly smaller: one side's bounded cover table, one rooted side identity,
and the exact two-copy intersection statement.

For K10B the first proposed root is its unique side `H`.  Session 117 must
test the complete cover words of `H`; uniqueness of its length among single
sides is not by itself enough when T-junction subdivisions are admitted.

## 9. N28: the K10B host side is deliberately non-atomic

### ST-M1.N28

Every realization of the complete K10B compiler language gives the unique
intrinsic `H` side at least the following three distinct root cover words:

```text
[H],             [A,B,C],             [A,C,B].                (9.1)
```

Therefore `H` is not an atomic K11S root, even though it is the only
intrinsic side of length `7`.

### Proof

The K10B half-turn shield uses the central side of `S` as a full `H--H`
contact, which supplies `[H]`.  The two selected K9A host states are exactly
the subdivisions of an `H` side by the non-reversal words `ABC` and `ACB`.
Their lengths satisfy the required identity

```text
|H| = |A|+|B|+|C| = 7 = 1+2+4.                  (9.2)
```

These are different cover words in the same all-tilings language.  Hence the
complete cover table cannot be the singleton (6.1).  □

N28 is not a contradiction in the proposed compiler: the multiplexing is
intentional.  It proves only that the unique-length argument cannot make `H`
select the shield rather than a host subdivision.

## 10. Audit of the other K10B roots

ERR-009 blocks the tempting shortest-side shortcut.  A terminal `A` side has
one internal reflex endpoint but its paired terminal angles sum to `pi/2`, so
it lacks the two-reflex endpoint barrier that would immediately prove vertex
alignment.  The internal `B,C` auxiliary sides do have two reflex endpoints,
but their length equations permit nontrivial numerical subdivisions
(`2=1+1` and `4=2+2=2+1+1`).  Numerical compatibility does not prove those
patches legal, but it means atomicity cannot be inferred from length alone.
The repeated `d` sides have neither a unique intrinsic role nor a complete
cover table.

Thus no side of the fixed K10B word currently satisfies all four K11S
hypotheses.  This is a missing finite certificate, not a no-go theorem for a
larger-radius contextual synchronizer or for another nonconvex carrier.

## 11. HC-20 disposition

HC-20 resolves its general question and applies the answer:

- N27 gives the exact endpoint-polarity filter where N26 applies;
- K11S proves a finite atomic root is sufficient to control an entire
  duplicated shield arc;
- ERR-009 corrects the terminal scope before a false `A`-root proof is used;
  and
- N28 proves K10B's unique `H` is non-atomic by design.

K10W remains frozen.  No alternative root has a complete vertex-alignment
and cover-table proof, and the pre-existing reopening condition—complete
exact coordinates plus both complete placement tables before computation—was
not met.  The checkpoint therefore ends without a polygon, SVG, experiment,
or candidate.

Reopening the same word requires either:

1. a complete finite cover table proving another named side atomic and exact
   K10B coordinates with both patches; or
2. a strictly stronger finite contextual synchronization theorem which
   accepts the multiplexed `H` words and still selects the shield pose on the
   full local closure.

Merely choosing another value of `d`, drawing the half-turn lens, or checking
one intended patch does not meet either condition.
