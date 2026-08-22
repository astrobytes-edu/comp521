---
title: "Part I Recap — Trustworthy Scientific Programming"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
---

## Your code is a scientific instrument

Scientific code mediates between a model, data, and a conclusion. A calculation
that runs is therefore not enough: another reader must be able to identify its
environment, numerical assumptions, algorithmic decisions, and interpretation.
Part I supplies the first tools for that work.

## A return route, not another chapter

Use this page after a first pass through Chapters 1–6, or return when a result
is difficult to trust. It does not introduce a second set of techniques to
memorize. Instead, it helps you identify the first assumption worth inspecting:
the environment, the numerical representation, the control logic, the data
representation, the function contract, or the boundary around shared state.

## Six chapters, one architecture

| Chapter | What it helps you establish |
|---|---|
| [1. Environments](01-python-environment.md) | which code and dependencies actually ran |
| [2. Numerical reality](02-python-calculator.md) | which numerical comparisons and representations are defensible |
| [3. Control flow](03-python-control-flow.md) | what decisions and termination conditions define the algorithm |
| [4. Data structures](04-python-data-structures.md) | how data is organized and accessed |
| [5. Functions and modules](05-python-functions-modules.md) | what a reusable calculation promises |
| [6. Small scientific objects](06-oop-fundamentals.md) | when state and behavior should be protected together |

## Diagnostic and transfer guide

| Symptom | Likely cause | Next check | Relevant chapter |
|---|---|---|---|
| The same code behaves differently elsewhere | different interpreter, package, path, or hidden state | record `sys.executable`, versions, and a clean rerun | [1](01-python-environment.md) |
| Two nearly identical values compare unequal | finite floating-point representation | choose a claim-appropriate absolute and relative tolerance | [2](02-python-calculator.md) |
| A calculation never finishes | missing progress condition or unbounded loop | state the invariant, tolerance, and maximum iteration count | [3](03-python-control-flow.md) |
| A once-small task becomes slow | data structure does not match the access pattern | count operations and inspect lookup/mutation behavior | [4](04-python-data-structures.md) |
| A result cannot explain its assumptions | an unclear or oversized function contract | name inputs, units, output, validity range, and failures | [5](05-python-functions-modules.md) |
| Related values drift out of agreement | no explicit invariant around shared state | consider a small validated object—or a simpler function/data pair | [6](06-oop-fundamentals.md) |

## Transfer prompt

Choose one computation from your own discipline. Before changing its algorithm,
write a short instrument record: interpreter and package versions, input units,
one limiting case, the stopping rule if it iterates, and the observable that
would count as evidence against its result. This record should make sense to a
reader outside the original domain.

## Recap and next connection

Part I is not a checklist to finish once. Return when a computation is hard to
trust, then use the relevant chapter as a diagnostic reference. Next, continue
to [Part II: Arrays, Visualization, and Reliable Computing](../04-scientific-computing/index.md),
where these habits become tools for inspecting arrays, figures, numerical
behavior, and small scientific types. Part II assumes these foundations; it
does not replace the environment, numerical, or contract checks established
here.
