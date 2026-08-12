---
title: "Part 1: Python Fundamentals"
subtitle: "Scientific Computing with Python | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is still being revised
Readings are reviewed and finalized **at least one week before they are
assigned**, so you will always have a settled version before you need it. Until
then, expect rough edges — wording, examples, and cross-references may change.

Where a reading disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
:::
<!-- prep-banner:end -->

## Your Computational Toolkit for Scientific Computing

Welcome to the Python Fundamentals module. This is not "learn Python syntax." This is **learn to think computationally and build trustworthy scientific code**.

You already know how to write code that *runs*. What this sequence of chapters teaches is how to write code that you can **trust**, **extend**, and **reason about six weeks later when you've forgotten what you were thinking**.

These chapters are written to be **used**, not memorized. You'll come back to them when your code is slow, confusing, wrong-but-not-crashing, or hard to extend (which is… most real science code).

:::{important} 🚫 Course Policy: No Jupyter Notebooks

All code in this course runs as **scripts** (`.py` files) executed in **IPython** or the terminal. Notebooks hide state, break reproducibility, and teach bad habits. See [Chapter 1](01-python-environment.md) for the full rationale and workflow.

**Your workflow:** Write `.py` files $\to$ Run in IPython (`%run script.py`) $\to$ Iterate $\to$ Commit to Git.
:::

---

## Why This Module Exists

Computational science fails far more often from *structure* problems than from syntax problems. Results are wrong because environments drift, state leaks, numerical assumptions are violated, or a small design choice quietly turns an O(n) operation into O($\mathrm{n}^{2}$). Chapters 1–6 exist to give you a mental framework for avoiding those failures.

**Think of this module as teaching you how to *build a laboratory*, not how to use a calculator.**

### From "It Runs" to "I Trust It"

[Chapter 1](01-python-environment.md) starts with environments and workflows because nothing else matters if you don't know **what code you're actually running**. If two students get different answers from the same script, or your code breaks when you move from your laptop to the cluster, that's not a programming problem — it's a reproducibility failure. By the end of Chapter 1, you should understand where Python is coming from, how packages are resolved, and why isolation (conda environments) is non-negotiable for real science.

Once you know *where* your code lives, [Chapter 2](02-python-calculator.md) forces you to confront a harder truth: computers don't do math the way humans do. Floating-point arithmetic is approximate, precision is finite, and naive numerical expressions can fail catastrophically without throwing errors. This chapter exists because many scientific disasters were caused by code that looked correct and ran without complaint. If you take nothing else from it, remember this: **numerical correctness is an active responsibility, not a default behavior**.

### Teaching the Computer to Think (Without Fooling It)

[Chapter 3](03-python-control-flow.md) is where we slow down and talk about *logic*. Control flow is not about syntax — it's about making your reasoning explicit. Writing pseudocode before you write Python is how you catch infinite loops, missing termination conditions, and logic that only works by accident. The patterns introduced here — accumulation, filtering, searching, convergence — appear in every simulation, every solver, and every data analysis pipeline you will ever write.

Then [Chapter 4](04-python-data-structures.md) zooms out and asks a question most beginners never ask soon enough: **how does this scale?** Lists, dictionaries, and sets aren't interchangeable containers; they encode assumptions about access patterns, uniqueness, and performance. Choosing the wrong data structure doesn't make your code slightly slower — it can make a problem fundamentally intractable. This chapter exists so that when your simulation slows to a crawl, you know *why*, and you know where to look.

### From Scripts to Systems

By the time you reach [Chapter 5](05-python-functions-modules.md), you've written enough code that repetition becomes painful. Functions are introduced not just as reusable blocks, but as *contracts*: given valid input, they promise correct output, without side effects or surprises. Scope rules, default arguments, and namespaces matter here because small mistakes quietly couple parts of your code that should be independent. Chapter 5 is where you start writing code that other people — including future you — can safely reuse.

[Chapter 6](06-oop-fundamentals.md) completes the arc by introducing object-oriented thinking. This is not about "using classes because Python has classes." It's about modeling **entities that have state and behavior**. When data and the operations on that data are inseparable — particles, observations, simulations, instruments — objects reduce cognitive load and prevent entire classes of bugs. Properties and validation exist here to enforce physical constraints *at the moment they are violated*, not weeks later during analysis.

Importantly, Chapter 6 also teaches restraint. Not everything should be a class. Knowing *when not to use OOP* is as important as knowing how to use it.

---

## The Throughline: Defensive Scientific Programming

Across all six chapters, a few ideas keep reappearing:

- **Make state explicit.** Don't let variables drift or hide.
- **Validate assumptions early.** Fail fast with clear messages.
- **Prefer clarity over cleverness.** Tomorrow-you is your first collaborator.
- **Choose abstractions that match the physics, not the syntax.** Data structures should reflect the problem.
- **Design first, then implement.** Pseudocode before Python.

These are not Python rules. They are **computational science rules**.

You are learning how to write code that can survive:

- different machines
- long runtimes
- collaborators
- future extensions
- and your own imperfect memory

**That is the real goal of Python Fundamentals.**

---

## Chapter-by-Chapter Guide

### [Chapter 1 — Computational Environments & Scientific Workflows](01-python-environment.md)

You learn how to *control your computing universe*:

- IPython as your computational lab
- how imports work (and why "it works on my machine" happens)
- reproducible environments (`conda`, dependency sanity)
- debugging environments systematically

**When to revisit:** ModuleNotFoundError, wrong Python, weird version issues, "it worked yesterday."

### [Chapter 2 — Python as Your Scientific Calculator](02-python-calculator.md)

You learn how computers represent numbers, and how scientific results go wrong:

- floating-point reality (IEEE 754)
- safe comparisons (`math.isclose`)
- numerical hazards (cancellation, overflow/underflow)
- defensive numerical checks

**When to revisit:** convergence tests, tolerance decisions, weird rounding, "why is 0.1 cursed?"

### [Chapter 3 — Control Flow & Logic](03-python-control-flow.md)

You learn to design algorithms that don't rely on hope:

- pseudocode as a real design tool
- boolean logic + short-circuiting
- guard clauses, loops, convergence patterns
- debugging control flow (prints, assertions used correctly, sanity checks)

**Why this one matters:** internalizing Chapter 3 is when you stop writing "Python that runs" and start designing **algorithms that work**.

### [Chapter 4 — Data Structures: Organizing Scientific Data](04-python-data-structures.md)

You learn how code scales (or doesn't):

- choosing between list/tuple/dict/set based on access pattern
- Big-O *as scaling intuition* (not trivia)
- memory layout, mutability, aliasing bugs
- caching, lookup tables, time–space tradeoffs

**When to revisit:** slow code, massive datasets, "why is this O($\mathrm{n}^{2}$)?", mysterious mutation bugs.

### [Chapter 5 — Functions & Modules: Building Reusable Scientific Code](05-python-functions-modules.md)

You learn how to turn scripts into tools:

- function contracts: inputs/outputs/units/failure modes
- argument design (keyword-only, defaults, *args/**kwargs)
- scope + namespaces (LEGB, avoiding global state)
- modular organization: building reusable libraries
- documentation + testing as scientific integrity tools

**When to revisit:** repeated code, unclear logic, messy scripts, "why did this variable change?"

### [Chapter 6 — OOP Fundamentals: Organizing Scientific Code](06-oop-fundamentals.md)

You learn when (and when **not**) objects help:

- stateful scientific entities (particles, instruments, datasets)
- invariants via properties + validation
- instance vs class attributes
- Pythonic special methods (`__repr__`, `__str__`, etc.)
- the crucial judgment: **objects vs functions**

**When to revisit:** you're passing too many related values around, or state bugs are multiplying.

---

## Quick Navigation Guide

| "I need to…" | Go to… | Look for… |
|--------------|--------|-----------|
| Fix import / environment problems | Ch 1 | Import system, diagnostics |
| Compare floats safely | Ch 2 | `math.isclose`, tolerances |
| Design a loop that converges | Ch 3 | Convergence pattern, guard clauses |
| Speed up lookups / membership tests | Ch 4 | dict/set O(1), access patterns |
| Stop copy/pasting code | Ch 5 | function contracts, modules |
| Bundle data + behavior safely | Ch 6 | properties, invariants, state |

---

## The Core Habits We're Building

### 1) Defensive Programming (correctness first)

- validate inputs early
- fail fast with clear error messages
- make invalid states hard to represent

### 2) Numerical Honesty (science first)

- tolerate floating-point reality
- use stability-aware formulas
- don't trust equality checks for floats

### 3) Traceability (Git + reproducibility)

- commit meaningful steps
- push early and often
- treat your repo as a scientific record

### 4) Scaling Intuition (performance-aware)

- recognize O($\mathrm{n}^{2}$) traps early
- choose data structures based on access patterns
- measure before guessing

---

## Your Reference Checklist

By mid-semester, you should be able to:

- [ ] run everything in **scripts** (not notebooks) with reproducible results
- [ ] explain why "same code, different answer" happens and how to debug it
- [ ] design algorithms using pseudocode + invariants + guard clauses
- [ ] choose data structures that scale beyond toy problems
- [ ] write functions with clear contracts (units, assumptions, failure modes)
- [ ] organize code into modules you can reuse across projects
- [ ] decide when objects help and when they're unnecessary

---

## How to Use This Going Forward

You are not expected to memorize this module, and you are not expected to master it all at once. You will return to these chapters later in the course — often after Project 2 or Project 3 — with better context and sharper questions. When something breaks, slows down, or behaves strangely, this module is where you diagnose *why*.

If you treat Chapters 1–6 as a **reference and a mindset** rather than a checklist, they will quietly make everything else in the course easier, more reliable, and more intellectually honest.

---

## What's Next

After these six chapters, the course can move faster because you have a shared toolkit. Next modules will lean heavily on:

- NumPy arrays (performance + vectorization)
- plotting and interpretation
- numerical solvers and modeling workflows
- structured projects with reusable code

---

**Ready to build your toolkit?** Start with [Chapter 1: Computational Environments & Scientific Workflows](01-python-environment.md) $\to$

*These chapters are your companions throughout the course. Bookmark them, return often, and use them actively as you solve real problems.*
