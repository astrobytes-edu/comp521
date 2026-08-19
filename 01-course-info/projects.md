---
title: "Projects"
subtitle: "COMP 521 | Fall 2026"
---

# Projects

Projects are the core of COMP 521: a one-week setup bootcamp followed by six
two-week projects. Each project has two halves:

- **Week 1** — method, implementation, and validation against known results
- **Week 2** — scientific application, diagnosis, or comparison

## Project 0 — Setup Bootcamp

**Due Thu Aug 27.** Project 0 makes sure the machinery works before project work
begins. You will:

- install and verify your Python environment;
- get comfortable enough at the command line to navigate and run things;
- set up `git` and GitHub;
- join the course on Classroom50 and push a first commit; and
- confirm your submission actually arrived.

Work through [Getting Started](../02-getting-started/index.md) alongside it.
Project 0 is completion-only and does not count toward your project average.

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
- end with a prose-only section titled `Discussion` that answers the project's
  questions and explains what the results mean.

Aim for 500–800 words in the Discussion; Project 1's discussion is shorter.

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
