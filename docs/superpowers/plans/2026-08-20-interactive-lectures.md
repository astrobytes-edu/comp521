# Interactive Lectures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build MyST-native, static-first interactive lecture components and use them to turn the Transit Depth Lab into a live-teaching pilot.

**Architecture:** Keep the MyST Book Theme and add a focused `interactive-lecture` plugin with page-local widgets for writing, reveals, checkpoints, presentation mode, and media. Reuse the existing isolated `panel-pyodide` iframe directive for rich visual evidence; ordinary MyST prose and figures remain the fallback learning path.

**Tech Stack:** MyST 1.10.1, local MyST plugins/anywidget ESM, vanilla browser APIs, Panel 1.9.x, Bokeh 3.9.x, Pyodide 0.29.3, Python standard-library `unittest`.

**Spec:** `docs/superpowers/specs/2026-08-20-interactive-lectures-design.md`

## Global Constraints

- Preserve the existing MyST Book Theme; do not introduce a replacement theme or slide runtime.
- Keep static prose, figures, equations, prompts, and fallbacks readable before JavaScript loads.
- Use Panel only through the existing `panel-pyodide` directive; no Panel server, WebSockets, accounts, analytics, chat, or synchronization service.
- Add no HoloViews, hvPlot, Plotly, ipywidgets, or 3-D/WebGL dependency.
- Use `$...$` for inline and `$$...$$` for display math; never use `\(...\)` or `\[...\]`.
- Student writing remains browser-local under `comp521:lecture:<page-slug>:<prompt-id>` and is exportable as UTF-8 text.
- Videos never autoplay and require MP4, WebM, poster, captions, transcript, and static alternative before publication.
- Every directive needs a stable author-supplied `id`; duplicate IDs are errors.
- Validate with the existing math guard, the new lecture guard, `myst build --html --execute`, keyboard and narrow-layout browser smoke checks.

---

## File structure

| File | Responsibility |
|---|---|
| `plugins/interactive-lecture/interactive-lecture.mjs` | Register and parse all lecture directives into anywidget models. |
| `plugins/interactive-lecture/shared.mjs` | Escape text, create controls, storage/export helpers, presentation state, and shared CSS. |
| `plugins/interactive-lecture/widget.mjs` | Render `interactive-lecture`, scene, write, reveal, checkpoint, and media widgets. |
| `assets/lectures/transit-occultation.svg` | Accessible static diagram for the Transit pilot fallback. |
| `scripts/check_interactive_lectures.py` | Reject invalid lecture source contracts before MyST build. |
| `tests/test_check_interactive_lectures.py` | Unit tests for the source validator using temporary Markdown fixtures. |
| `03-python/interactive-lab-transit-depth.md` | Refactor the existing activity into the interactive-lecture pilot. |
| `03-python/interactive-dashboard-transit.md` | Keep the reusable Panel evidence scene; add explicit static fallback prose. |
| `myst.yml` | Register the new plugin; do not change the Book Theme. |
| `README.md` | Document authoring and local-first privacy/media rules. |

### Task 1: Add source-contract tests and the lecture validator

**Files:**
- Create: `tests/test_check_interactive_lectures.py`
- Create: `scripts/check_interactive_lectures.py`

**Interfaces:**
- Produces `validate_text(text: str, path: str) -> list[str]`.
- Produces CLI exit code `0` when no errors and `1` after printing `path:line: message` errors.
- Later tasks rely on directive contracts checked by this CLI.

- [ ] **Step 1: Write failing validator tests**

```python
from scripts.check_interactive_lectures import validate_text

def test_rejects_duplicate_prompt_ids():
    text = """:::{lecture-write}\n:id: same\n:prompt: First\n:::\n:::{lecture-checkpoint}\n:id: same\n:prompt: Second\n:::\n"""
    assert validate_text(text, "lesson.md") == [
        "lesson.md:5: duplicate lecture prompt id 'same'"
    ]

def test_rejects_media_without_accessibility_assets():
    text = """:::{lecture-media}\n:id: orbit\n:mp4: orbit.mp4\n:::\n"""
    assert validate_text(text, "lesson.md") == [
        "lesson.md:1: lecture-media requires webm, poster, captions, transcript, and fallback"
    ]

def test_accepts_complete_panel_contract():
    text = """:::{lecture-panel}\n:id: depth\n:src: transit-geometry-dashboard\n:fallback: The blocked fraction is p squared.\n:::\n"""
    assert validate_text(text, "lesson.md") == []
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v`

Expected: FAIL because `scripts.check_interactive_lectures` does not exist.

- [ ] **Step 3: Implement the minimal validator**

Implement directive-block parsing with these exact requirements:

```python
LECTURE_DIRECTIVES = {
    "interactive-lecture", "lecture-scene", "lecture-write", "lecture-reveal",
    "lecture-panel", "lecture-checkpoint", "lecture-media",
}
PROMPT_DIRECTIVES = {"lecture-write", "lecture-checkpoint"}

def validate_text(text: str, path: str) -> list[str]:
    """Return source-contract errors using one-based Markdown line numbers."""
```

Require `id` for every lecture directive except `interactive-lecture`; require
`prompt` for writing/checkpoint, `src` plus nonempty `fallback` for Panel,
`reveal` target on writing blocks when supplied, and the five media fields
listed in the spec. Search all public reading directories used by
`check_math_rendering.py`.

- [ ] **Step 4: Run unit tests and source validation**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v && python3 scripts/check_interactive_lectures.py`

Expected: all unit tests PASS; the current corpus reports no invalid lecture
blocks because no lecture directives are yet registered in source.

- [ ] **Step 5: Commit the validator slice**

```bash
git add scripts/check_interactive_lectures.py tests/test_check_interactive_lectures.py
git commit -m "test: add interactive lecture source contract"
```

### Task 2: Register lecture directives and render static-first widgets

**Files:**
- Create: `plugins/interactive-lecture/interactive-lecture.mjs`
- Create: `plugins/interactive-lecture/shared.mjs`
- Create: `plugins/interactive-lecture/widget.mjs`
- Modify: `myst.yml`

**Interfaces:**
- Consumes directive options validated by Task 1.
- Produces the directives `interactive-lecture`, `lecture-scene`,
  `lecture-write`, `lecture-reveal`, `lecture-panel`, `lecture-checkpoint`, and
  `lecture-media`.
- Each directive passes `{kind, id, pageSlug, options, body}` to `widget.mjs`.

- [ ] **Step 1: Add a failing plugin smoke fixture**

Create `tests/fixtures/interactive-lecture-smoke.md` containing one of every
directive, including a `lecture-write` linked to a `lecture-reveal`, a panel
fallback, and complete media options. Add this assertion to the test module:

```python
def test_smoke_fixture_satisfies_the_source_contract():
    fixture = Path("tests/fixtures/interactive-lecture-smoke.md").read_text()
    assert validate_text(fixture, "fixture.md") == []
```

- [ ] **Step 2: Run the fixture test to verify failure**

Run: `python3 -m unittest tests.test_check_interactive_lectures.InteractiveLectureValidatorTests.test_smoke_fixture_satisfies_the_source_contract -v`

Expected: FAIL until the fixture exists with complete directive options.

- [ ] **Step 3: Implement directive registration**

Use the existing `interactive-python` plugin as the local convention. For each
directive, return an `anywidget` with a stable `id`, ESM path relative to the
source page, and a model matching this shape:

```js
{
  kind: "lecture-write",
  id: "depth-prediction",
  pageSlug: vfile.path.replace(/\.md$/, ""),
  options: { prompt: "…", rows: 4, reveal: "depth-reasoning" },
  body: ""
}
```

Register the plugin below the existing `panel-pyodide` plugin in `myst.yml`.
Do not alter `site.template: book-theme`.

- [ ] **Step 4: Implement static-first rendering and shared styling**

`widget.mjs` must render semantic HTML first: `<section>`, heading, prompt,
fallback prose, `<textarea>`, and native `<button>` controls. Add styles only
through the widget root. Use the semantic accents from the spec and
`@media (prefers-reduced-motion: reduce)` to suppress transition effects.

- [ ] **Step 5: Build the plugin smoke page**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v && myst build --html`

Expected: validator and MyST build PASS, and the output logs list
`COMP 521 interactive lectures` with seven directives.

- [ ] **Step 6: Commit the directive/runtime slice**

```bash
git add myst.yml plugins/interactive-lecture tests/fixtures tests/test_check_interactive_lectures.py
git commit -m "feat: add static-first interactive lecture directives"
```

### Task 3: Add private writing, reveal, checkpoint, and presentation behavior

**Files:**
- Modify: `plugins/interactive-lecture/shared.mjs`
- Modify: `plugins/interactive-lecture/widget.mjs`

**Interfaces:**
- Consumes `kind`, stable IDs, and page slug from Task 2.
- Produces `storageKey(pageSlug, promptId)`, `downloadNotes(pageSlug, title)`,
  `renderWrite(model)`, `renderReveal(model)`, `renderCheckpoint(model)`, and
  `renderLectureShell(model)`.

- [ ] **Step 1: Add failing browser-behavior specifications as comments in the fixture**

Place this exact acceptance section at the end of the smoke fixture:

```md
<!-- browser assertions:
write saves to comp521:lecture:tests/fixtures/interactive-lecture-smoke:depth-prediction
reveal begins collapsed and exposes aria-expanded
checkpoint text appears in downloaded notes
arrow navigation does not run while textarea is focused
-->
```

- [ ] **Step 2: Implement storage and note export**

Use these exact browser APIs:

```js
export function storageKey(pageSlug, promptId) {
  return `comp521:lecture:${pageSlug}:${promptId}`;
}

export function saveDraft(key, value) { localStorage.setItem(key, value); }
export function loadDraft(key) { return localStorage.getItem(key) ?? ""; }
```

On every `input`, save the draft; expose Copy using `navigator.clipboard`,
Download using a Blob with `text/plain;charset=utf-8`, and Clear after a native
confirmation. Build the export from all lecture prompt widgets in DOM order.

- [ ] **Step 3: Implement reveal and presentation behavior**

Render reveals as a native button plus target region. Start with
`aria-expanded="false"`, `hidden`, and no automatic reveal. Add presentation
mode controls to the lecture shell. Left/Right only moves between scenes when
`event.target` is not `INPUT`, `TEXTAREA`, `SELECT`, or a contenteditable node.
Focus the next scene heading after navigation.

- [ ] **Step 4: Manually verify the browser contract**

Run: `myst start --port 3001`

Verify in a clean browser tab: type a draft, reload, copy/download/clear it,
toggle reveal with keyboard, tab through controls, enter presentation mode,
and press arrow keys both inside and outside the textarea.

- [ ] **Step 5: Commit the interaction slice**

```bash
git add plugins/interactive-lecture tests/fixtures
git commit -m "feat: add private lecture prompts and paced reveals"
```

### Task 4: Add media and Panel fallback contracts

**Files:**
- Modify: `plugins/interactive-lecture/widget.mjs`
- Modify: `plugins/interactive-lecture/shared.mjs`
- Modify: `README.md`

**Interfaces:**
- Consumes `lecture-media` options `mp4`, `webm`, `poster`, `captions`,
  `transcript`, `fallback`, optional `youtube_id`.
- Consumes `lecture-panel` options `src`, `fallback`.
- Produces a native `<video>` plus local sources/tracks and a deliberate
  YouTube outbound link.

- [ ] **Step 1: Add a media contract test**

Add to `tests/test_check_interactive_lectures.py`:

```python
def test_rejects_youtube_only_media():
    text = """:::{lecture-media}\n:id: transit-motion\n:youtube_id: abc123\n:::\n"""
    assert validate_text(text, "lesson.md") == [
        "lesson.md:1: lecture-media requires mp4, webm, poster, captions, transcript, and fallback"
    ]
```

- [ ] **Step 2: Implement native media rendering**

Create a `<video controls preload="metadata" poster="…">` containing one MP4
and one WebM `<source>`, a `<track kind="captions" srclang="en" default>`, a
visible transcript link, and fallback text below it. Do not set `autoplay` or
render a YouTube iframe. When `youtube_id` is present, render an external link
to `https://www.youtube.com/watch?v=<encoded-id>` labeled “Watch on YouTube.”

- [ ] **Step 3: Render Panel fallbacks before the iframe**

`lecture-panel` must render its fallback explanatory paragraph before an iframe
whose `src` targets the route given by `src`; use `loading="lazy"` and title it
with the panel’s author-provided label. The fallback remains visible if the
iframe fails to load.

- [ ] **Step 4: Document the authoring rules**

Add a README section with the full option table, local-first privacy promise,
the media asset set, and the package exclusion list.

- [ ] **Step 5: Run checks**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v && python3 scripts/check_interactive_lectures.py && myst build --html`

Expected: PASS with no YouTube iframe in generated lecture HTML.

- [ ] **Step 6: Commit the media/fallback slice**

```bash
git add README.md plugins/interactive-lecture tests/test_check_interactive_lectures.py
git commit -m "feat: add accessible lecture media and panel fallbacks"
```

### Task 5: Refactor the Transit Depth Lab into the pilot interactive lecture

**Files:**
- Create: `assets/lectures/transit-occultation.svg`
- Modify: `03-python/interactive-lab-transit-depth.md`
- Modify: `03-python/interactive-dashboard-transit.md`
- Modify: `03-python/index.md`

**Interfaces:**
- Consumes all Task 2–4 directives and the existing
  `interactive-dashboard-transit` Panel route.
- Produces one live-useful, static-readable explanation of what a transit is.

- [ ] **Step 1: Add a failing source-contract assertion for the pilot**

```python
def test_transit_pilot_has_no_lecture_contract_errors():
    pilot = Path("03-python/interactive-lab-transit-depth.md").read_text()
    assert validate_text(pilot, "03-python/interactive-lab-transit-depth.md") == []
```

- [ ] **Step 2: Create the static transit diagram**

Create `assets/lectures/transit-occultation.svg` with a labeled stellar disk,
planet silhouette, observer arrow, blocked-light region, title, and a
`<desc>` explaining that a transit is a planet crossing in front of the visible
stellar disk. Keep all text at 16 px or larger and use course colors with
non-color labels.

- [ ] **Step 3: Rewrite the lab as a paced lecture**

Use this exact scene order:

```text
1. What a transit is — SVG plus plain definition.
2. Predict — private prompt asking whether doubling p doubles or quadruples depth.
3. Evidence — retained numeric calculation plus Panel geometry dashboard and fallback.
4. Reveal — area-ratio reasoning: blocked fraction p²; normalized flux 1 − p².
5. Checkpoint — exportable statement of relationship, evidence, and one limit.
```

Keep the existing clean-kernel/project-notebook handoff. Remove the bespoke
interactive Python widget only if every instructional function is supplied by
the lecture blocks and Panel scene; otherwise retain it as a named optional
“run the formula yourself” scene.

- [ ] **Step 4: Add explicit Panel fallback prose**

In `03-python/interactive-dashboard-transit.md`, add the fixed baseline:
`p = 0.10` gives blocked fraction `0.010` and normalized flux `0.990`; doubling
`p` to `0.20` gives blocked fraction `0.040`. State that the relationship is
quadratic and assumes a uniform fully occulted stellar disk.

- [ ] **Step 5: Run pilot checks**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v && python3 scripts/check_math_rendering.py && python3 scripts/check_interactive_lectures.py && myst build --html --execute`

Expected: all checks PASS and the build executes the retained static baseline.

- [ ] **Step 6: Perform browser acceptance checks**

Run: `myst start --port 3001`

Verify at desktop and 390 px width: diagram labels remain legible; the writing
draft persists across reload; reveal is keyboard-operable; Panel loads only
when reached; no second figure appears after footer navigation; disabling
JavaScript still leaves the definition, diagram, numerical baseline, reasoning,
and checkpoint prompt visible.

- [ ] **Step 7: Commit the pilot slice**

```bash
git add assets/lectures 03-python/interactive-lab-transit-depth.md 03-python/interactive-dashboard-transit.md 03-python/index.md tests/test_check_interactive_lectures.py
git commit -m "feat: pilot interactive transit depth lecture"
```

### Task 6: Integrate release checks and inspect the finished deliverable

**Files:**
- Modify: `README.md`
- Modify: `.github/workflows/ci.yml` if present; otherwise create `scripts/check_course_site.sh`

**Interfaces:**
- Consumes the two validator CLIs and MyST build commands.
- Produces a documented one-command local publication check.

- [ ] **Step 1: Locate CI without assuming a workflow exists**

Run: `rg --files .github scripts | sort`

Expected: identify whether the repository has a CI workflow. Use the existing
workflow if present; otherwise create `scripts/check_course_site.sh` with
`set -euo pipefail` and the exact commands from Step 2.

- [ ] **Step 2: Add the release command sequence**

```bash
python3 scripts/check_math_rendering.py
python3 scripts/check_interactive_lectures.py
python3 -m unittest tests.test_check_interactive_lectures -v
myst build --html --execute
git diff --check
```

- [ ] **Step 3: Run the full gate**

Run the exact sequence above.

Expected: all commands exit 0; MyST builds the full course including the
Transit pilot.

- [ ] **Step 4: Self-review against the spec**

Check each design heading—teaching model, authoring interface, runtime boundary,
visual system, media, accessibility, validation, and Transit pilot—against a
specific completed task. Confirm no package outside Panel/Bokeh/Pyodide was
added and no new theme was introduced.

- [ ] **Step 5: Commit the release-gate slice**

```bash
git add README.md .github scripts
git commit -m "chore: add interactive lecture release gate"
```

## Plan self-review

- Spec coverage: Tasks 1–2 implement directive contracts and static-first
  rendering; Task 3 implements private writing, reveals, checkpoints, and live
  pacing; Task 4 implements media and Panel fallback; Task 5 implements the
  Transit pilot and explains transits; Task 6 adds release verification.
- Placeholder scan: the plan contains no placeholder tasks, unspecified error
  paths, or generic testing steps; every command, interface, and acceptance
  criterion is named.
- Interface consistency: all prompts use `id`, all local drafts use
  `storageKey(pageSlug, promptId)`, and all Panel scenes use `src` plus
  `fallback` throughout the plan.
