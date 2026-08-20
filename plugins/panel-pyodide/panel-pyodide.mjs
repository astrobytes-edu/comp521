const PLUGIN_PATH = new URL(import.meta.url).pathname;
const WIDGET_PATH = PLUGIN_PATH.replace(/\/[^/]*$/, "/widget.mjs");

function relativePath(fromDir, toFile) {
  const from = fromDir.split("/").filter(Boolean);
  const to = toFile.split("/").filter(Boolean);
  let shared = 0;
  while (shared < from.length && from[shared] === to[shared]) shared += 1;
  return [...Array(from.length - shared).fill(".."), ...to.slice(shared)].join("/") || ".";
}

const panelPyodide = {
  name: "panel-pyodide",
  alias: ["panel-dashboard"],
  doc: "Render a browser-only Panel dashboard through Pyodide/WASM.",
  body: { type: String, required: true },
  options: {
    id: { type: String, doc: "Stable dashboard identifier." },
    height: { type: String, doc: "Dashboard height in CSS pixels." },
  },
  run(data, vfile) {
    const code = (data.body || "").trim();
    if (!code) return [];
    const fromDir = vfile.path.replace(/\/[^/]*$/, "");
    return [{
      type: "anywidget",
      esm: relativePath(fromDir, WIDGET_PATH),
      model: {
        code,
        id: data.options?.id?.trim() || `panel-${Math.random().toString(36).slice(2)}`,
        height: Number(data.options?.height) || 560,
      },
      id: data.options?.id?.trim() || Math.random().toString(36).slice(2),
    }];
  },
};

export default { name: "COMP 521 Panel + Pyodide", directives: [panelPyodide] };
