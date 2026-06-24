# Reviewer Re-Review (Round 2, post-heavy-edit)

**Reviewer profile:** consistency-checker (QA pass, not an evaluator)
**Target:** ICTSS 2026 paper — `paper/ICTSS26/main.tex` (+ `ref.bib`)
**Date:** 2026-06-23
**Mode:** re-review (round 2) after compaction 26→17pp, testing-first restructure, corrected statistics, anonymization, +4 refs
**Frame:** Springer LNCS one-column, double-blind

---

## Verdict: PASS-WITH-FIXES

Round-1 MUSTs are resolved: the impossible duplicate Wilcoxon W is gone (now W=81 on 42 pairs, single value); double-blind leaks are anonymized (author "Anonymous Author(s)", institute withheld, self-citation now `anon_archdetect_2026`, no Zenodo token); the six arXiv entries are re-typed `@misc` with proper `eprint`/`archiveprefix`/`doi`; the `\CRITICAL` macro is removed. The headline count chain and all four data-table totals reconcile cleanly. **However, a new edit-induced numeric contradiction has appeared (two different sensitivity p-values for the same outlier-removal test), Table 1's category definitions contradict the methodology's stated ±0.01 tolerance, and the round-1 `\label` collision is still physically present.**

## Numbers that reconcile (verified)

- 56 = 42 completed + 14 failed (10 clone + 4 impl) — abstract, §3.3 l.106, §5.1, §5.11 l.391, conclusion. OK.
- 42 = 18 improved + 17 stable + 7 worsened. OK. 17 stable = 3 syntax + 7 planner + 7 no-op (§5.1 l.239, §5.10 l.387, Table 1). OK.
- Rates: 18/42=42.9%, 18/56=32.1%, 18/32=56.2%, 17/42=40.5%, 7/42 & 7/42=16.7%, 3/42=7.1%, 14/56=25.0%. All round correctly.
- Tactic table (l.331–334): N 7+18+14+3=42; Impr 0+8+9+1=18; Stable 7+7+3+0=17; Worse 0+3+2+2=7. OK.
- Architecture table (l.354–356): N 7+26+9=42; Impr 3+9+6=18; Worse 0+5+2=7; Stable 4+12+1=17. OK.
- Size table (l.306–309): 11+9+12+10=42. OK.
- Behavioral gating: 28 applied / 208 steps / 20 logged / 121 steps / 15 with non-trivial suites / 0 regressions (§5.2 l.264–266). OK.
- Stats backbone: W=81, p=0.028, r̂=0.50, CI [0.29,2.98], 10k resamples (§5.3 l.272); conclusion l.422 matches W-free (p=0.028, r̂=0.50). OK.
- Arch-detection 86.0% = 49/57 (§3.8 l.136). OK. Prior-run baseline 18.2%/+0.48 consistent §3.8 l.136 & §5.1 l.259. OK.
- All 24 `\cite` keys resolve; no dangling `\ref`; arXiv entries fixed; anonymization applied.

## Concrete findings (each one line)

| # | Priority | Location | Finding |
|---|---|---|---|
| F1 | MUST | §5.13 Discussion l.400 and §6 Conclusion-validity l.414 | Sensitivity p-value contradiction: outlier-removal test is reported as **p=0.083** in §5.3 l.275 and conclusion l.422, but as **p=0.156** at l.400 and l.414 — same test, two values; the 0.156 figures are stale (corrected value is 0.083) and must be updated. |
| F2 | MUST | Table 1, l.226/227/231 | Category labels use bare `$\Delta MI > 0$` / `$= 0$` / `$< 0$`, contradicting the methodology's defined ±0.01 tolerance (l.116: improved `>0.01`, stable `|Δ|≤0.01`, worsened `<-0.01`). The table should restate the tolerance thresholds (or a footnote) so the "improved/stable" split is consistent with the stated rule that governs the 18/17/7 counts. |
| F3 | MUST | l.133–134 | `\label` collision unresolved: `\label{sec:eval_arch_detection}` and `\label{sec:eval_pipeline}` are both on the single §3.8 subsection, so `\ref{sec:eval_arch_detection}` (l.89, intended: arch-detection stage) and `\ref{sec:eval_pipeline}` (l.259, intended: initial pipeline experiment) resolve to the identical section number. Both referents do live in §3.8, so it is not a wrong-number bug, but two distinct cross-references collapse to one anchor — split or retarget. |
| F3-LaTeX | SHOULD | l.133–134 | Two `\label`s on one sectioning unit also triggers a "multiply defined / last value wins" condition under `hyperref`; mechanically fragile even though current targets coincide. |
| F4 | SHOULD | §5.3 l.275 | Sensitivity mean drop stated as "+1.48 to +0.56"; round-1 corrected value was +0.513. Confirm +0.56 is the intended re-computed figure (and that "+1.48" matches Table 2's "+1.484"); if +0.513 is correct, l.275 is stale. Internally not contradicted elsewhere, so SHOULD not MUST. |
| F5 | NICE | §5.4 l.291 | "Common pattern" remainder: 12 extracted MI=100 + 4 relieved MI=0 + "remaining two" = 18 — now fully accounted (round-1's loose remainder is fixed); only flagged as resolved. |
| F6 | NICE | §Acknowledgement l.428 | "Claude (Anthropic)" named as writing-assist tool. Standard AI-disclosure, not author identity, but under strict double-blind some chairs treat named tooling as a soft signal; consider neutral phrasing ("an LLM-based assistant") for the blind version. |
| F7 | NICE | `ref.bib` | ~24 of 48 entries uncited (e.g., garlan1995editorial, molnar2020study, visser2016maintainable, fowler2018refactoring, ge2022archtacrv, etc.); harmless with `\bibliography` but noisy — trim for camera-ready. |

## Terminology / cross-ref spot-checks (all PASS)

- Model name `Qwen3-Coder-34B` / `Qwen/Qwen3-Coder-34B-Instruct` consistent (abstract, §3.6, §4.3, Data Availability, ack). No "Qwen3-coder-next" drift.
- Tactic names Decomposability / Localized Modification / Reduced Coupling consistent (§3.5, Tables 5–6, §5.4/5.6, threats).
- Architecture labels script-based / modular monolith / layered consistent (§3.3, §4.2, Table 6).
- "32 maintainability-oriented tactics" stated §2.1 l.67 and §4.3 l.195 — consistent; implemented subset of 3 scoped in §3.5.
- Section roadmap (l.58) matches the seven actual `\section`s. RQ1/RQ2/RQ3 each answered (RQ1 §5.1/5.3; RQ2/RQ3 §5.2).
- "$\pm0.01$ tolerance treated as ties" (§5.3 l.272) consistent with methodology l.116 — only Table 1's labels (F2) drift from it.

## Bottom line

Three MUSTs remain before submission: F1 (contradictory sensitivity p-value 0.083 vs 0.156 — a methods reviewer will catch it), F2 (Table 1 category thresholds vs the stated ±0.01 tolerance), F3 (the `\label` collision). All are quick edits; the numeric backbone, citation graph, anonymization, and bib typing are otherwise sound.
