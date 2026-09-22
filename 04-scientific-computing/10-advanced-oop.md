---
title: "Chapter 10: Designing Small Scientific Types"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
---

## A measurement with a contract

### Introductory example

This type records one measurement with a finite, non-negative flux in a stated
unit. It does not model a detector, uncertainty distribution, calibration
pipeline, or unit conversion; each would require additional assumptions rather
than extra fields by default.

```python
from dataclasses import dataclass
from numbers import Real
import math


@dataclass(frozen=True)
class FluxMeasurement:
    value: float
    unit: str = "W m^-2"

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, Real):
            raise TypeError("flux must be one real scalar")
        if not math.isfinite(self.value) or self.value < 0.0:
            raise ValueError("flux must be finite and non-negative")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("unit must be stated")


def fractional_change(before: FluxMeasurement, after: FluxMeasurement) -> float:
    if not isinstance(before, FluxMeasurement) or not isinstance(after, FluxMeasurement):
        raise TypeError("fractional change requires FluxMeasurement instances")
    if before.unit != after.unit:
        raise ValueError("convert to a common unit before comparison")
    if before.value == 0.0:
        raise ValueError("fractional change is undefined from zero baseline")
    return (after.value - before.value) / before.value
```

### Preview activity

Predict what happens when you construct `FluxMeasurement(-0.01)`,
`FluxMeasurement(float("nan"))`, and two otherwise comparable measurements
with unequal units. Then run the constructions. For each failure, name the
assumption it exposes and decide whether conversion belongs in this model's
scope.

### Transfer prompt

Define a small type from your field with one invariant: a positive scale,
ordered bounds, a normalized fraction, or a stated unit. Write one valid case,
one invalid case, and one sentence explaining why a dictionary or function
would be preferable if that invariant did not exist.

### Chapter connection

Small types make meaningful state and constraints inspectable. The next
textbook part, [Part III: Tabular Data and Reproducible Workflows](part-3-data-workflows.md),
is in development; it moves from one validated entity to collections of
measurements and their provenance.

## Learning objectives

By the end of this chapter, you will be able to:

- decide when a scientific record needs a type with an explicit contract;
- use a dataclass to make state, units, and invariants legible;
- distinguish validation at a boundary from behavior a type can responsibly
  provide;
- use composition instead of an unnecessary inheritance hierarchy; and
- test valid cases, invalid cases, and a stated numerical behavior.

## Prerequisites

Before starting, you should be able to define a function and read a traceback
(Chapters 1–5), create a basic class (Chapter 6), work with NumPy arrays
(Chapter 7), and read a small `pytest` test (Chapter 9).

:::{note} Core route through this chapter

For the complete chapter, read Sections 10.1–10.4 in order. For Week 5, follow the narrower route on This Week: the opening example, 10.1, and 10.4. Dataclass syntax appears in these examples; using a dataclass in Project 3 is optional. An ordinary class with a tested contract is sufficient. The **Deep Dive** preserves advanced
research-software ideas for later lookup; it is not a second required route.
:::

## Why this chapter matters

Scientific programs often begin with dictionaries, tuples, and parallel arrays.
Those are useful representations when the program only transports values. A
small type earns its existence when it makes an invariant, a unit contract, or
a meaningful operation visible at the point where the value enters the program.

The goal is not to make a model look sophisticated. It is to make a limited
claim inspectable: *this object represents one finite, non-negative flux in one
stated unit.* The type cannot establish calibration, physical adequacy, or
interchangeability of arbitrary units. Those are separate claims with separate
evidence.

(week5-type-contract)=
## 10.1 From a record to a contract

A dictionary is often the right starting point:

```python
raw_measurement = {"value": 1.8e-12, "unit": "W m^-2"}

# A later function must remember every assumption itself.
def is_bright_enough(record, threshold):
    return record["value"] >= threshold
```

This is concise, but the dictionary accepts a missing unit, a misspelled key,
or `float("nan")` unless every consumer repeats the checks. A small type moves
the shared boundary contract to one place.

:::{important} Why This Matters: a type turns an assumption into a visible boundary

When a value crosses a file reader, instrument adapter, or analysis function,
the program needs a place to say what it accepts. A small type makes that claim
visible to the next reader and gives an invalid value an early, interpretable
failure. It does not replace inspection of the instrument, calibration, or
scientific model that produced the value.
:::

:::{important} Design decision: earn a type with a recurring invariant

Use a dictionary, tuple, or function when it is only carrying values. Introduce
a type when several parts of the program must agree on a constraint or on the
meaning of an operation. Do not create a class merely because a value has a
name.
:::

The `FluxMeasurement` opening makes three choices that are worth noticing:

1. `frozen=True` says the measurement value cannot be reassigned after
   construction.
2. `__post_init__` checks the invariant after the generated initializer has
   stored the fields.
3. `fractional_change` refuses a comparison whose unit or zero-baseline
   contract has not been established.

:::{tip} Predict before running

Before executing the code below, predict which line fails first and why. Then
compare the exception with your prediction.

```python
bright = FluxMeasurement(2.0e-12, "W m^-2")
faint = FluxMeasurement(1.0e-12, "W m^-2")

print(fractional_change(bright, faint))  # -0.5

# FluxMeasurement(float("nan"))
# fractional_change(bright, FluxMeasurement(1.0, "erg s^-1 cm^-2"))
```

The first calculation has an agreed quantity contract. The commented examples
are rejected for different reasons: a non-finite value violates the measurement
invariant, whereas unequal strings tell us that conversion is outside this
small function's scope.
:::

:::{tip} Modeling boundary: stated units are not unit conversion

The `unit` field records the representation chosen by the caller. It neither
parses every possible unit spelling nor converts a spectral flux density to a
band-integrated flux. Use a domain-appropriate quantity library or an explicit,
tested conversion layer when that broader behavior is required.
:::

## 10.2 Dataclasses make state legible

A dataclass writes routine methods for a class whose primary purpose is storing
state: an initializer, readable representation, and field-wise equality. It
does not infer a scientific invariant from type annotations; you still write
the checks that the model needs.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    """One named observation containing one validated measurement."""

    target: str
    measurement: FluxMeasurement
    instrument_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.target, str) or not self.target.strip():
            raise ValueError("target must be stated")
        if not isinstance(self.measurement, FluxMeasurement):
            raise TypeError("measurement must be a validated FluxMeasurement")
        if not isinstance(self.instrument_id, str) or not self.instrument_id.strip():
            raise ValueError("instrument identifier must be stated")


observation = Observation(
    target="comparison star",
    measurement=FluxMeasurement(2.0e-12, "W m^-2"),
    instrument_id="camera-17",
)
print(observation)
```

`Observation` **has a** `FluxMeasurement`; that is composition. It is more
honest than inventing an inheritance relationship such as “an observation is a
kind of flux.” It also lets each type defend its own boundary: the observation
knows that target and instrument identifiers are stated, while the measurement
knows about value and unit.

```{figure} ../assets/textbook-figures/ch10-composition-boundaries.svg
:name: ch10-composition-boundaries
:alt: An Observation object has a FluxMeasurement. Observation owns the target and instrument identifier; FluxMeasurement owns a finite value and stated unit. The diagram says this is composition, not a claim that an Observation is a FluxMeasurement.
:width: 100%

Composition gives each type responsibility for the part of the contract it can actually enforce.
```

What to notice: this local object design makes a boundary inspectable. It does
not supply detector calibration, an uncertainty model, or a system-level
provenance record.

::::{note} Check Your Understanding

Suppose these two constructions have the same values:

```python
a = FluxMeasurement(1.0, "W m^-2")
b = FluxMeasurement(1.0, "W m^-2")
```

What does `a == b` mean here? Is it a suitable test for agreement between two
independent experimental estimates?

:::{note} Answer
:class: dropdown

The dataclass-generated equality compares its fields exactly, so `a == b` is
`True`. That is useful for value objects and controlled test fixtures. It is
not a scientific agreement criterion for independently measured values: those
need uncertainty, resolution, and a stated comparison rule. In a numerical
test, use a tolerance justified by the calculation or measurement context—for
example, `pytest.approx` when its tolerance is warranted.
:::
::::

## 10.3 Behavior belongs with the contract it needs

Methods should express behavior that is meaningful for every valid instance of
the type. `fractional_change` belongs near `FluxMeasurement` because both its
unit agreement and zero-baseline limit are part of the calculation's contract.
It is deliberately a standalone function: the calculation compares two
measurements, so neither instance owns the other. A detector calibration method
does not belong here: calibration needs information that this type deliberately
does not carry.

```python
reference = FluxMeasurement(4.0e-12, "W m^-2")
later = FluxMeasurement(5.0e-12, "W m^-2")

change = fractional_change(reference, later)
print(f"fractional change = {change:.0%}")  # 25%
```

:::{tip} Computational Thinking: keep behavior close to the evidence it needs

A method is not a place to hide assumptions. If a calculation needs exposure
time, collecting area, wavelength response, or calibration provenance, make
those inputs explicit in a function or a separate domain model. A smaller,
honest type is more useful than an object whose methods appear universal.
:::

### Readable representations are diagnostic evidence

The generated `repr` makes the fields visible in a notebook, log, traceback,
or test failure. That is useful evidence, but it is not a complete provenance
record. A production data product may also need timestamps, configuration,
versions, uncertainties, and links to its raw inputs.

(week5-type-tests)=
## 10.4 Test the type's contract

Chapter 9 established that a passing test demonstrates stated behavior under
stated conditions. The following tests make the contract of this small type
executable; they do not validate a calibration or establish the physical
meaning of a flux measurement.

```python
import pytest


def test_flux_measurement_accepts_a_finite_nonnegative_value():
    measurement = FluxMeasurement(0.0, "W m^-2")
    assert measurement.value == 0.0


@pytest.mark.parametrize("bad_value", [-0.01, float("nan"), float("inf")])
def test_flux_measurement_rejects_invalid_values(bad_value):
    with pytest.raises(ValueError):
        FluxMeasurement(bad_value, "W m^-2")


def test_fractional_change_requires_a_common_unit_and_nonzero_baseline():
    before = FluxMeasurement(2.0, "W m^-2")
    after = FluxMeasurement(3.0, "W m^-2")
    assert fractional_change(before, after) == pytest.approx(0.5)

    with pytest.raises(ValueError, match="common unit"):
        fractional_change(before, FluxMeasurement(3.0, "erg s^-1 cm^-2"))
    with pytest.raises(ValueError, match="zero baseline"):
        fractional_change(FluxMeasurement(0.0), after)
```

The tests use arrange–act–assert: construct a stated case, call the behavior,
and compare the result or exception with the contract. The parameterized test
makes three invalid boundary values visible without copying the test body.

::::{note} Debug This!

This attempted constructor checks only one failure mode:

```python
@dataclass(frozen=True)
class UnsafeFluxMeasurement:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("flux must be non-negative")
```

Why can it still admit a value that should not become a measurement? What test
would demonstrate the problem?

:::{note} Answer
:class: dropdown

`float("nan") < 0` is `False`, so the check admits a non-finite value. Add a
finite-value check and a test such as
`with pytest.raises(ValueError): UnsafeFluxMeasurement(float("nan"))` after
repairing the class. This is a boundary-contract test, not evidence that a
finite flux is calibrated or physically plausible.
:::
::::

## Practice exercises

### Exercise 1: Extend a bounded measurement

Add an optional `uncertainty` field to `FluxMeasurement` or create a second
small measurement type. Decide and document whether zero uncertainty is
allowed. Add tests for a valid measurement, negative uncertainty, non-finite
uncertainty, and a missing unit. Do not add calibration behavior unless you can
state the inputs and assumptions it requires.

### Exercise 2: Compose an observation

Extend `Observation` with one field that your field genuinely needs—for
example, a sample identifier, an observing band, or a controlled temperature.
Keep the contained measurement responsible for its own value/unit invariant.
Write a test that demonstrates the two contracts fail independently.

### Exercise 3: Choose the smallest representation

For each case, choose a dictionary, a function, a small dataclass, or a larger
domain model. Defend the choice in one sentence.

1. A one-off plotting label and color.
2. A repeatedly passed coordinate pair that must remain ordered and finite.
3. A detector reduction that requires raw counts, bias, dark, flat, exposure,
   wavelength response, and calibration provenance.

The aim is not always “make a class.” The aim is to make the smallest contract
that tells the truth about the problem.

## Deep Dive: when a small type becomes a larger software boundary

The techniques below are real tools for larger software, but none follows
automatically from having a dataclass. They belong in the later Part IV
research-software reference when the program has a concrete maintenance,
interoperability, concurrency, or measured-performance need.

### Shared interfaces and abstract base classes

When independently maintained components must support the same operation, a
documented protocol or abstract base class can make the shared interface
explicit. The important design work is the contract: units, array shapes,
failure behavior, ownership, and calibration responsibility—not the `ABC`
syntax alone.

:::{note} The More You Know: interface agreements support collaboration

Multi-site projects often need different instruments or data sources to enter a
common processing workflow. Teams can agree on a small interface—such as a
method that returns a measurement plus its metadata—while retaining local
implementation details. That agreement only helps if its units, uncertainty,
quality flags, and failure behavior are specified and tested. An abstract base
class is one Python mechanism for expressing part of that agreement; it does
not make the scientific outputs interchangeable by itself.
:::

### Inheritance, mixins, and composition

Inheritance expresses a genuine “is a” relationship. Mixins can add an
orthogonal implementation feature, but multiple inheritance introduces method
resolution and initialization-order obligations. Prefer composition when one
object simply owns or uses another object, as `Observation` owns a
`FluxMeasurement`.

:::{tip} Design decision: escalation signals

Consider a protocol or ABC when several independently maintained components
must be accepted by the same consumer. Consider a mixin only after a repeated,
well-tested capability has a clear initialization contract. Prefer composition
when an object has collaborators or fields with independent responsibilities.
:::

:::{note} The More You Know: growing experimental systems change the design question

An early laboratory script may have one camera, one movement routine, and one
output file. A later system can have several instruments, shared timing,
configuration state, retries, and safety interlocks. The useful question then
is not “which advanced pattern should I use?” but “which responsibility is
repeated, and what evidence shows that it needs a shared interface?” Composition
often remains the clearest answer; a mixin or protocol earns its complexity
only when that evidence is real.
:::

### Async, registration, and performance

Async code is appropriate for independent I/O whose ordering, cancellation,
timeouts, cleanup, and device-state dependencies are explicit. It does not make
CPU-bound work parallel, and an instrument must never begin acquisition while a
required move or configuration change is incomplete.

Descriptors, metaclasses, registries, caching, and `__slots__` are similarly
specific tools. A descriptor can centralize repeated attribute behavior; a
registry can support plugin discovery; caching is safe only when inputs and
state make a result reusable; and memory changes require measurement on the
actual Python version and workload. Do not infer a library's internal design
from a public API or from a pattern's name.

### Simple choices before named patterns

| Need | Start with | Escalate only when |
| --- | --- | --- |
| Several numerical algorithms | A function argument or mapping of callables | independent implementations need a stable shared contract |
| Instrument operations | Explicit ordered functions | independent I/O, cancellation, and safety states require async design |
| Repeated computed result | A clear function | profiling shows repeated work and cache invalidation is defined |
| Many objects | A measured memory profile | retained memory is a demonstrated bottleneck |
| Plugins or data readers | Explicit registration/configuration | dynamic discovery is a real maintenance requirement |

## Reference: dataclass choices and escalation cues

| Tool | What it supplies | What it does not supply |
| --- | --- | --- |
| `@dataclass` | generated initializer, `repr`, and field equality | scientific validation or runtime type enforcement |
| `frozen=True` | blocks ordinary field reassignment | deep immutability of a contained mutable object |
| `field(default_factory=list)` | a fresh list per instance | an invariant for the list's contents |
| type annotation | a readable interface expectation | a conversion, unit check, or a static-checking result by itself |
| composition | separate responsibilities in separate objects | a shared interface across unrelated implementations |

### Definitions

**Dataclass**: A decorator that can generate common methods for a class whose
main role is holding state.

**Invariant**: A condition that must hold for every valid instance of a type.

**Composition**: A design in which an object contains or uses another object
with its own responsibility.

**Abstract base class (ABC)**: A class that can require subclasses to implement
selected methods; useful only when a shared interface is genuinely needed.

**Protocol**: A structural description of the attributes or methods a consumer
needs, without requiring a particular inheritance tree.

**Representation**: The stored form of a value, including fields and units; it
is distinct from the physical quantity or model the value may describe.

### Further reference connection

Finish Part II with the [Part II Recap — Inspectable Scientific Evidence](synthesis.md).
It turns Chapters 7–10 into a diagnostic return route for a result that needs
another check. [Part III: Tabular Data and Reproducible Workflows](part-3-data-workflows.md)
will extend this chapter's single-entity contracts to collections, schemas,
quality decisions, and provenance; it is not a prerequisite for the completed
Parts I–II route. Part IV will treat APIs, parallelism, and larger research
software as reference material once those pages are available.

## References

1. Python Software Foundation. [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html).
2. Python Software Foundation. [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html).
3. Python Software Foundation. [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html).
4. Python Software Foundation. [PEP 557 — Data Classes](https://peps.python.org/pep-557/).
