#!/usr/bin/env python3
"""
NotebookLM Source Manager
List, filter, and delete sources from a notebook to manage quality.

This helps trim low-quality sources (e.g., from Deep Research) before
running another research pass.
"""

import argparse
import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Optional

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

# Source panel selectors (from NotebookLM UI - Jan 2026)
SOURCE_PANEL_SELECTORS = [
    '.scroll-area-desktop',
    '[class*="scroll-area"]',
]

# Individual source item selectors
SOURCE_ITEM_SELECTORS = [
    '.single-source-container',
    '[class*="single-source-container"]',
]

# Source title/name selectors (within a source item)
SOURCE_TITLE_SELECTORS = [
    '.source-title',
    '[class*="source-title"]',
]

# Source type indicator (icon name in mat-icon)
SOURCE_TYPE_SELECTORS = [
    '.source-item-source-icon',
    'mat-icon.icon',
]

# More menu / options button for a source
SOURCE_MENU_SELECTORS = [
    '.source-item-more-button',
    'button[aria-label="More"]',
    'button.source-item-more-button',
]

# Delete option in menu
DELETE_OPTION_SELECTORS = [
    '.more-menu-delete-source-button',
    '[role="menuitem"]:has-text("Remove source")',
    '[role="menuitem"]:has-text("Delete")',
    'button:has-text("Remove source")',
    'button:has-text("Delete source")',
]

# Confirmation dialog
CONFIRM_DELETE_SELECTORS = [
    'button:has-text("Delete")',
    'button.mat-mdc-button:has-text("Delete")',
    '[mat-dialog-actions] button:has-text("Delete")',
]

# Source checkbox for bulk selection
SOURCE_CHECKBOX_SELECTORS = [
    '.select-checkbox input[type="checkbox"]',
    'mat-checkbox input[type="checkbox"]',
]


def list_sources(
    notebook_url: str,
    use_cdp: bool = True,
    cdp_url: str = "http://localhost:9222",
) -> List[Dict]:
    """
    List all sources in a NotebookLM notebook.

    Args:
        notebook_url: NotebookLM notebook URL
        use_cdp: Connect to existing Chrome via CDP
        cdp_url: CDP endpoint URL

    Returns:
        List of source dictionaries with title, type, index
    """
    print(f"📚 Listing sources for: {notebook_url}")

    playwright = None
    context = None
    browser = None
    sources = []

    try:
        playwright = sync_playwright().start()

        if use_cdp:
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)

            # Find existing NotebookLM tab or create new one
            page = None
            for p in context.pages:
                if "notebooklm.google.com" in p.url:
                    page = p
                    print(f"  Found existing NotebookLM tab")
                    break

            if not page:
                page = context.new_page()
                print("  Opening notebook in new tab...")
                page.goto(notebook_url, wait_until="domcontentloaded")
            elif notebook_url not in page.url:
                print("  Navigating to specified notebook...")
                page.goto(notebook_url, wait_until="domcontentloaded")
        else:
            auth = AuthManager()
            if not auth.is_authenticated():
                print("Not authenticated. Use CDP mode or run auth setup.")
                return []
            context = BrowserFactory.launch_persistent_context(playwright, headless=True)
            page = context.new_page()
            page.goto(notebook_url, wait_until="domcontentloaded")

        # Wait for page to load
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=10000)
        time.sleep(3)  # Let UI fully render

        # Find sources in the UI
        print("  Scanning for sources...")

        # Try different source item selectors
        source_elements = []
        for selector in SOURCE_ITEM_SELECTORS:
            try:
                elements = page.query_selector_all(selector)
                if elements:
                    source_elements = elements
                    print(f"  Found {len(elements)} sources using: {selector}")
                    break
            except Exception:
                continue

        if not source_elements:
            # Try to find sources panel first
            print("  Looking for sources panel...")
            for panel_selector in SOURCE_PANEL_SELECTORS:
                try:
                    panel = page.query_selector(panel_selector)
                    if panel:
                        print(f"  Found panel: {panel_selector}")
                        # Get all child items
                        source_elements = panel.query_selector_all('[class*="source"]')
                        if source_elements:
                            break
                except Exception:
                    continue

        # Extract info from each source
        for idx, el in enumerate(source_elements):
            try:
                source_info = {
                    "index": idx,
                    "title": "Unknown",
                    "type": "unknown",
                }

                # Get title
                for title_sel in SOURCE_TITLE_SELECTORS:
                    try:
                        title_el = el.query_selector(title_sel)
                        if title_el:
                            source_info["title"] = title_el.inner_text().strip()
                            break
                    except Exception:
                        continue

                # Get type
                for type_sel in SOURCE_TYPE_SELECTORS:
                    try:
                        type_el = el.query_selector(type_sel)
                        if type_el:
                            type_text = type_el.inner_text().strip()
                            if type_text:
                                source_info["type"] = type_text
                            break
                    except Exception:
                        continue

                sources.append(source_info)

            except Exception as e:
                print(f"  Warning: Could not extract source {idx}: {e}")

        print(f"\n  Total sources found: {len(sources)}")

    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()

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

    return sources


def delete_source_by_index(
    notebook_url: str,
    source_index: int,
    use_cdp: bool = True,
    cdp_url: str = "http://localhost:9222",
    confirm: bool = False,
) -> Dict:
    """
    Delete a source by its index in the source list.

    Args:
        notebook_url: NotebookLM notebook URL
        source_index: Index of source to delete (0-based)
        use_cdp: Connect via CDP
        cdp_url: CDP endpoint
        confirm: Actually delete (False = dry run)

    Returns:
        Status dictionary
    """
    if not confirm:
        print(f"  DRY RUN: Would delete source at index {source_index}")
        return {"status": "dry_run", "index": source_index}

    print(f"Deleting source at index {source_index}...")

    playwright = None
    context = None
    browser = None

    try:
        playwright = sync_playwright().start()

        if use_cdp:
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)
            page = None
            for p in context.pages:
                if "notebooklm.google.com" in p.url:
                    page = p
                    break
            if not page:
                page = context.new_page()
                page.goto(notebook_url, wait_until="domcontentloaded")
            elif notebook_url not in page.url:
                page.goto(notebook_url, wait_until="domcontentloaded")
        else:
            context = BrowserFactory.launch_persistent_context(playwright, headless=True)
            page = context.new_page()
            page.goto(notebook_url, wait_until="domcontentloaded")

        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com/"), timeout=10000)
        time.sleep(2)

        # Dismiss any existing overlays/menus by pressing Escape
        page.keyboard.press("Escape")
        time.sleep(0.3)

        # Click somewhere neutral to clear any focus/selection
        try:
            page.locator('body').click(position={"x": 10, "y": 10}, force=True)
            time.sleep(0.3)
        except Exception:
            pass

        # Use locators instead of element handles - more resilient to DOM changes
        source_locator = page.locator('.single-source-container')
        count = source_locator.count()

        if source_index >= count:
            return {"status": "error", "message": f"Index {source_index} out of range (found {count} sources)"}

        # Get the specific source by index
        target = source_locator.nth(source_index)

        # Get title for logging
        title = "Unknown"
        try:
            title_locator = target.locator('.source-title')
            if title_locator.count() > 0:
                title = title_locator.first.inner_text().strip()
        except Exception:
            pass

        print(f"  Target: {title}")

        # Find the More button within this source using locator
        more_button = target.locator('button[aria-label="More"]')

        if more_button.count() > 0:
            print("  Clicking More button...")
            more_button.first.click()
            time.sleep(0.5)

            # Wait for menu to appear and find Delete/Remove option
            # The menu appears as a mat-menu overlay
            delete_option = page.locator('.more-menu-delete-source-button, [role="menuitem"]:has-text("Remove source")').first

            try:
                delete_option.wait_for(state="visible", timeout=3000)
                print("  Clicking Remove source...")
                delete_option.click()
                time.sleep(0.5)

                # Handle confirmation dialog - look for Delete button in dialog
                confirm_button = page.locator('mat-dialog-actions button:has-text("Delete"), .mat-mdc-dialog-actions button:has-text("Delete")')
                try:
                    confirm_button.wait_for(state="visible", timeout=3000)
                    print("  Confirming delete...")
                    confirm_button.click()
                    time.sleep(1)
                    print(f"  Deleted: {title}")
                    return {"status": "success", "title": title, "index": source_index}
                except Exception:
                    # No confirmation dialog, might have deleted directly
                    print(f"  Deleted (no confirmation): {title}")
                    return {"status": "success", "title": title, "index": source_index}

            except Exception as e:
                print(f"  Delete option not found: {e}")
                return {"status": "error", "message": "Delete menu option not found"}
        else:
            print("  More button not found")
            return {"status": "error", "message": "More button not found"}

    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

    finally:
        if use_cdp and browser:
            try:
                browser.close()
            except Exception:
                pass
        elif context:
            try:
                context.close()
            except Exception:
                pass
        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


def delete_sources_by_pattern(
    notebook_url: str,
    pattern: str,
    use_cdp: bool = True,
    cdp_url: str = "http://localhost:9222",
    confirm: bool = False,
) -> Dict:
    """
    Delete sources matching a title pattern (regex).

    Args:
        notebook_url: NotebookLM notebook URL
        pattern: Regex pattern to match source titles
        use_cdp: Connect via CDP
        cdp_url: CDP endpoint
        confirm: Actually delete (False = dry run)

    Returns:
        Status with list of matched/deleted sources
    """
    print(f"Finding sources matching: {pattern}")

    # First list all sources
    sources = list_sources(notebook_url, use_cdp, cdp_url)

    # Filter by pattern
    regex = re.compile(pattern, re.IGNORECASE)
    matches = [s for s in sources if regex.search(s["title"])]

    print(f"\nMatched {len(matches)} sources:")
    for s in matches:
        print(f"  [{s['index']}] {s['title']}")

    if not confirm:
        print(f"\nDRY RUN: Add --confirm to delete these sources")
        return {"status": "dry_run", "matched": matches}

    # Store titles to delete (indices will shift after each deletion)
    titles_to_delete = [s["title"] for s in matches]
    deleted = []

    # Delete one at a time, re-fetching the list each time to get correct index
    for title in titles_to_delete:
        # Re-fetch sources to get current indices
        current_sources = list_sources(notebook_url, use_cdp, cdp_url)

        # Find the source by title
        source_to_delete = None
        for s in current_sources:
            if s["title"] == title:
                source_to_delete = s
                break

        if source_to_delete is None:
            print(f"  Source not found (may have been deleted): {title[:50]}")
            continue

        # Delete by current index
        result = delete_source_by_index(
            notebook_url, source_to_delete["index"], use_cdp, cdp_url, confirm=True
        )
        if result.get("status") == "success":
            deleted.append({"title": title, "index": source_to_delete["index"]})
        time.sleep(1)  # Wait between deletes

    return {"status": "success", "deleted": deleted, "total": len(deleted)}


def main():
    parser = argparse.ArgumentParser(
        description='Manage NotebookLM sources',
        epilog='''
Examples:
  # List all sources
  python manage_sources.py list --notebook-url "https://notebooklm.google.com/notebook/..."

  # Delete by index (dry run)
  python manage_sources.py delete --notebook-url "..." --index 5

  # Delete by index (actual)
  python manage_sources.py delete --notebook-url "..." --index 5 --confirm

  # Delete by pattern (dry run)
  python manage_sources.py delete --notebook-url "..." --pattern "blog|medium"

  # Delete by pattern (actual)
  python manage_sources.py delete --notebook-url "..." --pattern "blog|medium" --confirm
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List all sources')
    list_parser.add_argument('--notebook-url', required=True, help='NotebookLM URL')
    list_parser.add_argument('--cdp-url', default='http://localhost:9222', help='CDP endpoint')

    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete sources')
    del_parser.add_argument('--notebook-url', required=True, help='NotebookLM URL')
    del_parser.add_argument('--index', type=int, help='Source index to delete')
    del_parser.add_argument('--pattern', help='Regex pattern to match titles')
    del_parser.add_argument('--confirm', action='store_true', help='Actually delete (else dry run)')
    del_parser.add_argument('--cdp-url', default='http://localhost:9222', help='CDP endpoint')

    args = parser.parse_args()

    if args.command == 'list':
        sources = list_sources(args.notebook_url, cdp_url=args.cdp_url)
        print("\nSources:")
        print("-" * 60)
        for s in sources:
            print(f"  [{s['index']:2d}] {s['title'][:50]}")
        print("-" * 60)
        print(f"Total: {len(sources)}")

    elif args.command == 'delete':
        if args.index is not None:
            result = delete_source_by_index(
                args.notebook_url,
                args.index,
                cdp_url=args.cdp_url,
                confirm=args.confirm
            )
        elif args.pattern:
            result = delete_sources_by_pattern(
                args.notebook_url,
                args.pattern,
                cdp_url=args.cdp_url,
                confirm=args.confirm
            )
        else:
            print("Error: Must specify --index or --pattern")
            return 1

        print("\nResult:", result.get("status"))

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())
