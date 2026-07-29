"""Random square--triangle tilings for the E4 diffuse-order control.

This implements the local boundary-growth construction of Koga, Sakai,
Matsushita and Ishimasa (Phys. Rev. B 110, 094208, 2024).  Boundary gaps of
60, 90, 120 and 150 degrees are filled by a triangle, square, two triangles,
or an adjacent square--triangle pair.  At a 150-degree gap the pair order is
random; ``mixing`` biases the choice against extending like-tile domains.
It is a domain-suppression analogue, not a claim to reproduce the paper's
history-conditioned parameter p numerically.

The published construction discards rare self-intersecting growth histories
and repeatedly crops an interior disk to remove initial/boundary dependence.
Here proposed tiles are collision-checked up front, and the returned vertex
set is clipped inside the nearest boundary radius after a short bootstrap.

Primary construction:
  https://arxiv.org/abs/2409.16509
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random

import numpy as np


Point = tuple[float, float]
Polygon = tuple[Point, ...]
_TAU = 2.0 * math.pi
_STEP = math.pi / 6.0
_EPS = 1e-8


def _point(x: float, y: float) -> Point:
    return round(x, 10), round(y, 10)


def _unit(step: int) -> Point:
    angle = (step % 12) * _STEP
    return _point(math.cos(angle), math.sin(angle))


def _add(a: Point, b: Point) -> Point:
    return _point(a[0] + b[0], a[1] + b[1])


def _sub(a: Point, b: Point) -> Point:
    return _point(a[0] - b[0], a[1] - b[1])


def _direction_step(vector: Point) -> int:
    angle = math.atan2(vector[1], vector[0]) % _TAU
    return int(round(angle / _STEP)) % 12


def _polygon_edges(polygon: Polygon):
    return zip(polygon, polygon[1:] + polygon[:1])


def _strict_convex_overlap(a: Polygon, b: Polygon) -> bool:
    """Whether two convex polygons have overlapping interiors."""
    for polygon in (a, b):
        for p, q in _polygon_edges(polygon):
            edge = _sub(q, p)
            axis = (-edge[1], edge[0])
            pa = [x * axis[0] + y * axis[1] for x, y in a]
            pb = [x * axis[0] + y * axis[1] for x, y in b]
            if min(max(pa), max(pb)) - max(min(pa), min(pb)) <= _EPS:
                return False
    return True


def _tile_across_edge(a: Point, b: Point, sides: int) -> Polygon:
    """Regular CCW tile on the right of the oriented boundary edge a->b."""
    vertices = [b, a]
    edge = _sub(a, b)
    turn = _TAU / sides
    for _ in range(sides - 2):
        angle = math.atan2(edge[1], edge[0]) + turn
        edge = _point(math.cos(angle), math.sin(angle))
        vertices.append(_add(vertices[-1], edge))
    return tuple(vertices)


def _fan_tile(center: Point, start_step: int, sector_steps: int) -> Polygon:
    first = _add(center, _unit(start_step))
    last = _add(center, _unit(start_step + sector_steps))
    if sector_steps == 2:
        return center, first, last
    if sector_steps == 3:
        outer = _add(first, _unit(start_step + sector_steps))
        return center, first, outer, last
    raise ValueError(f"not a square/triangle sector: {sector_steps}")


@dataclass(frozen=True)
class SquareTrianglePatch:
    points: tuple[Point, ...]
    polygons: tuple[Polygon, ...]
    tile_types: tuple[int, ...]
    crop_center: Point
    crop_radius: float
    rejected_moves: int


class _Growth:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        h = math.sqrt(3.0) / 2.0
        self.polygons: list[Polygon] = [
            (_point(-0.5, -h / 3.0),
             _point(0.5, -h / 3.0),
             _point(0.0, 2.0 * h / 3.0))
        ]
        self.types = [3]
        self.edge_tiles: dict[tuple[Point, Point], list[int]] = {}
        self.spatial: dict[tuple[int, int], set[int]] = {}
        self.rejected = 0
        self._index_tile(0)

    @staticmethod
    def _edge_key(a: Point, b: Point):
        return (a, b) if a < b else (b, a)

    @staticmethod
    def _cells(polygon: Polygon):
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        for i in range(math.floor(min(xs)), math.floor(max(xs)) + 1):
            for j in range(math.floor(min(ys)), math.floor(max(ys)) + 1):
                yield i, j

    def _index_tile(self, index: int):
        polygon = self.polygons[index]
        for a, b in _polygon_edges(polygon):
            self.edge_tiles.setdefault(self._edge_key(a, b), []).append(index)
        for cell in self._cells(polygon):
            self.spatial.setdefault(cell, set()).add(index)

    def _boundary(self):
        oriented = []
        edge_type = {}
        for index, polygon in enumerate(self.polygons):
            for a, b in _polygon_edges(polygon):
                if len(self.edge_tiles[self._edge_key(a, b)]) == 1:
                    oriented.append((a, b))
                    edge_type[(a, b)] = self.types[index]
        return oriented, edge_type

    def _can_add(self, proposed: list[Polygon]) -> bool:
        for i, polygon in enumerate(proposed):
            nearby = set()
            for cell in self._cells(polygon):
                nearby.update(self.spatial.get(cell, ()))
            if any(_strict_convex_overlap(polygon, self.polygons[j])
                   for j in nearby):
                return False
            if any(_strict_convex_overlap(polygon, other)
                   for other in proposed[:i]):
                return False
            for a, b in _polygon_edges(polygon):
                if len(self.edge_tiles.get(self._edge_key(a, b), ())) >= 2:
                    return False
        return True

    def _add(self, proposed: list[Polygon], types: list[int]) -> bool:
        if not self._can_add(proposed):
            self.rejected += 1
            return False
        for polygon, tile_type in zip(proposed, types):
            index = len(self.polygons)
            self.polygons.append(polygon)
            self.types.append(tile_type)
            self._index_tile(index)
        return True

    def bootstrap(self, target: int = 80):
        """Create a compact seed; the published local rule then takes over."""
        while len(self.polygons) < target:
            boundary, _ = self._boundary()
            moves = []
            for edge in boundary:
                radius = math.hypot(
                    (edge[0][0] + edge[1][0]) / 2.0,
                    (edge[0][1] + edge[1][1]) / 2.0,
                )
                for sides in (3, 4):
                    polygon = _tile_across_edge(*edge, sides)
                    if self._can_add([polygon]):
                        moves.append((radius, self.rng.random(),
                                      polygon, sides))
            if not moves:
                raise RuntimeError("could not bootstrap square-triangle patch")
            moves.sort()
            _, _, polygon, sides = self.rng.choice(
                moves[:max(1, len(moves) // 5)]
            )
            self._add([polygon], [sides])

    def attach_boundary_tile(self) -> bool:
        boundary, _ = self._boundary()
        moves = []
        for edge in boundary:
            radius = math.hypot(
                (edge[0][0] + edge[1][0]) / 2.0,
                (edge[0][1] + edge[1][1]) / 2.0,
            )
            for sides in (3, 4):
                polygon = _tile_across_edge(*edge, sides)
                if self._can_add([polygon]):
                    moves.append((radius, self.rng.random(), polygon, sides))
        if not moves:
            return False
        moves.sort()
        _, _, polygon, sides = self.rng.choice(
            moves[:max(1, len(moves) // 10)]
        )
        return self._add([polygon], [sides])

    def fill_nearest_gap(self, mixing: float) -> bool:
        boundary, edge_type = self._boundary()
        incoming: dict[Point, list[Point]] = {}
        outgoing: dict[Point, list[Point]] = {}
        for a, b in boundary:
            outgoing.setdefault(a, []).append(b)
            incoming.setdefault(b, []).append(a)

        candidates = []
        for center in incoming.keys() & outgoing.keys():
            if len(incoming[center]) != 1 or len(outgoing[center]) != 1:
                continue
            before = incoming[center][0]
            after = outgoing[center][0]
            start = _direction_step(_sub(before, center))
            end = _direction_step(_sub(after, center))
            gap = (end - start) % 12
            if gap in (2, 3, 4, 5):
                candidates.append((
                    math.hypot(*center), self.rng.random(),
                    center, before, after, start, gap,
                ))
        if not candidates:
            return False

        for _, _, center, before, after, start, gap in sorted(candidates):
            if gap == 2:
                sector_orders = [[2]]
            elif gap == 3:
                sector_orders = [[3]]
            elif gap == 4:
                sector_orders = [[2, 2]]
            else:
                orders = ([2, 3], [3, 2])
                left_type = edge_type[(before, center)]
                right_type = edge_type[(center, after)]
                scores = [
                    int(order[0] + 1 == left_type)
                    + int(order[1] + 1 == right_type)
                    for order in orders
                ]
                if scores[0] == scores[1]:
                    first = self.rng.randrange(2)
                else:
                    preferred = scores.index(min(scores))
                    first = (
                        preferred if self.rng.random() < mixing
                        else 1 - preferred
                    )
                sector_orders = [list(orders[first]), list(orders[1 - first])]

            for sectors in sector_orders:
                proposed = []
                tile_types = []
                step = start
                for sector in sectors:
                    proposed.append(_fan_tile(center, step, sector))
                    tile_types.append(sector + 1)
                    step += sector
                if self._can_add(proposed):
                    return self._add(proposed, tile_types)
        return False


def random_square_triangle_patch(
    seed: int,
    target_tiles: int = 12_000,
    mixing: float = 0.75,
    bootstrap_tiles: int = 80,
    crop_fraction: float = 0.80,
) -> SquareTrianglePatch:
    """Grow a random tiling and return its safely cropped interior vertices."""
    if not 0.0 <= mixing <= 1.0:
        raise ValueError("mixing must lie in [0, 1]")
    growth = _Growth(seed)
    growth.bootstrap(bootstrap_tiles)
    stalled = 0
    while len(growth.polygons) < target_tiles and stalled < 2_000:
        if growth.fill_nearest_gap(mixing):
            stalled = 0
        else:
            stalled += 1
            if growth.attach_boundary_tile():
                stalled = 0
    if len(growth.polygons) < target_tiles:
        raise RuntimeError(
            f"square-triangle growth stalled at {len(growth.polygons)} tiles"
        )

    boundary, _ = growth._boundary()
    segments = np.asarray(boundary, dtype=np.float64)
    candidates = np.asarray([
        (
            sum(p[0] for p in polygon) / len(polygon),
            sum(p[1] for p in polygon) / len(polygon),
        )
        for polygon in growth.polygons
    ])
    if len(candidates) > 2_000:
        indices = np.linspace(0, len(candidates) - 1, 2_000, dtype=int)
        candidates = candidates[indices]
    starts = segments[:, 0]
    vectors = segments[:, 1] - starts
    lengths2 = np.sum(vectors * vectors, axis=1)
    best_center = None
    safe_radius = -1.0
    for candidate in candidates:
        factors = np.clip(
            np.sum((candidate - starts) * vectors, axis=1) / lengths2,
            0.0, 1.0,
        )
        nearest = starts + factors[:, None] * vectors
        distance = float(np.linalg.norm(nearest - candidate, axis=1).min())
        if distance > safe_radius:
            best_center = candidate
            safe_radius = distance
    center = _point(float(best_center[0]), float(best_center[1]))
    crop_radius = crop_fraction * safe_radius
    all_points = {p for polygon in growth.polygons for p in polygon}
    points = tuple(sorted(
        _sub(p, center) for p in all_points
        if math.hypot(p[0] - center[0], p[1] - center[1]) <= crop_radius
    ))
    return SquareTrianglePatch(
        points=points,
        polygons=tuple(growth.polygons),
        tile_types=tuple(growth.types),
        crop_center=center,
        crop_radius=crop_radius,
        rejected_moves=growth.rejected,
    )


def random_square_triangle_points(seed: int, **kwargs):
    return random_square_triangle_patch(seed, **kwargs).points
