const PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/";

function node(name, attributes = {}, text = "") {
  const el = document.createElement(name);
  Object.entries(attributes).forEach(([key, value]) => el.setAttribute(key, value));
  el.textContent = text;
  return el;
}

function injectStyles(root) {
  if (root.querySelector("#comp521-notebook-state-style")) return;
  const style = node("style", { id: "comp521-notebook-state-style" });
  style.textContent = `
    .notebook-state{max-width:70rem;border:1px solid #91b4d8;border-radius:.75rem;background:#f7fbff;padding:1rem;color:#122b38}
    .notebook-state__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:.9rem 0}
    .notebook-state__cell{padding:.75rem;border:1px solid #b7cadb;border-radius:.5rem;background:#fff;text-align:left;font:inherit;cursor:pointer}
    .notebook-state__cell:hover,.notebook-state__cell:focus{border-color:#075f63;outline:2px solid transparent;background:#eef8f7}
    .notebook-state__cell code{display:block;white-space:pre-wrap;margin-top:.4rem;font:.86em/1.4 ui-monospace,SFMono-Regular,Menlo,monospace}
    .notebook-state__controls{display:flex;gap:.6rem;flex-wrap:wrap}.notebook-state button{font:inherit;font-weight:650;padding:.45rem .7rem;border:1px solid #075f63;border-radius:.4rem;background:#fff;color:#075f63;cursor:pointer}
    .notebook-state__output{white-space:pre-wrap;min-height:3.5rem;margin-top:.85rem;padding:.75rem;border-radius:.45rem;background:#102a35;color:#f1fbfb;font:.9em/1.45 ui-monospace,SFMono-Regular,Menlo,monospace}
    @media (max-width:45rem){.notebook-state__grid{grid-template-columns:1fr}}
  `;
  root.append(style);
}

function loadPyodide() {
  return new Promise((resolve, reject) => {
    if (globalThis.loadPyodide) return resolve();
    const script = node("script", { src: `${PYODIDE_CDN}pyodide.js` });
    script.onload = resolve;
    script.onerror = () => reject(new Error("Could not load browser-local Python."));
    document.head.append(script);
  });
}

const cells = [
  ["Cell 1 · original configuration", "parameter = 70.0\ncorrection = 0.30\nprint('configuration:', parameter, correction)"],
  ["Cell 2 · revised configuration", "parameter = 67.4\ncorrection = 0.315\nprint('configuration:', parameter, correction)"],
  ["Cell 3 · calculate and record", "result = (1000 / parameter) * (1 + correction)\nrecorded_parameter = parameter\nprint('recorded parameter:', recorded_parameter)\nprint('stored result:', round(result, 3))"],
  ["Cell 4 · inspect current versus stored", "print('current parameter:', parameter)\nprint('parameter recorded with result:', recorded_parameter)\nprint('stored result:', round(result, 3))\nprint('result if recomputed now:', round((1000 / parameter) * (1 + correction), 3))"],
];

export default {
  render({ model, el }) {
    injectStyles(el.getRootNode());
    const wrapper = node("section", { class: "notebook-state", id: model.get("id") || "notebook-state", "aria-label": "Notebook state simulator" });
    wrapper.append(node("strong", {}, "Notebook State Simulator"));
    wrapper.append(node("p", {}, "Run cells in any order. Try 1 → 3 → 2 → 4, then reset and run 1 → 2 → 3 → 4."));
    const grid = node("div", { class: "notebook-state__grid" });
    const controls = node("div", { class: "notebook-state__controls" });
    const reset = node("button", { type: "button" }, "Restart kernel");
    const output = node("pre", { class: "notebook-state__output", "aria-live": "polite" }, "Python has not run yet.");
    controls.append(reset);
    wrapper.append(grid, controls, output);
    el.replaceChildren(wrapper);

    let runtime = null;
    let runtimePromise = null;
    let capture = "";
    async function getRuntime() {
      if (!runtimePromise) {
        runtimePromise = (async () => {
          await loadPyodide();
          runtime = await globalThis.loadPyodide({ indexURL: PYODIDE_CDN });
          runtime.setStdout({ batched: (text) => { capture += `${text}\n`; } });
          return runtime;
        })();
      }
      return runtimePromise;
    }
    async function execute(index) {
      capture = "";
      output.textContent = "Loading and running browser-local Python…";
      try {
        const active = await getRuntime();
        await active.runPythonAsync(cells[index][1]);
        output.textContent = `Ran ${cells[index][0]}\n\n${capture || "(no printed output)"}`;
      } catch (error) {
        output.textContent = `Python error:\n${error}`;
      }
    }
    cells.forEach(([label, code], index) => {
      const button = node("button", { type: "button", class: "notebook-state__cell" });
      button.append(node("strong", {}, label), node("code", {}, code));
      button.addEventListener("click", () => execute(index));
      grid.append(button);
    });
    reset.addEventListener("click", () => {
      runtime = null;
      runtimePromise = null;
      capture = "";
      output.textContent = "Kernel restarted. Run Cell 1 first for a clean execution.";
    });
  },
};
