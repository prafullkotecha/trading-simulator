// Renders each HTML diagram in this folder to a PNG in docs/images at 2x.
// Run: node docs/images/src/render.js [name ...]   (needs Playwright's Chromium)
const { chromium } = require('playwright');
const path = require('path');
const all = ['design-colors', 'design-app-map', 'design-wireframes', 'implementation-phases', 'implementation-ownership', 'implementation-pr-flow'];
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : all;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2300, height: 1400 }, deviceScaleFactor: 2 });
  for (const n of names) {
    await page.goto('file://' + path.join(__dirname, n + '.html'));
    await page.evaluate(() => document.fonts.ready);
    await page.locator('#frame').screenshot({ path: path.join(__dirname, '..', n + '.png') });
    console.log('wrote', n + '.png');
  }
  await browser.close();
})();
