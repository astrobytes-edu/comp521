---
title: "This Week"
subtitle: "COMP 521 | September 22–24, 2026"
---

# This Week

## Week 5 · Trustworthy answers and scientific classes

This week connects convergence and error estimates to the question: when should
we trust a numerical answer? Tuesday surveys advanced numerical methods and
examines what stopping criteria do and do not establish. Thursday introduces
a small scientific class, then begins Project 3 in lab.

## Required readings

### Before Tuesday · Convergence and trustworthy answers

Read these sections of [Root Finding](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md):

- **Comparison of Convergence Rates**: distinguish bracket contraction from
  measured root error and convergence order.
- **Hybrid Methods: preserve a bracket while using local models**: how
  safeguarded methods combine bracketing with faster proposals.
- **Investigation: which root estimate is justified?** and **Application: Units
  and Scaling**: residuals, root errors, absolute and relative tolerances.

Revisit **Adaptive Methods and Richardson Extrapolation** in
[Quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md),
focusing on refinement-based error estimates and the example where sampling
misses a feature. Gaussian quadrature is part of the in-class overview;
its derivation is optional. No new integration algorithm is required for
Project 3.

### Before Thursday · A small class with validated state

1. Follow the introductory examples in **§§6.1–6.4** of
   [OOP Fundamentals](../03-python/06-oop-fundamentals.md): `__init__`, `self`,
   methods, and derived properties. Focus on these examples rather than every
   exercise or extended example.
2. Read **§§10.1–10.4** of
   [Designing Small Scientific Types](../04-scientific-computing/10-advanced-oop.md)
   for validation and tests of an object's contract.

Inheritance, operator overloading, and advanced class machinery are not required.
Dataclasses are optional. Review importing modules and running `python -m pytest`
in [Functions and Modules](../03-python/05-python-functions-modules.md) if needed.

## In class

- **Tuesday, September 22:** advanced integration and root-finding overview;
  convergence evidence; physical-root selection; tolerances and trustworthy answers.
- **Thursday, September 24:** constructors, stored state, methods, and properties;
  a small validation example; then Project 3 lab.

Bring your Python environment, Lecture 8 root-finding module and tests, and
Project 1–2 code. In lab, aim to run a passing known-root test, explain the
returned history, and construct one valid `Star` while rejecting invalid state.
If the solver is unfinished, establish that passing test first.

## Project work

[Project 3 · Root Finding and Stellar Inference](../08-assessments/projects/project-3.md)
is due **Monday, October 5, 11:59 pm PT**. Build reusable root finders, investigate Wien's law, compute
Keplerian positions and transit contacts, and use a `Star` class for simplified
equilibrium-temperature zones. The project brief governs requirements and
submission; use the [course project rubric](projects.md#how-each-project-is-graded)
for the assessment dimensions.

Use the [Science Background](../08-assessments/projects/project-3-science-background.md)
for the spectral-density explanation, worked orbital example, and contact diagrams.
Read those sections alongside the corresponding project parts.

By the end of this week, aim to finish Parts 1–2 and begin Part 3. Test the root
library before using it for orbital calculations. These are pacing milestones;
the required submission is defined in the project brief.

## Looking ahead

Next week connects Kepler geometry to contact finding. Check the circular orbit
against Project 1 before finding eccentric transit contacts. Lab time will
support contact-duration comparisons, stellar temperature round trips, and a
clean notebook run before submission.
