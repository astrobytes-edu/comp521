---
title: "Practice Lab: Vectorization and Broadcasting"
subtitle: "Python Bootcamp | Chapter 7"
kernelspec:
  name: python3
  display_name: Python 3
---

Vectorization and broadcasting let one array expression describe a calculation
over many measurements. They are safe only when we know what each axis means.
This lab makes shapes visible before combining arrays.

## Goals

- distinguish an explicit Python loop from an elementwise NumPy expression;
- predict a result shape before running code;
- normalize one light curve and several light curves; and
- repair a broadcasting error by making an axis explicit.

## Part 1 — Vectorize one aligned measurement series

```{code-cell} python
flux_list = [1.000, 0.998, 0.985, 0.997, 1.001]
baseline_flux = 1.000
residuals_loop = []

for flux_value in flux_list:
    residuals_loop.append(flux_value - baseline_flux)

print(residuals_loop)
```

The loop is not wrong. It spells out a repeated procedure. NumPy lets us state
the same elementwise relationship directly after we choose an array.

:::{lecture-predict}
:id: vectorization-elementwise-prediction
:prompt: Predict the shape and first value of residuals before running the NumPy expression. Why should there be one result per flux measurement?
:options: shape-5-first-0|shape-1-first-1|shape-5-first-1
:rows: 3
:::

```{code-cell} python
import numpy as np

flux = np.array(flux_list)
residuals = flux - baseline_flux

print("flux shape:", flux.shape)
print("residuals shape:", residuals.shape)
print("residuals:", residuals)
assert np.allclose(residuals, residuals_loop)
```

This is vectorization: one expression applies an operation to aligned elements.
The assertion checks agreement with the simple loop; it does not validate a
transit model or measure speed.

## Part 2 — Broadcast one baseline per light curve

Rows now represent stars and columns represent observing times.

```{code-cell} python
flux_by_star = np.array([
    [1.000, 0.998, 0.985, 0.997],
    [0.980, 0.979, 0.966, 0.978],
])
baseline_per_star = np.array([[1.000], [0.980]])
normalized_flux = flux_by_star / baseline_per_star

print("flux shape:", flux_by_star.shape)
print("baseline shape:", baseline_per_star.shape)
print("normalized shape:", normalized_flux.shape)
print(normalized_flux)
```

The baseline’s shape is `(2, 1)`, meaning one value for each star and a length-
one time dimension that NumPy can repeat across four columns.

:::{important} Shape before syntax

When combining arrays, write the meaning and expected shape of each one. NumPy
compares dimensions from the right; they are compatible only when equal or when
one is `1`.
:::

## Part 3 — Repair a shape mistake

```python
baseline_per_star = np.array([1.000, 0.980])  # shape (2,)
normalized_flux = flux_by_star / baseline_per_star  # shape mismatch
```

Make the row ownership explicit:

```{code-cell} python
baseline_per_star = np.array([1.000, 0.980])
baseline_column = baseline_per_star[:, np.newaxis]
normalized_flux = flux_by_star / baseline_column

print("baseline column shape:", baseline_column.shape)
print(normalized_flux)
```

`np.newaxis` does not manufacture scientific information. It states that each
baseline belongs to a row, while each row has many time measurements.

## Try it live

Predict what happens if the second baseline changes. Then edit and run this
browser-local example. If browser Python is unavailable, run the static cells.

:::{interactive-python}
:id: vectorization-broadcasting-live
:packages: numpy
:controls: {"second_baseline":{"label":"second-star baseline","min":0.90,"max":1.05,"step":0.01,"value":0.98}}

import numpy as np

flux_by_star = np.array([
    [1.000, 0.998, 0.985, 0.997],
    [0.980, 0.979, 0.966, 0.978],
])
baseline_per_star = np.array([1.000, second_baseline])[:, np.newaxis]
normalized_flux = flux_by_star / baseline_per_star
print("flux shape:", flux_by_star.shape)
print("baseline shape:", baseline_per_star.shape)
print("normalized flux:\n", normalized_flux)
:::

## Explain

1. Why does `flux - baseline_flux` return one residual per observation?
2. What quantity does each axis of `flux_by_star` represent?
3. Why does `baseline_per_star[:, np.newaxis]` have shape `(2, 1)`?
4. Give one way a shape-correct expression could still make a poor scientific model.

Return to the [NumPy chapter](../04-scientific-computing/07-numpy-fundamentals.md)
for deeper explanations of arrays, masking, broadcasting, and copies/views.
