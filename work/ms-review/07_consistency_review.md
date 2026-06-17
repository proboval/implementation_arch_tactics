# Consistency Checker Review (QA pass)

**Reviewer:** QA pass (non-evaluator)
**Target:** diploma/v3 — `.tex` sources + `ref.bib`
**Date:** 2026-06-17

One row per finding. Priority: DESK-REJECT / MUST / SHOULD / NICE.

## 1. Template & required structure

| # | Check | Finding | Priority |
|---|-------|---------|----------|
| F1 | Required chapters | All present: abstract, Ch.1–6, bibliography, appendix. ✅ | — |
| F2 | Document class | `extreport`, A4, 14pt, 1.5 spacing per Innopolis template (`thesis.tex`). ✅ | — |
| F3 | Front matter | ToC, list of tables, list of figures all declared. ✅ | — |
| F4 | Abstract keywords | Present. ✅ | — |
| F5 | **Data Availability** | §6.1 claims artifacts "made publicly available" but **no URL/DOI anywhere** in the thesis. Add a Data Availability statement with an actual locator, or soften the claim. | MUST |

## 2. Formatting & floats

| # | Check | Finding | Priority |
|---|-------|---------|----------|
| F6 | `\chaptermark` placeholders | Ch.1 has `\chaptermark{Optional running chapter heading}` and Ch.2 `\chaptermark{Second Chapter Heading}` — these are template placeholder strings left in the running headers. Replace with real chapter titles. | MUST |
| F7 | Figures referenced | Pipeline figure (Fig, §3.4) is referenced. Only one figure in the body; consider an architecture-detection confusion visualization, but not required. | NICE |
| F8 | Tables referenced | All tables (§5.2–§5.6) are cross-referenced in text. ✅ | — |
| F9 | Pipeline figure numbering | The figure shows 7 nodes but the text enumerates 8 phases (statistical analysis is phase 8, not drawn). Caption/figure cover 7; clarify that phase 8 (statistics) is off-diagram. | SHOULD |

## 3. Internal & numeric consistency

| # | Check | Finding | Priority |
|---|-------|---------|----------|
| F10 | Study 1 improvement-rate denominator | Reported as **13.6%** (22/162, Table §5.2.1) but as **18.2%** (22/121, §5.5 comparison and §6 Obj.4). Both are arithmetically correct (different denominators) but the dual usage is confusing. State the denominator each time ("18.2% of completed"). | SHOULD |
| F11 | Study 3 failure-rate semantics | "25.0%" failures in Study 3 are **cloning** failures (§5.5.1); Study 1's 25.3% are **LLM-induced syntax/import** failures (§5.2.1). Same headline number, different phenomena — flagged by R1-T3; at minimum label them distinctly. | MUST |
| F12 | 57 → 56 → 42 attrition | Study 3 starts from 57 labeled repos, says "56 processable" (one dropped, unexplained), 14 cloning failures, 42 completed. Reconcile the 57→56 step. | SHOULD |
| F13 | "8 of 18" Reduced Coupling (Study 1) | §5.2.3 text: "8 of 18 completed improved (44.4%)." Table §5.2.3 shows Reduced Coupling N=23, null=5, improved=8, stable=9, degraded=1 → completed=18. ✅ Consistent. | — |
| F14 | Tactic catalog vs results | Catalog defines 4 tactics (§2.4, §3.7) incl. **Deferred Binding Time**, which appears in **no** results table. Note its absence or drop it (R2-D1). | MUST |
| F15 | "architecture-aware" vs "guided by architectural context" | Ch.3 (intro, §3.1) says "architecture-aware"; Ch.5/6 say "code-level … guided by architectural context." Inconsistent central terminology (R2-D3, EIC S3). | MUST |
| F16 | Model name forms | "Qwen3-coder-next" / "qwen3-coder-next:cloud" / "Qwen3" used interchangeably across §3.8, §4.4, §5.4 tables. Standardize, and give the version/snapshot (R1-R2). | SHOULD |
| F17 | Headline numbers cross-check | 162, 121, 41, 57, 42, 70.2%, 0.65 F1, 57.9% baseline, +0.48 [CI +0.18,+0.82], r=0.28, +1.484 [CI +0.26,+3.51] — internally consistent between abstract, Ch.5, Ch.6. ✅ | — |
| F18 | DA criticism references in-text | §5.6 and §5.12.3 cite "Devil's Advocate criticism C1/C2" — this references the *internal review* (`v3/review`), which is appropriate for a thesis defended internally but **must not** survive into any external publication. Flag for the journal version. | SHOULD |

## 4. Bibliography

| # | Check | Finding | Priority |
|---|-------|---------|----------|
| F19 | Citations resolve | Spot-check of `\cite`/`\autocite` keys (garlan1993introduction, bass2021software, horikawa2025agentic, robertson2009probabilistic, yao2022react, zhang2023repocoder, etc.) — 33 entries in `ref.bib`; biblatex/biber + IEEE style. No obvious dangling keys in the read. ✅ (full compile check recommended) | — |
| F20 | Key convention | Keys follow `[author][year][keyword]` lowercase. ✅ | — |
| F21 | Currency / forward-dated cites | Several 2025 cites (martinez2025refactoring, esposito2025generative, xu2025mantra, horikawa2025agentic, liu2025exploring, piao2025refactoring, pucho2025refactoring, shokri2024ipsynth). Verify these are published/preprinted and not placeholders; ensure DOIs/URLs present. | SHOULD |
| F22 | Coverage | 33 references is on the low side for an MS thesis literature review; consider whether architecture-recovery/conformance-checking classics (e.g., ACDC/Bunch lineage) warrant inclusion given the detection focus. | NICE |

## 5. Scope & title alignment

| # | Check | Finding | Priority |
|---|-------|---------|----------|
| F23 | Title ↔ content | Title "Automated Implementation of Architectural Tactics for Software Quality Improvement" overclaims relative to the §6 conclusion (code-level, not architectural). Align (EIC S3, R2-D3). | MUST |
| F24 | Abstract ↔ body | Abstract numbers match the body. Abstract framing ("statistically significant but modest") under-weights the sensitivity result the body reports (EIC P1). | SHOULD |

## Summary
No DESK-REJECT items. **MUST:** F5 (artifact locator), F6 (placeholder headers), F11 (failure-rate semantics), F14 (unused tactic), F15/F23 (terminology/title alignment). These are all writing-level fixes except F14, which needs a one-line factual confirmation. The numeric backbone of the thesis is internally consistent — a good sign of careful bookkeeping.
