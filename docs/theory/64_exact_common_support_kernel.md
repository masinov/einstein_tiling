# Exact common-support kernel for the two AHI macros

The two optimized Section 10.1 large patches each contain fifteen physical
SAB rhombi.  Let their exact supports be `A` and `B`.  Exhausting the full
triangular-lattice isometry group and all translations aligning primitive
vertices gives

\[
  \max_g |A\cap gB|=13
\]

at the rhombus level (equivalently 26 of 30 primitive triangles).  Hence no
one-rhombus attachments can make the two macros share a support.

At each of the four symmetry-equivalent maximizers, the symmetric difference
has two rhombi on each side and the union is a 17-rhombus topological disk
with sixteen unit boundary edges.  Thus the smallest exact same-envelope
relation is

\[
  A\cup\{L,S\}=gB\cup\{M,S\},
\]

up to exchanging sides and global isometry.  The braces name source roles,
not free tiles: the cells are already internal to the opposing macro.

This is a useful but incomplete compiler kernel.  The actual optimized source
has singleton tiles only of role `M`; it does not supply a free `L+S` pair.
The equality therefore cannot be repeated as a tiling by simply attaching
published singleton tiles.  A valid construction must obtain those role
differences through a larger source-native regrouping.  The local
interchangeable pairs in the primary paper are the next finite object because
they already provide equal-support regroupings in the admitted source
language.

The exact census and boundary certificates are serialized in
`data/sturmian-source/ahi-common-support-kernel.json` and independently
reconstructed by `scripts/verify_sturmian_common_support_kernel.py`.
