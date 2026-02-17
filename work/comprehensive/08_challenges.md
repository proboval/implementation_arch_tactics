# Challenges and Limitations

> **Learning objectives.** After reading this chapter you should be able to (1) identify and explain the five core technical challenges that limit LLM-based architectural transformation, (2) describe why static analysis tool disagreement undermines confidence in quality measurements, (3) articulate the detection-remediation gap and its implications for automated architecture improvement, and (4) evaluate the practical obstacles --- from developer trust to behavior preservation --- that any real-world deployment must address.

---

The preceding chapters have established that architectural tactics are powerful instruments for improving maintainability, that architecture erosion silently degrades software quality, and that LLMs show genuine promise for automated code refactoring. This chapter confronts the other side of the story: the obstacles that currently prevent us from simply pointing an LLM at a codebase and asking it to "implement the right architectural tactics." These challenges are not minor inconveniences; they are fundamental barriers that shape the design of any viable automated architecture-improvement pipeline.

We organize the discussion into three categories: technical challenges inherent to LLM-based architecture transformation (Section 8.1), challenges in measuring whether the transformation actually helped (Section 8.2), and practical challenges that arise when deploying such systems in real development workflows (Section 8.3).

## 8.1 Technical Challenges for LLM-Based Architecture Transformation

Architectural tactics are, by definition, cross-cutting design decisions that affect multiple modules and quality attributes simultaneously [@bass2021software]. This makes them fundamentally different from the local, syntactic code edits at which LLMs currently excel. Below we examine the five core technical challenges that any LLM-based tactic implementation system must overcome, providing for each one a description, evidence from the literature, an assessment of severity, and potential mitigation strategies.

### 8.1.1 Context Blindness

**Description.** LLMs process text in a bounded context window. When applied to code, they typically see one file at a time --- or, at best, a small collection of files that fits within the token budget. They have no inherent understanding of the system-wide architectural context: the dependency graph, the module boundary map, the import structure, the runtime call chains, or the design rationale that explains why modules are partitioned the way they are. For architecture-level changes --- which by definition span module boundaries --- this creates a fundamental mismatch between the scope of the problem and the scope of the LLM's awareness.

**Evidence.** The MANTRA framework addresses this gap by introducing a Context-Aware Retrieval-Augmented Generation (RAG) component that retrieves relevant code from the broader repository before the LLM generates a transformation. The ablation study quantifies the impact: removing RAG reduces the success rate from 82.8% to a level that represents a 40.7% decrease, confirming that external context injection is essential rather than optional [@xu2025mantra]. Horikawa et al.'s large-scale empirical study of AI coding agents (OpenAI Codex, Claude Code, Devin, Cursor) provides complementary evidence: agents touch only a single file in the vast majority of their refactoring actions, and their refactoring repertoire is overwhelmingly dominated by low-level, within-file edits (renaming variables, changing types) rather than cross-file structural changes [@horikawa2025agentic]. When agents do attempt structural decomposition (e.g., Extract Subclass, Split Class), the quality gains are large --- but such actions are rare precisely because the agents lack the architectural awareness to initiate them.

**Severity.** High. Architectural tactics inherently require multi-file, multi-module understanding. A tactic like "Use an Intermediary" requires knowing which modules currently depend on each other, creating a new intermediary module, and rewriting import statements and call sites across potentially dozens of files. Without system-wide context, the LLM cannot even identify where the tactic should be applied, let alone implement it correctly.

**Mitigation.** Several strategies can partially address context blindness:

- **Retrieval-Augmented Generation (RAG):** Retrieve relevant files, dependency information, and architectural documentation before prompting the LLM, as MANTRA demonstrates [@xu2025mantra].
- **Context injection:** Feed the LLM a structured representation of the system architecture (dependency graph, module map, quality profile) as part of the prompt, compressing thousands of lines of code into a tractable summary.
- **Multi-agent architectures:** Assign a dedicated "context-gathering agent" that analyzes the codebase and produces an architectural summary, which is then consumed by a "transformation agent" that generates code changes.

### 8.1.2 Hallucinations

**Description.** LLMs are generative models that produce statistically plausible output --- but "plausible" does not mean "correct." In code generation, hallucinations manifest as references to nonexistent variables, methods, APIs, classes, or modules. The LLM may generate a call to `subject.hasRole("admin")` when no such method exists in the codebase's security framework, or import a module that was never defined. These hallucinations are particularly dangerous for architecture-level changes because they often involve framework-specific APIs (dependency injection containers, ORM configurations, security frameworks) where the correct API surface is large and version-dependent.

**Evidence.** The IPSynth study provides the most striking evidence. When ChatGPT was tasked with implementing JAAS authentication tactics in 20 Java programs, it produced syntactically correct (compilable) code 95% of the time --- but only **5% of implementations were semantically correct** [@shokri2024ipsynth]. The dominant failure mode was generating code for *part* of the tactic while leaving the rest to the programmer, and hallucinating nonexistent API calls (e.g., `subject.hasRole(...)` instead of the correct JAAS `Subject.doAs(...)` pattern). Piao et al. report a similar pattern: most compilation errors in their real-scenario experiments were caused by LLMs referencing undeclared variables or methods --- hallucinations from insufficient context [@piao2025refactoring].

**Severity.** Critical. Unlike a naming mistake that produces a compiler error, a semantic hallucination can produce code that compiles and runs but implements the wrong behavior. In the security tactic domain, this means a system that *appears* to authenticate users but actually does not --- a silent, dangerous failure.

**Mitigation.**

- **Compilation and type-checking feedback loops:** Run the LLM-generated code through the compiler immediately and feed errors back to the LLM for correction, as MANTRA's Repair Agent does [@xu2025mantra].
- **Static analysis verification:** Use tools like RefactoringMiner, CheckStyle, or Radon to verify that the generated code meets structural expectations.
- **Test execution:** Run the project's existing test suite after each transformation to catch behavioral regressions.
- **Formal specification matching:** For well-defined tactics, compare the generated code against a formal specification (as IPSynth does with its FSpec model) to verify correct API usage [@shokri2024ipsynth].

### 8.1.3 Token and Length Limits

**Description.** LLM performance degrades as input length increases. While modern models support context windows of 100K+ tokens, the quality of code understanding and generation measurably declines for longer inputs. Architecture-level changes often require understanding thousands of lines of code spread across many files --- far beyond the effective attention span of current models.

**Evidence.** Liu et al. report a moderate negative correlation between code size and LLM refactoring success: correlation coefficients of -0.38 for GPT-4 and -0.28 for Gemini, with practical effectiveness confined to code segments under approximately 300 lines of code [@liu2025exploring]. Beyond this threshold, LLMs increasingly fail to identify refactoring opportunities and produce lower-quality solutions. This is particularly problematic for architectural tactics, which may require coordinated understanding of files totaling thousands of lines.

**Severity.** High. A single Python module implementing a complex service can easily exceed 300 LOC, and understanding the module's role in the system architecture requires examining its callers, callees, and configuration files --- potentially 10,000+ LOC in aggregate.

**Mitigation.**

- **Chunking strategies:** Break the system into logical units (modules, packages) and process each unit separately, maintaining a shared context summary across chunks.
- **Hierarchical prompting:** First prompt the LLM to produce an architectural plan (which files need to change, what changes each file needs), then execute each file-level change in a separate prompt with focused context.
- **Context summarization:** Summarize large files or modules into compact representations (function signatures, class hierarchies, dependency lists) that convey architectural structure without consuming the full token budget.

### 8.1.4 The Complexity Gap

**Description.** LLMs perform well on local, syntactic transformations --- Rename Variable, Extract Method, Inline Variable --- but struggle with cross-cutting, semantic transformations that require understanding design intent and coordinating changes across multiple code locations. This creates a "complexity gap" between the kinds of refactorings LLMs can reliably perform and the kinds of transformations that architectural tactics require.

**Evidence.** Piao et al. evaluated LLMs across all 61 refactoring types in Fowler's catalog and found that success rates are highly type-dependent. On simple refactoring types (variable-level operations), models achieved high success rates, while complex refactoring types requiring cross-cutting changes showed significantly lower performance. In benchmark scenarios, DeepSeek-V3 achieved 100% on some simple types but real-scenario compilation rates ranged only 38--51% across all strategies [@piao2025refactoring]. Horikawa et al. confirm this at scale: agents perform 35.8% low-level refactorings versus only 21.2% medium-level and 43.0% high-level (but the high-level category is dominated by simple type changes, not architectural restructuring). The study concludes that agents are "incremental cleanup partners" rather than "software architects" [@horikawa2025agentic]. Liu et al. found that both GPT-4 and Gemini achieved 0% recall for Extract Class identification with generic prompts --- the most architecturally relevant refactoring type [@liu2025exploring].

**Severity.** High. Architectural tactics like Split Module, Use an Intermediary, and Abstract Common Services are inherently complex, multi-location transformations. If LLMs cannot reliably perform Extract Class (a single-step structural refactoring), they are unlikely to succeed at multi-step tactic implementations without significant scaffolding.

**Mitigation.**

- **Decomposition:** Break complex architectural transformations into sequences of simpler refactorings that LLMs can handle individually. For example, "Use an Intermediary" could be decomposed into: (1) create a new class, (2) move relevant methods into it, (3) update import statements, (4) replace direct calls with calls through the intermediary.
- **Rule-based instruction:** Piao et al. found that formulating transformations as machine-oriented rules (pre/post conditions) rather than natural language descriptions significantly improves LLM performance [@piao2025refactoring].
- **Hybrid approaches:** Use the LLM for the generative parts of the transformation (writing new code) and traditional tools for the mechanical parts (updating imports, renaming references).

### 8.1.5 Non-Determinism

**Description.** LLMs are stochastic models. The same prompt, applied to the same code, can produce different outputs across runs. This non-determinism is problematic for automated pipelines that need consistent, reproducible results --- especially when the pipeline includes multiple stages where each stage's output feeds into the next.

**Evidence.** Multiple studies document this challenge. DePalma et al. note that ChatGPT's unpredictability makes it "difficult to fully assess capabilities," as the same prompt yields different results across runs [@depalma2024exploring]. MANTRA addresses this by setting temperature to 0 to reduce variability, though this does not eliminate it entirely [@xu2025mantra]. Piao et al. run each experiment 5 times per configuration to account for stochastic variation [@piao2025refactoring]. The practical implication is that an automated pipeline cannot guarantee that a transformation that succeeded in testing will produce the same result in production.

**Severity.** Medium. While temperature control and majority voting can reduce variance, they cannot eliminate it. For safety-critical systems or regulated environments where reproducibility is mandatory, non-determinism remains a fundamental concern.

**Mitigation.**

- **Temperature = 0:** Set the LLM's sampling temperature to zero (or near-zero) to minimize randomness, as MANTRA does [@xu2025mantra].
- **Majority voting:** Run the same prompt multiple times and select the most common output, or use an ensemble of models.
- **Deterministic verification:** Accept non-deterministic generation but require deterministic verification (compilation, testing, static analysis) before accepting any output.

### 8.1.6 Summary of Technical Challenges

The following table consolidates the five technical challenges:

| Challenge | Severity | Key Evidence | Current Best Mitigation | Open Problem? |
|-----------|----------|--------------|------------------------|---------------|
| Context Blindness | High | MANTRA needs RAG for 40.7% of success [@xu2025mantra]; agents touch 1 file in vast majority of edits [@horikawa2025agentic] | RAG, context injection, multi-agent | Yes --- no system achieves full architectural awareness |
| Hallucinations | Critical | IPSynth: ChatGPT 5% semantic correctness on tactic synthesis [@shokri2024ipsynth] | Compilation checks, type checking, test execution, formal spec matching | Yes --- semantic hallucinations evade compilers |
| Token/Length Limits | High | Performance degrades beyond ~300 LOC [@liu2025exploring] | Chunking, hierarchical prompting, context summarization | Partially --- improving with larger context windows |
| Complexity Gap | High | 0% Extract Class recall with generic prompts [@liu2025exploring]; agents are "cleanup partners" not "architects" [@horikawa2025agentic] | Decomposition into simpler steps, rule-based instructions | Yes --- no LLM handles multi-step architectural refactoring |
| Non-Determinism | Medium | Same prompt yields different outputs [@depalma2024exploring; @piao2025refactoring] | Temperature = 0, majority voting, deterministic verification | Partially --- mitigated but not eliminated |

Two challenges --- hallucinations and the complexity gap --- are currently open problems without satisfactory solutions. These define the frontier that any LLM-based architectural tactic implementation system must push against.

## 8.2 Measurement Challenges

Even if an LLM successfully implements an architectural tactic, how do we know whether the transformation actually improved the system? Measuring software quality is harder than it appears, and several methodological challenges undermine confidence in before/after comparisons.

### 8.2.1 Tool Disagreement

Lenarduzzi et al. conducted the largest empirical comparison of six widely used static analysis tools (SonarQube, Better Code Hub, CheckStyle, Coverity Scan, FindBugs, PMD) applied to 47 Java projects [@lenarduzzi2023critical]. The results are sobering:

- **Overall inter-tool detection agreement: less than 0.4%.** The best pairwise agreement was 9.378% (FindBugs--PMD at class level); the worst was 0.144% (CheckStyle--PMD).
- **Precision varies dramatically:** SonarQube had the broadest rule coverage but the lowest precision (18%); CheckStyle had the highest precision (86%) but detected mostly syntactic/formatting issues.
- **Only 6 out of 66 rule pairs** showed 100% agreement on detecting the same issue --- all between CheckStyle and PMD.

The implication is stark: **any metric improvement measured by a single tool may not be confirmed by another tool.** If a study reports that LLM-applied tactics reduced SonarQube violations by 30%, a reader cannot assume that an equivalent improvement would appear in PMD, FindBugs, or any other tool. This is not a minor calibration issue --- it is a fundamental disagreement about what constitutes a quality problem.

For researchers and practitioners designing evaluation frameworks, this finding demands a multi-tool validation strategy. Relying on a single tool --- even a respected one like SonarQube --- introduces both false positive risk (the tool flags issues that are not real problems) and blind spot risk (the tool misses issues that other tools catch).

### 8.2.2 No Tactic-Specific Metrics

There is currently no standardized, widely accepted way to measure whether an architectural tactic was *correctly implemented*. We have metrics for code complexity (cyclomatic complexity), coupling (fan-in/fan-out, CBO), cohesion (LCOM), and aggregate maintainability (Maintainability Index). But none of these directly answers the question: "Was the Use an Intermediary tactic correctly applied?"

Architecture conformance checking tools (e.g., Reflexion Modelling, Lattix, Structure101) can verify that module dependencies match an intended architecture [@li2021understanding], but these require a manually specified intended architecture as input --- which may not exist, may be outdated, or may be ambiguous. ArchTacRV [@ge2022archtacrv] proposes ML-based tactic detection combined with runtime behavioral verification against RBML specifications, but it focuses on *detecting existing* tactics rather than *verifying newly implemented* ones, and requires manually authored RBML specifications for each tactic type.

The absence of tactic-specific metrics means that researchers must rely on proxy indicators --- improvements in coupling, cohesion, or complexity that are *consistent with* the expected effect of a tactic, but do not conclusively prove that the tactic was correctly implemented.

### 8.2.3 Dataset Limitations

The benchmarks available for evaluating LLM-based architectural transformations suffer from three systematic limitations:

1. **Java domination.** Nearly all existing datasets and benchmarks are Java-only. IPSynth uses Java/JAAS [@shokri2024ipsynth]. MANTRA evaluates on 10 Java projects [@xu2025mantra]. Piao et al. translate Fowler's JavaScript examples to Java for evaluation [@piao2025refactoring]. Liu et al. restrict their study to Java because refactoring detection tools do not support other languages [@liu2025exploring]. Horikawa et al. analyze only Java files from the AIDev dataset [@horikawa2025agentic]. This means we have virtually no empirical evidence on how LLM-based transformations perform on Python, JavaScript, Go, Rust, or any other language.

2. **Small scale.** IPSynth's benchmark consists of only 20 tasks [@shokri2024ipsynth]. Liu et al.'s carefully curated dataset has 180 refactoring instances --- impressive in rigor but small in statistical power [@liu2025exploring]. Even MANTRA's 703-instance dataset, the largest, covers only 6 refactoring types across 10 projects [@xu2025mantra].

3. **No architecture-level transformation benchmarks.** Every existing benchmark operates at the method or class level. There are no publicly available datasets of systems before and after architectural tactic implementation, with ground truth labels indicating which tactic was applied, where, and what the expected quality improvement should be.

### 8.2.4 The Metric Paradox

Kim et al.'s field study at Microsoft provides a cautionary finding: **the same refactoring can improve one metric while worsening another** [@kim2014refactoring]. In the Windows 7 codebase, modules that underwent intensive refactoring reduced inter-module dependencies by a factor of 0.85 but *increased* lines of code and cross-cutting changes. This means that a simple "did the metric go up or down?" evaluation is insufficient.

The metric paradox is especially acute for architectural tactics, which often involve structural trade-offs. Introducing an intermediary (a new class that mediates between modules) reduces coupling but increases the total number of classes, increases LOC, and may introduce a new point of failure. A naive metric evaluation would see the LOC increase and conclude the transformation was harmful, while a more nuanced analysis would recognize the coupling reduction as the intended benefit.

This demands multi-dimensional evaluation: any assessment of architectural tactic impact must track multiple complementary metrics (coupling, cohesion, complexity, LOC, dependency counts) and interpret them in the context of the specific tactic's intended effect.

## 8.3 Practical Challenges

Technical feasibility and measurement validity are necessary but not sufficient. Even a perfectly functioning LLM-based tactic implementation system faces practical challenges when deployed in real development workflows.

### 8.3.1 The Detection-Remediation Gap

Rosik et al.'s 2-year longitudinal case study at IBM demonstrated a troubling pattern: **none of the 9 identified architectural violations were fixed by the development team**, despite being explicitly detected and reported [@rosik2011assessing]. Developers were aware of the drift. They could see the violations in the Reflexion Model output. But they chose not to fix them because:

- **Risk of ripple effects:** Fixing one violation might break other parts of the system.
- **Time pressure:** The effort required to fix the violation exceeded the perceived benefit.
- **Legacy code entanglement:** Violations were intertwined with code inherited from previous versions.

This finding reveals a fundamental gap between *detection* and *remediation*. The software architecture community has invested heavily in detection (conformance checking tools, smell detectors, metric dashboards), but detection alone does not produce improvement. As Rosik's team observed:

> "Maybe trying to fix these 'minor' issues would've possibly caused larger issues to appear and so made them not worth exploring..." [@rosik2011assessing]

Automated remediation --- using LLMs to not just identify but also *implement* the fix --- could potentially break this cycle by reducing the cost and risk of addressing detected violations. But this requires the LLM's output to be trustworthy enough that developers are willing to accept it, which leads to the next challenge.

### 8.3.2 Developer Trust and Adoption

Developers are, rightly, skeptical of automated architectural changes. Architecture-level modifications are among the highest-risk transformations in software engineering: they touch many files, affect many stakeholders, and can introduce subtle behavioral changes that are difficult to detect.

For automated architecture transformation to gain adoption, the system must provide:

- **Explainability:** Not just "here is the new code," but "here is *why* this change was made, *which tactic* it implements, and *what quality improvement* it targets." The LLM must generate documentation alongside code.
- **Diff-based review:** Changes should be presented as reviewable diffs, not wholesale file replacements, so developers can inspect exactly what changed.
- **Incremental application:** Tactics should be applied in small, individually reviewable steps --- not as a single monolithic transformation that changes 50 files at once.
- **Rollback capability:** Every transformation must be reversible. If the tactic implementation introduces unexpected problems, the developer must be able to return to the previous state instantly.
- **Confidence scores:** The system should report its confidence in each transformation, flagging uncertain changes for human review while applying confident changes automatically.

DePalma et al.'s user study found that while 85.8% of participants rated ChatGPT's refactoring quality at 5 or 6 out of 7, **92.9% said additional refactoring was still needed** [@depalma2024exploring]. This suggests that developers see LLMs as useful starting points but not as replacements for human judgment --- a "suggestive auxiliary tool" rather than an autonomous architect.

### 8.3.3 Behavior Preservation vs. Architecture Improvement

The standard assumption in refactoring research is that transformations must be strictly behavior-preserving: the system's external behavior must be identical before and after the change. This assumption works well for method-level refactorings (Rename Variable, Extract Method) where the external API is unchanged.

But architecture-level transformations may *legitimately require behavioral changes*. Consider:

- **Introducing an intermediary:** The module interfaces change --- callers now go through the intermediary instead of calling the original module directly. The functional outcome is the same, but the calling API is different.
- **Splitting a module:** A single module becomes two modules with a new inter-module interface. Existing clients must be updated to use the correct half.
- **Abstracting common services:** Concrete implementations are replaced by abstract interfaces. Client code must be updated to depend on the abstraction rather than the concrete class.

In each case, the system's *functionality* is preserved (the same inputs produce the same outputs), but the *interfaces* change. Current LLM evaluation frameworks --- which compare before and after behavior through test execution --- may incorrectly flag these legitimate interface changes as failures.

What is needed is a notion of "controlled behavioral change" rather than strict preservation: the system's functional behavior is preserved, but its structural interfaces are allowed to evolve in well-defined ways. Formalizing this notion and building verification tools around it is an open research challenge.

Liu et al. quantify the risk: 7.4% of GPT-4's refactoring solutions introduced unsafe changes (semantic bugs or syntax errors), with semantic changes being more dangerous because they evade compiler checks [@liu2025exploring]. For architecture-level changes that intentionally alter interfaces, distinguishing "intentional interface change" from "accidental semantic bug" requires understanding the designer's intent --- precisely the kind of reasoning that LLMs currently struggle to articulate.

## 8.4 Chapter Summary

The challenges described in this chapter are not reasons to abandon the pursuit of LLM-based architectural tactic implementation. Rather, they define the engineering requirements for a viable system. A successful pipeline must:

1. **Inject architectural context** into the LLM's reasoning (addressing context blindness).
2. **Verify every generated transformation** through compilation, testing, and static analysis (addressing hallucinations).
3. **Decompose complex tactics** into sequences of simpler, manageable transformations (addressing the complexity gap and token limits).
4. **Use multiple complementary metrics** interpreted in the context of each tactic's intended effect (addressing measurement challenges).
5. **Present changes as reviewable, incremental, and reversible diffs** with explanatory documentation (addressing trust and adoption).

The field is not at a dead end. MANTRA has shown that multi-agent pipelines with verification feedback loops can achieve 82.8% success at method-level refactoring [@xu2025mantra]. Goncalves et al. have demonstrated that iterative SonarQube-LLM feedback loops reduce code issues by over 58% [@goncalves2025sonarqube]. The challenge now is to extend these approaches from code-level to architecture-level transformations --- which is precisely the research gap explored in the next chapter.

---

> **Review questions.**
>
> 1. Why is "context blindness" particularly problematic for architectural tactics, as opposed to method-level refactorings? What evidence supports this claim?
> 2. Explain the difference between syntactic correctness and semantic correctness, using the IPSynth ChatGPT evaluation as an example. Why is this distinction critical for tactic implementation?
> 3. If a study reports that an LLM-applied tactic reduced SonarQube violations by 30%, what caveats should a careful reader consider, given the tool disagreement findings of Lenarduzzi et al.?
> 4. Rosik et al. found that 0 out of 9 detected violations were fixed by developers. How could automated remediation change this outcome? What risks does it introduce?
> 5. Why might strict behavior preservation be an inappropriate evaluation criterion for architecture-level transformations? Give a concrete example.
