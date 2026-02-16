---
name: web-scraper
description: Web scraping and content extraction using Playwright browser automation. Use when user wants to scrape web pages, extract content or tables from websites, take page screenshots, crawl multiple related pages, or extract data from authenticated sites using Chrome CDP connection.
---

# Web Scraper Skill

Browser-based web scraping with Playwright for content extraction, table parsing, screenshots, and multi-page crawling. Supports headless mode for public pages and CDP mode for authenticated sites.

## When to Use This Skill

Trigger when user:
- Says "scrape", "extract from website", "crawl pages", "get content from URL"
- Provides a URL and asks to extract content, tables, or data
- Asks for a screenshot of a web page
- Wants to scrape authenticated/logged-in sites
- Uses phrases like "get the content from this page", "extract the table", "scrape this site"

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# CORRECT - Always use run.py:
python scripts/run.py scrape_page.py --url "..." --format markdown
python scripts/run.py crawl_site.py --url "..." --depth 2

# WRONG - Never call directly:
python scripts/scrape_page.py --url "..."  # Fails without venv!
```

The `run.py` wrapper automatically creates `.venv`, installs dependencies, and runs scripts properly.

## Decision Flow

```
User wants to scrape web content
    |
    v
What type of extraction?
    |
    +--- Single page content:
    |       |
    |       v
    |    Needs authenticated access (logged-in session)?
    |       |
    |       +--- YES: Use CDP mode
    |       |       python scripts/run.py scrape_page.py --url "..." --mode cdp
    |       |
    |       +--- NO: Use headless mode (default)
    |               python scripts/run.py scrape_page.py --url "..."
    |
    +--- Multiple pages / crawl:
    |       python scripts/run.py crawl_site.py --url "..." --depth 2
    |
    +--- Tables only:
    |       python scripts/run.py extract_tables.py --url "..." --format csv
    |
    +--- Screenshot:
            python scripts/run.py screenshot.py --url "..." --output page.png
```

## CDP Mode (Authenticated Scraping)

For sites requiring login, connect to the user's Chrome browser via CDP:

### Step 1: Start Chrome with Debug Port

**Windows:**
```bash
chrome.exe --remote-debugging-port=9222
```

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### Step 2: Log in to Target Site

Open the target website in Chrome and log in with your credentials.

### Step 3: Scrape with CDP Mode

```bash
python scripts/run.py scrape_page.py --url "https://authenticated-site.com/page" --mode cdp
```

## Script Reference

### Single Page Scraper (`scrape_page.py`)

```bash
# Basic scrape (headless, markdown output)
python scripts/run.py scrape_page.py --url "https://example.com"

# CDP mode (authenticated)
python scripts/run.py scrape_page.py --url "https://..." --mode cdp

# Extract specific element
python scripts/run.py scrape_page.py --url "https://..." --selector "article"

# JSON output with metadata and links
python scripts/run.py scrape_page.py --url "https://..." --format json --include-metadata --include-links

# Save to file
python scripts/run.py scrape_page.py --url "https://..." --output content.md

# Scroll for lazy-loaded content
python scripts/run.py scrape_page.py --url "https://..." --scroll

# Wait for dynamic element
python scripts/run.py scrape_page.py --url "https://..." --wait-for ".data-loaded"
```

### Multi-Page Crawler (`crawl_site.py`)

```bash
# Basic crawl (depth 1)
python scripts/run.py crawl_site.py --url "https://example.com/docs/"

# Deeper crawl with limits
python scripts/run.py crawl_site.py --url "https://..." --depth 2 --max-pages 10

# Filter by URL pattern
python scripts/run.py crawl_site.py --url "https://..." --pattern "/docs/.*"

# Save to directory with index
python scripts/run.py crawl_site.py --url "https://..." --output-dir ./scraped/ --index

# Crawl with CDP
python scripts/run.py crawl_site.py --url "https://..." --mode cdp --depth 1
```

### Screenshot (`screenshot.py`)

```bash
# Full page screenshot
python scripts/run.py screenshot.py --url "https://example.com"

# Custom output and viewport
python scripts/run.py screenshot.py --url "https://..." --output page.png --viewport 1280x720

# Screenshot specific element
python scripts/run.py screenshot.py --url "https://..." --selector ".main-content"

# JPEG with quality setting
python scripts/run.py screenshot.py --url "https://..." --format jpeg --quality 90
```

### Table Extractor (`extract_tables.py`)

```bash
# Extract all tables as CSV
python scripts/run.py extract_tables.py --url "https://example.com"

# JSON format
python scripts/run.py extract_tables.py --url "https://..." --format json

# Markdown format
python scripts/run.py extract_tables.py --url "https://..." --format markdown

# Extract specific table by index
python scripts/run.py extract_tables.py --url "https://..." --index 0

# Save to file
python scripts/run.py extract_tables.py --url "https://..." --output tables/
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| CDP connection refused | Start Chrome with `--remote-debugging-port=9222` |
| Page timeout | Increase `--timeout` value |
| Missing dynamic content | Use `--scroll` or `--wait-for` |
| Empty content | Try `--selector` to target specific element |
| Rate limited | Add `--delay 2000` between requests |
| Tables not found | Check if tables are rendered by JavaScript, use `--wait-for "table"` |

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically (patchright, beautifulsoup4, markdownify, etc.)
- Everything isolated in skill directory
