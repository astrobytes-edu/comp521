// The same locally bundled KaTeX version used by the MyST-to-Reveal package.
import katex from './katex/katex.mjs';
export function mathMarkup(tex) {
  return katex.renderToString(tex,{throwOnError:true,strict:'error',output:'htmlAndMathml'});
}
export function renderMath(root) {
  for(const node of root.querySelectorAll('[data-math]')) {
    const tex=node.dataset.math;
    if(node.dataset.renderedMath===tex) continue;
    node.innerHTML=mathMarkup(tex);
    node.dataset.renderedMath=tex;
  }
}
