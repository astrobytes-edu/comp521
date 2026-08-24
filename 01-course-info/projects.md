---
title: "Projects"
subtitle: "COMP 521 | Fall 2026"
---

# Projects

Projects are the core of COMP 521: six two-week projects. Project 1 begins with
a required check in the actual Project 1 repository. Each project has two halves:

- **Week 1** — method, implementation, and validation against known results
- **Week 2** — scientific application, diagnosis, or comparison

See the [Course Schedule](schedule.md) for all assignment and submission dates.

(sec-p1-repository-check)=
## Project 1 First Milestone — Repository Check

**Due Fri Aug 28 at 11:59 pm PT.** This is a required, completion-only milestone
inside your **actual Project 1 repository**, not a separate Project 0 and not
part of the project average. It verifies only the repository submission path:

1. Use the course invitation in Canvas to accept your individual P1 repository
   through Classroom50, then clone that repository to your computer.
2. In the cloned repository's `README.md`, change the repository-check box from
   `[ ]` to `[x]`.
3. Commit that README change locally and push the commit to GitHub.
4. Open your P1 repository on GitHub and confirm that the commit is visible.

That one visible commit records completion; there is no separate upload or
automated readiness test. This check does **not** assess effort, code quality,
Python setup, or progress on the scientific work in P1. Complete the separate
[laptop setup](../02-getting-started/02-software-setup.md) before class Thursday
so that you can use Python and Jupyter in class.

Work through [Getting Started](../02-getting-started/getting-started.md) as needed.

:::{important} The Project 1 deadline does not move
Completing this check proves that your Classroom50 and GitHub submission route
works; it neither evaluates nor requires Project 1 progress. A missing check or
a repository problem discovered at or after the Project 1 deadline does not
extend that deadline. The exceptions are an approved accommodation or a
documented outage of GitHub/Classroom50; if an outage occurs, contact the
instructor through Canvas before the repository-check deadline.
:::

## Project Sequence

The six projects build a continuous scientific investigation: detecting and
characterizing exoplanets in real Kepler data.

| Project | Assigned | Due | Contribution to the investigation |
|---|---|---|---|
| 1 | Tue **Aug 25** | Tue **Sep 8** | Build and validate a transit model; place 15 real stars on a theoretical HR diagram |
| 2 | Tue **Sep 8** | Mon **Sep 21** | Integrate a limb-darkened transit model and derive the Stefan–Boltzmann constant |
| 3 | Tue **Sep 22** | Mon **Oct 5** | Solve orbital and transit-contact problems; infer habitable zones for those 15 stars |
| 4 | Tue **Oct 6** | Mon **Oct 19** | Build exoplanet interiors and test mass–radius relations against Seager et al. |
| 5 | Tue **Oct 20** | Mon **Nov 2** | Download, clean, and fit a transit model to real Kepler photometry |
| 6 | Tue **Nov 3** | Mon **Nov 16** | Classify a Gaia stellar sample with machine-learning methods |

The [Final Project](syllabus.md#sec-final-project) uses the course toolkit on a
bounded scientific question.

## What to Submit

Each project submission includes:

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

(sec-pairs)=
## Project Pairs & Collaboration

Projects 1–6 are done in rotating pairs. The final project is solo, although you
may still discuss design and debugging with classmates.

:::{important} You are responsible for your own work
Working in a pair does **not** mean submitting shared work. Each student writes
and submits their own code and written answers and must be able to explain both.
The [AI policy](ai-policy.md) applies to everything you submit.

- **Encouraged:** designing algorithms together, whiteboarding equations,
  debugging side by side, comparing strategies, and sharing **tests you wrote**.
- **Not allowed:** sharing or copying solution code or written answers — even
  from your partner, even when you worked out the approach together.
- **Required:** credit your partner and describe what you worked on together in
  your project `README.md`.
:::

If a pairing is not working, tell me promptly and I will re-pair you.
