## IPSynth: Interprocedural Program Synthesis for Software Security Implementation

| Field | Value |
|-------|-------|
| **Key** | `shokri2024ipsynth` |
| **Authors** | Ali Shokri, Ibrahim Jameel Mujhid, Mehdi Mirakhorli |
| **Venue** | arXiv preprint (2024); extended from ASE'21 Research Competition (1st place) |
| **Tier** | Preprint (extended from A*-venue competition track) |
| **Citations** | 0 (as of 2026) |
| **Level** | L3-Thesis-Specific |

### Contribution
IPSynth introduces a novel inter-procedural program synthesis approach that automatically implements architectural tactics in existing codebases. Unlike prior API-based synthesis methods that produce a single code block requiring manual decomposition, IPSynth (1) automatically learns tactic specifications from a pre-trained API usage model (FSpec via ArCode), (2) clusters API calls into sub-tasks annotated with meaningful labels, (3) maps clusters to correct code locations using four scoring criteria (method name similarity, variable availability, control/data dependencies, code quality), (4) generates code sketches with holes resolved via SMT solver (Z3), and (5) adds inter-related code snippets to the correct locations preserving semantic correctness. A comparative evaluation against ChatGPT shows IPSynth achieves 85% overall semantic correctness on 20 tactic synthesis tasks vs. ChatGPT's 5% (1/20), demonstrating that structured, specification-driven synthesis significantly outperforms LLMs on inter-procedural tactic implementation.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 4  |   3   |  3  |   3    | 18/25 |

**Relevance:** CRITICAL

This is the closest existing work to the thesis objective of automated architectural tactic implementation. It provides a formal, non-LLM baseline for tactic synthesis, directly compares against ChatGPT (finding LLMs weak at inter-procedural tasks), and identifies precise challenges (code location identification, dependency preservation, code quality) that the thesis LLM-based approach must address. The paper's evaluation framework (semantic correctness criteria, dataset structure) can inform the thesis experimental design.

### Method & Validation
- **Type:** Tool / Framework with Experimental Evaluation
- **Validation:** Prototype evaluated on custom benchmark; comparative analysis against ChatGPT
- **Evidence:** 20 curated test programs with increasing complexity (4-21 methods, 1-10 classes, 1-6 files); expert review team for correctness assessment; ArCode Plugin tool-based verification (avg. score 0.95/1.0); component-level and end-to-end evaluation

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Overall semantic correctness (IPSynth) | 85% (17/20 programs correct) |
| Overall semantic correctness (ChatGPT) | 5% (1/20 programs semantically correct) |
| ChatGPT syntax correctness | 95% (19/20 compilable, but semantically wrong) |
| Code annotation accuracy (CAS, all criteria) | HR@1 = 85%, HR@2 = 90%, MRR = 0.88 |
| Method name similarity alone (MNS) | HR@1 = 80%, MRR = 0.75 |
| Variable availability alone (AVS) | HR@1 = 15%, MRR = 0.21 |
| Sketch generation accuracy | 100% across all criteria (APIs, hole types, dependencies) |
| Sketch resolution accuracy | 100% (all 60 holes resolved, all 20 programs compilable) |
| ArCode Plugin verification score | Average 0.95/1.0 across all synthesized programs |
| Average synthesis time | 285.2 ms total (155.3 code annotation + 70.5 sketch gen + 33.2 sketch resolve) |
| Average memory usage | 901 MB total |
| FSpec model size | 88 API nodes, 130 dependency edges |
| Dataset size | 20 programs, avg. 4.5 methods per test case |
| ChatGPT failure mode | Generates code for part of the tactic, leaves rest to programmer; hallucinates non-existent APIs (e.g., `subject.hasRole(...)`) |
| IPSynth failure mode | Confused by similar method names, places code in undesired methods (P2, P4, P20) |

### Key Quotes
> "To mitigate these challenges, we introduce IPSynth, a novel inter-procedural program synthesis approach that automatically learns the specification of the tactic, synthesizes the tactic as inter-related code snippets, and adds them to an existing code base." (p. 1)

> "When it comes to semantic correctness, ChatGPT was only able to correctly synthesize the first program (i.e., P1) and failed to have semantically correct implementations for the rest of the programs. For example, it generates code for part of the tactic and leaves the implementation for the rest of the tactic to the programmer." (p. 13)

> "The state-of-the-art approaches are not designed and equipped for such a task... the task of program synthesis in architectural tactic implementation is an inter-procedural task. It means that APIs might be used in different methods of different classes in a program, yet they need to interact with each other through method calls." (p. 3)

> "This approach follows the concept of correct by construction, meaning that we make sure that the synthesis process does not generate an incorrect (semantically and syntactically) tactic." (p. 4)

> "The average ARCODE score for the tactics synthesized by our synthesizer was 0.95, meaning that the tool identifies the synthesized tactics as highly correctly implemented." (p. 13)

### Challenges & Limitations
1. **Loop-free synthesis only:** IPSynth synthesizes loop-free code snippets; more complex tactic implementations with loops are left to future work.
2. **Single framework evaluated:** Experimental study conducted only on the JAAS (Java Authentication and Authorization Services) framework; generalization to other tactic-enabler frameworks not demonstrated.
3. **Small dataset:** Only 20 test programs, though introduced as the first dataset of its kind for inter-procedural tactic synthesis.
4. **Method naming dependency:** Relies heavily on method name similarity for location identification; obfuscated code or poorly named methods would degrade performance (3 failures out of 20 due to similar method names).
5. **Java-only:** Approach relies on JavaParser and WALA for static analysis; not language-agnostic.
6. **No import handling:** Synthesized code does not automatically add required import statements.
7. **No abstract class implementation:** Cannot automatically implement abstract methods or interfaces required by the tactic (e.g., `CallbackHandler.handle()`).
8. **Security tactics only:** Focuses exclusively on security tactics (authentication); maintainability, performance, or availability tactics not explored.

### Dataset / Benchmark
- **Name:** Architectural Tactic Synthesis Dataset (first of its kind)
- **Size:** 20 Java programs with increasing complexity
- **Language:** Java
- **Domain:** Security tactic implementation (JAAS authentication)
- **Complexity range:** P1 (4 methods, 1 class, 1 file) to P20 (21 methods, 15 classes, 6 files in 4 packages)
- **Average:** 4.5 methods per inter-procedural task
- **Labels:** Correct locations for tactic pieces specified as `{API: [class, line_range]}` dictionaries
- **Availability:** https://anonymous.4open.science/r/Anonymous-82DE (anonymized)
- **Training data:** FSpec model built by ArCode from existing open-source projects using JAAS

### Key Takeaway
IPSynth demonstrates that automated architectural tactic implementation is feasible but requires structured specification models (FSpec) and formal constraint solving (SMT) to achieve high accuracy -- pure LLM-based generation (ChatGPT) fails dramatically at inter-procedural tactic synthesis (5% vs 85% semantic correctness). For the thesis, this suggests that an LLM-based approach to tactic implementation must incorporate architectural context awareness (understanding where code pieces go across methods/classes), dependency preservation mechanisms, and possibly hybrid strategies combining LLM generation with formal verification. The four-criteria scoring system (method naming, variable availability, control/data dependencies, code quality) provides a useful evaluation framework for assessing LLM-generated tactic implementations.

### Snowball References
**Backward:**
- `mirakhorli2015modifications` — Modifications, tweaks, and bug fixes in architectural tactics (MSR 2015) [ref 1]
- `bass2012software` — Software Architecture in Practice, 3rd ed. (foundational AT textbook) [ref 2]
- `shokri2021arcode` — ArCode: Facilitating the use of application frameworks to implement tactics and patterns (ICSA 2021) [ref 8]
- `gopalakrishnan2017latent` — Can latent topics in source code predict missing architectural tactics? (ICSE 2017) [ref 5]
- `garcia2021constructing` — Constructing a shared infrastructure for software architecture analysis and maintenance (ICSA 2021) [ref 7]
- `feng2017sypet` — Component-based synthesis for complex APIs (POPL 2017) [ref 12]
- `alon2019code2vec` — code2vec: Learning distributed representations of code (POPL 2019) [ref 21]

**Forward:** Check Google Scholar for papers citing this (arXiv:2403.10836); also check for follow-up work by Shokri and Mirakhorli at RIT on ArCode/IPSynth extensions.
