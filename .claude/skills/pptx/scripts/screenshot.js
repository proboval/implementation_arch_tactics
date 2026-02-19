/**
 * screenshot.js - Render HTML slides to PNG using Playwright
 *
 * Usage:
 *   node screenshot.js <html-dir> [output-dir]
 *
 * Renders each .html file in <html-dir> to a PNG image.
 * Output goes to <output-dir> (defaults to <html-dir>/png/).
 * Files are named slide-001.png, slide-002.png, etc.
 *
 * The viewport is derived from the HTML body's CSS width/height.
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const PT_TO_PX = 4 / 3; // 1pt = 1.333px

async function main() {
    const htmlDir = process.argv[2];
    const outputDir = process.argv[3] || path.join(htmlDir, 'png');

    if (!htmlDir) {
        console.error('Usage: node screenshot.js <html-dir> [output-dir]');
        process.exit(1);
    }

    // Find HTML files sorted alphabetically
    const htmlFiles = fs.readdirSync(htmlDir)
        .filter(f => f.endsWith('.html') && f !== 'build.js')
        .sort();

    if (htmlFiles.length === 0) {
        console.error('No HTML files found in ' + htmlDir);
        process.exit(1);
    }

    fs.mkdirSync(outputDir, { recursive: true });

    const browser = await chromium.launch();
    const context = await browser.newContext();

    for (let i = 0; i < htmlFiles.length; i++) {
        const htmlFile = htmlFiles[i];
        const htmlPath = path.resolve(htmlDir, htmlFile);
        const page = await context.newPage();

        // Load the HTML file
        await page.goto('file:///' + htmlPath.replace(/\\/g, '/'));

        // Read body dimensions from CSS (pt units → px)
        const dims = await page.evaluate(() => {
            const body = document.body;
            const style = window.getComputedStyle(body);
            return {
                width: parseFloat(style.width),
                height: parseFloat(style.height)
            };
        });

        // Set viewport to match slide dimensions
        const vpWidth = Math.ceil(dims.width);
        const vpHeight = Math.ceil(dims.height);
        await page.setViewportSize({ width: vpWidth, height: vpHeight });

        // Wait for any images/fonts to load
        await page.waitForLoadState('networkidle').catch(() => {});

        // Screenshot
        const padIdx = String(i + 1).padStart(3, '0');
        const pngPath = path.join(outputDir, `slide-${padIdx}.png`);
        await page.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: vpWidth, height: vpHeight } });

        console.log(`${htmlFile} → ${path.basename(pngPath)}`);
        await page.close();
    }

    await browser.close();
    console.log(`\n${htmlFiles.length} slides rendered to ${outputDir}`);
}

main().catch(err => { console.error(err); process.exit(1); });
