# Authoring lectures and research talks

This is the shared authoring contract for Anna, Codex, and Claude. It documents
implemented behavior. A successful build is not a scientific review or permission
to publish. Follow the owning repository's approval and privacy rules.

## Project setup

Keep slides in the same MyST project as readings and notebooks. Register
`plugin.mjs` in `project.plugins`, and list the documents in the usual MyST TOC.
Put shared presentation settings and deck selections in `slides.json`:

```json
{
  "reveal": { "transition": "fade" },
  "sources": ["analysis.ipynb", "methods.md"],
  "decks": [
    { "name": "lecture", "source": "lecture.md", "preset": "lecture", "handoutMode": "exercises" },
    { "name": "seminar", "source": "seminar.md", "preset": "seminar", "handoutMode": "worked" }
  ]
}
```

Each source is relative to the project root. Deck names are lowercase slugs.
Each deck emits `name.html` and `name.handout.html`. Explicitly listed `sources`
become portable reading pages in `sources/`. Links between decks and those pages
work offline. References to other project pages need `siteUrl`, such as
`https://example.edu/course`, and take the reader to that site. Only explicitly
selected sources are exported; do not select private instructor documents.
Build with `node src/build.mjs PROJECT OUTPUT_DIRECTORY`. The multi-deck exporter
renders everything in a staging directory before replacing the review outputs.
The preview watcher uses the same build path. `decks.json` maps slides to source
files/lines for later automated review.

For the COMP 521 SWE publication pilot, use
`node src/build.mjs migrations/comp536 _build/production --deck software-engineering`.
This processes the named source and exports only that deck and its handout;
the project's other decks and standalone source pages are excluded. Use a
separate output directory: selected export refuses to mix with unrelated files.
Keep `decks.json` and `provenance.json` in the build workspace, and copy only the
two HTML files into the course site's `reveal/` directory. This selection is for
a standalone deck; references requiring other exported source pages must use
the full project export or an explicit course-site destination.

Native MyST references, footnotes, bibliographies, and notebook embeds work in
selected decks. Footnotes are repeated on each slide that refers to them. For
example, `![](#labelled-output)` embeds the resolved notebook output and a source
link. Cross-project federation to an unrelated MyST project is not yet covered.

## Compose a slide

A top-level `##` starts a slide. Set layout with a `slide-options` JSON block:

```json
{"layout":"figure", "eyebrow":"Results", "takeaway":"The conclusion supported by this figure."}
```

Layouts: `title`, `section`, `figure`, `compare`, `code`, `derivation`, `result`,
and `summary`. `compare` uses two `slide-panel` blocks. Panels accept a title
and an optional fragment index for staged panel reveals. Use `slide-columns`
for arbitrary ratios. Presets `lecture`, `seminar`, and `conference` share the
same design system, with increasing base text sizes. Choose content density to
fit the preset; changing a preset does not automatically make a crowded slide fit.

Use one claim or teaching action per slide. Keep code lines short enough to read
without horizontal scrolling. Split a long derivation at a conceptual boundary.
Prefer an explicit figure inset to shrinking an entire figure. Never turn a
failed layout check into a pass by silently reducing the global font size.

## Polished code and executed results

For a standalone snippet:

````md
```{slide-code} python
:title: squares.py
:steps: [{"lines":"1","explain":"Choose inputs."},{"lines":"2","explain":"Transform each input."},{"lines":"3","explain":"Inspect the output."}]
values = [0, 1, 2, 3]
squares = [x * x for x in values]
print(squares)
```
````

The code card provides editor-style syntax colors, a title, a copy icon with
a tooltip and success checkmark, line
highlighting, and synchronized explanations. `:lines: 1|2-3|4` is the simpler
highlight-only form. `:id:` matches code blocks for Reveal Auto-Animate.
Snippets are displayed source; they are not automatically executed.

For code and output from one executed notebook cell:

````md
```{slide-code-example} analysis.ipynb#quadratic-cell
:title: Generate the figure
:lines: 1-2|3-4|5-7
:alt: A parabola with labelled axes showing y equals x squared.
```
````

Label the cell in notebook metadata or use a native MyST labelled code cell.
The same source produces the displayed code and result. `view` can be `both`
(default, side by side), `code`, or `output`. `steps` works here too. A source
cell that failed cannot be used as a successful example. Do not replace a failed
calculation with handwritten output.

For editable browser execution, use `slide-python`. Syntax colors update as you
type, using the same light palette as static snippets. Standard-library Python is
the default. `:packages: numpy,matplotlib` explicitly downloads those packages;
provide `:alt:` for generated plots. `plt.show()` sends figures to the output
pane. Run starts fresh, Stop terminates the worker, and Reset restores the source.
Execution has a 15-second limit after loading; loading has a 60-second limit.
This component needs network access and may scroll internally for large output.
Precompute expensive simulations and embed their outputs instead.

## Scientific figures

````md
```{slide-figure} analysis.ipynb#sample-figure
:alt: A precise description of the plotted relationship and axes.
:caption: What the reader should notice, with the relevant limitation.
:focus: 60 10 25 40
[{"x":70,"y":30,"text":"Identify the feature here.","step":0}]
```
````

The source may be a local PNG/JPEG/SVG or one labelled notebook image output.
Coordinates are percentages of the full image, including margins. `focus` is
`x y width height`; it crops a magnified inset from the same image. Annotation
markers and their explanations reveal together. The enlargement control supports
keyboard navigation. PDF retains the figure, inset, and all annotations.
An inset does not increase the underlying data or image resolution.

For linked data inspection, `slide-linked-plot` references a notebook cell with
one `application/json` output containing:

```json
{
  "x": [0, 1, 2],
  "xLabel": "Time (specified units)",
  "panels": [
    { "label": "Measured quantity", "values": [1, 2, 1], "lower": [0.8, 1.8, 0.8], "upper": [1.2, 2.2, 1.2] },
    { "label": "Second quantity", "values": [2, 4, 2] }
  ]
}
```

Use `slide-linked-plot` with the source reference as its argument and a `title`
option. One to three panels share a sample cursor; lower/upper bands are optional.
Arrays must be finite, equally sized, and have strictly increasing x values.
State what a band means; the component does not infer confidence levels or a
statistical model. Reset restores the first sample. PDF and handout show the
initial state as a static SVG. General Plotly/Altair/3D widget support is separate.

For a custom interactive HTML component, `slide-embed` accepts `fallback` (a local
image) and `alt`. PDF substitutes that image. Without a fallback it prints a
labelled notice. The fallback must convey the intended lesson, not merely show
an empty widget frame.

## Teaching sequence and handouts

- `slide-question`: prediction or concept-check prompt, with optional `title`.
- `slide-answer`: staged answer/explanation, with optional `title` and `index`.
- `slide-worked`: a worked example, containing `slide-step` blocks.
- `slide-step`: a staged derivation or explanation, with optional title/index.
- `slide-timer`: duration in seconds as its argument and an optional title.
  Start/Pause/Reset control it; leaving the slide pauses it. It does not advance
  slides automatically.

Keep answers inside `slide-answer` if an exercises-only handout should omit them.
That handout removes those blocks from the output bytes. The presentation still
contains its revealable answers. This is not a mechanism for private solutions.
Speaker notes are public in a downloadable deck. Keep private instructor material
outside the public project and select public sources deliberately.

A worked handout shows every answer and derivation step. Both handout profiles
show code-step explanations together and omit speaker notes. The deck's PDF
contains the full slide explanations; it does not inherit the handout's answer
exclusion. Export the exercises handout separately when that is the intended PDF.

## Verification for human and agent authors

1. Build using the project's actual Python kernel and pinned package dependencies.
2. Inspect `decks.json` for source selection, slide IDs, source lines, and outputs.
3. Run the relevant browser tests and inspect projector-sized screenshots. Check
   code inside its container and figure labels, not just outer slide bounds.
4. Test the prediction stage before advancing; verify that it does not show the
   answer. Inspect handout output bytes when answers are meant to be excluded.
5. Exercise every interactive component, including error/reset paths. Use
   `RUN_ONLINE_TESTS=1 npm test` when browser Python is part of the deck.
6. Print and visually inspect figures, code, annotations, and staged material.
   A successful PDF write is not evidence that the content survived correctly.
7. Report source/build/test/visual evidence separately from scientific review and
   publication status. Never infer that a tool-generated scientific claim is true.

The example regression command is `npm run build:all` followed by
`RUN_ONLINE_TESTS=1 npm test`, with the course Python environment on PATH.
The review CLI below supplies structured findings and evidence for this repair
loop. Its bounded checks supplement scientific and visual review.

## Columns and bounded sizing

`slide-columns` accepts two to four `slide-column` children. `ratio: 2 1 1`
sets their relative widths; `gap: 24` is in logical slide pixels; `align` is
`start`, `center`, `end`, or `stretch`. Ratios must match the number of columns.
Reading handouts stack columns in source order.

Reveal scales the whole slide to the viewport. Ordinary Markdown images are constrained to the slide width and figure-height budget while retaining their aspect ratio.
`layout: figure-wide` prioritizes a figure with a compact heading. A figure that
exceeds the available height is reduced within a bounded range. An authored
`focus` inset now marks its region on the original image.

For text, use `{"fit":"bounded","min-font":28}` in `slide-options` or set
`fit` and `minFont` in a deck configuration. The fitter reduces the slide's base
font by whole pixels only when needed, stopping at the specified floor (24–36
logical pixels; default 26). It never crops content or treats unresolved overflow
as success. Code-to-figure source, plot labels, and supporting labels have an 18-pixel floor. Other relative captions/code still require the checker and visual
review. `?review` shows an overflow notice. Prefer splitting a crowded slide to
using smaller text. The runtime reports its measurements in `slideFitReports`.

## Themes and live-code ergonomics

Set `theme: "dark"` on a deck or variant for the astronomy theme. Text, code,
controls, linked SVG plots, and live editors share a coordinated palette. Raster
figures retain their authored colors; they are never inverted. Prepare an actual
dark figure when it is appropriate for the data. Handouts use a light reading
canvas. The audience toolbar starts collapsed under **Tools** and remains
keyboard-accessible.

The live editor has line numbers, indentation, Ctrl/Command+Enter execution, and
a code/result divider. Drag the divider or focus it and press left/right arrows.
Tab indents; Escape then Tab moves focus out of the editor. Reset restores source,
parameter values, output, and trace state. This is a focused teaching editor, not
an IDE with autocomplete, semantic diagnostics, or a debugger.

Add a JSON `parameters` option to `slide-python`, for example:

```json
[{"name":"amplitude","label":"Amplitude","min":0.1,"max":2,"step":0.1,"value":1}]
```

The selected values are variables in the executed source's namespace. Moving a
slider does not execute code automatically. Use `fallback: analysis.ipynb#cell`
for a precomputed figure, with descriptive `alt`. The fallback is labelled as
precomputed and never presented as the result of a changed input. PDF uses the
fallback; HTML offers it even if runtime loading fails.

With `trace: true`, Run records actual Python `line` and `return` events for the
displayed source, then Previous/Next inspect snapshots. A line event precedes its
execution. Limits: 300 events, 20 primitive list/tuple elements, 120 characters
per scalar representation, and the existing execution timeout. Complex objects,
including arrays, show their type. It is replay after execution, not pausing a
live interpreter at breakpoints. Use tiny deterministic teaching examples.

## Scientific comparisons

`slide-image-compare` takes a JSON body with `title` and two `images`, each with
`source`, `label`, and `alt`. It starts side by side. The slider blends the second
image over the first; the author must establish compatible coordinate systems,
registration, aspect ratios, and color scales. PDF and handout retain both images.

`slide-movies` takes a JSON body with `title` and two or three `movies`, each with
local `source`, `poster`, and `label`. Shared Play/Pause/Reset and a time slider
synchronize elapsed video time over the shortest duration. Leaving the slide
pauses playback. This is browser synchronization, not frame-exact scientific
alignment; encode physical time consistently. PDF and handouts retain labelled
posters. Supply a `caption` stating the intended comparison and limitations.

Linked-plot JSON supports `xScale: "log"` and per-panel `scale: "log"`; all
corresponding values and interval endpoints must be positive. Linear is the
explicit default. Any lower/upper band requires `bandLabel` explaining its
meaning, such as a stated credible interval or an illustrative range. The
component does not estimate uncertainty or infer physical units.

## Talk variants and rehearsal

A deck can declare `variants`, for example:

```json
{"name":"talk","source":"talk.md","variants":[
  {"name":"short","includeTags":["core"],"preset":"conference"},
  {"name":"seminar","includeTags":["core","detail"],"theme":"dark"}
]}
```

Use `tags: ["core"]` or `["detail"]` in slide options. Untagged slides are shared.
Variant filenames append the variant name. Slide IDs remain stable. Do not leave
references to slides excluded from a variant; local unresolved destinations fail
export or review. Cross-deck routes point to the full target deck.

Slide options also support positive `timing` in seconds, `backup: true`, `cue`
(public speaker notes), `evidence` (an absolute URL), and `limit` (visible claim
qualification). **Tools → Backups** saves the current slide/fragment state and
**Return to talk** restores it. Backup slides remain reachable in normal navigation;
place them after the conclusion. A variant can omit them via tags.

**Tools → Rehearse** starts, pauses, resets, and downloads timings as JSON. Records
include repeat visits to slides. Nothing is sent to a service. Reset clears the
current session; downloading provides persistence. The panel is for rehearsal,
so close it before audience delivery. Scientific claims and source selection
still require Anna's approved brief.

## Agent review command

After building:

```sh
npm run check -- _build/html/reveal/decks.json --out _build/review
# Limit the first repair cycle to one deck:
npm run check -- _build/html/reveal/decks.json --deck advanced --out _build/review-advanced
# Compare against an earlier reviewed report without overwriting it:
npm run check -- _build/html/reveal/decks.json --baseline /path/to/approved/report.json
```

`report.json` links source paths, lines, slide IDs, components, observed values,
repair suggestions, and screenshot evidence. `index.html` is the contact sheet;
PDFs sit beside it. Errors produce a nonzero exit code. Warnings remain visible.
The checker visits initial and up to 40 fragment states per slide, tests geometry,
small text, images, local links, control names, programmatic focus, runtime errors,
and load-time network requests. Baseline comparison detects changed element
geometry, not pixel-perfect visual equivalence.

The checker does **not** certify scientific content, image-label legibility,
contrast against arbitrary imagery, full screen-reader behavior, tab order,
interactive state coverage, or every execution/network path. Those need visual
review and the component browser tests. Both agents should read the JSON, inspect
the relevant screenshots/PDFs, repair the source, and rerun the affected checks.
Never suppress a finding solely to obtain a green summary.

## Execution records and offline Python

Multi-deck export writes `provenance.json`: source hashes, pinned Node dependency
versions and lock hash, Node version, notebook kernelspecs, and observed Python
package versions when discoverable. This records the environment at export;
previously cached MyST results do not thereby gain historical provenance. For a
fresh calculation, clear only the relevant execution cache with approval and
rebuild, then retain the environment record with the result.

The optional local runtime package is about 25 MB for the current dependency set:

```sh
npm run bundle:python
npm run preview
```

The bundle command downloads pinned Pyodide 0.29.3 plus NumPy/Matplotlib dependencies,
verifies package hashes from its lock, and records hashes for all downloaded files.
Set `pythonRuntime` to the directory's absolute URL, such as
`http://127.0.0.1:4173/comp521/python/`, and rebuild the deck. Serve it with the
included preview server (correct MIME types and CORS for sandboxed frames).
This supports a disconnected laptop with a running local server; it is not
single-file offline Python. On another host, change that URL and serve the bundle
with equivalent MIME/CORS settings. The normal deck remains self-contained apart
from explicitly selected live computation.

Interactive slides cap Reveal's enlargement at native scale to avoid misrouted
pointer events in Chromium sandboxed iframes; they still scale down on smaller
screens. Other slides retain the configured Reveal scaling. Multi-cell notebook
slides are supported, and manifests/review findings include one-based `cellIndex`
where line numbers are local to a notebook Markdown cell.

### Viewer theme toggle

Tools → Dark mode switches between light and dark without resetting code edits,
results, parameters, or navigation. The preference is saved per deck URL when
browser storage is available; otherwise it lasts for the open page. The configured
`theme` remains the default. Python editors follow the toggle. Raster figures and
third-party embeds retain their original colors. Print/PDF uses the configured
theme; reading handouts remain light.

### Compact presentation tools

Tools starts collapsed as a sliders icon. Its popover uses original inline stroke
icons with accessible names and hover/focus tooltips; no icon library download is
required. Tab visits actions, Enter/Space activates buttons, and Escape closes the
popover and restores focus. Outside clicks, focus leaving the toolbar, and action
selection also close it. Active pointer/theme states retain a visible outline.

## Linked explanations, saved steps, and audience paths

`slide-explanation` connects author-specified equation terms, one-based code lines,
and normalized figure rectangles. Each JSON term contains `label`, `math`, `lines`,
`region: [left, top, width, height]`, and `explain`. The component requires `title`,
`source`, `alt`, and `code`; see `examples/courses/exploration.md`. Selection highlights
existing evidence. It does not infer a scientific relationship or execute that code.
The separate Python experiment provides actual computation. Optional `equation`
(LaTeX) and `prompt` (plain text) add a full equation above the aligned Python/result
columns and a prediction question below the code.

`slide-replay` adds contextual Save step, Replay from start, Next saved step,
Return to exploration, and Clear controls. Up to 20 states live in memory for this
open page. Supported state includes Reveal navigation/fragments, native input
values, linked terms, evidence expansion, media times (restored paused), and our
Python editor's code, parameters, output images/text and trace position. Python
results are restored with an explicit “not rerun” label. Running Python prevents
capture/restore. Reloading clears saved states. Arbitrary iframe/widget state,
Python heap/process state, ink annotations and external services are not captured.
No browser recording is silently promoted into a reproducible scientific result.

`slide-paths` takes `{"paths":[{"label":"Derivation","audience":"Mathematical",
"target":"slide-why-this-shape"}]}`. Targets must exist in the exported deck;
filtered-out variant targets fail export. The audience selector filters the visible
choices, not the slide content. A detour saves supported state and pushes a return
point, up to 12 levels. Include `slide-paths` on detail slides to expose Return.
Return is LIFO; it restores the state from before entering that branch.

Use `{"vertical":true}` in `slide-options` immediately after a main slide to create
native Reveal vertical detail slides. Right/left traverses main columns; down/up
visits detail rows. Reveal has two native dimensions, not arbitrary section nesting.
Deeper explanation trees use explicit detours with return points. The new example
contains a main slide plus two vertical details and three-level branch navigation.

## Evidence drawers and agent rehearsal

`slide-evidence` is a Markdown container with required `claim` and `status` and an
optional `title`. Status is `illustrative`, `draft`, or `source-backed` **as asserted
by the author**, never an automatic verification verdict. Include source links,
methods, assumptions, units, limitations and a likely audience question. The HTML
slide opens a drawer. Handouts and PDF expose the evidence in reading order.
Private notes and unpublished evidence must stay out of public exports.

```sh
npm run check -- _build/html/reveal/decks.json --deck exploration --out _build/exploration-review
npm run rehearse -- _build/html/reveal/decks.json _build/exploration-review/report.json _build/exploration-review/rehearsal.json
```

The rehearsal command verifies that the review matches the current HTML hash and
produces source-addressed briefs containing notes, evidence metadata, branch choices,
screenshots, detected issues and audience questions. Source locations such as
`/exploration.md` are relative to the MyST project root. Codex or Claude then performs
the review: inspect each screenshot/source, exercise the controls, answer from the
supplied evidence, and record reproduced defects separately from scientific questions
and editorial suggestions. Packet generation is not an LLM critique or a completed
scientific review. No external model API, account or credentials are required.
