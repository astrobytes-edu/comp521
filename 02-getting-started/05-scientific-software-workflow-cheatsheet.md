---
title: "COMP 521 — Scientific Software Workflow Cheatsheet"
subtitle: "Read this before every coding session"
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

**Read this before every coding session. Keep it open while you work.**

This course treats software engineering as part of the *scientific method*. The goal is not “code that runs,” but **code you can trust**.

---

## The Prime Rule

:::{important} The keyboard is the last step, not the first
If you start coding without a plan, you are choosing longer debugging later.
:::

## 1. Pre-Coding Contract (Required Before Writing Code)

Before you write *any* new function or module, answer these in writing (comment, notes file, or planning doc — anywhere visible):

### Inputs

- Type(s):
- Units:
- Valid range(s):
- Scalar or array?

### Outputs

- Type(s):
- Units:
- Shape / format:

### Edge Cases / Failure Modes

- What inputs should raise errors?
- What values are physically or numerically invalid?

### One Invariant (Sacred Rule)

- Something that must *never* silently change (e.g., units, coefficients, reference values)

### Validation Checks

- One anchor value (from paper / known result)
- One trend (what must increase/decrease?)
- One limiting case (behavior at boundaries)

If you cannot fill this out in ~15 minutes, you are not ready to code yet.

## 2. The Three Kinds of Evidence (Do Not Confuse Them)

Each tool answers a *different* question:

**Validation** (`python run.py validate`)  
$\to$ *Does the science make sense?* (anchor values, trends, limiting cases)

**Tests** (`python run.py test`)  
$\to$ *Does the code meet its contract?* (error handling, shape, behavior)

**Plots** (`python run.py make-figures`)  
$\to$ *Where is it going wrong?* (diagnostics, sanity checks, visualization)

A plot that “looks right” is not proof.  
A passing test suite is not scientific validation.  
You need all three.

```{mermaid}
flowchart LR
    S["Spec"] --> C["Contract"]
    C --> V["Validate<br/>(scientific evidence)"]
    V --> T["Test<br/>(behavioral evidence)"]
    T --> P["Plot<br/>(diagnostic evidence)"]
    P --> I["Iterate"]
    I --> S
```

## 3. Reproducibility Contract (Non-Negotiable)

Your project must run for someone who has never met you.

- One-command entrypoint: `python run.py <command>`
- Deterministic by default (fixed seeds unless overridden)
- No prompts or hidden manual steps; submitted notebooks run top to bottom from
  a clean kernel
- Separate concerns:
  - `validate` $\to$ fast scientific checks
  - `test` $\to$ automated contract checks
  - `make-figures` $\to$ plots only

If it only works “on your laptop,” it does not work.

## 4. Tiered Expectations (Know What “Good” Means)

### Bronze (minimum pass)

- Clean `run.py` workflow
- $\ge 3$ real validation checks
- Deterministic, non-interactive runs

### Silver (strong submission)

- Tests enforce contracts and error handling
- Clear module separation
- Validation catches at least one real bug during development

### Gold (professional-grade)

- Single source of truth for constants and formulas
- Plots used *during* development, not just at the end
- Willingness to delete and rewrite after validation

Aim high — but do not freeze trying to be perfect.

## 5. Debugging Ladder (Use in Order)

When something is wrong:

1. Can you reproduce it with one specific input?
2. Can you say a hypothesis in one sentence?
3. Can you write one small check to test that hypothesis?
4. Still stuck after ~30 minutes?
   - Walk away **or**
   - Rewrite the function cleanly using what you now know

Do not thrash. Debugging is hypothesis testing.

## 6. Permission to Delete (Use Git First)

If code is ugly, tangled, or fighting you:

```bash
git add -A
git commit -m "WIP: saving before rewrite"
```

Then delete and rewrite.

Code is cheap. Your time and sanity are not.

## Final Reminder

:::{important}
**Assume your code is wrong.**  
Prove otherwise with validation, tests, and plots.

That is what professional scientific computing looks like.
:::
