## Topic: LLM for Code Refactoring (Section 2.6)

**Papers:** 12 | **Updated:** 2026-02-17

### Summary

Large language models have rapidly emerged as tools for automated code refactoring, with research spanning standalone prompt-based approaches, multi-agent agentic frameworks, and tool-integrated iterative pipelines. The field has progressed from early evaluations of ChatGPT (GPT-3.5) on simple Java snippets (`depalma2024`) to sophisticated multi-agent systems like MANTRA (`xu2025`) that coordinate Developer, Reviewer, and Repair agents with RAG-enhanced context retrieval, achieving 82.8% success rates on compilable, test-passing refactored code -- a tenfold improvement over standalone single-prompt LLM baselines (8.7%). Two systematic literature reviews (`martinez2025`, `alomari2026`) confirm the rapid growth of this research area while identifying a consistent gap: no existing work addresses architecture-level refactoring or architectural tactic implementation via LLMs. Martinez et al.'s SLR of 50 primary studies (867 initial → 558 unique → 79 screened → 50 selected) provides the most comprehensive mapping to date, cataloging 7 distinct prompt engineering categories, documenting that Java dominates (66% of studies) while Python is second (44%), and quantifying three core challenges: erroneous code generation (50% of studies), failure on complex multi-file tasks (44%), and misunderstanding developer intent (34%). Critically, only 1 of 50 studies (Pandini et al.) addresses architecture-level refactoring (Cyclic Dependency smells via Arcan + LLM), and 72% of studies fail to address data leakage precautions. Meanwhile, a large-scale empirical study of AI coding agents in the wild (`horikawa2025`) demonstrates that current agents function as "incremental cleanup partners" performing low-level renaming and type changes (35.8% low-level operations), not as architectural planners -- only 1.1% of agentic refactoring targets duplication removal, compared to 13.7% for human developers.

Prompt engineering has proven to be the single most impactful lever for improving LLM refactoring outcomes. Generic prompts yield recall rates as low as 15.6% for refactoring opportunity identification, but specifying refactoring subcategories and narrowing the search scope raises success to 86.7% (`liu2025`). Piao et al. (`piao2025`) further demonstrate that rule-based instructions derived from automated detection heuristics outperform human-oriented step-by-step descriptions, and that DeepSeek-V3 achieves 100% success on 48 of 61 Fowler refactoring types with structured prompts. An intriguing "Objective Learning" paradox emerges: allowing LLMs to freely optimize code quality without prescribing a specific transformation type yields the best quality metrics (lowest cyclomatic complexity and LOC) despite producing the lowest correctness for the intended transformation (29.5-36.1%). This suggests a two-phase strategy -- first apply specific transformations with rule-based prompts, then use objective-based prompts for additional quality optimization -- which directly informs the thesis pipeline design.

Behavior preservation remains a critical concern but is generally achievable. DePalma et al. report 97.2% behavior preservation across 320 trials (`depalma2024`), though this was assessed via LLM self-evaluation rather than test execution. More rigorously, Liu et al. (`liu2025`) find a 7.4% unsafe solution rate (semantic bugs and syntax errors) using GPT-4 with automated unit test validation, while MANTRA (`xu2025`) integrates compilation verification, test execution, and RefactoringMiner detection into its feedback loop. The iterative SonarQube-LLM pipeline (`goncalves2025`) achieves over 58% defect reduction with no observed functional breakages across three production Java repositories, validating the iterative feedback loop paradigm. However, all these studies operate at the method or class level -- the thesis fills a fundamental gap by targeting architecture-level transformations (architectural tactics) where behavior preservation challenges are amplified by cross-component dependencies, larger code scopes (well beyond the 300 LOC practical limit identified by `liu2025`), and the need for system-wide reasoning that current LLMs lack.

Industrial evidence from Kim et al. (`kim2014`) provides essential context: in a study of 328 Microsoft engineers, developers define refactoring more broadly than behavior-preserving transformations (46% did not mention behavior preservation), and the top 5% of preferentially refactored modules reduced inter-module dependencies by a factor of 0.85. This confirms that real-world refactoring benefits require multi-dimensional assessment and that the thesis must track multiple maintainability indicators simultaneously -- not just simple issue counts or single metrics.

### Approach Taxonomy
| Approach | Papers | Success Rate | Scope | Verification |
|----------|--------|-------------|-------|--------------|
| Standalone LLM (single prompt) | `depalma2024`, `haindl2024` | 99.7% attempt rate, 97.2% behavior preservation (GPT-3.5); reduced complexity for novices | Method-level (20-50 LOC snippets) | PMD static analysis, self-evaluation, Checkstyle/SonarQube |
| Structured prompt strategies | `liu2025`, `piao2025` | 86.7% with subcategory prompts (`liu2025`); 100% for DeepSeek-V3 on 48/61 types (`piao2025`) | Method-level (<300 LOC) | Expert review (Fleiss' kappa 0.82), unit tests, RefactoringMiner |
| Agentic multi-step framework | `xu2025`, `horikawa2025`, `cordeiro2024` | 82.8% compile+test+verify (`xu2025`); 44.36% smell reduction rate (`cordeiro2024`) | Method-level (extract, move, inline) | Compilation + test suite + RefactoringMiner + DesigniteJava |
| Tool-integrated iterative pipeline | `goncalves2025` | >58% avg issue reduction; best config 81.29% | Code smells (class-level) | SonarQube iterative re-analysis, manual functional review |
| Agentic in-the-wild (observational) | `horikawa2025` | 26.1% of commits target refactoring; 86.9% PR merge rate | Low-level (renaming, type changes dominate) | RefactoringMiner 3.0, DesigniteJava 2.0 |
| SLR / Survey (meta-analysis) | `martinez2025`, `alomari2026`, `wang2025` | 50 primary studies (`martinez2025`): 89% smell reduction (UTRefactor+CoT); 76.3% hallucination rate (EM-Assist); only 28.8% of loop refactorings compilable | Landscape mapping | Systematic search protocol (8 databases, Kitchenham guidelines) |

### Model Comparison
| Model | Best At | Limitations | Source |
|-------|---------|-------------|--------|
| GPT-3.5 (ChatGPT) | Variable/method renaming, formatting, behavior preservation (97.2%) | Defaults to readability/maintainability regardless of target attribute; cannot distinguish coupling/cohesion; generic refactoring only (not Fowler types) | `depalma2024`, `haindl2024` |
| GPT-4 / GPT-4o | Refactoring opportunity identification (86.7% with optimized prompts); solution quality (63.6% comparable to human experts); 27.3% identical to developer solutions | 7.4% unsafe solutions (semantic bugs); moderate negative correlation with code size (-0.38); 0% recall for Extract Class with generic prompts | `liu2025`, `xu2025` |
| GPT-4o-mini | Multi-agent pipeline backbone (82.8% success in MANTRA); cost-efficient (<$0.10 per refactoring) | 83.6% peak on benchmark with Step-by-Step prompts; lower than DeepSeek-V3 on diverse types; compilation rates 38-51% in real scenarios | `xu2025`, `piao2025` |
| GPT-4-mini | Iterative SonarQube issue reduction | More sensitive to parameter tuning than Gemini; worst config only 49.49% issue reduction; temperature-prompt interaction issues | `goncalves2025` |
| DeepSeek-V3 | Broadest refactoring type coverage: 100% success on 48/61 Fowler types; zero new test failures once code compiles | Open-source model; limited evaluation on real-world (as opposed to benchmark) scenarios | `piao2025` |
| StarCoder2-15B | Code smell reduction (44.36% vs. 24.27% human); implementation smell handling; complexity reduction (17.4% AvgCyclomatic) | Very low Pass@1 (28.36%); fails at architectural-level changes (modularization, encapsulation); hallucination risk | `cordeiro2024` |
| Gemini 1.0 Pro / Gemini | Iterative improvement (81.29% issue reduction with 5 iterations); more robust across configurations; consistent performance | Lower initial refactoring identification (3.9% generic prompt recall vs GPT's 15.6%); 6.6% unsafe solutions | `liu2025`, `goncalves2025` |
| Claude Code | Minimal presence in empirical studies (0.6% of agentic commits in AIDev dataset) | Insufficient data for reliable comparison; underrepresented in current refactoring research | `horikawa2025` |

### Behavior Preservation
| Method | Description | Success Rate | Source |
|--------|-------------|-------------|--------|
| LLM self-evaluation | ChatGPT asked to verify its own output preserved behavior | 97.2% (311/320); 9 failures: wrong variable calls (6), incorrect loop params (2), data type errors (1) | `depalma2024` |
| Automated unit testing | 102 unit tests (59 inherent + 43 auto-generated) run against refactored code | 7.4% unsafe rate (GPT-4); 18/22 semantic bugs, 4/22 syntax errors | `liu2025` |
| Compilation + test + RefactoringMiner | Three-gate verification: code must compile, pass all tests, and be confirmed as valid refactoring by RefactoringMiner | 82.8% pass all three gates | `xu2025` |
| EvoSuite-generated test suites | Automated test generation for functional equivalence checking | Pass@1: 28.36%; Pass@5: 57.15% (multiple generations improve) | `cordeiro2024` |
| Manual inspection + execution | No automated test suite; manual review of functional preservation | No breakages observed; conservative changes (renaming, method extraction) | `goncalves2025` |
| Compilation + project test suite | Compile and run existing project tests on refactored code (ANTLR4, JUnit) | 38-51% compilation rate; DeepSeek-V3 produces zero new failures once compiled | `piao2025` |
| Verbal Reinforcement Learning (Reflexion) | Multi-agent self-reflection: Reviewer provides feedback, Developer revises, Repair agent fixes compilation/test failures iteratively | Repair Agent recovers 50.7% of otherwise-failing cases | `xu2025` |

### Prompt Engineering Strategies
| Strategy | Effect | Source |
|----------|--------|--------|
| Quality-attribute keywords in prompts | Including specific keywords (e.g., "quality and performance") triggers more significant refactoring than generic "quality" alone | `depalma2024` |
| Specifying refactoring subcategory | Recall jumps from 15.6% (generic) to 52.2% (type-specified) to 86.7% (subcategory + narrowed scope) -- 5.5x improvement | `liu2025` |
| Rule-based instructions (machine-oriented) | Heuristics from automated detection tools outperform human-oriented step-by-step descriptions for GPT-4o-mini | `piao2025` |
| Step-by-Step (human-oriented) | GPT-4o-mini peaks at 83.6% success; DeepSeek-V3 achieves 100% -- effective but model-dependent | `piao2025` |
| Objective Learning (goal-only) | Lowest correctness (29.5-36.1%) but best quality metrics (lowest CC and LOC) -- LLMs improve quality when given freedom | `piao2025` |
| One-shot prompting | Pass@1 improves +6.15% over zero-shot; smell reduction +3.52%; adds example-guided reasoning | `cordeiro2024` |
| Chain-of-thought prompting | Adds 7 new refactoring types to LLM capability (Extract Method, Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, Parameterize Variable) | `cordeiro2024` |
| Zero-shot with SonarQube context | SonarQube-detected issues embedded in prompt; iterative re-prompting with updated analysis | `goncalves2025` |
| Temperature calibration | Low temperature (0.1) + clear prompt = best results; high temperature (0.3) + vague prompt = worst results | `goncalves2025` |
| Context-Aware RAG | Dense (MiniLM) + sparse (BM25) retrieval merged with Reciprocal Rank Fusion; provides relevant code context to LLM agents | `xu2025` |
| Multiple generations (Pass@K) | Pass@5 yields 28.8% higher test pass rate than Pass@1; best-of-K selection is practical quality strategy | `cordeiro2024` |

**Cross-study prompt taxonomy from Martinez SLR (`martinez2025`, 50 studies):**

| Technique | Studies | Share | Most Effective When |
|-----------|---------|-------|---------------------|
| Context-Specific | 27 | 22% | Provides codebase context, usage patterns, quality goals |
| Few-Shot | 25 | 21% | Python (reduced CC 17.35%, LOC 25.85%); multiple examples |
| Zero-Shot | 19 | 16% | Baseline; minimal context |
| Chain-of-Thought | 18 | 15% | Adds diversity + new refactoring types; not always correctness |
| Output Constraints | 15 | 12% | Format/correctness specifications |
| One-Shot | 12 | 10% | Java correctness (34.51% test pass, best smell reduction 42.97%) |
| Ranking | 2 | 2% | Multiple versions ranked — least explored |

### Refactoring Types: Well vs Poorly Handled
| Well Handled | Poorly Handled | Source |
|-------------|----------------|--------|
| Rename Variable/Parameter/Method (high success across all models) | Extract Class (0% with generic prompts; both GPT and Gemini fail) | `liu2025`, `horikawa2025` |
| Extract Variable (0.94 success, easiest to compile) | Move Method (RawGPT fails entirely; requires cross-file context) | `piao2025`, `xu2025` |
| Split Variable (1.0 success, highest compilation rate) | Inline Variable (never compiles in real scenarios) | `piao2025` |
| Extract Method (70% good/excellent; MANTRA 77.1% vs EM-Assist 51.5%) | Introduce Special Case (never compiles in real scenarios) | `liu2025`, `xu2025`, `piao2025` |
| Inline Method (87.5% good/excellent for inline-related) | Broken Modularization (developers outperform LLMs) | `liu2025`, `cordeiro2024` |
| Change Variable Type (11.8% most common agentic refactoring) | Deficient Encapsulation (developers outperform LLMs) | `horikawa2025`, `cordeiro2024` |
| Long Statement, Magic Number, Empty Catch Clause (implementation smells) | Multifaceted Abstraction, Insufficient Modularization (design smells) | `cordeiro2024` |
| Annotation changes, access modifier changes (systematic, rule-based) | Pull Up Method, Extract Superclass (cross-class structural) | `cordeiro2024` |

### Key Papers
| Paper | Contribution | Relevance |
|-------|--------------|-----------|
| `xu2025mantra` | Multi-agent framework (Developer/Reviewer/Repair) achieving 82.8% success with RAG + Reflexion; proves agentic > standalone by 10x | HIGH -- blueprint for thesis multi-agent pipeline |
| `liu2025exploring` | Prompt optimization: subcategory prompts raise identification from 15.6% to 86.7%; quantifies 7.4% unsafe rate; 300 LOC practical limit | HIGH -- prompt engineering and safety validation strategy |
| `piao2025refactoring` | Systematic evaluation of 5 instruction strategies across all 61 Fowler types; rule-based > step-by-step; Objective Learning paradox | HIGH -- instruction design for architectural tactic prompts |
| `depalma2024exploring` | First systematic evaluation of ChatGPT for quality-attribute-specific refactoring; 97.2% behavior preservation; quality attribute confusion gap | HIGH -- baseline evidence and limitation characterization |
| `horikawa2025agentic` | First large-scale empirical study of AI agent refactoring in the wild (15,451 instances); agents are "cleanup partners" not architects | HIGH -- validates thesis gap: architecture-level is unaddressed |
| `cordeiro2024llm` | LLM vs. developer comparison: LLMs excel at implementation smells (44.36% vs 24.27%) but fail at design smells (modularization, encapsulation) | HIGH -- delineates code-level vs architecture-level boundary |
| `goncalves2025sonarqube` | Iterative SonarQube+LLM pipeline: >58% issue reduction; configuration sensitivity (model, temperature, prompt, iterations) | HIGH -- validates iterative static-analysis feedback loop |
| `martinez2025refactoring` | SLR of 50 studies (Nov 2022-Sept 2025, 8 databases, Kitchenham protocol). 7 prompt categories: Context-Specific (22%), Few-Shot (21%), Zero-Shot (16%), CoT (15%), Output Constraints (12%), One-Shot (10%), Ranking (2%). Java dominates (66%), Python second (44%). 3 core challenges: erroneous code (50% of studies, 76.3% hallucination in EM-Assist), complex multi-file failure (44%, only 28.8% loop refactorings compilable), misunderstanding intent (34%, avg 13.58 turns with unstructured prompts). Only 1/50 study at architecture level (Pandini et al. on Cyclic Dependencies). 72% ignore data leakage. 47% of ChatGPT code has style/maintainability issues despite compiling. | HIGH -- most comprehensive gap confirmation; quantifies challenge prevalence; provides prompt taxonomy directly applicable to thesis |
| `alomari2026llm` | SLR covering LLMs for all code quality dimensions; maps to ISO 25010; confirms architecture-level gap | HIGH -- broader quality context |
| `wang2025llmpa` | Survey of LLM-assisted program analysis; identifies token limits, hallucinations, non-determinism as cross-cutting challenges | MEDIUM -- cross-cutting challenge taxonomy |
| `haindl2024chatgpt` | ChatGPT reduces cyclomatic/cognitive complexity for novices; validates LLMs improve low-level maintainability metrics | MEDIUM -- supporting evidence for code-level effectiveness |
| `kim2014refactoring` | Industrial study at Microsoft (328 engineers): refactoring benefits are multi-dimensional; top 5% refactored modules reduce dependencies by 0.85x | MEDIUM -- industrial evidence; multi-metric assessment requirement |

### Consensus
| Finding | Papers | Confidence |
|---------|--------|------------|
| LLMs are effective for localized, pattern-based code refactoring (renaming, complexity reduction, implementation smells) | `depalma2024`, `liu2025`, `cordeiro2024`, `haindl2024`, `horikawa2025`, `piao2025` | High (6 papers) |
| Multi-agent/agentic approaches vastly outperform standalone single-prompt LLM baselines | `xu2025` (82.8% vs 8.7%), `cordeiro2024` (Pass@5 >> Pass@1), `goncalves2025` (iterative > single) | High (3 papers, 10x improvement) |
| Prompt specificity is critical: subcategory/rule-based instructions dramatically improve success rates | `liu2025` (5.5x improvement), `piao2025` (rule-based > step-by-step), `depalma2024` (keyword sensitivity) | High (3 papers) |
| LLMs struggle with architecture-level changes (Extract Class, cross-component refactoring, design smells) | `liu2025` (0% Extract Class), `cordeiro2024` (LLMs fail at modularization), `horikawa2025` (agents do low-level only) | High (3 papers) |
| Behavior preservation is achievable (>90%) but requires external validation (tests, static analysis), not LLM self-assessment | `depalma2024` (97.2% self-eval), `liu2025` (7.4% unsafe with tests), `xu2025` (compilation+test gates) | High (3 papers) |
| Code size >300 LOC significantly degrades LLM refactoring performance | `liu2025` (correlation -0.38), `wang2025` (token limits), `horikawa2025` (agents stick to small edits) | High (3 papers) |
| Iterative approaches with static analysis feedback improve outcomes over single-pass generation | `goncalves2025` (5 iterations > 2), `xu2025` (Repair Agent recovers 50.7%), `cordeiro2024` (Pass@5 >> Pass@1) | High (3 papers) |
| Non-determinism is an inherent limitation requiring multiple runs or temperature control | `depalma2024`, `liu2025`, `piao2025`, `goncalves2025`, `xu2025`, `wang2025` | High (6 papers) |
| LLMs generate erroneous/unreliable code in a majority of empirical studies | `martinez2025` (50% of 50 studies report this); 76.3% hallucination in EM-Assist; 15% Copilot smell introduction; only 28.8% of loop refactorings compilable | High (SLR of 50 studies) |
| Complex multi-file refactoring is a persistent failure mode | `martinez2025` (44% of studies); 45.5% of iteratively refactored methods non-plausible; token limits prevent large codebase processing | High (SLR of 50 studies) |
| LLMs misunderstand developer intent without structured prompts | `martinez2025` (34% of studies); unstructured prompts require avg 13.58 turns vs 1.45 structured; only 50% success detecting bad code | High (SLR of 50 studies) |
| Data leakage is underreported in LLM-refactoring research | `martinez2025`: 72% of studies make no mention of data leakage precautions; only 12% use training/testing splits | High (SLR of 50 studies) |
| Architecture-level LLM refactoring is virtually unexplored | `martinez2025`: only 1/50 studies (Pandini et al.) at architecture level; `horikawa2025`: 0% architectural restructuring in wild | High (SLR + empirical) |

### Contradictions
| Issue | Position A | Position B | Thesis Choice |
|-------|------------|------------|---------------|
| Behavior preservation reliability | `depalma2024`: 97.2% preservation (high confidence) | `liu2025`: 7.4% unsafe rate; `cordeiro2024`: 28.36% Pass@1 | Use external validation (tests + static analysis), not self-assessment. The gap is explained by evaluation method: self-evaluation inflates success; automated tests reveal real failures. |
| Quality-attribute targeting | `depalma2024`: ChatGPT defaults to readability regardless of target attribute (quality confusion) | `piao2025`: Rule-based instructions + DeepSeek-V3 achieve 100% on specific types | Use specific rule-based instructions and advanced models; the quality confusion is a GPT-3.5 limitation that improved models partially overcome. |
| Objective (unconstrained) vs. prescribed prompts | `piao2025`: Objective Learning gives best quality metrics (lowest CC, LOC) | `piao2025`, `liu2025`: Prescribed types give highest correctness of intended transformation | Adopt two-phase strategy: first apply specific tactic with rule-based prompt, then use objective-based prompt for additional quality optimization. |
| Model sensitivity to prompt style | `piao2025`: DeepSeek-V3 achieves 100% regardless of instruction strategy | `goncalves2025`: GPT-4-mini highly sensitive to temperature-prompt interaction | Design pipeline to be model-agnostic with configurable prompt strategies; test across models during evaluation. |
| Smell reduction effectiveness | `cordeiro2024`: LLMs reduce 44.36% of smells (vs 24.27% human) | `horikawa2025`: Median smell reduction delta = 0.00 in agentic commits (negligible) | The difference reflects controlled experiment vs. in-the-wild observation. The thesis pipeline should use controlled, targeted application (like `cordeiro2024`) not ad-hoc agentic usage. |

### Code-Level vs Architecture-Level Gap
| Aspect | Code-Level (Current Literature) | Architecture-Level (Thesis) |
|--------|---------------------|---------------------------|
| Scope | Within-method, within-class (20-300 LOC) | Cross-component, cross-module, system-wide |
| Refactoring types | Extract/Inline/Rename Method/Variable; implementation smells | Extract Service, Introduce Facade, Apply Strategy Pattern, Dependency Inversion; architectural tactics |
| Context required | Single file, local scope | Full project structure, module dependencies, architectural style, design rationale |
| Success rate | 82.8% (MANTRA, method-level) to 86.7% (optimized prompts) | Unknown -- no empirical study exists (thesis contribution) |
| Verification | Unit tests, compilation, RefactoringMiner | Architecture metrics (coupling, cohesion, MI), dependency analysis, integration tests |
| Quality attributes targeted | Readability, complexity, code style | Modularity, analysability, modifiability, testability (ISO 25010 maintainability sub-characteristics) |
| LLM challenge | Token limits at 300 LOC | Token limits at system scale (thousands of LOC across dozens of files) |
| Human role | "Suggestive auxiliary tool" (`liu2025`) | Must be guided by explicit architectural tactic knowledge -- LLMs cannot independently identify architectural improvement opportunities |
| Design smell impact | Negligible -- median 0.00 delta in agentic commits (`horikawa2025`) | Core target -- reducing Broken Modularization, Deficient Encapsulation, Multifaceted Abstraction |
| Existing tools | EM-Assist, JDeodorant, RefactoringMiner | None -- the thesis proposes the first pipeline |
| Industrial evidence | Kim 2014: module-level refactoring reduces dependencies by 0.85x at Microsoft | No industrial study on LLM-driven architectural tactic application |

### Gaps
| Gap | Impact on Thesis |
|-----|-----------------|
| No study combines LLMs with architectural tactic implementation | **Primary thesis contribution** -- the thesis fills this gap directly by designing and evaluating a pipeline for LLM-driven architectural tactic application |
| No evaluation of LLM refactoring beyond 300 LOC in a controlled setting | Thesis must design chunking strategies to decompose architectural changes into manageable units while maintaining cross-component coherence |
| No cross-file or cross-module LLM refactoring evaluation | Thesis must address how LLMs handle transformations spanning multiple files and modules, a prerequisite for architectural tactics |
| Limited model diversity in evaluations (mostly GPT-family and Java) | Thesis should evaluate with multiple models (including open-source) and consider Python backend projects |
| No study evaluates LLM refactoring against ISO 25010 maintainability sub-characteristics | Thesis maps architectural tactics directly to ISO 25010 sub-characteristics (O1), providing a quality-model-grounded evaluation |
| Behavior preservation not validated at architectural level | Thesis needs integration-level testing beyond unit tests to verify system-level behavior after architectural changes |
| No study combines design-smell detection with LLM-guided architectural remediation | Thesis pipeline could integrate DesigniteJava (`horikawa2025` recommendation) for detecting design smells that trigger tactic application |
| Industrial evidence exists for manual refactoring benefits (`kim2014`) but not for LLM-automated architectural refactoring | Thesis provides first empirical evidence of LLM-driven architectural tactic effectiveness on real backend projects |
| SonarQube-LLM pipeline validated for code issues but not for architectural quality | Thesis extends the iterative static-analysis feedback paradigm (`goncalves2025`) from code smells to architectural metrics |
| No standardized accuracy metrics across LLM-refactoring studies (`martinez2025`) | Thesis should define clear, reproducible metrics aligned with ISO 25010 sub-characteristics |
| 72% of studies ignore data leakage; no standardized benchmarks (`martinez2025`) | Thesis dataset must ensure no overlap with LLM training data; use recent GitHub projects |
| Ranking prompting technique barely explored (2/50 studies, `martinez2025`) | Thesis could apply multi-generation ranking: generate K tactic implementations, rank by metric improvement |
| 47% of ChatGPT code has style/maintainability issues despite compiling (`martinez2025`) | Thesis must validate beyond compilation — maintainability metrics are the primary quality gate |

### Recommendations
**Adopt:**
- Multi-agent pipeline architecture from MANTRA (`xu2025`): Developer/Reviewer/Repair agents with compilation+test feedback loops -- adapt Reviewer to use architectural metrics (Radon MI, coupling) instead of RefactoringMiner
- Rule-based instruction formulation from `piao2025`: formalize architectural tactic application as structured transformation rules rather than natural language descriptions
- Iterative static analysis feedback loop from `goncalves2025`: integrate maintainability metrics (Radon) as the iterative quality gate, analogous to SonarQube in their pipeline
- Multiple generation + best-of-K selection from `cordeiro2024`: generate multiple tactic implementations and select the one with best metric improvement
- Context-Aware RAG from `xu2025`: provide relevant architectural context (project structure, existing patterns, dependency graphs) to LLM during tactic implementation

**Adapt:**
- Subcategory prompt strategy from `liu2025`: instead of specifying refactoring subcategories, specify architectural tactic subcategories (e.g., "Apply Encapsulate Dependencies tactic to reduce coupling between module A and module B")
- Two-phase prompting from `piao2025` Objective Learning: Phase 1 applies specific tactic with rule-based prompt (correctness), Phase 2 uses objective prompt ("improve maintainability") for quality optimization
- 300 LOC chunking strategy: decompose architectural changes into per-module or per-class transformation units, each within LLM context limits, while maintaining a system-level orchestration plan
- DePalma's quality-attribute keyword strategy (`depalma2024`): use ISO 25010 sub-characteristic keywords (modularity, analysability, modifiability, testability) in prompts to steer LLM toward architecture-relevant improvements

**Avoid:**
- Single-prompt standalone LLM usage: 8.7% success rate (`xu2025`) is insufficient for reliable architectural transformation
- LLM self-evaluation for behavior preservation: 97.2% self-assessed rate (`depalma2024`) does not reflect actual ~7% unsafe rate found with automated tests (`liu2025`)
- Generic/vague prompts: 15.6% recall with generic prompts (`liu2025`) makes this approach impractical
- Relying on single metric for quality evaluation: Kim 2014 shows refactoring benefits are multi-dimensional; SonarQube issue counts alone miss architectural quality (`goncalves2025`)
- High temperature with vague prompts: worst configuration combination (`goncalves2025`)
- Expecting LLMs to independently identify architectural improvement opportunities: agents in the wild do not perform design-level reasoning (`horikawa2025`)

### Related Work Draft
> Recent research has established both the promise and limitations of using large language models for automated code refactoring. Standalone LLM approaches demonstrate high behavior preservation rates -- DePalma et al. report 97.2% across 320 refactoring trials with ChatGPT \cite{depalma2024exploring} -- but are constrained to superficial improvements (renaming, formatting) when given generic prompts, defaulting to readability and maintainability regardless of the targeted quality attribute. The effectiveness of LLM-based refactoring is highly sensitive to prompt design: Liu et al. show that specifying refactoring subcategories and narrowing the search scope raises identification recall from 15.6% to 86.7% \cite{liu2025exploring}, while Piao et al. demonstrate that rule-based instructions derived from automated detection heuristics outperform human-oriented step-by-step descriptions, with DeepSeek-V3 achieving 100% success on 48 of 61 Fowler refactoring types \cite{piao2025refactoring}. Multi-agent frameworks represent a significant advance: MANTRA's coordinated Developer, Reviewer, and Repair agents with RAG-enhanced context retrieval achieve 82.8% success on compilable, test-passing refactored Java code, compared to 8.7% for a single-prompt baseline \cite{xu2025mantra}. Tool-integrated iterative approaches also prove effective, with Goncalves and Maia's SonarQube-LLM pipeline reducing code quality issues by over 58% through iterative feedback cycles \cite{goncalves2025sonarqube}. Two recent systematic literature reviews confirm the rapid growth of LLM-based refactoring research while identifying persistent gaps. Martinez et al.'s SLR of 50 primary studies across 8 databases identifies three dominant challenges: erroneous code generation (50\% of studies), failure on complex multi-file tasks (44\%), and misunderstanding of developer intent (34\%), while cataloging seven distinct prompt engineering categories with Context-Specific (22\%) and Few-Shot (21\%) being the most prevalent \cite{martinez2025refactoring}. Critically, only one of 50 studies addresses architecture-level refactoring \cite{martinez2025refactoring, alomari2026llm}.
>
> However, a fundamental gap persists between code-level refactoring and architecture-level transformation. Cordeiro et al. demonstrate that LLMs excel at reducing implementation smells (44.36% reduction vs. 24.27% for developers) but fail at design-level changes requiring cross-class reasoning, such as broken modularization and deficient encapsulation \cite{cordeiro2024llm}. Liu et al. report 0% recall for Extract Class with generic prompts and a practical limit of 300 lines of code \cite{liu2025exploring}. Most tellingly, Horikawa et al.'s large-scale study of 15,451 refactoring instances by AI coding agents in real open-source projects finds that agents function as "incremental cleanup partners" performing predominantly low-level edits (35.8% of refactorings), while high-level architectural restructuring and design-smell remediation remain negligible -- median design smell reduction is zero \cite{horikawa2025agentic}. Industrial evidence from Kim et al.'s Microsoft study confirms that meaningful refactoring benefits require system-level, multi-dimensional assessment across coupling, complexity, and code size metrics \cite{kim2014refactoring}.
>
> The present work addresses this gap by targeting architectural tactic implementation -- a level of abstraction that no prior study has attempted with LLMs. Our approach builds on the validated paradigm of multi-agent pipelines with static analysis feedback \cite{xu2025mantra, goncalves2025sonarqube} and adopts prompt engineering strategies proven effective for code-level refactoring \cite{liu2025exploring, piao2025refactoring}, while extending them to the architectural level where cross-component reasoning, ISO 25010 quality sub-characteristic targeting, and system-wide behavior preservation are required.
