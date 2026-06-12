# P1-TRIGRS Validation

## Overview

This repository documents the installation, compilation, and benchmark
testing of TRIGRS (Transient Rainfall Infiltration and Grid-Based Regional
Slope Stability Analysis) as part of the IIT Kanpur SURGE 2026 Project P1.

**Scope note:** This repository covers installation and the four benchmark
test cases bundled with the TRIGRS v2.1 distribution (Tutorial, MinorCreek,
Flume, SY91). It does not cover the separate real-terrain application
exercise (Wayanad/Idukki, 2018 event), which is documented elsewhere as an
independent, ongoing effort with its own status.

## Repository Structure

```
P1-TRIGRS-Validation/
├── benchmark_tests/
│   ├── Tutorial/
│   ├── MinorCreek/
│   ├── Flume/
│   └── SY91/
├── benchmark_test_results/
│   ├── Tutorial/
│   ├── MinorCreek/
│   ├── Flume/
│   └── SY91/
├── benchmark_docs/
│   └── Validation_Summary.md
├── figures/
├── scripts/
└── README.md
```

## Validation Status (summary)

The four benchmark cases ran to completion without errors, confirming the
TRIGRS installation, compilation, and TopoIndex preprocessing are working
correctly. **Validation against external reference data is partial**, as
detailed in [`benchmark_docs/Validation_Summary.md`](benchmark_docs/Validation_Summary.md):

| Test | Quantitative reference available? | Status |
| --- | --- | --- |
| SY91 | Yes — analytically derived steady-state values | 3/4 checks pass (<0.02% error); 1 check shows expected transient lag (2.55%) |
| Tutorial | No (USGS Appendix-2 grids unreachable — proxy blocked) | Qualitative pass only — validation pending |
| MinorCreek | No digitised reference available | Qualitative pass only — validation pending |
| Flume | No digitised reference available | Qualitative pass only — validation pending |

A direct comparison against the Srivastava & Yeh (1991) Figure 3 curves —
the stated purpose of the SY91 test — was attempted but not completed,
because the S&Y semi-infinite analytical solution is degenerate for this
parameter set (alpha\*L = 10). This is documented as **validation pending**
in `Validation_Summary.md`.

## Validation Tests

### 1. Tutorial Test

**Objective**
- Check slope-stability calculations on the synthetic 10 x 10 grid bundled
  with the distribution.

**Result**
- Minimum FoS at 2 days = 1.167
- Minimum FoS at 2.5 days = 0.9817

**Validation basis**
- Qualitative only. No reference output grids were available (the USGS
  OFR 2008-1159 Appendix-2 expected-output package could not be downloaded
  — blocked by the lab network proxy). The result was checked against the
  *described behaviour* in Baum et al. (2008) Figure 2-3.

**Observation**
- Rainfall infiltration increased pore-water pressure and reduced slope
  stability. Several cells reached FoS < 1, consistent with the qualitative
  behaviour described in the manual for this dataset.

### 2. MinorCreek Test

**Objective**
- Check rainfall-induced slope instability over a long simulation period,
  reproducing the setup described by Iverson (2000) and Baum et al. (2008).

**Result**
- Initial minimum FoS = 1.0123
- Final minimum FoS = 0.9911
- Simulation duration = 84 days

**Validation basis**
- Qualitative only. No digitised reference curve from Iverson (2000) was
  available for point-by-point comparison.

**Observation**
- Factor of Safety decreased throughout the profile during the simulation,
  consistent with the expected long-duration rainfall response. A
  quantitative comparison against Iverson's published curves was not
  performed.

### 3. Flume Test

**Objective**
- Check TRIGRS behaviour against the configuration of the USGS debris-flow
  flume experiment described by Iverson (2000).

**Result**
- FoS decreased with depth.
- FoS remained greater than 1 throughout the profile.

**Validation basis**
- Qualitative only. No digitised reference curve from Iverson (2000) was
  available for comparison.

**Observation**
- The lower part of the profile was less stable than the surface, and no
  failure occurred under the experimental conditions tested — consistent
  with the qualitative pattern in Iverson (2000), but not quantitatively
  verified.

### 4. Srivastava and Yeh (1991) Test

**Objective**
- Check the unsaturated infiltration formulation against analytically known
  steady-state pressure-head values.

**Result**

| Time (h) | Surface Pressure Head psi(Z=0) (m) |
| --- | --- |
| 0 | -23.022 |
| 10 | -1.913 |
| 20 | -1.286 |
| 40 | -1.081 |

**Validation basis**

Quantitative, against analytically derived steady-state values
(`psi_ss = (1/alpha) * ln(Iz/Ks)`, Gardner 1958 exponential model):

- IC vs. uniform SS under Iz0=0.1 m/h: TRIGRS = -23.022 m, analytical =
  -23.026 m -> **0.017% error**. PASS.
- t=40h surface vs. uniform SS under Iz=0.9 m/h: TRIGRS = -1.081 m,
  analytical = -1.054 m -> **2.55% error**. Consistent with the surface
  still asymptotically approaching the new steady state (wetting front not
  yet fully equilibrated), not a model defect.
- Wetting front propagates downward monotonically with time. PASS.
- Water table (Z=100m) held at psi=0 throughout (max deviation < 1e-6 m). PASS.

A direct comparison against the S&Y (1991) Figure 3 curves — the stated
purpose of this test per the TRIGRS manual — was **not achieved** (S&Y's
semi-infinite erfc solution is degenerate for alpha\*L=10). This remains
**validation pending**. See `Validation_Summary.md` for full detail.

**Observation**
- Pressure head became progressively less negative with time, indicating
  wetting of the soil profile, with the surface approaching the
  analytically predicted new steady state. Factor of Safety remained
  constant at the program's capped maximum (10) because the slope angle
  was zero, so no FoS-based check is meaningful for this test.

## Overall Conclusion

- TRIGRS was installed and compiled correctly.
- TopoIndex preprocessing worked correctly.
- All four benchmark cases ran to completion without errors.
- The SY91 test passes 3 of 4 quantitative checks against analytically known
  steady-state values; the fourth shows a deviation consistent with expected
  transient behaviour rather than a defect.
- Quantitative comparison against the S&Y (1991) Figure 3 curves, and against
  reference data for Tutorial, MinorCreek, and Flume, was **not completed** and
  is documented as **validation pending**.

The installation and basic operation of TRIGRS are confirmed. Quantitative
benchmark validation against published reference data remains an open item,
documented honestly per project guidance that "validation pending / partial"
is an acceptable status for this phase.

## References

- Baum, R.L., Savage, W.Z., and Godt, J.W., 2008, TRIGRS-A Fortran program for
  transient rainfall infiltration and grid-based regional slope-stability
  analysis, version 2.0: U.S. Geological Survey Open-File Report 2008-1159, 75 p.
- Alvioli, M., and Baum, R.L., 2016, Parallelization of the TRIGRS model for
  rainfall-induced landslides using the message passing interface:
  Environmental Modelling & Software, v. 81, p. 122-135.
- Iverson, R.M., 2000, Landslide triggering by rain infiltration: Water
  Resources Research, v. 36, no. 7, p. 1897-1910.
- Srivastava, R., and Yeh, T.-C.J., 1991, Analytical solutions for
  one-dimensional, transient infiltration toward the water table in
  homogeneous and layered soils: Water Resources Research, v. 27, p. 753-762.
