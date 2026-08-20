---
title: "Getting Started"
subtitle: "Your COMP 521 computational workspace"
author: "Anna Rosen"
---

This module gets one complete scientific-computing loop working on your own
computer: navigate to a project, activate its Python environment, run a
notebook, and save the result with Git.

:::{warning} Classroom50 acceptance check
COMP 521 uses Classroom50, not GitHub Classroom. The course-specific invitation
and acceptance screens are scheduled for a fresh-student rehearsal on **August
20**. Until that check is complete, use the invitation posted in Canvas and the
verified P1 steps in this module; do not rely on Classroom50 screenshots from a
different course.
:::

## What to read, and when

### Complete for P1 technical readiness

::::{grid} 1 1 3 3

:::{card} 1. Command line
:link: 01-cli-intro.md

Learn the small set of terminal commands needed to find and run a project.
**About 25 minutes.**
:::

:::{card} 2. Software setup
:link: 02-software-setup.md

Install Miniforge and VS Code, create the `comp521` environment, and run a
local notebook check. **About 30–45 minutes.**
:::

:::{card} 3. Git and Classroom50
:link: 03-git-intro.md

Clone your assigned P1 repository, commit one targeted file, push it, and
verify the green readiness check. **About 35 minutes.**
:::

::::

### Use while writing Project 1

::::{grid} 1 1 2 2

:::{card} Markdown for analysis notebooks
:link: 06-markdown-analysis-notebooks.md

Use headings, equations, figures, and interpretation to turn a running notebook
into a scientific argument.
:::

:::{card} Scientific software guide
:link: 04-software-engineering-guide.md

Use the contract, evidence, and debugging sections in P1. The module-and-test
structure begins in P2.
:::

::::

### Keep beside you from Project 2 onward

:::{card} Scientific software workflow checklist
:link: 05-scientific-software-workflow-cheatsheet.md

A phase-aware pre-coding, debugging, and submission checklist. It is a working
aid, not a grading rubric.
:::

## The P1 readiness route

The readiness checkpoint is intentionally narrow. It verifies access, the
course environment, notebook execution, and a successful push—not progress on
the P1 science.

1. Follow the Project 1 invitation in Canvas and obtain your assigned
   Classroom50 repository.
2. Clone that repository and change into its directory.
3. Activate the `comp521` environment.
4. Open `analysis.ipynb`, run its tagged readiness cell, and save the notebook
   with the success message visible.
5. Stage **that notebook**, inspect the staged change, commit, and push:

   ```bash
   git status
   git add analysis.ipynb
   git diff --staged --stat
   git commit -m "Complete P1 technical readiness check"
   git push
   ```

6. Open your P1 repository on GitHub. Confirm that the commit is present and
   the **P1 readiness** check is green.

The complete checkpoint contract and due date live on the
[Projects page](../01-course-info/projects.md#before-project-1-technical-readiness-check).

## When an error appears

An error message is evidence, not a verdict on your ability. Preserve the exact
text before trying fixes.

| Symptom | First checks |
|---|---|
| `command not found` | Check spelling, whether the program is installed, and whether this shell can find it. |
| `ModuleNotFoundError` | Run `conda activate comp521`, then confirm which Python is active. |
| `No such file or directory` | Run `pwd` and `ls`; verify the path one component at a time. |
| `git push` fails | Read the exact reason; check `git status`, `git remote -v`, and whether you made a commit. Do not pull or force-push blindly. |
| A notebook uses the wrong kernel | In VS Code, select the `comp521` kernel, restart, and run the cell again. |

If the first checks do not resolve it, ask for help with:

- your operating system;
- the exact command or action;
- the complete error text;
- the output of `pwd`, `git status`, or `which python` when relevant; and
- what you already tried.

Use the Canvas discussion board when the answer may help the class, Canvas
Inbox for a private course matter, or bring the evidence to class or office
hours. Follow the [AI Use & Growth Mindset
Policy](../01-course-info/ai-policy.md) if you use an AI tool for tutoring or
error interpretation.

## Ready means observable

You are ready to begin P1 when you can demonstrate all of these:

- [ ] I can use `pwd`, `ls`, and `cd` to reach my P1 repository.
- [ ] `conda activate comp521` selects the course environment.
- [ ] VS Code opens `analysis.ipynb` with the `comp521` kernel.
- [ ] I can explain what `status`, `add`, `diff --staged`, `commit`, and `push`
  do.
- [ ] My saved readiness output is committed and visible on GitHub.
- [ ] The **P1 readiness** check is green.

:::{tip} Keep the loop small
During a project, work in short cycles: make one meaningful change, run the
smallest relevant check, inspect the result, then commit and push when the state
is worth keeping.
:::
