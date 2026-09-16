---
title: "Lecture Library"
subtitle: "COMP 521 | Course blocks, projects, and live class materials"
---

# Lecture Library

Each lecture is the canonical record of what we build together in class. It is
organized by **course block and project**, because a method is easier to learn
when its scientific question, computational choices, and evidence are visible
in one place.

Lectures are not replacement textbook chapters. Use the linked reading for a
slower, more complete treatment; use the lecture page to recover the question,
worked examples, predictions, and project connection from a specific class.

:::{important} A durable route through the site

- **Lectures** answer: *What did we do in class, and why?*
- **Scientific Background** answers: *What is this observable, model, or
  approximation?*
- **Scientific Computing with Python** and **Readings** answer: *Where can I
  study this method in depth?*
- **Practice Labs** provide focused, low-stakes rehearsal.
- **Projects** establish the required scientific evidence and deliverables.
:::

## Block 1 · Scientific Programming & Transit Model

**Project connection:** Project 1, a restartable notebook that models the
fraction of stellar light visible during a transit.

| Lecture | In-class question | Build toward |
|---|---|---|
| [Lecture 1: Python Foundations](../03-python/bootcamp-01-run-calculate-inspect.md) | How do mathematics, code, software environments, and finite-precision numbers connect? | vocabulary, legible calculations, numerical judgment |
| [Lecture 2: Procedures, Data, and Reusable Calculations](../03-python/bootcamp-02-procedures-decisions.md) | How does a stated scientific rule become a testable procedure for many observations? | Grade Calculator implementation and first NumPy arrays |
| [Lecture 3: Function Interfaces and Reusable Analysis](../03-python/bootcamp-03-data-functions.md) | How do arguments, unpacking, and return design keep a reusable calculation clear at every call site? | COMP 521 Course-Grade Calculator Lab |
| [Lecture 4: NumPy, Matplotlib, and Readable Evidence](../03-python/bootcamp-04-arrays-figures.md) | How do paired arrays, vectorized models, and a labeled figure support a bounded claim? | array shapes, masks, broadcasting, and figure-based reasoning |

Useful background: [Exoplanets](../10-scientific-background/exoplanets.md),
[transits](../10-scientific-background/transits.md),
[light curves](../10-scientific-background/light-curves.md), and the
[uniform-source model](../10-scientific-background/uniform-source-model.md).

## Block 2 · Numerical Integration

How do we turn a continuous mathematical model into a finite calculation, and
how do we decide whether its accuracy is sufficient?

| Lecture | In-class question | Build toward |
|---|---|---|
| [Lecture 5: Approximation, Errors, and Quadrature](lecture-05-approximation-errors-quadrature.md) | How do Taylor approximations and floating-point arithmetic shape numerical error? | absolute and relative tolerances, rectangle quadrature, and an error bound |
| [Lecture 6: Trapezoids, Simpson, Modules, and Tests](lecture-06-quadrature-modules-tests.md) | How do better local approximations and meaningful tests improve an integration method? | trapezoid and Simpson rules, reusable modules, and the sine rectangle lab |
| [Lecture 7: Approximations, Adaptivity, and Roots](lecture-07-adaptivity-roots.md) | How do local models guide adaptive integration and root finding? | quadrature recall, Simpson error estimates, bisection bounds, and Newton updates |
| [Lecture 8: Finite Differences and Root-Finding Tools](lecture-08-rootfinding-tools.md) | What evidence supports a solver’s stopping decision? | finite differences, secant updates, and a tested bisection module |

Read alongside the lectures: [numerical errors](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md),
[Taylor series](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md),
[quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md),
and [root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md).
These methods support [Project 2](../08-assessments/projects/project-2.md): integration and convergence investigations.

## Future course blocks

:::{warning} Library expansion in progress

These headings reserve the durable homes for later lecture pages. They are not
yet a second set of required materials. The course schedule and published
lecture pages determine what is currently assigned.
:::

- **Block 3 · Root Finding & Stellar Inference** — solving a model equation
  and checking whether a solution is trustworthy.
- **Block 4 · ODE Methods & Dynamical Models** — time stepping, stability, and
  conservation.
- **Block 5 · Real Data & Model Fitting** — data provenance, uncertainty, and
  model criticism.
- **Block 6 · ML & Scientific Classification** — evaluation, generalization,
  and scientific limits.
- **Block 7 · Final Project Studio** — question framing, evidence design, and
  reproducible communication.
