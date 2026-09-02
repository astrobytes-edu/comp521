---
title: "Lecture 4 · NumPy, Matplotlib, and Readable Evidence"
subtitle: "Block 1 · Week 2 | Chapters 7–8"
site:
  hide_toc: true
---

:::{projector-controls}
:id: lecture-04-controls
:::

:::{div}
:class: projector-lecture projector-slide

## NumPy, Matplotlib, and readable evidence

### From numerical arrays to a figure another person can inspect

Lecture 2 introduced arrays as one operation applied to many values. Today we
make that idea operational: create arrays with a stated shape, select matching
observations with a Boolean mask, evaluate a simple vectorized model, and make
a figure that separates data, assumptions, and conclusion.
:::

:::::{div}
:class: projector-lecture projector-slide

## The through-line

:::{div}
:class: lecture-through-line

1. **Question about a varying quantity**
2. **Paired arrays with units**
3. **A stated selection rule**
4. **One vectorized calculation**
5. **A labeled figure**
6. **A bounded claim**
:::

The same array can be useful or misleading depending on what each position
means, which values were selected, and what the figure actually shows.
:::::

:::{div}
:class: projector-lecture projector-slide

## Today’s question

How do arrays and figures make a numerical relationship inspectable without
quietly turning a toy model or a selection rule into a scientific discovery?

By the end of class, you should be able to:

- create and inspect one-dimensional NumPy arrays;
- use indexing, slicing, and Boolean masks without breaking paired data;
- explain elementwise operations and array shape;
- construct a Matplotlib figure with readable axes, labels, and a legend; and
- state what a figure shows directly and what it cannot establish alone.
:::

:::{div}
:class: projector-lecture projector-slide

## Today’s example is deliberately not Project 1

We will use a small **synthetic rotating-star brightness** example: a starspot
can make measured brightness vary smoothly as the star rotates. This is a toy
periodic signal with invented values. It is not a transit model, it is not
Project 1 data, and it does not ask you to infer a planet.

We begin with one fixed synthetic observation record and compare it with a
separately named toy model. It gives us a controlled setting in which:

- time has units of days;
- brightness is dimensionless and normalized;
- a period is an assumption we state; and
- a plot can be read without completing a project analysis.
:::

:::{div}
:class: projector-lecture projector-slide

## I · An array represents one numerical quantity across positions

### Question

What must be true before one operation can safely apply to many values?

### You will leave this section able to

- distinguish a Python list from a numerical array;
- read an array’s shape, size, and dtype;
- create a stated numerical grid with np.linspace; and
- recognize elementwise arithmetic.

**Through-line focus:** named quantity $\rightarrow$ numerical array.
:::

:::{div}
:class: projector-lecture projector-slide

## A list and an array make different promises

~~~python
import numpy as np

brightness_list = [1.000, 0.997, 0.991]
brightness_array = np.array(brightness_list)

print(brightness_list * 2)
print(brightness_array * 2)
~~~

| Expression | Result | Meaning |
|---|---|---|
| brightness_list * 2 | repeats the list | Python list operation |
| brightness_array * 2 | doubles each value | elementwise numerical operation |

A NumPy array stores values in a regular, typed arrangement designed for
numerical work. It does not attach units, validate the scientific model, or
tell us whether two values are comparable. Those remain our responsibilities.
:::

:::{div}
:class: projector-lecture projector-slide

## Shape says how positions are organized

~~~python
observation_time_days = np.linspace(0.0, 6.0, 13)
observed_brightness = np.array([
    0.986, 0.971, 0.973, 0.984, 0.999, 0.997, 0.985,
    0.973, 0.970, 0.986, 0.997, 0.999, 0.984,
])

print("time shape:", observation_time_days.shape)
print("brightness shape:", observed_brightness.shape)
print("number of values:", observed_brightness.size)
print("stored dtype:", observed_brightness.dtype)
~~~

Both arrays have shape (13,): one dimension containing thirteen positions. Index i
refers to the same observation in each array:

~~~text
observation_time_days[i]  ↔  observed_brightness[i]
~~~

This pairing is part of the representation. A matching shape does not prove
that arrays are correctly paired, but a mismatching shape is an immediate
reason to stop and inspect the data.
:::

:::{div}
:class: projector-lecture projector-slide

## A numerical grid names its endpoints and count

~~~python
time_days = np.linspace(0.0, 4.0, 9)

print(time_days)
print("shape:", time_days.shape)
~~~

np.linspace(start, stop, count) creates count evenly spaced values, including
both endpoints. Here it creates nine times from 0.0 to 4.0 days.

| Question | Correct answer |
|---|---|
| What are the units? | days, because the variable is time_days |
| How many values? | 9 |
| Is 4.0 included? | yes |
| What is the spacing? | 0.5 days |

The grid is an input to a calculation, not an observation by itself.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · make a grid and a toy brightness series

:::{interactive-python}
:id: lecture-04-array-grid
:packages: numpy
:controls: {"period_days":{"label":"rotation period (days)","min":1,"max":6,"step":0.5,"value":3},"amplitude":{"label":"brightness amplitude","min":0.005,"max":0.04,"step":0.005,"value":0.02}}

import numpy as np

model_time_days = np.linspace(0.0, 6.0, 13)
phase = 2 * np.pi * model_time_days / period_days
model_brightness = 1.0 - amplitude * (1.0 + np.sin(phase)) / 2.0

print("time shape:", model_time_days.shape)
print("brightness shape:", model_brightness.shape)
print("first three times:", model_time_days[:3])
print("first three brightness values:", model_brightness[:3])
:::

Before running, predict the two shapes. Then change the period: does the
number of values change, or only their modeled brightness?

**Worked result:** both arrays have shape (13,). The grid fixes the number of
samples; the period changes the calculation at each sample.
:::::

:::{div}
:class: projector-lecture projector-slide

## Elementwise arithmetic follows positions, not whole-array algebra

~~~python
background_level = 0.003
corrected_brightness = observed_brightness - background_level

print(corrected_brightness[:3])
~~~

Subtracting a scalar from an array applies the subtraction to every element:

~~~text
[b₀, b₁, b₂, …] - background
    = [b₀ - background, b₁ - background, b₂ - background, …]
~~~

This is useful only when the scalar means the same thing for every position.
If background varies with time, it should be an array whose value at each
position is documented and aligned with observed_brightness.
:::

:::{div}
:class: projector-lecture projector-slide

## Array dtype is a computational choice, not a unit label

~~~python
integer_counts = np.array([1000, 997, 991])
normalized_brightness = integer_counts / integer_counts[0]

print(integer_counts.dtype)
print(normalized_brightness.dtype)
~~~

The first array stores integer counts. Division produces floating-point values
because normalized brightness is not generally an integer. Neither dtype tells
us whether the counts were calibrated, whether the denominator is appropriate,
or what uncertainty the normalization introduces.

**Keep this rule:** use variable names, labels, and documentation for units;
use dtype to understand numerical representation.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · array creation and inspection

| Expression | What it does |
|---|---|
| np.array(values) | creates an array from a sequence |
| np.linspace(start, stop, count) | creates a specified evenly spaced grid |
| array.shape | reports dimension lengths, such as (13,) |
| array.size | counts all elements |
| array.dtype | reports stored numerical type |
| array + scalar | adds the scalar to every element |
| array_1 + array_2 | adds corresponding positions when shapes are compatible |

**Keep this rule:** each axis and position needs a stated meaning before array
arithmetic can support an interpretation.
:::

:::{div}
:class: projector-lecture projector-slide

## II · Indexing and masks preserve or break the pairing

### Question

How do we select a subset of observations without separating values from the
coordinates that give them meaning?

### You will leave this section able to

- retrieve one position and a contiguous slice;
- construct a Boolean mask from a stated rule;
- apply the same mask to paired arrays; and
- count selected values before interpreting them.

**Through-line focus:** paired arrays $\rightarrow$ inspectable selection.
:::

:::{div}
:class: projector-lecture projector-slide

## Indexing asks for one known position

~~~python
print("third time:", observation_time_days[2], "days")
print("third brightness:", observed_brightness[2])
~~~

Python and NumPy count positions from zero. The pair at index 2 is the third
synthetic observation: 1.0 days and 0.973 normalized brightness.

Indexing is not a license to pick a convenient point after seeing the result.
Use an index when it has a stated role: first observation, known reference
point, a documented event, or a value chosen by a rule you can show.
:::

:::{div}
:class: projector-lecture projector-slide

## Slicing selects a contiguous range without changing order

~~~python
early_time_days = observation_time_days[:3]
early_brightness = observed_brightness[:3]

print(early_time_days)
print(early_brightness)
~~~

start:stop includes start and excludes stop. Thus [:3] selects positions 0, 1,
and 2. Slicing both arrays with the same slice preserves the time–brightness
pairing.

| Slice | Positions selected |
|---|---|
| [:3] | 0, 1, 2 |
| [2:] | 2 through the last |
| [1:4] | 1, 2, 3 |
| [::2] | every second position |
:::

:::{div}
:class: projector-lecture projector-slide

## A Boolean mask stores the result of one rule per position

~~~python
low_brightness = observed_brightness < 0.985

print(low_brightness)
~~~

The mask is an array of True and False values with the same shape as
brightness. It answers a limited question: which readings satisfy the declared
numerical threshold?

~~~text
observed brightness: [0.986, 0.971, 0.973, 0.984, ...]
low brightness:      [False,  True,  True,  True, ...]
~~~

The mask does not identify the physical cause of a low reading. It records the
output of one selection rule.
:::

:::::{div}
:class: projector-lecture projector-slide

## Predict · select the same observations from both arrays

:::{interactive-python}
:id: lecture-04-boolean-mask
:packages: numpy
:controls: {"threshold":{"label":"brightness threshold","min":0.96,"max":1.0,"step":0.005,"value":0.995}}

import numpy as np

observation_time_days = np.linspace(0.0, 6.0, 13)
observed_brightness = np.array([
    0.986, 0.971, 0.973, 0.984, 0.999, 0.997, 0.985,
    0.973, 0.970, 0.986, 0.997, 0.999, 0.984,
])

low_brightness = observed_brightness < threshold
selected_time_days = observation_time_days[low_brightness]
selected_brightness = observed_brightness[low_brightness]

print("mask:               ", low_brightness)
print("selected times:     ", selected_time_days)
print("selected brightness:", selected_brightness)
print("number selected:    ", low_brightness.sum())
:::

Before running, count the values you expect the mask to select. Then change the
threshold: why must the same mask be applied to both arrays?

**Worked result:** the Boolean mask retains the corresponding times and
brightness values together. low_brightness.sum() counts True values.
:::::

:::{div}
:class: projector-lecture projector-slide

## Compare numbers, not arrays, in an ordinary if

~~~python
if observed_brightness < 0.985:
    print("low")
~~~

This does not ask one true-or-false question; it produces a whole Boolean
array. Python will refuse to guess whether you mean “any value is low” or “all
values are low.”

~~~python
if np.any(observed_brightness < 0.985):
    print("at least one reading is below the threshold")

if np.all(observed_brightness > 0.95):
    print("every reading exceeds 0.95")
~~~

Use np.any and np.all only after saying which group-level claim you mean. They
do not replace a mask when you need the individual selected positions.
:::

:::::{div}
:class: projector-lecture projector-slide

## Selection rules should make their limits visible

:::{admonition} A threshold is not a physical explanation
:class: warning

observed_brightness < 0.985 selects readings below a stated numerical threshold. It does
not establish that starspots caused the variation, that the data are calibrated,
or that the threshold is scientifically appropriate.
:::

A useful figure can show the threshold so a reader can see the decision rule.
It cannot turn a decision rule into evidence for an unstated mechanism.
:::::

:::{div}
:class: projector-lecture projector-slide

## Reference · indexing and Boolean selection

| Expression | Result |
|---|---|
| array[i] | one value at position i |
| array[start:stop] | a contiguous slice; stop is excluded |
| array[mask] | values where the same-shaped mask is True |
| mask = values < threshold | one Boolean decision per position |
| mask.sum() | number of selected positions |
| np.any(mask) | whether at least one position is selected |
| np.all(mask) | whether every position is selected |

**Keep this rule:** paired quantities require the same selection in every
array that represents the same observations.
:::

:::{div}
:class: projector-lecture projector-slide

## III · Vectorize one stated model before plotting it

### Question

How can one function evaluate a simple model at many times without concealing
which position corresponds to which time?

### You will leave this section able to

- write a NumPy expression that evaluates elementwise;
- check a vectorized result against one scalar calculation.

**Through-line focus:** one model evaluation $\rightarrow$ a family of values.
:::

:::{div}
:class: projector-lecture projector-slide

## A vectorized function can accept an array without a Python loop

~~~python
import numpy as np

def rotating_star_brightness(time_days, period_days, amplitude):
    """Return toy normalized brightness for times and period in days."""
    if period_days <= 0:
        raise ValueError("period_days must be positive")
    if not 0 <= amplitude < 1:
        raise ValueError("amplitude must be in [0, 1)")
    phase = 2 * np.pi * time_days / period_days
    return 1.0 - amplitude * (1.0 + np.sin(phase)) / 2.0


model_time_days = np.linspace(0.0, 6.0, 121)
model_brightness = rotating_star_brightness(model_time_days, 3.0, 0.02)
~~~

Every operation in the final expression is elementwise. If model_time_days has
121 values, model_brightness has 121 values. The function remains a toy model: it does
not include spot evolution, measurement noise, or instrumental effects.
:::

:::{div}
:class: projector-lecture projector-slide

## Verify one vectorized value against the same scalar calculation

~~~python
model_time_days = np.linspace(0.0, 6.0, 121)
model_brightness = rotating_star_brightness(model_time_days, 3.0, 0.02)

scalar_at_day_1 = rotating_star_brightness(1.0, 3.0, 0.02)
array_at_day_1 = model_brightness[20]  # model_time_days[20] is 1.0 day

print(scalar_at_day_1)
print(array_at_day_1)
~~~

This is a cheap local check: at the same time and parameters, the scalar and
array paths should agree. It does not validate the physical model or prove that
the grid samples the system adequately.
:::

:::{div}
:class: projector-lecture projector-slide

## Shape errors usually reveal a representation question

~~~python
observation_time_days = np.linspace(0.0, 6.0, 13)
model_time_days = np.linspace(0.0, 6.0, 121)

residual = observation_time_days - model_time_days
~~~

These arrays have shapes (13,) and (121,). NumPy cannot align them elementwise,
and it should not try to invent a correspondence. Do not “fix” a shape error by
truncating or reshaping values until you can state why positions should
correspond.

Ask first:

1. What does each axis mean?
2. Which positions should be compared?
3. Did a prior selection or grid construction change one array?
:::

:::{div}
:class: projector-lecture projector-slide

## Extension · broadcasting is a next-step array skill

Broadcasting compares a family of parameter choices over one grid by adding
length-one axes. It is useful, but it is not needed to make the model-versus-
observation figure in this lecture.

After you can explain the one-dimensional arrays above, complete the
[Vectorization and Broadcasting Lab](../07-practice-labs/vectorization-broadcasting.md).
There you will name rows, columns, and each array shape before using a
two-dimensional result.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · vectorization and compatible shapes

| Idea | Read it as… |
|---|---|
| elementwise operation | apply one operation at corresponding positions |
| (n,) | one-dimensional array with n positions |
| scalar check | compare one array position to the same scalar calculation |
| shape error | stop and state which positions should correspond |

**Keep this rule:** write the shape and the physical meaning of every position
before you combine two arrays.
:::

:::{div}
:class: projector-lecture projector-slide

## IV · A figure is a compact argument with visible assumptions

### Question

What does a reader need to see to distinguish measured values, a model curve,
and a selection rule?

### You will leave this section able to

- create a figure and axes with plt.subplots();
- use labels, units, legend entries, markers, and line styles deliberately;
- show a selection threshold without overstating it; and
- write a bounded evidence statement from a figure.

**Through-line focus:** arrays and model $\rightarrow$ inspectable evidence.
:::

:::{div}
:class: projector-lecture projector-slide

## Start with a figure and axes object

~~~python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(
    observation_time_days,
    observed_brightness,
    marker="o",
    linestyle="none",
    label="synthetic observations",
)
plt.show()
~~~

fig is the whole figure. ax is the plotting area that owns the data, labels,
limits, legend, and grid. Keeping a name for ax makes later choices explicit:

~~~python
ax.set(xlabel="Time (days)", ylabel="Normalized brightness")
ax.legend()
~~~

Use fig, ax = plt.subplots() as the default course pattern. It scales to
multiple axes and keeps figure decisions attached to the right object.
:::

:::{div}
:class: projector-lecture projector-slide

## Every visual element should answer a reader’s question

~~~python
fig, ax = plt.subplots()
ax.plot(
    observation_time_days,
    observed_brightness,
    marker="o",
    linestyle="none",
    label="synthetic observations",
)
ax.plot(
    model_time_days,
    model_brightness,
    color="tab:blue",
    label="toy rotating-star model",
)
ax.set(
    xlabel="Time (days)",
    ylabel="Normalized brightness",
    title="Synthetic periodic brightness variation",
)
ax.grid(alpha=0.25)
ax.legend()
plt.show()
~~~

| Element | What it lets a reader inspect |
|---|---|
| marker without a line | discrete synthetic observations |
| line | toy model evaluated on a denser grid |
| axis labels | the quantity and its units |
| title | what is shown, without a discovery claim |
| legend | which graphical marks belong to which series |
| grid | approximate coordinate reading |
:::

:::{div}
:class: projector-lecture projector-slide

## A threshold needs a label and a limited interpretation

~~~python
threshold = 0.985

fig, ax = plt.subplots()
ax.plot(
    observation_time_days,
    observed_brightness,
    marker="o",
    linestyle="none",
    label="synthetic observations",
)
ax.plot(model_time_days, model_brightness, label="toy rotating-star model")
ax.axhline(
    threshold,
    color="tab:red",
    linestyle="--",
    label="illustrative low-brightness threshold",
)
ax.set(xlabel="Time (days)", ylabel="Normalized brightness")
ax.legend()
ax.grid(alpha=0.25)
plt.show()
~~~

The dashed style distinguishes the threshold from the brightness series even
for readers who do not distinguish the colors. The legend calls it
illustrative because the line communicates a rule for this exercise, not a
validated scientific classification.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · draw the toy data, model, and rule together

:::{interactive-python}
:id: lecture-04-figure
:packages: numpy,matplotlib
:controls: {"period_days":{"label":"rotation period (days)","min":1,"max":6,"step":0.5,"value":3},"amplitude":{"label":"brightness amplitude","min":0.01,"max":0.06,"step":0.005,"value":0.03},"threshold":{"label":"illustrative threshold","min":0.94,"max":1.0,"step":0.005,"value":0.98}}

import numpy as np
import matplotlib.pyplot as plt

observation_time_days = np.linspace(0.0, 6.0, 13)
observed_brightness = np.array([
    0.986, 0.971, 0.973, 0.984, 0.999, 0.997, 0.985,
    0.973, 0.970, 0.986, 0.997, 0.999, 0.984,
])
model_time_days = np.linspace(0.0, 6.0, 121)
phase = 2 * np.pi * model_time_days / period_days
model_brightness = 1.0 - amplitude * (1.0 + np.sin(phase)) / 2.0

fig, ax = plt.subplots()
ax.plot(
    observation_time_days,
    observed_brightness,
    marker="o",
    linestyle="none",
    label="synthetic observations",
)
ax.plot(
    model_time_days,
    model_brightness,
    color="tab:blue",
    label="toy rotating-star model",
)
ax.axhline(
    threshold,
    color="tab:red",
    linestyle="--",
    label="illustrative threshold",
)
ax.set(
    xlabel="Time (days)",
    ylabel="Normalized brightness",
    title="Synthetic periodic brightness variation",
)
ax.grid(alpha=0.25)
ax.legend()
plt.show()
:::

Predict whether the curve crosses the threshold before changing a control. Then
name one thing this plot shows directly and one thing it does **not** establish.

**Worked interpretation:** the markers are fixed synthetic observations; the
line is the stated toy model; the dashed line is an illustrative threshold. The
agreement in this exercise does not establish that a measured star has this
period, amplitude, or physical cause.
:::::

:::{div}
:class: projector-lecture projector-slide

## Plotting choices can change the question a figure answers

~~~python
ax.set_xlim(0.0, 6.0)
ax.set_ylim(0.94, 1.01)
~~~

Axis limits can make small variations visible or hide meaningful context.
Choose them to serve a stated comparison, not to make a result look more
dramatic. When a convention requires an inverted axis—for example astronomical
magnitude—make that choice explicit:

~~~python
ax.invert_yaxis()  # only when the plotted quantity uses that convention
~~~

Normalized brightness is not magnitude. Do not invert its axis merely because
some astronomy plots have a reversed vertical direction.
:::

:::{div}
:class: projector-lecture projector-slide

## Write a bounded evidence statement

Use this three-part pattern after making a figure:

1. **What is visible:** “Several synthetic observations and the toy model lie
   below the 0.98 illustrative threshold.”
2. **What supports it:** “The labeled y-axis, circular observation markers,
   solid model line, and dashed threshold make those three elements distinct.”
3. **What remains open:** “The toy model contains no measured uncertainty,
   calibration, or competing physical explanation.”

The boundary is not a weakness. It tells a reader where the figure’s evidence
ends and the next scientific question begins.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · a readable Matplotlib figure

| Pattern | Purpose |
|---|---|
| fig, ax = plt.subplots() | create a figure and named axes |
| ax.plot(x, y, marker="o", linestyle="none", label="…") | plot discrete observations with an inspectable legend entry |
| ax.plot(model_x, model_y, label="…") | draw a separate model curve |
| ax.axhline(value, linestyle="--", label="…") | show a horizontal rule or threshold |
| ax.set(xlabel="…", ylabel="…", title="…") | name quantities, units, and the figure’s subject |
| ax.legend() | identify plotted series and rules |
| ax.grid(alpha=0.25) | aid coordinate reading without dominating the data |
| ax.set_xlim(...); ax.set_ylim(...) | choose a visible domain deliberately |
| plt.show() | display the completed figure |

**Keep this rule:** a figure should make its variables, units, model status,
and selection rule easier to inspect—not harder.
:::

:::{div}
:class: projector-lecture projector-slide

## Exit check

A teammate makes a plot with this code:

~~~python
ax.plot(observation_time_days, observed_brightness)
ax.axhline(0.985)
~~~

Name three additions needed before it can serve as an inspectable course figure,
and explain why each matters. Then answer:

1. Which marks in your revised plot are observations, which are the model, and
   which are the threshold?
2. Why must one Boolean mask be applied to both observation_time_days and
   observed_brightness?
3. What does a threshold line show directly—and what does it not establish?
:::

:::{div}
:class: projector-lecture projector-slide

## Carry forward

You now have a workflow for a small numerical question:

~~~text
state quantities and units
→ build and inspect arrays
→ select with a documented rule
→ evaluate a stated model
→ make a labeled figure
→ claim only what the figure supports
~~~

The next time you use arrays or plots in a project, reuse this workflow—but do
not mistake this toy stellar-variability example for a solution template. The
project’s question, data, assumptions, and validation needs determine the next
steps.
:::
