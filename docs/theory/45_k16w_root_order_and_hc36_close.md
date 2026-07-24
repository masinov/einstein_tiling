# K16W transverse-root order and HC-36 close

**Date:** 2026-07-24

**Status:** HC-36 final theorem draft; ordered root transitions, no transverse
root or cell elimination

**Scope:** two transverse closure roots arising from one fixed intrinsic
K16B parameter point

## 1. K37O: exact angular order of the closure roots

K30E factors as

```text
Z_epsilon=(A+i*B)*(T+i*epsilon*sqrt(Delta))/R.       (1.1)
```

For a complete K16W root, strict rectangle containment makes

```text
T=D dot p_8>0.                                      (1.2)
```

### ST-M1.K37O

On `Delta>0`, `Z_+` is obtained from `Z_-` by a strict counterclockwise
rotation through

```text
2*atan(sqrt(Delta)/T) in (0,pi).                    (1.3)
```

If both roots satisfy the first-quadrant terminal chart, the same statement
holds without crossing either coordinate axis.

**Admitted form:** exact root-order equivalence; it does not remove a root.

### Proof

Both factors in (1.1) have modulus `sqrt(R)`, because
`R=T^2+Delta`.  Their quotient by `R` is therefore unit.  The arguments of
`T+i*sqrt(Delta)` and `T-i*sqrt(Delta)` are respectively
`+atan(sqrt(Delta)/T)` and its negative.  The common first factor cancels in
their difference, proving (1.3).  □

## 2. K37Q: the two long-strand selector slopes have fixed signs

K36P uses

```text
Q_B=dot(rho_B,w_8),       Q_C=dot(rho_C,w_8).       (2.1)
```

Rotating by any complete terminal direction gives

```text
Q_B=dot(Z*rho_B,p_8),     Q_C=dot(Z*rho_C,p_8).     (2.2)
```

N38 and strict containment give

```text
Z*rho_B=(x_B,y_B),     x_B>0, y_B>0,
Z*rho_C=(x_C,y_C),     x_C<0, y_C<0,
p_8=(P,Q),             P>0, Q>0.                   (2.3)
```

### ST-M1.K37Q

Every intrinsic parameter point possessing a complete K16W root satisfies

```text
Q_B>0,             Q_C<0.                          (2.4)
```

Hence its conjugate strand expressions obey

```text
L_B^+<L_B^-,       L_C^+>L_C^-.                    (2.5)
```

**Admitted form:** necessary-condition implication.  It orders the two
strand tests but does not fix either product sign in K36P.

### Proof

Dot products are rotation invariant, giving (2.2).  Both summands in the B
dot product are positive, while both summands in the C dot product are
negative.  Equation (2.5) follows immediately from K36M's
`L_j^epsilon=F_j-epsilon*sqrt(Delta)*Q_j`.  □

The proof needs only one complete root to establish (2.4), since `Q_B,Q_C`
are intrinsic and are shared by its conjugate closure root even if that other
root later fails a predicate.

## 3. K37S: monotone two-root strand transitions

Use `-` for a crossing below H and `+` for one above H.  K36M and (2.5) show
that, as `epsilon` changes from `-1` to `+1`, each of B and C may keep its
sign or change from below to above, but can never change from above to below.

### ST-M1.K37S

If both transverse roots of one intrinsic parameter point are complete K16W
spines, their K32S cell labels can occur only in the six ordered pairs

```text
S2 -> S2, S3, S1;
S3 -> S3, S1;
S1 -> S1.                                           (3.1)
```

The reverse transitions are impossible.

**Admitted form:** necessary-condition implication for a two-complete-root
parameter point.  It reduces the abstract ordered cell-transition table from
`3*3=9` to `6`, but it does **not** reduce the six live K34Q cells, the two
closure roots within a cell, the continuous variables or polynomial degree.
It is therefore not booked as D-0178's quantified success.

### Proof

For B, K36M says `sign(d_B)=-sign(L_B)`.  Since `L_B` strictly decreases,
`d_B` can remain below, change from below to above, or remain above.  For C,
`sign(d_C)=sign(L_C)` and `L_C` strictly increases, giving the same three
possibilities.  N43 removes S4, so the only complete mixed-sign order is S3.
Coordinatewise monotonicity now gives exactly (3.1).  □

The additional S3 inequality `d_B+d_C<0` may reject a particular root, but
the present results do not make its sign monotone.  It is retained rather
than inferred.

## 4. Why the transverse roots remain open

K37Q supplies the signs of `Q_B,Q_C`, but not the relative magnitudes of
`F_j` and `sqrt(Delta)*Q_j`.  Thus it does not decide

```text
F_j^2-Delta*Q_j^2.                                  (4.1)
```

A strict tangent solution, if one exists, also explains the obstruction: as
`Delta` approaches zero the two roots coalesce, and every strict strand and
nonintersection sign can remain unchanged on both nearby branches.  This is
an explanatory continuity observation, not an existence claim for a tangent
K16W spine.

No complete per-cell chord inequality proved in HC-36 forces (4.1) negative.
Accordingly all six K34Q cells retain both transverse root obligations, and
no tangent cell is declared empty.

## 5. HC-36 disposition

HC-36 reaches one measured result and two structural ones:

```text
tangent solver variables:       8 -> 7   (K35T),
tangent geometric variables:    7 -> 6   (K35T),
transverse roots per live cell:  unchanged at 2,
live K34Q cells:                 unchanged at 6,
maximum polynomial degree:      no reduction claimed.          (5.1)
```

K35D/K36W give the exact physical frames; K36M/K36P isolate the missing
root-selector polynomial; K37O/K37Q/K37S order any two complete roots.  None
licenses a solver run, a timeout increase, a dropped predicate or a candidate
claim.

The three-session allowance is exhausted.  K16W remains open/frozen outside
the exact tangent reduction.  A next checkpoint must choose explicitly among:

1. a certified decision procedure applied separately to K35T's tangent
   presentation and K36P's transverse strata;
2. a new theorem targeting one named retained nonadjacent pair or the S3 sum;
   or
3. a pivot away from the thin-lens carrier.

No choice is made by HC-36.
