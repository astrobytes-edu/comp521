---
title: "Lecture 4 · Python Bootcamp: Arrays, Figures, and Evidence"
subtitle: "Block 1 · Week 2 | Chapters 7–8 and Project 1 readiness"
---

# Lecture 4 · Arrays, figures, and evidence

Project 1 needs more than a correct calculation. It needs a visible connection
between data, a model, a figure, and a bounded conclusion.

## 1. An array represents one quantity over many observations · 15 minutes

```python
import numpy as np

time_days = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
flux = np.array([1.000, 0.998, 0.985, 0.997, 1.001])

print("time shape:", time_days.shape)
print("flux shape:", flux.shape)
print("mean flux:", flux.mean())
```

The two one-dimensional arrays need the same shape because each flux value is
paired with one observation time. Shape is evidence about the representation,
not a cosmetic detail.

## 2. Use a Boolean mask to state a selection rule · 15 minutes

```python
candidate_mask = flux < 0.99
candidate_times = time_days[candidate_mask]
candidate_flux = flux[candidate_mask]

print("mask:", candidate_mask)
print("candidate times (days):", candidate_times)
print("candidate flux:", candidate_flux)
```

The mask contains one `True` or `False` value per observation. Applying it to
both arrays preserves the time–flux pairing. It does not prove that a selected
point is a planet; it only applies the stated threshold. Before running, count
how many values you expect `flux < 0.99` to select.

## 3. A plot is evidence only when it is readable · 20 minutes

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(time_days, flux, marker="o", label="observed normalized flux")
ax.axhline(0.99, color="tab:red", linestyle="--", label="candidate threshold")
ax.set(
    xlabel="Time (days)",
    ylabel="Normalized flux",
    title="Small transit-like light curve",
)
ax.legend()
ax.grid(alpha=0.25)
plt.show()
```

The axes name quantities and units. The threshold line makes the decision rule
inspectable. The title describes the data without claiming that a planet has
been discovered.

:::{note} Figure reading check

What does the figure show directly? What would require more data or a more
complete model before it could be claimed? Keep those two answers separate.
:::

## 4. Project 1 readiness sprint · 25 minutes

In a clean notebook, create two same-length arrays, make one Boolean selection,
and produce one labeled figure. Then restart the kernel and run the notebook
from top to bottom. Your final paragraph should state:

1. what the plot shows;
2. which visible evidence supports that statement; and
3. one assumption or limitation of the selection or model.

When a shape, mask, or array operation surprises you, do the short
[Vectorization and Broadcasting Lab](../07-practice-labs/vectorization-broadcasting.md)
before adding more code. It uses a small array you can reason through by hand.

## Exit check

Describe what a Boolean mask selected, cite one feature of your plot as
evidence, and name one claim the plot alone cannot establish.

## Start Project 1

You now have the minimum workflow: define quantities, write a rule, organize
data, make a reusable calculation, select evidence, plot it, and rerun cleanly.
The chapters remain the place to deepen each move when your project creates a
concrete need. Before guessing how an unfamiliar function behaves, use the
course [Docs First reference](docs-first.md).
