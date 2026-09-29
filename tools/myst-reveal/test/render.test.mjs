import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { renderSlides, splitSlides, walk } from '../src/render.mjs';
import { exportDeck } from '../src/build.mjs';

const project = new URL('../examples/prototype/', import.meta.url).pathname;
const publicDir = `${project}_build/site/public`;
const fixture = () => JSON.parse(fs.readFileSync(`${project}_build/site/content/index.json`, 'utf8'));

test('six slides retain resolved references, citations, columns, notes and executed output', () => {
  const html = renderSlides(fixture(), publicDir);
  assert.equal((html.match(/<section /g) || []).length, 6);
  assert.match(html, /href="#\/slide-state-and-a-derived-quantity" data-target="rectangle-area"/);
  assert.match(html, /Figure 1:/);
  assert.match(html, /href="https:\/\/docs.python.org\/3\/tutorial\/classes.html"/);
  assert.match(html, /class="myst-reveal-columns"/);
  assert.match(html, /<aside class="notes">/);
  assert.match(html, /<div class="fragment">/);
  assert.match(html, /class="cell-output">10\n<\/pre>/);
  assert.match(html, /data:image\/svg\+xml;base64,/);
  assert.match(html, /class="katex"/);
  assert.doesNotMatch(html, /undefined|unhandled/);
});

test('MyST random keys do not affect the standalone artifact', () => {
  const doc = fixture();
  const html = renderSlides(doc, publicDir);
  walk(doc.mdast, (n) => { n.key = 'different'; });
  assert.equal(renderSlides(doc, publicDir), html);
  const a = `${project}_build/a.html`, b = `${project}_build/second/a.html`;
  exportDeck(project, a);
  exportDeck(project, b);
  assert.deepEqual(fs.readFileSync(a), fs.readFileSync(b));
});

test('unsupported widgets fail rather than disappear', () => {
  const doc = fixture();
  doc.mdast.children.push({ type: 'anywidget', esm: 'widget.mjs' });
  assert.throws(() => renderSlides(doc, publicDir), /Unsupported MyST node: anywidget/);
});

test('unresolved references and remote images fail the export', () => {
  const doc = fixture();
  walk(doc.mdast, (n) => { if (n.type === 'crossReference') n.resolved = false; });
  assert.throws(() => renderSlides(doc, publicDir), /Unresolved/);
  const remote = fixture();
  walk(remote.mdast, (n) => { if (n.type === 'image') n.url = 'https://example.com/image.svg'; });
  assert.throws(() => renderSlides(remote, publicDir), /Image must be local/);
});

test('failed, missing and unsupported cell output cannot become a successful deck', () => {
  const doc = fixture();
  walk(doc.mdast, (n) => { if (n.type === 'output') n.jupyter_data = { output_type: 'error', ename: 'AssertionError', evalue: 'wrong area' }; });
  assert.throws(() => renderSlides(doc, publicDir), /Cell failed/);
  const missing = fixture();
  walk(missing.mdast, (n) => { if (n.kind === 'notebook-code') n.children = n.children.filter(c => c.type !== 'outputs'); });
  assert.throws(() => renderSlides(missing, publicDir), /no outputs/);
  const widget = fixture();
  walk(widget.mdast, (n) => { if (n.type === 'output') n.jupyter_data = { data: { 'application/vnd.jupyter.widget-view+json': {} } }; });
  assert.throws(() => renderSlides(widget, publicDir), /Unsupported notebook output/);
});

test('headings inside columns do not start slides; content before first slide fails', () => {
  assert.equal(splitSlides(fixture().mdast).length, 6);
  assert.throws(() => splitSlides({ children: [{ type: 'paragraph', children: [] }] }), /level-two/);
});

test('MyST inline spans preserve converted scientific exponents', () => {
 const doc = fixture();
 doc.mdast.children = [{type:'heading',depth:2,children:[{type:'text',value:'Exponent'}]}, {type:'paragraph',children:[{type:'span',children:[{type:'text',value:'10'},{type:'superscript',children:[{type:'text',value:'6'}]}]}]}];
 assert.match(renderSlides(doc, publicDir), /<span>10<sup>6<\/sup><\/span>/);
});

test('course-root links work without accepting protocol-relative URLs', () => {
 const doc=fixture();
 const link=url=>({type:'paragraph',children:[{type:'link',url,children:[{type:'text',value:'Reading'}]}]});
 doc.mdast.children=[{type:'heading',depth:2,children:[{type:'text',value:'Reading'}]},link('/comp521/software-engineering-for-scientists.html')];
 assert.match(renderSlides(doc,publicDir), /href="\/comp521\/software-engineering-for-scientists.html"/);
 for(const url of ['//example.com','/\\example.com','javascript:alert(1)']) {
  doc.mdast.children[1]=link(url);
  assert.throws(()=>renderSlides(doc,publicDir), /Unsupported link/);
 }
});
