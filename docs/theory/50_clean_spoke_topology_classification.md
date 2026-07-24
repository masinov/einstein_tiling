# Edge-minimal clean-spoke topology classification

**Date:** 2026-07-24

**Status:** HC-38 theorem draft; exact combinatorial classification, no
geometry witness, solver, polygon, patch or candidate

**Scope:** K9A/K9T selected transitions, complete full-side spokes, fixed
shield role order and two-copy half-turn docking

## 1. Directed endpoint ports

For a selected primary transition `X|Y`, write

```text
U_X = side immediately leaving the right endpoint of X,
V_Y = side immediately leaving the left endpoint of Y.       (1.1)
```

K9A/K9T's complete clean-spoke language requires

```text
|U_A|=|U_B|=|U_C|=u,
|V_B|=|V_C|=v.                                      (1.2)
```

The shield's directed first-half role order is

```text
A, B, C, H.                                         (1.3)
```

The second half is fixed by the half-turn. Thus the two constrained
first-half gaps are `A--B` and `B--C`; `C--H` has only the outgoing `u`
constraint because `H` is not a K9A right code role.

### ST-M1.K42P

If one polygon side is the complete gap between consecutive directed code
roles `X,Y`, then it simultaneously represents `U_X` and `V_Y`. Hence that
one-edge gap is legal only if

```text
u=v.                                                 (1.4)
```

If `u!=v`, every such gap contains at least two polygon sides and at least
one irredundant bridge vertex. At the minimum of two sides, its rooted length
word is exactly

```text
u,v.                                                 (1.5)
```

### Proof

A single geometric side has one length. At its first endpoint it is `U_X`
and at its second it is `V_Y`, giving (1.4). If the two lengths differ, the
two endpoint germs cannot belong to one side, so an intervening vertex is
necessary. A two-side path has its first length fixed to `u` and last fixed
to `v`, proving (1.5). □

This is the port-incidence form of N34 and N44. It depends only on directed
endpoint roles, not angles or coordinates.

## 2. K42M: the two edge-minimal half-turn words

### ST-M1.K42M

Up to cyclic reversal, the edge-minimal carrier words satisfying (1.2), the
role order (1.3), and the fixed half-turn shield pairing are exactly:

**Equal ports `u=v=d`:**

```text
d,A,d,B,d,C,d,H,d,C,d,B,d,A,d,                    (2.1)
```

the 15-edge K10B word.

**Unequal ports `u!=v`:**

```text
v,A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A,u,            (2.2)
```

the 19-edge K16B word.

No third edge-minimal word exists under these hypotheses.

### Proof

When `u=v`, K42P permits one side in each constrained gap. Keeping every
other gap at one side and applying the half-turn gives (2.1); deleting any
side merges distinct code or host roles.

Now assume `u!=v`. K42P forces both first-half gaps `A--B` and `B--C` to be
the two-side path `u,v`. The minimal `C--H` path is the single outgoing side
`u`. Thus the first half is forced:

```text
A,u,v,B,u,v,C,u.                                    (2.3)
```

The half-turn reverses the paired role order and fixes the central `H`, so
it forces the complete shield spine

```text
A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A.                 (2.4)
```

The guard path must present the incoming `v` at the first terminal role and
the paired outgoing `u` at the other; adjoining it to (2.4) gives (2.2).
Every insertion was forced either by a directed port or by central pairing.
Any other word with the same number of edges changes an endpoint length,
role order or pairing; any word with more edges is not edge-minimal. Reversal
accounts for the opposite global orientation. □

K42M upgrades K16B's earlier construction statement to an exhaustive
incidence classification. It does not prove either word geometrically
realizable.

## 3. N46: what the K28W failure exhausts

### ST-M1.N46

Within the fixed clean-spoke, half-turn, `A-B-C-H-C-B-A` architecture, there
is no third minimal carrier family between K10B and K16B.

- Keeping one-edge connectors forces `u=v` and belongs to K10B/K22S, closed
  by N33/N37.
- Allowing `u!=v` forces K16B, whose tangent stratum is under HC-38 decision
  and whose transverse strata remain open.
- Changing only the two outer lens lengths, as in K28G, cannot create a new
  contact family because the internal one-edge connectors still force
  equality (N44).

### Proof

This is the exhaustive dichotomy `u=v` or `u!=v` in K42M, with the cited
geometric dispositions. □

N46 is not a K16B nonexistence theorem. It says that another numerical lens
variation cannot constitute an independent clean-spoke pivot.

## 4. A reusable topology-synthesis filter

The proof gives a finite pre-geometry compiler for future carrier ideas:

1. specify the selected directed transition graph;
2. attach a required full-side port type to every directed role endpoint;
3. propagate equality whenever one boundary side serves two endpoint ports;
4. split precisely the unequal pairs with explicit bridge vertices;
5. impose the proposed docking involution on the resulting word; and
6. quotient by cyclic reversal only after the rooted roles are fixed.

Every step is an exact equality or finite word operation. A topology that
fails is rejected before angle algebra or coordinates; a survivor has a
complete list of bridge roles that geometry must realize. No method-novelty
claim is made.

## 5. The next genuinely different pivot

By N46, a new carrier outside the thin-lens family must change at least one
of the following named hypotheses:

```text
F: every guard interface is one complete full side;
O: the shield role order is A-B-C-H-C-B-A;
J: the two-copy shield docking is a half-turn;
S: one fixed guard occurrence supplies both port sides.       (5.1)
```

Changing only weights, angles or outer lens lengths is insufficient. Of the
four exits, changing `J` is the cleanest theorem-first question: classify
reflection-based two-copy shield docking before any boundary is drawn.
Changing `F` requires a complete partial/T-junction contact language and is
therefore a larger later branch. The next checkpoint should audit `J` first,
with a predeclared negative outcome accepted.
