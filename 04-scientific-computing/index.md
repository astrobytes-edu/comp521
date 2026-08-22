---
title: "Start Here: Part II Guide — Arrays, Visualization, and Reliable Computing"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
---

Part II develops the habits that turn a collection of numbers into
inspectable computational evidence. The emphasis is not on collecting APIs or
making a plot look persuasive. It is on making array operations, visual choices,
and checks visible enough that another reader can question the result.

## How to use this part

Read Chapters 7–10 in order on a first pass. The route moves from a numerical
representation, to an evidence-bearing figure, to tests of stated behavior,
and finally to a small type that protects a recurring contract. **Deep Dive**
and **Reference** sections remain available when a concrete problem demands
them; they are not hidden prerequisites for the core.

On a return visit, begin with the question that matches the problem in front of
you:

| If you are asking… | Start with… |
| --- | --- |
| “Why does this array have this shape or dtype?” | [Chapter 7: NumPy](07-numpy-fundamentals.md) |
| “What claim does this figure actually support?” | [Chapter 8: Matplotlib](08-matplotlib-fundamentals.md) |
| “How can I test this numerical behavior?” | [Chapter 9: Testing, Failure Modes, and Reproducible Scientific Code](09-robust-computing.md) |
| “Does this scientific entity need state and invariants?” | [Chapter 10: Designing Small Scientific Types](10-advanced-oop.md) |

## Chapter map

### [Chapter 7: NumPy — Arrays as Scientific Objects](07-numpy-fundamentals.md)

Shape, axes, dtype, vectorized operations, masking, broadcasting, copies and
views, and reproducible random generators. The central question is whether the
array represents the quantity you think it represents.

### [Chapter 8: Matplotlib — Visualizing Scientific Evidence](08-matplotlib-fundamentals.md)

The `Figure`/`Axes` model, labels and units, scales, uncertainty, accessible
encodings, and export. The central question is what an honest figure lets a
reader see—and what it cannot establish on its own.

### [Chapter 9: Testing, Failure Modes, and Reproducible Scientific Code](09-robust-computing.md)

Input validation, expected failures, assertions, tests, tolerances, known
solutions, convergence checks, and diagnostic logging. The central question is
what evidence supports a stated behavior of the code.

### [Chapter 10: Designing Small Scientific Types](10-advanced-oop.md)

Dataclasses, validation, invariants, readable representations, composition,
and tests for compact stateful models. The central question is whether a small
type makes a scientific assumption clearer than a loose collection of values.

## Scientific examples and transfer

Examples may use transit signals, laboratory measurements, field observations,
or simulation outputs. Their units, assumptions, and limits should be visible.
The transferable skill is always the same: inspect the representation, make a
claim proportionate to the evidence, and add a check that could expose a
mistake.

## The throughline: an evidence trail

A trustworthy scientific result has more than one checkpoint. Chapter 7 asks
whether an array has the intended shape, dtype, and values. Chapter 8 asks what
a figure lets a reader see. Chapter 9 asks what the program's tests establish.
Chapter 10 asks whether a repeated scientific assumption has a visible boundary.
Together, those questions trace an evidence trail from stored values to a claim
another reader can inspect.

## What comes next

Finish this first pass with [Part II Recap — Inspectable Scientific Evidence](synthesis.md).
[Part III: Tabular Data and Reproducible Workflows](part-3-data-workflows.md) is
in development. It will extend these habits to data provenance, tables,
cleaning decisions, exploratory analysis, and query workflows; it is not part
of this completed Part II route.
