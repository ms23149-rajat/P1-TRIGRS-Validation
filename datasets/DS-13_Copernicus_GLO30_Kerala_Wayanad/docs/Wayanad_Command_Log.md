# Wayanad Command Log

## Purpose

This document records the major commands used during the Wayanad TRIGRS implementation and validation workflow.

It serves as a reference for reproducing the work and understanding the sequence of processing steps.

---

# 1. Environment Setup

Activate TRIGRS environment:

```bash
conda activate trigrs
```

Navigate to TRIGRS directory:

```bash
cd ~/landslides-trigrs
```

---

# 2. GRASS GIS Setup

Open GRASS location:

```bash
grass /mnt/hdd/home/rajat-surge2026/iitk-landslide-toolkit/datasets/DS-13_Copernicus_GLO30/grassdata/wayanad/PERMANENT
```

Text mode:

```bash
grass --text /mnt/hdd/home/rajat-surge2026/iitk-landslide-toolkit/datasets/DS-13_Copernicus_GLO30/grassdata/wayanad/PERMANENT
```

Verify available rasters:

```bash
g.list type=raster
```

---

# 3. DEM Processing

Generate slope raster:

```bash
gdaldem slope wayanad_dem.tif wayanad_slope.tif
```

Convert slope GeoTIFF to ASCII:

```bash
gdal_translate -of AAIGrid \
wayanad_slope.tif \
wayanad_slope.asc
```

Convert DEM GeoTIFF to ASCII:

```bash
gdal_translate -of AAIGrid \
wayanad_dem.tif \
wayanad_dem.asc
```

---

# 4. Flow Direction and Flow Accumulation

Generate flow accumulation and flow direction:

```bash
r.watershed \
elevation=wayanad_dem \
accumulation=flow_acc \
drainage=flow_dir
```

Inspect raster statistics:

```bash
r.info map=flow_acc
```

Export flow direction raster:

```bash
r.out.gdal \
input=flow_dir \
output=flow_dir.tif \
format=GTiff
```

---

# 5. Flow Direction Conversion Experiments

Generated products:

- flow_dir.asc
- flow_dir_d8.asc
- flow_dir_esri.asc

Purpose:

Investigate compatibility with TopoIndex and TRIGRS runoff-routing workflow.

---

# 6. Zone Raster Creation

Create uniform zone map from DEM:

```python
zone = np.where(arr == -9999, -9999, 1)
```

Output:

```text
wayanad_zone.asc
```

---

# 7. TopoIndex Investigation

Files used:

```text
flow_dir_esri.asc
TIflodirGrid_wayanad.txt
TIdsneiList_wayanad.txt
```

Observation:

TopoIndex repeatedly stopped during:

"Correcting cell index numbers"

Decision:

Run TRIGRS without runoff routing.

---

# 8. TRIGRS Configuration

Input file:

```text
tr_in_wayanad.txt
```

Important settings:

```text
rifil = none

nxtfil = none
ndxfil = none
dscfil = none
wffil = none
```

Current parameters:

```text
Srivastava & Yeh (1991)
```

---

# 9. TRIGRS Execution

Run model:

```bash
./src/TRIGRS/trg
```

Generated outputs:

```text
TRfs_min_wayanad_1.asc
TRfs_min_wayanad_2.asc
TRfs_min_wayanad_3.asc
TRfs_min_wayanad_4.asc

TRlist_z_p_fs_wayanad.txt
```

---

# 10. FoS Analysis

Computed:

- Minimum FoS
- Mean FoS
- Maximum FoS
- Unstable cell counts
- Stability class percentages

Results:

```text
Minimum FoS = 0.3414
Mean FoS    = 2.5844
Maximum FoS = 10.0
```

---

# 11. GRASS Visualization

Import FoS raster:

```bash
r.in.gdal -o \
input=TRfs_min_wayanad_4.asc \
output=fos_40h
```

Compute statistics:

```bash
r.univar fos_40h
```

Create FoS classes:

```bash
r.mapcalc expression="fos_class=if(fos_40h<1.0,1,if(fos_40h<1.25,2,if(fos_40h<1.5,3,if(fos_40h<2.0,4,5))))"
```

Count cells:

```bash
r.stats -cn input=fos_class
```

Apply colors:

```bash
r.colors map=fos_class rules=fos_colors.txt
```

Export GeoTIFF:

```bash
r.out.gdal \
input=fos_class \
output=fos_class.tif \
format=GTiff
```

---

# 12. GitHub Archival

Check status:

```bash
git status
```

Stage files:

```bash
git add .
```

Commit:

```bash
git commit -m "<message>"
```

Push:

```bash
git push origin main
```

---

# Notes

This log records what was actually executed during the DS-13 Wayanad implementation.

A separate document,
Reproduce_Wayanad_TRIGRS_Run.md,
will provide a cleaned and structured workflow for new users.
