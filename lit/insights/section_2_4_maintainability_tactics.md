## Topic: Maintainability Tactics Catalog (Section 2.4)

**Papers:** 5 | **Updated:** 2026-02-16

### Summary

The architectural tactics catalog for maintainability is anchored in Bass, Clements, and Kazman's definitive taxonomy of 15 modifiability tactics organized into three categories: Increase Cohesion (5 tactics localizing changes), Reduce Coupling (4 tactics preventing ripple effects), and Defer Binding Time (6 tactics increasing runtime flexibility). This taxonomy, first introduced in the 2003 edition and refined through the 4th edition (2021), treats tactics as fine-grained "building blocks" that target a single quality attribute response -- distinguishing them from coarse-grained architectural patterns, which package multiple tactics and embed tradeoff decisions. Kim et al. (2009) formalize this distinction by representing tactics as feature models with explicit variability relationships (mandatory, optional, requires, suggested, mutually exclusive) and providing structural/behavioral specifications via RBML, establishing that tactics are composable primitives whose interactions must be explicitly managed. Harrison and Avgeriou (2010) extend this understanding by modeling how tactics structurally and behaviorally modify architecture patterns, identifying five types of impact (Implemented-in, Replicates, Add-in-pattern, Add-out-of-pattern, Modify) with a five-point compatibility scale ranging from Good Fit (++) to Poor Fit (--).

Bogner, Wagner, and Zimmermann (2019) operationalize the Bass taxonomy for service-oriented and microservice architectures, systematically mapping all 15 modifiability tactics onto SOA and Microservices principles and design patterns. Their analysis reveals that "Reduce Coupling" dominates principle-level mappings in both architectural styles (16 SOA mappings, 7 Microservices mappings), while at the pattern level, SOA relies heavily on intermediary patterns (Service Facade, Service Broker) and Microservices on runtime discovery and infrastructure automation patterns. Rahmati and Tanhaei (2021) complement this tactic-focused view by providing a pattern-level maintainability assessment framework: their six-sub-attribute quality model (analyzability, changeability, stability, testability, understandability, portability) with hexagonal radar diagrams scores standard architectural patterns on a 0-4 scale per sub-attribute. Critically, Rahmati's changeability factors -- localized modification, reduced coupling, and deferred binding time -- map directly onto Bass's three tactic categories, establishing that the tactic taxonomy and the pattern-level quality model describe the same maintainability concerns at different levels of granularity.

For the thesis, these five papers converge on a clear methodology: (1) use Bass's 15-tactic catalog as the primary selection menu, (2) filter tactics through Harrison's pattern-tactic compatibility model to identify which tactics are structurally feasible for the target architecture, (3) consult Bogner's service-pattern mappings to identify concrete implementation blueprints, and (4) use Rahmati's radar model to predict which maintainability sub-attributes will improve. The thesis focuses on modifiability tactics specifically because they are the most directly measurable through static analysis (coupling metrics, cohesion metrics, module size), the most structurally concrete (unlike performance or availability tactics which often require runtime infrastructure), and the most amenable to LLM-driven code transformation (they involve refactoring module boundaries, interfaces, and dependencies -- operations within the LLM's demonstrated capabilities).

### Modifiability Tactics Catalog (Bass 2021)

#### Category 1: Increase Cohesion
| Tactic | Description | ISO 25010 Sub-char |
|--------|-------------|-------------------|
| Increase Semantic Coherence | Ensure module responsibilities are related and unified; each module should have a single, well-defined purpose | Modularity, Analysability |
| Anticipate Expected Changes | Organize modules so that likely changes affect a limited number of modules; isolate volatility behind stable interfaces | Modifiability |
| Split Module | Break a module with multiple responsibilities into smaller, focused pieces; decompose large components into single-responsibility units | Modularity, Modifiability |
| Generalize Module | Make a module generic via parameters or broad interfaces so it can handle a wider range of inputs without modification | Reusability, Modifiability |
| Abstract Common Functionality | Move common logic to a shared entity (base class, utility module) to avoid duplication and ensure single-point-of-change | Modularity, Reusability |

#### Category 2: Reduce Coupling
| Tactic | Description | ISO 25010 Sub-char |
|--------|-------------|-------------------|
| Use Encapsulation | Hide implementation details behind a stable interface; changes to internals do not propagate to dependents | Modularity, Modifiability |
| Maintain Existing Interface | Use versioning, adapters, or deprecation strategies to evolve interfaces without breaking existing consumers | Modifiability, Analysability |
| Restrict Dependencies | Limit which modules can communicate; enforce dependency rules (e.g., layering constraints, acyclic dependency principle) | Modularity, Testability |
| Use an Intermediary | Introduce an indirection layer (broker, facade, mediator, proxy) to decouple producers from consumers | Modularity, Modifiability |

#### Category 3: Defer Binding Time
| Tactic | Description | ISO 25010 Sub-char |
|--------|-------------|-------------------|
| Runtime Registration & Dynamic Lookup | Services discover and connect to each other at runtime via registries or naming services | Modifiability, Reusability |
| Runtime Binding | Late binding, reflection, or dynamic dispatch to change behavior without recompilation | Modifiability |
| Publish-Subscribe | Decouple event producers from consumers via an event bus or notification mechanism | Modularity, Modifiability |
| Start-Up Time Binding | External configuration files loaded at system start determine behavior (e.g., feature flags, DB connection strings) | Modifiability, Analysability |
| Deployment Time Binding | Binding decisions made at installation or deployment (e.g., selecting a database driver, configuring service endpoints) | Modifiability |
| Compile Time Binding | Traditional build-time binding through static imports, generics, or preprocessor directives | (Baseline -- least flexible) |

### Microservice Modifiability Tactics (Bogner 2019)

| Tactic | Category | Service Pattern(s) |
|--------|----------|-------------------|
| Use an Intermediary | Reduce Coupling | Service Facade, Proxy Capability, Service Broker, API Gateway (9 SOA patterns total -- highest SOA coverage) |
| Runtime Registration & Dynamic Lookup | Defer Binding | Self Registration, Client-side Discovery, Server-side Discovery, Service Registry, 3rd Party Registration (5 Microservices patterns -- highest MS coverage) |
| Use Encapsulation | Reduce Coupling | Service Encapsulation, Entity Abstraction, Database per Service |
| Publish-Subscribe | Defer Binding | Event Sourcing, Domain Event, Messaging (Async) |
| Split Module | Increase Cohesion | Decompose by Business Capability, Decompose by Subdomain, Strangler Fig |
| Restrict Dependencies | Reduce Coupling | Service Autonomy, Service Statelessness, Bulkhead |
| Generalize Module | Increase Cohesion | Canonical Schema, Canonical Protocol |
| Maintain Existing Interface | Reduce Coupling | Compatible Change, Tolerant Reader, Consumer-Driven Contract |
| Compile Time Binding | Defer Binding | (No pattern in either SOA or MS catalogs -- the only tactic with zero mappings) |

**Key finding:** Reduce Coupling dominates SOA principle mappings (16/26), while Defer Binding Time dominates Microservices pattern mappings (11/21, ~52%). SOA achieves modifiability through governance, standardization, and intermediaries; Microservices through evolutionary design, infrastructure automation, and runtime discovery.

**Gap identified:** Only 3 of 21 mapped Microservices patterns fall under "Increase Cohesion" despite small, cohesive services being a core Microservices philosophy. This cohesion gap represents an area where LLM-driven tactic implementation could add particular value.

### Pattern-Tactic Mapping (Rahmati 2021)

| Pattern | Tactics Enabled | Maintainability Impact |
|---------|----------------|----------------------|
| Multi-Layered | Restrict Dependencies, Use Encapsulation, Anticipate Expected Changes | Testability: 4, Changeability: 4, Portability: 4, Stability: 3, Analyzability: 3 -- highest overall maintainability |
| Broker | Use an Intermediary, Use Encapsulation, Runtime Registration | Testability: 4, Changeability: 4, Analyzability: 4 -- strong for service-oriented systems |
| MVC | Split Module, Use Encapsulation, Restrict Dependencies | Testability: 4, Changeability: 4, Understandability: 3, Portability: 4 -- best for web applications |
| Pipe & Filter | Split Module, Generalize Module, Restrict Dependencies | Changeability: 4 (highest), but Testability: 1, Understandability: 0, Analyzability: 0 -- narrow benefit |
| Blackboard | Abstract Common Functionality | Changeability: high, but very low testability, understandability, analyzability -- worst overall maintainability |
| Object-Oriented | Use Encapsulation, Increase Semantic Coherence | Balanced mid-range scores across sub-attributes |
| Repository | Abstract Common Functionality, Use an Intermediary | Good analyzability and stability; moderate changeability |

**Critical insight from case studies:**
- Successful refactoring (Proxy to MVC): 50-64% maintenance effort reduction
- Failed refactoring (flat PHP to MVC): ~10% effort increase
- Conclusion: Architecture-level refactoring is "preventing rather than preserving" -- patterns prevent maintainability problems but cannot guarantee maintainability is not violated at lower levels. LLM-driven implementation must ensure correct lower-level realization, not just structural conformance.

### Key Papers

| Paper | Contribution | Relevance |
|-------|--------------|-----------|
| `bass2021software` | Canonical 15-tactic modifiability taxonomy (5 cohesion + 4 coupling + 6 binding); definitive tactic vs. pattern distinction; ATAM validation method | CRITICAL -- primary tactic catalog for thesis |
| `bogner2019modifiability` | Systematic mapping of 15 tactics to SOA/Microservices principles and patterns; identifies which service patterns realize which tactics; public dataset (GitHub: xjreb/research-modifiability-tactics) | HIGH -- provides concrete implementation blueprints for tactics in service-based systems |
| `rahmati2021ensuring` | Six-sub-attribute maintainability quality model with hexagonal radar diagrams; pattern-to-sub-attribute scoring (0-4 scale); two case studies showing 50-64% improvement vs. 10% degradation | HIGH -- provides maintainability prediction framework for pattern selection |
| `kim2009qualitydriven` | Formal tactic specification via feature models + RBML; explicit variability relationships (requires, suggested, mutually exclusive); automated architecture instantiation prototype (RBML-PI) | HIGH -- establishes that tactics have formal composability rules the LLM must respect |
| `harrison2010how` | Pattern-tactic interaction taxonomy (5 structural change types); five-point impact magnitude scale (Good Fit ++ to Poor Fit --); architecture drift warning from out-of-pattern additions | HIGH -- provides compatibility assessment framework for tactic-in-pattern feasibility |

### Consensus

| Finding | Papers | Confidence |
|---------|--------|------------|
| 15 modifiability tactics in 3 categories form a stable, reusable catalog | `bass2021software`, `bogner2019modifiability`, `harrison2010how`, `kim2009qualitydriven` | High -- consistent taxonomy across all four papers spanning 2003-2021 |
| Tactics are composable building blocks distinct from patterns | `bass2021software`, `kim2009qualitydriven`, `harrison2010how` | High -- formal distinction with feature models, RBML specs, and interaction taxonomy |
| Reduce Coupling tactics have broadest applicability across architectures | `bogner2019modifiability`, `rahmati2021ensuring`, `bass2021software` | High -- dominant category in both SOA (49% of patterns) and monolithic (highest radar scores) |
| Pattern-tactic compatibility varies widely; some combinations cause architecture drift | `harrison2010how`, `rahmati2021ensuring` | High -- both provide evidence of degradation from poor pattern-tactic matching |
| Architecture-level refactoring can improve maintainability 50-64% but is not universally beneficial | `rahmati2021ensuring`, `harrison2010how` | Medium -- limited to 2-3 case studies; no large-scale empirical validation |
| Tactic implementation order matters; prior tactics change feasibility of subsequent ones | `harrison2010how`, `kim2009qualitydriven` | Medium -- observed in case studies; not quantified systematically |
| Increase Cohesion tactics are underrepresented in modern service patterns despite being foundational | `bogner2019modifiability` | Medium -- single study; the gap may reflect implicit cohesion in microservice decomposition |

### Thesis Tactic Selection

| Selected Tactic | Rationale | Measurable By |
|----------------|-----------|---------------|
| **Split Module** (Cohesion) | Most directly implementable by LLM: extracting classes/functions into separate modules is a well-understood refactoring operation (Extract Class, Extract Method). Maps to Radon's per-module complexity and lines-of-code metrics. Harrison rates it as Good Fit for Layered and MVC patterns. | Radon: per-module CC reduction, LOC reduction, module count increase; SonarQube: reduced file complexity |
| **Abstract Common Functionality** (Cohesion) | LLM can identify duplicated code across modules and extract shared utilities/base classes. Directly reduces code duplication -- measurable by clone detection and DRY violation metrics. | Radon: reduced total LOC; duplicate code ratio; cohesion metrics (LCOM) |
| **Increase Semantic Coherence** (Cohesion) | LLM can analyze module contents and recommend reorganization by responsibility. Measurable through cohesion metrics and coupling analysis. Aligns with Single Responsibility Principle. | LCOM (Lack of Cohesion of Methods); Radon MI per module; responsibility distribution analysis |
| **Use Encapsulation** (Coupling) | LLM can identify public internals that should be private/protected and introduce proper interfaces. Directly reduces afferent/efferent coupling. Rated Good Fit for all common patterns. | Coupling metrics (Ca, Ce, instability); public API surface reduction; Radon MI |
| **Restrict Dependencies** (Coupling) | LLM can analyze import graphs and enforce layering rules by introducing proper interfaces or removing circular dependencies. Measurable through dependency structure matrices. | Circular dependency count; import graph depth; dependency violation count; afferent/efferent coupling |
| **Use an Intermediary** (Coupling) | LLM can introduce facade, adapter, or mediator patterns to decouple tightly coupled components. Bogner shows this tactic has the most SOA pattern implementations (9 patterns). Requires more structural change but is well-defined. | Coupling between objects (CBO); fan-in/fan-out metrics; intermediary component count |
| **Publish-Subscribe** (Binding) | LLM can refactor direct method calls into event-based communication. Well-defined pattern with clear implementation templates. Measurable through coupling reduction. | CBO reduction; direct dependency count; event channel count |
| **Start-Up Time Binding** (Binding) | LLM can extract hardcoded configuration values into external configuration files. Simple, well-understood refactoring with clear before/after measurement. | Hardcoded value count; configuration externalization ratio; Radon CC for config-heavy functions |

**Excluded tactics with justification:**

| Excluded Tactic | Reason for Exclusion |
|----------------|---------------------|
| Anticipate Expected Changes | Requires domain knowledge about future change scenarios that an LLM cannot reliably predict from code alone |
| Generalize Module | Risk of over-engineering; difficult to verify that generalization is appropriate without usage context |
| Maintain Existing Interface | Relevant primarily during API evolution, not single-snapshot refactoring; difficult to evaluate in static analysis |
| Runtime Registration & Dynamic Lookup | Requires runtime infrastructure (service registry); not a code-level refactoring an LLM can perform in isolation |
| Runtime Binding | Requires reflection/dynamic dispatch infrastructure; high risk of introducing runtime errors |
| Deployment Time Binding | Infrastructure-level concern, not amenable to source code transformation |
| Compile Time Binding | Baseline binding strategy; does not improve modifiability |

### Gaps

| Gap | Impact on Thesis |
|-----|-----------------|
| No empirical study has measured the effect of individual tactics on static analysis metrics (Radon MI, CC, coupling) in isolation | Thesis must establish this mapping experimentally -- a novel contribution. Each tactic implementation should be measured independently before combining. |
| Kim's formal tactic specifications (RBML) cover availability, performance, and security but NOT modifiability | Thesis cannot directly reuse RBML specs for modifiability tactics; must define its own structural templates for LLM prompts. The feature model relationship types (requires, suggested, mutually exclusive) are still applicable. |
| Bogner's SOA/Microservices mapping is qualitative with no strength quantification | Thesis should not assume all tactic-pattern mappings are equally strong; LLM implementation success may vary by mapping strength. |
| Harrison's pattern-tactic interaction model covers only reliability tactics in detail | Thesis must extend the interaction analysis to modifiability tactics for the target patterns (Layered, MVC, Repository). This is a potential contribution. |
| Rahmati's radar diagram scoring is based on expert judgment, not empirical measurement | Thesis should validate radar predictions against actual static analysis measurements after tactic implementation. Discrepancies would be a finding. |
| No study examines LLM capability to implement specific modifiability tactics | This is the core thesis gap. All five papers predate practical LLM-driven code transformation. The thesis is novel in combining the tactic catalog with LLM implementation capability. |
| Interaction effects between simultaneously implemented tactics are not well understood | Kim identifies pairwise composition rules, but no study addresses what happens when an LLM implements 3+ tactics on the same codebase. The thesis should implement tactics incrementally and measure after each. |

### Recommendations

**Adopt:**
- Bass's 15-tactic modifiability taxonomy as the canonical catalog for thesis tactic selection -- it is the most widely cited and consistently used across all five papers.
- Harrison's five-type structural change taxonomy (Implemented-in through Modify) for classifying the difficulty of each LLM tactic implementation and predicting architecture drift risk.
- Rahmati's six maintainability sub-attributes (analyzability, changeability, stability, testability, understandability, portability) as the evaluation framework for assessing pre/post tactic implementation.
- Bogner's public dataset (xjreb/research-modifiability-tactics) as a reference for mapping tactics to service-oriented patterns.

**Adapt:**
- Kim's feature model approach for representing tactic relationships: instead of formal RBML specifications (which are unavailable for modifiability), encode tactic prerequisites and conflicts as structured metadata in the LLM prompt chain (e.g., "Split Module" requires identifying multi-responsibility modules first; "Use an Intermediary" suggests prior "Use Encapsulation").
- Rahmati's hexagonal radar for quantitative validation: replace subjective 0-4 expert scoring with actual static analysis metric deltas (Radon MI, CC, coupling metrics) measured before and after LLM tactic implementation. This transforms a qualitative tool into a quantitative one.
- Harrison's impact magnitude scale: translate the five-point qualitative scale into measurable thresholds (e.g., Good Fit = <5% structural change in AST; Poor Fit = >30% structural change) to evaluate LLM output quality.

**Avoid:**
- Attempting all 15 tactics: focus on the 8 selected tactics that are (a) implementable through source code transformation, (b) measurable by static analysis, and (c) within demonstrated LLM refactoring capabilities. The excluded 7 tactics require runtime infrastructure, domain knowledge, or deployment-level changes beyond the thesis scope.
- Implementing tactics without pattern awareness: Harrison's case studies show that adding components "out of pattern" causes architecture drift. The LLM pipeline must detect the target system's pattern first and select tactics rated Good Fit or Minor Changes for that pattern.
- Relying on a single case study for validation: Rahmati's failed case study (10% degradation) demonstrates that architecture-level refactoring is context-dependent. The thesis should use multiple target systems of varying complexity and architecture styles.

### Related Work Draft

> Architectural tactics for modifiability were first systematically cataloged by Bass, Clements, and Kazman, who define 15 tactics organized into three categories: Increase Cohesion (5 tactics that localize changes within modules), Reduce Coupling (4 tactics that prevent change propagation across module boundaries), and Defer Binding Time (6 tactics that increase runtime flexibility by postponing binding decisions). This taxonomy has remained stable across four editions of *Software Architecture in Practice* and serves as the canonical reference for quality-driven architecture design. Kim et al. formalized tactics as feature models with explicit variability relationships (mandatory, optional, requires, suggested, mutually exclusive) and provided structural specifications using the Role-Based Metamodeling Language (RBML), establishing that tactics are composable building blocks whose interactions must be explicitly managed during architecture design. However, their formalization covers availability, performance, and security tactics; modifiability tactics remain without formal structural specifications.
>
> The relationship between tactics and architectural patterns has been studied from two complementary perspectives. Harrison and Avgeriou developed a model categorizing five types of structural changes that tactics impose on pattern participants (Implemented-in, Replicates, Add-in-pattern, Add-out-of-pattern, Modify) with a five-point impact magnitude scale, demonstrating that pattern-tactic compatibility varies widely and that implementing tactics "out of pattern" can trigger architecture drift with cascading maintainability consequences. Bogner, Wagner, and Zimmermann extended this analysis to service-oriented and microservice architectures, mapping all 15 modifiability tactics onto SOA and Microservices principles and design patterns. Their analysis found that Reduce Coupling tactics dominate SOA implementations (49% of mapped patterns), while Defer Binding Time tactics dominate Microservices implementations (52% of mapped patterns), reflecting the different modifiability strategies of the two architectural styles.
>
> At the pattern level, Rahmati and Tanhaei proposed a maintainability quality model decomposing maintainability into six sub-attributes (analyzability, changeability, stability, testability, understandability, portability) and evaluated standard architectural patterns using hexagonal radar diagrams scored on a 0-4 scale. Their case studies demonstrated that architecture-level refactoring can reduce maintenance effort by 50-64% when the target pattern is well-matched, but can increase effort by 10% when applied inappropriately, confirming that tactics and patterns are "preventing rather than preserving" for maintainability. For this thesis, we select eight modifiability tactics from Bass's catalog -- Split Module, Abstract Common Functionality, Increase Semantic Coherence, Use Encapsulation, Restrict Dependencies, Use an Intermediary, Publish-Subscribe, and Start-Up Time Binding -- based on three criteria: (1) implementability through source code transformation by an LLM, (2) measurability through static analysis metrics (cyclomatic complexity, coupling, cohesion, Maintainability Index), and (3) structural compatibility with common backend architecture patterns as assessed by Harrison's impact model.
