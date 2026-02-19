#!/usr/bin/env python3
"""
Simple NotebookLM Question Interface
Based on MCP server implementation - simplified without sessions

Implements hybrid auth approach:
- Persistent browser profile (user_data_dir) for fingerprint consistency
- Manual cookie injection from state.json for session cookies (Playwright bug workaround)
See: https://github.com/microsoft/playwright/issues/36139
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
from config import QUERY_INPUT_SELECTORS, RESPONSE_SELECTORS
from browser_utils import BrowserFactory, StealthUtils


# Follow-up reminder (adapted from MCP server for stateless operation)
# Since we don't have persistent sessions, we encourage comprehensive questions
FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question "
    "that includes all necessary context (since each question opens a new browser session)."
)


def ask_notebooklm(question: str, notebook_url: str, headless: bool = True, use_cdp: bool = True, cdp_url: str = "http://localhost:9222") -> str:
    """
    Ask a question to NotebookLM

    Args:
        question: Question to ask
        notebook_url: NotebookLM notebook URL
        headless: Run browser in headless mode (only used in token mode)
        use_cdp: Connect to existing Chrome via CDP (default: True, recommended)
        cdp_url: CDP endpoint URL (default: http://localhost:9222)

    Returns:
        Answer text from NotebookLM
    """
    # In token mode, check authentication
    if not use_cdp:
        auth = AuthManager()
        if not auth.is_authenticated():
            print("⚠️ Not authenticated. Run: python auth_manager.py setup")
            print("   Or use CDP mode (default): start Chrome with --remote-debugging-port=9222")
            return None

    print(f"💬 Asking: {question}")
    print(f"📚 Notebook: {notebook_url}")
    if use_cdp:
        print(f"🔗 Mode: CDP (connecting to your Chrome)")

    playwright = None
    context = None
    browser = None  # Only used in CDP mode

    try:
        # Start playwright
        playwright = sync_playwright().start()

        if use_cdp:
            # Connect to existing Chrome via CDP
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)

            # In CDP mode, find existing NotebookLM tab or create new one
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
                # Navigate to correct notebook if different
                print("  🌐 Navigating to specified notebook...")
                page.goto(notebook_url, wait_until="domcontentloaded")
        else:
            # Launch persistent browser context using factory
            context = BrowserFactory.launch_persistent_context(
                playwright,
                headless=headless
            )
            # Navigate to notebook
            page = context.new_page()
            print("  🌐 Opening notebook...")
            page.goto(notebook_url, wait_until="domcontentloaded")

        # Wait for NotebookLM
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=10000)

        # Wait for query input (MCP approach)
        print("  ⏳ Waiting for query input...")
        query_element = None

        for selector in QUERY_INPUT_SELECTORS:
            try:
                query_element = page.wait_for_selector(
                    selector,
                    timeout=10000,
                    state="visible"  # Only check visibility, not disabled!
                )
                if query_element:
                    print(f"  ✓ Found input: {selector}")
                    break
            except:
                continue

        if not query_element:
            print("  ❌ Could not find query input")
            return None

        # Type question (human-like, fast)
        print("  ⏳ Typing question...")
        
        # Use primary selector for typing
        input_selector = QUERY_INPUT_SELECTORS[0]
        StealthUtils.human_type(page, input_selector, question)

        # Submit
        print("  📤 Submitting...")
        page.keyboard.press("Enter")

        # Small pause
        StealthUtils.random_delay(500, 1500)

        # Wait for response (MCP approach: poll for stable text)
        print("  ⏳ Waiting for answer...")

        answer = None
        stable_count = 0
        last_text = None
        deadline = time.time() + 120  # 2 minutes timeout

        while time.time() < deadline:
            # Check if NotebookLM is still thinking (most reliable indicator)
            try:
                thinking_element = page.query_selector('div.thinking-message')
                if thinking_element and thinking_element.is_visible():
                    time.sleep(1)
                    continue
            except:
                pass

            # Try to find response with MCP selectors
            for selector in RESPONSE_SELECTORS:
                try:
                    elements = page.query_selector_all(selector)
                    if elements:
                        # Get last (newest) response
                        latest = elements[-1]
                        text = latest.inner_text().strip()

                        if text:
                            if text == last_text:
                                stable_count += 1
                                if stable_count >= 3:  # Stable for 3 polls
                                    answer = text
                                    break
                            else:
                                stable_count = 0
                                last_text = text
                except:
                    continue

            if answer:
                break

            time.sleep(1)

        if not answer:
            print("  ❌ Timeout waiting for answer")
            return None

        print("  ✅ Got answer!")
        # Add follow-up reminder to encourage Claude to ask more questions
        return answer + FOLLOW_UP_REMINDER

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        # Clean up - but handle CDP differently
        if use_cdp:
            # In CDP mode, just disconnect - don't close the user's browser!
            if browser:
                try:
                    browser.close()  # This disconnects, doesn't close Chrome
                except:
                    pass
        else:
            # In normal mode, close our own browser
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
        description='Ask NotebookLM a question',
        epilog='''
CDP mode (default): Connects to your running Chrome browser.
  Start Chrome with: chrome --remote-debugging-port=9222
  Then log into Google and open NotebookLM.

Token mode (--token): Uses stored authentication tokens.
  Requires: python auth_manager.py setup
        '''
    )

    parser.add_argument('--question', required=True, help='Question to ask')
    parser.add_argument('--notebook-url', help='NotebookLM notebook URL (required for CDP mode)')
    parser.add_argument('--notebook-id', help='Notebook ID from library (token mode only)')
    parser.add_argument('--token', action='store_true', help='Use token-based auth instead of CDP')
    parser.add_argument('--show-browser', action='store_true', help='Show browser (token mode only)')
    parser.add_argument('--cdp-url', default='http://localhost:9222', help='CDP endpoint URL')

    args = parser.parse_args()

    # CDP is the default, --token switches to token mode
    use_cdp = not args.token

    # Resolve notebook URL
    notebook_url = args.notebook_url

    if not notebook_url and args.notebook_id:
        library = NotebookLibrary()
        notebook = library.get_notebook(args.notebook_id)
        if notebook:
            notebook_url = notebook['url']
        else:
            print(f"❌ Notebook '{args.notebook_id}' not found")
            return 1

    if not notebook_url:
        if use_cdp:
            # In CDP mode (default), user must provide URL directly
            print("❌ Please provide --notebook-url")
            print()
            print("Example:")
            print('  python scripts/run.py ask_question.py --notebook-url "https://notebooklm.google.com/notebook/..." --question "..."')
            print()
            print("Make sure Chrome is running with: chrome --remote-debugging-port=9222")
            return 1

        # Token mode: check for active notebook in library
        library = NotebookLibrary()
        active = library.get_active_notebook()
        if active:
            notebook_url = active['url']
            print(f"📚 Using active notebook: {active['name']}")
        else:
            # Show available notebooks
            notebooks = library.list_notebooks()
            if notebooks:
                print("\n📚 Available notebooks:")
                for nb in notebooks:
                    mark = " [ACTIVE]" if nb.get('id') == library.active_notebook_id else ""
                    print(f"  {nb['id']}: {nb['name']}{mark}")
                print("\nSpecify with --notebook-id or set active:")
                print("python scripts/run.py notebook_manager.py activate --id ID")
            else:
                print("❌ No notebooks in library. Add one first:")
                print("python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS")
            return 1

    # Ask the question
    answer = ask_notebooklm(
        question=args.question,
        notebook_url=notebook_url,
        headless=not args.show_browser,
        use_cdp=use_cdp,
        cdp_url=args.cdp_url
    )

    if answer:
        print("\n" + "=" * 60)
        print(f"Question: {args.question}")
        print("=" * 60)
        print()
        print(answer)
        print()
        print("=" * 60)
        return 0
    else:
        print("\n❌ Failed to get answer")
        return 1


if __name__ == "__main__":
    sys.exit(main())
