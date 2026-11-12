---
title: "Course Schedule"
subtitle: "COMP 521 | Fall 2026"
---

# Course Schedule

Sixteen weeks: five projects (in rotating pairs), two individual code review
presentations, and a collaborative [final project](../08-assessments/final-project.md).
Project dates are listed below.
Class meets **Tue/Thu 5:30–6:45 pm in LSN 134**.

:::{important} How to read this page
**Deadlines are firm. Topics are not.**

Project due dates are fixed — plan around them. Topics and readings are listed
**by week, not by day**, because each session mixes instruction with working
time and the balance shifts depending on where we actually are. If we need an
extra session on a hard idea, we take it.

Projects are typically assigned **Tuesdays** and due
**Wednesdays at 11:59 pm PT**. Use the specific dates below for each project.

Come to class prepared to discuss and use the assigned sections.
[This Week](this-week.md) separates preparation, reference, and optional
enrichment for the current week and retains links for earlier weeks. Chapter
links below also serve as reference routes; a link to a chapter does not mean
every deep dive or exercise is assigned. Readings marked *(in preparation)* are
not yet complete lessons; their assigned sections will be identified when ready.
:::

:::{note} At a glance
| | |
|---|---|
| First class | Tue **Aug 25** |
| Office hours | Thu **4:00–5:00 pm** (and by appointment) |
| Add/drop deadline | Fri **Sep 4** |
| Labor Day — campus closed | Mon **Sep 7** |
| Project 4 | Assigned Wed **Oct 14**; due Wed **Oct 28** |
| Scientific computing code reviews | Thu **Oct 22**, in class |
| Project 5 | Assigned Thu **Oct 29**; due Wed **Nov 18** |
| DS/ML code reviews | Thu **Nov 12**, in class |
| Final-project work and check-ins | Tue **Nov 24**, in class |
| No class — Thanksgiving | Thu **Nov 26** |
| Final presentations | Thu **Dec 10** |
| Last class | Thu **Dec 10** |
| Growth Synthesis due | Mon **Dec 14** (start of finals week) |
| Final slides + code due | Thu **Dec 17**, 11:59 pm PT |
:::

## Block 1 · Project 1 — Scientific Programming & the Transit Model

*Assigned Tue Aug 25 · Due Tue Sep 8*

### Week 1 — Aug 25, 27 · Foundations and setup

**Readings**
- [Command line intro](../02-getting-started/01-cli-intro.md)
- [Software setup](../02-getting-started/02-software-setup.md)
- [Git intro](../02-getting-started/03-git-intro.md)
- [Part I guide](../03-python/index.md#how-to-use-this-part), then [Chapter 1](../03-python/01-python-environment.md), [Chapter 2](../03-python/02-python-calculator.md), and [Chapter 3](../03-python/03-python-control-flow.md): environment and clean-kernel execution; arithmetic, variables, numerical comparison; pseudocode, conditionals, and loops

**Topics** — environment setup, Git/GitHub workflow, Python syntax, floating
point, control flow, the five algorithmic patterns

**Before class Thu Aug 27** — complete the laptop setup so that you can use
Python and Jupyter in class

**Due Fri Aug 28, 11:59 pm PT** — **Project 1 Repository Check** in the Project 1
repository you will link through Canvas; use the brief for its setup route

**Assigned** — **Growth Memo 1**, Tue **Aug 25**; due Mon **Aug 31**, 11:59 pm PT

### Week 2 — Sep 1, 3 · Data structures, functions, and arrays

**Readings**
- [Part I guide](../03-python/index.md#how-to-use-this-part), then [Chapter 4](../03-python/04-python-data-structures.md) and [Chapter 5](../03-python/05-python-functions-modules.md): basic data structures, mutability, and function contracts
- [NumPy fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)
- [Matplotlib fundamentals](../04-scientific-computing/08-matplotlib-fundamentals.md)

**Topics** — arrays vs. lists, vectorization, plotting; log and inverted axes;
functions in P1 notebooks; modules from Project 2 onward. OOP is reference
material for now and returns when a later project needs it.

**Due** — **Project 1** + **analysis notebook**, Tue **Sep 8**

:::{note} Why Project 1 is due Tuesday
Project 1 used a Tuesday deadline because Mon Sep 7 was **Labor Day**.
Its original deadline remains listed here for reference.

Later projects are typically due Wednesday; use each listed deadline.
:::

## Block 2 · Project 2 — Numerical Integration

*Assigned Tue Sep 8 · Due Wed Sep 23*

### Week 3 — Sep 8, 10 · Discrete computing and visualization

**Readings**
- [Finite differences](../05-numerical-methods/01-foundations/01-mod1-part1-finite-differences.md)
- [Numerical errors](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md)
- [Taylor series](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md)

**Topics** — discretization, truncation vs. round-off error, Taylor expansion as
the source of every method in this course

### Week 4 — Sep 15, 17 · Quadrature

**Readings**
- [Quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md)
- [Module synthesis](../05-numerical-methods/01-foundations/04-mod1-synthesis.md)

**Topics** — rectangle, trapezoid, Simpson's rule; adaptive quadrature; error
estimation and convergence order; verifying you achieve the expected order

**Due** — **Project 2** (integration library + exoplanet transit model +
analysis notebook), Wed **Sep 23**

## Block 3 · Project 3 — Root Finding & Stellar Inference

*Assigned Tue Sep 22 · Due Wed Oct 7*

### Week 5 — Sep 22, 24 · Root finding

**Preparation** — use the [Week 5 section-level route](this-week.md#week-5).

**Reference**
- [Root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — bisection, Newton–Raphson, secant; convergence rates; failure modes
and bracketing; Wien's law and habitable-zone calculation

### Week 6 — Sep 29, Oct 1 · Kepler orbits and stellar inference

**Preparation** — use the [Week 6 science and project route](this-week.md#week-6).

**Reference**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — Kepler's equation, orbital geometry, root-finding contact points;
`Star` objects and habitable zones for the 15-star P1 sample

**Due** — **Project 3** (root-finding library + stellar-inference notebook), Wed
**Oct 7**

## Block 4 · Project 4 — ODE Methods & Exoplanet Interiors

*Assigned Wed Oct 14 · Due Wed Oct 28*

### Week 7 — Oct 6, 8 · ODE solvers

Use the [ODE overview](../09-lectures/block-04-odes.md) for lecture and reading
links. The existing ODE readings remain under revision.

**Reference**
- [Euler methods](../05-numerical-methods/03-odes/01-module3-part1-euler.md)
- [Runge–Kutta](../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md)

**Topics** — Euler, explicit midpoint RK2, RK4; local and global error; order
verification

**Assigned** — **Growth Memo 2**, Tue **Oct 6**; due Mon **Oct 19**, 11:59 pm PT

### Week 8 — Oct 13, 15 · ODE validation and planetary interiors

**Reference**
- [Stability](../05-numerical-methods/03-odes/04-module3-part4-stability.md)
- [Module synthesis](../05-numerical-methods/03-odes/05-mod3-synthesis.md)
- [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md) *(CSV reading and row selection)*

**Topics** — SHO convergence against an exact solution; hydrostatic equilibrium,
equations of state, and the constant-density analytic planet check

**Thu Oct 15** — Pandas introduction: read a saved NASA exoplanet CSV, select
columns and rows with a boolean mask, and plot mass/radius estimates with
uncertainties. Broader data analysis follows in Project 5.

**Assigned** — [**Project 4**](../08-assessments/projects/project-4.md), Wed **Oct 14**; due Wed **Oct 28**, 11:59 pm PT

**Due Mon Oct 19, 11:59 pm PT** — **Growth Memo 2** (mid-semester).

### Week 9 — Oct 20, 22 · Surface finding and mass–radius curves

**Topics** — locating the zero-pressure surface by refining the final RK4 step;
planetary profiles; a central-pressure sweep and comparison with the published
mass–radius relation. Project 4 is self-contained.

**In class** — [Scientific computing code reviews](../08-assessments/code-review-presentations.md),
Thu **Oct 22**

## Block 5 · Project 5 — Real Data & Model Fitting

*Assigned Thu Oct 29 · Due Wed Nov 18*

### Week 10 — Oct 27, 29 · Project 4 completion and real data

**Preparation and focused reference** — use the
[Week 10 route](this-week.md#week-10) for selected sections on variance,
covariance, dot products, projections, and Pandas table inspection. These are
bounded reference sections, not whole-chapter assignments.

**Tuesday, October 27** — why scientific Data Science starts with a model of
measurements: a primer on probability and linear algebra, connected through a
scientific example. Review random variables, distributions, expectations,
variance, covariance, vectors, data matrices, dot products, and projections.
Include Project 4 questions and completion time.

**Thursday, October 29** — begin the methods: inspect data provenance, units,
and missing values, then connect a first model fit to residuals and uncertainty
weights. Introduce the real Kepler photometry workflow, including Lightkurve,
quality flags, and gaps, for Project 5.

[Data acquisition, cleaning, and exploratory analysis](../04-scientific-computing/12-data-acquisition-cleaning.md)
remains an in-development scope note. The model-fitting reading is also in
preparation; completed assigned sections will be identified when ready.

**Due Wed Oct 28, 11:59 pm PT** — **Project 4** (ODE library +
exoplanet-interior notebook).

**Assigned** — **Project 5**, Thu **Oct 29**; due Wed **Nov 18**, 11:59 pm PT

### Week 11 — Nov 3, 5 · Data preparation, fitting, and uncertainty

**Readings**
- [Core linear algebra](../06-linear-algebra-stats/00-linear-algebra/00a-linear-algebra-core-module.md)
- [Linear algebra for statistics](../06-linear-algebra-stats/00-linear-algebra/00b-linear-algebra-stats-module.md)
- [Probability foundations](../06-linear-algebra-stats/01-probability/01-mod1-part1-foundations.md)
- [Statistical tools](../06-linear-algebra-stats/01-probability/02-mod1-part2-statistical-tools.md)
- [Model fitting and uncertainty](../06-linear-algebra-stats/03-model-fitting/00-overview.md) *(in preparation)*

**Topics** — data preparation, design matrices, normal equations, conditioning,
$\chi^2$, transit-model fitting, and bootstrap uncertainty; final-project
pathways and examples

**Final-project preparation** — begin exploring topics and connections. We will
return to the project during in-class work and check-ins.

## Block 6 · Machine Learning & Code Review

### Week 12 — Nov 10, 12 · Machine-learning introduction and evaluation

**Reference**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- [Supervised learning from scratch](../06-linear-algebra-stats/04-scientific-ml/01-supervised-learning.md) *(in preparation)*
- [Clustering, PCA, and model evaluation](../06-linear-algebra-stats/04-scientific-ml/02-unsupervised-learning.md) *(in preparation)*

**Topics** — a focused introduction to classification and clustering; train/test
splits, cross-validation, and evaluation metrics; Project 5 working time.
Relevant ML methods can return during final-project check-ins. There is no
separate Project 6 assignment.

**In class** — [DS/ML code reviews](../08-assessments/code-review-presentations.md),
Thu **Nov 12**

## Block 7 · Final Project

*Assigned Tue Nov 17 · Group · Presentation Thu Dec 10 · Slides + code due Thu Dec 17*

See the [Final Project brief](../08-assessments/final-project.md) for the group
format, individual topics, and shared computation.

### Week 13 — Nov 17, 19 · Inference and project scoping

**Readings**
- [Measurement](../06-linear-algebra-stats/02-inference/01-mod5-part1-measurement.md)
- [Inferential thinking](../06-linear-algebra-stats/02-inference/02-mod5-part2-inference.md)

**Topics** — measurement uncertainty, inference; final-project launch and
scoping. The final project launches Tue **Nov 17**, while Project 5 is being
completed.

**Due Wed Nov 18, 11:59 pm PT** — **Project 5** (real Kepler photometry +
transit-model fit + analysis notebook).

**Assigned** — **Growth Synthesis**, Tue **Nov 17**; due Mon **Dec 14**, 11:59 pm PT

### Week 14 — Nov 24 · Project work and discussion

:::{warning} No class Thursday Nov 26 — Thanksgiving
This week has one meeting instead of two. Plan your project work accordingly;
the following week has no cushion built in.
:::

In-class project work, discussion, and check-ins. Preparation and ongoing
project development contribute 5% of the course grade; there is no separate
proposal-pitch submission.

### Week 15 — Dec 1, 3 · Implementation

Working sessions with individual check-ins. Bring results to show, not just
code.

### Week 16 — Dec 8, 10 · Dress rehearsal and presentations

**Tue Dec 8** — dress rehearsal. Run your talk past me and your classmates; this
is the last chance to catch a figure nobody can read from the back of the room.

**Thu Dec 10** — **final group presentation**, roughly 15 minutes per student
plus 5 minutes together for the shared question and Python example, followed
by discussion. Last class meeting.

**Then:**

| Deliverable | Due |
|---|---|
| Growth Synthesis | Mon **Dec 14**, 11:59 pm PT |
| Final shared slides + runnable code | Thu **Dec 17**, 11:59 pm PT |
