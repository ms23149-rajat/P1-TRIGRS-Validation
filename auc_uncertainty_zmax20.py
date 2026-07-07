import numpy as np
import pandas as pd
from osgeo import gdal
from sklearn.metrics import roc_auc_score
gdal.UseExceptions()

COMP_GRID = 'data/idukki/validation/fs_min_composite_idukki_zmax20.asc'
INVENTORY = 'data/idukki/inventory/idukki_inventory_utm.csv'

print("Loading composite FS grid...")
ds = gdal.Open(COMP_GRID)
fs_min = ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
nd_val = ds.GetRasterBand(1).GetNoDataValue()
gt = ds.GetGeoTransform()
NROWS, NCOLS = ds.RasterYSize, ds.RasterXSize
ULX, RES, ULY = gt[0], gt[1], gt[3]
ds = None
VALID = fs_min != nd_val
print(f"Valid cells: {VALID.sum():,}")

print("\nLoading inventory...")
df = pd.read_csv(INVENTORY)
xs, ys = df['x_utm43n'].values, df['y_utm43n'].values
cols_ls = ((xs - ULX) / RES).astype(int)
rows_ls = ((ULY - ys) / RES).astype(int)
ib = (rows_ls>=0)&(rows_ls<NROWS)&(cols_ls>=0)&(cols_ls<NCOLS)
rows_ls, cols_ls = rows_ls[ib], cols_ls[ib]
fs_ls = fs_min[rows_ls, cols_ls]
od = fs_ls != nd_val
rows_ls, cols_ls, fs_ls = rows_ls[od], cols_ls[od], fs_ls[od]
n_ls = len(fs_ls)
print(f"Landslide points with valid FS: {n_ls}")

is_ls = np.zeros((NROWS, NCOLS), dtype=bool)
is_ls[rows_ls, cols_ls] = True
neg_mask = VALID & (~is_ls)
fs_neg_full = fs_min[neg_mask]
n_neg_full = len(fs_neg_full)
print(f"\nFull negative population: {n_neg_full:,} cells")

# ── Full-population AUC (deterministic, no sampling) ─────────────────────────
labels_full = np.concatenate([np.ones(n_ls), np.zeros(n_neg_full)])
scores_full = np.concatenate([-fs_ls, -fs_neg_full])
auc_full = roc_auc_score(labels_full, scores_full)
print(f"\nFULL-POPULATION AUC = {auc_full:.4f}")

# ── Bootstrap over 100 random 1:1-matched samples ────────────────────────────
n_boot = 100
auc_boot = np.zeros(n_boot)
for b in range(n_boot):
    rng = np.random.RandomState(b)
    idx = rng.choice(n_neg_full, size=n_ls, replace=False)
    labels = np.concatenate([np.ones(n_ls), np.zeros(n_ls)])
    scores = np.concatenate([-fs_ls, -fs_neg_full[idx]])
    auc_boot[b] = roc_auc_score(labels, scores)

print(f"\nBOOTSTRAP ({n_boot} seeds, 1:1 matched):")
print(f"  Mean = {auc_boot.mean():.4f}")
print(f"  Std  = {auc_boot.std():.4f}")
print(f"  Range = [{auc_boot.min():.4f}, {auc_boot.max():.4f}]")
print(f"  95% CI = [{np.percentile(auc_boot,2.5):.4f}, {np.percentile(auc_boot,97.5):.4f}]")

summary = f"""TRIGRS P-1 — AUC Uncertainty (Prof. Nandan review point 2)
Full-population AUC ({n_neg_full:,} negatives): {auc_full:.4f}
Bootstrap mean ({n_boot} seeds): {auc_boot.mean():.4f} +/- {auc_boot.std():.4f}
Bootstrap range: [{auc_boot.min():.4f}, {auc_boot.max():.4f}]
95% CI: [{np.percentile(auc_boot,2.5):.4f}, {np.percentile(auc_boot,97.5):.4f}]

Reportable: "ROC-AUC = {auc_full:.3f} (full population); bootstrap 95% CI
[{np.percentile(auc_boot,2.5):.3f}, {np.percentile(auc_boot,97.5):.3f}] across {n_boot} seeds."
"""
with open('data/idukki/validation/auc_uncertainty_summary_zmax20.txt', 'w') as f:
    f.write(summary)
print(f"\nWritten: data/idukki/validation/auc_uncertainty_summary_zmax20.txt")
