# COMP 521 interactive lectures design

## Decision

COMP 521 will add **MyST-native interactive lecture pages** for live,
instructor-led teaching. They keep the existing Book Theme and normal MyST
navigation; interaction is introduced through small, reusable directives, not
through a replacement theme or a separate slide application.

The first pilot refactors the Transit Depth Lab into an interactive lecture
that first explains what a transit is, then asks students to predict,
manipulate, and explain the uniform-disk depth model.

## Teaching model

Each scene follows one bounded cognitive move:

```text
setup → private prediction → instructor reveal → manipulate evidence → explain → checkpoint
```

The projected instructor page supplies pacing. Student copies remain usable for
review, but v1 has no cross-device reveal synchronization, analytics, or graded
submission service.

## Authoring interface

Lecture pages use the following MyST directives:

| Directive | Required fields | Behavior |
|---|---|---|
| `interactive-lecture` | `title`, `mode: live`, `duration` | Page-level metadata and presentation controls. |
| `lecture-scene` | `id`, `label`, `time` | Semantic paced section with an optional “what to notice” callout. |
| `lecture-write` | stable `id`, `prompt`, `rows` | Keyboard-accessible private textarea, browser-local autosave, Copy, Download, and Clear. |
| `lecture-reveal` | stable `id` | Native-button, `aria-expanded` expert reasoning. |
| `lecture-panel` | `src`, `fallback` | Lazy Panel/Pyodide scene plus visible non-JavaScript explanation. |
| `lecture-checkpoint` | stable `id`, `prompt` | Synthesis prompt whose draft participates in the page export. |
| `lecture-media` | `mp4`, `webm`, `poster`, `captions`, `transcript` | Local-first, non-autoplay video. Optional `youtube_id` provides a link, not an eager iframe. |

`lecture-write` and `lecture-checkpoint` use this storage key:

```text
comp521:lecture:<page-slug>:<prompt-id>
```

Student writing never leaves the browser. “Download notes” creates a UTF-8 text
file containing the page title, prompts, drafts, and timestamp.

## Runtime and package boundary

The normal static MyST page is authoritative and renders before any enhancement.

- Existing MyST Book Theme remains the site shell.
- Panel 1.9.x, Bokeh 3.9.x, and Pyodide 0.29.3 are the only rich-runtime
  dependencies in v1.
- The existing `panel-pyodide` directive remains the sole mechanism that starts
  a Panel/Pyodide iframe.
- Do not add HoloViews, hvPlot, Plotly, ipywidgets, 3-D/WebGL, chat,
  authentication, analytics, or collaboration in v1.
- A Panel scene must lazy-load and must not prevent its explanatory fallback
  from rendering.

## Visual system

The lecture layer uses course-owned CSS with restrained semantic accents:

- prediction: blue;
- evidence/manipulation: teal;
- assumption/limit: amber;
- synthesis/checkpoint: violet.

It keeps the ordinary reading width by default. Presentation mode is a
page-local focus view with Previous/Next scene buttons and Left/Right arrow
shortcuts outside editable controls. It must not trap focus or remove normal
site navigation from the document order.

## Media contract

Media is optional and supports a scientific purpose, not decoration. Short
Manim micro-animations (normally 10–45 seconds) are appropriate for motion,
transformation, or iterative processes. Each essential video has local MP4 and
WebM variants, poster, WebVTT captions, transcript, visible source/credit, and
a static alternative. Autoplay is prohibited. YouTube may receive a mirrored
copy; the course-local asset remains canonical and the page offers a deliberate
“Watch on YouTube” link instead of an eager third-party embed.

## Accessibility and failure contract

- Static prose, figures, equations, and every prompt render with JavaScript
  disabled.
- Native controls have accessible names and visible focus.
- Reveals use `<button>` semantics and `aria-expanded`.
- Video uses native controls, captions, transcript, poster, and no autoplay.
- Reduced-motion preference disables scene transition motion.
- A Panel failure shows a concise message and leaves the fallback visible.
- Mobile layouts stack controls and never require hover.

## Validation and publication gate

Create a source validator that rejects duplicate/missing stable prompt IDs,
reveals without IDs, local media without captions/transcript/poster, lecture
Panel blocks without fallback, and unknown lecture directives. Continue to run
the existing math validator.

An interactive lecture is publishable only when the following pass:

1. `python3 scripts/check_math_rendering.py`;
2. `python3 scripts/check_interactive_lectures.py`;
3. `myst build --html --execute`;
4. desktop and narrow-mobile browser smoke checks;
5. keyboard-only and reduced-motion checks; and
6. a JavaScript-disabled inspection that verifies the static learning path.

## Transit Depth pilot

The pilot is the existing `03-python/interactive-lab-transit-depth.md`. It
must begin with an accessible stellar-disk/planet-occultation diagram and a
plain explanation: a transit occurs when a planet passes in front of its star,
blocking a fraction of the observed light. The pilot then asks students to
predict the depth effect of doubling the radius ratio, uses the existing Panel
geometry dashboard as evidence, reveals the area-ratio reasoning, and ends
with an exportable synthesis draft naming a model limitation.
