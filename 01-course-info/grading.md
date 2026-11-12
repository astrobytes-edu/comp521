---
title: "Grading"
subtitle: "COMP 521 | Fall 2026"
---

# Grading

## How grading works in this course

**Each graded assignment receives one final letter grade.** Projects 1–5 use
four broad letter-graded dimensions; the weighted average becomes the project
letter. Code Review Presentations, Growth Reflections, and the final project's
components are holistically assessed as described below.

:::{note} Why it works this way
The project rubric is deliberately broad. It makes the basis of the grade
legible without rewarding a notebook assembled as a checklist. Within each
dimension I still judge the work as a coherent scientific artifact, then give a
written comment naming the strongest evidence and highest-leverage improvement.
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
creates some room to recover from one bad week.
:::

### Turning your average into a course grade

Each cutoff sits **0.2 below** that grade's own value, so you can fall a little
short of straight-A work and still earn an A. What it will not do is round you
up a whole step: consistent A− work earns an A−.

| Average | Grade | | Average | Grade |
|:--|:--|--|:--|:--|
| ≥ 3.80 | **A** | | 1.80 – 2.09 | **C** |
| 3.50 – 3.79 | **A−** | | 1.50 – 1.79 | **C−** |
| 3.10 – 3.49 | **B+** | | 1.10 – 1.49 | **D+** |
| 2.80 – 3.09 | **B** | | 0.80 – 1.09 | **D** |
| 2.50 – 2.79 | **B−** | | 0.50 – 0.79 | **D−** |
| 2.10 – 2.49 | **C+** | | < 0.50 | **F** |

## Weights

| Component | Weight |
|:--|--:|
| Projects 1–5 (8% each) | 40% |
| Code Review Presentations (5% each) | 10% |
| Final project (preparation and development 5%; finished project 25%) | 30% |
| Growth Reflections (3) | 10% |
| Scholarly engagement | 10% |

## What the grades mean

The descriptions below are anchors. Plus and minus grades indicate work between
adjacent descriptions; A+ is reserved for the judgment described above.

### Projects 1–5

(project-grade-calculation)=
#### Project grade calculation

The canonical project dimensions and weights live on the [Projects](projects.md#how-each-project-is-graded)
page. For each dimension, I assign a letter using the course scale above, then
calculate:

$$
\text{project score} = 0.40M + 0.25S + 0.20R + 0.15C,
$$

where $M$ is correct model and validation, $S$ scientific reasoning, $R$
reproducibility and code design, and $C$ communication and figures. I translate
the resulting score to a final letter with the cutoff table above.

For example, an A in model/validation, B+ in scientific reasoning, A− in
reproducibility, and A in communication produces
$0.40(4.0)+0.25(3.3)+0.20(3.7)+0.15(4.0)=3.765$, which is an A−.

#### Letter anchors for project dimensions

Use these anchors for all four dimensions. Plus and minus grades represent work
between adjacent anchors; A+ requires judgment beyond what was asked.

| | |
|:--|:--|
| **A** | It works, you showed that it works, and someone else could pick it up and run it. The validation is real — convergence at the expected order, a limiting case checked, a comparison against something that could have disagreed. The written interpretation explains what you did and what it means. |
| **B** | It works and you checked it, but the evidence is thinner than the claim, or the code takes effort to follow, or the writing leaves me guessing about a choice you made. |
| **C** | It runs, but there is little evidence it is right — tests that would pass for a broken implementation, or results reported without any check that could have caught an error. Or pieces are missing. |
| **D** | Substantially incomplete, not working, or missing what was asked for. |
| **F** | Not submitted, or not your own work. |

:::{important} Validation is where the grade is decided
Code that runs is the starting point, not the finish line. The difference
between a B and an A in this course is almost always whether you can show your
result is *right* — not whether you produced one.
:::

Each project's **analysis notebook** includes written reasoning and
interpretation in the places required by the project brief. Those answers are
evidence for the scientific-reasoning and communication dimensions; they are
not a separate points category.

### Code Review Presentations

Each of the two individual presentations receives one holistic letter grade
and counts for 5% of the course grade. I look for a useful map of the package,
a specific code trace, a check that could have disagreed with the student's
expectation, and a conclusion that stays within the evidence. See the
[assessment brief](../08-assessments/code-review-presentations.md) for the
rounds, format, and grading anchors.

### Final project

The [final project](../08-assessments/final-project.md) is judged holistically.
Each student's grade reflects the shared presentation and computation, their
individual understanding and contribution, and their explanation of connections
during discussion.

### Final-project preparation and development

The 5% preparation and development component recognizes project-specific
understanding and progress through our in-class work, discussions, and check-ins.
Come prepared to discuss what you are exploring and answer questions about
your developing work. This is an ongoing holistic assessment. The separate
10% Scholarly Engagement component covers broader participation across the
semester.

### Growth Reflections

Growth Memos 1 and 2 should each be **1–2 pages**, with a minimum of one full
page. The Growth Synthesis should be **2–3 pages**, with a minimum of two full
pages. They are judged on specificity, reflection, and evidence, not literary
polish. Submit each through the corresponding **Canvas assignment** as a
**single-spaced PDF** using a readable **12-point font** and **1-inch margins**.

| | |
|:--|:--|
| **A** | Specific and reflective. Uses concrete evidence to explain how you worked, what you learned, and what changed or stayed the same. |
| **B** | Relevant but general. Makes reasonable claims without enough specific evidence or reflection to show what they mean for your work. |
| **C** | Minimal or largely descriptive, with little specific evidence or reflection. |
| **D** | Substantially incomplete or too vague to demonstrate meaningful reflection. |
| **F** | Not submitted. |

*"I did not understand why Newton's method diverged until I plotted the
iterates"* is worth more than a page of general statements about learning a lot.

| | Assigned | Due |
|---|---|---|
| Growth Memo 1 — baseline | Tue **Aug 25** | Mon **Aug 31**, 11:59 pm PT |
| Growth Memo 2 — mid-semester | Tue **Oct 6** | Mon **Oct 19**, 11:59 pm PT |
| Growth Synthesis | Tue **Nov 17** | Mon **Dec 14**, 11:59 pm PT |

### Scholarly engagement

One grade, at the end of the semester, for the term as a whole.

| | |
|:--|:--|
| **A** | Consistently prepared. Contributes through questions, visible reasoning, productive collaboration, or substantive check-ins. |
| **B** | Steady and cooperative, with occasional unpreparedness or limited visible engagement. |
| **C** | Frequently unprepared or disengaged; contributes mainly when prompted. |
| **D** | Rarely prepared or engaged, with little visible participation in the work of the course. |
| **F** | No meaningful evidence of scholarly engagement. |

Attendance itself is not graded. However, excessive absences will affect
Scholarly Engagement because they limit prepared participation, collaboration,
substantive check-ins, and other visible engagement with the course.

## Submission

Project 1 is submitted by linking the GitHub repository in its Canvas
assignment. Later project briefs will name their submission route, including any
Classroom50 use. Code Review Presentations and Growth Reflections are submitted
through their corresponding Canvas assignments. The final-project brief will
specify its submission route.
Projects are typically due **Wednesdays at 11:59 pm PT**. The
[Schedule](schedule.md) lists each specific deadline.

**For projects, your submission is the latest commit pushed to GitHub by the
deadline.** Work that remains only on your computer has not been submitted.
Push early and often: a pushed work-in-progress always beats a perfect
uncommitted local copy.

See the syllabus for [extensions](syllabus.md#sec-late) and
[regrade requests](syllabus.md#sec-regrades).
