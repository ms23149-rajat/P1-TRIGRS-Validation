# P1-TRIGRS Validation
## Overview

This repository documents the installation, compilation, benchmark testing, and validation of TRIGRS (Transient Rainfall Infiltration and Grid-Based Regional Slope Stability Analysis) as part of the IIT Kanpur SURGE 2026 Project P1.

## Repository Structure

```text
P1-TRIGRS-Validation/
├── benchmark_tests/
│   ├── Tutorial/
│   ├── MinorCreek/
│   ├── Flume/
│   └── SY91/
├── results/
│   ├── Tutorial/
│   ├── MinorCreek/
│   ├── Flume/
│   └── SY91/
├── docs/
├── figures/
├── scripts/
└── README.md
```
## Validation Tests

Four benchmark tests were executed to verify the correct installation and operation of TRIGRS.

### 1. Tutorial Test

**Objective**

* Validate TRIGRS on a synthetic 10 × 10 grid.

**Result**

* Minimum FoS at 2 days = 1.167
* Minimum FoS at 2.5 days = 0.9817

**Observation**

* Rainfall infiltration increased pore-water pressure and reduced slope stability.
* Several cells reached FoS < 1, indicating potential instability.

### 2. MinorCreek Test

**Objective**

* Validate TRIGRS using the MinorCreek rainfall-induced landslide benchmark.

**Result**

* Initial minimum FoS = 1.0123
* Final minimum FoS = 0.9911

**Observation**

* Factor of Safety decreased throughout the soil profile during the 84-day simulation.
* Long-duration rainfall progressively reduced slope stability.
* The deepest portion of the profile reached FoS < 1, indicating potential failure initiation.

### 3. Flume Test

**Objective**

* Validate TRIGRS against the USGS experimental debris-flow flume benchmark.

**Result**

* FoS decreased with depth.
* FoS remained greater than 1 throughout the profile.

**Observation**

* Stability decreased from the surface toward deeper layers.
* No failure occurred under the specified experimental conditions.
* TRIGRS successfully reproduced laboratory-scale infiltration and stability behaviour.

### 4. Srivastava and Yeh (1991) Test

**Objective**

* Validate the unsaturated infiltration formulation implemented in TRIGRS.

**Result**

| Time | Surface Pressure Head |
| ---- | --------------------- |
| 0    | -23.022               |
| 10   | -1.913                |
| 20   | -1.286                |
| 40   | -1.081                |

**Observation**

* Pressure head became progressively less negative with time.
* Soil suction decreased as infiltration progressed.
* Factor of Safety remained constant at 10 because the slope angle was 0°.
* This benchmark validates infiltration physics rather than slope stability calculations.

## Overall Conclusion

The successful completion of all four benchmark tests demonstrates that:

* TRIGRS was installed and compiled correctly.
* Benchmark datasets executed successfully.
* Saturated infiltration simulations produced physically consistent results.
* Unsaturated infiltration simulations reproduced expected behaviour.
* The generated outputs matched the expected trends reported in benchmark studies.

These results confirm that the TRIGRS installation is functioning correctly and is ready for further landslide susceptibility and slope stability studies.
