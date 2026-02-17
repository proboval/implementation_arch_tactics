# Research Gaps and Future Directions

> **Learning objectives.** After reading this chapter you should be able to (1) describe the "transformation gap" between tactic detection and LLM-based code refactoring, (2) enumerate the specific research gaps that remain open in the literature, (3) evaluate the available datasets and benchmarks for future work, (4) outline a concrete five-point future research agenda, and (5) synthesize the journey of this entire study guide into a coherent understanding of the field's trajectory.

---

The previous chapter catalogued the challenges that confront LLM-based architecture transformation. This chapter asks a different question: *What has not yet been attempted?* By mapping the boundaries of existing work, we can identify the gaps that represent the highest-impact opportunities for advancing both research and practice. We begin with the core contribution gap that motivates the thesis, then enumerate specific open questions, survey available datasets, and conclude with a forward-looking research agenda.

## 9.1 The Transformation Gap

The most significant finding from our survey of the literature is that two mature, active research streams exist in almost complete isolation from each other.

**Stream 1: Tactic Detection.** A substantial body of work focuses on identifying which architectural tactics exist (or should exist) in a codebase. Marquez et al.'s systematic mapping study of 91 primary studies catalogues the full landscape of architectural tactics research, documenting 12 quality attributes, 10 tactic taxonomies, and the techniques used for tactic identification (manual mapping, code analysis, text analysis, ML-based classification) [@marquez2022architectural]. Ge et al.'s ArchTacRV tool uses machine learning to detect behavioral methods of tactic structures in code and then verifies their runtime consistency against RBML specifications [@ge2022archtacrv]. Bi et al. mine architecture tactic and quality attribute knowledge from 4,195 Stack Overflow posts, revealing relationships between 21 tactics and 8 quality attributes [@bi2021mining]. Shokri et al.'s IPSynth goes furthest, actually *implementing* tactics using program synthesis --- but with a formal specification model (FSpec) and SMT solver, not an LLM [@shokri2024ipsynth].

**Stream 2: LLM Code Refactoring.** A parallel body of work demonstrates that LLMs can transform code to improve quality. MANTRA achieves 82.8% success at method-level refactoring using a multi-agent LLM pipeline [@xu2025mantra]. Liu et al. show that LLMs with optimized prompts can identify 86.7% of refactoring opportunities and produce solutions rated comparable to human experts 63.6% of the time [@liu2025exploring]. Piao et al. evaluate LLMs across all 61 of Fowler's refactoring types, finding that rule-based instructions outperform descriptive ones [@piao2025refactoring]. Horikawa et al. analyze 15,451 real-world refactoring instances by AI coding agents, establishing that agents are active refactoring participants --- but at the code level, not the architecture level [@horikawa2025agentic].

**The gap is between them.** No existing work uses LLMs to implement architectural tactics. The detection stream knows *what* tactics to apply but has no LLM-based mechanism to *apply* them. The refactoring stream can *transform code* but lacks the architectural awareness to select and implement *tactics*. The following diagram illustrates this disconnect and the contribution that bridging it would represent:

```
Current State:
  [Tactic Detection]  --------  GAP  --------  [LLM Code Refactoring]
   Marquez (91 studies)                          MANTRA (82.8% success)
   ArchTacRV (ML detection)                      Liu et al. (86.7% recall)
   IPSynth (program synthesis)                   Piao et al. (61 types)
   Bi et al. (SO mining)                         Horikawa (15,451 instances)

Thesis Contribution:
  [Tactic Detection] ---> [LLM Tactic Implementation] ---> [Quality Measurement]
   Identify what              Apply architectural              Measure before/after
   tactics to apply           tactics using LLMs               with multi-tool framework
```

The evidence for this gap is unambiguous:

- **IPSynth** achieves 85% success on tactic implementation --- but uses program synthesis (FSpec + SMT solver), not LLMs. When the same tasks were given to ChatGPT, only 5% were semantically correct [@shokri2024ipsynth].
- **MANTRA** achieves 82.8% success on code refactoring --- but operates at the method level (Extract Method, Move Method, Inline Method), not the architecture level [@xu2025mantra].
- **Horikawa's agents** are empirically characterized as "tactical cleanup partners" that excel at localized consistency improvements but are not "software architects" capable of higher-level structural design [@horikawa2025agentic].
- **Marquez's mapping** of 91 studies found that **71% do not even describe how tactics were identified**, let alone how they might be implemented automatically [@marquez2022architectural].
- **Martinez et al.'s SLR** of LLM-based refactoring research explicitly identifies the absence of architecture-level LLM refactoring as a key gap in the field [@martinez2025refactoring].

Bridging this gap --- building systems that use LLMs to implement architectural tactics in real codebases, verified by multi-tool static analysis --- is the central research contribution that remains to be made.

## 9.2 Specific Research Gaps

Beyond the overarching transformation gap, the literature reveals seven specific research questions that remain unanswered. Each is grounded in empirical evidence.

| # | Gap | Evidence | Research Question |
|---|-----|----------|-------------------|
| 1 | **70% of studies lack tactic identification methods.** Most architectural tactic research does not describe how tactics were identified, making replication impossible and automation difficult. | Marquez et al. found that 65 of 91 primary studies (71%) do not describe their identification technique [@marquez2022architectural]. | How can tactic identification be systematically automated using LLMs or ML, producing reproducible results? |
| 2 | **Design rationale does not trace to code.** Architects express intent as quality attribute requirements and tactic selections, but there is no automated mechanism to translate this intent into concrete code changes. | Multiple studies document the gap between design decisions and implementation [@perry1992foundations; @li2021understanding]. Rosik et al. show that even detected violations are not remediated [@rosik2011assessing]. | How can LLMs bridge the gap between architectural intent (tactic specification) and code-level implementation (multi-file transformation)? |
| 3 | **No cost-benefit quantification for tactic implementation.** While tactics are qualitatively associated with quality attributes, the measurable impact of implementing a specific tactic in a specific codebase has never been systematically quantified. | Bogner et al. map 15 modifiability tactics to SOA/Microservices patterns but acknowledge that the mapping is qualitative, not quantitative [@bogner2019modifiability]. Kim et al. show that refactoring effects are multi-dimensional and metric-dependent [@kim2014refactoring]. | What is the measurable, multi-metric impact of implementing each modifiability tactic, and how does it vary across codebases? |
| 4 | **LLM + static analysis integration is ad hoc.** Several studies combine LLMs with static analysis tools, but each builds its own bespoke pipeline with different tools, configurations, and feedback mechanisms. | Goncalves et al. build a SonarQube-LLM loop but acknowledge that SonarQube as the sole metric misses architectural issues [@goncalves2025sonarqube]. MANTRA uses RefactoringMiner + CheckStyle. No standardized integration framework exists. | How can we create a systematic, reusable feedback loop between LLMs and multiple static analysis tools for architecture-level transformations? |
| 5 | **No Python-specific architectural tactic benchmarks.** Nearly all existing datasets and benchmarks are Java-only, despite Python being one of the most widely used languages for backend and data-intensive systems. | IPSynth: Java/JAAS [@shokri2024ipsynth]. MANTRA: Java [@xu2025mantra]. Liu et al.: Java [@liu2025exploring]. Piao et al.: Java [@piao2025refactoring]. Horikawa et al.: Java [@horikawa2025agentic]. | Can we create reusable, publicly available benchmarks for architectural tactic implementation in Python and other underrepresented languages? |
| 6 | **Agents do not plan architecturally.** Current AI coding agents (Codex, Claude Code, Devin, Cursor) perform refactoring reactively --- responding to individual code issues --- rather than proactively planning architecture-level improvements. | Horikawa et al. find agents overwhelmingly perform low-level edits (renaming, type changes) and recommend equipping agents with design-smell detection tools to enable higher-level reasoning [@horikawa2025agentic]. | How can we elevate AI coding agents from tactical cleanup partners to strategic architectural planners? |
| 7 | **Behavior preservation is not formally verified.** LLM-generated transformations are tested empirically (via test suites) but never formally verified. Architecture-level changes that legitimately alter interfaces are particularly problematic. | Liu et al. report 7.4% unsafe transformation rate [@liu2025exploring]. IPSynth uses a "correct by construction" approach with SMT solving but only for loop-free, single-framework code [@shokri2024ipsynth]. | Can lightweight formal methods (AST-based structural verification, refinement checking) be integrated with LLM output to provide stronger guarantees? |

## 9.3 Available Datasets and Benchmarks

For researchers entering this field, the following table summarizes the currently available datasets and benchmarks relevant to LLM-based architectural transformation. Note the absence of any architecture-level transformation dataset --- which is itself a gap identified in Section 9.2.

| Dataset | Size | Scope | Language | Source |
|---------|------|-------|----------|--------|
| IPSynth Tactic Synthesis | 20 tasks (4--21 methods, 1--10 classes per task) | Security tactic implementation (JAAS authentication) | Java | Shokri et al. [@shokri2024ipsynth] |
| Refactoring Oracle | 703 pure refactoring instances from 10 projects | Method-level refactoring (6 types: Extract/Move/Inline Method + compounds) | Java | MANTRA (Xu et al.) [@xu2025mantra] |
| Fowler Benchmark | 61 refactoring types + 53 real scenarios from ANTLR4/JUnit | Refactoring type coverage across Fowler's full catalog | Java (translated from JS) | Piao et al. [@piao2025refactoring] |
| LLM4Refactoring | 180 real-world refactorings from 20 projects + 102 unit tests | LLM refactoring opportunity identification and solution recommendation (9 types) | Java | Liu et al. [@liu2025exploring] |
| SO QA-AT Corpus | 1,165 labeled posts (4,195 verified QA-AT instances) | Practitioner knowledge on tactic--quality attribute relationships | N/A (text) | Bi et al. [@bi2021mining] |
| AIDev Refactoring | 15,451 refactoring instances across 12,256 PRs from 1,613 repositories | AI agent refactoring behavior in real-world open-source projects | Java | Horikawa et al. [@horikawa2025agentic] |
| DePalma Refactoring | 40 Java files x 8 quality attributes (320 trials) | LLM refactoring across quality attributes | Java | DePalma et al. [@depalma2024exploring] |

Several observations stand out:

- **Every dataset is Java-only** (or language-independent text). There are no code-level datasets in Python, JavaScript, Go, Rust, or C++.
- **The largest dataset** (AIDev, 15,451 instances) captures *what agents have already done*, not what they *should* do --- it is observational, not prescriptive.
- **The only tactic-level dataset** (IPSynth, 20 tasks) is restricted to a single tactic type (authentication) in a single framework (JAAS), and is too small for statistical analysis.
- **No dataset includes architecture-level before/after pairs** with ground truth indicating which tactic was applied, the intended quality improvement, and verification criteria.

Creating such a dataset --- labeled systems before and after tactic implementation, covering multiple languages and tactic types --- is itself a significant research contribution waiting to be made.

## 9.4 Future Research Agenda

Based on the gaps identified above, we propose five concrete research directions that collectively address the transformation gap and its surrounding challenges.

### 9.4.1 LLM-Driven Architectural Tactic Implementation

The most direct contribution is to build and evaluate systems that use LLMs to implement architectural tactics in real codebases. This requires solving several sub-problems simultaneously:

- **Architecture context injection:** Before the LLM generates any code, it must receive a structured representation of the system's current architecture --- dependency graphs, module boundaries, coupling/cohesion profiles, identified design smells. This is analogous to MANTRA's RAG component [@xu2025mantra] but elevated to the architectural level.
- **Multi-file transformation:** Unlike method-level refactoring, tactic implementation inherently requires coordinated changes across multiple files. The system must generate a transformation plan (which files to modify, in what order, with what changes) and execute it atomically.
- **Tactic-specific prompting:** The instruction given to the LLM must encode the tactic's definition, its expected structural effect, and its applicability conditions. Piao et al.'s finding that rule-based instructions outperform descriptive ones [@piao2025refactoring] suggests that formalizing tactics as structured rules (pre-conditions, transformation steps, post-conditions) may be more effective than natural language descriptions.
- **Modifiability tactics as the starting point:** The 15 modifiability tactics catalogued by Bogner et al. [@bogner2019modifiability] --- organized into Increase Cohesion (Split Module, Maintain Semantic Coherence), Reduce Coupling (Use an Intermediary, Restrict Dependencies, Abstract Common Services, Encapsulate), and Defer Binding Time --- provide a concrete, well-defined starting catalog.

A successful system in this space would demonstrate, for the first time, that LLMs can implement named architectural tactics with measurable quality improvement and verified behavior preservation.

### 9.4.2 Multi-Tool Validation Frameworks

The tool disagreement problem (less than 0.4% inter-tool agreement [@lenarduzzi2023critical]) demands a validation framework that synthesizes evidence from multiple complementary tools rather than relying on any single one. Such a framework should include:

- **Multiple static analysis tools:** Combine Radon (Python-specific: Maintainability Index, cyclomatic complexity, Halstead metrics), SonarQube (broad rule coverage, technical debt estimation), Pylint (PEP 8 compliance, design checks), and architecture-specific analyzers (dependency graphs, coupling/cohesion at the module level).
- **Statistical rigor:** Use appropriate statistical tests for before/after comparison: Cliff's Delta for effect size (non-parametric, appropriate for non-normal metric distributions), Wilcoxon signed-rank test for paired comparisons, and Benjamini-Hochberg FDR correction for multiple comparisons --- as Horikawa et al. demonstrate [@horikawa2025agentic].
- **Metric-paradox awareness:** Track multiple metrics simultaneously and interpret them in the context of the specific tactic's intended effect, following Kim et al.'s finding that single-metric evaluation is misleading [@kim2014refactoring].

The goal is not merely to report "metric X improved" but to provide convergent evidence from multiple independent tools that the tactic implementation achieved its architectural intent.

### 9.4.3 Architecture-Aware Agent Pipelines

Current AI coding agents operate without architectural awareness, treating each code change in isolation [@horikawa2025agentic]. The next generation of agents should understand system architecture *before* making changes:

- **Architecture-as-context:** Feed dependency graphs, module boundaries, quality profiles, and design smell reports to the LLM as structured input. This transforms the agent from a code-level responder into an architecture-level reasoner.
- **Proactive tactic selection:** Instead of waiting for a developer to request a specific change, the agent should analyze the system's architectural health, identify opportunities for tactic application, and propose tactic-level improvements --- moving from "tactical cleanup" to "strategic architecture improvement" [@horikawa2025agentic].
- **Multi-agent collaboration:** MANTRA's three-agent architecture (Developer, Reviewer, Repair) [@xu2025mantra] provides a proven blueprint. For architecture-level work, this could be extended to include an Architect Agent (analyzes system architecture and selects tactics), a Developer Agent (generates code changes), a Reviewer Agent (verifies correctness using static analysis and tests), and a Repair Agent (fixes issues identified by the Reviewer).

### 9.4.4 Tactic-Specific Benchmark Creation

The absence of architecture-level transformation benchmarks is a bottleneck for the entire field. Creating such benchmarks requires:

- **Labeled before/after systems:** Real or synthetic codebases captured before and after a known tactic was implemented, with ground truth labels indicating the tactic type, the files affected, and the intended quality improvement.
- **Multi-language coverage:** Especially Python, which is underrepresented in all existing datasets despite being one of the most widely used languages for backend systems.
- **Verification criteria:** For each benchmark entry, a specification of how to verify that the tactic was correctly implemented --- structural checks (does the intermediary class exist? are the original direct dependencies removed?), behavioral checks (do all tests pass?), and quality checks (did coupling decrease? did cohesion increase?).
- **Scalable construction:** Since manual benchmark creation is expensive (Liu et al. report 42 person-days for 180 instances [@liu2025exploring]), explore semi-automated approaches: mine open-source repositories for commits that implement known tactics (using commit message analysis and structural diff patterns), then manually validate a subset.

### 9.4.5 Formal Verification Integration

The 7.4% unsafe transformation rate reported by Liu et al. [@liu2025exploring] is acceptable for developer-reviewed suggestions but not for autonomous pipelines operating at scale. Bridging LLM output with lightweight formal methods could provide stronger guarantees:

- **AST-based structural verification:** After the LLM generates a transformation, parse the before and after versions into abstract syntax trees and verify that the structural changes match the tactic's expected pattern (e.g., for "Use an Intermediary": a new class was created, direct dependencies were replaced with dependencies through the new class, no direct dependencies remain).
- **Refinement calculus for behavioral equivalence:** Use program refinement techniques to verify that the transformed program is a valid refinement of the original --- meaning it preserves all externally observable behaviors while allowing internal structural changes.
- **IPSynth's "correct by construction" paradigm:** IPSynth demonstrates that formal approaches (FSpec models, SMT solving) can achieve 85% semantic correctness on tactic synthesis [@shokri2024ipsynth]. A hybrid approach --- using the LLM for generative code production and formal methods for verification --- could combine the flexibility of LLMs with the guarantees of formal techniques.

## 9.5 Conclusion

This study guide has traced a path through six decades of software engineering research, from the foundational recognition that software architecture is the primary determinant of system quality [@perry1992foundations; @garlan1993introduction] to the modern possibility that large language models could automate the implementation of architectural design decisions.

The journey followed a logical arc:

1. **Software architecture foundations** established that architectural decisions --- not individual lines of code --- determine how maintainable, modifiable, and testable a system will be.
2. **Quality and maintainability models** (ISO/IEC 25010 and its predecessors) provided a standardized vocabulary for measuring software quality, decomposing "maintainability" into modularity, analysability, modifiability, reusability, and testability.
3. **Architectural tactics** gave architects a catalog of design decisions (Split Module, Use an Intermediary, Abstract Common Services, Restrict Dependencies) that systematically target specific quality attributes --- the "building blocks" of quality-driven design [@bass2021software].
4. **Architecture erosion** revealed that even well-designed systems degrade over time, with 83.8% of practitioners reporting quality decline [@li2021understanding], and that detecting erosion does not guarantee its repair [@rosik2011assessing].
5. **Assessment methods** showed that static analysis tools can measure maintainability, but with significant inter-tool disagreement (less than 0.4% [@lenarduzzi2023critical]) and metric-dependent results [@kim2014refactoring], demanding multi-tool, multi-metric evaluation frameworks.
6. **LLMs for code refactoring** demonstrated that automated code transformation is feasible at the method level (82.8% success with multi-agent pipelines [@xu2025mantra]) but remains confined to local, syntactic changes rather than architectural restructuring [@horikawa2025agentic].
7. **Challenges** showed that context blindness, hallucinations, the complexity gap, tool disagreement, and the detection-remediation gap are real but not insurmountable barriers.

The field is at an inflection point. The individual components needed for automated architectural tactic implementation --- tactic catalogs, LLM code generation, multi-agent pipelines, static analysis verification, iterative feedback loops --- all exist. What does not yet exist is a system that combines them: one that takes a tactic specification, understands the target system's architecture, generates the multi-file transformation, verifies correctness, and measures quality improvement.

The **transformation gap** --- the disconnect between tactic detection and LLM-based code refactoring --- is the key unsolved problem. On one side, we know *what* to do (decades of architectural tactics research have produced detailed catalogs and quality attribute mappings). On the other side, we know *how to transform code* (LLMs with multi-agent verification can produce reliable method-level changes). Bridging this gap --- connecting architectural *intent* with automated *implementation* --- would advance both software engineering research (by providing the first empirical evidence of automated tactic implementation) and practice (by giving developers a tool that not only detects architectural problems but fixes them).

The research agenda outlined in this chapter --- LLM-driven tactic implementation, multi-tool validation, architecture-aware agents, tactic-specific benchmarks, and formal verification integration --- provides a roadmap for closing this gap. Future work in any of these directions would contribute meaningfully to the field. Work that addresses several of them simultaneously --- as this thesis aims to do --- has the potential to open an entirely new category of automated software architecture improvement.

---

> **Review questions.**
>
> 1. Describe the "transformation gap" in your own words. Why have the tactic detection and LLM refactoring communities not yet converged?
> 2. Choose one of the seven specific research gaps from Section 9.2 and design a study that would address it. What data would you need? What metrics would you use? What would constitute a successful outcome?
> 3. Why is the IPSynth dataset (20 tasks) insufficient for drawing generalizable conclusions about automated tactic implementation? What properties should a successor dataset have?
> 4. Compare and contrast two of the five future research directions (Section 9.4). Which would have the highest impact if solved? Which is the most feasible with current technology? Justify your answers.
> 5. The conclusion states that the field is at an "inflection point." Do you agree? What developments (in LLMs, in static analysis, in software architecture) would need to occur for automated tactic implementation to become practical?
