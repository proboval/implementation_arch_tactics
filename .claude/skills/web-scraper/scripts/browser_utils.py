"""
Browser Utilities for Web Scraper Skill
Handles browser launching (CDP + headless), stealth features, content extraction
"""

import json
import time
import random
import sys
from typing import Optional, Tuple
from urllib.parse import urljoin, urlparse

from patchright.sync_api import Playwright, BrowserContext, Page, Browser
from config import (
    BROWSER_ARGS, USER_AGENT, DEFAULT_CDP_URL, DEFAULT_VIEWPORT,
    CONTENT_SELECTORS, NOISE_SELECTORS, STRIP_TAGS, TABLE_SELECTORS,
    PAGE_LOAD_TIMEOUT, NETWORK_IDLE_TIMEOUT,
)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class BrowserFactory:
    """Factory for creating configured browser contexts"""

    @staticmethod
    def connect_to_cdp(
        playwright: Playwright,
        cdp_url: str = DEFAULT_CDP_URL
    ) -> Tuple[Browser, BrowserContext]:
        """
        Connect to an existing Chrome browser via CDP (Chrome DevTools Protocol).
        User must start Chrome with: --remote-debugging-port=9222
        """
        print(f"  Connecting to Chrome at {cdp_url}...")

        try:
            browser = playwright.chromium.connect_over_cdp(cdp_url)

            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                print(f"  Connected! Found {len(context.pages)} open tab(s)")
            else:
                context = browser.new_context()
                print("  Connected! Created new context")

            return browser, context

        except Exception as e:
            error_msg = str(e)
            if "connection refused" in error_msg.lower() or "cannot connect" in error_msg.lower():
                print(f"  Cannot connect to Chrome at {cdp_url}")
                print()
                print("  To use CDP mode, start Chrome with remote debugging:")
                print()
                print('    Windows:')
                print('      chrome.exe --remote-debugging-port=9222')
                print()
                print('    macOS:')
                print('      /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222')
                print()
                print("  Then navigate to the target page before running this script.")
            else:
                print(f"  CDP connection error: {e}")
            raise

    @staticmethod
    def launch_headless(
        playwright: Playwright,
        viewport: dict = None
    ) -> Tuple[Browser, BrowserContext]:
        """Launch a fresh headless browser for public pages."""
        print("  Launching headless browser...")

        browser = playwright.chromium.launch(
            channel="chrome",
            headless=True,
            args=BROWSER_ARGS
        )

        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport=viewport or DEFAULT_VIEWPORT,
        )

        print("  Headless browser ready")
        return browser, context

    @staticmethod
    def launch_headed(
        playwright: Playwright,
        viewport: dict = None
    ) -> Tuple[Browser, BrowserContext]:
        """Launch a visible browser for debugging."""
        print("  Launching visible browser...")

        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
            args=BROWSER_ARGS
        )

        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport=viewport or DEFAULT_VIEWPORT,
        )

        print("  Visible browser ready")
        return browser, context


class StealthUtils:
    """Human-like interaction utilities"""

    @staticmethod
    def random_delay(min_ms: int = 100, max_ms: int = 500):
        """Add random delay"""
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

    @staticmethod
    def human_type(page: Page, selector: str, text: str, wpm_min: int = 320, wpm_max: int = 480):
        """Type with human-like speed"""
        element = page.query_selector(selector)
        if not element:
            try:
                element = page.wait_for_selector(selector, timeout=2000)
            except Exception:
                pass

        if not element:
            print(f"Element not found for typing: {selector}")
            return

        element.click()

        for char in text:
            element.type(char, delay=random.uniform(25, 75))
            if random.random() < 0.05:
                time.sleep(random.uniform(0.15, 0.4))

    @staticmethod
    def realistic_click(page: Page, selector: str):
        """Click with realistic movement"""
        element = page.query_selector(selector)
        if not element:
            return

        box = element.bounding_box()
        if box:
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2
            page.mouse.move(x, y, steps=5)

        StealthUtils.random_delay(100, 300)
        element.click()
        StealthUtils.random_delay(100, 300)


class ContentExtractor:
    """Extract and clean content from web pages"""

    @staticmethod
    def extract_main_content(page: Page) -> str:
        """Extract the main content area HTML, stripping noise elements."""
        # Try content selectors in order
        for selector in CONTENT_SELECTORS:
            element = page.query_selector(selector)
            if element:
                html = element.inner_html()
                return ContentExtractor.clean_html(html)

        # Fallback: use body
        body = page.query_selector('body')
        if body:
            html = body.inner_html()
            return ContentExtractor.clean_html(html)

        return page.content()

    @staticmethod
    def clean_html(html: str) -> str:
        """Remove noise elements and strip tags from HTML."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'lxml')

        # Remove noise elements
        for selector in NOISE_SELECTORS:
            for element in soup.select(selector):
                element.decompose()

        # Remove script/style/etc tags
        for tag_name in STRIP_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        return str(soup)

    @staticmethod
    def html_to_markdown(html: str) -> str:
        """Convert HTML to clean markdown."""
        from markdownify import markdownify as md

        markdown = md(
            html,
            heading_style="ATX",
            bullets="-",
            strip=['img', 'script', 'style', 'noscript', 'iframe'],
        )

        # Clean up excessive whitespace
        lines = markdown.split('\n')
        cleaned = []
        prev_empty = False
        for line in lines:
            stripped = line.rstrip()
            if not stripped:
                if not prev_empty:
                    cleaned.append('')
                prev_empty = True
            else:
                cleaned.append(stripped)
                prev_empty = False

        return '\n'.join(cleaned).strip()

    @staticmethod
    def extract_text(page: Page) -> str:
        """Extract visible text from page."""
        # Try main content first
        for selector in CONTENT_SELECTORS:
            element = page.query_selector(selector)
            if element:
                return element.inner_text().strip()

        # Fallback to body
        return page.inner_text('body').strip()

    @staticmethod
    def extract_metadata(page: Page) -> dict:
        """Extract page metadata (title, description, og:tags, canonical URL)."""
        metadata = {}

        # Title
        metadata['title'] = page.title()

        # Meta description
        desc = page.query_selector('meta[name="description"]')
        if desc:
            metadata['description'] = desc.get_attribute('content') or ''

        # Open Graph tags
        og_tags = page.query_selector_all('meta[property^="og:"]')
        for tag in og_tags:
            prop = tag.get_attribute('property')
            content = tag.get_attribute('content')
            if prop and content:
                key = prop.replace('og:', 'og_')
                metadata[key] = content

        # Canonical URL
        canonical = page.query_selector('link[rel="canonical"]')
        if canonical:
            metadata['canonical_url'] = canonical.get_attribute('href') or ''

        # Language
        html_tag = page.query_selector('html')
        if html_tag:
            lang = html_tag.get_attribute('lang')
            if lang:
                metadata['language'] = lang

        metadata['url'] = page.url

        return metadata

    @staticmethod
    def extract_links(page: Page, base_url: str = None) -> list:
        """Extract all links with text and absolute URLs."""
        if not base_url:
            base_url = page.url

        links = []
        anchors = page.query_selector_all('a[href]')

        for anchor in anchors:
            href = anchor.get_attribute('href')
            text = anchor.inner_text().strip()

            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)

            links.append({
                'text': text,
                'url': absolute_url,
                'href': href,
            })

        return links

    @staticmethod
    def extract_tables(page: Page, selector: str = None) -> list:
        """Extract all tables as structured data."""
        from bs4 import BeautifulSoup

        table_selector = selector or 'table'
        table_elements = page.query_selector_all(table_selector)

        tables = []
        for table_el in table_elements:
            html = table_el.inner_html()
            soup = BeautifulSoup(f'<table>{html}</table>', 'lxml')
            table = soup.find('table')

            if not table:
                continue

            # Extract headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                for th in header_row.find_all('th'):
                    headers.append(th.get_text(strip=True))
            else:
                # Try first row as header
                first_row = table.find('tr')
                if first_row:
                    ths = first_row.find_all('th')
                    if ths:
                        headers = [th.get_text(strip=True) for th in ths]

            # Extract rows
            rows = []
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr'):
                cells = tr.find_all(['td', 'th'])
                row = [cell.get_text(strip=True) for cell in cells]
                if row and row != headers:
                    rows.append(row)

            tables.append({
                'headers': headers,
                'rows': rows,
                'row_count': len(rows),
                'col_count': len(headers) if headers else (len(rows[0]) if rows else 0),
            })

        return tables


class PageWaiter:
    """Wait utilities for page loading and dynamic content"""

    @staticmethod
    def wait_for_content(page: Page, timeout: int = None):
        """Wait for page content to be loaded and network idle."""
        try:
            page.wait_for_load_state('networkidle', timeout=timeout or NETWORK_IDLE_TIMEOUT)
        except Exception:
            # Fallback: at least wait for DOM
            try:
                page.wait_for_load_state('domcontentloaded', timeout=5000)
            except Exception:
                pass

    @staticmethod
    def wait_for_selector(page: Page, selector: str, timeout: int = 10000):
        """Wait for a specific selector to appear."""
        page.wait_for_selector(selector, timeout=timeout, state="visible")

    @staticmethod
    def scroll_to_bottom(page: Page, scroll_delay_ms: int = 300, max_scrolls: int = 20):
        """Scroll to bottom incrementally for lazy-loaded content."""
        prev_height = 0

        for _ in range(max_scrolls):
            current_height = page.evaluate("document.body.scrollHeight")

            if current_height == prev_height:
                break

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(scroll_delay_ms / 1000)
            prev_height = current_height

        # Scroll back to top
        page.evaluate("window.scrollTo(0, 0)")
