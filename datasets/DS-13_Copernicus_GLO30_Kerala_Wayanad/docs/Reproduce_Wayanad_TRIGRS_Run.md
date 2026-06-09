# Reproduce Wayanad TRIGRS Run

## Objective

This document describes the final successful workflow used to implement and run TRIGRS on the Wayanad DEM.

The workflow intentionally excludes unsuccessful TopoIndex experiments and focuses only on the steps required to reproduce the final results.

---

# Prerequisites

Required software:

* Conda
* GDAL
* GRASS GIS
* TRIGRS

Repository:

```text
~/iitk-landslide-toolkit/models/P1-TRIGRS-Validation
```

TRIGRS installation:

```text
~/landslides-trigrs
```

---

# Step 1: Activate Environment

```bash
conda activate trigrs
```

Verify:

```bash
which python
```

---

# Step 2: Prepare Dataset

Dataset:

Copernicus GLO-30 DEM

Study Area:

Wayanad, Kerala

Files required:

```text
wayanad_dem.tif
```

---

# Step 3: Generate Slope Raster

```bash
gdaldem slope wayanad_dem.tif wayanad_slope.tif
```

Verify creation:

```bash
ls -lh wayanad_slope.tif
```

---

# Step 4: Convert DEM and Slope to ASCII

DEM:

```bash
gdal_translate -of AAIGrid \
wayanad_dem.tif \
wayanad_dem.asc
```

Slope:

```bash
gdal_translate -of AAIGrid \
wayanad_slope.tif \
wayanad_slope.asc
```

---

# Step 5: Open GRASS GIS

```bash
grass /mnt/hdd/home/rajat-surge2026/iitk-landslide-toolkit/datasets/DS-13_Copernicus_GLO30/grassdata/wayanad/PERMANENT
```

Verify rasters:

```bash
g.list type=raster
```

Expected rasters include:

```text
wayanad_dem
flow_acc
flow_dir
```

---

# Step 6: Generate Flow Products

Generate flow accumulation and flow direction:

```bash
r.watershed \
elevation=wayanad_dem \
accumulation=flow_acc \
drainage=flow_dir
```

Inspect:

```bash
r.info map=flow_acc
```

---

# Step 7: Export Flow Direction Raster

```bash
r.out.gdal \
input=flow_dir \
output=flow_dir.tif \
format=GTiff
```

---

# Step 8: Create Zone Raster

Create a single-zone raster where all valid cells belong to zone 1.

Python logic:

```python
zone = np.where(arr == -9999, -9999, 1)
```

Output:

```text
wayanad_zone.asc
```

Verify:

```bash
python - <<'PY'
import numpy as np
arr=np.loadtxt("wayanad_zone.asc",skiprows=6)
print(np.unique(arr))
PY
```

Expected:

```text
[1.]
```

---

# Step 9: Prepare TRIGRS Input File

Input file:

```text
tr_in_wayanad.txt
```

Input rasters:

```text
data/wayanad/wayanad_dem.asc
data/wayanad/wayanad_slope.asc
data/wayanad/wayanad_zone.asc
```

Important settings:

```text
rifil = none

nxtfil = none
ndxfil = none
dscfil = none
wffil = none
```

Current simulation uses:

```text
Srivastava & Yeh (1991) benchmark parameters
```

---

# Step 10: Run TRIGRS

Move to TRIGRS directory:

```bash
cd ~/landslides-trigrs
```

Execute:

```bash
./src/TRIGRS/trg
```

Successful completion generates:

```text
TRfs_min_wayanad_1.asc
TRfs_min_wayanad_2.asc
TRfs_min_wayanad_3.asc
TRfs_min_wayanad_4.asc

TRlist_z_p_fs_wayanad.txt
```

---

# Step 11: Import FoS Raster Into GRASS

```bash
r.in.gdal -o \
input=/mnt/hdd/home/rajat-surge2026/landslides-trigrs/data/wayanad/TRfs_min_wayanad_4.asc \
output=fos_40h \
--overwrite
```

---

# Step 12: Compute Statistics

```bash
r.univar fos_40h
```

Expected values:

```text
Minimum FoS = 0.3414
Mean FoS    = 2.5844
Maximum FoS = 10.0
```

---

# Step 13: Create Stability Classes

```bash
r.mapcalc expression="fos_class=if(fos_40h<1.0,1,if(fos_40h<1.25,2,if(fos_40h<1.5,3,if(fos_40h<2.0,4,5))))" --overwrite
```

Count cells:

```bash
r.stats -cn input=fos_class
```

Expected:

```text
1 18717
2 17566
3 15612
4 23210
5 54495
```

---

# Step 14: Apply Color Scheme

Create:

```text
fos_colors.txt
```

Contents:

```text
1 255:0:0
2 255:165:0
3 255:255:0
4 0:255:255
5 0:255:0
```

Apply:

```bash
r.colors map=fos_class rules=fos_colors.txt
```

---

# Step 15: Export GeoTIFF

```bash
r.out.gdal \
input=fos_class \
output=fos_class.tif \
format=GTiff \
--overwrite
```

---

# Expected Final Results

FoS Statistics:

```text
Minimum FoS = 0.3414
Mean FoS    = 2.5844
Maximum FoS = 10.0
```

Stability Classes:

```text
FoS < 1.0      : 18,717 cells
1.0 - 1.25     : 17,566 cells
1.25 - 1.5     : 15,612 cells
1.5 - 2.0      : 23,210 cells
> 2.0          : 54,495 cells
```

---

# Notes

This workflow validates the TRIGRS implementation on a real Wayanad DEM.

The current simulation uses benchmark soil parameters and no rainfall forcing.

Results should therefore be interpreted as workflow-validation results rather than a realistic landslide hazard assessment.
