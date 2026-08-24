---
title: "Getting Started"
subtitle: "Your COMP 521 computational workspace"
author: "Anna Rosen"
---

This module gets one complete scientific-computing loop working on your own
computer: navigate to a project, activate its Python environment, run a
notebook, and save the result with Git.

:::{note} Classroom50 access
COMP 521 uses Classroom50, not GitHub Classroom. Use the Project 1 invitation
posted in Canvas and follow the course-specific directions it provides; do not
rely on screenshots or instructions from a different course.
:::

## Your first 10-minute success

Before installing anything, establish one small success in the terminal. Open
the course terminal described in Chapter 1 and run:

```bash
pwd
cd ~
mkdir -p comp521_cli_practice/terminal-practice
cd comp521_cli_practice/terminal-practice
pwd
```

Success means the final command prints a path ending in
`comp521_cli_practice/terminal-practice`. You have not installed software or
changed a course repository; you have simply proved that you can navigate a workspace.
Chapter 1 explains each command and gives you a longer practice task.

## What to read, and when

### Complete before class Thursday

Set aside **about two hours** for this route. Allow **up to three hours** if you
are installing software from scratch or encounter a network delay. Start early
enough to ask for help before you need Python and Jupyter in class.

::::{grid} 1 1 3 3

:::{card} 1. Command line
:link: 01-cli-intro.md

Learn the small set of terminal commands needed to find and run a project.
**About 25 minutes.**
:::

:::{card} 2. Software setup
:link: 02-software-setup.md

Install Miniforge and VS Code, create the `comp521` environment, and run a
local notebook check. **About 45–75 minutes from scratch.**
:::

::::

### Complete by Friday night

:::{card} 3. Git and Classroom50
:link: 03-git-intro.md

Accept and clone your assigned Project 1 repository, then push the required
README setup commit. **About 35–50 minutes after setup.**
:::

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

## The Project 1 Repository Check

**Due Fri Aug 28 at 11:59 pm PT.** This completion-only check verifies that you
can use Classroom50 and push to your assigned repository. It does not assess
Project 1 progress or Python skill.

1. Follow the Project 1 invitation in Canvas and obtain your assigned
   Classroom50 repository.
2. Clone that repository and change into its directory.
3. In `README.md`, change the repository-check box from `[ ]` to `[x]`.
4. Stage that README change, inspect it, commit, and push:

   ```bash
   git status
   git add README.md
   git diff --staged
   git commit -m "Complete Project 1 repository check"
   git push
   ```

5. Open your P1 repository on GitHub and confirm that the commit is visible.

The complete repository-check contract and due date live on the
[Projects page](../01-course-info/projects.md#sec-p1-repository-check).

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
- the output of `pwd`, `git status`, `which python`, or
  `python -c "import sys; print(sys.executable)"` when relevant; and
- what you already tried.

Use the Canvas discussion board when the answer may help the class, Canvas
Inbox for a private course matter, or bring the evidence to class or office
hours. Follow the [AI Use & Growth Mindset
Policy](../01-course-info/ai-policy.md) if you use an AI tool for tutoring or
error interpretation.

## Ready means observable

Your laptop is ready for Thursday when you can demonstrate all of these:

- [ ] I can use `pwd`, `ls`, and `cd` to navigate a practice directory.
- [ ] `conda activate comp521` selects the course environment.
- [ ] VS Code can run a local notebook with the `comp521` kernel.

Your repository check is complete Friday when your locally created README commit
is visible in your assigned Project 1 repository on GitHub.

:::{tip} Keep the loop small
During a project, work in short cycles: make one meaningful change, run the
smallest relevant check, inspect the result, then commit and push when the state
is worth keeping.
:::
