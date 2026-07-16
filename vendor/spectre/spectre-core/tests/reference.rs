//! Validation against the reference generator (shrx/spectre, the port of the
//! official SMKGS algorithm). The CSV was produced by an exact-arithmetic
//! Python port that was itself verified transform-by-transform against the
//! float reference for N=1..3 and roots Delta/Gamma/Psi.
use spectre_core::{tables, Aabb, Label, Tiling};

const REF: &str = include_str!("ref_leaves_n3_delta.csv");

#[test]
fn matches_reference_leaves_n3_delta() {
    // reference multiset: (s, r, x/8 rounded, y/8 rounded, is_gamma2)
    let mut expected: Vec<(u8, u8, i64, i64, bool)> = REF
        .lines()
        .map(|l| {
            let mut it = l.split(',');
            let label = it.next().unwrap();
            let s: u8 = it.next().unwrap().parse().unwrap();
            let r: u8 = it.next().unwrap().parse().unwrap();
            let x: f64 = it.next().unwrap().parse().unwrap();
            let y: f64 = it.next().unwrap().parse().unwrap();
            (s, r, (x * 8.0).round() as i64, (y * 8.0).round() as i64, label == "Gamma2")
        })
        .collect();
    expected.sort_unstable();

    let t = Tiling::new(Label::Delta, 3);
    let huge = Aabb::new(-1e9, -1e9, 1e9, 1e9);
    let mut got: Vec<(u8, u8, i64, i64, bool)> = Vec::new();
    t.for_each_in(&huge, (0.0, 0.0), |kind, s, r, x, y| {
        got.push((s, r, (x * 8.0).round() as i64, (y * 8.0).round() as i64, kind == 1));
    });
    got.sort_unstable();

    assert_eq!(expected.len(), 559);
    assert_eq!(expected, got);
}

#[test]
fn counts_match_substitution_recurrence() {
    let huge = Aabb::new(-1e12, -1e12, 1e12, 1e12);
    for lvl in 0..=6 {
        let t = Tiling::new(Label::Delta, lvl);
        assert_eq!(t.count_in(&huge) as u128, tables::TILE_COUNTS[lvl], "level {lvl}");
    }
}

#[test]
fn viewport_culling_is_consistent() {
    // every tile reported for a small viewport must also appear in the full
    // enumeration at the same coordinates, and the sets must agree with a
    // brute-force filter.
    let t = Tiling::new(Label::Delta, 5);
    let b = t.bounds();
    let (cx, cy) = ((b.min_x + b.max_x) / 2.0, (b.min_y + b.max_y) / 2.0);
    let vp = Aabb::new(cx - 15.0, cy - 15.0, cx + 15.0, cy + 15.0);

    let mut small: Vec<(u32, i64, i64)> = Vec::new();
    t.for_each_in(&vp, (0.0, 0.0), |k, s, r, x, y| {
        small.push(((k as u32) << 8 | (s as u32) << 4 | r as u32, (x * 8.0).round() as i64, (y * 8.0).round() as i64));
    });
    small.sort_unstable();

    let huge = Aabb::new(-1e12, -1e12, 1e12, 1e12);
    let mut brute: Vec<(u32, i64, i64)> = Vec::new();
    t.for_each_in(&huge, (0.0, 0.0), |k, s, r, x, y| {
        let bb = t.leaf_vertices(s, r);
        let (mut nx, mut ny, mut mx, mut my) = (f64::MAX, f64::MAX, f64::MIN, f64::MIN);
        for (vx, vy) in bb {
            nx = nx.min(x + *vx as f64);
            ny = ny.min(y + *vy as f64);
            mx = mx.max(x + *vx as f64);
            my = my.max(y + *vy as f64);
        }
        if mx >= vp.min_x && nx <= vp.max_x && my >= vp.min_y && ny <= vp.max_y {
            brute.push(((k as u32) << 8 | (s as u32) << 4 | r as u32, (x * 8.0).round() as i64, (y * 8.0).round() as i64));
        }
    });
    brute.sort_unstable();
    assert_eq!(small, brute);
    assert!(!small.is_empty());
}

#[test]
fn parallel_matches_serial() {
    let t = Tiling::new(Label::Delta, 6);
    let b = t.bounds();
    let vp = Aabb::new(b.min_x, b.min_y, b.max_x, b.max_y);
    let mut a = Vec::new();
    let mut p = Vec::new();
    t.instances_in(&vp, (0.0, 0.0), &mut a);
    t.instances_in_parallel(&vp, (0.0, 0.0), &mut p, 8);
    let key = |i: &spectre_core::Instance| (i.meta, i.x.to_bits(), i.y.to_bits());
    let mut ka: Vec<_> = a.iter().map(key).collect();
    let mut kp: Vec<_> = p.iter().map(key).collect();
    ka.sort_unstable();
    kp.sort_unstable();
    assert_eq!(ka, kp);
}

#[test]
fn ids_match_projected_enumeration_and_pick_roundtrips() {
    let t = Tiling::new(Label::Delta, 3);
    let huge = Aabb::new(-1e9, -1e9, 1e9, 1e9);

    let mut proj: Vec<(u8, u8, u8, i64, i64)> = Vec::new();
    t.for_each_in(&huge, (0.0, 0.0), |k, s, r, x, y| {
        proj.push((k, s, r, (x * 8.0).round() as i64, (y * 8.0).round() as i64));
    });
    proj.sort_unstable();

    let mut ids: Vec<(u8, u8, u8, i64, i64)> = Vec::new();
    let mut centroids: Vec<(spectre_core::TileId, f64, f64)> = Vec::new();
    t.for_each_ids_in(&huge, |id| {
        let (x, y) = id.anchor();
        ids.push((id.kind, id.s, id.r, (x * 8.0).round() as i64, (y * 8.0).round() as i64));
        let verts = t.leaf_vertices(id.s, id.r);
        let (mut cx, mut cy) = (0.0, 0.0);
        for (vx, vy) in verts {
            cx += *vx as f64 / 14.0;
            cy += *vy as f64 / 14.0;
        }
        centroids.push((id, x + cx, y + cy));
    });
    ids.sort_unstable();
    assert_eq!(proj, ids);

    // the spectre is star-shaped enough that the vertex centroid is interior
    for (id, cx, cy) in centroids {
        assert_eq!(t.pick(cx, cy), Some(id));
    }
}
