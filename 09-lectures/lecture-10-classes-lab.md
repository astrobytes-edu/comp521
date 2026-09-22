---
title: "Lecture 10 · Scientific Classes and Project Lab"
subtitle: "Week 5 · September 24, 2026"
site:
  hide_toc: true
  hide_outline: true
---

:::{lecture-controls}
:id: lecture-10-controls
:::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## When should data and behavior live together?

**Last time:** a numerical result needed a contract and evidence.

**Today:** **state → invariant → property → test → project lab**.

A small class keeps related state and its derived quantities consistent.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Predict · a rectangle changes width

:::{figure} ../assets/textbook-figures/l10-stale-state.svg
:alt: A three by four rectangle has area twelve. After width becomes six, a stored area of twelve is stale; a computed area is twenty-four.
:::

:::{div}
:class: lecture-prompt

**Pair prompt:** which values should we store, and which should we derive?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## An object owns one set of state

:::{figure} ../assets/textbook-figures/l10-object-state.svg
:alt: A Rectangle instance stores validated width and height. Reading the area property computes width times height rather than storing another value.
:::

A dictionary can hold the values. A class can own the rules governing them.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Construction · what does self refer to?

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = positive_dimension(width)
        self._height = positive_dimension(height)
```

`self` is the instance being constructed.

The helper validates each dimension before it becomes stored state.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Validate the input at the boundary

```python
from math import isfinite
from numbers import Real

def positive_dimension(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("need a real dimension")
    try:
        dimension = float(value)
    except OverflowError as exc:
        raise ValueError("need a positive finite dimension") from exc
    if not isfinite(dimension) or dimension <= 0:
        raise ValueError("need a positive finite dimension")
    return dimension
```

:::{div}
:class: lecture-prompt

**Predict:** what happens for zero, a negative number, and NaN?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Properties · read state, derive the result

```python
@property
def width(self):
    return self._width

@property
def area(self):
    return self.width * self.height
```

Define `height` like `width`. Read the result with `rect.area`, not `rect.area()`.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Choose how state can change

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

**Read-only state**

- Public `width` and `height` cannot be reassigned.
- Construct a new instance for a new rectangle.
- This is the example’s design.
:::::

:::::{div}
:class: lecture-column

**Validated updates**

- Setters check every public change.
- Derived properties use the current state.
- This is an alternative design.
:::::
::::::

**Choose one:** both designs can maintain a contract.

The underscore marks private state by convention; it does not prevent deliberate mutation.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Predict → run → explain

For `rect = Rectangle(3, 4)`:

| Expression | Your prediction |
|:--|:--|
| `rect.area` | value? |
| `rect.area()` | value or exception? |
| `rect.width = 6` | accepted or rejected? |
| `Rectangle(-3, 4)` | accepted or rejected? |

Explain the contract behind each answer.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Check the predictions

| Expression | Result | Reason |
|:--|:--|:--|
| `rect.area` | **12** | Computed property |
| `rect.area()` | **TypeError** | Value is not callable |
| `rect.width = 6` | **AttributeError** | No public setter |
| `Rectangle(-3, 4)` | **ValueError** | Invalid dimension |

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Transfer · one Star instance

| Quantity | Role |
|:--|:--|
| name, radius, temperature | stored state |
| luminosity, peak wavelength | derived properties |
| albedo | argument to a zone calculation |

:::{div}
:class: lecture-prompt

**Pair prompt:** why can a stored luminosity become stale?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Read the units before writing the method

`Star(name, radius, teff)`

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

**Inputs**

- **Radius:** solar radii.
- **Temperature:** K.
:::::

:::::{div}
:class: lecture-column

**Outputs**

- **Luminosity:** solar luminosities.
- **Peak wavelength:** cm.
- **Zone bounds:** AU.
:::::
::::::

**Contract:** a class does not convert units automatically; its implementation must do so.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## What earns a class?

A star's derived quantities share one validated state.

A root finder needs no persistent state between calls.

Orbital functions receive their parameters explicitly.

:::{div}
:class: lecture-prompt

**Explain:** when would a simple dictionary or function be sufficient?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Design check before the lab

Propose a valid construction, an invalid construction, and a consistency check.

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

**Read-only state**

Public reassignment must fail.
:::::

:::::{div}
:class: lecture-column

**Validated updates**

Doubling radius at fixed temperature must multiply luminosity by four.
:::::
::::::

**Choose one:** test the design you implement. You do not need both.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Project 3 lab · build on your own code

**30 minutes · individual code, paired discussion**

1. Import the Lecture 8 module and run `python -m pytest`.
2. Establish one passing known-root test; explain the history.
3. Construct one valid `Star` and reject invalid state.
4. Name the next unchecked layer.

Use the project brief as the interface contract.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Lab checkpoint 1 · a test that runs

From the project directory:

```text
python -m pytest
```

If imports fail, repair the environment or module layout first.

:::{div}
:class: lecture-prompt

**Explain:** which module does your test import? Where should plots and exploratory runs live?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Lab checkpoint 2 · a result you can explain

1. Begin with a known root and an explicit tolerance.
2. Inspect `(root, n_iter, history)`.
3. Check an endpoint root and an interior root.

**Limit:** one passing example does not establish the whole contract.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Lab checkpoint 3 · valid state

1. Construct a star with valid radius and temperature.
2. Try zero or nonfinite state; explain the exception.
3. Identify stored quantities and derived properties.

**Prerequisite:** if the solver is unfinished, establish its first passing test before switching tasks.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Lab checkpoint 4 · what should fail next?

**Choose the next check:**

- History convention.
- Invalid input.
- Property consistency.
- A known physical limit.

Do not add another numerical method.

:::{div}
:class: lecture-prompt

**Ask your partner:** what incorrect implementation would this test detect?
:::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-teaching

## Debrief · name the first unchecked layer

Root contract → physical root → circular orbit → contact times → stellar bounds.

State your next test in your working notes.

Aim to finish Parts 1–2 and begin Part 3 this week.

Project 3 is due **Monday, October 5, 11:59 pm PT**.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-10 projector-slide lecture-reference

## keep the class small

Chapter 6 §§6.1–6.4: construction, `self`, methods, properties.

Chapter 10 §§10.1 and 10.4: validated state and tests. Dataclass implementation is optional.

Inheritance and operator overloading are not required. Dataclasses are optional.

[Download the complete Rectangle example](examples/lecture10-rectangle.py).

Local modules, tests, notebooks, and Git remain the project workflow.
:::::::
