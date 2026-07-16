//! Dump exact Spectre leaves with their hidden substitution ancestry.
//!
//! This is validation-only ground truth for the A6 blind hierarchy miner.
//! The miner consumes the ordinary `anchors` CSV (poses only); its output is
//! compared with this dump afterward.  A path is the sequence of child slots
//! from the root, with a final `a`/`b` suffix for the two Gamma leaves.
//!
//! Usage: hierarchy <label> <level> <out.csv>

use spectre_core::tables::{CHILD_ROT, CHILD_T, GAMMA2_ROT, GAMMA2_T, RULES};
use spectre_core::{Label, LABEL_NAMES};
use std::io::{BufWriter, Write};

#[derive(Clone)]
struct Frame {
    label: u8,
    level: usize,
    s: u8,
    r: u8,
    t: [i64; 4],
    path: Vec<u8>,
    labels: Vec<u8>,
}

fn rot30(v: [i64; 4]) -> [i64; 4] {
    [-v[3], v[0], v[1] + v[3], v[2]]
}

fn mirror_y(v: [i64; 4]) -> [i64; 4] {
    [-v[0] - v[2], -v[1], v[2], v[1] + v[3]]
}

fn apply_sr(s: u8, r: u8, mut v: [i64; 4]) -> [i64; 4] {
    if s == 1 {
        v = mirror_y(v);
    }
    for _ in 0..(r % 12) {
        v = rot30(v);
    }
    v
}

fn add(a: [i64; 4], b: [i64; 4]) -> [i64; 4] {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]]
}

fn path_string(path: &[u8], gamma: Option<char>) -> String {
    let mut text = path
        .iter()
        .map(|p| p.to_string())
        .collect::<Vec<_>>()
        .join(".");
    if let Some(suffix) = gamma {
        text.push(suffix);
    }
    text
}

fn label_string(labels: &[u8]) -> String {
    labels
        .iter()
        .map(|label| label.to_string())
        .collect::<Vec<_>>()
        .join(".")
}

fn emit(
    out: &mut BufWriter<std::fs::File>,
    kind: u8,
    frame: &Frame,
    t: [i64; 4],
    r: u8,
    gamma: Option<char>,
) {
    writeln!(
        out,
        "{},{},{},{},{},{},{},{},{}",
        kind,
        frame.s,
        r,
        t[0],
        t[1],
        t[2],
        t[3],
        path_string(&frame.path, gamma),
        label_string(&frame.labels),
    )
    .unwrap();
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 4 {
        eprintln!("usage: hierarchy <label> <level> <out.csv>");
        std::process::exit(2);
    }
    let label = LABEL_NAMES
        .iter()
        .position(|name| name.eq_ignore_ascii_case(&args[1]))
        .unwrap_or_else(|| {
            eprintln!("unknown label {}", args[1]);
            std::process::exit(2);
        }) as u8;
    let level: usize = args[2].parse().expect("level must be an integer");
    let file = std::fs::File::create(&args[3]).expect("cannot create output");
    let mut out = BufWriter::new(file);
    writeln!(out, "kind,s,r,t0,t1,t2,t3,path,labels").unwrap();

    let mut stack = vec![Frame {
        label,
        level,
        s: 0,
        r: 0,
        t: [0; 4],
        path: Vec::new(),
        labels: vec![label],
    }];
    let mut count = 0usize;
    while let Some(frame) = stack.pop() {
        if frame.level == 0 {
            if frame.label == Label::Gamma as u8 {
                emit(&mut out, 0, &frame, frame.t, frame.r, Some('a'));
                let d = apply_sr(frame.s, frame.r, GAMMA2_T);
                let r = if frame.s == 1 {
                    (frame.r + 12 - GAMMA2_ROT) % 12
                } else {
                    (frame.r + GAMMA2_ROT) % 12
                };
                emit(&mut out, 1, &frame, add(frame.t, d), r, Some('b'));
                count += 2;
            } else {
                emit(&mut out, frame.label + 1, &frame, frame.t, frame.r, None);
                count += 1;
            }
            continue;
        }
        let rule = &RULES[frame.label as usize];
        let rotations = &CHILD_ROT[frame.level - 1];
        let translations = &CHILD_T[frame.level - 1];
        for slot in (0..8).rev() {
            if rule[slot] == 255 {
                continue;
            }
            let mut path = frame.path.clone();
            path.push(slot as u8);
            let mut labels = frame.labels.clone();
            labels.push(rule[slot]);
            let d = apply_sr(frame.s, frame.r, translations[slot]);
            let r = if frame.s == 1 {
                (frame.r + 12 - rotations[slot]) % 12
            } else {
                (frame.r + rotations[slot]) % 12
            };
            stack.push(Frame {
                label: rule[slot],
                level: frame.level - 1,
                s: frame.s ^ 1,
                r,
                t: add(frame.t, d),
                path,
                labels,
            });
        }
    }
    out.flush().unwrap();
    eprintln!("{count} leaves -> {}", args[3]);
}
