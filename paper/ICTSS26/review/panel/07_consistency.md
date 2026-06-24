# Reviewer Review (post-draft mode)

**Reviewer profile:** consistency-checker (QA pass, not an evaluator)
**Persona:** Consistency Checker
**Target:** ICTSS 2026 conference paper — `paper/ICTSS26/main.tex` (+ `ref.bib`)
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** ICTSS 2026, Springer LNCS one-column, full paper ≤15 pp + ≤2 ref pages, double-blind

---

## Summary judgment

The paper is in good mechanical shape after the acmart→LNCS conversion: all `\cite` keys resolve, all `\ref`/`\label` pairs resolve (no dangling/broken references), and the headline numeric chain reconciles cleanly across abstract, intro, results tables, and conclusion (56 = 42 completed + 14 failed; 42 = 18 + 17 + 7; stable 17 = 3 syntax + 7 planner + 7 no-op; all derived percentages round correctly; all four data tables' row totals sum to their stated N). The behavioral-gating figures (20 repos / 121 steps / 15 with tests / 21 passing / 0 regressions) are internally consistent. **However, one numeric result is almost certainly an edit-induced copy error (the identical Wilcoxon $W = 473$ reported for both the 42-pair and the 56-pair test), one `\label` collision conflates two distinct cross-references, and the double-blind anonymization is not yet applied — multiple hard identity leaks remain.** Overall: **PASS-WITH-FIXES.**

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | LNCS front matter (`\title`, `\author`, `\institute`, `\maketitle`, `\abstract`, `\keywords`) | ✅ Present | Title/abstract/keywords correctly placed for `llncs`. | — |
| S2 | `\begin{credits}` with `\ackname` + Disclosure of Interests | ✅ Present | Required Springer elements present (§Conclusion). | — |
| S3 | Data Availability statement | ✅ Present | Present, but the Zenodo URL carries a private access token (see P-leaks). | MUST |
| S4 | Section roadmap (intro) vs actual sections | ✅ Consistent | Intro promises §2 background, §3 methodology, §4 implementation, §5 results, §6 threats, §7 conclusion — matches the seven `\section`s exactly. | — |
| S5 | All floats captioned and referenced | ✅ Present | Fig. `pipeline_arch` + 6 tables, each captioned and each `\ref`'d at least once in text. No orphan floats. | — |
| S6 | Page budget (≤15 pp + ≤2 ref) | ⚠️ Unverified | Cannot confirm compiled length from `.tex`; authors must check after the 26→17 pp compaction. | SHOULD |

## Persuasive effectiveness (mechanical correctness)

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Headline count chain | ✅ Strong | 56 repos = 42 completed + 14 failed (10 clone + 4 impl); 42 = 18 improved + 17 stable + 7 worsened — reconciles in abstract, §3.3, §5.1, Table 1, §5.10, conclusion. | — |
| P2 | Stable-category breakdown | ✅ Strong | 17 = 3 syntax + 7 planner + 7 no-op in Table 1, §5.1, and §5.9 — all three agree. | — |
| P3 | Derived rates | ✅ Strong | 18/42=42.9%, 18/56=32.1%, 18/32=56.2% (56.25→56.2), 17/42=40.5%, 24/42=57.1% all round correctly. | — |
| P4 | Table internal totals | ✅ Strong | Tactics (7+18+14+3=42; impr 18; stable 17; worse 7), Architecture (7+26+9=42; impr 18; worse 7; stable 17), Size (11+9+12+10=42) all sum to N. | — |
| P5 | **Wilcoxon $W$ collision** | ❌ Error | §5.2: per-protocol test on **42** pairs reports "$W = 473$, $p = 0.023$"; the ITT test on **56** pairs reports "$W = 473$, $p = 0.087$". An identical $W$ for two different samples (adding 14 zero-diff pairs) is statistically impossible — one value is a copy/paste artifact of the compaction. | MUST |
| P6 | Architecture-detection figure | ✅ OK | 86.0% = 49/57 (85.96→86.0). Consistent line 135. | — |
| P7 | Prior-run baseline (18.2%, +0.48) | ✅ Consistent | Identical in §3.8 (line 135) and §5.1 (line 258). | — |
| P8 | Sensitivity / outlier numbers | ✅ Consistent | +1.484→+0.513 on outlier removal; webapp-color +21.98 and Paper2Rebuttal +18.14 match Table 4 max (21.98) and the case studies §5.4. | — |
| P9 | "Common pattern" tally | ⚠️ Weak | §5.4 "12 of 18 improvements extracted a new MI=100 module … and four partially relieved an MI=0 file" — 12+4=16 of 18, leaving 2 uncharacterized. Descriptive, not a hard contradiction, but reads as a loose remainder. | NICE |

## Standing critical issue coverage (QA-relevant items only)

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| QA-1 | `\label` collision | ❌ Open | Lines 132–133: `\label{sec:eval_arch_detection}` **and** `\label{sec:eval_pipeline}` are both on the single `\subsection{Prior Stages and Baseline}`. `\ref{sec:eval_arch_detection}` (line 88, meant to point at the *architecture-detection first stage*) and `\ref{sec:eval_pipeline}` (lines 96, 258, meant to point at the *initial pipeline experiment*) therefore resolve to the **same** subsection number. Two distinct cross-references collapsed by the conversion. Split or retarget. |
| QA-2 | Double-blind leaks | ❌ Open (authors plan as final step) | `\author{Saveliy Chertkov \and Andrey Sadovykh}` (l.28), `\authorrunning` (l.29), `\institute{Innopolis University…}` + emails (ll.30–31), self-citation `chertkov_2026_20051151` referenced in first person as "companion dataset" (ll.88, 135, 181), Zenodo **tokenized** link (l.435), and the acknowledgement naming "Claude (Anthropic)" + "Qwen3-Coder-34B" (l.427) all reveal identity/authorship. Anonymize before submission. |
| QA-3 | arXiv entries mis-typed | ❌ Open | `ref.bib` lines 184/301/330/414/424/434: six entries are `@inproceedings` with `booktitle = {arXiv preprint arXiv:…}`. `splncs04` will render these as conference papers with a bogus venue. Convert to `@misc`/`@article` (or `@online`) with proper `note`/`eprint`; of these, only `shokri2024ipsynth`, `piao2025refactoring`, `xu2025mantra`, `horikawa2025agentic`, `cordeiro2024llm` are actually cited. |
| QA-4 | Unused bib entries | ⚠️ Cosmetic | 24 of 44 `ref.bib` entries are uncited. With `\bibliography` they will not print, so no output impact, but the file is noisy. Trim for the camera-ready package. |
| QA-5 | Leftover `\CRITICAL` macro | ⚠️ Cosmetic | `\newcommand{\CRITICAL}` defined (l.21), used 0 times. Remove to avoid an accidental red review-annotation leaking into a future revision. |

## Terminology / consistency spot-checks (all PASS)

- Model name **Qwen3-Coder-34B** / `Qwen/Qwen3-Coder-34B-Instruct` used consistently (abstract, §3.6, §4.3, §Data Availability, acknowledgement). No "Qwen3-coder-next" drift.
- Tactic names **Decomposability / Localized Modification / Reduced Coupling** consistent between §3.5 catalog, Table 5, §5.6, §5.4 case labels, threats.
- Architecture labels **script-based / layered / modular monolith** consistent (§3.3, §4.2, Table 6).
- "32 maintainability-oriented tactics" stated in §2.1 (refined from M\'arquez 40+) and again in §4.3 — consistent; the implemented subset of 3 is explicitly scoped in §3.5.
- RQ1/RQ2/RQ3 (intro) each answered: RQ1 §5.1–5.2, RQ2 §5.3, RQ3 §5.3 — alignment present.

## Defensibility vs. publishability

- **Submittable as-is?** No — fix QA-2 (anonymization, desk-reject risk under double-blind) and P5 (the impossible identical $W$, which a methods reviewer will catch) first.
- **Mechanically sound after fixes?** Yes — the numeric backbone is otherwise clean and the float/citation/label graph is intact; QA-1/QA-3 are quick LaTeX/bib fixes.

## Decisions required

1. **Wilcoxon $W = 473$ (P5):** Recompute the ITT test on 56 pairs and report the correct $W$ — the per-protocol and ITT statistics cannot share an identical $W$.
2. **Label collision (QA-1):** Decide whether §3.8 should expose one anchor or two; split into separate labeled targets so the two distinct cross-references resolve correctly.
3. **Anonymization (QA-2):** Confirm the planned final-step anonymization will strip author/institute/emails, the tokenized Zenodo link, and neutralize the first-person self-citation `chertkov_2026_20051151`.
4. **Bib typing (QA-3):** Re-type the six arXiv `@inproceedings` entries so `splncs04` renders them as preprints, not conference papers.

---

_Priority definitions:_
- **MUST:** mechanical/numeric failure that confuses examiners or risks desk-reject — fix before submission.
- **SHOULD:** weakens completeness; fix if feasible.
- **NICE:** polish.
