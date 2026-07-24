# K28W guard-role collapse

**Date:** 2026-07-24

**Status:** HC-38 theorem draft; exact contact-language no-go for the K28G
transfer, no solver, coordinates, polygon, patch or candidate

**Scope:** K28G with the unchanged K9A/K9T complete clean-spoke mechanism
and K22R internal spine

## 1. The actual unequal-guard boundary word

K28G changes only the two lens sides incident to the guard vertex. Its
intrinsic cyclic side word is therefore

```text
e,A,d,B,d,C,d,H,d,C,d,B,d,A,f.                    (1.1)
```

The sides `e,f` meet at the guard vertex. The middle thirteen sides are the
centrally paired shield spine. In particular, both endpoints of every `B`
or `C` occurrence in (1.1) are incident to a side of length `d`.

### ST-M1.K41R

Assume `a,b,c,d,e,f,h` are pairwise distinct except for the repetitions
displayed in (1.1), with `h=a+b+c`. Then the intended guard roles are
intrinsic to the unmarked boundary word:

1. `H,e,f` are the three singleton length classes;
2. `e,f` are the unique singleton pair meeting at one vertex;
3. the unique `H` side roots the two directions around the cycle; and
4. the intervening ordered `A,B,C` progression distinguishes `e` from `f`
   in an oriented pose, while reflection reverses the complete rooted pose.

This is boundary-role recovery only. It does not classify subdivided covers
or prove that any intended contact patch exists.

### Proof

Multiplicity identifies the three singleton classes and the repeated
classes `A,B,C,d`. Of the singleton classes, only `e,f` are adjacent. The
remaining singleton `H` roots the opposite boundary arc. Reading from `H`
toward the `e|f` vertex gives the two reverse sequences

```text
d,C,d,B,d,A,f     and     d,C,d,B,d,A,e.            (1.2)
```

Since `e!=f`, these identify which end is which. An orientation-reversing
isometry reverses the whole word and hence the rooted role assignment; it
does not create a third assignment. □

K41R shows that mere boundary ambiguity is not the obstruction. The contact
equations themselves are.

## 2. N44: complete spokes force equal guard lengths

At a K9A primary division, let `u` and `v` be the lengths of the two complete
guard sides leaving its `gamma` vertex. K9A's selected directed adjacency
set is

```text
E={(A,B),(B,C),(A,C),(C,B)}.                       (2.1)
```

The complete clean-spoke equations from K9A/K9T are

```text
u_A=u_B=u_C=u,             v_B=v_C=v,              (2.2)
```

where `u_X` is the full carrier side leaving the right endpoint of code role
`X`, and `v_Y` the full side leaving the left endpoint of role `Y`.

### ST-M1.N44

For the boundary word (1.1), every realization of the four selected K9A
primary stars with complete clean guard contacts forces

```text
u=v=d,             hence {e,f}={d,d}.               (2.3)
```

The conclusion is unchanged by reflection or by swapping the names of the
two guard sides.

### Proof

Every intrinsic `B` side and every intrinsic `C` side in (1.1) is flanked on
both endpoints by `d`. Thus, regardless of which rooted occurrence supplies
the selected directed role,

```text
u_B=u_C=d,                v_B=v_C=d.                (2.4)
```

The transitions `(B,C)` and `(C,B)` occur in (2.1). Their two complete
guard--code interfaces identify the guard-side lengths with the values in
(2.4). Equation (2.2) therefore gives `u=v=d`. The two sides incident to
the guard vertex in (1.1) are precisely `e,f`, so both equal `d`. Reflection
interchanges left and right but leaves (2.4) unchanged. □

This proof uses no cover-table assumption beyond the complete full-side
contacts already built into K9A/K9T and K28W. Allowing partial, multi-edge or
context-dependent guard contacts is a different mechanism.

## 3. N45: the K28G transfer cannot realize K9A/K9T

### ST-M1.N45

No simple carrier in the K28G family realizes the K9A/K9T selected language
with the unchanged boundary word and complete clean spokes.

### Proof

If the guard lengths are genuinely unequal or distinct from `d`, N44 gives an
immediate contradiction. If they are permitted to collapse, N44 gives

```text
e=f=d.                                               (3.1)
```

K28G then specializes exactly to the equal-leg, equal-spoke K22S rhombic
family. N37 proves that one named pair of nonadjacent spoke segments crosses
throughout that complete family. Hence its spine is not simple. These two
cases exhaust K28G under the stated contact mechanism. □

N45 closes K28W at stronger scope than a semialgebraic UNSAT result: the
unequal geometric degrees of freedom cannot enter the selected contact
language at all, and their only clean-spoke specialization is already
geometrically refuted.

## 4. What remains outside the no-go

N44--N45 do not rule out:

- a carrier whose `B,C` code sides have intrinsically unequal endpoint
  spokes rather than the repeated `d` word;
- partial or multi-edge guard interfaces with a complete finite contact
  theorem;
- contextual guard poses whose left/right arcs are not fixed full sides;
- a different state selector or side word; or
- carriers without a centrally paired guard lens.

Each item changes a named hypothesis. Merely assigning new values to the two
outer sides of (1.1) cannot reopen K28W.
