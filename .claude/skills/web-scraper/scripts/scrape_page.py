#!/usr/bin/env python3
"""
Single Page Scraper - Core script for web content extraction
Supports headless and CDP modes, multiple output formats
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))

from patchright.sync_api import sync_playwright
from config import DEFAULT_CDP_URL, PAGE_LOAD_TIMEOUT, OUTPUT_FORMATS
from browser_utils import (
    BrowserFactory, StealthUtils, ContentExtractor, PageWaiter
)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def scrape_page(url, mode='headless', format='markdown', selector=None,
                wait_for=None, scroll=False, include_metadata=False,
                include_links=False, cdp_url=DEFAULT_CDP_URL,
                timeout=PAGE_LOAD_TIMEOUT, delay=0, javascript=None):
    """
    Scrape a single web page and extract content.

    Args:
        url: Page URL to scrape
        mode: 'headless' or 'cdp'
        format: Output format ('markdown', 'json', 'html', 'text')
        selector: CSS selector to extract specific element
        wait_for: Wait for specific selector before extracting
        scroll: Scroll to bottom for lazy-loaded content
        include_metadata: Include page metadata
        include_links: Include extracted links
        cdp_url: CDP endpoint URL
        timeout: Page load timeout in ms
        delay: Additional wait after load in ms
        javascript: JavaScript to execute before extraction

    Returns:
        dict with url, title, content, metadata, links, format, timestamp
    """
    playwright = None
    browser = None
    context = None
    page = None

    try:
        playwright = sync_playwright().start()

        # Connect or launch browser
        if mode == 'cdp':
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)
            # In CDP mode, check if page is already on the URL
            pages = context.pages
            page = None
            for p in pages:
                if url in p.url:
                    page = p
                    print(f"  Reusing existing tab: {p.url}")
                    break
            if not page:
                page = context.new_page()
                print(f"  Navigating to: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        else:
            browser, context = BrowserFactory.launch_headless(playwright)
            page = context.new_page()
            print(f"  Navigating to: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)

        # Wait for network idle
        PageWaiter.wait_for_content(page)

        # Wait for specific selector if requested
        if wait_for:
            print(f"  Waiting for selector: {wait_for}")
            PageWaiter.wait_for_selector(page, wait_for)

        # Scroll for lazy-loaded content
        if scroll:
            print("  Scrolling for lazy-loaded content...")
            PageWaiter.scroll_to_bottom(page)

        # Additional delay
        if delay > 0:
            StealthUtils.random_delay(delay, delay + 200)

        # Execute custom JavaScript
        if javascript:
            print("  Executing custom JavaScript...")
            page.evaluate(javascript)
            time.sleep(0.5)

        # Extract content
        print("  Extracting content...")
        result = {
            'url': page.url,
            'title': page.title(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'format': format,
        }

        if selector:
            # Extract specific element
            element = page.query_selector(selector)
            if element:
                html = element.inner_html()
                html = ContentExtractor.clean_html(html)
            else:
                print(f"  Warning: Selector '{selector}' not found, using full page")
                html = ContentExtractor.extract_main_content(page)
        else:
            html = ContentExtractor.extract_main_content(page)

        # Convert to requested format
        if format == 'markdown':
            result['content'] = ContentExtractor.html_to_markdown(html)
        elif format == 'html':
            result['content'] = html
        elif format == 'text':
            if selector:
                element = page.query_selector(selector)
                result['content'] = element.inner_text().strip() if element else ContentExtractor.extract_text(page)
            else:
                result['content'] = ContentExtractor.extract_text(page)
        elif format == 'json':
            result['content'] = ContentExtractor.html_to_markdown(html)

        # Optional metadata
        if include_metadata:
            result['metadata'] = ContentExtractor.extract_metadata(page)

        # Optional links
        if include_links:
            result['links'] = ContentExtractor.extract_links(page)

        print(f"  Extracted {len(result['content'])} characters")
        return result

    finally:
        # Cleanup
        if mode == 'cdp':
            # CDP: disconnect only, don't close user's browser
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
        else:
            # Headless: close everything
            if context:
                try:
                    context.close()
                except Exception:
                    pass
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass

        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def format_output(result: dict, output_format: str) -> str:
    """Format scraped result for display/saving."""
    if output_format == 'json':
        return json.dumps(result, indent=2, ensure_ascii=False)

    # For markdown/text/html, output content with optional header
    parts = []
    if result.get('metadata'):
        meta = result['metadata']
        parts.append(f"# {meta.get('title', result.get('title', 'Untitled'))}")
        parts.append(f"")
        parts.append(f"**URL:** {result['url']}")
        if meta.get('description'):
            parts.append(f"**Description:** {meta['description']}")
        parts.append(f"**Scraped:** {result['timestamp']}")
        parts.append(f"")
        parts.append("---")
        parts.append("")

    parts.append(result['content'])

    if result.get('links'):
        parts.append("")
        parts.append("---")
        parts.append("")
        parts.append("## Links")
        parts.append("")
        for link in result['links'][:50]:  # Limit to 50 links
            text = link['text'][:80] if link['text'] else link['url']
            parts.append(f"- [{text}]({link['url']})")

    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(
        description='Scrape a single web page and extract content'
    )

    # Required
    parser.add_argument('--url', required=True, help='Page URL to scrape')

    # Mode
    parser.add_argument('--mode', choices=['headless', 'cdp'], default='headless',
                        help='Browser mode (default: headless)')
    parser.add_argument('--cdp-url', default=DEFAULT_CDP_URL,
                        help=f'CDP endpoint (default: {DEFAULT_CDP_URL})')

    # Content options
    parser.add_argument('--format', choices=OUTPUT_FORMATS, default='markdown',
                        help='Output format (default: markdown)')
    parser.add_argument('--selector', help='CSS selector to extract specific element')
    parser.add_argument('--wait-for', help='Wait for specific selector before extracting')
    parser.add_argument('--scroll', action='store_true',
                        help='Scroll to bottom for lazy-loaded content')

    # Output
    parser.add_argument('--output', help='Save to file (default: print to stdout)')
    parser.add_argument('--include-metadata', action='store_true',
                        help='Include page metadata')
    parser.add_argument('--include-links', action='store_true',
                        help='Include extracted links')

    # Advanced
    parser.add_argument('--timeout', type=int, default=PAGE_LOAD_TIMEOUT,
                        help=f'Page load timeout in ms (default: {PAGE_LOAD_TIMEOUT})')
    parser.add_argument('--delay', type=int, default=0,
                        help='Additional wait after load in ms (default: 0)')
    parser.add_argument('--javascript', help='Execute JavaScript before extraction')

    args = parser.parse_args()

    print(f"Scraping: {args.url}")
    print(f"  Mode: {args.mode} | Format: {args.format}")

    result = scrape_page(
        url=args.url,
        mode=args.mode,
        format=args.format,
        selector=args.selector,
        wait_for=args.wait_for,
        scroll=args.scroll,
        include_metadata=args.include_metadata,
        include_links=args.include_links,
        cdp_url=args.cdp_url,
        timeout=args.timeout,
        delay=args.delay,
        javascript=args.javascript,
    )

    output = format_output(result, args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')
        print(f"\nSaved to: {output_path}")
    else:
        print("\n--- Content ---\n")
        print(output)


if __name__ == "__main__":
    main()
