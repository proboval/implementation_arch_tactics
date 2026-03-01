"""Verify all DATA-type CHECK markers in paper/v1/main.tex against experiment CSV.

Usage: python paper/v1/scripts/verify_data.py
Source: experiments/improvement_maintainability_experiment_3.csv
"""

import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # implementation_arch_tactics/
CSV_PATH = ROOT / "experiments" / "improvement_maintainability_experiment_3.csv"


def load_data():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        r["mi_before"] = float(r["mi_before"]) if r["mi_before"] else None
        r["mi_after"] = float(r["mi_after"]) if r["mi_after"] else None
    return rows


def check(label, expected, computed, tolerance=0.01):
    if isinstance(expected, float) and isinstance(computed, float):
        match = abs(expected - computed) < tolerance
    else:
        match = str(expected) == str(computed)
    status = "OK" if match else "MISMATCH"
    icon = "[OK]" if match else "[!!]"
    print(f"  {icon} {label}: paper={expected}, computed={computed}  [{status}]")
    return match


def main():
    rows = load_data()
    total = len(rows)
    null_rows = [r for r in rows if r["mi_after"] is None]
    paired = [r for r in rows if r["mi_after"] is not None and r["mi_before"] is not None]

    deltas = [r["mi_after"] - r["mi_before"] for r in paired]
    improved = [r for r, d in zip(paired, deltas) if d > 0.001]
    stable = [r for r, d in zip(paired, deltas) if abs(d) <= 0.001]
    degraded = [r for r, d in zip(paired, deltas) if d < -0.001]
    nonzero_deltas = [d for d in deltas if abs(d) > 0.001]

    mi_before = [r["mi_before"] for r in paired]
    mi_after = [r["mi_after"] for r in paired]

    mean = lambda xs: sum(xs) / len(xs) if xs else 0
    median = lambda xs: sorted(xs)[len(xs) // 2] if xs else 0
    std = lambda xs: (sum((x - mean(xs)) ** 2 for x in xs) / len(xs)) ** 0.5 if xs else 0

    print("=" * 70)
    print("VERIFY DATA MARKERS — experiment CSV")
    print("=" * 70)

    print("\n--- Overall Counts ---")
    check("total_repos", 162, total)
    check("null_count", 41, len(null_rows))
    check("paired_count", 121, len(paired))
    check("improved_count", 22, len(improved))
    check("stable_count", 92, len(stable))
    check("degraded_count", 7, len(degraded))
    check("nonzero_delta_count", 29, len(nonzero_deltas))

    print("\n--- Percentages ---")
    check("null_pct", 25.3, round(len(null_rows) / total * 100, 1))
    check("improved_pct_of_total", 13.6, round(len(improved) / total * 100, 1))
    check("stable_pct_of_paired", 56.8, round(len(stable) / len(paired) * 100, 1))
    check("degraded_pct_of_total", 4.3, round(len(degraded) / total * 100, 1))

    print("\n--- Descriptive Stats (Table 1) ---")
    check("mean_mi_before", 65.11, round(mean(mi_before), 2))
    check("mean_mi_after", 65.59, round(mean(mi_after), 2))
    check("median_mi_before", 68.42, round(median(mi_before), 2))
    check("median_mi_after", 68.67, round(median(mi_after), 2))
    check("std_mi_before", 19.17, round(std(mi_before), 2))
    check("std_mi_after", 19.22, round(std(mi_after), 2))
    check("mean_delta_mi", 0.48, round(mean(deltas), 2))
    check("median_delta_mi", 0.00, round(median(deltas), 2))

    # Mean dMI for improved repos only (abstract claims +2.89)
    improved_deltas = [r["mi_after"] - r["mi_before"] for r in improved]
    check("mean_delta_mi_improved_only", 2.89, round(mean(improved_deltas), 2))

    # Mean dMI for degraded repos (claims -0.78)
    degraded_deltas = [r["mi_after"] - r["mi_before"] for r in degraded]
    check("mean_delta_mi_degraded", -0.78, round(mean(degraded_deltas), 2))

    print("\n--- Tactic Distribution ---")
    tactics = {}
    for r in rows:
        t = r.get("chosen_tactic", "Unknown")
        tactics.setdefault(t, []).append(r)

    for tactic, repos in sorted(tactics.items(), key=lambda x: -len(x[1])):
        n = len(repos)
        nulls = sum(1 for r in repos if r["mi_after"] is None)
        p = [r for r in repos if r["mi_after"] is not None and r["mi_before"] is not None]
        ds = [r["mi_after"] - r["mi_before"] for r in p]
        impr = sum(1 for d in ds if d > 0.001)
        stab = sum(1 for d in ds if abs(d) <= 0.001)
        degr = sum(1 for d in ds if d < -0.001)
        avg_d = mean(ds) if ds else 0
        print(f"  {tactic}: N={n}, Null={nulls}, Impr={impr}, Stable={stab}, Degr={degr}, dMI={avg_d:+.2f}")

    most_frequent = max(tactics, key=lambda t: len(tactics[t]))
    freq_pct = len(tactics[most_frequent]) / total * 100
    check("most_frequent_tactic", "Decomposability", most_frequent)
    check("most_frequent_pct", 63.6, round(freq_pct, 1))

    print("\n--- Table 2: Per-Tactic Verification ---")
    # Check specific table values
    decomp = tactics.get("Decomposability", [])
    decomp_null = sum(1 for r in decomp if r["mi_after"] is None)
    decomp_paired = [r for r in decomp if r["mi_after"] is not None and r["mi_before"] is not None]
    decomp_ds = [r["mi_after"] - r["mi_before"] for r in decomp_paired]
    decomp_impr = sum(1 for d in decomp_ds if d > 0.001)
    decomp_stab = sum(1 for d in decomp_ds if abs(d) <= 0.001)
    check("decomp_N", 103, len(decomp))
    check("decomp_null", 29, decomp_null)
    check("decomp_impr", 7, decomp_impr)
    check("decomp_stable", 63, decomp_stab)
    check("decomp_mean_delta", 0.55, round(mean(decomp_ds), 2))
    check("decomp_null_rate", 28.2, round(decomp_null / len(decomp) * 100, 1))

    rc = tactics.get("Reduced Coupling", [])
    rc_null = sum(1 for r in rc if r["mi_after"] is None)
    rc_paired = [r for r in rc if r["mi_after"] is not None and r["mi_before"] is not None]
    rc_ds = [r["mi_after"] - r["mi_before"] for r in rc_paired]
    rc_impr = sum(1 for d in rc_ds if d > 0.001)
    rc_stab = sum(1 for d in rc_ds if abs(d) <= 0.001)
    check("rc_N", 23, len(rc))
    check("rc_null", 5, rc_null)
    check("rc_impr", 8, rc_impr)
    check("rc_stable", 9, rc_stab)
    check("rc_mean_delta", 0.70, round(mean(rc_ds), 2))
    check("rc_impr_rate", 44.4, round(rc_impr / len(rc_paired) * 100, 1))

    lm = tactics.get("Localized Modification", [])
    lm_null = sum(1 for r in lm if r["mi_after"] is None)
    lm_paired = [r for r in lm if r["mi_after"] is not None and r["mi_before"] is not None]
    lm_ds = [r["mi_after"] - r["mi_before"] for r in lm_paired]
    lm_impr = sum(1 for d in lm_ds if d > 0.001)
    lm_stab = sum(1 for d in lm_ds if abs(d) <= 0.001)
    check("lm_N", 32, len(lm))
    check("lm_null", 5, lm_null)
    check("lm_impr", 6, lm_impr)
    check("lm_stable", 19, lm_stab)
    check("lm_mean_delta", 0.13, round(mean(lm_ds), 2))

    print("\n--- Architecture Distribution ---")
    archs = {}
    for r in rows:
        a = r.get("architecture_summary", "Unknown")
        archs.setdefault(a, []).append(r)

    for arch, repos in sorted(archs.items(), key=lambda x: -len(x[1])):
        n = len(repos)
        pct = n / total * 100
        nulls = sum(1 for r in repos if r["mi_after"] is None)
        null_pct = nulls / n * 100
        p = [r for r in repos if r["mi_after"] is not None and r["mi_before"] is not None]
        ds = [r["mi_after"] - r["mi_before"] for r in p]
        impr = sum(1 for d in ds if d > 0.001)
        degr = sum(1 for d in ds if d < -0.001)
        avg_d = mean(ds) if ds else 0
        print(f"  {arch}: N={n} ({pct:.1f}%), Null={nulls} ({null_pct:.1f}%), Impr={impr}, Degr={degr}, dMI={avg_d:+.2f}")

    check("modular_monolith_pct", 51.2, round(len(archs.get("modular_monolith", [])) / total * 100, 1))
    check("script_based_pct", 43.8, round(len(archs.get("script_based", [])) / total * 100, 1))

    print("\n--- Table 3: Per-Architecture Verification ---")
    for arch_name, expected_n, expected_null_pct in [
        ("script_based", 71, 29.6),
        ("modular_monolith", 83, 19.3),
        ("layered", 6, 50.0),
        ("mvc", 2, 50.0),
    ]:
        repos = archs.get(arch_name, [])
        n = len(repos)
        nulls = sum(1 for r in repos if r["mi_after"] is None)
        null_pct = nulls / n * 100 if n else 0
        p = [r for r in repos if r["mi_after"] is not None and r["mi_before"] is not None]
        ds = [r["mi_after"] - r["mi_before"] for r in p]
        impr = sum(1 for d in ds if d > 0.001)
        degr = sum(1 for d in ds if d < -0.001)
        avg_d = mean(ds) if ds else 0
        check(f"{arch_name}_N", expected_n, n)
        check(f"{arch_name}_null_pct", expected_null_pct, round(null_pct, 1))
        print(f"    Impr={impr}, Degr={degr}, dMI={avg_d:+.2f}")

    print("\n--- Specific Repo Values ---")
    for r in rows:
        name = r.get("full_name", "")
        if "get-subscribe" in name.lower() or "get_subscribe" in name.lower():
            if r["mi_before"] is not None and r["mi_after"] is not None:
                delta = r["mi_after"] - r["mi_before"]
                check("get_subscribe_delta", 13.52, round(delta, 2))
                print(f"    full_name: {name}")
        if "whoogle" in name.lower():
            if r["mi_before"] is not None and r["mi_after"] is not None:
                check("whoogle_mi_before", 67.06, round(r["mi_before"], 2))
                check("whoogle_mi_after", 69.74, round(r["mi_after"], 2))
                print(f"    full_name: {name}")

    # Top 3 gains
    print("\n--- Top 3 Individual Gains ---")
    gained = [(r, r["mi_after"] - r["mi_before"]) for r in paired]
    gained.sort(key=lambda x: -x[1])
    for i, (r, d) in enumerate(gained[:3]):
        print(f"  #{i+1}: {r['full_name']} dMI={d:+.2f} (tactic={r['chosen_tactic']}, arch={r['architecture_summary']})")

    # All 7 degradations in modular_monolith?
    print("\n--- Degradation Check ---")
    all_degraded_archs = [r["architecture_summary"] for r in degraded]
    all_mm = all(a == "modular_monolith" for a in all_degraded_archs)
    check("all_degradations_modular_monolith", True, all_mm)
    if not all_mm:
        for r in degraded:
            print(f"    {r['full_name']}: arch={r['architecture_summary']}, dMI={r['mi_after']-r['mi_before']:+.2f}")

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
