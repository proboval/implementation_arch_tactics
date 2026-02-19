# Experiment 1

## Architecture Prompt

``` python
f"""
You are a software architecture expert.

Given the following metrics extracted from a Python project,
determine the most likely software architecture style.

Architecture metrics:
{json.dumps(arch_metrics, indent=2)}

Code maintainability metrics:
{json.dumps(code_metrics, indent=2)}

Repository tree:
{repo_tree}

Repository files content:
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

Choose ONE primary architecture type from:
- layered
- hexagonal (ports and adapters)
- modular_monolith
- script_based
- mvc
- microservices_like
- unclear

Return STRICT JSON with fields:
- architecture_type
- confidence (0.0 - 1.0)
- evidence (list of observations)
- alternatives (list)
- risks (list)

Do not include explanations outside JSON.

IMPORTANT:
- Return ONLY raw JSON
- Do NOT use markdown
- Do NOT wrap in ```json
- The first character of the response MUST be {{ or [
"""
```

## Tactic Define Prompt

``` python
f"""
ID: {t['AT_ID']}
Name: {t['Tactic_Name']}
Primary QA Impact: {t['Primary_QA_Impact']}
Description: {t['Description']}
Positive Impact: {t['Positive_Impact']}
Negative Impact: {t['Negative_Impact']}
Related Terms: {t['Related_Terms']}
Source: {t['Source']}
""".strip()
                for t in self.tactics
            )

            prompt = f"""
You are a software architecture expert.

ARCHITECTURE:
{architecture}

MAINTAINABILITY ISSUES (static analysis):
{issues}

ARCHITECTURAL TACTICS CATALOG:
{tactics_text}

REPOSITORY TREE:
{repo.repo_tree}

REPOSITORY FILES CONTENT:
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo.repo_files.items()
)}

TASK:
Select the most appropriate architectural tactic to improve maintainability.
Consider trade-offs.

OUTPUT STRICT JSON:
{{
  "selected_tactic": {{
    "id": "...",
    "name": "...",
    "primary_qa_impact": "...",
    "positive_impact": "...",
    "negative_impact": "..."
  }},
  "justification": "...",
  "expected_architectural_change": "...",
  "risks": "..."
}}

IMPORTANT:
- Return ONLY raw JSON
- Do NOT use markdown
- Do NOT wrap in ```json
- The first character of the response MUST be {{ or [
"""
```

## Tactic Implementation Prompt

``` python
f"""
You are an automated refactoring agent.

You work on an EXISTING Python repository.
Your goal is to APPLY the given architectural tactic
using SAFE, INCREMENTAL, LOCAL changes.

Repository:
{repo_name}

====================
Repository structure
====================
{repo_tree}

====================
Relevant file excerpts
====================
{"".join(
    f"\n--- {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

====================
Architectural tactic
====================
{json.dumps(tactic, indent=2)}

====================
Already applied changes
====================
{json.dumps(applied_steps, indent=2)}

====================
Rules (STRICT)
====================
- Propose EXACTLY ONE change
- Modify ONLY ONE file
- The change must be SMALL and LOCAL
- Prefer refactoring over new code
- Do NOT redesign architecture
- Do NOT introduce new abstractions
- If no safe change exists → STOP

- If modifying a large file:
  - Return the FULL file content
  - Ensure the JSON object is COMPLETE and CLOSED
  - Do NOT truncate the response


====================
Output format (CRITICAL)
====================
Return EXACTLY ONE JSON OBJECT.
NO explanations.
NO code fences.
NO additional text.
The response MUST end with a single closing brace `}}`.
Nothing is allowed after it.


Schema:
{{
  "action": "modify_file" | "create_file" | "STOP",
  "path": "relative/path.py",
  "content": "FULL file content (omit only if action=STOP)"
}}

If no change is safe:
{{ "action": "STOP" }}
"""
```

# Experiment 2

## Architecture Prompt

``` python
f"""
You are a software architecture expert.

Given the following metrics extracted from a Python project,
determine the most likely software architecture style.

Architecture metrics:
{json.dumps(arch_metrics, indent=2)}

Code maintainability metrics:
{json.dumps(code_metrics, indent=2)}

Repository tree:
{repo_tree}

Repository files content:
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

Choose ONE primary architecture type from:
- layered
- hexagonal (ports and adapters)
- modular_monolith
- script_based
- mvc
- microservices_like
- unclear

Return STRICT JSON with fields:
- architecture_type
- confidence (0.0 - 1.0)
- evidence (list of observations)
- alternatives (list)
- risks (list)

Do not include explanations outside JSON.

IMPORTANT:
- Return ONLY raw JSON
- Do NOT use markdown
- Do NOT wrap in ```json
- The first character of the response MUST be {{ or [
"""
```

## Tactic Define Prompt

``` python
f"""
You are a senior software architect specializing in maintainability improvements of real backend systems.

========================================
WHAT ARE ARCHITECTURAL TACTICS
========================================

Architectural tactics are design decisions applied to the structure of software to improve quality attributes.

A maintainability tactic typically:

• reduces code complexity
• improves modularity
• improves testability
• improves separation of concerns
• improves readability
• reduces coupling
• increases cohesion

Tactics operate on REAL code structure, not theory.

Examples:

GOOD tactics:

- Extract component
- Introduce abstraction
- Refactor large module
- Introduce dependency inversion
- Separate responsibilities

BAD tactics:

- Add comments
- Rename variables
- Improve documentation

These are NOT architectural tactics.

========================================
INPUT DATA
========================================

ARCHITECTURE DESCRIPTION:
{architecture}

STATIC ANALYSIS ISSUES:
{issues}

REPOSITORY TREE:
{repo.repo_tree}

REPOSITORY FILE CONTENTS (signatures only):
{"".join(
    f"\n--- FILE: {path} ---\n{content}\n"
    for path, content in repo.repo_files.items()
)}

========================================
ARCHITECTURAL TACTICS CATALOG
========================================

You MUST select ONLY ONE tactic from this catalog.

{tactics_text}

DO NOT invent new tactics.

========================================
TASK
========================================

Select the SINGLE BEST architectural tactic that:

• directly addresses REAL maintainability problems in THIS repository
• can be implemented incrementally
• can be implemented via code changes
• fits the actual repository structure

IMPORTANT:

You MUST base your decision on:

• static analysis issues
• real file structure
• real modules
• real architectural problems

NOT theory.

========================================
SELECTION RULES
========================================

The tactic MUST:

• improve maintainability

AND

• be implementable in this repository

AND

• affect identifiable files/modules

DO NOT select tactics that:

• require rewriting the entire system
• require unrealistic changes
• do not match repository structure

========================================
OUTPUT FORMAT (STRICT JSON ONLY)
========================================

Return ONLY JSON.

NO markdown.

NO explanations outside JSON.

First character MUST be {{


Required schema:

{{
  "selected_tactic": {{
    "id": "...",
    "name": "...",
    "primary_qa_impact": "...",
    "positive_impact": "...",
    "negative_impact": "..."
  }},

  "justification": "...",

  "target_components": [
    "path/to/file.py",
    "module.name"
  ],

  "expected_architectural_change": "...",

  "implementation_strategy": "...",

  "risks": "..."
}}


========================================
JUSTIFICATION REQUIREMENTS
========================================

Justification MUST explain:

• WHY this tactic
• WHAT maintainability problem it solves
• WHERE in repository

========================================
IMPLEMENTATION STRATEGY REQUIREMENTS
========================================

Strategy MUST describe:

• WHAT to refactor
• HOW structure will change
• WHAT new abstractions/modules may appear

========================================
IMPORTANT
========================================

Return ONLY valid JSON.

Do NOT wrap in ```json

Do NOT invent tactics.

Do NOT output multiple tactics.

Select ONLY ONE.
"""
```

## Tactic Implementation Prompt
``` python
f"""
You are an automated refactoring agent.

You work on an EXISTING Python repository.
Your goal is to APPLY the given architectural tactic
using SAFE, INCREMENTAL, LOCAL changes.

Repository:
{repo_name}

====================
Repository structure
====================
{repo_tree}

====================
Relevant file excerpts
====================
{"".join(
    f"\n--- {path} ---\n{content}\n"
    for path, content in repo_files.items()
)}

====================
Architectural tactic
====================
{json.dumps(tactic, indent=2)}

====================
Already applied changes
====================
{json.dumps(applied_steps, indent=2)}

====================
Rules (STRICT)
====================
- Propose EXACTLY ONE change
- Modify ONLY ONE file
- The change must be SMALL and LOCAL
- Prefer refactoring over new code
- Do NOT redesign architecture
- Do NOT introduce new abstractions
- If no safe change exists → STOP
- On the first step never STOP

- If modifying a large file:
  - Return the FULL file content
  - Ensure the JSON object is COMPLETE and CLOSED
  - Do NOT truncate the response


====================
Output format (CRITICAL)
====================
Return EXACTLY ONE JSON OBJECT.
NO explanations.
NO code fences.
NO additional text.
The response MUST end with a single closing brace `}}`.
Nothing is allowed after it.


Schema:
{{
  "action": "modify_file" | "create_file" | "STOP",
  "path": "relative/path.py",
  "content": "FULL file content (omit only if action=STOP)"
}}

If no change is safe:
{{ "action": "STOP" }}
```
