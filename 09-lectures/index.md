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
- **Python Textbook** and **Numerical Methods, Data & Inference** answer:
  *Where can I study this method in depth?*
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

**Watch and review:** [Quadrature animations](animations/animations.md#quadrature-animations) — integration geometry and adaptive refinement.

Read alongside the lectures: [numerical errors](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md),
[Taylor series](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md),
and [quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md).
These methods support [Project 2](../08-assessments/projects/project-2.md): integration and convergence investigations.

## Block 3 · Root Finding & Stellar Inference

**Project connection:** [Project 3](../08-assessments/projects/project-3.md),
a root-finding library and stellar-inference notebook. Lecture 7 bridges
adaptive integration and root finding.

| Lecture | In-class question | Build toward |
|---|---|---|
| [Lecture 7: Approximations, Adaptivity, and Roots](lecture-07-adaptivity-roots.md) | How do local models guide adaptive integration and root finding? | quadrature recall, Simpson error estimates, bisection bounds, and Newton updates |
| [Lecture 8: Finite Differences and Root-Finding Tools](lecture-08-rootfinding-tools.md) | What evidence supports a solver’s stopping decision? | finite differences, secant updates, and a tested bisection module |
| [Lecture 9: Trustworthy Numerical Answers](lecture-09-trustworthy-answers.md) | When do an accepted step, a small residual, or a refined integral support an answer? | line searches, Jacobians, damping, advanced quadrature, and convergence evidence |
| [Lecture 10: Modular Design and OOP](lecture-10-classes-lab.md) | How do functions and variables become methods and attributes in a class? | Rectangle, scientific classes, and Project 3 Part 5 |

Lectures 9 and 10 continue this lecture sequence in Week 5. Lecture 10 leads
into the Project 3 Part 5 lab.

**Watch and review:** [Root-finding animations](animations/animations.md#root-finding-animations) — bisection, Newton, and secant steps.

Read alongside the lectures: [root finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md)
and [robust computing](../04-scientific-computing/09-robust-computing.md).

### Software Engineering for Scientists

[Software Engineering for Scientists](software-engineering.md) provides the
slides, handout, and companion readings for contracts, independent checks,
systematic debugging, and reproducible results. Apply the examples to your
current project; its brief owns the required interface and deliverables.

## Block 4 · ODE Methods & Exoplanet Interiors

[Open the Block 4 lecture overview](block-04-odes.md) for the ODE and Pandas
slides, handouts, data downloads, and links to the existing ODE readings.

[Lecture 11: Ordinary Differential Equations](lecture-11-odes.md) provides
the ODE slides and worked handout, from Euler and Runge–Kutta methods to
stability, conservation, and planetary pressure balance.

[Lecture 12: Pandas and Exploratory Data Analysis](lecture-12-pandas.md)
provides a 30-minute introduction and worked handout. Students install Pandas,
create their own notebook, and explore the saved NASA exoplanet CSV.

## Block 5 · Real Data & Model Fitting

[Block 5 lecture overview](block-05-data.md) connects the lectures and readings.
[Lecture 13: Measurements, Probability, and Geometry](lecture-13-measurements.md)
connects noisy scientific measurements to probability, data matrices, and
projection. The lecture page links the slides, worked handout, and primer.

## Future course blocks

:::{warning} Library expansion in progress

These headings reserve the durable homes for later lecture pages. They are not
yet a second set of required materials. The course schedule and published
lecture pages determine what is currently assigned.
:::

- **Block 6 · ML & Scientific Classification** — evaluation, generalization,
  and scientific limits.
- **Block 7 · Final Project Studio** — question framing, evidence design, and
  reproducible communication.
