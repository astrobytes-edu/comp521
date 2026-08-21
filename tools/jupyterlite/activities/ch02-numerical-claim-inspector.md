---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Numerical Claim Inspector: predict → run → explain → revise

**Predict.** In binary64 arithmetic, when might `1 - cos(x)` become `0.0` even
though the mathematical expression is positive? If a residual is $10^{-4}$ m/s
and the measurement resolution is $10^{-3}$ m/s, what is the narrowest claim
you can make before seeing any calibration data?

```{code-cell} python
# Cell 1: compare two mathematically equivalent representations
import math


def stable_one_minus_cos(angle_rad):
    """Compute 1 - cos(angle_rad) without subtracting nearby floats."""
    return 2 * math.sin(angle_rad / 2) ** 2


def inspect_angle(angle_rad):
    direct = 1 - math.cos(angle_rad)
    stable = stable_one_minus_cos(angle_rad)
    print(f"angle: {angle_rad:.1e} rad")
    print(f"direct 1 - cos(angle): {direct:.18e}")
    print(f"stable identity:        {stable:.18e}")
    return direct, stable
```

```{code-cell} python
# Cell 2: start with the small angle from the chapter, then try 1e-7, 1e-8,
# 1e-9, and 1e-10. Where does the direct form lose the result's scale?
direct_value, stable_value = inspect_angle(1e-8)
```

```{code-cell} python
# Cell 3: compare a residual with a stated instrument resolution
def within_resolution(residual_m_s, resolution_m_s):
    """Return whether a residual is below a declared absolute resolution."""
    if resolution_m_s <= 0:
        raise ValueError("resolution_m_s must be positive")
    return math.isclose(residual_m_s, 0.0, rel_tol=0.0, abs_tol=resolution_m_s)


residual_m_s = 1e-4
resolution_m_s = 1e-3
print(within_resolution(residual_m_s, resolution_m_s))
```

## Explain the result

1. Change the angle in Cell 2. Record one angle where the direct form remains
   useful and one where it loses the scale that the stable identity preserves.
2. Change `resolution_m_s` in Cell 3. What resolution would make the same
   residual fail this particular comparison?
3. Complete this sentence: “The residual is within the stated resolution, so
   ________. This does **not** show that the instrument has no bias because
   ________.”

## Revise the design

Modify `within_resolution` so its name, arguments, and docstring identify the
quantity and units being compared. Then describe one source of uncertainty or
calibration evidence that would be required for an instrument-bias claim.

**Success condition.** You can distinguish a stable numerical representation
from an unsupported scientific conclusion, and you can explain why the
absolute tolerance in this activity comes from a stated measurement resolution
rather than from a universal default.

This activity demonstrates finite-precision and tolerance behavior. It does
**not** provide an uncertainty model, calibration data, or a rule for choosing
tolerances in every scientific problem.
