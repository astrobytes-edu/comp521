---
title: "Software Engineering Presentation"
subtitle: "COMP 521 | Fall 2026"
---

# Software Engineering Presentation

**Twice** during the semester you will **teach the class** a software
engineering tool or practice — a **12-minute talk** followed by **3 minutes of
questions**, built around a **live demonstration**, plus a **one-page handout**
for your classmates.

You present two different topics, once in each round. Each is worth 5% of your
course grade.

:::{important} The goal is that your classmates can use it afterward
That is the whole assignment. Not "cover" a tool, not summarize its
documentation — leave five other people able to go do the thing.

The practical test: **does someone in the room use your tool that week?** If
your talk sends one classmate off to add tests to their project on Thursday
night, it worked. If everyone nods politely and nothing changes, it did not,
however polished the slides were.

Everything below follows from that.
:::

## Why this matters

These are **software engineering** practices. They are routine in professional
software development and much less established in research computing — which is
a large part of why so much scientific code is hard to reproduce, hard to
extend, and hard to trust six months later. Most science and computing courses
never teach the tooling at all. People tend to pick it up years afterward, by
accident, from whoever they happen to sit next to.

That gap is getting more expensive, quickly. When plausible-looking code can be
generated in seconds, producing code stops being the bottleneck and
*establishing that code is correct* becomes the scarce skill. Tests, type
checks, automated runs, and review are the mechanisms for verifying work you did
not write line by line yourself — which is an increasingly large fraction of all
work. The faster code arrives, the more the infrastructure around it decides
whether you can believe any of it.

This course asks you to build things from scratch and know they are right. These
tools are how you keep knowing that when the code grows past what you can hold
in your head — or when you did not write all of it yourself.

## Why you are the one teaching it

**Teaching a tool is how you learn it properly.** You can read the `pytest`
documentation and come away feeling like you understand it. Standing in front of
five people who are going to ask you questions is a different bar entirely — you
tend to find the holes in your own understanding about an hour into preparing,
which is exactly the point.

**And it gets the class a whole toolchain instead of one tool.** Nobody picks
up a professional toolchain in a semester alone. Each of you learning two tools
well and teaching them means everyone leaves with a working map of the whole
thing — and knows who to ask about each piece.

The second round is also where the skill actually develops. You will have given
one talk, watched everyone else give theirs, and had feedback on yours. Almost
nobody's first talk is their good one.

## What you produce

**1. A 12-minute talk, plus 3 minutes of questions (15 minutes total).**
Assume your audience is your classmates: they write Python, they use git, they
have never used your tool. Twelve minutes is short — plan the talk to land at
twelve so the questions are not squeezed.

**2. A live demo.**
Not slides showing code — the tool actually running, in front of us. People
learn a tool by watching it work and then copying what they saw; a screenshot
of a terminal is not the same thing as a terminal.

**Demo on whatever makes the point best.** Use one of your own projects from
this course, write a small example from scratch, or use something you brought
from elsewhere. A previous project is often easiest, because you already know
where its problems are — but that is a convenience, not a requirement.

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

Each topic lists what it is, what a strong demo would show, and where the real
documentation lives. The demos are suggestions — if you have a better idea for
making the point, propose it.

### Testing and correctness

#### Testing with `pytest`

Automated tests that run in one command, instead of assertions you check by eye.

**Demo:** turn a set of validation checks into a real test suite. Then introduce
a bug on purpose and let the suite catch it in front of us.
**Docs:** <https://docs.pytest.org/>

#### Testing numerical code

The hard version of the above: how do you test code whose output is floating
point? Tolerances, `assert_allclose`, testing properties rather than values
(does your integrator conserve energy for *any* valid input?), and golden-file
regression tests.

**Demo:** show a test that passes for the wrong reason — a tolerance so loose it
would accept a broken implementation — then tighten it. Or write a property test
that fails on a subtly wrong algorithm.
**Docs:** <https://numpy.org/doc/stable/reference/routines.testing.html> ·
<https://hypothesis.readthedocs.io/>

#### Code review

How to read a change someone else wrote and say something useful about it — and
how that skill changes when the author is a machine and the code looks
plausible.

**Demo:** review a real diff live. Show what you check first, what you skip, and
what you would send back.
**Docs:** <https://google.github.io/eng-practices/review/>

#### Continuous integration with GitHub Actions

Tests that run automatically on every push, so a broken commit announces itself.

**Demo:** add a workflow that runs a test suite. Push something broken and show
the red X, then fix it and show it go green.
**Docs:** <https://docs.github.com/en/actions>

:::{note} Depends on the testing talk
CI runs your tests, so this is scheduled after `pytest`. If you pick it, you are
building on a classmate's talk — go see what they covered.
:::

### Code quality

#### Linting and formatting with `ruff` and pre-commit

Automatic detection of bugs, dead code, and style problems — and hooks that stop
bad code from being committed at all.

**Demo:** run `ruff` on a real codebase and show what it finds. Fix something.
Install a pre-commit hook and show it blocking a commit.
**Docs:** <https://docs.astral.sh/ruff/> · <https://pre-commit.com/>

#### Type hints and `mypy`

Annotations that document what your functions accept and return, and a checker
that verifies you meant it.

**Demo:** annotate a module. Show `mypy` catching something real — a function
that can return `None`, an array where a scalar was expected.
**Docs:** <https://mypy.readthedocs.io/>

### Debugging and performance

#### Debugging with `pdb` / `ipdb`

Inspecting a running program's state instead of adding `print` statements and
re-running.

**Demo:** find a real bug live, in the debugger, without adding a single
`print`.
**Docs:** <https://docs.python.org/3/library/pdb.html>

#### Finding regressions with `git bisect`

"It worked last week and I do not know what broke it." Binary search over your
commit history, automated.

**Demo:** take a repository where something broke, and find the exact commit
that did it — in front of us, in under two minutes.
**Docs:** <https://git-scm.com/docs/git-bisect>

#### Profiling

Finding where time actually goes, rather than where you assume it goes.

**Demo:** profile a numerical routine and find the hot spot. Make it faster.
Then show that the numbers did not change — a speedup that alters your results
is not a speedup, it is a bug.
**Docs:** <https://docs.python.org/3/library/profile.html>

#### Benchmarking honestly

Different from profiling: how to *measure* a speedup so that someone else
believes it. Warm-up runs, variance between repeats, and why timing something
once on a laptop with thirty browser tabs open means nothing.

**Demo:** show the same benchmark producing two different answers, then measure
it properly and report a number you can defend.
**Docs:** <https://docs.python.org/3/library/timeit.html> ·
<https://pytest-benchmark.readthedocs.io/> ·
<https://github.com/sharkdp/hyperfine>

### Reproducibility and sharing

#### Reproducible environments with `uv` and lockfiles

The difference between "it works on my machine" and "it works on any machine,
including mine in six months."

**Demo:** delete a virtual environment. Rebuild it from the lockfile. Show that
a computation produces identical output afterward.
**Docs:** <https://docs.astral.sh/uv/>

#### Reproducibility in practice

What "someone else can rerun this" actually requires: seeds and RNG state, where
your data came from, and a project layout that makes the entry point obvious.

**Demo:** show a stochastic result changing between runs, then pin it properly —
and explain why a global `seed()` call is not the right answer.
**Docs:** <https://numpy.org/doc/stable/reference/random/generator.html> ·
<https://the-turing-way.netlify.app/>

#### Data versioning and large files

Why the Kepler light curves do not belong in git, and what to do instead.

**Demo:** show what happens to a repository that commits large data files, then
demonstrate the alternative — `.gitignore` plus a documented fetch script, or a
tool built for it.
**Docs:** <https://git-lfs.com/> · <https://dvc.org/>

#### Licensing and citation for research software

What a `LICENSE` file actually decides, how someone cites your code, and how to
attach a permanent identifier to a release.

**Demo:** add a license and a `CITATION.cff` to a repository and show what each
one changes about how the project can be used and credited.
**Docs:** <https://choosealicense.com/> ·
<https://citation-file-format.github.io/> · <https://zenodo.org/>

## Choosing your topic

Topics are claimed in class, first come first served, one topic per person per
round — so have a backup ready. Claiming dates are announced early in the
semester.

I assign the presentation dates rather than letting you choose them, for two
reasons: some topics depend on others (CI needs testing to exist first), and
some are far more useful early than late. A testing talk in September helps
everyone for the rest of the semester; the same talk in November is a
curiosity.

## The two rounds

**Round 1** is the full treatment described above: 12 minutes, 3 for questions,
live demo, one-page handout.

**Round 2 is deliberately left open.** After watching a full round I will decide
whether the second is another 15-minute treatment or a shorter lightning talk,
depending on how round one goes and how much class time we have left. You will
know well before you have to prepare anything.

You may not present the same topic twice, and you should not pick two topics
from the same group below — the point is breadth.

## Schedule

Presentations happen at the **start of class**. Dates are announced once topics
are chosen — I assign them so that dependencies work out and the most broadly
useful tools come early.

Your handout is due to me by the start of your presentation.

## What makes these good

**Show, do not describe.** The strongest talks in this format are mostly
terminal. If your slides have more lines of code than your demo does, invert
that.

**Use a real problem.** "Here is a bug I actually had" beats "here is a bug one
might have" every time, and it is easier to talk about because you remember it.
This is the main reason people reach for a previous project — the problems in it
are already real.

**Twelve minutes is short.** You cannot cover everything a tool does, and trying
to is the most common way these talks fail. Pick the two things that would
change how your classmates work tomorrow, and go deep on those.

**Rehearse the demo.** Live demos fail. Run it start to finish at least once
beforehand, and have the commands somewhere you can paste from — nobody wants to
watch you fight a typo for ninety seconds.

**Expect questions about the boundaries.** I will ask where the tool breaks
down, what it costs, and when you would skip it. Those questions are the point.

**Aim for one thing they can do tomorrow.** If your classmates leave with a
single command they will actually run this week, that is a better outcome than a
complete survey nobody acts on.

## How this is graded

Each presentation is scored out of 100 and is worth 5% of your course grade.

| Component | Points | What earns full credit |
|:--|--:|:--|
| Technical accuracy and depth | 30 | Correct, and deeper than the tool's front page. You can answer why it works, not just what to type. |
| Live demo | 30 | The tool actually runs. The example makes the point. It is rehearsed enough that we watch the tool, not you debugging your terminal. |
| Clarity, pacing, and questions | 20 | Lands near 12 minutes. Pitched at your classmates. Handles questions honestly — "I do not know" is a fine answer, bluffing is not. |
| Handout | 20 | One page, genuinely usable afterward. Includes a worked example and a clear "when not to use this." |

The thing I am actually looking for is whether the class can use the tool
afterward. Everything in the table above is a means to that.

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
