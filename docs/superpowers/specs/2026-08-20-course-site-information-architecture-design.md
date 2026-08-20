# COMP 521 course-site information architecture

## Status and purpose

**Status:** Approved design; intentionally evolvable.

COMP 521 needs a site that serves two different but compatible student needs:

1. find the correct item for this week; and
2. return later to a lecture, reading, lab, policy, or assessment without
   reconstructing the semester's chronology.

The site therefore has canonical libraries for each material type and a
parallel, lightweight weekly route. A weekly page links to canonical material;
it never becomes a second copy of it.

The course's instructional throughline is: **build methods, test their limits,
and use them on real data.** This structure must make that path legible while
allowing class time to remain responsive to student questions and project pace.

## Decisions

### 1. Primary navigation is type-based

The top-level navigation is:

```text
Home
Course Info & Roadmap
Scientific Computing with Python
Readings
Lectures
Practice Labs
Assessments
Tools & Workflow
```

Home remains the entry point. The first top-level branch is Course Info &
Roadmap. The textbook, readings, lectures, labs, assessments, and reusable
workflow material each have an independent, durable home.

### 2. `This Week` is a parallel route, not a content bucket

`This Week` is a new page or small sequence of weekly pages under Course Info
& Roadmap. For each active week it links to:

- preparation or bounded reading;
- the canonical lecture page or pages;
- an optional practice lab;
- the current project or assessment action; and
- due dates already established in the course schedule.

It contains no duplicate lecture prose, assignment instructions, or reading
content. Students can reach the same material through its canonical library or
through `This Week`.

### 3. A lecture page is the canonical in-class artifact

Each class meeting receives one complete, scrollable, scene-based lecture page.
The default planning envelope is 75 minutes, but pages are modular enough to
shorten for discussion, project work, or a focused mini-lecture. The page serves
live instruction, later review, accessibility, and absence recovery.

A typical lecture contains 5–7 scenes:

1. observable and motivating question;
2. concise conceptual model;
3. prediction pause and open discussion;
4. direct evidence, calculation, or embedded interactive model;
5. explanation and explicit assumptions;
6. transfer to students' own notebook or project; and
7. optional synthesis checkpoint.

Panel/Pyodide embeds are used only where direct manipulation clarifies a
scientific relationship. They are not decorative and do not replace explanation
or a visible static fallback. Polling platforms and synchronized classroom
controls are out of scope for v1: the instructor asks questions directly in the
small class, with optional private browser-local writing support.

### 4. Practice Labs are distinct from Assessments

Practice Labs are ungraded, voluntary or instructor-directed activities. Each
lab page states a goal, expected time, prerequisite, and a clear `you are done
when` criterion. They do not masquerade as projects or create a submission
burden.

Assessments collects graded and submission-bearing work: Projects, Growth
Reflections, the final-project proposal pitch, the final project, grading
criteria, and scholarly engagement expectations.

### 5. JupyterLite is not a default lecture surface

The course-built xeus/JupyterLite environment may remain available for future
notebook-centered work, but it is not the primary interface for ordinary
lectures. The Transit pilot demonstrated that a browser IDE adds load time and
an unnecessary change of context during a live explanation. Use short visible
code excerpts in lectures and require durable, clean-kernel work in the actual
project notebook.

## Proposed canonical table of contents

```text
Home

Course Info & Roadmap
├── Syllabus                                      [existing]
├── Course Schedule                               [existing]
├── This Week                                     [new]
├── AI Use & Growth Mindset Policy                [existing]
├── Course Technology & Submission Path           [new concise orientation]
└── Getting Help / Office Hours                    [new only if split from syllabus]

Scientific Computing with Python
├── Part I · Programming for Scientific Work
│   ├── Overview                                  [existing]
│   ├── Ch. 1 · Computational Environments & Scientific Workflows
│   ├── Ch. 2 · Python as Your Scientific Calculator
│   ├── Ch. 3 · Control Flow & Logic
│   ├── Ch. 4 · Data Structures
│   ├── Ch. 5 · Functions & Modules
│   ├── Ch. 6 · OOP Fundamentals
│   └── Synthesis                                 [all existing]
├── Part II · The Scientific Python Toolkit
│   ├── Overview
│   ├── NumPy Fundamentals
│   ├── Matplotlib Fundamentals
│   ├── Robust Computing
│   └── Advanced OOP                              [all existing]
└── Part III · Real Data Workflows
    ├── Overview
    ├── Pandas Fundamentals
    └── Data Acquisition, Cleaning & Exploratory Analysis

Readings
├── Numerical Modeling
│   ├── Foundations of Discrete Computing          [existing module]
│   ├── Root Finding & Quadrature                  [existing module]
│   └── ODE Methods & Conservation                 [existing module]
└── Data, Inference & Scientific ML
    ├── Linear Algebra for Modeling                [existing module]
    ├── Probability & Sampling                     [existing module]
    ├── Statistical Inference                      [existing module]
    ├── Model Fitting & Uncertainty                [existing module]
    └── Scientific Machine Learning                [existing module]

Lectures
├── Lecture Library                                [new index]
├── Block 1 · Scientific Programming & Transit Model
│   └── Interactive Lecture: How a Transit Dims a Star [existing pilot]
├── Block 2 · Numerical Integration                [future lecture pages]
├── Block 3 · Root Finding & Stellar Inference     [future lecture pages]
├── Block 4 · ODE Methods & Exoplanet Interiors    [future lecture pages]
├── Block 5 · Real Data & Model Fitting            [future lecture pages]
├── Block 6 · ML & Scientific Classification       [future lecture pages]
└── Block 7 · Final Project                        [future workshop pages]

Practice Labs
└── Practice Labs                                  [new index; no standalone labs yet]

Assessments
├── Assessment Overview                            [new]
├── Projects
│   ├── Before P1 · Technical Readiness Check
│   └── Projects 1–6 sequence                      [existing Projects page]
├── Growth Reflections                             [existing]
├── Final-Project Proposal Pitch                   [new; syllabus content exists]
├── Final Project                                  [new; syllabus content exists]
└── Grading & Scholarly Engagement                 [existing Grading page + syllabus]

Tools & Workflow
├── Getting Started                                [existing index]
├── Command Line                                   [existing]
├── Software Setup                                 [existing]
├── Git & Classroom50                              [existing]
├── Scientific Software Guide                      [existing]
├── Scientific Software Workflow Checklist         [existing]
└── Markdown for Analysis Notebooks                [existing]
```

## Inventory facts and placement rules

- The current `myst.yml` already contains the full Scientific Computing with
  Python textbook as three parts. It remains intact as its own top-level branch.
- The current Numerical Modeling and Data/Inference/Scientific ML branches move
  together beneath the top-level `Readings` branch. Their existing internal
  module structure remains intact.
- The current Transit Depth page is a lecture pilot, not a textbook chapter. It
  moves from the textbook branch to `Lectures`.
- No standalone practice-lab pages currently exist. The Practice Labs branch is
  introduced only as an empty index until a real activity merits a page.
- The existing Projects page covers readiness and the Project 1–6 sequence. The
  current syllabus covers the final-project proposal pitch and final project,
  but neither currently has a dedicated page.
- Current course policies and assessment criteria are distributed across the
  syllabus, AI policy, grading, projects, and growth-reflections pages. The
  restructuring must preserve their existing authority rather than silently
  duplicate or rewrite them.

## Authoring and navigation rules

1. Every item has one canonical source page and one canonical location in the
   primary navigation.
2. `This Week` may link to any canonical page but may not duplicate its body.
3. A lecture page belongs in Lectures even if it draws directly on a textbook
   chapter or is associated with a project block.
4. A practice activity becomes a Practice Lab only when it has a bounded goal
   and completion condition; otherwise it remains an activity within its
   lecture or reading.
5. A page belongs in Assessments only when it governs a grade, deliverable,
   submission path, or assessment criterion.
6. The source of truth for dates remains Course Schedule and the Syllabus;
   `This Week` links to those dates rather than retyping them.
7. New page types begin with an index page and a small number of real routes;
   placeholder lecture, lab, or assessment pages are not published merely to
   fill an outline.

## Change management

This is a living architecture, not a freeze. Changes are expected as the first
lecture and lab pages reveal what students actually need. A proposed change
should state:

- the student problem it solves;
- the canonical page home affected;
- whether an existing route moves, redirects, or remains as a compatibility
  link; and
- the corresponding `This Week` link change, if any.

The structure should be revised when evidence shows that students cannot find
the right material, a library label has become misleading, or a new activity
has become substantial enough to deserve a standalone page. It should not be
reorganized merely for visual novelty.

## Verification criteria for the future implementation

- Every existing page remains reachable from one canonical location.
- The Transit lecture appears only under Lectures, while the relevant textbook
  and reading pages remain independently reachable.
- Every `This Week` link targets a canonical page and has no duplicate body.
- No Practice Lab is represented as graded work.
- Existing syllabus deadlines, policy links, project links, and handbook routes
  continue to resolve after the TOC move.
- MyST builds without orphaned TOC entries or broken internal links.
