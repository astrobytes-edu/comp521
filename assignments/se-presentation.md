---
title: "Software Engineering Presentation"
subtitle: "COMP 521 | Fall 2026"
---

# Software Engineering Presentation

Once during the semester you will teach the class one software engineering tool
or practice — a **12-minute talk** followed by **3 minutes of questions**, built
around a **live demonstration**, plus a **one-page handout** for your
classmates.

:::{important} The demo is the assignment
This is not a research talk about a tool. It is a demonstration of the tool
actually running, solving a problem you can explain.

The difference matters. Anyone can summarize the `pytest` documentation in
twelve minutes. Showing us a test catching a real bug — and explaining why it
caught it — requires you to have used the thing.
:::

## Why this exists

This course description promises software engineering practice: testing,
version control, documentation, reproducible research. The readings cover the
*principles* — contracts, invariants, validation-first development, the
reproducibility contract.

What they do not cover is the **tooling**. You are told to make your work
reproducible; nobody shows you a lockfile. You are told to validate your
results; nobody shows you a test suite that runs on every push.

That gap is what these presentations fill. Six people each learn one tool
properly and teach it to the other five — which is both a faster way to cover
eight tools than lecturing about them, and a considerably better way to learn
the one you present.

## What you produce

**1. A 12-minute talk, plus 3 minutes of questions (15 minutes total).**
Assume your audience is your classmates: they write Python, they use git, they
have never used your tool. Twelve minutes is short — plan the talk to land at
twelve so the questions are not squeezed.

**2. A live demo.**
Not slides showing code — the tool actually running, in front of us.

**3. A one-page handout.**
One page. It must contain:

- a **worked example** — the actual commands and output
- **when *not* to use this** — the situation where the tool is the wrong answer,
  or where its cost exceeds its benefit

Everything else on the page is up to you. Most people will want the three or
four commands that matter and a link to the real documentation.

:::{tip} Why "when not to use this" is required
It is the fastest way to tell the difference between someone who used a tool and
someone who read about one. Every tool has a regime where it is a waste of time.
If you cannot name that regime, you have not used it enough to teach it.
:::

## Topics

Each topic below is paired with what a strong demo would show. These are
suggestions, not requirements — if you have a better demo idea for your project,
propose it.

### Testing with `pytest`

Automated tests that run in one command, instead of assertions you check by
eye.

**Demo:** turn a set of validation checks into a real test suite. Then introduce
a bug on purpose and let the suite catch it in front of us.

### Linting and formatting with `ruff` and pre-commit

Automatic detection of bugs, dead code, and style problems — and hooks that stop
bad code from being committed at all.

**Demo:** run `ruff` on a real codebase and show what it finds. Fix something.
Install a pre-commit hook and show it blocking a commit.

### Reproducible environments with `uv` and lockfiles

The difference between "it works on my machine" and "it works on any machine,
including mine in six months."

**Demo:** delete your virtual environment. Rebuild it from the lockfile. Show
that a computation produces identical output afterward.

### Continuous integration with GitHub Actions

Tests that run automatically on every push, so a broken commit announces itself.

**Demo:** add a workflow that runs your test suite. Push something broken and
show the red X, then fix it and show it go green.

:::{note} Depends on the testing talk
CI runs your tests, so this topic is scheduled after `pytest`. If you pick it,
you are building on your classmate's talk — go see what they covered.
:::

### Profiling and performance measurement

Finding where time actually goes, rather than where you assume it goes.

**Demo:** profile a numerical routine and find the hot spot. Make it faster.
Then show that the numbers did not change — a speedup that alters your results
is not a speedup, it is a bug.

### Debugging with `pdb` / `ipdb`

Inspecting a running program's state instead of adding `print` statements and
re-running.

**Demo:** find a real bug live, in the debugger, without adding a single
`print`.

### Type hints and `mypy`

Annotations that document what your functions accept and return, and a checker
that verifies you meant it.

**Demo:** annotate a module. Show `mypy` catching something real — a function
that can return `None`, an array where a scalar was expected.

### Data versioning and large files

Why the Kepler light curves do not belong in git, and what to do instead.

**Demo:** show what happens to a repository that commits large data files, then
demonstrate the alternative — `.gitignore` plus a documented fetch script that
reproduces the dataset from scratch.

## Choosing your topic

Pick your topic **in class on Thursday, September 3**. First come, first served;
one topic per person, so have a second choice ready.

I assign the presentation dates rather than letting you choose them, for two
reasons: some topics depend on others (CI needs testing to exist first), and
some are far more useful early than late. A testing talk in September helps
everyone for the rest of the semester. The same talk in November is a curiosity.

## Schedule

Presentations happen at the **start of Thursday class**, one per week:

| Week | Date |
|:--|:--|
| 4 | Thu **Sep 17** |
| 5 | Thu **Sep 24** |
| 6 | Thu **Oct 1** |
| 7 | Thu **Oct 8** |
| 8 | Thu **Oct 15** |
| 9 | Thu **Oct 22** |

Your handout is due to me by the start of your presentation.

## What makes these good

**Show, do not describe.** The strongest talks in this format are mostly
terminal. If your slides have more lines of code than your demo does, invert
that.

**Use a real problem.** "Here is a bug I actually had" beats "here is a bug one
might have" every time, and it is easier to talk about because you remember it.

**Twelve minutes is short.** You cannot cover everything a tool does, and trying
to is the most common way these talks fail. Pick the two things that would
change how your classmates work tomorrow, and go deep on those.

**Rehearse the demo.** Live demos fail. Run it start to finish at least once
beforehand, and have the commands somewhere you can paste from — nobody wants to
watch you fight a typo for ninety seconds.

**Expect questions about the boundaries.** I will ask where the tool breaks
down, what it costs, and when you would skip it. Those questions are the point.

## Using AI on this assignment

The [AI Use & Growth Mindset Policy](../01-course-info/ai-policy.md) applies as
it does everywhere else in this course, with two clarifications:

- **Slides and handout wording** are presentation work, and fall under the same
  rules as documentation and formatting in your current phase.
- **If your demo uses your own project code, core-solution rules apply to it in
  full.** You may not have AI write the tests, the workflow file, or the
  annotations you are presenting — those *are* the assignment.

If you use AI to help you understand the tool, that is tutoring and it is
encouraged. Disclose it as usual.
