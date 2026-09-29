import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { chromium } from 'playwright';
import { previewServer } from '../src/preview.mjs';

const root = new URL('../_build/html', import.meta.url).pathname;
const artifacts = new URL('../_build/checks', import.meta.url).pathname;
fs.mkdirSync(artifacts, { recursive: true });
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

test('browser: navigation, fragments, references, notes, offline assets, layout and PDF', { timeout: 60000 }, async () => {
  const server = previewServer(root);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({ headless: true, ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}) });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();
    const errors = [], remote = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', req => { if (/^https?:/.test(req.url()) && !req.url().startsWith('http://127.0.0.1:')) remote.push(req.url()); });
    const origin = `http://127.0.0.1:${server.address().port}`;
    await page.goto(`${origin}/comp521/`);
    await page.getByRole('link', { name: 'Open the six-slide prototype' }).click();
    await page.waitForFunction(() => window.deckReady);
    assert.equal(await page.locator('.slides > section').count(), 6);
    assert.equal(await page.locator('pre.cell-output').textContent(), '10\n');
    assert.ok(await page.locator('.hljs-keyword').count() > 0);
    await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => Reveal.getIndices().h === 1);
    assert.equal(await page.locator('.fragment').getAttribute('aria-hidden'), 'true');
    await page.keyboard.press('ArrowRight');
    await page.waitForFunction(() => document.querySelector('.fragment').classList.contains('visible'));
    assert.equal(await page.locator('.fragment').getAttribute('aria-hidden'), 'false');
    await page.keyboard.press('ArrowLeft');
    assert.equal(await page.locator('.fragment').getAttribute('aria-hidden'), 'true');
    await page.evaluate(() => Reveal.slide(4));
    await page.locator('.present a[data-target="rectangle-area"]').click();
    await page.waitForFunction(() => Reveal.getIndices().h === 3);
    assert.match(page.url(), /#\/slide-state-and-a-derived-quantity$/);
    await page.reload();
    await page.waitForFunction(() => window.deckReady && Reveal.getIndices().h === 3);
    for (const viewport of [{ width: 1440, height: 900 }, { width: 1280, height: 720 }]) {
      await page.setViewportSize(viewport);
      for (let i = 0; i < 6; i++) {
        await page.evaluate(i => { Reveal.configure({ transition: 'none' }); Reveal.slide(i, 0, 99); Reveal.layout(); }, i);
        await page.evaluate(() => document.fonts.ready);
        // Reveal applies visibility/layout on animation frames after navigation.
        await page.waitForTimeout(400);
        const bounds = await page.evaluate(() => {
          const slide = Reveal.getCurrentSlide();
          return { height: slide.scrollHeight, width: slide.scrollWidth,
            titleTop: slide.querySelector('h2').getBoundingClientRect().top };
        });
        assert.ok(bounds.titleTop >= 0, `Slide ${i + 1} title is clipped`);
        assert.ok(bounds.height <= 700, `Slide ${i + 1} overflows vertically: ${JSON.stringify(bounds)}`);
        assert.ok(bounds.width <= 1100, `Slide ${i + 1} overflows horizontally: ${JSON.stringify(bounds)}`);
        if (viewport.width === 1440) await page.screenshot({ path: `${artifacts}/slide-${i + 1}.png` });
      }
    }
    await page.evaluate(() => Reveal.slide(0));
    const popupPromise = page.waitForEvent('popup');
    await page.keyboard.press('s');
    const notes = await popupPromise;
    await notes.waitForFunction(() => document.body.textContent.includes('Ask students to identify'), undefined, { timeout: 15000 });
    await notes.screenshot({ path: `${artifacts}/speaker-view.png` });
    await notes.close();
    assert.deepEqual(remote, [], 'Presentation assets must not request external resources');
    assert.deepEqual(errors, []);
    await context.setOffline(true);
    const offline = await context.newPage();
    await offline.goto(new URL(`file://${root}/reveal/prototype.html`).href);
    await offline.waitForFunction(() => window.deckReady);
    const imagesLoaded = await offline.locator('img').evaluateAll(imgs => imgs.every(img => img.complete && img.naturalWidth > 0));
    assert.ok(imagesLoaded);
    assert.ok(await offline.locator('.katex').count() > 0);
    await context.setOffline(false);
    const print = await context.newPage();
    await print.goto(`${origin}/comp521/reveal/prototype.html?print-pdf`);
    await print.waitForFunction(() => document.querySelectorAll('.pdf-page').length === 6);
    await print.pdf({ path: `${artifacts}/prototype.pdf`, printBackground: true, preferCSSPageSize: true });
  } finally {
    await browser?.close();
    await new Promise(resolve => server.close(resolve));
  }
});
