# Review: SE Researcher
**Reviewer profile:** SE Researcher (empirical SE, software architecture, LLM-based code analysis)
**Target:** paper/v2-ecsa-industry/main.tex — full paper
**Date:** 2026-05-05
**Mode:** post-draft
**Call context:** ECSA 2026 Industry Track — Short Papers and Presentations

---

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Ground truth labeling process described | ⚠️ Partial | Single annotator acknowledged in Threats as "most significant validity threat." Process stated (taxonomy-first labeling). No κ or inter-rater check. For a 57-repo dataset where the key finding depends on the MM/layered boundary, this is the weakest structural element. | SHOULD |
| S2 | Repository size reported | ✅ Present | "5–312 Python files, median 38; 3–847 import edges, median 61." Addresses PREV-R2-GAP-2. | — |
| S3 | Context-window handling described | ❌ Missing | At P3 (code signatures), a 312-file repo could generate very long prompts. How does the pipeline handle repos that approach or exceed the model context limit? Was any repo truncated? This is a direct reproducibility issue and was the reason R2 raised repo size in the first place. | MUST |
| S4 | Model version identifiers | ⚠️ Partial | Models named as "Qwen3-coder-next", "DeepSeek-v3.2", "Gemini-3-Flash-Preview:cloud" etc. via Ollama API. No snapshot/version hash provided. Model behavior on cloud APIs changes over time. Results are not reproducible without pinned versions. | MUST |
| S5 | Prompt design transparency | ⚠️ Partial | P1–P4 structure described. Temperature stated. Actual prompts in replication package. The paper does not state whether prompts were tuned/iterated on the evaluation set (prompt engineering contamination). This is a standard internal validity concern. | SHOULD |
| S6 | Related work: architecture recovery prior art | ⚠️ Partial | Shokri (IPSynth) and Lenarduzzi (static analysis limits) cited. No mention of earlier static-analysis-based style classification work (ACDC, Bunch, Reflexion-based recovery). Claim "To our knowledge, no prior work has systematically evaluated automated style classification" may be falsifiable. | SHOULD |
| S7 | Majority-class baseline stated | ✅ Present | "Majority-class baseline (predicting modular monolith for every repository) yields 57.9% accuracy; the best LLM configuration exceeds this by 12.3 percentage points." Good. | — |
| S8 | Threats to validity | ✅ Present | All four validity types addressed. Single annotator explicitly named as the most significant threat. LLM non-determinism mentioned. Construct validity addresses hybrid repos. | — |
| S9 | Prompt engineering / leakage statement | ❌ Missing | Were any labeled repositories used during prompt development? If the prompts were iterated on examples from the evaluation set, the 70.2% figure is optimistic. Even a one-sentence statement ("prompts were designed before labeling was finalized" or "prompts were developed on a held-out set") would close this. | SHOULD |

---

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Claims proportionate to evidence | ✅ Strong | "sufficient for triage-level automation," "preliminary baselines, not definitive claims" — well calibrated throughout. The N=57 caveat in the Results opener is exactly right. | — |
| P2 | Import graph finding credibility | ✅ Strong | Mechanistic explanation (dependency structure vs. naming hierarchy) is sound and maps cleanly to architectural theory. The fact that it holds across all 5 models strengthens the claim. | — |
| P3 | Modular monolith / layered analysis | ✅ Strong | The explanation (semantic naming property vs. structural property visible in import topology) is correct and insightful. The "prior toward layered" hypothesis is appropriately caveated. | — |
| P4 | Confidence calibration analysis | ✅ Strong | RLHF training hypothesis properly caveated as "one possible explanation." Operational implication clearly stated. | — |
| P5 | "First systematic evaluation" claim | ⚠️ Weak | The claim rests solely on Esposito's survey. If a reviewer knows of ACDC-based or clustering-based style classification work, this claim will be challenged. "To our knowledge" is the right hedge — but the Related Work should make a stronger case by explicitly distinguishing *why* prior static-analysis recovery work does not constitute "systematic evaluation" of LLM-based style classification. | SHOULD |
| P6 | Model ranking validity | ✅ Strong | "adjacent model rankings differ by one or two predictions and should be treated as indicative" — explicit and appropriate. | — |
| P7 | Python-only generalizability | ⚠️ Weak | External validity threat mentions it but the Main text says "Python backend repositories are a relevant industrial proxy" without proving it. A one-sentence acknowledgment in Dataset or Threats that the findings may not transfer to polyglot or enterprise systems would strengthen this. | NICE |
| P8 | Single-annotator credibility for the core finding | ⚠️ Weak | The MM/layered confusion is the study's most important negative finding. Its credibility depends on the ground-truth labels being correct. If the single annotator also confused some MM/layered cases, the "confusion" is partly measuring labeling uncertainty, not just model error. This is acknowledged in Threats but not addressed with even a spot-check. | SHOULD |

---

## EASE 2026 rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth for architecture classification | ✅ Fixed | 57 manually labeled repos, ground truth used throughout. Single annotator acknowledged as threat. |
| PREV-R2-GAP-2 | No repository size info | ✅ Fixed | "5–312 Python files, median 38; 3–847 import edges, median 61" in Dataset. |
| PREV-R2-GAP-3 | No description of how tactics manifest in Python | ✅ Fixed by descoping | No code changes in v2. |
| PREV-R2-GAP-4 | Semantic correctness / behaviour preservation | ✅ Fixed by descoping | No transformations in v2. |
| PREV-R3-GAP-1 | Paper tries to do too much | ✅ Fixed | Detection only. Future work one sentence at end. |
| PREV-R1-GAP-1 | Pipeline not separated from evaluation | ✅ Fixed | §3 describes the pipeline; evaluation is the paper's body. Clear separation. |

---

## New risks (ECSA industry-track framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Paper reads as academic, not industry experience | ✅ Addressed | Abstract, Introduction, and Practitioner Guidance all use practitioner framing. |
| NEW-RISK-2 | "Potential for discussion" not addressed | ✅ Addressed | MM/layered confusion, confidence calibration inversion (Gemini), and "what would it take for 85%?" are strong discussion hooks. |
| NEW-RISK-3 | ECSA mandatory policies violated | ✅ Addressed | Acknowledgements with GAIDeT disclosure present. Data Availability section present after Conclusions. Authors named. |
| NEW-RISK-4 | 70.2% accuracy not contextualized | ✅ Addressed | Majority-class baseline stated. "triage not final labeling" positioned in Conclusion and implied in Practitioner Guidance. |

---

## Decisions required

1. **Context-window handling (MUST):** How were large repositories handled at P3 and P4? Were any truncated? A one-sentence answer in §3.3 (Evidence Extraction) would close S3.

2. **Model version pinning (MUST):** Are Ollama cloud API versions pinned or snapshot-reproducible? If not, state this explicitly as a reproducibility limitation in Threats. If they are, report the version identifiers.

3. **Prompt engineering contamination (SHOULD):** Add one sentence in §3.4 or Threats stating whether prompts were developed before or after the evaluation set was finalized.

4. **Prior static-analysis recovery work (SHOULD):** Add one sentence distinguishing traditional architecture recovery (ACDC/Bunch/clustering) from LLM-based style classification to justify the "To our knowledge" claim more robustly.

---

_Priority definitions: MUST = blocking / likely rejection. SHOULD = weakens credibility. NICE = polish. DEFER = future work._
