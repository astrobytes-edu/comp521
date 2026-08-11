---
title: "Grading & Rubrics"
subtitle: "COMP 521 | Fall 2026"
---

# Grading & Rubrics

This page gives the detailed rubrics. For weights, deadlines, late work, and
regrade policy, the [Syllabus](syllabus.md) is authoritative.

| Component | Weight |
|:--|--:|
| Projects (6 × ~8.3%) | 50% |
| Final project | 25% |
| Reflections (3 × 5%) | 15% |
| Scholarly engagement | 10% |

## Project rubric (50%)

Each project is scored out of 100:

| Component | Points | What earns full credit |
|:--|--:|:--|
| Correctness | 40 | Passes the provided test suite; results validated against analytic or published values |
| Code quality & design | 25 | Modular, documented, readable; sensible interfaces |
| Visualization | 15 | Correct, labeled, publication-quality figures |
| Research memo | 20 | Correct methods (40%), clear communication (30%), valid results (30%) |

:::{important} Tests run before you submit
Every project ships with a test suite. You can run it as often as you like. A
submission that fails the provided tests has not met the correctness bar — there
is no partial credit for "almost passing," because in computational science
there is no partial credit for an almost-correct integrator.
:::

### Validation is not the same as testing

Passing tests means your code does what was asked. **Validation** means showing
your result is *right*: convergence at the theoretically expected order, energy
conserved to the expected tolerance, agreement with a published value, sensible
behavior in a limiting case.

Projects ask for validation explicitly, and it is where most of the correctness
points actually live. A student who passes every test but cannot demonstrate
second-order convergence has not finished the assignment.

## Research memos

Submitted with each project, scored within the project's 20-point memo
allocation.

- Submit as a **PDF** in your project repo
- **Single-spaced**, **2–3 pages of text** (not counting figures or references)
- Include at minimum: **methods**, **results**, and **discussion**

## Reflections (15%)

Three across the semester, 5% each. See
[Reflections](syllabus.md#sec-reflections) for what each should contain.

| # | Due with | Date |
|---|---|---|
| Growth Memo 1 | Project 1 | Fri **Sep 4** |
| Growth Memo 2 | Project 4 | Mon **Oct 19** |
| Growth Synthesis | Final Project | *Finals slot* |

Graded on engagement, not polish:

| Mark | Meaning | Credit |
|:--|:--|--:|
| ✓+ | Exceptional reflection — specific, honest, identifies real conceptual shifts | 100% |
| ✓ | Adequate reflection | 85% |
| ✓− | Minimal effort | 50% |

Be specific. *"I did not understand why Newton's method diverged until I plotted
the iterates"* is worth more than a page of general statements about learning a lot.

## Final project (25%)

| Component | Points | What earns full credit |
|:--|--:|:--|
| Correctness & methodology | 35 | Methods appropriate and correctly implemented; results validated |
| Reproducibility | 20 | Repository runs end to end from a clean checkout; documented |
| Research report | 30 | 5–7 pages; background, methods, results, conclusions |
| Presentation | 15 | Clear, well-paced, handles questions on design choices |

You should expect to defend your design and verification choices.

## Scholarly engagement (10%)

Scored on the rubric in the
[Syllabus](syllabus.md#sec-engagement). In a class this size, engagement is
assessed continuously through observable behavior rather than by attendance
tally.

## Submission

Submission is via GitHub, using
[Classroom50](https://github.com/foundation50/classroom50/wiki). Projects are due
**Mondays at 11:59 PM PT** (Project 1 excepted — see the
[Schedule](schedule.md)).

**Your last commit before the deadline is your submission.** Commit timestamps
are unambiguous, which cuts both ways: there is never a dispute about what you
turned in and when, and "I finished it but forgot to push" is not recoverable.
Push early and often — a pushed work-in-progress always beats a perfect
uncommitted local copy.
