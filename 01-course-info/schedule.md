---
title: "Course Schedule"
subtitle: "COMP 521 | Fall 2026"
---

# Course Schedule

Sixteen weeks: six two-week projects (in rotating pairs), then a four-week
solo final project.
Class meets **Tue/Thu 5:30–6:45 pm in LSN 134**.

:::{important} How to read this page
**Deadlines are firm. Topics are not.**

Project due dates are fixed — plan around them. Topics and readings are listed
**by week, not by day**, because each session mixes instruction with working
time and the balance shifts depending on where we actually are. If we need an
extra session on a hard idea, we take it.

Projects are assigned **Tuesdays** and due **Mondays at 11:59 pm PT**, so you
arrive at Tuesday class having submitted rather than finishing in the room.

Come to class prepared to discuss and use the assigned readings. The schedule
and Canvas announcements will identify what to prepare. Readings marked *(to be
posted)* are being written and will appear before they are needed.
:::

:::{note} At a glance
| | |
|---|---|
| First class | Tue **Aug 25** |
| Office hours | Thu **4:00–5:00 pm** (and by appointment) |
| Add/drop deadline | Fri **Sep 4** |
| Labor Day — campus closed | Mon **Sep 7** |
| No class — Thanksgiving | Thu **Nov 26** |
| Final presentations | Thu **Dec 10** |
| Last class | Thu **Dec 10** |
| Growth Synthesis due | Mon **Dec 14** (start of finals week) |
| Final report due | Thu **Dec 17**, 11:59 pm PT |
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

**Due** — **P1 Technical Readiness Check** in your Project 1 repository, before
class Thu **Aug 27** · **Growth Memo 1** (baseline), Mon **Aug 31**

### Week 2 — Sep 1, 3 · Data structures, functions, and arrays

**Readings**
- [Part I guide](../03-python/index.md#how-to-use-this-part), then [Chapter 4](../03-python/04-python-data-structures.md) and [Chapter 5](../03-python/05-python-functions-modules.md): basic data structures, mutability, and function contracts
- [NumPy fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)
- [Matplotlib fundamentals](../04-scientific-computing/08-matplotlib-fundamentals.md)

**Topics** — arrays vs. lists, vectorization, plotting; log and inverted axes;
functions in P1 notebooks; modules from Project 2 onward. OOP is reference
material for now and returns when a later project needs it.

**Due** — **Project 1** + **analysis notebook** + Discussion, Tue **Sep 8**

:::{note} Why Project 1 is due Tuesday
Every other project is due Monday. Project 1 is the exception because Mon Sep 7
is **Labor Day** — campus is closed and some of you will be travelling.

You get the long weekend, and the deadline is **11:59 pm Tuesday**, so you have
the whole day after class as well. From Project 2 on, deadlines are Mondays.
:::

## Block 2 · Project 2 — Numerical Integration

*Assigned Tue Sep 8 · Due Mon Sep 21*

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

**Due** — **Project 2** (integration library + exoplanet transit model) +
notebook Discussion, Mon **Sep 21**

## Block 3 · Project 3 — Root Finding & Stellar Inference

*Assigned Tue Sep 22 · Due Mon Oct 5*

### Week 5 — Sep 22, 24 · Root finding

**Readings**
- [Root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — bisection, Newton–Raphson, secant; convergence rates; failure modes
and bracketing; Wien's law and habitable-zone calculation

### Week 6 — Sep 29, Oct 1 · Kepler orbits and stellar inference

**Readings**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — Kepler's equation, orbital geometry, root-finding contact points;
`Star` objects and habitable zones for the 15-star P1 sample

**Due** — **Project 3** (root-finding library + stellar-inference notebook) +
notebook Discussion, Mon **Oct 5**

## Block 4 · Project 4 — ODE Methods & Exoplanet Interiors

*Assigned Tue Oct 6 · Due Mon Oct 19*

### Week 7 — Oct 6, 8 · ODE solvers

**Readings**
- [Euler methods](../05-numerical-methods/03-odes/01-module3-part1-euler.md)
- [Runge–Kutta](../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md)

**Topics** — Euler, RK2, RK4; local and global error; order verification

### Week 8 — Oct 13, 15 · Shooting and planetary interiors

**Readings**
- [Stability](../05-numerical-methods/03-odes/04-module3-part4-stability.md)
- [Module synthesis](../05-numerical-methods/03-odes/05-mod3-synthesis.md)

**Topics** — hydrostatic equilibrium, equations of state, locating a moving
surface, shooting, and diagnosing observed order loss

**Due** — **Project 4** (ODE library + exoplanet-interior notebook) + notebook
Discussion + **Growth Memo 2**
(mid-semester), Mon **Oct 19**

## Block 5 · Project 5 — Real Data & Model Fitting

*Assigned Tue Oct 20 · Due Mon Nov 2*

### Week 9 — Oct 20, 22 · Real data acquisition and cleaning

**Readings**
- [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md)
- [Data acquisition, cleaning, and exploratory analysis](../04-scientific-computing/12-data-acquisition-cleaning.md)

**Topics** — archives and APIs, Lightkurve, quality flags, gaps, outliers, and
exploratory analysis of real Kepler light curves

### Week 10 — Oct 27, 29 · Model fitting and uncertainty

**Readings**
- [Core linear algebra](../06-linear-algebra-stats/00-linear-algebra/00a-linear-algebra-core-module.md)
- [Linear algebra for statistics](../06-linear-algebra-stats/00-linear-algebra/00b-linear-algebra-stats-module.md)
- [Probability foundations](../06-linear-algebra-stats/01-probability/01-mod1-part1-foundations.md)
- [Statistical tools](../06-linear-algebra-stats/01-probability/02-mod1-part2-statistical-tools.md)
- [Model fitting and uncertainty](../06-linear-algebra-stats/03-model-fitting/00-overview.md)

**Topics** — design matrices, normal equations, conditioning, $\chi^2$, transit
model fitting, and bootstrap uncertainty

**Due** — **Project 5** (real Kepler photometry + transit-model fit) +
notebook Discussion, Mon **Nov 2**

## Block 6 · Project 6 — Machine Learning & Scientific Classification

*Assigned Tue Nov 3 · Due Mon Nov 16*

### Week 11 — Nov 3, 5 · Supervised learning

**Readings**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- [Supervised learning from scratch](../06-linear-algebra-stats/04-scientific-ml/01-supervised-learning.md)

**Topics** — k-NN, decision trees, train/test splits, cross-validation;
classifying stellar types; final-project pathways and examples

**Assigned** — **Final-Project Proposal Pitch**, Tue **Nov 3**; due Thu **Nov
19**, in class

### Week 12 — Nov 10, 12 · Unsupervised learning and evaluation

**Readings** — [Clustering, PCA, and model evaluation](../06-linear-algebra-stats/04-scientific-ml/02-unsupervised-learning.md)

**Topics** — k-means, hierarchical clustering, PCA; ROC curves, confusion
matrices, feature importance; clustering the Gaia sample from Project 1 and
comparing against scikit-learn

**Due** — **Project 6**, Mon **Nov 16**

## Block 7 · Final Project

*Assigned Tue Nov 17 · Solo · Presentations Thu Dec 10 · Report due Thu Dec 17*

### Week 13 — Nov 17, 19 · Inference and project scoping

**Readings**
- [Measurement](../06-linear-algebra-stats/02-inference/01-mod5-part1-measurement.md)
- [Inferential thinking](../06-linear-algebra-stats/02-inference/02-mod5-part2-inference.md)

**Topics** — measurement uncertainty, inference; final-project launch

**Due** — **Final-Project Proposal Pitch** (5 minutes + short slide deck), Thu
**Nov 19**, in class

### Week 14 — Nov 24 · Implementation

:::{warning} No class Thursday Nov 26 — Thanksgiving
This week has one meeting instead of two. Plan your project work accordingly;
the following week has no cushion built in.
:::

Working sessions with individual check-ins.

### Week 15 — Dec 1, 3 · Implementation

Working sessions with individual check-ins. Bring results to show, not just
code.

### Week 16 — Dec 8, 10 · Dress rehearsal and presentations

**Tue Dec 8** — dress rehearsal. Run your talk past me and your classmates; this
is the last chance to catch a figure nobody can read from the back of the room.

**Thu Dec 10** — **final presentations**, 10 minutes each (about 8 to present,
2 for questions). Last class meeting.

**Then:**

| Deliverable | Due |
|---|---|
| Growth Synthesis | Mon **Dec 14**, 11:59 pm PT |
| Final report + repository | Thu **Dec 17**, 11:59 pm PT |
