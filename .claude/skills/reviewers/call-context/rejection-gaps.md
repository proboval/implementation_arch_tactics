# EASE 2026 Rejection Gaps — v2 Coverage Status

## Source paper

**Submission 385** — "Improving Software Maintainability Through LLM-Implemented Architectural Tactics: Early Empirical Evidence"  
Rejected at EASE 2026 Short Papers and Emerging Results track (29% acceptance rate).

## v2 strategy

The v2 paper is scoped to **Architecture Detection only**, submitted to the ECSA 2026 Industry Track as a short paper. Gaps related to Tactic Selection and Implementation (R3-GAP-1) are resolved by descoping. Gaps about the detection methodology (R2-GAP-1, 2) must be checked carefully.

---

## Gap inventory

### From Reviewer 2 (Soundness / Methodology)

| Gap ID | Description | v2 Status | What to check |
|---|---|---|---|
| PREV-R2-GAP-1 | Architecture classification not validated against ground truth — only "self-reported confidence" used as accuracy proxy | **Partially fixed** — v2 paper uses 57 manually labeled repositories as ground truth | Confirm ground truth labeling process is described: who labeled, how many annotators, inter-rater agreement? |
| PREV-R2-GAP-2 | Repository sizes not reported despite context-window size being identified as a constraint | **Open** | Does paper report median/range of file count, LOC, or file tree depth per repo? |
| PREV-R2-GAP-3 | No description of how architectural tactics manifest as concrete Python code changes | **Fixed by descoping** — v2 covers detection only, no code changes | Confirm paper does not claim to cover tactic implementation |
| PREV-R2-GAP-4 | Semantic correctness and behaviour preservation not addressed after transformation | **Fixed by descoping** — no transformations in v2 | Same as R2-GAP-3 |

### From Reviewer 3 (Scope / Focus)

| Gap ID | Description | v2 Status | What to check |
|---|---|---|---|
| PREV-R3-GAP-1 | Paper tries to do too much: Architecture Detection + Tactic Selection + Implementation each deserve a full paper | **Fixed by descoping** — v2 is detection-only | Confirm paper has a single, clearly stated contribution; no scope creep into selection or implementation beyond a forward-looking sentence in Conclusion |

### From Reviewer 1 (Presentation — minor)

| Gap ID | Description | v2 Status | What to check |
|---|---|---|---|
| PREV-R1-GAP-1 | Proposed pipeline approach not clearly separated from study methodology | **Should be fixed** — v2 is a focused experience report with clearer structure | Check whether Section 3 (Methodology) cleanly distinguishes the pipeline/tool from the evaluation protocol |

---

## New risks introduced by v2 framing

These are not rejections gaps from v1 but are risks specific to the ECSA industry track reframing:

| Risk ID | Description | What to check |
|---|---|---|
| NEW-RISK-1 | Paper reads like a pure academic paper, not an industry experience report | Does the Introduction frame an industrial problem? Does Discussion contain practitioner guidance? |
| NEW-RISK-2 | "Potential for discussion" criterion not addressed | Does the paper surface open questions, surprises, or counterintuitive findings that practitioners and researchers would want to debate? |
| NEW-RISK-3 | ECSA mandatory policies violated | Is Acknowledgements section present with GAIDeT AI tool disclosure? Is Data Availability section present immediately after Conclusions? |
| NEW-RISK-4 | 70.2% accuracy not contextualized for industrial use | Is there a clear statement of what this accuracy means in practice — when is it useful and when is it not? |
