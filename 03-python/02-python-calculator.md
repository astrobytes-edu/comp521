---
title: "Chapter 2: Python as Your Scientific Calculator"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

## Learning objectives

By the end of this chapter, you will be able to:

- [ ] **(1) Use Python as an interactive scientific calculator** with correct operator precedence (PEMDAS) and all seven arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`).
- [ ] **(2) Explain how computers represent numbers in memory** using IEEE 754 standard for floats (64 bits: sign, exponent, fraction field $\to$ ~53-bit significand precision) and arbitrary precision for integers.
- [ ] **(3) Demonstrate why $0.1 + 0.2 \neq 0.3$** due to binary representation limits and handle comparisons with `math.isclose()`.
- [ ] **(4) Recognize and prevent three numerical hazards**: catastrophic cancellation, overflow (float64 max ~1e308; float32 max ~1e38), and silent underflow to zero.
- [ ] **(5) Choose appropriate numeric types** (int, float32, float64, complex) based on precision needs and memory constraints.
- [ ] **(6) Format scientific output using f-strings** with format specifiers (`.2f`, `.2e`, `:10.2f`, `:,`) for publication-quality results.
- [ ] **(7) Convert between data types** safely using `int()`, `float()`, `complex()` while understanding truncation vs rounding.
- [ ] **(8) Apply defensive programming techniques** including validation functions, safe division, and domain-specific checks.
- [ ] **(9) Use essential `math` module functions** for scientific computing: `sqrt()`, `log()`, `sin()`, `cos()`, `isfinite()`, `isnan()`.
- [ ] **(10) Work with complex numbers** using Python's `j` notation for wave physics and Fourier analysis.

## Prerequisites

:::{note} Before Starting This Chapter

- [ ] You can launch IPython and use basic magic commands (Chapter 1)
- [ ] You understand the difference between scripts and interactive sessions (Chapter 1)
- [ ] You can navigate your file system and activate your conda environment (Chapter 1)
- [ ] A Python environment is active and an interactive session or script can run

If any boxes are unchecked, review Chapter 1 first.
:::

---

## Why this chapter matters

Now that you've mastered setting up your computational environment and understand how Python finds and loads code, it's time to transform IPython into your personal calculator. But this chapter goes far beyond simple arithmetic - you're about to discover the hidden complexity of numerical computation that can make the difference between correct results and completely wrong ones due to rounding errors.

You'll learn why spacecraft have crashed, why some calculations fail catastrophically, and how to write code that handles extreme scales — from the quantum level at $10^{-35}$ meters to the cosmological scale at $10^{26}$ meters. The floating-point precision issues we explore here aren't academic exercises; they're the source of real bugs that have corrupted simulations, invalidated published results, and caused navigation errors costing hundreds of millions of dollars.

By mastering these fundamentals now, you'll develop the numerical intuition that separates computational scientists from programmers who just happen to work with scientific data. Every simulation you build, every dataset you analyze, and every statistical test you run will rely on the concepts in this chapter. Let's begin your journey from calculator user to numerical computing expert.

:::{important} Numerical Thinking Checklist (use throughout your work)

Before trusting a numerical result, quickly ask:

- **Scale:** What order(s) of magnitude are the inputs and outputs?
- **Representation:** Should this be `int`, `float64`, `float32`, `Decimal`, or `complex`?
- **Stability:** Am I subtracting nearly equal numbers? Summing many terms? Repeating an update many times?
- **Propagation:** Will small errors accumulate (iterations, long integrations, long time series)?
- **Comparison:** Should I compare with absolute tolerance, relative tolerance, or both?
- **Diagnostics:** What are the dtypes? Are values finite (`math.isfinite`, `np.isfinite`)? Any `nan`/`inf`?
:::

---

## 2.1 Python as Your Scientific Calculator

Open a Python cell in VS Code, or an optional `ipython` session, and start with
the basics. Python handles arithmetic operations naturally, but there are
subtleties that matter for scientific work:

```{code-cell} python
# Basic arithmetic - but watch the precision!
print(f"2 + 2 = {2 + 2}")
print(f"10 / 3 = {10 / 3}")  # Division always gives a float
print(f"2 ** 10 = {2 ** 10}")  # Exponentiation - the power operator
```

Notice that `10 / 3` gives us `3.3333333333333335` — not exactly 1/3! This tiny imprecision at the end might seem trivial, but it's your first glimpse into a fundamental challenge of computational science.

### Operator Precedence: A Source of Real Bugs

Python follows PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction), but relying on memorized rules causes expensive errors. Let's see this with a real calculation:

```{code-cell} python
# Calculate orbital velocity: v = sqrt(GM/r)
# Using SI units
# (Constants are rounded for pedagogy; for research, prefer astropy.constants.)
G = 6.67e-11   # Gravitational constant (m^3 kg^-1 s^-2)
M = 1.989e30  # Solar mass (kg)
r = 1.496e11  # 1 AU (m)

# WRONG - operator precedence error!
v_wrong = G * M / r ** 0.5
print(f"Wrong velocity: {v_wrong:.2e} m/s")

# CORRECT - parentheses clarify intent
v_right = (G * M / r) ** 0.5
print(f"Correct velocity: {v_right:.2e} m/s")
print(f"That's {v_right/1e3:.1f} km/s - Earth's orbital speed!")

# The error factor
error_factor = v_wrong / v_right
print(f"Wrong answer is {error_factor:.0f}x too large!")
```

The wrong version calculated $(GM/\sqrt{r})$ instead of $\sqrt{(GM/r)}$ — a huge error!

One more precedence pitfall worth memorizing: exponentiation is **right-associative**.

```{code-cell} python
print(f"2**3**2 = {2**3**2}  (this is 2**(3**2), not (2**3)**2)")
print(f"(2**3)**2 = {(2**3)**2}")
```

:::{tip} Check Your Understanding
:class: dropdown

Before running this code, predict the result of: `-2**2 + 3*4//2`

Work through it step by step:

1. First, identify the operations: negation, exponentiation, multiplication, floor division, addition
2. Apply PEMDAS rules (*remember*: exponentiation before negation!)
3. Write your predicted answer

**Solution:**

Let's work through `-2**2 + 3*4//2` step by step:

1. **Exponentiation first**: `2**2 = 4`
2. **Then negation**: `-4` (the negative applies after exponentiation!)
3. **Multiplication**: `3*4 = 12`
4. **Floor division**: `12//2 = 6`
5. **Finally addition**: `-4 + 6 = 2`

The result is `2`. The tricky part is that `-2**2` equals `-4`, not `4`! Python interprets this as `-(2**2)`, not `(-2)**2`. This subtle precedence rule has caused real bugs in calculations.
:::

### Complete Arithmetic Operators

Python provides operators beyond basic arithmetic that prove essential for scientific calculations:

```{code-cell} python
# Integer division - useful for time calculations
days = 17
weeks = days // 7  # Floor division
remaining_days = days % 7  # Modulo (remainder)
print(f"{days} days = {weeks} weeks and {remaining_days} days")

# Warning: Floor division rounds toward negative infinity!
print(f"17 // 3 = {17 // 3}")    # Result: 5
print(f"-17 // 3 = {-17 // 3}")  # Result: -6, not -5!

# This catches many people by surprise
print("\nBe careful with negative values:")
print(f"int(-17/3) = {int(-17/3)} (truncates toward zero)")
print(f"-17 // 3 = {-17 // 3} (floors toward -infinity)")
```

:::{warning} Common Bug Alert: Negative Floor Division

Floor division with negative numbers often surprises programmers calculating phases or time intervals before an epoch. When working with values that can be negative, always test your edge cases or use `int(a/b)` for truncation toward zero.
:::

---

## 2.2 How Python Stores Numbers: Critical for Scientific Computing

Here's where your journey gets interesting! You're about to peek behind the curtain and see how computers really think about numbers. This knowledge is your superpower — it's what lets you calculate trajectories with precision.

### Integers: Arbitrary Precision Power

Unlike many languages, Python integers have unlimited precision — a huge advantage when dealing with enormous numbers:

```{code-cell} python
# Number of atoms in the observable universe (approximate)
atoms_in_universe = 10 ** 80
print(f"Atoms in universe: {atoms_in_universe}")

# Python handles it perfectly!
atoms_squared = atoms_in_universe ** 2
print(f"Can even square it: {atoms_squared}")

# Memory usage scales with size
import sys
print(f"\nMemory usage comparison:")
print(f"Small integer (42) uses: {sys.getsizeof(42)} bytes")
print(f"Universe atoms uses: {sys.getsizeof(atoms_in_universe)} bytes")
print(f"Atoms squared uses: {sys.getsizeof(atoms_squared)} bytes")
```

This **arbitrary precision** is wonderful but comes with a cost — Python integers use more memory (and can be slower) than fixed-size integers in compiled languages. This is why specialized numerical libraries become essential for large datasets.

### Floating-Point Numbers: The Heart of Numerical Computing

This is it — the concept that separates casual programmers from computational scientists! Don't worry if this seems complex at first; every professional scientist had to learn these same lessons.

Floating-point numbers use **IEEE 754** representation: 64 bits split into sign (1 bit), exponent (11 bits), and a **fraction field** (52 stored bits). For normal (non-subnormal) numbers there is an implicit leading 1, so you get about **53 bits of significand precision** (roughly **15–16 decimal digits**). This creates fundamental limitations that every computational scientist must understand.

### Understanding Bits and Precision

Before diving into floating-point challenges, let's understand the fundamental unit of computer memory: the **bit**. A bit (binary digit) can store exactly one of two values: 0 or 1. Think of it as a light switch—either on or off. Everything your computer does ultimately reduces to manipulating billions of these tiny switches.

Groups of bits form larger units:

- **8 bits** = 1 byte (can represent 256 different values: $2^{8}$)
- **32 bits** = 4 bytes (can represent ~4.3 billion values: $2^{32}$)
- **64 bits** = 8 bytes (can represent ~18 quintillion values: $2^{64}$)

### Single vs Double Precision: The 32-bit vs 64-bit Choice

Floating-point numbers come in two main flavors:

```{code-cell} python
import numpy as np
import sys

# Python's default float is 64-bit (double precision)
regular_float = 3.14159265358979323846
print(f"Python float: {sys.getsizeof(regular_float)} bytes")
print(f"Precision: {regular_float}")

# NumPy lets us choose 32-bit (single precision)
single_precision = np.float32(3.14159265358979323846)
double_precision = np.float64(3.14159265358979323846)

print(f"\n32-bit representation: {single_precision}")
print(f"64-bit representation: {double_precision}")
print(f"Lost digits in 32-bit: {double_precision - single_precision:.10e}")

# Where do those bits go?
print("\nIEEE 754 Standard bit allocation:")
print("32-bit: 1 sign + 8 exponent + 23 fraction bits")
print("64-bit: 1 sign + 11 exponent + 52 fraction bits")
```

The trade-offs are crucial for scientific computing:

| Aspect | 32-bit (float32) | 64-bit (float64) |
|--------|------------------|------------------|
| **Precision** | ~7 decimal digits | ~15 decimal digits |
| **Range** | $\pm 10^{-38}$ to $10^{38}$ | $\pm 10^{-308}$ to $10^{308}$ |
| **Memory** | 4 bytes | 8 bytes |
| **Speed** | Faster on GPU | Standard on CPU |
| **Use case** | Graphics, ML training | Scientific computing |

If you want the actual limits (min/max/eps) instead of memorizing them, use `numpy.finfo`:

```{code-cell} python
import numpy as np
print(np.finfo(np.float32))
print(np.finfo(np.float64))
```

Python defaults to 64-bit because scientific computing needs that precision. But libraries like JAX default to 32-bit for machine learning where speed matters more than precision. For numerical computing with JAX, you can configure it to use 64-bit precision by setting `jax.config.update('jax_enable_x64', True)` at the start of your program. *Always know which precision you're using!*

### Why 0.1 + 0.2 $\neq$ 0.3

Now that you understand bits and precision, let's see why even 64-bit floats can't exactly represent simple decimals.

```{code-cell} python
# The famous example that confuses beginners
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")
print(f"0.1 + 0.2 == 0.3? {result == 0.3}")
print(f"Actual stored value: {result:.17f}")

# Let's see what's really stored
from decimal import Decimal
print(f"\nWhat Python actually stores:")
print(f'As exact decimals (from strings): {Decimal("0.1")}, {Decimal("0.2")}, {Decimal("0.3")}')

# Warning: Decimal(0.1) converts the already-approximated *float* into Decimal.
print(f"From floats (captures float approximation): {Decimal(0.1)}")

# Peek at the exact float representation (hex is exact)
print(f"0.1 as float hex: {(0.1).hex()}")
```

Why does this happen? Just as 1/3 can't be exactly represented in decimal (0.33333...), 1/10 can't be exactly represented in binary. This has crashed spacecraft and corrupted years of simulations!

:::{tip} Check Your Understanding
:class: dropdown

Will this return True or False? Think carefully before testing:

```python
result = 0.1 * 3 == 0.3
```

Make your prediction, then test it. What do you think causes the result?

**Solution:**

This returns `False`! Here's why:

```{code-cell} python
print(f"0.1 * 3 = {0.1 * 3:.17f}")
print(f"0.3 =     {0.3:.17f}")
```

You'll see that `0.1 * 3` gives approximately `0.30000000000000004`, while `0.3` is approximately `0.29999999999999999`. They're different by about $5.5 \times 10^{-17}$ — *tiny* but not zero!

This isn't a quirk — it's fundamental to how every computer on Earth handles decimals. This is why we use `math.isclose()` (see Section @sec-isclose) for floating-point comparisons.
:::

:::{important} Computational Thinking: Representation Limits

Every number system has values it cannot represent exactly. In base 10, we can't write 1/3 exactly. In base 2 (binary), we can't write 1/10 exactly. This isn't a flaw — it's a fundamental property of finite representation.

This pattern appears everywhere in computing:

- JPEG images lose information through compression
- MP3s approximate sound waves
- Floating-point approximates real numbers
- Neural networks approximate functions

Understanding representation limits helps you choose the right tool for each task. The key insight: always assume floating-point arithmetic is approximate, never exact.
:::

### Machine Epsilon: The Smallest Distinguishable Difference

Ready for something mind-blowing? Your computer literally cannot tell the difference between some numbers that are mathematically different! This isn't a flaw — it's a fundamental property of finite systems.

```{code-cell} python
import sys

# Machine epsilon - the fundamental precision limit
epsilon = sys.float_info.epsilon
print(f"Machine epsilon: {epsilon}")
print(f"That's about {epsilon:.2e}")

# Epsilon is a *relative* spacing near 1.0: numbers closer than ~epsilon to 1.0 cannot be distinguished
test1 = 1.0 + epsilon/2
test2 = 1.0 + epsilon

print(f"\nCan Python tell these apart from 1.0?")
print(f"1.0 + epsilon/2 = {test1}, equals 1.0? {test1 == 1.0}")
print(f"1.0 + epsilon   = {test2}, equals 1.0? {test2 == 1.0}")

# This affects scientific calculations
distance_m = 1.496e11  # 1 AU in meters
tiny_change = distance_m * epsilon
print(f"\nAt 1 AU distance ({distance_m:.2e} m):")
print(f"We cannot detect changes smaller than {tiny_change:.2e} m")
print(f"That's about {tiny_change*1e6:.1f} mum (~{tiny_change*1e3:.3f} mm)")
```

:::{warning} Why This Matters: The Patriot Missile Timing Disaster
:class: dropdown

On February 25, 1991, an American Patriot missile battery in Dhahran, Saudi Arabia, failed to intercept an incoming Iraqi Scud missile. The Scud struck an Army barracks, killing 28 soldiers and injuring 98 others. The cause? A tiny numerical error that accumulated over time.

The Patriot's targeting system tracked time using a 24-bit fixed point register, counting in tenths of seconds. However, 1/10 has no exact binary representation—in 24-bit precision, the stored value was actually 0.099999904632568359375, creating an error of approximately 0.000000095 seconds per tenth of a second.

After running continuously for 100 hours (360,000 tenth-second increments), this microscopic error had grown to:

- **Timing error**: 0.34 seconds
- **Range gate error**: ~687 meters (Scud velocity $\approx$ 2,000 m/s)

The Patriot radar system looked in the wrong section of sky and never detected the incoming missile.

**The lesson for scientific computing**: Even "negligible" rounding errors become significant when accumulated over many iterations. Whether you're integrating orbits over millions of timesteps or tracking particles in a simulation, always consider:

1. How errors propagate through iterations
2. Whether your precision is adequate for the timescales involved
3. The difference between relative and absolute error tolerances

[Source: [GAO Report IMTEC-92-26](https://www.gao.gov/products/imtec-92-26)]
:::

(sec-isclose)=
### Safe Floating-Point Comparisons

For values produced by a calculation, do not assume `==` expresses the
scientific comparison you intend. Use a tolerance chosen for the quantity and
claim. Exact equality remains appropriate when exactness is explicitly part of
the contract.

**Stage 1: Understanding the Problem**

```{code-cell} python
# The problem with direct comparison
velocity = 299792458.0  # Speed of light in m/s
calculated = 299792457.9999  # From some calculation

print(f"Velocity: {velocity}")
print(f"Calculated: {calculated}")
print(f"Difference: {velocity - calculated:.2e}")
print(f"Are they equal? {velocity == calculated}")
print("The floats differ, but the relevant question is whether the discrepancy matters.")
```

**Stage 2: Basic Solution**

```{code-cell} python
import math

v1 = 299792458.0
v2 = 299792457.9999

# Absolute tolerance matters when values are near 0 (units matter!)
print(math.isclose(v1, v2, abs_tol=1e-6))
```

**Stage 3: Professional Solution**

```{code-cell} python
# Relative tolerance matters when values scale (percent error)
print(math.isclose(v1, v2, rel_tol=1e-12, abs_tol=0.0))

# In practice you often want both:
print(math.isclose(v1, v2, rel_tol=1e-12, abs_tol=1e-6))

# For arrays, use numpy.isclose / numpy.allclose
```

:::{important} Debug This! Distance Calculator
:class: dropdown

A programmer's distance calculation code produces inconsistent results:

```python
def calculate_distance(parallax_mas):
    """
    Calculate distance from parallax.
    Parallax in milliarcseconds, returns parsecs.
    """
    # Distance in parsecs = 1000 / parallax_in_mas
    distance_pc = 1000.0 / parallax_mas

    return distance_pc

# Test with known value
parallax = 768.5  # milliarcseconds
d_pc = calculate_distance(parallax)

print(f"Distance: {d_pc} pc")

# Verify with known value
known_distance = 1.301  # parsecs
if d_pc == known_distance:
    print("✓ Calculation verified!")
else:
    print("✗ Calculation mismatch!")

# Why does verification always fail even when values look identical?
```

This reciprocal is a useful **high-signal-to-noise geometric point estimate**,
not a general distance-inference procedure. Parallax uncertainties, selection
effects, and negative measured parallaxes require an uncertainty-aware model;
do not silently invert every catalogued parallax.

**Find and fix the three bugs!** Think about:

1. The verification method
2. The reference value (rounding / significant digits)
3. Error propagation

**Solution:**

**Three bugs found:**

**Bug 1: Float comparison with ==**

```python
# WRONG: Never use == with floats
if d_pc == known_distance:

# CORRECT: Use tolerance-based comparison
if abs(d_pc - known_distance) < 0.001:
```

**Bug 2: The reference value is rounded**

```python
# The "known" value is rounded (insufficient significant digits)
print(f"Actual value: {d_pc:.12f}")  # 1000/768.5 approx 1.301236174365
```

**Bug 3: No error handling for zero/negative parallax**

```python
def calculate_distance_safe(parallax_mas):
    """Safe version with validation."""
    if parallax_mas <= 0:
        raise ValueError(f"Parallax must be positive: {parallax_mas}")

    if parallax_mas < 0.1:  # Less than 0.1 mas
        raise ValueError(f"Parallax {parallax_mas} mas too small")

    distance_pc = 1000.0 / parallax_mas

    return distance_pc
```

**Complete fix:**

```python
import math

def verify_distance(calculated, expected, tolerance=0.001):
    """Properly compare floating-point distances."""
    return math.isclose(calculated, expected, rel_tol=0.0, abs_tol=tolerance)

# Now verification works correctly
if verify_distance(d_pc, known_distance):
    print("✓ Calculation verified within tolerance!")
```

**Key lesson:** Floating-point equality is an illusion. Always use tolerance-based comparisons in scientific computing!
:::

---

(sec-hazards)=
## 2.3 Numerical Hazards in Scientific Computing

You've mastered how Python stores numbers — now let's see these concepts in action with real scientific calculations! This is where things get exciting: you're about to learn the techniques that enable precision in spacecraft navigation, sensitive instruments, and scientific simulations.

### Catastrophic Cancellation: When Subtraction Destroys Precision

**Catastrophic cancellation** happens when you subtract nearly equal numbers, eliminating most significant digits and leaving only a few unreliable digits behind.

**Stage 1: The Problem**

```{code-cell} python
import math

# Computing 1 - cos(x) for small x (common in calculations)
x = 1e-8  # Small angle in radians

# Direct computation - catastrophic cancellation!
cos_x = math.cos(x)
result_bad = 1 - cos_x
print(f"Direct: 1 - cos({x}) = {result_bad}")
print(f"This result is completely wrong!")
```

**Stage 2: Understanding Why**

```{code-cell} python
# Let's see what's happening
print(f"cos({x}) = {cos_x:.20f}")
print(f"1.0 =      1.00000000000000000000")
print("At this scale, float64 cannot represent the difference between cos(x) and 1.0,")
print("so cos(x) rounds to exactly 1.0 and 1 - cos(x) becomes 0.0.")

# The true value (from Taylor series)
true_value = x**2 / 2  # For small x, 1-cos(x) approx x^2/2
print(f"\nTrue value: {true_value:.6e}")
print(f"Our result: {result_bad:.6e}")
print(f"Relative error: {abs(result_bad - true_value)/true_value:.1%}")
```

**Stage 3: The Solution**

```{code-cell} python
# Better: use mathematical identity
# 1 - cos(x) = 2sin^2(x/2)
result_good = 2 * math.sin(x/2) ** 2
print(f"Using identity: {result_good:.6e}")
print(f"True value:     {true_value:.6e}")
print(f"Much better! Error: {abs(result_good - true_value)/true_value:.2e}")

# This preserves precision for small angles
```

:::{tip} Two stability power tools: `expm1` and `log1p`

When you see patterns like “something very close to 1” or “`exp(x) - 1` for tiny `x`”, look for functions designed to preserve precision:

- `math.expm1(x)` computes `exp(x) - 1` accurately when `x` is near 0
- `math.log1p(x)` computes `log(1 + x)` accurately when `x` is near 0
:::

:::{tip} Another cancellation “greatest hit”: the quadratic formula

When $b^2 \gg 4ac$, the naive quadratic formula can lose many digits in $-b \pm \sqrt{b^2 - 4ac}$.

```python
import math

def quadratic_roots_stable(a, b, c):
    """Return real roots of ax**2 + bx + c = 0 with reduced cancellation."""
    if a == 0:
        raise ValueError("a must be nonzero for a quadratic")
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None, None

    sqrt_discriminant = math.sqrt(discriminant)
    # copysign makes q use the larger-magnitude numerator. When b is zero,
    # use +sqrt(discriminant) rather than creating q = 0.
    q = -0.5 * (b + math.copysign(sqrt_discriminant, b or 1.0))
    if q == 0:  # repeated root at zero: x**2 = 0
        return 0.0, 0.0
    return q / a, c / q
```

The take-home: if you see subtraction of nearly equal numbers, look for a mathematically equivalent form that avoids it.
:::

### Overflow and Underflow in Extreme Scales

Get ready to work with numbers that break normal intuition! Science deals with scales that push Python to its limits.

**Stage 1: The Overflow Problem**

```{code-cell} python
import math
import numpy as np

print("float64 max:", np.finfo(np.float64).max)

# Overflow can appear in exponential-like growth.
try:
    math.exp(1000)
except OverflowError as e:
    print("Overflow from math.exp(1000):", e)

# Some operations quietly return inf (behavior varies by platform).
try:
    y = 10.0**400
    print("10.0**400 =", y)
    print("Is finite?", math.isfinite(y))
except OverflowError as e:
    print("10.0**400 raised OverflowError:", e)
    print("This platform raises instead of returning inf")
```

**Stage 2: The Solution - Working in Log Space**

```{code-cell} python
import math

# When direct calculation fails (or returns inf), work in log space.
log10_exp_1000 = 1000 / math.log(10)  # log10(exp(1000))
print(f"exp(1000) approx 10^{log10_exp_1000:.1f}")

# A scientific example: total luminosity from many sources
L_sun = 3.828e26  # Solar luminosity (W)
n_stars_galaxy = 1e11  # Stars in a galaxy
n_galaxies = 2e12  # Galaxies in observable universe

log_L_sun = math.log10(L_sun)
log_n_stars = math.log10(n_stars_galaxy)
log_n_galaxies = math.log10(n_galaxies)

# Add logarithms instead of multiplying
log_L_universe = log_L_sun + log_n_stars + log_n_galaxies

print(f"Universe luminosity: 10^{log_L_universe:.1f} W")
print(f"That's 10^{log_L_universe:.1f} watts every second!")
```

:::{important} Computational Thinking: Working in Transformed Space

When direct calculation fails, transform your problem into a space where it succeeds. This universal pattern appears throughout computational science:

- **Log space**: Avoid overflow/underflow in products
- **Fourier space**: Turn convolution into multiplication
- **Spherical coordinates**: Simplify radially symmetric problems
- **Standardized variables**: Compare different scales

The key insight: the same problem can be easy or impossible depending on your representation. When you hit numerical limits, ask yourself whether there's a transformation that makes the problem tractable.

Remember: transforming to a different space isn't cheating — it's often the mathematically correct approach that reveals the true structure of your problem.
:::

:::{warning} Common Bug Alert: Silent Underflow

Unlike **overflow**, **underflow** to zero is silent — no error is raised!

```python
tiny = 1e-200
tinier = tiny * tiny  # Underflows to 0.0 silently!
if tinier == 0:
    print("Warning: Underflow detected!")
```

For products of many positive factors—such as tiny likelihoods—log space is
often the right representation. It is not a universal replacement: addition
in ordinary space becomes `logsumexp` in log space, and quantities that can be
zero or negative require a different treatment.

```{code-cell} python
import math

def logsumexp(log_values):
    """Compute log(sum(exp(value) for value in log_values)) stably."""
    if not log_values:
        raise ValueError("need at least one log value")
    largest = max(log_values)
    return largest + math.log(sum(math.exp(value - largest) for value in log_values))

print(logsumexp([-1000.0, -1001.0]))  # finite, despite exp(-1000) underflowing
```
:::

### Defensive Programming with Numerical Checks

You've seen the challenges — now here's your toolkit for conquering them! Defensive programming protects every major scientific data pipeline.

**Stage 1: Basic Validation**

```{code-cell} python
def validate_positive(value, name="value"):
    """Ensure value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive: {value}")
    return value

# Example use
mass = validate_positive(1.989e30, "stellar mass")
print(f"Valid mass: {mass:.2e} kg")
```

**Stage 2: Safe Division**

```{code-cell} python
def safe_divide(a, b, *, abs_tol=0.0):
    """
    Division with protection against near-zero denominators.

    Choose abs_tol based on your problem's scale and units (domain decision).
    """
    if abs(b) <= abs_tol:
        raise ValueError(f"Division by near-zero denominator: {b:.2e}")
    return a / b

# Test with safe division
G = 6.67e-11
M = 1.989e30
r = 1.496e11
force = safe_divide(G * M, r * r)
print(f"Gravitational acceleration: {force:.2e} m/s^2")
```

**Stage 3: Complete Validation**

```{code-cell} python
import math

def validate_magnitude(value, name="value", max_exp=100):
    """Ensure value is reasonable for scientific calculations."""
    if value == 0:
        return value

    if not math.isfinite(value):
        raise ValueError(f"{name} is not finite: {value}")

    log_val = abs(math.log10(abs(value)))
    if log_val > max_exp:
        raise ValueError(f"{name} has unreasonable magnitude: {value:.2e}")

    return value

# Test validation
L_sun = 3.828e26
test_value = validate_magnitude(L_sun, "luminosity", max_exp=50)
print(f"Validated luminosity: {test_value:.2e} W")
```

---

## 2.4 Complex Numbers for Wave Physics

Welcome to one of the most elegant corners of mathematics! **Complex numbers** might sound intimidating, but they're actually your gateway to understanding wave physics, signal processing, and Fourier analysis. Python handles complex numbers as naturally as integers.

```{code-cell} python
# Complex numbers in Python use 'j' for the imaginary unit
z = 3 + 4j
print(f"Complex number: {z}")
print(f"Real part: {z.real}")
print(f"Imaginary part: {z.imag}")
print(f"Magnitude: {abs(z)}")

# Euler's formula - the most beautiful equation in mathematics
import math
import cmath
euler = cmath.exp(1j * cmath.pi)
print(f"\ne^(ipi) = {euler.real:.0f}")
print(f"Tiny imaginary part {euler.imag:.2e} is just rounding error")

# Phase calculation (useful for wave interference)
phase = cmath.phase(z)
print(f"\nPhase of {z}: {phase:.3f} radians")
print(f"That's {math.degrees(phase):.1f} degrees")
```

Guardrail: most functions in `math` do **not** accept complex numbers. If you might have complex values, use `cmath` (or NumPy’s complex-aware functions).

Complex numbers aren't just mathematical abstractions — they're essential for:

- Fourier transforms (spectral analysis)
- Quantum mechanics (wave functions)
- Signal processing (interferometry)

:::{important} Computational Thinking: Complex Numbers as 2D Vectors

Think of complex numbers as 2D vectors that know how to multiply:

- **Addition**: vector addition
- **Multiplication**: rotation and scaling
- **Magnitude**: vector length
- **Phase**: angle from positive real axis

This pattern — representing compound data as single objects with rich behavior — appears throughout scientific computing. Master this concept here, and you'll recognize it everywhere!
:::

:::{important} Why This Matters: Fourier Transforms Reveal Hidden Periods
:class: dropdown

Complex numbers aren't just mathematical elegance—they're essential for discovering patterns in data! The Fourier transform, which relies entirely on complex exponentials, transforms time-series measurements into frequency space, revealing hidden periodicities.

**Real Research Application:**

Finding periodic signals in noisy data requires Fourier analysis:

```python
# Simplified signal detection
import numpy as np

# Time series: signal over time
time = np.linspace(0, 100, 10000)  # 100 units
# Hidden signal: 3.5 unit period, small amplitude
signal = 1.0 - 0.0001 * np.cos(2*np.pi*time/3.5)
# Add noise
rng = np.random.default_rng(42)
noise = rng.normal(0, 0.0005, len(time))
data = signal + noise

# Fourier transform uses complex exponentials
frequencies = np.fft.fftfreq(len(time), time[1]-time[0])
fft = np.fft.fft(data - np.mean(data))
power = np.abs(fft)**2  # Complex magnitude squared

# Peak in power spectrum reveals hidden period!
peak_idx = np.argmax(power[1:len(power)//2]) + 1
detected_period = 1/frequencies[peak_idx]
print(f"Detected period: {detected_period:.2f}")
```

Every periodogram you'll ever compute—whether finding oscillation modes, orbital periods, or rotation rates—depends on complex arithmetic.

**The bottom line:** Master complex numbers now, because every time-series analysis technique you'll learn builds on them!
:::

---

## 2.5 Variables and Dynamic Typing

Now that you understand how Python represents numbers, let's see how it manages them! Variables in Python are names that refer to objects, not containers that hold values. This distinction matters:

```{code-cell} python
# Variables are references, not containers
stellar_mass = 1.989e30  # Solar mass in kg
solar_mass = stellar_mass  # Both names refer to the SAME number

print(f"stellar_mass: {stellar_mass:.2e} kg")
print(f"solar_mass: {solar_mass:.2e} kg")
print(f"Same object? {stellar_mass is solar_mass}")

# Warning: `is` checks object identity, not numeric equality. Don't use it for comparisons!
print(f"Numerically equal? {stellar_mass == solar_mass}")

# But numbers are immutable, so this is safe
stellar_mass = stellar_mass * 2  # Creates NEW number
print(f"\nAfter doubling stellar_mass:")
print(f"stellar_mass: {stellar_mass:.2e} kg")
print(f"solar_mass (unchanged): {solar_mass:.2e} kg")
```

Python is dynamically typed — variables can refer to any type of object:

```{code-cell} python
# Dynamic typing in action
observation = 42  # Integer
print(f"Type: {type(observation).__name__}, Value: {observation}")

observation = 42.0  # Now a float
print(f"Type: {type(observation).__name__}, Value: {observation}")

observation = "42 measurements"  # Now a string
print(f"Type: {type(observation).__name__}, Value: {observation}")

# This flexibility is powerful but requires discipline
# In scientific code, changing types unexpectedly is usually a bug!
```

---

## 2.6 Strings and Scientific Output Formatting

Time to make your results shine! Clear output formatting isn't just about aesthetics — it's about scientific communication. The formatting skills you learn here will help you create publication-quality output.

```{code-cell} python
# Basic f-string formatting
star_name = "Betelgeuse"
distance_ly = 400
luminosity = 1.2e5  # Solar luminosities

print(f"{star_name} is {distance_ly} light-years away")
print(f"Luminosity: {luminosity:.2e} Lsun")
```

### Format Specifications for Scientific Data

**F-strings** support sophisticated formatting perfect for scientific output:

```{code-cell} python
# Comprehensive formatting examples
value = 1234.56789

print(f"Fixed-point (2 decimals): {value:.2f}")
print(f"Scientific notation: {value:.2e}")
print(f"Width 10, 2 decimals: {value:10.2f}")
print(f"Thousands separator: {value:,.0f}")

# Create a formatted table of data
stars = [
    ("Sirius", -1.46, 8.6),
    ("Canopus", -0.74, 310),
    ("Arcturus", -0.05, 37),
]

print(f"\n{'Star':<10} {'Magnitude':>10} {'Distance (ly)':>15}")
print("-" * 37)
for name, mag, dist in stars:
    print(f"{name:<10} {mag:>10.2f} {dist:>15.1f}")
```

:::{tip} Check Your Understanding
:class: dropdown

What will this print?

```python
redshift = 0.00123456
print(f"z = {redshift:.2e}")
```

Predict the format before running it.

**Solution:**

This prints: `z = 1.23e-03`

The `.2e` format specifier means:

- Use scientific notation (e)
- Show 2 digits after the decimal point
- Python automatically handles the exponent

So 0.00123456 becomes 1.23 $\times$ $10^{-3}$, displayed as 1.23e-03.
:::

---

## 2.7 Type System and Conversions

Python's type system strikes a perfect balance — flexible enough for rapid exploration but strong enough to catch errors. Understanding types and conversions is crucial for handling data from any source.

```{code-cell} python
# Type checking
value = 3.14159
print(f"Type of {value}: {type(value).__name__}")
print(f"Is it a float? {isinstance(value, float)}")

# Type conversion
text = "2.718"
number = float(text)
print(f"\nConverted '{text}' to {number}")

# Dangerous conversion - truncation!
print(f"\nint(3.9) = {int(3.9)}")  # Truncates, doesn't round!
print(f"round(3.9) = {round(3.9)}")  # Use this for rounding
```

:::{tip} Check Your Understanding
:class: dropdown

What happens when you convert -3.7 to an integer? Predict the result:

a) -4 (rounds to nearest integer)
b) -3 (truncates toward zero)
c) -3 (floors toward negative infinity)
d) Error

**Solution:**

The answer is b) -3 (truncates toward zero).

Python's `int()` truncates toward zero, not toward negative infinity like floor division!

```{code-cell} python
print(f"int(-3.7) = {int(-3.7)}")    # Gives -3 (toward zero)
print(f"-3.7 // 1 = {-3.7 // 1}")    # Gives -4.0 (toward -infinity)
```

This inconsistency has caused numerous bugs in calculations where negative values represent positions before an epoch.
:::

---

## 2.8 The Math Module: Your Scientific Calculator

Here comes the fun part — Python's math module transforms your computer into a scientific calculator more powerful than anything that existed when we sent humans to the Moon!

```{code-cell} python
import math

# Fundamental constants
print(f"pi = {math.pi}")
print(f"e = {math.e}")
print(f"tau = {math.tau}")  # tau = 2pi, useful for circular motion

# Trigonometry (always in radians!)
angle_degrees = 30
angle_radians = math.radians(angle_degrees)
print(f"\nsin(30 deg) = {math.sin(angle_radians):.4f}")
print(f"cos(30 deg) = {math.cos(angle_radians):.4f}")

# Logarithms for magnitude calculations
flux_ratio = 100
magnitude_diff = 2.5 * math.log10(flux_ratio)
print(f"\nFlux ratio {flux_ratio} = {magnitude_diff:.1f} magnitudes")

# Special functions
print(f"\nGamma(5) = {math.gamma(5)} = 4!")
print(f"Error function: erf(1) = {math.erf(1):.4f}")

# Numerically stable helpers you will reuse constantly
x = 1e-10
print(f"\nexp(x)-1 naive: {math.exp(x) - 1:.3e}")
print(f"expm1(x) stable: {math.expm1(x):.3e}")

y = 1e-10
print(f"log(1+y) naive: {math.log(1 + y):.3e}")
print(f"log1p(y) stable: {math.log1p(y):.3e}")

# Stable vector magnitude (avoids overflow/underflow in sqrt(x**2 + y**2))
print(f"\nhypot(3,4) = {math.hypot(3, 4)}")

# Stable summation when adding many floats
vals = [1e16, 1.0, -1e16]
print(f"sum(vals) = {sum(vals)}")
print(f"math.fsum(vals) = {math.fsum(vals)}")
```

**Remember:** trigonometric functions use radians, not degrees! This is a constant source of bugs in scientific code.

---

## 2.9 From Interactive to Script

Congratulations! You've been exploring Python interactively, testing ideas and learning how numbers behave. Now let's transform your interactive explorations into a reusable script:

```python
#!/usr/bin/env python
"""
schwarzschild_radius.py
Calculate Schwarzschild radius with proper numerical handling.

Constants below are rounded for pedagogy. For high-precision work, use a
consistent constants set (e.g., CODATA via astropy.constants).
"""

import math

def schwarzschild_radius_simple(mass_kg):
    """Calculate Schwarzschild radius in m."""
    G = 6.67e-11   # m^3/kg/s^2
    c = 2.998e8    # m/s

    rs = 2 * G * mass_kg / c**2
    return rs

def schwarzschild_radius_validated(mass_kg):
    """Calculate with input validation."""
    G = 6.67e-11
    c = 2.998e8

    if mass_kg <= 0:
        raise ValueError(f"Mass must be positive: {mass_kg}")

    rs = 2 * G * mass_kg / c**2
    return rs

def schwarzschild_radius_robust(mass_kg):
    """Handle extreme masses using log space."""
    G = 6.67e-11
    c = 2.998e8

    if mass_kg <= 0:
        raise ValueError(f"Mass must be positive")

    # Use log space for extreme masses
    if mass_kg > 1e45:  # Galaxy cluster scale
        log_rs = math.log10(2*G) + math.log10(mass_kg) - 2*math.log10(c)
        return 10**log_rs

    return 2 * G * mass_kg / c**2

# Test our functions
if __name__ == "__main__":
    test_masses = {
        "Earth": 5.972e24,
        "Sun": 1.989e30,
        "Sgr A*": 8.2e36,
    }

    for name, mass in test_masses.items():
        rs = schwarzschild_radius_robust(mass)
        print(f"{name}: Rs = {rs:.2e} m ({rs/1e3:.2f} km)")
```

---

## Main Takeaways

You've just built the foundation for all numerical computing you'll ever do. The seemingly simple act of adding two numbers opens a universe of complexity that affects every calculation from simulations to data analysis. The key insight isn't that floating-point arithmetic is broken — it's that it's approximate by design, and understanding these approximations separates successful computational scientists from those who publish retracted papers due to numerical errors.

The defensive programming techniques you learned here might seem overcautious at first, but they're battle-tested practices from real scientific software. That `safe_divide` function has prevented countless divide-by-zero errors in production code. The validation checks have caught bugs that would have wasted weeks of supercomputer time. Working in log space isn't just a clever trick — for many calculations spanning extreme scales, it's the only way to get meaningful answers.

Perhaps most importantly, you've learned to think about numbers the way computers do. When you see `0.1 + 0.2`, you now know it's not exactly 0.3, and more crucially, you know why. When you calculate values over many orders of magnitude, you instinctively think about whether the number might overflow. When you subtract two nearly-equal values, alarm bells ring about catastrophic cancellation. This numerical awareness will serve you throughout your career.

---

## Key Takeaways

✓ Floating-point arithmetic is approximate by design — use a claim-appropriate tolerance for computed quantities; use `==` only when exact equality is the stated contract

✓ Machine epsilon (~2.2e-16) sets the fundamental precision limit for calculations

✓ Catastrophic cancellation occurs when subtracting nearly equal numbers — use mathematical identities

✓ Work in log space to handle extreme scales without overflow/underflow

✓ Python integers have unlimited precision but use more memory than floats

✓ Variables are references to objects, not containers holding values

✓ Defensive programming with validation prevents numerical disasters

✓ F-strings provide powerful formatting for scientific output

✓ Complex numbers are essential for wave physics and spectral analysis

✓ Always use radians with trigonometric functions

✓ Type conversion can lose information — always validate

---

## Quick Reference Tables

### Math Module Functions

**Mathematical Constants**

```python
import math
```

- `math.pi` - $\pi$ (3.14159...)
- `math.e` - Euler's number (2.71828...)
- `math.tau` - $\tau$ = 2$\pi$ (6.28318...)

**Arithmetic Functions**

- `math.sqrt(x)` - Square root
- `math.log(x)` - Natural logarithm
- `math.log1p(x)` - `log(1+x)` accurate for small `x`
- `math.log10(x)` - Base-10 logarithm
- `math.exp(x)` - Exponential (e^x)
- `math.expm1(x)` - `exp(x)-1` accurate for small `x`
- `math.hypot(x, y)` - Stable `sqrt(x^2 + y^2)`
- `math.fsum(iterable)` - Stable summation of many floats

**Trigonometric Functions** (use radians!)

- `math.sin(x)`, `math.cos(x)`, `math.tan(x)` - Basic trig
- `math.radians(degrees)` - Convert degrees to radians
- `math.degrees(radians)` - Convert radians to degrees

**Special Functions**

- `math.gamma(x)` - Gamma function
- `math.erf(x)` - Error function
- `math.isclose(a, b, rel_tol=1e-9)` - Safe float comparison
- `math.isfinite(x)` - Check if finite (not inf or nan)
- `math.isnan(x)` - Check if Not-a-Number

### F-String Format Specifiers

| Format | Meaning | Example | Result |
|--------|---------|---------|--------|
| `:.2f` | Fixed decimal | `f"{3.14159:.2f}"` | `3.14` |
| `:.2e` | Scientific notation | `f"{1234:.2e}"` | `1.23e+03` |
| `:10.2f` | Width and decimals | `f"{3.14:10.2f}"` | `      3.14` |
| `:,.0f` | Thousands separator | `f"{1234567:,.0f}"` | `1,234,567` |
| `:<10` | Left align | `f"{'test':<10}"` | `test      ` |
| `:>10` | Right align | `f"{'test':>10}"` | `      test` |
| `:^10` | Center align | `f"{'test':^10}"` | `   test   ` |

### Type Checking and Conversion

| Function | Purpose | Example |
|----------|---------|---------|
| `type(x)` | Get object type | `type(3.14)` $\to$ `<class 'float'>` |
| `isinstance(x, type)` | Check type | `isinstance(3.14, float)` $\to$ `True` |
| `float(x)` | Convert to float | `float("3.14")` $\to$ `3.14` |
| `int(x)` | Convert to int (truncates!) | `int(3.9)` $\to$ `3` |
| `complex(r, i)` | Create complex | `complex(3, 4)` $\to$ `(3+4j)` |
| `round(x, n)` | Round to n decimals | `round(3.14159, 2)` $\to$ `3.14` |

---

## Next Chapter Preview

Armed with a deep understanding of Python's numeric types and the perils of floating-point arithmetic, you're ready for Chapter 3: Control Flow & Logic. You'll learn to make your code dynamic with `if`-statements and loops, building algorithms that can adapt to data and iterate until convergence. The numerical foundations from this chapter become essential when you're checking whether a calculation has converged, comparing values within tolerance, or detecting numerical instabilities in your simulations. Get ready to transform static calculations into intelligent algorithms that can make decisions and repeat tasks — the essence of computational thinking.
