# Critical Review — "Can LLMs Implement Architectural Tactics? Early Results"

Reviewer-perspective critique of `paper/v1/main.tex` for EASE 2026 Short Papers.
Organized by severity. Line references to main.tex.

**Status legend:** FIXED = addressed in current draft, OPEN = still needs attention

---

## Critical Issues (would likely cause rejection or major revision)

### 1. ~~Wilcoxon test reported on pre-filtered N=29, not N=121~~ — FIXED
**Line 216:** Now reports "Wilcoxon signed-rank test on all 121 paired observations (W=360.0, p=0.001, 29 non-zero differences)."

Also added Shapiro-Wilk normality test (W=0.34, p<0.001) to justify the non-parametric choice.

**Script:** `verify_stats.py`

---

### 2. ~~Cliff's delta is the wrong effect size for paired data~~ — FIXED
**Line 216:** Replaced with matched-pairs rank-biserial correlation r=0.28 ("small" effect). Also updated abstract (line 77), methodology (line 127), and threats (line 306) to consistently use rank-biserial.

**Script:** `verify_stats.py`

---

### 3. RQ1 is trivially answered — no validation of detection accuracy — OPEN
**Lines 93, 306:** "RQ1: Can an automated LLM-based pipeline detect architectural patterns and select appropriate tactics?" → Answer: "Yes, for all 162 repositories."

An LLM will always produce output when asked to classify. A 100% "success rate" for architecture detection is meaningless without validation that the detections are *correct*. The paper provides no ground truth, no manual annotation, and no sample validation.

**Fix options:**
- (a) Manually validate a random sample (e.g., 20 repos) and report agreement rate
- (b) Reframe RQ1 to: "Can the pipeline produce plausible architectural analyses?" and discuss plausibility criteria
- (c) Use the ai_analysis JSON artifacts (which include confidence scores) to report a distribution of confidence levels

---

### 4. ~~Table 2 missing Degraded column~~ — FIXED
**Lines 245-252:** Degraded column added. Rows now sum correctly: Decomposability 29+7+63+4=103, Localized 5+6+19+2=32, Reduced Coupling 5+8+9+1=23, Other 2+1+1+0=4.

**Script:** `verify_data.py` — "Tactic Distribution" section.

---

### 5. ~~"Over 40 tactics" vs "4 tactics" contradiction~~ — FIXED
**Line 187:** Changed to "a catalog of 32 architectural tactics" (matching the actual `architectural_tactics_complete_catalog.csv`). §3.5 lists the 4 maintainability-related tactics that were actually selected by the LLM.

**Note:** The relationship between the full 32-tactic catalog and the 4 observed tactics could be made more explicit. The LLM has access to all 32 but consistently selects from the 4 maintainability-relevant ones. Consider adding a sentence explaining this.

---

## Major Issues (would require revision)

### 6. ~~No normality test reported to justify Wilcoxon~~ — FIXED
**Line 216:** Added: "A Shapiro-Wilk test confirmed non-normality of the delta distribution (W=0.34, p<0.001), justifying the use of a non-parametric test."

---

### 7. ~~"56.8% of completed cases" — wrong denominator~~ — FIXED
Fixed in 3 locations (lines 218, 285, 314). Now consistently says "76.0% of completed cases (92 of 121)."

---

### 8. Layered architecture conclusions from N=3 — OPEN
**Line 263:** "layered structures may provide the most favorable context" based on 3 completed repositories.

No statistical conclusion is possible from N=3. The claim is speculative at best.

**Fix:** Add explicit caveat: "though this observation is based on only 3 completed repositories and requires further investigation with a larger sample."

---

### 9. No data availability / replication package — OPEN
**Line 79 (abstract):** Claims "reproducible methodology" but provides no link to code, data, or artifacts.

EASE 2026 values reproducibility. Most SE venues now expect or require a data availability statement.

**Fix:** Add before References:
```latex
\section*{Data Availability}
The replication package, including pipeline code, experiment data, and analysis scripts, is available at [URL].
```

---

### 10. Qwen3-coder-next model choice unjustified — OPEN
**Line 185:** Uses "Qwen3-coder-next:cloud" without justification.

Reviewers will ask: Why not GPT-4, Claude, CodeLlama, or DeepSeek-Coder? The model is relatively obscure and has no established SE benchmarks.

**Fix:** Add 1-2 sentences justifying the choice, e.g.: "We selected Qwen3-coder-next for its 256k context window (necessary for repository-level analysis), open-source availability enabling local deployment, and competitive coding benchmarks [citation]."

---

### 11. Supplementary metrics lack statistical tests — OPEN
**Lines 289-296:** Fan-out and docstring deltas are reported descriptively only. If MI gets a Wilcoxon test, reviewers will ask why supplementary metrics don't.

**Fix:** Either add Wilcoxon tests for fan-out and docstring deltas, or explicitly state: "Given the small number of changes (28/123 for fan-out, 17/123 for docstring), statistical testing was not meaningful for these metrics."

---

## Minor Issues

### 12. Section 3.6 vs Section 4 overlap — OPEN
The LLM transformation process is described twice: once in Methodology §3.6 (Architecture Detection / Tactic Selection / Implementation) and again in Implementation §4 with more detail. The boundary between "what we do" and "how we do it" is blurry.

**Fix:** Sharpen the distinction. §3.6 should describe the conceptual method (what inputs, what outputs, what decisions). §4 should describe technical implementation (model name, prompt structure, JSON format, tooling).

---

### 13. ~~Abstract mean dMI=+2.89 vs body +0.48~~ — FIXED
**Line 77:** Now reads "mean dMI = +2.89 among improved", clarifying this is the improved-only subset, not the overall mean.

---

### 14. "Transformation Gap" coined but not defined — OPEN
**Line 89:** Introduces the term in quotes as if established, but it appears to be coined by the authors.

**Fix:** Either formally define it ("We define the Transformation Gap as the disconnect between...") or remove the term and describe the gap directly.

---

### 15. ~~Empty acknowledgments~~ — FIXED
Acknowledgments block commented out (appropriate for double-anonymous submission).

---

### 16. ~~CHECK markers must be removed~~ — FIXED
All 61 `\CHECK{}` markers stripped. The `\newcommand{\CHECK}` definition and associated `xcolor`/`soul` packages removed.

---

## New Issues Found During Validation

### 17. ~~Fabricated statistic: "96.3% single-file refactorings" (Horikawa 2025)~~ — FIXED
**Line 110 (old):** Attributed "96.3% of agentic refactorings are confined to a single file" to Horikawa 2025. This number does not exist in the paper (confirmed via full-text search and NotebookLM cross-validation). Likely hallucinated from an earlier Claude session.

**Fix applied:** Replaced with accurate qualitative description: "agentic refactorings are dominated by low-level, localized edits (renaming, type changes), with agents performing fewer high-level design changes than human developers."

---

### 18. ~~"5 Python source files minimum" — not enforced in code~~ — FIXED
**Line 147 (old):** Paper claimed minimum 5 Python files, but `dataset_create.py` only checks `len(py_files) > 0`.

**Fix applied:** Changed to "Presence of Python source files (.py) to ensure the project contains analyzable code."

---

### 19. ~~"star counts >= 10" — misleading~~ — FIXED
**Line 149 (old):** Paper said ">= 10" but actual dataset ranges were (1-20), (100-1200), (1000-12000). Minimum in dataset is 20.

**Fix applied:** Changed to "star counts across multiple ranges from 20 to 12,000."

---

### 20. ~~Bogner 2019 overstatement~~ — FIXED
**Line 103 (old):** "coupling reduction leads to measurable quality improvements" — Bogner did qualitative mapping, not quantitative measurement.

**Fix applied:** Changed to "modifiability tactics---particularly coupling reduction---are systematically addressed through service-oriented design patterns."

---

### 21. "cataloging over 40 tactics" in Background still says "over 40" — OPEN
**Line 107:** Background §2.1 still says "cataloging over 40 tactics" when referencing Marquez 2022. The Implementation section (line 187) was fixed to "32", but this Background reference was not updated.

**Fix:** Either change to "cataloging over 30 tactics" or verify the exact Marquez 2022 count. Note: the actual CSV has 32 tactics, but Marquez 2022's SMS may catalogue a different number across all quality attributes (the CSV only includes a subset).

---

## Summary

| Severity | Total | Fixed | Open | Key themes |
|----------|-------|-------|------|------------|
| Critical | 5 | 4 | 1 | Statistical methodology (FIXED), RQ1 validity (OPEN) |
| Major | 6 | 3 | 3 | Replication package, model justification, supplementary stats |
| Minor | 5 | 3 | 2 | Section overlap, terminology |
| New (validation) | 5 | 5 | 0 | Fabricated stat, code-paper mismatches |

**Remaining OPEN issues (7):**
1. **#3 RQ1 trivially answered** — needs ground-truth validation or reframing
2. **#8 Layered N=3** — needs caveat
3. **#9 No replication package** — needs URL
4. **#10 Model choice unjustified** — needs 1-2 sentences
5. **#11 Supplementary metrics** — needs statistical tests or justification for omitting
6. **#12 Section overlap** — needs sharper method/implementation boundary
7. **#14 "Transformation Gap"** — needs definition or removal
8. **#21 "over 40" in Background** — needs correction to match §4's "32"

**Most impactful fix already applied:** Correcting the effect size from "negligible" (Cliff's delta 0.017) to "small" (rank-biserial r=0.28) significantly strengthens the paper's contribution claim.
