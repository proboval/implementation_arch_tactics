"""
Configuration for Web Scraper Skill
Centralizes constants, paths, timeouts, and selectors
"""

import sys
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Paths
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
SCREENSHOTS_DIR = SKILL_DIR / "screenshots"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Browser Configuration
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--no-first-run',
    '--no-default-browser-check',
]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

# CDP Configuration
DEFAULT_CDP_URL = "http://localhost:9222"

# Timeouts (milliseconds unless noted)
PAGE_LOAD_TIMEOUT = 30000
NETWORK_IDLE_TIMEOUT = 10000
SCREENSHOT_TIMEOUT = 10000
CRAWL_DELAY_MIN_MS = 500
CRAWL_DELAY_MAX_MS = 2000

# Safety limits
MAX_CRAWL_DEPTH = 5
MAX_CRAWL_PAGES = 50

# Content extraction selectors (tried in order)
CONTENT_SELECTORS = [
    'article',
    'main',
    '[role="main"]',
    '.content',
    '.post-content',
    '.article-content',
    '#content',
    '#main-content',
]

# Table selectors
TABLE_SELECTORS = [
    'table',
    '[role="table"]',
    '.data-table',
    '.table',
]

# Tags to strip from content
STRIP_TAGS = ['script', 'style', 'noscript', 'iframe', 'svg']

# Noise elements to remove for clean extraction
NOISE_SELECTORS = [
    'nav', 'header', 'footer',
    '.sidebar', '.menu', '.navigation',
    '.ad', '.advertisement', '.cookie-banner',
    '#cookie-consent', '.social-share',
]

# Screenshot defaults
DEFAULT_VIEWPORT = {'width': 1920, 'height': 1080}
FULL_PAGE_SCREENSHOT = True

# Output formats
OUTPUT_FORMATS = ['markdown', 'json', 'html', 'text']
TABLE_FORMATS = ['csv', 'json', 'markdown']
