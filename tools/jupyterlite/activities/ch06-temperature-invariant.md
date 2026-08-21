---
jupyter:
  jupytext:
    formats: myst
  kernelspec:
    display_name: Python (XPython)
    language: python
    name: xpython
---

# Temperature invariant: predict → run → explain → revise

**Predict.** If `Temperature(-1)` is constructed, should it succeed or raise
`ValueError`? Write a one-sentence reason before you run the next cell.

```{code-cell} python
import math

class Temperature:
    """Temperature with a non-negative Kelvin invariant."""

    def __init__(self, kelvin):
        self.kelvin = kelvin

    @property
    def kelvin(self):
        return self._kelvin

    @kelvin.setter
    def kelvin(self, value):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError(f"Kelvin temperature must be finite and non-negative, got {value}")
        self._kelvin = value

    @property
    def celsius(self):
        return self.kelvin - 273.15
```

## Run the prediction

The `try`/`except` keeps the intentional invalid input visible without stopping
the activity.

```{code-cell} python
try:
    Temperature(-1)
except ValueError as error:
    print(type(error).__name__, error)

absolute_zero = Temperature(0)
print(f"{absolute_zero.kelvin:.0f} K = {absolute_zero.celsius:.2f} degC")
```

## Explain and revise

The constructor uses `self.kelvin = kelvin`, so it runs the same setter used by
later assignments. Change `-1` to `0` or `273.15`, predict the output, then run
again. Explain both the boundary this class enforces and one thing it cannot
validate, such as sensor calibration.
