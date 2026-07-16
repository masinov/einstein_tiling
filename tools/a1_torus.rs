//! Exact compiled A1 torus screen for one `A0PK` level.
//!
//! Periodic shapes are retired only after finding an exact torus cover.
//! Refuted and node-budget-exhausted shapes remain in the survivor stream.

use std::env;
use std::fs::{File, OpenOptions};
use std::io::{
    BufReader, BufWriter, Read, Seek, SeekFrom, Write,
};
use std::path::Path;
use std::time::Instant;

const MAGIC: &[u8; 4] = b"A0PK";

#[derive(Clone, Copy, Debug)]
struct Cell {
    x: i16,
    y: i16,
    d: u8,
}

#[derive(Clone, Copy)]
struct Placement {
    op: u8,
    tu: u8,
    tv: u8,
    mask: u128,
}

fn read_u16(input: &mut impl Read) -> u16 {
    let mut raw = [0_u8; 2];
    input.read_exact(&mut raw).expect("read u16");
    u16::from_le_bytes(raw)
}

fn read_u64(input: &mut impl Read) -> u64 {
    let mut raw = [0_u8; 8];
    input.read_exact(&mut raw).expect("read u64");
    u64::from_le_bytes(raw)
}

fn unpack(code: u16) -> Cell {
    Cell {
        x: (2 * ((code >> 9) & 63)) as i16,
        y: 2 * ((((code >> 3) & 63) as i16) - 32),
        d: (code & 7) as u8,
    }
}

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

fn cell_to_lattice(cell: Cell) -> (i16, i16, u8) {
    let p = 2 * cell.x + cell.y;
    let q = cell.y - cell.x;
    assert!(p % 6 == 0 && q % 6 == 0);
    (p / 6, q / 6, cell.d)
}

fn reduce(u: i16, v: i16, a: i16, b: i16, d: i16) -> (usize, usize) {
    let quotient = v.div_euclid(d);
    let vv = v.rem_euclid(d);
    let uu = (u - quotient * b).rem_euclid(a);
    (uu as usize, vv as usize)
}

fn sublattices(k: usize) -> Vec<(usize, usize, usize)> {
    let mut result = Vec::new();
    for a in 1..=k {
        if k % a != 0 {
            continue;
        }
        let d = k / a;
        for b in 0..a {
            result.push((a, b, d));
        }
    }
    result
}

fn placements(
    images: &[Vec<(i16, i16, u8)>],
    shape_size: usize,
    hnf: (usize, usize, usize),
) -> Vec<Placement> {
    let (a, b, d) = hnf;
    let mut result = Vec::<Placement>::new();
    for (op, image) in images.iter().enumerate() {
        for tu in 0..a {
            for tv in 0..d {
                let mut mask = 0_u128;
                for &(u, v, sector) in image {
                    let (uu, vv) = reduce(
                        u + tu as i16,
                        v + tv as i16,
                        a as i16,
                        b as i16,
                        d as i16,
                    );
                    let index = (uu * d + vv) * 6 + sector as usize;
                    let bit = 1_u128 << index;
                    if mask & bit != 0 {
                        break;
                    }
                    mask |= bit;
                }
                if mask.count_ones() as usize == shape_size
                    && !result.iter().any(|placement| placement.mask == mask)
                {
                    result.push(Placement {
                        op: op as u8,
                        tu: tu as u8,
                        tv: tv as u8,
                        mask,
                    });
                }
            }
        }
    }
    result
}

fn exact_cover(
    placements: &[Placement],
    n_cells: usize,
    node_budget: u64,
) -> Result<Option<Vec<Placement>>, ()> {
    let full = (1_u128 << n_cells) - 1;
    let mut by_cell = vec![Vec::<usize>::new(); n_cells];
    for (index, placement) in placements.iter().enumerate() {
        let mut mask = placement.mask;
        while mask != 0 {
            let bit = mask.trailing_zeros() as usize;
            by_cell[bit].push(index);
            mask &= mask - 1;
        }
    }
    let mut nodes = 0_u64;
    let mut chosen = Vec::<usize>::new();

    fn search(
        cover: u128,
        full: u128,
        placements: &[Placement],
        by_cell: &[Vec<usize>],
        chosen: &mut Vec<usize>,
        nodes: &mut u64,
        node_budget: u64,
    ) -> Result<bool, ()> {
        *nodes += 1;
        if *nodes > node_budget {
            return Err(());
        }
        if cover == full {
            return Ok(true);
        }
        let mut uncovered = full & !cover;
        let mut best = Vec::<usize>::new();
        let mut first = true;
        while uncovered != 0 {
            let cell = uncovered.trailing_zeros() as usize;
            uncovered &= uncovered - 1;
            let options: Vec<_> = by_cell[cell]
                .iter()
                .copied()
                .filter(|&index| placements[index].mask & cover == 0)
                .collect();
            if options.is_empty() {
                return Ok(false);
            }
            if first || options.len() < best.len() {
                first = false;
                best = options;
                if best.len() == 1 {
                    break;
                }
            }
        }
        for index in best {
            chosen.push(index);
            if search(
                cover | placements[index].mask,
                full,
                placements,
                by_cell,
                chosen,
                nodes,
                node_budget,
            )? {
                return Ok(true);
            }
            chosen.pop();
        }
        Ok(false)
    }

    match search(
        0,
        full,
        placements,
        &by_cell,
        &mut chosen,
        &mut nodes,
        node_budget,
    ) {
        Ok(true) => Ok(Some(
            chosen.into_iter().map(|index| placements[index]).collect(),
        )),
        Ok(false) => Ok(None),
        Err(()) => Err(()),
    }
}

fn periodic_certificate(
    shape: &[Cell],
    k_max: usize,
    node_budget: u64,
) -> (Option<((usize, usize, usize), Vec<Placement>)>, bool) {
    let n = shape.len();
    let mut exhausted = false;
    let images: Vec<Vec<_>> = (0..12)
        .map(|op| {
            shape
                .iter()
                .copied()
                .map(|cell| cell_to_lattice(transform(cell, op)))
                .collect()
        })
        .collect();
    for k in 1..=k_max {
        if (6 * k) % n != 0 {
            continue;
        }
        for hnf in sublattices(k) {
            let candidates = placements(&images, n, hnf);
            match exact_cover(&candidates, 6 * k, node_budget) {
                Ok(Some(solution)) => return (Some((hnf, solution)), exhausted),
                Ok(None) => {}
                Err(()) => exhausted = true,
            }
        }
    }
    (None, exhausted)
}

fn write_header(output: &mut impl Write, n: u8, count: u64) {
    output.write_all(MAGIC).expect("write magic");
    output.write_all(&[1, n]).expect("write version/size");
    output.write_all(&0_u16.to_le_bytes()).expect("write reserved");
    output.write_all(&count.to_le_bytes()).expect("write count");
}

fn write_certificate(
    output: &mut impl Write,
    codes: &[u16],
    hnf: (usize, usize, usize),
    solution: &[Placement],
) {
    write!(output, "{{\"shape\":\"").expect("write certificate");
    for code in codes {
        write!(output, "{code:04x}").expect("write shape key");
    }
    write!(
        output,
        "\",\"hnf\":[{},{},{}],\"placements\":[",
        hnf.0, hnf.1, hnf.2,
    )
    .expect("write hnf");
    for (index, placement) in solution.iter().enumerate() {
        if index != 0 {
            output.write_all(b",").expect("write separator");
        }
        write!(
            output,
            "[{},{},{}]",
            placement.op, placement.tu, placement.tv,
        )
        .expect("write placement");
    }
    output.write_all(b"]}\n").expect("finish certificate");
}

fn screen(
    input_path: &Path,
    survivor_path: Option<&Path>,
    certificate_path: Option<&Path>,
    k_max: usize,
    node_budget: u64,
    start: u64,
    requested_count: Option<u64>,
) {
    let mut input = BufReader::new(File::open(input_path).expect("open input"));
    let mut magic = [0_u8; 4];
    input.read_exact(&mut magic).expect("read magic");
    assert_eq!(&magic, MAGIC);
    let mut metadata = [0_u8; 4];
    input.read_exact(&mut metadata).expect("read metadata");
    assert_eq!(metadata[0], 1);
    assert_eq!(&metadata[2..], &[0, 0]);
    let n = metadata[1] as usize;
    let total_count = read_u64(&mut input);
    assert!(n > 0 && 6 * k_max <= 127);
    assert!(start <= total_count);
    let count = requested_count
        .unwrap_or(total_count - start)
        .min(total_count - start);
    input
        .seek(SeekFrom::Start(16 + start * (2 * n) as u64))
        .expect("seek input range");

    let mut survivors = survivor_path.map(|path| {
        let mut output = BufWriter::new(File::create(path).expect("create survivors"));
        write_header(&mut output, n as u8, 0);
        output
    });
    let mut certificates = certificate_path.map(|path| {
        BufWriter::new(File::create(path).expect("create certificates"))
    });
    let started = Instant::now();
    let mut periodic = 0_u64;
    let mut survivor_count = 0_u64;
    let mut exhausted = 0_u64;
    let mut codes = vec![0_u16; n];
    for index in 0..count {
        for code in &mut codes {
            *code = read_u16(&mut input);
        }
        let shape: Vec<_> = codes.iter().copied().map(unpack).collect();
        let (certificate, hit_budget) =
            periodic_certificate(&shape, k_max, node_budget);
        if let Some((hnf, solution)) = certificate {
            periodic += 1;
            if let Some(output) = certificates.as_mut() {
                write_certificate(output, &codes, hnf, &solution);
            }
        } else {
            survivor_count += 1;
            if hit_budget {
                exhausted += 1;
            }
            if let Some(output) = survivors.as_mut() {
                for code in &codes {
                    output
                        .write_all(&code.to_le_bytes())
                        .expect("write survivor");
                }
            }
        }
        if (index + 1) % 1_000_000 == 0 {
            eprintln!(
                "{} / {} in {:.1}s",
                index + 1,
                count,
                started.elapsed().as_secs_f64(),
            );
        }
    }
    if start + count == total_count {
        assert!(input.read(&mut [0_u8; 1]).expect("check trailing data") == 0);
    }
    drop(survivors);
    drop(certificates);
    if let Some(path) = survivor_path {
        let mut output = OpenOptions::new()
            .write(true)
            .open(path)
            .expect("patch survivor header");
        output.seek(SeekFrom::Start(8)).expect("seek count");
        output
            .write_all(&survivor_count.to_le_bytes())
            .expect("patch count");
    }
    println!(
        "n={n} start={start} total={count} periodic={periodic} \
         survivors={survivor_count} exhausted={exhausted} seconds={:.3}",
        started.elapsed().as_secs_f64(),
    );
}

fn main() {
    let mut args = env::args().skip(1);
    let input = args.next().expect(
        "usage: a1_torus input [survivors|-] [certificates|-] [k_max] [node_budget]",
    );
    let survivors = args.next().unwrap_or_else(|| "-".to_string());
    let certificates = args.next().unwrap_or_else(|| "-".to_string());
    let k_max = args
        .next()
        .unwrap_or_else(|| "12".to_string())
        .parse()
        .expect("invalid k_max");
    let node_budget = args
        .next()
        .unwrap_or_else(|| "200000".to_string())
        .parse()
        .expect("invalid node_budget");
    let start = args
        .next()
        .unwrap_or_else(|| "0".to_string())
        .parse()
        .expect("invalid start");
    let count = args
        .next()
        .map(|value| value.parse().expect("invalid count"));
    assert!(args.next().is_none(), "too many arguments");
    screen(
        Path::new(&input),
        (survivors != "-").then(|| Path::new(&survivors)),
        (certificates != "-").then(|| Path::new(&certificates)),
        k_max,
        node_budget,
        start,
        count,
    );
}
