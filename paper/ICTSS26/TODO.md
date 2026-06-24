# TODO — ICTSS 2026 submission

New version dir: `paper/ICTSS26/` (copied from `tactic_implementation_v3`, 2026-06-23).
Paper: *"Can LLMs Implement Architectural Tactics?"* — [main.tex](main.tex)

## Venue pivot: EASE 2026 → ICTSS 2026

ICTSS = International Conference on Testing Software and Systems (Springer LNCS), Paris, Oct 13–15 2026. CFP: [cfp.md](cfp.md).

| Item | Value |
|---|---|
| **Submission deadline** | **July 1, 2026 (extended)** — ~8 days from today (2026-06-23) |
| Notification | Aug 23, 2026 |
| Camera-ready | Sep 14, 2026 |
| Format | **Springer LNCS, one-column** (PDF only) |
| Length (full paper) | **12–15 pages + ≤2 ref pages** (short/WIP: ≤6 + 1) |
| Review | **Double-blind** (anonymized) |
| Refs | Springer/CrossRef style, **DOIs strongly encouraged** |
| On acceptance | Disclosure of Interests; one fixed corresponding author; ORCIDs encouraged |

---

## ⚠️ P0 — Existential: venue fit (testing reframe)

ICTSS is a **testing** conference; the paper is currently a **maintainability/architecture** paper. As-is it does not fit and risks desk-reject on relevance. It must be reframed around a **testing contribution**.

**The good news — the machinery already exists.** The pipeline does test-baseline detection + **regression gating** + **self-healing** (§4.4.2 + planner loop), but the paper *undersells and even contradicts it* ("behavioral verification = future work"). Reframing this into a first-class contribution simultaneously creates ICTSS fit **and** closes the EASE reviewers' biggest gap (no behavioral-preservation check; CRIT-2/CRIT-4).

Fits ICTSS topics: *"Testing and validation of generative AI outputs"*, *"Regression testing and test maintenance"*, *"LLM-assisted test case generation and oracle design"*.

- [x] **Angle chosen + retitled** → *"Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation"* (tests-as-oracle / behavioral safety-gate).
- [x] **Behavioral-preservation RQs added** — RQ2 (regression gate effectiveness) + RQ3 (test-suite adequacy as oracle); RQ1 keeps the maintainability capability.
- [x] **Test data mined + VERIFIED** — 20 repos produced 121 modification steps; gate ran but caught **0 regressions**; tests meaningfully ran in only **15** repos, 21 passing executions. → honest finding: **test-adequacy gap** (suites too sparse to be oracles). Reframe is grounded, NOT thin.
- [x] **New results subsection added** — §5 "Behavioral Gating and Test Adequacy" (answers RQ2/RQ3).
- [x] **Reframed abstract, intro, motivation/Research-Gaps** (Validation/Oracle Void as gap #1); cites depalma/liu/shokri/horikawa/cordeiro (all already in ref.bib).
- [x] **Stopped framing test execution as "future work"** — fixed §3.6 sentence + 3 Conclusion spots; future work now points to **LLM-assisted test generation**.

> **Reframe landed and is data-backed** (the 0-regressions / test-adequacy finding is a genuine testing-venue contribution). The testing dimension is now first-class, MI is secondary. Remaining reframe polish: consider re-ordering §5 to lead with behavioral gating; optionally retitle §3/§4 to foreground the gate.

---

## P0 — Format conversion: ACM acmart → Springer LNCS  ✅ DONE (builds)

- [x] `llncs.cls` (v2.26) + `splncs04.bst` bundled in this dir.
- [x] Preamble rewritten → `\documentclass[runningheads]{llncs}`; removed CCSXML/`\ccsdesc`/`\acmConference`/ACM bibstyle/acmart `\subsubsection` redef; added `float`, `hyperref` last.
- [x] Author block → LNCS (`\author … \and`, `\authorrunning`, `\institute`, `\titlerunning`); abstract after `\maketitle`; `\keywords` (with `\and`) inside abstract; `\acks` → `\begin{credits}` (`\ackname` + Disclosure of Interests).
- [x] `ref.bib` made BibTeX-compatible: `journaltitle`→`journal`, `@dataset`→`@misc`; `\bibliographystyle{splncs04}`.
- [x] **Builds cleanly** via [build.sh](build.sh) (TinyTeX, no sudo): 0 bibtex errors, 0 undefined citations/refs.
- [x] **LENGTH: 26 → 17 pp.** Body ~14 pp (≤15 ✓); references on pp.15–17. Done: removed the planner algorithm + 2 verbatim JSON blocks (→ replication package), cut 5 case studies to 2, merged/condensed all per-group result prose, Discussion, Threats, Conclusion, and §3. Total is at the 17-pp ceiling (15+2).
  - [ ] *Optional hard buffer to 16 pp:* trim ~5 background citations **or** drop the Fig.~1 pipeline diagram (references currently run ~2.5 pp).

---

## P0 — Double-blind anonymization  (deferred per author: keep real identities for now)

> Decision: real author identities + the **real Zenodo dataset** citation are kept for the working draft (the dataset exists; it is not a prior accepted paper — in-text now says "companion dataset"). Anonymization is the **final step before submission**.
- [ ] Swap author block → anonymous; `\authorrunning`/`\institute` → anonymized.
- [ ] Anonymize self-citation `\cite{chertkov_2026_20051151}` + the tokenized Zenodo Data-Availability link (both deanonymize) — use anonymized mirrors for review.
- [x] `\acks` → `credits` with neutral AI-tools disclosure (not identifying).

---

## P1 — Springer requirements

- [ ] Exactly one corresponding author, marked, with email.
- [ ] ORCID identifiers (encouraged).
- [ ] Disclosure of Interests statement.
- [x] DOIs added/verified via CrossRef — **37 of 44 entries now carry DOIs** (10 published DOIs CrossRef-verified, incl. `wang2025llmpa` upgraded preprint→published *Transactions on AI*; 6 arXiv DOIs for still-unpublished preprints). Remaining 7 are legitimately DOI-less: 4 books (ISBN), ISO 25010 (URL), and 2 papers with no findable DOI (`garlan1995editorial`, `alqutaish2010quality`).
- [ ] Convert bib to **splncs04** style during LNCS migration; tidy the 6 arXiv entries (`@inproceedings` + `booktitle={arXiv preprint…}` → `@misc` + `eprint`/`archivePrefix`).
- [ ] (Optional) sync the new DOIs back to `tactic_implementation_v3/ref.bib` and `diploma/latex_diploma/ref.bib` (header marks them as synced).

---

## P2 — Carry-over quality fixes (from EASE review; still improve the paper)

- [ ] **(#1)** Broken supplementary ref — `examples/webapp-color-decomposability.diff` cited but **not in repo**. Add to package or drop.
- [ ] **(#2)** Docstring coverage "collected" but not reported (fan-out now is, Table 7) — report or stop claiming.
- [ ] **(#3)** RQ3 multiple-comparison — frame tactic/architecture breakdowns (§5.4–5.5) as *exploratory*.
- [ ] **(#4)** Stable-category vs tactic table — "(none selected) = 7" (Table 5) vs "7 planner failures / 7 no-op" (§5.6) not obviously the same 7; reconcile.
- [ ] **(#5)** Verify inferential stats (W=473, p=0.023, r̂=0.35, CI [0.21, 3.04], sensitivity p=0.156) from [../tactic_implementation/artifacts/improvement_maintainability_dataset.csv](../tactic_implementation/artifacts/improvement_maintainability_dataset.csv).
- [ ] **CRIT-2 / CRIT-4 baseline** — random-split / "do-nothing" control. *Largely subsumed by the testing reframe* (behavioral validation is the stronger answer).
- [ ] **CRIT-3 IRR** — single annotator, no Cohen's κ. Acknowledged, not fixed.

### Already resolved in v3 (verify, don't redo)
Peer review: Wilcoxon test (§5.2); bootstrap CI + p-values; failure count reconciled (14); sampling criteria; MI-gaming/metric-arithmetic para + sensitivity; model ID + gen params; failed-vs-completed covariates; regression-to-the-mean.
Thesis CRIT: **CRIT-1** resolved by reframing to "code-level, not architecture-level"; **CRIT-5** scoped to small repos.

---

## Review-track note (updated for ICTSS)

- The existing reviews — Falessi peer review ([review/review_methodology_peer1.md](review/review_methodology_peer1.md)) and the thesis panel ([../../diploma/v3/review/](../../diploma/v3/review/)) — were written for **EASE / the thesis**. Their methodological substance (inferential stats, sampling, MI-gaming, scoping, behavioral-verification gap) carries over and still applies.
- **New ICTSS reviewer lens:** an ICTSS reviewer judges **testing contribution and fit first**. The dominant new risk is *"this is not a testing paper."* Everything else is secondary to the P0 reframe.
- [ ] Re-run the `reviewers` skill (methodology-examiner) **under a testing/ICTSS framing** once the reframe lands, to confirm fit + that CRIT-* stay clear.

---

## Suggested order (deadline July 1 — tight)

1. **Verify test-outcome data + decide reframe/title** — gates everything (P0 fit).
2. **LNCS skeleton** (`llncs.cls`) + migrate content + compact to ≤15pp.
3. **Anonymize** + Springer reqs (corresponding author, DoI statement, DOIs).
4. **Re-review** under the ICTSS testing lens; fix carry-over items #1–#4.

---

## TODO — Replication package (OSF, anonymized for double-blind)

The Data Availability statement now promises an anonymous repository, so build it:

- [ ] **Assemble `replication.zip`** with:
  - [ ] `measure_edit_coverage.py` + `coverage_results.csv` + `RESULTS.md` (coverage/positive-control experiment)
  - [ ] `improvement_maintainability_dataset.csv` (the 56-repo outcome dataset)
  - [ ] static-analysis artifacts (Radon MI logs, architecture proxies, per-step test outcomes)
  - [ ] the two LLM prompt templates (tactic selection + patch generation) + planner pseudocode
  - [ ] pipeline source (the 5 filter modules / 767 LOC)
  - [ ] a top-level `README` describing structure + how to reproduce stats (Wilcoxon W=81, p=0.028) and the coverage run
- [ ] **Anonymize before upload (double-blind):** strip author names from file headers, code comments, commit metadata, file paths, and any embedded emails/URLs; do NOT include `.git`. Re-zip from a clean copy.
- [ ] **Upload to OSF** as an anonymized project; enable a **view-only anonymized link** (OSF: Settings → View-only links → "Anonymize").
- [ ] **Put the anon link in the paper** — replace the placeholder "anonymous repository for double-blind review" in §Data Availability with the actual OSF anon URL.
- [ ] Camera-ready: de-anonymize the OSF project, mint a DOI, and swap the link.
