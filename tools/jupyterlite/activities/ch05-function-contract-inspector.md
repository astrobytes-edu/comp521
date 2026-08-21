---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Function Contract Inspector: predict → run → explain → revise

**Predict.** Before running the cells, decide which calls should be rejected by
the kinetic-energy contract and whether two calls to each measurement function
share a history. Units are grams, centimeters per second, seconds, and ergs.

```{code-cell} python
import math


def kinetic_energy_cgs(mass_g, velocity_cms):
    """Return Newtonian kinetic energy in ergs for finite, nonnegative mass."""
    if not (math.isfinite(mass_g) and math.isfinite(velocity_cms)):
        raise ValueError("mass_g and velocity_cms must be finite")
    if mass_g < 0:
        raise ValueError("mass_g must be nonnegative")
    return 0.5 * mass_g * velocity_cms**2


def record_buggy(value, history=[]):
    """Deliberately buggy: this default list is shared by independent calls."""
    history.append(value)
    return history


def record_checked(value, history=None):
    """Return the history explicitly supplied by the caller, or a fresh one."""
    if history is None:
        history = []
    history.append(value)
    return history
```

```{code-cell} python
# Cell 2: alter these calls and rerun this cell to test your prediction.
for mass_g, velocity_cms in ((1.0, 100.0), (-1.0, 100.0), (1.0, float("nan"))):
    try:
        energy_erg = kinetic_energy_cgs(mass_g, velocity_cms)
        print(f"mass={mass_g:g} g, velocity={velocity_cms:g} cm/s -> {energy_erg:g} erg")
    except ValueError as error:
        print(f"mass={mass_g:g} g, velocity={velocity_cms:g} cm/s -> rejected: {error}")

buggy_first = record_buggy(23.5)
buggy_second = record_buggy(24.1)
checked_first = record_checked(23.5)
checked_second = record_checked(24.1)

print("\nBuggy histories share state:", buggy_first, buggy_second, buggy_first is buggy_second)
print("Checked histories are independent:", checked_first, checked_second, checked_first is checked_second)
```

```{code-cell} python
# Cell 3: executable postconditions for the public contracts above.
assert kinetic_energy_cgs(2.0, 3.0) == 9.0
for invalid_mass, invalid_velocity in ((-1.0, 1.0), (1.0, float("inf"))):
    try:
        kinetic_energy_cgs(invalid_mass, invalid_velocity)
    except ValueError:
        pass
    else:
        raise AssertionError("the kinetic-energy contract accepted invalid input")

fresh_a = record_checked(1.0)
fresh_b = record_checked(2.0)
assert fresh_a == [1.0]
assert fresh_b == [2.0]
assert fresh_a is not fresh_b
print("Contract checks passed: validation and fresh-state ownership agree with the specification.")
```

## Explain the result

1. Which inputs were rejected, and which part of the kinetic-energy contract
   justified each rejection?
2. Why can `record_buggy` return a plausible list while still violating the
   expectation of independent calls?
3. If a caller wants deliberate accumulation, how should the caller make that
   shared `history` object visible at the call site?

## Revise the design

Choose one new domain constraint, document it in `kinetic_energy_cgs` in Cell
1, and add the matching guard there. Then add a call to Cell 2 and an
executable postcondition to Cell 3 that show the new rejected input. For
example, a particle-only analysis could require `mass_g > 0` rather than this
activity's current `mass_g >= 0`; explain why that stricter rule fits the
domain. Then make an explicit history list, pass it to `record_checked` twice,
and explain why that shared state is now intentional rather than hidden.

**Success condition.** You can turn a function's input, output, failure, and
ownership promises into executable checks, and you can distinguish intentional
shared state from a mutable-default bug.

This activity demonstrates local Python function contracts. It does **not**
validate a physical model outside its stated domain, establish a production API,
or measure the performance of a scientific workflow.
