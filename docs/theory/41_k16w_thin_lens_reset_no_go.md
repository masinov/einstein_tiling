# K16W thin-lens reset no-go

**Date:** 2026-07-23

**Status:** HC-33 theorem draft; the complete K16W existential obligation is
refuted, with no solver, polygon, patch or candidate

**Scope:** the fixed 19-edge K16B unequal-spoke rectangular carrier,
normalized by `u=1`

## 1. A directed reset bound

Consider two directed segments contained in the open vertical strip
`0<x<v`.  Suppose their horizontal displacements have the same nonzero
sign and absolute values strictly above `s_1,s_2`.  If a polygonal path of
total length `P` joins the terminal endpoint of the first segment to the
initial endpoint of the second, then

```text
P>s_1+s_2-v.                                      (1.1)
```

Indeed, for two eastward segments the first terminal endpoint has
`x>s_1`, while the second initial endpoint has `x<v-s_2`.  The joining path
must reset westward by more than `s_1+s_2-v`, and its length strictly exceeds
that horizontal displacement.  Reflection in a vertical line gives the
westward case.

This is a necessary condition only.  It does not replace or weaken any of
K21Q's segment predicates.

## 2. The forced neighboring pair

In the sole N41-surviving polarity cell, the length-`v` C strand is westward.
Its centrally paired mate C' is eastward.  Let the central H strand have
length

```text
h=a+b+c.                                          (2.1)
```

Every endpoint is in the open `v`-by-1 rectangle.  Therefore the C/C'
horizontal span is strictly above

```text
L=sqrt(v^2-1),                                    (2.2)
```

and the H horizontal span is strictly above

```text
M=sqrt(h^2-1).                                    (2.3)
```

The central strand cannot be vertical because `h>5/sqrt(2)>1`, whereas its
vertical displacement is below `1`.  Hence it points either west or east.

- If H points west, C and H have the same polarity.  The intervening path is
  exactly the `c,1` path from `p_6` to `p_8`.
- If H points east, H and C' have the same polarity.  The intervening path is
  the centrally paired `1,c` path from `p_9` to `p_11`.

Thus (1.1) gives in both exhaustive cases

```text
c+1>M+L-v=M-delta(v),
M<c+1+delta(v),                                  (2.4)
```

where `delta(v)=v-sqrt(v^2-1)`.

## 3. The opposite exact budget

K31C and K30W give

```text
v>v_0=sqrt(23/2),
c<U(v)<U_0=sqrt(46)/(sqrt(21)-sqrt(2)),
delta(v)<delta_0=(sqrt(46)-sqrt(42))/2.           (3.1)
```

The three exact rational comparisons needed below are

```text
v_0>10/3,       U_0<13/6,       delta_0<1/6.     (3.2)
```

The first follows by squaring, since `207>200`.  For the second, both sides
of

```text
6*sqrt(46)<13*(sqrt(21)-sqrt(2))                 (3.3)
```

are positive.  The left square is `1656`; the right square is
`3887-338*sqrt(42)`, which is strictly above `1690` because
`sqrt(42)<13/2`.  The last comparison in (3.2) follows from

```text
delta_0=2/(sqrt(46)+sqrt(42))<1/6.               (3.4)
```

Meanwhile `a>1/sqrt(2)`, `b>sqrt(2)`, and `c>sqrt(2)`, so

```text
h>5/sqrt(2),
M=sqrt(h^2-1)>sqrt(23/2)=v_0>10/3.               (3.5)
```

Equations (3.1)--(3.2) give the incompatible upper bound

```text
c+1+delta(v)<U_0+1+delta_0
                 <13/6+1+1/6=10/3.              (3.6)
```

## 4. ST-M1.N42: K16W is empty

There is no simple K16W spine in the fixed K16B topology.

**Admitted form:** necessary-condition implication from complete K16W,
ending in contradiction.

### Proof

Section 2 exhausts the two possible horizontal polarities of H and proves
the necessary reset inequality `M<c+1+delta(v)`.  Sections 3.5--3.6 prove
the strict reverse chain

```text
M>10/3>c+1+delta(v).
```

Contradiction.  The proof uses only complete K16W containment, simplicity,
the fixed K16B edge order, N38 and the admitted K30W/K31C bounds.  □

## 5. Exact disposition of the 16 HC-32 cells

Each K32S strand cell `S_1,...,S_4` and each K32A chart pair
`(+,+),(+,-),(-,+),(-,-)` inherits (2.4), because neither the reset lemma
nor the weight budget selects a bridge chart or vertical order.  Hence the
complete table is

```text
             S_1       S_2       S_3       S_4
(+,+)        empty     empty     empty     empty
(+,-)        empty     empty     empty     empty
(-,+)        empty     empty     empty     empty
(-,-)        empty     empty     empty     empty
```

Every entry is refuted by the same necessary inequality and its exact
opposite.  No discriminant or strict-boundary stratum survives, so K32R does
not require computational treatment and no HC-33 formula is warranted.

## 6. Scope boundary

N42 refutes K16W: the exact witness obligation for the minimal 19-edge
split-spoke rectangular carrier K16B.  It does **not** prove that no
aperiodic monotile exists, that no guard-and-shield construction exists, or
that unequal guard legs and other boundary words are impossible.  The
conditional symbolic compiler and K13F weighted-language family remain
valid.  Reopening this geometric route requires changing a named N42
hypothesis, such as the fixed `C,1,H,1,C'` neighboring topology or the unit-
height thin lens; a longer solver budget is not a change of hypothesis.
