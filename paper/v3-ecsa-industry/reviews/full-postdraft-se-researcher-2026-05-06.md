# Review Output Template (post-draft mode)

**Reviewer profile:** SE Researcher  
**Target:** paper/v3-ecsa-industry/main.tex (full paper)  
**Date:** 2026-05-06  
**Mode:** post-draft  
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Structural completeness

Does the paper contain everything the ECSA evaluation criteria require?

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Ground truth labeling process described | ⚠️ Partial | Dataset section states "Ground truth labels were assigned by a single expert annotator following the taxonomy." Single-annotator is disclosed, but the annotator's qualifications are not stated in §3.2 — only in Threats. This means the reader encounters a critical validity concern without the mitigation context, weakening the methodology section. | SHOULD |
| S2 | Inter-annotator reliability | ❌ Missing | No Cohen's κ or Krippendorff's α computed. Threats honestly acknowledges "inter-annotator agreement was not measured." For the MM/layered distinction — the study's central finding — this is the most consequential gap. If two annotators disagree on 20% of MM/layered cases, the confusion attributed to models may partly be a labeling artifact. | MUST |
| S3 | Repository characterization | ⚠️ Partial | File count (5–312, median 38) and import edge count (3–847, median 61) are reported — this is good and exceeds what many short papers provide. Missing: LOC, project domain distribution, project age, GitHub star distribution. No correlation of size with classification accuracy. For an 8-page short paper, the reported stats are acceptable; missing the size-accuracy correlation is a missed opportunity. | SHOULD |
| S4 | Prompt transparency | ⚠️ Partial | P1–P4 configurations described clearly. System prompt structure noted ("same identical system prompt specifying the task, taxonomy, allowed labels, and required JSON output schema"). Full prompts claimed to be in the Data Availability artifact. Temperature = 0.2 stated. This is sufficient for an industry short paper. | SHOULD |
| S5 | Model version identifiers | ⚠️ Partial | Five model names given with their Ollama API labels. Threats §6 honestly notes: "Model identifiers are Ollama API tags without pinned snapshot hashes, limiting exact reproducibility." This is the right disclosure, but it means results are not exactly reproducible. Given the public API nature, this is a real reproducibility risk. | SHOULD |
| S6 | Related work — static analysis baselines | ⚠️ Partial | Paper positions against static analysis ("lack semantic reasoning") but cites no specific static analysis architecture recovery tools (e.g., ACDC, Bunch, clustering-based approaches). This means the claim that static analysis is insufficient is asserted, not demonstrated. No traditional architecture recovery paper (pre-LLM) is compared experimentally or even discussed in specifics. | SHOULD |
| S7 | Train/test contamination risk | ⚠️ Partial | Threats notes "Prompt templates were finalized before evaluation runs, though taxonomy awareness was shared between prompt development and labeling." This partially addresses the concern. However, it is unclear whether any repositories from the evaluation set were viewed during prompt development or taxonomy definition. The disclosure is honest but the contamination risk is not fully resolved. | SHOULD |
| S8 | Threats to validity section | ✅ Present | All four validity types addressed honestly. Single-annotator risk is the most prominent and is correctly flagged as "the most significant validity threat." LLM non-determinism addressed. Class imbalance noted. This is one of the stronger threats sections I have seen in an 8-page industry paper. | — |
| S9 | Claims proportionate to evidence | ✅ Strong | "70.2% accuracy" is not overclaimed. "Sufficient for triage" is the correct framing. Majority-class baseline (57.9%) provided. "Preliminary baselines, not definitive performance claims" in Threats. No claim of generalizability beyond Python backends. | — |
| S10 | RQ-answer alignment | ✅ Present | RQ1 → §4.1, RQ2 → §4.2, RQ3 → §4.4. All answered. | — |

---

## Persuasive effectiveness

Is what is present convincing to this reviewer?

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Core accuracy finding (70.2%) | ✅ Strong | The majority-class baseline of 57.9% provides the right reference point. "+12.3 pp" over baseline is stated explicitly. The result is not overclaimed. | — |
| P2 | Evidence-type finding (P2 is optimal) | ✅ Strong | The monotone degradation from P2→P3 across all five models is compelling. "An unambiguous design choice" is defensible at this scale. | — |
| P3 | MM/layered confusion finding | ✅ Strong | Table 3 makes the pattern clear. The mechanistic explanation (structural similarity, naming-convention dependency) is well-reasoned. The training-data prior hypothesis for over-assignment to "layered" is plausible and interesting. | — |
| P4 | Confidence miscalibration finding | ✅ Strong | Table 4, with near-zero Δ across all models, is the paper's most striking finding. The Gemini inversion (highest confidence, lowest accuracy) is a memorable concrete example. | — |
| P5 | Single-annotator validity | ⚠️ Weak | The paper's core empirical claim rests on 57 manually labeled repositories. The labeling quality is asserted ("single expert annotator") but not validated. A reader who asks "how do we know the labels are correct?" will find only a threats acknowledgment, not a methodological defense. For the central finding (MM/layered confusion), this matters most: if the ground truth itself conflates MM and layered, the model's confusion is uninformative. | MUST |
| P6 | N=57 sample size adequacy | ⚠️ Weak | 57 repositories with 33/16/8 class distribution. Rankings between adjacent models differ by 1–2 predictions. The paper acknowledges this ("indicative rather than definitive"), which is appropriate. However, the paper makes model comparison claims (RQ3 results) that are difficult to substantiate at N=57, especially for the minority classes (script-based N=8). The acknowledgment in Results is the right approach, but the Discussion should reinforce this more explicitly. | SHOULD |
| P7 | Mechanistic explanation (code signatures degrade) | ✅ Strong | The explanation — signatures add high-volume low-structural-content noise — is coherent and is the kind of finding practitioners will find memorable and actionable. | — |
| P8 | Practical significance of confidence miscalibration | ✅ Strong | "Route all MM/layered cases to human review regardless of reported confidence" is a direct, justified operational recommendation. | — |

---

## EASE 2026 rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth for architecture classification — confidence used as proxy | ⚠️ Partially fixed | v3 uses 57 manually labeled repositories, which is a real ground truth. The labeling process is disclosed (single expert annotator, taxonomy-first). Inter-annotator agreement is not measured and is explicitly called out as missing in Threats. For an ECSA industry short paper, this is borderline acceptable — the honest disclosure and sound threat write-up partially offset the methodological gap. Add one sentence in §3.2 stating annotator role/qualification and that this is the primary limitation, so readers do not have to find it only in Threats. |
| PREV-R2-GAP-2 | Repository sizes not reported despite context window constraint | ✅ Fixed | File count (5–312, median 38) and import edges (3–847, median 61) reported. All 57 repositories completed within the 300-second timeout. Acceptable for 8-page short paper. |
| PREV-R2-GAP-3 | No description of how tactics manifest as Python code changes | ✅ Fixed by descoping | v3 covers detection only. No code changes described or claimed. |
| PREV-R2-GAP-4 | Semantic correctness / behaviour preservation not addressed | ✅ Fixed by descoping | Same as GAP-3. |
| PREV-R3-GAP-1 | Paper tries to do too much | ✅ Fixed by descoping | Single contribution, cleanly stated. Tactic selection/implementation is one forward-looking sentence in Conclusion. |
| PREV-R1-GAP-1 | Pipeline approach not separated from study methodology | ✅ Fixed | §3 Methodology clearly separates (a) artifact extraction pipeline from (b) evaluation protocol (models, prompts, configurations). |

---

## New risks (ECSA industry-track framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Paper reads as academic, not industry experience report | ⚠️ Partially addressed | Introduction frames an industrial problem (large organizations, migration planning, technical debt). Practitioner Guidance subsection (§5.3) provides specific, scoped recommendations. The language is somewhat academic in places. The finding about code signatures degrading accuracy has clear industrial design guidance — this reads well. |
| NEW-RISK-2 | "Potential for discussion" criterion not addressed | ✅ Addressed | Three strong hooks: (1) code signatures harm — counterintuitive, challengeable; (2) confidence miscalibration — directly applicable to LLM tool design; (3) MM/layered confusion as fundamental taxonomy ambiguity. This paper will generate practitioner discussion. |
| NEW-RISK-3 | ECSA mandatory policies violated | ⚠️ Partially addressed | Acknowledgements present with tool names and roles. Data Availability section present after Conclusions with GitHub URL. However: (a) Acknowledgements are not in explicit GAIDeT taxonomy format; (b) the Data Availability URL is `anonymous-ghub` — an anonymous placeholder in a **single-blind** paper where authors are named. This inconsistency should be resolved: either use the real repository URL or explain the placeholder. |
| NEW-RISK-4 | 70.2% accuracy not contextualized for industrial use | ✅ Addressed | "Sufficient for triage" framing used consistently. +12.3 pp over majority-class baseline stated. §5.3 gives specific guidance on which classes to trust and when to route to human review. |

---

## Decisions required

MUST-priority items that need a human decision before the next revision.

1. **Inter-annotator agreement (P5 / PREV-R2-GAP-1):** The single-annotator limitation is the study's primary validity threat, and it is most critical for the MM/layered finding. Options: (a) accept the limitation with the current threats disclosure; (b) add a brief inter-annotator sample — even 10 repos reviewed by a second annotator with κ reported would substantially strengthen this. Given the May 8 deadline, option (a) is realistic but should at minimum add the annotator's qualification to §3.2 ("a single author with N years of architecture experience"). What is the annotator profile?

2. **Data Availability URL:** The `https://github.com/anonymous-ghub/Architecture-Detection-in-Software-Repositories` URL appears to be an anonymous placeholder. ECSA is single-blind — authors are identified. Is this repository live and accessible? If not, the Data Availability section is technically unresolvable by a reviewer, which could be flagged as a policy gap.

---

_Priority definitions:_
- **MUST:** Blocking — likely to cause rejection or score below acceptance threshold. Fix before submission.
- **SHOULD:** Significant — weakens the paper's credibility. Fix if time permits before May 8.
- **NICE:** Minor polish. Fix only after all MUST/SHOULD resolved.
- **DEFER:** Not required for this scope.
