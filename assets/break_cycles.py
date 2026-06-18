#!/usr/bin/env python3
import numpy as np
import sys

DIR_OFFSET = {
    1:  (0,  1),  2:  (1,  1),  4:  (1,  0),  8:  (1, -1),
    16: (0, -1), 32: (-1, -1), 64: (-1,  0), 128:(-1,  1),
}

def read_ascii_grid(path):
    header = {}
    with open(path) as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        parts = lines[i].split()
        if len(parts) == 2 and not parts[0].lstrip('-').replace('.','').isdigit():
            header[parts[0].lower()] = parts[1]
            i += 1
        else:
            break
    ncols  = int(header['ncols'])
    nrows  = int(header['nrows'])
    nodata = float(header.get('nodata_value', -9999))
    data   = []
    for line in lines[i:]:
        data.extend(float(v) for v in line.split())
    import numpy as np
    grid = np.array(data, dtype=np.float64).reshape(nrows, ncols)
    return header, grid, nodata

def write_ascii_grid(path, header, grid, nodata):
    with open(path, 'w') as f:
        for k in ['ncols','nrows','xllcorner','yllcorner','cellsize','nodata_value']:
            if k in header:
                f.write(f"{k}  {header[k]}\n")
        for row in grid:
            f.write(' '.join(str(int(v) if v != nodata else int(nodata)) for v in row) + '\n')

def downstream(r, c, d, nrows, ncols):
    if int(d) not in DIR_OFFSET:
        return None
    dr, dc = DIR_OFFSET[int(d)]
    nr, nc = r+dr, c+dc
    if 0 <= nr < nrows and 0 <= nc < ncols:
        return nr, nc
    return None

def find_and_break_cycles(grid, nodata, nrows, ncols):
    import numpy as np
    broken = 0
    for pass_num in range(30):
        print(f"  Pass {pass_num+1}: scanning for cycles...", flush=True)
        WHITE, GRAY, BLACK = 0, 1, 2
        color = np.zeros((nrows, ncols), dtype=np.int8)
        stack = []
        found = []
        for sr in range(nrows):
            for sc in range(ncols):
                if color[sr, sc] != WHITE or grid[sr, sc] == nodata:
                    continue
                stack = [(sr, sc, False)]
                path = []
                in_path = {}
                while stack:
                    r, c, returning = stack.pop()
                    if returning:
                        if path and path[-1] == (r, c):
                            path.pop()
                            del in_path[(r, c)]
                        color[r, c] = BLACK
                        continue
                    if color[r, c] == BLACK:
                        continue
                    if color[r, c] == GRAY:
                        continue
                    color[r, c] = GRAY
                    path.append((r, c))
                    in_path[(r, c)] = len(path) - 1
                    stack.append((r, c, True))
                    d = grid[r, c]
                    if d != nodata and int(d) in DIR_OFFSET:
                        nb = downstream(r, c, d, nrows, ncols)
                        if nb is not None:
                            nr, nc = nb
                            if (nr, nc) in in_path:
                                found.append((nr, nc))
                            elif color[nr, nc] == WHITE:
                                stack.append((nr, nc, False))
        if not found:
            print(f"  No cycles found after {pass_num+1} passes. Grid is acyclic!", flush=True)
            break
        print(f"  Breaking {len(found)} cycle entry points...", flush=True)
        for (r, c) in found:
            grid[r, c] = 0
            broken += 1
    return grid, broken

def main():
    import numpy as np
    in_path  = sys.argv[1]
    out_path = sys.argv[2]
    print(f"Reading {in_path}...")
    header, grid, nodata = read_ascii_grid(in_path)
    nrows = int(header['nrows'])
    ncols = int(header['ncols'])
    print(f"  {nrows} x {ncols}, nodata={nodata}")

    unique = set(int(v) for v in np.unique(grid[grid != nodata]))
    grass = {1,2,3,4,5,6,7,8}
    arcgis = {1,2,4,8,16,32,64,128}
    if (unique - {0}) <= grass and not (unique - {0}) <= arcgis:
        print("  Remapping GRASS -> ArcGIS D8...")
        g2a = {1:1, 2:128, 3:64, 4:32, 5:16, 6:8, 7:4, 8:2}
        new = np.full_like(grid, nodata)
        for g, a in g2a.items():
            new[grid == g] = a
        new[grid < 0]      = 0
        new[grid == nodata] = nodata
        grid = new
    else:
        print("  ArcGIS D8 encoding detected, no remap needed.")

    print("Breaking cycles...")
    grid, n = find_and_break_cycles(grid, nodata, nrows, ncols)
    print(f"Total cells broken: {n}")
    print(f"Writing {out_path}...")
    write_ascii_grid(out_path, header, grid, nodata)
    print("Done.")

if __name__ == "__main__":
    main()
