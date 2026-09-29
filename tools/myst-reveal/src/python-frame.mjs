import fs from 'node:fs';
import { sourceImage } from './figures.mjs';
export function pythonFrame(opts, settings, publicDir, escape) {
  const packages = opts.packages ? opts.packages.split(',').map(s => s.trim()) : [];
  if (packages.some(p => !['numpy', 'matplotlib'].includes(p))) throw new Error('Browser Python packages currently support numpy and matplotlib.');
  if ((packages.includes('matplotlib') || opts.fallback) && !opts.alt) throw new Error('Live Python figures need descriptive alt text.');
  const parameters = opts.parameters ? JSON.parse(opts.parameters) : [];
  if (!Array.isArray(parameters) || parameters.length > 4 || parameters.some(p => !/^[A-Za-z_]\w*$/.test(p.name) || !p.label || ![p.min,p.max,p.step,p.value].every(Number.isFinite) || p.max <= p.min || p.step <= 0 || p.value < p.min || p.value > p.max) || new Set(parameters.map(p => p.name)).size !== parameters.length) throw new Error('Python parameters need unique names, labels, finite bounds, positive steps, and an initial value in range.');
  let runtime = settings.pythonRuntime || 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/';
  if (!/^https?:\/\//.test(runtime) || !runtime.endsWith('/')) throw new Error('pythonRuntime must be an absolute HTTP(S) directory URL ending with /.');
  const fallback = opts.fallback ? sourceImage({ source: opts.fallback }, settings, publicDir) : null;
  let template = fs.readFileSync(new URL('./python-widget.html', import.meta.url), 'utf8');
  const replacements = {
    '__THEME__': settings.theme === 'dark' ? 'dark' : 'light', '__PYTHON_SOURCE__': escape(opts.source), '__FIGURE_ALT__': escape(opts.alt || 'Python output'),
    '__PYTHON_PACKAGES__': JSON.stringify(packages), '__PARAMETERS__': JSON.stringify(parameters).replace(/</g, '\\u003c'),
    '__RUNTIME__': JSON.stringify(runtime).replace(/</g, '\\u003c'), '__TRACE_ENABLED__': String(!!opts.trace),
    '__FALLBACK__': fallback ? `<img src="${fallback.data}" alt="${escape(opts.alt)}"><p>Precomputed result from the authored source; not the current edit.</p>` : '',
    '__HIGHLIGHT_SCRIPT__': fs.readFileSync(new URL('../node_modules/reveal.js/plugin/highlight/highlight.js', import.meta.url), 'utf8').replace(/<\/script/gi, '<\\/script'),
  };
  // A single pass prevents user source that resembles a placeholder from being substituted.
  template = template.replace(/__(?:THEME|PYTHON_SOURCE|FIGURE_ALT|PYTHON_PACKAGES|PARAMETERS|RUNTIME|TRACE_ENABLED|FALLBACK|HIGHLIGHT_SCRIPT)__/g, key => replacements[key]);
  const frame = `<iframe srcdoc="${escape(template)}" title="Live Python experiment" sandbox="allow-scripts" class="slide-embed python-embed"${fallback ? ' data-has-fallback="true"' : ''}></iframe>`;
  return fallback ? `<div class="embed-with-fallback">${frame}<figure class="embed-static"><img src="${fallback.data}" alt="${escape(opts.alt)}"><figcaption>Precomputed Python result</figcaption></figure></div>` : frame;
}
