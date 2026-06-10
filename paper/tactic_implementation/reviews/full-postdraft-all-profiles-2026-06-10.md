# Paper Review — post-draft, all profiles

**Target:** paper/tactic_implementation/main.tex — full paper
**Date:** 2026-06-10
**Mode:** post-draft
**Call context:** EASE 2026 (ACM sigconf)
**Note:** This paper targets EASE 2026, not ECSA 2026. The reviewers skill was calibrated for ECSA 2026 Industry Track; profiles are applied with that caveat. Formatting checks use ACM sigconf rules, not LNCS.

---

## REVIEW 1 — SE Researcher

### Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Paper structure matches roadmap | ❌ Missing | Introduction (§1) explicitly promises "Section 4 details the implementation" and "Section 7 concludes." Neither section exists. The paper jumps from Methodology (§3) directly to Results and Discussion (§4 in the LaTeX), then Threats to Validity (§5). Section 4 (Implementation) and Section 7 (Conclusion) are absent. Reviewers will flag this immediately. | MUST |
| S2 | Abstract completeness | ❌ Missing | Abstract enumerates pipeline stages as "(1) architectural tactic selection...and (3) tactic implementation" — stage (2) is unnamed and missing. The gap is visible and unexplained. | MUST |
| S3 | Statistical test | ❌ Missing | §3.1 states: "The null hypothesis is that tactic implementation does not produce a statistically significant change in the Maintainability Index." No statistical test (Wilcoxon signed-rank, paired t-test) is ever reported. The null hypothesis is declared and then silently dropped. | MUST |
| S4 | Cross-references resolve | ❌ Missing | `\ref{sec:eval_arch_detection}` (appears in §3.1, §4.1) and `\ref{sec:eval_pipeline}` (§4.1, §4.4) reference sections not defined in this document. These resolve to a larger thesis document. A standalone paper submission will have broken `??` references that expose the chapter-extraction problem. | MUST |
| S5 | Ground truth labeling protocol | ⚠️ Partial | §3.3 says labels come from "the architecture detection study" and §6 acknowledges "single annotator." No labeling criteria, κ, or protocol is described in this paper. As a standalone submission, the validation basis for the entire experiment is undefined. | SHOULD |
| S6 | Model version identifier | ⚠️ Partial | `qwen3-coder-next:cloud` is an Ollama-local identifier, not a reproducible model version. Which Qwen3-Coder model exactly? What parameter count? "Cloud" appears to be an Ollama deployment variant, not a version pin. This blocks reproducibility. | SHOULD |
| S7 | Inference configuration | ⚠️ Partial | Temperature = 0.2 and context window = 256k reported. Top-p, max tokens, and repetition penalty omitted. Acceptable for a short paper. | NICE |
| S8 | Prompt design transparency | ⚠️ Partial | §3.5 describes the LLM's inputs (file tree, import graph, metrics, validated label) and output format (structured JSON plan). No actual prompt structure or example is shown. The Zenodo artifact link is present but not described as containing prompts. | SHOULD |
| S9 | Threats to validity | ✅ Present | All four validity types covered (§6). Internal, external, construct, and conclusion validity discussed concisely and honestly. Well-written. | ✅ |
| S10 | Data Availability | ✅ Present | Zenodo link provided. Acceptable. | ✅ |

---

### Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | MI improvement mechanism is genuine vs. confounded | ⚠️ Weak | The paper itself reveals (§4.2–4.3) that 12 of 18 improvements came from extracting a new module achieving MI = 100. Adding *any* simple utility file (e.g., `config.py` with 5 constants) will raise a repository's average MI regardless of architectural merit. This is a known MI gaming pattern. The Discussion acknowledges size as a moderator but does not address whether the improvement signal is architectural or metric-arithmetic. A reviewer will ask: "Would adding any file with MI = 100 produce the same effect?" This question must be addressed. | MUST |
| P2 | Null hypothesis tested | ❌ Unconvincing | The null hypothesis is stated but never tested. Without a p-value or effect size, "42.9% improvement rate" is descriptive only. With N = 42, a paired Wilcoxon signed-rank test takes one line of Python. The omission of any significance test significantly weakens the empirical claim. | MUST |
| P3 | Behavioral correctness framing | ⚠️ Weak | §3.5 explicitly states: "The current implementation does not guarantee semantic behavior preservation." §4.4 echoes this. Yet the paper title is "Can LLMs *Implement* Architectural Tactics?" and the abstract claims the pipeline "improves software maintainability." A reader will reasonably interpret "improvement" as including correctness. The abstract must be qualified: "syntactic improvement in MI" rather than unhedged "improves software maintainability." | MUST |
| P4 | Comparison baseline | ❌ Unconvincing | No baseline is reported. What would random tactic selection produce? What would simply adding an empty `utils.py` file produce? The improvement rate is presented in isolation. Even a trivial baseline (random tactic + no implementation, measuring null change) would make 42.9% meaningful. Without it, the number has no reference point. | SHOULD |
| P5 | Supplementary metrics unused | ⚠️ Weak | §3.4 says fan-out and docstring coverage are "collected as supplementary indicators." They never appear in the results tables. The stated rationale for collecting them (that MI alone is debated per Lenarduzzi et al.) is therefore not acted upon. Either report them or remove the claim that they were collected. | SHOULD |
| P6 | Stable outcome framing | ⚠️ Weak | 40.5% stable is framed as a neutral outcome. But the pipeline ran, consumed compute, and generated code modifications in the non-planner-failure cases. Code that changed but produced ΔMI = 0 should be labeled a failed intervention, not a stable state. The current framing overstates the pipeline's effectiveness. | SHOULD |
| P7 | Comparison between experiments | ⚠️ Weak | §4.1 compares 42.9% (this study) vs. 18.2% (prior study) with the note "the datasets differ and direct comparison must be made cautiously." This is the right hedge, but it is immediately followed by attributing the difference to "validated labels." This causal claim cannot be supported given different datasets. Remove the causal interpretation or add a controlled experiment. | SHOULD |
| P8 | Related work on metric gaming | ❌ Unconvincing | The mechanism of improvement (extracting MI=100 modules) parallels known "metric gaming" patterns in automated refactoring. No prior work is cited on this. Adding a sentence acknowledging this literature would pre-empt a rejection argument. | SHOULD |

---

### EASE rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth for architecture classification | ⚠️ Partially addressed | This paper uses validated labels from the prior detection study. But in a standalone submission, the labeling process is undefined (single annotator, no κ, criteria not in this paper). Requires either a brief labeling protocol description or a citation to the detection paper if submitted as part of a larger work. |
| PREV-R2-GAP-2 | No repository size information | ✅ Fixed | Table 3 explicitly breaks results by repository size with N, median/mean ΔMI, and max ΔMI per bin. |
| PREV-R2-GAP-3 | No description of how tactics manifest in Python | ⚠️ Partially addressed | §3.4 defines the three tactics with descriptions, and §4.2 shows concrete examples. However, there are no code excerpts showing what a tactic looks like as a diff. The absence of code examples limits reproducibility. |
| PREV-R2-GAP-4 | Semantic correctness / behaviour preservation not addressed | ❌ Still present | Explicitly acknowledged as not done and deferred to future work. The paper cannot claim "implementation" of tactics without behavioral verification. The framing must be adjusted to "syntactic tactic application" rather than "implementation." |
| PREV-R3-GAP-1 | Paper tries to do too much | ✅ Fixed | This paper covers only tactic selection and implementation (Stage 2+). Architecture detection is out of scope and correctly deferred to the prior study. Scope discipline is good. |
| PREV-R1-GAP-1 | Pipeline approach not separated from study methodology | ❌ Still present | The paper contains cross-references to undefined sections (`\ref{sec:eval_arch_detection}`, `\ref{sec:eval_pipeline}`), revealing it is a thesis chapter extract. A standalone paper must either include the referenced content or remove the references. |

---

### New risks (EASE framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | MI gaming: improvement mechanism may be metric-arithmetic rather than architectural | ❌ Present | 12/18 improvements from adding MI=100 files. Must be addressed in Discussion: acknowledge the confound, compute what a "trivial extraction" baseline would produce, and clarify what makes the LLM's decomposition architecturally meaningful vs. adding any simple file. |
| NEW-RISK-2 | Behavioral correctness claim in title and abstract | ❌ Present | Title says "Implement" and abstract says "improves...maintainability." Both imply correctness. Without behavioral tests, all claims must be scoped to "syntactic/metric changes." |
| NEW-RISK-3 | Broken section references reveal thesis-chapter origin | ❌ Present | `\ref{sec:eval_arch_detection}` and `\ref{sec:eval_pipeline}` will appear as `??` in compiled PDF. Submission-blocking. |
| NEW-RISK-4 | Null hypothesis without statistical test | ❌ Present | Declared null hypothesis never tested. For EASE ("Evaluation and Assessment in Software Engineering"), this is particularly conspicuous. |

---

### Decisions required (SE Researcher)

1. **Standalone vs. companion paper:** If standalone, all `\ref{sec:eval_*}` cross-references must be replaced with inline summaries. If part of a two-paper package, clarify which sections are co-submitted.
2. **MI gaming confound:** Do you have data to compute what "adding a trivial utility file" would produce in terms of ΔMI per size bin? If yes, include as a baseline row in Table 2 or a discussion paragraph. If not, acknowledge explicitly that the observed gains are partially metric-arithmetic.
3. **Statistical test:** Run a Wilcoxon signed-rank test on the 42 paired (before, after) MI values and report W, p-value, and r. This is a one-line `scipy.stats.wilcoxon` call and removes a significant credibility gap.
4. **Missing sections:** Write Section 4 (Implementation) and Section 7 (Conclusion) as promised in the roadmap.
5. **Behavioral framing:** Either qualify all MI improvement claims with "without behavioral verification" throughout, or run test suites on a subset of improved repositories and report pass rates.

---

---

## REVIEW 2 — Industry Practitioner

### Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Industrial problem framing | ⚠️ Partial | The "Transformation Gap" in §1 is a good practitioner hook. But the Introduction quickly becomes academic (research questions, roadmap), and there is no concrete scenario. Who is doing this? An architect assessing 80 repos before a migration? A DevOps team in a CI pipeline? Without a scenario, practitioners cannot project themselves into the work. | SHOULD |
| S2 | Practitioner guidance subsection | ❌ Missing | There is no "Practitioner Guidance" or "Implications for Practice" subsection. The Discussion (§4.7) contains useful analysis but reads as academic interpretation, not actionable guidance. No clear takeaway for a team considering this tool. | MUST |
| S3 | Accuracy baseline contextualization | ❌ Missing | 42.9% improvement rate, 25% failure rate, 40.5% stable — but with no baseline (random tactic? expert selection? trivial file extraction?), these numbers cannot be judged. A practitioner needs: "compared to what?" | MUST |
| S4 | Conclusion section | ❌ Missing | No Section 7 Conclusion as promised in the roadmap. The paper ends on Threats to Validity. No practitioner takeaway. | MUST |
| S5 | Behavioral verification as deployment boundary | ⚠️ Partial | §3.5 and §4.4 acknowledge no behavioral verification. But this is stated as a limitation, not as a deployment boundary. A practitioner needs: "do not use this in production without test suite validation." State it directly. | SHOULD |

---

### Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | End-to-end success rate | ⚠️ Weak | The paper reports "42.9% improvement rate" but this is of-completed only. End-to-end: 18 improved out of 56 attempted = 32.1%. Additionally, of the 42 completed: 40.5% stable (no benefit) + 16.7% worsened = 57.2% non-beneficial. On 100 repos, a practitioner can expect useful output on ~32. This honest framing belongs in the paper. | MUST |
| P2 | Are the "improvements" real improvements? | ⚠️ Weak | The primary mechanism (§4.2–4.3) is extracting a simple utility file that gets MI = 100. A `config.py` with 5 constants is not an architectural tactic — it is housekeeping. The paper needs to defend why the LLM's decomposition choices are architecturally meaningful, not just metric-arithmetic. | MUST |
| P3 | Potential for discussion | ✅ Strong | The validated-label vs. auto-detected-label comparison (42.9% vs. 18.2%) is a genuinely interesting practitioner finding: "know your architecture before applying tactics." The failure taxonomy (clone failure, planner failure, stuck loops) is honest and industry-relevant. The size effect is useful. These are real discussion hooks. | ✅ |
| P4 | Failure modes described honestly | ✅ Strong | §4.6 (Pipeline Failure Analysis) is one of the best parts of the paper. Rate limiting, stuck loops, parse failures — this is the kind of honest industrial experience that EASE values. | ✅ |
| P5 | When NOT to use this tool | ❌ Missing | §4.3 shows median ΔMI = 0.00 for large repos (>80 files). The clear practitioner takeaway — "do not run this on your 200-file Django monolith expecting visible improvement" — is never stated directly. It is the single most actionable finding in the paper. | MUST |
| P6 | Setup and operational cost | ❌ Missing | No mention of compute cost, runtime per repository, or tooling requirements. GPU required? Ollama API cloud subscription? These are table-stakes questions for a practitioner considering adoption. | SHOULD |

---

### EASE rejection gap coverage

| Gap ID | Gap description | Status in this draft | Remaining action |
|---|---|---|---|
| PREV-R2-GAP-1 | No ground truth | ⚠️ Partial | Uses validated labels but labeling process not in this paper. For a practitioner: "who checked the architecture labels were correct?" One person is not reassuring. |
| PREV-R2-GAP-2 | No repo size info | ✅ Fixed | Table 3 is clear and useful. |
| PREV-R2-GAP-3 | Tactics in Python | ⚠️ Partial | The case studies (§4.2) are concrete and readable. But there are no code snippets (before/after diff). One 10-line diff would be worth more than all the MI tables to a practitioner audience. |
| PREV-R2-GAP-4 | Semantic correctness | ❌ Still present | Not verified. Must be stated as a hard deployment boundary, not just a limitation. |
| PREV-R3-GAP-1 | Too much scope | ✅ Fixed | Good scope discipline. |
| PREV-R1-GAP-1 | Pipeline vs. study methodology | ❌ Still present | Broken cross-references reveal thesis-chapter origin. Submission-blocking. |

---

### New risks (Industry Practitioner framing)

| Risk ID | Risk description | Status | Remaining action |
|---|---|---|---|
| NEW-RISK-1 | Metric gaming framing | ❌ Present | 67% of improvements (12/18) are from adding MI=100 files. Without a trivial baseline, practitioners cannot judge whether the LLM is doing architecture work or just shuffling code into simpler files. |
| NEW-RISK-2 | Potential for discussion | ✅ Addressed | Multiple strong discussion hooks present. |
| NEW-RISK-3 | AI/tool disclosure | ❌ Present | `\begin{acks}` is commented out. ACM EASE likely requires this. |
| NEW-RISK-4 | Results not contextualized for industrial use | ❌ Present | No baseline, no "when to use / when not to use" framing, no deployment boundary statement. |

---

### Decisions required (Industry Practitioner)

1. **Practitioner guidance section:** Write a short §4.8 or §5 "Implications for Practice" with at minimum: (a) use this for tiny/small repos with monolithic files, not for medium/large; (b) always run test suites after; (c) treat stable and worsened outputs as pipeline failures; (d) end-to-end success rate is 32.1%, not 42.9%.
2. **Honest success rate framing:** Report 18/56 = 32.1% end-to-end alongside the 42.9% of-completed figure and explain the difference.
3. **One code diff:** Add one before/after code snippet showing what "Decomposability" looks like concretely. Highest-ROI addition for a practitioner audience.

---

---

## REVIEW 3 — Consistency Checker

| # | Category | Finding | Priority |
|---|----------|---------|---------|
| C1 | ACM policy — AI disclosure | `\begin{acks}` block is commented out. ACM EASE 2026 requires Acknowledgements with AI tool disclosure (tool names, roles). | DESK-REJECT risk |
| C2 | Document class | `\documentclass[sigconf,review,anonymous]{acmart}` — the `anonymous` flag suppresses author names. Authors are named in the source. Confirm whether EASE 2026 uses double-blind submission; if so, author block should be suppressed for submission but present for camera-ready. Flag for attention. | MUST |
| C3 | Missing sections | Introduction roadmap promises: Section 4 (Implementation), Section 5 (Results), Section 6 (Threats), Section 7 (Conclusion). Actual sections: §3 Methodology → §4 Results and Discussion → §5 Threats to Validity → (ends). Sections 4 (Implementation) and 7 (Conclusion) are absent. Section numbers in roadmap do not match actual sections. | MUST |
| C4 | Abstract stage numbering | Abstract: "(1) architectural tactic selection...and (3) tactic implementation" — stage (2) is unnamed. | MUST |
| C5 | Undefined cross-references | `\ref{sec:eval_arch_detection}` appears in §3.1 and §4.1. `\ref{sec:eval_pipeline}` appears in §4.1 and §4.4. Neither label is defined in this document. These will render as `??` in the compiled PDF. | MUST |
| C6 | Number inconsistency in §4.6 | §3.3: "14 (25.0%) were lost during cloning." §4.6: "The 14 failed cases divide into two categories. Ten repositories failed during the cloning stage...Five repositories...had a completed before-analysis but could not produce after-analysis measurements." 10 + 5 = 15 ≠ 14. | MUST |
| C7 | Statistical claim without test | §3.1 states the null hypothesis explicitly. No statistical test result is reported anywhere. | MUST |
| C8 | Model identifier | `qwen3-coder-next:cloud` used throughout — Ollama-local identifier, not a reproducible model version. Should reference a specific Qwen3-Coder release tag or Huggingface model ID. | SHOULD |
| C9 | RQ1 coverage weak | RQ1: "reliably identify architectural patterns and align them with appropriate tactics" — alignment quality (was the chosen tactic appropriate?) is not formally evaluated. RQ2 and RQ3 are answered. RQ1 coverage is incomplete. | SHOULD |
| C10 | Table column layout | Table 4: column "Impr. / Worse. / Stable" carries three values in one cell. Difficult to read and to reference. Prefer three separate numeric columns. | NICE |
| C11 | Page limit | Verify EASE 2026 page limit. EASE short papers are typically 4–6 pages ACM format; this paper appears to run 7–8 pages. Confirm submission category. | SHOULD |
| C12 | Tables cross-referenced | All tables (1–4) cited in text. ✅ | — |
| C13 | Data Availability | Present with Zenodo link, placed after Threats to Validity. ✅ | — |
| C14 | Number consistency (repo counts) | 57 → 56 → 42 transitions all explained in §3.3. Consistent. ✅ | — |
| C15 | Terminology | "Architectural tactics" / "architectural style" / "architecture label" used consistently. ✅ | — |
| C16 | References style | `\bibliographystyle{ACM-Reference-Format}` — correct for ACM sigconf. ✅ | — |

---

## Cross-review MUST priority consolidation

All items requiring a decision or fix before submission:

| # | Item | Blocking reason |
|---|---|---|
| M1 | Write Section 4 (Implementation) and Section 7 (Conclusion) | Roadmap in §1 is broken; section numbers in roadmap do not match actual sections |
| M2 | Fix abstract: name the missing stage (2) | Visible numbering error in abstract |
| M3 | Fix all `\ref{sec:eval_arch_detection}` and `\ref{sec:eval_pipeline}` | These render as `??` — will cause desk scrutiny |
| M4 | Fix 10 + 5 ≠ 14 inconsistency in §4.6 | Numerical inconsistency in failure analysis |
| M5 | Run Wilcoxon signed-rank test on 42 paired MI values; report W, p, r | Null hypothesis declared but never tested |
| M6 | Uncomment and complete `\begin{acks}` with AI tool disclosure | ACM EASE policy compliance |
| M7 | Address MI gaming confound | 12/18 improvements = adding MI=100 files; add trivial baseline or reframe contribution as "metric-measurable changes without behavioral guarantee" |
| M8 | Qualify behavioral correctness claims in title and abstract | "implement" and "improves maintainability" imply correctness that the paper explicitly disclaims |
| M9 | Add Practitioner Guidance subsection | No actionable guidance; key for EASE audience |
| M10 | Report end-to-end success rate (18/56 = 32.1%) alongside 42.9% | The of-completed figure alone is misleading |

_Priority definitions:_
- **MUST:** Blocking — likely to cause rejection or score below acceptance threshold. Fix before submission.
- **SHOULD:** Significant — weakens the paper's credibility or practitioner value. Fix if time permits.
- **NICE:** Minor — polish item. Fix only after all MUST/SHOULD resolved.
- **DEFER:** Not required for this scope, or needs information not currently available.
