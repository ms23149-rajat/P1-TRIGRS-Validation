# TRIGRS Validation Summary

## Overview

TRIGRS (Transient Rainfall Infiltration and Grid-Based Regional Slope Stability Analysis) was installed, compiled, and validated using the benchmark datasets provided with the software distribution.

Four benchmark tests were executed to verify the correct implementation of infiltration, pore-pressure computation, and factor-of-safety calculations.

---

## 1. Tutorial Test

### Objective

Validate slope stability calculations on a synthetic 10 × 10 grid.

### Results

* Minimum FoS at 2 days = 1.167
* Minimum FoS at 2.5 days = 0.9817

### Observation

Rainfall infiltration increased pore-water pressure and reduced slope stability. Several cells crossed the failure threshold (FoS < 1), indicating potential instability.

---

## 2. MinorCreek Test

### Objective

Validate rainfall-induced slope instability over a long simulation period.

### Results

* Initial minimum FoS = 1.0123
* Final minimum FoS = 0.9911
* Simulation duration = 84 days

### Observation

Factor of Safety decreased throughout the profile during the simulation. Long-duration rainfall progressively reduced stability until failure conditions were reached.

---

## 3. Flume Test

### Objective

Validate TRIGRS against a controlled USGS debris-flow flume experiment.

### Results

* FoS decreased with depth.
* FoS remained greater than 1 throughout the profile.

### Observation

The lower part of the profile was less stable than the surface. No failure occurred under the experimental conditions.

---

## 4. Srivastava and Yeh (1991) Test

### Objective

Validate the unsaturated infiltration formulation.

### Results

| Time | Surface Pressure Head |
| ---- | --------------------- |
| 0    | -23.022               |
| 10   | -1.913                |
| 20   | -1.286                |
| 40   | -1.081                |

### Observation

Pressure head became progressively less negative with time, indicating wetting of the soil profile. Factor of Safety remained constant because the slope angle was zero.

---

## Conclusion

The successful completion of all benchmark tests confirms that:

* TRIGRS was installed correctly.
* Compilation was successful.
* TopoIndex preprocessing worked correctly.
* Saturated and unsaturated infiltration calculations behaved as expected.
* Output results matched benchmark trends and expected physical behaviour.

The model is ready for further landslide and slope-stability applications.
