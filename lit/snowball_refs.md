# Snowball References Tracker

**Last run:** 2026-02-16 | **Method:** Semantic Scholar citation API + keyword searches

## Forward Snowballing

### kim2009qualitydriven (94 citations total)
| Citing Paper | Year | Relevance | Action |
|---|---|---|---|
| `marquez2022architectural` — Systematic mapping of AT research | 2022 | CRITICAL | ✅ Added |
| `ge2022archtacrv` — ArchTacRV: Detecting tactics in code | 2022 | HIGH | ✅ Added |
| `bi2021mining` — Mining tactics from Stack Overflow | 2021 | CRITICAL | Already had |
| `sharifi2022microtactics` — Clone Microtactics for QA traceability | 2022 | HIGH | Noted |
| `indykov2025tradeoffs` — Quality trade-offs in ML systems | 2025 | MEDIUM | Skipped |

### harrison2010how (113 citations total)
| Citing Paper | Year | Relevance | Action |
|---|---|---|---|
| `marquez2022architectural` — Systematic mapping of AT research | 2022 | CRITICAL | ✅ Added |
| `bi2021mining` — Mining tactics from Stack Overflow | 2021 | CRITICAL | Already had |
| `serban2021adapting` — Adapting architectures to ML | 2021 | HIGH | Noted |
| `jarvenpa2023green` — Green tactics for ML systems | 2023 | MEDIUM | Skipped |
| `paradis2021energy` — Tactics for energy efficiency (Kazman) | 2021 | MEDIUM | Skipped |
| `milhem2022aws` — Tactics in AWS (Harrison co-author) | 2022 | MEDIUM | Skipped |

### depalma2024exploring (43 citations total)
| Citing Paper | Year | Relevance | Action |
|---|---|---|---|
| `xu2025mantra` — MANTRA multi-agent refactoring | 2025 | HIGH | ✅ Added |
| `horikawa2025agentic` — Agentic refactoring at scale | 2025 | HIGH | ✅ Added |
| `martinez2025refactoring` — LLM refactoring SLR | 2025 | HIGH | ✅ Added |
| `alomari2026llm` — LLMs for code quality SLR | 2026 | HIGH | ✅ Added |
| `cordeiro2024llm` — LLM agents for refactoring | 2024 | HIGH | ✅ Added |
| `goncalves2025sonarqube` — SonarQube + LLM pipeline | 2025 | HIGH | ✅ Added |
| `piao2025bridging` — Refactoring with LLMs: instruction strategies | 2025 | HIGH | Noted |
| `midolo2026human` — GPT-4 Python class refactoring | 2026 | HIGH | Noted |
| `karabiyik2025refactorgpt` — RefactorGPT multi-agent | 2025 | HIGH | Noted |

### liu2025exploring (17 citations total)
| Citing Paper | Year | Relevance | Action |
|---|---|---|---|
| `xu2025mantra` — MANTRA (also cites depalma) | 2025 | HIGH | ✅ Added |
| `horikawa2025agentic` — Agentic refactoring (also cites depalma) | 2025 | HIGH | ✅ Added |
| `xu2026swerefactor` — SWE-Refactor benchmark | 2026 | HIGH | Noted |
| `robredo2025motivations` — LLM study of refactoring motivations | 2025 | MEDIUM | Noted |

## Backward Snowballing

### From sqr_lit_review BibTeX files
| Source File | Referenced Paper | Relevance | Action |
|---|---|---|---|
| QAM/A09 Maintainability | `oman1992maintainability` — Original MI | HIGH | ✅ Added (bib-only) |
| QAM/A09 Maintainability | `baggen2012standardized` — SIG benchmarking | HIGH | Noted |
| SQR/L02 Metrics | `mccabe1976complexity` — Cyclomatic complexity | HIGH | ✅ Added (bib-only) |
| SQR/L02 Metrics | `halstead1977elements` — Halstead metrics | HIGH | ✅ Added (bib-only) |
| SQR/L02 Metrics | `chidamber1994metrics` — CK OO metrics suite | MEDIUM | Noted |
| org/practice | `kim2014refactoring` — MS refactoring empirical | HIGH | ✅ Added |
| verif/static | `wang2025llmpa` — LLM program analysis survey | HIGH | ✅ Added |
| verif/static | `sadowski2015tricorder` — Google Tricorder SA | MEDIUM | Noted |

## Key Gap: No Paper Combining LLMs + Architectural Tactics

Forward snowballing on all 4 seeds confirms: **no existing work uses LLMs to automatically implement architectural tactics**. Closest works:
- `ge2022archtacrv` — *detects* tactics but doesn't *implement* them
- `shokri2024ipsynth` — *synthesizes* interprocedural programs for tactic detection, not generation
- `xu2025mantra` — multi-agent LLM *refactoring* but not tactic-level

This validates the thesis research gap.

## Papers Noted but Not Added (available for future inclusion)

| Paper | Year | Why noted |
|---|---|---|
| Sharifi & Barforoosh — Clone Microtactics | 2022 | Bridges tactics→code gap |
| Serban & Visser — Architectures for ML | 2021 | ML system architecture adaptation |
| Piao et al. — LLM refactoring instructions | 2025 | Prompt engineering for refactoring |
| Midolo & Di Penta — GPT-4 Python refactoring | 2026 | Multi-tool quality evaluation |
| Karabiyik — RefactorGPT | 2025 | Sequential multi-agent pipeline |
| Xu et al. — SWE-Refactor benchmark | 2026 | Evaluation benchmark |
| Baumgartner et al. — Data clumps + ChatGPT | 2025 | Pipeline for code smell detection |
