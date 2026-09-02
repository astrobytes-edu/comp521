---
title: "Lecture 3 · Function Interfaces and Reusable Analysis"
subtitle: "Block 1 · Week 2 | Chapters 4–5 and the Grade Calculator"
site:
  hide_toc: true
---

:::{projector-controls}
:id: lecture-03-controls
:::

:::{div}
:class: projector-lecture projector-slide

## Function interfaces and reusable analysis

### Arguments, data records, and small functions that another person can call

Lecture 2 established the basic function contract: named inputs, validation,
and `return`. Today we continue that work. We will make calls readable, pass
structured observations without losing their meaning, and decide when a
function should accept a flexible number of inputs.
:::

:::::{div}
:class: projector-lecture projector-slide

## The through-line

:::{div}
:class: lecture-through-line

1. **Scientific question**
2. **Named quantities and units**
3. **A readable function call**
4. **A small, stated interface**
5. **Returned result and test**
6. **Reusable analysis**
:::

The syntax matters because it makes the relationship among values visible.
One computation should be understandable at its definition *and* at each call
site.
:::::

:::{div}
:class: projector-lecture projector-slide

## Today’s question

How do we design a function call so its inputs, defaults, and returned value
remain clear when someone else uses it later?

By the end of class, you should be able to:

- distinguish positional, keyword, default, and keyword-only arguments;
- use `*args` and `**kwargs` deliberately rather than as catch-all syntax;
- unpack a tuple or dictionary into a function call without hiding meaning;
- choose whether a helper returns a value, a collection, or an error; and
- use small functions to implement and test a published rule.
:::

:::{div}
:class: projector-lecture projector-slide

## I · Read a call as part of the function’s contract

### Question

When is the order of two correct numbers still too ambiguous for a reader?

### You will leave this section able to

- name the difference between a parameter and an argument;
- use positional and keyword calls for their appropriate roles;
- explain what a default says about a common case; and
- require a consequential option to be named.

**Through-line focus:** named quantities $\rightarrow$ readable call.
:::

:::{div}
:class: projector-lecture projector-slide

## Parameters are names in a definition; arguments are values at a call

```python
def phase_fraction(time_days, period_days, *, epoch_days=0.0):
    """Return phase in [0, 1) for times and period in days."""
    ...
```

| In the definition | In this call | Meaning |
|---|---|---|
| `time_days` | `3.5` | observation time in days |
| `period_days` | `2.0` | repeating period in days |
| `epoch_days` | `epoch_days=0.5` | declared phase reference in days |

The parameters are local names. The arguments are particular values supplied
by one caller. A function body should not need to know where those values came
from.

For this toy example, phase means position within one repeating cycle:

~~~text
(3.5 days - 0.5 day epoch) / 2.0 day period = 1.5 cycles
1.5 % 1.0 = 0.5 phase
~~~

The modulo operation keeps only the fractional cycle. We use this small
calculation to practice function interfaces, not to infer a physical period.
:::

:::{div}
:class: projector-lecture projector-slide

## Positional arguments are good when order is conventional and short

```python
phase_fraction(3.5, 2.0)
```

This call is compact, but only works if the reader can reliably remember that
the first number is a time and the second is a period. Positional arguments are
usually reasonable when:

- there are only one or two required inputs;
- their order is conventional in this domain; and
- swapping them would be obviously wrong or caught by the contract.

`math.sqrt(9.0)` is readable positionally because the operation has one input.
`phase_fraction(3.5, 2.0)` is tolerable in a short local example; a less familiar
call deserves more help.
:::

:::{div}
:class: projector-lecture projector-slide

## Keywords preserve the role of each value

```python
phase = phase_fraction(
    time_days=3.5,
    period_days=2.0,
    epoch_days=0.5,
)
```

The numerical result is the same as the preceding positional call. The
inspection burden is not: the units and roles are visible where the values are
chosen.

Use keywords when values have the same type or unit but different scientific
roles, when a call has more than two inputs, or when an option changes the
interpretation of the result. Keywords do not compensate for vague parameter
names; choose names that say what the value represents.
:::

:::::{div}
:class: projector-lecture projector-slide

## Predict · which calls describe the same phase?

:::{interactive-python}
:id: lecture-03-phase-calls
:controls: {"time_days":{"label":"time (days)","min":0,"max":12,"step":0.5,"value":3.5},"period_days":{"label":"period (days)","min":1,"max":6,"step":0.5,"value":2.0},"epoch_days":{"label":"epoch (days)","min":0,"max":3,"step":0.5,"value":0.5}}

def phase_fraction(time_days, period_days, *, epoch_days=0.0):
    if period_days <= 0:
        raise ValueError("period_days must be positive")
    return ((time_days - epoch_days) / period_days) % 1.0


with_default = phase_fraction(time_days, period_days)
with_keywords = phase_fraction(
    time_days=time_days,
    period_days=period_days,
)
with_epoch = phase_fraction(
    time_days=time_days,
    period_days=period_days,
    epoch_days=epoch_days,
)

print("default epoch:    ", with_default)
print("keyword call:     ", with_keywords)
print("declared epoch:   ", with_epoch)
:::

Before running, identify the two calls that must agree. Then change the epoch:
which call makes the scientific convention easiest to find six weeks from now?

**Worked result:** the first two calls agree because each uses `epoch_days=0.0`.
The third changes only when the named epoch differs from zero.
:::::

:::{div}
:class: projector-lecture projector-slide

## A default is a stated common case, not a missing decision

```python
def phase_fraction(time_days, period_days, *, epoch_days=0.0):
    ...
```

The default says: “unless the caller declares a different reference, phase zero
is at time zero.” That can be a sound convention for a toy model or a local
analysis. It is not suitable if the reference time is unknown or scientifically
essential.

| Good use of a default | Poor use of a default |
|---|---|
| `grid_points=200` for a documented display grid | `period_days=1.0` when the period is unknown |
| `show_grid=True` for a plotting preference | `flux_unit="normalized"` when units are not known |
| `epoch_days=0.0` in a declared toy convention | a placeholder that silently changes interpretation |

**Keep this rule:** a default belongs in the documented contract.
:::

:::{div}
:class: projector-lecture projector-slide

## Keyword-only parameters protect consequential options

```python
def phase_fraction(time_days, period_days, *, epoch_days=0.0):
    """Return phase in [0, 1) for a declared epoch in days."""
    if period_days <= 0:
        raise ValueError("period_days must be positive")
    return ((time_days - epoch_days) / period_days) % 1.0


phase_fraction(3.5, 2.0, epoch_days=0.5)  # clear

try:
    phase_fraction(3.5, 2.0, 0.5)
except TypeError as error:
    print(error)
```

The `*` says that every parameter after it must be supplied by name. This is
useful when an optional value could be mistaken for another number with the
same units. It does **not** mean “all arguments must be keywords”: the required
time and period remain positional-or-keyword arguments.

`phase_fraction(3.5, 2.0, 0.5)` now raises `TypeError` rather than letting the
reference convention disappear into a row of values. This is a deliberate
signature decision, not a new version of the calculation.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · ordinary function parameters

| Signature form | Caller supplies it as… | Use when… |
|---|---|---|
| `f(x)` | a required positional or keyword argument | one essential, unambiguous input |
| `f(x, y)` | two required arguments | order is short and documented |
| `f(x, option=True)` | an optional positional or keyword argument | the default is a stated common case |
| `f(x, *, option=True)` | a keyword argument only | the option changes interpretation or is easy to swap |
| `f(*, unit)` | a required keyword argument | a named choice must never be omitted |

**Keep this rule:** the function signature is part of the documentation. Read
it before you call an unfamiliar function and design it before others call
yours.
:::

:::{div}
:class: projector-lecture projector-slide

## II · Flexible calls need a narrow purpose

### Question

What do `*args` and `**kwargs` collect—and when do they make an interface less
clear instead of more useful?

### You will leave this section able to

- collect a variable number of same-role positional values with `*args`;
- collect named options with `**kwargs` only at a deliberate boundary;
- unpack a tuple with `*` and a mapping with `**`; and
- reject unknown options rather than silently ignoring them.

**Through-line focus:** related inputs $\rightarrow$ a deliberate interface.
:::

:::{div}
:class: projector-lecture projector-slide

## `*args` gathers extra positional arguments into one tuple

```python
def mean_flux(*flux_values):
    """Return the mean of one or more dimensionless flux values."""
    if not flux_values:
        raise ValueError("supply at least one flux value")
    return sum(flux_values) / len(flux_values)


print(mean_flux(1.000, 0.993, 0.989, 0.975))
```

Inside this function, `flux_values` is the tuple
`(1.000, 0.993, 0.989, 0.975)`. `*args` is appropriate because every collected
value has exactly the same role and units.

It is a poor choice for unrelated inputs such as time, flux, period, and an
instrument name. Those need their own parameter names or a documented record.
:::

:::{div}
:class: projector-lecture projector-slide

## Known options should be explicit keyword-only parameters

```python
def describe_series(values, *, label="series", unit=""):
    return f"{label}: {len(values)} values {unit}".strip()


print(describe_series([1.0, 0.99], label="normalized flux", unit=""))
```

The two supported options are known in advance, so the signature names them.
Python now rejects a misspelling automatically. Use this pattern for the
ordinary public interface of a small course function.
:::

:::{div}
:class: projector-lecture projector-slide

## `**kwargs` is useful at a documented forwarding boundary

```python
def plot_series(ax, time_days, brightness, **plot_options):
    allowed = {"label", "color", "marker", "linestyle"}
    unknown = set(plot_options) - allowed
    if unknown:
        raise TypeError(f"unknown plot option: {sorted(unknown)}")
    return ax.plot(time_days, brightness, **plot_options)
```

`plot_options` is a dictionary inside this function. The wrapper forwards a
small, documented set of display choices to `ax.plot`. This is the appropriate
role for `**kwargs`: preserve named options at a boundary rather than hide the
function’s ordinary input contract.

Try reading this call before running it:

```python
plot_series(ax, time_days, brightness, lable="synthetic observations")
```

The misspelled `lable` must raise an error. A wrapper that silently accepts it
would make a later figure harder to trust.

| Interface choice | What it communicates |
|---|---|
| explicit parameters | the supported inputs are known in advance |
| `*args` | any number of values with one shared role |
| `**kwargs` with checking | named options pass through one defined boundary |
| unrestricted `**kwargs` | the supported interface is unclear |

**Keep this rule:** flexibility is useful only when the contract stays
inspectable.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · pack and inspect a variable-length measurement set

:::{interactive-python}
:id: lecture-03-variable-inputs
:controls: {"first_flux":{"label":"first flux","min":0.94,"max":1.02,"step":0.005,"value":1.000},"second_flux":{"label":"second flux","min":0.94,"max":1.02,"step":0.005,"value":0.990},"third_flux":{"label":"third flux","min":0.94,"max":1.02,"step":0.005,"value":0.985}}

def mean_flux(*flux_values):
    if not flux_values:
        raise ValueError("supply at least one flux value")
    return sum(flux_values) / len(flux_values)


measurements = (first_flux, second_flux, third_flux)
print("tuple passed to the function:", measurements)
print("mean normalized flux:", mean_flux(*measurements))
:::

Change one reading. Why is `mean_flux(*measurements)` not the same syntax as
`mean_flux(measurements)`? What type would the latter supply as its one argument?

**Worked result:** `*measurements` unpacks the tuple into three arguments;
without `*`, the function receives one tuple and cannot add it to a float.
:::::

:::{div}
:class: projector-lecture projector-slide

## Unpacking lets a record meet a matching signature

```python
observation = {
    "time_days": 3.5,
    "period_days": 2.0,
    "epoch_days": 0.5,
}

phase = phase_fraction(**observation)
```

`**observation` supplies each key-value pair as a named argument. This is
helpful only when the keys exactly match the function’s documented parameter
names. It does not magically validate a record, convert units, or establish
that the period is physically meaningful.

For a short ordered pair, tuple unpacking is also useful:

```python
time_days, flux = (3.5, 0.987)
```

The left-hand side names the roles; the tuple preserves their order.
:::

:::{div}
:class: projector-lecture projector-slide

## Select the fields a helper promises to use

```python
observation = {
    "target_id": "demo-17",
    "time_days": 3.5,
    "period_days": 2.0,
    "epoch_days": 0.5,
    "filter_name": "r",
}

phase_inputs = {
    name: observation[name]
    for name in ("time_days", "period_days", "epoch_days")
}
phase = phase_fraction(**phase_inputs)
```

Do not send an entire record to `**kwargs` and hope the function finds the
right fields. Select the fields the function promises to use. That selection is
part of the analysis logic and should be easy to inspect.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · packing and unpacking

| Syntax | At a definition | At a call |
|---|---|---|
| `*values` | collects extra positional arguments into a tuple | unpacks an iterable into positional arguments |
| `**options` | collects extra keyword arguments into a dictionary | unpacks a mapping into keyword arguments |
| `a, b = pair` | — | unpacks an ordered pair into named roles |

Before using `*` or `**`, say the sentence in plain language: “these are many
values of the same kind,” or “these dictionary keys match this function’s
documented parameters.” If you cannot say that sentence, choose a clearer
representation.
:::

:::{div}
:class: projector-lecture projector-slide

## III · Return values should support the next question

### Question

How does a small function hand an analysis result back without mutating the
input record or hiding a failure?

### You will leave this section able to

- choose between returning one value, a tuple of values, or a new collection;
- distinguish a returned result from printed display text;
- avoid changing an input collection unexpectedly; and
- test an interface’s ordinary, boundary, and invalid cases.

**Through-line focus:** calculation $\rightarrow$ inspectable result.
:::

:::{div}
:class: projector-lecture projector-slide

## Return a result; print it at the human-facing boundary

```python
def centered_fluxes(flux_values):
    """Return a new list centered on the mean flux."""
    mean_flux_value = sum(flux_values) / len(flux_values)
    return [flux - mean_flux_value for flux in flux_values]


raw_fluxes = [1.000, 0.993, 0.989]
residual_fluxes = centered_fluxes(raw_fluxes)
print("residuals:", residual_fluxes)
```

`centered_fluxes` returns a value that later code can plot, compare, or test.
The `print` belongs outside the calculation because printing is a display
choice, not the mathematical result.
:::

:::{div}
:class: projector-lecture projector-slide

## Returning a new collection preserves the raw record

```python
def centered_fluxes(flux_values):
    mean_flux_value = sum(flux_values) / len(flux_values)
    return [flux - mean_flux_value for flux in flux_values]


raw_fluxes = [1.000, 0.993, 0.989]
residual_fluxes = centered_fluxes(raw_fluxes)

print("raw:", raw_fluxes)
print("residuals:", residual_fluxes)
```

The function uses the input list but does not append, remove, sort, or replace
any of its values. A separate returned list makes it possible to check the raw
measurements later. If a function *does* change an input in place, its name and
documentation should say so clearly.
:::

:::{div}
:class: projector-lecture projector-slide

## Test the interface, not only its arithmetic

```python
import math

assert phase_fraction(0.0, 2.0) == 0.0                  # boundary
assert math.isclose(phase_fraction(3.5, 2.0), 0.75)     # ordinary

try:
    phase_fraction(3.5, 0.0)
except ValueError:
    pass
else:
    raise AssertionError("nonpositive period was accepted")
```

An interface test checks the behavior the caller relies on: a valid output for
a stated input and a clear failure outside the stated domain. It does not prove
that an assumed period describes a real source.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · change a raw series without changing the raw series

:::{interactive-python}
:id: lecture-03-return-values
:controls: {"third_flux":{"label":"third flux","min":0.96,"max":1.02,"step":0.005,"value":0.989}}

def centered_fluxes(flux_values):
    if not flux_values:
        raise ValueError("flux_values must not be empty")
    mean_flux_value = sum(flux_values) / len(flux_values)
    return [flux - mean_flux_value for flux in flux_values]


raw_fluxes = [1.000, 0.993, third_flux]
residual_fluxes = centered_fluxes(raw_fluxes)

print("raw values:     ", raw_fluxes)
print("mean-centered:  ", residual_fluxes)
print("sum residuals:  ", sum(residual_fluxes))
:::

Predict the sign of the third residual before changing the slider. Why should
the residuals sum to approximately zero, rather than exactly zero for every
floating-point input?

**Worked result:** the return value is a new list; `raw_fluxes` remains the
three original readings. Floating-point arithmetic can leave a tiny roundoff.
:::::

:::{div}
:class: projector-lecture projector-slide

## Reference · return values and mutation

| Design choice | Use it when… | Caution |
|---|---|---|
| return one value | one quantity answers the next question | document its units and domain |
| return a tuple | a few results always travel together | unpack immediately into named roles |
| return a dictionary | results have several named roles | make keys part of the contract |
| return a new list | derived values should not alter raw inputs | state the ordering and length |
| mutate an input | in-place change is the explicit purpose | name and document the mutation |
| raise an exception | the request violates the contract | explain which condition failed |

**Keep this rule:** a caller should be able to tell whether a function returns,
mutates, or refuses a request without reading every line of its body.
:::

:::{div}
:class: projector-lecture projector-slide

## IV · A small policy program should keep its jobs separate

### Question

How can a 30-minute grade-calculator activity exercise function interfaces
without becoming an official grade record?

### You will leave this section able to

- decompose a calculation and a classification policy into separate helpers;
- select direct boundary tests for the policy; and
- distinguish a practice result from an authoritative course grade.

**Through-line focus:** published rule $\rightarrow$ small, testable program.
:::

:::{div}
:class: projector-lecture projector-slide

## The grade-calculator lab is a practice policy, not a grade system

For the [COMP 521 Course-Grade Calculator Lab](../07-practice-labs/grade-calculator-design.md),
you will work only with the supplied fictional record. Canvas remains the
authoritative course record.

Keep these jobs separate:

```text
letter grade  →  grade points
component grades  →  component mean
component means + weights  →  unrounded course average
unrounded average  →  final course letter
```

Each arrow is a small function with a different contract. This makes a wrong
letter boundary easier to locate than it would be in one long cell.
:::

:::{div}
:class: projector-lecture projector-slide

## A direct boundary test is better than a manufactured scenario

```python
assert final_course_letter(3.80) == "A"
assert final_course_letter(3.79) == "A-"
```

The point of these tests is the branch boundary, not the construction of a
fictional record that happens to average to 3.80. Test the policy at its own
interface.

Use the full 30 minutes for the activity:

1. read the contract and supplied test table;
2. implement one small helper at a time;
3. run the direct policy tests plus one invalid-input test;
4. restart and run the notebook top to bottom; and
5. write one sentence explaining a failed test or a checked boundary.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · readings and documentation

| Use this for… | Read |
|---|---|
| lists, dictionaries, tuples, and mutation | [Chapter 4: Data Structures](04-python-data-structures.md) |
| definitions, arguments, scope, and modules | [Chapter 5: Functions & Modules](05-python-functions-modules.md) |
| Python parameter rules and call syntax | [Python: defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) |
| Python function calls and unpacking | [Python: more on defining functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions) |
| the practice activity | [COMP 521 Course-Grade Calculator Lab](../07-practice-labs/grade-calculator-design.md) |

Read documentation at the point of use. A signature tells you how to call a
function; its documentation tells you what that call means.
:::

:::{div}
:class: projector-lecture projector-slide

## Exit check

For the function below, label each part of the call and explain one design
choice.

```python
phase = phase_fraction(5.0, 2.0, epoch_days=1.0)
```

1. Which values are positional arguments? Which is keyword-only?
2. Repair this call so it is valid: `phase_fraction(5.0, 2.0, 1.0)`.
3. A record has keys `time_days`, `period_days`, and `epoch_days`. Which
   operator supplies it to `phase_fraction` by name?
4. In one sentence: when would you choose `*args` instead of explicit
   parameters, and when would you use `**kwargs`?

Bring one question about arrays, shapes, or plotting to Lecture 4.
:::

:::{div}
:class: projector-lecture projector-slide

## Before Lecture 4

Read [Chapter 7: NumPy Fundamentals](../04-scientific-computing/07-numpy-fundamentals.md)
through **7.4 Indexing and Boolean Masks**, and [Chapter 8: Matplotlib
Fundamentals](../04-scientific-computing/08-matplotlib-fundamentals.md) through
the first labeled figure.

Be ready to explain:

- why a NumPy array is not merely a faster list;
- what one Boolean value in a mask corresponds to; and
- what an axis label must tell a reader.

Lecture 4 uses a small, synthetic stellar-variability example—not Project 1—to
practice the array and figure habits that later work will need.
:::
