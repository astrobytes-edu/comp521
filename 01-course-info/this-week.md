---
title: "This Week"
subtitle: "COMP 521 | September 8–10, 2026"
---

# This Week

## Week 3 · Numerical approximation and integration

This week connects Taylor approximation and floating-point error to numerical
integration. Next week continues with adaptive quadrature and a conceptual
Monte Carlo introduction in Lecture 7, then introduces root finding in Lecture 8.
Both meetings include time for labs and Project 2 work.

## Required readings

### Foundations · Lecture 5

- [Finite differences](../05-numerical-methods/01-foundations/01-mod1-part1-finite-differences.md): how a finite calculation approximates a derivative.
- [Numerical errors](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md): representation, rounding, truncation, absolute and relative error, and `atol`/`rtol`.
- [Taylor series](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md): local polynomials, remainders, and error order.

### Quadrature and implementation · prepare for Lecture 6

Read the following sections of [Quadrature — Discrete Sums, Error, and Adaptation](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md):

- **Building a reusable numerical method** and **Methods 1–3**: callable interfaces, left rectangles, trapezoids, Simpson's rule, and their error assumptions.
- **Adaptive Methods and Richardson Extrapolation**: estimating error from refinement, deciding where to subdivide, and the limits of an estimator.
- **Investigation: why did the expected order disappear?**: smoothness, convergence evidence, and known breakpoints.
- **Project 2 applications: endpoints and branch points**: the removable Planck endpoint and the radial transit formulation. The change-of-variables subsection is optional enrichment.

Review **5.4 Modules as Reusable Scientific Boundaries** and the testing material
in **5.5 Documentation, Tests, and Public Type Hints** in
[Functions and Modules](../03-python/05-python-functions-modules.md).
Focus on importing functions, organizing test files, running `python -m pytest`,
and choosing justified numerical tolerances.

Gaussian quadrature, Monte Carlo, and the spectrum application are optional
reading this week. Monte Carlo is a conceptual comparison, not an assigned
Project 2 implementation or deliverable.

## In class

- [Lecture 5 · Approximation, Errors, and Quadrature](../09-lectures/lecture-05-approximation-errors-quadrature.md)
- [Lecture 6 · Trapezoids, Simpson, Modules, and Tests](../09-lectures/lecture-06-quadrature-modules-tests.md)

Use the lecture pages for the class examples and reference tables; use the
readings for the full explanations. Bring your Python environment ready for
the rectangle-rule lab and numerical tests.

## Project work

Read [Project 2 · Numerical Integration](../08-assessments/projects/project-2.md),
including its learning outcomes, five-part overview, interfaces, and required
evidence. Start by organizing your modules and tests, then build and check the
fixed quadrature rules. The project brief governs requirements and submission.

## Looking ahead

Next week introduces root finding ahead of Project 3, with time for labs and
continued Project 2 work. The
[root-finding reading](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
is available for an early look; it is not required preparation for this week.
