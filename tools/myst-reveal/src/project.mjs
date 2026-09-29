import fs from 'node:fs';
import path from 'node:path';

export function loadDocuments(projectDir) {
  const dir = path.join(projectDir, '_build/site/content');
  return fs.readdirSync(dir).filter(name => name.endsWith('.json')).sort()
    .map(name => JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8'))).filter(doc => doc.mdast);
}
export const sourceName = doc => doc.location.replace(/^\//, '');
export function selectDocument(documents, source) {
  const found = documents.filter(doc => sourceName(doc) === source);
  if (found.length !== 1) throw new Error(`Expected one resolved MyST document for ${source}, found ${found.length}.`);
  return found[0];
}
export function findSource(documents, reference) {
  const [file, label] = reference.split('#');
  if (!label) throw new Error(`A reusable source needs a #label: ${reference}`);
  const hits = [];
  for (const doc of documents) {
    if (file && sourceName(doc) !== file) continue;
    function visit(node) {
      if ((node.identifier === label || node.html_id === label) && !['crossReference', 'cite', 'captionNumber', 'footnoteReference'].includes(node.type)) hits.push({ document: doc, node });
      for (const child of node.children || []) visit(child);
    }
    visit(doc.mdast);
  }
  if (hits.length !== 1) throw new Error(`Source ${reference} must resolve once; found ${hits.length}. Use file#label to disambiguate.`);
  return hits[0];
}
export function projectLink(settings, doc, anchor = '', handout = settings.handout) {
  const route = settings.routes?.[sourceName(doc)];
  if (route) {
    let filename = route.file;
    if (route.kind === 'deck' && handout) filename = filename.replace(/\.html$/, '.handout.html');
    const relative = path.posix.relative(path.posix.dirname(settings.currentFile || ''), filename);
    return `${relative}${anchor ? '#' + (route.kind === 'deck' && !handout ? '/' : '') + anchor : ''}`;
  }
  if (settings.siteUrl) return `${settings.siteUrl.replace(/\/$/, '')}/${doc.slug}${anchor ? '#' + anchor : ''}`;
  throw new Error(`No output route for ${sourceName(doc)}. Add it to sources or configure siteUrl.`);
}
