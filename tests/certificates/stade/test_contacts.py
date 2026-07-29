from einstein.tilings.stade.contacts import (
    DIRECTIONS,
    analyze_length,
    fixed_forbidden,
    physical_contact,
    polygonal_physical_contact,
    rotate,
    stick_ports,
)


def test_stick_port_reconstruction_matches_source_boundary_counts():
    for n in (5, 6, 12):
        ports = stick_ports(n)
        assert len(ports) == 4 * n + 2
        by_label = {port.label: port for port in ports}
        assert (by_label["z1"].cell, by_label["z1"].direction) == (n - 1, 1)
        assert (by_label["a1"].cell, by_label["a1"].direction) == (n - 1, 2)
        assert (by_label[f"b{n-1}"].cell, by_label[f"b{n-1}"].direction) == (0, 1)
        assert (by_label["x2"].cell, by_label["x2"].direction) == (0, 2)
        assert (by_label["z2"].cell, by_label["z2"].direction) == (0, 4)
        assert (by_label["x1"].cell, by_label["x1"].direction) == (n - 1, 5)


def test_axial_rotation_cycles_the_six_outward_normals():
    for index, direction in enumerate(DIRECTIONS):
        assert rotate(direction, 1) == DIRECTIONS[(index + 1) % 6]
        assert rotate(direction, 6) == direction


def test_fixed_rule_anchor_and_physical_placement_controls():
    n = 6
    ports = {port.label: port for port in stick_ports(n)}
    assert fixed_forbidden(n, "z1", "b1")
    assert not fixed_forbidden(n, "z1", "a2")
    assert not fixed_forbidden(n, "a1", "a2")
    assert not fixed_forbidden(n, "a1", "b1")
    # A stick can stack against the matching sawtooth side without overlap.
    assert physical_contact(n, ports["a1"], ports["c1"])


def test_axial_and_polygonal_contact_tests_agree_on_controls():
    n = 6
    ports = {port.label: port for port in stick_ports(n)}
    for left, right in (
        ("b1", "b3"),
        ("b1", "x1"),
        ("d1", "z1"),
        ("z1", "a4"),
        ("a1", "b1"),
    ):
        assert physical_contact(n, ports[left], ports[right]) == (
            polygonal_physical_contact(n, ports[left], ports[right])
        )


def _later_forbidden_family(left: str, right: str) -> bool:
    labels = {left, right}
    kinds = {left[0], right[0]}
    return (
        kinds == {"a", "y"}
        or kinds == {"c", "y"}
        or ("x1" in labels and "a" in kinds)
        or ("z2" in labels and "b" in kinds)
    )


def test_fixed_allowed_graph_stays_connected_after_all_later_family_deletions():
    for n in (5, 8, 12):
        result = analyze_length(n)
        labels = [port.label for port in stick_ports(n)]
        adjacency = {f"{side}:{label}": set() for side in ("L", "R") for label in labels}
        for left, right in result["allowed_physical_pairs"]:
            if _later_forbidden_family(left, right):
                continue
            adjacency[f"L:{left}"].add(f"R:{right}")
            adjacency[f"R:{right}"].add(f"L:{left}")
        seen = {"L:b1"}
        frontier = ["L:b1"]
        while frontier:
            current = frontier.pop()
            for neighbor in adjacency[current] - seen:
                seen.add(neighbor)
                frontier.append(neighbor)
        assert seen == set(adjacency)


def test_symbolic_spanning_contact_families_are_stable_controls():
    for n in range(5, 21):
        ports = {port.label: port for port in stick_ports(n)}
        pairs = []
        for index in range(1, n):
            pairs.extend(
                (
                    ("b1", f"b{index}"),
                    ("b1", f"d{index}"),
                    ("x2", f"c{index}"),
                    ("z1", f"a{index}"),
                )
            )
        pairs.extend(
            (
                ("b1", "x1"),
                ("b1", "x2"),
                ("b1", "y1"),
                ("b1", "y2"),
                ("d1", "z1"),
                (f"d{n-1}", "z2"),
            )
        )
        for left, right in pairs:
            assert physical_contact(n, ports[left], ports[right])
            assert not fixed_forbidden(n, left, right)
            assert not _later_forbidden_family(left, right)
