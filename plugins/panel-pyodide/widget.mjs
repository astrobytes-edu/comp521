const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js";
const BOKEH_VERSION = "3.9.2";
const PANEL_VERSION = "1.9.4";

function escapeScript(text) {
  return text.replace(/<\/script/gi, "<\\/script");
}

function documentFor({ code, id }) {
  const python = `${code}\n\napp.servable(target=${JSON.stringify(id)});`;
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{margin:0;padding:.25rem;font:16px system-ui,sans-serif;color:#172b3a}#status{padding:.75rem;background:#f7fbff;border:1px solid #91b4d8;border-radius:.35rem}#status.error{color:#8b1c1c;background:#fff5f5;border-color:#d8a2a2}</style>
<script src="${PYODIDE_URL}"><\/script>
<script src="https://cdn.bokeh.org/bokeh/release/bokeh-${BOKEH_VERSION}.min.js"><\/script>
<script src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-${BOKEH_VERSION}.min.js"><\/script>
<script src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-${BOKEH_VERSION}.min.js"><\/script>
<script src="https://cdn.jsdelivr.net/npm/@holoviz/panel@${PANEL_VERSION}/dist/panel.min.js"><\/script>
</head><body><div id="status" role="status">Loading the browser-local dashboard…</div><div id="${id}"></div>
<script>
async function main() {
  const status = document.getElementById("status");
  try {
    const pyodide = await loadPyodide({indexURL: "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/"});
    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync(${JSON.stringify(`
import micropip
await micropip.install([
  "https://cdn.holoviz.org/panel/${PANEL_VERSION}/dist/wheels/bokeh-${BOKEH_VERSION}-py3-none-any.whl",
  "https://cdn.holoviz.org/panel/${PANEL_VERSION}/dist/wheels/panel-${PANEL_VERSION}-py3-none-any.whl",
])
`) });
    await pyodide.runPythonAsync(${JSON.stringify(python)});
    status.remove();
  } catch (error) {
    status.className = "error";
    status.textContent = "Dashboard could not start: " + error;
  }
}
main();
<\/script></body></html>`;
}

function render({ model, el }) {
  const frame = document.createElement("iframe");
  frame.title = "Interactive Panel dashboard";
  frame.loading = "lazy";
  frame.style.cssText = `display:block;width:100%;height:${model.get("height") || 560}px;border:1px solid #91b4d8;border-radius:.6rem;background:#fff;`;
  frame.setAttribute("sandbox", "allow-scripts allow-same-origin");
  frame.srcdoc = documentFor({ code: escapeScript(model.get("code") || ""), id: model.get("id") || "panel-dashboard" });
  el.replaceChildren(frame);
}

export default { render };
