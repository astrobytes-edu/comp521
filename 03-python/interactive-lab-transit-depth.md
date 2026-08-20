---
title: "Interactive Lab: Transit Depth"
subtitle: "COMP 521 | Predict, run, explain, change"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

## A 10-minute computational experiment

This is a small scientific experiment, not a syntax worksheet. The browser can
run the cells on this page using a local WebAssembly Python kernel. Your code
and results stay in your browser: use this space to rehearse an idea, then put
your documented Project 1 work in your course notebook.

:::{important} Start the live kernel

Select **Run experiment** on the interactive card below. The first start may
take a moment because your browser is loading Python. If live execution is
unavailable, the rendered outputs below still show the expected baseline
results.
:::

### 1. Predict

For a uniform stellar disk and a planet that is fully in front of the disk, the
remaining normalized flux is

$$
F = 1 - p^2,
$$

where $p = R_p/R_\star$ is dimensionless.

Before running anything, predict the flux for `p = 0.10`. Then predict whether
changing `p` from `0.10` to `0.20` doubles the blocked light or quadruples it.
Write your prediction in a notebook, on paper, or in a comment in the cell.

### 2. Run and inspect

```{code-cell} python
from math import isclose

p = 0.10
flux = 1 - p**2
expected_flux = 0.99

print(f"p = {p:.2f}")
print(f"normalized flux = {flux:.3f}")
print("matches the stated expectation:", isclose(flux, expected_flux))
```

### 3. Explore with a control widget

Use the slider to choose `p`, predict the result, then select **Run
experiment**. The code is editable: change one thing at a time, and use
**Reset Python** when you want a clean state. The slider is a browser control,
not a replacement for explaining the calculation.

:::{interactive-python}
:id: transit-depth-experiment
:packages: matplotlib
:controls: {"p":{"label":"radius ratio p = Rp / Rstar","min":0.02,"max":0.50,"step":0.01,"value":0.10}}

from math import isclose
import matplotlib.pyplot as plt

flux = 1 - p**2
blocked_fraction = p**2

print(f"p = {p:.2f}")
print(f"normalized flux = {flux:.3f}")
print(f"blocked fraction = {blocked_fraction:.3f}")
print("flux + blocked fraction = 1:", isclose(flux + blocked_fraction, 1.0))

p_values = [value / 100 for value in range(0, 51)]
fig, ax = plt.subplots()
ax.plot(p_values, [value**2 for value in p_values], color="tab:blue", linewidth=2)
ax.scatter([p], [blocked_fraction], color="tab:orange", zorder=3)
ax.set(xlabel=r"radius ratio $p = R_p/R_\star$",
       ylabel="blocked fraction",
       title="Uniform-source transit-depth model")
ax.grid(alpha=0.3)
plt.show()
:::

The calculation is intentionally small enough to audit: `p` is a dimensionless
radius ratio, the result is a dimensionless normalized flux, and `isclose`
checks a stated numerical expectation rather than assuming all floats are
exactly comparable.

### 4. Change one assumption

Edit only the value of `p` to `0.20`, run the cell again, and answer:

1. What fraction of light is blocked at each value of `p`?
2. Does the blocked fraction scale linearly with `p`?
3. Which scientific assumption makes this calculation incomplete for ingress or
   egress?

:::{tip} Check your reasoning
:class: dropdown

At `p = 0.10`, the blocked fraction is `0.01`; at `p = 0.20`, it is `0.04`.
Doubling radius ratio quadruples blocked area. The calculation assumes complete
overlap and a uniform source, so it does not model partial-overlap geometry or
limb darkening.
:::

### 5. Explain and carry it forward

In one or two sentences, explain why the curve is quadratic and name one limit
of this model. Then reproduce the calculation in your Project 1 notebook and
run that notebook from a clean kernel. Browser execution is useful for a first
experiment; the project notebook is the durable scientific record.

:::{note} Reset is evidence, not punishment

Use **Reset Python** in the experiment card, then rerun the experiment. If a
result depends on a variable you forgot to define, that is useful evidence that
the calculation is not yet reproducible from a clean state.
:::
