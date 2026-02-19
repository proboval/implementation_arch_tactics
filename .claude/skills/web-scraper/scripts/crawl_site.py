#!/usr/bin/env python3
"""
Site Crawler - Multi-page BFS crawler with depth control
Scrapes related pages starting from a URL
"""

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).parent))

from patchright.sync_api import sync_playwright
from config import (
    DEFAULT_CDP_URL, PAGE_LOAD_TIMEOUT, MAX_CRAWL_DEPTH, MAX_CRAWL_PAGES,
    CRAWL_DELAY_MIN_MS, CRAWL_DELAY_MAX_MS,
)
from browser_utils import (
    BrowserFactory, StealthUtils, ContentExtractor, PageWaiter
)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class SiteCrawler:
    """Multi-page BFS crawler with depth control and domain filtering."""

    def __init__(self, context, same_domain=True, pattern=None, exclude=None):
        self.context = context
        self.same_domain = same_domain
        self.pattern = re.compile(pattern) if pattern else None
        self.exclude = re.compile(exclude) if exclude else None
        self.visited = set()
        self.results = []

    def crawl(self, start_url, max_depth=1, max_pages=20, format='markdown',
              selector=None):
        """
        BFS crawl starting from URL.

        Args:
            start_url: Starting URL
            max_depth: Maximum link-following depth
            max_pages: Maximum pages to scrape
            format: Output format for content
            selector: CSS selector for content on each page

        Returns:
            list of page result dicts
        """
        start_domain = urlparse(start_url).netloc

        # BFS queue: (url, depth)
        queue = deque([(start_url, 0)])
        self.visited.add(start_url)

        while queue and len(self.results) < max_pages:
            url, depth = queue.popleft()

            print(f"  [{len(self.results) + 1}/{max_pages}] Depth {depth}: {url}")

            # Scrape page
            result = self._scrape_single(url, format, selector)
            if result:
                result['depth'] = depth
                self.results.append(result)

                # Extract and queue links if we haven't hit max depth
                if depth < max_depth and result.get('links'):
                    for link in result['links']:
                        link_url = link['url']

                        # Skip already visited
                        if link_url in self.visited:
                            continue

                        # Check filters
                        if self._should_follow(link_url, start_domain):
                            self.visited.add(link_url)
                            queue.append((link_url, depth + 1))

            # Respectful delay between requests
            if queue:
                StealthUtils.random_delay(CRAWL_DELAY_MIN_MS, CRAWL_DELAY_MAX_MS)

        print(f"\n  Crawl complete: {len(self.results)} pages scraped")
        return self.results

    def _should_follow(self, url, start_domain):
        """Check if URL should be followed based on filters."""
        parsed = urlparse(url)

        # Skip non-HTTP(S)
        if parsed.scheme not in ('http', 'https', ''):
            return False

        # Skip common non-page extensions
        path_lower = parsed.path.lower()
        skip_extensions = ('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.svg',
                          '.zip', '.tar', '.gz', '.mp4', '.mp3', '.css', '.js')
        if any(path_lower.endswith(ext) for ext in skip_extensions):
            return False

        # Same domain check
        if self.same_domain and parsed.netloc and parsed.netloc != start_domain:
            return False

        # Pattern filter
        if self.pattern and not self.pattern.search(url):
            return False

        # Exclude filter
        if self.exclude and self.exclude.search(url):
            return False

        return True

    def _scrape_single(self, url, format, selector):
        """Scrape a single page within the crawl context."""
        page = None
        try:
            page = self.context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT)
            PageWaiter.wait_for_content(page)

            result = {
                'url': page.url,
                'title': page.title(),
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }

            # Extract content
            if selector:
                element = page.query_selector(selector)
                if element:
                    html = ContentExtractor.clean_html(element.inner_html())
                else:
                    html = ContentExtractor.extract_main_content(page)
            else:
                html = ContentExtractor.extract_main_content(page)

            if format == 'markdown':
                result['content'] = ContentExtractor.html_to_markdown(html)
            else:
                result['content'] = html

            # Extract links for crawling
            result['links'] = ContentExtractor.extract_links(page)

            return result

        except Exception as e:
            print(f"    Error scraping {url}: {e}")
            return None

        finally:
            if page:
                try:
                    page.close()
                except Exception:
                    pass


def generate_index(results):
    """Generate a summary index of crawled pages."""
    lines = [
        "# Crawl Index",
        "",
        f"**Pages crawled:** {len(results)}",
        f"**Timestamp:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "| # | Depth | Title | URL | Content Length |",
        "|---|-------|-------|-----|---------------|",
    ]

    for i, r in enumerate(results):
        title = (r['title'] or 'Untitled')[:50]
        content_len = len(r.get('content', ''))
        lines.append(f"| {i+1} | {r.get('depth', 0)} | {title} | {r['url']} | {content_len} chars |")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Crawl multiple web pages starting from a URL'
    )

    # Required
    parser.add_argument('--url', required=True, help='Starting URL to crawl')

    # Crawl control
    parser.add_argument('--depth', type=int, default=1,
                        help=f'Maximum crawl depth (default: 1, max: {MAX_CRAWL_DEPTH})')
    parser.add_argument('--max-pages', type=int, default=20,
                        help=f'Maximum pages to crawl (default: 20, max: {MAX_CRAWL_PAGES})')
    parser.add_argument('--same-domain', action='store_true', default=True,
                        help='Only follow same-domain links (default: true)')
    parser.add_argument('--no-same-domain', action='store_true',
                        help='Follow cross-domain links')
    parser.add_argument('--pattern', help='Only follow links matching regex pattern')
    parser.add_argument('--exclude', help='Exclude links matching regex pattern')

    # Mode
    parser.add_argument('--mode', choices=['headless', 'cdp'], default='headless',
                        help='Browser mode (default: headless)')
    parser.add_argument('--cdp-url', default=DEFAULT_CDP_URL,
                        help=f'CDP endpoint (default: {DEFAULT_CDP_URL})')

    # Content
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                        help='Output format (default: markdown)')
    parser.add_argument('--selector', help='CSS selector for content on each page')

    # Output
    parser.add_argument('--output-dir', help='Save each page as separate file')
    parser.add_argument('--output', help='Save all results to single file')
    parser.add_argument('--index', action='store_true',
                        help='Generate index/summary of crawled pages')

    args = parser.parse_args()

    # Enforce safety limits
    depth = min(args.depth, MAX_CRAWL_DEPTH)
    max_pages = min(args.max_pages, MAX_CRAWL_PAGES)
    same_domain = not args.no_same_domain

    print(f"Crawling: {args.url}")
    print(f"  Depth: {depth} | Max pages: {max_pages} | Same domain: {same_domain}")
    if args.pattern:
        print(f"  Pattern: {args.pattern}")
    if args.exclude:
        print(f"  Exclude: {args.exclude}")

    playwright = None
    browser = None
    context = None

    try:
        playwright = sync_playwright().start()

        if args.mode == 'cdp':
            browser, context = BrowserFactory.connect_to_cdp(playwright, args.cdp_url)
        else:
            browser, context = BrowserFactory.launch_headless(playwright)

        crawler = SiteCrawler(
            context=context,
            same_domain=same_domain,
            pattern=args.pattern,
            exclude=args.exclude,
        )

        results = crawler.crawl(
            start_url=args.url,
            max_depth=depth,
            max_pages=max_pages,
            format=args.format,
            selector=args.selector,
        )

        if not results:
            print("\nNo pages crawled")
            return

        # Output results
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            ext = '.md' if args.format == 'markdown' else '.json'
            for i, r in enumerate(results):
                # Create safe filename from title
                safe_title = re.sub(r'[^\w\-]', '_', r['title'] or f'page_{i}')[:60]
                file_path = output_dir / f"{i:03d}_{safe_title}{ext}"

                if args.format == 'json':
                    content = json.dumps(r, indent=2, ensure_ascii=False)
                else:
                    content = f"# {r['title']}\n\n**URL:** {r['url']}\n\n---\n\n{r['content']}"

                file_path.write_text(content, encoding='utf-8')

            print(f"\nSaved {len(results)} pages to: {output_dir}")

            # Generate index
            if args.index:
                index_path = output_dir / "INDEX.md"
                index_path.write_text(generate_index(results), encoding='utf-8')
                print(f"  Index: {index_path}")

        elif args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if args.format == 'json':
                # Strip links from JSON output (too verbose)
                clean_results = []
                for r in results:
                    clean = {k: v for k, v in r.items() if k != 'links'}
                    clean_results.append(clean)
                content = json.dumps(clean_results, indent=2, ensure_ascii=False)
            else:
                parts = []
                for r in results:
                    parts.append(f"# {r['title']}")
                    parts.append(f"\n**URL:** {r['url']}\n")
                    parts.append("---\n")
                    parts.append(r['content'])
                    parts.append("\n\n")
                content = '\n'.join(parts)

            output_path.write_text(content, encoding='utf-8')
            print(f"\nSaved to: {output_path}")

        else:
            # Print index + content summary
            if args.index:
                print("\n" + generate_index(results))
            else:
                for r in results:
                    print(f"\n--- {r['title']} ({r['url']}) ---")
                    # Truncate content for stdout display
                    content = r['content'][:500]
                    if len(r['content']) > 500:
                        content += f"\n... ({len(r['content'])} chars total)"
                    print(content)

    finally:
        if args.mode == 'cdp':
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass
        else:
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


if __name__ == "__main__":
    main()