// Render doc.html to PDF with headless Chromium (Node Playwright) and audit it.
// Usage: node render.cjs doc.html "Output-2026-11.pdf"
// If Playwright isn't available, use render.py instead.
const fs = require('node:fs');
const path = require('node:path');

let chromium;
// Look next to this script, then in the working folder (npm install playwright there).
for (const load of [() => require('playwright'), () => require('node:module').createRequire(path.join(process.cwd(), 'x.js'))('playwright')]) {
  try { ({ chromium } = load()); break; } catch (e) { /* try next */ }
}
if (!chromium) {
  console.error('Node Playwright not found. Use: python3 render.py <html> <pdf>  (or npm install playwright in this folder)');
  process.exit(2);
}

(async () => {
  const [, , input = 'doc.html', output = 'doc.pdf'] = process.argv;
  const browser = await chromium.launch().catch(async () => chromium.launch({ channel: 'chrome' }));
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const report = JSON.parse(await page.evaluate(fs.readFileSync(path.join(__dirname, 'audit.js'), 'utf8')));
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
  await browser.close();

  let problems = 0;
  for (const f of report.fonts) { console.log(`${f.loaded ? 'ok  ' : 'FAIL'} font ${f.token}: ${f.family}`); if (!f.loaded) problems++; }
  const low = Object.entries(report.lowContrast);
  if (low.length) { problems += low.length; low.forEach(([k, o]) => console.log(`FAIL contrast ${o.ratio}:1  ${k}  e.g. "${o.example}"`)); }
  else console.log('ok   all text outside the cover is 4.5:1 or better');
  if (report.placeholders.length) { problems++; console.log('FAIL leftover placeholders: ' + report.placeholders.join(', ')); }
  console.log(`wrote ${output}${problems ? ` with ${problems} problem(s) to fix` : ''}`);
})();
