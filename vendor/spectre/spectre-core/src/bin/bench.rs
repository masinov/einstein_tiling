//! Benchmark suite. Run with: cargo run --release --bin bench
//! Covers the benchmark matrix from the review: enumeration throughput,
//! materialization ns/tile, viewport queries on a huge implicit root,
//! pan traces with and without hysteresis, and parallel regen.
use spectre_core::{Aabb, CachedRegion, Instance, Label, Tiling};
use std::time::Instant;

fn main() {
    let huge = Aabb::new(-1e18, -1e18, 1e18, 1e18);

    // 1. enumeration throughput (count only, no output)
    for lvl in 6..=8 {
        let t = Tiling::new(Label::Delta, lvl);
        let t0 = Instant::now();
        let n = t.count_in(&huge);
        let dt = t0.elapsed().as_secs_f64();
        println!(
            "enumerate level {lvl}: {n} tiles in {:.3} ms ({:.1} ns/tile, {:.1} Mtiles/s)",
            dt * 1e3,
            dt * 1e9 / n as f64,
            n as f64 / dt / 1e6
        );
    }

    // 2. materialization into a reused instance buffer
    {
        let t = Tiling::new(Label::Delta, 8);
        let mut out: Vec<Instance> = Vec::with_capacity(17_000_000);
        t.instances_in(&huge, (0.0, 0.0), &mut out); // warm
        let t0 = Instant::now();
        t.instances_in(&huge, (0.0, 0.0), &mut out);
        let dt = t0.elapsed().as_secs_f64();
        println!(
            "materialize level 8: {} instances in {:.1} ms ({:.1} ns/tile, {:.2} GB/s)",
            out.len(),
            dt * 1e3,
            dt * 1e9 / out.len() as f64,
            out.len() as f64 * 16.0 / dt / 1e9
        );

        let threads = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1);
        let t0 = Instant::now();
        t.instances_in_parallel(&huge, (0.0, 0.0), &mut out, threads);
        let dt = t0.elapsed().as_secs_f64();
        println!(
            "materialize level 8 ({} threads): {:.1} ms ({:.1} ns/tile)",
            threads,
            dt * 1e3,
            dt * 1e9 / out.len() as f64
        );
    }

    // 3. viewport queries against a level-24 root (~1.6e21 tiles)
    {
        let t = Tiling::new(Label::Delta, 24);
        let b = t.bounds();
        let (cx, cy) = ((b.min_x + b.max_x) / 2.0, (b.min_y + b.max_y) / 2.0);
        let mut out = Vec::with_capacity(4 << 20);
        let mut rng: u64 = 0x0123456789abcdef;
        for size in [200.0, 1000.0, 5000.0] {
            let iters = 200;
            let mut total = 0usize;
            let t0 = Instant::now();
            for _ in 0..iters {
                rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
                let fx = (rng >> 40) as f64 / (1u64 << 24) as f64 - 0.5;
                rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
                let fy = (rng >> 40) as f64 / (1u64 << 24) as f64 - 0.5;
                let px = cx + fx * (b.max_x - b.min_x) * 0.5;
                let py = cy + fy * (b.max_y - b.min_y) * 0.5;
                let vp = Aabb::new(px, py, px + size, py + size);
                t.instances_in(&vp, (px, py), &mut out);
                total += out.len();
            }
            let dt = t0.elapsed().as_secs_f64();
            println!(
                "viewport {size:.0}x{size:.0} @ level-24 root: {:.3} ms/query, {:.0} tiles avg, {:.1} ns/emitted",
                dt * 1e3 / iters as f64,
                total as f64 / iters as f64,
                dt * 1e9 / total as f64
            );
        }
    }

    // 4. pan trace, with and without hysteresis
    {
        let t = Tiling::new(Label::Delta, 24);
        let b = t.bounds();
        let (cx, cy) = ((b.min_x + b.max_x) / 2.0, (b.min_y + b.max_y) / 2.0);
        let (vw, vh) = (480.0, 270.0);
        let frames = 240;

        let mut out = Vec::with_capacity(1 << 20);
        let (mut worst, mut total) = (0.0f64, 0usize);
        let t0 = Instant::now();
        for f in 0..frames {
            let (px, py) = (cx + f as f64 * 3.0, cy + f as f64 * 1.5);
            let f0 = Instant::now();
            let vp = Aabb::new(px, py, px + vw, py + vh);
            t.instances_in(&vp, (px, py), &mut out);
            worst = worst.max(f0.elapsed().as_secs_f64());
            total += out.len();
        }
        let dt = t0.elapsed().as_secs_f64();
        println!(
            "pan (regen every frame, {:.0} tiles/frame): avg {:.3} ms, worst {:.3} ms",
            total as f64 / frames as f64,
            dt * 1e3 / frames as f64,
            worst * 1e3
        );

        let mut cache = CachedRegion::new(0.3);
        let t0 = Instant::now();
        for f in 0..frames {
            let (px, py) = (cx + f as f64 * 3.0, cy + f as f64 * 1.5);
            let vp = Aabb::new(px, py, px + vw, py + vh);
            cache.update(&t, &vp, 1);
        }
        let dt = t0.elapsed().as_secs_f64();
        println!(
            "pan (30% hysteresis): {} regens / {frames} frames, {:.3} ms/frame amortized",
            cache.generations,
            dt * 1e3 / frames as f64
        );
    }
}
