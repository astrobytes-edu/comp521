import { mountLecture } from "./runtime.mjs";
const STYLE_ID = "comp521-interactive-lecture-styles";
const STYLES = `.comp521-lecture-widget{margin:1rem 0;padding:1rem;border-left:4px solid #195c8f;background:#f7fbff;color:#172b3a}.comp521-lecture-widget button{margin:.25rem .5rem .25rem 0;padding:.45rem .7rem;border:1px solid #195c8f;border-radius:.3rem;background:#fff;color:#195c8f;font-weight:600}.comp521-lecture-widget textarea{box-sizing:border-box;width:100%;margin:.5rem 0;padding:.65rem;border:1px solid #91b4d8;border-radius:.3rem;font:inherit}.comp521-lecture-widget .reveal{margin-top:.6rem;padding:.7rem;background:#fff8e7;border-left:4px solid #bd7c00}.comp521-lecture-widget iframe,.comp521-lecture-widget video{display:block;width:100%;border:0;min-height:18rem}.comp521-lecture-widget video{min-height:0}.comp521-lecture-widget[data-kind="lecture-checkpoint"]{border-left-color:#714d9b}.comp521-lecture-widget[data-kind="lecture-panel"]{border-left-color:#007f7a}@media (prefers-reduced-motion:reduce){.comp521-lecture-widget *{scroll-behavior:auto!important;transition:none!important}}`;

function node(name, attributes = {}, text = "") {
  const item = document.createElement(name);
  Object.entries(attributes).forEach(([key, value]) => item.setAttribute(key, value));
  item.textContent = text;
  return item;
}

function ensureStyles(el) {
  const root = el.getRootNode();
  if (root.querySelector?.(`#${STYLE_ID}`)) return;
  const style = node("style", { id: STYLE_ID });
  style.textContent = STYLES;
  root.append(style);
}

function storageKey(pageSlug, promptId) { return `comp521:lecture:${pageSlug}:${promptId}`; }

function draftWidget(model, checkpoint = false) {
  const options = model.get("options") || {};
  const key = storageKey(model.get("pageSlug"), model.get("id"));
  const prompt = options.prompt || "Write your reasoning.";
  const wrap = node("div", {}, prompt);
  const textarea = node("textarea", { rows: String(options.rows || 4), "aria-label": prompt });
  textarea.value = localStorage.getItem(key) || "";
  textarea.addEventListener("input", () => localStorage.setItem(key, textarea.value));
  const copy = node("button", { type: "button" }, "Copy");
  copy.addEventListener("click", async () => navigator.clipboard?.writeText(textarea.value));
  const download = node("button", { type: "button" }, checkpoint ? "Download notes" : "Download draft");
  download.addEventListener("click", () => {
    const text = `${prompt}\n\n${textarea.value}\n`;
    const url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" }));
    const link = node("a", { href: url, download: `${model.get("id")}.txt` });
    link.click(); URL.revokeObjectURL(url);
  });
  const clear = node("button", { type: "button" }, "Clear");
  clear.addEventListener("click", () => { if (confirm("Clear this private draft?")) { textarea.value = ""; localStorage.removeItem(key); } });
  wrap.append(textarea, copy, download, clear);
  return wrap;
}

function render({ model, el }) {
  return mountLecture(model, el);
  ensureStyles(el);
  const kind = model.get("kind");
  const options = model.get("options") || {};
  const wrap = node("section", { class: "comp521-lecture-widget", "data-kind": kind, "aria-label": options.label || kind });
  if (kind === "lecture-write") wrap.append(draftWidget(model));
  else if (kind === "lecture-checkpoint") wrap.append(draftWidget(model, true));
  else if (kind === "lecture-reveal") {
    const button = node("button", { type: "button", "aria-expanded": "false" }, "Reveal reasoning");
    const answer = node("div", { class: "reveal", hidden: "" }, model.get("body") || "");
    button.addEventListener("click", () => { const open = answer.hidden; answer.hidden = !open; button.setAttribute("aria-expanded", String(open)); button.textContent = open ? "Hide reasoning" : "Reveal reasoning"; });
    wrap.append(button, answer);
  } else if (kind === "lecture-panel") {
    const frame = node("iframe", { loading: "lazy", title: options.label || "Interactive lecture model" });
    const code = model.get("body") || "";
    if (code) {
      const python = `${code}\n\napp.servable(target='app');`;
      frame.srcdoc = `<!doctype html><html><head><meta charset="utf-8"><script src="https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js"><\/script><script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.9.2.min.js"><\/script><script src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.9.2.min.js"><\/script><script src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.9.2.min.js"><\/script><script src="https://cdn.jsdelivr.net/npm/@holoviz/panel@1.9.4/dist/panel.min.js"><\/script></head><body><p id="status">Loading interactive model…</p><div id="app"></div><script>async function main(){try{const p=await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/'});await p.loadPackage('micropip');await p.runPythonAsync(${JSON.stringify("import micropip\nawait micropip.install(['https://cdn.holoviz.org/panel/1.9.4/dist/wheels/bokeh-3.9.2-py3-none-any.whl','https://cdn.holoviz.org/panel/1.9.4/dist/wheels/panel-1.9.4-py3-none-any.whl'])")});await p.runPythonAsync(${JSON.stringify(python)});document.getElementById('status').remove()}catch(e){document.getElementById('status').textContent='Model unavailable: '+e}}main()<\/script></body></html>`;
    } else frame.src = `/${options.src || ""}`;
    frame.addEventListener("load", () => {
      // Panel scenes are authored as ordinary MyST pages for standalone use.
      // In a lecture, retain only their Panel widget rather than nesting a
      // second copy of the site navigation and page chrome.
      const document = frame.contentDocument;
      const article = document?.querySelector("article");
      const panelFrame = document?.querySelector('iframe[title="Interactive Panel dashboard"]');
      if (!article || !panelFrame) return;
      let keep = panelFrame;
      while (keep.parentElement && keep.parentElement !== article) keep = keep.parentElement;
      [...article.children].forEach((child) => { child.style.display = child === keep ? "block" : "none"; });
      article.style.maxWidth = "none";
      article.style.margin = "0";
      article.style.padding = "0";
    });
    wrap.append(frame);
  } else if (kind === "lecture-media") {
    const video = node("video", { controls: "", preload: "metadata", poster: options.poster || "" });
    video.append(node("source", { src: options.mp4 || "", type: "video/mp4" }), node("source", { src: options.webm || "", type: "video/webm" }), node("track", { kind: "captions", src: options.captions || "", srclang: "en", default: "" }));
    wrap.append(video, node("a", { href: options.transcript || "" }, "Read transcript"));
    if (options.youtube_id) wrap.append(node("a", { href: `https://www.youtube.com/watch?v=${encodeURIComponent(options.youtube_id)}` }, "Watch on YouTube"));
  } else if (kind === "interactive-lecture") {
    wrap.append(node("strong", {}, `${options.title || "Interactive lecture"} · ${options.duration || ""}`));
  }
  el.replaceChildren(wrap);
}

export default { render };
