import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { chromium } from 'playwright';
import { exportProject } from '../src/build.mjs';
import { loadDocuments } from '../src/project.mjs';
import { renderSlides } from '../src/render.mjs';
import { previewServer } from '../src/preview.mjs';

const root = new URL('../', import.meta.url).pathname;
const project = `${root}examples/courses`;
const artifacts = `${root}_build/courses-checks`;
fs.mkdirSync(artifacts, { recursive: true });
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const launch = () => chromium.launch({ headless: true, ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}) });

test('project export: shared notebook outputs, portable routes, bibliography, and exercise handout exclusion', () => {
  const result = exportProject(project, `${root}_build/project-check`);
  assert.deepEqual(result.decks.slice(0, 2).map(d => d.slides), [13, 10]);
  const html = fs.readFileSync(`${root}_build/project-check/computation.html`, 'utf8');
  assert.match(html, /astronomy.html#\/slide-astro-start/);
  assert.match(html, /sources\/methods.html#synthetic-method/);
  assert.match(html, /data:image\/png;base64,/);
  assert.match(html, /class="bibliography"/);
  const handout = fs.readFileSync(`${root}_build/project-check/computation.handout.html`, 'utf8');
  assert.doesNotMatch(handout, /They are|The result is/);
  assert.match(handout, /astronomy.handout.html#slide-astro-start/);
  assert.ok(fs.existsSync(`${root}_build/project-check/sources/analysis.html`));
  const docs = loadDocuments(project), doc = structuredClone(docs.find(d => d.location === '/astronomy.md'));
  const mutate = n => { if (n.class === 'slide-scientific-figure') n.reveal.focus = '99 99 10 10'; (n.children || []).forEach(mutate); };
  mutate(doc.mdast);
  assert.throws(() => renderSlides(doc, `${project}/_build/site/public`, { projectDir: project, documents: docs, siteUrl: '/comp521' }), /Figure focus/);
});

test('course browser: code explanations, computed figures, links, annotations, linked plots, timers, handouts and print', { timeout: 150000 }, async () => {
  const server = previewServer(`${root}_build/html`);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const browser = await launch();
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, permissions: ['clipboard-read', 'clipboard-write'] });
    const page = await context.newPage();
    const errors = [], remote = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('request', r => { if (/^https?:/.test(r.url()) && !r.url().startsWith('http://127.0.0.1:')) remote.push(r.url()); });
    const base = `http://127.0.0.1:${server.address().port}/comp521/reveal`;
    const go = async i => { await page.evaluate(i => { Reveal.slide(i, 0, -1); }, i); await page.waitForTimeout(350); };
    await page.goto(`${base}/computation.html`); await page.waitForFunction(() => window.deckReady);
    await go(2);
    assert.equal(await page.locator('.present .slide-answer').getAttribute('aria-hidden'), 'true');
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('.present .slide-answer').getAttribute('aria-hidden'), 'false');
    await go(3);
    assert.equal(await page.locator('.present .code-explanations li:visible').textContent(), 'Choose the input values.');
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('.present .code-explanations li:visible').textContent(), 'Transform each input independently.');
    const copy = page.getByRole('button', { name: 'Copy', exact: true }).filter({ visible: true });
    assert.equal(await copy.locator('svg').count(), 1);
    assert.equal(await copy.textContent(), '');
    await copy.click();
    assert.equal(await page.evaluate(() => navigator.clipboard.readText()), 'values = [0, 1, 2, 3]\nsquares = [x * x for x in values]\nprint(squares)');
    await go(4);
    assert.match(await page.locator('.present .cell-output').textContent(), /\[0, 1, 4, 9\]/);
    await go(5); assert.equal(await page.locator('.present .cell-outputs img').count(), 1);
    await go(6);
    assert.equal(await page.locator('.present .figure-inset svg').count(), 1);
    await page.getByRole('button', { name: 'Enlarge figure', exact: true }).filter({ visible: true }).click();
    assert.ok(await page.getByRole('dialog', { name: 'Enlarged figure' }).isVisible());
    await page.keyboard.press('Escape');
    await go(9);
    const timer = page.locator('.present .exercise-timer');
    await timer.getByRole('button', { name: 'Start', exact: true }).click();
    await page.waitForTimeout(1200);
    assert.notEqual(await timer.locator('output').textContent(), '1:30');
    await timer.getByRole('button', { name: 'Reset', exact: true }).click();
    assert.equal(await timer.locator('output').textContent(), '1:30');
    await go(11);
    await page.locator('.present .footnote-ref a').click();
    assert.equal(await page.evaluate(() => document.activeElement.className), 'slide-footnote');
    await page.locator('.present a[data-target="astro-start"]').click();
    await page.waitForFunction(() => window.deckReady && Reveal.getSlides().length === 10);
    await go(3);
    const slider = page.getByRole('slider', { name: 'Inspect sample' });
    await slider.fill('10');
    const cursors = await page.locator('.present .plot-cursor').evaluateAll(els => els.map(e => e.getAttribute('x1')));
    assert.equal(cursors.length, 2); assert.equal(cursors[0], cursors[1]);
    assert.match(await page.locator('.present output').textContent(), /Time \(arbitrary units\): 1;/);
    await page.getByRole('button', { name: 'Reset', exact: true }).filter({ visible: true }).click();
    assert.equal(await slider.inputValue(), '0');
    for (const [deck, count] of [['computation', 13], ['astronomy', 10]]) {
      await page.goto(`${base}/${deck}.html`); await page.waitForFunction(() => window.deckReady);
      for (const viewport of [{ width: 1440, height: 900 }, { width: 1280, height: 720 }]) {
        await page.setViewportSize(viewport);
        await page.evaluate(() => Reveal.configure({ transition: 'none', backgroundTransition: 'none', autoAnimate: false }));
        for (let i = 0; i < count; i++) {
          await page.evaluate(i => { Reveal.slide(i, 0, 99); Reveal.layout(); }, i);
          await page.waitForTimeout(300);
          const bounds = await page.evaluate(() => { const s = Reveal.getCurrentSlide(); return { height: s.scrollHeight, width: s.scrollWidth, code: [...s.querySelectorAll('pre code')].some(c => c.scrollWidth > c.clientWidth + 2) }; });
          assert.ok(bounds.height <= 700 && bounds.width <= 1100 && !bounds.code, `${deck} slide ${i + 1}: ${JSON.stringify(bounds)}`);
          if (viewport.width === 1440) await page.screenshot({ path: `${artifacts}/${deck}-${i + 1}.png` });
        }
      }
      const print = await context.newPage(); await print.goto(`${base}/${deck}.html?print-pdf`);
      await print.waitForFunction(n => document.querySelectorAll('.pdf-page').length >= n, count);
      await print.waitForFunction(() => getComputedStyle(document.querySelector('section.layout-compare')).display === 'grid');
      await print.pdf({ path: `${artifacts}/${deck}.pdf`, printBackground: true, preferCSSPageSize: true });
      if (deck === 'astronomy') assert.ok(await print.locator('.embed-static img').isVisible());
      await print.close();
    }
    assert.deepEqual(errors, []); assert.deepEqual(remote, []);
    await context.setOffline(true);
    await page.goto(`file://${root}_build/html/reveal/computation.html`); await page.waitForFunction(() => window.deckReady);
    await go(5); await page.locator('.present .source-link').click();
    assert.match(page.url(), /sources\/analysis.html#quadratic-cell/);
    assert.equal(await page.locator('#quadratic-cell').count(), 1);
    await page.goto(`file://${root}_build/html/reveal/computation.handout.html`);
    assert.equal(await page.locator('.slide-answer').count(), 0);
    await page.goto(`file://${root}_build/html/reveal/astronomy.handout.html`);
    assert.ok(await page.getByText('At t=0,1,2,3,4', { exact: false }).count() || await page.locator('.slide-answer').count() > 0);
  } finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
});

test('online browser Python generates a real Matplotlib figure and resets', { timeout: 150000, skip: process.env.RUN_ONLINE_TESTS !== '1' }, async () => {
  const browser = await launch();
  try {
    const page = await browser.newPage(); await page.goto(`file://${root}_build/html/reveal/computation.html#/slide-edit-code-and-generate-a-plot`); await page.waitForFunction(() => window.deckReady);
    const frame = page.frameLocator('.present iframe');
    assert.ok(await frame.locator('#highlighted .hljs-keyword').count() > 0);
    const initial = await frame.locator('#code').inputValue();
    await frame.locator('#code').fill('# A comment\nvalue = 42\nprint("hello")');
    assert.equal(await frame.locator('#highlighted .hljs-comment').textContent(), '# A comment');
    assert.equal(await frame.locator('#highlighted .hljs-number').textContent(), '42');
    assert.equal(await frame.locator('#highlighted .hljs-string').textContent(), '"hello"');
    await frame.getByRole('button', { name: 'Reset', exact: true }).click();
    assert.equal(await frame.locator('#code').inputValue(), initial);
    assert.ok(await frame.locator('#highlighted .hljs-keyword').count() > 0);
    await frame.getByRole('button', { name: 'Run Python', exact: true }).click();
    await frame.locator('#status').filter({ hasText: /^Done$/ }).waitFor({ timeout: 90000 });
    assert.equal(await frame.locator('#figures img').count(), 1);
    assert.ok(await frame.locator('#figures img').evaluate(img => img.complete && img.naturalWidth > 0));
    await page.screenshot({ path: `${artifacts}/live-python.png` });
    await frame.getByRole('button', { name: 'Reset', exact: true }).click();
    assert.equal(await frame.locator('#status').innerText(), 'Ready');
    assert.equal(await frame.locator('#figures img').count(), 0);
  } finally { await browser.close(); }
});

test('a late deck error preserves all previous project outputs', () => {
  const copy = `${root}_build/failing-project`, output = `${root}_build/failing-output`;
  fs.mkdirSync(`${copy}/_build`, { recursive: true });
  fs.cpSync(`${project}/_build/site`, `${copy}/_build/site`, { recursive: true });
  for (const name of ['area-widget.html', 'rectangle.svg']) fs.copyFileSync(`${project}/${name}`, `${copy}/${name}`);
  const config = JSON.parse(fs.readFileSync(`${project}/slides.json`));
  config.decks[1].preset = 'unknown-preset';
  fs.writeFileSync(`${copy}/slides.json`, JSON.stringify(config));
  fs.mkdirSync(output, { recursive: true });
  fs.writeFileSync(`${output}/computation.html`, 'previous successful artifact');
  assert.throws(() => exportProject(copy, output), /Unknown presentation preset/);
  assert.equal(fs.readFileSync(`${output}/computation.html`, 'utf8'), 'previous successful artifact');
  assert.equal(fs.existsSync(`${output}/computation.handout.html`), false);
});
