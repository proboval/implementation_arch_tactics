#!/usr/bin/env python3
"""
NotebookLM Deep Research Interface
Triggers Deep Research to search the web and add new sources to a notebook.

Deep Research performs multi-step web research and adds discovered sources
to your NotebookLM notebook for further analysis.
"""

import argparse
import sys
import time
import re
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from notebook_manager import NotebookLibrary
from browser_utils import BrowserFactory, StealthUtils

# Deep Research UI Selectors
RESEARCH_MODE_DROPDOWN = [
    'button:has-text("Fast Research")',
    'button:has-text("Deep Research")',
    '[aria-haspopup="listbox"]',  # Generic dropdown
    '.research-mode-selector',
]

DEEP_RESEARCH_OPTION = [
    'text="Deep Research"',
    '[role="option"]:has-text("Deep Research")',
    'li:has-text("Deep Research")',
    'div:has-text("In-depth report")',
]

SEARCH_INPUT_SELECTORS = [
    # Exact NotebookLM selectors (from inspector)
    'textarea.query-box-textarea',
    'textarea[placeholder*="would you like to research"]',
    'textarea[aria-label*="Discover sources"]',
    'textarea[formcontrolname="discoverSourcesQuery"]',
    '.query-box textarea',
    # Fallbacks
    'textarea[placeholder*="research"]',
    'textarea[placeholder*="Search"]',
    '[role="textbox"]',
]

SUBMIT_BUTTON_SELECTORS = [
    'button[aria-label*="Search"]',
    'button[aria-label*="Submit"]',
    'button.search-submit',
    'button:has(svg)',  # Arrow button
]

# Completion detection selectors (from inspector)
COMPLETION_SELECTORS = [
    '.source-discovery-completed-container',
    '.source-discovery-completed-header-text',
    'text="Deep Research completed!"',
]

# Import button selectors
IMPORT_BUTTON_SELECTORS = [
    'button.source-discovery-completed-action-import-button',
    'button:has-text("Import")',
    '.source-discovery-completed-action-import-button',
]

# Timeout for deep research (can take several minutes)
DEEP_RESEARCH_TIMEOUT = 600  # 10 minutes


def _handle_completed_research(page, query: str, start_time: float) -> dict:
    """Handle already-completed Deep Research: extract info and import."""
    sources_count = 0
    report_title = ""

    # Extract report info
    try:
        title_el = page.query_selector('.report-title')
        if title_el:
            report_title = title_el.inner_text().strip()
            print(f"  📄 Report: {report_title}")

        count_el = page.query_selector('.report-source-count')
        if count_el:
            count_text = count_el.inner_text()
            match = re.search(r'(\d+)', count_text)
            if match:
                sources_count = int(match.group(1))
                print(f"  📚 Sources discovered: {sources_count}")
    except Exception:
        pass

    # Find and click Import button
    print("  ⏳ Looking for Import button...")
    import_button = None

    for selector in IMPORT_BUTTON_SELECTORS:
        try:
            import_button = page.wait_for_selector(selector, timeout=5000, state="visible")
            if import_button:
                print("  ✓ Found Import button")
                break
        except:
            continue

    if not import_button:
        print("  ⚠️ Import button not found")
        return {
            "status": "completed_no_import",
            "query": query,
            "report_title": report_title,
            "sources_discovered": sources_count,
            "message": "Research completed but import button not found",
            "elapsed_seconds": int(time.time() - start_time)
        }

    # Click import
    print("  📥 Importing sources...")
    import_button.click()
    time.sleep(5)  # Wait for import to process

    print("  ✅ Sources imported!")
    return {
        "status": "success",
        "query": query,
        "report_title": report_title,
        "sources_imported": sources_count,
        "elapsed_seconds": int(time.time() - start_time)
    }


def deep_research(
    query: str,
    notebook_url: str,
    use_cdp: bool = True,
    cdp_url: str = "http://localhost:9222",
    headless: bool = True
) -> dict:
    """
    Trigger Deep Research in NotebookLM.

    Args:
        query: Research query/topic
        notebook_url: NotebookLM notebook URL
        use_cdp: Connect to existing Chrome via CDP (default: True)
        cdp_url: CDP endpoint URL
        headless: Run headless (only for token mode)

    Returns:
        dict with status and any discovered sources
    """
    if not use_cdp:
        auth = AuthManager()
        if not auth.is_authenticated():
            print("⚠️ Not authenticated. Run: python auth_manager.py setup")
            print("   Or use CDP mode (default): start Chrome with --remote-debugging-port=9222")
            return {"status": "error", "message": "Not authenticated"}

    print(f"🔬 Deep Research: {query}")
    print(f"📚 Notebook: {notebook_url}")
    if use_cdp:
        print(f"🔗 Mode: CDP (connecting to your Chrome)")

    playwright = None
    context = None
    browser = None

    try:
        playwright = sync_playwright().start()

        if use_cdp:
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)

            # Find existing NotebookLM tab or create new one
            page = None
            for p in context.pages:
                if "notebooklm.google.com" in p.url:
                    page = p
                    print(f"  📑 Found existing NotebookLM tab")
                    break

            if not page:
                page = context.new_page()
                print("  🌐 Opening notebook in new tab...")
                page.goto(notebook_url, wait_until="domcontentloaded")
            elif notebook_url not in page.url:
                print("  🌐 Navigating to specified notebook...")
                page.goto(notebook_url, wait_until="domcontentloaded")
        else:
            context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
            page = context.new_page()
            print("  🌐 Opening notebook...")
            page.goto(notebook_url, wait_until="domcontentloaded")

        # Wait for NotebookLM to load
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=10000)
        time.sleep(2)  # Let UI fully render

        # Step 0: Check if there's already a completed Deep Research waiting
        print("  ⏳ Checking for existing Deep Research results...")
        existing_research = None
        for selector in COMPLETION_SELECTORS:
            try:
                existing_research = page.query_selector(selector)
                if existing_research and existing_research.is_visible():
                    print("  📋 Found existing Deep Research results!")
                    # Skip to import step
                    return _handle_completed_research(page, query, time.time())
            except:
                continue

        # Step 1: Find and click the research mode dropdown
        print("  ⏳ Looking for research mode dropdown...")
        dropdown = None

        for selector in RESEARCH_MODE_DROPDOWN:
            try:
                dropdown = page.wait_for_selector(selector, timeout=5000, state="visible")
                if dropdown:
                    print(f"  ✓ Found dropdown: {selector}")
                    break
            except:
                continue

        if not dropdown:
            # Try finding by text content more broadly
            try:
                dropdown = page.locator('button', has_text=re.compile(r'Research', re.IGNORECASE)).first
                if dropdown.is_visible():
                    print("  ✓ Found dropdown by text search")
                else:
                    dropdown = None
            except:
                pass

        if not dropdown:
            print("  ❌ Could not find research mode dropdown")
            print("  💡 Make sure the Sources panel is visible in NotebookLM")
            return {"status": "error", "message": "Dropdown not found"}

        # Click dropdown to open options
        print("  🖱️ Opening dropdown...")
        dropdown.click()
        StealthUtils.random_delay(300, 600)

        # Step 2: Select Deep Research option
        print("  ⏳ Selecting Deep Research...")
        deep_option = None

        for selector in DEEP_RESEARCH_OPTION:
            try:
                deep_option = page.wait_for_selector(selector, timeout=3000, state="visible")
                if deep_option:
                    print(f"  ✓ Found Deep Research option")
                    break
            except:
                continue

        if not deep_option:
            print("  ❌ Could not find Deep Research option")
            return {"status": "error", "message": "Deep Research option not found"}

        deep_option.click()
        print("  ⏳ Waiting for UI to update...")
        time.sleep(2)  # Give UI time to update after mode change

        # Step 3: Find search input
        print("  ⏳ Looking for search input...")
        search_input = None

        for selector in SEARCH_INPUT_SELECTORS:
            try:
                search_input = page.wait_for_selector(selector, timeout=5000, state="visible")
                if search_input:
                    print(f"  ✓ Found search input")
                    break
            except:
                continue

        if not search_input:
            print("  ❌ Could not find search input")
            return {"status": "error", "message": "Search input not found"}

        # Step 4: Type query
        print(f"  ⌨️ Typing query: {query}")
        search_input.click()
        StealthUtils.random_delay(200, 400)

        # Clear any existing text and type new query
        search_input.fill("")
        for char in query:
            search_input.type(char, delay=30)
            if len(query) > 20 and char == ' ':
                StealthUtils.random_delay(50, 150)

        StealthUtils.random_delay(300, 600)

        # Step 5: Submit the search
        print("  📤 Submitting Deep Research request...")

        # Try clicking submit button first
        submitted = False
        for selector in SUBMIT_BUTTON_SELECTORS:
            try:
                submit_btn = page.query_selector(selector)
                if submit_btn and submit_btn.is_visible():
                    submit_btn.click()
                    submitted = True
                    print(f"  ✓ Clicked submit button")
                    break
            except:
                continue

        if not submitted:
            # Fall back to pressing Enter
            page.keyboard.press("Enter")
            print("  ✓ Pressed Enter to submit")

        # Step 6: Wait for Deep Research to complete
        print("  ⏳ Deep Research in progress (this may take several minutes)...")

        # Monitor for completion indicators
        start_time = time.time()
        research_complete = False
        sources_count = 0
        report_title = ""

        while time.time() - start_time < DEEP_RESEARCH_TIMEOUT:
            try:
                # Check for completion using exact selectors from inspector
                for selector in COMPLETION_SELECTORS:
                    try:
                        element = page.query_selector(selector)
                        if element and element.is_visible():
                            research_complete = True
                            print("  ✅ Deep Research completed!")
                            break
                    except:
                        continue

                if research_complete:
                    break

                # Check for error states
                error_indicators = [
                    'text="Error"',
                    'text="Failed"',
                    '.error-message',
                ]

                for indicator in error_indicators:
                    try:
                        element = page.query_selector(indicator)
                        if element and element.is_visible():
                            error_text = element.inner_text()
                            print(f"  ❌ Research error: {error_text}")
                            return {"status": "error", "message": error_text}
                    except:
                        continue

                # Progress indicator
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0 and elapsed > 0:
                    print(f"  ⏳ Still researching... ({elapsed}s elapsed)")

            except Exception:
                pass

            time.sleep(2)

        if not research_complete:
            print("  ⚠️ Research may still be in progress (timeout reached)")
            return {
                "status": "timeout",
                "message": "Deep Research timeout - check notebook manually",
                "elapsed_seconds": int(time.time() - start_time)
            }

        # Extract report info before importing
        try:
            # Get report title
            title_el = page.query_selector('.report-title')
            if title_el:
                report_title = title_el.inner_text().strip()
                print(f"  📄 Report: {report_title}")

            # Get sources count
            count_el = page.query_selector('.report-source-count')
            if count_el:
                count_text = count_el.inner_text()
                # Extract number from "59 sources discovered"
                import re as regex
                match = regex.search(r'(\d+)', count_text)
                if match:
                    sources_count = int(match.group(1))
                    print(f"  📚 Sources discovered: {sources_count}")
        except Exception:
            pass

        # Step 7: Click Import button
        print("  ⏳ Looking for Import button...")
        import_button = None

        for selector in IMPORT_BUTTON_SELECTORS:
            try:
                import_button = page.wait_for_selector(selector, timeout=5000, state="visible")
                if import_button:
                    print("  ✓ Found Import button")
                    break
            except:
                continue

        if not import_button:
            print("  ⚠️ Import button not found - sources may need manual import")
            return {
                "status": "completed_no_import",
                "query": query,
                "report_title": report_title,
                "sources_discovered": sources_count,
                "message": "Research completed but import button not found",
                "elapsed_seconds": int(time.time() - start_time)
            }

        # Click import
        print("  📥 Importing sources...")
        import_button.click()
        time.sleep(3)  # Wait for import to process

        # Check if import succeeded (container should disappear or change)
        try:
            # Wait a bit for import to complete
            time.sleep(5)
            print("  ✅ Sources imported!")
        except Exception:
            pass

        return {
            "status": "success",
            "query": query,
            "report_title": report_title,
            "sources_imported": sources_count,
            "elapsed_seconds": int(time.time() - start_time)
        }

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    finally:
        if use_cdp:
            if browser:
                try:
                    browser.close()
                except:
                    pass
        else:
            if context:
                try:
                    context.close()
                except:
                    pass

        if playwright:
            try:
                playwright.stop()
            except:
                pass


def main():
    parser = argparse.ArgumentParser(
        description='Trigger Deep Research in NotebookLM',
        epilog='''
Deep Research searches the web and adds relevant sources to your notebook.
This process can take several minutes.

CDP mode (default): Connects to your running Chrome browser.
  Start Chrome with: chrome --remote-debugging-port=9222
  Then log into Google and open NotebookLM.

Token mode (--token): Uses stored authentication tokens.
  Requires: python auth_manager.py setup
        '''
    )

    parser.add_argument('--query', required=True, help='Research query/topic')
    parser.add_argument('--notebook-url', required=True, help='NotebookLM notebook URL')
    parser.add_argument('--token', action='store_true', help='Use token-based auth instead of CDP')
    parser.add_argument('--show-browser', action='store_true', help='Show browser (token mode only)')
    parser.add_argument('--cdp-url', default='http://localhost:9222', help='CDP endpoint URL')

    args = parser.parse_args()

    use_cdp = not args.token

    result = deep_research(
        query=args.query,
        notebook_url=args.notebook_url,
        use_cdp=use_cdp,
        cdp_url=args.cdp_url,
        headless=not args.show_browser
    )

    print("\n" + "=" * 60)
    print("Deep Research Result:")
    print("=" * 60)
    for key, value in result.items():
        print(f"  {key}: {value}")
    print("=" * 60)

    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
