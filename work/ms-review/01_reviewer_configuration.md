# Phase 0: Reviewer Configuration Card

**Target:** `diploma/v3` (current `.tex` sources, read 2026-06-17 — substantially revised beyond the original `diploma/v3/review/` baseline)
**Date:** 2026-06-17
**Review focus (per author request):** technical questions, reproducibility, choice of projects to analyse, methodology.

## Thesis Profile

| Dimension | Assessment |
|---|---|
| **Title** | Automated Implementation of Architectural Tactics for Software Quality Improvement |
| **Institution / Year** | Innopolis University, 2026 |
| **Primary Discipline** | Software Engineering |
| **Secondary Discipline** | AI for SE / Empirical SE |
| **Research Paradigm** | Quantitative empirical — 3 sequential studies + architectural analysis |
| **Methodology Type** | Pipeline experiment + comparative LLM evaluation + statistical hypothesis testing |
| **Maturity** | Strong, honest MS draft; revision has closed framing/statistics gaps. Two experiments (baseline, second annotator) still outstanding for publication. |
| **Defensibility target** | Innopolis MS defense committee |
| **Publishability target** | EMSE / JSS / ICSE-NIER (after the two outstanding experiments) |

## Review Team

| # | Reviewer | Persona archetype & focus |
|---|---|---|
| **EIC** | Editor / committee chair | Significance, coherence, defense readiness, claim–evidence alignment, decision authority. |
| **R1 (Methodology)** | Empirical-SE methods professor | Research design, statistics, validity threats, **reproducibility**. *(primary focus)* |
| **R2 (Domain)** | Software-architecture specialist | Tactic/architecture theory, **the code-level vs. architecture-level gap**, literature. |
| **R3 (Perspective)** | SE-measurement & industry relevance | Construct/measurement validity, MI semantics, practical impact, cost. |
| **Devil's Advocate** | Rigorous critical empiricist | Strongest counter-argument, confounds, **harness-induced artifacts**, alternatives. |
| **Consistency Checker** | QA pass (non-evaluator) | Innopolis template, numeric/internal consistency, **method↔results promises**, citations. |

## Standing critical issues carried into this review (status reflects the *current* revised draft)

| ID | Issue | Status now | Evidence |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability (construct validity) | ⚠️ **Largely addressed, residual** | Reframed to "code-level … guided by architectural context" (§5.6.4, §6); webapp-color vs Paper2Rebuttal analysis (Table, §5.6). **But** title + Ch.3 still say "architectural tactics" / "architecture-aware"; promised architecture-level metrics not reported (see R1-T4). |
| CRIT-2 | File-splitting confound; no non-architectural baseline | ❌ **Open** | Acknowledged in §5.10.3 and §6 Limitations/Future Work; no baseline run. |
| CRIT-3 | Single-annotator ground truth; no inter-rater reliability | ❌ **Open** | Acknowledged §5.9.1, §6; Cohen's κ not measured. |
| CRIT-4 | No baseline comparison condition | ❌ **Open** | Same as CRIT-2. |
| CRIT-5 | Overgeneralization from niche script repos | ✅ **Addressed** | Scoped explicitly to script-based sweet spot; all results framed as preliminary (§5.13, §6). |

## Scope of this review
Full panel. Chapters read in full: abstract, ch.1–6, appendix, plus `ref.bib` (33 entries). Focus weighting on Ch.3 (Methodology), Ch.4 (Implementation), Ch.5 (Evaluation), and the dataset/selection passages, per the author's request.

## Headline
The revision is a marked improvement: the central construct-validity problem has been confronted head-on and the statistics are now honest (sensitivity analysis, CIs, multiple-comparison bounding). The thesis is **defensible**. The remaining issues the panel raises are concentrated exactly where the author asked us to look — **reproducibility artifacts (prompts, model pinning, dataset manifests), project-selection bias, and two methodological gaps (no baseline; a method↔results mismatch on architecture-level metrics)**.
