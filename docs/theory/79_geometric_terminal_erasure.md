# Geometric terminal erasure for the parity zipper

**Date:** 2026-07-29  
**Scope:** K70P clauses 1 and 3 at rooted contact-complex level; coexistence of
all required side germs on one connected asymmetric polygon  
**Status:** phase-zero terminals erased exactly; collision-free parity patches
and all-tilings local closure remain open

K70Z used a three-code-side word with phase zero assigned at both endpoints.
This note removes those assignments.  Two intrinsically different delimiter
sides and fixed three-participant terminal stars force the two endpoint
phases geometrically.  A separate constructive lemma proves that one simple
asymmetric polygon can carry the host, delimiter, code, and cap germs
simultaneously.

No claim is made that the resulting polygon realizes the complete patches:
placing three congruent neighbor bodies without overlap is the next
obligation.

## 1. The exact terminal roles

Retain K70Z's four unit code roles

```text
E_pq,       p,q in {0,1},       visible bit p xor q,
```

with endpoint angles

```text
L_0=pi/3,          L_1=pi/4,
R_0=2pi/3,         R_1=3pi/4.                           (1.1)
```

Add two directed delimiter sides of length four:

```text
D_L : (outer-left angle, inner-right angle) = (pi/2, 2pi/3),
D_R : (inner-left angle, outer-right angle) = (pi/3, pi/2).   (1.2)
```

Finally take a host side `H` of length eleven.  At both endpoints of `H`,
the host occurrence contributes angle `5pi/6`.  A fixed cap role contributes
angle `2pi/3` at the same point.

The terminal star then fills exactly for the delimiter's outer angle:

```text
5pi/6 + pi/2 + 2pi/3 = 2pi.                            (1.3)
```

No code endpoint has angle `pi/2`; its possibilities are
`pi/4,pi/3,2pi/3,3pi/4`.  Thus the rooted terminal star distinguishes the
delimiter from every code role.  Full-isometry reversal does not create a
false complete word: reversing `D_L` presents inner angle `2pi/3` at the
outer terminal and angle `pi/2` at the first internal junction, while
reversing `D_R` gives the analogous mismatch.  Neither can satisfy both its
terminal and internal equations.

The cap angle is a rooted role, not a claim that angle `2pi/3` alone
identifies one vertex of the final polygon.  K71B below makes the complete
adjacent germ intrinsically distinguishable; the all-contact converse
remains a later atlas obligation.

## 2. K71T — terminals force the exact even-parity word

Place `H` as a straight interval.  Require a gapless full-side cover in the
directed order

```text
D_L, E_1, E_2, E_3, D_R.                              (2.1)
```

The lengths are

```text
4+1+1+1+4=11=|H|.                                     (2.2)
```

At each of the four internal division points the host contributes angle
`pi`.  Equations (1.1)--(1.2) give

```text
right(D_L)+left(E_pq)=pi       iff p=0,
right(E_pq)+left(E_rs)=pi      iff q=r,
right(E_pq)+left(D_R)=pi       iff q=0.                (2.3)
```

The mismatched sums are `11pi/12` or `13pi/12`, never `pi`.  Hence the
first code side has incoming phase zero, consecutive phases match, and the
last has outgoing phase zero.  Eliminating the internal phases gives exactly

```text
000, 011, 101, 110.                                   (2.4)
```

Conversely, each word in (2.4) integrates uniquely from phase zero and all
five sides satisfy (1.3) and (2.3).  Thus the terminal phases are no longer
assigned colors: they are forced by the two delimiter germs and the bounded
terminal stars.

The fixed order in (2.1) is part of the rooted contact complex.  For a final
polygon it must be forced rather than assumed.  One sufficient exact
mechanism is:

1. the terminal stars admit only the outer germs of `D_L` and `D_R`;
2. those two complete length-four sides occupy the two ends of `H`; and
3. every other side capable of meeting the residual host interval has length
   one.

Then the residual interval has length three and is covered by exactly three
unit code sides.  No third delimiter fits because its length is four.

## 3. K71B — arbitrary finite convex side germs coexist on one polygon

### Lemma

Let

```text
G={(ell_i,lambda_i,rho_i):1<=i<=m}
```

be a finite list with `ell_i>0` and
`0<lambda_i,rho_i<pi`.  There is a connected simple polygonal disk containing
pairwise nonadjacent directed boundary sides whose lengths and endpoint
interior angles are exactly the members of `G`.  Extra side lengths and
angles can be chosen to make the polygon symmetry-free and to distinguish
the complete rooted two-edge germ of every listed side.

If all lengths and the sines/cosines of the angles lie in one ordered
algebraic field, the construction uses coordinates in that field.

### Proof

For each prescribed side, make it the outer edge of a shallow trapezoidal
tab.  Put the side horizontally with polygon interior below it.  From its
left and right endpoints draw the adjacent tab flanks downward at the unique
directions that give interior angles `lambda_i` and `rho_i`.  Stop both
flanks at a common sufficiently small depth `epsilon_i`.  This realizes the
complete prescribed side germ.

Place the tabs far apart along the upper boundary of a large rectangle.
Because there are finitely many and their depths may be chosen arbitrarily
small, their closed bounding boxes are disjoint.  Join successive tab bases
by horizontal and short slanted connector chains, and use the other three
sides of the rectangle to close the boundary.  The resulting cyclic chain is
simple and bounds a disk.  Prescribed sides are separated by connector
chains, so none shares a vertex with another.

Choose all tab spacings, connector lengths, and one additional asymmetric
marker tab pairwise distinct and outside the finite prescribed length set.
Any polygon symmetry must preserve the unique marker and then the directed
sequence of distinct spacings, hence is the identity.  The same choices make
each prescribed side's adjacent two-edge length/angle word unique.  All
coordinates use field operations and the prescribed direction vectors, so
the field assertion follows.  QED.

### Application

Apply K71B to the seven side roles

```text
H, D_L, D_R, E_00, E_01, E_10, E_11
```

with the lengths and angles in Sections 1--2, and add one rooted cap vertex
of angle `2pi/3` with a unique adjacent length word.  Since all angles are
multiples of `pi/12`, one connected symmetry-free algebraic polygon can carry
every required role.  This closes K70P clause 1 as an existence theorem for
the boundary alphabet.  It does not close simultaneous patch packing.

## 4. What is now solved and what is not

Solved exactly:

- phase-zero is forced at both ends without a painted bit;
- the complete five-side cover projects exactly to ternary even parity;
- full-isometry reversal of a delimiter cannot imitate the opposite terminal;
- one connected asymmetric polygon can contain all seven rooted side germs
  and a distinguishable cap germ.

Still open:

1. place the host, two delimiters, three code neighbors, and two terminal cap
   occurrences for all four words with pairwise-disjoint interiors;
2. make those occurrences copies of the **same** K71B polygon while retaining
   the stated rooted roles;
3. prove that every possible host cover in every tiling has the form (2.1),
   including contacts by connector sides and reflected copies;
4. integrate the zipper with the 31-state AHI macro cover; and
5. reject periodic and nondecoding whole-plane tilings.

The next mathematical object is therefore a simultaneous congruent-packing
lemma for the four finite parity patches.  Boundary-role existence and
terminal erasure are no longer the blockers.
