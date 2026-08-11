---
title: "Course Schedule"
subtitle: "COMP 521 | Fall 2026"
---

# Course Schedule

Sixteen weeks: six two-week projects, then a four-week final project.
Class meets **Tue/Thu 5:30–6:45 pm in LSN 134**.

:::{important} How to read this page
**Deadlines are firm. Topics are not.**

Project due dates are fixed — plan around them. Topics and readings are listed
**by week, not by day**, because each session mixes instruction with working
time and the balance shifts depending on where we actually are. If we need an
extra session on a hard idea, we take it.

Projects are assigned **Tuesdays** and due **Mondays at 11:59 pm PT**, so you
arrive at Tuesday class having submitted rather than finishing in the room.

Complete a week's readings by the start of that week. When a new project block
begins, its readings are for **Thursday** — you will have been finishing the
previous project Monday night. Readings marked *(to be posted)* are being
written and will appear before their week.
:::

:::{note} At a glance
| | |
|---|---|
| First class | Tue **Aug 25** |
| Office hours | Thu **4:00–5:00 pm** (and by appointment) |
| Add/drop deadline | Fri **Sep 4** |
| Labor Day — campus closed | Mon **Sep 7** |
| Late withdrawal deadline | Sun **Nov 1** |
| No class — Thanksgiving | Thu **Nov 26** |
| Final presentations | Tue **Dec 8**, Thu **Dec 10** |
| Last class | Thu **Dec 10** |
| Final report + Synthesis due | Final exam slot, **Dec 12–18** *(TBA)* |
:::

## Block 1 · Project 1 — Scientific Programming & EDA

*Assigned Tue Aug 25 · Due Fri Sep 4*

### Week 1 — Aug 25, 27 · Foundations and setup

**Readings**
- [Command line intro](../02-getting-started/01-cli-intro.md)
- [Software setup](../02-getting-started/02-software-setup.md)
- [Git intro](../02-getting-started/03-git-intro.md)
- [Python environment](../03-python/01-python-environment.md)
- [Python as a calculator](../03-python/02-python-calculator.md)
- [Control flow and logic](../03-python/03-python-control-flow.md)

**Topics** — environment setup, Git/GitHub workflow, Python syntax, floating
point, control flow, the five algorithmic patterns

**Due** — **Project 0** (bootcamp), Mon **Aug 31**

### Week 2 — Sep 1, 3 · Data structures, OOP, and arrays

**Readings**
- [Data structures](../03-python/04-python-data-structures.md)
- [Functions and modules](../03-python/05-python-functions-modules.md)
- [OOP fundamentals](../03-python/06-oop-fundamentals.md)
- [NumPy fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)

**Topics** — classes for scientific data, arrays vs. lists, vectorization;
building a `ScientificData` class; exploratory analysis of the Gaia DR3 sample

**Due** — **Project 1** + **Growth Memo 1** (baseline), Fri **Sep 4**

:::{note} Why Project 1 is due Friday
Every other project is due Monday. Project 1 is the exception because Mon Sep 7
is **Labor Day** — the campus is closed and some of you will be travelling.
:::

## Block 2 · Project 2 — Numerical Integration

*Assigned Tue Sep 8 · Due Mon Sep 21*

### Week 3 — Sep 8, 10 · Discrete computing and visualization

**Readings**
- [Matplotlib fundamentals](../04-scientific-computing/08-matplotlib-fundamentals.md)
- [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md)
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
Research Memo, Mon **Sep 21**

## Block 3 · Project 3 — Root Finding & Data Acquisition

*Assigned Tue Sep 22 · Due Mon Oct 5*

### Week 5 — Sep 22, 24 · Root finding

**Readings**
- [Root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — bisection, Newton–Raphson, secant; convergence rates; failure modes
and bracketing; habitable-zone calculation

### Week 6 — Sep 29, Oct 1 · Real data acquisition

**Readings** — *Data acquisition and cleaning* (to be posted)

**Topics** — APIs, Lightkurve, quality flags, missing data, outlier
identification; downloading and cleaning real Kepler light curves

**Due** — **Project 3** (root-finding library + Kepler data pipeline) +
Research Memo, Mon **Oct 5**

## Block 4 · Project 4 — Linear Algebra & Statistical Methods

*Assigned Tue Oct 6 · Due Mon Oct 19*

### Week 7 — Oct 6, 8 · Linear systems

**Readings**
- [Core linear algebra](../06-linear-algebra-stats/00-linear-algebra/00a-linear-algebra-core-module.md)
- [Formula sheet](../06-linear-algebra-stats/00-linear-algebra/00c-linear-algebra-formula-sheet.md)

**Topics** — Gaussian elimination, LU decomposition, conditioning, least squares
and the normal equations

### Week 8 — Oct 13, 15 · Statistics and model fitting

**Readings**
- [Linear algebra for statistics](../06-linear-algebra-stats/00-linear-algebra/00b-linear-algebra-stats-module.md)
- [Probability foundations](../06-linear-algebra-stats/01-probability/01-mod1-part1-foundations.md)
- [Statistical tools](../06-linear-algebra-stats/01-probability/02-mod1-part2-statistical-tools.md)
- [Moments](../06-linear-algebra-stats/01-probability/03-mod1-part3-moments.md)

**Topics** — hypothesis testing, chi-squared, goodness of fit; fitting the
transit model to real Kepler data

**Due** — **Project 4** + Research Memo + **Growth Memo 2** (mid-semester),
Mon **Oct 19**

:::{tip} Check your standing before Nov 1
Growth Memo 2 is due Oct 19 and returned the following week — before the
**Nov 1 late withdrawal deadline**. If you are struggling, that feedback is
meant to reach you while you still have options. Come talk to me.
:::

## Block 5 · Project 5 — ODEs & Time Series

*Assigned Tue Oct 20 · Due Mon Nov 2*

### Week 9 — Oct 20, 22 · ODE solvers

**Readings**
- [Euler methods](../05-numerical-methods/03-odes/01-module3-part1-euler.md)
- [Runge–Kutta](../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md)
- [Symplectic integrators](../05-numerical-methods/03-odes/03-module3-part3-symplectic.md)
- [Stability](../05-numerical-methods/03-odes/04-module3-part4-stability.md)

**Topics** — Euler, RK2, RK4; local vs. global error; stability regions; energy
conservation and why symplectic methods matter

### Week 10 — Oct 27, 29 · Time series

**Readings**
- [Sampling](../06-linear-algebra-stats/01-probability/04-mod1-part4-sampling.md)
- *Time series analysis* (to be posted)

**Topics** — autocorrelation, periodograms, detrending, period recovery

**Due** — **Project 5** (ODE solver library + time series analysis) +
Research Memo, Mon **Nov 2**

## Block 6 · Project 6 — Machine Learning Foundations

*Assigned Tue Nov 3 · Due Mon Nov 16*

### Week 11 — Nov 3, 5 · Supervised learning

**Readings**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- *Supervised learning from scratch* (to be posted)

**Topics** — k-NN, decision trees, train/test splits, cross-validation;
classifying stellar types

### Week 12 — Nov 10, 12 · Unsupervised learning and evaluation

**Readings** — *Clustering, PCA, and model evaluation* (to be posted)

**Topics** — k-means, hierarchical clustering, PCA; ROC curves, confusion
matrices, feature importance; clustering the Gaia sample from Project 1 and
comparing against scikit-learn

**Due** — **Project 6** + Research Memo, Mon **Nov 16**

## Block 7 · Final Project

*Assigned Tue Nov 17 · Presentations Dec 8 & 10 · Report due in the finals slot*

### Week 13 — Nov 17, 19 · Inference and project scoping

**Readings**
- [Measurement](../06-linear-algebra-stats/02-inference/01-mod5-part1-measurement.md)
- [Inferential thinking](../06-linear-algebra-stats/02-inference/02-mod5-part2-inference.md)

**Topics** — measurement uncertainty, inference; scoping your final project

**Due** — final project proposal (one page), Thu **Nov 19**

### Week 14 — Nov 24 · Implementation

:::{warning} No class Thursday Nov 26 — Thanksgiving
This week has one meeting instead of two. Plan your project work accordingly;
the following week has no cushion built in.
:::

Working sessions with individual check-ins.

### Week 15 — Dec 1, 3 · Implementation

Working sessions with individual check-ins. Bring results to show, not just code.

### Week 16 — Dec 8, 10 · Presentations

**Due** — in-class presentation (Tue **Dec 8** or Thu **Dec 10**)

**Due** — final report + **Growth Synthesis**, in our assigned final exam slot,
**Dec 12–18** *(exact slot TBA)*

:::{note} Final project options
1. **Exoplanet discovery pipeline** — apply your full toolkit to unseen Kepler data
2. **Custom scientific data analysis** — a dataset from your own field
3. **Algorithm comparison study** — your implementations vs. libraries, with
   complexity analysis
:::
