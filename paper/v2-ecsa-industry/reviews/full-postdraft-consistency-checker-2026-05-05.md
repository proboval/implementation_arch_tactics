# Review: Consistency Checker
**Reviewer profile:** Consistency Checker (QA pass — ECSA policy compliance, LNCS formatting, internal coherence)
**Target:** paper/v2-ecsa-industry/main.tex — full paper
**Date:** 2026-05-05
**Mode:** post-draft
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Findings

| # | Category | Check | Status | Finding | Priority |
|---|----------|-------|--------|---------|----------|
| C1 | Policy | AI disclosure | ✅ Pass | Acknowledgements present with named tools (GitHub Copilot, Claude Sonnet) and GAIDeT-style role descriptions (writing, code gen, data analysis, literature discovery). | — |
| C2 | Policy | Data Availability | ✅ Pass | Section present after Conclusions, before References. Contains replication package URL. | — |
| C3 | Policy | Single-blind | ✅ Pass | Authors named: S. Chertkov and A. Sadovykh, Innopolis University. Emails present. | — |
| C4 | Policy | Concurrent submission | ✅ Pass | No indicators of parallel submission in text. | — |
| C5 | Policy | Plagiarism risk | ✅ Pass | v2 is a focused re-scoping. Background and Discussion are original drafts. Results tables overlap with source experiment but the analysis and framing are new. No verbatim paragraphs from v1. | — |
| C6 | Policy | Page limit | ✅ Pass | Compiled output: 8 pages. Within limit. | — |
| C7 | LNCS | Document class | ✅ Pass | `\documentclass[runningheads]{llncs}` — correct. | — |
| C8 | LNCS | Title / author block | ✅ Pass | Title, running title, authors, affiliation, email all present in standard LNCS format. | — |
| C9 | LNCS | Abstract length | ⚠️ Over limit | Abstract is approximately 163 words. LNCS recommends ≤ 150 words. Not a desk-reject but a formatting deviation reviewers may notice. | SHOULD |
| C10 | LNCS | Keywords | ✅ Pass | 5 keywords present after abstract. Within 4–6 range. | — |
| C11 | LNCS | Section numbering | ⚠️ Check | Acknowledgements and Data Availability are `\section*{}` (unnumbered) — correct per LNCS. All other sections numbered 1–7. No gaps observed. | — |
| C12 | LNCS | References style | ✅ Pass | `\bibliographystyle{splncs04}` — correct LNCS numeric style. | — |
| C13 | LNCS | Table captions and references | ✅ Pass | All 4 tables have captions. All 4 are referenced in text: `tab:accuracy` (Results opener + §4.1), `tab:per_class` (§4.3 + §4.4), `tab:mm_errors` (§4.5 + §5.1), `tab:confidence` (§4.6 + §5.2 via `sec:confidence` label). | — |
| C14 | LNCS | Data Availability placement | ✅ Pass | Immediately after `\section{Conclusion}`, before `\bibliographystyle`. | — |
| C15 | LNCS | Acknowledgements placement | ✅ Pass | After Data Availability. | — |
| C16 | Consistency | RQ–result alignment | ⚠️ Partial | RQ1, RQ2, RQ3 are stated inline in the Introduction ("addressing: RQ1... RQ2... RQ3"). Results section has subsections for §4.1 (RQ1), §4.2 (RQ2 — inline prose, no subsection header), §4.4 (RQ3). The RQ2 result subsection header was removed in a prior revision; the section now just says "Impact of Evidence Types" without explicitly saying it answers RQ2. Minor inconsistency — reviewer may note that RQ2 has no dedicated answer label. | SHOULD |
| C17 | Consistency | Number consistency | ✅ Pass | "57 repositories" consistent across Abstract, Dataset, Results, Threats, Conclusion. "70.2%" consistent across Abstract, Results, Discussion, Conclusion. "57.9%" (baseline) stated once in Results opener — not repeated elsewhere, which is correct. | — |
| C18 | Consistency | Model names | ⚠️ Inconsistent | Models listed in §3.5 as "Qwen3-coder-next, DeepSeek-v3.2, Gemini-3-Flash-Preview, Gemma4-31B, MiniMax-M2.7 (all cloud variants)." Tables use abbreviated names: "Qwen3", "MiniMax", "Gemma4", "DeepSeek", "Gemini". Abstract uses "Qwen3-coder-next, DeepSeek-v3.2…" (full names). The abbreviations in tables are appropriate but should be introduced once (e.g., "hereafter Qwen3" in §3.5). | SHOULD |
| C19 | Consistency | Terminology | ✅ Pass | "Architectural style" used consistently throughout. No mixing with "architecture pattern" or "architecture type." | — |
| C20 | Consistency | Prompt labels | ✅ Pass | P1, P2, P3, P4 used consistently in §3.4, Tables 1, and §4.2. | — |
| C21 | Bibliography | All citations resolve | ✅ Pass | pdflatex final pass produced no undefined citation warnings after bibtex run. | — |
| C22 | Bibliography | Model version IDs | ❌ Missing | Model names are given without reproducible version identifiers (e.g., no Ollama model hash or API snapshot date). "Qwen3-coder-next:cloud" is an Ollama model tag, not a pinned version. This is a reproducibility issue flagged also by se-researcher. | MUST |
| C23 | Scope | Title matches content | ✅ Pass | "LLM-Based Architecture Detection in Practice: An Empirical Multi-Model Evaluation" — signals detection, not the full pipeline. | — |
| C24 | Scope | No scope creep | ✅ Pass | Tactic selection / implementation mentioned only in Conclusion ("under active investigation"). | — |
| C25 | Scope | Abstract matches paper | ✅ Pass | Both failure modes stated in Abstract (MM/layered confusion, confidence miscalibration) are substantiated with full sections in Results and Discussion. Code signature degradation stated in Abstract is supported in §4.2. | — |
| C26 | LNCS | `\textit` bug | ✅ Fixed | Background §2, line containing "coarse-grained style classification" — `\textit` now correctly rendered. Confirmed fixed. | — |
| C27 | Policy | Author email format | ⚠️ Check | `\email{\{s.chertkov, a.sadovykh\}@innopolis.university}` — combined email syntax. LNCS standard allows this but some publisher tools prefer separate `\email{}` per author. Not a review risk but worth checking in camera-ready. | NICE |

---

## Summary of blocking / high-priority items

| Priority | Count | Items |
|---|---|---|
| MUST | 1 | C22 (model version identifiers) |
| SHOULD | 4 | C9 (abstract ~13 words over), C16 (RQ2 subsection label), C18 (table abbreviations not introduced), plus cross-reference to se-researcher S3 (context-window handling) |
| NICE | 1 | C27 (email format) |

---

_No desk-rejection risks identified. One MUST item (C22) should be addressed or explicitly acknowledged as a limitation in Threats._
