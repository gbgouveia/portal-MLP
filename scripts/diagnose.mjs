import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACT_DIR = 'C:\\Users\\HOME\\.gemini\\antigravity-ide\\brain\\54c8eeec-8d1f-4f0a-ab84-27f6f47949d9';

const viewports = [
  { name: '360', width: 360, height: 740 },
  { name: '390', width: 390, height: 844 },
  { name: '430', width: 430, height: 932 },
  { name: '706', width: 706, height: 1000 },
  { name: '768', width: 768, height: 1024 },
  { name: '1024', width: 1024, height: 768 },
  { name: '1440', width: 1440, height: 900 },
  { name: '1920', width: 1920, height: 1080 },
  { name: 'landscape_844x390', width: 844, height: 390 },
  { name: 'zoom_200_390', width: 390, height: 844, deviceScaleFactor: 2 },
];

async function run() {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  console.log('=== VALIDATING HOME PAGE (#ministerio) ===');
  for (const vp of viewports) {
    await page.setViewport({
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: vp.deviceScaleFactor || 1
    });
    await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle2' });

    // Scroll to #ministerio
    await page.evaluate(() => {
      const el = document.getElementById('ministerio');
      if (el) el.scrollIntoView();
    });
    await new Promise(r => setTimeout(r, 400));

    // Check overflow in #ministerio specifically
    const sectionOverflows = await page.evaluate(() => {
      const section = document.getElementById('ministerio');
      if (!section) return [];
      const all = [...section.querySelectorAll('*')];
      const overflows = all.filter(e => {
        const r = e.getBoundingClientRect();
        return r.right > window.innerWidth + 1 || r.left < -1;
      });
      return overflows.map(e => ({
        tag: e.tagName,
        className: (e.className && typeof e.className === 'string') ? e.className : '',
        rect: {
          left: Math.round(e.getBoundingClientRect().left),
          right: Math.round(e.getBoundingClientRect().right),
          width: Math.round(e.getBoundingClientRect().width)
        },
        innerWidth: window.innerWidth
      }));
    });

    console.log(`Home #ministerio ${vp.name}px: ${sectionOverflows.length} overflows`);
    if (sectionOverflows.length > 0) {
      console.log('Overflow details:', sectionOverflows);
    }

    if (vp.name === '390' || vp.name === '768') {
      const sectionHandle = await page.$('#ministerio');
      if (sectionHandle) {
        await sectionHandle.screenshot({
          path: path.join(ARTIFACT_DIR, `after_home_${vp.name}.png`)
        });
      }
    }
  }

  console.log('\n=== VALIDATING LEGACY PAGE (/legado-pastor-leonel/) ===');
  for (const vp of viewports) {
    await page.setViewport({
      width: vp.width,
      height: vp.height,
      deviceScaleFactor: vp.deviceScaleFactor || 1
    });
    await page.goto('http://127.0.0.1:8000/legado-pastor-leonel/', { waitUntil: 'networkidle2' });

    await new Promise(r => setTimeout(r, 600));

    // Check entire page overflow
    const overflows = await page.evaluate(() => {
      const all = [...document.querySelectorAll('*')];
      const overflows = all.filter(e => {
        const r = e.getBoundingClientRect();
        return r.right > window.innerWidth + 1 || r.left < -1;
      });
      return overflows.map(e => ({
        tag: e.tagName,
        className: (e.className && typeof e.className === 'string') ? e.className : '',
        rect: {
          left: Math.round(e.getBoundingClientRect().left),
          right: Math.round(e.getBoundingClientRect().right),
          width: Math.round(e.getBoundingClientRect().width)
        },
        innerWidth: window.innerWidth
      }));
    });

    console.log(`Legacy page ${vp.name}px: ${overflows.length} overflows`);
    if (overflows.length > 0) {
      console.log('Overflow details:', overflows);
    }

    if (vp.name === '390' || vp.name === '768' || vp.name === '1024' || vp.name === '1440') {
      await page.screenshot({
        path: path.join(ARTIFACT_DIR, `after_legacy_page_${vp.name}.png`),
        fullPage: true
      });
    }
  }

  await browser.close();
  console.log('\nValidation script finished!');
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
