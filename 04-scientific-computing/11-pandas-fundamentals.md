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

## Learning Objectives

By the end of this chapter, you will be able to:

- **(1) Create** and manipulate DataFrames to organize simulation outputs, parameter studies, and numerical experiments
- **(2) Apply** indexing, slicing, and boolean masking to extract specific subsets of computational results efficiently
- **(3) Implement** groupby operations to analyze convergence, parameter dependencies, and ensemble statistics
- **(4) Design** data pipelines that merge outputs from different simulation codes and combine multi-physics results
- **(5) Transform** raw simulation outputs into clean, analysis-ready DataFrames using reshaping and pivoting
- **(6) Calculate** rolling statistics, track conservation quantities, and handle missing data from failed runs
- **(7) Optimize** memory usage and performance when processing large simulation snapshots or parameter grids
- **(8) Export** computational results to various formats for publication, collaboration, and checkpoint management

## Prerequisites Check

Before starting this chapter, verify you can:

- [ ] Work confidently with NumPy arrays (Chapter 7)
- [ ] Create plots with Matplotlib (Chapter 8)
- [ ] Handle errors and validate data (Chapter 9)
- [ ] Design classes with proper methods (Chapters 5, 10)
- [ ] Read and write files in various formats (Chapter 5)
- [ ] Use list comprehensions and dictionary operations (Chapter 4)

### Self-Assessment Diagnostic

Test your readiness by predicting the outputs:

```python
import numpy as np

# Question 1: What's the shape of this array operation?
data = np.array([[1, 2, 3], [4, 5, 6]])
result = data.mean(axis=0)
print(result)  # Shape and values?

# Question 2: How would you find unique values efficiently?
values = [0.5, 1.2, 0.5, 2.3, 1.2, 3.5]
# How many unique values?

# Question 3: What's wrong with this dictionary operation?
params = {'mass': [1e10, 2e10], 'radius': [1, 2, 3]}
# Why would this cause problems in analysis?

# Question 4: How would you organize this simulation output?
results = []
for mass in [1e10, 2e10, 3e10]:
    for viscosity in [0.001, 0.01, 0.02]:
        result = mass * viscosity  # Simplified
        results.append([mass, viscosity, result])
# What data structure would be better?
```

:::{note} Self-Assessment Answers
:class: dropdown

1. Result is `[2.5, 3.5, 4.5]` with shape `(3,)` - mean along columns
2. Use `set(values)` to get unique values: 4 unique values
3. Dictionary values have different lengths (2 vs 3) - can't form rectangular data
4. A table/DataFrame would be better for parameter study results

If you struggled with array operations or organizing structured data, review NumPy (Chapter 7) first!
:::

:::{important} Primary Resource
The official Pandas documentation (<https://pandas.pydata.org/docs/>) is your lifelong reference. This chapter provides a scientific computing-focused introduction, but the official docs contain comprehensive guides, API references, and advanced techniques you'll need throughout your career. Bookmark it now—you'll use it weekly.
:::

---

## Chapter Overview

Every simulation produces vast outputs: density fields, velocity distributions, temperature maps across thousands of timesteps. Every numerical solver generates tracks: state variables evolving over time. Every particle-based integration outputs positions, velocities, and energies for countless particles. Whether you're running fluid dynamics simulations, molecular dynamics, or custom codes for dynamical systems, you face the same challenge: how do you organize, analyze, and track results from hundreds of runs across multi-dimensional parameter spaces? NumPy (Chapter 7) gave you arrays for numerical computation, but real computational science requires more—you need to track which parameters produced which results, merge outputs from different physics modules, analyze convergence across resolutions, and maintain data integrity through complex analysis pipelines. **Pandas** is Python's answer to this challenge, providing DataFrames that combine the computational efficiency of arrays with the organizational power of databases.

Pandas transforms how computational scientists manage simulation data. Instead of the error-prone manual bookkeeping common in Fortran or C++ codes—where parallel arrays track different quantities and a single misaligned index corrupts your entire analysis—DataFrames keep related data together with meaningful labels. Remember the frustration from Chapter 4 when managing parallel lists led to synchronization bugs? DataFrames solve this systematically. Instead of writing nested loops to analyze parameter dependencies (like those we struggled with in Chapter 5), you use vectorized groupby operations that run at compiled speeds. Instead of complex pointer arithmetic to combine outputs from different modules, you use high-level merge operations that handle the details. This isn't just about convenience; it's about correctness and reproducibility. When you're comparing models across a six-dimensional parameter space, tracking convergence through resolution studies, or combining outputs from separate solver modules, manual data management becomes a primary source of scientific errors. Pandas handles the bookkeeping, letting you focus on the physics.

This chapter teaches Pandas from a computational physicist's perspective, building on the programming foundations from earlier chapters. You'll extend the NumPy array operations from Chapter 7 to labeled data structures. The file I/O techniques from Chapter 5 will expand to handle multiple data formats efficiently. The error handling principles from Chapter 9 become crucial when dealing with missing data and failed simulation runs. You'll learn to organize simulation outputs where each row might represent a complete timestep, a converged model, or a parameter combination. You'll discover how groupby operations let you analyze ensemble runs—finding which initial conditions lead to stable solutions, which resolutions achieve convergence, or which parameters match theoretical predictions. You'll master techniques for tracking conservation quantities through long integrations, detecting numerical instabilities, and validating simulation outputs. Most importantly, you'll learn the mental model of "split-apply-combine" that makes complex computational analyses both clear and efficient. By chapter's end, you'll transform from manually managing arrays and writing error-prone bookkeeping code to elegantly expressing data transformations that are both readable and robust.

---

## 11.1 DataFrames: Your Simulation's Best Friend

:::{margin}
**DataFrame**
A 2D labeled data structure with columns of potentially different types, like a computational spreadsheet with programming superpowers.
:::

:::{margin}
**Series**
A 1D labeled array, essentially a single column of a DataFrame with an index.
:::

### Beyond Arrays: Why DataFrames Matter for Simulations

You've been using NumPy arrays successfully for numerical computations, and if you've worked with compiled languages, you've used structs or derived types to organize data. So why do you need DataFrames? The answer lies in the complexity of modern computational workflows.

Consider a typical parameter study. In Fortran, you might organize your data like this:

```fortran
! Traditional Fortran approach - separate arrays
real*8 :: masses(1000)
real*8 :: viscosities(1000)
real*8 :: outputs(1000, 500)  ! 500 timesteps
integer :: convergence_flags(1000)
character(len=20) :: model_names(1000)

! Or using derived types - better but still limited
type simulation_model
    real*8 :: mass
    real*8 :: viscosity
    real*8, dimension(500) :: output_track
    integer :: converged
    character(len=20) :: name
end type simulation_model

type(simulation_model) :: models(1000)
```

This approach has fundamental problems:

1. **No built-in operations**: Want the mean output for all models with mass > 10? Write a loop.
2. **Manual memory management**: Need to add a column? Reallocate everything.
3. **No metadata**: Which index corresponds to which parameter combination?
4. **Error-prone indexing**: One wrong index and you're analyzing the wrong model.
5. **No missing data handling**: A failed run? Hope you track that manually.

**DataFrames solve these problems systematically:**

```python
import pandas as pd
import numpy as np

# Modern approach with Pandas
simulation_models = pd.DataFrame({
    'mass': [0.5, 1.0, 2.0, 5.0],
    'viscosity': [0.02, 0.02, 0.01, 0.001],
    'max_output': [0.08, 1.0, 7.9, 832.0],
    'converged': [True, True, True, False],
    'runtime_hours': [2.3, 5.1, 8.7, 48.2]
})

# Operations that would require loops in Fortran/C++
unit_mass = simulation_models[simulation_models['mass'] == 1.0]
mean_runtime = simulation_models.groupby('viscosity')['runtime_hours'].mean()
converged_fraction = simulation_models['converged'].mean()

print(f"Converged models: {converged_fraction:.1%}")
print(f"Unit mass model output: {unit_mass['max_output'].values[0]}")
```

### DataFrames vs Excel: Why Not Just Use Spreadsheets?

Many students default to Excel for data organization — it's familiar and visual. But Excel fails catastrophically for computational science:

**Excel's Fatal Flaws for Computational Science:**

| Aspect | Excel | Pandas | Why It Matters |
|--------|--------|---------|----------------|
| **Row limit** | 1,048,576 rows | Billions (memory limited) | One large simulation timestep can exceed Excel's total capacity |
| **Reproducibility** | Mouse clicks, no version control | Code-based, git-trackable | Papers require reproducible analysis |
| **Performance** | Minutes for 100k rows | Milliseconds | Analyzing parameter studies becomes impractical |
| **Computation** | Basic math only | Full NumPy/SciPy integration | Can't compute eigenvalues, FFTs, or solve ODEs |
| **Automation** | Manual or VBA macros | Python scripts on HPC | Can't run Excel on supercomputers |
| **Type safety** | Converts data unpredictably | Explicit dtype control | Gene names $\to$ dates, numbers $\to$ text |
| **Memory** | Loads everything + GUI overhead | Efficient columnar storage | Can't handle simulation outputs |

Here's a concrete example that breaks Excel:

```python
# Typical N-body simulation output
n_particles = 100000
n_snapshots = 100

# This would be 10 million rows - Excel crashes
nbody_data = []
for snap in range(n_snapshots):
    for particle in range(1000):  # Just 1000 for demo
        nbody_data.append({
            'snapshot': snap,
            'particle_id': particle,
            'x': np.random.randn(),
            'y': np.random.randn(),
            'z': np.random.randn(),
            'vx': np.random.randn() * 100,
            'vy': np.random.randn() * 100,
            'vz': np.random.randn() * 100,
            'mass': np.random.lognormal(10, 1)
        })

# Pandas handles this easily
nbody_df = pd.DataFrame(nbody_data)
print(f"Created {len(nbody_df):,} rows in memory")
print(f"Memory usage: {nbody_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# Analysis that would be impossible in Excel
velocity_evolution = nbody_df.groupby('snapshot').agg({
    'vx': 'std',
    'vy': 'std',
    'vz': 'std'
})
print(f"\nVelocity dispersion evolution computed in milliseconds")
```

### DataFrames vs C++/Fortran Structures

For computational scientists coming from compiled languages, here's how DataFrames compare:

```python
# What you'd write in C++ (pseudocode):
# struct SimulationRun {
#     double param_a, param_b, param_c;
#     vector<double> output_spectrum;
#     bool converged;
# };
# vector<SimulationRun> runs;
#
# // Finding all converged runs with param_a > 0.3:
# vector<SimulationRun*> selected;
# for(auto& run : runs) {
#     if(run.converged && run.param_a > 0.3) {
#         selected.push_back(&run);
#     }
# }

# In Pandas - cleaner and safer:
runs = pd.DataFrame({
    'param_a': [0.25, 0.30, 0.35],
    'param_b': [0.75, 0.70, 0.65],
    'param_c': [0.79, 0.81, 0.83],
    'converged': [True, True, False]
})

# One line instead of a loop
selected = runs[(runs['converged']) & (runs['param_a'] > 0.3)]
print(selected)
```

### Understanding DataFrame Structure

A DataFrame is fundamentally a collection of Series (columns) sharing a common index:

```python
# Create a simulation output DataFrame
sim_output = pd.DataFrame({
    'timestep': [0, 100, 200, 300, 400],
    'kinetic_energy': [1000.0, 998.5, 997.2, 996.1, 995.3],
    'potential_energy': [-2000.0, -1997.0, -1994.4, -1992.2, -1990.6],
    'virial_ratio': [0.5, 0.501, 0.502, 0.502, 0.502]
})

# Set timestep as index for efficient lookup
sim_output = sim_output.set_index('timestep')

print("DataFrame structure:")
print(sim_output)
print(f"\nIndex type: {type(sim_output.index)}")
print(f"Column types: {sim_output.dtypes.to_dict()}")

# Each column is a Series
kinetic = sim_output['kinetic_energy']
print(f"\nKinetic energy series type: {type(kinetic)}")
```

:::{tip} Check Your Understanding: DataFrame Structure
:class: dropdown

What happens when you extract a single column from a DataFrame?

a) You get a NumPy array
b) You get a Python list
c) You get a Series object
d) You get a single-column DataFrame

**Answer:** c) You get a Series object. A Series is like a 1D labeled array - it maintains the index from the DataFrame, allowing for aligned operations. To get a NumPy array, use `.values` or `.to_numpy()`.
:::

### Creating DataFrames from Simulation Results

Now we'll explore how to create DataFrames from typical computational workflows. The key insight is that DataFrames excel at organizing heterogeneous data—mixing floats, integers, strings, and booleans in a single structure while maintaining relationships between them. This is exactly what we need when tracking simulation parameters alongside their outputs.

:::{note} Note on Code Examples
Each section's code examples are self-contained. DataFrames created in one section aren't automatically available in the next, allowing you to run sections independently. When we reference a DataFrame from an earlier section, we'll either recreate it or note that it's from a previous example.
:::

Consider first how we organize simulation models. In real simulation codes, each model run produces hundreds of output quantities at thousands of timesteps. Here we'll use simplified scaling relations to illustrate the data organization principles. Remember from Chapter 7 that NumPy arrays excel at homogeneous numerical data—DataFrames extend this to mixed-type, labeled data:

```python
# Example 1: Simple model grid
import pandas as pd
import numpy as np

models = []
for mass in [0.5, 1.0, 2.0, 5.0, 10.0]:
    for parameter in [0.001, 0.01, 0.02]:
        # Simplified relations (pedagogical model)
        # Real physics involves solving coupled ODEs
        # as we'll see in Chapter 12 with SciPy
        output = mass**3.5  # Simple power law approximation
        temperature = 300 * mass**0.5  # Rough scaling
        lifetime = 10.0 * mass**(-2.5)  # Time scale

        models.append({
            'mass': mass,
            'parameter': parameter,
            'output': output,
            'temperature': temperature,
            'lifetime': lifetime
        })

model_df = pd.DataFrame(models)
print(f"Model grid: {len(model_df)} models")
print(model_df.head())
print(f"\nData types (compare to Chapter 4's type discussion):")
print(model_df.dtypes)
```

Notice how the DataFrame automatically infers column types and aligns the data. Unlike the manual type management we discussed in Chapter 4, Pandas handles type inference intelligently. Each row represents one complete model with all its parameters and outputs together. This prevents the synchronization errors that plague parallel array approaches.

DataFrames excel at organizing particle-based simulation data where properties evolve over time. Consider how dynamical simulations need to track positions and velocities across many timesteps. This structure keeps all related information synchronized:

```python
# Example 2: Particle simulation output organization
n_particles = 1000
n_snapshots = 10

# Mock snapshot data structure
snapshots = []
for snap in range(n_snapshots):
    # Sample subset for demonstration
    for i in range(100):
        snapshots.append({
            'snapshot': snap,
            'particle_id': i,
            'x': np.random.randn(),
            'y': np.random.randn(),
            'z': np.random.randn(),
            'vx': np.random.randn() * 10,
            'vy': np.random.randn() * 10,
            'vz': np.random.randn() * 10
        })

particle_df = pd.DataFrame(snapshots)
print(f"\nParticle snapshots: {len(particle_df)} particle-timesteps")
print(particle_df.head())

# Easy selection of specific timesteps
snap_5 = particle_df[particle_df['snapshot'] == 5]
print(f"\nParticles at snapshot 5: {len(snap_5)}")
```

This structure enables tracking individual particles across time, computing ensemble statistics at each timestep, and verifying physical conservation laws—essential for any dynamical simulation validation.

:::{tip} Computational Thinking Box: Row-wise vs Column-wise Operations

**PATTERN: Vectorized Column Operations for Performance**

Pandas inherits NumPy's vectorization philosophy. Always think column-wise:

```python
# BAD: Row iteration (Fortran/C++ habit) - SLOW!
for idx, row in df.iterrows():
    df.loc[idx, 'kinetic'] = 0.5 * row['mass'] * row['velocity']**2

# GOOD: Vectorized column operation - FAST!
df['kinetic'] = 0.5 * df['mass'] * df['velocity']**2

# BETTER: Direct NumPy when possible - FASTEST!
df['kinetic'] = 0.5 * df['mass'].values * df['velocity'].values**2
```

For 1 million particles:

- Row iteration: ~5 seconds
- Pandas vectorized: ~50 milliseconds
- NumPy arrays: ~5 milliseconds
:::

---

## 11.2 Indexing and Selection: Finding Your Data

:::{margin}
**Index**
The row labels of a DataFrame, providing O(1) lookup and automatic alignment.
:::

### The Mental Model: Labels vs Positions

DataFrames offer two indexing paradigms, each suited to different tasks:

1. **Label-based (`.loc[]`)**: Like accessing simulation runs by parameter values
2. **Position-based (`.iloc[]`)**: Like accessing array elements by index

This dual nature exists because computational workflows need both:

- **Labels** for identifying specific models: "Get the M=5, param=0.02 run"
- **Positions** for algorithmic operations: "Get every 10th timestep for visualization"

```python
# Create a simulation catalog with meaningful index
sim_catalog = pd.DataFrame({
    'param_a': [0.25, 0.30, 0.35, 0.30, 0.30],
    'param_b': [0.75, 0.81, 0.87, 0.81, 0.81],
    'box_size': [100, 100, 100, 200, 500],
    'n_particles': [256**3, 256**3, 256**3, 512**3, 1024**3]
})

# Create meaningful index from parameters
sim_catalog.index = [
    f"L{box}_A{a:.2f}"
    for box, a in zip(sim_catalog['box_size'], sim_catalog['param_a'])
]

print("Simulation catalog with labeled index:")
print(sim_catalog)
```

### Label-based Selection with `loc`

```python
# Select specific simulation
sim = sim_catalog.loc['L100_A0.30']
print(f"Single simulation:\n{sim}\n")

# Select multiple simulations
large_boxes = sim_catalog.loc[['L200_A0.30', 'L500_A0.30']]
print(f"Large box simulations:\n{large_boxes}\n")

# Select with conditions
high_res = sim_catalog.loc[sim_catalog['n_particles'] > 256**3]
print(f"High resolution runs:\n{high_res}")
```

### Boolean Masking: The Power Tool

Boolean masking is essential for analyzing scientific data:

```python
# Create sample data
sample_data = pd.DataFrame({
    'object_id': range(100),
    'value_a': np.random.randn(100) * 50,
    'value_b': np.random.randn(100) * 50,
    'magnitude': np.random.uniform(10, 22, 100)
})

# Find high-value objects
total_value = np.sqrt(sample_data['value_a']**2 + sample_data['value_b']**2)
high_value_objects = sample_data[total_value > 50]

print(f"High value objects: {len(high_value_objects)}/{len(sample_data)}")

# Multiple criteria
selected = sample_data[
    (sample_data['magnitude'] < 15) &  # Bright
    (total_value > 20) &                # Significant
    (sample_data['object_id'] < 50)    # First half
]

print(f"Selected candidates: {len(selected)}")

# Using query method for readable selection
bright_objects = sample_data.query(
    'magnitude < 12'
)
print(f"Bright objects: {len(bright_objects)}")
```

:::{warning} Common Bug Alert: The SettingWithCopyWarning

This warning prevents silent data corruption:

```python
# DANGER: May not modify original!
subset = df[df['energy'] < 0]
subset['flag'] = 1  # SettingWithCopyWarning!

# SAFE: Explicit copy
subset = df[df['energy'] < 0].copy()
subset['flag'] = 1  # Now safe

# SAFE: Direct modification
df.loc[df['energy'] < 0, 'flag'] = 1
```

This is crucial when flagging failed runs or bad timesteps!
:::

---

## 11.3 GroupBy: Analyzing Parameter Dependencies

:::{margin}
**GroupBy**
Split-apply-combine pattern for analyzing grouped data efficiently.
:::

### Understanding Split-Apply-Combine for Simulations

The groupby operation represents a fundamental shift in how we think about data analysis. Instead of the explicit loops we learned in Chapter 5, we express our analysis intent declaratively. This pattern, formalized by Hadley Wickham in the R community and adopted throughout data science, consists of three conceptual steps:

1. **Split**: Partition data into groups based on some criteria
2. **Apply**: Execute a function on each group independently
3. **Combine**: Merge the results back into a single data structure

Think of groupby like sorting homework by student name, then computing each student's average. Instead of manually looping through all assignments, checking which student each belongs to, and accumulating totals, groupby does this automatically. The mental model is powerful: you describe what you want ("average grade per student"), not how to compute it (loops and conditionals).

Let's see this in action with our models. First, we'll recreate the model DataFrame from Section 11.1:

```python
# Recreate models DataFrame for this section
np.random.seed(42)

models_data = []
for mass in [0.5, 1.0, 2.0, 5.0, 10.0]:
    for parameter in [0.001, 0.01, 0.02]:
        # Add multiple realizations with slight variations
        for seed in range(3):
            # Use different but reproducible seeds
            np.random.seed(42 + seed + int(mass*100))

            # Base calculations (simplified physics)
            base_output = mass**3.5
            base_lifetime = 10.0 * mass**(-2.5)

            # Add numerical scatter to simulate code variations
            output = base_output * np.random.normal(1, 0.02)
            lifetime = base_lifetime * np.random.normal(1, 0.01)

            models_data.append({
                'mass': mass,
                'parameter': parameter,
                'seed': seed,
                'output': output,
                'lifetime': lifetime,
                'converged': np.random.random() > 0.1  # 90% convergence
            })

model_df = pd.DataFrame(models_data)
print(f"Parameter study with {len(model_df)} models")
print(model_df.head())
```

Now let's apply groupby to understand parameter dependencies. This is exactly the type of analysis you'd perform when validating simulation codes or exploring parameter space:

```python
# Group by mass to analyze mass-dependent properties
mass_groups = model_df.groupby('mass')

# Compute statistics across different random seeds
# This is how we verify numerical stability
lifetime_stats = mass_groups['lifetime'].agg([
    'mean',  # Average across seeds
    'std',   # Numerical scatter
    'min',   # Minimum value
    'max',   # Maximum value
    'count'  # Number of successful runs
])

print("Lifetime statistics by mass:")
print(lifetime_stats)

# Coefficient of variation - key metric for numerical stability
lifetime_stats['cv'] = lifetime_stats['std'] / lifetime_stats['mean']
print(f"\nNumerical scatter (CV): {lifetime_stats['cv'].mean():.4f}")
print("CV < 0.02 indicates good numerical stability")
```

The groupby operation just accomplished what would require nested loops and manual bookkeeping in traditional approaches. Compare this to the loop-based approach from Chapter 5—the intent is much clearer here.

### Multi-level Grouping for Parameter Studies

Real computational studies often vary multiple parameters simultaneously. Consider a simulation campaign where you vary several physical parameters. Each combination might be run multiple times with different random seeds to assess statistical variance. Multi-level grouping handles this complexity elegantly:

```python
# Create a more complex parameter study
np.random.seed(42)

params = []
for param_a in [0.25, 0.30, 0.35]:
    for param_b in [0.65, 0.70, 0.75]:
        for param_c in [67, 70, 73]:
            # Multiple random seeds for variance estimation
            for seed in range(5):
                np.random.seed(seed * 100 + int(param_a * 100))

                # Mock results
                result_base = 0.8 * (param_a/0.3)**0.5
                result = result_base * np.random.normal(1, 0.02)

                # Number of features above threshold
                n_features = int(1000 * result * np.random.normal(1, 0.1))

                params.append({
                    'param_a': param_a,
                    'param_b': param_b,
                    'param_c': param_c,
                    'seed': seed,
                    'result': result,
                    'n_features': n_features,
                    'cpu_hours': np.random.uniform(100, 500)
                })

param_df = pd.DataFrame(params)
print(f"Parameter grid: {len(param_df)} simulations")

# Multi-level grouping - group by all parameters
param_groups = param_df.groupby(['param_a', 'param_b', 'param_c'])

# Compute mean and variance across random seeds
# This separates physical effects from statistical variance
results = param_groups.agg({
    'result': ['mean', 'std'],
    'n_features': ['mean', 'std'],
    'cpu_hours': 'sum'  # Total computational cost
})

print("\nResults by parameters:")
print(results.head(10))

# Flatten column names for easier access
results.columns = ['_'.join(col).strip() for col in results.columns.values]
print(f"\nTotal CPU hours: {results['cpu_hours_sum'].sum():.0f}")
```

This hierarchical analysis structure scales to arbitrarily complex parameter studies.

:::{tip} Check Your Understanding: GroupBy Operations
:class: dropdown

You have 1000 N-body simulations with different numbers of particles. What does this code do?

```python
df.groupby('n_particles')['energy_error'].mean()
```

a) Computes total energy error across all simulations
b) Finds mean energy error for each resolution level
c) Returns the mean number of particles
d) Groups by energy error values

**Answer:** b) It computes the mean energy error for each unique value of n_particles. This is how you'd analyze convergence with resolution—seeing if energy conservation improves with more particles.
:::

### Custom Aggregation for Analysis

In real data analysis, we need to apply custom functions to detect patterns in our data. The examples below show simplified approaches to illustrate Pandas functionality.

```python
def detect_variability_simple(values):
    """
    Simplified variability detection for pedagogical purposes.

    NOTE: Real variability detection uses sophisticated methods.
    This is just for illustration!
    """
    if len(values) < 10:
        return False
    # Check if standard deviation exceeds threshold
    return values.std() > 0.2

def classify_behavior(group):
    """
    Toy classifier for demonstration.
    Real classifiers use features like period, amplitude,
    and other domain-specific information.
    """
    value_range = group['value'].max() - group['value'].min()
    time_span = group['time'].max() - group['time'].min()

    if value_range > 1.0:
        return 'possible_transient'
    elif value_range > 0.3:
        return 'variable_candidate'
    else:
        return 'stable'

# Create sample time series data
np.random.seed(42)
time_series_data = []
for obj_id in range(50):
    for t in range(20):
        time_series_data.append({
            'object_id': obj_id,
            'time': t,
            'value': np.random.randn() * (0.5 if obj_id % 5 == 0 else 0.1)
        })

ts_df = pd.DataFrame(time_series_data)

# Apply classification to each object
classifications = ts_df.groupby('object_id').apply(
    classify_behavior, include_groups=False
)
print("Object classifications:")
print(classifications.value_counts())
```

The groupby-apply pattern shown here is fundamental to scientific data analysis. Whether you're classifying time series, finding clusters, or analyzing simulation convergence, the pattern remains the same: split your data into meaningful groups, apply analysis functions to each group, and combine the results.

:::{important} Why This Matters: Managing Large-Scale Data

Modern scientific instruments and simulations generate unprecedented data volumes. Large surveys produce:

- **Terabytes of data per night** for years of operation
- **Millions of alerts nightly** requiring real-time processing
- **Petabytes of total data** over survey lifetimes

This data avalanche makes DataFrame operations essential for processing pipelines. The ability to efficiently group, filter, and aggregate data is crucial for analyzing such massive datasets.
:::

---

## 11.4 Merging and Joining: Combining Data Sources

:::{margin}
**Join**
Combining DataFrames based on common columns or indices, essential for multi-source data analysis.
:::

### Combining Multi-Source Observations

Modern science often requires combining data from different instruments and surveys:

```python
# Optical catalog
optical_catalog = pd.DataFrame({
    'source_id': [f'SRC_{i:05d}' for i in range(1000)],
    'ra': np.random.uniform(0, 30, 1000),
    'dec': np.random.uniform(-5, 5, 1000),
    'band_a': np.random.uniform(15, 22, 1000),
    'band_b': np.random.uniform(15, 22, 1000)
})

# Infrared catalog (70% overlap with optical)
n_ir = 700
overlap_ids = np.random.choice(optical_catalog['source_id'],
                              n_ir, replace=False)

infrared_catalog = pd.DataFrame({
    'source_id': overlap_ids,
    'band_c': np.random.uniform(14, 20, n_ir),
    'band_d': np.random.uniform(13, 19, n_ir),
    'band_e': np.random.uniform(12, 18, n_ir)
})

# Merge optical and infrared data
multiwave = optical_catalog.merge(
    infrared_catalog,
    on='source_id',
    how='left'  # Keep all optical sources
)

print(f"Multi-wavelength catalog: {len(multiwave)} sources")
print(f"Sources with IR: {multiwave['band_c'].notna().sum()}")
print(multiwave.head())
```

### Different Join Types for Different Science Goals

```python
# Spectroscopic follow-up (subset of photometry)
spec_targets = np.random.choice(optical_catalog['source_id'],
                               100, replace=False)

spectroscopy = pd.DataFrame({
    'source_id': spec_targets,
    'redshift': np.random.uniform(0, 2, 100),
    'line_flux': np.random.exponential(1e-16, 100),
    'quality_flag': np.random.choice(['A', 'B', 'C'], 100)
})

# Inner join: Complete multi-wavelength + spectra
complete_data = multiwave.merge(
    spectroscopy,
    on='source_id',
    how='inner'
)
print(f"Sources with photometry + spectroscopy: {len(complete_data)}")

# Left join: All photometry, spectra where available
all_photo = multiwave.merge(
    spectroscopy,
    on='source_id',
    how='left'
)
print(f"All sources (with/without spectra): {len(all_photo)}")
print(f"Missing spectra: {all_photo['redshift'].isna().sum()}")
```

:::{warning} Debug This!: Merge Pitfalls
:class: dropdown

Find and fix the bugs in this merge operation:

```python
# BUG 1: Duplicate keys create cartesian product
df1 = pd.DataFrame({'id': [1, 1, 2], 'val': [10, 20, 30]})
df2 = pd.DataFrame({'id': [1, 2], 'data': [100, 200]})
result = df1.merge(df2, on='id')  # Creates 3 rows for id=1!

# FIX: Aggregate before merging or expect multiple matches
df1_agg = df1.groupby('id')['val'].mean().reset_index()
result_fixed = df1_agg.merge(df2, on='id')

# BUG 2: Type mismatch
df1 = pd.DataFrame({'id': ['1', '2'], 'val': [10, 20]})  # String IDs
df2 = pd.DataFrame({'id': [1, 2], 'data': [100, 200]})   # Integer IDs
result = df1.merge(df2, on='id')  # No matches!

# FIX: Ensure consistent types
df1['id'] = df1['id'].astype(int)
result_fixed = df1.merge(df2, on='id')
```
:::

---

## 11.5 Time Series and Evolution Tracking

:::{margin}
**Time Series**
Data indexed by time, essential for transient detection and simulation evolution.
:::

### Understanding Time Series in Scientific Computing

Time series data is ubiquitous in science. Every variable system has a time evolution, every simulation has timesteps, every detector produces temporal data. The challenge isn't just storing these time series—it's analyzing them efficiently to detect patterns, periodicities, and anomalies. Building on the array operations from Chapter 7 and the plotting techniques from Chapter 8, Pandas adds sophisticated time-aware functionality.

### Simulating Observational Data

To understand how to process data streams, let's simulate a simplified version of observational alerts:

```python
# Simulate nightly observations
np.random.seed(42)  # Reproducibility (Chapter 9 best practice)

# Define observation parameters
object_types = ['stable', 'variable', 'transient']
n_objects = 100
n_nights = 30
filters = ['a', 'b', 'c']  # Spectral bands

# Initialize collection list
observations = []

print("Generating mock observational data...")
```

```python
# Generate mock observations with realistic structure
for obj_id in range(n_objects):
    obj_type = np.random.choice(object_types, p=[0.7, 0.25, 0.05])
    base_value = 18.0 if obj_type == 'stable' else 19.0

    for night in range(n_nights):
        # Observe each field 2x per night in different filters
        for band in np.random.choice(filters, size=2, replace=False):
            # Simplified variability model (not physical!)
            if obj_type == 'variable':
                # Sinusoidal for simplicity
                value = base_value + 0.5 * np.sin(2 * np.pi * night / 8.3)
            elif obj_type == 'transient' and 10 < night < 20:
                # Transient event
                value = base_value - 2.0 * np.exp(-(night-15)**2/10)
            else:
                value = base_value

            # Add measurement noise
            value += np.random.normal(0, 0.05)

            observations.append({
                'object_id': f'OBJ_{obj_id:06d}',
                'time': 1000 + night + np.random.uniform(0, 0.4),
                'filter': band,
                'value': value,
                'error': 0.02 + np.random.exponential(0.01),
                'quality': np.random.lognormal(0, 0.2)
            })

obs_df = pd.DataFrame(observations)
print(f"\nGenerated {len(obs_df)} observations")
print(f"Unique objects: {obs_df['object_id'].nunique()}")
print("\nFirst few observations:")
print(obs_df.head())
```

### Finding Variables with Rolling Statistics

One of the most powerful features of Pandas for time series analysis is the ability to compute rolling (moving window) statistics. This is essential for detecting changes in behavior over time, whether you're looking for variable sources in data or numerical instabilities in simulation outputs.

```python
# Analyze variability for each object
variability_stats = obs_df.groupby('object_id').agg({
    'value': ['mean', 'std', 'count'],
    'time': ['min', 'max']
})

# Flatten multi-level column names for easier access
variability_stats.columns = ['_'.join(col).strip()
                             for col in variability_stats.columns]

# Calculate observation timespan
variability_stats['time_span'] = (
    variability_stats['time_max'] - variability_stats['time_min']
)

# Identify statistically significant variables
variability_stats['significant'] = (
    (variability_stats['value_std'] > 0.15) &
    (variability_stats['value_count'] > 10)
)

variables = variability_stats[variability_stats['significant']]
print(f"\nDetected variables: {len(variables)}/{len(variability_stats)}")
print(variables[['value_mean', 'value_std', 'time_span']].head())
```

### Tracking Energy Conservation in Dynamical Systems

Energy conservation is one of the fundamental validation tests for any dynamical simulation. In isolated systems, total energy should remain constant to within numerical precision. Systematic drift indicates problems with integration schemes, timestep choices, or force calculations.

```python
# Example energy conservation tracking structure
timesteps = np.arange(0, 1000, 10)
n_steps = len(timesteps)

# Mock energy values representing typical simulation output
energy_tracking = pd.DataFrame({
    'timestep': timesteps,
    'kinetic': 1000 + np.random.normal(0, 1, n_steps).cumsum(),
    'potential': -2000 + np.random.normal(0, 1, n_steps).cumsum()
})

# Calculate total energy and conservation metrics
energy_tracking['total'] = (
    energy_tracking['kinetic'] + energy_tracking['potential']
)
initial_energy = energy_tracking['total'].iloc[0]
energy_tracking['drift'] = energy_tracking['total'] - initial_energy
energy_tracking['relative_error'] = (
    energy_tracking['drift'] / abs(initial_energy)
)

# Find conservation violations
threshold = 1e-5  # Typical threshold
bad_steps = energy_tracking[
    abs(energy_tracking['relative_error']) > threshold
]

print(f"Energy conservation check:")
print(f"Initial E: {initial_energy:.2f}")
print(f"Max drift: {energy_tracking['drift'].abs().max():.2e}")
print(f"Violations: {len(bad_steps)} timesteps exceed threshold")

if len(bad_steps) > 0:
    print(f"\nFirst violation at timestep {bad_steps['timestep'].iloc[0]}")
```

:::{tip} Computational Thinking Box: Conservation as Validation

**PATTERN: Using Conservation Laws to Validate Simulations**

```python
def validate_simulation_run(df):
    """Check simulation validity via conservation."""

    # Energy should be conserved to machine precision
    energy_drift = (df['total_energy'].iloc[-1] -
                   df['total_energy'].iloc[0]) / df['total_energy'].iloc[0]

    # Angular momentum for isolated system
    L_drift = (df['angular_momentum'].iloc[-1] -
              df['angular_momentum'].iloc[0]) / df['angular_momentum'].iloc[0]

    return {
        'valid': abs(energy_drift) < 1e-6,
        'energy_drift': energy_drift,
        'angular_momentum_drift': L_drift
    }
```

This pattern is used in many simulation codes to validate numerical integrators.
:::

---

## 11.6 Handling Missing Data and Failed Runs

Real computational work is messy. Simulations crash due to numerical instabilities, observations fail due to conditions, instruments malfunction, and data gets corrupted. Unlike the perfect datasets in tutorials, production data has gaps, errors, and inconsistencies. Pandas provides sophisticated tools for handling these realities—tools that go far beyond the simple error checking we learned in Chapter 9.

Missing data in scientific computing has different meanings depending on context:

- **Failed convergence**: Simulation didn't reach steady state
- **Numerical overflow**: Calculation exceeded floating-point limits
- **Resource limits**: Job killed due to time/memory constraints
- **Bad data**: Measurement outside physical bounds
- **Not applicable**: Parameter combination not physical

Understanding why data is missing is crucial for deciding how to handle it:

```python
# Simulate a parameter study with realistic failure modes
np.random.seed(42)

# Generate runs with different failure patterns
run_status = []
for run_id in range(100):
    mass = np.random.choice([0.5, 1.0, 5.0, 10.0, 20.0])
    resolution = np.random.choice([32, 64, 128, 256])

    # Higher mass and resolution = higher failure probability
    failure_prob = 0.05 + 0.1 * (mass/20) + 0.1 * (resolution/256)

    if np.random.random() > failure_prob:
        # Successful run
        result = {
            'run_id': run_id,
            'mass': mass,
            'resolution': resolution,
            'converged': True,
            'final_energy': -1000 + np.random.normal(0, 10),
            'iterations': np.random.randint(1000, 5000),
            'cpu_hours': resolution**2 / 100 + np.random.exponential(1),
            'error_flag': None
        }
    else:
        # Failed run - different failure modes
        failure_mode = np.random.choice(
            ['timeout', 'diverged', 'memory', 'numerical'],
            p=[0.3, 0.3, 0.2, 0.2]
        )

        iterations = np.random.randint(0, 1000) if failure_mode != 'memory' else 0

        result = {
            'run_id': run_id,
            'mass': mass,
            'resolution': resolution,
            'converged': False,
            'final_energy': np.nan,  # No valid result
            'iterations': iterations,
            'cpu_hours': np.random.exponential(0.5),  # Failed runs end early
            'error_flag': failure_mode
        }

    run_status.append(result)

runs_df = pd.DataFrame(run_status)

# Analyze failure patterns
print(f"Simulation campaign summary:")
print(f"Total runs: {len(runs_df)}")
print(f"Successful: {runs_df['converged'].sum()} ({runs_df['converged'].mean():.1%})")
print(f"Failed: {(~runs_df['converged']).sum()}")

print(f"\nFailure analysis:")
failure_counts = runs_df[~runs_df['converged']]['error_flag'].value_counts()
for failure_type, count in failure_counts.items():
    print(f"  {failure_type}: {count} runs")

# Check if failures correlate with parameters
failure_by_params = runs_df.groupby(['mass', 'resolution'])['converged'].agg([
    'mean',  # Success rate
    'count'  # Total attempts
])
print(f"\nSuccess rate by parameters (showing worst):")
worst = failure_by_params.nsmallest(5, 'mean')
print(worst)
```

### Handling Missing Data Strategies

```python
# Different strategies for missing data

# Strategy 1: Drop failed runs
clean_runs = runs_df.dropna(subset=['final_energy'])
print(f"Clean dataset: {len(clean_runs)} runs")

# Strategy 2: Fill with defaults for specific analyses
runs_filled = runs_df.copy()
runs_filled['final_energy'] = runs_df['final_energy'].fillna(
    runs_df['final_energy'].mean()
)

# Strategy 3: Interpolate (for time series)
# Useful for occasional missing timesteps
time_data = pd.DataFrame({
    'time': range(20),
    'value': [i**2 if i % 5 != 0 else np.nan for i in range(20)]
})
time_data['interpolated'] = time_data['value'].interpolate(method='cubic')

print("\nInterpolation example:")
print(time_data[time_data['value'].isna()])
```

:::{tip} Check Your Understanding: Missing Data
:class: dropdown

Your simulation crashes at random timesteps, leaving NaN in the energy column. What's the safest approach?

a) Fill all NaN with 0
b) Fill with the mean energy
c) Drop timesteps with NaN
d) Interpolate if gaps are small, otherwise mark run as failed

**Answer:** d) Small gaps (1-2 timesteps) can be safely interpolated, but large gaps indicate serious problems. Mark runs with >5% missing data as failed and exclude from analysis. Never fill with arbitrary values that could hide physical problems!
:::

---

## 11.7 Performance Optimization

When processing large simulation outputs:

```python
# Demonstrate memory optimization
n_particles = 50000

# Unoptimized DataFrame
unoptimized = pd.DataFrame({
    'particle_id': np.arange(n_particles, dtype='int64'),
    'mass': np.random.lognormal(10, 1, n_particles).astype('float64'),
    'x': np.random.randn(n_particles).astype('float64'),
    'y': np.random.randn(n_particles).astype('float64'),
    'z': np.random.randn(n_particles).astype('float64'),
    'species': np.random.choice(['type_a', 'type_b', 'type_c'], n_particles)
})

print("Unoptimized memory usage:")
print(unoptimized.info(memory_usage='deep'))
memory_before = unoptimized.memory_usage(deep=True).sum() / 1024**2
```

```python
# Optimize data types
optimized = unoptimized.copy()

# Use smaller integer type
optimized['particle_id'] = optimized['particle_id'].astype('int32')

# Use float32 for positions (sufficient precision)
for col in ['x', 'y', 'z']:
    optimized[col] = optimized[col].astype('float32')

# Use categorical for repeated strings
optimized['species'] = optimized['species'].astype('category')

print("\nOptimized memory usage:")
print(optimized.info(memory_usage='deep'))
memory_after = optimized.memory_usage(deep=True).sum() / 1024**2

print(f"\nMemory reduction: {memory_before:.1f} MB -> {memory_after:.1f} MB")
print(f"Savings: {(1 - memory_after/memory_before)*100:.1f}%")
```

### Using NumPy for Numerical Operations

While Pandas excels at data organization and high-level operations, NumPy remains superior for pure numerical computation. The key is knowing when to extract NumPy arrays from DataFrames for computational efficiency:

```python
import time

# Compare Pandas vs NumPy for numerical operations
n_particles = 10000
particles = pd.DataFrame({
    'x': np.random.randn(n_particles),
    'y': np.random.randn(n_particles),
    'z': np.random.randn(n_particles),
})

# Method 1: Pandas column operations
start = time.time()
for _ in range(100):
    r_pandas = np.sqrt(
        particles['x']**2 +
        particles['y']**2 +
        particles['z']**2
    )
time_pandas = time.time() - start

# Method 2: Extract NumPy array first
positions = particles[['x', 'y', 'z']].values  # Convert to NumPy
start = time.time()
for _ in range(100):
    r_numpy = np.linalg.norm(positions, axis=1)
time_numpy = time.time() - start

# Method 3: Direct array access (fastest)
start = time.time()
for _ in range(100):
    r_direct = np.sqrt(
        particles['x'].values**2 +
        particles['y'].values**2 +
        particles['z'].values**2
    )
time_direct = time.time() - start

print(f"Performance comparison (100 iterations):")
print(f"Pandas columns: {time_pandas*1000:.1f} ms")
print(f"NumPy norm: {time_numpy*1000:.1f} ms")
print(f"Direct arrays: {time_direct*1000:.1f} ms")
print(f"\nSpeedup NumPy vs Pandas: {time_pandas/time_numpy:.1f}x")
print(f"Speedup direct vs Pandas: {time_pandas/time_direct:.1f}x")

# Verify results are identical (Chapter 9: validation)
assert np.allclose(r_pandas.values, r_numpy)
assert np.allclose(r_pandas.values, r_direct)
print("\n✓ All methods produce identical results")
```

The lesson here is clear: use Pandas for data management and selection, but extract NumPy arrays for intensive calculations. This is especially important in hot loops—code that executes millions of times in your simulation.

---

## 11.8 Input/Output: Managing Simulation Data

DataFrames support numerous file formats, each with specific advantages for different scientific workflows. Building on the file I/O concepts from Chapter 5, Pandas adds high-level functions that handle complex data structures automatically. The choice of format depends on your specific needs: human readability, storage efficiency, type preservation, or compatibility with other tools.

Understanding format trade-offs is crucial for computational workflows:

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| CSV | Sharing with collaborators | Human readable, universal | No type info, large files |
| HDF5 | Large simulation outputs | Fast, compressed, preserves types | Binary, needs library |
| Pickle | Python-only workflows | Perfect preservation | Python-specific, version sensitive |
| Parquet | Big data analysis | Columnar, compressed, typed | Requires special tools |
| Excel | Non-programmers | Familiar interface | Size limits, slow |
| JSON | Web APIs, config files | Human readable, structured | Verbose, no binary data |

Let's explore these formats with a realistic example:

```python
# Create example simulation results to save
sim_results = pd.DataFrame({
    'run_id': [f'RUN_{i:04d}' for i in range(10)],
    'model_type': ['TypeA']*5 + ['TypeB']*5,
    'param_a': [0.3]*5 + [0.31]*5,
    'param_b': np.random.normal(0.81, 0.02, 10),
    'chi_squared': np.random.uniform(0.8, 2.5, 10),
    'converged': [True]*8 + [False]*2,
    'cpu_hours': np.random.uniform(100, 500, 10),
    'completion_date': pd.date_range('2024-01-01', periods=10, freq='D')
})

print("Simulation results to save:")
print(sim_results)
print(f"\nData types (note datetime):")
print(sim_results.dtypes)
```

Now let's save in different formats and understand the implications:

```python
# CSV - Human readable, git-friendly
# Good for: Small datasets, sharing, version control
sim_results.to_csv('simulation_results.csv', index=False)
csv_size = len(sim_results.to_csv(index=False).encode('utf-8'))
print(f"CSV format: {csv_size} bytes")
print("✓ Human readable, can diff in git")
print("✗ Loses type information (dates become strings)")

# HDF5 - Efficient for large datasets
# Good for: Checkpoint files, large arrays, hierarchical data
sim_results.to_hdf('simulation_results.h5', key='runs', mode='w')
print("\n✓ HDF5: Fast I/O, preserves all types, supports compression")
print("✓ Can store multiple DataFrames in one file")
print("✗ Binary format, needs HDF5 libraries")

# Pickle - Perfect Python preservation
# Good for: Intermediate results, Python-only pipelines
sim_results.to_pickle('simulation_results.pkl')
print("\n✓ Pickle: Preserves everything perfectly")
print("✗ Python-specific, can break between versions")

# JSON - Web and configuration friendly
# Good for: APIs, configuration, JavaScript interop
json_str = sim_results.to_json(orient='records', indent=2,
                               date_format='iso')
print("\n✓ JSON: Human readable, web-friendly")
print("✗ Verbose, limited type support")
print(f"First record in JSON:\n{json_str[:200]}...")
```

For publication tables, LaTeX export is invaluable:

```python
# LaTeX for publications
# Select subset of columns for paper
table_data = sim_results[['run_id', 'param_a', 'param_b', 'chi_squared']]

latex_table = table_data.head(5).to_latex(
    index=False,
    float_format='%.3f',
    column_format='lccc',  # Left, center, center, center alignment
    caption='Simulation parameters and goodness of fit.',
    label='tab:sim_params',
    position='htbp'
)

print("LaTeX table for paper:")
print(latex_table)
```

### Chunked I/O for Large Files

Real simulation outputs often exceed available RAM. A single simulation snapshot might be 100 GB, a full dataset could be terabytes. Pandas handles this through chunked processing—reading and processing data in manageable pieces:

```python
def process_large_simulation(filename, chunksize=10000):
    """
    Process large simulation output in chunks.

    This pattern is used for:
    - Multi-GB checkpoint files
    - Catalogs with billions of objects
    - Time series with millions of timesteps
    """

    # Initialize accumulators
    running_stats = {
        'mean_energy': 0,
        'n_chunks': 0,
        'total_rows': 0,
        'min_energy': float('inf'),
        'max_energy': float('-inf')
    }

    # In practice, you'd read an actual file:
    # for chunk in pd.read_csv(filename, chunksize=chunksize):

    # Simulate chunked processing
    print(f"Processing file in chunks of {chunksize} rows...")

    # Mock processing 3 chunks
    for i in range(3):
        # Simulate a chunk of data
        chunk = pd.DataFrame({
            'timestep': range(i*chunksize, (i+1)*chunksize),
            'energy': np.random.normal(-1000, 50, chunksize),
            'momentum': np.random.normal(0, 10, chunksize)
        })

        # Process this chunk
        chunk_mean = chunk['energy'].mean()
        chunk_min = chunk['energy'].min()
        chunk_max = chunk['energy'].max()

        # Update running statistics
        running_stats['mean_energy'] += chunk_mean
        running_stats['n_chunks'] += 1
        running_stats['total_rows'] += len(chunk)
        running_stats['min_energy'] = min(running_stats['min_energy'], chunk_min)
        running_stats['max_energy'] = max(running_stats['max_energy'], chunk_max)

        # Check for problems in this chunk
        if chunk_min < -1200:  # Unphysical energy
            print(f"  Warning: Unphysical energy in chunk {i}")

        print(f"  Processed chunk {i+1}: {len(chunk)} rows")

    # Finalize statistics
    running_stats['mean_energy'] /= running_stats['n_chunks']

    print(f"\nProcessing complete:")
    print(f"  Total rows: {running_stats['total_rows']:,}")
    print(f"  Energy range: [{running_stats['min_energy']:.1f}, "
          f"{running_stats['max_energy']:.1f}]")

    return running_stats

# Demonstrate the pattern
stats = process_large_simulation('mock_file.csv', chunksize=5000)

print("\n This pattern scales to arbitrarily large files!")
```

The chunked processing pattern is fundamental for production scientific computing. It allows you to:

- Process files larger than RAM
- Show progress during long operations
- Fail gracefully if corruption is detected
- Parallelize by processing chunks on different cores

---

## Main Takeaways

This chapter has transformed you from manually managing arrays and writing error-prone bookkeeping code to elegantly organizing complex computational data with Pandas DataFrames. You've learned that DataFrames aren't just convenient—they're essential for maintaining data integrity when dealing with parameter studies, convergence tests, and multi-physics simulations. The shift from procedural data handling to declarative data transformations represents a fundamental upgrade in how computational scientists approach data analysis.

**DataFrames as Scientific Infrastructure**: You now understand that DataFrames provide the organizational backbone for modern computational science. Rather than parallel arrays that can silently desynchronize or manual struct management requiring constant vigilance, DataFrames keep related quantities together with meaningful labels. This prevents the index-mismatch bugs that have plagued scientific computing for decades while making your analysis code self-documenting through descriptive column names and indices.

**Indexing for Computational Workflows**: You've mastered Pandas' dual indexing system—labels for identifying specific models or parameter combinations, positions for algorithmic operations. Label-based indexing ensures you analyze the right simulation even after sorting or filtering, while boolean masking enables complex selection criteria that would require nested loops in traditional approaches. This is crucial when selecting converged runs, filtering physical parameter ranges, or identifying numerical instabilities.

**GroupBy for Parameter Studies**: The split-apply-combine paradigm has revolutionized how you analyze parameter dependencies. Instead of writing nested loops to process subsets—prone to errors and slow to execute—you express your intent declaratively: "group by resolution and compute convergence rates." This mental model makes complex analyses like comparing ensemble statistics or tracking convergence across parameter spaces both conceptually clear and computationally efficient.

**Merging Multi-Physics Outputs**: You've learned to combine outputs from different simulation codes—hydrodynamics from one solver, chemistry from another, radiation from a third. Understanding join semantics (inner, outer, left) lets you control exactly how modules combine, preserving all data or focusing on overlaps as physics requires. This is essential for modern multi-scale, multi-physics simulations.

**Time Series for Evolution Tracking**: Pandas' time series capabilities—rolling windows, resampling, datetime indexing—provide sophisticated tools for analyzing simulation evolution. Whether tracking energy conservation through millions of timesteps, detecting numerical instabilities, or analyzing orbital evolution, you can now handle non-uniform outputs and compute diagnostic statistics efficiently.

**Performance for Production Runs**: You've learned that while Pandas provides convenient high-level operations, performance matters for large simulations. Using appropriate dtypes, leveraging NumPy for numerics, and processing in chunks makes the difference between analyses that complete in seconds versus hours—critical when processing terabyte-scale simulation outputs.

The overarching insight is that Pandas provides a computational framework that matches how scientists think about simulation data. Instead of low-level array manipulation, you express high-level scientific intent: "find runs where energy is conserved" or "compute statistics for each parameter combination." This isn't just syntactic sugar—it reduces bugs, improves reproducibility, and lets you focus on physics rather than bookkeeping.

---

## Definitions

**Aggregation**: Combining multiple values into summary statistics using functions like mean, std, or custom operations.

**Boolean masking**: Filtering DataFrame rows using conditional expressions that return True/False arrays for selection.

**Categorical dtype**: Memory-efficient type for columns with repeated values, crucial for large simulation metadata.

**Chunking**: Processing large files in pieces to handle datasets exceeding available RAM.

**Convergence**: Systematic improvement of numerical accuracy with increasing resolution or smaller timesteps.

**DataFrame**: Two-dimensional labeled data structure organizing heterogeneous typed columns with a shared index.

**GroupBy**: Split-apply-combine operation partitioning data by values, applying functions, and combining results.

**HDF5**: Hierarchical Data Format optimized for large scientific datasets, preserving types and supporting compression.

**Index**: Row labels providing O(1) lookup time and automatic alignment in operations between DataFrames.

**Inner join**: Merge keeping only rows with matching keys in both DataFrames.

**Left join**: Merge keeping all rows from left DataFrame, filling missing right values with NaN.

**Loc**: Label-based accessor for selecting DataFrame elements by index and column names.

**Iloc**: Integer position-based accessor for selecting DataFrame elements by numerical position.

**Merge**: Combining DataFrames based on common columns, essential for multi-physics outputs.

**MultiIndex**: Hierarchical indexing for representing multi-dimensional parameter spaces.

**NaN**: Not a Number, representing missing/failed values in numerical computations.

**Rolling window**: Moving window for computing statistics over time series, useful for stability analysis.

**Series**: One-dimensional labeled array, essentially a single DataFrame column with an index.

**SettingWithCopyWarning**: Warning preventing silent corruption from modifying DataFrame views.

**Time series**: Data indexed by temporal values, essential for tracking simulation evolution.

**Vectorization**: Applying operations to entire columns simultaneously rather than iterating over rows.

---

## Key Takeaways

- **DataFrames organize simulation outputs** — Keep parameters, results, and metadata together with meaningful labels

- **Label-based indexing ensures correctness** — Access data by physical meaning, not fragile integer positions

- **GroupBy enables parameter study analysis** — Analyze dependencies without writing error-prone loops

- **Merging combines multi-physics results** — Join outputs from different codes while controlling data preservation

- **Time series tools track evolution** — Monitor conservation, detect instabilities, analyze dynamics

- **Handle failures explicitly** — Track and manage failed runs, missing timesteps, numerical problems

- **Optimize memory for large outputs** — Use appropriate dtypes, chunk processing for TB-scale data

- **Leverage NumPy for numerics** — Extract arrays for computational performance in hot loops

- **Chain operations for clarity** — Express complex analyses as readable transformation pipelines

- **Choose formats purposefully** — HDF5 for large data, CSV for sharing, pickle for complete preservation

---

## Quick Reference Tables

### Essential DataFrame Operations

| Operation | Method | Simulation Example |
|-----------|--------|-------------------|
| Create from results | `pd.DataFrame()` | `df = pd.DataFrame(simulation_outputs)` |
| Select parameters | `df['column']` | `masses = df['mass']` |
| Filter converged | `df.loc[]` | `df.loc[df['converged'] == True]` |
| Add derived quantity | Assignment | `df['virial'] = df['KE'] / df['PE']` |
| Drop failed runs | `df.dropna()` | `df.dropna(subset=['energy'])` |
| Sort by error | `df.sort_values()` | `df.sort_values('energy_error')` |

### GroupBy for Parameter Studies

| Function | Purpose | Example |
|----------|---------|---------|
| `mean()` | Average across runs | `df.groupby('n_particles')['error'].mean()` |
| `std()` | Scatter between runs | `df.groupby('resolution')['energy'].std()` |
| `agg()` | Multiple statistics | `.agg(['mean', 'std', 'min', 'max'])` |
| `transform()` | Normalize by group | `.transform(lambda x: x / x.mean())` |
| `apply()` | Custom convergence test | `.apply(check_convergence)` |

### Join Types for Multi-Physics

| Join Type | Use Case | Physics Example |
|-----------|----------|-----------------|
| `inner` | Both codes succeeded | Hydro + Chemistry cells |
| `left` | Primary + optional | All particles + tagged subset |
| `outer` | Complete picture | All cells from all modules |
| `merge` | By common ID | Combine by particle_id |

### Performance Optimization

| Technique | Purpose | Example |
|-----------|---------|---------|
| Dtype optimization | Reduce memory | `astype('float32')` for positions |
| Categorical | Repeated strings | `astype('category')` for species |
| Chunking | Large files | `pd.read_csv(chunksize=10000)` |
| NumPy operations | Speed numerics | `df.values` for computation |
| HDF5 storage | Fast I/O | `to_hdf()` with compression |

---

## Next Chapter Preview

With Pandas providing the organizational foundation for your computational data, the next modules introduce more advanced scientific computing topics. You'll learn to solve differential equations, integrate complex systems, optimize model parameters to match observations, and analyze signals from time-varying phenomena. The DataFrames you've mastered will organize inputs and outputs, tracking which parameters yield stable solutions, storing optimization trajectories, and managing results from numerical experiments. This combination of tools will transform you from writing basic analysis scripts to building sophisticated computational pipelines capable of tackling real research problems!

## Resources for Continued Learning

### Essential References

**Official Pandas Documentation**: <https://pandas.pydata.org/docs/>

- User Guide for conceptual understanding
- API Reference for detailed function documentation
- "10 Minutes to Pandas" quickstart tutorial
- Cookbook with practical recipes

**Performance Optimization**:

- <https://pandas.pydata.org/docs/user_guide/enhancingperf.html>
- Critical for processing large datasets
- Covers Cython, Numba, and parallel processing

### Books for Deep Learning

- **"Python for Data Analysis" by Wes McKinney** (Pandas creator) - The definitive guide
- **"Effective Pandas" by Matt Harrison** - Advanced patterns and best practices
- **"Pandas Cookbook" by Theodore Petrou** - Practical recipes for common tasks

### Performance and Scaling

When DataFrames aren't enough:

- **Dask**: <https://docs.dask.org/> - Parallel computing, larger-than-memory datasets
- **Vaex**: <https://vaex.io/> - Billion-row catalogs
- **Polars**: <https://pola.rs/> - Rust-based, extremely fast DataFrame library
- **Ray**: <https://www.ray.io/> - Distributed computing for ML pipelines

### Troubleshooting and Community

- **Stack Overflow pandas tag**: <https://stackoverflow.com/questions/tagged/pandas>
- **Common Gotchas**: <https://pandas.pydata.org/docs/user_guide/gotchas.html>
- **PyData Community**: <https://pydata.org/>

### Quick Reference Bookmarks

Save these for daily use:

1. **Indexing and Selection**: <https://pandas.pydata.org/docs/user_guide/indexing.html>
2. **GroupBy Guide**: <https://pandas.pydata.org/docs/user_guide/groupby.html>
3. **Merge/Join/Concat**: <https://pandas.pydata.org/docs/user_guide/merging.html>
4. **Time Series**: <https://pandas.pydata.org/docs/user_guide/timeseries.html>
5. **IO Tools**: <https://pandas.pydata.org/docs/user_guide/io.html>

**Remember:** The Pandas documentation is exceptionally well-written. When in doubt, check the official docs first — they often have exactly the example you need.
