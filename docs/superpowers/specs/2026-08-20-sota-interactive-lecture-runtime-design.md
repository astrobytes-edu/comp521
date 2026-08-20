# SOTA interactive lecture runtime design

## Status and decision

**Status:** approved for planning; implementation has not started.

COMP 521 will replace the current collection of lecture wrapper widgets with a course-owned, MyST-native interactive lecture runtime. A single MyST page will serve two deliberate experiences:

1. **Student mode:** an accessible narrative reading and activity page.
2. **Presenter mode:** a projector-first sequence of focused lecture scenes.

Both modes share one source of truth, stable scene anchors, the same physics, and the same learning activities. Students advance independently in v1. There are no accounts, cross-device synchronization, analytics, graded submission, or network-service dependencies.

## Teaching contract

Every core activity follows this sequence:

```text
commit a prediction → change one meaningful variable → observe linked evidence
→ explain or revise the claim → optionally inspect/edit a Python model
```

The runtime must make the task visible before it exposes controls. It must not show a solution before a student chooses to reveal it. It must distinguish a brief conceptual interaction from an open-ended computational sandbox.

| Activity | Purpose | Required experience |
|---|---|---|
| `prediction` | Elicit a claim before evidence | Quick choice, optional private reasoning, no automatic grade |
| `figure` | Link a model parameter to an observable | One initial control; geometry, graph, value, and interpretation update together |
| `reveal` | Explain evidence and correct model | Unavailable until student action; retains formatted MyST mathematics |
| `code` | Practice computational reasoning | Editable short starter code, run/reset, static result and explanation fallback |
| `compare` | Surface assumptions and limits | Clear comparison of what changes and what does not |
| `checkpoint` | Consolidate learning | Short private response included in page-wide export |
| `sandbox` | Support deeper exploration | Separately labeled Panel activity, never the core projected scene |

## Authoring interface

The local `interactive-lecture` MyST plugin owns semantic directives:

| Directive | Required metadata | Static behavior | Enhanced behavior |
|---|---|---|---|
| `interactive-lecture` | title, duration | Normal page introduction | Enables presenter controls and scene index |
| `lecture-scene` | stable id, label, duration | Numbered section with anchor | Addressable scene and presentation stage |
| `lecture-predict` | stable id, prompt, options | Prompt plus static reasoning context | Private choice/reasoning and commit state |
| `lecture-figure` | stable id, model | Explanatory figure and caption | Native direct-manipulation figure |
| `lecture-reveal` | stable id | Hidden/details-style explanation | Controlled reveal preserving rendered MathJax |
| `lecture-code` | stable id, starter, fallback | Starter listing and worked interpretation | xeus-python JupyterLite execution, reset, output |
| `lecture-checkpoint` | stable id, prompt | Reflection prompt | Private browser-local draft and page-wide export |
| `lecture-sandbox` | stable id, source, fallback | Clear exploration invitation | Lazy Panel/Pyodide dashboard |
| `presenter-note` | cue, time | Omitted from student reading | Instructor timing, question, misconception, transition |

Stable IDs create predictable anchors of the form `#scene-<id>` and data keys of the form `comp521:lecture:<page-slug>:<activity-id>`. Student writing never leaves the browser. A page-level export contains every saved response, prompt, scene identifier, and export timestamp.

## Mode behavior

### Student mode

- Normal MyST Book-theme page and navigation remain visible.
- Each scene shows its number, total, and a copy-link action.
- Students can advance independently, reveal when ready, and reset native or code activities to their starter state.
- Reading prose and static explanation remain the authoritative fallback.

### Presenter mode

- A URL toggle enables presentation without a distinct build or login.
- The current scene is a high-contrast, full-width stage with visible scene number/progress, previous/next controls, and keyboard navigation outside editable controls.
- Presenter notes show an ask cue, suggested wait time, likely misconception, and transition prompt. They are absent from student mode and exports.
- Presenter mode does not remove ordinary document navigation from the DOM or trap focus.

## Visual and interaction system

The physics is the visual center. Generic alert boxes, duplicate static/dynamic wrappers, nested course chrome, and foreign dashboard styling are prohibited.

- Presenter mode uses a dark, high-contrast stage; student mode uses a quiet, warm reading surface.
- Prediction uses a blue accent, direct evidence teal, assumptions/limits amber, and checkpoints violet.
- Interactions use browser-native SVG, HTML, CSS, and custom elements to share course typography, responsive behavior, and accessibility semantics.
- Animation is optional and respects reduced-motion preferences; the result is always represented by text, numeric value, geometry, or graph as applicable.

### Transit Depth pilot interaction

The core figure begins with the radius ratio

$$
p = \frac{R_p}{R_\star}.
$$

Students predict what happens to the blocked fraction when they increase \(p\), then use a labeled slider to make the planet larger. The stellar disk, planet geometry, normalized flux, and light-curve depth update as a single linked observable. A prediction marker remains visible. The reveal explains the stated uniform-disk approximation:

$$
\frac{F}{F_0} = 1 - p^2.
$$

It then asks students to revise their claim and move into a short Python experiment. Impact parameter and limb darkening are introduced only as deliberate later model upgrades, not simultaneous initial controls.

## Browser-Python environment

### Primary environment: JupyterLite with xeus-python

The standard runnable course environment is a course-built JupyterLite distribution using xeus-python and a version-pinned `environment.yml`. Students should open a code activity and find the validated scientific stack ready; activities must not ask them to install packages.

The initial candidate stack is Python, NumPy, Matplotlib, SciPy, pandas, and ipywidgets. A package enters the environment only after it has a compatible WebAssembly build, is required by an authored activity, and passes browser smoke tests. The final environment file records exact channels and versions.

### Panel boundary

Panel remains available for explicitly labeled advanced dashboards. Its browser-delivered runtime is a separate, lazy Pyodide/Panel sandbox because that is Panel's supported WebAssembly route. It is not used for the core lecture stage or ordinary code cells. The course must not promise Panel inside the xeus-python kernel unless a dedicated compatibility test proves that exact configuration.

### Runtime loading

- Do not download JupyterLite or Panel for pages without a relevant activity.
- A code activity lazily loads the course-built xeus JupyterLite asset bundle.
- A sandbox lazily loads its Pyodide/Panel bundle.
- Every runtime has a clear loading, retry, reset, and failure state while retaining a static worked result and next learning task.

## Accessibility, privacy, and reliability

- Native buttons, labels, focus order, and keyboard controls are required.
- The active presenter scene announces its heading without unexpectedly moving focus when a student is reading or editing.
- Every executable/interactive activity provides descriptive static content, rendered equations, and a no-JavaScript learning path.
- Stored drafts use browser-local storage only; export is explicit.
- The runtime reports an understandable error and preserves the fallback if browser execution, a CDN asset, or a local-state operation fails.
- Responsive layouts are validated at projected desktop, tablet, and narrow-phone widths.

## Validation gates

The implementation must add focused checks for:

1. directive schema, stable unique IDs, and stable scene anchors;
2. static output that has no duplicate question/reveal content;
3. presenter/student mode behavior, keyboard navigation, and copyable scene links;
4. private-note persistence, reset, and page-wide download;
5. transit model values, including the \(p^2\) uniform-disk relation;
6. xeus JupyterLite startup and imports for every declared package;
7. runtime failure fallback, reduced motion, and no-JavaScript behavior; and
8. desktop, projector, tablet, and narrow-phone visual smoke checks.

The publication gate requires these checks plus the existing mathematical-rendering check and a successful MyST site build.

## Non-goals and future extension

V1 does not include Reveal.js, a replacement MyST theme, real-time sync, accounts, submissions, analytics, automatic grading, arbitrary package installation, or a server-side kernel.

A future optional synchronization service may publish an instructor room's scene/reveal state to voluntarily joined student devices. It remains a separate service layer and must not change the static, independent-use contract above.
