# K16W selector attack table

**Date:** 2026-07-24

**Status:** HC-37 theorem draft; second-chart obstruction and exact
root-labelled attack table, no root or cell elimination

**Scope:** the transverse parts of S1, S2 and S3 after K33C

## 1. K39C: exact C-line offset under the second bridge

Retain the B frame and put

```text
U=conj(rho_B)*w_5=U_x+i*U_y,
kappa=rho_C/rho_B=q^2*z_2=-i*z_2.                  (1.1)
```

Since `rho_C=rho_B*kappa`,

```text
m_C=det(rho_C,w_5)
   =Im(conj(kappa)*U)
   =Re(conj(z_2)*U)
   =dot(z_2,U).                                    (1.2)
```

On either K32A chart `z_2=sigma_2*T(t_2)`, this is

```text
m_C=sigma_2*((1-t_2^2)*U_x+2*t_2*U_y)/(1+t_2^2),
-1<=t_2<=1,       t_2!=0.                          (1.3)
```

### ST-M1.K39C

The second bridge-chart sign does not, by itself, fix `m_C`:

- if `U_y!=0`, the limits at `t_2=-1,+1` are
  `-sigma_2*U_y` and `+sigma_2*U_y`, so both signs occur in that one chart;
- if `U_y=0`, the strict chart interior has sign `sigma_2*sign(U_x)` but the
  vertical seams have `m_C=0`.

**Admitted form:** exact scope obstruction.  It is not a complete-cell
feasibility result and does not prove that `P_C` takes both signs under all
K16W predicates.

### Proof

Equation (1.2) follows from `conj(kappa)=i*conj(z_2)` and
`Im(i*z)=Re(z)`.  Substitute the tangent chart to get (1.3).  Evaluation at
the two vertical endpoints gives the stated values.  If `U_y=0`, the remaining
factor `1-t_2^2` is positive in the strict interior and zero at the seams.  □

Thus neither `sigma_2=-1` nor `sigma_2=+1` supplies the missing C selector
without full-cell inequalities.

## 2. K39O: which selector can still be negative

Label the two transverse roots by K35D's `epsilon=-,+`.  K37Q gives

```text
L_B^+<L_B^-,             L_C^+>L_C^-.              (2.1)
```

K36M converts cell signs to

```text
          B             C
S1:   L_B<0         L_C>0
S2:   L_B>0         L_C<0
S3:   L_B>0         L_C>0.                         (2.2)
```

If one root's signed expression lies farther in the direction of (2.1), the
conjugate root necessarily has the same sign and the selector product is
positive.  Applying this observation gives the exact table

```text
root stratum    P_B may be negative    P_C may be negative
----------------------------------------------------------
S1, epsilon=-          no                     no
S1, epsilon=+          yes                    yes
S2, epsilon=-          yes                    yes
S2, epsilon=+          no                     no
S3, epsilon=-          yes                    no
S3, epsilon=+          no                     yes.         (2.3)
```

Here “yes” means only “not excluded by monotonicity,” never that the
polynomial is negative.

### ST-M1.K39O

Among the twelve root-labelled B/C selector attacks
(`3 cells * 2 roots * 2 strands=12`), exactly six can possibly satisfy K36P's
negative selector condition.  In the other six, the corresponding product is
strictly positive.  The live attack set is

```text
S1+: B,C;       S2-: B,C;       S3-: B;       S3+: C.       (2.4)
```

**Admitted form:** necessary-condition implication on root-labelled strata.
It reduces selector-attack bookkeeping from 12 to 6, but removes no closure
root or K34Q cell and lowers no continuous-variable or degree count.  It is
therefore explicitly not an HC-37 success metric.

### Proof

For example, on `S1,epsilon=-`, `L_B^-<0`; (2.1) forces
`L_B^+<L_B^-<0`, so `P_B=L_B^+L_B^->0`.  Also `L_C^->0` and
`L_C^+>L_C^->0`, so `P_C>0`.  This proves the first row.  The other five rows
follow identically by inserting (2.2) into (2.1).  Strictness follows from
`Delta>0`, `Q_B>0>Q_C`, and the center-contact exclusion in K36M.  □

## 3. Final-session target

The bridge semicircles do not fix either selector.  K39O nevertheless removes
half of the exact attacks and shows where a proof can still exist.  Session
161 gets one final theorem attempt on the six expressions in (2.4), including
the S3 sum sign.  If none is uniformly negative and no admitted count falls,
D-0182's thin-lens freeze fires.
