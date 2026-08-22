---
title: "Part II Recap — Inspectable Scientific Evidence"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
---

## One result, several checkpoints

Part II treats a numerical result as an evidence trail rather than a number
that becomes trustworthy merely because code produced it. An array represents
quantities with a shape, dtype, and indexing convention. A figure makes a
selected relationship visible. A test checks stated behavior under stated
conditions. A small type makes a recurring invariant or unit boundary visible
where values enter a program.

These are connected checks, not four competing programming styles. A light
curve, simulation output, laboratory series, or field observation can need all
four: a sound representation, an honest visual argument, a behavioral check,
and a clearly limited contract for the values that move through the analysis.

## A return route, not another chapter

Use this recap after Chapters 7–10 or when a result needs diagnosis. It does
not add a hidden requirement beyond the completed route. Start from the
question that most closely resembles the uncertainty in front of you, then
return to the chapter for the full explanation and examples.

| If you notice… | First question to ask | Return to… |
| --- | --- | --- |
| a surprising mean, mask, or broadcast result | What do the array's shape, axes, dtype, and missing values represent? | [Chapter 7](07-numpy-fundamentals.md) |
| a persuasive-looking plot | What quantities, units, scale, uncertainty, and comparison make the visual claim warranted? | [Chapter 8](08-matplotlib-fundamentals.md) |
| code that runs but is hard to trust | Which stated behavior, edge case, known solution, or convergence trend could expose an error? | [Chapter 9](09-robust-computing.md) |
| repeated values whose meaning drifts across functions | Is there a small invariant, unit boundary, or meaningful operation that deserves an explicit type? | [Chapter 10](10-advanced-oop.md) |

## Transfer prompt: trace a claim backward

Choose one figure or numerical conclusion from your own work. Write four short
notes: what the stored values represent; what the visual or numerical result
shows; what behavior you have tested; and which assumption would be worth
making explicit in a function or small type. If a note is missing, you have
found a productive next check—not evidence that the result is already wrong.

## Next connection

Part III will extend this evidence trail from one array or measurement to a
collection of records, their schemas, quality decisions, and provenance. It is
[in development](part-3-data-workflows.md), so it is not a prerequisite for the
completed Parts I–II route. For a difficult foundational question, return to
[Part I Recap — Trustworthy Scientific Programming](../03-python/synthesis.md).
