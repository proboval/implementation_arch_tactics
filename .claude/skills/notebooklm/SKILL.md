---
name: notebooklm
description: Query Google NotebookLM notebooks for source-grounded answers from Gemini. Use when user mentions NotebookLM, shares notebook URL, asks to query docs, or wants Deep Research to find/import web sources on a topic. Triggers on "ask my NotebookLM", "query notebook", "research topic", "find sources for".
---

# NotebookLM Research Assistant

Query NotebookLM for source-grounded answers. Includes **Deep Research** for web source discovery and auto-import. Connects via CDP to your Chrome browser.

## Critical: Always Use run.py Wrapper

```bash
# ✅ CORRECT:
python scripts/run.py ask_question.py --notebook-url "..." --question "..."
python scripts/run.py deep_research.py --notebook-url "..." --query "..."

# ❌ WRONG - fails without venv:
python scripts/ask_question.py --question "..."
```

## CDP Setup (Required)

Start Chrome with debug port (close all Chrome windows first):

```bash
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-debug-profile"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug-profile"
```

Then log into NotebookLM in Chrome.

## Ask Questions

```bash
python scripts/run.py ask_question.py --notebook-url "https://notebooklm.google.com/notebook/..." --question "Your question"
```

## Deep Research (Web Search + Import)

Searches the web for sources and imports them into the notebook:

```bash
python scripts/run.py deep_research.py --notebook-url "https://notebooklm.google.com/notebook/..." --query "research topic"
```

**How it works:**
1. Checks for existing completed research → imports if found
2. Selects Deep Research mode, submits query
3. Waits for completion (1-5 minutes typical)
4. Extracts report info and auto-clicks Import

**Use when:** Building research corpus, finding papers on a topic, user asks to "research" or "find sources".

## Source Quality Management (Post-Deep Research)

After Deep Research, clean up low-quality sources to improve answer quality.

### Method 1: Smart Filtering (Recommended)

Ask NotebookLM to identify the most relevant sources for your research topics:

```bash
# Step 1: Query for top sources per topic
python scripts/run.py ask_question.py --notebook-url "..." \
  --question "List TOP 10 most relevant sources for EACH topic: [Topic1]; [Topic2]; [Topic3]. Format as numbered lists with source titles."

# Step 2: List all sources
python scripts/run.py manage_sources.py list --notebook-url "..."

# Step 3: Compare and delete sources NOT in top lists by index
python scripts/run.py manage_sources.py delete --notebook-url "..." --index 5 --confirm
```

**Benefits:** Uses NotebookLM's understanding of content relevance rather than simple pattern matching.

### Method 2: Pattern-Based Filtering

Quick removal of obviously low-quality sources:

```bash
# Preview sources to remove (dry run)
python scripts/run.py manage_sources.py delete --notebook-url "..." \
  --pattern "medium|blog|reddit|Talent500|a1qa|Testmo"

# Delete low-quality sources (re-fetches after each delete for accuracy)
python scripts/run.py manage_sources.py delete --notebook-url "..." \
  --pattern "medium|blog|reddit|Talent500|a1qa|Testmo" --confirm
```

**Note:** Pattern delete re-fetches the source list after each deletion to handle index shifting correctly. This makes it slower but accurate.

**Recommended filter patterns:**
- `medium|blog` - Blog posts
- `reddit|quora` - Forum content
- `Talent500|a1qa|Testmo|Articsledge` - Vendor blogs
- `QuantumXL|SumatoSoft|veritysoftware` - SEO content

**Keep:** ResearchGate, arXiv, IEEE, ACM, DORA Report, official docs

### Method 3: Index-Based Deletion

For precise control, delete one source at a time:

```bash
# List sources to get indices
python scripts/run.py manage_sources.py list --notebook-url "..."

# Delete highest index first (indices shift after each delete!)
python scripts/run.py manage_sources.py delete --notebook-url "..." --index 42 --confirm
python scripts/run.py manage_sources.py delete --notebook-url "..." --index 38 --confirm
# etc.
```

**Important:** Always delete from highest index to lowest to avoid index shifting issues.

## Notebook Library Management

```bash
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py search --query KEYWORD
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
```

**Smart Add** - Query notebook first to discover content:
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" --question "What topics are covered? Brief overview."
# Then use discovered info for add command
```

## Follow-Up Mechanism (CRITICAL)

Every answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required behavior:**
1. Compare answer to user's original request
2. If gaps exist, ask follow-up immediately
3. Repeat until information complete
4. Synthesize all answers before responding to user

## Token Mode (Alternative to CDP)

If CDP unavailable:

```bash
python scripts/run.py auth_manager.py setup  # One-time setup
python scripts/run.py ask_question.py --token --notebook-url "..." --question "..."
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common issues.

Quick fixes:
- `ModuleNotFoundError` → Use `run.py` wrapper
- CDP connection refused → Use fresh `--user-data-dir`
- Can't connect to Chrome → Close all Chrome, restart with debug port

## Resources

- `scripts/` - Automation scripts:
  - `ask_question.py` - Query notebooks
  - `deep_research.py` - Web source discovery
  - `manage_sources.py` - List/delete sources for quality control
  - `notebook_manager.py` - Library management
  - `auth_manager.py` - Authentication
- `references/` - Detailed docs: api_reference.md, troubleshooting.md, usage_patterns.md
- `data/` - Local storage for auth and notebook library
