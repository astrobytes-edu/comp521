import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { chromium } from 'playwright';
import { previewServer } from '../src/preview.mjs';
import { renderSlides } from '../src/render.mjs';

const root = new URL('../', import.meta.url).pathname;
const project = `${root}examples/features`;
const fixture = () => JSON.parse(fs.readFileSync(`${project}/_build/site/content/index.json`, 'utf8'));
const artifacts = `${root}_build/features-checks`;
fs.mkdirSync(artifacts, { recursive: true });

test('feature export preserves metadata and rejects unsupported slide options', () => {
  const doc = fixture();
  const html = renderSlides(doc, `${project}/_build/site/public`, { projectDir: project });
  for (const expected of ['data-auto-animate=""', 'data-fragment-index="0"', 'data-line-numbers="1|2-3|4"',
    'data-background-image="data:image/', '<video', '<audio', '<track', 'sandbox="allow-scripts"',
    'class="slide-tabs"', 'class="bibliography"']) assert.ok(html.includes(expected), expected);
  assert.ok(!renderSlides(doc, `${project}/_build/site/public`, { projectDir: project, handout: true }).includes('Feature tour: confirm'));
  const top = doc.mdast.children[0].children;
  top.splice(1, 0, { type: 'div', class: 'myst-reveal-options', reveal: { 'unknown-setting': 42 }, children: [] });
  assert.throws(() => renderSlides(doc, `${project}/_build/site/public`, { projectDir: project }), /Unsupported slide attribute/);
});

test('feature browser: effects, animation, code steps, tabs, media, embedded UI and controls', { timeout: 120000 }, async () => {
  const server = previewServer(`${root}_build/html`);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    browser = await chromium.launch({ headless: true, ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}) });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();
    const errors = [], remote = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('request', r => { if (/^https?:/.test(r.url()) && !r.url().startsWith('http://127.0.0.1:')) remote.push(r.url()); });
    const url = `http://127.0.0.1:${server.address().port}/comp521/reveal/features.html`;
    await page.goto(url);
    await page.waitForFunction(() => window.deckReady);
    assert.equal(await page.evaluate(() => Reveal.getSlides().length), 26);
    assert.equal(await page.locator('.reveal').getAttribute('data-extension'), 'loaded');
    const go = async (i, fragment = -1) => {
      await page.evaluate(({ i, fragment }) => { const s = Reveal.getSlides()[i]; const { h, v } = Reveal.getIndices(s); Reveal.slide(h, v, fragment); }, { i, fragment });
      await page.waitForTimeout(400);
    };
    await go(1);
    assert.equal(await page.locator('.present .fade-out').getAttribute('aria-hidden'), 'false');
    assert.equal(await page.locator('.present .fade-up').getAttribute('aria-hidden'), 'true');
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('.present .fade-out').getAttribute('aria-hidden'), 'true');
    assert.equal(await page.locator('.present .fade-up').getAttribute('aria-hidden'), 'false');
    await go(2);
    assert.equal(await page.locator('.present li.fragment').count(), 3);
    await go(3);
    assert.ok(await page.locator('.present .hljs-ln').count() > 0);
    await page.keyboard.press('ArrowRight');
    assert.ok(await page.evaluate(() => Reveal.getIndices().f >= 0));
    await go(4);
    await page.evaluate(() => { window.animations = []; Reveal.on('autoanimate', e => window.animations.push(e.toSlide.id)); });
    await go(5);
    await page.waitForFunction(() => window.animations.length === 1);
    assert.ok(await page.locator('.present [data-auto-animate-target]').count() > 0);
    await go(6); await go(7);
    await page.waitForFunction(() => window.animations.length === 2);
    await go(11);
    const tabs = page.locator('.present').getByRole('tab');
    assert.equal(await tabs.count(), 2);
    await tabs.nth(0).focus(); await page.keyboard.press('ArrowRight');
    assert.equal(await tabs.nth(1).getAttribute('aria-selected'), 'true');
    assert.equal(await page.evaluate(() => Reveal.getIndices().h), 11);
    await go(13); await page.keyboard.press('ArrowDown');
    assert.equal(await page.evaluate(() => Reveal.getIndices().v), 1);
    await go(15);
    const frame = page.frameLocator('.present iframe');
    await frame.getByRole('slider', { name: 'Width' }).fill('8');
    assert.equal(await frame.locator('output').textContent(), '16');
    await go(16);
    const media = await page.locator('.present video').evaluate(async video => {
      await video.play();
      await new Promise(resolve => setTimeout(resolve, 300));
      video.pause();
      return { time: video.currentTime, width: video.videoWidth, tracks: video.textTracks.length };
    });
    assert.ok(media.time > 0 && media.width > 0); assert.equal(media.tracks, 1);
    await go(17);
    assert.ok(await page.locator('.present audio').evaluate(async audio => { await audio.play(); audio.pause(); return audio.duration > 0; }));
    await go(21);
    await page.waitForFunction(() => document.querySelector('.slide-background.present video')?.currentTime > 0, undefined, { timeout: 10000 });
    await go(23);
    const background = page.frameLocator('.slide-background.present iframe');
    await background.getByRole('slider', { name: 'Width' }).fill('7');
    assert.equal(await background.locator('output').textContent(), '14');
    await go(25);
    const plot = page.frameLocator('.present iframe');
    const curveBefore = await plot.locator('#curve').getAttribute('points');
    await plot.getByRole('slider', { name: 'Coefficient a' }).fill('2');
    assert.equal(await plot.locator('output').textContent(), '2');
    assert.notEqual(await plot.locator('#curve').getAttribute('points'), curveBefore);
    await go(18);
    assert.equal(await page.frameLocator('.present iframe').getByRole('cell', { name: '10', exact: true }).textContent(), '10');
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.getByRole('button', { name: 'Slides', exact: true }).click();
    await page.getByRole('dialog').getByRole('button', { name: '1. Presenter controls', exact: true }).click();
    assert.equal(await page.evaluate(() => Reveal.getIndices().h), 0);
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.getByRole('button', { name: 'Pointer', exact: true }).click();
    assert.ok(await page.locator('.laser-pointer').isVisible());
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.getByRole('button', { name: 'Pointer', exact: true }).click();
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.getByRole('button', { name: 'Overview', exact: true }).click();
    assert.ok(await page.evaluate(() => Reveal.isOverview()));
    await page.keyboard.press('Escape');
    await page.getByRole('button', { name: 'Tools', exact: true }).click();
    await page.getByRole('button', { name: 'Search', exact: true }).click();
    assert.ok(await page.locator('.searchinput').isVisible());
    await page.locator('.searchinput').pressSequentially('Video with captions');
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(() => Reveal.getCurrentSlide().id), 'slide-video-with-captions');
    await page.keyboard.press('Escape');
    await page.keyboard.press('b'); assert.ok(await page.evaluate(() => Reveal.isPaused()));
    await page.keyboard.press('b');
    for (const viewport of [{ width: 1440, height: 900 }, { width: 1280, height: 720 }]) {
      await page.setViewportSize(viewport);
      await page.evaluate(() => Reveal.configure({ transition: 'none', backgroundTransition: 'none', autoAnimate: false }));
      for (let i = 0; i < 26; i++) {
        await go(i, 99);
        const bounds = await page.evaluate(() => ({ height: Reveal.getCurrentSlide().scrollHeight, width: Reveal.getCurrentSlide().scrollWidth }));
        assert.ok(bounds.height <= 700 && bounds.width <= 1100, `Slide ${i + 1}: ${JSON.stringify(bounds)}`);
        if (viewport.width === 1440) await page.screenshot({ path: `${artifacts}/slide-${i + 1}.png` });
      }
    }
    assert.deepEqual(errors, []); assert.deepEqual(remote, []);
    const reduced = await browser.newPage({ reducedMotion: 'reduce' });
    await reduced.goto(url); await reduced.waitForFunction(() => window.deckReady);
    assert.equal(await reduced.evaluate(() => Reveal.getConfig().autoAnimate), false);
    await context.setOffline(true);
    const offline = await context.newPage();
    await offline.goto(`file://${root}_build/html/reveal/features.html`);
    await offline.waitForFunction(() => window.deckReady);
    const handout = await context.newPage();
    await handout.goto(`file://${root}_build/html/reveal/features.handout.html`);
    assert.equal(await handout.locator('aside.notes').count(), 0);
    assert.ok(await handout.getByText('This explanation appears on that same step.').isVisible());
    assert.equal(await handout.locator('.slide-tab-content:visible').count(), 2);
    assert.equal(await handout.frameLocator('iframe[title="Interactive slide background"]').getByRole('slider', { name: 'Width' }).count(), 1);
    await context.setOffline(false);
    const print = await context.newPage();
    await print.goto(`${url}?print-pdf`);
    await print.waitForFunction(() => document.querySelectorAll('.pdf-page').length >= 26);
    assert.ok(await print.getByText('This explanation appears on that same step.').isVisible());
    assert.ok(await print.getByText('First: identify the changing state.').isVisible());
    assert.ok(await print.getByText('Next: compute the quantity from that state.').isVisible());
    await print.pdf({ path: `${artifacts}/features.pdf`, printBackground: true, preferCSSPageSize: true });
  } finally {
    await browser?.close();
    await new Promise(resolve => server.close(resolve));
  }
});

test('online Python: real execution, errors, fresh state, and stop control', { timeout: 120000, skip: process.env.RUN_ONLINE_TESTS !== '1' }, async () => {
  const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser = await chromium.launch({ headless: true, ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}) });
  try {
    const page = await browser.newPage();
    await page.goto(`file://${root}_build/html/reveal/features.html`);
    await page.waitForFunction(() => window.deckReady);
    await page.evaluate(() => { const s = document.getElementById('slide-live-python-in-the-browser'); const { h, v } = Reveal.getIndices(s); Reveal.slide(h, v); });
    const frame = page.frameLocator('.present iframe');
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Done$/ }).waitFor({ timeout: 60000 });
    assert.equal((await frame.locator('#output').innerText()).trim(), '10');
    await frame.getByRole('textbox', { name: 'Python code' }).fill('x = 9\nprint(x)');
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Done$/ }).waitFor({ timeout: 30000 });
    await frame.getByRole('textbox', { name: 'Python code' }).fill('print("x" in globals())');
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Done$/ }).waitFor({ timeout: 30000 });
    assert.equal((await frame.locator('#output').innerText()).trim(), 'False');
    await frame.getByRole('textbox', { name: 'Python code' }).fill('raise ValueError("expected test error")');
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Error$/ }).waitFor({ timeout: 30000 });
    assert.match(await frame.locator('#output').innerText(), /expected test error/);
    await frame.getByRole('textbox', { name: 'Python code' }).fill('while True: pass');
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Running/ }).waitFor({ timeout: 30000 });
    await frame.getByRole('button', { name: 'Stop', exact: true }).click();
    assert.equal(await frame.locator('#status').innerText(), 'Stopped');
    await page.screenshot({ path: `${artifacts}/python.png` });
  } finally { await browser.close(); }
});
