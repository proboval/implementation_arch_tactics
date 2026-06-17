# Phase 2: Editorial Synthesis & Decision

**Target:** diploma/v3 (current revised draft)
**Date:** 2026-06-17
**Chair:** EIC, on behalf of the review board
**Review focus (author request):** technical questions, reproducibility, project selection, methodology

## Cross-Reviewer Matrix: Consensus vs. Disagreement

| Dimension | EIC | R1 (Method) | R2 (Domain) | R3 (Perspective) | DA | Verdict |
|-----------|:---:|:---:|:---:|:---:|:---:|---------|
| Three-study arc coherent | + | + | + | + | ~ | **Consensus** |
| Reframing to code-level is correct & honest | + | + | + | + | + | **Consensus (5 agree)** |
| §5.6 self-undermining analysis is a strength | + | + | + | + | + | **Consensus (5 agree)** |
| Statistics now adequate (CIs, sensitivity, mult-comp) | + | + | ~ | + | ~ | **Consensus** |
| Import-graph / confidence-calibration findings durable | + | + | + | + | + | **Consensus (5 agree)** |
| Title/Ch.3 ↔ conclusion alignment | − | ~ | − | ~ | − | **Consensus: misaligned** |
| Architecture-level metrics delivered | − | **C** | **C** | ~ | ~ | **Consensus: promised, missing** |
| Label-quality claim (18.2%→42.9%) sound | − | **C** | ~ | ~ | **C6** | **Divergent → confound** |
| Code-level ceiling = LLM limit vs harness design | ~ | ~ | **C** | ~ | **C5** | **Major: partly harness-designed** |
| Baseline needed for defense (vs publication) | ~ | ~ | ~ | ~ | **C4** | **Divergent (see arbitration)** |
| Reproducibility package sufficient | ~ | **C** | ~ | ~ | **C9** | **Consensus: insufficient** |

*(+ strength, ~ neutral/acknowledged, − weakness, C specific criticism)*

## Arbitration of Disputed Issues

**Issue: Is the missing baseline (C2/C4) a defense blocker?**
- DA holds it as an open CRITICAL/MAJOR; R1/R2/R3 want it for publication; EIC notes the thesis already *demonstrates* the confound it would test.
- **Resolution:** The baseline is **required for publication, optional-but-strongly-recommended for the defense.** Because the thesis itself proves the file-splitting confound (§5.6, ρ=0.74) and reports the fragile significance honestly, it does not *hide* the gap — it documents it. A defense can stand on "we identified and characterized the confound; the controlled baseline is the immediate next step." However, the cheap partial substitute — **LOC-weighted MI (R1-T1/R3-P2)** — is computable from existing data and should be done *before the defense*, because it directly tests the mechanical-splitting hypothesis without new data collection. This is promoted to MUST.

**Issue: Architecture-level metrics promised (§3.10.4) but absent from Ch.5 (R1-T2, R2-S3).**
- Unanimous that this is a method↔results gap. Two reviewers rate it C.
- **Resolution:** MUST. Either report cyclic-dependency ratio / coupling intensity / package-tangle deltas for the 42 Study-3 repos, or remove the §3.10.4 commitment. A methodology that claims a measurement the results never present cannot be evaluated and reads as an unfulfilled response to the prior review.

**Issue: Confounded label-quality claim (R1-M2, C6).**
- No reviewer defends the causal framing across two different populations.
- **Resolution:** MUST (writing-level). State the 162↔57 overlap explicitly and restate "18.2%→42.9%" as associational unless a within-sample arm is run.

**Issue: Code-level ceiling — LLM limitation or harness artifact (R2-D2, C5)?**
- Domain + DA: the harness *forbids* package creation by construction (no `__init__.py` edits, single-file patches, ≤5 iterations).
- **Resolution:** MUST (writing-level). The central architectural conclusion must explicitly attribute the code-level ceiling jointly to LLM behavior *and* harness design. This does not weaken the finding for *this* pipeline; it bounds its generality.

**Issue: Single annotator (C3).**
- Unanimous concern; acknowledged thoroughly in-text.
- **Resolution:** Required for publication (second-annotator subset + κ, oversampling modular-monolith). For the defense, the prominent acknowledgment (§5.12.1, §6) is acceptable.

## Devil's Advocate CRITICAL Issue Evaluation

| DA Issue | Severity | Verdict |
|----------|----------|---------|
| **C1** — MI ≠ construct | CRITICAL | **Downgraded / resolved-by-reframing** — conditional on title alignment + delivering §3.10.4 metrics. The thesis demonstrates and absorbs the critique. |
| **C2/C4** — file-splitting confound, no baseline | CRITICAL/MAJOR | **Upheld but re-scoped** — open for publication; mitigated for defense by the in-text demonstration + the now-mandatory LOC-weighted robustness check. |

> **Checkpoint rule applied:** An upheld CRITICAL-class item (C2/C4) stands, so **ACCEPT is not available.** Given that the thesis honestly documents the confound and the defense bar differs from the publication bar, the decision is **MINOR REVISION for the defense**, escalating to **MAJOR REVISION for journal submission.**

---

## Editorial Decision Letter

**Date:** 2026-06-17
**Decision: MINOR REVISION (for defense) / MAJOR REVISION (for publication)**

Dear Author,

This is a strong revision. The panel unanimously recognizes that you confronted the central construct-validity problem rather than evading it: the §5.6 demonstration that the Maintainability Index gives nearly identical scores to a trivial split (webapp-color) and a genuine decomposition (Paper2Rebuttal), the sensitivity analysis that honestly reports significance collapsing without three outliers, and the confidence-calibration inversion are the marks of a mature empirical thesis. The detection findings (import graphs help all five models; code signatures harm; confidence is uncalibrated) and the code-level-vs-architecture-level gap are durable, citable contributions. The three-study arc is coherent and the statistics are now sound.

The decision is governed by one upheld issue (the missing non-architectural baseline) and a small set of fixes concentrated exactly where you asked us to look — reproducibility, project selection, and method. None of the defense-required items need new data collection.

### Required Revisions — for the defense (MUST)

1. **Align the title and Ch.3 with the reframing (F23, F15, S3, R2-D3).** The title and Ch.3's "architecture-aware workflow" promise architecture-level work the thesis correctly concludes it did not do. Retitle toward "code-level tactic implementation guided by architectural context," or, if the title is fixed, add an explicit reframing paragraph in Ch.1.

2. **Deliver or withdraw the architecture-level metrics (R1-T2, R2-S3).** §3.10.4 promises cyclic-dependency ratio, coupling intensity, and package-tangle deltas for the 42 Study-3 repos. Report them, or delete the promise. As the prior review demanded exactly this for CRIT-1, leaving it unfulfilled is conspicuous.

3. **Add a LOC-weighted ΔMI robustness column (R1-T1, R3-P2).** This is the cheap, decisive test of the file-splitting confound, computable from existing data. Report ΔMI both unweighted and LOC-weighted; it converts §5.6 from "we admit the artifact" into "we quantified it."

4. **De-confound the label-quality claim (R1-M2, C6).** State whether the 57 are a subset of the 162; restate "18.2%→42.9%" as associational unless a within-sample comparison is run.

5. **Own the harness-design confound (R2-D2, C5).** Explicitly state in §5.6/§5.11.3 that the harness (no `__init__.py` edits, single-file patches, ≤5 iterations) cannot create packages by construction, so the code-level ceiling is jointly an LLM and a design property.

6. **Name regression-to-the-mean (R3-P1).** Add it to §5.12.1 and check whether baseline MI predicts ΔMI.

7. **Reproducibility manifest (R1-R4, R1-R5, F5).** Provide the GitHub query + collection date, a per-repo URL+commit-SHA+label manifest for all 162 and 57, and a real artifact link in a Data Availability statement.

8. **Mechanical fixes (consistency).** Replace placeholder running-header `\chaptermark` text (F6); distinguish Study-3 cloning failures from Study-1 LLM failures (F11); resolve the 57→56 attrition (F12); confirm or drop Deferred Binding Time (F14).

### Required for publication (MAJOR — not blocking the defense)

- **Non-architectural baseline (C2/C4):** random file-splitting arm, ideally also static-analysis-only. The decisive control.
- **Second annotator + Cohen's κ (C3):** ≥20–30 repos oversampling modular-monolith.
- **Prompts + model snapshots (R1-R1, R1-R2):** verbatim prompts in an appendix; record model versions/dates and Radon version (R1-R3).
- **Variance estimate (R1-M1):** repeat the best detection configuration 3–5× and report stability.
- Remove internal "Devil's Advocate C1/C2" references from any external version (F18).

### Optional but recommended
- Foreground the durable findings over the fragile significance in the abstract (P1).
- Re-anchor cost-benefit on the median (zero-gain) repo and state the compounding success rate ≈0.52 (R3-P4, R3-I2).
- A "faithful vs. mechanical" tally across the 18 improved repos (R2-D4).

Please submit a response letter mapping each MUST item to the changed sections. The revised manuscript returns to this panel for verification against the roadmap criteria.

Sincerely,
**EIC**, on behalf of the Review Board
