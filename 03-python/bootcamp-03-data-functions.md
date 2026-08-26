---
title: "Lecture 3 · Python Bootcamp: Data and Functions"
subtitle: "Block 1 · Week 2 | Chapters 4–5 and the Grade Calculator"
---

# Lecture 3 · Data and functions

Scientific programs need two kinds of structure: a way to represent related
information and a way to state a reusable calculation with a clear contract.

## 1. Choose a representation that answers the question · 15 minutes

An ordered series of observations belongs naturally in a list. Named facts
about one target belong naturally in a dictionary. These are choices about
meaning, not merely punctuation.

```python
observation = {
    "star_id": "demo-01",
    "period_days": 3.50,
    "flux": [1.000, 0.993, 0.989, 0.975],
}

print(observation["star_id"])
print("first flux measurement:", observation["flux"][0])
```

The key `"flux"` identifies what the values mean. The index `[0]` selects the
first item in that ordered list; Python counts from zero. Predict what
`observation["flux"][2]` returns before you run it.

## 2. Put a calculation behind a contract · 20 minutes

A function makes a promise: given a stated kind of input, it returns a stated
kind of output. This function takes a dimensionless radius ratio and returns a
dimensionless transit depth for our uniform-disk model.

```python
def transit_depth(radius_ratio):
    """Return the uniform-disk transit depth for a dimensionless radius ratio."""
    if radius_ratio < 0:
        raise ValueError("radius_ratio must not be negative")
    return radius_ratio**2


print(transit_depth(0.10))
print(transit_depth(0.20))
```

`return` gives a value back to code that called the function. Printing inside a
function is not the same as returning a value that later code can use. A useful
contract names its input, output, units when relevant, and invalid cases.

## 3. Test the promised behavior · 15 minutes

```python
import math

assert transit_depth(0.0) == 0.0
assert math.isclose(transit_depth(0.10), 0.01, rel_tol=0.0, abs_tol=1e-12)
assert math.isclose(transit_depth(0.20), 0.04, rel_tol=0.0, abs_tol=1e-12)

print("three stated cases passed")
```

An assertion checks a claim we stated in advance. Passing these three tests
does **not** prove that a uniformly bright disk describes a real star. It shows
only that this function implements its stated formula for these cases.

:::{tip} Test selection

Every function needs an ordinary case, a boundary case, and an invalid case.
Which of those categories does `transit_depth(0.0)` represent? What invalid
input would you add next?
:::

## 4. Turn a design into a small program · 25 minutes

Return to the [Grade Calculator Design Lab](../07-practice-labs/grade-calculator-design.md).
Use your test table to implement a first version with small functions. One
function should calculate the numerical course percentage; a separate function
should make the letter-grade decision. Separating those jobs makes it possible
to test and revise each rule without breaking the other.

## Exit check

State one function contract from today: its input, output, one invalid input,
and one test case. Then explain why a passing unit test is not automatically a
scientific conclusion.

## Before Lecture 4

Read [Chapter 7](../04-scientific-computing/07-numpy-fundamentals.md) and
[Chapter 8](../04-scientific-computing/08-matplotlib-fundamentals.md) through
the first plotting example. Bring the working core of your Grade Calculator.
