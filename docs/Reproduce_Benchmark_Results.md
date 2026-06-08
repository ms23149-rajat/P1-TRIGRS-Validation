# TRIGRS Installation, Compilation and Benchmark Execution Guide

## 1. Clone Repository

```bash
git clone <repository-url>
cd landslides-trigrs
```

## 2. Create Environment

```bash
conda env create -f environment_trigrs.yml
conda activate trigrs
```

## 3. Compile TopoIndex

```bash
cd src/TopoIndex
gfortran *.f90 -o tpx
cd ../..
```

## 4. Compile TRIGRS

```bash
cd src/TRIGRS
gfortran *.f90 -o trg
cd ../..
```

## 5. Tutorial Benchmark

### Run TopoIndex

```bash
cp tpx_in_original.txt tpx_in.txt
./src/TopoIndex/tpx
```

### Run TRIGRS

```bash
./src/TRIGRS/trg
```

### Inspect Outputs

```bash
head -20 data/tutorial/TRfs_min_tutorial_1.asc
head -20 data/tutorial/TRfs_min_tutorial_2.asc
```

---

## 6. MinorCreek Benchmark

### Run

```bash
cp tr_in_mc.txt tr_in.txt
./src/TRIGRS/trg
```

### Inspect Outputs

```bash
grep -n "cell" data/MinorCreek/TRlist_z_p_fs_MC.txt
tail -20 data/MinorCreek/TRlist_z_p_fs_MC.txt
```

---

## 7. Flume Benchmark

### Run

```bash
cp tr_in_flume.txt tr_in.txt
./src/TRIGRS/trg
```

### Inspect Outputs

```bash
head -40 data/flume/TRlist_z_p_fs_flume.txt
```

---

## 8. Srivastava and Yeh (1991) Benchmark

### Run

```bash
cp tr_in_sy.txt tr_in.txt
./src/TRIGRS/trg
```

### Inspect Outputs

```bash
grep -n "cell" data/sy91/TRlist_z_p_fs_syfig3.txt

sed -n '47,60p' data/sy91/TRlist_z_p_fs_syfig3.txt
sed -n '89,102p' data/sy91/TRlist_z_p_fs_syfig3.txt
sed -n '131,144p' data/sy91/TRlist_z_p_fs_syfig3.txt
```

---

## 9. Verify Successful Execution

### Check TopoIndex Log

```bash
tail -20 TopoIndexLog.txt
```

### Check TRIGRS Log

```bash
tail -30 TrigrsLog.txt
```
