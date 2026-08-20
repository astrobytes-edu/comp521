export function transitDepth(p) { return p * p; }
export function normalizedFlux(p) { return 1 - transitDepth(p); }

export function mountTransitDepthFigure(container) {
  let p = 0.10;
  const render = () => {
    const depth = transitDepth(p);
    container.innerHTML = `<div class="transit-activity"><p><strong>Test the model.</strong> Increase the radius ratio and watch the disk, light curve, and values change together.</p><label>Radius ratio <i>p</i> = R<sub>p</sub>/R<sub>★</sub>: <output>${p.toFixed(2)}</output><input aria-label="Planet to star radius ratio" type="range" min="0.02" max="0.50" step="0.01" value="${p}"></label><div class="transit-activity__views"><svg viewBox="0 0 280 180" role="img" aria-label="Planet blocking part of a stellar disk"><circle cx="95" cy="90" r="68" fill="#fff2bf" stroke="#d59c28" stroke-width="3"/><circle cx="${95 + 68 * (1 - p)}" cy="90" r="${68 * p}" fill="#14283b"/><path d="M175 90 H270" stroke="#8aa6b8"/><path d="M175 90 C205 90 218 ${90 + depth * 420} 238 ${90 + depth * 420} C254 ${90 + depth * 420} 260 90 270 90" fill="none" stroke="#007f7a" stroke-width="4"/></svg><dl><dt>Blocked fraction</dt><dd>${depth.toFixed(3)}</dd><dt>Normalized flux F/F<sub>0</sub></dt><dd>${normalizedFlux(p).toFixed(3)}</dd></dl></div><p class="transit-activity__limit">Uniform-brightness, complete-overlap model: depth = p<sup>2</sup>.</p></div>`;
    container.querySelector("input").oninput = (event) => { p = Number(event.target.value); render(); };
  };
  render();
}
