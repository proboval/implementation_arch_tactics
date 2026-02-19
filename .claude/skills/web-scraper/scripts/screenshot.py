#!/usr/bin/env python3
"""
Page Screenshot - Capture web page screenshots
Supports headless and CDP modes, full-page and element screenshots
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from patchright.sync_api import sync_playwright
from config import (
    DEFAULT_CDP_URL, PAGE_LOAD_TIMEOUT, SCREENSHOTS_DIR, DEFAULT_VIEWPORT
)
from browser_utils import BrowserFactory, StealthUtils, PageWaiter

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def take_screenshot(url, output=None, full_page=True, viewport=None,
                    selector=None, wait_for=None, delay=1000,
                    format='png', quality=80,
                    mode='headless', cdp_url=DEFAULT_CDP_URL,
                    timeout=PAGE_LOAD_TIMEOUT):
    """
    Take a screenshot of a web page.

    Returns: path to saved screenshot file
    """
    playwright = None
    browser = None
    context = None
    page = None

    # Determine output path
    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        domain = url.split('//')[1].split('/')[0].replace('.', '_') if '//' in url else 'page'
        output = str(SCREENSHOTS_DIR / f"{domain}_{timestamp}.{format}")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        playwright = sync_playwright().start()

        # Parse viewport
        vp = viewport or DEFAULT_VIEWPORT
        if isinstance(vp, str) and 'x' in vp:
            w, h = vp.split('x')
            vp = {'width': int(w), 'height': int(h)}

        # Connect or launch browser
        if mode == 'cdp':
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)
            pages = context.pages
            page = None
            for p in pages:
                if url in p.url:
                    page = p
                    break
            if not page:
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        else:
            browser, context = BrowserFactory.launch_headless(playwright, viewport=vp)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)

        # Wait for content
        PageWaiter.wait_for_content(page)

        # Wait for specific selector
        if wait_for:
            PageWaiter.wait_for_selector(page, wait_for)

        # Additional delay for rendering
        if delay > 0:
            StealthUtils.random_delay(delay, delay + 200)

        # Take screenshot
        screenshot_kwargs = {
            'path': str(output_path),
            'type': format,
        }

        if selector:
            # Screenshot specific element
            element = page.query_selector(selector)
            if element:
                element.screenshot(**screenshot_kwargs)
                print(f"  Element screenshot saved: {output_path}")
            else:
                print(f"  Warning: Selector '{selector}' not found, taking full page screenshot")
                screenshot_kwargs['full_page'] = full_page
                if format == 'jpeg':
                    screenshot_kwargs['quality'] = quality
                page.screenshot(**screenshot_kwargs)
        else:
            screenshot_kwargs['full_page'] = full_page
            if format == 'jpeg':
                screenshot_kwargs['quality'] = quality
            page.screenshot(**screenshot_kwargs)

        file_size = output_path.stat().st_size
        print(f"  Screenshot saved: {output_path} ({file_size / 1024:.1f} KB)")
        return str(output_path)

    finally:
        if mode == 'cdp':
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


def main():
    parser = argparse.ArgumentParser(
        description='Take a screenshot of a web page'
    )

    parser.add_argument('--url', required=True, help='Page URL to screenshot')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--full-page', action='store_true', default=True,
                        help='Capture full page (default: true)')
    parser.add_argument('--no-full-page', action='store_true',
                        help='Capture viewport only')
    parser.add_argument('--viewport', help='Viewport size WxH (default: 1920x1080)')
    parser.add_argument('--selector', help='Screenshot specific element only')
    parser.add_argument('--wait-for', help='Wait for selector before screenshot')
    parser.add_argument('--delay', type=int, default=1000,
                        help='Wait after load before screenshot in ms (default: 1000)')
    parser.add_argument('--format', choices=['png', 'jpeg'], default='png',
                        help='Image format (default: png)')
    parser.add_argument('--quality', type=int, default=80,
                        help='JPEG quality 0-100 (default: 80)')
    parser.add_argument('--mode', choices=['headless', 'cdp'], default='headless',
                        help='Browser mode (default: headless)')
    parser.add_argument('--cdp-url', default=DEFAULT_CDP_URL,
                        help=f'CDP endpoint (default: {DEFAULT_CDP_URL})')
    parser.add_argument('--timeout', type=int, default=PAGE_LOAD_TIMEOUT,
                        help=f'Page load timeout in ms (default: {PAGE_LOAD_TIMEOUT})')

    args = parser.parse_args()

    full_page = not args.no_full_page

    print(f"Taking screenshot: {args.url}")
    print(f"  Mode: {args.mode} | Full page: {full_page} | Format: {args.format}")

    result = take_screenshot(
        url=args.url,
        output=args.output,
        full_page=full_page,
        viewport=args.viewport,
        selector=args.selector,
        wait_for=args.wait_for,
        delay=args.delay,
        format=args.format,
        quality=args.quality,
        mode=args.mode,
        cdp_url=args.cdp_url,
        timeout=args.timeout,
    )

    print(f"\nScreenshot: {result}")


if __name__ == "__main__":
    main()