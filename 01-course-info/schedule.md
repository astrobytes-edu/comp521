---
title: "Course Schedule"
subtitle: "COMP 521 | Fall 2026"
---

# Week-by-Week Schedule

Fifteen weeks: six two-week projects, then a three-week final project.
Projects are due the **second Monday of their block at 11:59 PM PT**.

:::{important} How to use this page
Readings listed for a week should be completed **before** that week's lab.
Labs are working sessions for the current project — there are no separate lab
deliverables.
:::

## Block 1 · Project 1 — Scientific Programming & EDA

### Week 1 — Foundations and setup

**Readings**
- [Command line intro](../02-getting-started/01-cli-intro.md)
- [Software setup](../02-getting-started/02-software-setup.md)
- [Git intro](../02-getting-started/03-git-intro.md)
- [Python environment](../03-python/01-python-environment.md)
- [Python as a calculator](../03-python/02-python-calculator.md)
- [Control flow and logic](../03-python/03-python-control-flow.md)

**Topics** — environment, Git/GitHub workflow, Python syntax, floating point,
control flow, the five algorithmic patterns

**Due** — Project 0 (bootcamp), end of week

### Week 2 — Data structures, OOP, and arrays

**Readings**
- [Data structures](../03-python/04-python-data-structures.md)
- [Functions and modules](../03-python/05-python-functions-modules.md)
- [OOP fundamentals](../03-python/06-oop-fundamentals.md)
- [NumPy fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)

**Topics** — classes for scientific data, arrays vs. lists, vectorization

**Lab** — build a `ScientificData` class with statistics methods

**Due** — **Project 1** + Growth Memo

## Block 2 · Project 2 — Numerical Integration

### Week 3 — Discrete computing and visualization

**Readings**
- [Matplotlib fundamentals](../04-scientific-computing/08-matplotlib-fundamentals.md)
- [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md)
- [Finite differences](../05-numerical-methods/01-foundations/01-mod1-part1-finite-differences.md)
- [Numerical errors](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md)
- [Taylor series](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md)

**Topics** — discretization, truncation vs. round-off error, Taylor expansion
as the source of every method in this course

### Week 4 — Quadrature

**Readings**
- [Quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md)
- [Module synthesis](../05-numerical-methods/01-foundations/04-mod1-synthesis.md)

**Topics** — rectangle, trapezoid, Simpson's rule; adaptive quadrature; error
estimation and convergence order

**Lab** — implement the integration suite from scratch; verify convergence rates
against theory

**Due** — **Project 2** (integration library + exoplanet transit model) +
Research Memo + Growth Memo

## Block 3 · Project 3 — Root Finding & Data Acquisition

### Week 5 — Root finding

**Readings**
- [Root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
- [Robust computing](../04-scientific-computing/09-robust-computing.md)

**Topics** — bisection, Newton–Raphson, secant; convergence rates; failure modes
and bracketing

**Lab** — implement all three methods; habitable-zone calculation

### Week 6 — Real data acquisition

**Readings** — *Data acquisition and cleaning* (to be posted)

**Topics** — APIs, Lightkurve, quality flags, missing data, outlier
identification

**Lab** — download and clean real Kepler light curves

**Due** — **Project 3** (root-finding library + Kepler data pipeline) +
Research Memo + Growth Memo

## Block 4 · Project 4 — Linear Algebra & Statistical Methods

### Week 7 — Linear systems

**Readings**
- [Core linear algebra](../06-linear-algebra-stats/00-linear-algebra/00a-linear-algebra-core-module.md)
- [Formula sheet](../06-linear-algebra-stats/00-linear-algebra/00c-linear-algebra-formula-sheet.md)

**Topics** — Gaussian elimination, LU decomposition, conditioning, least squares
and the normal equations

### Week 8 — Statistics and model fitting

**Readings**
- [Linear algebra for statistics](../06-linear-algebra-stats/00-linear-algebra/00b-linear-algebra-stats-module.md)
- [Probability foundations](../06-linear-algebra-stats/01-probability/01-mod1-part1-foundations.md)
- [Statistical tools](../06-linear-algebra-stats/01-probability/02-mod1-part2-statistical-tools.md)
- [Moments](../06-linear-algebra-stats/01-probability/03-mod1-part3-moments.md)

**Topics** — hypothesis testing, chi-squared, goodness of fit

**Lab** — fit the transit model to real Kepler data

**Due** — **Project 4** + Research Memo + Growth Memo

## Block 5 · Project 5 — ODEs & Time Series

### Week 9 — ODE solvers

**Readings**
- [Euler methods](../05-numerical-methods/03-odes/01-module3-part1-euler.md)
- [Runge–Kutta](../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md)
- [Symplectic integrators](../05-numerical-methods/03-odes/03-module3-part3-symplectic.md)
- [Stability](../05-numerical-methods/03-odes/04-module3-part4-stability.md)

**Topics** — Euler, RK2, RK4; local vs. global error; stability regions;
energy conservation and why symplectic methods matter

### Week 10 — Time series

**Readings**
- [Sampling](../06-linear-algebra-stats/01-probability/04-mod1-part4-sampling.md)
- *Time series analysis* (to be posted)

**Topics** — autocorrelation, periodograms, detrending, period recovery

**Due** — **Project 5** (ODE solver library + time series analysis) +
Research Memo + Growth Memo

## Block 6 · Project 6 — Machine Learning Foundations

### Week 11 — Supervised learning

**Readings**
- [Advanced OOP](../04-scientific-computing/10-advanced-oop.md)
- *Supervised learning from scratch* (to be posted)

**Topics** — k-NN, decision trees, train/test splits, cross-validation

**Lab** — implement classifiers from scratch; classify stellar types

### Week 12 — Unsupervised learning and evaluation

**Readings** — *Clustering, PCA, and model evaluation* (to be posted)

**Topics** — k-means, hierarchical clustering, PCA; ROC curves, confusion
matrices, feature importance

**Lab** — cluster the Gaia DR3 dataset from Project 1; compare your
implementations against scikit-learn

**Due** — **Project 6** + Research Memo + Growth Memo

## Block 7 · Final Project

### Week 13 — Inference and project scoping

**Readings**
- [Measurement](../06-linear-algebra-stats/02-inference/01-mod5-part1-measurement.md)
- [Inferential thinking](../06-linear-algebra-stats/02-inference/02-mod5-part2-inference.md)

**Deliverable** — final project proposal (one page)

### Week 14 — Implementation

Full-week working sessions. Instructor check-ins during lab.

### Week 15 — Presentations and synthesis

**Due** — **Final project**, presentation, and Technical Growth Synthesis

:::{note} Final project options
1. **Exoplanet discovery pipeline** — apply your full toolkit to unseen Kepler data
2. **Custom scientific data analysis** — a dataset from your own field
3. **Algorithm comparison study** — your implementations vs. libraries, with
   complexity analysis
:::
