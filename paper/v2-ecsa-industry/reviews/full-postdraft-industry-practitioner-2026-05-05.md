# Review: Industry Practitioner
**Reviewer profile:** Industry Practitioner (Principal Software Architect, 12 years, Python/Java backends, two architecture migrations)
**Target:** paper/v2-ecsa-industry/main.tex — full paper
**Date:** 2026-05-05
**Mode:** post-draft
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Industrial problem framing | ✅ Present | Abstract opens with the portfolio-assessment problem. Introduction connects to migration, tech debt, tooling. Addresses NEW-RISK-1. | — |
| S2 | Explicit triage framing | ⚠️ Partial | "Triage at repository-portfolio scale" appears in Conclusion. Practitioner Guidance §5.3 point (3) ends with "route MM/layered cases to human review" but does not explicitly say "this tool is for candidate flagging, not final architectural decisions." An architect reading quickly might miss the appropriate use boundary. | SHOULD |
| S3 | False positive / negative cost asymmetry | ❌ Missing | In architecture migration, the cost of wrong classification is asymmetric: calling a modular monolith "layered" leads to applying wrong tactics. Calling it "script-based" is a different kind of mistake. The paper treats all errors as equal. A sentence in §5.1 or §5.3 noting the practical cost of MM→layered misclassification vs. the other direction would add real practitioner value. | SHOULD |
| S4 | Pipeline setup cost | ✅ Present | "Lightweight, scriptable pipeline... no GPU or fine-tuning required" in abstract and Conclusion. P2 is "pure AST parsing — lightweight, scriptable, no LLM calls required" in §4.2. Good. | — |
| S5 | When to use vs. when not to use | ⚠️ Partial | "P2 as the correct default" is stated but the threshold for when this approach is worth deploying vs. manual review is not given. For a 10-repo project, manual review is faster. For 100+, the pipeline pays off. A sentence stating the scale at which it becomes worth deploying would make §5.3 more actionable. | NICE |
| S6 | Scope discipline | ✅ Present | Paper stays focused on detection. Pipeline mention only in Conclusion as future work. | — |
| S7 | AI disclosure | ✅ Present | GAIDeT-style, tools named, roles described. | — |
| S8 | Data Availability | ✅ Present | Replication package link present after Conclusions. | — |

---

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Abstract readability for practitioners | ✅ Strong | Opens with the problem, leads with failure modes as the primary takeaway. A practitioner will read this and immediately understand what they will learn. Significant improvement over standard academic abstract. | — |
| P2 | Confidence calibration finding — practical framing | ✅ Strong | "A high-confidence prediction is no more likely to be correct than a low-confidence one" is exactly the right language for a practitioner. The Gemini inversion (highest confidence, lowest accuracy) is memorable and discussion-worthy. | — |
| P3 | MM/layered discussion — practitioner relevance | ⚠️ Weak | §5.1 explains *why* the confusion happens (naming semantics vs. import topology) but does not tell practitioners *what to do about it*. The guidance in §5.3 says "treat MM vs. layered with caution" but does not explain what "caution" means in practice: check module names manually? Use the two-class collapse as the default? Require a second human review for any MM/layered prediction? | SHOULD |
| P4 | Practitioner Guidance section | ⚠️ Weak | Compressed to 3 points in the latest revision. Point (1) is good. Point (2) on confidence is strong. Point (3) is doing too much work: it combines "treat MM/layered with caution" + "consider two-class collapse" + "route to human review" in one sentence. These are separate decisions with different implications. For a practitioner reading this before a project, each deserves a sentence. | SHOULD |
| P5 | Potential for discussion | ✅ Strong | Three strong hooks: (1) import graphs > code signatures — counterintuitive, practitioners expect more data = better; (2) confidence inversion — Gemini is confidently wrong; (3) MM/layered confusion reflects real architectural ambiguity that human architects also struggle with. This paper would generate a good 30-minute session. | — |
| P6 | Honesty about limitations | ✅ Strong | "Closing the gap toward 85%+ accuracy will require..." in Conclusion is honest and specific. 57.9% baseline stated upfront. | — |
| P7 | Connection to broader pipeline | ✅ Present | Last sentence of Conclusion positions this in a broader pipeline. Industry audience understands this is step one. | — |
| P8 | "Python only" justification | ✅ Present | "Python was chosen for its dominant role in open-source backend development and consistent AST toolchain" — adequate for industry track. | — |

---

## EASE 2026 rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth | ✅ Fixed | Ground truth used; single-annotator limitation honestly disclosed. |
| PREV-R2-GAP-2 | No repo size info | ✅ Fixed | Size range and medians in Dataset. |
| PREV-R2-GAP-3 | Tactics not described | ✅ Fixed by descoping | — |
| PREV-R2-GAP-4 | Behaviour preservation | ✅ Fixed by descoping | — |
| PREV-R3-GAP-1 | Scope too broad | ✅ Fixed | Detection only. |
| PREV-R1-GAP-1 | Pipeline/evaluation separation | ✅ Fixed | Clear structure. |

---

## New risks (ECSA industry-track framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Academic framing, not industry experience | ✅ Addressed | Practitioner framing throughout. |
| NEW-RISK-2 | Potential for discussion | ✅ Addressed | Three strong hooks present. |
| NEW-RISK-3 | ECSA mandatory policies | ✅ Addressed | AI disclosure and Data Availability present. |
| NEW-RISK-4 | Accuracy not contextualized | ✅ Addressed | Baseline stated; triage framing in Conclusion. Partially present in Practitioner Guidance. |

---

## Decisions required

1. **MM/layered guidance more specific (SHOULD):** §5.3 point (3) currently says "treat all MM vs. layered predictions as uncertain" and "consider collapsing to two-class when distinction not required." Split into: (a) what to do when you need the distinction (mandatory human review); (b) what to do when you don't (use two-class collapse). One sentence each.

2. **Error cost asymmetry (SHOULD):** Add one sentence in §5.1 or §5.3 noting which misclassification direction is more costly in practice for downstream tactic selection — MM→layered is more harmful than script→MM because tactic mismatch will be invisible at the code level.

3. **Scale threshold (NICE):** Add one sentence in §5.3 or Conclusion framing when the pipeline pays off vs. manual review. "At 20+ repositories, automated first-pass triage reduces expert review effort by..." (or a qualitative equivalent).

---

_Priority definitions: MUST = practitioners will misuse this. SHOULD = weakens practical credibility. NICE = extra practitioner value. DEFER = follow-up study._
