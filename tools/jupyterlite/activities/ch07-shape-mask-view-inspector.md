---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Shape, mask, and view inspector: predict → run → explain

**Predict.** Before running anything, write down the shape of `flux_grid +
background_by_column`. Then decide whether `basic_slice` and `fancy_columns`
will share memory with `flux_grid`.

```{code-cell} python
import numpy as np

# Rows are observations; columns are wavelength channels.
flux_grid = np.array(
    [[10.0, 11.0, 12.0],
     [20.0, 21.0, 22.0]]
)
background_by_column = np.array([0.5, 1.0, 1.5])

corrected = flux_grid + background_by_column
print("flux grid shape:", flux_grid.shape)
print("background shape:", background_by_column.shape)
print("corrected shape:", corrected.shape)
print(corrected)
```

## Explain the broadcast

`background_by_column` has shape `(3,)`, so NumPy aligns it with the final
axis of `flux_grid` and uses the same three values for each row. Change it to
`np.array([[0.5], [1.0]])`, predict the new result, and run the first cell
again. What quantity would that column-shaped array represent instead?

```{code-cell} python
# A boolean mask retains values meeting a stated threshold.
bright_mask = corrected >= 21.0
bright_values = corrected[bright_mask]
print("mask:\n", bright_mask)
print("selected values:", bright_values)
print("selected shape:", bright_values.shape)
```

## Explain the ownership boundary

```{code-cell} python
# Basic slicing preserves a view when NumPy can do so; fancy indexing copies.
basic_slice = flux_grid[:, 1:]
fancy_columns = flux_grid[:, [0, 2]]

print("basic slice shares memory:", np.shares_memory(basic_slice, flux_grid))
print("fancy columns share memory:", np.shares_memory(fancy_columns, flux_grid))

basic_slice[0, 0] = -99.0
print("original after changing the basic slice:\n", flux_grid)
```

## Revise your prediction

The basic slice shares the original buffer, so changing it changes
`flux_grid`. Fancy indexing creates a separate array because it gathers
non-contiguous columns. In a scientific workflow, make a copy before editing
when the original calibrated data must remain unchanged.

**Success condition:** you can state the output shape before running the
broadcast, explain why masking returns a one-dimensional selection here, and
verify the view/copy distinction with `np.shares_memory`. This activity does
**not** decide whether a threshold is scientifically justified; that boundary
comes from the measurement model and analysis plan.
