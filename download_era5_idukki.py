import cdsapi
import os

c = cdsapi.Client()

# Idukki district center: ~9.9N, 77.0E
# Download a small box around it: 9.5-10.5N, 76.5-77.5E
# August 1-20 2018 to capture the buildup and peak

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': 'total_precipitation',
        'year': '2018',
        'month': '08',
        'day': [f'{d:02d}' for d in range(1, 21)],
        'time': [f'{h:02d}:00' for h in range(24)],
        'area': [10.5, 76.5, 9.5, 77.5],  # N, W, S, E
        'format': 'netcdf',
    },
    'era5_extract/idukki_aug2018.nc'
)
print("Download complete")
