---
title: "ND Array Evidence Check"
subtitle: "Individual graded assessment | Week 2"
kernelspec:
  name: python3
  display_name: Python 3
---

# ND Array Evidence Check

## Purpose

Show that you can read, manipulate, check, and communicate a two-dimensional
scientific record. This is an individual assessment. It is recorded as a
specific piece of evidence for Scholarly Engagement; it does not create a new
course-grade category.

Do not use Project 1 code or data. This is a different, small data record.

## What you submit

Submit one executed notebook, `nd_array_evidence_check.ipynb`, to the
designated Canvas assignment. It must run top to bottom from a fresh kernel.

Your notebook needs short Markdown headings for each task, visible code and
output, one figure, and your written interpretation. Do not submit a screenshot
of code or an unexecuted notebook.

## Shared record

Rows are targets. Columns are observation times in days. The values are
synthetic normalized fluxes.

```{code-cell} python
import numpy as np

target_labels = np.array(["P", "Q", "R"])
time_days = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
flux_by_target = np.array([
    [1.000, 0.996, 0.989, 0.997, 1.002],
    [0.972, 0.970, 0.958, 0.971, 0.973],
    [1.018, 1.015, 1.004, 1.016, 1.019],
])

print("targets:", target_labels)
print("times (days):", time_days)
print("flux shape:", flux_by_target.shape)
print(flux_by_target)
```

## Tasks

### 1. State the representation

In prose, state the meaning of:

- axis `0`;
- axis `1`;
- `flux_by_target.shape`; and
- `flux_by_target[1, 2]`.

Then write code that confirms the shape and `ndim` of `flux_by_target`.

### 2. Select without guessing

Write code and show its output for:

- all five fluxes for target `Q`;
- the fluxes of all three targets at day `2.0`; and
- the single value for target `Q` at day `2.0`.

For each result, state its shape and what the remaining position or positions
mean.

### 3. Normalize one target at a time

Use the first observation of each target as that target’s baseline. Construct a
baseline array with an explicit length-one time axis, then normalize the full
array.

Your notebook must include checks equivalent to:

```python
assert normalized_flux.shape == flux_by_target.shape
assert np.allclose(normalized_flux[:, 0], 1.0)
```

Explain why a baseline with shape `(3,)` is not sufficient for this expression
and why `(3, 1)` is.

### 4. Reduce one stated axis

Compute:

- one mean normalized flux per target; and
- one mean normalized flux per observing time.

For each computation, state which axis was reduced, the result shape, and what
one value in the result represents.

### 5. Make one inspectable figure

Plot normalized flux for one target against `time_days` using Matplotlib.

Your figure must have:

- an x-axis label with units;
- a y-axis label;
- a legend entry that identifies the target;
- markers for the discrete values; and
- a title that says what the figure shows without making a discovery claim.

Save the figure as a file and display it in the notebook.

### 6. Make a bounded claim

Write three short sentences:

1. what the figure shows directly;
2. what the labeled axes, markers, and legend let a reader check; and
3. one thing the synthetic record does not establish.

## What I assess

This is holistic letter feedback, not a point checklist.

| Mark | Evidence |
| --- | --- |
| **A** | Axes, shapes, selection, and broadcasting are correct and explained; checks could catch a plausible axis or normalization error; figure and claim are easy to inspect. |
| **B** | The core operations work, but one axis meaning, validation step, figure choice, or interpretation is incomplete. |
| **C** | Code runs, but it misstates an axis or shape, relies on an unexplained reshaping operation, or makes a claim the output does not support. |
| **Revise** | The notebook does not run top to bottom, does not show the required ND-array reasoning, or is not the student’s own work. |

This feedback is evidence for your term Scholarly Engagement grade. It is not a
separate weighted course component. See [Grading](../01-course-info/grading.md)
for the course’s letter-based grading model.

## You are done when

Your notebook runs from a fresh kernel, every array has a stated shape and axis
meaning, the normalization checks pass, the figure is labeled, and your three
sentences do not claim more than the synthetic data can show.
