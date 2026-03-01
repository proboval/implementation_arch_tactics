"""Verify all STAT-type CHECK markers — recompute statistical tests from raw data.

Usage: python paper/v1/scripts/verify_stats.py
Source: experiments/improvement_maintainability_experiment_3.csv
Requires: scipy, numpy
"""

import csv
import math
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = ROOT / "experiments" / "improvement_maintainability_experiment_3.csv"


def load_paired():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    paired = []
    for r in rows:
        if r["mi_before"] and r["mi_after"]:
            paired.append({
                "name": r["full_name"],
                "before": float(r["mi_before"]),
                "after": float(r["mi_after"]),
                "tactic": r["chosen_tactic"],
                "arch": r["architecture_summary"],
            })
    return paired


def check(label, expected, computed, tolerance=0.01):
    if isinstance(expected, float) and isinstance(computed, float):
        match = abs(expected - computed) < tolerance
    else:
        match = str(expected) == str(computed)
    icon = "[OK]" if match else "[!!]"
    print(f"  {icon} {label}: paper={expected}, computed={computed}")
    return match


def cliffs_delta(x, y):
    """Cliff's delta for two independent samples."""
    n_x, n_y = len(x), len(y)
    more = sum(1 for xi in x for yi in y if xi > yi)
    less = sum(1 for xi in x for yi in y if xi < yi)
    return (more - less) / (n_x * n_y)


def main():
    paired = load_paired()
    deltas = np.array([p["after"] - p["before"] for p in paired])
    before = np.array([p["before"] for p in paired])
    after = np.array([p["after"] for p in paired])

    nonzero_mask = np.abs(deltas) > 0.001
    nonzero_deltas = deltas[nonzero_mask]

    print("=" * 70)
    print("VERIFY STAT MARKERS — Statistical Tests")
    print("=" * 70)

    # --- Normality test (not in paper but should be) ---
    print("\n--- Shapiro-Wilk Normality Test on ΔMI ---")
    sw_stat, sw_p = stats.shapiro(deltas)
    print(f"  Shapiro-Wilk W={sw_stat:.4f}, p={sw_p:.6f}")
    print(f"  Normal? {'Yes' if sw_p > 0.05 else 'No'} (p {'>' if sw_p > 0.05 else '<'} 0.05)")
    print(f"  → {'Wilcoxon justified' if sw_p <= 0.05 else 'Could use t-test instead'}")

    # --- Wilcoxon on ALL 121 pairs (CORRECT approach) ---
    print("\n--- Wilcoxon Signed-Rank Test (ALL N=121 pairs) ---")
    w_all, p_all = stats.wilcoxon(deltas, alternative="greater")
    n_eff = np.sum(nonzero_mask)
    z_all = stats.norm.ppf(1 - p_all)  # approximate Z from p
    r_all = z_all / math.sqrt(len(deltas))
    print(f"  W={w_all:.1f}, p={p_all:.6f}, N={len(deltas)}, non-zero={int(n_eff)}")
    print(f"  Rank-biserial r = Z/√N = {z_all:.3f}/√{len(deltas)} = {r_all:.3f}")
    print(f"  → This is the CORRECT approach for the paper")

    # --- Wilcoxon on 29 non-zero deltas (current paper approach) ---
    print("\n--- Wilcoxon on Non-Zero Deltas Only (N=29, current paper) ---")
    w_nz, p_nz = stats.wilcoxon(nonzero_deltas, alternative="greater")
    z_nz = stats.norm.ppf(1 - p_nz)
    r_nz = z_nz / math.sqrt(len(nonzero_deltas))
    print(f"  W={w_nz:.1f}, p={p_nz:.6f}, N={len(nonzero_deltas)}")
    check("wilcoxon_W (paper)", 75.0, float(round(w_nz, 1)))
    check("wilcoxon_p (paper)", 0.001, round(p_nz, 3))
    print(f"  Rank-biserial r = {r_nz:.3f}")

    # --- Cliff's delta (current paper approach — wrong for paired) ---
    print("\n--- Cliff's delta (paper's approach — NOTE: wrong for paired data) ---")
    cd = cliffs_delta(list(after), list(before))
    check("cliffs_delta (paper)", 0.017, round(cd, 3))
    print(f"  Classification: ", end="")
    abs_cd = abs(cd)
    if abs_cd < 0.147:
        print("negligible")
    elif abs_cd < 0.33:
        print("small")
    elif abs_cd < 0.474:
        print("medium")
    else:
        print("large")

    # --- RECOMMENDED: matched-pairs rank-biserial ---
    print("\n--- RECOMMENDED Effect Size: Matched-Pairs Rank-Biserial ---")
    print(f"  From all 121 pairs: r = {r_all:.3f}")
    print(f"  From 29 non-zero:   r = {r_nz:.3f}")
    abs_r = abs(r_all)
    if abs_r < 0.1:
        cls = "negligible"
    elif abs_r < 0.3:
        cls = "small"
    elif abs_r < 0.5:
        cls = "medium"
    else:
        cls = "large"
    print(f"  Classification (Cohen): {cls}")

    # --- Per-architecture mean ΔMI ---
    print("\n--- Per-Architecture Mean ΔMI ---")
    arch_groups = {}
    for p in paired:
        arch_groups.setdefault(p["arch"], []).append(p["after"] - p["before"])
    for arch in ["script_based", "modular_monolith", "layered", "mvc"]:
        ds = arch_groups.get(arch, [])
        avg = np.mean(ds) if ds else 0
        print(f"  {arch}: N={len(ds)}, mean ΔMI = {avg:+.2f}")

    check("script_based_mean_delta", 0.81, round(float(np.mean(arch_groups.get("script_based", [0]))), 2))
    check("modular_monolith_mean_delta", 0.22, round(float(np.mean(arch_groups.get("modular_monolith", [0]))), 2))
    check("layered_mean_delta", 0.94, round(float(np.mean(arch_groups.get("layered", [0]))), 2))

    # --- Reduced Coupling improvement rate ---
    print("\n--- Tactic-Specific Rates ---")
    rc_paired = [p for p in paired if p["tactic"] == "Reduced Coupling"]
    rc_impr = sum(1 for p in rc_paired if p["after"] - p["before"] > 0.001)
    rate = rc_impr / len(rc_paired) * 100 if rc_paired else 0
    check("rc_improvement_rate", 44.4, round(rate, 1))

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
