---
title: "Grading"
subtitle: "COMP 521 | Fall 2026"
---

# Grading

## How grading works in this course

**Everything is graded with letters, and each assignment gets one letter.**

There are no point breakdowns, no percentage subscores, and no itemized
rubrics. When I grade your project I read the whole thing — code, validation,
figures, memo — and judge it as a piece of work, the way a referee assesses a
paper.

:::{note} Why it works this way
An itemized rubric tells you exactly what to optimize, and people optimize what
they are shown. That produces submissions assembled to satisfy a checklist
rather than to be correct, which is the opposite of what this course is for.

What you get instead is a clear description of what each grade *means* — below —
plus a written comment on every submission explaining the grade you got. If you
want to know how to do better, that comment is the answer, and it will tell you
more than a number would.
:::

## The scale

| A+ | A | A− | B+ | B | B− | C+ | C | C− | D+ | D | D− | F |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 4.3 | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0.7 | 0 |

Your grade in each component is the average of the letters you earned in it, and
your course grade is the weighted average of those. Letters average the way you
would expect: an A+ and an A− come out to an A. Grades are recorded as these
numbers in Canvas, so you can see where you stand at any point.

**A+ is not "did extra."** It is for work showing judgment beyond what was asked
— a validation you thought of yourself, a failure mode you found and explained,
a simpler approach than the one specified. Volume does not earn it.

:::{note} A+ on an assignment, but not as a course grade
SDSU does not award A+ as a final grade, so **the highest course grade is an
A** — a semester of straight A+ work earns an A.

An A+ is still worth having. Because it counts as 4.3, it lifts your average and
can offset a weaker piece of work elsewhere. That is the point of it: not a
higher ceiling, but room to recover from one bad week.
:::

### Turning your average into a course grade

Your weighted average is rounded to the nearest letter:

| Average | Grade | | Average | Grade |
|:--|:--|--|:--|:--|
| ≥ 3.85 | **A** | | 1.85 – 2.14 | **C** |
| 3.50 – 3.84 | **A−** | | 1.50 – 1.84 | **C−** |
| 3.15 – 3.49 | **B+** | | 1.15 – 1.49 | **D+** |
| 2.85 – 3.14 | **B** | | 0.85 – 1.14 | **D** |
| 2.50 – 2.84 | **B−** | | 0.35 – 0.84 | **D−** |
| 2.15 – 2.49 | **C+** | | < 0.35 | **F** |

## Weights

| Component | Weight |
|:--|--:|
| Projects (6) | 50% |
| Final project | 20% |
| SE presentations (2) | 10% |
| Growth Reflections (3) | 10% |
| Scholarly engagement | 10% |

## What the grades mean

### Projects and the final project

Judged as a whole: does the code do the right thing, do you know that it does,
and could someone else follow it?

| | |
|:--|:--|
| **A** | It works, you showed that it works, and someone else could pick it up and run it. The validation is real — convergence at the expected order, a limiting case checked, a comparison against something that could have disagreed. The memo says what you did and what it means. |
| **B** | It works and you checked it, but the evidence is thinner than the claim, or the code takes effort to follow, or the writing leaves me guessing about a choice you made. |
| **C** | It runs, but there is little evidence it is right — tests that would pass for a broken implementation, or results reported without any check that could have caught an error. Or pieces are missing. |
| **D** | Substantially incomplete, not working, or missing what was asked for. |
| **F** | Not submitted, or not your own work. |

:::{important} Validation is where the grade is decided
Code that runs is the starting point, not the finish line. The difference
between a B and an A in this course is almost always whether you can show your
result is *right* — not whether you produced one.
:::

Each project includes a **research memo** (2–3 pages: methods, results,
discussion; Project 1 substitutes a 1–2 page EDA report). It is not graded
separately — it is part of the work I am reading.

### SE presentations

Judged on whether the class can use the tool afterward.

| | |
|:--|:--|
| **A** | The room ran the tool and left able to use it. Your repository worked on other people's machines. You knew where the tool breaks down and said so. |
| **B** | A solid walkthrough, but some people got stuck and stayed stuck, or the setup needed hand-holding, or you could not say much about the tool's limits. |
| **C** | Mostly a demo you performed rather than one we did, or a repository that did not really work outside your own laptop. |
| **D / F** | Unprepared, or not delivered. |

Full assignment and topic list:
[Software Engineering Presentation](../assignments/se-presentation.md).

### Growth Reflections

Judged on honesty and specificity, not polish or length.

| | |
|:--|:--|
| **A** | Specific and honest. Names things you actually got wrong and what you did about them. Someone reading it would learn something real about how you work. |
| **B** | Genuine but general — true statements that could have been written by anyone in the class. |
| **C** | Phoned in. |
| **F** | Not submitted. |

*"I did not understand why Newton's method diverged until I plotted the
iterates"* is worth more than a page of general statements about learning a lot.

| | Due |
|---|---|
| Growth Memo 1 — baseline | Mon **Aug 31** |
| Growth Memo 2 — mid-semester | Mon **Oct 19** |
| Growth Synthesis | Mon **Dec 14** |

### Scholarly engagement

One grade, at the end of the semester, for the term as a whole.

| | |
|:--|:--|
| **A** | Prepared and present. Contributes and asks real questions. Arrives at classmates' presentations already set up. Comes to check-ins with work to show. |
| **B** | Steady and cooperative, with some quiet stretches or occasional unpreparedness. |
| **C** | Frequently unprepared or disengaged; participates mainly when prompted. |
| **D / F** | Habitually absent or habitually disengaged. |

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
