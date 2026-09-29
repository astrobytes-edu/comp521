import fs from 'node:fs';
import { explanationHtml } from './explanations.mjs';
import path from 'node:path';
import { unified } from 'unified';
import { mystToHast } from 'myst-to-html';
import { all } from 'mdast-util-to-hast';
import stringify from 'rehype-stringify';
import katex from 'katex';
import { assetData, embeddedHtml } from './assets.mjs';
import { selectSlides } from './selection.mjs';
import { comparisonHtml, moviesHtml } from './science-components.mjs';
import { pythonFrame } from './python-frame.mjs';
import { prepareDocument } from './prepare.mjs';
import { projectLink } from './project.mjs';
import { outputContent, figureHtml, linkedPlotHtml } from './figures.mjs';

export const escapeHtml = (text) => String(text).replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[c]));
const text = (value) => ({ type: 'text', value });
const raw = (value) => ({ type: 'raw', value });
const id = (node) => node.html_id || node.identifier;

export function walk(node, fn) {
  fn(node);
  for (const child of node.children ?? []) walk(child, fn);
}

/** Only unwrap document/notebook prose blocks, never nested layouts or code. */
export function splitSlides(tree) {
  const notebook = tree.children.some(n => n.kind === 'notebook-code' || n.kind === 'notebook-content');
  const nodes = tree.children.flatMap((n, i) => (n.type === 'block' && (!n.kind || n.kind === 'notebook-content') ? n.children : [n]).map(node => ({ node, cellIndex: notebook ? i + 1 : undefined })));
  const slides = [];
  for (const { node, cellIndex } of nodes) {
    if (node.type === 'heading' && node.depth === 2) {
      slides.push({ id: `slide-${id(node) || slides.length + 1}`, cellIndex, children: [] });
    }
    if (!slides.length) throw new Error('Start slide content with a level-two heading (##).');
    if (node.type === 'div' && node.class === 'myst-reveal-options') {
      if (slides.at(-1).options) throw new Error('Use one slide-options block per slide.');
      slides.at(-1).options = node.reveal;
      continue;
    }
    slides.at(-1).children.push(node);
  }
  if (!slides.length) throw new Error('The document contains no slides.');
  const ids = slides.map((s) => s.id);
  if (new Set(ids).size !== ids.length) throw new Error('Slide headings must have unique identifiers.');
  return slides;
}

const supported = new Set([
  'root', 'block', 'heading', 'paragraph', 'text', 'strong', 'emphasis', 'delete',
  'inlineCode', 'code', 'break', 'thematicBreak', 'blockquote', 'list', 'listItem',
  'link', 'image', 'div', 'math', 'inlineMath', 'crossReference', 'container',
  'caption', 'captionNumber', 'cite', 'citeGroup', 'outputs', 'output',
  'table', 'tableRow', 'tableCell', 'admonition', 'admonitionTitle', 'keyboard',
  'subscript', 'superscript', 'span', 'abbreviation', 'comment',
  'tabSet', 'tabItem', 'tabLabel', 'tabContent', 'embed', 'footnoteReference', 'footnoteDefinition', 'bibliography',
]);

function safeLink(url) {
  if (!url || (!/^(https?:|mailto:|#)/i.test(url) && !/^\/(?![\/\\])[^\\]*$/.test(url))) {
    throw new Error(`Unsupported link ${JSON.stringify(url)}; use an absolute web URL, site-root path or local reference.`);
  }
  return url;
}

function imageData(url, publicDir) {
  if (/^data:image\/(png|jpeg|gif|webp|svg\+xml);base64,/.test(url)) return url;
  if (/^[a-z]+:|^\/\//i.test(url)) throw new Error(`Image must be local for offline export: ${url}`);
  const root = fs.realpathSync(publicDir);
  const file = fs.realpathSync(path.resolve(root, url.replace(/^\//, '')));
  if (!file.startsWith(root + path.sep)) throw new Error(`Image escapes the MyST public directory: ${url}`);
  const mime = { '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif' }[path.extname(file)];
  if (!mime) throw new Error(`Unsupported image format: ${file}`);
  return `data:${mime};base64,${fs.readFileSync(file).toString('base64')}`;
}

export function renderSlides(document, publicDir, settings = {}) {
  settings = { ...settings, documents: settings.documents || [document] };
  document = prepareDocument(document, settings);
  const slides = selectSlides(splitSlides(document.mdast), settings);
  if (!slides.length) throw new Error("No slides selected for this variant.");
  const definitions = new Map();
  for (const slide of slides) walk({ children: slide.children }, node => { if (node.type === 'footnoteDefinition') definitions.set(node.identifier, node); });
  const pruneDefinitions = node => { if (node.children) { node.children = node.children.filter(c => c.type !== 'footnoteDefinition'); node.children.forEach(pruneDefinitions); } };
  for (const slide of slides) {
    const tree = { children: slide.children }; pruneDefinitions(tree); slide.children = tree.children;
    const needed = new Set();
    walk(tree, node => { if (node.type === 'footnoteReference') { needed.add(node.identifier); node.footnoteId = `${slide.id}-fn-${node.identifier}`; } });
    for (const label of needed) {
      if (!definitions.has(label)) throw new Error(`Missing footnote: ${label}`);
      slide.children.push({ ...structuredClone(definitions.get(label)), html_id: `${slide.id}-fn-${label}` });
    }
  }
  const projectDir = settings.projectDir || path.resolve(publicDir, '../../..');
  const targetSlide = new Map();
  for (const slide of slides) {
    walk({ children: slide.children }, (node) => {
      if (!supported.has(node.type) && node.type !== undefined) {
        throw new Error(`Unsupported MyST node: ${node.type}. Add a tested renderer before using it.`);
      }
      if (id(node) && node.type !== 'crossReference' && node.type !== 'captionNumber' && node.type !== 'cite' && node.type !== 'footnoteReference') {
        if (targetSlide.has(id(node))) throw new Error(`Duplicate target: ${id(node)}`);
        targetSlide.set(id(node), slide.id);
      }
      if (node.type === 'block' && node.children?.some((n) => n.executable) && !node.children.some((n) => n.type === 'outputs')) {
        throw new Error('Executable code has no outputs. Build with --execute before exporting.');
      }
    });
  }
  const math = (h, node) => h(node, node.type === 'math' ? 'div' : 'span', {
    id: id(node), class: node.type === 'math' ? 'equation' : 'inline-math',
  }, [raw(katex.renderToString(node.value, {
    displayMode: node.type === 'math', throwOnError: true, trust: false,
    macros: Object.fromEntries(Object.entries(document.frontmatter?.math || {}).map(([key, value]) => [key, typeof value === 'string' ? value : value.macro])),
  })), ...(node.type === 'math' && node.enumerator ? [h(node, 'span', { class: 'equation-number' }, [text(`(${node.enumerator})`)])] : [])]);
  const referenceHref = (node) => {
    if (!node.resolved) throw new Error(`Unresolved reference: ${node.identifier}`);
    if (!node.remote && targetSlide.has(node.identifier)) return settings.reading ? `#${node.identifier}` : `#/${targetSlide.get(node.identifier)}`;
    const other = settings.documents.find(doc => `/${doc.slug}` === node.url);
    if (!other) throw new Error(`Unresolved or cross-document reference: ${node.identifier}`);
    let anchor = node.html_id || node.identifier;
    const route = settings.routes?.[other.location.replace(/^\//, '')];
    if (route?.kind === 'deck') {
      const dest = selectSlides(splitSlides(other.mdast), other.location === document.location ? settings : {}).find(slide => {
        let found = false; walk({ children: slide.children }, n => { if (id(n) === node.identifier && n.type !== 'crossReference') found = true; }); return found;
      });
      if (!dest) throw new Error(`No destination slide for ${node.identifier}`);
      anchor = dest.id;
    }
    return projectLink(settings, other, anchor);
  };
  const bibliography = (h, node) => h(node, 'ol', { class: 'bibliography' }, Object.entries(document.references?.cite?.data || {}).map(([key, ref]) => h(node, 'li', { id: `bib-${key}` }, [raw(ref.html)])));
  const handlers = {
    span(h, node) { return h(node, 'span', {}, all(h, node)); },
    div(h, node) {
      const notes = node.class === 'myst-reveal-notes';
      if (notes && settings.handout) return h(node, 'span', {}, []);
      const opts = node.reveal || {};
      const props = { class: notes ? 'notes' : node.class };
      if (node.class === 'slide-explanation') return raw(explanationHtml(opts,{...settings,projectDir},publicDir,escapeHtml));
      if (node.class === 'slide-replay') return raw('<div class="slide-replay"><button type="button" data-replay="save">Save step</button><button type="button" data-replay="start">Replay from start</button><button type="button" data-replay="next">Next saved step</button><button type="button" data-replay="return">Return to exploration</button><button type="button" data-replay="clear">Clear saved steps</button><output aria-live="polite">No saved steps.</output></div>');
      if (node.class === 'slide-evidence') {
        if (!opts.claim || !['illustrative','draft','source-backed'].includes(opts.status)) throw Error('Evidence needs a claim and status: illustrative, draft, or source-backed.');
        return h(node,'details',{class:'slide-evidence',open:settings.handout || undefined,'data-claim':opts.claim,'data-status':opts.status},[h(node,'summary',{},[text(opts.title||'Evidence and assumptions')]),h(node,'p',{class:'evidence-status'},[text(`Author status: ${opts.status}. Claim: ${opts.claim}`)]),...all(h,node)]);
      }
      if (node.class === 'slide-paths') {
        if (!Array.isArray(opts.paths)||!opts.paths.length||opts.paths.some(p=>!p.label||!p.audience||!slides.some(s=>s.id===p.target))) throw Error('Explanation paths need label, audience and an included slide ID target.');
        const audiences=[...new Set(opts.paths.map(p=>p.audience))];
        return raw(`<nav class="explanation-paths" aria-label="Explanation paths"><label>Explanation level <select aria-label="Explanation level"><option value="all">All</option>${audiences.map(a=>`<option value="${escapeHtml(a)}">${escapeHtml(a)}</option>`).join('')}</select></label>${opts.paths.map(p=>`<a data-detour="${escapeHtml(p.target)}" data-audience="${escapeHtml(p.audience)}" href="#/${escapeHtml(p.target)}">${escapeHtml(p.label)}</a>`).join('')}<button type="button" data-detour-return hidden>Return to previous explanation</button><output aria-live="polite"></output></nav>`);
      }
      if (node.class === 'slide-scientific-figure') return raw(figureHtml(opts, { ...settings, projectDir }, publicDir, escapeHtml));
      if (node.class === 'slide-image-compare') return raw(comparisonHtml(opts, { ...settings, projectDir }, publicDir, escapeHtml));
      if (node.class === 'slide-movies') return raw(moviesHtml(opts, { ...settings, projectDir }, escapeHtml));
      if (node.class === 'slide-linked-plot') return raw(linkedPlotHtml(opts, settings, publicDir, escapeHtml));
      if (['slide-question', 'slide-answer', 'slide-worked', 'slide-step', 'slide-panel'].includes(node.class)) {
        const names = { 'slide-question': 'Predict', 'slide-answer': 'Explain', 'slide-worked': 'Worked example', 'slide-step': 'Step' };
        if (['slide-answer', 'slide-step'].includes(node.class) || (node.class === 'slide-panel' && opts.index !== undefined)) {
          if (!settings.handout) { props.class += ' fragment'; props['data-fragment-index'] = opts.index; }
        }
        return h(node, 'div', props, [...(opts.title || names[node.class] ? [h(node, 'div', { class: 'component-label' }, [text(opts.title || names[node.class])])] : []), ...all(h, node)]);
      }
      if (node.class === 'slide-timer') {
        if (!Number.isInteger(opts.seconds) || opts.seconds < 1 || opts.seconds > 7200) throw new Error('Timer duration must be 1..7200 seconds.');
        return h(node, 'div', { class: 'exercise-timer', 'data-seconds': opts.seconds }, [h(node, 'span', { class: 'component-label' }, [text(opts.title || 'Think and discuss')]), h(node, 'output', { 'aria-label': 'Time remaining' }, [text(`${Math.floor(opts.seconds / 60)}:${String(opts.seconds % 60).padStart(2, '0')}`)]), ...(!settings.handout ? ['Start', 'Reset'].map(name => h(node, 'button', { type: 'button', 'data-timer-action': name.toLowerCase() }, [text(name)])) : [])]);
      }
      if (node.class === 'slide-code-example') {
        const doc = settings.documents.find(d => d.location === opts.sourceDocument);
        return h(node, 'div', { class: `code-example code-example-${opts.view || 'both'}` }, [...all(h, node), h(node, 'a', { class: 'source-link', href: projectLink(settings, doc, opts.source.split('#')[1]) }, [text(`Executed source: ${doc.location}`)])]);
      }
      if (node.class === 'fragment') {
        const effects = ['fade-in', 'fade-out', 'fade-up', 'fade-down', 'fade-left', 'fade-right', 'fade-in-then-out',
          'fade-in-then-semi-out', 'current-visible', 'grow', 'shrink', 'strike', 'semi-fade-out',
          'highlight-red', 'highlight-green', 'highlight-blue', 'highlight-current-red', 'highlight-current-green', 'highlight-current-blue'];
        if (opts.effect && !effects.includes(opts.effect)) throw new Error(`Unknown fragment effect: ${opts.effect}`);
        if (opts.index !== undefined && (!Number.isInteger(opts.index) || opts.index < 0)) throw new Error('Fragment index must be a nonnegative integer.');
        props.class += opts.effect ? ` ${opts.effect}` : '';
        props['data-fragment-index'] = opts.index;
      }
      if (node.class === 'myst-reveal-columns') {
        const count = node.children.filter(n => n.class === 'myst-reveal-column').length;
        if (count < 2 || count > 4 || node.children.some(n => n.class !== 'myst-reveal-column')) throw new Error('Columns require two to four slide-column children.');
        const ratio = opts.ratio ? opts.ratio.trim().split(/\s+/).map(Number) : Array(count).fill(1);
        if (ratio.length !== count || ratio.some(n => !Number.isFinite(n) || n <= 0)) throw new Error('Column ratio must contain one positive number per column.');
        if (opts.gap !== undefined && (!Number.isFinite(opts.gap) || opts.gap < 0 || opts.gap > 100)) throw new Error('Column gap must be 0..100 pixels.');
        if (opts.align && !['start', 'center', 'end', 'stretch'].includes(opts.align)) throw new Error('Column align must be start, center, end, or stretch.');
        props.style = `grid-template-columns:${ratio.map(n => `minmax(0, ${n}fr)`).join(' ')};gap:${opts.gap ?? 28}px;align-items:${opts.align || 'start'}`;
      }
      if (node.class === 'myst-reveal-element') {
        props['data-id'] = opts.id;
        props.style = opts.style;
        if (opts.class) props.class += ` ${opts.class}`;
      }
      if (node.class === 'myst-reveal-media') {
        const kind = opts.kind || (/\.(mp3|wav|ogg)$/i.test(opts.src) ? 'audio' : 'video');
        if (!['audio', 'video'].includes(kind)) throw new Error('Media kind must be audio or video.');
        const children = opts.captions ? [h(node, 'track', { kind: 'captions', srclang: 'en', label: 'English', default: true, src: assetData(projectDir, opts.captions) }, [])] : [];
        return h(node, kind, { src: assetData(projectDir, opts.src), controls: true,
          'aria-label': opts.title, muted: opts.muted, loop: opts.loop,
          'data-autoplay': opts.autoplay ? '' : undefined,
          poster: opts.poster ? assetData(projectDir, opts.poster) : undefined }, children);
      }
      if (node.class === 'myst-reveal-embed') {
        const frame = h(node, 'iframe', { srcdoc: embeddedHtml(projectDir, opts.src), title: opts.title,
          sandbox: 'allow-scripts', class: 'slide-embed', 'data-has-fallback': opts.fallback ? 'true' : undefined }, []);
        if (!opts.fallback) return frame;
        if (!opts.alt) throw new Error('An embed fallback needs alt text.');
        return h(node, 'div', { class: 'embed-with-fallback' }, [frame, h(node, 'figure', { class: 'embed-static' }, [h(node, 'img', { src: assetData(projectDir, opts.fallback), alt: opts.alt }, []), h(node, 'figcaption', {}, [text(opts.title)])])]);
      }
      if (node.class === 'myst-reveal-python') {
        return raw(pythonFrame(opts, { ...settings, projectDir }, publicDir, escapeHtml));
      }
      if (node.class === 'myst-reveal-bibliography') return bibliography(h, node);
      return h(node, notes ? 'aside' : 'div', props, all(h, node));
    },
    code(h, node) {
      const opts = node.reveal || {};
      if (opts.lines !== undefined && !/^[\d,|\- ]*$/.test(opts.lines)) throw new Error('Code lines must use numbers, commas, ranges and | steps.');
      if (opts.start !== undefined && (!Number.isInteger(opts.start) || opts.start < 1)) throw new Error('Code start must be a positive integer.');
      let steps;
      if (opts.steps) {
        steps = JSON.parse(opts.steps);
        if (!Array.isArray(steps) || !steps.length || steps.some(s => !s.lines || !s.explain || !/^[\d,\- ]+$/.test(s.lines))) throw new Error('Code steps need lines and explain strings.');
        opts.lines = steps.map(s => s.lines).join('|');
      }
      const pre = h(node, 'pre', { 'data-id': opts.id }, [h(node, 'code', {
        class: node.lang ? `language-${node.lang}` : undefined,
        'data-line-numbers': opts.lines, 'data-ln-start-from': opts.start,
      }, [text(node.value || '')])]);
      if (!opts.title && !steps) return pre;
      return h(node, 'div', { class: 'code-card', 'data-code-source': node.value || '', 'data-code-steps': steps ? JSON.stringify(steps) : undefined }, [
        h(node, 'div', { class: 'code-heading' }, [h(node, 'span', {}, [text(opts.title || node.lang || 'Code')]), ...(!settings.handout ? [h(node, 'button', { type: 'button', class: 'code-copy', 'aria-label': 'Copy', title: 'Copy code' }, [raw('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/></svg>')])] : [])]),
        pre, ...(steps ? [h(node, 'ol', { class: 'code-explanations' }, steps.map((step, i) => h(node, 'li', { 'data-code-step': i }, [text(step.explain)])))] : []),
      ]);
    },
    bibliography,
    embed(h, node) {
      const doc = settings.documents.find(d => d.location === node.source?.location);
      if (!doc || !node.children?.length) throw new Error('Unresolved MyST embed.');
      return h(node, 'div', { class: 'notebook-embed' }, [...all(h, node), h(node, 'a', { class: 'source-link', href: projectLink(settings, doc, node.source.label) }, [text(`Source: ${doc.location}`)])]);
    },
    footnoteReference(h, node) { return h(node, 'sup', { class: 'footnote-ref' }, [h(node, 'a', { href: `#${node.footnoteId}`, 'data-footnote': node.footnoteId, 'aria-label': `Footnote ${node.enumerator}` }, [text(node.enumerator)])]); },
    footnoteDefinition(h, node) { return h(node, 'aside', { id: node.html_id, class: 'slide-footnote', tabindex: '-1', role: 'note' }, [h(node, 'span', { class: 'footnote-number' }, [text(`${node.enumerator}. `)]), ...all(h, node)]); },
    tabSet(h, node) { return h(node, 'div', { class: 'slide-tabs' }, all(h, node)); },
    tabItem(h, node) { return h(node, 'div', { class: 'slide-tab' }, [
      h(node, 'button', { class: 'slide-tab-label', type: 'button' }, [text(node.title)]),
      h(node, 'div', { class: 'slide-tab-content' }, all(h, node)),
    ]); },
    tabLabel(h, node) { return h(node, 'button', { class: 'slide-tab-label', type: 'button' }, all(h, node)); },
    tabContent(h, node) { return h(node, 'div', { class: 'slide-tab-content' }, all(h, node)); },
    math, inlineMath: math,
    image(h, node) {
      if (!node.alt) throw new Error('Every slide image needs descriptive alt text.');
      return h(node, 'img', { src: imageData(node.url, publicDir), alt: node.alt }, []);
    },
    crossReference(h, node) {
      return h(node, 'a', { href: referenceHref(node), 'data-target': node.identifier }, all(h, node));
    },
    link(h, node) {
      if (node.url?.startsWith('#')) {
        const target = node.url.slice(1);
        const slide = targetSlide.get(target);
        if (!slide) throw new Error(`Unresolved local link: ${node.url}`);
        return h(node, 'a', { href: `#/${slide}`, 'data-target': target }, all(h, node));
      }
      return h(node, 'a', { href: safeLink(node.url), rel: 'noopener noreferrer' }, all(h, node));
    },
    captionNumber(h, node) {
      return h(node, 'span', { class: 'caption-number' }, [...all(h, node), text(' ')]);
    },
    citeGroup(h, node) { return h(node, 'span', { class: 'citation' }, [text('('), ...all(h, node).flatMap((n, i) => i ? [text('; '), n] : [n]), text(')')]); },
    cite(h, node) {
      const ref = document.references?.cite?.data?.[node.identifier];
      if (!ref) throw new Error(`Unresolved citation: ${node.identifier}`);
      if (ref.url) return h(node, 'a', { href: safeLink(ref.url), rel: 'noopener noreferrer' }, all(h, node));
      return h(node, 'span', { title: node.identifier }, all(h, node));
    },
    outputs(h, node) { return h(node, 'div', { class: 'cell-outputs', 'aria-label': 'Executed output' }, all(h, node)); },
    output(h, node) {
      const data = node.jupyter_data;
      const content = mime => outputContent(data, mime, publicDir);
      if (data?.output_type === 'error') throw new Error(`Cell failed: ${data.ename}: ${data.evalue}`);
      if (data?.output_type === 'stream') {
        if (data.name !== 'stdout') throw new Error(`Cell emitted ${data.name}; inspect it before export.`);
        return h(node, 'pre', { class: 'cell-output' }, [text([data.text].flat().join(''))]);
      }
      if (content('image/png')) return h(node, 'img', { src: `data:image/png;base64,${[content('image/png')].flat().join('')}`, alt: node.outputAlt || 'Executed notebook figure; see the slide explanation.' }, []);
      if (content('image/svg+xml')) return h(node, 'img', { src: `data:image/svg+xml;base64,${Buffer.from([content('image/svg+xml')].flat().join('')).toString('base64')}`, alt: node.outputAlt || 'Executed notebook figure; see the slide explanation.' }, []);
      if (content('text/html')) return h(node, 'iframe', { srcdoc: [content('text/html')].flat().join(''), sandbox: 'allow-scripts', title: 'Executed HTML output', class: 'slide-embed output-embed' }, []);
      if (content('application/json') && settings.reading) return h(node, 'pre', { class: 'cell-output' }, [text(JSON.stringify(content('application/json'), null, 2))]);
      if (data?.data?.['text/plain'] && Object.keys(data.data).every(k => k === 'text/plain')) {
        return h(node, 'pre', { class: 'cell-output' }, [text([content('text/plain')].flat().join(''))]);
      }
      throw new Error('Unsupported notebook output; use stdout, plain text, PNG, SVG, or self-contained HTML.');
    },
  };
  const processor = unified().use(mystToHast, { handlers }).use(stringify, { allowDangerousHtml: true });
  const rendered = slides.map((slide) => {
    const tree = { type: 'root', children: structuredClone(slide.children) };
    let html = processor.stringify(processor.runSync(tree));
    if (settings.handout && slide.options?.['background-iframe']) {
      html += `<iframe class="slide-embed" title="Interactive slide background" sandbox="allow-scripts" srcdoc="${escapeHtml(embeddedHtml(projectDir, slide.options['background-iframe']))}"></iframe>`;
    }
    const options = { ...slide.options };
    delete options.vertical;
    delete options.class;
    for (const key of ['layout', 'eyebrow', 'takeaway', 'tags', 'backup', 'fit', 'min-font', 'cue', 'evidence', 'limit']) delete options[key];
    const layout = slide.options?.layout;
    if (layout && !['title', 'section', 'figure', 'compare', 'code', 'derivation', 'result', 'summary', 'figure-wide'].includes(layout)) throw new Error(`Unknown layout: ${layout}`);
    if (slide.options?.eyebrow) html = `<p class="slide-eyebrow">${escapeHtml(slide.options.eyebrow)}</p>` + html;
    if (slide.options?.takeaway) html += `<p class="slide-takeaway">${escapeHtml(slide.options.takeaway)}</p>`;
    const fit = slide.options?.fit || settings.fit || 'none';
    const minimum = slide.options?.['min-font'] ?? settings.minFont ?? 26;
    if (!['none', 'bounded'].includes(fit) || !Number.isFinite(minimum) || minimum < 24 || minimum > 36) throw new Error('Fit must be none or bounded; min-font must be 24..36 logical pixels.');
    if (slide.options?.timing !== undefined && (!Number.isFinite(slide.options.timing) || slide.options.timing <= 0)) throw new Error('Slide timing must be positive seconds.');
    if (slide.options?.backup !== undefined && typeof slide.options.backup !== 'boolean') throw new Error('backup must be boolean.');
    if (slide.options?.cue && !settings.handout) html += `<aside class="notes">${escapeHtml(slide.options.cue)}</aside>`;
    if (slide.options?.evidence) html += `<a class="evidence-link" href="${escapeHtml(safeLink(slide.options.evidence))}">Evidence</a>`;
    if (slide.options?.limit) html += `<p class="claim-limit">${escapeHtml(slide.options.limit)}</p>`;
    const metadata = `data-source="${escapeHtml(document.location)}" data-source-cell="${slide.cellIndex || ''}" data-source-line="${slide.children.find(n => n.type === 'heading')?.position?.start?.line || ''}" data-fit="${fit}" data-min-font="${minimum}"${slide.options?.backup ? ' data-backup="true"' : ''}`;
    const classes = [slide.options?.class, layout ? `layout-${layout}` : ''].filter(Boolean).join(' ');
    const attrs = Object.entries(options).map(([key, value]) => {
      if (!/^(?:transition(?:-speed)?|background(?:-color|-image|-size|-position|-repeat|-opacity|-video|-video-loop|-video-muted|-iframe|-interactive|-transition)?|auto-animate(?:-id|-restart|-duration|-delay|-easing|-unmatched)?|autoslide|visibility|state|timing)$/.test(key)) throw new Error(`Unsupported slide attribute: ${key}`);
      if (['background-image', 'background-video'].includes(key)) value = assetData(projectDir, value);
      if (key === 'background-iframe') value = `data:text/html;base64,${Buffer.from(embeddedHtml(projectDir, value)).toString('base64')}`;
      if (value === false && ['auto-animate', 'auto-animate-restart', 'background-video-loop', 'background-video-muted'].includes(key)) return '';
      return `data-${key}="${escapeHtml(value === true ? '' : value)}"`;
    }).join(' ');
    return `<section id="${escapeHtml(slide.id)}" ${metadata}${attrs ? ' ' + attrs : ''}${classes ? ` class="${escapeHtml(classes)}"` : ''}>${html}</section>`;
  });
  const groups = [];
  for (let i = 0; i < slides.length; i++) {
    if (slides[i].options?.vertical) {
      if (!groups.length) throw new Error('A vertical slide needs a preceding horizontal slide.');
      groups.at(-1).push(rendered[i]);
    } else groups.push([rendered[i]]);
  }
  return groups.map(group => group.length === 1 ? group[0] : `<section>${group.join('\n')}</section>`).join('\n');
}
