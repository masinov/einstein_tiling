//! Exact compiled A0 census for free polykites, n <= 16.
//!
//! This mirrors `einstein.polykites.enumeration`: breadth-first boundary
//! growth followed by canonicalization under translations and the full D6
//! point group.  A canonical shape is stored in a fixed 32-byte key.

use std::collections::HashSet;
use std::env;
use std::fs::{self, File};
use std::hash::{BuildHasherDefault, Hasher};
use std::io::{BufWriter, Write};
use std::path::Path;
use std::time::Instant;

const MAX_N: usize = 16;
const UNUSED: u16 = u16::MAX;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Cell {
    x: i16,
    y: i16,
    d: u8,
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Shape([u16; MAX_N]);

#[derive(Default)]
struct FastHasher(u64);

impl Hasher for FastHasher {
    fn finish(&self) -> u64 {
        self.0
    }

    fn write(&mut self, bytes: &[u8]) {
        let mut h = if self.0 == 0 {
            0x517c_c1b7_2722_0a95
        } else {
            self.0
        };
        for &byte in bytes {
            h ^= u64::from(byte);
            h = h.wrapping_mul(0x1000_0000_01b3);
        }
        self.0 = h;
    }
}

type ShapeSet = HashSet<Shape, BuildHasherDefault<FastHasher>>;

fn rot60(cell: Cell) -> Cell {
    Cell {
        x: -cell.y,
        y: cell.x + cell.y,
        d: (cell.d + 1) % 6,
    }
}

fn transform(mut cell: Cell, op: u8) -> Cell {
    let turns = op % 6;
    if op >= 6 {
        cell = Cell {
            x: cell.x + cell.y,
            y: -cell.y,
            d: (6 - cell.d) % 6,
        };
    }
    for _ in 0..turns {
        cell = rot60(cell);
    }
    cell
}

fn pack(cell: Cell, tx: i16, ty: i16) -> u16 {
    let dx = cell.x - tx;
    let dy = cell.y - ty;
    assert!(dx % 2 == 0 && dy % 2 == 0);
    let x = dx / 2;
    let y = dy / 2 + 32;
    assert!((0..64).contains(&x), "x key overflow: {x}");
    assert!((0..64).contains(&y), "y key overflow: {y}");
    ((x as u16) << 9) | ((y as u16) << 3) | u16::from(cell.d)
}

fn unpack(code: u16) -> Cell {
    Cell {
        x: (2 * ((code >> 9) & 63)) as i16,
        y: 2 * ((((code >> 3) & 63) as i16) - 32),
        d: (code & 7) as u8,
    }
}

fn canonical(cells: &[Cell]) -> Shape {
    let mut best = [UNUSED; MAX_N];
    for op in 0..12 {
        let mut image: Vec<Cell> = cells
            .iter()
            .copied()
            .map(|cell| transform(cell, op))
            .collect();
        image.sort_unstable();
        let tx = image[0].x;
        let ty = image[0].y;
        let mut key = [UNUSED; MAX_N];
        for (slot, cell) in key.iter_mut().zip(image) {
            *slot = pack(cell, tx, ty);
        }
        if key < best {
            best = key;
        }
    }
    Shape(best)
}

fn directions() -> [(i16, i16); 6] {
    let mut result = [(0, 0); 6];
    let mut point = (1, 1);
    for slot in &mut result {
        *slot = point;
        point = (-point.1, point.0 + point.1);
    }
    result
}

fn neighbors(cell: Cell, mdir: &[(i16, i16); 6]) -> [Cell; 4] {
    let d = cell.d as usize;
    let ma = mdir[(d + 5) % 6];
    let mb = mdir[d];
    [
        Cell {
            d: ((d + 1) % 6) as u8,
            ..cell
        },
        Cell {
            d: ((d + 5) % 6) as u8,
            ..cell
        },
        Cell {
            x: cell.x + 2 * ma.0,
            y: cell.y + 2 * ma.1,
            d: ((d + 2) % 6) as u8,
        },
        Cell {
            x: cell.x + 2 * mb.0,
            y: cell.y + 2 * mb.1,
            d: ((d + 4) % 6) as u8,
        },
    ]
}

fn decode(shape: Shape, n: usize) -> Vec<Cell> {
    shape.0[..n].iter().copied().map(unpack).collect()
}

fn dump_level(directory: &Path, n: usize, level: &ShapeSet) {
    fs::create_dir_all(directory).expect("create dump directory");
    let path = directory.join(format!("polykites-{n:02}.bin"));
    let mut output = BufWriter::new(File::create(path).expect("create dump"));
    output.write_all(b"A0PK").expect("write magic");
    output.write_all(&[1, n as u8]).expect("write version/size");
    output.write_all(&0_u16.to_le_bytes()).expect("write reserved");
    output
        .write_all(&(level.len() as u64).to_le_bytes())
        .expect("write count");
    for shape in level {
        for code in &shape.0[..n] {
            output.write_all(&code.to_le_bytes()).expect("write shape");
        }
    }
    output.flush().expect("flush dump");
}

fn enumerate(n_max: usize, dump_directory: Option<&Path>) {
    let mdir = directions();
    let mut level = ShapeSet::default();
    level.insert(canonical(&[Cell { x: 0, y: 0, d: 0 }]));
    let start = Instant::now();
    println!("1 {} {:.3}", level.len(), start.elapsed().as_secs_f64());
    if let Some(directory) = dump_directory {
        dump_level(directory, 1, &level);
    }
    for n in 2..=n_max {
        let expected = level.len().saturating_mul(3);
        let mut next = ShapeSet::with_capacity_and_hasher(
            expected,
            BuildHasherDefault::default(),
        );
        for shape in level.drain() {
            let cells = decode(shape, n - 1);
            let mut exterior = Vec::with_capacity(2 * n + 2);
            for &cell in &cells {
                for neighbor in neighbors(cell, &mdir) {
                    if !cells.contains(&neighbor) && !exterior.contains(&neighbor) {
                        exterior.push(neighbor);
                    }
                }
            }
            for neighbor in exterior {
                let mut grown = cells.clone();
                grown.push(neighbor);
                next.insert(canonical(&grown));
            }
        }
        level = next;
        println!(
            "{n} {} {:.3}",
            level.len(),
            start.elapsed().as_secs_f64(),
        );
        if let Some(directory) = dump_directory {
            dump_level(directory, n, &level);
        }
    }
}

fn main() {
    let mut args = env::args().skip(1);
    let n_max = args
        .next()
        .unwrap_or_else(|| "12".to_string())
        .parse::<usize>()
        .expect("usage: a0_polykites [n_max] [dump_directory]");
    assert!((1..=MAX_N).contains(&n_max), "n_max must be 1..={MAX_N}");
    let dump_directory = args.next();
    assert!(args.next().is_none(), "too many arguments");
    enumerate(n_max, dump_directory.as_deref().map(Path::new));
}
