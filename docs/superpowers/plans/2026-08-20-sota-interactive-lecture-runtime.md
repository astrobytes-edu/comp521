# SOTA Interactive Lecture Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a MyST-native, dual-mode interactive lecture runtime and use it to make the Transit Depth lecture a polished projector-first experience with independent student activities and browser-native Python.

**Architecture:** Keep MyST pages as the authoritative static reading path. The local `interactive-lecture` plugin will transform semantic source directives into accessible static sections and progressively enhance them into a presenter scene player or student activity page. Standard code activities load a course-built xeus-python JupyterLite bundle; only advanced Panel sandboxes use the documented Pyodide/Panel runtime.

**Tech Stack:** MyST 1.10.1, local JavaScript MyST plugins, browser custom elements/SVG, JupyterLite, jupyterlite-xeus, xeus-python, emscripten-forge/conda-forge, NumPy, Matplotlib, SciPy, pandas, ipywidgets, Panel 1.9.x/Bokeh 3.9.x/Pyodide 0.29.3, Python `unittest` source validators.

**Spec:** `docs/superpowers/specs/2026-08-20-sota-interactive-lecture-runtime-design.md`

## Global Constraints

- Use one MyST source page for student and presenter modes; do not introduce Reveal.js or a second slide build.
- Student mode retains normal Book-theme navigation; presenter mode is a query-string toggle with stable `#scene-<id>` anchors.
- Students advance independently. Do not add synchronization, accounts, analytics, submission, or network services.
- Core activities use the sequence: prediction, one-variable manipulation, linked evidence, explanation/revision, optional Python model.
- Use xeus-python JupyterLite for ordinary runnable code; activities must not request package installation from students.
- Use Pyodide/Panel only for labeled advanced sandboxes. Do not claim Panel is supported in xeus-python.
- Native SVG/HTML/CSS owns core instructional figures. Never use an iframe/dashboard as the primary projected stage.
- Static prose, rendered math, fallbacks, and a no-JavaScript learning path are required. Display math uses `$$...$$`.
- Drafts remain local browser state and a lecture-wide export is explicit.
- Preserve existing user changes outside the files named by a task. Work directly on `main`; do not create a worktree.

---

## File structure

| Path | Responsibility |
|---|---|
| `tools/jupyterlite/requirements.txt` | Reproducible build tooling for the course JupyterLite bundle, following the `jupyterlite/xeus-lite-demo` deployment pattern. |
| `tools/jupyterlite/environment.yml` | xeus-python browser-kernel package contract. |
| `tools/jupyterlite/jupyter_lite_config.json` | Lite build paths, contents, and frontend settings. |
| `tools/jupyterlite/build.sh` | Deterministic local builder for `assets/jupyterlite/`. |
| `assets/jupyterlite/` | Generated, deployable JupyterLite site; produced by the builder and intentionally not hand-edited. |
| `plugins/interactive-lecture/interactive-lecture.mjs` | MyST directive schemas and semantic static HTML contract. |
| `plugins/interactive-lecture/widget.mjs` | Thin MyST anywidget entry point that mounts the lecture runtime. |
| `plugins/interactive-lecture/runtime.mjs` | Scene player, mode selection, notes/export, reveal, and activity enhancement. |
| `plugins/interactive-lecture/transit-depth-figure.mjs` | Accessible native SVG transit model and exact `p^2` calculation. |
| `plugins/interactive-lecture/jupyterlite.mjs` | Lazy xeus JupyterLite code-activity iframe/controller. |
| `plugins/panel-pyodide/widget.mjs` | Isolated, lazy Pyodide/Panel sandbox implementation. |
| `03-python/interactive-lab-transit-depth.md` | First complete dual-mode lecture pilot. |
| `tests/test_check_interactive_lectures.py` | Directive-source and content-contract unit tests. |
| `scripts/check_interactive_lectures.py` | Publish-time source validator. |
| `scripts/check_jupyterlite_bundle.py` | Bundle manifest and required-package verification. |
| `README.md` | Instructor-facing authoring/build/runtime guidance. |
| `.gitignore` | Ignores visual-companion and generated local build artifacts while retaining intentional deployable assets. |

## Task 1: Build and validate the xeus-python JupyterLite environment

**Files:**
- Create: `tools/jupyterlite/requirements.txt`
- Create: `tools/jupyterlite/environment.yml`
- Create: `tools/jupyterlite/jupyter_lite_config.json`
- Create: `tools/jupyterlite/build.sh`
- Create: `scripts/check_jupyterlite_bundle.py`
- Modify: `.gitignore`
- Test: `tests/test_check_jupyterlite_bundle.py`

**Interfaces:**
- Consumes: `tools/jupyterlite/environment.yml` and the JupyterLite executable.
- Produces: `assets/jupyterlite/` containing an `xeus-python` kernel spec and packages required by code activities.

- [ ] **Step 1: Write failing bundle-contract tests**

```python
from scripts.check_jupyterlite_bundle import required_bundle_files, validate_bundle

def test_requires_xeus_kernel_and_declared_scientific_packages(tmp_path):
    (tmp_path / "jupyter-lite.json").write_text('{"jupyter-lite-schema-version": 0}')
    assert validate_bundle(tmp_path) == required_bundle_files(tmp_path)
```

- [ ] **Step 2: Run the focused test and confirm it fails because the module does not exist**

Run: `python3 -m unittest tests.test_check_jupyterlite_bundle -v`

Expected: an import failure for `scripts.check_jupyterlite_bundle`.

- [ ] **Step 3: Define the curated environment and builder**

Create `tools/jupyterlite/environment.yml` with the two channels used by the maintained `jupyterlite/xeus-lite-demo` template and exact declared packages:

```yaml
name: comp521-xeus
channels:
  - https://repo.prefix.dev/emscripten-forge-dev
  - https://repo.prefix.dev/conda-forge
dependencies:
  - xeus-python
  - numpy
  - matplotlib
  - scipy
  - pandas
  - ipywidgets
```

Create `requirements.txt` with `jupyterlite`, `jupyterlite-xeus`, and a version floor that is compatible with the installed JupyterLab. Make `build.sh` create `assets/jupyterlite/` using `jupyter lite build --output-dir`, copy `environment.yml` into the Lite build directory, and exit nonzero on any failed command. Do not silently download or install a student dependency at page runtime.

- [ ] **Step 4: Implement `validate_bundle`**

Require `jupyter-lite.json`, an `api/kernelspecs/xeus-python/kernel.json` path, and the built runtime files referenced by the Lite manifest. Require that `environment.yml` declares all six approved packages. Return formatted missing-path errors; `main()` prints errors and returns `1`, otherwise prints `JupyterLite xeus bundle check passed.`

- [ ] **Step 5: Run the focused test, build the Lite bundle, and verify the result**

Run:

```bash
python3 -m unittest tests.test_check_jupyterlite_bundle -v
bash tools/jupyterlite/build.sh
python3 scripts/check_jupyterlite_bundle.py
```

Expected: tests pass; the build emits `assets/jupyterlite/`; validator prints the pass message.

- [ ] **Step 6: Add only generated/local artifacts to `.gitignore`, then commit**

Add `/.superpowers/` and the builder's temporary directory, but do not ignore `tools/jupyterlite/` or the final deployable Lite assets if the hosting build requires them in Git.

```bash
git add .gitignore tools/jupyterlite assets/jupyterlite scripts/check_jupyterlite_bundle.py tests/test_check_jupyterlite_bundle.py
git commit -m "feat: add xeus JupyterLite course environment"
```

## Task 2: Establish semantic lecture directives and static-first HTML

**Files:**
- Modify: `plugins/interactive-lecture/interactive-lecture.mjs`
- Modify: `scripts/check_interactive_lectures.py`
- Modify: `tests/test_check_interactive_lectures.py`
- Create: `tests/fixtures/interactive-lecture-v2.md`

**Interfaces:**
- Consumes: semantic source directives from lecture pages.
- Produces: static sections with `data-lecture-kind`, `data-lecture-id`, and `data-scene-id`; the runtime consumes those attributes.

- [ ] **Step 1: Write source-validator failures for the new contract**

Add exact tests for a scene without `id`, a prediction without options, a code activity without fallback, and a duplicate activity ID. Include a passing fixture that has `lecture-predict`, `lecture-figure`, `lecture-reveal`, `lecture-code`, `lecture-checkpoint`, and `presenter-note`.

- [ ] **Step 2: Run the lecture validator tests and confirm the new cases fail**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v`

Expected: failures that identify the missing directives/validation paths.

- [ ] **Step 3: Replace note-wrapper fallback generation with semantic static sections**

Implement directive schemas for `lecture-predict`, `lecture-figure`, `lecture-code`, and `lecture-sandbox`; retain `lecture-scene`, `lecture-reveal`, `lecture-checkpoint`, `lecture-media`, and `presenter-note`. Each `run()` must emit one static section, not a static note plus a duplicate widget sibling. Preserve parsed MyST body children for formatted mathematics and links.

Use this emitted attribute shape:

```html
<section data-lecture-kind="predict" data-lecture-id="transit-depth-prediction">
  <h3>Predict</h3>
  <!-- parsed static prompt and fallback remain here -->
</section>
```

- [ ] **Step 4: Extend the source validator**

Make `validate_text()` require unique IDs for every scene/activity, `options` for predictions, `fallback` for code/sandbox, a matching reveal only when `:reveal:` is set, and valid `scene` IDs. Keep errors deterministic as `<path>:<line>: <message>`.

- [ ] **Step 5: Run the validator, MyST build, and inspect static output**

Run:

```bash
python3 -m unittest tests.test_check_interactive_lectures -v
python3 scripts/check_interactive_lectures.py
myst build --html
```

Expected: all pass; built lecture HTML has one prompt and one hidden reveal explanation, with no duplicated note shell.

- [ ] **Step 6: Commit the semantic authoring boundary**

```bash
git add plugins/interactive-lecture/interactive-lecture.mjs scripts/check_interactive_lectures.py tests/test_check_interactive_lectures.py tests/fixtures/interactive-lecture-v2.md
git commit -m "feat: add semantic interactive lecture directives"
```

## Task 3: Implement the dual-mode scene runtime and private learning state

**Files:**
- Modify: `plugins/interactive-lecture/widget.mjs`
- Create: `plugins/interactive-lecture/runtime.mjs`
- Create: `tests/runtime/lecture-runtime.html`
- Create: `tests/test_lecture_runtime_source.py`

**Interfaces:**
- Consumes: `section[data-lecture-kind]` emitted in Task 2 and `?lecture=presentation` URL state.
- Produces: `mountLecture(root: HTMLElement): void`, stable scene numbering, presenter controls, local drafts, and lecture-wide export.

- [ ] **Step 1: Write source/runtime tests for the public contract**

Test that runtime source exports `mountLecture`, uses `URLSearchParams` for `lecture=presentation`, preserves `#scene-<id>` anchors, filters keyboard navigation when `event.target.matches('input, textarea, select, [contenteditable]')`, and creates one page-wide export function.

- [ ] **Step 2: Run the focused source test and confirm it fails**

Run: `python3 -m unittest tests.test_lecture_runtime_source -v`

Expected: module/function assertions fail because `runtime.mjs` does not exist.

- [ ] **Step 3: Split widget mounting from lecture behavior**

Reduce `widget.mjs` to style injection and `mountLecture(el)` invocation. Move behavior into focused functions in `runtime.mjs`:

```js
export function presentationEnabled(url = window.location) {
  return new URL(url).searchParams.get("lecture") === "presentation";
}

export function storageKey(pageSlug, activityId) {
  return `comp521:lecture:${pageSlug}:${activityId}`;
}
```

Use `try/catch` for local storage and clipboard access. On failure, display an inline status message without discarding entered text.

- [ ] **Step 4: Implement mode behavior and export**

In student mode retain every scene in reading order. In presenter mode show one `.lecture-scene--active` stage at a time, preserve offstage content in the DOM, update `aria-current="step"`, and provide visible previous/next buttons. Copy links use `new URL('#scene-id', location.href)` with the current mode removed. Export gathers every local draft into one UTF-8 text file containing title, scene number/ID, prompt, response, and ISO timestamp.

- [ ] **Step 5: Run focused tests and a keyboard smoke check**

Run:

```bash
python3 -m unittest tests.test_lecture_runtime_source -v
myst build --html
```

Manual check: open the Transit lecture with `?lecture=presentation`, advance with ArrowRight/ArrowLeft, type into a prediction field, and confirm arrows no longer advance scenes while the field has focus.

- [ ] **Step 6: Commit the dual-mode runtime**

```bash
git add plugins/interactive-lecture/widget.mjs plugins/interactive-lecture/runtime.mjs tests/runtime/lecture-runtime.html tests/test_lecture_runtime_source.py
git commit -m "feat: add presenter and student lecture modes"
```

## Task 4: Build the native, accessible transit-depth activity

**Files:**
- Create: `plugins/interactive-lecture/transit-depth-figure.mjs`
- Create: `tests/test_transit_depth_model.py`
- Modify: `plugins/interactive-lecture/runtime.mjs`

**Interfaces:**
- Consumes: `lecture-figure` with `model: transit-depth` and a student prediction choice.
- Produces: `transitDepth(p: number): number`, `normalizedFlux(p: number): number`, and `mountTransitDepthFigure(container, state): void`.

- [ ] **Step 1: Write failing exact-model tests**

```python
from scripts.transit_depth_model import normalized_flux, transit_depth

def test_uniform_disk_depth_is_radius_ratio_squared():
    assert transit_depth(0.10) == 0.01
    assert transit_depth(0.20) == 0.04
    assert normalized_flux(0.20) == 0.96
```

Add a source contract test that requires `aria-label` text for the slider, visible normalized-flux text, and a written uniform-disk limitation.

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `python3 -m unittest tests.test_transit_depth_model -v`

Expected: import error because the shared model helper is absent.

- [ ] **Step 3: Implement a shared pure model and native SVG figure**

Create `scripts/transit_depth_model.py` with range-checked pure functions. In `transit-depth-figure.mjs`, render an SVG stellar disk, planet disk, radius-ratio slider, numerical blocked fraction, normalized flux, and a simple depth-vs-`p` curve. On every input, update all representations from the same `p * p` value. Do not use an iframe, Bokeh, or a canvas-only representation.

- [ ] **Step 4: Implement prediction-to-evidence flow**

Render three quick choices: `doubles`, `quadruples`, and `unchanged`; then permit optional private reasoning. The figure should initially show `p=0.10`; a labeled “Increase p to 0.20” control changes `p` and retains a visible “Your prediction” marker. Do not auto-grade. Reveal only becomes available after a prediction choice or explicit “skip prediction” action.

- [ ] **Step 5: Run unit checks, build, and perform visual physics checks**

Run:

```bash
python3 -m unittest tests.test_transit_depth_model -v
python3 scripts/check_math_rendering.py
myst build --html
```

Manual check: at `p=0.10`, display `0.010` blocked and `0.990` normalized flux; at `p=0.20`, display `0.040` blocked and `0.960` normalized flux. Verify keyboard slider operation and reduced-motion mode.

- [ ] **Step 6: Commit the native core activity**

```bash
git add scripts/transit_depth_model.py plugins/interactive-lecture/transit-depth-figure.mjs plugins/interactive-lecture/runtime.mjs tests/test_transit_depth_model.py
git commit -m "feat: add native transit depth learning activity"
```

## Task 5: Integrate xeus JupyterLite code activities

**Files:**
- Create: `plugins/interactive-lecture/jupyterlite.mjs`
- Modify: `plugins/interactive-lecture/runtime.mjs`
- Modify: `tools/jupyterlite/jupyter_lite_config.json`
- Create: `tests/test_jupyterlite_activity_source.py`

**Interfaces:**
- Consumes: `lecture-code` source fields `id`, `starter`, and `fallback` plus `assets/jupyterlite/` from Task 1.
- Produces: `mountCodeActivity(container, {id, starter, fallback}): Promise<void>` and a resettable xeus-python code surface.

- [ ] **Step 1: Write failing integration-source tests**

Require `mountCodeActivity`, `loading="lazy"`, a course-relative JupyterLite URL, a `Reset starter code` button, and fallback retention when iframe load fails. Assert there is no `piplite.install` or `micropip.install` in a xeus activity.

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `python3 -m unittest tests.test_jupyterlite_activity_source -v`

Expected: import/file assertions fail because `jupyterlite.mjs` does not exist.

- [ ] **Step 3: Implement lazy code-activity mounting**

Create a launch button labeled `Run this Python experiment`. On click, create a sandboxed iframe targeting the course-built JupyterLite activity URL with the starter notebook/cell path encoded as a course asset. Show an explanatory static fallback before launch and a failure message with a retry button if the iframe errors. Reset must recreate the original starter state rather than clear the kernel environment.

- [ ] **Step 4: Include a small transit starter activity in the Lite bundle**

Add a notebook or source file that calculates `depth = p**2`, prints normalized flux, plots the depth curve with the selected point, and asks the student to change one value. It must import only declared packages and match the native figure's numerical values.

- [ ] **Step 5: Run bundle, source, and browser checks**

Run:

```bash
bash tools/jupyterlite/build.sh
python3 scripts/check_jupyterlite_bundle.py
python3 -m unittest tests.test_jupyterlite_activity_source -v
myst build --html
```

Manual check: launch the activity in a fresh browser profile, execute the starter, change `p` to `0.20`, reset it, and verify no package-install instruction appears.

- [ ] **Step 6: Commit the xeus code-activity integration**

```bash
git add plugins/interactive-lecture/jupyterlite.mjs plugins/interactive-lecture/runtime.mjs tools/jupyterlite assets/jupyterlite tests/test_jupyterlite_activity_source.py
git commit -m "feat: add xeus-powered lecture code activities"
```

## Task 6: Contain Panel in a reliable Pyodide sandbox

**Files:**
- Modify: `plugins/panel-pyodide/widget.mjs`
- Modify: `plugins/interactive-lecture/runtime.mjs`
- Modify: `03-python/transit-geometry-panel.py`
- Create: `tests/test_panel_sandbox_source.py`

**Interfaces:**
- Consumes: `lecture-sandbox` static fallback and a Panel source file.
- Produces: a lazy, sandboxed Pyodide/Panel iframe titled `Advanced Panel exploration` with no nested MyST content.

- [ ] **Step 1: Write failing sandbox-source tests**

Require a sandboxed iframe, `loading="lazy"`, a status element, a retry path, title text `Advanced Panel exploration`, and no code that queries an iframe `article` or hides site navigation.

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `python3 -m unittest tests.test_panel_sandbox_source -v`

Expected: source assertions fail against the existing crop-hack implementation.

- [ ] **Step 3: Remove route embedding and the iframe crop hack**

Delete logic that loads a course route inside a Panel iframe or reaches into `contentDocument` to hide the Book theme. The only sandbox input is direct Panel Python source. Use the supported Pyodide/Panel runtime with an explicit error message and retain the static model interpretation outside the iframe.

- [ ] **Step 4: Make the Transit sandbox explicitly exploratory**

Retitle the Panel activity `Explore further: transit model sandbox`. Keep its slider and linked plot, but add an initial task that asks students to compare one changed parameter against the core `p^2` activity. Do not repeat the core prediction/reveal sequence inside the sandbox.

- [ ] **Step 5: Run focused checks and inspect the sandbox boundary**

Run:

```bash
python3 -m unittest tests.test_panel_sandbox_source -v
myst build --html
```

Manual check: open the sandbox after a hard reload; verify it has no nested course header/footer, has one plot, and its failure state leaves the static `p^2` explanation visible.

- [ ] **Step 6: Commit the Panel isolation**

```bash
git add plugins/panel-pyodide/widget.mjs plugins/interactive-lecture/runtime.mjs 03-python/transit-geometry-panel.py tests/test_panel_sandbox_source.py
git commit -m "fix: isolate Panel lecture sandboxes"
```

## Task 7: Refactor the Transit Depth page to the approved teaching sequence

**Files:**
- Modify: `03-python/interactive-lab-transit-depth.md`
- Modify: `tests/test_check_interactive_lectures.py`
- Modify: `tests/fixtures/interactive-lecture-v2.md`

**Interfaces:**
- Consumes: every directive/runtime component created in Tasks 2–6.
- Produces: a 12-minute lecture with four numbered scenes, links, presenter cues, native figure, xeus code experiment, optional Panel sandbox, and one exportable checkpoint.

- [ ] **Step 1: Write the failing pilot-contract test**

Assert the lecture source has exactly four `lecture-scene` IDs in order: `transit-setup`, `depth-model`, `transit-evidence`, `transit-run-it-yourself`; has one `lecture-predict` linked to `transit-area-reasoning`; contains the display equations `$$ p = \\frac{R_p}{R_\\star}. $$` and `$$ \\frac{F}{F_0} = 1 - p^2. $$`; and contains one `lecture-code` plus one optional `lecture-sandbox`.

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `python3 -m unittest tests.test_check_interactive_lectures.InteractiveLectureValidatorTests.test_transit_pilot_v2_contract -v`

Expected: failure because the pilot uses older directives and duplicated interaction systems.

- [ ] **Step 3: Rewrite the page around the scene sequence**

Keep the plain, concise explanation of transit, flux, normalized flux, dimensionless radius ratio, uniform surface brightness, and complete overlap. Introduce the prediction before controls; put the native transit figure directly after it; place the formatted reveal after evidence; put the xeus code activity next; move Panel to an explicitly optional end sandbox; end with a checkpoint that names relationship, evidence, and one model limitation.

- [ ] **Step 4: Add presenter cues without leaking them into student mode**

For each scene, add `presenter-note` metadata: `ask`, `wait`, `misconception`, and `transition`. Use `45 seconds` for the first prediction and make the likely misconception explicit: linear rather than area scaling.

- [ ] **Step 5: Run content and physics validation**

Run:

```bash
python3 -m unittest tests.test_check_interactive_lectures -v
python3 scripts/check_interactive_lectures.py
python3 scripts/check_math_rendering.py
python3 -m unittest tests.test_transit_depth_model -v
myst build --html --execute
```

Expected: all checks pass; no malformed math; page displays the correct flux values and one required core interaction.

- [ ] **Step 6: Commit the complete Transit pilot**

```bash
git add 03-python/interactive-lab-transit-depth.md tests/test_check_interactive_lectures.py tests/fixtures/interactive-lecture-v2.md
git commit -m "feat: pilot dual-mode transit depth lecture"
```

## Task 8: Complete accessibility, documentation, and publication checks

**Files:**
- Modify: `README.md`
- Modify: `scripts/check_interactive_lectures.py`
- Modify: `tests/test_check_interactive_lectures.py`
- Create: `docs/interactive-lecture-authoring.md`

**Interfaces:**
- Consumes: final directive schemas and built browser runtime.
- Produces: an instructor authoring guide and enforceable publication gate.

- [ ] **Step 1: Write failing validation tests for accessibility-critical source fields**

Add tests rejecting a `lecture-figure` without alt/caption text, a `lecture-code` without fallback, a `lecture-sandbox` without fallback, and a presenter note lacking a scene association.

- [ ] **Step 2: Run the validator tests and confirm the new cases fail**

Run: `python3 -m unittest tests.test_check_interactive_lectures -v`

Expected: the new constraints are not yet enforced.

- [ ] **Step 3: Implement the final source gate and author guide**

Document each directive with one compact source example, authoring criteria for a good activity, xeus build/rebuild commands, the Panel-only exception, presenter URL usage, note privacy/export behavior, and the required validation commands. Update `README.md` to replace the old scoped-`interactive-python` recommendation with the xeus/Panel distinction.

- [ ] **Step 4: Run the complete automated gate**

Run:

```bash
python3 -m unittest discover -v
python3 scripts/check_interactive_lectures.py
python3 scripts/check_jupyterlite_bundle.py
python3 scripts/check_math_rendering.py
myst build --html --execute
git diff --check
```

Expected: every command exits zero.

- [ ] **Step 5: Perform the final browser acceptance checks**

At desktop projection width, verify presenter scene navigation, controls, equation rendering, copy scene link, reveal gating, Panel lazy loading, and exported notes. At narrow student width, verify reading order, slider keyboard controls, no horizontal clipping, static fallbacks, and reduced-motion behavior. Temporarily disable JavaScript and verify that prose, equations, prompt, worked result, and model limitation are still usable.

- [ ] **Step 6: Commit documentation and close the implementation**

```bash
git add README.md docs/interactive-lecture-authoring.md scripts/check_interactive_lectures.py tests/test_check_interactive_lectures.py
git commit -m "docs: document interactive lecture authoring and checks"
```
