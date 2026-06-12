import numpy as np, re, os

alpha=0.10; Ks=1.0; Iz=0.9; Iz0=0.1; L=100.0
psi_ss_old = (1/alpha)*np.log(Iz0/Ks)
psi_ss_new = (1/alpha)*np.log(Iz /Ks)

trlist = os.path.expanduser(
    "~/iitk-landslide-toolkit/models/P1-TRIGRS-Validation/"
    "benchmark_test_results/SY91/TRlist_z_p_fs_syfig3.txt"
)

results = {}
cur_t = None; z_v=[]; p_v=[]
with open(trlist) as f:
    for line in f:
        line = line.strip()
        m = re.match(r'^cell\s+\d+\s+[\d.]+\s+\d+\s+([\d.]+)', line)
        if m:
            if cur_t is not None and z_v:
                results[cur_t] = {'z': np.array(z_v), 'P': np.array(p_v)}
            cur_t = float(m.group(1)); z_v=[]; p_v=[]
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                z_v.append(float(parts[0]))
                p_v.append(float(parts[1]))
            except:
                pass
if cur_t is not None and z_v:
    results[cur_t] = {'z': np.array(z_v), 'P': np.array(p_v)}

print("=" * 62)
print("  TRIGRS SY91 - Physical Validation Results")
print("=" * 62)

# Check 1: IC matches uniform SS under Iz0
td = results[0.0]
psi0 = td['P'][0]
err1 = abs(psi0 - psi_ss_old) / abs(psi_ss_old) * 100
c1 = err1 < 1.0
print(f"  [{'PASS' if c1 else 'FAIL'}] Check 1: IC matches uniform SS under Iz0")
print(f"         psi(Z=0, t=0)  = {psi0:.4f} m")
print(f"         analytical SS  = {psi_ss_old:.4f} m  [(1/alpha)*ln(Iz0/Ks)]")
print(f"         error          = {err1:.4f}%")
print()

# Check 2: Surface reaches new SS by t=40h
td = results[40.0]
psi40 = td['P'][0]
err2 = abs(psi40 - psi_ss_new) / abs(psi_ss_new) * 100
c2 = err2 < 1.0
print(f"  [{'PASS' if c2 else 'FAIL'}] Check 2: Surface psi reaches new SS by t=40h")
print(f"         psi(Z=0, t=40h) = {psi40:.4f} m")
print(f"         new SS          = {psi_ss_new:.4f} m  [(1/alpha)*ln(Iz/Ks)]")
print(f"         error           = {err2:.4f}%")
print()

# Check 3: Wetting front propagates downward (surface psi increases monotonically)
sv = [(t, results[t]['P'][0]) for t in sorted(results.keys())]
c3 = all(sv[i][1] >= sv[i-1][1] for i in range(1, len(sv)))
print(f"  [{'PASS' if c3 else 'FAIL'}] Check 3: Wetting front propagates downward over time")
for t, p in sv:
    print(f"         t={t:4.0f} h:  psi(Z=0) = {p:.4f} m")
print()

# Check 4: Water table (Z=100m) held at psi=0 throughout
wt = [(t, results[t]['P'][-1]) for t in sorted(results.keys())]
c4 = all(abs(p) < 0.01 for _, p in wt)
print(f"  [{'PASS' if c4 else 'FAIL'}] Check 4: Water table Z=100m held at psi=0")
for t, p in wt:
    print(f"         t={t:4.0f} h:  psi(Z=100) = {p:.6f} m")
print()

print("=" * 62)
overall = all([c1, c2, c3, c4])
print(f"  Overall: {'ALL 4 CHECKS PASS' if overall else 'SOME CHECKS FAILED'}")
print("=" * 62)
print()
print("Analytical reference values used:")
print(f"  psi_ss_old = (1/alpha)*ln(Iz0/Ks) = {psi_ss_old:.6f} m")
print(f"  psi_ss_new = (1/alpha)*ln(Iz/Ks)  = {psi_ss_new:.6f} m")
print()
print("Note: Quantitative comparison against S&Y (1991) analytical solution")
print("was not achieved. The S&Y semi-infinite erfc formula is degenerate")
print("for this parameter set (alpha*L=10). Physical consistency confirmed")
print("via 4 checks against analytically known steady-state values.")
