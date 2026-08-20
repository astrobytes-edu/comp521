# Course-Site Cutover Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the published MyST navigation into durable course-material libraries, with a concise weekly route and clear homes for lectures, practice labs, assessments, and reusable tools.

**Architecture:** Keep existing source files in place and change only their MyST navigation homes, so internal links and current URLs remain stable. Add four intentionally small canonical orientation/index pages that direct students to existing authority rather than duplicating deadlines, project instructions, or policies.

**Tech Stack:** MyST Markdown, MyST book-theme navigation, existing site-validation scripts, pytest.

**Spec:** `docs/superpowers/specs/2026-08-20-course-site-information-architecture-design.md`

## Global Constraints

- Preserve every existing source file path and internal link during this cutover.
- Use `Course Info & Roadmap` as the first top-level navigation branch.
- Keep `Scientific Computing with Python` as a top-level textbook; retain `Chapter N:` for all twelve Python textbook chapters.
- Move Numerical Modeling and Data/Inference/Scientific ML beneath the top-level `Readings` branch without rewriting their content.
- Put the Transit Depth page in `Lectures`; do not expose a browser notebook launcher as a lecture requirement.
- Create `This Week`, `Course Technology & Submission Path`, `Practice Labs`, and `Assessment Overview` as concise canonical orientation pages only.
- Do not copy authoritative dates, deadlines, grading criteria, policy prose, or project instructions into a new page.
- `This Week` links to canonical content and the schedule; it has no copied lesson or assessment body.
- `myst build --site --strict`, `python scripts/check_landing_page.py`, targeted pytest, and `git diff --check` must pass.

---

### Task 1: Establish student-facing route indexes

**Files:**
- Create: `01-course-info/this-week.md`
- Create: `01-course-info/technology-submission.md`
- Create: `07-practice-labs/index.md`
- Create: `08-assessments/index.md`
- Test: `tests/test_course_navigation.py`

**Interfaces:**
- Consumes: dates in `01-course-info/schedule.md`, submission rules in `01-course-info/projects.md`, policies in `01-course-info/syllabus.md` and `01-course-info/grading.md`.
- Produces: four navigation targets that can be listed in `myst.yml`; each contains only canonical links and its stated boundary.

- [ ] **Step 1: Write the failing navigation-content test**

Create `tests/test_course_navigation.py` with a parametrized test that reads each new page and asserts its title plus link fragments: `this-week.md` must contain `schedule.md` and `projects.md`; `technology-submission.md` must contain `02-getting-started/index.md` and `projects.md`; `07-practice-labs/index.md` must contain `ungraded`; `08-assessments/index.md` must contain `projects.md`, `growth-reflections.md`, and `grading.md`.

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_course_navigation.py -q`
Expected: FAIL because the four canonical route pages do not exist.

- [ ] **Step 3: Write the four bounded route pages**

- `this-week.md`: a weekly launchpad. Link to Schedule as date authority, then to the P1 core route, Transit lecture, Projects, and Growth Reflections for the launch period. State that later entries will link—not duplicate—their canonical materials.
- `technology-submission.md`: five links in order—software setup, terminal, Git/Classroom50, project repository, clean-kernel verification. State that Projects owns submission requirements.
- `07-practice-labs/index.md`: define labs as ungraded and non-submission practice; say that none are published yet; prescribe goal, expected time, prerequisites, and `you are done when` for future labs.
- `08-assessments/index.md`: link Projects, Growth Reflections, Grading, and the two final-assessment syllabus anchors. State that each linked document remains authoritative.

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `pytest tests/test_course_navigation.py -q`
Expected: PASS with four parametrized cases.

- [ ] **Step 5: Commit**

Run: `git add 01-course-info/this-week.md 01-course-info/technology-submission.md 07-practice-labs/index.md 08-assessments/index.md tests/test_course_navigation.py && git commit -m "feat: add canonical course route indexes"`.

### Task 2: Cut the MyST navigation over to the approved architecture

**Files:**
- Modify: `myst.yml`
- Modify: `tests/test_course_navigation.py`

**Interfaces:**
- Consumes: Task 1’s four new routes and all existing course source paths.
- Produces: top-level navigation ordered `Course Info & Roadmap`, `Scientific Computing with Python`, `Readings`, `Lectures`, `Practice Labs`, `Assessments`, and `Tools & Workflow` after Home.

- [ ] **Step 1: Extend the failing navigation test**

Parse `myst.yml` with `yaml.safe_load`, collect `config["project"]["toc"][1:]` titles, and assert they equal the seven approved titles in the stated order.

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_course_navigation.py -k approved_top_level -q`
Expected: FAIL because the current TOC uses Course Roadmap, Getting Started, Numerical Modeling, and Data/Inference/Scientific ML as peers.

- [ ] **Step 3: Rewrite only the `project.toc` list in `myst.yml`**

- Course Info & Roadmap: syllabus, schedule, This Week, AI policy, and technology/submission route.
- Scientific Computing with Python: retain all three current parts and Chapter 1–12; remove Transit from Part I.
- Readings: retain current Numerical Modeling and Data/Inference/Scientific ML topic trees.
- Lectures: add only the existing Transit pilot as Block 1.
- Practice Labs: add the new index only.
- Assessments: add its index, then existing Projects, Growth Reflections, and Grading pages.
- Tools & Workflow: add the seven current Getting Started pages.

Keep all exact existing file paths unchanged. Use TOC labels rather than editing source titles for shorter sidebar copy.

- [ ] **Step 4: Run navigation test and MyST build**

Run: `pytest tests/test_course_navigation.py -q && myst build --site --strict`
Expected: all navigation assertions PASS and MyST completes successfully.

- [ ] **Step 5: Commit**

Run: `git add myst.yml tests/test_course_navigation.py && git commit -m "refactor: reorganize course site navigation"`.

### Task 3: Make the Python textbook chapter convention coherent

**Files:**
- Modify: `03-python/index.md`, `03-python/01-python-environment.md` through `03-python/06-oop-fundamentals.md`
- Modify: `04-scientific-computing/07-numpy-fundamentals.md` through `04-scientific-computing/12-data-acquisition-cleaning.md`
- Modify: `tests/test_course_navigation.py`

**Interfaces:**
- Consumes: the sequential twelve-part textbook arrangement in `myst.yml`.
- Produces: front-matter titles beginning `Chapter N:` for all twelve Python textbook pages, while preserving source paths and anchors.

- [ ] **Step 1: Add a failing chapter-title test**

Map the twelve existing files to chapter numbers 1–12 and assert their front matter contains `title: "Chapter N:`.

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_course_navigation.py -k chapter_title -q`
Expected: FAIL for pages whose title currently omits a chapter number.

- [ ] **Step 3: Normalize the twelve front-matter titles and index wording**

Retain the established Chapter 1–11 authorial titles and add the missing
`Chapter 12:` prefix to `Data Acquisition, Cleaning, and Exploratory Analysis`.
Keep the existing “Chapter-by-Chapter Guide” and sequential prose in
`03-python/index.md`. Do not label separate Readings or Lectures as chapters.

- [ ] **Step 4: Run tests, math checks, and strict build**

Run: `pytest tests/test_course_navigation.py -q && python scripts/check_math_rendering.py && myst build --site --strict`
Expected: all checks PASS with no math, link, or TOC failure.

- [ ] **Step 5: Commit**

Run: `git add 03-python 04-scientific-computing tests/test_course_navigation.py && git commit -m "docs: normalize Python textbook chapter labels"`.

### Task 4: Qualify the published navigation experience

**Files:**
- Modify: `tests/test_course_navigation.py` only if visual inspection exposes a durable route omission.
- Verify: `_build/html/`

**Interfaces:**
- Consumes: Tasks 1–3 and the existing MyST build.
- Produces: an evidence-backed navigation release for the first three project blocks.

- [ ] **Step 1: Inspect canonical entry points**

Build with `myst build --site --strict`, then inspect Home, This Week, textbook, Transit lecture, Practice Labs, Assessments, and Tools & Workflow. Confirm each has one intelligible role; confirm P1–P3 reading links resolve; confirm no sidebar item is blank or a generic placeholder.

- [ ] **Step 2: Run automated gates**

Run: `pytest -q && python scripts/check_landing_page.py && python scripts/check_math_rendering.py && python scripts/check_interactive_lectures.py && git diff --check`.

Expected: every command exits 0.

- [ ] **Step 3: Commit only an assertion justified by an observed failure**

Run: `git add tests/test_course_navigation.py && git commit -m "test: cover course navigation contract"` only if Step 1 reveals and resolves a route omission.

- [ ] **Step 4: Record completion evidence**

In the handoff, name commit IDs and verification commands. Separate this IA cutover from remaining authored content: lecture outlines/pages and P1–P3 project materials are drafted next as substantive course content, not fabricated as generic placeholders.
