import os,sys,textwrap
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from osgeo import gdal
from sklearn.metrics import roc_curve, auc
gdal.UseExceptions()

BASE='.'
OUT_DIR=f'{BASE}/data/idukki/output_utm'
VAL_DIR=f'{BASE}/data/idukki/validation'
INVENTORY=f'{BASE}/data/idukki/inventory/idukki_inventory_utm.csv'
COMP_GRID=f'{VAL_DIR}/fs_min_composite_idukki.asc'
os.makedirs(VAL_DIR,exist_ok=True)

print("Step 1: Computing cell-wise minimum FS...")
fs_min=None; nd_val=None; hdr={}
for t in range(1,11):
    ds=gdal.Open(f'{OUT_DIR}/TRfs_min_idukki_{t}.asc')
    arr=ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    nd=ds.GetRasterBand(1).GetNoDataValue()
    gt=ds.GetGeoTransform()
    NROWS,NCOLS=ds.RasterYSize,ds.RasterXSize; ds=None
    if fs_min is None:
        fs_min=arr.copy(); nd_val=nd; hdr['gt']=gt
        ULX,RES,ULY=gt[0],gt[1],gt[3]; LRY=ULY+NROWS*gt[5]
        NROWS_=NROWS; NCOLS_=NCOLS
    else:
        vb=(arr!=nd)&(fs_min!=nd_val); fs_min[vb]=np.minimum(fs_min[vb],arr[vb])
        nv=(arr!=nd)&(fs_min==nd_val); fs_min[nv]=arr[nv]
    print(f"  t={t}")

VALID=fs_min!=nd_val
v=fs_min[VALID]
print(f"Composite: n={VALID.sum()}, min={v.min():.3f}, max={v.max():.3f}, mean={v.mean():.3f}")

with open(COMP_GRID,'w') as f:
    f.write(f"ncols          {NCOLS_}\nnrows          {NROWS_}\n")
    f.write(f"xllcorner      {ULX:.6f}\nyllcorner      {LRY:.6f}\n")
    f.write(f"cellsize       {RES:.1f}\nnodata_value   {nd_val}\n")
    np.savetxt(f,fs_min,fmt='%.4f')
print(f"Written: {COMP_GRID}")

print("\nStep 2: Loading inventory...")
import pandas as pd
df=pd.read_csv(INVENTORY)
xs=df['x_utm43n'].values; ys=df['y_utm43n'].values
cols_ls=((xs-ULX)/RES).astype(int); rows_ls=((ULY-ys)/RES).astype(int)
ib=(rows_ls>=0)&(rows_ls<NROWS_)&(cols_ls>=0)&(cols_ls<NCOLS_)
rows_ls,cols_ls=rows_ls[ib],cols_ls[ib]
fs_ls=fs_min[rows_ls,cols_ls]; od=fs_ls!=nd_val
rows_ls,cols_ls,fs_ls=rows_ls[od],cols_ls[od],fs_ls[od]
n_ls=len(fs_ls)
print(f"Inventory points with valid FS: {n_ls}")
print(f"FS at inventory: min={fs_ls.min():.3f} max={fs_ls.max():.3f} mean={fs_ls.mean():.3f}")
print(f"FS<1.0 at inventory: {int(np.sum(fs_ls<1.0))} ({100*np.mean(fs_ls<1.0):.1f}%)")

print(f"\nStep 3: Sampling {n_ls} non-landslide points...")
np.random.seed(42)
ls_set=set(zip(rows_ls.tolist(),cols_ls.tolist()))
all_rows,all_cols=np.where(VALID)
idx=np.random.permutation(len(all_rows))
nl_rows,nl_cols=[],[]
for i in idx:
    r,c=all_rows[i],all_cols[i]
    if (r,c) not in ls_set: nl_rows.append(r); nl_cols.append(c)
    if len(nl_rows)==n_ls: break
nl_rows=np.array(nl_rows); nl_cols=np.array(nl_cols)
fs_nl=fs_min[nl_rows,nl_cols]
print(f"Non-LS FS: min={fs_nl.min():.3f} max={fs_nl.max():.3f} mean={fs_nl.mean():.3f}")

print("\nStep 4: ROC/AUC...")
labels=np.concatenate([np.ones(n_ls),np.zeros(len(fs_nl))])
scores=np.concatenate([-fs_ls,-fs_nl])
fpr,tpr,_=roc_curve(labels,scores); roc_auc=auc(fpr,tpr)
print(f"ROC-AUC = {roc_auc:.4f}")

print("Step 5: Success-rate curve...")
all_fs=fs_min[VALID]; sort_idx=np.argsort(all_fs)
sorted_rows=all_rows[sort_idx]; sorted_cols=all_cols[sort_idx]
n_total=len(all_fs)
ls_map=np.zeros((NROWS_,NCOLS_),dtype=bool); ls_map[rows_ls,cols_ls]=True
ls_sorted=ls_map[sorted_rows,sorted_cols]
cum_ls=np.cumsum(ls_sorted)/n_ls; pct_area=np.arange(1,n_total+1)/n_total*100
src_auc=np.trapezoid(cum_ls,pct_area/100)
print(f"SRC-AUC = {src_auc:.4f}")
for pct in [5,10,20,30,50]:
    cut=int(pct/100*n_total)
    print(f"  Top {pct}% area -> {ls_sorted[:cut].sum()/n_ls*100:.1f}% LS captured")

fig,ax=plt.subplots(figsize=(7,6))
ax.plot(fpr,tpr,color='steelblue',lw=2,label=f'TRIGRS FS_min (AUC={roc_auc:.3f})')
ax.plot([0,1],[0,1],'k--',lw=1,label='Random (AUC=0.500)')
ax.set_xlabel('False Positive Rate',fontsize=12); ax.set_ylabel('True Positive Rate',fontsize=12)
ax.set_title(f'ROC Curve — TRIGRS P-1, Idukki Aug 2018\n(n={n_ls:,} LS vs {len(fs_nl):,} non-LS)',fontsize=11)
ax.legend(fontsize=11); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{VAL_DIR}/roc_curve_idukki2018.png',dpi=150); plt.close(fig)

fig,ax=plt.subplots(figsize=(7,6))
ax.plot(pct_area,cum_ls*100,color='firebrick',lw=2,label=f'TRIGRS FS_min (AUC={src_auc:.3f})')
ax.plot([0,100],[0,100],'k--',lw=1,label='Random baseline')
ax.set_xlabel('% Study Area (ranked by FS)',fontsize=12)
ax.set_ylabel('% Inventory Captured',fontsize=12)
ax.set_title('Success-Rate Curve — TRIGRS P-1, Idukki Aug 2018',fontsize=12)
ax.legend(fontsize=11); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.grid(alpha=0.3)
for pct in [10,20,30]:
    cut=int(pct/100*n_total); hit=ls_sorted[:cut].sum()/n_ls*100
    ax.annotate(f'{pct}%→{hit:.0f}%',xy=(pct,hit),xytext=(pct+3,hit-10),fontsize=9,color='firebrick',
                arrowprops=dict(arrowstyle='->',color='firebrick'))
fig.tight_layout(); fig.savefig(f'{VAL_DIR}/success_rate_curve_idukki2018.png',dpi=150); plt.close(fig)

summary=f"""
TRIGRS P-1 Validation — Idukki August 2018
===========================================
ROC-AUC  : {roc_auc:.4f}
SRC-AUC  : {src_auc:.4f}
Inventory: {n_ls:,} points (valid cells)
FS<1.0 at inventory: {int(np.sum(fs_ls<1.0))} ({100*np.mean(fs_ls<1.0):.1f}%)
Domain FS<1.0: {int(np.sum(v<1.0)):,} ({100*np.mean(v<1.0):.1f}%)
"""
print(summary)
with open(f'{VAL_DIR}/validation_summary_idukki2018.txt','w') as f: f.write(summary)
print("Done. Results in data/idukki/validation/")
