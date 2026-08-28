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

:::{div}
:class: lecture-through-line

1. **Scientific question**
2. **Stated rule and assumptions**
3. **Comparisons and branches**
4. **Related observations**
5. **Reusable function with a contract**
6. **Many values with an array**
7. **Inspectable result and a test**
:::

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
- identify an accumulator and its expected value;
- choose when a loop should skip, stop, or build a derived list.

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

**Rule:** select a value only when `flux < 0.99`.

Before coding, decide:

- Is the comparison strict or inclusive?
- What happens at exactly `0.990`?

**Scope:** a real transit search also needs uncertainties, cadence, and
systematics. This exercise practices only the computational decision.
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

## Why programs need control flow

A calculation follows one fixed path. A procedure often cannot: what it does
next depends on the observation in front of it.

- A **conditional** is a fork in a procedure: ask a yes/no question, then
  choose the matching action.
- A **loop** repeats one stated procedure for many observations or until a
  stopping condition is met.

**Why it matters:** without control flow, students and researchers fill in
decision steps by hand. That makes a policy hard to inspect, repeat, and test.
:::

:::{div}
:class: projector-lecture projector-slide

## A Boolean expression chooses a branch

A conditional first evaluates a question. Its `True` or `False` result selects
one branch; the indented statements specify what happens on that path.

```python
flux = 0.989
threshold = 0.99

if flux < threshold:
    print("candidate low-flux measurement")
else:
    print("not below the stated threshold")
```

`flux < threshold` is either `True` or `False`; indentation assigns statements
to its branch. At equality, this rule reaches `else`.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · move the boundary, then explain

Use the control to separate the stated English rule from its Python spelling:
the only difference between the two comparisons is what happens at the boundary.

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

**Worked result:** at `0.990`, `<` is `False`; `<=` is `True`.
:::::

:::{div}
:class: projector-lecture projector-slide

## More than two outcomes · `elif`

This observation-triage example categorizes one measurement by threshold; it
is not a complete detection procedure. For mutually exclusive outcomes, `elif`
extends the decision tree: Python chooses one branch and skips the rest.

```python
flux = 0.984

if flux < 0.970:
    status = "strong low-flux candidate"
elif flux < 0.990:
    status = "candidate low-flux observation"
else:
    status = "not below the threshold"
```

**Read it:** `0.984` reaches the `0.990` branch. The stronger `0.970` test must
come first, or Python will never reach it.
:::

:::{div}
:class: projector-lecture projector-slide

## Combine conditions deliberately

Real decisions often depend on more than one fact. Boolean operators make the
combination rule visible: use `and` when both requirements must hold, `or` when
either is sufficient, and `not` when reversing a Boolean statement is the
actual rule.

```python
import math

flux = 0.989
uncertainty = 0.002

usable_measurement = math.isfinite(flux) and uncertainty > 0.0
candidate = usable_measurement and flux < 0.99
needs_review = candidate or uncertainty > 0.01
```

**Example `or` policy:** review a measurement if it is a candidate **or** its
uncertainty is unusually large.

Parenthesize mixed `and` / `or` conditions unless the grouping is obvious.
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

**Expected result:** no error; the body is skipped.

For an empty list, `flux_measurements` is false, so Python never tries
`flux_measurements[0]`. Reversing the terms would raise an `IndexError`.

**Limit:** this prevents a programming error; it does not establish that the
data set is scientifically adequate.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · conditionals and Boolean logic

| Need to… | Use | Read it as… |
|---|---|---|
| choose one of two paths | `if` / `else` | if this question is true, do this; otherwise do that |
| choose one ordered outcome | `if` / `elif` / `else` | first true branch wins |
| require every condition | `and` | all must be true |
| allow either condition | `or` | at least one must be true |
| protect a risky expression | safe check `and` risky expression | Python stops once the answer is known |

**Keep this rule:** write the English decision first; then test the boundary
where the answer changes.
:::

:::{div}
:class: projector-lecture projector-slide

## Loops apply one procedure repeatedly

Observations rarely arrive one at a time. A loop prevents copy-pasting the
same decision for every measurement, which would make inconsistent edits easy
to introduce and hard to audit.

| Choose | When it fits | What must be explicit |
|---|---|---|
| `for` | a collection already supplies the items | the procedure for each item |
| `while` | the number of repeats is not known in advance | progress and a stopping guard |

The condition can appear inside either kind of loop; a loop does not decide
what the scientific rule should be.
:::

:::{div}
:class: projector-lecture projector-slide

## `while` repeats until a stated condition changes

A `while` loop is for work whose number of repeats is not known in advance. It
must state progress and a bound.

```python
residual = 0.08
tolerance = 0.01
step = 0
max_steps = 5

while residual > tolerance and step < max_steps:
    residual = residual / 2
    step = step + 1

print(f"stopped at step {step}: residual = {residual:.3f}")
```

This is a toy update, not a physical fitting method.
:::

:::{div}
:class: projector-lecture projector-slide

## Trace a `while` loop; do not guess

| Step | Residual before update | Continue? | Residual after update |
|---:|---:|---:|---:|
| `0` | `0.080` | `True` | `0.040` |
| `1` | `0.040` | `True` | `0.020` |
| `2` | `0.020` | `True` | `0.010` |
| `3` | `0.010` | `False` | stop |

**Expected result:** `stopped at step 3: residual = 0.010`.
:::

:::{div}
:class: projector-lecture projector-slide

## `for` loops: one procedure for every observation

A `for` loop is the right default when a collection supplies the work items.
Python binds the loop name to one item at a time.

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

`candidate_count` is an **accumulator**: it records selected values so far.
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

**Invariant:** after each step, `candidate_count` equals the number of selected
values seen so far. If the trace breaks that rule, inspect the update and
indentation.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · loop patterns

| Pattern | Use it when | Must change or be stated |
|---|---|---|
| `for item in items:` | a collection supplies each work item | the loop variable and indented body |
| `while condition:` | stopping depends on a changing state | progress plus a guard such as `max_steps` |
| accumulator | you need one result across the loop | its initial value and update rule |

**Keep this rule:** trace the first few iterations. A loop is correct only if
its state means what you think it means after every step.
:::

:::{div}
:class: projector-lecture projector-slide

## Stop, skip, or finish a loop deliberately

Most loops should process every item. State an exception when they should not:

- `continue` skips this item and moves to the next;
- `break` stops the loop immediately;
- `for ... else` runs its `else` block only when no `break` occurred.

```python
import math

for flux in [1.000, float("nan"), 0.989]:
    if not math.isfinite(flux):
        continue
    if flux < 0.980:
        break
else:
    print("checked every usable measurement")
```

**Keep this rule:** do not hide a stopping or skipping policy in a loop body.
:::

:::{div}
:class: projector-lecture projector-slide

## Nested loops: one procedure across two dimensions

One loop visits one sequence. A nested loop visits every stated combination:

```python
nights = [1, 2]
filters = ["g", "r"]

for night in nights:
    for filter_name in filters:
        print(night, filter_name)
```

The inner body runs four times: `(1, "g")`, `(1, "r")`, `(2, "g")`, and
`(2, "r")`. Use nested loops when the scientific question is genuinely about
combinations; do not add one merely because data are stored in a table.
:::

:::{div}
:class: projector-lecture projector-slide

## List comprehensions: compact a simple loop

A comprehension builds a derived list when one transformation or filter is
readable in one line:

```python
candidate_fluxes = [
    flux for flux in flux_measurements
    if flux < threshold
]
```

It is equivalent to the earlier loop that appends selected values. Prefer an
ordinary `for` loop when tracing, multiple decisions, or side effects make the
comprehension harder to read.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · refinements to loop control

| Construct | Meaning | Use with care when… |
|---|---|---|
| `continue` | skip the rest of this iteration | the skipped data must be recorded or explained |
| `break` | stop the loop now | stopping early changes the result or coverage |
| `for ... else` | run `else` only if no `break` occurred | a found/not-found outcome is part of the rule |
| nested loops | visit every explicit combination | the number of combinations can grow quickly |
| list comprehension | build one simple derived list | the line would hide the procedure |
:::

:::{div}
:class: projector-lecture projector-slide

## II · Store related observations deliberately

### Question

What representation makes the relationship among values visible?

### You will leave this section able to

- use a list for an ordered sequence;
- use a dictionary for named, related fields;
- choose a tuple or set when that relationship is more honest;
- recognize when mutation and copying are useful and when they are risky.

**Through-line focus:** observations $\rightarrow$ inspectable representation.
:::

:::{div}
:class: projector-lecture projector-slide

## A list keeps an ordered sequence

A list represents several values that play the same role, in a meaningful
order. That lets one procedure—such as a `for` loop—operate on every value
without losing the original sequence.

```python
flux_measurements = [1.000, 0.993, 0.989, 0.975]

first_flux = flux_measurements[0]
number_of_measurements = len(flux_measurements)
```

- Use a list when order matters and values play the same role.
- `flux_measurements[0]` is the first value; `len(...)` counts values.
- A list is not automatically a time series: record the time coordinate too.
:::

:::{div}
:class: projector-lecture projector-slide

## A dictionary names related fields

One observation can have values with different roles: a time, a flux, and a
filter label should not be confused merely because they travel together. A
dictionary makes those roles explicit before we access a value by name.

```python
observation = {
    "time_days": 4.5,
    "normalized_flux": 0.989,
    "filter_name": "r",
}

print(observation["normalized_flux"])
```

- Use a dictionary when values have different, named roles.
- Keys make the structure legible.
- Keys do not establish calibration or physical comparability.
:::

:::{div}
:class: projector-lecture projector-slide

## Tuples and sets express different relationships

Use a tuple for a small, ordered value that should not change; use a set for
unique members when order and repetition do not matter.

```python
survey_window_days = (0.0, 4.0)        # ordered, immutable pair
observed_nights = {1, 2, 2, 3}         # unique members only

print(survey_window_days[0])            # 0.0
print(observed_nights)                  # {1, 2, 3}
print(2 in observed_nights)             # True
```

Tuples protect a fixed small record; sets answer membership questions and
remove duplicates. Neither preserves the meaning of a measurement by itself.
:::

:::{div}
:class: projector-lecture projector-slide

## Mutability is a bookkeeping choice

Before changing a collection, decide whether the change belongs to the raw
inputs or a derived working copy. This matters because two names can refer to
the same mutable list.

```python
raw_fluxes = [1.000, 0.993, 0.989]
working_fluxes = raw_fluxes
working_fluxes.append(0.975)

print(raw_fluxes)  # also changed
```

**Result:** both names refer to the same list, so `raw_fluxes` changes too.

```python
independent_fluxes = raw_fluxes.copy()
```

Use `.copy()` when you need an independent one-dimensional working list.
:::

:::{div}
:class: projector-lecture projector-slide

## Copying nested data needs an explicit decision

`.copy()` creates a new outer list, but nested lists still refer to the same
inner objects. Ask whether you need a shallow or independent deep copy.

```python
import copy

raw_by_night = [[1.000, 0.993], [0.989, 0.975]]
shallow = raw_by_night.copy()
shallow[0].append(0.991)                # also changes raw_by_night[0]

independent = copy.deepcopy(raw_by_night)
```

**Keep this rule:** choose copying depth from the data structure, not from the
name of the method. Prefer a clear representation over indiscriminate copying.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · collections and mutation

| Need to represent… | Use | Key operation | Caution |
|---|---|---|---|
| ordered values with the same role | a list | `values[index]`, `len(values)` | indexing starts at `0` |
| named fields with different roles | a dictionary | `record["field_name"]` | a missing key is an error |
| a fixed, ordered small record | a tuple | `pair[0]` | tuples cannot be changed in place |
| unique membership | a set | `item in members` | sets do not preserve a useful order |
| a new derived sequence | a second list | `selected.append(value)` | keep raw inputs unchanged |
| an independent nested structure | `copy.deepcopy(raw)` | copies inner objects too | use only when independence is required |

**Keep this rule:** names are not copies. Decide which values are raw and
which are derived before changing a collection.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · select values without losing the original list

This loop creates a second list for selected values. The original observations
remain available for inspection, comparison, or a different threshold later.

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

**Worked result:** the original list is unchanged; `candidate_fluxes` is a
separate list containing `0.989` and `0.975`.
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
- use keyword and default arguments when they make intent clearer;
- explain local scope, mutable defaults, and a module boundary;
- test a function with ordinary, boundary, and invalid inputs.

**Through-line focus:** calculation $\rightarrow$ reusable, testable contract.
:::

:::{div}
:class: projector-lecture projector-slide

## A function gives a calculation a name and a boundary

When a calculation will be reused, a function makes its inputs, output, and
invalid cases visible in one place. That lets us change or test the rule
without hunting through repeated code.

For a full-overlap, uniform-brightness transit geometry, the idealized
fractional flux loss is

$$
\delta = \left(\frac{R_p}{R_\star}\right)^2.
$$

**Call contract:** `transit_depth(Rp_cm, Rstar_cm)` returns dimensionless depth
for `0 < Rp <= Rstar` in full-overlap, uniform-brightness geometry.

**Limit:** this omits limb darkening and partial/grazing overlap.
:::

:::{div}
:class: projector-lecture projector-slide

## Anatomy of a function

```python
def transit_depth(radius_planet_cm, radius_star_cm):  # name + parameters
    """Return full-overlap depth for two radii in cm."""  # contract
    if not 0 < radius_planet_cm <= radius_star_cm:     # validation
        raise ValueError("requires 0 < Rp <= Rstar")
    return (radius_planet_cm / radius_star_cm) ** 2    # returned result
```

- `def` creates a reusable function; the **name** says what it calculates.
- **Parameters** name the inputs a caller must supply.
- The indented **body** validates and calculates.
- `return` gives the result back to the caller; `raise` refuses an invalid call.

**Why it matters:** a function is a contract, not just a convenient code box.
:::

:::{div}
:class: projector-lecture projector-slide

## Read a function call as a contract

A call supplies particular inputs to a named calculation. Ask what each input
represents and what result returns.

```python
depth = transit_depth(
    radius_planet_cm=7.1492e9,
    radius_star_cm=6.957e10,
)
```

**Why keywords?** The inputs share a unit but have different physical roles.
:::

:::{div}
:class: projector-lecture projector-slide

## `return` makes a result reusable; `print` only displays it

Printing is useful for inspection. Returning gives the caller a value it can
store, compare, plot, or pass into another calculation.

```python
def show_depth(radius_ratio):
    print(radius_ratio ** 2)        # displays a value

def depth_from_ratio(radius_ratio):
    return radius_ratio ** 2        # supplies a value

depth = depth_from_ratio(0.1)
print(100 * depth, "%")
```

**Keep this rule:** calculate with `return`; display results with `print` at
the boundary where a person needs to inspect them.
:::

:::{div}
:class: projector-lecture projector-slide

## Defaults and scope keep function behavior predictable

A default makes a common call short. A parameter is local to the function, so
using the same name does not rewrite a name outside it.

```python
threshold = 0.01

def label_depth(depth, threshold=0.01):
    if depth >= threshold:
        return "review"
    return "below threshold"

print(label_depth(0.012))          # uses 0.01
print(label_depth(0.012, 0.02))    # uses 0.02 for this call
print(threshold)                   # still 0.01
```

Pass needed information as arguments. Do not rely on a hidden global value
when the function's result should be reproducible elsewhere.
:::

:::{div}
:class: projector-lecture projector-slide

## Never use a mutable object as a default argument

A default list or dictionary is created once, then shared across calls. Use
`None` to create a fresh collection when the function runs.

```python
def add_flag(flag, flags=None):
    if flags is None:
        flags = []
    flags.append(flag)
    return flags

print(add_flag("cloud"))
print(add_flag("instrument"))      # a new list, not a shared one
```

**Keep this rule:** a mutable default is a shared state bug waiting to happen.
:::

:::{div}
:class: projector-lecture projector-slide

## Separate calculation from policy

The same numerical result can support different policies. Keeping the policy
in its own function means that changing a decision rule does not alter the
calculation itself.

```python
def classify_depth(depth, review_depth=0.01):
    """Label a nonnegative model depth using a stated review threshold."""
    if depth < 0.0 or review_depth <= 0.0:
        raise ValueError("depths must be nonnegative and review_depth positive")
    if depth >= review_depth:
        return "review this modeled depth"
    return "below this review threshold"
```

`transit_depth(...)` supplies the numerical `depth`; `classify_depth(depth)`
applies a separate, inspectable policy.

**Design rule:** keep the numerical calculation and observation-classification
policy in separate functions so a change to one does not silently rewrite the
other.
:::

:::{div}
:class: projector-lecture projector-slide

## Modules are reusable boundaries

A module is a Python file whose names another file can import. Modules keep a
course project from becoming one long notebook or script.

```python
# transit_tools.py
def transit_depth(radius_planet_cm, radius_star_cm):
    return (radius_planet_cm / radius_star_cm) ** 2

# analysis.py or a notebook
from transit_tools import transit_depth

depth = transit_depth(1.0, 10.0)
```

`import math` and `import numpy as np` use the same idea with modules supplied
by Python or a package. A module boundary is useful only when its public names
and assumptions are clear.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · a reusable transit-depth calculation

The slider supplies one input to the function; the function applies the same
stated geometric rule each time. This is reuse, not a different calculation.

:::{interactive-python}
:id: lecture-02-transit-depth
:controls: {"radius_ratio":{"label":"Rp / Rstar","min":0.01,"max":0.2,"step":0.01,"value":0.1}}

def transit_depth_from_ratio(radius_ratio):
    # Full-overlap, uniform-brightness geometry requires 0 < Rp/Rstar <= 1.
    if not 0.0 < radius_ratio <= 1.0:
        raise ValueError("radius_ratio must be in (0, 1]")
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

## From a function contract to evidence

A definition states what a function promises. Tests turn that promise into
executable checks, so a later edit cannot silently change the agreed behavior.

For this function, test three kinds of claim:

1. an **ordinary** input gives the expected numerical result;
2. a **boundary** input behaves at the edge of the stated domain;
3. an **invalid** input raises the documented error.

Run the definition next; the following two slides test exactly that definition.
:::

:::{div}
:class: projector-lecture projector-slide

## Run the definition, then run its tests

Run this definition first. The next two slides are a complete test sequence
for exactly this function.

```python
def transit_depth(radius_planet_cm, radius_star_cm):
    if radius_planet_cm <= 0 or radius_star_cm <= 0:
        raise ValueError("radii must be positive")
    if radius_planet_cm > radius_star_cm:
        raise ValueError("full-overlap geometry requires Rp <= Rstar")
    return (radius_planet_cm / radius_star_cm) ** 2
```
:::

:::{div}
:class: projector-lecture projector-slide

## Test ordinary and boundary inputs

An ordinary test confirms the expected calculation; a boundary test confirms
the edge of the stated domain.

```python
import math

assert math.isclose(
    transit_depth(1.0, 10.0), 0.01,
    rel_tol=1e-12, abs_tol=0.0,
)                                               # ordinary case
assert transit_depth(1.0, 1.0) == 1.0         # toy-geometry boundary
```

**Why `isclose`?** Binary floating point stores this ordinary result as
`0.010000000000000002`, not exactly `0.01`.

`rel_tol=1e-12` is a **strict software-test tolerance**, not a measurement
uncertainty.
:::

:::{div}
:class: projector-lecture projector-slide

## Test invalid inputs fail loudly

An invalid-input test must fail if the function accepts an invalid request.
Printing only after an error is not enough.

```python
for radius_planet_cm, radius_star_cm in [(-1.0, 10.0), (11.0, 10.0)]:
    try:
        transit_depth(radius_planet_cm, radius_star_cm)
    except ValueError:
        continue
    else:
        raise AssertionError("transit_depth accepted invalid geometry")
```

**Keep this rule:** ordinary, boundary, and invalid tests establish a function
contract—not the adequacy of the underlying scientific model.
:::

:::{div}
:class: projector-lecture projector-slide

## Reference · functions and tests

| Part | Purpose |
|---|---|
| `def name(parameters):` | define a reusable calculation and its inputs |
| parameter | local name for an input inside a function |
| argument | value supplied at a call site |
| `return value` | send a reusable result back to the caller |
| `print(value)` | display a value; it does not return it |
| `parameter=default` | supply a default when the caller omits an argument |
| local scope | names inside a function do not rewrite outer names |
| `None` for a mutable default | create a fresh list or dictionary per call |
| `raise ValueError(...)` | reject an input outside the contract |
| ordinary / boundary / invalid test | verify normal behavior, the edge, and rejection |
| `import module` | use names from another Python file or package |

**Keep this rule:** a function, its contract, and its tests must agree on the
same inputs, units, outputs, and invalid cases.
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

A Python list preserves a sequence of objects. A NumPy array applies numerical
arithmetic to every element.

```python
import numpy as np

flux_list = [1.000, 0.993, 0.989, 0.975]
flux_array = np.array(flux_list)

print(flux_list * 2)
print(flux_array * 2)
```

`flux_list * 2` repeats the list; `flux_array * 2` doubles each element. NumPy
does not supply units, calibration, uncertainty, or interpretation.
:::

:::::{div}
:class: projector-lecture projector-slide

## Run · make one simple numerical grid

This is the first array example: create several times, then apply one
calculation to every time at once. The purpose is to recognize the shape of an
array computation before Week 2 develops the broader NumPy toolkit.

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

- `np.linspace(0.0, 4.0, 5)` makes five evenly spaced values, including both
  endpoints.
- `np.ones_like(time_days)` creates ones with the same shape as `time_days`.
- The flux is deliberately constant: this demonstrates an array operation,
  not a complete transit model.

**Check yourself:** Why does `model_flux` contain five values?
:::::

:::{div}
:class: projector-lecture projector-slide

## Reference · NumPy essentials

| Expression | What it does |
|---|---|
| `np.array(values)` | makes a NumPy array from a sequence |
| `array * 2` | applies multiplication to every element |
| `np.linspace(start, stop, count)` | makes `count` evenly spaced values, including endpoints |
| `np.ones_like(array)` | makes ones with the same shape as `array` |
| `array.size` | counts all elements in the array |

**Keep this rule:** arrays repeat numerical operations over many values; they
do not provide units, calibration, or an interpretation.
:::

:::{div}
:class: projector-lecture projector-slide

## NumPy is an introduction today, not the whole method

We are **not yet learning**:

- array shapes beyond one dimension;
- indexing, slicing, masks, and broadcasting;
- array views versus copies;
- vectorized transit geometry, plotting, or performance claims.

**Carry forward:** an array applies one numerical operation to many values;
you must still know what every value represents.
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
