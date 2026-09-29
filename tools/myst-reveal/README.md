# MyST Reveal

Author lecture slides in MyST Markdown and export a standalone Reveal.js deck
and a scrolling student handout. Quarto is not used. This package includes a
six-slide teaching example, a 26-slide feature tour, and computational-science
(13 slides), astronomy (10 slides), and advanced-tools (9 slides plus a 4-slide
short variant) examples sharing an executed notebook. A five-slide exploration
deck demonstrates linked equation/code/figure highlights, nested audience
detours, offline Python state replay, and evidence drawers.

Start with [AUTHORING.md](AUTHORING.md) for the authoring contract used by humans,
Codex, and Claude. The examples in `examples/courses/` exercise priorities 1–4
of the approved development plan. Talk variants, rehearsal tools, and a bounded agent review CLI are also implemented.

## Location and extraction

The implementation, theme, pinned dependencies, tests, and example assets live
inside this directory. It imports no course files. Extract this directory into a
separate repository when ready; install from its lockfile and use the same
commands. Existing lectures and the course publishing configuration are not
changed by this package. It is private and experimental, not a published MyST
export backend.

## Build, present, and edit

Requires Node 22+ and a working Jupyter Python kernel on PATH. The course
examples require NumPy and Matplotlib in that kernel. In this checkout:

```sh
cd /Users/anna/Teaching/comp521
source .venv/bin/activate
cd tools/myst-reveal
npm ci --ignore-scripts
npm run build:all
npm run preview
```

Open <http://127.0.0.1:4173/comp521/>. Outputs are
`_build/html/reveal/{prototype,features,computation,astronomy}.html`, with
matching `.handout.html` files and portable notebook/method pages in `sources/`. The preview is a local host, not a course deployment.

For rebuild-on-save with browser reload:

```sh
npm run dev
```

Open <http://127.0.0.1:4174/comp521/reveal/features.html>. A failed rebuild leaves
the last successful output in place and prints the build error. The watcher
covers project sources/assets and package renderer/theme sources. For the
shared course project, use `node src/dev.mjs examples/courses` and open
`http://127.0.0.1:4174/comp521/reveal/computation.html`.

For a project with several decks (configured in `slides.json`):

```sh
node src/build.mjs /absolute/path/to/project /absolute/path/to/output-directory
node src/dev.mjs /absolute/path/to/project
```

For a single-document project without a decks list:

```sh
node src/build.mjs /absolute/path/to/project /absolute/path/to/deck.html
node src/dev.mjs /absolute/path/to/project
```

The builder runs pinned MyST `build --site --execute --strict`, then renders its
resolved AST. MyST owns parsing, execution, citations, and reference resolution;
Reveal owns presentation state. This is not a generic Markdown conversion.
MyST may download its template on first build and manages cell execution caching.
Delete the project's `_build/execute` directory to require fresh execution.

## Authoring

Register `plugin.mjs` under `project.plugins`, as in the examples. Start content
with `##`; each top-level level-two heading begins a slide. Use native MyST
figures, math, citations, code cells, admonitions, and tab sets. The complete
working syntax is in `examples/features/slides.md`.

| Feature | Authoring interface |
| --- | --- |
| Reveal fragment effects and ordering | `{fragment}` with `:effect:` and optional `:index:`; equal indices reveal together |
| Incremental lists | `{slide-incremental}` around a list |
| Progressive code highlights | `{slide-code} python` with `:lines: 1\|2-3\|4` and optional `:start:` |
| Auto-Animate code | Matching `:id:` on `slide-code`, plus slide options |
| Auto-Animate elements | `{slide-element}` with `:id:`, `:style:`, and optional `:class:` |
| Columns | `{slide-columns}` with `:ratio: 2 1`, containing `{slide-column}` blocks |
| Overlaid fragments | `{slide-stack}` around staged elements |
| Speaker notes | `{speaker-note}` |
| Slide settings | `{slide-options}` containing a JSON object |
| Local video/audio | `{slide-media} file.mp4`, required `:title:`, optional kind/poster/captions/muted/loop/autoplay |
| Interactive HTML/plots | `{slide-embed} widget.html` with required `:title:` |
| Live browser Python | `{slide-python}` containing editable Python source |
| Bibliography | `{slide-bibliography}` using resolved MyST citation records |

Fragment effects include fade-in/out/up/down/left/right, fade-in-then-out,
fade-in-then-semi-out, current-visible, grow, shrink, strike, semi-fade-out, and
red/green/blue highlight and highlight-current effects. Hidden fragments are also
hidden from assistive technology and keyboard focus. Reduced-motion preferences
turn off transitions and Auto-Animate.

Example slide metadata:

````md
## A changing diagram

```{slide-options}
{"auto-animate": true, "auto-animate-id": "diagram", "transition": "fade"}
```
````

Supported attributes include transitions/speed, background color/image/video/
iframe and their size/position/repeat/opacity/transition options, Auto-Animate
options, autoslide, visibility, and state. `class` assigns a slide CSS class.
`vertical: true` groups a slide below the preceding horizontal slide. Background
images/videos and iframe HTML are local project files and are embedded.

Native MyST frontmatter `math` defines KaTeX macros. References to exported decks
navigate to the containing slide; exported source pages retain their anchors; equation/figure numbering comes from MyST.
Executed output supports stdout, plain text, PNG, SVG, and HTML. HTML output and
local HTML components run in sandboxed frames. Both native `{bibliography}` and `{slide-bibliography}` are supported. Notebook widgets that require a
Jupyter widget manager are not supported.

## Presenter controls and extensions

Reveal supplies the speaker window (S), current/next slide previews, public notes,
clock/timer, fullscreen (F), blackout (B), overview (Esc), keyboard/touch navigation,
search, and Alt-click zoom. The toolbar adds a slide navigator, notes/search/
overview shortcuts, pointer, and handout link. Use a localhost or HTTPS host for
presenter view; browser popup/fullscreen policies still apply.

Optional `slides.json` passes JSON-compatible native Reveal settings and bundles
local custom CSS and browser-global Reveal plugins:

```json
{
  "reveal": { "transition": "fade", "defaultTiming": 90 },
  "css": ["slides.css"],
  "plugins": [{ "script": "my-plugin.js", "global": "MyRevealPlugin" }]
}
```

Put extensions in top-level `plugins`, not `reveal.plugins`. Scripts must expose
the named global and bundle their own dependencies. The tour verifies the
extension interface; it does not certify every third-party plugin. CSS and
plugin scripts are trusted author code and must be self-contained for offline
use. Do not put secrets or private solutions in downloadable HTML: speaker notes
remain readable in the deck source, even though the handout removes them.

## Offline, live Python, handouts, and PDF

The presentation runtime, highlighting, KaTeX fonts, local figures, media, and
self-contained interactive components are embedded. Ordinary deck use makes no
remote asset requests in the browser checks. A browser Python component is an
explicit exception: pressing Run downloads pinned Pyodide 0.29.3 from jsDelivr.
It runs in a worker, starts fresh for each run, reports errors, has a Stop button,
and terminates execution after 15 seconds. Python runtime loading has a separate
60-second timeout. The `packages` option enables NumPy and Matplotlib; generated plots are captured
as images. This is not a configured research environment or an offline Python
distribution. Reset restores the original source and clears the output.

The handout shows fragments and tab panels in reading order and removes
presenter notes. `handoutMode: exercises` removes `slide-answer` blocks from the
file; `worked` retains them. Native linked plots become static in the handout. Open `deck.html?print-pdf`, then print/save as PDF with background
graphics enabled. The PDF contains revealed answers and static HTML tables;
audio/video and live Python receive labelled fallbacks. A `slide-embed` can
provide an authored fallback image; otherwise it receives a labelled fallback.
Interactive behavior is available in HTML. The handout is the preferred complete
reading copy of staged or tabbed material.

## Verification

Build before testing:

```sh
npm run build:all
npm test
RUN_ONLINE_TESTS=1 npm test
```

The last command also downloads and executes the real Python runtime. Tests use
macOS Google Chrome, `CHROME_PATH` when set, or Playwright Chromium elsewhere.
They start localhost servers. They cover navigation, fragment accessibility,
Auto-Animate events, code stepping, tabs, vertical slides, media playback,
interactive controls, presenter view, search, references, offline loading,
handout content, rebuild-on-save, output determinism, and rejection of unsupported
content. All tour slides are checked for overflow at 1440×900 and 1280×720.
Screenshots and PDFs are saved in `_build/checks/`, `_build/features-checks/`,
and `_build/courses-checks/` for visual inspection; geometry checks alone do not
establish good composition. Browser suites run sequentially to avoid contention
between Chrome instances during screenshots and PDF export.

For actual MyST hosting, build this isolated fixture:

```sh
cd examples/site
BASE_URL=/comp521 ../../node_modules/.bin/myst build --html --strict
```

The fixture uses `project.static_files` to copy the generated `reveal`
directory. It links decks beneath the MyST site's `/comp521/` base path. A real
course cutover should use the same arrangement and retain stable lecture pages.

## Current boundary

This is a MyST authoring layer over real Reveal.js, not complete Quarto parity.
A project can now export several decks, cross-document references, footnotes,
native bibliographies, and labelled notebook output reuse. Arbitrary MyST
interactive directives, Jupyter widget state, Quarto-specific extensions, and
arbitrary notebook MIME formats are not covered.
Unknown nodes, unresolved references, missing alt text, failed cells, and
unsupported outputs stop export instead of silently dropping content. Rich
outputs and custom embeds must provide their own accessible explanations and
self-contained resources. Layout remains an authoring responsibility.

MyST's resolved JSON and renderer are version-coupled; dependency upgrades need
these fixtures and visual checks. The theme adapts Lecture 10's indigo/teal colors
and system typography, not its entire Quarto template. No existing lecture is
migrated, and no public site is changed by these commands.


## Talk tools, columns, sizing, and review

The advanced example adds flexible two-to-four-column layouts, bounded text fit,
a dark astronomy theme, larger figure compositions, linked inset regions, image
blending, synchronized movies, live Python parameters and execution traces,
short/full talk variants, backup navigation, and rehearsal timing exports.

```sh
npm run check -- _build/html/reveal/decks.json --out _build/review
npm run bundle:python
```

The first command emits structured source-addressable findings, a contact sheet,
fragment screenshots, and PDFs. The second optionally packages the existing Python
runtime for a local server without external network access. See AUTHORING.md for
settings, examples, verification boundaries, and explicit font floors.

The checker detects defined layout and runtime issues; it does not certify visual
quality or scientific validity. Research claims, audience, timing, and source
selection still need an approved brief. Private mechanical imports of Lecture 10
(47 content slides) and the selected research talk (16 content slides) were evaluated.
The former retains one overflow and five small-text findings; the latter retains
five overflows. They are not delivery-ready migrations. Existing course slides are unchanged.
