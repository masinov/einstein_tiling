# Shield contact synchronization after N26

**Status:** proof draft; no polygon, candidate, or contact-completeness theorem
for K10B

**Scope:** unrestricted locally finite gapless tilings by one irredundant
polygonal disk, allowing the full Euclidean isometry group

## 1. HC-20 question

N26 shows that a two-copy full-spine docking necessarily creates a second
boundary side of each code length.  The intended side has convex endpoint
angles; its partner on the other half of the carrier has reflex endpoint
angles.  HC-20 separates two claims which must not be conflated:

1. the auxiliary same-length sides are **unavoidable** in this docking; and
2. those sides admit **uncontrollable alternative contacts** in every tiling.

Only the first statement follows from N26.  This note asks for a finite local
criterion sufficient for controlling the second.  It then tests K10B against
that criterion before any coordinate work can resume.

The HC-19 correction is a precondition: the two copies belong to one length
class but are not the same directed role.

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

Let an intended code side have two convex endpoint angles, and let its
full-arc docking partner have the N26 complementary reflex endpoint angles.
At an internal subdivision point of a straight host side, the reflex partner
cannot replace the intended side in any interior-disjoint gapless patch.
Consequently length together with convex endpoint context locally recovers
the intended code role at every K9A primary host junction.

### Proof

The host occupies a straight sector of angle `pi` at an internal subdivision
point.  A reflex auxiliary occurrence contributes an angle strictly greater
than `pi` at the same point.  Their sector sum is therefore strictly greater
than `2*pi`, so their interiors overlap.  An intended convex endpoint is not
excluded by this argument and is the endpoint used in the K9A sector
equation.  Applying the argument at both endpoints distinguishes the intended
side from its auxiliary side of the same length.  □

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
