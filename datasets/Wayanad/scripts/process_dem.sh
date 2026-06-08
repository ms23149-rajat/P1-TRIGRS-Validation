#!/bin/bash

echo "DEM information"
gdalinfo "$1"

echo
echo "Creating slope raster..."
gdaldem slope "$1" slope.tif

echo
echo "Slope raster created:"
ls -lh slope.tif
