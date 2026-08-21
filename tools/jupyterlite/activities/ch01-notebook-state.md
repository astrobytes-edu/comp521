---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Notebook State Detective: predict → run → explain → revise

**Predict.** This notebook is written to run cleanly from top to bottom. What
will happen if you deliberately calculate a result *before* applying its
revised configuration, then inspect it only after the revision? Write your
reason before running anything.

```{code-cell} python
# Cell 1: establish an exploratory configuration
param_a = 70.0
param_b = 0.3
x_value = 1000

def calculate_result(x):
    """Use the current exploratory configuration."""
    return (x / param_a) * (1 + param_b)
```

## Run in an order that creates stale state

```{code-cell} python
# Cell 2: revise the exploratory configuration
param_a = 67.4
param_b = 0.315
```

```{code-cell} python
# Cell 3: calculate and record the configuration used right now
result = calculate_result(x_value)
recorded_param_a = param_a
```

```{code-cell} python
# Cell 4: inspect whether stored and current state agree
print(f"current param_a: {param_a}")
print(f"param_a recorded with result: {recorded_param_a}")
print(f"stored result: {result:.3f}")
print(f"result if recomputed now: {calculate_result(x_value):.3f}")
```

1. Run Cells **1, 3, 2, 4**. The stored result should say it used `70.0`, while
   the current configuration says `67.4`.
2. From the **Run** menu, choose **Restart Kernel and Run All Cells**. This time
   Cells 1, 2, 3, and 4 run in their written order, so the recorded and current
   values should both be `67.4`.

## Revise the design

Change `calculate_result` so `param_a` and `param_b` are required arguments.
Then call it with the values you intend to use and explain what must be saved
beside a figure or table for another person to interpret that result.

**Success condition.** You can explain why the wrong order leaves a stale
derived result, why a clean run removes that particular ambiguity, and why
neither run identifies the scientifically correct configuration by itself.

This activity demonstrates a notebook-state failure mode. It does **not** tell
you which interpreter, package versions, input files, or scientific assumptions
produced an analysis result; those belong in the surrounding record.
