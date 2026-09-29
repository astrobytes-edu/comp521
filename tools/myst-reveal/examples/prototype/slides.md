---
title: Classes and Computed State
subtitle: COMP 521 · MyST Reveal prototype
kernelspec:
  name: python3
  display_name: Python 3
---

## One class, two instances

A class defines behavior. Each instance holds its own state.

```python
wide = Rectangle(width=5, height=2)
tall = Rectangle(width=2, height=5)
```

Changing `wide.width` does not change `tall.width`.

Background: the Python tutorial [@python-classes].

:::{speaker-note}
Ask students to identify the two instances and the shared class.
These demonstration notes are public, not instructor-only material.
:::

## Predict before revealing

Suppose `area` was calculated once in `__init__` and stored as an attribute.

```python
rectangle = Rectangle(width=3, height=2)
rectangle.width = 5
print(rectangle.area)
```

**Predict:** will this print 6 or 10? Explain your choice.

:::{fragment}
It prints **6**. Assigning a new width does not recompute a stored area.
:::

## Two ways to represent area

:::::{slide-columns}
::::{slide-column}
### Stored once

```python
self.area = width * height
```

Later changes to width can leave the stored area stale.
::::

::::{slide-column}
### Computed on access

```python
@property
def area(self):
    return self.width * self.height
```

Accessing `area` uses the current dimensions.
::::
:::::

## State and a derived quantity

For a rectangle with width $w$ and height $h$,

```{math}
:label: rectangle-area
A = w h.
```

With $w=5$ and $h=2$, [](#rectangle-area) gives $A=10$ square units.

The property encodes this relationship without storing a second copy of it.

## Follow the data dependency

```{figure} rectangle.svg
:label: rectangle-diagram
:alt: Width five and height two feed into the area calculation, which returns ten.

Area is derived from the current width and height.
```

[](#rectangle-diagram) shows the inputs to [](#rectangle-area).

## Execute and check

```{code-cell} python
class Rectangle:
    def __init__(self, width, height):
        self.width, self.height = width, height

    @property
    def area(self):
        return self.width * self.height

r = Rectangle(3, 2)
r.width = 5
print(r.area)
assert r.area == 10
```

**Explain:** why does the computed property stay consistent?
