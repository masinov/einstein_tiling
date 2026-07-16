//! Export a viewport of the tiling as SVG.
//! Usage: cargo run --release --bin svg -- [level] [size] [out.svg]
use spectre_core::{Aabb, Label, Tiling, LABEL_NAMES};
use std::fmt::Write as _;

fn main() {
    let mut args = std::env::args().skip(1);
    let level: usize = args.next().and_then(|s| s.parse().ok()).unwrap_or(6);
    let size: f64 = args.next().and_then(|s| s.parse().ok()).unwrap_or(60.0);
    let path = args.next().unwrap_or_else(|| "spectre.svg".into());

    let t = Tiling::new(Label::Delta, level);
    let b = t.bounds();
    let (cx, cy) = ((b.min_x + b.max_x) / 2.0, (b.min_y + b.max_y) / 2.0);
    let vp = Aabb::new(cx - size / 2.0, cy - size / 2.0, cx + size / 2.0, cy + size / 2.0);

    let pal = [
        "#c4c9a9", "#9ca074", "#dcdcdc", "#ffbfbf", "#ffa07a", "#fff200", "#87cefa",
        "#f5f5dc", "#00ff00", "#00ffff",
    ];
    let mut body = String::new();
    let mut n = 0u64;
    t.for_each_in(&vp, (cx, cy), |kind, s, r, x, y| {
        let verts = t.leaf_vertices(s, r);
        let mut d = String::with_capacity(200);
        for (vx, vy) in verts {
            let _ = write!(d, "{:.3},{:.3} ", x + *vx as f64, y + *vy as f64);
        }
        let _ = write!(
            body,
            "<polygon points=\"{}\" fill=\"{}\" stroke=\"black\" stroke-width=\"0.08\"/>",
            d.trim_end(),
            pal[kind as usize]
        );
        n += 1;
    });
    let h = size / 2.0;
    let svg = format!(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"{} {} {} {}\" width=\"1000\" height=\"1000\">{}</svg>",
        -h, -h, size, size, body
    );
    std::fs::write(&path, svg).unwrap();
    println!("{n} tiles -> {path} (labels: {})", LABEL_NAMES.join(", "));
}
