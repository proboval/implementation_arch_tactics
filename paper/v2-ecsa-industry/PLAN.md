# ECSA 2026 Industry Track Paper — Plan

## Context

The original v1 EASE 2026 submission ("Improving Software Maintainability Through LLM-Implemented Architectural Tactics") was rejected. Reviewer 3 was decisive: the paper tried to do too much — Architecture Detection, Tactic Selection, and Tactic Implementation each deserved a full paper-length treatment. Reviewer 2 also criticized the lack of ground truth validation for architecture classification.

**Decision**: split the work. This paper covers the architecture detection slice only.

A complete, well-structured research paper on architecture detection already exists at `experiment_llm_arch_detection/paper_text/main.tex`. It directly addresses both reviewer criticisms:
- Single focused contribution (detection only)
- Ground truth: 57 manually labeled repositories

The task is to **adapt** that paper for the ECSA 2026 Industry Track Short Paper format (8 pages, Springer LNCS), repositioning it from pure research to a practitioner-relevant experience report.

**Deadline**: May 8, 2026 (paper submission). Abstract deadline was May 1 — confirm with PC chairs if late abstract is still accepted.

---

## Venue

ECSA 2026 Industry Track — Short Papers and Presentations (up to 8 pages LNCS).  
Selection criteria: **originality, practical relevance, potential for discussion**.  
CFP: `paper/v2-ecsa-industry/cfp.md`

Content fits two stated ECSA topics:
1. *"Experience with architectures for emerging technologies, like LLM"*
2. *"Architectural patterns, tactics, and tools"*

---

## Source Material

| File | Role |
|------|------|
| `experiment_llm_arch_detection/paper_text/main.tex` | Source paper (complete, LNCS format) |
| `experiment_llm_arch_detection/paper_text/ref.bib` | Bibliography |
| `lit/` | Full lit review — summaries, insights, `references.bib` |
| `paper/v1/rejection.md` | Reviewer feedback to address |

No figures/plots — paper uses tables only, which is fine.

---

## Files to Create

```
paper/v2-ecsa-industry/
├── PLAN.md         (this file)
├── cfp.md          (exists)
├── main.tex        (create — adapted from experiment paper)
└── ref.bib         (copy from experiment_llm_arch_detection/paper_text/ref.bib)
```

---

## Section-by-Section Adaptation Plan

### Title
Optionally add "in Practice" to signal industry framing:
> "LLM-Based Architecture Detection in Practice: An Empirical Multi-Model Evaluation"

Or keep original if preferred.

### Abstract
Keep 95% as-is. Prepend one sentence grounding the industrial need:
> "Practitioners in large organizations frequently need to assess the architectural style of dozens or hundreds of repositories for migration planning, tech debt assessment, or tooling — yet manual classification does not scale."

### Section 1 — Introduction
- **Lead with industrial problem**: scale challenge, tech debt assessment, architecture-aware migration tooling
- Frame contribution as "what we tried and what we learned" (experience framing)
- Keep the 3 RQs unchanged
- Add one sentence connecting to the broader tactic-implementation pipeline (future work)
- Trim 2–3 academic citations that add bulk without practitioner value

### Section 2 — Background and Related Work (trim)
- **Cut to ~0.5 pages**. Industry track cares less about exhaustive lit review.
- Keep: Bass et al. (architectural style/quality), Esposito survey (research gap)
- Compress: MANTRA, Piao et al., Shokri et al. — one sentence per cluster
- Check `lit/insights/` for any additional relevant findings to incorporate

### Section 3 — Methodology (keep mostly unchanged)
- Keep all subsections (taxonomy, dataset, evidence extraction, prompts, models, metrics)
- Add short motivating note in dataset section: why Python backend repos are a relevant industrial proxy
- Emphasize the reproducible pipeline aspect

### Section 4 — Results (keep all tables)
All tables stay. Add a brief "key takeaway" sentence after each table:
- Table 1: Class distribution
- Table 2: Accuracy / macro-F1 across models × prompts (RQ1, RQ3)
- Table 3: Evidence delta (RQ2) — **most important for practitioners**
- Table 4: Per-class accuracy at P2
- Table 5: Model profiles
- Table 6: Modular monolith misclassifications
- Table 7: Confidence calibration

### Section 5 — Discussion (expand practitioner content)
Keep existing subsections. **Add two new subsections**:

**"Practitioner Guidance"** (~0.5 page):
- Recommended default: file tree + import graph (P2); omit code signatures
- Do not use confidence scores as a reliability filter
- Treat modular-monolith vs. layered predictions with caution; consider 2-class collapse
- Cost-benefit: artifact extraction is lightweight and scriptable — no GPU needed
- Appropriate use: flagging candidates for expert review, not fully automated labeling

**"Industrial Applicability"** (~0.25 page):
- 70.2% accuracy is useful for triage at scale, not for final decisions
- The modular-monolith/layered confusion reflects genuine architectural ambiguity — not only a model weakness
- Discussion hook: what would it take to reach 85%+? (larger dataset, multi-annotator labels, fine-tuning)

### Section 6 — Threats to Validity
Keep all four validity types. Compress prose slightly. Target ~0.25 pages.

### Section 7 — Conclusion
Keep RQ summary answers. Add one sentence:
> "This detection capability is designed as the first stage of a broader architecture-aware quality improvement pipeline, with tactic selection and automated implementation as subsequent steps under active investigation."

### Acknowledgements (NEW — required by ECSA ethics policy)
ECSA **requires** explicit AI tool disclosure (per GAIDeT taxonomy). Add Acknowledgements section listing AI tools used and their roles (writing, code generation, data analysis).

### Data Availability
ECSA explicitly requires this section immediately after Conclusions. Already present in source paper — keep as-is.

---

## Page Budget (8 pages LNCS)

| Section | Target |
|---------|--------|
| Title + Abstract | 0.4 pp |
| Introduction | 1.0 pp |
| Background | 0.5 pp |
| Methodology | 1.5 pp |
| Results | 2.5 pp |
| Discussion | 1.0 pp |
| Threats + Conclusion | 0.4 pp |
| Ack + Data Availability | 0.2 pp |
| References | ~0.5 pp |
| **Total** | **~8.0 pp** |

Background is the primary trim lever if paper runs long.

---

## Implementation Steps

1. Copy `experiment_llm_arch_detection/paper_text/ref.bib` → `paper/v2-ecsa-industry/ref.bib`
2. Check `lit/references.bib` and `lit/insights/` for additional relevant citations for Background
3. Create `paper/v2-ecsa-industry/main.tex` using source paper as base with adaptations above
4. Compile (`pdflatex` + `bibtex`) and check page count
5. Trim Background section if over 8 pages
6. Review: does the paper read as a practitioner experience report?

---

## Verification Checklist

- [ ] Compiles to PDF without errors
- [ ] Page count ≤ 8 in LNCS style
- [ ] All result tables present and readable
- [ ] "Practitioner Guidance" subsection present in Discussion
- [ ] "Industrial Applicability" subsection present in Discussion
- [ ] Acknowledgements with AI tool disclosure present
- [ ] Data Availability section immediately after Conclusion
- [ ] Authors unblinded (single-blind review per CFP)
- [ ] Submitted via EasyChair → "Industry Track"
