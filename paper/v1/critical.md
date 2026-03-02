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

### 3. ~~RQ1 is trivially answered — no validation of detection accuracy~~ — FIXED
**Fix applied:** RQ1 reframed from binary "Can..." to empirical "How reliably does..." with confidence scores and structural alignment. Conclusion updated to report confidence distribution (median 0.95, range 0.85–0.98) and tactic coherence (94% of script-based repos received Decomposability), while explicitly acknowledging the absence of ground-truth validation as a limitation. Manual expert validation added to future work.

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

### 8. ~~Layered architecture conclusions from N=3~~ — FIXED
**Fix applied:** Added explicit caveat: "though this observation is based on only 3 completed repositories and cannot support statistical conclusions; it requires validation with a substantially larger sample." Also added dataset scaling to future work.

---

### 9. ~~No data availability / replication package~~ — FIXED
**Fix applied:** Added `\section*{Data Availability}` before References with anonymized URL (`https://github.com/ANONYMIZED`). Actual URL to be added in camera-ready version.

---

### 10. ~~Qwen3-coder-next model choice unjustified~~ — FIXED
**Fix applied:** Added justification: 256k context window necessary for repository-level analysis, local deployment via Ollama ensuring reproducibility without API dependencies. Multi-model comparison explicitly noted as future work.

---

### 11. ~~Supplementary metrics lack statistical tests~~ — FIXED
**Fix applied:** Added explicit justification: "Given the small number of repositories with non-zero changes (28/123 for fan-out, 17/123 for docstring coverage), formal hypothesis testing was not meaningful for these metrics; we report descriptive statistics only."

---

## Minor Issues

### 12. ~~Section 3.6 vs Section 4 overlap~~ — FIXED
**Fix applied:** Condensed §3.6 from three detailed paragraphs to a single concise paragraph listing the three layers conceptually. Technical details (model name, prompt structure, confidence scores, JSON format) remain only in §4. Added cross-reference: "Section~4 details the technical realization of each layer."

---

### 13. ~~Abstract mean dMI=+2.89 vs body +0.48~~ — FIXED
**Line 77:** Now reads "mean dMI = +2.89 among improved", clarifying this is the improved-only subset, not the overall mean.

---

### 14. ~~"Transformation Gap" coined but not defined~~ — FIXED
**Fix applied:** Changed from informal "what we term" to formal definition: "We define this as the *Transformation Gap*---the disconnect between detecting architectural deficiencies through static analysis or expert review and automatically implementing design-level corrections that address them."

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

### 21. ~~"cataloging over 40 tactics" in Background still says "over 40"~~ — FIXED
**Fix applied:** Changed to "mapping architectural tactics across 12 quality attributes based on 91 primary studies" — accurately describes what Márquez 2022 SMS did without claiming a specific tactic count that contradicts §4's "32."

---

## Summary

| Severity | Total | Fixed | Open | Key themes |
|----------|-------|-------|------|------------|
| Critical | 5 | 5 | 0 | Statistical methodology, RQ1 reframed with confidence scores |
| Major | 6 | 6 | 0 | Replication package, model justification, supplementary stats |
| Minor | 5 | 5 | 0 | Section overlap resolved, terminology defined |
| New (validation) | 5 | 5 | 0 | Fabricated stat, code-paper mismatches |

**All 21 issues FIXED.** No remaining OPEN issues.

**Key fixes applied in final round:**
- #3: RQ1 reframed from binary to empirical; conclusion reports confidence distribution + tactic coherence
- #8: Explicit N=3 caveat added
- #9: Data Availability section added (anonymized URL)
- #10: Model justification added (256k context, local deployment)
- #11: Statistical test omission justified (small N of changes)
- #12: §3.6 condensed; clear boundary with §4
- #14: "Transformation Gap" formally defined
- #21: "over 40 tactics" → accurate Márquez SMS description

**Future work expanded:** Added (5) dataset scaling for underrepresented architectures and (6) manual expert validation of architecture detection.
