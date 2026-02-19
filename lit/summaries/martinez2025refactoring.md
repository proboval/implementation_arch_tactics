## Software Refactoring Research with Large Language Models: A Systematic Literature Review

| Field | Value |
|-------|-------|
| **Key** | `martinez2025refactoring` |
| **Authors** | Sofia Martinez, Luo Xu, Mariam Elnaggar, Eman Abdullah AlOmar |
| **Venue** | Journal of Systems and Software (2025), Stevens Institute of Technology |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Code refactoring is imperative for readability, maintainability, and efficiency, but its exhaustive nature causes developers to avoid it. LLMs are increasingly explored for automation, but individual studies address only isolated aspects (e.g., a single prompting technique, one language, one refactoring type) with no comprehensive synthesis.
- **Gap:** No existing SLR specifically focuses on LLMs applied to refactoring. Prior SLRs covered automated refactoring generally (Baqais & Alshayeb 2020, 41 studies), code smells (Singh & Kaur 2018, 238 publications), or impact on quality (AlDallal & Abdin 2017, 76 studies), but none centered on generative LLMs for refactoring. Additionally, there is a lack of standardized terminology, evaluation metrics, and benchmarks across LLM-refactoring studies.

### Contribution
Systematic Literature Review of 50 peer-reviewed primary studies (Nov 2022 - Sept 2025) from 8 digital libraries, answering 6 research questions. Categorizes studies by tools used, datasets/benchmarks, prompt engineering techniques, accuracy metrics, refactoring types, and key challenges. Identifies 7 distinct prompt engineering categories, catalogs 18 code smell types studied, maps refactoring across code-level, design-level, and architecture-level abstractions, and formulates 10 actionable insights for future research.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 2  |   4   |  5  |   3    | 15/25 |

**Relevance:** HIGH

This SLR provides the most comprehensive mapping of LLM-based refactoring research available. It confirms that nearly all work operates at code-level or design-level refactoring; only 1 study (Pandini et al.) explicitly addresses architecture-level refactoring (Cyclic Dependency architectural smells), and only 1 study (Rajendran et al.) proposes multi-agent systems for design/refactoring. The thesis on automated implementation of architectural tactics fills a clear gap identified here: architecture-level LLM-driven transformations are virtually unexplored. The findings on prompt engineering effectiveness (Context-Specific + Few-Shot being most common), LLM limitations with complex multi-file refactoring, and the 89% code smell reduction achievable with structured prompting are directly actionable for thesis methodology design.

### Method & Validation
- **Type:** Systematic Literature Review (SLR)
- **Protocol:** Followed Kitchenham et al. (2007) guidelines for SLR in software engineering
- **Databases searched (8):** ScienceDirect, Scopus, Springer Link, Web of Science, ACM Digital Library, IEEE Xplore, Wiley, Google Scholar
- **Time range:** November 2022 to September 2025
- **Search string:** Combined refactoring terms ("refactor*" OR "code refinement" OR "code restructure" OR "transforming code" OR "code modification") with LLM terms ("LLM*" OR "language model" OR "ChatGPT" OR "GPT" OR "pre-trained" OR "BERT" OR "Copilot" etc.)
- **Selection stages:**
  - Stage 1: Initial search yielded 867 publications
  - Stage 2: Duplicate removal reduced to 558 unique papers (309 duplicates removed)
  - Stage 3: Title/abstract screening narrowed to 79 papers
  - Stage 4: Full-text analysis selected 50 final primary studies
- **Inclusion criteria:** Peer-reviewed, published in journals/conferences in computing, explicitly discusses LLMs in software refactoring
- **Exclusion criteria:** Non-peer-reviewed (preprints excluded), non-English, position papers, encoder-only models (BERT for classification only), studies not using generative LLMs
- **Quality assessment:** 3 quality questions (objective focus, automatic/semi-automatic approach, sufficient technique description) scored Yes/Partially/No (1/0.5/0)
- **Cross-validation:** Two authors independently reviewed, cross-checked, and reconciled; ChatGPT-4 used to verify completeness of extraction for 32% (16/50) of papers
- **Studies reviewed:** 50 primary studies

### Models & Tools

**LLM models mentioned across the 50 studies (non-exhaustive):**
- **OpenAI family:** ChatGPT-3.5, ChatGPT-3.5 Turbo, ChatGPT-4, ChatGPT-4 Turbo, ChatGPT-4o, ChatGPT-4o mini, GPT-o1, GPT-o3, GPT-2, Codex (via Copilot)
- **Meta/LLaMA family:** LLaMA 2 (7B), LLaMA 3, LLaMA 3.1-405B, CodeLLaMA, CodeLlama-34B
- **Anthropic:** Claude 3.5 Sonnet, Claude 3.7 Sonnet
- **Google:** Gemini, Gemini 1.5, Gemini Pro 2.5, Gemini 2.0 Flash, PaLM
- **Open-source/Other:** StarChat, StarCoder, CodeT5, PLBART, CodeGPT, CodeGPT-adapt, CodeGen, PolyCoder, DeepSeek V2, DeepSeek V3, DeepSeek 7B, CodeQwen 7B, Mixtral-8x22b, StableCode3B, Phi-4, Phind 2.0 70B, Qwen 2.5-Coder, Grok 3 thinking
- **Code models used as tools:** CodeBERT, GraphCodeBERT, RoBERTa, ALBERT, XLNet, CodeReviewer, T5-Review, Unixcoder

**Tools mentioned across studies:**
- **IDE plugins/tools:** EM-Assist (IntelliJ IDEA), JExtract, JDeodorant, JMove, RMove, PathMove
- **Static analysis:** SonarQube, PMD, Radon, Lizard, ESLint, iPlasma, Cayenne, Pinpoint, DesigniteJava, JSpIRIT, Organic
- **Refactoring detection:** RefactoringMiner, SEART, tree-sitter, Pydriller
- **Frameworks:** PyCraft, UTRefactor, RETESTER, iSMELL, HECS, HMove, MoveRec, RRG, MM-Assist, BuildRefMiner, OpenRewrite, MetaGPT, Arcan, LangChain, Ollama
- **Testing:** EvoSuite, Defects4J, SAFEREFACTOR, ASTGen
- **Semantic:** VoyageAI (semantic similarity), Sentence Transformer
- **Benchmarks:** CodeReviewer, SWE-bench, CodeSearchNet, Concode

**Languages studied (across 50 primary studies):**
- Java: 33 studies (66%) -- most prevalent
- Python: 22 studies (44%)
- JavaScript: 10 studies (20%)
- C++: 7 studies (14%)
- Other (24%): C#, Kotlin, TypeScript, Go, Ruby, PHP, SQL, PL/SQL, Bash, C, Swift, Objective-C, Perl, Scala, R, UML, Docker

### Dataset / Benchmark
- **Sources of datasets across 50 studies:**
  - 35 studies (70%) collected data from open-source repositories (GitHub, Apache, F-Droid)
  - 11 studies (22%) relied on previously published work/established datasets
  - 2 studies (4%) sourced from educational environments (student submissions)
  - 2 studies (4%) generated new datasets by prompting LLMs
- **Scale range:** Smallest: 116 methods; Largest: up to 30,000 code samples and 41,311 refactoring cases
- **Key benchmarks used:** Defects4J, CodeSearchNet, Concode, SWE-bench, DevGPT, Aizu Online Judge, CodeReview/CodeReview-New
- **Data leakage precautions:** 36/50 (72%) made NO mention of data leakage precautions; 14/50 (28%) reported some precautions:
  - Training/testing splits: 6 studies (12%)
  - Unseen projects/repositories: 4 studies (8%)
  - Held-out datasets: 3 studies (6%)
  - Cross-validation: 1 study (2%)
- **Domain:** Academic literature on LLM + code refactoring

### Key Findings

| Finding | Value/Detail |
|---------|-------------|
| **RQ1: Tools used** | External frameworks (iSMELL, EM-Assist, PyCraft, UTRefactor, etc.) combined with LLMs significantly improve performance. iSMELL + LLM achieved 28.7% improvement over standalone LLM. Hybrid rule-based + LLM approaches achieved >90% accuracy (Python). IDE-based filtering eliminated all hallucinations that affected 80% of results. RefactoringMiner was used across multiple studies for dataset generation. EM-Assist improved Recall from 39.4% to 53.4% vs JExtract. |
| **RQ2: Datasets & benchmarks** | 70% sourced from open-source repos. Java dominates (66%), Python second (44%). No standardized benchmark exists. 72% of studies fail to report data leakage precautions. Dataset sizes vary enormously (1 program to 41,311 refactoring cases). |
| **RQ3: Prompt techniques** | 7 categories identified: Zero-Shot (19 studies, 16%), One-Shot (12 studies, 10%), Few-Shot (25 studies, 21%), Chain-of-Thought (18 studies, 15%), Context-Specific (27 studies, 22% -- most common), Output Constraints (15 studies, 12%), Ranking (2 studies, 2%). Best technique is context-dependent. |
| **RQ3: Prompt effectiveness** | One-Shot improved test pass rates by 6.15% over Zero-Shot and reduced code smells 3.52% more. One-Shot yielded highest unit test pass rate of 34.51% and smell reduction of 42.97%. Few-Shot in Python reduced CC by 17.35% and LOC by 25.85%. Context-enhanced UTRefactor reduced test smells from 2,375 to 265 (89% elimination vs 55% for standard LLM). One-Shot in build system refactoring: P/R/F1 of 0.79/0.78/0.76 vs Zero-Shot's 0.67/0.72/0.66. |
| **RQ4: Accuracy** | 22/50 studies reported performance metrics. Accuracy generally >78.61% (one outlier at 58.78%). F1-scores generally >74%. Recall ranged 48%-100% (majority >84.3%). Precision varied (both increases and decreases depending on context). 50/50 (100%) had quantitative analysis; 37/50 (74%) had comparative analysis; 22/50 (44%) had correctness assessment; 13/50 (26%) had qualitative/human feedback. |
| **RQ5: Refactoring types** | Most studied: Extract Method (most widely studied, highest accuracy). Most common code smells: Large Class and Long Method. Refactoring types covered: Rename Method, Extract Method, Extract Class, Simplifying Method, Code Formatting, Split File, Inline Method, JUnit Migration, Move Method, Loop Optimization. Only 1 study at Architecture Level (Pandini et al. on Cyclic Dependencies). Vast majority at Code Level or Design Level. |
| **RQ6: Key challenges** | (1) LLMs generate erroneous code (50% of studies, 25/50): 76.3% of EM-Assist LLM suggestions were hallucinations; Copilot produced code smells in 15% of output; only 28.8% of ChatGPT loop refactorings compilable. (2) LLMs struggle with complex multi-file tasks (44% of studies, 22/50): 45.5% of iteratively refactored methods were non-plausible; performance declines with complexity. (3) LLMs misunderstand developer intent (34% of studies, 17/50): unstructured prompts required avg 13.58 conversational turns; Gemini and Claude achieved only 50% success in detecting bad code. |

### Specific Metrics Reported Across Studies

| Metric/Study | Value |
|-------------|-------|
| Gehring (ChatGPT-3.5 + CoT) | 100% Accuracy (1 project, switch statements) |
| DePalma et al. (ChatGPT) | 96.8% Accuracy |
| Shirafuji et al. (Few-Shot) | 95.68% successful refactoring |
| PyCraft (Few-Shot + CoT) | 96.6% F1-measure |
| UTRefactor (CoT) | 89% smell elimination (2,375 to 265) |
| Zhang et al. (hybrid rule+LLM) | >90% Accuracy and Precision (Python idioms) |
| iSMELL (One-Shot + Context) | 95.14% Accuracy, 95.52% F1, 92.41% Recall |
| HMove (Cui et al.) | 93.3% avg Precision, 85.4% avg Recall, 80.7% avg F1 |
| MoveRec (Zhang et al.) | F1 improved from 9.4% to 53.4% |
| HECS (Cui/Wang et al.) | 76.8% Precision, 84.3% Recall, 80.4% F1 |
| Copilot Chat (Few-Shot + CoT) | 87.1% successful refactoring rate |
| BuildRefMiner (One-Shot) | 76% F1-score |
| MM-Assist (CoT) | 80% Recall@3, 2.4x improvement over SOTA |
| Midolo et al. (ChatGPT loops) | Only 28.8% compilable (71% failed) |
| Wang et al. (CRB tasks) | Only 17.5% and 12.5% Real Change Accuracy |
| Caumartin et al. (CodeLlama) | 77.13 BLEU-T (comparable to ChatGPT's 76.44) |
| Xu et al. (HLSRewriter) | 86.67% refactoring pass rate |
| De Sousa et al. (GPT-4o for PL/SQL) | F1: 79% |
| Amaral (Copilot test smells) | 58.78% successful smell removals |

### Prompt Engineering Breakdown

| Technique | Studies | Percentage | Key Insight |
|-----------|---------|------------|-------------|
| Context-Specific | 27 | 22% | Most commonly used; provides codebase context, usage patterns, quality goals |
| Few-Shot | 25 | 21% | Provides multiple examples; best for Python (reduced CC by 17.35%) |
| Zero-Shot | 19 | 16% | Minimal context; baseline performance |
| Chain-of-Thought | 18 | 15% | Step-by-step reasoning; improves diversity but not always correctness |
| Output Constraints | 15 | 12% | Format/correctness specifications |
| One-Shot | 12 | 10% | Single example; most effective for Java correctness (34.51% test pass) |
| Ranking | 2 | 2% | Multiple versions ranked; least explored |

### Code Smells Addressed (from Table 7)

| Code Smell | # Studies | Notes |
|-----------|-----------|-------|
| Large Class | 15+ | Most frequently mentioned alongside Long Method |
| Long Method | 14+ | Most frequently mentioned alongside Large Class |
| Code Duplication | 11 | |
| Feature Envy | 7 | |
| Poor Naming | 7+ | |
| Switch Statements | 5 | |
| Comments | 3 | |
| Refused Bequest | 2 | |
| Long Parameter List | 2 | |
| Lazy Class | 1 | |
| Data Clumps | 1 | |
| Message Chain | 1 | |
| Linguistic smells | 1 | Specialized for natural language in goals |
| Test code smells | 2 | Eager Test, Duplicate Assert, Assertion Roulette |
| Dockerfile code smells | 1 | Temporary File Smells, Shell/Script Smells |
| Architectural code smells | 1 | Cyclic Dependency, Unstable Dependency, God Component, Hublike Dependency |
| Hardware code smells | 1 | Dynamic pointers, recursion, dynamic memory |
| SQL code smells | 1 | UVP, CDO, IEW, ECB, PMO, USA, CAT, QEH |

### Abstraction Layers

| Layer | Prevalence | Notes |
|-------|-----------|-------|
| Code Level | Majority (~80%+) | Most studies operate here (single file, few lines) |
| Design Level | ~40% of studies | Cross-file, cross-class, cross-module refactoring |
| Architecture Level | 2 studies only | Pandini et al. (Cyclic Dependency via Arcan + LLM); Rajendran et al. (multi-agent conceptual framework) |

### Challenges & Limitations

**Challenges identified across the 50 primary studies (RQ6):**
- **LLMs generate erroneous/unreliable code (50% of studies, 25/50):** 76.3% of EM-Assist suggestions were hallucinations (57.4% syntactically incorrect, 18.9% illogical). Copilot produced code smells in ~15% of generated code. Only 28.8% of ChatGPT for-loop refactorings were compilable. ChatGPT produced buggy code 5-7.2% of the time in Java. F1-scores for detecting some smells dropped as low as 33%. Up to 80% of Move Method LLM recommendations were hallucinations.
- **LLMs struggle with complex multi-file refactoring (44% of studies, 22/50):** Performance degrades with larger codebases and multi-file tasks. 45.5% of iteratively refactored methods were non-plausible. Token limits prevent processing extremely large codebases. LLMs struggle to retain global project context.
- **LLMs misunderstand developer intent (34% of studies, 17/50):** Unstructured prompts required avg 13.58 conversational turns vs 1.45 with structured prompts. ChatGPT frequently fails to detect code smells (unreliable educational tool alone). LLMs focus on individual methods rather than broader project structure. General-purpose models achieved only 50% success in detecting bad code.

**Open issues identified by the authors:**
1. Lack of standardized terminology for refactoring method types
2. Unknown optimal combinations of prompt engineering techniques
3. Unclear which LLMs excel at specific refactoring types
4. Continuous LLM development may invalidate findings (e.g., ChatGPT formatting degradation between versions)
5. Possible language and dataset biases in LLMs (non-English comment deletion: 95.11% to 97.16% English)
6. Ranking prompting technique underexplored (only 2 studies)
7. Evaluation dominated by Java (66%) and Python (44%) -- other languages underrepresented
8. Lack of standardized performance metrics across studies
9. 47% of ChatGPT-generated code has style/maintainability issues despite compiling correctly
10. 74% of studies lack human feedback evaluation
11. Security concerns with proprietary LLMs in industry (data privacy, black-box models)
12. 72% of studies fail to address data leakage prevention

### Key Quotes

> "We found that prompt structure, context of the project, and providing examples can significantly improve the quality of LLM-generated refactorings, mitigating critical concerns such as hallucinations, context loss, and scalability issues."

> "76.3% of LLM suggestions were hallucinations -- 57.4% were syntactically incorrect while 18.9% were illogical (e.g., suggesting to extract an entire method body)."

> "Using Chain-of-Thought, the tool UTRefactor is capable of achieving an 89% reduction of code smells, from 2,375 of the testing data to 265."

> "One study evaluated ChatGPT's ability to refactor for-loops, finding that only 28.8% of its refactored outputs were compilable noting ChatGPT's difficulty handling complex control flows and implicit dependencies."

> "Unstructured developer prompts required an average of 13.58 conversational turns to reach a satisfactory result, indicating a lack of understanding of the developer's intentions in initial prompts."

> "Nearly 47% of ChatGPT-generated code snippets suffer from code style and maintainability issues -- such as having variables that should be private declared as public or using implementation types instead of interface -- despite a majority compiling and running without errors."

### Key Takeaway
This SLR of 50 studies confirms that LLM-based code refactoring is promising but limited to code-level and design-level operations. Architecture-level refactoring is virtually unexplored (only 1 study on architectural smells). Context-Specific and Few-Shot prompting are most effective, structured Chain-of-Thought approaches can achieve up to 89% smell elimination, but LLMs still hallucinate extensively (up to 76% in some studies) and struggle with multi-file reasoning. The thesis on automated architectural tactic implementation fills a well-documented gap: no existing work applies LLMs to systematically implement architectural tactics, and the challenges identified (hallucination, context loss, multi-file complexity) must be mitigated through semantic analysis, structured prompting, and human-in-the-loop validation.

### Snowball References
**Backward (key references cited):**
- `fowler2018refactoring` -- Refactoring: Improving the Design of Existing Code (foundational)
- `alomar2021preserving` -- On Preserving the Behavior in Software Refactoring (behavior preservation mapping)
- `baqais2020automatic` -- Automatic Software Refactoring: A Systematic Literature Review (predecessor SLR, 41 studies)
- `alomar2024extract` -- Behind the Intent of Extract Method Refactoring (Extract Method SLR, 83 studies)
- `hou2024llmse` -- Large Language Models for Software Engineering: SLR (395 papers, 70+ LLMs)
- `he2025llmagents` -- LLM-based Multi-Agent Systems for Software Development (71 papers)
- `sallou2024breaking` -- Breaking the Silence: Threats of Using LLMs in SE (data leakage threats)
- `depalma2024exploring` -- Exploring ChatGPT's Code Refactoring Capabilities (primary study)
- `liu2025exploring` -- Exploring the Potential of General Purpose LLMs in Automated Software Refactoring (primary study)
- `pomian2024emassist` -- EM-Assist: Safe Automated Extract Method Refactoring with LLMs (primary study)
- `gao2025utrefactor` -- Automated Unit Test Refactoring (primary study, 89% smell reduction)
- `pandini2025architectural` -- Exploratory Study on Architectural Smell Refactoring Using LLMs (only architecture-level study)
- `rajendran2025multiagent` -- Multi-Agent LLM Environment for Software Design and Refactoring (conceptual framework)
**Forward:** Recently published (Feb 2026 preprint) -- forward citations still accumulating
