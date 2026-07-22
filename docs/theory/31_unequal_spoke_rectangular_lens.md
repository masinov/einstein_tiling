# Unequal-spoke right-angle guard

**Status:** HC-25 topology proof draft; no polygon, coordinates or candidate

**Retained data:** K9A/K9T complete clean spokes, `gamma=pi/2`,
`theta=rho_X=pi/4`, central guard--shield half-turn and full Euclidean
isometries

**Changed datum:** outgoing spoke length `u` and incoming spoke length `v`
may differ

## 1. Directed spoke roles

At a selected primary transition `X|Y`, K9A's guard has two complete sides:

```text
right endpoint of X -- length u -- guard,
guard -- length v -- left endpoint of Y.              (1.1)
```

Equivalently, the intrinsic side immediately leaving the right endpoint of
each left role `X in {A,B,C}` has length `u`, while the side immediately
leaving the left endpoint of each right role `Y in {B,C}` has length `v`.
These are directed boundary roles, not two names for an unmeasured port.

## 2. N34: the old connector forces equal legs

### ST-M1.N34

K10B's original 15-edge boundary word cannot realize the complete clean-
spoke equations with `u!=v`.

### Proof

In the old word, the boundary segment between the intrinsic `A` and `B`
sides is one complete side. At its `A` endpoint it is the outgoing spoke
`u_A`, hence has length `u`. At its `B` endpoint the same segment is the
incoming spoke `v_B`, hence has length `v`. A polygonal side has one length,
so `u=v`. The one-side connector between `B` and `C` gives the same identity.
The paired half of the spine repeats both identities. □

Thus unequal guard legs are not a numerical variation of K10B. They require
a changed boundary topology. N33 cannot be evaded merely by replacing some
printed `d` labels with `u` and others with `v` on the old word.

## 3. K16B: minimal split-spoke lift

Each incompatible `A--B` and `B--C` connector needs at least one new boundary
vertex so an outgoing `u` side and incoming `v` side can be distinct. The
minimal centrally paired split replaces each such connector by the ordered
two-side path `u,v`. It leaves the outgoing `C--H` side as `u`, because `H`
has no K9A incoming-`v` role.

The first half-spine is therefore

```text
A,u,v,B,u,v,C,u,                                      (3.1)
```

and central pairing fixes the complete spine as

```text
A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A.                  (3.2)
```

Choose the guard path from `R` to `Q` to have consecutive lengths `v,u`.
The resulting cyclic carrier word is

```text
v,A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A,u.              (3.3)
```

It has 19 sides. Relative to K10B, the four added sides are forced by the two
split connectors and their centrally paired copies. Up to cyclic reversal,
(3.3) is the unique edge-count-minimal split of those four one-side
connectors while leaving every other K10B adjacency unchanged.

### Angle inventory

The five retained sharp vertices on the first half are

```text
A|u,  v|B,  B|u,  v|C,  C|u,                        (3.4)
```

each with carrier angle `pi/4`. The new bridge vertices `u|v` have angles
`delta_1,delta_2 in (0,2*pi)`, to be derived rather than guessed. The
`u|H` angle and terminal `v|A` angle remain free under the earlier K10B
contract, and the paired half has complementary shield contexts.

### Status

K16B is a finite combinatorial carrier topology, not a realization theorem.
In particular it has not proved:

- that the two new bridge angles can be recognized without markings;
- that the many repeated `u` and `v` sides have complete cover tables;
- simplicity or containment of its spine;
- either complete `ABC/ACB` placement patch; or
- the all-tilings converse.

## 4. Rectangular guard lens

Put

```text
R=(0,0),       Gamma=(v,0),       Q=(v,u).           (4.1)
```

The half-turn about `(v/2,u/2)` sends `Gamma` to `(0,u)`. The two guard paths
therefore bound the exact rectangle

```text
L(u,v)=[0,v] x [0,u].                                (4.2)
```

This is the sole geometric gain admitted by HC-25: the square has become a
rectangle, and the incompatible connector has become the explicit `u|v`
bridge. No additional junction participant or contact radius is introduced.

## 5. Next exact obligation

Let the signed exterior bridge turns be

```text
sigma_i=pi-delta_i,       i=1,2.                     (5.1)
```

Session 129 must apply the fixed turn sequence

```text
3*pi/4, sigma_1, 3*pi/4, 3*pi/4,
sigma_2, 3*pi/4, 3*pi/4                              (5.2)
```

to (3.1), derive every first-half partial sum, impose central host closure
and all rectangle inequalities, and determine whether the free bridge angles
are genuine geometric degrees of freedom or merely unmarked colors. No
coordinate fitting or angle enumeration is admitted.
