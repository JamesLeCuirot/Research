// Usage: node pdf.js <input.html> <output.pdf> <running-title>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [,, input, output, rtitle] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'networkidle' });
  await page.pdf({
    path: output, format: 'A4', printBackground: true,
    margin: { top: '22mm', bottom: '22mm', left: '20mm', right: '20mm' },
    displayHeaderFooter: true,
    headerTemplate: `<div style="font-size:7.5pt;color:#777;width:100%;padding:0 20mm;font-family:Arial,sans-serif;">${(rtitle||'').replace(/</g,'&lt;')}</div>`,
    footerTemplate: '<div style="font-size:7.5pt;color:#777;width:100%;text-align:center;font-family:Arial,sans-serif;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
})();
