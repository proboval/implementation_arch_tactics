# Snowball Cross-Check via NLM

**Source:** NLM analysis of citation overlap across 34 sources
**Date:** 2026-02-16

## Most Frequently Cited (Hub Papers)

| Paper | Cited by | Status |
|-------|----------|--------|
| Bass, Clements & Kazman (2003/2021) | 11+ sources | **In collection** (`bass2021software`) |
| Fowler (1999/2018) Refactoring | 10+ sources | **In collection** (`fowler2018refactoring`) |
| Mirakhorli & Cleland-Huang (2012/2016) Tactic Detection | 7+ sources | **NOT in collection — consider adding** |
| Chidamber & Kemerer (1994) CK Metrics | 6+ sources | Noted in snowball_refs.md |
| Harrison & Avgeriou (2010) | 3+ sources | **In collection** (`harrison2010how`) |
| Silva, Tsantalis & Valente (2016) Why We Refactor | 4+ sources | **NOT in collection** |
| Kim, Zimmermann & Nagappan (2014) MS Refactoring | 3+ sources | **In collection** (`kim2014refactoring`) |
| Heitlager, Kuipers & Visser (2007) SIG Model | 3+ sources | **NOT in collection** |

## Potentially Missing Papers (cited by 3+)

| Paper | Why Important | Action |
|-------|---------------|--------|
| Mirakhorli & Cleland-Huang 2016 | Seminal tactic detection/traceability | Consider bib-only ref |
| Silva et al. 2016 "Why We Refactor" | Ground truth for refactoring motivations | Consider bib-only ref |
| Heitlager et al. 2007 SIG Model | Foundation for Visser's benchmark approach | Consider bib-only ref |
| AlOmar et al. 2021 Behavior Preservation | Mapping study on preserving behavior in refactoring | Consider bib-only ref |
| Chidamber & Kemerer 1994 CK Metrics | Standard OO metrics suite | Consider bib-only ref |

## Behavior Preservation Papers (Critical for Thesis)

| Paper | Contribution |
|-------|-------------|
| AlOmar et al. 2021 | Systematic mapping of behavior preservation techniques |
| Alikhanifard & Tsantalis 2024/2025 | Semantic-aware AST differencing tool |
| Cai et al. 2025 | Refinement calculus for LLM verification |
| Ren et al. 2020 CodeBLEU | AST + semantic data-flow similarity metric |

## Foundational Quality Models (Beyond Halstead/McCabe)

| Model | Sub-attributes |
|-------|---------------|
| McCall 1977 | Analysability, Changeability, Stability |
| Boehm 1978 | Hierarchical quality factors |
| Li & Henry 1993 | MPC, DAC — OO maintainability predictors |
| ISO 25010 (2011) | Modularity, Reusability, Analysability, Modifiability, Testability |

## Recommendation
The literature base is solid. The 5 potentially missing papers are all well-known references that could be added as bib-only entries for completeness, but are not essential gaps. The main finding is that **no paper combining LLMs + architectural tactic implementation** was found across any reference list — confirming the thesis gap.
