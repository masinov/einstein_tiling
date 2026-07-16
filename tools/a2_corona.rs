//! Exact compiled A2 first-corona screen for one `A0PK` survivor stream.
//!
//! Shapes are rejected only after exhaustive proof that no hole-free first
//! corona exists. Witnessed coronas and node-budget exhaustions survive.

use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs::{File, OpenOptions};
use std::io::{BufReader, BufWriter, Read, Seek, SeekFrom, Write};
use std::path::Path;
use std::time::Instant;

const MAGIC: &[u8; 4] = b"A0PK";

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Cell {
    x: i16,
    y: i16,
    d: u8,
}

#[derive(Clone)]
struct Placement {
    op: u8,
    tx: i16,
    ty: i16,
    cells: Vec<Cell>,
    ids: Vec<usize>,
    required: Vec<usize>,
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

fn rot_point(point: (i16, i16)) -> (i16, i16) {
    (-point.1, point.0 + point.1)
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

fn directions(first: (i16, i16)) -> [(i16, i16); 6] {
    let mut result = [(0, 0); 6];
    let mut point = first;
    for slot in &mut result {
        *slot = point;
        point = rot_point(point);
    }
    result
}

fn is_center(point: (i16, i16)) -> bool {
    point.0 % 2 == 0 && point.1 % 2 == 0 && (point.1 - point.0) % 6 == 0
}

fn cell_vertices(cell: Cell, vdir: &[(i16, i16); 6], mdir: &[(i16, i16); 6]) -> [(i16, i16); 4] {
    let d = cell.d as usize;
    let m0 = mdir[(d + 5) % 6];
    let vertex = vdir[d];
    let m1 = mdir[d];
    [
        (cell.x, cell.y),
        (cell.x + m0.0, cell.y + m0.1),
        (cell.x + vertex.0, cell.y + vertex.1),
        (cell.x + m1.0, cell.y + m1.1),
    ]
}

fn cells_at_point(point: (i16, i16), vdir: &[(i16, i16); 6], mdir: &[(i16, i16); 6]) -> Vec<Cell> {
    if is_center(point) {
        return (0..6)
            .map(|d| Cell {
                x: point.0,
                y: point.1,
                d,
            })
            .collect();
    }
    let mut result = Vec::new();
    for (d, direction) in vdir.iter().enumerate() {
        let center = (point.0 - direction.0, point.1 - direction.1);
        if is_center(center) {
            result.push(Cell {
                x: center.0,
                y: center.1,
                d: d as u8,
            });
        }
    }
    if !result.is_empty() {
        return result;
    }
    for (d, direction) in mdir.iter().enumerate() {
        let center = (point.0 - direction.0, point.1 - direction.1);
        if is_center(center) {
            result.push(Cell {
                x: center.0,
                y: center.1,
                d: d as u8,
            });
            result.push(Cell {
                x: center.0,
                y: center.1,
                d: ((d + 1) % 6) as u8,
            });
        }
    }
    result
}

fn ring(occupied: &HashSet<Cell>) -> Vec<Cell> {
    let vdir = directions((2, 0));
    let mdir = directions((1, 1));
    let mut result = HashSet::new();
    for &cell in occupied {
        for point in cell_vertices(cell, &vdir, &mdir) {
            for neighbor in cells_at_point(point, &vdir, &mdir) {
                if !occupied.contains(&neighbor) {
                    result.insert(neighbor);
                }
            }
        }
    }
    let mut result: Vec<_> = result.into_iter().collect();
    result.sort_unstable();
    result
}

fn candidate_placements(
    shape: &[Cell],
    patch: &HashSet<Cell>,
    required: &[Cell],
) -> Vec<Placement> {
    let required_index: HashMap<_, _> = required
        .iter()
        .copied()
        .enumerate()
        .map(|(index, cell)| (cell, index))
        .collect();
    let mut seen = HashSet::<Vec<Cell>>::new();
    let mut result = Vec::new();
    for op in 0..12 {
        let image: Vec<_> = shape
            .iter()
            .copied()
            .map(|cell| transform(cell, op))
            .collect();
        for &target in required {
            for &source in &image {
                if source.d != target.d {
                    continue;
                }
                let tx = target.x - source.x;
                let ty = target.y - source.y;
                let mut cells: Vec<_> = image
                    .iter()
                    .map(|cell| Cell {
                        x: cell.x + tx,
                        y: cell.y + ty,
                        d: cell.d,
                    })
                    .collect();
                cells.sort_unstable();
                if cells.iter().any(|cell| patch.contains(cell)) || !seen.insert(cells.clone()) {
                    continue;
                }
                let required_cells = cells
                    .iter()
                    .filter_map(|cell| required_index.get(cell).copied())
                    .collect();
                result.push(Placement {
                    op,
                    tx,
                    ty,
                    cells,
                    ids: Vec::new(),
                    required: required_cells,
                });
            }
        }
    }
    let mut cell_ids = HashMap::<Cell, usize>::new();
    for placement in &mut result {
        placement.ids = placement
            .cells
            .iter()
            .map(|&cell| {
                let next = cell_ids.len();
                *cell_ids.entry(cell).or_insert(next)
            })
            .collect();
    }
    result
}

fn cell_to_lattice(cell: Cell) -> (i16, i16, u8) {
    let p = 2 * cell.x + cell.y;
    let q = cell.y - cell.x;
    assert!(p % 6 == 0 && q % 6 == 0);
    (p / 6, q / 6, cell.d)
}

fn lattice_to_cell(cell: (i16, i16, u8)) -> Cell {
    Cell {
        x: 2 * cell.0 - 2 * cell.1,
        y: 2 * cell.0 + 4 * cell.1,
        d: cell.2,
    }
}

fn cell_neighbors(cell: Cell, mdir: &[(i16, i16); 6]) -> [Cell; 4] {
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

fn has_hole(patch: &HashSet<Cell>) -> bool {
    let occupied: HashSet<_> = patch.iter().copied().map(cell_to_lattice).collect();
    let u0 = occupied.iter().map(|cell| cell.0).min().unwrap() - 2;
    let u1 = occupied.iter().map(|cell| cell.0).max().unwrap() + 2;
    let v0 = occupied.iter().map(|cell| cell.1).min().unwrap() - 2;
    let v1 = occupied.iter().map(|cell| cell.1).max().unwrap() + 2;
    let mut empty = HashSet::new();
    for u in u0..=u1 {
        for v in v0..=v1 {
            for d in 0..6 {
                let cell = (u, v, d);
                if !occupied.contains(&cell) {
                    empty.insert(cell);
                }
            }
        }
    }
    let mut queue = VecDeque::new();
    let mut reached = HashSet::new();
    for &cell in &empty {
        if cell.0 == u0 || cell.0 == u1 || cell.1 == v0 || cell.1 == v1 {
            reached.insert(cell);
            queue.push_back(cell);
        }
    }
    let mdir = directions((1, 1));
    while let Some(cell) = queue.pop_front() {
        for neighbor in cell_neighbors(lattice_to_cell(cell), &mdir) {
            let lattice = cell_to_lattice(neighbor);
            if lattice.0 >= u0
                && lattice.0 <= u1
                && lattice.1 >= v0
                && lattice.1 <= v1
                && empty.contains(&lattice)
                && reached.insert(lattice)
            {
                queue.push_back(lattice);
            }
        }
    }
    reached.len() != empty.len()
}

fn corona_chain(
    shape: &[Cell],
    depth_cap: usize,
    node_budget: u64,
) -> Result<Option<Vec<Vec<Placement>>>, ()> {
    let seed: HashSet<_> = shape.iter().copied().collect();
    let mut nodes = 0_u64;
    let mut chain = Vec::<Vec<Placement>>::new();

    fn extend(
        shape: &[Cell],
        patch: &HashSet<Cell>,
        level: usize,
        depth_cap: usize,
        nodes: &mut u64,
        node_budget: u64,
        chain: &mut Vec<Vec<Placement>>,
    ) -> Result<bool, ()> {
        let required = ring(patch);
        let placements = candidate_placements(shape, patch, &required);
        let mut by_required = vec![Vec::<usize>::new(); required.len()];
        let mut cell_count = 0;
        for (index, placement) in placements.iter().enumerate() {
            cell_count = cell_count.max(placement.ids.iter().copied().max().unwrap_or(0) + 1);
            for &item in &placement.required {
                by_required[item].push(index);
            }
        }
        if by_required.iter().any(Vec::is_empty) {
            return Ok(false);
        }
        let mut covered = vec![false; required.len()];
        let mut used = vec![false; cell_count];
        let mut chosen = Vec::<usize>::new();

        fn search(
            covered: &mut [bool],
            remaining: usize,
            shape: &[Cell],
            patch: &HashSet<Cell>,
            level: usize,
            depth_cap: usize,
            placements: &[Placement],
            by_required: &[Vec<usize>],
            used: &mut [bool],
            chosen: &mut Vec<usize>,
            nodes: &mut u64,
            node_budget: u64,
            chain: &mut Vec<Vec<Placement>>,
        ) -> Result<bool, ()> {
            *nodes += 1;
            if *nodes > node_budget {
                return Err(());
            }
            if remaining == 0 {
                let mut next_patch = patch.clone();
                for &index in chosen.iter() {
                    next_patch.extend(placements[index].cells.iter().copied());
                }
                if has_hole(&next_patch) {
                    return Ok(false);
                }
                chain.push(
                    chosen
                        .iter()
                        .map(|&index| placements[index].clone())
                        .collect(),
                );
                let reached = if level == depth_cap {
                    true
                } else {
                    extend(
                        shape,
                        &next_patch,
                        level + 1,
                        depth_cap,
                        nodes,
                        node_budget,
                        chain,
                    )?
                };
                if !reached {
                    chain.pop();
                }
                return Ok(reached);
            }
            let mut best = Vec::<usize>::new();
            let mut first = true;
            for item in 0..covered.len() {
                if covered[item] {
                    continue;
                }
                let options: Vec<_> = by_required[item]
                    .iter()
                    .copied()
                    .filter(|&index| placements[index].ids.iter().all(|&id| !used[id]))
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
                for &id in &placements[index].ids {
                    used[id] = true;
                }
                for &item in &placements[index].required {
                    assert!(!covered[item]);
                    covered[item] = true;
                }
                chosen.push(index);
                if search(
                    covered,
                    remaining - placements[index].required.len(),
                    shape,
                    patch,
                    level,
                    depth_cap,
                    placements,
                    by_required,
                    used,
                    chosen,
                    nodes,
                    node_budget,
                    chain,
                )? {
                    return Ok(true);
                }
                chosen.pop();
                for &item in &placements[index].required {
                    covered[item] = false;
                }
                for &id in &placements[index].ids {
                    used[id] = false;
                }
            }
            Ok(false)
        }

        search(
            &mut covered,
            required.len(),
            shape,
            patch,
            level,
            depth_cap,
            &placements,
            &by_required,
            &mut used,
            &mut chosen,
            nodes,
            node_budget,
            chain,
        )
    }

    if extend(
        shape,
        &seed,
        1,
        depth_cap,
        &mut nodes,
        node_budget,
        &mut chain,
    )? {
        Ok(Some(chain))
    } else {
        Ok(None)
    }
}

fn write_header(output: &mut impl Write, n: u8, count: u64) {
    output.write_all(MAGIC).expect("write magic");
    output.write_all(&[1, n]).expect("write version/size");
    output
        .write_all(&0_u16.to_le_bytes())
        .expect("write reserved");
    output.write_all(&count.to_le_bytes()).expect("write count");
}

fn write_witness(output: &mut impl Write, codes: &[u16], chain: &[Vec<Placement>]) {
    write!(output, "{{\"shape\":\"").expect("write witness");
    for code in codes {
        write!(output, "{code:04x}").expect("write shape key");
    }
    output
        .write_all(b"\",\"coronas\":[")
        .expect("write coronas");
    for (level, placements) in chain.iter().enumerate() {
        if level != 0 {
            output.write_all(b",").expect("write level separator");
        }
        output.write_all(b"[").expect("write corona");
        for (index, placement) in placements.iter().enumerate() {
            if index != 0 {
                output.write_all(b",").expect("write separator");
            }
            write!(
                output,
                "[{},{},{}]",
                placement.op, placement.tx, placement.ty,
            )
            .expect("write placement");
        }
        output.write_all(b"]").expect("finish corona");
    }
    output.write_all(b"]}\n").expect("finish witness");
}

fn screen(
    input_path: &Path,
    survivor_path: Option<&Path>,
    witness_path: Option<&Path>,
    exhausted_path: Option<&Path>,
    depth_cap: usize,
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
    let mut witnesses =
        witness_path.map(|path| BufWriter::new(File::create(path).expect("create witnesses")));
    let mut exhausted_shapes = exhausted_path.map(|path| {
        let mut output = BufWriter::new(File::create(path).expect("create exhausted"));
        write_header(&mut output, n as u8, 0);
        output
    });
    let started = Instant::now();
    let mut below_cap = 0_u64;
    let mut witnessed = 0_u64;
    let mut exhausted = 0_u64;
    let mut codes = vec![0_u16; n];
    for index in 0..count {
        for code in &mut codes {
            *code = read_u16(&mut input);
        }
        let shape: Vec<_> = codes.iter().copied().map(unpack).collect();
        match corona_chain(&shape, depth_cap, node_budget) {
            Ok(None) => below_cap += 1,
            Ok(Some(chain)) => {
                witnessed += 1;
                if let Some(output) = witnesses.as_mut() {
                    write_witness(output, &codes, &chain);
                }
                if let Some(output) = survivors.as_mut() {
                    for code in &codes {
                        output
                            .write_all(&code.to_le_bytes())
                            .expect("write survivor");
                    }
                }
            }
            Err(()) => {
                exhausted += 1;
                if let Some(output) = survivors.as_mut() {
                    for code in &codes {
                        output
                            .write_all(&code.to_le_bytes())
                            .expect("write survivor");
                    }
                }
                if let Some(output) = exhausted_shapes.as_mut() {
                    for code in &codes {
                        output
                            .write_all(&code.to_le_bytes())
                            .expect("write exhausted");
                    }
                }
            }
        }
        if (index + 1) % 100_000 == 0 {
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
    drop(witnesses);
    drop(exhausted_shapes);
    let survivor_count = witnessed + exhausted;
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
    if let Some(path) = exhausted_path {
        let mut output = OpenOptions::new()
            .write(true)
            .open(path)
            .expect("patch exhausted header");
        output
            .seek(SeekFrom::Start(8))
            .expect("seek exhausted count");
        output
            .write_all(&exhausted.to_le_bytes())
            .expect("patch exhausted count");
    }
    println!(
        "n={n} start={start} total={count} depth_cap={depth_cap} \
         below_cap={below_cap} witnessed={witnessed} exhausted={exhausted} \
         survivors={survivor_count} seconds={:.3}",
        started.elapsed().as_secs_f64(),
    );
}

fn main() {
    let mut args = env::args().skip(1);
    let input = args.next().expect(
        "usage: a2_corona input [survivors|-] [witnesses|-] \
         [node_budget] [start] [count]",
    );
    let survivors = args.next().unwrap_or_else(|| "-".to_string());
    let witnesses = args.next().unwrap_or_else(|| "-".to_string());
    let exhausted = args.next().unwrap_or_else(|| "-".to_string());
    let depth_cap = args
        .next()
        .unwrap_or_else(|| "1".to_string())
        .parse()
        .expect("invalid depth_cap");
    let node_budget = args
        .next()
        .unwrap_or_else(|| "100000".to_string())
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
        (witnesses != "-").then(|| Path::new(&witnesses)),
        (exhausted != "-").then(|| Path::new(&exhausted)),
        depth_cap,
        node_budget,
        start,
        count,
    );
}
