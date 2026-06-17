# Phase 2: Editorial Synthesis & Decision

## Cross-Reviewer Matrix: Consensus vs. Disagreement

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) | DA | Verdict |
|-----------|:---:|:---:|:---:|:---:|:---:|---------|
| Three-study design coherent | + | + | + | + | ~ | **Consensus (4 agree, DA neutral)** |
| Import graph best evidence type | + | + | + | + | + | **Consensus (5 agree)** |
| Code-level > architecture-level gap | + | + | + | + | + | **Consensus (5 agree)** |
| Single annotator is a threat | + | + | + | + | + | **Consensus (5 agree)** |
| Artifact release is valuable | + | + | + | + | + | **Consensus (5 agree)** |
| MI construct validity sufficient | + | ~ | ~ | ~ | **C1** | **Major disagreement** |
| Failure rate acceptable | + | ~ | + | ~ | ~ | **Divergent** |
| Stat. methods adequate | + | **C** | ~ | ~ | ~ | **Divergent** |
| Practical recommendations bold enough | − | ~ | ~ | **C** | ~ | **Divergent** |

*(+ = strength, ~ = neutral/acknowledged, − = weakness, C = specific criticism)*

## Arbitration of Disputed Issues

**Issue: MI as the primary dependent variable (DA C1 + C2)**
- EIC, R3, and DA all express reservations about MI's scope
- DA's C1 is the deepest challenge: if MI does not measure architectural maintainability, the central claim collapses
- R2 (Domain) also notes the absence of architecture-level metrics
- **Resolution**: This is the most serious unresolved issue. The paper needs to either (a) add architecture-level metrics (cyclic dependency ratio, module cohesion) or (b) reframe the claim explicitly to code-level maintainability improvement with architectural context. The current framing is not supported by the evidence.

**Issue: Adequacy of statistical methods (R1)**
- R1 correctly notes the multiple-comparisons problem in Study 2 (20 model-prompt pairs) and the lack of confidence intervals for key effect sizes
- No reviewer disputes these points
- **Resolution**: Straightforward fix — add Bonferroni-Holm adjustment note and 95% CIs. No fundamental disagreement.

**Issue: Single annotator threat (all reviewers)**
- Unanimous concern. DA identifies it as MAJOR
- **Resolution**: Requires at minimum a second-annotator subset with agreement metrics before publication

## Devil's Advocate CRITICAL Issue Evaluation

| DA Issue | Severity | Verdict |
|----------|----------|---------|
| **C1**: MI does not measure the construct | CRITICAL | **Upheld** — the paper's central dependent variable is a code-level complexity metric, not an architecture-level maintainability metric |
| **C2**: File splitting trivially improves MI | CRITICAL | **Upheld** — no baseline comparison against non-architectural file splitting |

**⚠️ Per Checkpoint Rule #4: DA CRITICAL issues found → Decision cannot be Accept.**

---

## Editorial Decision Letter

**Date:** June 16, 2026
**Decision: MAJOR REVISION**

Dear Author,

Thank you for submitting your manuscript. The topic — using LLMs for architecture-aware maintainability improvement — is timely and relevant. The three-study design and the transparency in reporting null results and failures are commendable. All five reviewers found value in the work, and several noted that the evidence-type findings (import graphs beneficial, code signatures harmful, LLM confidence uncalibrated) are directly actionable for the community.

However, the reviewers identified significant issues that must be addressed before this work can be accepted for publication.

### Required Revisions

**1. Address the primary construct validity challenge (DA C1, C2; also raised by EIC, R2, R3).**
The Maintainability Index is insufficient as the sole dependent variable for a claim about *architecture-aware* maintainability improvement. You have two options: (a) add at least one architecture-level structural metric (e.g., cyclic dependency ratio, modularity index, or inter-module coupling intensity) and show results on both MI and the architecture-level metric; or (b) reframe the paper's central claim explicitly: "LLM-based code-level tactic implementation guided by architectural context" rather than "architecture-aware maintainability improvement." Option (a) is strongly preferred.

**2. Add a baseline comparison (DA C4).**
The paper lacks any comparison condition. At minimum, compare LLM-based tactic implementation against: (a) a random file-splitting baseline (to rule out the mechanical MI improvement argument — DA C2); and (b) a static-analysis-only condition. Without baselines, the paper demonstrates capability but not relative effectiveness.

**3. Add a second annotator (DA C3; all reviewers).**
The single-annotator ground truth in Studies 2 and 3 is a critical threat. Obtain a second annotator for at least a random subset of 20–30 repositories and report Cohen's $\kappa$ or similar. The modular monolith / layered boundary specifically requires this.

**4. Condense implementation details, expand analysis depth (EIC; R1).**
Chapter 4 (~490 lines of pipeline mechanics) is disproportionate relative to the evaluation chapters (~500 lines). Move implementation parameters (BM25 $k$, iteration limits, backup directory structure) to an appendix and use the space to add confidence intervals to all effect sizes, a multiple-comparisons sensitivity analysis, and deeper discussion of Study 3's implications.

**5. Add confidence intervals and multiple-comparisons awareness (R1).**
Report 95% CIs for all $\Delta MI$ means. Acknowledge and bound the multiple-comparisons issue in Study 2 (20 model-prompt comparisons).

### Optional but Recommended

- Add a cost-benefit estimate (R3) — API tokens, execution time, and break-even point for different repository sizes.
- Add a discussion of automation bias and LLM training-data architectural preferences (R3).
- Either trim the tactic catalog to the 4 implemented tactics or explain the 16 exclusions (R2).

### Revision Instructions

Please submit a detailed response letter addressing each point above, with page/line references to changes made. The revised manuscript will be returned to the same reviewer panel for verification.

We look forward to receiving your revision.

Sincerely,
**Dr. Martin Fowler**
Editor-in-Chief, on behalf of the Review Board
