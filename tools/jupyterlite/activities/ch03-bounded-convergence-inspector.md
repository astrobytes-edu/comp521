---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Bounded Convergence Inspector: predict → run → explain → revise

**Predict.** A numerical update can move closer to a target while still
stopping before it satisfies its stated tolerance. Before running the cells,
predict which case will return `"converged"` and which will return
`"max_iterations_reached"`.

```{code-cell} python
import math


def bounded_relaxation(initial_value, target_value, rate, abs_tol, max_iterations):
    """Return a value, a stopping status, and an iteration count.

    Inputs and the absolute tolerance must use the same units. This function
    checks a numerical contract; it does not validate a physical model.
    """
    if not 0 < rate <= 1:
        raise ValueError("rate must be in (0, 1]")
    if abs_tol <= 0:
        raise ValueError("abs_tol must be positive")
    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")

    value = initial_value
    for iteration in range(1, max_iterations + 1):
        value = value * (1 - rate) + target_value * rate
        if math.isclose(value, target_value, rel_tol=0.0, abs_tol=abs_tol):
            return value, "converged", iteration
    return value, "max_iterations_reached", max_iterations
```

```{code-cell} python
# Cell 2: inspect a run that stops at its work limit, then one that satisfies
# the same tolerance contract. Change one input at a time and predict first.
for max_iterations in (5, 100):
    value, status, iteration = bounded_relaxation(
        initial_value=100.0,
        target_value=1.0,
        rate=0.1,
        abs_tol=0.01,
        max_iterations=max_iterations,
    )
    print(f"limit={max_iterations:3d}; stopped after {iteration:3d}; {status}; value={value:.3f}")
```

```{code-cell} python
# Cell 3: make the decision contract visible to a caller.
value, status, iteration = bounded_relaxation(
    initial_value=100.0,
    target_value=1.0,
    rate=0.1,
    abs_tol=0.01,
    max_iterations=5,
)

if status == "converged":
    print("This run met its stated numerical tolerance.")
else:
    print("This run stopped without meeting its stated numerical tolerance.")
```

## Explain the result

1. Which outcome changed when only `max_iterations` changed? Why is that not
   evidence that the update rule is scientifically valid?
2. Change `rate` and then `abs_tol`. Which is an algorithm setting, and which
   represents a numerical decision contract in this toy example?
3. Complete this sentence: “The status is `converged`, so this run ________.
   This does **not** show that ________.”

## Revise the design

Modify the function so that its parameter names carry a unit, such as
`abs_tol_m_s`, for a quantity in metres per second. Then name one independent
check—known solution, calibration measurement, conservation law, or refinement
comparison—that would be needed before a scientific claim could rely on the
calculation.

**Success condition.** You can distinguish a run that met an explicit numerical
contract from one that merely exhausted its allowed work, and you can state the
additional evidence required for a scientific conclusion.

This activity illustrates bounded iteration and a tolerance contract. It does
**not** select a physically meaningful tolerance, validate an update rule, or
establish convergence for every input.
