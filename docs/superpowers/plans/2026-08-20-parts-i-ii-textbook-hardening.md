# Parts I and II Textbook Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Parts I and II as coherent, course-agnostic, scientifically rigorous textbook parts while accurately deferring Parts III and IV.

**Architecture:** Preserve the existing chapter files and their explanatory depth. Add a consistent reader-facing core/reference contract at the top of every completed chapter; make guides and recaps independent entry points; replace course-specific framing with transferable scientific examples and prompts. Use lightweight structural tests to prevent regressions, while MyST builds and visual reviews qualify the rendered result.

**Tech Stack:** MyST Markdown, Python/pytest structural tests, existing MyST validation scripts.

**Spec:** `docs/superpowers/specs/2026-08-20-scientific-computing-with-python-textbook-design.md`

## Global Constraints

- Do not include expected-time estimates, COMP 521 projects, deadlines, grades, submissions, or weekly schedule language in textbook pages.
- Preserve useful scientific examples, including astronomy and transit/root-finding examples, but label assumptions and provide a domain-transferable interpretation or prompt.
- Keep advanced material. Mark it as `Deep dive / reference` rather than deleting important context.
- A completed Chapter 1–10 must expose: Scientific question, Core ideas, Prerequisites, Learning objectives, worked scientific example, Predict → run → explain → revise, Apply or extend, and Recap/next connection.
- Parts III and IV must be visibly deferred, never presented as Release 1 requirements or completed instruction.
- Work directly on `main`; the user explicitly declined worktrees.
- Preserve the existing untracked `tests/fixtures/` directory.

---

### Task 1: Encode the Release 1 contract in the design and tests

**Files:**
- Modify: `docs/superpowers/specs/2026-08-20-scientific-computing-with-python-textbook-design.md`
- Modify: `tests/test_course_navigation.py`

**Interfaces:**
- Consumes: the completed-chapter contract in the design spec.
- Produces: `PART_I_II_CHAPTERS` structural inventory and assertions that prevent title, contract-heading, and course-specific-language regressions.

- [ ] **Step 1: Add the approved release implementation strategy to the design specification.**

  Include explicit Release 1 completion criteria for Parts I–II, a deferral policy for Parts III–IV, and a per-chapter audit/build/visual-review workflow.

- [ ] **Step 2: Write failing structural tests.**

  Add a single parameterized inventory for Chapters 1–10 and assert the course-agnostic contract tokens:

  ```python
  PART_I_II_CHAPTERS = (
      "03-python/01-python-environment.md",
      # … Chapters 2–10 in canonical order …
  )

  @pytest.mark.parametrize("path", PART_I_II_CHAPTERS)
  def test_completed_chapter_exposes_reader_contract(path):
      text = (ROOT / path).read_text()
      for heading in (
          "## Scientific question",
          "## Core ideas",
          "## Prerequisites",
          "## Learning objectives",
          "## Predict → run → explain → revise",
          "## Apply or extend",
          "## Recap and next connection",
      ):
          assert heading in text
  ```

  Add targeted assertions that Part I and II guides do not contain `Project 1`,
  `assignments and projects`, or a link to Chapter 11; assert the Part III
  guide contains `in development`.

- [ ] **Step 3: Run the targeted test to verify failure.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

  Expected: failure because the live chapters have not yet adopted the
  contract.

- [ ] **Step 4: Complete the remaining tasks, then run the structural suite.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

- [ ] **Step 5: Commit the contract gate with the first hardening slice.**

  Commit message: `test: enforce Parts I and II textbook contract`

### Task 2: Make the Part I guide and recap independent textbook pages

**Files:**
- Modify: `03-python/index.md`
- Modify: `03-python/synthesis.md`

**Interfaces:**
- Consumes: Part I title and Chapter 1–6 order in `myst.yml`.
- Produces: independent entry and recap pages that link only to the Part I
  chapter sequence and Part II guide.

- [ ] **Step 1: Replace course-facing front matter and headings.**

  Use `Start Here: Part I Guide — Foundations for Scientific Programming` and
  `Part I Recap — Trustworthy Scientific Programming`. Remove COMP 521
  subtitles and all book-level use of `module`.

- [ ] **Step 2: Replace the project core route with a reader route.**

  Give the guide two entry modes: `First reading` (Chapters 1–5 in order,
  Chapter 6 when stateful entities are useful) and `Return visit` (diagnostic
  links by problem). Preserve useful habits, but replace project language with
  statements such as “use this when a calculation needs a named assumption or
  a reproducible check.”

- [ ] **Step 3: Add an explicit core/reference convention.**

  Explain that each chapter starts with core concepts and an evidence loop;
  deep dives are reference material that can be consulted when the reader has
  a concrete need. Do not give reading-time estimates.

- [ ] **Step 4: Make the recap a diagnostic and transfer page.**

  Preserve the code-as-instrument framing; replace course standards with a
  reusable diagnostic table: symptom, likely cause, next check, and relevant
  chapter. End at the Part II guide.

- [ ] **Step 5: Commit the Part I entry slice.**

  Commit message: `docs: harden Part I textbook guide and recap`

### Task 3: Harden Chapters 1–3 as the scientific-programming core

**Files:**
- Modify: `03-python/01-python-environment.md`
- Modify: `03-python/02-python-calculator.md`
- Modify: `03-python/03-python-control-flow.md`

**Interfaces:**
- Consumes: the shared chapter headings from Task 1 and the Part I guide from
  Task 2.
- Produces: course-agnostic Chapter 1–3 opening contracts and accurate
  forward links to Chapters 2–4.

- [ ] **Step 1: Insert the shared reader-contract headings before legacy content.**

  For each chapter, write concise content under the required headings. Keep
  the existing detailed material below an explicit `## Deep dive / reference`
  boundary when it is not part of the first-use core.

- [ ] **Step 2: Use these chapter-specific core examples and checks.**

  - Chapter 1: record `sys.executable`, Python version, and a package version;
    predict why a different interpreter changes an import result; revise the
    environment record.
  - Chapter 2: compute a quantity with explicitly named units, compare two
    floating-point results with `math.isclose`, and explain a failed exact
    equality check.
  - Chapter 3: write a bounded convergence loop with `max_iter`, predict the
    outcome for a non-converging case, then explain why the guard is evidence
    rather than a workaround.

- [ ] **Step 3: Remove course setup, project policy, and course-specific
  prerequisites.**

  Chapter 1 links to the generic environment concepts and may refer readers to
  a separately maintained setup companion; it must not require a `comp521`
  environment. Chapters 2–3 must not invoke course projects or course
  submission rules.

- [ ] **Step 4: Repair forward links and terminology.**

  Ensure each recap names the immediate next chapter and uses `Part`/`Chapter`
  rather than `module`.

- [ ] **Step 5: Run targeted structural tests and commit.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

  Commit message: `docs: harden foundational scientific programming chapters`

### Task 4: Harden Chapters 4–6 and complete Part I

**Files:**
- Modify: `03-python/04-python-data-structures.md`
- Modify: `03-python/05-python-functions-modules.md`
- Modify: `03-python/06-oop-fundamentals.md`
- Modify: `myst.yml`

**Interfaces:**
- Consumes: shared chapter contract and Part I navigation.
- Produces: complete Part I whose TOC label and pages agree with the design
  specification.

- [ ] **Step 1: Add the shared opening/closing contract to Chapters 4–6.**

  Use scientific data organization, a unit-bearing function contract, and a
  small stateful measured entity as the worked examples. Each chapter gets a
  direct predict–inspect–explain–revise activity and a transfer prompt.

- [ ] **Step 2: Preserve depth but bound it.**

  Mark caching/memory internals and specialized structures in Chapter 4;
  closures/decorators/package internals in Chapter 5; inheritance and
  special-method catalogues in Chapter 6 as `Deep dive / reference`.

- [ ] **Step 3: Correct scientific and cross-reference claims.**

  Correct the Mars Climate Orbiter description: incompatible lbf-s versus N-s
  impulse-bit data caused an approximately 4.45 factor error in navigation
  calculations; it does not establish that physical thrusters delivered 4.45
  times their intended force. Remove course-project framing and make the
  Chapter 6 next connection Chapter 7.

- [ ] **Step 4: Align the Part I TOC label and page titles with the canonical
  design.**

  In `myst.yml`, use `Part I · Foundations for Scientific Programming` and
  `Part II · Arrays, Visualization, and Reliable Computing`.

- [ ] **Step 5: Run structural tests, strict build, and commit.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

  Run: `myst build --site --strict`

  Commit message: `docs: complete Part I textbook hardening`

### Task 5: Make the Part II guide a truthful independent entry page

**Files:**
- Modify: `04-scientific-computing/index.md`

**Interfaces:**
- Consumes: Part II chapter sequence (7–10) and Part III deferred status.
- Produces: Part II guide that describes arrays, figures, reliability, and
  small scientific types without promising Chapter 11, productionization, or
  universal performance outcomes.

- [ ] **Step 1: Replace title, subtitle, warning banner, and module wording.**

  Use `Start Here: Part II Guide — Arrays, Visualization, and Reliable
  Computing`. Remove the generic revision banner and all COMP 521 language.

- [ ] **Step 2: Describe Chapters 7–10 using their actual Release 1 scope.**

  Chapters 7–8: arrays and figures for inspection. Chapter 9: behavioral and
  numerical evidence. Chapter 10: small scientific types and invariants.
  Remove the Chapter 11 link and advanced OOP/performance/C/Fortran promise.

- [ ] **Step 3: Add first-reading and diagnostic routes.**

  Include entry questions such as “why is this shape wrong?”, “what does this
  plot support?”, “how do I test a numerical claim?”, and “does this object
  need state?” Link only to Chapters 7–10 and Part III as an optional future
  direction.

- [ ] **Step 4: Run targeted test and commit.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

  Commit message: `docs: harden Part II textbook guide`

### Task 6: Harden Chapters 7–8 as arrays and visual evidence

**Files:**
- Modify: `04-scientific-computing/07-numpy-fundamentals.md`
- Modify: `04-scientific-computing/08-matplotlib-fundamentals.md`

**Interfaces:**
- Consumes: the shared chapter contract and Part II guide.
- Produces: accurate core explanations of NumPy arrays and Matplotlib figures,
  with specialized material behind reference boundaries.

- [ ] **Step 1: Add shared first-screen contracts and core/deep-dive routes.**

  Chapter 7 core covers creation, dtype, shape, vectorization, masking,
  broadcasting, copies/views, and reproducible random generators. Chapter 8
  core covers `Figure`/`Axes`, labels/units, scale selection, uncertainty,
  accessible encodings, and export.

- [ ] **Step 2: Add evidence-loop activities.**

  Chapter 7: predict the result shape before a broadcast, inspect it, then
  revise an incorrect axis assumption. Chapter 8: compare two encodings of the
  same measurements, identify the claim each figure can and cannot support,
  then revise labels/scales/caption.

- [ ] **Step 3: Correct unsafe or overconfident reference material.**

  Do not recommend rounding physically meaningful float values as cache keys;
  require a declared grid/bin identity or resolution. Defer FFT, interpolation,
  Monte Carlo, WCS, `yt`, Seaborn, Plotly, Astropy, and performance claims to
  deep dives. If FFT remains, explain `fftfreq` ordering and real-signal
  `rfft`/`rfftfreq` accurately.

- [ ] **Step 4: Correct file-I/O prerequisites.**

  Do not claim Chapter 6 teaches file I/O; either link to the actual file-I/O
  section or introduce the necessary operation locally.

- [ ] **Step 5: Run strict build and commit.**

  Run: `myst build --site --strict`

  Commit message: `docs: harden arrays and visual evidence chapters`

### Task 7: Rebuild Chapters 9–10 around scientific evidence and small types

**Files:**
- Modify: `04-scientific-computing/09-robust-computing.md`
- Modify: `04-scientific-computing/10-advanced-oop.md`

**Interfaces:**
- Consumes: Part II guide, the shared contract, pytest/Ruff references in the
  design spec.
- Produces: a completed evidence/testing chapter and a focused small-scientific-
  types chapter, both pointing accurately to Part III's deferred guide.

- [ ] **Step 1: Reframe Chapter 9.**

  Rename it `Chapter 9: Testing, Failure Modes, and Reproducible Scientific
  Code`. Make `pytest`, `numpy.testing`, tolerances, parameterized boundary
  tests, known-solution checks, deterministic random generators, and
  convergence tests part of the core. State plainly that passing tests does
  not validate physical adequacy or calibration.

- [ ] **Step 2: Rebuild Chapter 10's opening and core narrative.**

  Rename it `Chapter 10: Designing Small Scientific Types`. Make a dataclass
  with unit-bearing fields, validation/invariants, representation, composition
  with functions, and tests the only core implementation. Do not require
  abstract base classes, multiple inheritance, mixins, async, metaclasses,
  patterns, descriptors, slots, or profiling.

- [ ] **Step 3: Move advanced material behind one explicit reference boundary.**

  Preserve useful advanced material but label it reference-only and remove all
  claims that NumPy ufuncs rely on ABCs, Matplotlib uses mixins, or fixed
  memory/speed multipliers apply generally. Replace with “measure in the
  workload you have” and a small local measurement pattern where needed.

- [ ] **Step 4: Repair navigation and terminology.**

  Chapter 9 ends at Chapter 10. Chapter 10 ends at the deferred Part III
  guide. Remove `Module 2`/`Module 3`, current-course, and production-grade
  rhetoric.

- [ ] **Step 5: Run focused tests, strict build, and commit.**

  Run: `PYTHONPATH=. uv run --with pytest pytest -q tests/test_course_navigation.py`

  Run: `myst build --site --strict`

  Commit message: `docs: complete Part II scientific evidence core`

### Task 8: Defer Parts III and IV honestly and perform release qualification

**Files:**
- Modify: `04-scientific-computing/part-3-data-workflows.md`
- Modify: `04-scientific-computing/11-pandas-fundamentals.md`
- Modify: `04-scientific-computing/12-data-acquisition-cleaning.md`
- Modify: `myst.yml`
- Modify: `tests/test_course_navigation.py`

**Interfaces:**
- Consumes: Release 1 boundary.
- Produces: a stable main navigation that shows Parts III–IV as planned rather
  than completed textbook material, while retaining already authored content
  as clearly marked preview/reference pages.

- [ ] **Step 1: Replace Part III's course project wording with a concise status card.**

  Use `Part III Guide — Tabular Data and Reproducible Workflows (in
  development)`. State its intended themes and that Release 1 does not require
  it. Do not describe its organization, examples, or exercises as final.

- [ ] **Step 2: Mark Chapters 11–12 accurately.**

  Chapter 11 is an early preview/reference and not part of the Release 1
  textbook contract. Chapter 12 is explicitly in development; preserve no
  implication that a scope note is a finished chapter.

- [ ] **Step 3: Ensure no Part IV placeholder is added to the live TOC.**

  Keep Part IV in the design specification only until its first substantive
  guide exists. The main textbook navigation should expose the Part III
  preview only as an optional later direction.

- [ ] **Step 4: Add/update tests for deferred-status copy.**

  Assert the Part III guide and Chapter 12 include `in development` and that
  the Part II guide does not link Chapter 11.

- [ ] **Step 5: Run the full qualification suite.**

  Run:

  ```bash
  PYTHONPATH=. uv run --with pytest pytest -q
  python scripts/check_math_rendering.py
  python scripts/check_landing_page.py
  python scripts/check_interactive_lectures.py
  myst build --site --strict
  git diff --check
  ```

- [ ] **Step 6: Inspect the Part I guide, Chapter 1, Part II guide, Chapters
  7–10, and Part III guide at desktop and narrow widths.**

  Record any clipped callouts, broken math, duplicate headings, stale course
  links, or visually indistinguishable deep dives; repair them before Release
  1 is called ready.

- [ ] **Step 7: Commit the release boundary and qualification changes.**

  Commit message: `docs: defer unfinished textbook parts`

## Plan self-review

- **Spec coverage:** Tasks 1–7 implement Release 1; Task 8 implements the
  Parts III–IV deferral and release qualification boundary.
- **No-placeholder check:** The plan contains no unspecified implementation
  step; chapter-specific core examples, exact headings, tests, commands, and
  commit boundaries are stated.
- **Scope check:** Part III authoring and Part IV page creation are intentionally
  excluded. The first release is Parts I–II only.
