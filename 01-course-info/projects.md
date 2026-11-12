---
title: "Projects"
subtitle: "COMP 521 | Fall 2026"
---

# Projects

Projects are the core of COMP 521: five investigations. Use the listed dates for
each project. Each project has two halves:

- **Week 1** — method, implementation, and validation against known results
- **Week 2** — scientific application, diagnosis, or comparison

See the [Course Schedule](schedule.md) for all assignment and submission dates.
The [Project 1 brief](../08-assessments/projects/project-1.md) is the
authoritative source for its repository check, scientific work, deliverables,
and interpretation prompts.

## Start with Project 1

The [Project 1 brief](../08-assessments/projects/project-1.md) begins with the
required, completion-only GitHub repository check and then defines the
scientific model, notebook work, figures, written interpretation, and Canvas
repository-link submission route. Complete the separate
[laptop setup](../02-getting-started/02-software-setup.md) before class so that
you can use Python and Jupyter.

## Project Sequence

The five projects build a continuous scientific investigation: detecting and
characterizing exoplanets in real Kepler data.

| Project | Assigned | Due | Contribution to the investigation |
|---|---|---|---|
| 1 | Tue **Aug 25** | Tue **Sep 8** | Build and validate a transit model; place 15 real stars on a theoretical HR diagram |
| [2](../08-assessments/projects/project-2.md) | Tue **Sep 8** | Wed **Sep 23** | Integrate a limb-darkened transit model and derive the Stefan–Boltzmann constant |
| [3](../08-assessments/projects/project-3.md) | Tue **Sep 22** | Wed **Oct 7** | Solve orbital and transit-contact problems; compare simplified temperature zones for 15 stars |
| [4](../08-assessments/projects/project-4.md) | Wed **Oct 14** | Wed **Oct 28** | Validate ODE methods on the SHO and a constant-density planet; reproduce Seager mass–radius relations and compare with NASA observations |
| 5 | Thu **Oct 29** | Wed **Nov 18** | Download, clean, and fit a transit model to real Kepler photometry |

The [Final Project](../08-assessments/final-project.md) is a group presentation
connecting topics from physics, inference, transport, and learning through
shared computation and individual science applications.
Two individual [Code Review Presentations](../08-assessments/code-review-presentations.md)
give you a chance to study open source scientific and DS/ML packages alongside
the numerical-methods and data/ML work.

## What to Submit

Submissions for Projects 1–5 include:

- a code repository with a runnable workflow, README, and reproduction instructions;
- verification evidence: tests, sanity checks, or convergence diagnostics; and
- an **analysis notebook** that runs top to bottom, is documented well enough
  for another scientist to follow, and answers the project questions with clear
  written reasoning and interpretation.

### Notebook and code policy

**The notebook is the report, not a hiding place for reusable code.** Project 1
is the bootcamp exception: its functions may live in the notebook. From Project
2 onward, implementation belongs in importable, testable `.py` modules; the
notebook imports that code and contains the ordered analysis, figures, and
interpretation.

Every submitted notebook must:

- use Markdown headings and short explanations so the purpose and order of the
  work are easy to follow;
- make inputs, assumptions, units, and important choices visible where they are
  used;
- produce its figures and numerical results without undocumented manual steps;
  and
- use the interpretation structure required by its project brief.

Use [Markdown for Analysis
Notebooks](../02-getting-started/06-markdown-analysis-notebooks.md) for the
submission-focused writing and formatting conventions.

Each project mixes coding with written questions that ask you to explain choices,
interpret results, diagnose failures, and defend conclusions. Written
interpretation may appear throughout the notebook or in a combined discussion
at the end, depending on the project brief.

:::{important} Run it top to bottom before you submit
Use **Kernel → Restart Kernel and Run All Cells** before your final commit. I
re-execute submitted notebooks from a clean kernel using the repository's
instructions. If I cannot run yours from top to bottom, it does not count as
running.
:::

## How each project is graded

Projects 1–5 receive **one final letter grade each**. I assign a letter in each of
four broad dimensions, convert those letters using the course grade scale, and
take the weighted average. The final project letter uses the same cutoff table
as the rest of the course.

This is a weighted professional judgment, not a point checklist. A student does
not earn an A by collecting isolated rubric items: evidence must actually
support the computational and scientific claim.

| Dimension | Weight | A-level evidence |
|---|---:|---|
| Correct model and validation | 40% | The method is correct and checks could have exposed a plausible mistake. |
| Scientific reasoning | 25% | The interpretation connects outputs to the question, assumptions, and limits. |
| Reproducibility and code design | 20% | A clean run works; functions, inputs, outputs, and repository workflow are inspectable. |
| Communication and figures | 15% | Figures and prose let another scientist understand the evidence without guessing. |

Use the [Grading](grading.md#project-grade-calculation) page for the letter-to-
number scale, final-letter cutoffs, and the meaning of A/B/C/D/F work. Written
feedback identifies the category that most shaped the final grade and the
highest-leverage next improvement.

(sec-pairs)=
## Project Pairs & Collaboration

Projects 1–5 are done in rotating pairs. The code review presentations are
individual work. The [final project](../08-assessments/final-project.md) is
one joint presentation by all three students, with an individual contribution
from each student.

:::{important} You are responsible for your own work
For Projects 1–5, working in a pair does **not** mean submitting shared work.
Each student writes and submits their own code and written answers and must
be able to explain both.
The [AI policy](ai-policy.md) applies to everything you submit.

- **Encouraged:** designing algorithms together, whiteboarding equations,
  debugging side by side, comparing strategies, and sharing **tests you wrote**.
- **Not allowed:** sharing or copying solution code or written answers — even
  from your partner, even when you worked out the approach together.
- **Required:** credit your partner and describe what you worked on together in
  your project `README.md`.
:::

If a pairing is not working, tell me promptly and I will re-pair you.
