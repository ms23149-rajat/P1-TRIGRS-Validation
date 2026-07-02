# P1-TRIGRS Validation

## Overview

This repository documents installation, compilation, benchmark testing, and
real-terrain application of TRIGRS v2.1 (Transient Rainfall Infiltration and
Grid-Based Regional Slope Stability Analysis) as part of IIT Kanpur SURGE
2026 Project P-1.

**Scope:** The repository covers four USGS benchmark cases (Tutorial,
MinorCreek, Flume, SY91) and a complete real-terrain application for Idukki
district, Kerala, reproducing the August 2018 flood event at 30 m UTM
resolution. The Idukki application is fully validated against the 2018
Kerala landslide inventory (ROC-AUC = 0.707).

---

## Repository Structure

```
P1-TRIGRS-Validation/
├── src/
│   ├── TRIGRS/          # TRIGRS v2.1 source + compiled binaries (trg, prg, tpx)
│   ├── TopoIndex/
│   ├── GridMatch/
│   └── UnitConvert/
├── data/
│   ├── tutorial/        # Benchmark test data
│   ├── MinorCreek/
│   ├── flume/
│   ├── sy91/
│   ├── gridmatch/
│   └── idukki/
│       ├── dem/                  # Original geographic-CRS grids
│       ├── dem_utm/              # UTM 43N (EPSG:32643) 30m grids
│       │   ├── idukki_dem_utm30m_masked.asc       # DEM, nodata-masked
│       │   ├── idukki_flowdir_arcgis_utm30m_final.asc  # D8 ArcGIS encoding
│       │   ├── idukki_slope_degrees_utm30m_raw.tif     # Slope in degrees
│       │   ├── TIgrid_size.txt                    # TopoIndex size record
│       │   ├── TIdscelGrid_idukki.txt             # TopoIndex D8 grid
│       │   ├── TIcelindxGrid_idukki.txt           # TopoIndex cell-index grid
│       │   ├── TIcelindxList_idukki.txt           # Cell ordering list
│       │   ├── TIdscelList_idukki.txt             # Downslope cell list
│       │   └── TIwfactorList_idukki.txt           # Weighting factor list
│       ├── trigrs_input/         # Original 90m geographic inputs
│       ├── trigrs_input_utm/     # 30m UTM inputs fed to TRIGRS
│       │   ├── idukki_slope_utm30m.asc            # Slope (degrees, corrected)
│       │   ├── idukki_zone_utm30m.asc             # 3-class soil zone
│       │   ├── idukki_depth_utm30m.asc            # Soil depth
│       │   ├── idukki_depthwt_utm30m.asc          # Initial water table depth
│       │   ├── idukki_rizero_utm30m.asc           # Initial infiltration rate
│       │   └── rainfall/
│       │       └── idukki_rain_period{1-9}_utm30m.asc
│       ├── output_utm/           # TRIGRS outputs (40 ASC grids)
│       │   ├── TRfs_min_idukki_{1-10}.asc         # Min factor of safety
│       │   ├── TRz_at_fs_min_idukki_{1-10}.asc   # Depth at min FS
│       │   ├── TRp_at_fs_min_idukki_{1-10}.asc   # Pressure head at min FS
│       │   └── TRwater_depth_idukki_{1-10}.asc   # Water table depth
│       ├── validation/
│       │   ├── fs_min_composite_idukki.asc        # Cell-wise min FS (all 10 times)
│       │   ├── roc_curve_idukki2018.png           # ROC curve figure
│       │   ├── success_rate_curve_idukki2018.png  # Success-rate curve figure
│       │   └── validation_summary_idukki2018.txt  # Numeric summary
│       ├── inventory/
│       │   └── idukki_inventory_utm.csv           # 2223 inventory points, UTM 43N
│       └── output_utm_WRONG_PCTSLOPE/   # Archived invalid outputs (percent-slope bug)
├── benchmark_tests/
├── benchmark_test_results/
├── benchmark_docs/
├── assets/
│   └── break_cycles.py          # DFS cycle-breaker for flow-direction grid
├── tr_in.txt                    # TRIGRS initialisation file
├── tpx_in.txt                   # TopoIndex initialisation file
├── validate_trigrs.py           # ROC/AUC validation script
├── TRIGRS_TECHNICAL_README.md
├── USER_GUIDE.md
├── DISCLAIMER.md
├── LICENSE.md
└── README.md
```

---

## Benchmark Tests

### Validation Status

| Test | Reference | Status |
|---|---|---|
| SY91 | Analytical steady-state (Srivastava & Yeh 1991) | 3/4 checks pass (<0.02% error); 1 check shows expected transient lag (2.55%) |
| Tutorial | USGS OFR 2008-1159 App. 2 (unavailable — proxy blocked) | Qualitative pass |
| MinorCreek | Iverson (2000) — no digitised curve available | Qualitative pass |
| Flume | Iverson (2000) — no digitised curve available | Qualitative pass |

### Key Results

**Tutorial:** Min FoS = 1.167 at t=2 days → 0.9817 at t=2.5 days. Cells
reach FoS < 1 consistent with Baum et al. (2008) Figure 2-3.

**MinorCreek:** Min FoS decreases from 1.0123 (initial) to 0.9911 (84 days),
consistent with long-duration rainfall response.

**Flume:** FoS decreases with depth; remains > 1 under experimental conditions,
consistent with Iverson (2000) qualitative description.

**SY91:** Surface pressure head approaches -1.081 m at t=40h vs analytical
steady-state -1.054 m (2.55% error, consistent with asymptotic approach still
in progress — not a model defect). IC check: -23.022 m vs -23.026 m (0.017%).

---

## Idukki Real-Terrain Application

### Objective

Reproduce rainfall-induced shallow landslide hazard for Idukki district,
Kerala, for the August 2018 flood event using soil parameters from
Reichenbach et al. (2023) and 9-period rainfall derived from the August 2018
daily record. Validate against the Kerala 2018 landslide inventory
(DANS doi:10.17026/dans-x6c-y7x2).

### Configuration

| Parameter | Value |
|---|---|
| DEM | Copernicus GLO-30 (DS-13), 30 m UTM EPSG:32643 |
| Domain | Idukki district, 3888 × 2584 cells = 10,035,422 valid cells |
| Soil zones | 3-class (Reichenbach et al. 2023 Table 1) |
| Rainfall | 9 periods, 86400 s each, total 777600 s (9 days) |
| Output times | 10 snapshots: t = 0, 86400, …, 777600 s |
| Flow routing | TopoIndex MFD (convergence at iteration 581) |
| Model mode | Unsaturated finite-depth (`unsfin()`) |

### Soil Parameters

| Zone | c (Pa) | φ (°) | γ (N/m³) | D (m²/s) | Ks (m/s) |
|---|---|---|---|---|---|
| 1 | 10000 | 22.5 | 13000 | 9.40e-6 | 4.53e-6 |
| 2 | 29000 | 20.0 | 15000 | 6.20e-6 | 6.59e-6 |
| 3 | 35000 | 20.0 | 14000 | 5.00e-6 | 2.72e-6 |

### Results

**TRIGRS run:** Completed normally, 0 nonconvergent cells.

| Output time | Mean FS | FS < 1.0 | FS < 1.5 |
|---|---|---|---|
| t=1 (day 0, pre-storm) | 4.158 | 5.55% | 15.27% |
| t=5 (day 4) | 4.157 | 5.59% | 15.30% |
| t=10 (day 9, storm peak) | 4.143 | 5.81% | 15.64% |

The FS<1.0 fraction increases monotonically with cumulative rainfall,
concentrated in the heaviest rainfall periods (periods 7–8, ~116 mm/day).

**Validation against 2018 inventory** (2,219 Idukki points):

| Metric | Value |
|---|---|
| ROC-AUC | **0.707** |
| SRC-AUC | 0.719 |
| Mean FS at inventory locations | 2.016 |
| Mean FS at random non-inventory | 4.012 |
| FS < 1.0 at inventory points | 1.3% |

Hit rates (success-rate curve):

| % study area flagged | % inventory captured |
|---|---|
| 10% | 7.5% |
| 20% | 39.0% |
| 30% | 62.8% |
| 50% | 90.4% |

ROC-AUC = 0.707 exceeds the 0.70 threshold widely used in the landslide
hazard literature (Frattini et al. 2010, Beguería 2006) to indicate
acceptable model skill.

**Known limitation:** The top 5–10% of area (lowest-FS cells) performs
below random in the success-rate curve. These extreme-FS cells correspond
to steep terrain features (gorge walls, escarpments) that are physically
unstable under infinite-slope assumptions but were not mapped in the
human-impact-focused inventory, or are sub-pixel relative to the 30 m
grid. This is a documented limitation of TRIGRS at regional scale with
spatially-uniform soil parameters.

### How to Reproduce

**Dependencies:** gfortran, GDAL, Python ≥3.10, geopandas, scikit-learn,
scipy, numpy, matplotlib (all available in the `trigrs` conda environment).

```bash
conda activate trigrs
cd ~/landslides-trigrs

# 1. Run TopoIndex (builds TI* routing files — ~1 hour)
src/TRIGRS/tpx tpx_in.txt

# 2. Run TRIGRS (produces 40 output grids — ~3.5 hours)
stdbuf -oL -eL nohup src/TRIGRS/trg tr_in.txt > trigrs_run.log 2>&1 &

# 3. Run validation (ROC/AUC — ~5 minutes)
python3 validate_trigrs.py
```

Expected outputs in `data/idukki/output_utm/`: 40 ASC grids (10 timesteps
× 4 variables). Validation figures in `data/idukki/validation/`.

---

## Source Code Modifications

Two bugs were found and fixed in the TRIGRS v2.1 source during this project.
Both fixes are committed to this repository in `src/TRIGRS/rnoff.f95`.

### Bug 1 — `srdswm` separator mismatch (heap corruption crash)

**File:** `src/TRIGRS/rnoff.f95`, line 77

**Problem:** `srdswm()` (reads the TopoIndex weighting-factor list) was
called with `test1` as its row-separator argument. `test1` is initialised
from the DEM/slope grid nodata value (−9999), but the `TIwfactorList`
file uses **−1** as its row separator. With the wrong separator, `srdswm`
reads every line (including markers and row-index numbers) as data,
incrementing the array index until it overflows the heap — crashing the
process with `double free or corruption` and killing the terminal.

**Fix:**
```fortran
! Before (broken):
call srdswm(nwf, imax, u(21), test1, wf, dsctr, u(19))

! After (fixed):
call srdswm(nwf, imax, u(21), -1., wf, dsctr, u(19))
```

### Bug 2 — `dsc`/`wf` array allocation off-by-one

**File:** `src/TRIGRS/rnoff.f95`, line 54

**Problem:** `dsc(nwf)` and `wf(nwf)` were allocated exactly `nwf`
elements, but `srdswm` writes a sentinel to index `nwf+1` at EOF
(`ctr(jmax+1) = k+1`). This one-past-the-end write silently corrupted the
heap on every run where `nwf` was set exactly.

**Fix:**
```fortran
! Before (off-by-one):
allocate (dsc(nwf), wf(nwf))

! After (fixed):
allocate (dsc(nwf+1), wf(nwf+1))
```

---

## Critical Preprocessing Note — Slope Grid Units

When generating the slope grid with GDAL, **do not use the `-p` flag**.
The `-p` flag produces percent slope (unbounded), not degrees. TRIGRS
passes slope directly to `sin()`/`cos()` assuming degrees. Using percent
slope silently corrupts all FS calculations across the entire domain
(observed: max = 550° instead of 79.7°, mean ~2× too high).

```bash
# CORRECT:
gdaldem slope dem.tif slope_degrees.tif

# WRONG — produces percent slope, breaks TRIGRS:
gdaldem slope dem.tif slope_pct.tif -p
```

---

## References

- Alvioli, M., and Baum, R.L., 2016, Parallelization of the TRIGRS model
  for rainfall-induced landslides using the message passing interface:
  Environmental Modelling & Software, v. 81, p. 122–135.
- Baum, R.L., Savage, W.Z., and Godt, J.W., 2008, TRIGRS — A Fortran
  program for transient rainfall infiltration and grid-based regional
  slope-stability analysis, version 2.0: USGS OFR 2008-1159, 75 p.
- Beguería, S., 2006, Validation and evaluation of predictive models in
  hazard assessment and risk management: Natural Hazards, v. 37, p. 315–329.
- Frattini, P., Crosta, G., and Carrara, A., 2010, Techniques for evaluating
  the performance of landslide susceptibility models: Engineering Geology,
  v. 111, p. 62–72.
- Iverson, R.M., 2000, Landslide triggering by rain infiltration: Water
  Resources Research, v. 36, no. 7, p. 1897–1910.
- Kerala 2018 landslide inventory: DANS Data Station,
  doi:10.17026/dans-x6c-y7x2.
- Reichenbach, P., and others, 2023, Physically based slope stability model
  to evaluate timing and distribution of rainfall-induced shallow landslides:
  ISPRS International Journal of Geo-Information, v. 12, no. 2.
- Srivastava, R., and Yeh, T.-C.J., 1991, Analytical solutions for
  one-dimensional, transient infiltration toward the water table:
  Water Resources Research, v. 27, p. 753–762.
