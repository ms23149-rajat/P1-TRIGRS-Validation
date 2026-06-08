# Wayanad DEM Preprocessing Workflow for TRIGRS

## Objective

Prepare terrain-derived inputs from a Copernicus GLO-30 DEM for future TRIGRS and hydrologic analysis.

---

## Dataset Acquisition

Dataset: Copernicus GLO-30 DEM

Study Area: Wayanad, Kerala, India

Approximate Bounding Coordinates:

```text
Xmin = 76.0000
Ymin = 11.4500

Xmax = 76.1000
Ymax = 11.5500
```

Output Format:

```text
GeoTIFF
```

Downloaded File:

```text
wayanad_dem.tif
```

---

## DEM Validation

DEM Metadata:

```text
Coordinate System: EPSG:4326 (WGS84)
Rows: 360
Columns: 360
Total Cells: 129600
```

Elevation Statistics:

```text
Minimum Elevation = 32.08 m
Maximum Elevation = 2066.75 m
Mean Elevation = 826.48 m
```

Observation:

* Terrain exhibits significant relief.
* Elevation range confirms mountainous topography suitable for landslide studies.

---

## Slope Generation

Command:

```bash
gdaldem slope wayanad_dem.tif wayanad_slope.tif
```

Slope Statistics:

```text
Minimum Slope = 0.00°
Maximum Slope = 63.16°
Mean Slope = 21.58°
```

Observation:

* Presence of both flat valley areas and steep hillslopes.
* Suitable terrain for slope-stability analysis.

---

## Import into GRASS GIS

Create GRASS Location:

```bash
grass -c sample_data/wayanad_dem.tif grassdata/wayanad
```

Import DEM:

```bash
r.in.gdal input=sample_data/wayanad_dem.tif output=wayanad_dem
```

Verify Raster:

```bash
g.list type=raster
```

---

## Flow Direction and Flow Accumulation

Generate Hydrologic Products:

```bash
r.watershed elevation=wayanad_dem accumulation=flow_acc drainage=flow_dir
```

Generated Outputs:

```text
flow_acc
flow_dir
```

---

## Flow Accumulation Statistics

Command:

```bash
r.info map=flow_acc
```

Statistics:

```text
Minimum = -30562.89
Maximum = 26336.63
```

Observation:

* High positive values correspond to major drainage pathways.
* Negative values represent cells draining outside the map boundary.
* Flow accumulation identifies areas of concentrated surface runoff.

---

## Export Flow Accumulation Raster

Command:

```bash
r.out.gdal input=flow_acc output=flow_acc.tif format=GTiff
```

Exported File:

```text
flow_acc.tif
```

Verification:

```bash
gdalinfo -stats flow_acc.tif
```

Export preserved raster statistics successfully.

---

## Workflow Summary

```text
Copernicus DEM
        ↓
DEM Validation
        ↓
Slope Raster
        ↓
GRASS Import
        ↓
Flow Direction
        ↓
Flow Accumulation
        ↓
GeoTIFF Export
        ↓
TRIGRS Preprocessing Inputs
```

---

## Future Work

* Generate Topographic Wetness Index (TWI)
* Delineate drainage network
* Export flow direction raster
* Investigate TopoIndex compatibility
* Develop TRIGRS-ready terrain preprocessing workflow
