# K16W same-cell obstruction and HC-37 freeze

**Date:** 2026-07-24

**Status:** HC-37 final theorem draft; exact S3 sum selector, no root/cell
elimination, thin-lens carrier frozen

**Scope:** the six complete transverse K34Q cells

## 1. K40E: what the remaining attacks mean

Assume one intrinsic parameter point has two complete transverse roots.  The
K37S order is

```text
S2 <= S3 <= S1                                         (1.1)
```

as `epsilon` moves from minus to plus.  K39O then has a direct interpretation.

### ST-M1.K40E

- on an `S1,+` root, both B/C selector products fail to be negative exactly
  when the minus root is also in S1;
- on an `S2,-` root, both fail exactly when the plus root is also in S2;
- on an S3 root, the only individually live selector records whether the
  conjugate root leaves the mixed B-below/C-above sign pattern.

Thus B/C strand selection reduces a two-root obligation precisely when the
two roots do **not** retain the same coarse strand cell.  The unresolved cases
are the three diagonal transitions

```text
S1 -> S1,       S2 -> S2,       S3 -> S3.            (1.2)
```

**Admitted form:** exact necessary-and-sufficient interpretation of K39O for
two complete roots.  It changes no admitted complexity count.

### Proof

For `S1,+`, K36M requires `L_B^+<0<L_C^+`.  The B selector is negative
exactly when `L_B^->0`, and the C selector exactly when `L_C^-<0`; either
change takes the minus root out of S1, while if neither changes it remains in
S1.  The S2 statement is the same argument with signs reversed.  In S3,
K39O already proves one product positive and leaves exactly the strand whose
sign change exits the mixed pattern.  □

The S3 sum still distinguishes S3 from the already-refuted S4 and must be
handled separately.

## 2. K40H: exact conjugate selector for the S3 sum

Write the two terminal roots as

```text
Z_epsilon=Z_0+epsilon*sqrt(Delta)*Z_1,
Z_0=T*(A+i*B)/R,
Z_1=i*(A+i*B)/R.                                     (2.1)
```

For the physical horizontal components put

```text
x_epsilon= Re(Z_epsilon*rho_B)
           =x_0+epsilon*sqrt(Delta)*x_1>0,
u_epsilon=-Re(Z_epsilon*rho_C)
           =u_0+epsilon*sqrt(Delta)*u_1>0.            (2.2)
```

K36M gives the actual midline offsets

```text
d_B^epsilon=-L_B^epsilon/(2*r^2*x_epsilon),
d_C^epsilon= L_C^epsilon/(2*r^2*u_epsilon).          (2.3)
```

Define

```text
H_epsilon=-u_epsilon*L_B^epsilon
           +x_epsilon*L_C^epsilon.                   (2.4)
```

Since the omitted denominator in (2.3) is positive,

```text
sign(d_B^epsilon+d_C^epsilon)=sign(H_epsilon).        (2.5)
```

Expansion gives another affine-radical pair

```text
H_epsilon=H_0+epsilon*sqrt(Delta)*H_1,                (2.6)

H_0=-u_0*F_B+Delta*u_1*Q_B
    +x_0*F_C-Delta*x_1*Q_C,
H_1= u_0*Q_B-u_1*F_B-x_0*Q_C+x_1*F_C.                (2.7)
```

### ST-M1.K40H

The exact radical-free selector for the extra S3 condition is

```text
H_+*H_-=H_0^2-Delta*H_1^2.                           (2.8)
```

If (2.8) is negative, at most one root can satisfy S3's
`d_B+d_C<0`.  If it is positive and one root satisfies the inequality, the
other has the same sum sign.  Equality puts one root on the already-excluded
S3/S4 boundary `d_B+d_C=0`.

**Admitted form:** exact conditional root selector.  No uniform sign of
(2.8) is proved on a live cell, so no root reduction is booked.

### Proof

Equation (2.3) is K36M with the known B-east/C-west denominator signs.
Multiplication by `2*r^2*x_epsilon*u_epsilon>0` gives (2.4)--(2.5).  Substitute
`L_j^epsilon=F_j-epsilon*sqrt(Delta)*Q_j` and (2.2); the even and odd terms are
exactly (2.7).  Multiplying the two conjugates proves (2.8) and the sign
claims.  □

## 3. Why HC-37 cannot book a selector reduction

K40E and K40H reduce the remaining question to excluding the same-cell pairs
(1.2).  Neither bridge semicircle fixes the necessary support-line offset
(K38B/K39C), and no retained containment or chord theorem fixes the signs of

```text
P_B,       P_C,       H_0^2-Delta*H_1^2             (3.1)
```

on those complete strata.  In particular, HC-37 proves no uniform negative
selector.  Treating the exact formulas as if their sign were established
would be the same conditional-to-global error the checkpoint was designed to
prevent.

## 4. HC-37 disposition

The measured counts remain

```text
continuous variables:          unchanged,
maximum polynomial degree:     unchanged,
live K34Q cells:                6,
transverse roots per live cell: 2.                    (4.1)
```

The auxiliary selector-attack list falls from 12 to 6 and then to three
same-cell obstructions, but this is not an admitted success metric.  No root,
cell, variable or degree count decreases.

D-0182's stop therefore fires.  The K16W thin-lens carrier is frozen; another
theorem-only refinement of the same selectors is not authorized.  Reopening
requires a new human decision choosing either:

1. a separately preregistered certified decision on K35T's seven-variable
   tangent stratum (with SAT requiring exact cold verification and bare UNSAT
   remaining solver evidence); or
2. a pivot to a different carrier geometry not governed by the same
   thin-lens same-cell obstruction.
