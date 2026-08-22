---
title: "Start Here: Part I Guide — Foundations for Scientific Programming"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
---

Part I develops the habits that make a scientific calculation inspectable: know
which interpreter ran it, state numerical assumptions, make algorithmic logic
explicit, choose data structures deliberately, and give reusable code a clear
contract.

## How to use this part

Read the numbered chapters in order on a first pass. Their examples differ, but
they share one habit: make an assumption visible, inspect what the program
actually did, and revise the claim when the evidence demands it. **Deep Dive**
and **Reference** sections preserve useful detail for the moment when you have
a concrete need; they are not a second hidden prerequisite sequence.

### First reading

Read [Chapter 1](01-python-environment.md) through
[Chapter 6](06-oop-fundamentals.md) in order. Chapter 6 completes the first
pass by asking when shared state and behavior need an explicit boundary; that
question returns in Part II when Chapter 10 develops small scientific types.

| Chapter | Central question | Return when… |
|---|---|---|
| [1. Computational environments](01-python-environment.md) | Which Python and package versions produced this result? | an import, version, or notebook result differs between machines |
| [2. Python as a scientific calculator](02-python-calculator.md) | What numerical claim can this computation support? | a value rounds oddly, overflows, or fails an equality check |
| [3. Control flow and logic](03-python-control-flow.md) | What precisely makes this algorithm stop or choose a path? | a loop does not terminate or a condition silently skips cases |
| [4. Data structures](04-python-data-structures.md) | What access pattern does this data representation promise? | mutation, lookup, or scaling behavior is surprising |
| [5. Functions and modules](05-python-functions-modules.md) | What does this computation promise about inputs, outputs, and failure? | code is duplicated or a result’s assumptions are unclear |
| [6. Small scientific objects](06-oop-fundamentals.md) | Does state belong with the operations that maintain it? | related values travel together and invariants are being lost |

### Return visit

Use the chapters diagnostically rather than memorizing them. A result that
changes across machines belongs in Chapter 1; an uncertain tolerance belongs in
Chapter 2; a non-terminating loop belongs in Chapter 3; an unexpectedly slow
lookup belongs in Chapter 4; and a computation with unclear assumptions belongs
in Chapter 5.

## The throughline: defensive scientific programming

Computational science fails as often from structure as from syntax: an
environment drifts, hidden state changes an analysis, a numerical assumption is
unstated, or a data representation does not match the question. These chapters
treat code as an instrument for reasoning.

- Make state and assumptions explicit.
- Validate inputs and limiting cases early.
- Prefer clarity over cleverness.
- Choose abstractions that fit the problem, not the language feature.
- Design the logic before implementing it.

These are computational-science habits, not Python trivia. They make work
portable across scientific domains: a transit-depth calculation, a climate
model, an image-processing pipeline, or a laboratory calibration all need an
environment record, named quantities, explicit stopping rules, and interpretable
code.

## Core habits to carry forward

| Habit | What it protects | Where to build it |
|---|---|---|
| Reproducible environments | accidental interpreter and dependency drift | Chapter 1 |
| Numerical honesty | unsupported precision and fragile comparisons | Chapter 2 |
| Explicit control flow | hidden branches and unbounded iteration | Chapter 3 |
| Scaling intuition | inappropriate lookup and mutation patterns | Chapter 4 |
| Function contracts | ambiguous inputs, units, and failure modes | Chapter 5 |
| Useful state | invalid or disconnected scientific entities | Chapter 6 |

## Next connection

Finish the first pass with [Part I Recap — Trustworthy Scientific Programming](synthesis.md).
Then continue to [Part II: Arrays, Visualization, and Reliable Computing](../04-scientific-computing/index.md),
where the same reliability habits become tools for inspecting arrays, figures,
numerical behavior, and small scientific types.
