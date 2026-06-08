# Common Issues and Fixes

## Issue 1: Lost Terminal Output

### Problem

The terminal session was closed or cleared after TRIGRS completed, making it impossible to view previous outputs.

### Solution

Check whether output files were already generated:

```bash
find ~/landslides-trigrs -name "TR*"
find ~/landslides-trigrs -name "*.asc"
```

Inspect the generated files directly:

```bash
head -20 data/tutorial/TRfs_min_tutorial_1.asc
head -20 data/tutorial/TRfs_min_tutorial_2.asc
```

### Lesson

TRIGRS writes results to files. Even if terminal output is lost, results can usually be recovered from the data folders.

---

## Issue 2: Could Not Find FoS Results

### Problem

After running TRIGRS, no obvious FoS output appeared in the terminal.

### Solution

Search for generated output files:

```bash
find data -name "TR*"
```

Check benchmark-specific output files:

```bash
data/tutorial/TRfs_min_tutorial_1.asc
data/tutorial/TRfs_min_tutorial_2.asc
```

### Lesson

TRIGRS stores results in output files rather than displaying them directly in the terminal.

---

## Issue 3: MinorCreek Produced Only One Cell

### Problem

The MinorCreek benchmark appeared incorrect because only one cell was processed.

### Solution

Inspect the output:

```bash
grep -n "cell" data/MinorCreek/TRlist_z_p_fs_MC.txt
```

### Lesson

MinorCreek is a one-dimensional benchmark. Processing one cell is expected behaviour.

---

## Issue 4: Expected Grid Output But Received Text Profile

### Problem

MinorCreek, Flume and SY91 did not generate FoS grids like the Tutorial benchmark.

### Solution

Inspect profile outputs instead:

```bash
head -40 data/flume/TRlist_z_p_fs_flume.txt

tail -20 data/MinorCreek/TRlist_z_p_fs_MC.txt

grep -n "cell" data/sy91/TRlist_z_p_fs_syfig3.txt
```

### Lesson

Not all benchmarks generate raster outputs. Some generate depth-profile text files.

---

## Issue 5: Tutorial Results Did Not Match Expected Timing

### Problem

Confusion regarding whether the benchmark represented 2 days or 2.5 days.

### Solution

Check available output files:

```bash
ls data/tutorial/
```

Inspect:

```bash
TRfs_min_tutorial_1.asc
TRfs_min_tutorial_2.asc
```

### Lesson

Tutorial outputs correspond to different output times. Verify output times before interpreting results.

---

## Issue 6: Understanding SY91 Output

### Problem

The SY91 benchmark appeared to produce constant FoS values.

### Solution

Inspect the output times:

```bash
grep -n "cell" data/sy91/TRlist_z_p_fs_syfig3.txt
```

View each output block:

```bash
sed -n '47,60p' data/sy91/TRlist_z_p_fs_syfig3.txt
sed -n '89,102p' data/sy91/TRlist_z_p_fs_syfig3.txt
sed -n '131,144p' data/sy91/TRlist_z_p_fs_syfig3.txt
```

### Lesson

SY91 validates infiltration physics. The slope angle is 0°, so FoS remains constant.

---

## Issue 7: Wrong GitHub Remote URL

### Problem

Git remote was configured using:

```bash
git remote add origin https://github.com/USERNAME/P1-TRIGRS-Validation.git
```

which is only a placeholder.

### Solution

Remove incorrect remote:

```bash
git remote remove origin
```

Add the correct remote:

```bash
git remote add origin https://github.com/ms23149-rajat/P1-TRIGRS-Validation.git
```

### Lesson

Always replace placeholder URLs with the actual repository URL.

---

## Issue 8: GitHub Authentication Failed

### Problem

GitHub requested a username and password during push operations.

### Solution

Use:

```text
GitHub Username
```

and a

```text
Personal Access Token (PAT)
```

instead of the GitHub account password.

### Lesson

GitHub no longer accepts account passwords for Git operations.

---

## Issue 9: Verifying Successful TRIGRS Execution

### Problem

Uncertainty whether TRIGRS completed successfully.

### Solution

Check:

```bash
tail -30 TrigrsLog.txt
```

Successful execution should end with:

```text
TRIGRS finished normally
```

### Lesson

Always verify execution using TrigrsLog.txt instead of relying on terminal output.
