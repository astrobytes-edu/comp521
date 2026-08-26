---
title: "Lecture 2 · Procedures, Data, and Reusable Calculations"
subtitle: "Chapters 3–5, plus a first NumPy encounter | Projector lecture"
site:
  hide_toc: true
---

:::{projector-controls}
:id: lecture-02-controls
:::

:::{div}
:class: projector-lecture projector-slide

## Procedures, data, and reusable calculations

### From one stated rule to many inspectable results

Today we turn the one-off calculations from Lecture 1 into a small scientific
program: a procedure that makes decisions, stores related observations, and
packages a calculation so we can reuse and test it.
:::

:::{div}
:class: projector-lecture projector-slide

## The through-line

```{mermaid}
flowchart LR
    question[Scientific question] --> rule[Stated rule<br/>and assumptions]
    rule --> decision[Comparisons<br/>and branches]
    decision --> data[Related observations<br/>in a data structure]
    data --> function[Reusable function<br/>with a contract]
    function --> array[Many values<br/>with an array]
    array --> evidence[Inspectable result<br/>and a test]

    classDef start fill:#dff4f1,stroke:#075f63,stroke-width:2px,color:#073447
    classDef work fill:#eef5ff,stroke:#547da8,stroke-width:2px,color:#122b38
    classDef outcome fill:#fff1d9,stroke:#a46511,stroke-width:2px,color:#4a2b00
    class question start
    class rule,decision,data,function,array work
    class evidence outcome
```

The computer does not infer a missing rule. It repeats exactly the procedure
we make explicit.
:::

:::{div}
:class: projector-lecture projector-slide

## Today’s question

How do we turn a human rule into a procedure that another person can read,
test, and apply to more than one observation?

By the end of class, you should be able to:

- write and trace a conditional and a loop;
- choose a simple structure for related values;
- define a function with an input/output contract;
- explain what an array changes—and what it does not prove.
:::

:::{div}
:class: projector-lecture projector-slide

## I · Procedures and decisions

### Question

What must be stated before Python can make a defensible decision?

### You will leave this section able to

- write pseudocode before syntax;
- distinguish `<` from `<=` at a boundary;
- trace an `if` statement and a `for` loop;
- identify an accumulator and its expected value.

**Through-line focus:** stated rule $\rightarrow$ repeatable decision.
:::

:::{div}
:class: projector-lecture projector-slide

## Write the rule before the code

Suppose we call a normalized flux measurement a **candidate low-flux
observation** when it is strictly below `0.99`.

```text
For each flux measurement:
    If the flux is below 0.99,
        report it as a candidate low-flux observation.
```

This is pseudocode: a precise plan, not Python syntax. Before code can answer
a question, we must decide whether “below” is strict and what happens at the
exact boundary.

A transit search needs uncertainties, cadence, systematics, and a defined
detection procedure. This example practices only the computational decision.
:::

:::{div}
:class: projector-lecture projector-slide

## Predict · which values pass the rule?

For `[1.000, 0.993, 0.990, 0.989, 0.975]`, which values pass “below `0.99`”?

| Comparison | Is `0.990` selected? | Why? |
|---|---:|---|
| `flux < 0.99` |  |  |
| `flux <= 0.99` |  |  |

Neither comparison is universally correct. The rule is correct only when it
matches the stated decision and is tested at its boundary.
:::

:::{div}
:class: projector-lecture projector-slide

## A Boolean expression chooses a branch

```python
flux = 0.989
threshold = 0.99

if flux < threshold:
    print("candidate low-flux measurement")
else:
    print("not below the stated threshold")
```

`flux < threshold` evaluates to `True` or `False`. Indentation is part of the
program: it tells Python which statements belong to each branch.

At `flux == threshold`, this code reaches `else`. That is a policy choice we
can inspect and test—not a fact discovered by Python.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · move the boundary, then explain

:::{interactive-python}
:id: lecture-02-boundary
:controls: {"flux":{"label":"normalized flux","min":0.97,"max":1.01,"step":0.001,"value":0.99}}

threshold = 0.99
print("flux:", format(flux, ".3f"))
print("strictly below threshold:", flux < threshold)
print("at or below threshold:", flux <= threshold)
:::

Set `flux` to exactly `0.990`, just below it, and just above it. Which rule
matches the English sentence “below `0.99`”? What sentence would justify the
other rule?
:::::

:::{div}
:class: projector-lecture projector-slide

## More than two outcomes · `elif`

When a procedure has several mutually exclusive outcomes, state their order.

```python
percentage = 84.0

if percentage >= 90.0:
    grade = "A"
elif percentage >= 80.0:
    grade = "B"
elif percentage >= 70.0:
    grade = "C"
elif percentage >= 60.0:
    grade = "D"
else:
    grade = "F"
```

Python checks from top to bottom and stops after the first true branch. The
order is therefore part of the grade policy: `84.0` is a B because the A test
fails and the B test is the first one that succeeds.
:::

:::{div}
:class: projector-lecture projector-slide

## Combine conditions deliberately

Use `and` when both requirements must hold, `or` when either is sufficient,
and `not` when reversing a Boolean statement is the actual rule.

```python
import math

flux = 0.989
uncertainty = 0.002

usable_measurement = math.isfinite(flux) and uncertainty > 0.0
candidate = usable_measurement and flux < 0.99

if candidate:
    print("candidate under this toy rule")
```

Parenthesize mixed `and` / `or` conditions unless the intended grouping is
obvious. A compact expression is not clearer if another reader cannot state
the policy in words.
:::

:::{div}
:class: projector-lecture projector-slide

## Short-circuiting protects a calculation

Python evaluates Boolean expressions from left to right and may stop as soon
as the answer is known. Put the safety check first.

```python
flux_measurements = []
threshold = 0.99

if flux_measurements and flux_measurements[0] < threshold:
    print("first measurement is a candidate")
```

For an empty list, `flux_measurements` is false, so Python never tries
`flux_measurements[0]`. Reversing the terms would raise an `IndexError`.

Short-circuiting is a control-flow tool, not a substitute for checking whether
the data set is scientifically adequate.
:::

:::{div}
:class: projector-lecture projector-slide

## `while` repeats until a stated condition changes

Use `while` when you do not know the number of repetitions in advance—but
always state how progress happens and what bounds the work.

```python
residual = 0.08
tolerance = 0.01
step = 0
max_steps = 5

while residual > tolerance and step < max_steps:
    print(f"step {step}: residual = {residual:.3f}")
    residual = residual / 2
    step = step + 1

print(f"stopped at step {step}: residual = {residual:.3f}")
```

This is a toy update, not a physical fitting method. Its computational lesson
is real: a `while` loop needs a condition that can change and a maximum-step
guard so a failed convergence rule cannot run forever.
:::

:::{div}
:class: projector-lecture projector-slide

## One rule can apply to many observations

```python
flux_measurements = [1.000, 0.993, 0.989, 0.975]
threshold = 0.99
candidate_count = 0

for flux in flux_measurements:
    if flux < threshold:
        candidate_count = candidate_count + 1
        print(f"candidate: {flux:.3f}")

print("number of candidates:", candidate_count)
```

The name `flux` takes one value at a time. `candidate_count` is an
**accumulator**: it remembers a quantity that changes as the loop advances.
:::

:::{div}
:class: projector-lecture projector-slide

## Trace the loop; do not guess

| Current `flux` | Is `flux < 0.99`? | `candidate_count` after this step |
|---:|---:|---:|
| `1.000` | `False` | `0` |
| `0.993` | `False` | `0` |
| `0.989` | `True` | `1` |
| `0.975` | `True` | `2` |

An accumulator has an invariant: after each step, it equals the number of
values selected so far. If your hand trace violates that sentence, inspect the
update and indentation.
:::

:::{div}
:class: projector-lecture projector-slide

## II · Store related observations deliberately

### Question

What representation makes the relationship among values visible?

### You will leave this section able to

- use a list for an ordered sequence;
- use a dictionary for named, related fields;
- recognize when mutation is useful and when it is risky.

**Through-line focus:** observations $\rightarrow$ inspectable representation.
:::

:::{div}
:class: projector-lecture projector-slide

## A list keeps an ordered sequence

```python
flux_measurements = [1.000, 0.993, 0.989, 0.975]

first_flux = flux_measurements[0]
number_of_measurements = len(flux_measurements)
```

Use a list when order matters and values play the same role. A list is not
automatically a time series: if timing matters, store or document the time
coordinate too.
:::

:::{div}
:class: projector-lecture projector-slide

## A dictionary names related fields

```python
observation = {
    "time_days": 4.5,
    "normalized_flux": 0.989,
    "filter_name": "r",
}

print(observation["normalized_flux"])
```

Use a dictionary when values have different, named roles. The keys make the
structure legible; they do not establish calibration or physical comparability.
:::

:::{div}
:class: projector-lecture projector-slide

## Mutability is a bookkeeping choice

```python
raw_fluxes = [1.000, 0.993, 0.989]
working_fluxes = raw_fluxes
working_fluxes.append(0.975)

print(raw_fluxes)  # also changed
```

The two names refer to the same list. If you need an independent shallow copy
of a one-dimensional list, make it explicit:

```python
working_fluxes = raw_fluxes.copy()
```

Keep raw inputs distinct from derived values. That is a provenance habit, not
just a Python trick.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · select values without losing the original list

:::{interactive-python}
:id: lecture-02-list-loop

flux_measurements = [1.000, 0.993, 0.989, 0.975]
threshold = 0.99
candidate_fluxes = []

for flux in flux_measurements:
    if flux < threshold:
        candidate_fluxes.append(flux)

print("original measurements:", flux_measurements)
print("candidate measurements:", candidate_fluxes)
print("candidate count:", len(candidate_fluxes))
:::

Change one value, then explain why `flux_measurements` still contains every
input. What would change if you appended to `flux_measurements` inside the
loop?
:::::

:::{div}
:class: projector-lecture projector-slide

## III · Package a calculation as a function

### Question

How can one calculation state what it needs, what it returns, and when it
refuses an invalid request?

### You will leave this section able to

- define a small function with `def`, parameters, and `return`;
- state an input/output contract in plain language;
- use keyword arguments when they make intent clearer;
- test a function with ordinary, boundary, and invalid inputs.

**Through-line focus:** calculation $\rightarrow$ reusable, testable contract.
:::

:::{div}
:class: projector-lecture projector-slide

## A function gives a calculation a name and a boundary

For a uniform-source transit model, the idealized fractional flux loss is

$$
\delta = \left(\frac{R_p}{R_\star}\right)^2.
$$

```python
def transit_depth(radius_planet_cm, radius_star_cm):
    """Return idealized fractional flux loss for two positive radii in cm."""
    if radius_planet_cm <= 0 or radius_star_cm <= 0:
        raise ValueError("radii must be positive")
    return (radius_planet_cm / radius_star_cm) ** 2
```

The function makes units, a domain restriction, and the returned quantity
visible. The simplified model is still an approximation.
:::

:::{div}
:class: projector-lecture projector-slide

## Read a function call as a contract

```python
depth = transit_depth(
    radius_planet_cm=7.1492e9,
    radius_star_cm=6.957e10,
)
```

| Part | Meaning |
|---|---|
| `transit_depth` | the calculation we are asking for |
| named inputs | two radii, both in centimeters |
| returned value | dimensionless fractional flux loss |
| `depth` | name holding the result |

Keyword arguments help when inputs share a type and unit but play different
physical roles.
:::

:::{div}
:class: projector-lecture projector-slide

## Separate calculation from policy

```python
def letter_grade(percentage):
    if not 0.0 <= percentage <= 100.0:
        raise ValueError("percentage must be in [0, 100]")
    if percentage >= 90.0:
        return "A"
    if percentage >= 80.0:
        return "B"
    if percentage >= 70.0:
        return "C"
    if percentage >= 60.0:
        return "D"
    return "F"
```

The numerical calculation and letter-grade policy should be separate
functions. Then a change to one does not silently rewrite the other.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · a reusable transit-depth calculation

:::{interactive-python}
:id: lecture-02-transit-depth
:controls: {"radius_ratio":{"label":"Rp / Rstar","min":0.01,"max":0.2,"step":0.01,"value":0.1}}

def transit_depth_from_ratio(radius_ratio):
    if not 0.0 < radius_ratio < 1.0:
        raise ValueError("radius_ratio must be between 0 and 1")
    return radius_ratio ** 2

depth = transit_depth_from_ratio(radius_ratio)
print("radius ratio:", radius_ratio)
print("idealized fractional depth:", format(depth, ".4f"))
print("idealized percent depth:", format(100 * depth, ".2f"), "%")
:::

Move the slider. Which line converts a geometric ratio into a fractional depth?
What physical effects are absent from this uniform-source model?
:::::

:::{div}
:class: projector-lecture projector-slide

## Test the contract at three kinds of inputs

```python
assert transit_depth(1.0, 10.0) == 0.01       # ordinary case
assert transit_depth(1.0, 1.0) == 1.0         # toy-geometry boundary

try:
    transit_depth(-1.0, 10.0)                 # invalid case
except ValueError:
    print("invalid radius rejected")
```

Ask: What ordinary input should work? What boundary tests the policy? What
invalid input should fail clearly? Passing these tests establishes the function
contract, not the adequacy of the underlying scientific model.
:::

:::{div}
:class: projector-lecture projector-slide

## IV · First contact with NumPy

### Question

What changes when one operation applies to an array of values instead of one
scalar?

### You will leave this section able to

- create a one-dimensional NumPy array from a list;
- recognize elementwise arithmetic;
- use `np.linspace` to create a specified grid;
- state why Week 2 is needed before treating arrays as routine.

**Through-line focus:** one calculation $\rightarrow$ a structured collection
of calculations.
:::

:::{div}
:class: projector-lecture projector-slide

## Lists and arrays answer different questions

```python
import numpy as np

flux_list = [1.000, 0.993, 0.989, 0.975]
flux_array = np.array(flux_list)

print(flux_list * 2)
print(flux_array * 2)
```

`flux_list * 2` repeats the list. `flux_array * 2` multiplies each numeric
element by two. That elementwise arithmetic is a central reason scientific
work uses NumPy arrays.

An array does not supply units, calibration, an uncertainty model, or a valid
scientific interpretation.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · make one simple numerical grid

:::{interactive-python}
:id: lecture-02-numpy-preview
:packages: numpy

import numpy as np

time_days = np.linspace(0.0, 4.0, 5)
radius_ratio = 0.1
idealized_depth = radius_ratio ** 2
model_flux = np.ones_like(time_days) - idealized_depth

print("time grid (days):", time_days)
print("model flux:", model_flux)
print("number of model values:", model_flux.size)
:::

`np.linspace(0.0, 4.0, 5)` asks for five evenly spaced values, including both
endpoints. The model flux is deliberately constant: the point is the array
operation, not a complete transit model.
:::::

:::{div}
:class: projector-lecture projector-slide

## NumPy is an introduction today, not the whole method

We are **not yet learning**:

- array shapes beyond one dimension;
- indexing, slicing, masks, and broadcasting;
- array views versus copies;
- vectorized transit geometry, plotting, or performance claims.

Those are Week 2 topics. For today, carry forward just this idea: an array lets
us state the same numerical operation over many values, provided we still know
what every value represents.
:::

:::{div}
:class: projector-lecture projector-slide

## The Grade Calculator is this lecture’s design artifact

Begin or revise the [Grade Calculator Design Lab](../07-practice-labs/grade-calculator-design.md).

Your individual packet must make visible:

1. inputs, allowed ranges, and output units/scales;
2. pseudocode for the numerical calculation and grade policy;
3. behavior at every letter-grade boundary;
4. ordinary, boundary, and invalid test cases;
5. the two functions you will implement after design review.

Do not convert the Grade Calculator to NumPy. Its purpose is to make ordinary
Python control flow and function contracts legible first.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · readings and documentation

| Use this for… | Read |
|---|---|
| pseudocode, comparisons, branches, loops | [Chapter 3: Control Flow & Logic](03-python-control-flow.md) |
| lists, dictionaries, mutation, copying | [Chapter 4: Data Structures](04-python-data-structures.md) |
| function definitions, arguments, return values | [Chapter 5: Functions & Modules](05-python-functions-modules.md) |
| lists versus arrays and array creation | [Chapter 7: NumPy Fundamentals](../04-scientific-computing/07-numpy-fundamentals.md) |
| NumPy function details | [NumPy reference](https://numpy.org/doc/stable/reference/index.html) |

For this lecture, Chapter 7 is a preview. Week 2 will use it as a working
toolkit.
:::

:::{div}
:class: projector-lecture projector-slide

## Exit check

For a list of normalized flux measurements, write:

1. one sentence of pseudocode that states a threshold rule;
2. a function signature for a calculation that returns a candidate count;
3. one ordinary, one boundary, and one invalid test case;
4. one sentence explaining why `np.array(values) * 2` differs from
   `values * 2` when `values` is a Python list.

Bring your completed Grade Calculator design packet and these answers to the
next meeting.
:::

:::{div}
:class: projector-lecture projector-slide

## Before Week 2

Read [Chapter 7: NumPy Fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)
through **7.2 Creating Arrays**. Be ready to explain:

- the difference between a list and an array;
- why `linspace` names a fixed number of grid points;
- what an array’s shape tells you;
- one question you still have about arrays.

Week 2 will deepen the NumPy work before we rely on it for figures or project
analysis.
:::
