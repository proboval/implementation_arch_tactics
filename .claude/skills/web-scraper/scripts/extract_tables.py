#!/usr/bin/env python3
"""
Table Extractor - Extract structured tables from web pages
Outputs CSV, JSON, or markdown format
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from patchright.sync_api import sync_playwright
from config import DEFAULT_CDP_URL, PAGE_LOAD_TIMEOUT, TABLE_FORMATS
from browser_utils import BrowserFactory, ContentExtractor, PageWaiter

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def format_table_csv(table: dict) -> str:
    """Format a table as CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)

    if table['headers']:
        writer.writerow(table['headers'])

    for row in table['rows']:
        writer.writerow(row)

    return output.getvalue()


def format_table_json(table: dict) -> str:
    """Format a table as JSON string."""
    if table['headers']:
        # Convert to list of dicts
        records = []
        for row in table['rows']:
            record = {}
            for i, header in enumerate(table['headers']):
                record[header] = row[i] if i < len(row) else ''
            records.append(record)
        return json.dumps(records, indent=2, ensure_ascii=False)
    else:
        return json.dumps(table['rows'], indent=2, ensure_ascii=False)


def format_table_markdown(table: dict) -> str:
    """Format a table as markdown."""
    lines = []

    headers = table['headers']
    rows = table['rows']

    if not headers and rows:
        # Use first row as headers
        headers = rows[0]
        rows = rows[1:]

    if headers:
        lines.append('| ' + ' | '.join(headers) + ' |')
        lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

    for row in rows:
        # Pad row to match header length
        padded = row + [''] * (len(headers) - len(row)) if len(row) < len(headers) else row
        lines.append('| ' + ' | '.join(padded[:len(headers)]) + ' |')

    return '\n'.join(lines)


def extract_all_tables(url, format='csv', selector=None, index=None,
                       mode='headless', cdp_url=DEFAULT_CDP_URL,
                       timeout=PAGE_LOAD_TIMEOUT):
    """
    Extract tables from a web page.

    Returns: list of formatted table strings
    """
    playwright = None
    browser = None
    context = None

    try:
        playwright = sync_playwright().start()

        if mode == 'cdp':
            browser, context = BrowserFactory.connect_to_cdp(playwright, cdp_url)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        else:
            browser, context = BrowserFactory.launch_headless(playwright)
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)

        PageWaiter.wait_for_content(page)

        print(f"  Extracting tables...")
        tables = ContentExtractor.extract_tables(page, selector=selector)

        if not tables:
            print("  No tables found on page")
            return []

        print(f"  Found {len(tables)} table(s)")

        # Filter by index if specified
        if index is not None:
            if index < len(tables):
                tables = [tables[index]]
                print(f"  Using table #{index}")
            else:
                print(f"  Warning: Table index {index} out of range (0-{len(tables)-1})")
                return []

        # Format tables
        formatter = {
            'csv': format_table_csv,
            'json': format_table_json,
            'markdown': format_table_markdown,
        }[format]

        results = []
        for i, table in enumerate(tables):
            formatted = formatter(table)
            results.append({
                'index': i,
                'headers': table['headers'],
                'row_count': table['row_count'],
                'col_count': table['col_count'],
                'content': formatted,
            })
            print(f"  Table #{i}: {table['row_count']} rows x {table['col_count']} cols")

        return results

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
        description='Extract tables from a web page'
    )

    parser.add_argument('--url', required=True, help='Page URL with tables')
    parser.add_argument('--format', choices=TABLE_FORMATS, default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--output', help='Output file or directory')
    parser.add_argument('--selector', help='CSS selector for specific table')
    parser.add_argument('--index', type=int, help='Extract Nth table only (0-based)')
    parser.add_argument('--mode', choices=['headless', 'cdp'], default='headless',
                        help='Browser mode (default: headless)')
    parser.add_argument('--cdp-url', default=DEFAULT_CDP_URL,
                        help=f'CDP endpoint (default: {DEFAULT_CDP_URL})')
    parser.add_argument('--timeout', type=int, default=PAGE_LOAD_TIMEOUT,
                        help=f'Page load timeout in ms (default: {PAGE_LOAD_TIMEOUT})')

    args = parser.parse_args()

    print(f"Extracting tables from: {args.url}")
    print(f"  Mode: {args.mode} | Format: {args.format}")

    results = extract_all_tables(
        url=args.url,
        format=args.format,
        selector=args.selector,
        index=args.index,
        mode=args.mode,
        cdp_url=args.cdp_url,
        timeout=args.timeout,
    )

    if not results:
        print("\nNo tables extracted")
        return

    if args.output:
        output_path = Path(args.output)

        if len(results) == 1:
            # Single table - save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(results[0]['content'], encoding='utf-8')
            print(f"\nSaved to: {output_path}")
        else:
            # Multiple tables - save to directory
            output_path.mkdir(parents=True, exist_ok=True)
            ext = {'csv': '.csv', 'json': '.json', 'markdown': '.md'}[args.format]
            for r in results:
                file_path = output_path / f"table_{r['index']}{ext}"
                file_path.write_text(r['content'], encoding='utf-8')
                print(f"  Saved table #{r['index']}: {file_path}")
    else:
        for r in results:
            print(f"\n--- Table #{r['index']} ({r['row_count']} rows x {r['col_count']} cols) ---\n")
            print(r['content'])


if __name__ == "__main__":
    main()