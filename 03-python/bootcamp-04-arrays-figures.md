---
title: "Lecture 4 · NumPy, Matplotlib, and Readable Evidence"
subtitle: "Block 1 · Week 2 | Chapters 7–8"
site:
  hide_toc: true
kernelspec:
  name: python3
  display_name: Python 3
---

:::{projector-controls}
:id: lecture-04-controls
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## NumPy, Matplotlib, and readable evidence

### Arrays, figures, and executable code

Use one small synthetic brightness record to inspect arrays and figures.

Run the Python cells in order. They print the arrays and render the figures
used in this lecture.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Use the docs for the full API

We show a small, useful subset of NumPy and Matplotlib. Use the official docs
to check the full API: signatures, options, return values, errors, and examples.

- NumPy: [user guide](https://numpy.org/doc/stable/user/index.html) · [API reference](https://numpy.org/doc/stable/reference/index.html)
- Matplotlib: [documentation](https://matplotlib.org/stable/index.html) · [API reference](https://matplotlib.org/stable/api/index.html) · [cheatsheets](https://matplotlib.org/cheatsheets/) · [Figure anatomy](https://matplotlib.org/stable/gallery/showcase/anatomy.html)
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## The through-line

:::{div}
:class: lecture-through-line

1. **A numerical record**
2. **A one-dimensional array**
3. **A selection rule**
4. **Named axes in an ND array**
5. **A vectorized calculation**
6. **A labeled figure**
7. **A limited claim**
:::

State what positions, axes, and marks mean before interpreting a result.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Today’s question

How do we organize values across positions and axes, select and combine them
safely, and make a figure a reader can check?

By the end of class, you should be able to:

- create and inspect NumPy arrays with `shape`, `size`, and `dtype`;
- use indexing, slicing, and Boolean masks while preserving aligned data;
- read and index 2-D and ND arrays by their named axes and shape order;
- use a length-one axis to broadcast an explicitly owned quantity safely;
- write and check a vectorized calculation; and
- construct a readable Matplotlib figure and state what it shows—and what it
  cannot establish alone.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## One synthetic record supplies the values

These synthetic brightness measurements let us practice array operations and
plots without reproducing a Project 1 analysis. A periodic reference curve
appears later to distinguish calculated values from observations.

| Quantity | Meaning | Units |
| --- | --- | --- |
| `observation_time_days` | observation time | days |
| `observed_brightness` | invented measurement | normalized; dimensionless |
| `reference_period_days` | period used by one reference curve | days |
| `dimming_depth` | reference-curve drop from bright to dim | dimensionless |
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## I · NumPy arrays: quantities, positions, and elementwise operations

### Question

What is an array, and what must be true before one operation can safely apply
to many values?

### You will leave this section able to

- distinguish a Python list from a NumPy array;
- read `shape`, `size`, and `dtype`;
- create a numerical grid with `np.linspace`; and
- explain elementwise arithmetic.

**Through-line focus:** named quantity → numerical array.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A list and an array make different promises

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

- A `list` can hold related Python objects.
- A numerical array supports elementwise arithmetic.
- Neither stores units or validates a model for you.
:::

:::{div}
:class: lecture-column

```{code-cell} python
import numpy as np

brightness_list = [1.000, 0.997, 0.991]
brightness_array = np.array(brightness_list)

print("list * 2:", brightness_list * 2)
print("array * 2:", brightness_array * 2)
```

| Expression | Meaning |
| --- | --- |
| `brightness_list * 2` | Python repeats the list. |
| `brightness_array * 2` | NumPy doubles each position. |
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Shape says how positions are organized

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

```{code-cell} python
observation_time_days = np.linspace(0.0, 6.0, 13)
observed_brightness = np.array([
    0.986, 0.971, 0.973, 0.984, 0.999, 0.997, 0.985,
    0.973, 0.970, 0.986, 0.997, 0.999, 0.984,
])

print("time:", observation_time_days)
print("brightness:", observed_brightness)
print("time shape:", observation_time_days.shape)
print("brightness shape:", observed_brightness.shape)
print("number of observations:", observed_brightness.size)
print("dtype:", observed_brightness.dtype)
```
:::

:::{div}
:class: lecture-column

`shape` says how positions are organized. Both arrays have shape `(13,)`:
one dimension with one value per observation, in order.

Index `i` has the same meaning in both arrays:

`observation_time_days[i]` ↔ `observed_brightness[i]`

Matching shapes do not prove a correct pairing. A mismatch is an immediate
reason to stop and inspect the record.
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A numerical grid names its endpoints and count

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`np.linspace(start, stop, num)` returns `num` evenly spaced values,
including both endpoints.

The grid is an input to a calculation, not an observation by itself.
:::

:::{div}
:class: lecture-column

```{code-cell} python
time_days = np.linspace(0.0, 4.0, 9)

print("time grid:", time_days)
print("shape:", time_days.shape)
print("spacing:", time_days[1] - time_days[0], "days")
```
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Common array generators

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

Choose a generator from the structure you need:

- `np.arange` for integer steps;
- `np.linspace` for a stated interval and count;
- `np.logspace` for powers of a base;
- `np.zeros`, `np.ones`, or `np.full` for a stated shape and initial value.
:::

:::{div}
:class: lecture-column

```{code-cell} python
integer_steps = np.arange(0, 5)
log_values = np.logspace(0, 3, 4)
blank_by_source = np.zeros((3, 5))
unit_weights = np.ones(5)
missing_values = np.full(5, np.nan)

print("integer steps:", integer_steps)
print("log values:", log_values)
print("blank shape:", blank_by_source.shape)
print("weights:", unit_weights)
print("missing values:", missing_values)
```
:::
::::

`np.logspace(0, 3, 4)` returns `10**0` through `10**3`. For a floating-point
grid with a stated number of values, use `np.linspace` rather than `np.arange`.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Elementwise arithmetic follows positions

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

Subtracting a scalar applies the same operation at every position.

`[b₀, b₁, b₂, …] - background`

`= [b₀ - background, b₁ - background, b₂ - background, …]`

This only makes sense when the scalar has the same meaning for every
observation. A time-dependent correction needs an aligned array.
:::

:::{div}
:class: lecture-column

```{code-cell} python
background_level = 0.003
corrected_brightness = observed_brightness - background_level

print("first three corrected values:", corrected_brightness[:3])
print("shape preserved:", corrected_brightness.shape)
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## `dtype` is a numerical representation, not a unit

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`integer_counts` stores integers. Division produces floating-point normalized
brightness because the result is not generally an integer.

Use variable names, labels, and documentation for units. Use `dtype` to
inspect how values are stored.
:::

:::{div}
:class: lecture-column

```{code-cell} python
integer_counts = np.array([1000, 997, 991])
normalized_brightness = integer_counts / integer_counts[0]

print("count dtype:", integer_counts.dtype)
print("normalized dtype:", normalized_brightness.dtype)
print("normalized values:", normalized_brightness)
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · array creation and inspection

| Expression | What it does |
| --- | --- |
| `np.array(values)` | Creates an array from a sequence. |
| `np.arange(start, stop, step)` | Creates regularly spaced values; `stop` is excluded. |
| `np.linspace(start, stop, num)` | Creates an evenly spaced grid. |
| `np.logspace(start, stop, num)` | Creates powers of `10` from `10**start` through `10**stop` with the default `base=10`. |
| `np.zeros(shape)` | Creates an array of zeros with the given shape. |
| `np.ones(shape)` | Creates an array of ones with the given shape. |
| `np.full(shape, fill_value)` | Creates an array filled with one value. |
| `np.eye(N)` | Creates an `N`-by-`N` array with ones on the main diagonal. |
| `array.shape` | Reports dimension lengths, such as `(13,)`. |
| `array.size` | Counts all elements. |
| `array.dtype` | Reports stored numerical type. |
| `array + scalar` | Applies the operation at every position. |

**Rule:** state what each position represents before combining
arrays.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## II · Indexing, slicing, and Boolean selection

### Question

How do we retrieve or select values while preserving the relationships among
aligned arrays?

### You will leave this section able to

- retrieve the first, last, or a contiguous range of positions;
- construct a Boolean mask from a stated rule;
- apply the same mask to paired arrays; and
- count selected values before interpreting them.

**Through-line focus:** paired arrays → same selection.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Indexing starts at `0`; negative indices count from the end

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

- `values[0]` selects the first position; `values[1]` selects the second.
- `values[-1]` selects the last position; `values[-2]` selects the one before it.
- `values[start:stop]` includes `start` and stops before `stop`.
- Apply the same slice to every array in the same record.

Indexing is not permission to choose a convenient point after seeing a result.
Use it for a stated role: a reference point, documented event, or predeclared
check.
:::

:::{div}
:class: lecture-column

```{code-cell} python
first_time_days = observation_time_days[0]
third_time_days = observation_time_days[2]
last_time_days = observation_time_days[-1]
penultimate_time_days = observation_time_days[-2]
third_brightness = observed_brightness[2]
early_time_days = observation_time_days[:3]
early_brightness = observed_brightness[:3]

print("first observation:", first_time_days, "days")
print("third observation:", third_time_days, "days;", third_brightness)
print("last observation:", last_time_days, "days")
print("one before last:", penultimate_time_days, "days")
print("early times:", early_time_days)
print("early brightness:", early_brightness)

assert observation_time_days[-1] == observation_time_days[len(observation_time_days) - 1]
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A Boolean mask selects the same positions from both arrays

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

Make one mask, then use it on every aligned array.

The mask has one `True` or `False` value per observation. Applying it to both
arrays preserves the time--brightness pairing.
:::

:::{div}
:class: lecture-column

```{code-cell} python
low_brightness = observed_brightness < 0.985

print("mask:", low_brightness)
print("selected times:", observation_time_days[low_brightness])
print("selected brightness:", observed_brightness[low_brightness])
print("selected count:", np.count_nonzero(low_brightness))
```
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Arrays need an explicit many-value question

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`if low_brightness:` fails because `low_brightness` contains many Boolean
values.

Use `np.any` for “at least one” and `np.all` for “every.”
:::

:::{div}
:class: lecture-column

```{code-cell} python
try:
    if low_brightness:
        print("This will not run.")
except ValueError as error:
    print(type(error).__name__ + ":", error)

print("any low values?", np.any(low_brightness))
print("all low values?", np.all(low_brightness))
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A threshold is a selection rule

:::{admonition} State the rule
:class: warning

`observed_brightness < 0.985` selects readings below a stated numerical
threshold.
:::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · indexing and Boolean selection

| Expression | Read it as |
| --- | --- |
| `array[0]` | First position. |
| `array[-1]` | Last position. |
| `array[i]` | One value at position `i`. |
| `array[start:stop]` | A slice; `stop` is excluded. |
| `array[mask]` | Positions where the same-shaped mask is `True`. |
| `mask = values < threshold` | One Boolean decision per position. |
| `np.count_nonzero(mask)` | Number of selected positions. |
| `np.any(mask)` / `np.all(mask)` | At least one / every position. |

**Rule:** use the same selection on every array that describes the
same observations.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## III · 2-D and ND arrays: matrices, axes, and shape

### Question

How do we represent values across multiple named axes without losing the
meaning of any dimension?

### You will leave this section able to

- read `ndim` and a two-dimensional `shape`;
- state what each axis and position represents;
- index a row, column, or one specific value;
- state what `axis=0` and `axis=1` leave behind; and
- broadcast one owned value per source across time.

**Through-line focus:** named positions → named axes.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A 2-D array can represent a labeled matrix

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

A regular two-dimensional `ndarray` is NumPy’s representation for a matrix or
any rectangular table of values. Its shape uses the matrix convention:
`(number_of_rows, number_of_columns)`.

`brightness_by_source` is a measurement matrix with shape `(3, 5)`:

- axis `0`: three sources (rows);
- axis `1`: five observing times (columns);
- `brightness_by_source[source_index, time_index]`: one measurement.

The layout is matrix-like; the axis meanings are scientific: `(source, time)`.
State what every axis owns.

`*` is elementwise multiplication for `ndarray` objects. `A @ B` is matrix
multiplication. Use `@` only when the inner dimensions and the linear mapping
have been stated.

Here, matrices are data tables with named axes. We will use matrix
multiplication when its linear-algebra meaning is the topic.
:::

:::{div}
:class: lecture-column lecture-matrix

| source row / time column | `0` (0 days) | `1` (1 day) | `2` (2 days) | `3` (3 days) | `4` (4 days) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0` · source A | 1.000 | 0.998 | 0.985 | 0.997 | 1.001 |
| `1` · source B | 0.980 | 0.979 | **0.966** | 0.978 | 0.981 |
| `2` · source C | 1.020 | 1.018 | 1.006 | 1.017 | 1.021 |

`brightness_by_source[1, 2]` is the bold entry: source B at day `2.0`.
:::
::::

```{code-cell} python
source_labels = np.array(["A", "B", "C"])
sample_time_days = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
brightness_by_source = np.array([
    [1.000, 0.998, 0.985, 0.997, 1.001],
    [0.980, 0.979, 0.966, 0.978, 0.981],
    [1.020, 1.018, 1.006, 1.017, 1.021],
])

print("ndim:", brightness_by_source.ndim)
print("shape:", brightness_by_source.shape)
print("row labels:", source_labels)
print("column times (days):", sample_time_days)
```
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Matrix order and coordinate order are different conventions

For a matrix or ordinary 2-D array, use `array[row, column]`: first vertical
row, then horizontal column.

Cartesian coordinates are conventionally written `(x, y)`: horizontal
position first, then vertical position. An image stored in a 2-D array is
therefore commonly accessed as `image[y, x]`, not `image[x, y]`.

:::{admonition} Write the convention before indexing
:class: warning

Do not infer an axis order from variable names alone. State whether a pair is
`(row, column)`, `(x, y)`, `(source, time)`, or another named convention.
:::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Shape and indexing use the same axis order

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

NumPy lists axis lengths left to right:

`array.shape == (axis_0_length, axis_1_length, ...)`

Indexing follows the same order:

`array[axis_0_index, axis_1_index, ...]`

For a conventional 2-D table, that is `(row, column)` and
`array[row, column]`. In this lecture, the axes are `(source, time)`, so
`brightness_by_source[source, time]` uses the same convention.

An array does not assign the meanings “row,” “column,” “source,” or “time.”
You define and document them.
:::

:::{div}
:class: lecture-column

```{code-cell} python
source_index = 1
time_index = 2

brightness_by_time_source = brightness_by_source.T

print("axis order:", "(source, time)")
print("shape:", brightness_by_source.shape)
print("value at [source, time]:", brightness_by_source[source_index, time_index])
print("transposed axis order:", "(time, source)")
print("transposed shape:", brightness_by_time_source.shape)
print("same value at [time, source]:", brightness_by_time_source[time_index, source_index])

assert (
    brightness_by_source[source_index, time_index]
    == brightness_by_time_source[time_index, source_index]
)
```

For a 3-D array, use the same rule: a shape such as `(3, 5, 2)` could mean
`(source, time, filter)` and be indexed as `array[source, time, filter]`.
:::
::::

:::{admonition} Memory order is separate
:class: note

New NumPy arrays use C order by default, so the last index changes fastest in
memory. That does not assign scientific meaning to an axis. Use `shape`,
indexing, and documented axis names to establish meaning.
:::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Indexing a 2-D array names both axes

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

Read these in order:

- `brightness_by_source[1]` selects source `B` across all times: shape `(5,)`.
- `brightness_by_source[:, 2]` selects all sources at day `2.0`: shape `(3,)`.
- `brightness_by_source[1, 2]` selects one scalar measurement.
:::

:::{div}
:class: lecture-column

```{code-cell} python
source_index = 1
time_index = 2

print("one source:", brightness_by_source[source_index])
print("one time across sources:", brightness_by_source[:, time_index])
print(
    "one measurement:",
    source_labels[source_index],
    "at day",
    sample_time_days[time_index],
    "=",
    brightness_by_source[source_index, time_index],
)
```
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A reduction consumes one axis

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`mean(axis=1)` reduces the time axis, leaving one mean per source.

`mean(axis=0)` reduces the source axis, leaving one mean per observing time.

The output shape is part of the scientific meaning, not an implementation
detail.
:::

:::{div}
:class: lecture-column

```{code-cell} python
mean_brightness_per_source = brightness_by_source.mean(axis=1)
mean_brightness_per_time = brightness_by_source.mean(axis=0)

print("per-source shape:", mean_brightness_per_source.shape)
print("per-source means:", mean_brightness_per_source)
print("per-time shape:", mean_brightness_per_time.shape)
print("per-time means:", mean_brightness_per_time)
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Broadcasting: one operation across compatible shapes

**Definition:** Broadcasting is NumPy’s shape-matching rule for elementwise
operations. NumPy aligns shapes from the right. On each aligned axis, the
lengths must match or one length must be `1`; missing leading axes behave like
length `1`. The result uses the larger length on each axis.

NumPy does not need to copy a value into a larger array. Broadcasting describes
how the operation is evaluated.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Apply the shape rule before the operation

| Left shape | Right shape | Result shape | What repeats conceptually |
| --- | --- | --- | --- |
| `(3, 5)` | `(5,)` | `(3, 5)` | One value per column across every row. |
| `(3, 5)` | `(3, 1)` | `(3, 5)` | One value per row across every column. |
| `(3, 1)` | `(1, 5)` | `(3, 5)` | A row quantity and column quantity combine. |
| `(3, 5)` | `(3,)` | error | Trailing lengths `5` and `3` conflict. |

Equal lengths are compatible. A length-one axis can expand. Any other pair of
aligned lengths raises `ValueError`.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## See broadcasting on generic rows and columns

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`values_by_row_and_column` has shape `(3, 5)`.

- `per_column` has shape `(5,)`, so it aligns with the trailing column axis.
- `per_row` has shape `(3,)`, so it conflicts with the trailing axis.
- `per_row[:, np.newaxis]` has shape `(3, 1)`, so its length-one column axis
  expands across five columns.
:::

:::{div}
:class: lecture-column

```{code-cell} python
values_by_row_and_column = np.zeros((3, 5))
per_column = np.array([10, 20, 30, 40, 50])
per_row = np.array([1, 2, 3])

print("per-column result shape:", (values_by_row_and_column + per_column).shape)

try:
    values_by_row_and_column + per_row
except ValueError as error:
    print("per-row without newaxis:", type(error).__name__)

per_row_column = per_row[:, np.newaxis]
print("per-row result shape:", (values_by_row_and_column + per_row_column).shape)
print("per-row result:\n", values_by_row_and_column + per_row_column)
```
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Apply broadcasting to one baseline per source

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`brightness_by_source` has shape `(3, 5)` with axes `(source, time)`.
`baseline_per_source` has shape `(3,)`. Right alignment compares its `3` with
the table’s trailing time length `5`, so the operation fails.

`baseline_per_source[:, np.newaxis]` has shape `(3, 1)`: one baseline per
source and a length-one time axis. Broadcasting expands that time axis across
the five columns, giving shape `(3, 5)`.
:::

:::{div}
:class: lecture-column

```{code-cell} python
baseline_per_source = brightness_by_source[:, 0]

try:
    brightness_by_source / baseline_per_source
except ValueError as error:
    print("without an explicit axis:", type(error).__name__)

baseline_column = baseline_per_source[:, np.newaxis]
normalized_by_source = brightness_by_source / baseline_column

assert normalized_by_source.shape == brightness_by_source.shape
assert np.allclose(normalized_by_source[:, 0], 1.0)
print("baseline shape:", baseline_per_source.shape)
print("explicit baseline shape:", baseline_column.shape)
print("normalized shape:", normalized_by_source.shape)
print("first normalized row:", normalized_by_source[0])
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · ND arrays, axes, and broadcasting

| Expression | Read it as |
| --- | --- |
| `array.ndim` | Number of axes. |
| `array.shape == (3, 5)` | Three row positions and five column positions. |
| `array[row, column]` | One value with both positions named. |
| `array.mean(axis=1)` | One value per row after reducing columns. |
| `array.mean(axis=0)` | One value per column after reducing rows. |
| `values[:, np.newaxis]` | Add a length-one column axis. |
| `array + values` | Align shapes from the right; each axis must match or have length `1`. |

**Rule:** before combining ND arrays, name each axis, its owner, and
the expected output shape.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Practice the 2-D case before using it in larger work

The [Vectorization and Broadcasting Lab](../07-practice-labs/vectorization-broadcasting.md)
repeats this reasoning with a fresh data table. Complete it after this lecture:
predict a shape, write the axis meaning, then run the expression.

Then complete the [ND Array Evidence Check](../08-assessments/nd-array-evidence-check.md):
state axes and shapes, broadcast a baseline, make a figure, and write a bounded
claim.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## IV · Vectorized calculations and shape checks

### Question

How can one stated calculation accept a scalar or many positions while
preserving correspondence and checking shape?

### You will leave this section able to

- write a vectorized function with an explicit input contract;
- check an array result against one scalar result; and
- distinguish a vectorized one-dimensional calculation from an ND-array
  broadcasting operation.

**Through-line focus:** paired array → stated calculation.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A vectorized calculation accepts a scalar, list, or array

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`time_days` must be finite. `reference_period_days` must be finite and
positive. `dimming_depth` is the drop from `1.0` to
`1.0 - dimming_depth` in this reference curve.
:::

:::{div}
:class: lecture-column

```{code-cell} python
def periodic_reference_brightness(time_days, reference_period_days, dimming_depth):
    """Return a periodic reference curve for finite times in days.

    dimming_depth sets the drop from 1.0 to 1.0 - dimming_depth.
    """
    time_days = np.asarray(time_days, dtype=float)
    if not np.all(np.isfinite(time_days)):
        raise ValueError("time_days must contain only finite values")
    if not np.isfinite(reference_period_days) or reference_period_days <= 0:
        raise ValueError("reference_period_days must be finite and positive")
    if not np.isfinite(dimming_depth) or not 0 <= dimming_depth < 1:
        raise ValueError("dimming_depth must be finite and in [0, 1)")

    phase = 2.0 * np.pi * time_days / reference_period_days
    return 1.0 - dimming_depth * (1.0 + np.sin(phase)) / 2.0


reference_period_days = 3.0
dimming_depth = 0.030
reference_brightness = periodic_reference_brightness(
    observation_time_days,
    reference_period_days,
    dimming_depth,
)

print("reference shape:", reference_brightness.shape)
print("reference values:", np.round(reference_brightness, 4))
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Check one vectorized result against one scalar call

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

The assertion checks the scalar and vector paths at the same input.
:::

:::{div}
:class: lecture-column

```{code-cell} python
index = 4
scalar_brightness = periodic_reference_brightness(
    observation_time_days[index],
    reference_period_days,
    dimming_depth,
)

np.testing.assert_allclose(
    reference_brightness[index],
    scalar_brightness,
    rtol=0.0,
    atol=1e-12,
)
print("scalar and vector results agree at index", index)
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## A shape error asks a representation question

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

These arrays represent different grids: one has `13` positions and the other
has `400`. NumPy should not invent a one-to-one correspondence.

Before combining arrays, ask:

1. What does each position mean?
2. Which positions should correspond?
3. Did a grid or selection change one array?
:::

:::{div}
:class: lecture-column

```{code-cell} python
reference_time_days = np.linspace(0.0, 6.0, 400)

try:
    observation_time_days - reference_time_days
except ValueError as error:
    print(type(error).__name__ + ":", error)
```
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · vectorization and compatible shapes

| Idea | Read it as |
| --- | --- |
| Elementwise operation | Apply one operation at corresponding positions. |
| `(n,)` | One-dimensional array with `n` positions. |
| Scalar check | Compare one array position with the same scalar calculation. |
| Shape error | Stop and state which positions should correspond. |

**Rule:** write the shape and physical meaning of every position
before combining arrays.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## V · Matplotlib: readable figures and bounded evidence

### Question

What must a reader identify to interpret a figure and assess a bounded claim?

### You will leave this section able to

- create a figure and axes object;
- distinguish observations, a reference calculation, and a threshold;
- choose scales and axis direction deliberately; and
- write a bounded evidence statement from a figure.

**Through-line focus:** stated calculation → readable figure.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Run this: render the observations

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

`fig` is the whole figure. `ax` is the plotting area that owns the data,
labels, limits, legend, and grid.

Use `fig, ax = plt.subplots()` as the default course pattern. It keeps later
choices attached to a named axes object and extends cleanly to multi-panel
figures.
:::

:::{div}
:class: lecture-column

```{code-cell} python
:tags: [remove-output]

import matplotlib.pyplot as plt

fig, ax = plt.subplots(
    figsize=(8.5, 4.8),
    layout="constrained",
)
ax.scatter(
    observation_time_days,
    observed_brightness,
    color="#0072B2",
    marker="o",
    label="synthetic observations",
)
ax.set(
    xlabel="Observation time (days)",
    ylabel="Normalized brightness (dimensionless)",
    title="Synthetic observations",
)
ax.grid(alpha=0.25)
ax.legend()
fig.savefig(
    "lecture-04-synthetic-observations.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

::::{figure} lecture-04-synthetic-observations.png
:label: fig:synthetic-observations
:alt: Thirteen blue circular markers show synthetic normalized brightness from 0 to 6 days, ranging from 0.970 to 0.999. No curve is shown.

Synthetic observations plotted as discrete markers.
::::

**Read the rendered output:** each circle is one observation. No curve is shown
yet.
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Add a separately named reference curve

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

A line can look more authoritative than the data. Name it as a reference
calculation and use a denser, separately named grid so the reader can
distinguish calculated values from observations.
:::

:::{div}
:class: lecture-column

```{code-cell} python
:tags: [remove-output]

reference_time_days = np.linspace(0.0, 6.0, 400)
smooth_reference_brightness = periodic_reference_brightness(
    reference_time_days,
    reference_period_days,
    dimming_depth,
)

comparison_fig, comparison_ax = plt.subplots(
    figsize=(8.5, 4.8),
    layout="constrained",
)
comparison_ax.scatter(
    observation_time_days,
    observed_brightness,
    color="#0072B2",
    marker="o",
    label="synthetic observations",
    zorder=3,
)
comparison_ax.plot(
    reference_time_days,
    smooth_reference_brightness,
    color="#D55E00",
    linestyle="-",
    label="periodic reference curve",
)
comparison_ax.set(
    xlabel="Observation time (days)",
    ylabel="Normalized brightness (dimensionless)",
    title="Synthetic observations and a reference calculation",
    xlim=(0.0, 6.0),
)
comparison_ax.grid(alpha=0.25)
comparison_ax.legend()
comparison_fig.savefig(
    "lecture-04-observations-reference.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

::::{figure} lecture-04-observations-reference.png
:label: fig:observations-reference
:alt: Thirteen blue circular observations are plotted from 0 to 6 days with an orange periodic reference curve on a denser time grid. Both range from about 0.970 to 1.000.

Synthetic observations and a separately evaluated reference curve.
::::

**Read the rendered output:** markers are 13 observations; the solid line uses
a denser reference grid.
:::
::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Add a threshold and complete the figure

```{code-cell} python
:tags: [remove-output]

import matplotlib.pyplot as plt

reference_time_days = np.linspace(0.0, 6.0, 400)
smooth_reference_brightness = periodic_reference_brightness(
    reference_time_days,
    reference_period_days,
    dimming_depth,
)
threshold_brightness = 0.985

brightness_fig, ax = plt.subplots(figsize=(8.5, 4.8), layout="constrained")
ax.scatter(
    observation_time_days,
    observed_brightness,
    color="#0072B2",
    marker="o",
    label="synthetic observations",
    zorder=3,
)
ax.plot(
    reference_time_days,
    smooth_reference_brightness,
    color="#D55E00",
    linestyle="-",
    label="periodic reference curve",
)
ax.axhline(
    threshold_brightness,
    color="#4D4D4D",
    linestyle="--",
    label="illustrative threshold",
)
ax.set(
    xlabel="Observation time (days)",
    ylabel="Normalized brightness (dimensionless)",
    title="Synthetic brightness observations and a reference calculation",
    xlim=(0.0, 6.0),
)
ax.grid(alpha=0.25)
ax.legend()
brightness_fig.savefig(
    "lecture-04-synthetic-brightness-figure.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

::::{figure} lecture-04-synthetic-brightness-figure.png
:label: fig:observations-reference-threshold
:alt: Thirteen blue circular observations and an orange periodic reference curve range from about 0.970 to 1.000 normalized brightness. A gray dashed horizontal line marks the illustrative 0.985 threshold.

Synthetic observations, a periodic reference curve, and an illustrative threshold.
::::

- Circles are the synthetic observations.
- The solid line is a reference calculation, not a fit.
- The dashed line is an illustrative threshold.
- Marker shape and line style work even without color.

**Read the rendered output:** markers, the solid line, and the dashed line
represent different things. The legend names them.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Use figure anatomy as a checklist

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

The [Matplotlib Anatomy of a Figure](https://matplotlib.org/stable/gallery/showcase/anatomy.html)
is a reference for figure and axes vocabulary.

```{code-cell} python
from pathlib import Path

export_path = Path("lecture-04-synthetic-brightness-figure.png")
brightness_fig.savefig(
    export_path,
    dpi=200,
    bbox_inches="tight",
)
print(f"saved: {export_path} (exists: {export_path.exists()})")
```

`plt.show()` displays a figure in a notebook. `savefig(...)` writes an image
file. The examples do both so this page can display the executed figures.

Save only after you set labels, limits, scale, and legend.
:::

:::{div}
:class: lecture-column

| Part | Check |
| --- | --- |
| Axis labels | Quantity and units are visible. |
| Limits and scale | The relevant range is visible. |
| Legend | Every encoding is identified. |
| Title or caption | It says what is shown. |
| Export | Text remains readable. |
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Check the axes before exporting

```{code-cell} python
print("x label:", ax.get_xlabel())
print("y label:", ax.get_ylabel())
print("title:", ax.get_title())
print("legend labels:", ax.get_legend_handles_labels()[1])
```

The figure object exposes labels and legend entries for code-based checks.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Scale changes what a reader can see

```{code-cell} python
:tags: [remove-output]

distance_pc = np.array([1.0, 10.0, 100.0, 1_000.0])
relative_signal = distance_pc ** -2

scale_fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.8), layout="constrained")

for ax, title in zip(axes, ("Linear axes", "Log--log axes")):
    ax.plot(distance_pc, relative_signal, marker="o", linestyle="-")
    ax.set(
        xlabel="Distance (pc)",
        ylabel="Relative signal (dimensionless)",
        title=title,
    )
    ax.grid(alpha=0.25)

axes[1].set_xscale("log")
axes[1].set_yscale("log")
scale_fig.savefig(
    "lecture-04-scale-comparison.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

::::{figure} lecture-04-scale-comparison.png
:label: fig:scale-comparison
:alt: Two panels show the same inverse-square relative signal versus distance from 1 to 1,000 parsecs. On linear axes the three farthest values cluster near zero; on log-log axes the points form a descending straight line.

The same inverse-square relationship on linear and log-log axes.
::::

The values are positive, so logarithmic axes are allowed. Equal ratios occupy
equal distances on a log axis. A log scale changes the view, not the values.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Axis direction is a stated convention

```{code-cell} python
:tags: [remove-output]

lookback_time_gyr = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
normalized_quantity = np.array([1.00, 0.93, 0.87, 0.80, 0.74])
detector_row = np.array([1, 2, 3, 4, 5])
row_signal = np.array([12, 9, 7, 10, 11])

direction_fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.8), layout="constrained")

axes[0].plot(lookback_time_gyr, normalized_quantity, marker="o", linestyle="-")
axes[0].invert_xaxis()
axes[0].set(
    xlabel="Lookback time (Gyr; present at right)",
    ylabel="Normalized quantity (dimensionless)",
    title="An inverted x-axis",
)
axes[0].grid(alpha=0.25)

axes[1].plot(row_signal, detector_row, marker="s", linestyle="-")
axes[1].invert_yaxis()
axes[1].set(
    xlabel="Detector signal (counts)",
    ylabel="Detector row (1 at top)",
    title="An inverted y-axis",
)
axes[1].grid(alpha=0.25)
direction_fig.savefig(
    "lecture-04-axis-direction.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
```

::::{figure} lecture-04-axis-direction.png
:label: fig:axis-direction
:alt: Two panels demonstrate stated axis inversions. The left panel places present-day lookback time at the right; the right panel places detector row 1 at the top.

Inverted axes require an explicit convention in the axis label.
::::

Call `invert_xaxis()` or `invert_yaxis()` only when the label states the
convention.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## State what the figure shows

Use three parts:

1. **Visible:** Several synthetic observations and portions of the reference
   curve lie below the `0.985` illustrative threshold.
2. **Evidence:** The labeled axes, circular markers, solid line, and
   dashed threshold distinguish the three visual elements.
3. **Open:** The reference calculation has no measured uncertainty,
   calibration, or competing physical explanation.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · a readable Matplotlib figure

| Pattern | Purpose |
| --- | --- |
| `fig, ax = plt.subplots()` | Creates a figure and named axes. |
| `ax.scatter(x, y, ...)` | Shows discrete observations. |
| `ax.plot(reference_x, reference_y, ...)` | Draws a separately named reference curve. |
| `ax.axhline(value, ...)` | Shows a horizontal rule or threshold. |
| `ax.set(xlabel=..., ylabel=..., title=...)` | Names quantities, units, and subject. |
| `ax.legend()` | Identifies plotted series and rules. |
| `ax.grid(alpha=0.25)` | Aids coordinate reading without dominating data. |
| `brightness_fig.savefig(...)` | Exports after the figure is checked. |

**Rule:** name variables, units, calculation status, and selection rules.
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Documentation for the next question

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

| Resource | Use it for |
| --- | --- |
| [NumPy user guide](https://numpy.org/doc/stable/user/index.html) | concepts and worked guides |
| [NumPy API reference](https://numpy.org/doc/stable/reference/index.html) | exact functions, parameters, and returns |
| [Matplotlib documentation](https://matplotlib.org/stable/index.html) | plotting guides and API |
| [Matplotlib API reference](https://matplotlib.org/stable/api/index.html) | exact plotting methods, parameters, and returns |
| [Matplotlib cheatsheets](https://matplotlib.org/cheatsheets/) | compact reminders |
| [Matplotlib Anatomy of a Figure](https://matplotlib.org/stable/gallery/showcase/anatomy.html) | figure and axes vocabulary |
:::

:::{div}
:class: lecture-column

Start with the user guide for concepts and worked examples. Use an API
reference when you need an exact parameter, return type, or error condition.

Use the cheatsheets and figure anatomy page while you are building a plot, not
after you have guessed at the method names.
:::
::::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Exit check

A teammate writes:

```python
ax.plot(observation_time_days, observed_brightness)
ax.axhline(0.985)
```

Name three additions needed before this can serve as a course figure, and say
why each matters. Then answer:

1. Why must one Boolean mask select both `observation_time_days` and
   `observed_brightness`?
2. What does a threshold line show directly? What does it not establish?
3. What does `reference_brightness.shape == observation_time_days.shape` check,
   and what does it not prove about the pairing?
4. `brightness_by_source` has shape `(3, 5)` and `baseline_per_source` has
   shape `(3,)`. Why does their division fail? What does
   `baseline_per_source[:, np.newaxis]` change, and why does `(3, 1)` work?
5. Why might a Cartesian point `(x, y)` be accessed as `image[y, x]` in a
   2-D image array?
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Carry forward

`state quantities and units`

`→ build and inspect arrays`

`→ select with a documented rule`

`→ evaluate a stated calculation`

`→ make a labeled figure`

`→ claim only what the figure supports`

Reuse this workflow in later work. The next scientific question determines the
data, assumptions, and validation it needs.
:::::
