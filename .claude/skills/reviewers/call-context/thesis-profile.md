# Call Context: Thesis Profile & Standing Critical Issues

The specific facts of the thesis under review. Reviewers use this to anchor judgments in the actual claims and to track the standing critical issues across versions. Verify against the current `.tex` sources — figures below reflect thesis **v3** and may change in later versions.

## Thesis at a glance

| Dimension | Value |
|---|---|
| Title | Automated Implementation of Architectural Tactics for Software Quality Improvement |
| Institution / year | Innopolis University, 2026 |
| Primary discipline | Software Engineering |
| Secondary | AI for SE / Empirical SE |
| Paradigm | Quantitative empirical — three sequential studies |
| Methods | End-to-end pipeline experiment + comparative LLM evaluation + statistical hypothesis testing |
| Maturity | Mature MS draft; needs construct-validity fix and compaction for publication |

## Central claim

LLMs can support software maintainability improvement through **code-level tactic implementation guided by architectural context**. (Note: the abstract sometimes frames this as "architecture-aware" — the validity of that framing is the central dispute; see CRIT-1.)

## The three studies

- **Study 1 — End-to-end pipeline.** Detect architecture → select tactic from a catalog → implement via LLM code edits. Measures Maintainability Index (MI) before/after across **162** open-source Python backend repos. Result: $\overline{\Delta MI} = +0.48$, $p = 0.001$, $r = 0.28$; 13.6% of completed repos improved; 25.3% pipeline failure rate.
- **Study 2 — Architecture detection.** 5 LLMs × 4 context configurations on **57** manually labeled repos. Best: Qwen3-coder-next + file tree + import graph → **70.2%** accuracy, **0.65** macro-F1 (+12.3 pp over majority-class baseline). Import graphs help across all models; code signatures hurt; confidence scores poorly calibrated; modular-monolith/layered systematically confused.
- **Study 3 — Tactic implementation with validated labels.** Using ground-truth architecture labels raises improvement rate to **42.9%** and mean gain to **+1.484**, showing detection quality propagates downstream.

## Key reported findings

- Strongest MI gains in small, script-based repos (Decomposability extracting modules from near-MI=0 monolithic files; up to +21.98).
- Repository size is the dominant moderator; large repos dilute file-level changes.
- Implementation operates at the **code level, not the architecture level** — package count unchanged across all repos; fan-out changed in <25% of cases.
- MI does not distinguish genuine architectural restructuring from mechanical file splitting (e.g., Paper2Rebuttal vs. webapp-color).

## Standing critical issues (CRIT-*)

Every review must state the status of each: ✅ resolved / ⚠️ partially / ❌ open, with the section evidence.

| ID | Issue | Dimension | Why it matters |
|---|---|---|---|
| **CRIT-1** | MI is a code-level complexity metric and does not capture architecture-level maintainability (modularity, coupling, conformance), yet results are sometimes framed as "architecture-aware." | Construct validity | If MI ≠ the claimed construct, the central claim collapses. Resolve by adding an architecture-level metric **or** explicitly reframing the claim to code-level. |
| **CRIT-2** | The largest MI gains come from file splitting, which mechanically reduces MI inputs; no non-architectural "random file-splitting" baseline rules this out. | Internal validity | The effect may be an arithmetic artifact of averaging, not architectural improvement. |
| **CRIT-3** | All architecture labels assigned by a single annotator; no inter-rater reliability, especially for modular-monolith vs. layered. | Measurement | Unreliable ground truth undermines Study 2 accuracy and Study 3 conclusions. |
| **CRIT-4** | No comparison condition (random split, static-analysis-only, or manual developer). | External validity | Demonstrates absolute capability, not relative effectiveness. |
| **CRIT-5** | Strongest results are from a vanishingly small niche (near-MI=0 script repos) but generalized to "software maintainability" broadly. | External validity | Overgeneralization from niche to general. |

### Secondary recurring concerns

- No behavioral-preservation check (tests not executed) — MI may improve on broken code.
- Small effect size ($r = 0.28$; +0.48 on a 100-point scale) — practical significance unaddressed.
- Multiple-comparison problem across 20 model-prompt pairs; missing 95% CIs.
- API model instability (cloud LLM behind a moving tag); variance not bounded.
- Ch.4 (Implementation) disproportionately long vs. the analysis chapters — compaction needed.
- Tactic catalog lists ~20 tactics but only 4 implemented — scope or justify the exclusions.

## Editorial precedent

The v3 panel reached **MAJOR REVISION** (June 2026): CRIT-1 and CRIT-2 upheld as CRITICAL by the devil's advocate, so ACCEPT was blocked per the checkpoint rule. The required revisions were: fix MI construct validity (add architecture-level metric or reframe), add a baseline, add a second annotator + Cohen's κ, condense Ch.4 and expand analysis, add CIs and multiple-comparison awareness. Use this as the baseline when reviewing later versions: check whether each was addressed.
