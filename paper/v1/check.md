# Validation Checklist — paper/v1/main.tex

Every `\CHECK{}` marker and unchecked claim that needs verification before submission.

**Run scripts to verify:** `PYTHONUTF8=1 python paper/v1/scripts/verify_data.py` (and `verify_stats.py`, `verify_artifacts.py`)

Legend: OK = verified against data, !! = mismatch found, ?? = needs manual check

---

## Abstract (line 77)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 77 | DATA | 162 | total repos in CSV | `verify_data.py → total_repos` | OK |
| 77 | DATA | 121 | repos with paired MI | `verify_data.py → paired_count` | OK |
| 77 | DATA | 22 | improved repos | `verify_data.py → improved_count` | OK |
| 77 | STAT | +2.89 | mean dMI of 22 improved | `verify_data.py → mean_delta_mi_improved_only` | OK |
| 77 | DATA | 92 | stable repos | `verify_data.py → stable_count` | OK |
| 77 | DATA | 7 | degraded repos | `verify_data.py → degraded_count` | OK |
| 77 | STAT | W=75.0, p=0.001 | Wilcoxon test | `verify_stats.py → wilcoxon_W` | !! W convention differs (scipy=360.0) |
| 77 | STAT | negligible | Cliff's delta class | `verify_stats.py → cliffs_delta` | OK (0.017=negligible) but wrong metric for paired data |
| 77 | DATA | 63.6% | Decomposability frequency | `verify_data.py → most_frequent_pct` | OK |

---

## Background and Related Work (lines 100-120)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 107 | SOURCE | 10% increase in maintenance effort | Rahmati 2021 paper | manual | OK (verified: Case Study 2 ~10% effort increase) |
| 110 | SOURCE | 82.8% success rate (MANTRA) | Xu 2025 paper | manual | OK (verified: 582/703 = 82.8%) |
| 110 | SOURCE | ~~96.3% single-file refactorings~~ | ~~Horikawa 2025~~ | manual | FIXED — fabricated statistic, replaced with qualitative description from Horikawa |
| 112 | SOURCE | 86.7% refactoring opportunities | Liu 2025 paper | manual | OK (verified: ChatGPT success rate after prompt narrowing) |

**All SOURCE CHECK markers removed from lines 107-112.** Horikawa claim replaced with accurate qualitative text: "agentic refactorings are dominated by low-level, localized edits."

---

## Methodology (lines 122-180)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 147 | DATA | 5 Python source files minimum | pipeline config / filter code | manual | !! MISMATCH: `dataset_create.py` only checks `len(py_files) > 0` (at least 1, not 5) |
| 149 | DATA | star counts >= 10 | pipeline config / filter code | manual | !! MISLEADING: config.py STARS=(1000,2000); actual dataset range 20-11889. ">= 10" is technically true but understates actual filtering |
| 151 | DATA | 162 repos retained | CSV row count | `verify_data.py → total_repos` | OK |

---

## Implementation (lines 182-189)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 185 | DATA | Qwen3-coder-next:cloud | config.py / docker-compose | manual | OK (config.py: `MODEL_NAME = "qwen3-coder-next:cloud"`) |
| 185 | DATA | 0.2 (temperature) | config.py | manual | OK (call_llm.py: `temperature: float = 0.2` default) |

---

## Results §5.1 Overall Quantitative Impact (lines 191-218)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 195 | DATA | 162 | total | `verify_data.py → total_repos` | OK |
| 195 | DATA | 41 (25.3%) null | null count | `verify_data.py → null_count, null_pct` | OK |
| 195 | DATA | 121 paired | paired count | `verify_data.py → paired_count` | OK |
| 198 | DATA | N=121 in table caption | | `verify_data.py → paired_count` | OK |
| 206 | DATA | Mean MI before=65.11 | | `verify_data.py → mean_mi_before` | OK |
| 206 | DATA | Mean MI after=65.59 | | `verify_data.py → mean_mi_after` | OK |
| 207 | DATA | Median before=68.42 | | `verify_data.py → median_mi_before` | OK |
| 207 | DATA | Median after=68.67 | | `verify_data.py → median_mi_after` | OK |
| 208 | DATA | Std before=19.17 | | `verify_data.py → std_mi_before` | OK |
| 208 | DATA | Std after=19.22 | | `verify_data.py → std_mi_after` | OK |
| 210 | DATA | Mean dMI=+0.48 | | `verify_data.py → mean_delta_mi` | OK |
| 211 | DATA | Median dMI=0.00 | | `verify_data.py → median_delta_mi` | OK |
| 216 | DATA | 29 non-zero deltas | | `verify_data.py → nonzero_delta_count` | OK |
| 216 | STAT | W=75.0 | Wilcoxon W | `verify_stats.py` | !! scipy gives W=360.0 (different convention) |
| 216 | STAT | p=0.001 | Wilcoxon p | `verify_stats.py` | OK |
| 216 | STAT | 0.017 (negligible) | Cliff's delta | `verify_stats.py` | OK value, but !! wrong metric for paired data |
| 218 | DATA | 56.8% of completed cases | stable % | `verify_data.py → stable_pct_of_paired` | !! MISMATCH: 92/121=76.0%, not 56.8%. Paper uses 92/162=56.8% but says "of completed cases" |

---

## Results §5.2 Success Cases (lines 227-255)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 229 | DATA | 22 (13.6%) improved | | `verify_data.py → improved_count` | OK (but 13.6%=22/162, see denominator issue) |
| 229 | DATA | get_subscribe dMI=+13.52 | | `verify_data.py → get_subscribe_delta` | OK |
| 229 | DATA | whoogle before=67.06 | | `verify_data.py → whoogle_mi_before` | OK |
| 229 | DATA | whoogle after=69.74 | | `verify_data.py → whoogle_mi_after` | OK |
| 238 | DATA | RC: 8/18 improved | | `verify_data.py → rc_impr, rc_paired` | OK |
| 238 | STAT | 44.4% RC improvement rate | | `verify_data.py → rc_impr_rate` | OK |
| 238 | DATA | Decomp N=103 | | `verify_data.py → decomp_N` | OK |
| 238 | DATA | Decomp null=29 (28.2%) | | `verify_data.py → decomp_null, decomp_null_rate` | OK |

---

## Results §5.3 Failure Rates (line 258)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 258 | DATA | 41 (25.3%) null | | `verify_data.py → null_count` | OK |
| 258 | DATA | 4.3% (7 repos) degraded | | `verify_data.py → degraded_count` | OK |
| 258 | STAT | degraded mean dMI=-0.78 | | `verify_data.py → mean_delta_mi_degraded` | OK |

---

## Results §5.4 Architectural Influence (lines 260-280)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 261 | DATA | modular monolith 51.2% | | `verify_data.py → modular_monolith_pct` | OK |
| 261 | DATA | script-based 43.8% | | `verify_data.py → script_based_pct` | OK |
| 261 | STAT | script-based mean dMI=+0.81 | | `verify_stats.py → script_based_mean_delta` | OK |
| 261 | CLAIM | top 3: get_subscribe +13.52, ps4-exploit-host +11.45, DXY-COVID-19-Crawler +9.99 | | `verify_data.py → Top 3 Individual Gains` | OK |
| 261 | DATA | script-based null rate=29.6% | | `verify_data.py → script_based_null_pct` | OK |
| 263 | STAT | modular monolith mean dMI=+0.22 | | `verify_stats.py → modular_monolith_mean_delta` | OK |
| 263 | CLAIM | all 7 degradations in modular_monolith | | `verify_data.py → all_degradations_modular_monolith` | OK |
| 263 | STAT | layered mean dMI=+0.94 | | `verify_stats.py → layered_mean_delta` | OK |

---

## Results §5.5 Discussion (lines 282-287)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 283 | DATA | 25.3% failure rate | | `verify_data.py → null_pct` | OK |
| 283 | DATA | 13.6% improvement rate | | `verify_data.py → improved_pct_of_total` | OK |
| 283 | SOURCE | MANTRA 82.8% | Xu 2025 paper | manual | OK (verified, CHECK marker removed) |
| 285 | DATA | 56.8% stable | | | !! same denominator issue as line 218 |

---

## Results §5.6 Supplementary Metrics (lines 289-296)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 290 | DATA | 123 paired artifact repos | | `verify_artifacts.py → paired_repos` | OK |
| 292 | DATA | fan-out: 28 changed | | `verify_artifacts.py → fanout_changed` | OK |
| 292 | STAT | fan-out mean delta=-0.016 | | `verify_artifacts.py → fanout_mean_delta` | OK |
| 292 | DATA | 20 decreased, 8 increased | | `verify_artifacts.py → fanout_decreased, fanout_increased` | OK |
| 294 | DATA | docstring: 17 changed | | `verify_artifacts.py → docstring_changed` | OK |
| 294 | STAT | docstring mean delta=+0.004 | | `verify_artifacts.py → docstring_mean_delta` | OK |
| 294 | DATA | 10 increased, 7 decreased | | `verify_artifacts.py → docstring_increased, docstring_decreased` | OK |

---

## Threats + Conclusion (lines 298-318)

| Line | Type | Value in Paper | Verify Against | Script | Status |
|------|------|----------------|----------------|--------|--------|
| 306 | DATA | 22/162 | | `verify_data.py` | OK |
| 312 | DATA | all 162 repos | | `verify_data.py → total_repos` | OK |
| 314 | STAT | mean dMI=+0.48 | | `verify_data.py → mean_delta_mi` | OK |
| 314 | STAT | p=0.001 | | `verify_stats.py` | OK |
| 314 | DATA | 22 improved | | `verify_data.py → improved_count` | OK |
| 314 | DATA | 56.8% unchanged | | | !! denominator issue |
| 314 | DATA | 25.3% failed | | `verify_data.py → null_pct` | OK |
| 318 | DATA | 25.3% | | `verify_data.py → null_pct` | OK |

---

## Table 2 (Per-Tactic) — Completeness Check

| Tactic | N | Null | Impr | Stable | **Degr (MISSING from table)** | dMI |
|--------|---|------|------|--------|-------------------------------|-----|
| Decomposability | 103 | 29 | 7 | 63 | **4** | +0.55 |
| Localized Mod. | 32 | 5 | 6 | 19 | **2** | +0.13 |
| Reduced Coupling | 23 | 5 | 8 | 9 | **1** | +0.70 |
| Other | 4 | 2 | 1 | 1 | **0** | +0.67 |

Source: `verify_data.py → Tactic Distribution`

---

## Unchecked Claims (no CHECK marker but need validation)

| Line | Claim | Verify Against | Status |
|------|-------|----------------|--------|
| 89 | "60-80% lifecycle costs" | Bass 2021 book | OK (standard figure; also in Abdelmoez 2006: "60-80% of the overall software system cost") |
| 103 | Kim 2009 "systematically improve quality attributes" | Kim 2009 paper | OK (Kim provides systematic quality-driven approach with feature models and RBML specs for tactic selection) |
| 103 | Bogner 2019 "coupling reduction leads to measurable improvements" | Bogner 2019 paper | !! OVERSTATEMENT: Bogner did qualitative mapping of modifiability tactics to service patterns, NOT quantitative measurement. Should say "coupling reduction is systematically addressed through modifiability tactics" |
| 112 | Shokri: "95% syntactic correctness, 5% semantic" | Shokri 2024 paper | OK (verified: 19/20 syntactic, 1/20 semantic from converted paper) |
| 127 | "non-normally distributed" (implies Shapiro-Wilk was done) | `verify_stats.py → Shapiro-Wilk` | OK (W=0.34, p<0.001) |
| 187 | "catalog of over 40 architectural tactics" | Marquez 2022 + actual CSV | !! MISMATCH: actual catalog CSV has 32 tactics (not "over 40"); §3.5 lists only 4 used. Should fix to "32" or "over 30" |
| 263 | "15 of 67 completed modular_monolith improved" | CSV | OK (verified: 83 total - 16 null = 67 paired; 15 improved) |

---

## Summary of Issues Found

| Severity | Issue | Lines |
|----------|-------|-------|
| !! | **stable_pct denominator**: paper says "56.8% of completed cases" but 92/121=76.0%. The 56.8%=92/162 is of total repos, not completed. Fix text or number. | 218, 285, 314 |
| !! | **Wilcoxon W value**: paper says W=75.0, scipy gives W=360.0. Different conventions — need to clarify which (T+ vs T-). | 77, 216 |
| !! | **Cliff's delta wrong for paired**: Should use matched-pairs rank-biserial (r=0.280, "small" effect) instead. | 77, 216 |
| !! | **Table 2 missing Degraded column**: 7 degraded repos not visible in per-tactic table. | 240-255 |
| !! | **"Over 40 tactics" vs "4 tactics"**: Implementation §4 says 40+, actual catalog has 32, Methodology §3.5 lists 4. | 163, 187 |
| !! | **"5 Python source files minimum"**: Code only checks `len(py_files) > 0`. No minimum of 5 enforced. | 147 |
| !! | **"star counts >= 10"**: Misleading — actual filter ranges were (1-20), (100-1200), (1000-2000). Min in dataset is 20 stars, not 10. | 149 |
| !! | **Bogner 2019 overstatement**: Paper claims "coupling reduction leads to measurable quality improvements" but Bogner did qualitative mapping, not quantitative measurement. | 103 |
| FIXED | **Horikawa 96.3% fabricated**: "96.3% single-file refactorings" did not exist in Horikawa 2025. Replaced with qualitative description. | 110 |
