"""Generic finite-target boundary quotient enumeration for W2.D."""

from __future__ import annotations

import itertools

from einstein.theory.holonomy import KITE_EDGE_GENERATORS, polykite_boundary_relators
from einstein.theory.holonomy_symmetry import (
    inverse_d6_operation,
    signed_edge_action,
)


def word_value(word, images, group):
    value = group.identity
    for letter in word:
        image = images[abs(letter) - 1]
        if letter < 0:
            image = group.inverses[image]
        value = group.multiplication[value][image]
    return value


def generated_subgroup(images, group):
    subgroup = {group.identity}
    frontier = [group.identity]
    generators = tuple(images) + tuple(group.inverses[value] for value in images)
    while frontier:
        value = frontier.pop()
        for generator in generators:
            product = group.multiplication[value][generator]
            if product not in subgroup:
                subgroup.add(product)
                frontier.append(product)
    return frozenset(subgroup)


def displacement_kernel(images, group):
    """Normal closure of zero-displacement loop images in a finite target."""
    loops = [(2, 1, -2, -1)]
    for index, (x, y) in enumerate(KITE_EDGE_GENERATORS, 1):
        loop = [index]
        loop.extend([-2] * x if x >= 0 else [2] * -x)
        loop.extend([-1] * y if y >= 0 else [1] * -y)
        loops.append(tuple(loop))
    seeds = {word_value(loop, images, group) for loop in loops}
    subgroup = {group.identity}
    changed = True
    while changed:
        changed = False
        pool = tuple(subgroup | seeds)
        candidates = set(pool)
        for value in pool:
            candidates.add(group.inverses[value])
            for other in pool:
                candidates.add(group.multiplication[value][other])
            for conjugator in range(group.order):
                candidates.add(group.conjugate(value, conjugator))
        if not candidates <= subgroup:
            subgroup.update(candidates)
            changed = True
    return frozenset(subgroup)


def canonical_inner_class(images, group):
    return min(tuple(
        group.conjugate(image, conjugator) for image in images
    ) for conjugator in range(group.order))


def pullback_images(images, op, group):
    """Contravariantly transport a finite-group edge map under D6."""
    out = []
    for letter in signed_edge_action(inverse_d6_operation(op)):
        image = images[abs(letter) - 1]
        out.append(image if letter > 0 else group.inverses[image])
    return canonical_inner_class(tuple(out), group)


def boundary_quotient_census(shape, group, keep_representatives=True):
    """Exhaust all six-generator maps into one small exact finite group."""
    relators = polykite_boundary_relators(shape)
    multiplication = group.multiplication
    inverses = group.inverses
    compiled = tuple(tuple(
        (abs(letter) - 1, letter < 0) for letter in word
    ) for word in relators)
    homomorphisms = 0
    surjections = 0
    raw_kernel_orders = {}
    representatives = {}
    for images in itertools.product(range(group.order), repeat=6):
        valid = True
        for word in compiled:
            value = group.identity
            for generator, negative in word:
                image = images[generator]
                if negative:
                    image = inverses[image]
                value = multiplication[value][image]
            if value != group.identity:
                valid = False
                break
        if not valid:
            continue
        homomorphisms += 1
        if len(generated_subgroup(images, group)) != group.order:
            continue
        surjections += 1
        kernel_order = len(displacement_kernel(images, group))
        raw_kernel_orders[kernel_order] = raw_kernel_orders.get(kernel_order, 0) + 1
        if keep_representatives:
            representative = canonical_inner_class(images, group)
            representatives[(kernel_order, representative)] = None
    by_kernel = {}
    for kernel_order, representative in representatives:
        by_kernel.setdefault(kernel_order, []).append(representative)
    return {
        "target": group.name,
        "order": group.order,
        "homomorphisms": homomorphisms,
        "surjections": surjections,
        "surjective_displacement_kernel_orders": {
            str(order): count for order, count in sorted(raw_kernel_orders.items())
        },
        "inner_conjugacy_classes_by_kernel": {
            str(order): len(values) for order, values in sorted(by_kernel.items())
        },
        "representatives_by_kernel": {
            str(order): [list(images) for images in sorted(values)]
            for order, values in sorted(by_kernel.items())
        },
    }
