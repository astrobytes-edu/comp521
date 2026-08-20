const PYODIDE_CDN = "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/";
let runtime = null;
let runtimePromise = null;
let currentCapture = null;

function loadScript(source) {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(`script[src="${source}"]`);
    if (existing) return resolve();
    const script = document.createElement("script");
    script.src = source;
    script.onload = resolve;
    script.onerror = () => reject(new Error("Could not load browser-local Python."));
    document.head.append(script);
  });
}

async function getRuntime(packages) {
  if (!runtimePromise) {
    runtimePromise = (async () => {
      if (typeof globalThis.loadPyodide !== "function") await loadScript(`${PYODIDE_CDN}pyodide.js`);
      runtime = await globalThis.loadPyodide({ indexURL: PYODIDE_CDN });
      runtime.setStdout({ batched: (text) => { if (currentCapture) currentCapture.stdout += `${text}\n`; } });
      runtime.setStderr({ batched: (text) => { if (currentCapture) currentCapture.stderr += `${text}\n`; } });
      return runtime;
    })();
  }
  const activeRuntime = await runtimePromise;
  if (packages.length) await activeRuntime.loadPackage(packages);
  return activeRuntime;
}

async function resetRuntime() {
  runtime = null;
  runtimePromise = null;
}

function element(name, attributes = {}, text = "") {
  const node = document.createElement(name);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
  node.textContent = text;
  return node;
}

const STYLE_ID = "comp521-interactive-python-styles";
const STYLES = `
.comp521-experiment{margin:1.5rem 0;border:1px solid #91b4d8;border-radius:.6rem;background:#f7fbff;color:#172b3a;padding:1rem}.comp521-experiment-header{display:flex;justify-content:space-between;gap:1rem;align-items:center}.comp521-controls{display:grid;gap:.75rem;margin:1rem 0}.comp521-control{display:grid;grid-template-columns:minmax(10rem,1fr) 2fr 3rem;gap:.75rem;align-items:center}.comp521-editor{box-sizing:border-box;width:100%;min-height:14rem;padding:.75rem;font:0.9rem/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#fff;color:#172b3a;border:1px solid #91b4d8;border-radius:.35rem}.comp521-run,.comp521-reset{margin-top:.75rem;padding:.45rem .75rem;border-radius:.3rem;border:1px solid #195c8f;font-weight:600;cursor:pointer}.comp521-run{background:#195c8f;color:#fff}.comp521-reset{background:#fff;color:#195c8f}.comp521-status{margin:.75rem 0;font-size:.95rem}.comp521-output{padding:.75rem;background:#fff;border:1px solid #c7d7e6;border-radius:.35rem}.comp521-output pre{white-space:pre-wrap;overflow:auto}.comp521-output img{display:block;max-width:100%;height:auto;margin-top:.75rem}.comp521-error{color:#a61b1b}@media (max-width:40rem){.comp521-control{grid-template-columns:1fr}.comp521-experiment-header{align-items:flex-start;flex-direction:column}.comp521-reset{margin-top:0}}`;

function ensureStyles(el) {
  const root = el.getRootNode();
  if (root.querySelector?.(`#${STYLE_ID}`)) return;
  const style = element("style", { id: STYLE_ID });
  style.textContent = STYLES;
  root.append(style);
}

function injectControls(controls) {
  return Object.entries(controls).map(([name, control]) => `${name} = ${Number(control.value)}`).join("\n");
}

async function run(code, controls, packages) {
  const activeRuntime = await getRuntime(packages);
  const capture = { stdout: "", stderr: "" };
  currentCapture = capture;
  try {
    // Force the non-interactive backend before student code imports pyplot.
    // The browser backend otherwise creates a second canvas at document level,
    // outside this widget and therefore after MyST's page footer.
    activeRuntime.runPython("import warnings\nwarnings.filterwarnings('ignore', message='FigureCanvasAgg is non-interactive')\nimport matplotlib\nmatplotlib.use('Agg', force=True)\nimport matplotlib.pyplot as plt\nplt.close('all')");
    await activeRuntime.runPythonAsync(`${injectControls(controls)}\n${code}`);
    const figures = activeRuntime.runPython(`
import base64, io, json
import matplotlib.pyplot as plt
images = []
for number in plt.get_fignums():
    buffer = io.BytesIO()
    plt.figure(number).savefig(buffer, format="png", bbox_inches="tight", dpi=120)
    images.append("data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode())
json.dumps(images)
`);
    return { ...capture, figures: JSON.parse(figures), error: null };
  } catch (error) {
    return { ...capture, figures: [], error: String(error) };
  } finally {
    currentCapture = null;
  }
}

function render({ model, el }) {
  ensureStyles(el);
  const controls = structuredClone(model.get("controls") || {});
  const packages = model.get("packages") || [];
  const id = model.get("id") || "interactive-python";
  const wrapper = element("section", { class: "comp521-experiment", "aria-label": "Interactive Python experiment", id });
  const header = element("div", { class: "comp521-experiment-header" });
  header.append(element("strong", {}, "Interactive Python experiment"));
  const reset = element("button", { type: "button", class: "comp521-reset" }, "Reset Python");
  header.append(reset);
  wrapper.append(header);

  const controlsRegion = element("div", { class: "comp521-controls" });
  for (const [name, control] of Object.entries(controls)) {
    const label = element("label", { for: `${id}-${name}` }, control.label || name);
    const value = element("output", { for: `${id}-${name}`, class: "comp521-control-value" }, Number(control.value).toFixed(2));
    const slider = element("input", { id: `${id}-${name}`, type: "range", min: control.min, max: control.max, step: control.step, value: control.value, "aria-label": control.label || name });
    slider.addEventListener("input", () => {
      control.value = Number(slider.value);
      value.textContent = Number(control.value).toFixed(2);
    });
    const group = element("div", { class: "comp521-control" });
    group.append(label, slider, value);
    controlsRegion.append(group);
  }
  if (Object.keys(controls).length) wrapper.append(controlsRegion);

  const editor = element("textarea", { class: "comp521-editor", "aria-label": "Editable Python code", spellcheck: "false" });
  editor.value = model.get("code") || "";
  const runButton = element("button", { type: "button", class: "comp521-run" }, "Run experiment");
  const status = element("p", { class: "comp521-status", "aria-live": "polite" }, "Predict before you run.");
  const output = element("div", { class: "comp521-output", "aria-live": "polite", hidden: "" });
  wrapper.append(editor, runButton, status, output);
  el.replaceChildren(wrapper);

  reset.addEventListener("click", async () => {
    reset.disabled = true;
    await resetRuntime();
    output.replaceChildren();
    output.hidden = true;
    status.textContent = "Python reset. Rerun from a clean state.";
    reset.disabled = false;
  });

  runButton.addEventListener("click", async () => {
    runButton.disabled = true;
    status.textContent = "Loading and running browser-local Python…";
    output.replaceChildren();
    try {
      const result = await run(editor.value, controls, packages);
      if (result.stdout) output.append(element("pre", {}, result.stdout));
      if (result.stderr) output.append(element("pre", { class: "comp521-error" }, result.stderr));
      if (result.error) output.append(element("pre", { class: "comp521-error" }, result.error));
      result.figures.forEach((source) => output.append(element("img", { src: source, alt: "Figure generated by the interactive Python experiment" })));
      output.hidden = false;
      status.textContent = result.error ? "The experiment reported an error; inspect the traceback and change one thing." : "Done. Explain what changed before changing another input.";
    } finally {
      runButton.disabled = false;
    }
  });
}

export default { render };
