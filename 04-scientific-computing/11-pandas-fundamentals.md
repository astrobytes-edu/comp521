---
title: "Chapter 11: DataFrames — Tables, Types, and Relational Operations"
subtitle: "Scientific Computing with Python | early reference"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{important} Early reference — Part III is in development

This chapter is available as reference material while Part III is being
hardened. It is not part of the completed Parts I–II route. Its durable focus
is table semantics, types, filtering, aggregation, joins, and provenance-aware
operations; Pandas is the first concrete implementation.
:::
<!-- prep-banner:end -->

## An observation table with a contract

### Introductory example

Each row below represents one observation. The table makes the relation between
source, time, band, measured flux, uncertainty, and quality flag inspectable.
It does not calibrate the fluxes or establish that sources in two catalogs are
the same physical object.

```python
import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "source_id", "time_mjd", "band", "flux_w_m2", "flux_uncertainty_w_m2", "quality"
}
VALID_QUALITY_FLAGS = {"good", "suspect", "failed"}


def validate_observation_table(table: pd.DataFrame) -> pd.DataFrame:
    """Validate this chapter's small observation-table contract."""
    missing = REQUIRED_COLUMNS - set(table.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    validated = table.copy()
    numeric_columns = ["time_mjd", "flux_w_m2", "flux_uncertainty_w_m2"]
    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(validated[column]):
            raise TypeError(f"{column} must be numeric")
        if not np.isfinite(validated[column]).all():
            raise ValueError(f"{column} contains non-finite values")

    if (validated["flux_uncertainty_w_m2"] < 0).any():
        raise ValueError("flux uncertainty must be non-negative")
    if not validated["quality"].isin(VALID_QUALITY_FLAGS).all():
        raise ValueError("quality contains an unsupported flag")
    if validated.duplicated(["source_id", "time_mjd", "band"]).any():
        raise ValueError("rows must have unique source/time/band keys")
    return validated


observations = pd.DataFrame(
    {
        "source_id": ["S-101", "S-101", "S-202", "S-202"],
        "time_mjd": [60200.1, 60200.1, 60200.2, 60200.2],
        "band": ["g", "r", "g", "r"],
        "flux_w_m2": [2.1e-15, 1.6e-15, 0.8e-15, 0.7e-15],
        "flux_uncertainty_w_m2": [0.1e-15, 0.1e-15, 0.2e-15, 0.2e-15],
        "quality": ["good", "good", "suspect", "failed"],
    }
)

observations = validate_observation_table(observations)
print(observations)
```

### Preview activity

Before running anything, predict what the validator does if one uncertainty is
negative, if one quality flag is misspelled, or if a row repeats the same
source/time/band key. For each case, decide whether the appropriate response is
to reject the table, preserve a quality flag, or revise the schema.

### Transfer prompt

Choose a table from your field. State what one row represents, name its key,
identify two columns whose units or types matter, and name one missingness or
quality state that must not be silently converted into an ordinary value.

## Learning objectives

By the end of this chapter, you will be able to:

- describe the row, key, columns, types, and quality states of a scientific table;
- use Pandas to select rows without losing the condition that selected them;
- aggregate groups while keeping count and variation visible;
- order time-indexed records deliberately and plot measurements with their
  uncertainties and units visible;
- merge tables with an explicit key-cardinality and unmatched-row check; and
- preserve failed or missing records as evidence rather than replacing them by default.

## Prerequisites

You should be comfortable with NumPy arrays (Chapter 7), reading a simple plot
(Chapter 8), and validating/test-driving a small behavior contract (Chapter 9).
Pandas is the first concrete tool here; the table concepts transfer to other
dataframe systems and relational databases.

:::{note} Core route through this chapter

Read Sections 11.1–11.6 in order. The **Deep Dive** contains storage,
chunking, and performance decisions that need an actual workload; the
**Reference** is for later lookup.
:::

## Why this chapter matters

Numerical arrays are excellent for homogeneous calculations. A scientific
workflow also needs to remember which source, parameter set, run, timestamp,
quality decision, and software configuration produced a value. A table gives
those records a shared schema so that selection, aggregation, and joining can
be inspected rather than reconstructed from parallel lists.

A DataFrame improves organization; it does not make an analysis correct. A
misstated unit, nonunique identifier, inappropriate join, or dropped failure
can still change a conclusion. The habits in this chapter make those decisions
visible and testable.

## 11.1 A DataFrame is a table with a schema

A Pandas `DataFrame` has rows, named columns, column dtypes, and an index. For
the observation table, a row is one source-time-band measurement and
`(source_id, time_mjd, band)` is the chapter's declared key. The default Pandas
index is a row label, not automatically a scientific identifier or a database
primary key.

:::{important} Why This Matters: table semantics prevent bookkeeping errors

When simulations, instruments, or analysis steps produce related values, a
schema tells the next reader how records fit together. It is a stronger defense
than relying on two arrays staying in the same order. It still needs explicit
checks for types, units, keys, and provenance.
:::

### Inspect columns before analyzing them

```python
print(observations.dtypes)
print(observations["quality"].value_counts(dropna=False))
print(observations[["source_id", "time_mjd", "band"]].duplicated().any())
```

The last line is `False` because the validator checked the declared key. This
does not prove that `source_id` is globally meaningful or that two records from
different surveys identify the same source.

:::{tip} Modeling boundary: a table is not a physical model

The flux columns are values in a stated unit. Their interpretation still needs
calibration, uncertainty modeling, selection effects, and domain knowledge.
Putting values in a DataFrame does not create that evidence.
:::

## 11.2 Select rows while keeping the rule visible

Use `.loc` with a named boolean condition when the condition is part of the
scientific record. Use `.iloc` only for positional selection after you have
made sure that position, rather than a label, is the intended meaning.

```python
usable = observations.loc[
    observations["quality"].eq("good"),
    [
        "source_id",
        "time_mjd",
        "band",
        "flux_w_m2",
        "flux_uncertainty_w_m2",
        "quality",
    ],
].copy()

print(usable)
```

`.copy()` makes this a deliberate derived table. Keep the original table and
the quality column available so another reader can see which rows were excluded
and why.

::::{note} Check Your Understanding

Which statement is justified by the selection above?

1. The selected fluxes are physically valid.
2. The selected rows satisfy this table's `quality == "good"` rule.
3. The selected sources are the complete population.

:::{note} Answer
:class: dropdown

Only statement 2 follows. A quality flag is a stated workflow decision; it does
not establish physical validity or completeness. Those claims need a documented
quality model and a selection-function argument.
:::
::::

### Labels, positions, and alignment

Pandas aligns labeled objects in many operations. That can prevent accidental
position-based mismatches, but it can also create missing values when labels do
not overlap. Inspect indexes and missingness after combining Series rather than
assuming alignment proves the intended relationship.

## 11.3 Aggregate groups without hiding variation

Grouping answers a question of the form “for each value of this declared
column, summarize these declared rows.” The grouping key and the summary both
belong in the analysis record.

```python
by_band = (
    observations.groupby("band", dropna=False)
    .agg(
        n_measurements=("flux_w_m2", "size"),
        mean_flux_w_m2=("flux_w_m2", "mean"),
        std_flux_w_m2=("flux_w_m2", "std"),
        n_good=("quality", lambda values: values.eq("good").sum()),
    )
    .reset_index()
)
print(by_band)
```

The mean is a descriptive statistic for these rows. It is not an uncertainty
model, a convergence result, or evidence that the two bands measure the same
physical quantity. The count and quality summary reveal how much data support
each group.

:::{tip} Computational Thinking: split, apply, combine is a question, not magic

Before writing `groupby`, say the question in a sentence: “For each band, how
many rows and what flux summary remain after this quality rule?” If you cannot
state the population, group key, and summary, the operation is not yet an
interpretable analysis.
:::

## 11.4 Time-indexed records need an explicit order and an honest figure

The `time_mjd` column is a measurement coordinate, not a promise that rows are
already chronological. Sort explicitly before connecting observations with a
line or computing a time-dependent quantity. Keep the original timestamp in
the table; a shifted time coordinate can make a figure easier to read without
discarding the recorded time.

```python
import matplotlib.pyplot as plt


light_curve = pd.DataFrame(
    {
        "source_id": ["S-101", "S-101", "S-101"],
        "time_mjd": [60200.3, 60200.1, 60200.2],
        "band": ["g", "g", "g"],
        "flux_w_m2": [2.0e-15, 2.2e-15, 2.1e-15],
        "flux_uncertainty_w_m2": [0.1e-15, 0.1e-15, 0.1e-15],
        "quality": ["good", "good", "good"],
    }
)

chronological = validate_observation_table(light_curve).sort_values("time_mjd")
reference_mjd = chronological["time_mjd"].iloc[0]
chronological = chronological.assign(
    days_since_first=chronological["time_mjd"] - reference_mjd
)

fig, ax = plt.subplots()
ax.errorbar(
    chronological["days_since_first"],
    chronological["flux_w_m2"],
    yerr=chronological["flux_uncertainty_w_m2"],
    fmt="o-",
    capsize=3,
)
ax.set(
    xlabel="Days since first observation [day]",
    ylabel="Flux [W m$^{-2}$]",
    title="Three g-band measurements of S-101",
)
plt.show()
```

The line makes the measured time order legible; it is not an interpolation,
fit, or evidence for a physical trend. The error bars show the supplied
per-row uncertainties, not every source of systematic uncertainty.

:::{tip} Predict before running

The rows were deliberately entered out of order. Predict the x-coordinate of
the first plotted point before running the code. It is `0.0` days because the
code sorts by `time_mjd` before subtracting the earliest timestamp.
:::

## 11.5 Join tables with a declared relationship

Merging is where a convenient table operation can quietly duplicate or discard
evidence. First decide the relationship: is each observation expected to match
one metadata row, many metadata rows, or none? Then encode that expectation in
the merge.

```python
source_metadata = pd.DataFrame(
    {
        "source_id": ["S-101", "S-202", "S-303"],
        "field": ["north", "south", "north"],
        "catalog_version": ["v1", "v1", "v1"],
    }
)

joined = observations.merge(
    source_metadata,
    on="source_id",
    how="left",
    validate="many_to_one",  # many observations may share one metadata row
    indicator=True,
)
print(joined[["source_id", "field", "_merge"]])
```

The `_merge` column reports whether each observation matched metadata. A left
join preserves all observations; it does not prove that the identifiers describe
the same physical object across catalogs.

::::{warning} Debug This!: join cardinality is part of the contract

Predict what happens if the metadata table contains `S-101` twice.

```python
duplicate_metadata = pd.concat(
    [source_metadata, source_metadata.iloc[[0]]], ignore_index=True
)

# This should raise: observations expect at most one metadata row per source.
observations.merge(
    duplicate_metadata,
    on="source_id",
    how="left",
    validate="many_to_one",
)
```

:::{note} Answer
:class: dropdown

`validate="many_to_one"` raises `MergeError` because the right-hand key is no
longer unique. Duplicated keys are not inherently a Cartesian-product bug: they
can be intentional in a many-to-many relationship. The error is useful here
because it conflicts with the relationship we declared.
:::
::::

## 11.6 Preserve missingness and failed runs as evidence

Missing values have different meanings: an instrument may not have observed a
band, a solver may have diverged, a calculation may be inapplicable, or a file
may be incomplete. Put that meaning in an explicit status or reason column; do
not use `NaN` alone as the complete explanation.

```python
runs = pd.DataFrame(
    {
        "run_id": ["R-01", "R-02", "R-03", "R-04"],
        "resolution": [64, 64, 128, 128],
        "status": ["completed", "diverged", "completed", "timed_out"],
        "final_energy": [-1.02, np.nan, -1.00, np.nan],
        "failure_reason": [pd.NA, "nonlinear solve", pd.NA, "wall-time limit"],
    }
)

completed = runs.loc[runs["status"].eq("completed")].copy()
excluded = runs.loc[~runs["status"].eq("completed"), ["run_id", "failure_reason"]]
print(completed)
print(excluded)
```

This selection is not a recommendation to delete failed runs. It creates a
declared analysis subset while preserving a table that can reveal whether
failure is correlated with resolution or another input.

:::{tip} Modeling boundary: interpolation is a model choice

Interpolating an occasional missing time sample may be appropriate when a
scientific model, cadence, uncertainty treatment, and intended use justify it.
It is not a generic repair for a failed run, a missing observation, or a gap
across a discontinuity. Preserve the original missingness and record any
imputation separately.
:::

## Practice exercises

### Exercise 1: Write a table contract

Create a DataFrame for a small dataset in your field. State the row meaning,
key, required columns, units, valid quality states, and one condition that
should reject the table. Implement and test one validator check.

### Exercise 2: Audit a merge

Make two tiny tables with a key and intentionally duplicate a key on one side.
Predict the expected cardinality, run `merge(..., validate=...)`, and explain
whether the duplicate is a data problem or an intended relationship.

### Exercise 3: Make an exclusion visible

Create a table with at least two failure reasons. Produce one summary table for
all rows and one for an analysis subset. Report both row counts and explain what
the subset cannot establish.

## Deep Dive: storage, chunking, and performance need measured evidence

DataFrames are useful for labeled records and relational operations. Whether a
particular dtype, storage format, or NumPy conversion improves a real workflow
depends on data range, missingness, libraries, machine, and access pattern.

### Dtypes and memory

Measure memory with `df.memory_usage(deep=True)` before and after a candidate
change. Narrowing a float dtype is justified only after checking the needed
range, precision, downstream numerical sensitivity, and file-format behavior.
Categorical columns can reduce memory for repeated labels, but they also change
some operations and serialization choices.

### Chunked CSV processing

The following pattern computes a row-weighted mean across chunks. It is a
template for a real file; it does not create an input file or claim that every
operation can stream in this way.

```python
def mean_finite_flux_from_csv(filename, chunksize=100_000):
    total_flux = 0.0
    n_rows = 0

    for chunk in pd.read_csv(filename, chunksize=chunksize):
        flux = chunk["flux_w_m2"]
        finite_flux = flux[np.isfinite(flux)]
        total_flux += finite_flux.sum()
        n_rows += len(finite_flux)

    if n_rows == 0:
        raise ValueError("no finite flux values were found")
    return total_flux / n_rows
```

### Format choices

| Format | Useful when | Important boundary |
| --- | --- | --- |
| CSV | simple exchange and inspection | store schema, units, missing-value rules, and parsing choices separately |
| Parquet | typed columnar tables and supported tooling | verify round trips, dependency versions, and metadata behavior |
| HDF5 | a project has a defined HDF5 layout and dependency path | it is a container, not a universal DataFrame contract |
| JSON | small structured interchange/configuration | numeric, datetime, and nested-type conventions must be stated |
| Pickle | short-lived, trusted Python-only cache | never load untrusted Pickle data; do not treat it as a durable exchange format |

## Reference: common operations and cautions

| Task | Pandas operation | Check before trusting the result |
| --- | --- | --- |
| inspect schema | `df.dtypes`, `df.columns` | expected columns, numeric types, units, and nulls |
| select rows | `df.loc[mask]` | the mask's population and exclusion count |
| summarize groups | `df.groupby(...).agg(...)` | group key, count, variation, and missing groups |
| join tables | `df.merge(..., validate=..., indicator=True)` | key uniqueness/cardinality and unmatched rows |
| retain failures | status/reason columns | whether the analysis subset is biased |
| move to NumPy | `df[[...]].to_numpy()` | units, dtype, column order, and measured need |

### Definitions

**DataFrame**: A two-dimensional labeled table whose columns can have different
types and whose rows share an index.

**Schema**: The stated row meaning, columns, types, units, keys, and allowed
quality/missingness states of a table.

**Key**: A column or column combination used to identify a row for a declared
purpose. It is not automatically unique or physically meaningful.

**Aggregation**: A summary of groups of rows, such as a count, mean, or
standard deviation.

**Join cardinality**: The expected one-to-one, one-to-many, many-to-one, or
many-to-many relationship between two tables' keys.

**Missingness**: An absent value together with its reason and treatment;
different causes need not support the same analysis response.

### Further reference connection

This early-reference chapter establishes table contracts and relational checks.
Later Part III material will extend those ideas to acquisition, cleaning,
exploration, storage formats, and scalable tabular workflows as those chapters
become available.

## References

1. Pandas documentation. [User Guide](https://pandas.pydata.org/docs/user_guide/).
2. Pandas documentation. [Merge, join, concatenate and compare](https://pandas.pydata.org/docs/user_guide/merging.html).
3. Pandas documentation. [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html).
4. Pandas documentation. [Scaling to large datasets](https://pandas.pydata.org/docs/user_guide/scale.html).
