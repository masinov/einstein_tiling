"""Exact Cayley-diagram controls and first definitions for W2 Layer D."""

from __future__ import annotations

from collections import deque
from fractions import Fraction
import itertools

from einstein.geometry.kite_grid import (
    N_OPS,
    boundary_cycle,
    shoelace2,
    transform_cell,
)


Eisenstein = tuple[Fraction, Fraction]
Affine = tuple[int, tuple[int, int]]


def _zeta_mul(value, power):
    """Multiply ``a+b*zeta`` by zeta**power, with zeta^2+zeta+1=0."""
    a, b = value
    power %= 3
    if power == 0:
        return a, b
    if power == 1:
        return -b, a - b
    return b - a, -a


def _add(left, right):
    return left[0] + right[0], left[1] + right[1]


def _neg(value):
    return -value[0], -value[1]


def affine_compose(left: Affine, right: Affine) -> Affine:
    """Composition ``left after right`` in the p3 affine group."""
    rotation = (left[0] + right[0]) % 3
    shifted = _zeta_mul(right[1], left[0])
    translation = _add(left[1], shifted)
    return rotation, (int(translation[0]), int(translation[1]))


def affine_inverse(value: Affine) -> Affine:
    rotation = (-value[0]) % 3
    translation = _neg(_zeta_mul(value[1], rotation))
    return rotation, (int(translation[0]), int(translation[1]))


def affine_apply(value: Affine, point: Eisenstein) -> Eisenstein:
    return _add(_zeta_mul(point, value[0]), value[1])


IDENTITY: Affine = (0, (0, 0))
A: Affine = (1, (0, 0))
U: Affine = (2, (2, 1))
GENERATORS = {
    "A": A,
    "a": affine_inverse(A),
    "U": U,
    "u": affine_inverse(U),
}


def free_reduce(word: str) -> str:
    inverse = {"A": "a", "a": "A", "U": "u", "u": "U"}
    stack = []
    for letter in word:
        if letter not in inverse:
            raise ValueError(f"unknown free-group letter: {letter}")
        if stack and stack[-1] == inverse[letter]:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def p3_value(word: str) -> Affine:
    """Image of a conventional left-to-right free-group word in p3."""
    value = IDENTITY
    for letter in word:
        value = affine_compose(value, GENERATORS[letter])
    return value


def _cayley_path(word: str) -> tuple[Eisenstein, ...]:
    """Paper convention: read the word right-to-left using left multiplication."""
    base = (Fraction(1, 2), Fraction(0))
    value = IDENTITY
    vertices = [base]
    for letter in reversed(word):
        value = affine_compose(GENERATORS[letter], value)
        vertices.append(affine_apply(affine_inverse(value), base))
    return tuple(vertices)


def _orientation(a, b, point):
    # Determinants in the (1,zeta) basis have the same sign as Cartesian
    # determinants because Im(zeta)>0.
    return (
        (b[0] - a[0]) * (point[1] - a[1])
        - (b[1] - a[1]) * (point[0] - a[0])
    )


def winding_number(path, point) -> int:
    """Exact winding number of a closed Eisenstein-coordinate polygonal path."""
    if path[0] != path[-1]:
        raise ValueError("winding requires a closed path")
    winding = 0
    for start, end in zip(path, path[1:]):
        side = _orientation(start, end, point)
        if side == 0 and min(start[0], end[0]) <= point[0] <= max(start[0], end[0]) and min(start[1], end[1]) <= point[1] <= max(start[1], end[1]):
            raise ValueError("point lies on path")
        if start[1] <= point[1] < end[1] and side > 0:
            winding += 1
        elif end[1] <= point[1] < start[1] and side < 0:
            winding -= 1
    return winding


def _u_face_centers(depth: int):
    """Enumerate U-labelled triangle centers in a Cayley ball."""
    seen = {IDENTITY}
    queue = deque([(IDENTITY, 0)])
    centers = set()
    center = (Fraction(1), Fraction(0))
    while queue:
        value, distance = queue.popleft()
        centers.add(affine_apply(affine_inverse(value), center))
        if distance == depth:
            continue
        for generator in GENERATORS.values():
            neighbor = affine_compose(generator, value)
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))
    return centers


def u_triangle_winding(word: str) -> int:
    """Conway--Lagarias phi: total winding about U-labelled triangles."""
    if p3_value(word) != IDENTITY:
        raise ValueError("word is not in the subgroup H")
    path = _cayley_path(word)
    lo0, hi0 = min(p[0] for p in path), max(p[0] for p in path)
    lo1, hi1 = min(p[1] for p in path), max(p[1] for p in path)
    # A Cayley radius linear in word length contains every face whose center
    # can lie in the path's bounding box. The explicit box check discards the
    # remaining enumerated faces.
    centers = _u_face_centers(len(word) + 6)
    relevant = [
        center for center in centers
        if lo0 <= center[0] <= hi0 and lo1 <= center[1] <= hi1
    ]
    # Our affine realization uses the mirror of Figure 3.3; reverse the
    # orientation so the paper's counterclockwise convention is positive.
    return -sum(winding_number(path, center) for center in relevant)


def staircase_boundary_word(index: int) -> str:
    """Equation (3.1): boundary of the square-lattice staircase T_N."""
    if index < 0:
        raise ValueError("index must be nonnegative")
    return "A" * index + "u" * index + "aU" * index


def line_tile_boundary_words() -> tuple[str, str, str]:
    """The three translation-inequivalent L3 boundaries from Figure 3.2(b)."""
    return (
        "AAA" + "u" + "aaa" + "U",
        "A" + "uuu" + "a" + "UUU",
        "AuAuAu" + "aUaUaU",
    )


# Six unoriented directions in the deltoidal-trihexagonal edge skeleton.
KITE_EDGE_GENERATORS = (
    (0, 1),
    (1, 0),
    (1, -1),
    (1, 1),
    (1, -2),
    (2, -1),
)
_KITE_EDGE_LETTER = {
    vector: index + 1
    for index, vector in enumerate(KITE_EDGE_GENERATORS)
} | {
    (-vector[0], -vector[1]): -(index + 1)
    for index, vector in enumerate(KITE_EDGE_GENERATORS)
}


def free_reduce_signed(word):
    stack = []
    for letter in word:
        if not 1 <= abs(letter) <= len(KITE_EDGE_GENERATORS):
            raise ValueError(f"unknown signed generator: {letter}")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def polykite_boundary_word(shape) -> tuple[int, ...]:
    """Counterclockwise free-direction word of a disk-like polykite."""
    cycle = boundary_cycle(shape)
    if shoelace2(cycle) < 0:
        cycle = [cycle[0], *reversed(cycle[1:])]
    word = []
    for start, end in zip(cycle, cycle[1:] + cycle[:1]):
        vector = end[0] - start[0], end[1] - start[1]
        try:
            word.append(_KITE_EDGE_LETTER[vector])
        except KeyError as error:
            raise ValueError(f"non-kite boundary edge {vector}") from error
    return free_reduce_signed(word)


def polykite_boundary_relators(shape) -> tuple[tuple[int, ...], ...]:
    """Distinct free-group relators for every allowed D6 pose."""
    shape = tuple(tuple(cell) for cell in shape)
    return tuple(sorted({
        polykite_boundary_word(tuple(transform_cell(cell, op) for cell in shape))
        for op in range(N_OPS)
    }))


S3 = tuple(itertools.permutations(range(3)))
S3_IDENTITY = (0, 1, 2)


def _perm_compose(left, right):
    return tuple(left[right[index]] for index in range(3))


def _perm_inverse(value):
    out = [0] * 3
    for index, image in enumerate(value):
        out[image] = index
    return tuple(out)


def _permutation_word_value(word, images):
    value = S3_IDENTITY
    for letter in word:
        image = images[abs(letter) - 1]
        if letter < 0:
            image = _perm_inverse(image)
        value = _perm_compose(value, image)
    return value


def _generated_permutations(images):
    subgroup = {S3_IDENTITY}
    frontier = [S3_IDENTITY]
    generators = tuple(images) + tuple(_perm_inverse(value) for value in images)
    while frontier:
        value = frontier.pop()
        for generator in generators:
            product = _perm_compose(value, generator)
            if product not in subgroup:
                subgroup.add(product)
                frontier.append(product)
    return subgroup


def verify_s3_boundary_quotient(shape, images, require_surjective=False) -> bool:
    """Check a six-generator S3 map against every allowed tile relator."""
    images = tuple(tuple(image) for image in images)
    if len(images) != len(KITE_EDGE_GENERATORS) or any(
        image not in S3 for image in images
    ):
        return False
    if any(
        _permutation_word_value(relator, images) != S3_IDENTITY
        for relator in polykite_boundary_relators(shape)
    ):
        return False
    return not require_surjective or len(_generated_permutations(images)) == len(S3)


def _conjugate_s3_images(images, conjugator):
    inverse = _perm_inverse(conjugator)
    return tuple(
        _perm_compose(_perm_compose(conjugator, image), inverse)
        for image in images
    )


def s3_boundary_surjections(
    shape,
    displacement_kernel_order=None,
    conjugacy_reduced=True,
):
    """Enumerate verified S3 surjections, optionally modulo inner conjugacy."""
    relators = polykite_boundary_relators(shape)
    representatives = {}
    for images in itertools.product(S3, repeat=len(KITE_EDGE_GENERATORS)):
        if any(
            _permutation_word_value(relator, images) != S3_IDENTITY
            for relator in relators
        ):
            continue
        if len(_generated_permutations(images)) != len(S3):
            continue
        if (
            displacement_kernel_order is not None
            and len(s3_displacement_kernel(images)) != displacement_kernel_order
        ):
            continue
        if conjugacy_reduced:
            orbit = tuple(_conjugate_s3_images(images, value) for value in S3)
            representative = min(orbit)
        else:
            representative = images
        representatives[representative] = None
    return tuple(sorted(representatives))


def s3_displacement_kernel(images):
    """Image of zero-displacement free words in an S3 boundary quotient.

    The kernel of F6 -> Z2 is normally generated by the commutator of the two
    coordinate steps and by expressing every other edge direction in those
    coordinates. We take the normal closure of their S3 images.
    """
    loops = [(2, 1, -2, -1)]
    for index, (x, y) in enumerate(KITE_EDGE_GENERATORS, 1):
        loop = [index]
        loop.extend([-2] * x if x >= 0 else [2] * -x)
        loop.extend([-1] * y if y >= 0 else [1] * -y)
        loops.append(tuple(loop))
    subgroup = {S3_IDENTITY}
    seeds = {_permutation_word_value(loop, images) for loop in loops}
    generators = tuple(images) + tuple(_perm_inverse(value) for value in images)
    changed = True
    while changed:
        changed = False
        pool = tuple(subgroup | seeds)
        candidates = set(pool)
        for left in pool:
            candidates.add(_perm_inverse(left))
            for right in pool:
                candidates.add(_perm_compose(left, right))
            for generator in generators:
                candidates.add(_perm_compose(
                    _perm_compose(generator, left), _perm_inverse(generator)
                ))
        if not candidates <= subgroup:
            subgroup.update(candidates)
            changed = True
    return frozenset(subgroup)


def s3_cosets_all_admit_commuting_pairs(kernel) -> bool:
    """Whether every ordered pair of cosets has commuting representatives."""
    unseen = set(S3)
    cosets = []
    while unseen:
        representative = next(iter(unseen))
        coset = frozenset(_perm_compose(representative, value) for value in kernel)
        cosets.append(coset)
        unseen.difference_update(coset)
    for left in cosets:
        for right in cosets:
            if not any(
                _perm_compose(a, b) == _perm_compose(b, a)
                for a in left for b in right
            ):
                return False
    return True


def s3_boundary_quotients(shape, keep=12) -> dict:
    """Enumerate homomorphisms of the tile-boundary presentation into S3."""
    relators = polykite_boundary_relators(shape)
    homomorphisms = surjections = 0
    displacement_kernel_orders = {}
    displacement_coset_obstructions = 0
    samples = []
    samples_by_kernel = {}
    for images in itertools.product(S3, repeat=len(KITE_EDGE_GENERATORS)):
        if any(
            _permutation_word_value(relator, images) != S3_IDENTITY
            for relator in relators
        ):
            continue
        homomorphisms += 1
        image_order = len(_generated_permutations(images))
        if image_order == 6:
            surjections += 1
            kernel = s3_displacement_kernel(images)
            kernel_order = len(kernel)
            displacement_kernel_orders[str(kernel_order)] = (
                displacement_kernel_orders.get(str(kernel_order), 0) + 1
            )
            if not s3_cosets_all_admit_commuting_pairs(kernel):
                displacement_coset_obstructions += 1
            if len(samples) < keep:
                samples.append([list(image) for image in images])
            samples_by_kernel.setdefault(str(kernel_order), [
                list(image) for image in images
            ])
    return {
        "target": "S3",
        "generators": len(KITE_EDGE_GENERATORS),
        "relators": [list(relator) for relator in relators],
        "homomorphisms": homomorphisms,
        "surjections": surjections,
        "surjective_displacement_kernel_orders": displacement_kernel_orders,
        "surjections_with_displacement_coset_obstruction": (
            displacement_coset_obstructions
        ),
        "sample_surjections": samples,
        "sample_surjections_by_displacement_kernel": samples_by_kernel,
    }


def kite_edge_letter(start, end) -> int:
    """Signed free-group generator for one oriented kite-skeleton edge."""
    vector = end[0] - start[0], end[1] - start[1]
    try:
        return _KITE_EDGE_LETTER[vector]
    except KeyError as error:
        raise ValueError(f"non-kite edge {vector}") from error
