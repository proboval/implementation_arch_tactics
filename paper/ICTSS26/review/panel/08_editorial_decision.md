# Editorial Decision — ICTSS 2026 submission

**Decision: MAJOR REVISION.**
Per the checkpoint rule, the devil's advocate raised CRITICAL issues that the panel **upholds**, so ACCEPT is blocked until they are resolved or the central claim is reframed.

## Cross-reviewer matrix

| Reviewer | Decision | Headline concern |
|---|---|---|
| EIC | Major (leaning positive) | Test adequacy asserted, not measured; double-blind leaks |
| Methodology | Major | No positive control + no coverage evidence for the null; stat-reporting bugs |
| Domain | Major | No test-oracle literature; "gap" not demonstrated; missing LLM-test-gen refs |
| Perspective | Major | Narrative still maintainability-led; testing payoff buried; term drift |
| Devil's advocate | (blocks ACCEPT) | "0 regressions ⇒ adequacy gap" is an uncontrolled positive-from-null inference |
| Consistency | Pass-with-fixes | Impossible duplicate Wilcoxon W; `\label` collision; arXiv entry types; anonymization |

## Arbitration — the one issue that decides the paper

**Five of six reviewers independently converge on the same CRITICAL:** the paper's headline contribution — that existing test suites are **inadequate behavioral oracles** for LLM architectural edits — is **inferred from a null result (0 regressions / 121 steps) that is never measured or controlled.** The claim is currently unfalsifiable: "the gate never fired" is equally consistent with three unseparated explanations —
1. the LLM edits were genuinely behavior-preserving (the *benign* reading — and the unchanged structural metrics in Table 7 actually support it);
2. the edits did not touch tested code paths;
3. the suites were too sparse to exercise the edits (the authors' reading).

To move to a defensible contribution the paper must **operationalize test adequacy** and **separate these explanations**. This is CRIT-4 (no comparison condition) re-surfacing in testing clothing.

The secondary consensus: the paper is **structurally still a maintainability study** (5/8 result subsections, 5/6 tables serve RQ1/MI, which the authors themselves call noise), with a **testing title/abstract bolted on**. Readability suffers because the lead is buried and terminology drifts.

CRIT status (panel consensus): **CRIT-1 ✅ (residual phrasing), CRIT-2 ⚠️, CRIT-3 ❌, CRIT-4 ❌ (now central), CRIT-5 ✅.**

## Decision letter (summary)

The reframe toward a testing contribution is the right strategic move and the paper's statistical candour (bootstrap CIs, outlier sensitivity, intention-to-treat) is commendable and rare. However, the central testing claim is not yet evidenced: it needs (a) a **positive control** proving the gate can detect a known behavior-changing edit, and (b) a **coverage/mutation measurement** of the modified code to substantiate "suites too sparse." Without these the paper observes the already-known fact that small OSS projects under-test, rather than establishing a new result about LLM architectural edits. Combined with a required restructure to lead with the testing question, two stat-reporting errors, and double-blind anonymization, this is a major revision. With (a)+(b) added and the narrative rebalanced, the paper would be a strong, venue-appropriate contribution.
