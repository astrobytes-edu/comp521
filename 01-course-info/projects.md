---
title: "Projects"
subtitle: "COMP 521 | Fall 2026"
---

# Projects

Projects are the core of COMP 521: six two-week projects, beginning with a
required technical-readiness checkpoint inside Project 1. Each project has two
halves:

- **Week 1** — method, implementation, and validation against known results
- **Week 2** — scientific application, diagnosis, or comparison

See the [Course Schedule](schedule.md) for all assignment and submission dates.

## Before Project 1 — Technical Readiness Check

**Due before class Thu Aug 27.** This is a required, completion-only milestone
inside your **actual Project 1 repository**, not a separate Project 0 and not
part of the project average. It verifies only the minimum submission path:

1. Use the course invitation in Canvas to accept your individual P1 repository
   through Classroom50, then clone that repository to your computer.
2. Activate your COMP 521 Python environment and open the starter
   `analysis.ipynb`.
3. Run the tagged readiness cell and save its printed success message in the
   notebook.
4. Commit and push `analysis.ipynb`, then open your P1 repository on GitHub and
   confirm that the **P1 readiness** GitHub Actions check is green.

The GitHub check runs automatically after each push. A green check records
completion; there is no separate upload. You may retry as often as necessary
before class. This checkpoint does **not** assess effort, code quality, or
progress on the scientific work in P1.

Work through [Getting Started](../02-getting-started/index.md) as needed.

:::{important} The P1 deadline does not move
Completing this checkpoint proves that your environment and submission route
work; it neither evaluates nor requires P1 progress. A missing checkpoint or a
technical problem discovered at or after the P1 deadline does not extend that
deadline. The exceptions are an approved accommodation or a documented outage
of GitHub/Classroom50; if an outage occurs, contact the instructor through
Canvas before the checkpoint deadline.
:::

## Project Sequence

The six projects build a continuous scientific investigation: detecting and
characterizing exoplanets in real Kepler data.

| Project | Contribution to the investigation |
|---|---|
| 1 | Build and validate a transit model; place 15 real stars on a theoretical HR diagram |
| 2 | Integrate a limb-darkened transit model and derive the Stefan–Boltzmann constant |
| 3 | Solve orbital and transit-contact problems; infer habitable zones for those 15 stars |
| 4 | Build exoplanet interiors and test mass–radius relations against Seager et al. |
| 5 | Download, clean, and fit a transit model to real Kepler photometry |
| 6 | Classify a Gaia stellar sample with machine-learning methods |

The [Final Project](syllabus.md#sec-final-project) uses the course toolkit on a
bounded scientific question.

## What to Submit

Each project submission includes:

- a code repository with a runnable workflow, README, and reproduction instructions;
- verification evidence: tests, sanity checks, or convergence diagnostics; and
- an **analysis notebook** that runs top to bottom, is documented well enough
  for another scientist to follow, and ends with a written **Discussion**.

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

Project 1 places short interpretation next to each part and ends with
`Looking back`; it has no separate final report. From Project 2 onward, include
the prose-only `Discussion` required by the current brief, normally 500–800
words unless that brief says otherwise.

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

:::{important} You are responsible for your own code
Working in a pair does **not** mean submitting shared work. Each student writes,
submits, and must be able to explain their own implementation.

- **Encouraged:** designing algorithms together, whiteboarding equations,
  debugging side by side, comparing strategies, and sharing **tests you wrote**.
- **Not allowed:** sharing or copying solution code — even from your partner,
  even when you worked out the approach together.
- **Required:** credit your partner and describe what you worked on together in
  your project `README.md`.
:::

If a pairing is not working, tell me promptly and I will re-pair you.
