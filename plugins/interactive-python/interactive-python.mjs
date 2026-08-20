const PLUGIN_PATH = new URL(import.meta.url).pathname;
const WIDGET_PATH = PLUGIN_PATH.replace(/\/[^/]*$/, "/widget.mjs");

function relativePath(fromDir, toFile) {
  const from = fromDir.split("/").filter(Boolean);
  const to = toFile.split("/").filter(Boolean);
  let shared = 0;
  while (shared < from.length && from[shared] === to[shared]) shared += 1;
  return [...Array(from.length - shared).fill(".."), ...to.slice(shared)].join("/") || ".";
}

function parseControls(value) {
  if (!value) return {};
  try {
    const parsed = JSON.parse(value);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    throw new Error("interactive-python controls must be a JSON object");
  }
}

const interactivePython = {
  name: "interactive-python",
  alias: ["pyodide-experiment"],
  doc: "Render an editable browser-local Python experiment backed by Pyodide.",
  body: { type: String, required: true },
  options: {
    id: { type: String, doc: "Stable identifier for the experiment." },
    packages: { type: String, doc: "Comma-separated Pyodide packages." },
    controls: { type: String, doc: "JSON object describing numeric controls." },
  },
  run(data, vfile) {
    const code = (data.body || "").trim();
    if (!code) return [];
    const fromDir = vfile.path.replace(/\/[^/]*$/, "");
    const packages = (data.options?.packages || "").split(",").map((item) => item.trim()).filter(Boolean);
    return [{
      type: "anywidget",
      esm: relativePath(fromDir, WIDGET_PATH),
      model: {
        code,
        controls: parseControls(data.options?.controls),
        packages,
        id: data.options?.id?.trim() || `experiment-${Math.random().toString(36).slice(2)}`,
      },
      id: data.options?.id?.trim() || Math.random().toString(36).slice(2),
    }];
  },
};

export default { name: "COMP 521 interactive Python", directives: [interactivePython] };
