# Cross-Verification of CRITICAL Paper Claims

**Source:** NLM cross-verification against 34 sources
**Date:** 2026-02-16

## Verification Results

### Kim 2009 — Modifiability Coverage
- **Claim:** Covers availability, performance, security only
- **Verified:** PARTIALLY ACCURATE
- Mentions modifiability tactics in background (e.g., Semantic Coherence)
- But feature models and specifications limited to Availability, Performance, Security
- **Modifiability explicitly listed as FUTURE WORK**
- **Action:** Update summary to note modifiability is mentioned but not formalized

### Harrison 2010 — Interaction Types
- **Verified:** ACCURATE
- 5 structural types: Implemented-in, Replicates, Added-in-pattern, Added-out-of-pattern, Modified
- 2 behavioral types: Sequences of actions, Timing of actions
- **Action:** Summary already captures these

### Shokri IPSynth 2024 — Success Rate
- **Verified:** 85% CONFIRMED (17/20 programs)
- 100% accuracy on API usage and internal dependencies
- 85% on External dependencies with surrounding code
- **Security tactics only** (JAAS Authentication/Authorization)
- **Action:** Summary is accurate

### Marquez 2022 — Primary Studies
- **Verified:** 91 CONFIRMED (79 initial + 12 snowball)
- **71% rigor gap CONFIRMED** (65/91 studies don't describe tactic identification method)
- **Action:** Summary is accurate

### DePalma 2024 — Behavior Preservation
- **Claim:** 97.2% behavior preservation (311/320)
- **NLM:** 320 code segments confirmed, but **97.2% not explicitly in excerpts**
- 8 quality attributes tested (not Fowler refactoring types): Performance, Complexity, Coupling, Cohesion, Design Size, Readability, Reusability, Understandability
- GPT suggested generic operations (rename, reformat, simplify loops), not specific Fowler refactorings
- **Action:** Verify 97.2% from converted markdown; update summary to clarify quality-attribute-based evaluation
