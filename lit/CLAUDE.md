# Literature Review — Architectural Tactics & Maintainability with LLMs

## DO NOT READ PDFs DIRECTLY

**NEVER use the Read tool on `.pdf` files.** Always convert to Markdown first, then analyse the converted version:

```bash
# Convert PDF to Markdown
python -m markitdown lit/pdfs/paper.pdf > lit/converted/paper.md

# Then read and analyse the .md file
```

Alternative: use MCP `read_*_paper` tools (e.g., `read_arxiv_paper`, `read_semantic_paper`) which extract text automatically.

---

## Starting This Workflow

Tell Claude: `"Lit review for [topic]. Working dir: lit/"`

## Resuming After Chat Break

1. Read `lit/status.md` to see progress
2. Read `lit/readings.md` for prioritized reading list
3. Read `lit/insights/*.md` if they exist (synthesis state)
4. Tell Claude: `"Resume lit review from Phase N. Status: lit/status.md"`

---

## Thesis Context

**Title:** Automated Implementation of Architectural Tactics for Software Quality Improvement
**Institution:** Innopolis University (2026)

### Research Objectives

| # | Objective | Focus |
|---|-----------|-------|
| **O1** | Identify architectural tactics that directly influence maintainability as defined by ISO/IEC 25010 | Tactic catalog, quality attribute mapping |
| **O2** | Implement selected tactics in existing open-source backend projects using LLM | LLM-driven code transformation, architectural refactoring |
| **O3** | Evaluate impact of LLM-generated architectural changes on maintainability | Static analysis, architecture metrics, erosion indicators |
| **O4** | Compare maintainability before and after LLM transformations | Before/after metric comparison, Maintainability Index |
| **O5** | Evaluate advantages and limitations of LLM for architecture-level modifications | Consistency, correctness, behavior preservation |
| **O6** | Formulate recommendations for applying architectural tactics using LLM | Guidelines, best practices for real-world backend systems |

### Literature Review Sections (Chapter 2)

| Section | Topic | Key Concerns |
|---------|-------|--------------|
| 2.1 | Software Architecture Foundations | Architectural styles, Pipes-and-Filters, Layered, design rationale |
| 2.2 | Maintainability Foundations | ISO/IEC 25010, modularity, analysability, modifiability, testability |
| 2.3 | Pattern–Tactic Interaction | Tactic classification, architecture erosion, drift, quality-driven design |
| 2.4 | Maintainability Tactics | Modularity tactics, testability tactics, coupling reduction, erosion mitigation |
| 2.5 | Maintainability Assessment Methods | Static analysis tools, metric frameworks, tool agreement |
| 2.6 | LLMs for Code Refactoring | LLM-based refactoring, behavior preservation, readability improvement |

---

## Research Area Hierarchy

### Level 1 — Foundational (seminal works, established methods)

| Sub-topic | Key Paper | Status |
|-----------|-----------|--------|
| Software architecture | `garlan1993introduction` — An Introduction to Software Architecture | ✅ have |
| Architecture foundations | `perry1992foundations` — Foundations for the Study of Software Architecture | ✅ have |
| Quality model | `ISO25010` — ISO/IEC 25010 Product Quality Model | ✅ have |
| Maintainability evolution | `molnar2020study` — Maintainability in Evolving Open-Source Software | ✅ have |
| Quality-driven architecture | `kim2009qualitydriven` — Quality-Driven Architecture Using Tactics | ✅ have |

### Level 2 — Intersection (tactics + architecture + quality)

| Sub-topic | Key Paper | Status |
|-----------|-----------|--------|
| Pattern–tactic interaction | `harrison2010how` — How Do Architecture Patterns and Tactics Interact? | ✅ have |
| Mining architecture tactics | `bi2021mining` — Mining Architecture Tactics and QA Knowledge in SO | ✅ have |
| Architectural patterns for maintainability | `rahmati2021ensuring` — Ensuring Maintainability at Architecture Level | ✅ have |
| Architecture erosion | `li2021understanding` — Understanding Architecture Erosion | ✅ have |
| Architectural drift | `rosik2011assessing` — Assessing Architectural Drift | ✅ have |
| Software architectural patterns | `kassab2018software` — Software Architectural Patterns in Practice | ✅ have |
| Static analysis comparison | `lenarduzzi2023critical` — Critical Comparison on Six Static Analysis Tools | ✅ have |

### Level 3 — Thesis-Specific (LLM + refactoring + automated tactics)

| Sub-topic | Key Paper | Status |
|-----------|-----------|--------|
| LLM code refactoring | `depalma2024exploring` — Exploring ChatGPT's Code Refactoring Capabilities | ✅ have |
| LLM automated refactoring | `liu2025exploring` — Exploring LLMs in Automated Software Refactoring | ✅ have |
| LLM for novice code | `haindl2024chatgpt` — Does ChatGPT Help Novice Programmers Write Better Code? | ✅ have |
| Static analysis FPs/FNs | `cui2024empirical` — False Negatives and Positives of Static Code Analyzers | ✅ have |
| SonarQube mining study | `nocera2025sonarqube` — Dealing with SonarQube Cloud: Mining Study | ✅ have |
| Maintainability risk methods | `abdelmoez2006methodology` — Methodology for Maintainability-Based Risk Assessment | ✅ have |
| Quality models comparison | `albadareen2011quality` — Software Quality Models: A Comparative Study | ✅ have |
| Quality models in SE literature | `alqutaish2010quality` — Quality Models in Software Engineering Literature | ✅ have |
| Maintainability assessment (industrial) | `moreu2012practical` — Practical Maintainability Assessment in Industrial Devices | ✅ have |

---

## Snowballing Strategy

### Backward Snowballing
Check references of Level 3 and Level 2 papers to find missing foundational works:
1. Start with the L3 papers → extract their reference lists
2. Look for frequently cited works (cited by 3+ of our papers = high priority)
3. Prioritize: L1 foundations > L2 intersections > tangential

### Forward Snowballing
Use Google Scholar "Cited by" and Semantic Scholar citations on core papers:
- `kim2009qualitydriven`, `harrison2010how`, `depalma2024exploring`
- Look for 2024-2026 papers that build on these

### Tracking
All snowball references tracked in `lit/snowball_refs.md`.

---

## Prioritized Reading

### Tier 1 — Must-Read (read in full, create summary)
All Level 3 papers + key Level 1/2 papers:
- Core architectural tactics papers (kim2009, harrison2010, bi2021, rahmati2021)
- LLM refactoring (depalma2024)
- Architecture erosion (li2021, rosik2011)

### Tier 2 — Key Sections (abstract + methodology + results)
Remaining Level 2 papers, quality model papers:
- Quality models (ISO25010, quality models comparison papers)
- Static analysis (lenarduzzi2023, SonarQube study)
- Software patterns (kassab2018)

### Tier 3 — Skim (abstract + conclusion only)
Supporting papers with indirect relevance:
- General LLM for programming papers
- Broad software quality surveys

Full reading list tracked in `lit/readings.md`.

---

## Inclusion / Exclusion Criteria

**Include:**
- Published 2018 or later (exceptions for seminal works like Perry 1992, Garlan 1993)
- Peer-reviewed or high-quality preprint (arXiv with citations)
- Directly addresses: architectural tactics, maintainability, LLM code refactoring, software architecture quality, or static analysis
- Provides reproducible methodology or empirical evidence

**Exclude:**
- Non-English publications
- No methodology section (opinion pieces, blog posts — use as grey literature only)
- Superseded by newer version from same authors
- Purely commercial / marketing whitepapers

---

## Workflow Pipeline

```
Phase 1: Inventory existing papers → status.md
Phase 2: Search & download new papers → pdfs/
Phase 3: Summarize papers → summaries/
Phase 4: Cross-paper synthesis → insights/
Phase 5: Update thesis lit review sections
```

---

## Phase 1: Inventory

### Before searching — check existing sources first

1. **Read thesis draft**: `diploma/latex_diploma/chapters/chapter2.tex`
2. **Read bibliography**: `diploma/latex_diploma/ref.bib`
3. **Check pdfs/ dir** for already-downloaded papers
4. **Check summaries/** for completed summaries
5. **Check readings.md** for prioritized list

Only search for papers NOT already available.

### Folder structure

```
lit/
├── CLAUDE.md          # This file
├── status.md          # Progress tracking
├── readings.md        # Prioritized reading list (Tier 1/2/3)
├── snowball_refs.md   # Snowball reference tracking
├── references.bib     # Verified BibTeX entries for all papers
├── pdfs/              # Downloaded papers (PDFs)
├── converted/         # PDF→Markdown conversions
├── templates/         # Reusable templates for summaries & insights
├── summaries/         # Per-paper summaries (Markdown)
└── insights/          # Cross-paper topic synthesis
```

### status.md format

```markdown
| # | Key | Title | Section | Era | PDF | Summary | Relevance | Phase |
|---|-----|-------|---------|-----|-----|---------|-----------|-------|
| 1 | kim2009qualitydriven | Quality-Driven Architecture Using Tactics | 2.3 | Foundational | ✅ | ❌ | HIGH | Phase 3 |
```

Update status.md after completing each phase per paper.

---

## Phase 2: Search & Download Papers

### Tiered Search Strategy

**TIER 1 — Core (architectural tactics + maintainability + LLM):**
```python
search_semantic("architectural tactics maintainability improvement automated", year="2020-")
search_semantic("LLM code refactoring architecture quality", year="2023-")
search_semantic("automated architectural tactic implementation software", year="2020-")
search_arxiv("architectural tactics maintainability LLM refactoring")
search_arxiv("automated software architecture improvement")
```

**TIER 2 — Technical (metrics, static analysis, quality models):**
```python
search_semantic("software maintainability metrics static analysis", year="2020-")
search_semantic("architecture erosion detection automated", year="2020-")
search_semantic("ISO 25010 maintainability assessment framework", year="2020-")
search_semantic("software quality models comparison survey", year="2020-")
```

**TIER 3 — Broader (patterns, refactoring, pipelines):**
```python
search_semantic("software architectural patterns empirical study", year="2018-")
search_semantic("pipes and filters architecture pattern implementation", year="2018-")
search_semantic("LLM automated code transformation behavior preservation", year="2023-")
```

### MCP Tool Priority

1. Semantic Scholar (cross-database, citations, year filters)
2. arXiv (CS/SE preprints)
3. CrossRef (DOI validation, metadata)
4. Google Scholar (citation tracking, broad coverage)

### Download

```python
# arXiv papers
download_arxiv(paper_id="XXXX.XXXXX", save_path="./lit/pdfs")

# Semantic Scholar (if open access)
download_semantic(paper_id="DOI:10.xxxx/...", save_path="./lit/pdfs")
```

### PDF naming convention

Rename after download: `[topic]_[##]_[author][year]_[description].pdf`

| Topic Code | Meaning |
|------------|---------|
| `at` | Architectural tactics (selection, implementation, cataloging) |
| `sa` | Software architecture (patterns, styles, foundations) |
| `maint` | Maintainability (metrics, models, ISO 25010) |
| `llm` | LLM for code analysis/refactoring |
| `refac` | Refactoring and code improvement |
| `static` | Static analysis tools |
| `pipe` | Pipeline approaches |

Example: `at_01_kim2009_quality-driven-tactics.pdf`

### Convert PDFs

**NEVER read PDFs directly.** Always convert first:
```bash
python -m markitdown lit/pdfs/paper.pdf > lit/converted/paper.md
```

Or use MCP `read_*_paper` tools which extract text automatically.

---

## Phase 3: Summarize Papers

### Templates

Copy the appropriate template from `lit/templates/`:

| Tier | Template | When to Use |
|------|----------|-------------|
| Tier 1 (Must-Read) | `templates/summary_full.md` | Full read — all fields including challenges, datasets, NLM queries |
| Tier 2 (Key Sections) | `templates/summary_partial.md` | Abstract + method + results only |
| Tier 3 (Skim) | `templates/summary_skim.md` | Abstract + conclusion — minimal card |
| NLM-Only | `templates/summary_nlm_only.md` | Sources only in NLM (e.g., books not available as PDF) |

### NLM-Assisted Workflow

For any paper, use `/notebooklm` to help extract information:
- Quotes: `"What are the most important quotes from {Paper Title}?"`
- Challenges: `"What challenges does {author} report in {short title}?"`
- Datasets: `"What dataset or benchmark does {short title} use?"`

### Summary template (inline reference)

Save to `summaries/[key].md`:

```markdown
## [Paper Title]

| Field | Value |
|-------|-------|
| **Key** | `author_year_keyword` |
| **Authors** | First Author et al. |
| **Venue** | Journal/Conference (Year) |
| **Tier** | Q1/Q2/A*/A/B/Workshop/Preprint |
| **Citations** | N (if known) |
| **Level** | L1-Foundational / L2-Intersection / L3-Thesis-Specific |

### Contribution
[2-3 sentences: What is the main contribution?]

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| X  | X  |   X   |  X  |   X    |  /25  |

**Relevance:** CRITICAL / HIGH / MEDIUM / LOW

[1-2 sentences: How does this help the thesis?]

### Method & Validation
- **Type:** Survey / Framework / Case Study / Experiment / Tool
- **Validation:** Prototype / Benchmark / Expert Review / Comparison / None
- **Evidence:** [What supports claims?]

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| ... | ... |

### Key Quotes
> "Exact quote from paper" (p. XX)

### Key Takeaway
[One actionable insight for the thesis]

### Snowball References
**Backward:** `ref1`, `ref2` (most relevant citations)
**Forward:** Check Google Scholar for papers citing this
```

### Relevance scoring guide

| Score | Meaning | Example |
|-------|---------|---------|
| **5** | Core topic, directly reusable | Paper on automated architectural tactic implementation |
| **4** | Highly relevant pattern | LLM refactoring with maintainability metrics |
| **3** | Useful background | General software quality model survey |
| **2** | Tangential | LLM survey with brief architecture mention |
| **1** | Keyword only | Mentions "maintainability" once |
| **0** | Not relevant | Unrelated domain |

**Categories:**
- **AT:** Architectural tactics, tactic selection, tactic catalogs, pattern–tactic interaction
- **SA:** Software architecture styles, patterns, foundations, erosion, drift
- **Maint:** Maintainability metrics, ISO 25010, quality models, modularity, testability
- **LLM:** LLM for code analysis, refactoring, code generation, behavior preservation
- **Static:** Static analysis tools, Radon, SonarQube, metric computation

---

## Phase 4: Cross-Paper Synthesis

### Templates

Copy the appropriate template from `lit/templates/`:

| Template | When to Use |
|----------|-------------|
| `templates/insight_topic.md` | General cross-paper synthesis per topic/section |
| `templates/insight_metrics_validation.md` | Specialized review of metrics & validation approaches |

### NLM Cross-Paper Queries

Use `/notebooklm` for synthesis across all sources:
- Comparisons: `"Compare how X and Y approach {topic}"`
- Thematic: `"What do the sources say about {challenge/gap}?"`
- Metrics: `"Which papers use maintainability metrics for evaluation?"`

### Insight template (inline reference)

Create topic files in `insights/`:

```markdown
## Topic: [Topic Name]

**Papers:** N | **Updated:** YYYY-MM-DD

### Summary
[2-3 paragraphs synthesizing findings]

### Key Papers
| Paper | Contribution | Relevance |
|-------|--------------|-----------|
| `key` | Finding | HIGH/MED |

### Consensus
| Finding | Papers | Confidence |
|---------|--------|------------|
| Finding | `p1`, `p2` | High/Med/Low |

### Contradictions
| Issue | Position A | Position B | Thesis Choice |
|-------|------------|------------|---------------|
| Issue | `p1`: X | `p2`: Y | Decision |

### Gaps
| Gap | Impact on Thesis |
|-----|-----------------|
| Gap | Effect on Objective |

### Recommendations
**Adopt:** Pattern from `paper` — reason
**Adapt:** Pattern from `paper` — changes needed
**Avoid:** Approach from `paper` — why not

### Related Work Draft
> [Draft paragraph for thesis Chapter 2]
```

### Topics to synthesize

Map to thesis sections:
- **Software Architecture Foundations** → Section 2.1
- **Maintainability & Quality Models** → Section 2.2
- **Pattern–Tactic Interaction & Erosion** → Section 2.3
- **Maintainability Tactics Catalog** → Section 2.4
- **Assessment Methods & Static Analysis** → Section 2.5
- **LLM for Code Refactoring** → Section 2.6
- **Metrics & Validation Approaches** → Cross-cutting (O3, O4)

---

## Phase 5: Update Thesis

Use insights to strengthen Chapter 2 sections. For each section:
1. Check `insights/` for synthesized findings
2. Identify gaps in current thesis text
3. Add new citations, findings, comparisons
4. Ensure each Objective has supporting literature

---

## Managing references.bib

### Creating entries
**Always verify new papers with MCP before adding to references.bib:**

```python
# 1. Search for metadata
search_semantic(query="exact paper title", max_results=3)
# or
search_crossref(query="exact paper title", kwargs="")
# or
get_crossref_paper_by_doi(doi="10.xxxx/...")

# 2. Verify: authors, year, venue, DOI match the PDF
# 3. Generate BibTeX entry with key matching status.md
```

### BibTeX quality checklist
- [ ] Every entry has: author, title, year, and either journal/booktitle/howpublished
- [ ] DOI present where available
- [ ] arXiv ID (eprint field) present for preprints
- [ ] Keys match `lit/status.md` keys exactly
- [ ] No duplicate entries
- [ ] URLs are valid and accessible

### Key format
`authorYYYYkeyword` — e.g., `kim2009qualitydriven`, `harrison2010how`, `depalma2024exploring`

---

## Tools Quick Reference

| Tool | Command / Trigger |
|------|-------------------|
| Paper Search MCP | `search_semantic`, `search_arxiv`, `search_crossref`, `search_google_scholar` |
| Paper Download | `download_arxiv`, `download_semantic` |
| Paper Read | `read_arxiv_paper`, `read_semantic_paper` |
| DOI Lookup | `get_crossref_paper_by_doi` |
| NotebookLM | `/notebooklm` (requires Chrome CDP on port 9222) — see NLM Integration below |
| PDF skill | `/pdf` for extraction, form filling, merge/split |
| Web Scraper | `/web-scraper` for scraping content from websites |
| Doc Converter | Agent `doc-converter` for PDF↔Markdown conversion |

---

## NotebookLM Integration

**Notebook URL:** `[TO BE CREATED]`

A dedicated notebook should be created with all papers from `lit/pdfs/` imported.

**Usage in Phase 3 (Summaries):**
- Query NLM to extract specific findings, quotes, challenges from individual papers
- Example: `"What challenges does Kim report in quality-driven architecture?"`

**Usage in Phase 4 (Insights):**
- Cross-paper comparisons: `"Compare how Harrison and Kim approach pattern–tactic interaction"`
- Thematic synthesis: `"What do the sources say about maintainability assessment challenges?"`
- Metrics inventory: `"Which papers use static analysis metrics for evaluation?"`

**Skill:** Use `/notebooklm` (requires Chrome CDP on port 9222)

---

## Quality Checks

**Per Summary:**
- [ ] Title correctly identified
- [ ] Authors and venue extracted
- [ ] All 5 relevance scores assigned (AT/SA/Maint/LLM/Static)
- [ ] Contribution is specific, not generic
- [ ] Key takeaway is actionable for thesis
- [ ] At least 2 snowball refs listed
- [ ] Level assigned (L1/L2/L3)
- [ ] Challenges & limitations identified (Tier 1 only)
- [ ] Dataset/benchmark and metrics documented (Tier 1 only)
- [ ] At least 1 key quote extracted

**Per Insights:**
- [ ] 3+ papers analyzed per topic
- [ ] Contradictions identified (if any)
- [ ] Metrics & validation approaches table filled
- [ ] Challenges table with frequency counts
- [ ] Key quotes supporting consensus and challenges
- [ ] Gaps specific to thesis Objectives noted
- [ ] Recommendations are actionable
- [ ] Related work draft paragraph written

**Per references.bib entry:**
- [ ] Verified with MCP (Semantic Scholar / CrossRef)
- [ ] Key matches status.md
- [ ] DOI or arXiv ID present
- [ ] All required BibTeX fields present

---

*Instructions v1.0 | 2026-02-16*
