//! # spectre-core
//!
//! Hyper-optimized generator for Spectre / Tile(1,1) einstein tilings.
//!
//! Design (see README for rationale and benchmarks):
//! * **Exact integer lattice.** Every vertex lies on the rank-4 Z-module
//!   spanned by unit vectors at 0/30/60/90 degrees. Substitution transforms
//!   are (mirror, rotation-by-30k, module translation) triples — pure integer
//!   arithmetic, no floats, no error accumulation, valid to level 32
//!   (~10^31 tiles) within i64.
//! * **Implicit hierarchy.** Nothing is materialized: a viewport query is an
//!   iterative DFS over a fixed-size stack with table-driven child transforms
//!   and conservative per-(level,label) AABB culling. Zero heap allocation.
//! * **16-byte GPU-ready instances.** `{f32 x, f32 y, u32 rot|mirror|label,
//!   u32 rgba}` relative to a caller-supplied f64 origin, so f32 precision
//!   survives even at level-30 world coordinates.

pub mod tables;

use tables::*;

pub const SQ3_2: f64 = 0.866_025_403_784_438_6;

/// Tile / metatile labels of the 9-unit substitution system.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
#[repr(u8)]
pub enum Label {
    Gamma = 0,
    Delta,
    Theta,
    Lambda,
    Xi,
    Pi,
    Sigma,
    Phi,
    Psi,
}

pub const LABEL_NAMES: [&str; 9] = [
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi",
];

/// Default per-label fill colors (RGBA8, matching the reference generator).
pub const PALETTE: [u32; 10] = [
    0xffa9c9c4, // Gamma1  (0xAABBGGRR little-endian abgr -> use as-is in shader unpack)
    0xff74a09c, // Gamma2
    0xffdcdcdc, // Delta
    0xffbfbfff, // Theta
    0xff7aa0ff, // Lambda
    0xff00f2ff, // Xi
    0xffface87, // Pi
    0xffdcf5f5, // Sigma
    0xff00ff00, // Phi
    0xffffff00, // Psi
];

/// Axis-aligned box in world coordinates.
#[derive(Clone, Copy, Debug)]
pub struct Aabb {
    pub min_x: f64,
    pub min_y: f64,
    pub max_x: f64,
    pub max_y: f64,
}

impl Aabb {
    #[inline]
    pub fn new(min_x: f64, min_y: f64, max_x: f64, max_y: f64) -> Self {
        Self { min_x, min_y, max_x, max_y }
    }
    #[inline]
    pub fn inflate(&self, fx: f64, fy: f64) -> Self {
        Self::new(self.min_x - fx, self.min_y - fy, self.max_x + fx, self.max_y + fy)
    }
    #[inline]
    pub fn contains(&self, o: &Aabb) -> bool {
        o.min_x >= self.min_x && o.min_y >= self.min_y && o.max_x <= self.max_x && o.max_y <= self.max_y
    }
}

/// GPU-ready packed instance, 16 bytes.
/// `meta` bit layout: rotation (0..12) in bits 0..4, mirror flag in bit 4,
/// tile kind (0 = Gamma1, 1 = Gamma2, 2.. = Delta..Psi shifted by 1) in bits 5..9.
#[derive(Clone, Copy, Debug, PartialEq)]
#[repr(C)]
pub struct Instance {
    pub x: f32,
    pub y: f32,
    pub meta: u32,
    pub color: u32,
}

// -------------------------------------------------------------------- module

/// Rotation/mirror matrices on the rank-4 module: `MSR[s][r]` = Rot(30r)·MirY^s.
struct Msr([[[[i64; 4]; 4]; 12]; 2]);

impl Msr {
    fn build() -> Self {
        let mut m = [[[[0i64; 4]; 4]; 12]; 2];
        for s in 0..2 {
            for r in 0..12 {
                for b in 0..4 {
                    let mut v = [0i64; 4];
                    v[b] = 1;
                    if s == 1 {
                        // mirror across y-axis: e_k -> e_{6-k}
                        v = [-v[0] - v[2], -v[1], v[2], v[1] + v[3]];
                    }
                    for _ in 0..r {
                        // rotate +30 deg: e_k -> e_{k+1}
                        v = [-v[3], v[0], v[1] + v[3], v[2]];
                    }
                    for row in 0..4 {
                        m[s][r][row][b] = v[row];
                    }
                }
            }
        }
        Msr(m)
    }
    #[inline(always)]
    fn apply(&self, s: usize, r: usize, t: &[i64; 4]) -> [i64; 4] {
        let m = &self.0[s][r];
        [
            m[0][0] * t[0] + m[0][1] * t[1] + m[0][2] * t[2] + m[0][3] * t[3],
            m[1][0] * t[0] + m[1][1] * t[1] + m[1][2] * t[2] + m[1][3] * t[3],
            m[2][0] * t[0] + m[2][1] * t[1] + m[2][2] * t[2] + m[2][3] * t[3],
            m[3][0] * t[0] + m[3][1] * t[1] + m[3][2] * t[2] + m[3][3] * t[3],
        ]
    }
}

/// Convert a module vector to Cartesian coordinates.
#[inline(always)]
pub fn to_xy(u: &[i64; 4]) -> (f64, f64) {
    (
        u[0] as f64 + SQ3_2 * u[1] as f64 + 0.5 * u[2] as f64,
        0.5 * u[1] as f64 + SQ3_2 * u[2] as f64 + u[3] as f64,
    )
}

// ------------------------------------------------------------------ tiling

#[derive(Clone, Copy)]
struct Frame {
    label: u8,
    level: u8,
    r: u8,
    s: u8,
    t: [i64; 4],
}

/// An implicit spectre tiling: a level-`level` supertile of type `label`
/// anchored at the module origin. Nothing is materialized; queries traverse
/// the substitution DAG through static tables.
pub struct Tiling {
    level: usize,
    label: u8,
    msr: Msr,
    rot_c: [[f64; 12]; 2],
    rot_s: [[f64; 12]; 2],
    /// exact leaf AABB per (mirror, rotation), including the Gamma2 companion reach
    leaf_bb: [[[f32; 4]; 12]; 2],
    /// spectre vertex positions per (mirror, rotation): 14 x (x,y)
    verts: [[[(f32, f32); 14]; 12]; 2],
}

impl Tiling {
    /// `level` up to [`tables::MAX_LEVEL`] (32). A level-24 Delta root already
    /// contains ~1.6e21 tiles — effectively infinite for interactive use.
    pub fn new(label: Label, level: usize) -> Self {
        assert!(level <= MAX_LEVEL, "level must be <= {MAX_LEVEL}");
        let msr = Msr::build();
        let mut rot_c = [[0.0; 12]; 2];
        let mut rot_s = [[0.0; 12]; 2];
        let mut verts = [[[(0.0f32, 0.0f32); 14]; 12]; 2];
        let mut leaf_bb = [[[0.0f32; 4]; 12]; 2];
        for s in 0..2 {
            let mx = if s == 1 { -1.0 } else { 1.0 };
            for r in 0..12 {
                let a = r as f64 * std::f64::consts::PI / 6.0;
                rot_c[s][r] = a.cos();
                rot_s[s][r] = a.sin();
                let (mut bb, c, sn) = ([f32::MAX, f32::MAX, f32::MIN, f32::MIN], a.cos(), a.sin());
                for (vi, v) in SPECTRE_VERTS.iter().enumerate() {
                    let u = [v[0] as i64, v[1] as i64, v[2] as i64, v[3] as i64];
                    let (x, y) = to_xy(&u);
                    let xs = mx * x;
                    let (wx, wy) = ((c * xs - sn * y) as f32, (sn * xs + c * y) as f32);
                    verts[s][r][vi] = (wx, wy);
                    bb[0] = bb[0].min(wx);
                    bb[1] = bb[1].min(wy);
                    bb[2] = bb[2].max(wx);
                    bb[3] = bb[3].max(wy);
                }
                leaf_bb[s][r] = bb;
            }
        }
        Self { level, label: label as u8, msr, rot_c, rot_s, leaf_bb, verts }
    }

    /// World-space bounding box of the whole root patch.
    pub fn bounds(&self) -> Aabb {
        let b = LOCAL_AABB[self.level][self.label as usize];
        Aabb::new(b[0], b[1], b[2], b[3])
    }

    /// Vertex positions (local, origin-anchored) of a spectre with the given
    /// mirror flag and rotation.
    pub fn leaf_vertices(&self, s: u8, r: u8) -> &[(f32, f32); 14] {
        &self.verts[s as usize][r as usize]
    }

    /// Static triangulation of the 14-gon (12 triangles), for GPU meshes.
    pub fn triangles() -> &'static [[u16; 3]; 12] {
        &TRIANGLES
    }

    /// Visit every spectre whose AABB intersects `vp`.
    /// The sink receives `(kind, mirror, rotation, x, y)` with `x, y` relative
    /// to `origin` (subtract a nearby origin to preserve f32 precision).
    /// `kind`: 0 = Gamma1, 1 = Gamma2, `label as u8 + 1` otherwise.
    /// Zero heap allocation; fixed stack.
    #[inline]
    pub fn for_each_in<F: FnMut(u8, u8, u8, f64, f64)>(&self, vp: &Aabb, origin: (f64, f64), mut sink: F) {
        let root = Frame { label: self.label, level: self.level as u8, r: 0, s: 0, t: [0; 4] };
        self.for_each_from(root, vp, origin, &mut sink);
    }

    #[inline(always)]
    fn emit_leaf<F: FnMut(u8, u8, u8, f64, f64)>(&self, f: &Frame, vp: &Aabb, origin: (f64, f64), sink: &mut F) {
        let emit_one = |this: &Self, kind: u8, s: u8, r: u8, t: &[i64; 4], sink: &mut F| {
            let bb = &this.leaf_bb[s as usize][r as usize];
            let (x, y) = to_xy(t);
            if x + bb[0] as f64 > vp.max_x
                || x + bb[2] as f64 - vp.min_x < 0.0
                || y + bb[1] as f64 > vp.max_y
                || y + bb[3] as f64 - vp.min_y < 0.0
            {
                return;
            }
            sink(kind, s, r, x - origin.0, y - origin.1);
        };
        if f.label == Label::Gamma as u8 {
            emit_one(self, 0, f.s, f.r, &f.t, sink);
            // Gamma2 companion: node ∘ (rot 30°, translate p8)
            let d = self.msr.apply(f.s as usize, f.r as usize, &GAMMA2_T);
            let t2 = [f.t[0] + d[0], f.t[1] + d[1], f.t[2] + d[2], f.t[3] + d[3]];
            let r2 = if f.s == 1 { (f.r + 12 - GAMMA2_ROT) % 12 } else { (f.r + GAMMA2_ROT) % 12 };
            emit_one(self, 1, f.s, r2, &t2, sink);
        } else {
            emit_one(self, f.label + 1, f.s, f.r, &f.t, sink);
        }
    }

    /// Count tiles intersecting `vp` without producing output.
    pub fn count_in(&self, vp: &Aabb) -> u64 {
        let mut n = 0u64;
        self.for_each_in(vp, (0.0, 0.0), |_, _, _, _, _| n += 1);
        n
    }

    /// Fill `out` (cleared, capacity reused) with packed 16-byte instances.
    pub fn instances_in(&self, vp: &Aabb, origin: (f64, f64), out: &mut Vec<Instance>) {
        out.clear();
        self.for_each_in(vp, origin, |kind, s, r, x, y| {
            out.push(Instance {
                x: x as f32,
                y: y as f32,
                meta: r as u32 | ((s as u32) << 4) | ((kind as u32) << 5),
                color: PALETTE[kind as usize],
            });
        });
    }

    /// Parallel instance generation: splits the root's children across
    /// `threads` OS threads (std only). Order of output is deterministic.
    pub fn instances_in_parallel(&self, vp: &Aabb, origin: (f64, f64), out: &mut Vec<Instance>, threads: usize) {
        if self.level == 0 || threads <= 1 {
            return self.instances_in(vp, origin, out);
        }
        let rule = &RULES[self.label as usize];
        let crot = &CHILD_ROT[self.level - 1];
        let ct = &CHILD_T[self.level - 1];
        let subs: Vec<Frame> = (0..8)
            .filter(|&i| rule[i] != 255)
            .map(|i| {
                let d = self.msr.apply(0, 0, &ct[i]);
                Frame { label: rule[i], level: (self.level - 1) as u8, r: crot[i] % 12, s: 1, t: d }
            })
            .collect();
        let mut results: Vec<Vec<Instance>> = subs.iter().map(|_| Vec::new()).collect();
        std::thread::scope(|scope| {
            for (f, res) in subs.iter().zip(results.iter_mut()) {
                let this = &*self;
                scope.spawn(move || {
                    this.for_each_from(*f, vp, origin, &mut |kind, s, r, x, y| {
                        res.push(Instance {
                            x: x as f32,
                            y: y as f32,
                            meta: r as u32 | ((s as u32) << 4) | ((kind as u32) << 5),
                            color: PALETTE[kind as usize],
                        });
                    });
                });
            }
        });
        out.clear();
        for r in results {
            out.extend_from_slice(&r);
        }
    }

    /// Traverse starting from an explicit frame (used by the parallel splitter).
    #[inline]
    fn for_each_from<F: FnMut(u8, u8, u8, f64, f64)>(&self, root: Frame, vp: &Aabb, origin: (f64, f64), sink: &mut F) {
        let mut stack = [Frame { label: 0, level: 0, r: 0, s: 0, t: [0; 4] }; (MAX_LEVEL + 2) * 8];
        stack[0] = root;
        let mut sp: isize = 0;
        while sp >= 0 {
            let f = stack[sp as usize];
            sp -= 1;
            let bb = &LOCAL_AABB[f.level as usize][f.label as usize];
            let (cx, cy) = ((bb[0] + bb[2]) * 0.5, (bb[1] + bb[3]) * 0.5);
            let (hx, hy) = ((bb[2] - bb[0]) * 0.5, (bb[3] - bb[1]) * 0.5);
            let (su, ru) = (f.s as usize, f.r as usize);
            let (c, sn) = (self.rot_c[su][ru], self.rot_s[su][ru]);
            let mx = if f.s == 1 { -1.0 } else { 1.0 };
            let (m00, m01, m10, m11) = (c * mx, -sn, sn * mx, c);
            let (tx, ty) = to_xy(&f.t);
            let (ncx, ncy) = (m00 * cx + m01 * cy + tx, m10 * cx + m11 * cy + ty);
            let (nhx, nhy) = (m00.abs() * hx + m01.abs() * hy, m10.abs() * hx + m11.abs() * hy);
            if ncx - nhx > vp.max_x || ncx + nhx < vp.min_x || ncy - nhy > vp.max_y || ncy + nhy < vp.min_y {
                continue;
            }
            if f.level == 0 {
                self.emit_leaf(&f, vp, origin, sink);
                continue;
            }
            let rule = &RULES[f.label as usize];
            let crot = &CHILD_ROT[f.level as usize - 1];
            let ct = &CHILD_T[f.level as usize - 1];
            for i in 0..8 {
                if rule[i] == 255 {
                    continue;
                }
                let d = self.msr.apply(su, ru, &ct[i]);
                let nr = if f.s == 1 { (f.r + 12 - crot[i] % 12) % 12 } else { (f.r + crot[i]) % 12 };
                sp += 1;
                stack[sp as usize] = Frame {
                    label: rule[i],
                    level: f.level - 1,
                    r: nr,
                    s: f.s ^ 1,
                    t: [f.t[0] + d[0], f.t[1] + d[1], f.t[2] + d[2], f.t[3] + d[3]],
                };
            }
        }
    }
}

// ---------------------------------------------------------------- hysteresis

/// Viewport cache with hysteresis: regenerates instances only when the live
/// viewport escapes the inner region of the last generated (inflated) region.
pub struct CachedRegion {
    pub margin: f64,
    pub region: Option<Aabb>,
    pub origin: (f64, f64),
    pub instances: Vec<Instance>,
    pub generations: u64,
}

impl CachedRegion {
    pub fn new(margin: f64) -> Self {
        Self { margin, region: None, origin: (0.0, 0.0), instances: Vec::new(), generations: 0 }
    }

    /// Returns `true` if the instance buffer changed (needs GPU re-upload).
    pub fn update(&mut self, tiling: &Tiling, vp: &Aabb, threads: usize) -> bool {
        if let Some(r) = &self.region {
            if r.contains(vp) {
                return false;
            }
        }
        let w = (vp.max_x - vp.min_x) * self.margin;
        let h = (vp.max_y - vp.min_y) * self.margin;
        let region = vp.inflate(w, h);
        let origin = ((region.min_x + region.max_x) * 0.5, (region.min_y + region.max_y) * 0.5);
        if threads > 1 {
            tiling.instances_in_parallel(&region, origin, &mut self.instances, threads);
        } else {
            tiling.instances_in(&region, origin, &mut self.instances);
        }
        self.region = Some(region);
        self.origin = origin;
        self.generations += 1;
        true
    }
}

// ------------------------------------------------------------ exact identity

/// Exact, drift-free tile identity: substitution kind plus the exact pose on
/// the rank-4 integer module. Stable across zoom levels, viewport origins and
/// regenerations — suitable as a hash key for interactive overlays
/// (painting, ownership, game state).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct TileId {
    pub kind: u8,
    pub s: u8,
    pub r: u8,
    pub t: [i64; 4],
}

impl TileId {
    /// World-space anchor (module origin of the tile), exact within f64.
    pub fn anchor(&self) -> (f64, f64) {
        to_xy(&self.t)
    }
}

impl Label {
    pub fn from_index(i: u8) -> Label {
        match i {
            0 => Label::Gamma,
            1 => Label::Delta,
            2 => Label::Theta,
            3 => Label::Lambda,
            4 => Label::Xi,
            5 => Label::Pi,
            6 => Label::Sigma,
            7 => Label::Phi,
            _ => Label::Psi,
        }
    }
}

impl Tiling {
    /// Like [`Tiling::for_each_in`], but hands the sink exact integer-lattice
    /// identities instead of projected coordinates.
    pub fn for_each_ids_in<F: FnMut(TileId)>(&self, vp: &Aabb, mut sink: F) {
        let root = Frame { label: self.label, level: self.level as u8, r: 0, s: 0, t: [0; 4] };
        let mut stack = [Frame { label: 0, level: 0, r: 0, s: 0, t: [0; 4] }; (MAX_LEVEL + 2) * 8];
        stack[0] = root;
        let mut sp: isize = 0;
        let mut emit = |this: &Self, kind: u8, s: u8, r: u8, t: [i64; 4]| {
            let bb = &this.leaf_bb[s as usize][r as usize];
            let (x, y) = to_xy(&t);
            if x + bb[0] as f64 <= vp.max_x
                && x + bb[2] as f64 >= vp.min_x
                && y + bb[1] as f64 <= vp.max_y
                && y + bb[3] as f64 >= vp.min_y
            {
                sink(TileId { kind, s, r, t });
            }
        };
        while sp >= 0 {
            let f = stack[sp as usize];
            sp -= 1;
            let bb = &LOCAL_AABB[f.level as usize][f.label as usize];
            let (cx, cy) = ((bb[0] + bb[2]) * 0.5, (bb[1] + bb[3]) * 0.5);
            let (hx, hy) = ((bb[2] - bb[0]) * 0.5, (bb[3] - bb[1]) * 0.5);
            let (su, ru) = (f.s as usize, f.r as usize);
            let (c, sn) = (self.rot_c[su][ru], self.rot_s[su][ru]);
            let mx = if f.s == 1 { -1.0 } else { 1.0 };
            let (m00, m01, m10, m11) = (c * mx, -sn, sn * mx, c);
            let (tx, ty) = to_xy(&f.t);
            let (ncx, ncy) = (m00 * cx + m01 * cy + tx, m10 * cx + m11 * cy + ty);
            let (nhx, nhy) = (m00.abs() * hx + m01.abs() * hy, m10.abs() * hx + m11.abs() * hy);
            if ncx - nhx > vp.max_x || ncx + nhx < vp.min_x || ncy - nhy > vp.max_y || ncy + nhy < vp.min_y {
                continue;
            }
            if f.level == 0 {
                if f.label == Label::Gamma as u8 {
                    emit(self, 0, f.s, f.r, f.t);
                    let d = self.msr.apply(su, ru, &GAMMA2_T);
                    let t2 = [f.t[0] + d[0], f.t[1] + d[1], f.t[2] + d[2], f.t[3] + d[3]];
                    let r2 = if f.s == 1 { (f.r + 12 - GAMMA2_ROT) % 12 } else { (f.r + GAMMA2_ROT) % 12 };
                    emit(self, 1, f.s, r2, t2);
                } else {
                    emit(self, f.label + 1, f.s, f.r, f.t);
                }
                continue;
            }
            let rule = &RULES[f.label as usize];
            let crot = &CHILD_ROT[f.level as usize - 1];
            let ct = &CHILD_T[f.level as usize - 1];
            for i in 0..8 {
                if rule[i] == 255 {
                    continue;
                }
                let d = self.msr.apply(su, ru, &ct[i]);
                let nr = if f.s == 1 { (f.r + 12 - crot[i] % 12) % 12 } else { (f.r + crot[i]) % 12 };
                sp += 1;
                stack[sp as usize] = Frame {
                    label: rule[i],
                    level: f.level - 1,
                    r: nr,
                    s: f.s ^ 1,
                    t: [f.t[0] + d[0], f.t[1] + d[1], f.t[2] + d[2], f.t[3] + d[3]],
                };
            }
        }
    }

    /// Exact identity of the tile containing world point `(x, y)`, or `None`
    /// if the point lies outside the patch. Point-in-polygon over the (few)
    /// candidates whose AABB covers the point.
    pub fn pick(&self, x: f64, y: f64) -> Option<TileId> {
        let vp = Aabb::new(x, y, x, y);
        let mut hit: Option<TileId> = None;
        self.for_each_ids_in(&vp, |id| {
            if hit.is_some() {
                return;
            }
            let (tx, ty) = id.anchor();
            let verts = self.leaf_vertices(id.s, id.r);
            let (px, py) = (x - tx, y - ty);
            let mut inside = false;
            let mut j = 13usize;
            for i in 0..14 {
                let (xi, yi) = (verts[i].0 as f64, verts[i].1 as f64);
                let (xj, yj) = (verts[j].0 as f64, verts[j].1 as f64);
                if (yi > py) != (yj > py) && px < (xj - xi) * (py - yi) / (yj - yi) + xi {
                    inside = !inside;
                }
                j = i;
            }
            if inside {
                hit = Some(id);
            }
        });
        hit
    }
}
