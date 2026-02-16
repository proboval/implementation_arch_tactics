"""
Browser Utilities for NotebookLM Skill
Handles browser launching, stealth features, and common interactions
"""

import json
import time
import random
import sys
from typing import Optional, List, Tuple

from patchright.sync_api import Playwright, BrowserContext, Page, Browser
from config import BROWSER_PROFILE_DIR, STATE_FILE, BROWSER_ARGS, USER_AGENT

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Default CDP endpoint
DEFAULT_CDP_URL = "http://localhost:9222"


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

        Args:
            playwright: Playwright instance
            cdp_url: CDP endpoint URL (default: http://localhost:9222)

        Returns:
            Tuple of (Browser, BrowserContext) - caller must manage cleanup
        """
        print(f"  🔗 Connecting to Chrome at {cdp_url}...")

        try:
            browser = playwright.chromium.connect_over_cdp(cdp_url)

            # Get existing contexts (tabs)
            contexts = browser.contexts
            if contexts:
                context = contexts[0]  # Use first context
                print(f"  ✅ Connected! Found {len(context.pages)} open tab(s)")
            else:
                # Create new context if none exists
                context = browser.new_context()
                print("  ✅ Connected! Created new context")

            return browser, context

        except Exception as e:
            error_msg = str(e)
            if "connection refused" in error_msg.lower() or "cannot connect" in error_msg.lower():
                print(f"  ❌ Cannot connect to Chrome at {cdp_url}")
                print()
                print("  To use CDP mode, start Chrome with remote debugging:")
                print()
                print('    Windows:')
                print('      chrome.exe --remote-debugging-port=9222')
                print()
                print('    Or create a shortcut with that flag.')
                print()
                print("  Then open NotebookLM and log in before running this script.")
            else:
                print(f"  ❌ CDP connection error: {e}")
            raise

    @staticmethod
    def launch_persistent_context(
        playwright: Playwright,
        headless: bool = True,
        user_data_dir: str = str(BROWSER_PROFILE_DIR)
    ) -> BrowserContext:
        """
        Launch a persistent browser context with anti-detection features
        and cookie workaround.
        """
        # Launch persistent context
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",  # Use real Chrome
            headless=headless,
            no_viewport=True,
            ignore_default_args=["--enable-automation"],
            user_agent=USER_AGENT,
            args=BROWSER_ARGS
        )

        # Cookie Workaround for Playwright bug #36139
        # Session cookies (expires=-1) don't persist in user_data_dir automatically
        BrowserFactory._inject_cookies(context)

        return context

    @staticmethod
    def _inject_cookies(context: BrowserContext):
        """Inject cookies from state.json if available"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    if 'cookies' in state and len(state['cookies']) > 0:
                        context.add_cookies(state['cookies'])
                        # print(f"  🔧 Injected {len(state['cookies'])} cookies from state.json")
            except Exception as e:
                print(f"  ⚠️  Could not load state.json: {e}")


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
            # Try waiting if not immediately found
            try:
                element = page.wait_for_selector(selector, timeout=2000)
            except:
                pass
        
        if not element:
            print(f"⚠️ Element not found for typing: {selector}")
            return

        # Click to focus
        element.click()
        
        # Type
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

        # Optional: Move mouse to element (simplified)
        box = element.bounding_box()
        if box:
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2
            page.mouse.move(x, y, steps=5)

        StealthUtils.random_delay(100, 300)
        element.click()
        StealthUtils.random_delay(100, 300)
