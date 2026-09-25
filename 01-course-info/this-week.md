---
title: "This Week"
subtitle: "COMP 521 | September 22–24, 2026"
---

# This Week

## Week 5 · Trustworthy answers and scientific classes

This week connects convergence and error estimates to the question: when should
we trust a numerical answer? Tuesday surveys advanced numerical methods and
examines what stopping criteria do and do not establish. It also includes
Project 2 work time. Thursday introduces
a small scientific class, then begins Project 3 in lab.

## Reading route

### Prepare for Tuesday

Read [convergence rates](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-convergence) and the [root-evidence investigation](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#root-investigation). Be ready to distinguish residual, update, and root error.

### Review after Tuesday

- [Backtracking](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#backtracking-newton): direction, distance, and acceptance.
- [Jacobians and local fitting](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-jacobians): matrix dimensions, predicted changes, and damping.
- [Safeguarded methods](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-hybrids): preserve a bracket while using local proposals.
- [Adaptive estimates](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#adaptive-methods), [Richardson extrapolation](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#richardson-extrapolation), and [Gaussian quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#method-4-gaussian): match the method to the available information.

Focus on the explanations and worked examples. Implementations of advanced methods are optional enrichment; Project 3 requires the basic solvers specified in its brief.

### Prepare for Thursday

1. Read [class basics and `self`](../03-python/06-oop-fundamentals.md#week5-class-basics), [methods](../03-python/06-oop-fundamentals.md#week5-methods), and [properties](../03-python/06-oop-fundamentals.md#week5-properties). Follow the introductory examples; extended examples and exercises are optional.
2. Read the [type contract](../04-scientific-computing/10-advanced-oop.md#week5-type-contract) and [tests of that contract](../04-scientific-computing/10-advanced-oop.md#week5-type-tests). The example uses a dataclass; understand its stored fields and validation, but implementing a dataclass is optional. An ordinary class is sufficient for Project 3.

Inheritance and operator overloading are not required. Review imports and `python -m pytest` in [Functions and Modules](../03-python/05-python-functions-modules.md) if needed.

## In class

- **Tuesday, September 22:** [Lecture 9](../09-lectures/lecture-09-trustworthy-answers.md) surveys methods including backtracking,
  Levenberg–Marquardt, integration, and convergence evidence; then Project 2 work time. Advanced methods are conceptual context, not new
  implementation requirements.
- **Thursday, September 24:** [Lecture 10](../09-lectures/lecture-10-classes-lab.md) develops methods, attributes, constructors, public and internal names, properties, and scientific classes; then Project 3 Part 5 lab.

Bring your Python environment, Project 1 stellar data and luminosity code,
and any completed Project 3 Part 2 work. In lab, build the `Star` class for
Part 5, reject invalid state, check derived values, and start the fifteen-star
comparison.

## Project work

[Project 2 · Numerical Integration](../08-assessments/projects/project-2.md)
is due **Wednesday, September 23, 11:59 pm PT**. Use Tuesday’s work time to
resolve your first unchecked requirement and rerun the relevant tests.

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
