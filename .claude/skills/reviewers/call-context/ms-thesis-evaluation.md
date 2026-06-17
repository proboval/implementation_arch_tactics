# Call Context: Innopolis University MS Thesis Evaluation (2026)

This is the evaluation frame every reviewer applies. The artifact under review is a **Master's thesis** defended before a State Examination Committee at Innopolis University. A strong thesis here is also expected to be **publishable** (journal/conference), so reviewers assess two bars and keep them distinct:

- **Defensibility** — is the thesis sound, complete, and honest enough to pass the defense?
- **Publishability** — would the core contribution survive peer review at a venue such as IEEE TSE, EMSE, JSS, or an ICSE/NIER track?

A thesis can be defensible but not yet publishable. Flag the two separately; do not let publishability demands inflate the defense bar.

## Document expectations

| Element | Expectation |
|---|---|
| Length / format | LaTeX `extreport`, A4, 1.5 spacing, 14pt — Innopolis template. Reviewers read `chapters/*.tex`, never `thesis.pdf`. |
| Structure | Abstract → Ch.1 Introduction → Ch.2 Literature Review → Ch.3 Methodology → Ch.4 Implementation → Ch.5 Evaluation & Discussion → Ch.6 Conclusion → Bibliography → Appendix. |
| Abstract | Self-contained; states problem, approach, headline quantitative results, and the honest scope of the claim. Keywords present. |
| Front matter | Table of contents, list of tables, list of figures. |
| Reproducibility | Data/artifact availability; enough methodological detail to re-run the pipeline. |

## Evaluation criteria

Each examiner scores the dimensions in their lens. The committee aggregates them.

### C1 — Problem relevance & motivation
- Is the problem real, current, and clearly scoped?
- Is the gap in existing work articulated, not just asserted?
- Do the research objectives/questions follow from the motivation?

### C2 — Literature review adequacy
- Coverage of the relevant fields (software architecture, architectural tactics, maintainability metrics, LLM-for-SE, automated refactoring).
- Critical synthesis vs. annotated-bibliography listing.
- Positioning: what does this thesis do that prior work did not?
- Currency: recent (2022–2026) LLM-for-architecture work cited.

### C3 — Methodology soundness
- Research design fits the questions (here: 3 sequential empirical studies).
- Operational definitions; dataset construction and selection criteria stated.
- Ground truth: who labeled, how, with what reliability check.
- Statistics: appropriate tests, effect sizes, confidence intervals, multiple-comparison control.
- Reproducibility: model versions/IDs, inference config, prompts, parameters.

### C4 — Results validity & honesty
- Claims proportionate to evidence; no overclaiming.
- Null results and failures reported, not hidden.
- A genuine **threats to validity** treatment (internal / external / construct / reliability).
- The dependent variable actually measures the construct claimed.

### C5 — Contribution & originality
- A clear, defensible statement of what is new.
- Significance to research and/or practice.
- Practical guidance/recommendations grounded in the evidence.

### C6 — Writing, structure & presentation
- Logical flow; each chapter earns its place and length.
- Figures/tables captioned, referenced, and necessary.
- Terminology and numbers consistent across chapters.
- Implementation detail proportionate (not crowding out analysis).

### C7 — Defense readiness
- Could the candidate answer the obvious hard questions (the devil's-advocate list)?
- Are the limitations stated by the candidate before the committee raises them?

## Priority levels (used in all reviews)

- **MUST** — blocks the defense or makes the central claim unsupported; fix before defending.
- **SHOULD** — significantly weakens credibility/quality; fix if feasible.
- **NICE** — strengthens the thesis; optional polish.
- **DEFER** — legitimately out of scope for an MS thesis; note as future work.

## What separates a pass from a strong thesis here

- Honest, specific limitations the candidate raises *first*.
- A construct-valid dependent variable, or an explicit reframing when it is not.
- At least one safeguard against the most damaging confound (here: baseline comparison; inter-rater reliability).
- Claims scoped to what the evidence supports (e.g., "code-level improvement guided by architectural context" rather than "architecture-aware maintainability improvement" if only MI is measured).
