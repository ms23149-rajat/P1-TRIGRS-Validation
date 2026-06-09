# Wayanad TRIGRS Implementation Summary

## Current Status

### Completed

* Wayanad DEM preprocessing completed
* Slope generation completed
* Flow accumulation generation completed
* Flow direction generation completed
* TRIGRS successfully executed on Wayanad DEM
* FoS rasters generated
* Stability classification completed
* Results committed to GitHub

### Next Phase

* Obtain Wayanad geotechnical parameters
* Obtain Wayanad rainfall datasets
* Build rainfall-triggered TRIGRS scenarios
* Compare model results with observed landslide events

---

# Objective

Implement the TRIGRS slope-stability model on a real-world study area (Wayanad, Kerala) using open-source terrain data and verify the complete preprocessing and execution workflow.

---

# Data Used

## DEM

Source: Copernicus GLO-30

Resolution: ~30 m

Study Area: Wayanad, Kerala

Grid Size:

* Rows: 360
* Columns: 360
* Total Cells: 129,600

---

# Preprocessing Completed

## Terrain Products Generated

* DEM
* Slope raster
* Flow accumulation raster
* Flow direction raster

## Tools Used

* GDAL
* GRASS GIS
* TRIGRS

---

# Flow Direction Investigation

Several flow-direction products were tested:

1. GRASS drainage raster
2. D8 flow directions
3. ESRI-style D8 directions
4. TopoIndex-compatible directions

## Purpose

To determine whether runoff routing could be implemented through TopoIndex.

---

# TopoIndex Investigation

## Issue Encountered

TopoIndex repeatedly stopped during:

"Correcting cell index numbers"

without producing valid routing outputs.

## Tests Performed

* GRASS-generated flow directions
* Python D8 conversion
* ESRI D8 conversion
* Multiple direction-numbering schemes
* Increased iteration limits
* Loop diagnostics

## Observation

Flow-direction networks produced non-converging behavior within TopoIndex.

## Decision

TopoIndex was not used for the current Wayanad implementation.

## Justification

TRIGRS supports operation without runoff-routing files when:

```text
nxtfil = none
ndxfil = none
dscfil = none
wffil = none
```

This allows infiltration and FoS calculations to proceed normally.

---

# TRIGRS Execution

## Status

SUCCESSFUL

Model completed without errors.

---

# Parameters Used

Current simulation uses:

**Srivastava & Yeh (1991) benchmark parameters**

These are not Wayanad-specific soil properties.

---

# Rainfall Forcing

Current run:

```text
rifil = none
```

Therefore:

* No rainfall forcing
* No transient infiltration event
* Baseline stability assessment only

---

# Results

## Factor of Safety Statistics

| Metric      | Value  |
| ----------- | ------ |
| Minimum FoS | 0.3414 |
| Mean FoS    | 2.5844 |
| Maximum FoS | 10.0   |

## Stability Classes

| FoS Range        |  Cells | Percentage |
| ---------------- | -----: | ---------: |
| FoS < 1.0        | 18,717 |     14.44% |
| 1.0 ≤ FoS < 1.25 | 17,566 |     13.55% |
| 1.25 ≤ FoS < 1.5 | 15,612 |     12.05% |
| 1.5 ≤ FoS < 2.0  | 23,210 |     17.91% |
| FoS > 2.0        | 54,495 |     42.05% |

---

# Outputs Generated

* TRIGRS FoS rasters
* Stability classification raster
* Stability statistics
* GIS-ready outputs
* FoS class map

---

# Limitations

Current results should not be interpreted as actual landslide susceptibility for Wayanad because:

1. Soil parameters are benchmark values.
2. Rainfall forcing was not applied.
3. Runoff routing was disabled.
4. Wayanad-specific geotechnical properties have not yet been incorporated.

---

# Future Work

## Phase 2: Wayanad Geotechnical Parameters

Obtain:

* Cohesion
* Friction angle
* Unit weight
* Hydraulic conductivity
* Soil depth
* Porosity parameters

## Phase 3: Rainfall Data Collection

Potential sources:

* IMD
* ERA5-Land
* CHIRPS
* GPM IMERG

## Phase 4: Realistic TRIGRS Simulations

* Build rainfall scenarios
* Simulate transient infiltration
* Evaluate FoS evolution through time
* Compare with known landslide events

---

# Conclusion

The TRIGRS workflow was successfully implemented and executed on a real Wayanad DEM.

The current implementation serves as a workflow validation and baseline stability assessment using benchmark parameters.

Future work will focus on replacing benchmark assumptions with Wayanad-specific geotechnical properties and rainfall forcing to produce realistic landslide susceptibility assessments.

