---
title: "Software Engineering Presentation"
subtitle: "COMP 521 | Fall 2026"
---

<!-- prep-banner:start -->
:::{warning} This page is still being prepared
COMP 521 begins **Tuesday, August 25**. This page is being written and revised
until then — dates, policies, and details may still change. It is published
early so you can see the shape of the course, not because it is finished.

Anything still under discussion is settled by **Monday, August 24**. After that,
what is written here is what the course does.
:::
<!-- prep-banner:end -->

# Software Engineering Presentation

**Twice** during the semester you will **teach the class** a software
engineering tool or practice — not by talking at us, but by **walking us through
it while we follow along on our own machines**.

You publish a **GitHub repository**; everyone clones it before class; you lead
the room through the demo in **12 minutes**, with **3 minutes for questions**.

You present two different topics, once in each round. Each is worth 5% of your
course grade.

:::{important} The goal is that your classmates can use it afterward
That is the whole assignment. Not "cover" a tool, not summarize its
documentation — leave five other people able to go do the thing.

This is why it is hands-on rather than a talk. Watching someone use a tool and
using it yourself are different experiences, and only one of them tends to
survive the week. By the end of your fifteen minutes, everyone in the room
should have run the thing at least once on their own laptop.

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

**1. A 12-minute guided walkthrough, plus 3 minutes of questions.**
Your classmates will have your repository open in front of them. Lead them
through it: tell them what to run, wait for them to run it, and talk about what
they are seeing.

Assume they write Python and use git and have never seen your tool. Twelve
minutes is short, and following along is slower than watching — so aim to get
everyone through **one complete useful thing**, not a tour of everything the
tool does. Your repo is what lets them go further afterward.

**2. A live demo everyone runs, not just you.**
The tool actually running — on six laptops, not one. That is a higher bar than
demoing solo, and it is the reason the repository has to genuinely work rather
than merely exist.

**Use a Jupyter notebook where the topic suits it** — testing, profiling,
benchmarking, type checking, seeds and reproducibility all demo well in a
notebook, and the notebook doubles as your written explanation.

**Some topics do not live in a notebook**, and that is fine. `git bisect`,
pre-commit hooks, CI, code review, and licensing happen in a terminal or on
GitHub — demo them there. The repository is still the deliverable either way.

**Demo on whatever makes the point best.** Use one of your own projects from
this course, write a small example from scratch, or use something you brought
from elsewhere. A previous project is often easiest, because you already know
where its problems are — but that is a convenience, not a requirement.

**3. A GitHub repository containing everything needed to follow along.**
This replaces slides and a handout — it *is* the artifact your classmates keep,
and during class it is what they are working from.

**Post the repository link at least 48 hours before your slot** so everyone can
clone it and get set up in advance. A repo that appears five minutes before
class has failed at its main job.

Its `README.md` must contain:

- a **worked example** — the actual commands and output
- **when *not* to use this** — the situation where the tool is the wrong answer,
  or where its cost exceeds its benefit

- **setup instructions** that work — what to install, how to check it worked

Beyond that, include whatever someone needs to actually run what you showed: the
notebook, the environment file, the sample data, the broken commit. Someone who
clones your repo a month from now should be able to reproduce your demo without
asking you anything.

:::{note} No slides
You do not need slides, and I would rather you did not make any. Work from the
notebook or the terminal, alongside everyone else. If something needs
explaining, put it in a markdown cell or in the README, where it stays useful
after you sit down.
:::

:::{warning} Your classmates' job
When someone else is presenting, **clone their repository and set it up before
class**. Turning up unprepared wastes the presenter's fifteen minutes and
everyone else's, and it counts against your
[Scholarly Engagement](../01-course-info/syllabus.md#sec-engagement).

If you cannot get their setup working, tell the presenter *before* class — that
is useful information for them, and it is fixable in advance rather than live.
:::

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
live demo, repository.

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

Your repository link is due **48 hours before** your slot, so your classmates
can clone and set up in advance.

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

**Test it on a clean clone.** Not your working copy — clone your own repo into
a fresh directory, follow your own setup instructions exactly, and see whether
it works. This is where most of these will break, and it is entirely
preventable.

**Keep dependencies minimal.** Every extra install is another way one person's
laptop stalls the whole room. If the demo works with the packages everyone
already has for this course, keep it that way.

**Have a fallback.** If someone's setup will not cooperate, be ready to keep
going and sort them out afterward rather than stopping the session.

**Expect questions about the boundaries.** I will ask where the tool breaks
down, what it costs, and when you would skip it. Those questions are the point.

**Aim for one thing they can do tomorrow.** If your classmates leave with a
single command they will actually run this week, that is a better outcome than a
complete survey nobody acts on.

## How this is graded

One letter for the presentation as a whole — the walkthrough, the repository,
and how you handle questions, judged together. There is no point breakdown.

| | |
|:--|:--|
| **A** | The room ran the tool and left able to use it. Your repository worked on other people's machines. You knew where the tool breaks down and said so. |
| **B** | A solid walkthrough, but some people got stuck and stayed stuck, or the setup needed hand-holding, or you could not say much about the tool's limits. |
| **C** | Mostly a demo you performed rather than one we did, or a repository that did not really work outside your own laptop. |
| **D / F** | Unprepared, or not delivered. |

The thing I am actually looking for is whether the class can use the tool
afterward. Everything else is a means to that.

## Using AI on this assignment

The [AI Use & Growth Mindset Policy](../01-course-info/ai-policy.md) applies as
it does everywhere else in this course, with two clarifications:

- **Your README and notebook prose** are presentation work, and fall under the
  same rules as documentation and formatting in your current phase.
- **If your demo uses your own project code, core-solution rules apply to it in
  full.** You may not have AI write the tests, the workflow file, or the
  annotations you are presenting — those *are* the assignment.

If you use AI to help you understand the tool, that is tutoring and it is
encouraged. Disclose it as usual.
