---
title: "AI Policy"
subtitle: "COMP 521 | Fall 2026"
---

# AI Policy

Read this page carefully. It is not boilerplate.

## The reasoning

You are learning to implement algorithms so that you understand them. An AI
assistant can produce a working Runge–Kutta integrator in four seconds. If you
let it, you will finish this course with a repository full of correct code and
no ability to tell whether the next piece of code you are handed is correct.

That is the specific failure this policy exists to prevent. The restrictions
loosen as the semester progresses, because the risk changes: early on, the
algorithm *is* the lesson. Later, the algorithm is a tool and the science is the
lesson.

:::{important} The standard that applies all semester
You must be able to explain every line you submit — what it does, why it is
there, and what would break if it were removed. I will ask. This holds in every
phase below, including Phase 3.
:::

## Phase 1 — Projects 1–2 (Weeks 1–4)

**Permitted:** documentation lookup, conceptual questions ("what is a stack
frame?"), language syntax questions.

**Not permitted:** generating implementations of course algorithms, debugging
your code, writing your memos.

Build the understanding from scratch. This is the phase where the difficulty is
the point.

## Phase 2 — Projects 3–4 (Weeks 5–8)

**Additionally permitted:** debugging support, *after* 30 minutes of documented
independent effort.

"Documented" means a note in your commit message or lab notebook describing what
you tried and what you observed. You must understand and be able to reproduce
any fix you accept.

**Still not permitted:** generating algorithm implementations, writing memos.

## Phase 3 — Projects 5–6 and Final (Weeks 9–15)

**Additionally permitted:** boilerplate generation, plotting code, refactoring
suggestions, performance optimization.

**Still not permitted:** generating the core algorithm implementations that a
project is assessing, and writing your memos. Your Research and Growth memos are
your own thinking, always.

## Disclosure

Every project includes an `AI_USE.md` file. Record:

- which tools you used,
- what you asked them for,
- what you accepted and what you rejected.

Honest disclosure of heavy use is not penalized. Undisclosed use is an academic
integrity violation. I care much more about your calibration than your purity —
a student who writes "I asked Claude to explain why my Newton solver diverged,
then implemented the bracketing fix myself" is doing exactly what I want.

## A note on what these tools are bad at

They are confidently wrong about numerical analysis. They will hand you an
integrator that looks right and silently loses second-order accuracy. They will
"fix" a stability problem by shrinking the timestep instead of changing the
method. Verifying that requires the understanding this course is building — so
in a real sense, the skill you are learning here is the one that makes these
tools safe to use later.
