# Review Output Template (post-draft mode)

**Reviewer profile:** Industry Practitioner  
**Target:** paper/v3-ecsa-industry/main.tex (full paper)  
**Date:** 2026-05-06  
**Mode:** post-draft  
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Structural completeness

Does the paper contain everything the ECSA Industry Track requires?

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Industrial problem framing | ⚠️ Partial | Introduction opens with a real scenario: "Large organizations routinely need to assess... dozens or hundreds of repositories for technical debt assessment, migration planning, or tooling configuration." This is plausible and resonant. However, it never becomes concrete — there is no example scale (e.g., "when we were assessing 80 repositories for a migration project"), no cost estimate of manual classification, and no bridge from the abstract "organization" to what an architect actually does next after running this tool. | SHOULD |
| S2 | Practitioner guidance (specific, scoped) | ✅ Present | §5.3 gives three concrete, justified recommendations: use P2, discard confidence scores, treat MM/layered as unreliable and route to human review. This is the best section in the paper from a practitioner standpoint. The "collapse to two-class taxonomy" alternative is a practical suggestion many architects will act on immediately. | — |
| S3 | Potential for discussion | ✅ Strong | Three strong hooks: (1) code signatures degrade — a counterintuitive result engineers will want to debate; (2) confidence uncalibrated — directly applicable to anyone building LLM tool pipelines; (3) MM/layered boundary as fundamental taxonomy ambiguity rather than just model error — this will resonate with architects who have argued about this in real projects. | — |
| S4 | Accuracy contextualized for industrial use | ✅ Present | Majority-class baseline (57.9%) provided. +12.3 pp over baseline stated. "Sufficient for triage" used consistently. §5.3 explicitly distinguishes triage use from automated labeling. | — |
| S5 | Scope discipline | ✅ Present | Detection only. Tactic selection/implementation mentioned in one sentence in Conclusion as active work. No scope creep. | — |
| S6 | AI disclosure | ⚠️ Partial | Acknowledgements section present and names tools (GitHub Copilot, Claude Sonnet, Semantic Scholar MCP, NotebookLM) with roles. Not in formal GAIDeT category format, but substance is there. This is acceptable for most reviewers; a strict ECSA policy checker may flag the informal format. | SHOULD |
| S7 | Data Availability | ⚠️ Partial | Section present after Conclusions. URL provided. However the URL is `https://github.com/anonymous-ghub/Architecture-Detection-in-Software-Repositories` — this looks like a placeholder. In a single-blind submission (authors named), an anonymous placeholder is inconsistent. A reviewer trying to verify the artifacts cannot do so. | MUST |

---

## Persuasive effectiveness

Is what is present convincing to a principal practitioner?

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | "No GPU required" as industrial differentiator | ✅ Strong | "No GPU or fine-tuning required" is mentioned in the Abstract and reinforced in §4.1. This is the single most important industrial enabler and it is correctly emphasized. | — |
| P2 | Cost/setup transparency | ⚠️ Weak | The paper says "no GPU" and "lightweight, scriptable" but never gives a concrete time or cost estimate. How long does it take to classify 57 repositories? What is the API cost? For a practitioner deciding whether to deploy this at 500 repos, these numbers matter. Even an order-of-magnitude estimate ("approximately N minutes, $M per 100 repos") would significantly increase practical credibility. | SHOULD |
| P3 | Industrial scenario specificity | ⚠️ Weak | The problem introduction is generic ("large organizations"). An industry paper at ECSA should open with enough specificity that a practitioner can place themselves in the scenario. Consider: "An architect asked to recommend tactic improvements across 150 backend repositories before a migration project has two choices: spend 3 weeks manually reviewing codebases, or use an automated first pass that narrows the field to high-confidence candidates." This kind of framing activates practitioner engagement. | SHOULD |
| P4 | Confidence miscalibration implications | ✅ Strong | The operational implication is stated clearly: "confidence thresholds cannot be used to filter uncertain predictions." For a practitioner who might be tempted to set a confidence threshold and ship the rest automatically, this is a direct stop signal. | — |
| P5 | MM/layered confusion practical implication | ✅ Strong | "When the distinction matters downstream, route all MM/layered predictions to human review" is actionable. The "collapse to two-class taxonomy" suggestion is a practical workaround. Both demonstrate that the authors have thought through the practitioner's actual decision problem, not just the experimental result. | — |
| P6 | Discussion of random/lower baseline | ⚠️ Weak | The paper provides majority-class baseline (57.9%) but not the random three-class baseline (~33.3%). A practitioner evaluating the tool might ask: "vs. a random guess?" The 70.2% vs. 33.3% gap (+37 pp) paints a much stronger picture than 70.2% vs. 57.9% (+12 pp). Both should be stated. | NICE |
| P7 | Open questions that invite conference debate | ✅ Present | Conclusion's "Closing the gap toward 85%+: multi-annotator ground truth + hybrid LLM + static structural thresholds" is a strong open question. MM/layered confusion as a genuine taxonomic ambiguity (not just a model failure) is a second. Both will sustain a 30-minute session discussion. | — |
| P8 | The "what I would do differently" framing | ❌ Missing | ECSA industry papers gain credibility when they include a clear "if we were running this again, here is what we would change" statement. The paper has good threats and honest limitations but does not synthesize them into a direct practitioner lesson for tool builders. A single paragraph ("For practitioners deploying this today: X; for teams planning to replicate: Y") would close this gap. | NICE |

---

## EASE 2026 rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth — confidence as proxy | ✅ Fixed for practical purposes | 57 manually labeled repos, single expert annotator. Honest disclosure. Practitioner reviewers will accept this. |
| PREV-R2-GAP-2 | No repository size info | ✅ Fixed | File count and import edge ranges reported. |
| PREV-R2-GAP-3 | No tactics implementation description | ✅ Fixed by descoping | |
| PREV-R2-GAP-4 | Semantic correctness not addressed | ✅ Fixed by descoping | |
| PREV-R3-GAP-1 | Paper does too much | ✅ Fixed by descoping | Single clean contribution. |
| PREV-R1-GAP-1 | Pipeline not separated from methodology | ✅ Fixed | |

---

## New risks (ECSA industry-track framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Paper reads as academic, not industry experience report | ⚠️ Partially addressed | The Practitioner Guidance section saves this. Introduction could be more industrial in framing. Overall passes the threshold. |
| NEW-RISK-2 | "Potential for discussion" criterion not addressed | ✅ Addressed | Three strong hooks. Confidence calibration inversion (Gemini: highest confidence, lowest accuracy) is the strongest single finding for a conference audience. |
| NEW-RISK-3 | ECSA mandatory policies violated | ⚠️ Partially addressed | Acknowledgements present (informal format). Data Availability present but uses an anonymous-sounding placeholder URL that is inconsistent with single-blind submission. This is the main compliance risk. |
| NEW-RISK-4 | 70.2% accuracy not contextualized for industrial use | ✅ Addressed | Well-framed as triage-level accuracy. §5.3 gives explicit trust/no-trust guidance per class. |

---

## Decisions required

MUST-priority items that need a human decision before the next revision.

1. **Data Availability URL (S7):** The `https://github.com/anonymous-ghub/Architecture-Detection-in-Software-Repositories` URL appears to be an anonymous placeholder. Since ECSA Industry Track is single-blind (authors are named), there is no reason for an anonymous repository. Is this the real URL, or does it need to be replaced with the actual repository? If the repository is not yet public, the section should say: "The dataset, artifacts, and evaluation scripts will be made available at [URL] upon acceptance." A non-functional or placeholder URL is worse than an honest "not yet public" statement.

---

_Priority definitions:_
- **MUST:** Practitioners will misuse the paper or it will fail a desk-reject check. Fix before submission.
- **SHOULD:** Weakens practical credibility or misses industrial value. Fix if time permits before May 8.
- **NICE:** Extra practitioner value. Fix only after all MUST/SHOULD resolved.
- **DEFER:** Belongs in a follow-up study.
