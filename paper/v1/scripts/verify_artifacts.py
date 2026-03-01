"""Verify supplementary metrics (fan-out, docstring) from artifacts_experiment_3.

Usage: python paper/v1/scripts/verify_artifacts.py
Source: artifacts_experiment_3/artifacts/static_analysis/BEFORE/ and AFTER/
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BEFORE_DIR = ROOT / "artifacts_experiment_3" / "artifacts" / "static_analysis" / "BEFORE"
AFTER_DIR = ROOT / "artifacts_experiment_3" / "artifacts" / "static_analysis" / "AFTER"


def check(label, expected, computed, tolerance=0.01):
    if isinstance(expected, float) and isinstance(computed, float):
        match = abs(expected - computed) < tolerance
    else:
        match = str(expected) == str(computed)
    icon = "[OK]" if match else "[!!]"
    print(f"  {icon} {label}: paper={expected}, computed={computed}")
    return match


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main():
    before_repos = set(os.listdir(BEFORE_DIR)) if BEFORE_DIR.exists() else set()
    after_repos = set(os.listdir(AFTER_DIR)) if AFTER_DIR.exists() else set()
    paired = sorted(before_repos & after_repos)

    print("=" * 70)
    print("VERIFY ARTIFACT MARKERS — Supplementary Metrics")
    print("=" * 70)

    check("paired_repos", 123, len(paired))

    # --- Fan-out ---
    fo_deltas = []
    fo_changed = 0
    fo_increased = 0
    fo_decreased = 0
    pkg_changed = 0
    depth_changed = 0

    for repo in paired:
        bm = load_json(BEFORE_DIR / repo / "architecture_maintainability.json")
        am = load_json(AFTER_DIR / repo / "architecture_maintainability.json")
        if bm and am:
            b_fo = bm.get("avg_fan_out", 0) or 0
            a_fo = am.get("avg_fan_out", 0) or 0
            delta = a_fo - b_fo
            fo_deltas.append(delta)
            if abs(delta) > 0.001:
                fo_changed += 1
                if delta > 0:
                    fo_increased += 1
                else:
                    fo_decreased += 1

            b_pkg = bm.get("packages", 0) or 0
            a_pkg = am.get("packages", 0) or 0
            if b_pkg != a_pkg:
                pkg_changed += 1

            b_depth = bm.get("max_directory_depth", 0) or 0
            a_depth = am.get("max_directory_depth", 0) or 0
            if b_depth != a_depth:
                depth_changed += 1

    mean_fo = sum(fo_deltas) / len(fo_deltas) if fo_deltas else 0

    print("\n--- Fan-out ---")
    check("fanout_changed", 28, fo_changed)
    check("fanout_mean_delta", -0.016, round(mean_fo, 3))
    check("fanout_decreased", 20, fo_decreased)
    check("fanout_increased", 8, fo_increased)
    check("packages_changed", 0, pkg_changed)
    print(f"  (directory depth changed: {depth_changed})")

    # --- Docstring coverage ---
    doc_deltas = []
    doc_changed = 0
    doc_increased = 0
    doc_decreased = 0

    for repo in paired:
        bd = load_json(BEFORE_DIR / repo / "documentation_maintainability.json")
        ad = load_json(AFTER_DIR / repo / "documentation_maintainability.json")
        if bd and ad:
            b_doc = bd.get("docstring_coverage", 0) or 0
            a_doc = ad.get("docstring_coverage", 0) or 0
            delta = a_doc - b_doc
            doc_deltas.append(delta)
            if abs(delta) > 0.001:
                doc_changed += 1
                if delta > 0:
                    doc_increased += 1
                else:
                    doc_decreased += 1

    mean_doc = sum(doc_deltas) / len(doc_deltas) if doc_deltas else 0

    print("\n--- Docstring Coverage ---")
    check("docstring_changed", 17, doc_changed)
    check("docstring_mean_delta", 0.004, round(mean_doc, 3))
    check("docstring_increased", 10, doc_increased)
    check("docstring_decreased", 7, doc_decreased)

    # --- Cross-validate MI from artifacts vs CSV ---
    print("\n--- MI Cross-Validation (artifacts vs CSV) ---")
    import csv as csv_mod
    csv_path = ROOT / "experiments" / "improvement_maintainability_experiment_3.csv"
    csv_mi = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv_mod.DictReader(f):
            name = r["full_name"].split("/")[-1] if "/" in r["full_name"] else r["full_name"]
            if r["mi_before"]:
                csv_mi[name] = float(r["mi_before"])

    mismatches = 0
    checked = 0
    for repo in paired[:20]:  # spot-check first 20
        cm = load_json(BEFORE_DIR / repo / "code_maintainability.json")
        if cm and repo in csv_mi:
            art_mi = cm.get("mi_avg", 0)
            csv_val = csv_mi[repo]
            checked += 1
            if abs(art_mi - csv_val) > 0.5:
                mismatches += 1
                print(f"  [!!] {repo}: artifact={art_mi:.2f}, csv={csv_val:.2f}")

    if mismatches == 0:
        print(f"  [OK] Spot-checked {checked} repos: all MI values consistent")
    else:
        print(f"  [!!] {mismatches}/{checked} repos had MI mismatches")

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
