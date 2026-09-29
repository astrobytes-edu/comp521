import { findSource } from './project.mjs';

const walk = (node, visit) => { visit(node); for (const child of node.children || []) walk(child, visit); };
export function prepareDocument(document, settings) {
  const doc = structuredClone(document);
  function expand(node) {
    if (node.class === 'slide-code-example') {
      const opts = node.reveal;
      const source = findSource(settings.documents || [document], opts.source);
      if (source.node.type !== 'block' || !source.node.children?.some(n => n.type === 'code')) throw new Error(`Code example ${opts.source} must reference a notebook cell.`);
      if (!['both', 'code', 'output'].includes(opts.view || 'both')) throw new Error('Code example view must be both, code, or output.');
      walk(source.node, n => { if (n.jupyter_data?.output_type === 'error') throw new Error(`Failed source cell: ${opts.source}`); });
      node.children = structuredClone(source.node.children).filter(n => opts.view === 'code' ? n.type === 'code' : opts.view === 'output' ? n.type === 'outputs' : true);
      node.reveal.sourceDocument = source.document.location;
      walk(node, n => {
        delete n.identifier; delete n.html_id;
        if (n.type === 'code') n.reveal = { ...n.reveal, title: opts.title, lines: opts.lines, steps: opts.steps };
        if (n.type === 'output') n.outputAlt = opts.alt;
      });
    }
    if (settings.handout && settings.handoutMode === 'exercises') node.children = node.children?.filter(n => n.class !== 'slide-answer');
    for (const child of node.children || []) expand(child);
  }
  expand(doc.mdast);
  return doc;
}
