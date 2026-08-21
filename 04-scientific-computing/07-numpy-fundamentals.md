---
title: "Chapter 7: NumPy Arrays for Scientific Reasoning"
subtitle: "Shapes, dtypes, and operations that make numerical assumptions inspectable"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

## Learning objectives

By the end of this chapter, you will be able to:

- [ ] **(1) Create and manipulate NumPy arrays** for efficient numerical computation
- [ ] **(2) Apply vectorized operations** to express repeated numerical operations clearly
- [ ] **(3) Master array indexing, slicing, boolean masking, and broadcasting** for sophisticated data manipulation
- [ ] **(4) Use essential NumPy functions** for scientific computing (`linspace`, `logspace`, `where`, `meshgrid`)
- [ ] **(5) Perform array transformations** including reshaping, stacking, and splitting for data analysis
- [ ] **(6) Generate and apply random numbers** from various distributions for Monte Carlo simulations
- [ ] **(7) Apply NumPy to real scientific calculations** with proper unit conversions and unit-aware variable names
- [ ] **(8) Recognize when and why to use NumPy** instead of pure Python for numerical tasks

## Prerequisites

Before starting this chapter, verify you can:

- [ ] Work with Python lists and list comprehensions (Chapter 4)
- [ ] Use the math module for mathematical operations (Chapter 2)
- [ ] Understand functions and return values (Chapter 5)
- [ ] Work with nested data structures (Chapter 4)
- [ ] Import and use modules (Chapter 5)

### Self-Assessment Diagnostic

Test your readiness by predicting these outputs WITHOUT running the code:

```python
# Question 1: What does this produce?
result = [x**2 for x in range(5) if x % 2 == 0]
# Your answer: _______

# Question 2: What's the final value of total?
total = sum([len(str(x)) for x in [10, 100, 1000]])
# Your answer: _______

# Question 3: What error (if any) occurs here?
import math
values = [1, 4, 9]
# roots = math.sqrt(values)  # Uncomment to test
# Your answer: _______

# Question 4: Can you understand this nested structure?
matrix = [[1, 2], [3, 4]]
flattened = [item for row in matrix for item in row]
# Your answer: _______
```

:::{tip} Self-Assessment Answers
:class: dropdown

1. `[0, 4, 16]` - squares of even numbers from 0-4
2. `9` - lengths are 2, 3, 4, sum = 9
3. `TypeError` - math.sqrt() doesn't accept lists, only single values
4. `[1, 2, 3, 4]` - flattens the 2D list into 1D

If you got all four correct, you're ready for NumPy! If not, review the indicated chapters.
:::

---

## Why this chapter matters

You've been using Python lists to store collections of numbers, and the math module to perform calculations. But what happens when you need to analyze a million stellar spectra, each with thousands of wavelength points? Or when you need to perform the same calculation on every pixel in a telescope image? Try using a list comprehension on a million-element list, and you'll be waiting a while. This is where NumPy transforms Python from a general-purpose language into a powerhouse for scientific computing, providing the speed and tools necessary for research-grade computational science.

**NumPy**, short for Numerical Python, is the foundation upon which the entire scientific Python ecosystem is built. Every plot you'll make with Matplotlib, every optimization you'll run with SciPy, every dataframe you'll analyze with Pandas – they all build on NumPy arrays. But NumPy isn't just about speed; it's about expressing mathematical operations naturally. Instead of writing loops to add corresponding elements of two lists, you simply write `a + b`. Instead of nested loops for matrix multiplication, you write `a @ b`. This isn't just convenience – it's a fundamental shift in how you think about numerical computation, from operating on individual elements to operating on entire arrays at once.

This chapter introduces you to NumPy's ndarray (n-dimensional array), the object that makes scientific Python possible. You'll discover why NumPy arrays are often much faster than Python lists for numerical operations, and how **vectorization** eliminates the need for most explicit loops. You'll master **broadcasting**, NumPy's powerful mechanism for operating on arrays of different shapes, which enables elegant solutions to complex problems. Most importantly, you'll learn to think in arrays – a skill that transforms you from someone who writes code that processes data to someone who writes code that expresses mathematical ideas directly. The examples lean astro‑flavored, but the patterns apply just as well to climate, biology, imaging, and signal processing.

:::{important} 📚 Essential Resource: NumPy Documentation

This chapter introduces NumPy's core concepts, but NumPy is vast! The official documentation at **https://numpy.org/doc/stable/** is your indispensable companion. Throughout your career, you'll constantly reference it for:

- Complete function signatures and parameters
- Advanced broadcasting examples
- Performance optimization tips
- Specialized submodules (random, fft, linalg)

**Practice using the documentation NOW**: After each new function you learn, look it up in the official docs. Read the parameters, check the examples, and explore related functions. The ability to efficiently navigate documentation is as important as coding itself. Bookmark the NumPy documentation – you'll use it daily in research!

**Pro tip:** Use the NumPy documentation's search function to quickly find what you need. Type partial function names or concepts, and it will suggest relevant pages. The "See Also" sections are goldmines for discovering related functionality.
:::

---

## 7.1 From Lists to Arrays: Why NumPy?

:::{margin}
**NumPy**
A fundamental package for scientific computing in Python, providing support for large, multi-dimensional arrays and matrices.
:::

:::{margin}
**ndarray**
NumPy's n-dimensional array object, the core data structure for numerical computation.
:::

:::{margin}
**Contiguous Memory**
Data stored in adjacent memory locations, enabling fast access and cache efficiency.
:::

Let's start with a problem you already know how to solve, then see how NumPy transforms it. Imagine you're analyzing brightness measurements from a variable star:

```{code-cell} python
import time
import math

# Python list approach (what you know from Chapter 4)
magnitudes_list = [12.3, 12.5, 12.4, 12.7, 12.6] * 20000  # 100,000 measurements
fluxes = []

start = time.perf_counter()
for mag in magnitudes_list:
    flux = 10**(-mag/2.5)  # Convert magnitude to relative flux
    fluxes.append(flux)
list_time = time.perf_counter() - start

print(f"List approach: {list_time*1000:.2f} ms")
print(f"First 5 fluxes: {fluxes[:5]}")
```

Now let's see the NumPy approach:

```{code-cell} python
import time
import numpy as np  # Standard abbreviation used universally

# NumPy array approach (what you're learning)
magnitudes = np.array([12.3, 12.5, 12.4, 12.7, 12.6] * 20000)

start = time.perf_counter()
fluxes_np = 10**(-magnitudes/2.5)  # Operates on entire array at once!
numpy_time = time.perf_counter() - start

print(f"NumPy approach: {numpy_time*1000:.2f} ms")
print(f"Speedup: {list_time/numpy_time:.1f}x faster")
print(f"First 5 fluxes: {fluxes_np[:5]}")
```

The NumPy version is not only faster but also cleaner – no explicit loop needed! This is called **vectorization**, and it's the key to NumPy's power.

### NumPy vs. the math Module: Arrays vs. Scalars

You've been using the math module for operations like `math.sin()`, `math.sqrt()`, and `math.log()`. NumPy covers most of the same operations while adding array support, which is why it becomes the default tool in scientific computing:

```python
# Math module - works on single values only
import math
x = 2.0
math_result = math.sin(x)
print(f"math.sin({x}) = {math_result}")

# Try with a list - this fails!
# values = [0, 1, 2, 3]
# math.sin(values)  # TypeError!

# NumPy - works on single values AND arrays
x = 2.0
numpy_scalar_result = np.sin(x)
print(f"np.sin({x}) = {numpy_scalar_result}")

# NumPy shines with arrays
values = np.array([0, 1, 2, 3])
numpy_array_result = np.sin(values)
print(f"np.sin({values}) = {numpy_array_result}")

# NumPy has everything math has (and more)
print(f"\nComparison for x = {x}:")
print(f"  math.sqrt({x}) = {math.sqrt(x):.6f}")
print(f"  np.sqrt({x})   = {np.sqrt(x):.6f}")
print(f"  math.exp({x})  = {math.exp(x):.6f}")
print(f"  np.exp({x})    = {np.exp(x):.6f}")
print(f"  math.log10({x}) = {math.log10(x):.6f}")
print(f"  np.log10({x})   = {np.log10(x):.6f}")
```

**Key insight**: For arrays, prefer NumPy. For scalar-only work, `math` is perfectly fine. A few specialized functions live in `math` or `scipy.special`, so use the tool that matches the problem.

:::{note} Quick Check

You need square roots for a single number and for a whole array. Which module would you use for each, and why?
:::

:::{note} 🎯 The More You Know: NumPy Powers Gravitational Wave Detection
:class: dropdown

In the mid-2010s, the Laser Interferometer Gravitational-Wave Observatory (LIGO) detected gravitational waves for the first time, opening a new window on the universe. This discovery depended on sophisticated data analysis pipelines, including PyCBC, which relies heavily on NumPy.

Astro example — the same signal‑processing workflow appears in seismology, acoustics, and medical imaging.

LIGO's detectors produce high-rate, noisy data streams. Detecting a gravitational wave requires comparing those streams against large banks of theoretical waveform templates using matched filtering — a computationally intensive process that would be impossible without efficient numerical libraries.

The PyCBC pipeline is built on NumPy arrays and operations. The power of NumPy's vectorized operations, which call optimized compiled routines (often BLAS/LAPACK; FFT via optimized routines), enables the analysis of gravitational wave data at practical timescales. Here's how NumPy transforms the core matched filtering operation:

```python
# Traditional loop-based approach
def matched_filter_slow(data, template):
    result = 0
    for i in range(len(data)):
        result += data[i] * template[i]
    return result

# NumPy vectorized approach
def matched_filter_fast(data, template):
    return np.dot(data, template)  # Or simply: data @ template
```

The vectorized NumPy version is dramatically faster, enabling searches through large template banks. NumPy's FFT implementation accelerates the frequency-domain operations that are central to the analysis.

Today, gravitational-wave detections are processed through analysis pipelines built on NumPy arrays. The library you're learning provides the computational foundation for this new kind of astronomy.
:::

---

## 7.2 Creating Arrays: Your Scientific Data Containers

:::{margin}
**dtype**
Data type of array elements, controlling memory usage and precision.
:::

NumPy provides many ways to create arrays, each suited for different scientific tasks:

```python
# From Python lists (most common starting point)
measurements = [23.5, 24.1, 23.8, 24.3]
arr = np.array(measurements)
print(f"From list: {arr}, dtype: {arr.dtype}")

# Specify data type for memory efficiency
counts = np.array([1000, 2000, 1500], dtype=np.int32)
print(f"Integer array: {counts}, dtype: {counts.dtype}")

# 2D array (matrix) - like an image
image_data = np.array([[10, 20, 30],
                       [40, 50, 60],
                       [70, 80, 90]])
print(f"2D array shape: {image_data.shape}")
print(f"2D array:\n{image_data}")
```

### Essential Array Creation Functions for Science

:::{margin}
**CGS Units**
Centimeter-Gram-Second system, traditionally used in astronomy and astrophysics.
:::

These functions are workhorses in scientific computing:

Unit clarity matters: even without a units library, include units in variable names (e.g., `wavelengths_nm`, `mass_g`) and stay consistent within a workflow.

```python
# linspace: Evenly spaced values (inclusive endpoints)
# Perfect for wavelength grids, time series
wavelengths_nm = np.linspace(400, 700, 11)  # 11 points from 400 to 700 nm
print(f"Wavelengths (nm): {wavelengths_nm}")

# Convert to CGS (cm) - standard in stellar atmosphere models
wavelengths_cm = wavelengths_nm * 1e-7
print(f"Wavelengths (cm): {wavelengths_cm}")

# logspace: Logarithmically spaced values
# Essential for frequency grids, stellar masses
masses_solar = np.logspace(-1, 2, 4)  # 0.1 to 100 solar masses
masses_g = masses_solar * 1.989e33  # Convert to grams (CGS)
print("Stellar masses (g):", ", ".join(f"{x:.2e}" for x in masses_g))
```

```python
# arange: Like Python's range but returns array
times_s = np.arange(0, 10, 0.1)  # 0 to 9.9 in 0.1s steps
print(f"Time points: {len(times_s)} samples from {times_s[0]} to {times_s[-1]}")

# zeros and ones: Initialize arrays
dark_frame = np.zeros((100, 100))  # 100x100 CCD dark frame
flat_field = np.ones((100, 100))   # Flat field (perfect response)
print(f"Dark frame shape: {dark_frame.shape}, sum: {dark_frame.sum()}")
print(f"Flat field shape: {flat_field.shape}, sum: {flat_field.sum()}")

# full: Create array filled with specific value
bias_level = np.full((100, 100), 500)  # CCD bias level
print(f"Bias array: all values = {bias_level[0, 0]}")

# eye: Identity matrix
identity = np.eye(3)
print(f"Identity matrix:\n{identity}")
```

:::{tip} 💡 Computational Thinking Box: Row-Major vs Column-Major

**PATTERN: Memory Layout Matters for Performance**

NumPy stores arrays in row-major order (C-style) by default, meaning elements in the same row are adjacent in memory. This affects performance dramatically:

```python
# Row-major (NumPy default) - fast row operations
image = np.zeros((1000, 1000))
# Accessing image[0, :] is fast (contiguous memory)
# Accessing image[:, 0] is slower (strided memory)

# For column operations, consider Fortran order
image_fortran = np.zeros((1000, 1000), order='F')
# Now image_fortran[:, 0] is fast
```

Why this matters:

- Processing images row-by-row? Use default (C-order)
- Processing spectra in columns? Consider Fortran order
- Matrix multiplication? NumPy optimizes automatically

Real impact: The wrong memory order can make your code noticeably slower for large arrays!
:::

::::{note} 🔍 Check Your Understanding

What's the memory difference between `np.zeros(1000)`, `np.ones(1000)`, and `np.empty(1000)`? When would you use each?

:::{tip} Answer
:class: dropdown

All three allocate the same amount of memory (8000 bytes for float64), but:

- `np.zeros()`: Allocates AND sets all values to 0 (slower, safe)
- `np.ones()`: Allocates AND sets all values to 1 (slower, safe)
- `np.empty()`: Only allocates, doesn't initialize (fastest, dangerous)

Use cases:

- `zeros()/ones()`: When you need initialized values for accumulation or defaults
- `empty()`: ONLY when you'll immediately overwrite ALL values, like filling with calculated results

Example where `empty()` is appropriate:

```python
result = np.empty(1000)
for i in range(1000):
    result[i] = expensive_calculation(i)  # Overwrites immediately
```
:::
::::

### Saving and Loading Arrays

This section introduces NumPy's array-specific storage operations locally. They
are useful when a calculation needs to preserve values, shape, and dtype
together:

```python
import os  # For cleanup
rng = np.random.default_rng(42)

# Save astronomical data in binary format
flux_data = rng.normal(1000, 50, size=1000)
np.save('observations.npy', flux_data)  # Binary format, fast

# Load for analysis
loaded_data = np.load('observations.npy')
print(f"Loaded {len(loaded_data)} measurements")

# For text format (human-readable but slower)
np.savetxt('observations.txt', flux_data[:10], fmt='%.2f')
text_data = np.loadtxt('observations.txt')
print(f"Text file sample: {text_data[:3]}")

# Clean up files
os.remove('observations.npy')
os.remove('observations.txt')
```

---

## 7.3 Random Numbers for Monte Carlo Simulations

:::{margin}
**Monte Carlo**
A computational technique using random sampling to solve problems that might be deterministic in principle.
:::

Scientific computing often requires random data for **Monte Carlo** simulations, noise modeling, and statistical testing. NumPy's random module provides a comprehensive suite of distributions essential for computational astrophysics:

:::{note} Note on Reproducibility

Random number generation can produce slightly different values across NumPy versions and hardware architectures, even with the same seed. The statistical properties remain consistent, but exact values may vary. For reproducible workflows, use the `np.random.Generator` interface (`default_rng`) and record both your NumPy version and the bit generator (`rng.bit_generator`).
:::

Legacy `np.random.*` functions still exist, but they rely on global state. In new scientific code, prefer a local generator created with `np.random.default_rng(...)`.

### Common Distributions

The three distributions you'll use most frequently are **uniform**, **normal (Gaussian)**, and **Poisson**. Master these first before moving to specialized distributions.

#### Uniform Distribution

Use for random positions, phases, and any quantity that's equally likely across a range:

```{code-cell} python
import numpy as np

# Create a local Generator for reproducibility without global state
rng = np.random.default_rng(42)

# Uniform distribution: random positions, phases
# Generate random sky coordinates uniformly on the sphere
n_stars = 1000
ra = rng.uniform(0, 360, n_stars)  # Right Ascension in degrees
u = rng.uniform(-1, 1, n_stars)  # Uniform in sin(dec), not in dec
dec = np.degrees(np.arcsin(u))  # Declination in degrees
print(f"Generated {n_stars} random sky positions")
print(f"RA range: [{ra.min():.1f}, {ra.max():.1f}] deg")

# Random phases for periodic variables
phases = rng.uniform(0, 2*np.pi, n_stars)
print(f"Phase range: [0, 2pi]")

# Shorthand for uniform [0, 1)
random_fractions = rng.random(5)
print(f"Random fractions: {random_fractions}")
```

Uniform sky coverage is a subtle but important point: equal-area sampling on a sphere means uniform in $\sin(\mathrm{dec})$, not uniform in declination itself. Sampling dec uniformly would over-weight the poles.

#### Normal (Gaussian) Distribution

Use for measurement errors, thermal noise, and any quantity resulting from many small independent effects:

```{code-cell} python
# Normal (Gaussian) distribution: measurement errors, thermal noise
# Simulate CCD readout noise
rng = np.random.default_rng(42)
mean_counts = 1000  # electrons
read_noise = 10  # electrons RMS
n_pixels = 10000

pixel_values = rng.normal(mean_counts, read_noise, n_pixels)
print(f"Pixel statistics:")
print(f"  Mean: {pixel_values.mean():.1f} (expected: {mean_counts})")
print(f"  Std: {pixel_values.std():.1f} (expected: {read_noise})")
print(f"  SNR: {pixel_values.mean()/pixel_values.std():.1f}")

# Shorthand for standard normal (mean=0, std=1)
standard_normal = rng.standard_normal(5)
print(f"Standard normal samples: {standard_normal}")
```

#### Poisson Distribution

Use for counting statistics—photon counting, radioactive decay, or any discrete events occurring at a constant average rate:

```{code-cell} python
# Poisson distribution: photon counting, radioactive decay
# Simulate photon arrival statistics
rng = np.random.default_rng(42)
mean_photons = 100  # photons per exposure
n_exposures = 1000

photon_counts = rng.poisson(mean_photons, n_exposures)
print(f"Photon counting statistics:")
print(f"  Mean: {photon_counts.mean():.1f} (expected: {mean_photons})")
print(f"  Std: {photon_counts.std():.2f} (expected: {np.sqrt(mean_photons):.2f})")
print(f"  Variance/Mean: {photon_counts.var()/photon_counts.mean():.2f} (should be ~1)")
```

:::{tip} When to Use Each Distribution

| Distribution | Use When | Scientific Examples |
|-------------|----------|---------------------|
| **Uniform** | All values equally likely | Random phases, sky positions, initial conditions |
| **Normal** | Many small effects combine | Measurement errors, thermal noise, stellar velocities |
| **Poisson** | Counting discrete events | Photon counts, particle detections, cosmic ray hits |
:::

### Advanced Distributions for Astrophysics

These distributions are less common but essential for specific astrophysical applications.

#### Exponential Distribution

Use for waiting times between events (time to next supernova, time between cosmic ray hits):

```{code-cell} python
# Exponential distribution: time between events, decay processes
# Simulate time between supernova detections (days)
rng = np.random.default_rng(42)
mean_interval = 30  # days
n_events = 100
intervals = rng.exponential(mean_interval, n_events)
print(f"Supernova intervals: mean = {intervals.mean():.1f} days")
```

#### Power-Law Distribution

Use for stellar masses (IMF), galaxy luminosities, and many astrophysical scaling relations:

```{code-cell} python
# Power-law distribution (using Pareto for x_min=1)
# Initial Mass Function approximation
rng = np.random.default_rng(42)
alpha = 2.35  # Salpeter IMF slope (dN/dM ∝ M^-alpha)
n_stars = 1000
# Generate masses from 0.1 to 100 solar masses
a = alpha - 1  # np.random.pareto(a) has p(x) ∝ x^-(a+1)
x = rng.pareto(a, n_stars) + 1  # Pareto starts at 1
masses = 0.1 * x  # Scale to start at 0.1 solar masses
masses = masses[masses < 100]  # Truncate at 100 solar masses
print(f"Generated {len(masses)} stellar masses with power-law distribution")
```

This is a classic "parameter name mismatch" moment: NumPy's `pareto(a)` returns a distribution with $p(x) \propto x^{-(a+1)}$, while the Salpeter IMF is $dN/dM \propto M^{-\alpha}$. Matching the exponents means using $a = \alpha - 1$.

#### Multivariate Normal Distribution

Use for correlated parameters (color-magnitude relationships, correlated measurement errors):

```{code-cell} python
# Multivariate normal: correlated parameters
# Simulate color-magnitude relationship
rng = np.random.default_rng(42)
mean = [12, 1.0]  # Mean magnitude, mean color (B-V)
# Covariance matrix: brighter stars tend to be bluer
cov = [[1.0, -0.3],   # Variance in mag, covariance
       [-0.3, 0.25]]  # Covariance, variance in color

n_stars = 500
mag_color = rng.multivariate_normal(mean, cov, n_stars)
magnitudes = mag_color[:, 0]
colors = mag_color[:, 1]

correlation = np.corrcoef(magnitudes, colors)[0, 1]
print(f"Generated {n_stars} stars with correlated properties")
print(f"Correlation coefficient: {correlation:.2f} (expected: ~-0.6)")
```

Visualizing correlated data helps build intuition for covariance:

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Recreate correlated stellar data
rng = np.random.default_rng(42)
mean = [12, 1.0]  # Mean magnitude, mean color (B-V)
cov = [[1.0, -0.3], [-0.3, 0.25]]  # Negative correlation

n_stars = 500
mag_color = rng.multivariate_normal(mean, cov, n_stars)
magnitudes = mag_color[:, 0]
colors = mag_color[:, 1]

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(colors, magnitudes, alpha=0.5, s=15, c='navy')
ax.set_xlabel('B-V Color', fontsize=11)
ax.set_ylabel('Magnitude', fontsize=11)
ax.set_title('Correlated Stellar Properties from Multivariate Normal', fontsize=12)
ax.invert_yaxis()  # Astronomical convention
ax.grid(True, alpha=0.3)

# Add correlation annotation
corr = np.corrcoef(colors, magnitudes)[0, 1]
ax.text(0.05, 0.95, f'r = {corr:.2f}', transform=ax.transAxes,
        fontsize=11, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()
```

*Multivariate normal distribution showing correlated stellar properties. The elliptical shape reveals the negative correlation between magnitude and color.*

### Random Sampling Techniques

#### Weighted Random Choice

Use for selecting objects from catalogs with known probability distributions:

```{code-cell} python
# Random choice: selecting objects from catalogs
rng = np.random.default_rng(42)
star_types = np.array(['O', 'B', 'A', 'F', 'G', 'K', 'M'])
# Probabilities based on stellar statistics
probs = np.array([0.00003, 0.0013, 0.006, 0.03, 0.076, 0.121, 0.765])
probs = probs / probs.sum()  # Ensure normalization

n_sample = 1000
sampled_types = rng.choice(star_types, n_sample, p=probs)

# Count occurrences
unique, counts = np.unique(sampled_types, return_counts=True)
for star_type, count in zip(unique, counts):
    print(f"Type {star_type}: {count/n_sample*100:.1f}%")
```

#### Bootstrap Resampling

Use for estimating uncertainties when you don't know the underlying distribution:

```{code-cell} python
# Random permutation: bootstrap resampling
rng = np.random.default_rng(42)
# Original dataset
data = np.array([23.5, 24.1, 23.8, 24.3, 23.9])

# Bootstrap resampling for error estimation
n_bootstrap = 1000
bootstrap_means = []

for i in range(n_bootstrap):
    # Resample with replacement
    resampled = rng.choice(data, len(data), replace=True)
    bootstrap_means.append(resampled.mean())

bootstrap_means = np.array(bootstrap_means)
print(f"Original mean: {data.mean():.2f}")
print(f"Bootstrap mean: {bootstrap_means.mean():.2f}")
print(f"Bootstrap std error: {bootstrap_means.std():.3f}")

# Shuffle for randomization tests
shuffled = rng.permutation(data)
print(f"Original: {data}")
print(f"Shuffled: {shuffled}")
```

:::{important} 🌟 Why This Matters: Monte Carlo Markov Chain (MCMC) in Cosmology
:class: dropdown

The random number generation you're learning powers one of modern cosmology's most important techniques: MCMC sampling for parameter estimation. When analyzing the cosmic microwave background or galaxy surveys, we need to explore vast parameter spaces to find the best-fit cosmological model.

Astro example — the same Monte Carlo ideas show up in ecology, materials science, and Bayesian machine learning.

MCMC uses random walks through parameter space, with each step drawn from distributions like those above. Missions such as Planck used these methods to place tight constraints on the universe’s age, composition, and expansion history.

Your ability to generate and manipulate random numbers with NumPy is the foundation for these universe-spanning discoveries.
:::

## 7.4 Array Operations: Vectorization Powers

:::{margin}
**Vectorization**
Performing operations on entire arrays at once rather than using explicit loops.
:::

:::{margin}
**Universal Functions**
NumPy functions that operate element-wise on arrays, supporting broadcasting and type casting.
:::

The true power of NumPy lies in vectorized operations – performing calculations on entire arrays without writing loops:

```python
# Basic arithmetic operates element-wise
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(f"a + b = {a + b}")      # Element-wise addition
print(f"a * b = {a * b}")      # Element-wise multiplication
print(f"a ** 2 = {a ** 2}")    # Element-wise power
print(f"b / a = {b / a}")      # Element-wise division
print(f"b // a = {b // a}")    # Element-wise floor division
print(f"b % a = {b % a}")      # Element-wise modulo

# Matrix multiplication uses @ operator
c = np.array([[1, 2], [3, 4]])
d = np.array([[5, 6], [7, 8]])
print(f"\nMatrix multiplication (c @ d):\n{c @ d}")
# Alternative: np.dot(c, d)
print(f"Using np.dot:\n{np.dot(c, d)}")

# Compare with list approach (verbose and slow)
a_list = [1, 2, 3, 4]
b_list = [10, 20, 30, 40]
result_list = []
for i in range(len(a_list)):
    result_list.append(a_list[i] + b_list[i])
print(f"\nList addition: {result_list}")  # Same result, more code!
```

### Universal Functions (ufuncs): Optimized Operations

NumPy's **universal functions** operate element-wise on arrays with optimized C code:

```python
# Trigonometric functions for coordinate transformations
angles_deg = np.array([0, 30, 45, 60, 90])
angles_rad = np.deg2rad(angles_deg)  # Convert to radians

sines = np.sin(angles_rad)
cosines = np.cos(angles_rad)

print(f"Angles (deg): {angles_deg}")
print(f"sin(theta): {sines}")
print(f"cos(theta): {cosines}")
print(f"sin^2(theta) + cos^2(theta): {sines**2 + cosines**2}")  # Should all be 1!
```

```python
# Exponential and logarithm for magnitude scales
magnitudes = np.array([0, 1, 2, 5, 10])
flux_ratios = 10**(-magnitudes/2.5)  # Pogson's equation
print(f"\nMagnitudes: {magnitudes}")
print(f"Flux ratios: {flux_ratios}")

# Verify: magnitude difference = -2.5 * log10(flux ratio)
recovered_mags = -2.5 * np.log10(flux_ratios)
print(f"Recovered magnitudes: {recovered_mags}")

# Floating point comparison - use allclose for safety
print(f"Magnitudes match: {np.allclose(magnitudes, recovered_mags)}")
```

### Array Methods: Built-in Analysis

Arrays come with methods for common statistical operations:

```python
# Create sample data: Gaussian with outliers
rng = np.random.default_rng(42)
data = rng.normal(100, 15, 1000)  # Normal dist: mean=100, std=15
data[::100] = 200  # Add outliers every 100th point

# Statistical methods
print(f"Mean: {data.mean():.2f}")
print(f"Median: {np.median(data):.2f}")  # More robust to outliers
print(f"Std dev (population): {data.std():.2f}")
print(f"Std dev (sample, ddof=1): {data.std(ddof=1):.2f}")
print(f"Min: {data.min():.2f}, Max: {data.max():.2f}")

# Find outliers
outliers = data > 150
n_outliers = outliers.sum()  # True counts as 1
print(f"Number of outliers (>150): {n_outliers}")

# Clean data by filtering
clean_data = data[~outliers]  # ~ means NOT
print(f"Clean mean: {clean_data.mean():.2f}")
print(f"Clean std: {clean_data.std():.2f}")

# Additional useful statistics
print(f"\nPercentiles:")
print(f"  25th: {np.percentile(data, 25):.2f}")
print(f"  75th: {np.percentile(data, 75):.2f}")
print(f"  95th: {np.percentile(data, 95):.2f}")
```

:::{warning} ⚠️ Common Bug Alert: Integer Division Trap

```python
# DANGER: Integer arrays can cause unexpected results!
counts = np.array([100, 200, 300])  # Default type is int
normalized = counts / counts.max()
print(f"Normalized (float result): {normalized}")

# But watch out for integer division with //
integer_div = counts // 2  # Floor division
print(f"Integer division by 2: {integer_div}")

# Mixed operations preserve precision
counts_int = np.array([100, 200, 300], dtype=int)
scale = 2.5  # float
scaled = counts_int / scale  # Result is float!
print(f"Int array / float = {scaled}")

# Best practice: Use float arrays for scientific calculations
counts_safe = np.array([100, 200, 300], dtype=float)
print(f"Safe float array: {counts_safe / counts_safe.max()}")
```

Always use float arrays for scientific calculations unless you specifically need integer arithmetic!
:::

:::{tip} 💡 Computational Thinking Box: Algorithmic Complexity and Big-O

**PATTERN: Understanding Algorithmic Scaling**

Different approaches to the same problem can have vastly different performance:

```python
# O(n) - Linear time with Python loop
def sum_squares_loop(arr):
    total = 0
    for x in arr:
        total += x**2
    return total

# O(n) - Linear time with NumPy; measure the result on your workload.
def sum_squares_numpy(arr):
    return (arr**2).sum()

# O(n^3) - Cubic time for naive matrix multiplication
def matrix_multiply_loops(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# O(n^3) - Optimized with NumPy using BLAS
def matrix_multiply_numpy(A, B):
    return A @ B
```

**Real impact (varies by hardware):** For a $1000 \times 1000$ matrix:

- Nested loops: seconds
- NumPy with optimized BLAS: milliseconds
- That's the difference between waiting and real-time processing!

Note: While algorithms like Strassen's achieve $O(n^{2.807})$ complexity theoretically, NumPy uses highly optimized BLAS libraries that, despite being $O(n^3)$, are typically faster in practice due to cache optimization, vectorization, and parallel processing.
:::

---

## 7.5 Indexing and Slicing: Data Selection Mastery

:::{margin}
**Boolean Masking**
Using boolean arrays to select elements that meet certain conditions.
:::

NumPy's indexing extends Python's list indexing with powerful new capabilities:

```python
# 1D indexing (like lists but more powerful)
spectrum = np.array([1.0, 1.2, 1.5, 1.3, 1.1, 0.9, 0.8])
print(f"Full spectrum: {spectrum}")
print(f"First element: {spectrum[0]}")
print(f"Last element: {spectrum[-1]}")  # Negative indexing works!
print(f"Middle section: {spectrum[2:5]}")

# Fancy indexing - select multiple specific indices
important_indices = [0, 2, 4, 6]
selected = spectrum[important_indices]
print(f"Selected wavelengths: {selected}")
```

```python
# 2D indexing - like accessing matrix elements
image = np.array([[10, 20, 30],
                  [40, 50, 60],
                  [70, 80, 90]])
print(f"2D array:\n{image}")
print(f"Element at row 1, col 2: {image[1, 2]}")  # Note: comma notation!
print(f"Entire row 1: {image[1, :]}")
print(f"Entire column 2: {image[:, 2]}")
print(f"Sub-image: \n{image[0:2, 1:3]}")
```

:::{note} Shape Checkpoint

What is the shape of `image`? What is the shape of `image[1, :]` and `image[:, 2]`? Which of those is a 1D array, and why?
:::

### Boolean Masking: The Power Tool

**Boolean masking** is one of NumPy's most powerful features for data filtering:

```python
# Stellar catalog example
stars_mag = np.array([8.2, 12.5, 6.1, 15.3, 9.7, 11.2, 5.5])
stars_color = np.array([0.5, 1.2, 0.3, 1.8, 0.7, 1.0, 0.2])  # B-V color

# Create boolean masks
bright_mask = stars_mag < 10  # True where magnitude < 10
blue_mask = stars_color < 0.6  # True where B-V < 0.6 (blue stars)

print(f"Bright stars mask: {bright_mask}")
print(f"Bright star magnitudes: {stars_mag[bright_mask]}")

# Combine conditions with & (not 'and'), | (not 'or')
bright_and_blue = (stars_mag < 10) & (stars_color < 0.6)
print(f"Bright AND blue: {stars_mag[bright_and_blue]}")

# Count matching objects
n_bright = bright_mask.sum()  # True = 1, False = 0
print(f"Number of bright stars: {n_bright}")
```

### Essential Array Functions

```python
# where: conditional operations and finding indices
data = np.array([1, 5, 3, 8, 2, 9, 4])
high_indices = np.where(data > 5)[0]  # Returns tuple, we want first element
print(f"Indices where data > 5: {high_indices}")
print(f"Values at those indices: {data[high_indices]}")

# Conditional replacement
clipped = np.where(data > 5, 5, data)  # Clip values above 5
print(f"Clipped data: {clipped}")

# clip: cleaner way to bound values
clipped_better = np.clip(data, 2, 8)  # Clip to range [2, 8]
print(f"Clipped with np.clip: {clipped_better}")
```

```python
# unique: find unique values in catalogs
star_types = np.array(['G', 'K', 'M', 'G', 'K', 'G', 'M', 'M', 'K'])
unique_types, counts = np.unique(star_types, return_counts=True)
print(f"Unique star types: {unique_types}")
print(f"Counts: {counts}")

# histogram: bin data for analysis
rng = np.random.default_rng(42)
magnitudes = rng.normal(12, 2, 1000)
hist, bins = np.histogram(magnitudes, bins=20)
print(f"Histogram has {len(hist)} bins")
print(f"Bin edges from {bins[0]:.1f} to {bins[-1]:.1f}")
print(f"Peak bin has {hist.max()} stars")

# Check for NaN and Inf values
test_array = np.array([1.0, np.nan, 3.0, np.inf, 5.0])
print(f"\nNaN check: {np.isnan(test_array)}")
print(f"Inf check: {np.isinf(test_array)}")
print(f"Finite check: {np.isfinite(test_array)}")
```

### Handling Missing Data: NaN Patterns

Real scientific data is messy. Telescope observations have bad pixels, surveys have non-detections, and data pipelines occasionally produce invalid values. NumPy's `np.nan` (Not a Number) represents these missing or invalid values, but working with NaN requires special care.

:::{warning} ⚠️ NaN Propagation Warning

NaN values propagate through calculations silently—one NaN can contaminate an entire analysis!

```{code-cell} python
import numpy as np
# NaN propagates through operations
data = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
print(f"Sum with NaN: {data.sum()}")  # Returns nan!
print(f"Mean with NaN: {data.mean()}")  # Returns nan!
```

Always check for and handle NaN values before analysis.
:::

#### Detecting NaN Values

```{code-cell} python
# Create data with missing values (common in astronomical catalogs)
magnitudes = np.array([12.5, np.nan, 14.2, np.nan, 11.8, 15.3])
print(f"Data: {magnitudes}")
print(f"Is NaN: {np.isnan(magnitudes)}")
print(f"Number of NaN values: {np.isnan(magnitudes).sum()}")
print(f"Any NaN present: {np.any(np.isnan(magnitudes))}")
```

#### Strategy 1: Filter Out NaN Values

The simplest approach—remove NaN values entirely:

```{code-cell} python
# Filter approach: remove NaN values
magnitudes = np.array([12.5, np.nan, 14.2, np.nan, 11.8, 15.3])

# Method 1: Boolean masking
clean_data = magnitudes[~np.isnan(magnitudes)]
print(f"Original length: {len(magnitudes)}")
print(f"Clean length: {len(clean_data)}")
print(f"Clean mean: {clean_data.mean():.2f}")

# Method 2: Using np.compress
clean_data2 = np.compress(~np.isnan(magnitudes), magnitudes)
print(f"Using compress: {clean_data2}")
```

#### Strategy 2: Use NaN-Safe Functions

NumPy provides `nan`-prefixed functions that ignore NaN values:

```{code-cell} python
# NaN-safe functions
magnitudes = np.array([12.5, np.nan, 14.2, np.nan, 11.8, 15.3])

print("Standard functions (corrupted by NaN):")
print(f"  np.mean(): {np.mean(magnitudes)}")
print(f"  np.std(): {np.std(magnitudes)}")
print(f"  np.sum(): {np.sum(magnitudes)}")

print("\nNaN-safe functions (ignore NaN):")
print(f"  np.nanmean(): {np.nanmean(magnitudes):.2f}")
print(f"  np.nanstd(): {np.nanstd(magnitudes):.2f}")
print(f"  np.nansum(): {np.nansum(magnitudes):.2f}")
print(f"  np.nanmin(): {np.nanmin(magnitudes):.2f}")
print(f"  np.nanmax(): {np.nanmax(magnitudes):.2f}")
print(f"  np.nanmedian(): {np.nanmedian(magnitudes):.2f}")
```

#### Strategy 3: Replace NaN Values

Sometimes you want to fill NaN with a specific value:

```{code-cell} python
# Replace NaN with specific values
magnitudes = np.array([12.5, np.nan, 14.2, np.nan, 11.8, 15.3])

# Replace with a constant (e.g., detection limit)
filled_constant = np.where(np.isnan(magnitudes), 99.99, magnitudes)
print(f"Filled with 99.99: {filled_constant}")

# Replace with the mean of valid values
mean_val = np.nanmean(magnitudes)
filled_mean = np.where(np.isnan(magnitudes), mean_val, magnitudes)
print(f"Filled with mean ({mean_val:.2f}): {filled_mean}")

# Using np.nan_to_num for NaN and Inf
data_with_inf = np.array([1.0, np.nan, np.inf, -np.inf, 5.0])
cleaned = np.nan_to_num(data_with_inf, nan=0.0, posinf=1e10, neginf=-1e10)
print(f"nan_to_num result: {cleaned}")
```

#### Strategy 4: Interpolate Over NaN

For time series data, interpolate missing values:

```{code-cell} python
# Linear interpolation over NaN values
time = np.array([0, 1, 2, 3, 4, 5])
flux = np.array([1.0, 1.2, np.nan, np.nan, 1.1, 0.9])

# Find valid and invalid indices
valid_mask = ~np.isnan(flux)
valid_time = time[valid_mask]
valid_flux = flux[valid_mask]

# Interpolate at all time points
interpolated_flux = np.interp(time, valid_time, valid_flux)
print(f"Original: {flux}")
print(f"Interpolated: {interpolated_flux}")
```

:::{tip} 💡 NaN Handling Best Practices

1. **Check early**: Always check for NaN at the start of analysis
2. **Document the source**: Know why NaN values exist (non-detections vs bad data)
3. **Choose strategy wisely**:
   - Filter for statistics (mean, std)
   - Replace for algorithms that can't handle NaN
   - Interpolate for time series with small gaps
4. **Use NaN-safe functions** when available (`np.nanmean`, etc.)
5. **Propagate intentionally**: Sometimes NaN should propagate to flag problematic results
:::

:::{note} Quick Check

You have flux measurements where non-detections are marked as NaN. You want to calculate the mean flux of detected sources only. Which approach would you use?
:::

:::{note} Answer
:class: dropdown

Use `np.nanmean()` or filter first:

```python
# Both approaches work
mean_flux = np.nanmean(flux_data)
# or
detected = flux_data[~np.isnan(flux_data)]
mean_flux = detected.mean()
```

The first is more concise; the second is clearer about intent and lets you reuse the filtered array.
:::

::::{note} 🔍 Check Your Understanding

What's the difference between `np.linspace(0, 10, 11)` and `np.arange(0, 11, 1)`?

:::{tip} Answer
:class: dropdown

Both create arrays from 0 to 10, but:

- `np.linspace(0, 10, 11)` creates exactly 11 evenly-spaced points including both endpoints: [0, 1, 2, ..., 10]
- `np.arange(0, 11, 1)` creates points from 0 up to (but not including) 11 with step 1: [0, 1, 2, ..., 10]

In this case they're equivalent, but:

- `np.linspace(0, 10, 20)` gives 20 points with fractional spacing
- `np.arange(0, 10.5, 0.5)` gives points with exact 0.5 steps

Use `linspace` when you need a specific number of points, `arange` when you need a specific step size.
:::
::::

:::{important} 🌟 Why This Matters: Finding Exoplanets with Boolean Masking
:class: dropdown

The Kepler Space Telescope discovered thousands of exoplanets by monitoring the brightness of many stars over long time spans. Finding planets in this data required sophisticated boolean masking with NumPy.

Astro example — the same masking patterns are used in climate data, microscopy, and quality control.

When a planet transits its star, the brightness drops by a small amount, but the data is noisy, with stellar flares, cosmic rays, and instrumental effects. Here's a simplified version of the detection algorithm:

```python
# Simulated light curve data
rng = np.random.default_rng(42)
time = np.linspace(0, 30, 1000)  # 30 days
flux = np.ones_like(time) + rng.normal(0, 0.001, 1000)  # Noise

# Add transits every 3.5 days (period), 0.1 day duration, 1% deep
period, duration, depth = 3.5, 0.1, 0.01
in_transit = ((time % period) < duration)
flux[in_transit] -= depth

# Detection using boolean masking
median_flux = np.median(flux)
threshold = median_flux - 3 * flux.std()  # 3-sigma detection
transit_candidates = flux < threshold
n_transits = np.diff(np.where(transit_candidates)[0] > 1).sum()

print(f"Found {n_transits} transit events")
```

This technique, scaled up with more sophisticated statistics, is how we've discovered thousands of worlds orbiting other stars!
:::

---

## 7.6 Broadcasting: NumPy's Secret Superpower

:::{margin}
**Broadcasting**
NumPy's ability to perform operations on arrays of different shapes by automatically expanding dimensions.
:::

**Broadcasting** allows NumPy to perform operations on arrays of different shapes, eliminating the need for explicit loops or array duplication:

```python
# Simple broadcasting: scalar with array
arr = np.array([1, 2, 3, 4])
result = arr + 10  # 10 is "broadcast" to [10, 10, 10, 10]
print(f"Array + scalar: {result}")

# Row vector + column vector = matrix
row = np.array([[1, 2, 3]])      # Shape (1, 3)
col = np.array([[10], [20], [30]])  # Shape (3, 1)
matrix = row + col  # Broadcasting creates (3, 3) result
print(f"Row shape: {row.shape}")
print(f"Column shape: {col.shape}")
print(f"Result:\n{matrix}")
print(f"Result shape: {matrix.shape}")
```

### Broadcasting Rules Visualization

Broadcasting follows simple rules:

1. Arrays are compatible if dimensions are equal or one is 1
2. Missing dimensions are treated as 1
3. Arrays are stretched along dimensions of size 1

```markdown
Text representation of broadcasting rules:

Array A: Shape (3, 1)    Array B: Shape (1, 4)
         v                        v
   [10]  ───┐              [1, 2, 3, 4]
   [20]  ───┼── (+) ──────────────┘
   [30]  ───┘
         v
   Result: Shape (3, 4)
   [[11, 12, 13, 14],
    [21, 22, 23, 24],
    [31, 32, 33, 34]]

Rule Check:
- Dimension 0: 3 vs 1 -> Compatible (1 broadcasts)
- Dimension 1: 1 vs 4 -> Compatible (1 broadcasts)
- Result shape: (3, 4)
```

### Shape Tools: (n,), (1, n), and (n, 1)

The same values can represent different shapes, and broadcasting depends on shape, not just size:

```python
a = np.array([1, 2, 3])      # Shape (3,)
row = a[np.newaxis, :]       # Shape (1, 3)
col = a[:, np.newaxis]       # Shape (3, 1)

print(a.shape, row.shape, col.shape)
```

If you want an operation to broadcast across rows or columns, use `np.newaxis` (or `None`) to add the dimension you need.

:::{note} Shape Checkpoint

If `a` has shape `(3,)`, what shapes do `a[np.newaxis, :]` and `a[:, np.newaxis]` have? Which one broadcasts across rows, and which across columns?
:::

```python
# Practical example: Normalize each row of a matrix
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]], dtype=float)

# Calculate row means and keep the dimension for broadcasting
row_means = data.mean(axis=1, keepdims=True)  # Shape (3, 1)
print(f"Row means shape: {row_means.shape}")

# With keepdims=True, broadcasting works without reshape
normalized = data - row_means  # Broadcasting!
print(f"Normalized data:\n{normalized}")
print(f"New row means: {normalized.mean(axis=1)}")  # Should be ~0
```

### Real-World Broadcasting: CCD Image Calibration

```python
# Flat-field correction for CCD images
rng = np.random.default_rng(42)

# Simulate CCD data
raw_image = rng.poisson(1000, size=(100, 100))  # 100x100 pixels
dark_current = np.full((100, 100), 50)  # Uniform dark current
flat_field = np.ones((100, 100))
flat_field[:, :50] = 0.9  # Left half less sensitive

# Calibrate image using broadcasting
calibrated = (raw_image - dark_current) / flat_field

print(f"Raw image mean: {raw_image.mean():.1f}")
print(f"Calibrated mean: {calibrated.mean():.1f}")
print(f"Left half sensitivity: {calibrated[:, :50].mean():.1f}")
print(f"Right half sensitivity: {calibrated[:, 50:].mean():.1f}")
```

:::{warning} ⚠️ Common Bug Alert: Broadcasting Shape Mismatch

```python
# Common mistake: incompatible shapes
a = np.array([1, 2, 3])  # Shape: (3,)
b = np.array([1, 2])     # Shape: (2,)

# This will fail!
try:
    result = a + b
except ValueError as e:
    print(f"Error: {e}")

# Solutions:
# 1. Pad the shorter array
b_padded = np.append(b, 0)  # Now shape (3,)
print(f"Padded addition: {a + b_padded}")

# 2. Use different shapes that broadcast
a_col = a.reshape(-1, 1)  # Shape: (3, 1)
b_row = b.reshape(1, -1)  # Shape: (1, 2)
broadcasted = a_col + b_row  # Shape: (3, 2)
print(f"Broadcasted result:\n{broadcasted}")
```

Always check shapes when debugging broadcasting errors!
:::

:::{note} Broadcasting Debug Checklist

1. Print each array's `.shape` and write the expected result shape.
2. Use `reshape` or `np.newaxis` to add dimensions where you intend broadcasting.
3. If you reduce with `mean` or `sum`, consider `keepdims=True` so shapes stay compatible.
:::

## 7.7 Array Manipulation: Reshaping Your Data

:::{margin}
**View**
A new array object that shares data with the original array.
:::

:::{margin}
**Copy**
A new array with its own data, independent of the original.
:::

NumPy provides powerful tools for reorganizing array data:

```python
# Reshape: Change dimensions without changing data
data = np.arange(12)
print(f"Original: {data}")

# Reshape to 2D
matrix = data.reshape(3, 4)
print(f"As 3x4 matrix:\n{matrix}")

# Reshape to 3D
cube = data.reshape(2, 2, 3)
print(f"As 2x2x3 cube:\n{cube}")

# Use -1 to infer dimension
auto_reshape = data.reshape(3, -1)  # NumPy figures out the 4
print(f"Auto-reshape to 3x?:\n{auto_reshape}")

# Flatten back to 1D
flattened = matrix.flatten()
print(f"Flattened: {flattened}")
```

### Stacking and Splitting Arrays

Combining and separating arrays is common in data analysis:

```python
# Stacking arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([7, 8, 9])

# Vertical stack (row-wise)
vstacked = np.vstack([a, b, c])
print(f"Vertical stack:\n{vstacked}")

# Horizontal stack (column-wise)
hstacked = np.hstack([a, b, c])
print(f"Horizontal stack: {hstacked}")

# Concatenate (general purpose)
concat_axis0 = np.concatenate([a, b, c])  # Default axis=0
print(f"Concatenated: {concat_axis0}")

# Stack as columns
column_stack = np.column_stack([a, b, c])
print(f"Column stack:\n{column_stack}")
```

### Transpose and Axis Manipulation for Coordinate Systems

```python
# Transpose swaps axes - useful for coordinate transformations
# Example: RA/Dec coordinates to X/Y projections
ra_dec = np.array([[10.5, -25.3],   # Star 1: RA, Dec
                    [15.2, -30.1],   # Star 2: RA, Dec
                    [20.8, -22.7]])  # Star 3: RA, Dec

# Transpose to get all RAs and all Decs
coords_transposed = ra_dec.T
print(f"Original (each row is a star):\n{ra_dec}")
print(f"Transposed (row 0 = all RAs, row 1 = all Decs):\n{coords_transposed}")

all_ra = coords_transposed[0]
all_dec = coords_transposed[1]
print(f"All RA values: {all_ra}")
print(f"All Dec values: {all_dec}")
```

:::{tip} 💡 Views vs Copies: Memory Efficiency in Large Datasets

**PATTERN: Understanding When NumPy Shares Memory**

Many NumPy operations return **views**, not copies, sharing memory with the original. This is crucial when working with large telescope images or survey data:

```python
# Real telescope data scenario
ccd_image = np.zeros((4096, 4096), dtype=np.float32)  # 64 MB

# Views - no extra memory used
quadrant1 = ccd_image[:2048, :2048]       # View: shares memory
reshaped = ccd_image.reshape(16, 1024, 1024)  # View: same data
transposed = ccd_image.T                  # View: different ordering

# Debugging tool: confirm whether two arrays share memory
print(np.shares_memory(quadrant1, ccd_image))  # True for views

# Copies - additional memory allocated
quadrant1_safe = ccd_image[:2048, :2048].copy()  # Copy: +16 MB
fancy_indexed = ccd_image[[0, 100, 200]]  # Copy: new array
masked = ccd_image[ccd_image > 100]       # Copy: filtered data

# Danger: modifying a view changes the original!
quadrant1 -= 100  # This modifies ccd_image too!

# Safe approach for calibration
quadrant1_calibrated = quadrant1.copy()
quadrant1_calibrated -= 100  # Original ccd_image unchanged
```

Operations returning views:

- Basic slicing: `arr[2:8]`
- Reshaping: `arr.reshape(2, 5)`
- Transpose: `arr.T`

Operations returning copies:

- Fancy indexing: `arr[[1, 3, 5]]`
- Boolean indexing: `arr[arr > 5]`
- Arithmetic: `arr + 1`

For observatories processing massive nightly data volumes, understanding views vs copies can mean the difference between feasible and impossible memory requirements!
:::

---

## Deep dive / reference: numerical methods and performance

The following tools are useful in particular scientific contexts. They are not
part of the Chapter 7 first-use core; introduce their assumptions explicitly
before relying on them for an inference.

## 7.8 Essential Scientific Functions

NumPy provides specialized functions crucial for scientific computing:

### Meshgrid: Creating Coordinate Grids

The **meshgrid** function is fundamental for numerical simulations and 2D/3D function evaluation. When you need to evaluate a function f(x,y) at every point on a 2D grid, you could use nested loops – but that's slow and cumbersome. Meshgrid creates coordinate matrices that enable vectorized evaluation.

**Mathematical Foundation:**
Given vectors x = [$x_{1}$, $x_{2}$, ..., $x_{n}$] and y = [$y_{1}$, $y_{2}$, ..., $y_{m}$], meshgrid creates two matrices X and Y where:

- $X[i,j] = x_j$ for all $i$ (x-coordinates repeated along rows)
- $Y[i,j] = y_i$ for all $j$ (y-coordinates repeated along columns)

This creates a rectangular grid of (x,y) coordinate pairs covering all combinations.

**Why is this powerful?** Any function f(x,y) can now be evaluated at all grid points simultaneously using vectorized operations, essential for:

- Solving partial differential equations (PDEs)
- Creating potential fields for N-body simulations
- Generating synthetic telescope images
- Computing 2D Fourier transforms
- Visualizing mathematical surfaces

```python
# Basic meshgrid demonstration
x = np.linspace(-2, 2, 5)  # 5 x-coordinates
y = np.linspace(-1, 1, 3)  # 3 y-coordinates
X, Y = np.meshgrid(x, y)

print(f"Original x: {x}")
print(f"Original y: {y}")
print(f"\nX coordinates (shape {X.shape}):\n{X}")
print(f"\nY coordinates (shape {Y.shape}):\n{Y}")

# Each (X[i,j], Y[i,j]) gives a coordinate pair
print(f"\nCoordinate at row 1, col 2: ({X[1,2]:.1f}, {Y[1,2]:.1f})")

# Evaluate f(x,y) = x^2 + y^2 at every grid point
Z = X**2 + Y**2  # No loops needed!
print(f"\nFunction values:\n{Z}")
```

```python
# Numerical simulation example: gravitational potential field
# Simulate potential from multiple point masses
masses = [1.0, 0.5, 0.3]  # Solar masses
positions = [(0, 0), (3, 2), (-2, 1)]  # AU

# Create fine grid for field calculation
x_grid = np.linspace(-5, 5, 50)
y_grid = np.linspace(-5, 5, 50)
X_field, Y_field = np.meshgrid(x_grid, y_grid)

# Calculate gravitational potential at each grid point
G = 1  # Normalized units
potential = np.zeros_like(X_field)

for mass, (px, py) in zip(masses, positions):
    # Distance from each grid point to this mass
    R = np.sqrt((X_field - px)**2 + (Y_field - py)**2)
    # Avoid singularity at mass position
    R = np.maximum(R, 0.1)
    # Add contribution to potential (Phi = -GM/r)
    potential += -G * mass / R

print(f"Potential field shape: {potential.shape}")
print(f"Min potential: {potential.min():.2f}, Max: {potential.max():.2f}")

# Numerical gradient gives force field
Fx, Fy = np.gradient(-potential, x_grid[1]-x_grid[0], y_grid[1]-y_grid[0])
force_magnitude = np.sqrt(Fx**2 + Fy**2)
print(f"Max force magnitude: {force_magnitude.max():.2f}")
```

```python
# Common use: creating synthetic star images
x_pixels = np.linspace(0, 10, 100)
y_pixels = np.linspace(0, 10, 100)
X_img, Y_img = np.meshgrid(x_pixels, y_pixels)

# Create 2D Gaussian (like a star PSF)
sigma = 2.0
star_x, star_y = 5.0, 5.0  # Star position
psf = np.exp(-((X_img - star_x)**2 + (Y_img - star_y)**2) / (2 * sigma**2))
print(f"PSF shape: {psf.shape}, peak: {psf.max():.3f}")

# 3D meshgrid for volume simulations
x_3d = np.linspace(-1, 1, 10)
y_3d = np.linspace(-1, 1, 10)
z_3d = np.linspace(-1, 1, 10)
X_3d, Y_3d, Z_3d = np.meshgrid(x_3d, y_3d, z_3d)
print(f"\n3D grid shape: {X_3d.shape}")  # (10, 10, 10)

# Evaluate 3D density field rho(x,y,z) = exp(-r^2)
density = np.exp(-(X_3d**2 + Y_3d**2 + Z_3d**2))
print(f"Total mass (integrated density): {density.sum():.2f}")
```

### Numerical Differentiation and Integration

```python
# gradient: numerical differentiation
# Useful for finding peaks, trends in light curves
time = np.linspace(0, 10, 100)
rng = np.random.default_rng(42)
flux = np.sin(time) + 0.1 * rng.standard_normal(100)

# Calculate derivative (rate of change)
flux_gradient = np.gradient(flux, time)
print(f"Maximum rate of increase: {flux_gradient.max():.3f}")
print(f"Maximum rate of decrease: {flux_gradient.min():.3f}")

# Find turning points (where derivative approx 0)
turning_points = np.where(np.abs(flux_gradient) < 0.1)[0]
print(f"Found {len(turning_points)} turning points")
```

### Interpolation with interp

```python
# Linear interpolation - crucial for spectra, light curves
wavelengths_measured = np.array([400, 500, 600, 700])  # nm
flux_measured = np.array([1.0, 1.5, 1.2, 0.8])

# Interpolate to finer grid
wavelengths_fine = np.linspace(400, 700, 31)
flux_interpolated = np.interp(wavelengths_fine,
                              wavelengths_measured,
                              flux_measured)

print(f"Original: {len(wavelengths_measured)} points")
print(f"Interpolated: {len(wavelengths_fine)} points")
print(f"Flux at 550 nm: {np.interp(550, wavelengths_measured, flux_measured):.3f}")
```

### Fourier Transforms: Frequency Analysis

The **Fast Fourier Transform (FFT)** is one of the most important algorithms in computational science, converting signals from the time domain to the frequency domain. This reveals periodic patterns hidden in noisy data – essential for finding pulsars, detecting exoplanets, and analyzing gravitational waves.

**Mathematical Foundation:**
The Discrete Fourier Transform (DFT) of a sequence x[n] with N samples is:

$$X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-2\pi i k n / N}$$

where:

- x[n] is the input signal at time sample n
- X[k] is the frequency component at frequency k
- k ranges from 0 to N-1, representing frequencies from 0 to the sampling frequency

The FFT algorithm computes this in $O(N\log N)$ operations instead of $O(N^2)$, making it practical for large datasets.

Units and assumptions: N, n, and k are unitless indices. The physical units of frequency come from your sample spacing. If your spacing `d` is in seconds, `np.fft.fftfreq(..., d)` returns frequencies in Hz; if `d` is in days, you get cycles per day. The FFT assumes uniform sampling; for uneven sampling, use methods like Lomb–Scargle.

**Physical Interpretation:**

- **Magnitude |X[k]|**: The amplitude of oscillation at frequency k
- **Phase $\arg(X[k])$**: The phase shift of that frequency component
- **Power $|X[k]|^2$**: The energy at that frequency (power spectrum)
- **Frequency bins**: $k$ corresponds to frequency $f = k \times (\mathrm{sampling\_rate}/N)$

`np.fft.fftfreq` orders bins as zero frequency, positive frequencies, then
negative frequencies. For a real-valued signal, use `np.fft.rfft` with
`np.fft.rfftfreq` when you need only the non-negative-frequency half; this
matches the transform's Hermitian symmetry. Both choices still require a
uniform sample spacing and an explicit interpretation of units.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Create a signal with multiple frequencies
t = np.linspace(0, 1, 500)  # 1 second, 500 samples
sampling_rate = 500  # Hz (samples per second)

# Build composite signal
rng = np.random.default_rng(42)
signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz component
signal += 0.5 * np.sin(2 * np.pi * 10 * t)  # 10 Hz component
signal += 0.3 * np.sin(2 * np.pi * 50 * t)  # 50 Hz component
signal += 0.2 * rng.normal(size=t.shape)  # Noise

# Compute FFT
fft = np.fft.fft(signal)

# Get corresponding frequencies
# fftfreq returns frequencies in cycles per unit of sample spacing
# Since our sample spacing is 1/500 seconds, frequencies are in Hz
freqs = np.fft.fftfreq(len(t), d=1/sampling_rate)

# Power spectrum (squared magnitude)
power = np.abs(fft)**2

# Due to symmetry, only look at positive frequencies
pos_mask = freqs > 0
freqs_pos = freqs[pos_mask]
power_pos = power[pos_mask]

# Find peaks (simplified - use scipy.signal.find_peaks for real work)
threshold = power_pos.max() / 10
peak_indices = np.where(power_pos > threshold)[0]
peak_freqs = freqs_pos[peak_indices]

print(f"Sampling rate: {sampling_rate} Hz")
print(f"Frequency resolution: {freqs[1]-freqs[0]:.2f} Hz")
print(f"Nyquist frequency: {sampling_rate/2} Hz")
print(f"Detected peaks near: 5, 10, and 50 Hz")
```

*FFT reveals hidden frequencies in a composite signal*

#### Visualizing the FFT: Time Domain vs Frequency Domain

The power of the FFT becomes clear when visualized—patterns invisible in the time domain jump out in the frequency domain:

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Recreate the signal
t = np.linspace(0, 1, 500)
sampling_rate = 500
rng = np.random.default_rng(42)
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)
signal += 0.3 * np.sin(2 * np.pi * 50 * t) + 0.2 * rng.normal(size=t.shape)

# Compute FFT
fft = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(t), d=1/sampling_rate)
power = np.abs(fft)**2

# Positive frequencies only
pos_mask = freqs > 0
freqs_pos = freqs[pos_mask]
power_pos = power[pos_mask]

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Time domain
axes[0].plot(t, signal, 'b-', linewidth=0.8, alpha=0.8)
axes[0].set_xlabel('Time (seconds)', fontsize=11)
axes[0].set_ylabel('Amplitude', fontsize=11)
axes[0].set_title('Time Domain: Signal looks complex/noisy', fontsize=12)
axes[0].set_xlim(0, 0.5)  # Show first half second
axes[0].grid(True, alpha=0.3)

# Frequency domain
axes[1].semilogy(freqs_pos, power_pos, 'r-', linewidth=0.8)
axes[1].axvline(x=5, color='green', linestyle='--', alpha=0.7, label='5 Hz')
axes[1].axvline(x=10, color='green', linestyle='--', alpha=0.7, label='10 Hz')
axes[1].axvline(x=50, color='green', linestyle='--', alpha=0.7, label='50 Hz')
axes[1].set_xlabel('Frequency (Hz)', fontsize=11)
axes[1].set_ylabel('Power (log scale)', fontsize=11)
axes[1].set_title('Frequency Domain: Three peaks clearly visible!', fontsize=12)
axes[1].set_xlim(0, 100)
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

*Left: Composite signal looks noisy in time domain. Right: FFT reveals the three frequency components clearly.*

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Practical example: Finding periodic signal in noisy data
# Simulate exoplanet transit light curve with periodic dips
time = np.linspace(0, 30, 3000)  # 30 days of observations
period = 3.456  # Planet orbital period in days
transit_duration = 0.15  # days

# Create light curve with transits
flux = np.ones_like(time)
phase = (time % period) / period
in_transit = phase < (transit_duration / period)
flux[in_transit] *= 0.99  # 1% transit depth

# Add realistic noise
rng = np.random.default_rng(42)
flux += rng.normal(0, 0.002, len(time))  # 0.2% noise

# FFT to find periodicity
fft_flux = np.fft.fft(flux - flux.mean())  # Remove DC component
freqs_flux = np.fft.fftfreq(len(time), time[1] - time[0])  # Frequencies in 1/day

# Power spectrum
power_flux = np.abs(fft_flux)**2

# Look for peak in physically reasonable range (periods from 2 to 15 days)
# Note: We use a narrower frequency range to avoid harmonics from the box-shaped transit
freq_mask = (freqs_flux > 0.07) & (freqs_flux < 0.5)  # Periods ~2-14 days
peak_freq = freqs_flux[freq_mask][np.argmax(power_flux[freq_mask])]
detected_period = 1 / peak_freq

print(f"True period: {period:.3f} days")
print(f"Detected period: {detected_period:.3f} days")
print(f"Error: {abs(detected_period - period)*24*60:.1f} minutes")

# Visualize the transit detection
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Raw light curve
axes[0, 0].plot(time, flux, 'k.', markersize=1, alpha=0.5)
axes[0, 0].set_xlabel('Time (days)', fontsize=11)
axes[0, 0].set_ylabel('Relative Flux', fontsize=11)
axes[0, 0].set_title('Raw Light Curve (transits barely visible)', fontsize=12)
axes[0, 0].set_ylim(0.98, 1.02)
axes[0, 0].grid(True, alpha=0.3)

# Zoomed view showing transits
axes[0, 1].plot(time, flux, 'k.', markersize=2, alpha=0.5)
axes[0, 1].set_xlabel('Time (days)', fontsize=11)
axes[0, 1].set_ylabel('Relative Flux', fontsize=11)
axes[0, 1].set_title('Zoomed: First 10 days', fontsize=12)
axes[0, 1].set_xlim(0, 10)
axes[0, 1].set_ylim(0.98, 1.02)
axes[0, 1].axhline(y=0.99, color='red', linestyle='--', alpha=0.5, label='Transit depth')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Power spectrum
pos_freq_mask = freqs_flux > 0
axes[1, 0].semilogy(1/freqs_flux[pos_freq_mask], power_flux[pos_freq_mask], 'b-', linewidth=0.5)
axes[1, 0].axvline(x=period, color='red', linestyle='--', linewidth=2, label=f'True P = {period:.3f} d')
axes[1, 0].axvline(x=detected_period, color='green', linestyle=':', linewidth=2, label=f'Detected P = {detected_period:.3f} d')
axes[1, 0].set_xlabel('Period (days)', fontsize=11)
axes[1, 0].set_ylabel('Power', fontsize=11)
axes[1, 0].set_title('Power Spectrum: Period Detection', fontsize=12)
axes[1, 0].set_xlim(0.5, 10)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Phase-folded light curve
phase_fold = (time % detected_period) / detected_period
axes[1, 1].plot(phase_fold, flux, 'b.', markersize=1, alpha=0.3)
axes[1, 1].set_xlabel('Phase', fontsize=11)
axes[1, 1].set_ylabel('Relative Flux', fontsize=11)
axes[1, 1].set_title(f'Phase-folded at P = {detected_period:.3f} days', fontsize=12)
axes[1, 1].set_ylim(0.98, 1.02)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

*FFT detection of exoplanet transit period from noisy light curve data*

Reality check: FFTs are excellent for sinusoidal signals, but transit light curves are boxy and generate strong harmonics. In practice, astronomers often use Box Least Squares (BLS) for transit searches and Lomb–Scargle periodograms for unevenly sampled data. You do not need those methods yet — just know that FFT is a first look, not the final word.

:::{tip} 💡 Advanced: Window Functions and Spectral Leakage
:class: dropdown

When your signal doesn't fit perfectly within your sampling window (which is almost always!), the FFT produces **spectral leakage** — power spreads to neighboring frequencies, creating artificial peaks.

**Window functions** reduce this leakage by tapering the signal edges. Common choices include:

- **Hanning** (`np.hanning(N)`): Good general-purpose choice, reduces leakage significantly
- **Hamming** (`np.hamming(N)`): Similar to Hanning, slightly different sidelobe structure
- **Blackman** (`np.blackman(N)`): Best sidelobe suppression, wider main lobe

```python
# Apply a window function before FFT
window = np.hanning(len(signal))
windowed_signal = signal * window
fft_windowed = np.fft.fft(windowed_signal)
```

Window functions are a specialized signal-processing tool. Use one only after
checking how it changes resolution, leakage, and the interpretation of any
amplitudes.
:::

:::{note} Quick Check

If your sampling rate doubles while your number of samples stays the same, what happens to the Nyquist frequency and the frequency resolution?
:::

### Covariance and Correlation

**Covariance** and **correlation** measure how two variables change together – crucial for understanding relationships in astronomical data like the color-magnitude diagram, period-luminosity relations, or Tully-Fisher correlations.

**Mathematical Definitions:**

**Covariance** between variables $X$ and $Y$:

$$
\mathrm{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)] = \frac{1}{n}\sum_{i=1}^{n} (x_i-\bar{x})(y_i-\bar{y})
$$

where:

- $E[\cdot]$ is the expected value (mean)
- $\mu_X$, $\mu_Y$ (or $\bar{x}$, $\bar{y}$) are the means of $X$ and $Y$
- $n$ is the number of data points

**Interpretation:**

- Positive covariance: Variables tend to increase together
- Negative covariance: When one increases, the other tends to decrease
- Zero covariance: No linear relationship (but there could be nonlinear relationships!)

**Problem with covariance:** It depends on the units. Temperature in Kelvin vs Celsius gives different covariances with luminosity!
The units of covariance are the units of $X$ multiplied by the units of $Y$, which makes raw covariance hard to compare across unit systems.
For sample covariance, you often divide by $n-1$ instead of $n$; `np.cov` uses the $n-1$ convention by default.

**Correlation coefficient** (Pearson's $r$) solves this by normalizing:

$$
r = \frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}
$$

Where $\sigma_X$ and $\sigma_Y$ are the standard deviations. This gives:

- $r \in [-1, 1]$ always
- $r = 1$: Perfect positive linear correlation
- $r = -1$: Perfect negative linear correlation
- $r = 0$: No linear correlation
- $|r| > 0.7$: Generally considered strong correlation
- $|r| < 0.3$: Generally considered weak correlation

**Covariance Matrix:**

For multiple variables, we organize covariances into a matrix:

```
       X    Y    Z
   X  Var(X) Cov(X,Y) Cov(X,Z)
   Y  Cov(Y,X) Var(Y) Cov(Y,Z)
   Z  Cov(Z,X) Cov(Z,Y) Var(Z)
```

The diagonal contains variances (a variable's covariance with itself), and the matrix is symmetric ($\mathrm{Cov}(X,Y) = \mathrm{Cov}(Y,X)$).

```python
# Calculate covariance and correlation between datasets
# Simulate correlated stellar properties
rng = np.random.default_rng(42)
n_stars = 100
temperature = rng.normal(5800, 500, n_stars)  # Kelvin
# Luminosity correlates with temperature (Stefan-Boltzmann: L propto T^4)
# Add noise to make it realistic
luminosity_true = (temperature/5800)**4  # Normalized to solar
luminosity = luminosity_true + rng.normal(0, 0.1, n_stars)

# Manual calculation to understand the math
temp_mean = temperature.mean()
lum_mean = luminosity.mean()
temp_centered = temperature - temp_mean
lum_centered = luminosity - lum_mean

# Covariance: average of products of deviations
covariance_manual = (temp_centered * lum_centered).mean()
print(f"Manual covariance: {covariance_manual:.6f}")

# Standard deviations
temp_std = temperature.std()
lum_std = luminosity.std()

# Correlation coefficient
correlation_manual = covariance_manual / (temp_std * lum_std)
print(f"Manual correlation: {correlation_manual:.3f}")

# Using NumPy functions
# Covariance matrix
cov_matrix = np.cov(temperature, luminosity)
print(f"\nCovariance matrix:\n{cov_matrix}")
print(f"Temperature variance: {cov_matrix[0,0]:.1f}")
print(f"Luminosity variance: {cov_matrix[1,1]:.6f}")
print(f"Temp-Lum covariance: {cov_matrix[0,1]:.6f}")

# Correlation coefficient
corr_matrix = np.corrcoef(temperature, luminosity)
print(f"\nCorrelation matrix:\n{corr_matrix}")
print(f"Correlation coefficient: {corr_matrix[0,1]:.3f}")

# Interpretation
if abs(corr_matrix[0,1]) > 0.7:
    strength = "strong"
elif abs(corr_matrix[0,1]) > 0.3:
    strength = "moderate"
else:
    strength = "weak"
print(f"This indicates a {strength} correlation between temperature and luminosity")
```

```python
# Multiple variables: complete covariance analysis
# Add more stellar properties
rng = np.random.default_rng(42)
mass = rng.normal(1, 0.3, n_stars)  # Solar masses
# Radius correlates with mass (mass-radius relation)
radius = mass**0.8 + rng.normal(0, 0.05, n_stars)
# Age (uncorrelated with current properties for main sequence)
age = rng.uniform(1, 10, n_stars)  # Gyr

# Stack all variables
data = np.vstack([temperature, luminosity, mass, radius, age])

# Full covariance matrix
full_cov = np.cov(data)
print("Full covariance matrix shape:", full_cov.shape)

# Full correlation matrix (easier to interpret)
full_corr = np.corrcoef(data)
labels = ['Temp', 'Lum', 'Mass', 'Radius', 'Age']

print("\nCorrelation matrix:")
print("       ", "  ".join(f"{l:>7}" for l in labels))
for i, label in enumerate(labels):
    print(f"{label:>7}", "  ".join(f"{full_corr[i,j]:7.3f}" for j in range(5)))

print("\nStrong correlations (|r| > 0.5):")
for i in range(5):
    for j in range(i+1, 5):
        if abs(full_corr[i,j]) > 0.5:
            print(f"  {labels[i]}-{labels[j]}: {full_corr[i,j]:.3f}")
```

```python
# Cross-correlation for time series alignment
# Useful for aligning light curves or spectra
signal1 = np.sin(np.linspace(0, 10, 100))
signal2 = np.sin(np.linspace(0, 10, 100) + 1)  # Phase shifted

# Cross-correlation finds the shift
correlation = np.correlate(signal1, signal2, mode='same')
lag = np.argmax(correlation) - len(correlation)//2
print(f"Maximum correlation at lag: {lag} samples")

# This tells us signal2 is shifted relative to signal1
```

:::{important} 🌟 Why This Matters: The Vera Rubin Observatory's Data Challenge
:class: dropdown

The Vera Rubin Observatory (formerly LSST) will produce enormous data volumes every night. Using Python lists instead of NumPy arrays would make this impossible.

Astro example — the same memory and throughput issues appear in satellite imaging, genomics, and materials characterization.

**Memory Requirements:** Python lists store objects with large overhead, while NumPy stores contiguous numeric buffers. For large images with millions of pixels, lists can be orders of magnitude larger than arrays.

**Processing Speed:** Detecting moving asteroids requires comparing images pixel-by-pixel. Vectorized NumPy operations make those comparisons fast enough to be practical.

**Real-time Alerts:** NumPy's speed enables rapid detection and alerting for transient events — the core workflow of time-domain astronomy.

Without NumPy's memory efficiency and speed, modern time-domain astronomy would be infeasible. The same library you're learning makes it possible to monitor the sky for changes every night.
:::

## 7.9 Performance and Memory Considerations

Understanding NumPy's performance characteristics helps write efficient code:

```python
import time
import numpy as np

# Compare performance: loops vs vectorization
size = 100000
rng = np.random.default_rng(42)
a = rng.standard_normal(size)
b = rng.standard_normal(size)

# Method 1: Python loop
start = time.perf_counter()
result_loop = []
for i in range(size):
    result_loop.append(a[i] * b[i] + a[i]**2)
loop_time = time.perf_counter() - start

# Method 2: NumPy vectorization
start = time.perf_counter()
result_vector = a * b + a**2
vector_time = time.perf_counter() - start

print(f"Loop time: {loop_time*1000:.2f} ms")
print(f"Vector time: {vector_time*1000:.2f} ms")
print(f"Speedup: {loop_time/vector_time:.1f}x")
```

```python
# Memory usage comparison
array_float64 = np.ones(1000000, dtype=np.float64)
array_float32 = np.ones(1000000, dtype=np.float32)
array_float16 = np.ones(1000000, dtype=np.float16)

print(f"Memory usage for 1 million elements:")
print(f"float64: {array_float64.nbytes / 1e6:.1f} MB")
print(f"float32: {array_float32.nbytes / 1e6:.1f} MB")
print(f"float16: {array_float16.nbytes / 1e6:.1f} MB")
```

### Performance Comparison Table

Let's create concrete performance benchmarks you can run on your system:

```python
"""
Performance comparison: Lists vs NumPy
Run these on your machine - results vary by hardware!
"""
import time
import numpy as np

def benchmark_operation(name, list_func, numpy_func, size=100000):
    """Benchmark a single operation."""
    # Setup data
    list_data = list(range(size))
    numpy_data = np.arange(size, dtype=float)

    # Time list operation
    start = time.perf_counter()
    list_result = list_func(list_data)
    list_time = time.perf_counter() - start

    # Time NumPy operation
    start = time.perf_counter()
    numpy_result = numpy_func(numpy_data)
    numpy_time = time.perf_counter() - start

    speedup = list_time / numpy_time
    return list_time * 1000, numpy_time * 1000, speedup

# Define operations to benchmark
operations = {
    "Element-wise square": (
        lambda x: [i**2 for i in x],
        lambda x: x**2
    ),
    "Sum all elements": (
        lambda x: sum(x),
        lambda x: x.sum()
    ),
    "Element-wise sqrt": (
        lambda x: [i**0.5 for i in x],
        lambda x: np.sqrt(x)
    ),
    "Find maximum": (
        lambda x: max(x),
        lambda x: x.max()
    )
}

print("Performance Comparison (100,000 elements):")
print("-" * 60)
print(f"{'Operation':<20} {'List (ms)':<12} {'NumPy (ms)':<12} {'Speedup':<10}")
print("-" * 60)

for name, (list_op, numpy_op) in operations.items():
    list_ms, numpy_ms, speedup = benchmark_operation(name, list_op, numpy_op)
    print(f"{name:<20} {list_ms:<12.2f} {numpy_ms:<12.3f} {speedup:<10.1f}x")
```

```python
import time
import numpy as np

# Matrix multiplication comparison (smaller size due to O(n^3) complexity)
def matrix_multiply_lists(A, B):
    """Matrix multiplication with nested lists."""
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Create test matrices
n = 100  # 100x100 matrices
A_list = [[float(i+j) for j in range(n)] for i in range(n)]
B_list = [[float(i-j) for j in range(n)] for i in range(n)]
A_numpy = np.array(A_list)
B_numpy = np.array(B_list)

# Benchmark matrix multiplication
start = time.perf_counter()
C_list = matrix_multiply_lists(A_list, B_list)
list_matmul_time = time.perf_counter() - start

start = time.perf_counter()
C_numpy = A_numpy @ B_numpy
numpy_matmul_time = time.perf_counter() - start

print(f"\nMatrix Multiplication (100x100):")
print(f"  Nested loops: {list_matmul_time*1000:.1f} ms")
print(f"  NumPy (@):    {numpy_matmul_time*1000:.3f} ms")
print(f"  Speedup:      {list_matmul_time/numpy_matmul_time:.0f}x")
```

::::{note} 🔍 Check Your Understanding

Why is `np.empty()` faster than `np.zeros()` but potentially dangerous?

:::{tip} Answer
:class: dropdown

`np.empty()` allocates memory without initializing values, while `np.zeros()` allocates and sets all values to 0.

```python
# empty is faster but contains garbage
empty_arr = np.empty(5)
print(empty_arr)  # Random values from memory!

# zeros is slower but safe
zero_arr = np.zeros(5)
print(zero_arr)  # Guaranteed [0. 0. 0. 0. 0.]
```

Use `np.empty()` only when you'll immediately overwrite all values. Otherwise, you might accidentally use uninitialized data, leading to non-reproducible bugs!
:::
::::

### NumPy Gotchas: Top 5 Student Mistakes

:::{warning} ⚠️ Common NumPy Pitfalls

1. **Integer division with integer arrays**
   ```python
   # Wrong: integer division
   arr = np.array([1, 2, 3])
   normalized = arr / arr.max()  # Works but be careful with //

   # Safe: always use floats for science
   arr = np.array([1, 2, 3], dtype=float)
   ```

2. **Views modify the original**
   ```python
   data = np.arange(10)
   view = data[2:8]
   view[0] = 999  # Changes data[2] to 999!
   ```

3. **Using `and`/`or` instead of `&`/`|`**
   ```python
   # Wrong: Python keywords don't work
   # mask = (arr > 5) and (arr < 10)  # Error!

   # Right: Use bitwise operators
   mask = (arr > 5) & (arr < 10)
   ```

4. **Misunderstanding axis parameter**
   ```python
   matrix = np.array([[1, 2], [3, 4]])
   matrix.sum(axis=0)  # [4, 6] - sum down columns
   matrix.sum(axis=1)  # [3, 7] - sum across rows
   ```

5. **Assuming `np.empty()` contains zeros**
   ```python
   # Dangerous: contains random memory
   arr = np.empty(100)
   # arr might contain huge values!

   # Safe: explicitly initialize
   arr = np.zeros(100)
   ```
:::

---

## Main Takeaways

You've just acquired the fundamental tool that transforms Python into a scientific computing powerhouse. NumPy isn't just a faster way to work with numbers – it's a different way of thinking about computation. Instead of writing loops that process elements one at a time, you now express mathematical operations on entire datasets at once. This vectorized thinking mirrors how we conceptualize scientific problems: we don't think about individual photons hitting individual pixels; we think about images, spectra, and light curves as coherent wholes. NumPy lets you write code that matches this conceptual model, making your programs both faster and more readable.

The performance gains you've witnessed aren't just convenient; they're transformative. Calculations that would be sluggish with Python lists can become fast with NumPy arrays. This speed isn't achieved through complex optimization tricks but through NumPy's elegant design: contiguous memory storage, vectorized operations that call optimized compiled routines, and broadcasting that eliminates redundant data copying. The same ideas that make your homework scripts faster also power large‑scale data analysis workflows at observatories and laboratories worldwide.

Beyond performance, NumPy provides a vocabulary for scientific computing that's consistent across the entire Python ecosystem. The array indexing, broadcasting rules, and ufuncs you've learned aren't just NumPy features – they're the standard interface for numerical computation in Python. When you move on to using SciPy for optimization, Matplotlib for visualization, or Pandas for data analysis, you'll find they all speak NumPy's language. This consistency means the effort you've invested in understanding NumPy pays dividends across every scientific Python library you'll ever use. You've learned to leverage views for memory efficiency, use boolean masking for sophisticated data filtering, and apply broadcasting to solve complex problems elegantly. These aren't just programming techniques; they're computational thinking patterns that will shape how you approach every numerical problem.

Random generators let you create controlled synthetic data, but a simulation is
only as defensible as its stated distributional assumptions and seed record.

Looking ahead, NumPy arrays will be the primary data structure for the rest of your scientific computing journey. Every image you process, every spectrum you analyze, every simulation you run will flow through NumPy arrays. You now have the tools to use NumPy for arrays and the `math` module for scalar-only tasks when appropriate. The concepts you've mastered – vectorization, broadcasting, boolean masking – aren't just NumPy features; they're the foundation of modern computational science. You're no longer limited by Python's native capabilities; you have access to the same computational power that enables large‑scale data analysis across many scientific fields. In the next chapter, you'll see how NumPy arrays become the canvas for scientific visualization with Matplotlib, where every plot, image, and diagram starts with the arrays you now know how to create and manipulate.

---

:::{note} Quick Check

Suppose you want to compute the mean of each row of a 2D array and subtract it from that row. Which shape should the row means have to broadcast correctly?
:::

## Definitions

**Array**: NumPy's fundamental data structure, a grid of values all of the same type, indexed by a tuple of integers.

**Boolean Masking**: Using an array of boolean values to select elements from another array that meet certain conditions.

**Broadcasting**: NumPy's mechanism for performing operations on arrays of different shapes by automatically expanding dimensions according to specific rules.

**CGS Units**: Centimeter-Gram-Second unit system, traditionally used in astronomy and astrophysics for convenient scaling.

**Contiguous Memory**: Data stored in adjacent memory locations, enabling fast access and efficient cache utilization.

**Copy**: A new array with its own data, independent of the original array's memory.

**dtype**: The data type of array elements, determining memory usage and numerical precision (e.g., float64, int32).

**Monte Carlo**: A computational technique using random sampling to solve problems that might be deterministic in principle.

**ndarray**: NumPy's n-dimensional array object, the core data structure for numerical computation.

**NumPy**: Numerical Python, the fundamental package for scientific computing providing support for arrays and mathematical functions.

**Shape**: The dimensions of an array, given as a tuple indicating the size along each axis.

**ufunc**: Universal function, a NumPy function that operates element-wise on arrays, supporting broadcasting and type casting.

**Universal Functions**: NumPy functions that operate element-wise on arrays, supporting broadcasting and type casting.

**Vectorization**: Performing operations on entire arrays at once rather than using explicit loops, leveraging optimized C code.

**View**: A new array object that shares data with the original array, saving memory but linking modifications.

---

## Key Takeaways

✔ **NumPy arrays are often much faster than Python lists** for numerical operations by using contiguous memory and calling optimized compiled routines

✔ **Vectorization eliminates explicit loops** by operating on entire arrays at once, making code both faster and more readable

✔ **NumPy covers most math operations and adds array support** – use `np.sin()` for arrays, and `math` for scalar-only work when appropriate

✔ **Broadcasting enables operations on different-shaped arrays** by automatically expanding dimensions, eliminating data duplication

✔ **Boolean masking provides powerful data filtering** using conditions to select array elements, essential for data analysis

✔ **Essential creation functions** like `linspace`, `logspace`, and `meshgrid` are workhorses for scientific computing

✔ **Random number generation** from various distributions (uniform, normal, Poisson) enables Monte Carlo simulations

✔ **Memory layout matters** – row-major vs column-major ordering can change performance

✔ **Views share memory while copies are independent** – understanding this prevents unexpected data modifications

✔ **Array methods provide built-in analysis** – `.mean()`, `.std()`, `.max()` operate efficiently along specified axes

✔ **NumPy is the foundation of scientific Python** – every major package (SciPy, Matplotlib, Pandas) builds on NumPy arrays

---

## Quick Reference Tables

### Array Creation Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `np.array()` | Create from list | `np.array([1, 2, 3])` |
| `np.zeros()` | Initialize with 0s | `np.zeros((3, 4))` |
| `np.ones()` | Initialize with 1s | `np.ones((2, 3))` |
| `np.empty()` | Uninitialized (fast) | `np.empty(5)` |
| `np.full()` | Fill with value | `np.full((3, 3), 7)` |
| `np.eye()` | Identity matrix | `np.eye(4)` |
| `np.arange()` | Like Python's range | `np.arange(0, 10, 2)` |
| `np.linspace()` | N evenly spaced | `np.linspace(0, 1, 11)` |
| `np.logspace()` | Log-spaced values | `np.logspace(0, 3, 4)` |
| `np.meshgrid()` | 2D coordinate grids | `np.meshgrid(x, y)` |

### Essential Array Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `+, -, *, /` | Element-wise arithmetic | `a + b` |
| `**` | Element-wise power | `a ** 2` |
| `//` | Floor division | `a // 2` |
| `%` | Modulo | `a % 3` |
| `@` | Matrix multiplication | `a @ b` |
| `np.dot()` | Dot product | `np.dot(a, b)` |
| `==, !=, <, >` | Element-wise comparison | `a > 5` |
| `&, |, ~` | Boolean operations | `(a > 0) & (a < 10)` |
| `.T` | Transpose | `matrix.T` |
| `.reshape()` | Change dimensions | `arr.reshape(3, 4)` |
| `.flatten()` | Convert to 1D | `matrix.flatten()` |

### Statistical Methods

| Method | Description | Example |
|--------|-------------|---------|
| `.mean()` | Average | `arr.mean()` or `arr.mean(axis=0)` |
| `.std()` | Standard deviation | `arr.std()` |
| `.min()/.max()` | Extrema | `arr.min()` |
| `.sum()` | Sum elements | `arr.sum()` |
| `.cumsum()` | Cumulative sum | `arr.cumsum()` |
| `.argmin()/.argmax()` | Index of extrema | `arr.argmax()` |
| `np.median()` | Median value | `np.median(arr)` |
| `np.percentile()` | Percentiles | `np.percentile(arr, 95)` |
| `np.cov()` | Covariance matrix | `np.cov(x, y)` |
| `np.corrcoef()` | Correlation coefficient | `np.corrcoef(x, y)` |
| `np.histogram()` | Compute histogram | `np.histogram(data, bins=20)` |

### Random Number Functions

Assume `rng = np.random.default_rng(42)` for the examples below.

| Function | Distribution | Example |
|----------|-------------|---------|
| `rng.uniform()` | Uniform | `rng.uniform(0, 1, 1000)` |
| `rng.random()` | Uniform [0,1) | `rng.random(100)` |
| `rng.normal()` | Gaussian/Normal | `rng.normal(0, 1, 1000)` |
| `rng.standard_normal()` | Standard normal | `rng.standard_normal(100)` |
| `rng.poisson()` | Poisson | `rng.poisson(100, 1000)` |
| `rng.exponential()` | Exponential | `rng.exponential(1.0, 1000)` |
| `rng.choice()` | Random selection | `rng.choice(arr, 10)` |
| `rng.permutation()` | Shuffle array | `rng.permutation(arr)` |
| `np.random.default_rng()` | Create generator | `rng = np.random.default_rng(42)` |
| `rng.multivariate_normal()` | Multivariate normal | `rng.multivariate_normal(mean, cov, n)` |

### Common NumPy Functions

| Function | Purpose | Math Equivalent |
|----------|---------|-----------------|
| `np.sin()` | Sine | `math.sin()` |
| `np.cos()` | Cosine | `math.cos()` |
| `np.exp()` | Exponential | `math.exp()` |
| `np.log()` | Natural log | `math.log()` |
| `np.log10()` | Base-10 log | `math.log10()` |
| `np.sqrt()` | Square root | `math.sqrt()` |
| `np.abs()` | Absolute value | `abs()` |
| `np.round()` | Round to integer | `round()` |
| `np.where()` | Conditional selection | N/A |
| `np.clip()` | Bound values | N/A |
| `np.unique()` | Find unique values | `set()` |
| `np.concatenate()` | Join arrays | `+` for lists |
| `np.gradient()` | Numerical derivative | N/A |
| `np.interp()` | Linear interpolation | N/A |
| `np.allclose()` | Float comparison | N/A |
| `np.isnan()` | Check for NaN | N/A |
| `np.isinf()` | Check for infinity | N/A |
| `np.isfinite()` | Check for finite | N/A |
| `np.correlate()` | Cross-correlation | N/A |

### Memory and Performance Reference

| Operation | Returns View | Returns Copy |
|-----------|--------------|--------------|
| Basic slicing `arr[2:8]` | ✓ | |
| Fancy indexing `arr[[1,3,5]]` | | ✓ |
| Boolean masking `arr[arr>5]` | | ✓ |
| `.reshape()` | ✓ | |
| `.flatten()` | | ✓ |
| `.ravel()` | ✓ (usually) | |
| `.T` or `.transpose()` | ✓ | |
| Arithmetic `arr + 1` | | ✓ |
| `.copy()` | | ✓ |

---

## References

1. Harris, C. R., et al. (2020). **Array programming with NumPy**. *Nature*, 585(7825), 357-362.

2. van der Walt, S., Colbert, S. C., & Varoquaux, G. (2011). **The NumPy array: a structure for efficient numerical computation**. *Computing in Science & Engineering*, 13(2), 22-30.

3. Oliphant, T. E. (2006). **A guide to NumPy**. USA: Trelgol Publishing.

4. VanderPlas, J. (2016). **Python Data Science Handbook**. O'Reilly Media.

5. Johansson, R. (2019). **Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib** (2nd ed.). Apress.

---

## Next Chapter Preview

In Chapter 8: Matplotlib - Visualizing Your Universe, you'll discover how to transform the NumPy arrays you've mastered into publication-quality visualizations. You'll learn to create everything from simple line plots to complex multi-panel figures displaying astronomical data. Using the same NumPy arrays you've been working with, you'll visualize spectra with proper wavelength scales, create color-magnitude diagrams from stellar catalogs, display telescope images with world coordinate systems, and generate the kinds of plots that appear in research papers. You'll master customization techniques to control every aspect of your figures, from axis labels with LaTeX formatting to colormaps optimized for astronomical data. The NumPy operations you've learned – slicing for zooming into data, masking for highlighting specific objects, and meshgrid for creating coordinate systems – become the foundation for creating compelling scientific visualizations. Most importantly, you'll understand how NumPy and Matplotlib work together as an integrated system, with NumPy handling the computation and Matplotlib handling the visualization, forming the core workflow that will carry you through your entire career in computational astrophysics!
