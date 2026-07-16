//! Dump exact tile anchors of a spectre patch as CSV (added for the
//! einstein search program; not part of upstream).
//!
//! Each row is a leaf tile's exact identity: kind (0=Gamma1, 1=Gamma2,
//! 2..=Delta..Psi shifted by 1), mirror flag s, rotation r (30-degree
//! units), and the exact rank-4 module translation t0..t3.  Cartesian
//! projection is left to the consumer: x = t0 + (sqrt3/2) t1 + t2/2,
//! y = t1/2 + (sqrt3/2) t2 + t3 — done downstream so this output stays
//! integer-exact.
//!
//! Usage: anchors <label> <level> <out.csv> [x0 y0 x1 y1]
//! Without a clip box the whole root patch is dumped.

use spectre_core::{Aabb, Label, Tiling, LABEL_NAMES};
use std::io::{BufWriter, Write};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 && args.len() != 8 {
        eprintln!("usage: anchors <label> <level> <out.csv> [x0 y0 x1 y1]");
        std::process::exit(2);
    }
    let label_idx = LABEL_NAMES
        .iter()
        .position(|n| n.eq_ignore_ascii_case(&args[1]))
        .unwrap_or_else(|| {
            eprintln!("unknown label {} (want one of {:?})", args[1], LABEL_NAMES);
            std::process::exit(2);
        });
    let level: usize = args[2].parse().expect("level must be an integer");
    let tiling = Tiling::new(Label::from_index(label_idx as u8), level);
    let vp = if args.len() == 8 {
        Aabb::new(
            args[4].parse().unwrap(),
            args[5].parse().unwrap(),
            args[6].parse().unwrap(),
            args[7].parse().unwrap(),
        )
    } else {
        tiling.bounds()
    };
    let f = std::fs::File::create(&args[3]).expect("cannot create output file");
    let mut w = BufWriter::new(f);
    writeln!(w, "kind,s,r,t0,t1,t2,t3").unwrap();
    let mut n: u64 = 0;
    tiling.for_each_ids_in(&vp, |id| {
        writeln!(
            w,
            "{},{},{},{},{},{},{}",
            id.kind, id.s, id.r, id.t[0], id.t[1], id.t[2], id.t[3]
        )
        .unwrap();
        n += 1;
    });
    w.flush().unwrap();
    eprintln!("{n} tiles -> {}", args[3]);
}
