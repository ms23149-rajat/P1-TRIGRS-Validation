# TRIGRS Validation Summary

## Overview
TRIGRS (Transient Rainfall Infiltration and Grid-Based Regional Slope Stability
Analysis) was installed and compiled successfully. Four benchmark test cases
included in the TRIGRS v2.1 distribution (Tutorial, MinorCreek, Flume, and
Srivastava & Yeh 1991) were executed to check installation correctness and
physical plausibility of the infiltration and factor-of-safety calculations.

**Validation status:** The benchmark distribution does not include independent
reference output (expected-result grids or published numerical values) for any
of the four test cases on this system. Re-downloading the USGS OFR 2008-1159
tutorial package (which ships Appendix-2 expected-output grids) was attempted
but blocked by the lab network proxy (404/500 errors from pubs.usgs.gov). As a
result, three of the four tests below are **qualitative checks of physical
plausibility only** — they confirm TRIGRS ran correctly and produced
internally consistent, physically reasonable output, but do not constitute a
quantitative match against an external reference. The SY91 test is the
exception: it is checked quantitatively against analytically known
steady-state pressure-head values.

---

## 1. Tutorial Test

### Objective
Check slope-stability calculations on the synthetic 10 x 10 grid bundled with
the distribution.

### Results
* Minimum FoS at 2 days = 1.167
* Minimum FoS at 2.5 days = 0.9817

### Validation basis
**Qualitative only.** No reference output grids were available for this run
(the USGS distribution's Appendix-2 expected-output grids could not be
downloaded). The result was checked against the *described behaviour* in
Baum et al. (2008) Figure 2-3: rainfall infiltration should raise pore
pressure and reduce FoS, with some cells dropping below FoS=1 by the end of
the storm. The observed trend (FoS dropping from >1 to <1 between day 2 and
day 2.5) is consistent with this description.

### Observation
Rainfall infiltration increased pore-water pressure and reduced slope
stability. Several cells crossed the failure threshold (FoS < 1), consistent
with the qualitative behaviour described in the TRIGRS manual for this dataset.

---

## 2. MinorCreek Test

### Objective
Check rainfall-induced slope instability over a long simulation period,
reproducing the setup described by Iverson (2000) and Baum et al. (2008).

### Results
* Initial minimum FoS = 1.0123
* Final minimum FoS = 0.9911
* Simulation duration = 84 days

### Validation basis
**Qualitative only.** No digitised reference curve from Iverson (2000) or
Baum et al. (2008) was available on this system for a point-by-point
comparison. The result was checked for the *correct qualitative behaviour*
described in those papers: progressive FoS decline under sustained rainfall,
approaching but not necessarily crossing FoS=1.

### Observation
Factor of Safety decreased throughout the profile during the simulation,
consistent with the expected long-duration rainfall response. A quantitative
comparison against Iverson's (2000) published pressure-head and FoS curves
was not performed.

---

## 3. Flume Test

### Objective
Check TRIGRS behaviour against the configuration of the USGS debris-flow flume
experiment described by Iverson (2000) and Baum et al. (2008).

### Results
* FoS decreased with depth.
* FoS remained greater than 1 throughout the profile.

### Validation basis
**Qualitative only.** No digitised reference curve from Iverson (2000) was
available for comparison. The result was checked for the qualitative pattern
described in the source paper (FoS decreasing with depth, no failure under
the tested flux).

### Observation
The lower part of the profile was less stable than the surface, and no
failure occurred under the experimental conditions tested — consistent with
the qualitative description in Iverson (2000), but not quantitatively verified
against the published curves.

---

## 4. Srivastava and Yeh (1991) Test

### Objective
Check the unsaturated infiltration formulation against analytically known
steady-state pressure-head values.

### Results
| Time (h) | Surface Pressure Head psi(Z=0) (m) |
| -------- | ----------------------------------- |
| 0        | -23.022                              |
| 10       | -1.913                               |
| 20       | -1.286                               |
| 40       | -1.081                               |

### Validation basis
**Quantitative, against analytically derived steady-state values** (not the
S&Y 1991 Figure 3 curves directly — see note below):

* The Gardner (1958) exponential conductivity model gives a closed-form
  uniform steady-state pressure head for a given surface flux:
  psi_ss = (1/alpha) * ln(Iz/Ks).
* For the initial background flux Iz0=0.1 m/h: psi_ss_old = -23.026 m.
  TRIGRS t=0 surface value = -23.022 m (**0.017% error**). PASS.
* For the rainfall flux Iz=0.9 m/h: psi_ss_new = -1.054 m. TRIGRS t=40h
  surface value = -1.081 m (**2.55% error**). This is consistent with the
  surface still asymptotically approaching the new steady state at t=40h
  (the wetting front has not fully equilibrated) rather than a model error.
* Wetting front propagates downward monotonically with time (surface psi
  increases from -23.022 -> -1.913 -> -1.286 -> -1.081 m over t=0,10,20,40h). PASS.
* Water table (Z=100m) is held at psi=0 throughout all time steps
  (max deviation < 1e-6 m). PASS.

**A direct quantitative comparison against the S&Y (1991) Figure 3 curves
(the stated purpose of this test, per the TRIGRS manual) was not achieved.**
The S&Y semi-infinite analytical solution (eq. A-17, erfc-based) is degenerate
for this parameter set because alpha*L = 0.1 x 100 = 10 >> 1, causing the
exp(alpha*z) term to overflow. Reproducing TRIGRS's exact internal algorithm
(Baum et al. 2008 eq. 8B eigenfunction series with S&Y's upward-z convention)
was attempted but not completed. This remains **validation pending**.

### Observation
Pressure head became progressively less negative with time, indicating
wetting of the soil profile, with the surface approaching the analytically
predicted new steady state. Factor of Safety remained constant (FS=10,
the program's capped maximum) because the slope angle was zero, so no
FoS-based check is meaningful for this test.

---

## Conclusion

* TRIGRS was installed and compiled correctly.
* TopoIndex preprocessing worked correctly.
* All four benchmark cases ran to completion without errors.
* The SY91 test passes 3 of 4 quantitative physical checks against
  analytically known steady-state values (errors <0.02% on two checks);
  the fourth check shows a 2.55% deviation consistent with expected
  transient lag rather than a model defect.
* A direct comparison against the S&Y (1991) Figure 3 curves was not
  completed — **validation pending**.
* Tutorial, MinorCreek, and Flume tests show output that is qualitatively
  consistent with the behaviour described in Baum et al. (2008) and
  Iverson (2000), but **no quantitative reference data was available** on
  this system for point-by-point comparison — **validation pending** for
  these three tests.

The installation and basic operation of TRIGRS are confirmed. Quantitative
benchmark validation against published reference data remains incomplete and
is documented here as an open item, per project plan guidance that an honest
"validation pending / partial" status is an acceptable output of this phase.
