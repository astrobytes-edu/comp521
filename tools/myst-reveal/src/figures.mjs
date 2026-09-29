import fs from 'node:fs';
import path from 'node:path';
import { findSource, projectLink } from './project.mjs';
import { assetData } from './assets.mjs';

export function outputContent(data, mime, publicDir) {
  const entry = data?.data?.[mime];
  if (!entry || typeof entry !== 'object' || Array.isArray(entry)) return entry;
  if (entry.content !== undefined) return entry.content;
  if (entry.path) {
    const root = fs.realpathSync(publicDir);
    const file = fs.realpathSync(path.resolve(root, entry.path.replace(/^\//, '')));
    if (!file.startsWith(root + path.sep)) throw new Error('Notebook output escapes the MyST asset directory.');
    return fs.readFileSync(file, mime === 'image/png' ? 'base64' : 'utf8');
  }
}
function allOutputs(node) {
  const results = [];
  function visit(n) { if (n.type === 'output') results.push(n); for (const c of n.children || []) visit(c); }
  visit(node); return results;
}
export function sourceImage(opts, settings, publicDir) {
  if (!opts.source.includes('#')) return { data: assetData(settings.projectDir, opts.source) };
  const source = findSource(settings.documents, opts.source);
  const outputs = allOutputs(source.node);
  if (outputs.some(n => n.jupyter_data?.output_type === 'error')) throw new Error(`Failed figure source: ${opts.source}`);
  const images = outputs.flatMap(n => {
    for (const mime of ['image/svg+xml', 'image/png']) {
      const value = outputContent(n.jupyter_data, mime, publicDir);
      if (value) return [`data:${mime};base64,${mime === 'image/png' ? [value].flat().join('') : Buffer.from([value].flat().join('')).toString('base64')}`];
    }
    return [];
  });
  if (images.length !== 1) throw new Error(`Figure ${opts.source} must contain exactly one image output; found ${images.length}.`);
  return { data: images[0], href: projectLink(settings, source.document, source.node.html_id || source.node.identifier), source: source.document.location };
}
function imageSize(data) {
  const bytes = Buffer.from(data.split(',')[1], 'base64');
  if (data.startsWith('data:image/png;')) return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
  if (data.startsWith('data:image/jpeg;')) {
    let offset = 2;
    while (offset + 8 < bytes.length) {
      if (bytes[offset] !== 255) break;
      const marker = bytes[offset + 1], length = bytes.readUInt16BE(offset + 2);
      if ([192, 193, 194, 195, 197, 198, 199, 201, 202, 203, 205, 206, 207].includes(marker)) return [bytes.readUInt16BE(offset + 7), bytes.readUInt16BE(offset + 5)];
      if (length < 2) break;
      offset += length + 2;
    }
  }
  const svg = bytes.toString('utf8');
  const view = /viewBox=["']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)/.exec(svg);
  if (view) return [Number(view[1]), Number(view[2])];
  throw new Error('Scientific figures require PNG, JPEG, or SVG with a viewBox.');
}
export function figureHtml(opts, settings, publicDir, escape) {
  const image = sourceImage(opts, settings, publicDir);
  if (!opts.alt) throw new Error('Scientific figures require descriptive alt text.');
  if (!Array.isArray(opts.annotations)) throw new Error('Figure annotations must be a JSON list.');
  const annotations = opts.annotations.map((a, i) => {
    if (![a.x, a.y].every(n => Number.isFinite(n) && n >= 0 && n <= 100) || !a.text || (a.step !== undefined && (!Number.isInteger(a.step) || a.step < 0))) throw new Error('Annotation coordinates must be percentages; step must be a nonnegative integer.');
    const fragment = a.step !== undefined && !settings.handout ? ` fragment" data-fragment-index="${a.step}` : '';
    return { marker: `<span class="figure-marker${fragment}" style="left:${a.x}%;top:${a.y}%" aria-label="${escape(a.text)}">${i + 1}</span>`, label: `<li class="figure-annotation${fragment}">${escape(a.text)}</li>` };
  });
  const [imageWidth, imageHeight] = imageSize(image.data);
  let inset = '', region = '';
  if (opts.focus) {
    const box = opts.focus.split(/\s+/).map(Number), [x, y, w, h] = box;
    if (box.length !== 4 || !box.every(Number.isFinite) || x < 0 || y < 0 || w <= 0 || h <= 0 || x + w > 100 || y + h > 100) throw new Error('Figure focus must be x y width height in percentages within 0..100.');
    region = `<span class="figure-region" style="left:${x}%;top:${y}%;width:${w}%;height:${h}%" aria-label="Region shown in magnified detail"></span>`;
    const [width, height] = imageSize(image.data);
    inset = `<figure class="figure-inset"><svg role="img" aria-label="${escape('Magnified detail: ' + opts.alt)}" viewBox="${x * width / 100} ${y * height / 100} ${w * width / 100} ${h * height / 100}"><image href="${image.data}" width="${width}" height="${height}"/></svg><figcaption>Magnified detail</figcaption></figure>`;
  }
  return `<figure class="scientific-figure"><div class="figure-composition"><div class="figure-canvas" style="--image-aspect:${imageWidth / imageHeight};max-width:calc(var(--figure-height, 360px) * ${imageWidth / imageHeight})"><img src="${image.data}" alt="${escape(opts.alt)}">${annotations.map(a => a.marker).join('')}${region}</div>${inset}</div>${opts.caption ? `<figcaption>${escape(opts.caption)}</figcaption>` : ''}${annotations.length ? `<ol class="figure-annotations">${annotations.map(a => a.label).join('')}</ol>` : ''}${image.href ? `<a class="source-link" href="${escape(image.href)}">Source: ${escape(image.source)}</a>` : ''}${!settings.handout ? '<button type="button" class="figure-enlarge">Enlarge figure</button>' : ''}</figure>`;
}
export function linkedPlotHtml(opts, settings, publicDir, escape) {
  const source = findSource(settings.documents, opts.source);
  if (allOutputs(source.node).some(n => n.jupyter_data?.output_type === 'error')) throw new Error(`Failed plot source: ${opts.source}`);
  const data = allOutputs(source.node).map(n => outputContent(n.jupyter_data, 'application/json', publicDir)).filter(Boolean);
  if (data.length !== 1) throw new Error('A linked plot requires one application/json notebook output.');
  const spec = typeof data[0] === 'string' ? JSON.parse(data[0]) : data[0];
  const x = spec.x, panels = spec.panels;
  if (!Array.isArray(x) || x.length < 2 || !x.every((v, i) => Number.isFinite(v) && (!i || v > x[i - 1])) || !Array.isArray(panels) || panels.length < 1 || panels.length > 3) throw new Error('Linked plots need increasing finite x values and one to three panels.');
  if (spec.xScale && !['linear','log'].includes(spec.xScale)) throw new Error('xScale must be linear or log.');
  if (spec.xScale === 'log' && x.some(v => v <= 0)) throw new Error('Log x values must be positive.');
  const tx = v => spec.xScale === 'log' ? Math.log10(v) : v;
  const positions = x.map(v => 65 + (tx(v)-tx(x[0]))/(tx(x.at(-1))-tx(x[0]))*560);
  const charts = panels.map(panel => {
    const vectors = [panel.values, ...(panel.lower || panel.upper ? [panel.lower, panel.upper] : [])];
    if (!panel.label || vectors.some(a => !Array.isArray(a) || a.length !== x.length || !a.every(Number.isFinite))) throw new Error('Plot panel arrays must have matching finite values and a label.');
    if (panel.lower && panel.lower.some((v, i) => v > panel.upper[i])) throw new Error('Plot lower bound exceeds upper bound.');
    if (panel.scale && !['linear','log'].includes(panel.scale)) throw new Error('Panel scale must be linear or log.');
    if (panel.scale === 'log' && vectors.flat().some(v => v <= 0)) throw new Error('Log y values must be positive.');
    if (panel.lower && !panel.bandLabel) throw new Error('Uncertainty bands require a bandLabel defining their meaning.');
    const ty = v => panel.scale === 'log' ? Math.log10(v) : v;
    const ymin = Math.min(...vectors.flat()), ymax = Math.max(...vectors.flat());
    const X = value => 65 + (tx(value) - tx(x[0])) / (tx(x.at(-1)) - tx(x[0])) * 560;
    const Y = value => 180 - (ty(value) - ty(ymin)) / (ty(ymax) - ty(ymin) || 1) * 135;
    const points = panel.values.map((v, i) => `${X(x[i])},${Y(v)}`).join(' ');
    const band = panel.lower ? `<polygon points="${panel.lower.map((v, i) => `${X(x[i])},${Y(v)}`).join(' ')} ${panel.upper.map((v, i) => `${X(x[i])},${Y(v)}`).reverse().join(' ')}" fill="#2f6f6f" opacity="0.15"/>` : '';
    return `<svg viewBox="0 0 660 225" role="img" aria-label="${escape(panel.label)}"><text x="65" y="23" class="plot-title">${escape(panel.label + (panel.scale === 'log' ? ' (log)' : ''))}</text><path d="M65 40V180H625" fill="none" stroke="#64748b"/>${band}<polyline points="${points}" fill="none" stroke="#2f6f6f" stroke-width="3"/><text x="5" y="52">${ymax.toPrecision(3)}</text><text x="5" y="183">${ymin.toPrecision(3)}</text><text x="65" y="210">${x[0]}</text><text x="605" y="210">${x.at(-1)}</text><text x="250" y="210">${escape((spec.xLabel || 'x') + (spec.xScale === 'log' ? ' (log)' : ''))}</text><line class="plot-cursor" x1="65" x2="65" y1="40" y2="180" stroke="#a65724" stroke-dasharray="4 3"/><circle class="plot-dot" cx="65" cy="${Y(panel.values[0])}" r="5" fill="#a65724" data-y="${escape(JSON.stringify(panel.values.map(Y)))}"/></svg>`;
  });
  return `<div class="linked-plot" role="group" aria-label="${escape(opts.title)}" data-plot="${escape(JSON.stringify(spec))}" data-x="${escape(JSON.stringify(positions))}"><div class="linked-panels">${charts.join('')}</div>${panels.filter(p => p.bandLabel).map(p => `<p class="band-label">${escape(p.label + ': ' + p.bandLabel)}</p>`).join('')}<label class="plot-control">Inspect sample <input type="range" aria-label="Inspect sample" min="0" max="${x.length - 1}" step="1" value="0"></label><output aria-live="polite">${escape(`${spec.xLabel || 'x'}: ${x[0]}; ${panels.map(p => `${p.label}: ${p.values[0].toPrecision(4)}`).join('; ')}`)}</output><button type="button" class="plot-reset">Reset</button><a class="source-link" href="${escape(projectLink(settings, source.document, source.node.html_id || source.node.identifier))}">Source: ${escape(source.document.location)}</a></div>`;
}
