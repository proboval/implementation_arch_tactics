# Motivation and Context

> **Learning objectives.** After reading this chapter you should be able to (1) explain why software maintenance dominates lifecycle costs, (2) identify the knowledge barriers that prevent developers from applying architectural tactics, (3) articulate the promise --- and the current limits --- of using LLMs for architecture-level code improvement, and (4) describe the scope and structure of this study guide.

---

## 1.1 The Software Maintenance Crisis

Software is not built once and forgotten. The overwhelming majority of a system's total cost of ownership is spent not on initial development but on understanding, modifying, extending, and fixing the code that already exists. Industry data consistently places maintenance at **60--80% of total lifecycle costs** [@bass2021software]. Martin Fowler goes further, estimating that up to **75% of development effort** is consumed by refactoring --- the restructuring of existing code to improve its internal quality without changing its external behavior [@fowler2018refactoring].

Why is maintenance so expensive? The root cause is seldom the individual line of code. Instead, it is the *decisions made at the architectural level* --- the choice of decomposition strategy, the way modules communicate, the degree to which responsibilities are encapsulated --- that determine how easily (or painfully) a system can absorb future changes. Garlan and Perry captured this insight in a memorable metaphor:

> "Software architecture can expose the dimensions along which a system is expected to evolve. By making explicit the **load-bearing walls** of a system, system maintainers can better understand the ramifications of changes, and thereby more accurately estimate costs of modifications." [@garlan1995editorial]

Just as removing a load-bearing wall in a building risks structural collapse, modifying a core architectural decision in software can trigger cascading changes across dozens of files, modules, or services. Conversely, a well-chosen architecture confines the blast radius of change. The maintenance crisis, then, is fundamentally an *architecture* crisis.

| Cost factor | Typical range | Source |
|-------------|--------------|--------|
| Maintenance share of total lifecycle cost | 60--80% | [@bass2021software] |
| Development effort spent on refactoring | up to 75% | [@fowler2018refactoring] |
| Practitioners reporting quality degradation from architecture erosion | 83.8% | [@li2021understanding] |

## 1.2 The Knowledge Barrier

If good architectural decisions are the key to maintainability, why do so many systems end up poorly structured? The answer lies in a persistent knowledge barrier that separates *knowing what to do* from *knowing how to do it in code*.

### Cross-cutting tactics require deep framework knowledge

Architectural tactics --- the fine-grained design decisions that target a single quality attribute [@bass2021software] --- are conceptually straightforward. "Use an intermediary to decouple producers from consumers" is easy to state. But *implementing* that tactic in a real codebase often requires touching multiple files, understanding framework-specific APIs, and coordinating changes across method boundaries. Shokri et al. demonstrated this concretely: implementing a JAAS authentication tactic (a security tactic) requires inter-procedural changes spanning multiple classes and packages, with API calls that must be placed in precisely the right locations [@shokri2024ipsynth]. When they tested ChatGPT on this task, the LLM produced syntactically correct code 95% of the time --- but only **5% of implementations were semantically correct**, because the model failed to coordinate changes across methods and classes.

### Novice developers produce measurably worse code

The knowledge barrier is especially acute for less experienced developers. Haindl and Weinberger conducted a controlled experiment comparing code written by novice programmers with and without ChatGPT assistance. The ChatGPT-assisted group produced code with significantly lower cyclomatic complexity and fewer coding convention violations (p < 0.005) [@haindl2024chatgpt]. This is encouraging at the code level, but it also reveals a gap: current LLM tools help with *local* code quality (naming, complexity, style) but do not address *architectural* quality (module boundaries, coupling patterns, tactic implementation).

### Architecture erosion: the silent degradation

Even when systems start with a well-designed architecture, implementations gradually diverge from the intended design --- a phenomenon formally described by Perry and Wolf as **architectural erosion** (violations of architecture leading to brittleness) and **architectural drift** (insensitivity to architecture leading to loss of coherence) [@perry1992foundations].

Li et al. conducted a systematic mapping study of 73 studies on architecture erosion and found that **83.8% of practitioners report quality degradation** as a direct consequence [@li2021understanding]. The top technical causes include architecture violations (24.7%), evolution issues (23.3%), and technical debt (17.8%). Critically, technical debt forms a *vicious cycle* with erosion: it is both a cause and a consequence.

Rosik et al. provided striking empirical evidence in a 2-year longitudinal case study at IBM: architectural drift occurred even during initial de novo implementation, even when the architect was also the sole developer [@rosik2011assessing]. More troublingly, **identifying drift did not lead to its removal** --- developers tolerated violations because fixing them risked ripple effects, consumed time, and entangled legacy code. Detection alone is not enough; developers need low-cost, low-risk *remediation* paths.

| Barrier | Evidence | Source |
|---------|----------|--------|
| Cross-cutting tactic implementation requires inter-procedural coordination | ChatGPT: 95% syntax-correct but only 5% semantically correct on tactic synthesis | [@shokri2024ipsynth] |
| Novice developers produce higher-complexity code | Controlled study: ChatGPT reduces cyclomatic and cognitive complexity (p < 0.005) | [@haindl2024chatgpt] |
| Architecture erosion degrades quality | 83.8% of practitioners report quality degradation | [@li2021understanding] |
| Drift occurs even with a single architect-developer | 9 divergent edges found in 2-year IBM case study | [@rosik2011assessing] |
| Detection does not equal remediation | Zero identified inconsistencies were removed by developers | [@rosik2011assessing] |

## 1.3 The Promise of LLMs

Large language models have demonstrated remarkable ability to understand and transform source code. In the domain of refactoring --- the restructuring of code to improve quality without changing behavior --- recent results are striking:

- **MANTRA** [@xu2025mantra], a multi-agent LLM framework, achieved an **82.8% success rate** (582 out of 703 cases) in producing compilable, test-passing refactored Java code across six refactoring types. A baseline single-prompt LLM achieved only 8.7%.
- A user study with 37 developers found MANTRA-generated code *comparable to human-written code* in readability (4.15 vs. 4.02) and reusability (4.13 vs. 3.97), with no statistically significant difference.
- The ablation study revealed that the **Reviewer Agent** --- which uses traditional SE tools (RefactoringMiner, CheckStyle) to provide structured feedback --- was the most critical component, contributing a 61.9% improvement. This suggests that combining LLMs with static analysis verification is more effective than using LLMs alone.

These results establish a crucial precedent: LLMs can perform code-level transformations reliably, *provided* they operate within a structured pipeline that includes external verification. But current tools operate almost exclusively at the **code level** --- extracting methods, inlining variables, moving classes. They do not reason about **architecture-level** concerns: module boundaries, coupling patterns, quality attribute trade-offs, or the systematic application of architectural tactics.

This is the gap that motivates the present work. Can LLMs bridge the distance between *design intent* (an architectural tactic specification) and *code implementation* (the actual changes across files, classes, and methods)? Can we build a pipeline that takes a tactic like "Use an Intermediary" and automatically produces the correct multi-file transformation in a real codebase --- while preserving behavior, respecting existing architecture, and improving measurable maintainability?

## 1.4 A Motivating Example

Consider a Python web service for an e-commerce platform. The service handles product catalog queries, and every endpoint directly queries the database:

```python
# routes/products.py
from db import get_connection

def get_product(product_id):
    conn = get_connection()
    result = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    return result.fetchone()

def get_products_by_category(category_id):
    conn = get_connection()
    result = conn.execute(
        "SELECT * FROM products WHERE category_id = ?", (category_id,)
    )
    return result.fetchall()
```

```python
# routes/orders.py
from db import get_connection

def get_order_products(order_id):
    conn = get_connection()
    result = conn.execute(
        "SELECT p.* FROM products p JOIN order_items oi ON p.id = oi.product_id "
        "WHERE oi.order_id = ?", (order_id,)
    )
    return result.fetchall()
```

```python
# routes/recommendations.py
from db import get_connection

def get_similar_products(product_id):
    conn = get_connection()
    # Complex query: get products in same category, ordered by popularity
    result = conn.execute(
        "SELECT p.* FROM products p WHERE p.category_id = "
        "(SELECT category_id FROM products WHERE id = ?) "
        "ORDER BY p.view_count DESC LIMIT 10", (product_id,)
    )
    return result.fetchall()
```

Now a change request arrives: **"Add caching to reduce database load for product queries."**

In the current architecture, every module that touches product data has its own direct database call. Implementing caching requires modifying *every call site* --- potentially **15 or more files** across routes, background workers, admin endpoints, and test fixtures. Each modification risks inconsistency: one file might cache with a 5-minute TTL, another with 10 minutes, and a third might forget caching entirely.

**Applying the "Use an Intermediary" tactic** transforms this situation. We introduce a single `ProductRepository` that encapsulates all product data access and add caching at that layer:

```python
# repositories/product_repository.py
from db import get_connection
from cache import cache

class ProductRepository:
    @cache(ttl=300)
    def get_by_id(self, product_id):
        conn = get_connection()
        result = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return result.fetchone()

    @cache(ttl=300)
    def get_by_category(self, category_id):
        conn = get_connection()
        result = conn.execute(
            "SELECT * FROM products WHERE category_id = ?", (category_id,)
        )
        return result.fetchall()

    @cache(ttl=600)
    def get_similar(self, product_id):
        conn = get_connection()
        result = conn.execute(
            "SELECT p.* FROM products p WHERE p.category_id = "
            "(SELECT category_id FROM products WHERE id = ?) "
            "ORDER BY p.view_count DESC LIMIT 10", (product_id,)
        )
        return result.fetchall()
```

```python
# routes/products.py  (after tactic application)
from repositories.product_repository import ProductRepository

repo = ProductRepository()

def get_product(product_id):
    return repo.get_by_id(product_id)

def get_products_by_category(category_id):
    return repo.get_by_category(category_id)
```

The caching change now lives in **2--3 files** (the repository and the cache configuration) instead of 15. Future changes to data access --- switching databases, adding query logging, implementing read replicas --- similarly require modification in one place. The architectural tactic has reduced the *coupling* between route handlers and the database, *increased the cohesion* of data-access logic, and made the system dramatically more maintainable.

This is exactly the kind of transformation that a well-designed LLM pipeline could automate: detect the scattered database access pattern, select the "Use an Intermediary" tactic, generate the repository class, and rewrite the call sites --- all while ensuring the tests still pass.

## 1.5 Guide Roadmap

This study guide is organized as follows:

| Chapter | Title | What you will learn |
|---------|-------|---------------------|
| 1 | Motivation and Context | Why maintenance is expensive, the knowledge barrier, and the LLM opportunity |
| 2 | Software Architecture Foundations | Definitions (Perry & Wolf, Garlan & Shaw), architectural styles, design rationale |
| 3 | Quality and Maintainability | ISO/IEC 25010, sub-characteristics (modularity, analysability, modifiability, testability), quality models |
| 4 | Architectural Tactics | Tactic taxonomy (Bass et al.), modifiability tactics catalog, tactics vs. patterns |
| 5 | Architecture Erosion and Drift | Definitions, symptoms, causes, consequences, detection approaches |
| 6 | Maintainability Assessment Methods | Static analysis metrics (CC, MI, Halstead), tools (Radon, SonarQube), tool agreement |
| 7 | LLMs for Code Refactoring | Current capabilities, agentic frameworks, multi-agent pipelines, behavior preservation |
| 8 | Open Challenges | Inter-procedural synthesis, architecture awareness, evaluation methodology |
| 9 | Research Gaps and Thesis Scope | What remains unsolved and how this thesis addresses it |

Each chapter builds on the previous ones. By the end, you will have a comprehensive understanding of the theoretical foundations, practical tools, and open research questions surrounding the automated implementation of architectural tactics for software quality improvement.
