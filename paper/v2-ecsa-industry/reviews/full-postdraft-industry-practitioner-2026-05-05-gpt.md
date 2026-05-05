**Reviewer profile:** Industry practitioner
**Target:** paper/v2-ecsa-industry/main.tex
**Date:** 2026-05-05
**Mode:** post-draft
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Industrial problem framing | ✅ Present | The paper opens from a portfolio-assessment problem and stays tied to migration, technical debt, and tooling configuration. | — |
| S2 | Appropriate-use boundary | ✅ Present | The current text consistently frames the result as useful for triage, not autonomous labeling. | — |
| S3 | Practitioner guidance specificity | ✅ Present | §5.3 now gives clear guidance on the default evidence set, confidence handling, and MM/layered review policy. This was the main practical gap in earlier versions and is now fixed. | — |
| S4 | Error-cost framing | ✅ Present | The paper now states that MM→layered is the more harmful direction because it drives the wrong tactic family. That is exactly the kind of practical distinction I want. | — |
| S5 | Setup cost clarity | ✅ Present | The paper is explicit that P2 is based on AST extraction, is lightweight, and requires no GPU or fine-tuning. | — |
| S6 | Scale threshold | ⚠️ Partial | The paper says the approach is useful for portfolio-scale triage, but it still does not say when this becomes worth deploying instead of manual review. A practitioner deciding between reviewing 10 repos and 200 repos still has to infer the threshold. | NICE |
| S7 | Scope discipline | ✅ Present | Detection only. The broader pipeline is mentioned only as forward-looking work. | — |
| S8 | Reading flow / professionalism | ⚠️ Partial | There is no explicit Background section heading before the background material. Practitioners are less sensitive to formal structure than academics, but this still reads like a dropped heading in the middle of the paper. | SHOULD |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Usefulness of main result | ✅ Strong | "70.2% is good enough for triage" is a defensible and useful claim for large portfolios. | — |
| P2 | Failure-mode honesty | ✅ Strong | The paper does not hide the two reasons I would hesitate to deploy this blindly: MM/layered confusion and uncalibrated confidence. | — |
| P3 | Discussion value | ✅ Strong | The import-graph result is counterintuitive, and the MM/layered ambiguity clearly reflects a real architecture-assessment problem rather than a toy benchmark quirk. | — |
| P4 | Actionability | ✅ Strong | I can leave this paper with three operational decisions: use P2, ignore confidence, and force human review on MM/layered cases. | — |
| P5 | Enterprise realism | ⚠️ Weak | The paper does acknowledge Python/open-source limits, but it still stops short of saying that enterprise polyglot repositories may behave materially differently. This is present in Threats, though briefly. | SHOULD |
| P6 | Session potential | ✅ Strong | This would generate a solid industry-track discussion because it gives practitioners something arguable, not just a benchmark table. | — |

## EASE 2026 rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth for architecture classification | ✅ Fixed | Manual labeling now anchors the results. |
| PREV-R2-GAP-2 | No repository size info | ✅ Fixed | Repository size ranges and medians are now included. |
| PREV-R2-GAP-3 | No description of how tactics manifest in Python | ✅ Fixed | Resolved by descoping; the paper no longer pretends to cover tactic implementation. |
| PREV-R2-GAP-4 | Semantic correctness / behaviour preservation not addressed | ✅ Fixed | Resolved by descoping. |
| PREV-R3-GAP-1 | Paper tries to do too much | ✅ Fixed | The scope is now narrow enough for an industry short paper. |
| PREV-R1-GAP-1 | Pipeline approach not separated from study methodology | ✅ Fixed | The paper reads as an empirical evaluation, not a vague pipeline pitch. |

## New risks (ECSA industry-track framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Paper reads as academic, not industry experience report | ✅ Addressed | The framing and discussion are now recognizably practitioner-oriented. |
| NEW-RISK-2 | "Potential for discussion" criterion not addressed | ✅ Addressed | The two failure modes and the evidence-design result give the paper real discussion value. |
| NEW-RISK-3 | ECSA mandatory policies violated | ⚠️ Partially | Required sections exist, but Data Availability is not immediately after Conclusions because Acknowledgements comes first. | SHOULD |
| NEW-RISK-4 | 70.2% accuracy not contextualized for industrial use | ✅ Addressed | The paper now gives enough context for a practitioner to understand where the result is useful and where it is not. |

## Decisions required

1. **Fix the missing Background heading:** This is a presentation defect, not a content defect, but it makes the paper look less finished than it is.
2. **Decide whether to spend a sentence on deployment threshold:** If there is room, add one practical sentence about this being worthwhile for portfolio-scale review rather than small one-off assessments.
3. **Move Data Availability ahead of Acknowledgements if ECSA ordering is meant to be followed literally:** The content is present; this is an ordering cleanup.

---

_Priority definitions:_
- **MUST:** Practitioners will misuse this if it says X.
- **SHOULD:** Significant — weakens practical credibility.
- **NICE:** Minor — extra practitioner value.
- **DEFER:** Follow-up study.
