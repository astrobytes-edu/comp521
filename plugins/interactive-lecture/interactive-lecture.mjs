import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const PLUGIN_PATH = new URL(import.meta.url).pathname;
const WIDGET_PATH = PLUGIN_PATH.replace(/\/[^/]*$/, "/widget.mjs");

function relativePath(fromDir, toFile) {
  const from = fromDir.split("/").filter(Boolean);
  const to = toFile.split("/").filter(Boolean);
  let shared = 0;
  while (shared < from.length && from[shared] === to[shared]) shared += 1;
  return [...Array(from.length - shared).fill(".."), ...to.slice(shared)].join("/") || ".";
}

function widget(data, vfile, kind) {
  const fromDir = vfile.path.replace(/\/[^/]*$/, "");
  return {
    type: "anywidget",
    esm: relativePath(fromDir, WIDGET_PATH),
    model: {
      kind,
      id: data.options?.id || "lecture",
      pageSlug: vfile.path.replace(/\.md$/, ""),
      options: data.options || {},
      body: (data.body || "").trim(),
    },
  };
}

function staticContent(ctx, kind, heading, body, id) {
  const safeId = String(id || kind).replace(/[^a-z0-9_-]/gi, "-");
  return ctx.parseMyst(`:::{div}\n:class: comp521-lecture-static comp521-lecture-static--${kind} lecture-id-${safeId}\n\n### ${heading}\n\n${body}\n:::`).children;
}

function lectureDirective(name, staticBody) {
  return {
    name,
    body: { type: String, required: false },
    options: {
      id: { type: String }, label: { type: String }, title: { type: String },
      mode: { type: String }, duration: { type: String }, time: { type: String },
      prompt: { type: String }, rows: { type: Number }, reveal: { type: String }, options: { type: String },
      model: { type: String }, starter: { type: String }, source: { type: String }, scene: { type: String },
      ask: { type: String }, wait: { type: String }, misconception: { type: String }, transition: { type: String },
      src: { type: String }, "code-file": { type: String }, fallback: { type: String }, mp4: { type: String },
      webm: { type: String }, poster: { type: String }, captions: { type: String },
      transcript: { type: String }, youtube_id: { type: String },
    },
    run(data, vfile, ctx) {
      if (name === "lecture-panel" && data.options?.["code-file"]) {
        data.body = readFileSync(resolve(dirname(vfile.path), data.options["code-file"]), "utf8");
      }
      const body = staticBody(data);
      const fallbackHeading = {
        "interactive-lecture": "Interactive lecture",
        "lecture-scene": "Lecture scene",
        "lecture-predict": "Make a prediction",
        "lecture-figure": "Interactive figure",
        "lecture-write": "Write your reasoning",
        "lecture-reveal": "Reasoning",
        "lecture-code": "Browser Python experiment",
        "lecture-sandbox": "Optional exploration",
        "lecture-panel": "Interactive model",
        "lecture-checkpoint": "Evidence checkpoint",
        "lecture-media": "Media",
        "presenter-note": "Presenter note",
      }[name];
      return [...staticContent(ctx, name, data.options?.label || data.options?.title || fallbackHeading, body, data.options?.id), widget(data, vfile, name)];
    },
  };
}

const directives = [
  lectureDirective("interactive-lecture", (data) => data.body || "Interactive lecture controls load below this introduction."),
  lectureDirective("lecture-scene", (data) => data.body || "Continue to the next lecture scene."),
  lectureDirective("lecture-predict", (data) => `**Prediction prompt:** ${data.options?.prompt || "Make a prediction."}`),
  lectureDirective("lecture-figure", (data) => data.options?.fallback || "Interactive figure unavailable."),
  lectureDirective("lecture-write", (data) => `**Prediction prompt:** ${data.options?.prompt || "Write your prediction."}`),
  lectureDirective("lecture-reveal", (data) => data.body || "Instructor reasoning is unavailable."),
  lectureDirective("lecture-code", (data) => data.options?.fallback || "Code activity unavailable."),
  lectureDirective("lecture-sandbox", (data) => data.options?.fallback || "Exploration unavailable."),
  lectureDirective("lecture-panel", (data) => data.options?.fallback || "Interactive model unavailable."),
  lectureDirective("lecture-checkpoint", (data) => `**Checkpoint:** ${data.options?.prompt || "Summarize your evidence."}`),
  lectureDirective("lecture-media", (data) => data.options?.fallback || "Media description unavailable."),
  lectureDirective("presenter-note", (data) => data.options?.ask || "Presenter guidance."),
];

export default { name: "COMP 521 interactive lectures", directives };
