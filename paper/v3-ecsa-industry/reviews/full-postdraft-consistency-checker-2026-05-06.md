# Review Output Template (post-draft mode)

**Reviewer profile:** Consistency Checker  
**Target:** paper/v3-ecsa-industry/main.tex (full paper)  
**Date:** 2026-05-06  
**Mode:** post-draft  
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Findings table

| # | Category | Check | Status | Finding | Priority |
|---|----------|-------|--------|---------|----------|
| C1 | ECSA policy | AI disclosure (GAIDeT) | ⚠️ Partial | Acknowledgements section is present and names tools (GitHub Copilot, Claude Sonnet, Semantic Scholar MCP, NotebookLM) with role descriptions. However, it is not structured using GAIDeT domain categories (conceptualization, literature review, methodology, code generation, data management, quality assurance, writing, figures/multimedia, supervision, ethical review). The roles described are: writing assistance, code generation, data analysis/table generation, literature discovery. Missing explicit statement for: data management, quality assurance, supervision. For strict compliance, restructure into GAIDeT format with explicit "not used" or N/A for omitted domains. | SHOULD |
| C2 | ECSA policy | Data Availability section | ⚠️ Partial | Section `\section*{Data Availability}` is present immediately after Conclusions and before Acknowledgements (correct order). Content claims artifacts are available at `https://github.com/anonymous-ghub/Architecture-Detection-in-Software-Repositories`. This URL contains "anonymous-ghub" — an anonymous placeholder pattern inconsistent with ECSA single-blind review (authors are named). Either: (a) replace with the real repository URL, or (b) change the text to "will be made available upon acceptance at [URL]." A placeholder that resolves to nothing is technically a policy violation. | MUST |
| C3 | ECSA policy | Single-blind compliance | ✅ Pass | Authors named: Saveliy Chertkov (Innopolis University) and Andrey Sadovykh (Softeam, Paris, France). Both affiliations and emails present. No anonymization placeholders in the text body. |  |
| C4 | ECSA policy | Concurrent submission | ✅ Pass | No language indicating parallel submission. Introduction says "This work is the first stage of a broader architecture-aware pipeline" — this is forward scope description, not a concurrent submission signal. |  |
| C5 | ECSA policy | Page limit (8 pp LNCS) | ✅ Likely pass | Paper has 7 numbered sections + 2 unnumbered (Data Availability, Acknowledgements) + References. Four tables. Content volume suggests approximately 7–8 pages in compiled LNCS format. Main.pdf exists (just regenerated); no compile errors. Visual inspection recommended before submission to confirm no overflow. | NICE |
| C6 | LNCS | Document class | ✅ Pass | `\documentclass[runningheads]{llncs}` — correct LNCS template. |  |
| C7 | LNCS | Title and author block | ✅ Pass | Title present. `\author{}`, `\authorrunning{}`, `\institute{}` all present. Two institutes correctly defined with `\inst{1}` and `\inst{2}`. Emails present for both authors. |  |
| C8 | LNCS | Abstract length | ⚠️ Partial | Abstract runs approximately 155–160 words (estimated from text). LNCS recommends ≤150 words. Exceeds recommendation by ~5–10 words. Trim the final sentence ("Both findings have direct implications for practitioners building architecture-aware automation pipelines.") or condense elsewhere to reach ≤150. | SHOULD |
| C9 | LNCS | Keywords | ✅ Pass | 5 keywords present after abstract: `software architecture detection`, `large language models`, `architectural classification`, `repository analysis`, `empirical software engineering`. Within the 4–6 range. |  |
| C10 | LNCS | Section numbering | ✅ Pass | Sections 1–7 numbered correctly (Introduction, Background, Methodology, Results, Discussion, Threats to Validity, Conclusion). `\section*{Data Availability}` and `\section*{Acknowledgements}` correctly unnumbered. |  |
| C11 | LNCS | References style | ✅ Pass | `\bibliographystyle{splncs04}` — correct LNCS bibliography style. |  |
| C12 | LNCS | Figures/tables captions and references | ✅ Pass | Four tables: `tab:accuracy` (Table 1), `tab:per_class` (Table 2), `tab:mm_errors` (Table 3), `tab:confidence` (Table 4). All have captions. All are referenced in the body text. No orphan tables. |  |
| C13 | LNCS | Data Availability placement | ✅ Pass | `\section*{Data Availability}` appears after `\section{Conclusion}` and before `\section*{Acknowledgements}`. Correct order. |  |
| C14 | LNCS | Acknowledgements placement | ✅ Pass | `\section*{Acknowledgements}` appears after Data Availability and before `\bibliography{}`. Correct order. |  |
| C15 | Internal | RQ–result alignment | ✅ Pass | RQ1 (accuracy) → §4.1 answered with Table 1. RQ2 (evidence types) → §4.2 answered with accuracy deltas. RQ3 (model comparison) → §4.4 answered with per-model analysis. All three RQs answered. |  |
| C16 | Internal | Table cross-references | ✅ Pass | All four tables cited in text before or at their position. Table 3 (MM misclassifications) cited in Discussion as well ("Table~\ref{tab:mm_errors}"). |  |
| C17 | Internal | Number consistency | ✅ Pass | "57 repositories" consistent in Abstract, §3.2, §4.1, Threats, Conclusion. "70.2%" consistent in Abstract, §4.1, Discussion, Conclusion. "57.9%" (majority-class baseline) consistent in §4.1 and Conclusion. "12.3 percentage points" stated once in §4.1. |  |
| C18 | Internal | Model names consistency | ✅ Pass | Models introduced in §3.5 with full names and abbreviations. Abbreviated forms (Qwen3, DeepSeek, Gemini, Gemma4, MiniMax) used consistently in all tables. |  |
| C19 | Internal | Terminology consistency | ⚠️ Partial | Paper uses "architectural style" (§3.1, §3.2, Background), "architectural classification" (keywords, abstract), and "architecture detection" (title, §2). These are subtly different terms. §3.1 explicitly calls the task "style classification" which is correct. However, the title uses "Architecture Detection" which is broader than style classification. This inconsistency is not fatal but could prompt a reviewer question about whether the paper is about detection (is there an architecture?) or classification (which architectural style?). Since the paper does classification, not detection, consider aligning: "LLM-Based Architectural Style Classification in Practice" — though the shorter "Architecture Detection" is more memorable and is established in prior literature. Flag only if a reviewer raises it. | NICE |
| C20 | Internal | Prompt label consistency | ✅ Pass | P1–P4 labels introduced in §3.4 and used consistently in all tables and discussion text. |  |
| C21 | Bibliography | Citation resolution | ✅ Pass (estimated) | All in-text `\cite{}` keys visible in the paper body appear to have corresponding entries based on ref.bib contents verified: `esposito2025generative`, `bass2021software`, `marquez2022architectural`, `lenarduzzi2023critical`, `liu2025exploring`, `piao2025refactoring`, `horikawa2025agentic`, `shokri2024ipsynth`, `ISO25010`, `kim2009qualitydriven`, `perry1992foundations`. No compile errors reported. |  |
| C22 | Bibliography | Unused .bib entries | ⚠️ Minor | ref.bib contains entries visible in the file (`garlan1993introduction`, `garlan1995editorial`, `molnar2020study`, `albadareen2011quality`, `alqutaish2010quality`, `harrison2010how`, `bi2021mining`, `kassab2018software`, `li2021understanding`, `rosik2011assessing`) that do not appear to be cited in main.tex. These are unused entries — carry-over from a shared bibliography. Not a desk-reject issue but adds unnecessary file weight. Remove unused entries or confirm they are intentionally retained for future use. | NICE |
| C23 | Bibliography | Key convention | ✅ Pass | Visible keys follow `[author][year][keyword]` pattern: `kim2009qualitydriven`, `perry1992foundations`, `esposito2025generative`, `ISO25010` (reasonable exception for standard). |  |
| C24 | Scope/title | Title matches content | ✅ Pass | "LLM-Based Architecture Detection in Practice: An Empirical Multi-Model Evaluation" — signals architecture detection, multi-model comparison, empirical scope. Matches paper content. |  |
| C25 | Scope/title | No scope creep | ✅ Pass | Tactic selection and implementation appear only once in Conclusion: "tactic selection and implementation are under active investigation." Correct. |  |
| C26 | Scope/title | Abstract matches paper | ✅ Pass | Abstract claims: 70.2% accuracy on 57 repos, file tree + import graph is optimal, MM/layered confusion, confidence miscalibration — all verified in Results. |  |

---

## Summary counts

| Priority | Count | Items |
|----------|-------|-------|
| DESK-REJECT | 0 | — |
| MUST | 1 | C2 (Data Availability URL placeholder) |
| SHOULD | 3 | C1 (GAIDeT format), C8 (abstract length ~155 words) |
| NICE | 3 | C5 (verify final page count), C19 (terminology alignment), C22 (clean unused bib entries) |
| PASS | 19 | All other checks |

---

## Top actions before May 8 submission

1. **[MUST] Fix Data Availability URL** (C2): Replace `anonymous-ghub` placeholder with the real repository URL, or change to "will be made available upon acceptance at [URL]."
2. **[SHOULD] Trim abstract to ≤150 words** (C8): Currently ~155–160 words. Cut the final sentence or compress one earlier sentence.
3. **[SHOULD] Upgrade Acknowledgements to GAIDeT format** (C1): Add domain categories explicitly (conceptualization, methodology, code generation, writing, data management, literature review). Add "not used" for domains not applicable.
4. **[NICE] Verify final PDF page count** (C5): Open main.pdf and confirm it fits within 8 pages including references.
5. **[NICE] Remove unused .bib entries** (C22): Clean up carry-over bibliography entries.
