import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { renderSlides, escapeHtml, splitSlides, walk } from './render.mjs';
import { buildProvenance } from './provenance.mjs';
import { selectSlides } from './selection.mjs';
import { localFile } from './assets.mjs';
import { loadDocuments, selectDocument, sourceName } from './project.mjs';

const packageRoot = fileURLToPath(new URL('../', import.meta.url));
const read = (relative) => fs.readFileSync(path.join(packageRoot, relative), 'utf8');
const script = (source) => `<script>${source.replace(/<\/script/gi, '<\\/script')}</script>`;

const readingScripts = () => script(read('node_modules/reveal.js/plugin/highlight/highlight.js')) + script('RevealHighlight().hljs.highlightAll();');

function mathCss() {
  return read('node_modules/katex/dist/katex.min.css').replace(/url\(([^)]+)\)/g, (_match, url) => {
    const font = url.replace(/["']/g, '');
    const bytes = fs.readFileSync(path.join(packageRoot, 'node_modules/katex/dist', font));
    const mime = { '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' }[path.extname(font)];
    if (!mime) throw new Error(`Unexpected font type: ${font}`);
    return `url(data:${mime};base64,${bytes.toString('base64')})`;
  });
}

export function exportDeck(projectDir, outputFile, overrides = {}) {
  const configFile = path.join(projectDir, 'slides.json');
  const config = { ...(fs.existsSync(configFile) ? JSON.parse(fs.readFileSync(configFile, 'utf8')) : {}), ...overrides };
  if (config.reveal?.plugins) throw new Error('Use top-level plugins to bundle Reveal extensions.');
  const pluginScripts = (config.plugins || []).map(plugin => {
    if (!/^[A-Za-z_$][\w$]*$/.test(plugin.global)) throw new Error('A plugin needs a valid browser global name.');
    return script(fs.readFileSync(localFile(projectDir, plugin.script), 'utf8'));
  }).join('\n');
  const documents = config.documents || loadDocuments(projectDir);
  if (!config.document && documents.length !== 1) throw new Error('A multi-document project needs a decks list in slides.json.');
  const document = config.document || documents[0];
  const publicDir = path.join(projectDir, '_build/site/public');
  const settings = { ...config, documents, projectDir };
  const preset = config.preset || 'lecture';
  if (!['lecture', 'seminar', 'conference'].includes(preset)) throw new Error(`Unknown presentation preset: ${preset}`);
  if (!['worked', 'exercises'].includes(config.handoutMode || 'worked')) throw new Error('handoutMode must be worked or exercises.');
  if (!['light','dark'].includes(config.theme || 'light')) throw new Error('theme must be light or dark.');
  const body = renderSlides(document, publicDir, settings);
  const notices = `<template id="third-party-notices">${escapeHtml('Reveal.js\n' + read('node_modules/reveal.js/LICENSE') + '\nKaTeX\n' + read('node_modules/katex/LICENSE'))}</template>`;
  const extraCss = (config.css || []).map(file => fs.readFileSync(localFile(projectDir, file), 'utf8'));
  const css = [read('node_modules/reveal.js/dist/reveal.css'), mathCss(), read('theme.css'), read('components.css'), read('advanced.css'), ...extraCss].join('\n');
  const handoutFile = outputFile.replace(/\.html$/, '.handout.html');
  if (handoutFile === outputFile) throw new Error('Output must end in .html');
  const runtimeSettings = {
    reveal: { width: 1100, height: 700, margin: 0.06, center: false, hash: true, history: true,
      slideNumber: 'c/t', controls: true, progress: true, transition: 'slide', pdfSeparateFragments: false,
      ...config.reveal },
    variant: config.variant || null, plugins: (config.plugins || []).map(p => p.global), handout: path.basename(handoutFile),
  };
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(document.frontmatter.title)}</title>
<meta name="generator" content="MyST Reveal prototype 0.1.0; MyST 1.10.1; Reveal 5.1.0">
<style>${css.replace(/<\/style/gi, '<\\/style')}</style></head><body class="preset-${preset} theme-${config.theme || 'light'}">
${notices}
<div class="deck-label">${escapeHtml(document.frontmatter.subtitle || document.frontmatter.title)}</div>
<div class="reveal"><div class="slides">${body}</div></div>
${script(read('node_modules/reveal.js/dist/reveal.js'))}
${script(read('node_modules/reveal.js/plugin/highlight/highlight.js'))}
${script(read('node_modules/reveal.js/plugin/notes/notes.js'))}
${script(read('node_modules/reveal.js/plugin/search/search.js'))}
${script(read('node_modules/reveal.js/plugin/zoom/zoom.js'))}
${pluginScripts}
${script(`window.mystRevealSettings = ${JSON.stringify(runtimeSettings).replace(/</g, '\\u003c')};`)}
${script(read('src/exploration.js'))}
${script(read('src/advanced.js'))}
${script(read('src/runtime.js'))}
</body></html>\n`;
  fs.mkdirSync(path.dirname(outputFile), { recursive: true });
  fs.writeFileSync(outputFile, html);
  const handout = renderSlides(document, publicDir, { ...settings, handout: true }).replaceAll('href="#/', 'href="#');
  fs.writeFileSync(handoutFile, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(document.frontmatter.title)} — Handout</title>
<style>${css}\n${read('handout.css')}</style></head><body class="handout preset-${preset}">${notices}<main class="reveal"><div class="slides">${handout}</div></main>${readingScripts()}</body></html>`);
  const slideIndex = selectSlides(splitSlides(document.mdast), settings).map(slide => {
    const heading = slide.children.find(n => n.type === 'heading');
    const title = []; walk(heading, n => { if (n.value) title.push(n.value); });
    const evidence=[], paths=[];walk({children:slide.children},node=>{if(node.class==='slide-evidence')evidence.push(node.reveal);if(node.class==='slide-paths')paths.push(...node.reveal.paths);});
    return { cue:slide.options?.cue || '', evidence, paths, vertical:!!slide.options?.vertical, id: slide.id, cellIndex: slide.cellIndex, title: title.join(''), line: heading.position?.start?.line, layout: slide.options?.layout || 'default', backup: !!slide.options?.backup, timing: slide.options?.timing, tags: slide.options?.tags || [] };
  });
  return { source: document.location, preset, variant: config.variant || null, theme: config.theme || 'light', slideIndex, slides: slideIndex.length, bytes: Buffer.byteLength(html), outputFile };
}

function exportProjectFiles(projectDir, outputDir) {
  const config = JSON.parse(fs.readFileSync(path.join(projectDir, 'slides.json'), 'utf8'));
  if (!Array.isArray(config.decks) || !config.decks.length) throw new Error('slides.json needs a nonempty decks list.');
  const documents = loadDocuments(projectDir);
  const routes = {};
  const names = new Set();
  for (const deck of config.decks) {
    if (!/^[a-z][a-z0-9-]*$/.test(deck.name) || names.has(deck.name)) throw new Error(`Invalid or duplicate deck name: ${deck.name}`);
    names.add(deck.name);
    selectDocument(documents, deck.source);
    if (routes[deck.source]) throw new Error(`Duplicate deck source: ${deck.source}`);
    routes[deck.source] = { file: `${deck.name}.html`, kind: 'deck' };
  }
  for (const source of config.sources || []) {
    const doc = selectDocument(documents, source);
    if (routes[source]) throw new Error(`Source is already a deck: ${source}`);
    routes[source] = { file: `sources/${doc.slug}.html`, kind: 'source' };
  }
  const results = config.decks.map(deck => exportDeck(projectDir, path.join(outputDir, routes[deck.source].file), {
    ...config, ...deck, reveal: { ...config.reveal, ...deck.reveal },
    documents, routes, currentFile: routes[deck.source].file, document: selectDocument(documents, deck.source),
  }));
  for (const deck of config.decks) {
    for (const variant of deck.variants || []) {
      if (!/^[a-z][a-z0-9-]*$/.test(variant.name)) throw new Error('Invalid variant name.');
      const name = `${deck.name}-${variant.name}`;
      if (names.has(name)) throw new Error(`Duplicate variant output: ${name}`);
      names.add(name);
      const variantRoutes = { ...routes, [deck.source]: { file: `${name}.html`, kind: 'deck' } };
      results.push(exportDeck(projectDir, path.join(outputDir, `${name}.html`), {
        ...config, ...deck, ...variant, variant: variant.name,
        reveal: { ...config.reveal, ...deck.reveal, ...variant.reveal },
        documents, routes: variantRoutes, currentFile: `${name}.html`, document: selectDocument(documents, deck.source),
      }));
    }
  }
  for (const source of config.sources || []) {
    const doc = structuredClone(selectDocument(documents, source));
    // Reading copies retain notebook cells and anchors, but do not split into slides.
    const children = doc.mdast.children.flatMap(node => node.type === 'block' && (!node.kind || node.kind === 'notebook-content') ? node.children : [node]);
    for (const node of children) if (node.type === 'heading' && node.depth === 2) node.depth = 3;
    doc.mdast.children = [{ type: 'heading', depth: 2, identifier: 'source-page', children: [{ type: 'text', value: doc.frontmatter.title }] }, ...children];
    if (!['light','dark'].includes(config.theme || 'light')) throw new Error('theme must be light or dark.');
  const body = renderSlides(doc, path.join(projectDir, '_build/site/public'), { ...config, projectDir, documents, routes, currentFile: routes[source].file, handout: true, reading: true });
    const file = path.join(outputDir, routes[source].file);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(doc.frontmatter.title)}</title><style>${mathCss()}\n${read('theme.css')}\n${read('components.css')}\n${read('advanced.css')}\n${read('handout.css')}</style><body class="handout"><main class="reveal"><div class="slides">${body}</div></main>${readingScripts()}</body></html>`);
  }
  fs.writeFileSync(path.join(outputDir, 'provenance.json'), JSON.stringify(buildProvenance(projectDir, documents), null, 2) + '\n');
  const manifest = { version: 1, provenance: 'provenance.json', decks: results.map(({ outputFile, ...result }) => ({ ...result, file: path.basename(outputFile) })), sources: config.sources || [] };
  fs.writeFileSync(path.join(outputDir, 'decks.json'), JSON.stringify(manifest, null, 2) + '\n');
  return manifest;
}

export function exportProject(projectDir, outputDir) {
  const stage = fs.mkdtempSync(path.join(projectDir, '_build/.reveal-'));
  try {
    const manifest = exportProjectFiles(projectDir, stage);
    fs.mkdirSync(outputDir, { recursive: true });
    fs.cpSync(stage, outputDir, { recursive: true });
    return manifest;
  } finally { fs.rmSync(stage, { recursive: true, force: true }); }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const projectDir = path.resolve(process.argv[2] || 'examples/prototype');
    const outputFile = path.resolve(process.argv[3] || path.join(packageRoot, '_build/html/reveal/prototype.html'));
    const result = spawnSync(process.execPath, [path.join(packageRoot, 'node_modules/mystmd/dist/myst.cjs'),
      'build', '--site', '--execute', '--strict'], { cwd: projectDir, encoding: 'utf8' });
    const log = `${result.stdout || ''}${result.stderr || ''}`.replace(/token=[^\s]+/g, 'token=[redacted]');
    if (result.error) throw result.error;
    if (result.status !== 0) throw new Error(`MyST processing failed:\n${log}`);
    console.log(log.trim());
    const configFile = path.join(projectDir, 'slides.json');
    const multi = fs.existsSync(configFile) && JSON.parse(fs.readFileSync(configFile)).decks;
    console.log(JSON.stringify(multi ? exportProject(projectDir, process.argv[3] ? path.resolve(process.argv[3]) : path.join(packageRoot, '_build/html/reveal')) : exportDeck(projectDir, outputFile)));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
