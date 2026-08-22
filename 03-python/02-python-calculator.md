---
title: "Chapter 2: Python as Your Scientific Calculator"
subtitle: "Scientific Computing with Python"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
site:
  hide_outline: true
---

## Learning objectives

By the end of this chapter, you will be able to:

- [ ] **(1) Write and interpret an arithmetic calculation with explicit grouping, units-aware names, and a dimensional check.**
- [ ] **(2) Explain why floating-point results are finite approximations and identify when exact equality is—and is not—the intended contract.**
- [ ] **(3) Choose and justify an absolute tolerance, relative tolerance, or both for a stated numerical claim.**
- [ ] **(4) Diagnose cancellation, overflow, underflow, and non-finite values; choose an appropriate stable representation or test.**
- [ ] **(5) State what a numerical check establishes and what still requires a scientific model, uncertainty analysis, or independent validation.**

## Prerequisites

:::{note} Before Starting This Chapter

- [ ] You can start a Python session or run a short script.
- [ ] You know that the interpreter and packages that produced a result should be recorded (Chapter 1).

IPython and Conda are useful optional tools, not prerequisites for the reasoning
in this chapter. If Python is not yet available, return after completing the
setup path appropriate to your computer.
:::

---

## Why this chapter matters

Now that you can identify the computational environment that ran your code,
it's time to use Python as a scientific calculator. But this chapter goes far
beyond simple arithmetic: a numerical result can look precise while still being
an inappropriate representation, comparison, or scientific conclusion.

You'll learn why spacecraft have crashed, why some calculations fail catastrophically, and how to write code that handles extreme scales — from the quantum level at $10^{-35}$ meters to the cosmological scale at $10^{26}$ meters. The floating-point precision issues we explore here aren't academic exercises; they're the source of real bugs that have corrupted simulations, invalidated published results, and caused navigation errors costing hundreds of millions of dollars.

These fundamentals build numerical intuition: the habit of asking what a
calculation supports before treating its output as evidence. Every simulation,
dataset, and statistical test later in the course relies on that habit.

:::{important} Research practice: before trusting a numerical claim

Before trusting a numerical result, quickly ask:

- **Scale:** What order(s) of magnitude are the inputs and outputs?
- **Representation:** Should this be `int`, `float64`, `float32`, `Decimal`, or `complex`?
- **Stability:** Am I subtracting nearly equal numbers? Summing many terms? Repeating an update many times?
- **Propagation:** Will small errors accumulate (iterations, long integrations, long time series)?
- **Comparison:** Should I compare with absolute tolerance, relative tolerance, or both?
- **Diagnostics:** What are the dtypes? Are values finite (`math.isfinite`, `np.isfinite`)? Any `nan`/`inf`?
:::

:::{note} How to Use This Chapter

For a first reading, follow this route:

1. [Make an arithmetic calculation legible](#legible-calculation).
2. [Choose a comparison that matches a claim](#floating-comparisons).
3. [Diagnose a numerical hazard](#numerical-hazards).
4. [Investigate the numerical-claim case file](#numerical-claim-case-file).

The bit-level representation discussion, Patriot story, complex numbers,
formatting, type conversion, and `math` catalog remain useful **Deep Dive** or
**Reference** material. Return when a concrete calculation gives you a reason
to need them; they are not hidden prerequisites.
:::

## Try this chapter

- [**Browser Python lab · Numerical Claim Inspector**](jupyterlite/ch02-numerical-claim-inspector.html): vary a small angle and a stated measurement resolution, then decide which numerical claim is warranted. The activity is optional; the static cancellation and comparison examples below remain complete without browser Python.

[Return to the Part I guide](index.md) when choosing a first-reading route.

---

(legible-calculation)=
## 2.1 Core: make an arithmetic calculation legible

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

### Operator precedence and dimensions: a source of real bugs

Python follows PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction), but relying on memorized rules causes expensive errors. Let's see this with a real calculation:

```{code-cell} python
# Calculate orbital velocity: v = sqrt(GM/r)
# Using SI units
# (Constants are rounded for pedagogy; for research, prefer astropy.constants.)
G = 6.67e-11   # Gravitational constant (m^3 kg^-1 s^-2)
M = 1.989e30  # Solar mass (kg)
r = 1.496e11  # 1 AU (m)

# WRONG - grouping error. This expression is not even a velocity:
# (G M) / sqrt(r) has units m^(5/2) / s^2.
expression_wrong = G * M / r ** 0.5
print(f"Wrong expression: {expression_wrong:.2e} m^(5/2)/s^2 (not a velocity)")

# CORRECT - parentheses clarify intent
v_right = (G * M / r) ** 0.5
print(f"Correct velocity: {v_right:.2e} m/s")
print(f"That's {v_right/1e3:.1f} km/s - Earth's orbital speed!")

# Parentheses make the equation and the units inspectable.
```

The wrong version calculated $(GM/\sqrt{r})$ instead of $\sqrt{(GM/r)}$.
The numerical magnitude is alarming, but the more decisive diagnostic comes
first: its dimensions are not velocity. A physically meaningful variable name
and a dimensional check can catch this mistake before comparison with a known
orbital speed.

:::{important} Design decision: names and grouping carry scientific meaning

Use names such as `radius_m`, `mass_kg`, and `velocity_m_s` when a quantity's
unit matters. Parentheses are not merely decoration: in a scientific expression
they document the model's grouping and make a dimensional check possible.
:::

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

:::{important} Common Bug Alert: Negative Floor Division

Floor division with negative numbers often surprises programmers calculating phases or time intervals before an epoch. When working with values that can be negative, always test your edge cases or use `int(a/b)` for truncation toward zero.
:::

---

(number-representation)=
## 2.2 Core: finite representation and numerical agreement

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

On the usual CPython platforms, a Python `float` is an IEEE 754 binary64 value:
64 bits split into sign (1 bit), exponent (11 bits), and a **fraction field**
(52 stored bits). For normal (non-subnormal) numbers there is an implicit
leading 1, so you get about **53 bits of significand precision** (roughly
**15–16 decimal digits**). Inspect `sys.float_info` on an unfamiliar platform
rather than assuming an implementation detail.

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
| **Largest finite magnitude** | about $3.4\times10^{38}$ | about $1.8\times10^{308}$ |
| **Memory** | 4 bytes | 8 bytes |
| **Performance** | Hardware- and workload-dependent; may reduce memory use and help on supported accelerators | Hardware- and workload-dependent; often chosen when its additional precision is required |
| **Common use** | Graphics and some machine-learning workloads | Many scientific calculations with a demanding error budget |

If you want the actual limits (min/max/eps) instead of memorizing them, use `numpy.finfo`:

```{code-cell} python
import numpy as np
print(np.finfo(np.float32))
print(np.finfo(np.float64))
```

Python's ordinary `float` is typically binary64. Array libraries may offer—or
default to—other dtypes; for example, JAX commonly runs with 64-bit values
disabled unless its configuration enables them. *Always inspect the precision
your calculation is actually using.* Choose a dtype from the error and range
your calculation can tolerate, then measure performance on the hardware and
workload you actually plan to use.

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

Why does this happen? Just as 1/3 cannot be exactly represented in decimal
($0.33333\ldots$), 1/10 cannot be exactly represented in binary. The lesson is
not that every small rounding difference causes a failure; it is that a
calculation needs a comparison rule connected to the decision being made.

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

This is not a quirk—it follows from finite binary representation. Use
[`math.isclose()`](#floating-comparisons) only after deciding what numerical
agreement means for the quantity and claim at hand.
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

### Deep Dive: machine epsilon and local spacing

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
print(f"A representative binary64 spacing at this scale is about {tiny_change:.2e} m")
print(f"That's about {tiny_change*1e6:.1f} micrometres (~{tiny_change*1e3:.3f} mm)")
```

:::{tip} The More You Know: The Patriot Missile Timing Disaster
:class: dropdown

On February 25, 1991, an American Patriot missile battery in Dhahran, Saudi Arabia, failed to intercept an incoming Iraqi Scud missile. The Scud struck an Army barracks, killing 28 soldiers and injuring 98 others. The cause? A tiny numerical error that accumulated over time.

The Patriot's targeting system tracked time using a 24-bit fixed point register, counting in tenths of seconds. However, 1/10 has no exact binary representation—in 24-bit precision, the stored value was actually 0.099999904632568359375, creating an error of approximately 0.000000095 seconds per tenth of a second.

After running continuously for 100 hours (3,600,000 tenth-second increments), this microscopic error had grown to:

- **Timing error**: 0.34 seconds
- **Range gate error**: ~687 meters (Scud velocity $\approx$ 2,000 m/s)

The Patriot radar system looked in the wrong section of sky and never detected the incoming missile.

**The lesson for scientific computing**: Even "negligible" rounding errors become significant when accumulated over many iterations. Whether you're integrating orbits over millions of timesteps or tracking particles in a simulation, always consider:

1. How errors propagate through iterations
2. Whether your precision is adequate for the timescales involved
3. The difference between relative and absolute error tolerances

[Source: [GAO Report IMTEC-92-26](https://www.gao.gov/products/imtec-92-26)]
:::

(floating-comparisons)=
## 2.3 Core: choose a comparison that matches a claim

For values produced by a calculation, do not assume `==` expresses the
scientific comparison you intend. Use a tolerance chosen for the quantity and
claim. Exact equality remains appropriate when exactness is explicitly part of
the contract.

**Stage 1: name the claim and its scale.**

```{code-cell} python
# The problem with direct comparison
expected_offset_m_s = 0.0
measured_offset_m_s = 0.0001  # A computed residual, in m/s

print(f"Expected offset: {expected_offset_m_s} m/s")
print(f"Measured offset: {measured_offset_m_s:.2e} m/s")
print(f"Exactly equal? {measured_offset_m_s == expected_offset_m_s}")
print("The relevant question is whether this residual is resolvable for this measurement.")
```

**Stage 2: an absolute tolerance near zero.**

```{code-cell} python
import math

measurement_resolution_m_s = 0.001

# Near zero, state a tolerance in the measurement's units and turn off the
# default relative tolerance so this line demonstrates the intended rule.
print(math.isclose(
    measured_offset_m_s,
    expected_offset_m_s,
    rel_tol=0.0,
    abs_tol=measurement_resolution_m_s,
))
```

**Stage 3: a relative tolerance for a scale-dependent quantity.**

```{code-cell} python
predicted_flux = 2.00e-14
measured_flux = 2.03e-14
fractional_precision = 0.02  # 2%; supplied by this illustrative measurement contract

print(math.isclose(measured_flux, predicted_flux, rel_tol=fractional_precision, abs_tol=0.0))

# Use both tolerances only when both an absolute resolution and a fractional
# requirement are independently meaningful. For arrays, use numpy.isclose/allclose.
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

**Find and fix the three problems.** Think about:

1. The verification method
2. The reference value (rounding / significant digits)
3. Which conclusion the reciprocal can and cannot support

**Solution:**

**Three bugs found:**

**Problem 1: The comparison does not state a tolerance contract.**

```python
# Exact equality is not the intended contract here.
if d_pc == known_distance:

# A display rounded to 0.001 pc justifies only this display-level check.
if math.isclose(d_pc, known_distance, rel_tol=0.0, abs_tol=0.0005):
```

**Problem 2: The reference value is rounded.**

```python
# The "known" value is rounded (insufficient significant digits)
print(f"Actual value: {d_pc:.12f}")  # 1000/768.5 approx 1.301236174365
```

**Problem 3: A geometric reciprocal is not a general distance inference.**

```python
def parallax_point_estimate_pc(parallax_mas):
    """Geometric point estimate for a positive, high-signal-to-noise parallax."""
    if parallax_mas <= 0:
        raise ValueError(f"Parallax must be positive: {parallax_mas}")
    return 1000.0 / parallax_mas
```

Negative parallaxes and low-signal-to-noise measurements are not repaired by an
arbitrary cutoff such as `0.1` mas. They require an uncertainty-aware inference
model. For small fractional uncertainty, propagation gives
$\sigma_d \approx 1000\sigma_p / p^2$; that approximation and its regime must
be recorded beside any claim about distance.

**A bounded verification:**

```python
import math

one_parsec = parallax_point_estimate_pc(1000.0)
assert math.isclose(one_parsec, 1.0, rel_tol=0.0, abs_tol=1e-12)

print("✓ The reciprocal passes the constructed 1000 mas → 1 pc check.")
```

**Key lesson:** Choose a tolerance because the quantity, units, uncertainty, or
decision supplies one. A passing numerical comparison tests that stated
contract; it does not validate the underlying distance model.
:::

---

(numerical-hazards)=
## 2.4 Core: numerical hazards in scientific computing

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

# The leading small-angle approximation is useful for scale, but it is not the
# exact value of 1 - cos(x).
small_angle_approximation = x**2 / 2
print(f"\nSmall-angle approximation: {small_angle_approximation:.6e}")
print(f"Our result: {result_bad:.6e}")
print(f"Loss relative to the small-angle scale: {abs(result_bad - small_angle_approximation)/small_angle_approximation:.1%}")
```

**Stage 3: The Solution**

```{code-cell} python
# Better: use mathematical identity
# 1 - cos(x) = 2sin^2(x/2)
result_good = 2 * math.sin(x/2) ** 2
print(f"Using identity: {result_good:.6e}")
print(f"Small-angle approximation: {small_angle_approximation:.6e}")
print("The identity is algebraically equivalent to 1 - cos(x), but avoids the subtraction.")

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

# Scalar Python operations and array-library operations can signal overflow
# differently; inspect the API you are actually using.
try:
    y = 10.0**400
    print("10.0**400 =", y)
    print("Is finite?", math.isfinite(y))
except OverflowError as e:
    print("10.0**400 raised OverflowError:", e)
    print("This scalar Python operation raises instead of returning inf")
```

**Stage 2: The Solution - Working in Log Space**

```{code-cell} python
import math

# When direct calculation fails (or returns inf), work in log space.
log10_exp_1000 = 1000 / math.log(10)  # log10(exp(1000))
print(f"exp(1000) approx 10^{log10_exp_1000:.1f}")

# A deliberately crude scale estimate: assume every star has solar luminosity.
# It illustrates products in log space; it is not an estimate of the observed
# luminosity of the Universe.
L_sun = 3.828e26  # Solar luminosity (W)
n_stars_galaxy = 1e11  # Stars in a galaxy
n_galaxies = 2e12  # Galaxies in observable universe

log_L_sun = math.log10(L_sun)
log_n_stars = math.log10(n_stars_galaxy)
log_n_galaxies = math.log10(n_galaxies)

# Add logarithms instead of multiplying
log_L_universe = log_L_sun + log_n_stars + log_n_galaxies

print(f"Universe luminosity: 10^{log_L_universe:.1f} W")
print(f"Under the stated toy assumption: 10^{log_L_universe:.1f} W")
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

:::{important} Common Bug Alert: Silent Underflow

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
    """Compute log(sum(exp(value) for value in log_values)) stably.

    Finite inputs and ``-inf`` are supported; NaNs propagate.
    """
    if not log_values:
        raise ValueError("need at least one log value")
    largest = max(log_values)
    if largest == -math.inf:
        return -math.inf
    return largest + math.log(sum(math.exp(value - largest) for value in log_values))

print(logsumexp([-1000.0, -1001.0]))  # finite, despite exp(-1000) underflowing
```
:::

(numerical-claim-case-file)=
## Core check: investigate a numerical claim

An analysis note reports: “The computed offset is $10^{-4}$ m/s, therefore the
instrument has no measurable bias.” The calculation used binary64 values; the
instrument resolution is $10^{-3}$ m/s; and no uncertainty model, calibration
record, or independent standard is supplied.

:::{tip} Check Your Understanding
:class: dropdown

Before reading the answer, write down:

1. Which statement is supported by the stated numerical comparison?
2. Which tolerance belongs in that comparison, and why?
3. What additional evidence would be needed before claiming that the instrument
   has no bias?

**Answer.** The calculation supports the limited statement that the reported
offset is within the stated $10^{-3}$ m/s resolution, assuming that resolution
is the relevant acceptance criterion. An absolute tolerance is appropriate
because the comparison is to zero in m/s. It does **not** establish that the
instrument has no bias: that needs a calibration model, uncertainty budget,
and comparison against an appropriate standard. Numerical agreement and
scientific validation are related but different claims.
:::

:::::{admonition} Browser Python lab · Numerical Claim Inspector
:class: tip

**Predict.** For which small angles will direct `1 - cos(x)` lose the scale of
the result in binary64? If a residual is $10^{-4}$ m/s and the measurement
resolution is $10^{-3}$ m/s, what can you conclude?

**Act.** In the browser lab, change the angle and resolution, compare direct
and stable forms, then state the narrowest conclusion supported by the result.

**Observe.** A stable representation can preserve a calculation that direct
subtraction loses; a passing tolerance comparison still does not prove a model
or instrument correct.

**Limit.** The lab does not supply an uncertainty model, calibration data, or a
universal tolerance. Those are scientific decisions outside the calculation.

[Open the Numerical Claim Inspector →](jupyterlite/ch02-numerical-claim-inspector.html)
:::::

## Reference: numerical guard patterns

Defensive programming is not a catalog of universal numeric bounds. A useful
guard names the quantity and units, the numerical failure it prevents, and the
consequence of failure. For example, a positive mass can be checked before a
square root because the physical model requires it; a near-zero denominator
requires a threshold justified by the scale of the numerator and the decision
the quotient supports. An arbitrary `max_exp=100` is not validation.

The durable pattern is **state a model-specific expectation → test it → record
what happened → decide whether the result is usable**. Later chapters develop
convergence, bounded iteration, and test design with concrete numerical models.

---

(complex-numbers)=
## Deep Dive: complex numbers for wave physics

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

::::{important} Why This Matters: Fourier Transforms Reveal Hidden Periods
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

:::{important} Modeling boundary: a Fourier peak is not a discovery

This evenly sampled toy signal has a planted period and no window function,
systematic errors, false-alarm calculation, or competing models. A peak can be
useful evidence; it does not by itself establish that a physical period exists.
The Deep Dive shows why complex arithmetic appears in the calculation, not how
to make a detection claim from real survey data.
:::

**The bottom line:** Complex arithmetic gives a compact representation for
amplitude and phase. Later chapters return to arrays, sampling, and evidence
needed for a defensible time-series claim.
::::

---

(numeric-reference)=
## Reference: values, types, and scientific output

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

### Strings and scientific output formatting

Clear output formatting is not just aesthetics—it is scientific communication.
Formatting makes a value readable, but it cannot create precision absent from
the measurement, calculation, or uncertainty record.

```{code-cell} python
# Basic f-string formatting
star_name = "Betelgeuse"
distance_ly = 400
luminosity = 1.2e5  # Solar luminosities

print(f"{star_name} is {distance_ly} light-years away")
print(f"Luminosity: {luminosity:.2e} Lsun")
```

#### Format specifications for scientific data

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

### Type system and conversions

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

### Selected `math` tools

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

# Numerically stable helpers: use an input that makes the difference visible.
x = 1e-16
print(f"\nexp(x)-1 naive: {math.exp(x) - 1:.18e}")
print(f"expm1(x) stable: {math.expm1(x):.18e}")

y = 1e-16
print(f"log(1+y) naive: {math.log(1 + y):.18e}")
print(f"log1p(y) stable: {math.log1p(y):.18e}")

# Stable vector magnitude (avoids overflow/underflow in sqrt(x**2 + y**2))
print(f"\nhypot(3,4) = {math.hypot(3, 4)}")

# math.fsum documents an accurate summation strategy. Modern Python versions
# may also compensate sum() for short sequences, so agreement here is not a
# proof that their numerical contracts are identical.
vals = [1e16, 1.0, -1e16]
print(f"sum(vals) = {sum(vals)}")
print(f"math.fsum(vals) = {math.fsum(vals)}")
```

**Remember:** trigonometric functions use radians, not degrees! This is a constant source of bugs in scientific code.

---

## Reference preview: from a checked calculation to reusable code

Congratulations! You've been exploring Python interactively, testing ideas and learning how numbers behave. Now let's transform your interactive explorations into a reusable script:

The function below names its input unit, rejects an unphysical mass, and keeps
one analytic scaling check beside the calculation. Those are the parts worth
carrying from an interactive calculation into a reusable reference.

```python
#!/usr/bin/env python
"""
schwarzschild_radius.py
Calculate Schwarzschild radius with proper numerical handling.

Constants below are rounded for pedagogy. For high-precision work, use a
consistent constants set (e.g., CODATA via astropy.constants).
"""

import math

def schwarzschild_radius_checked(mass_kg):
    """Calculate a Schwarzschild radius for a positive mass in kg."""
    G = 6.67e-11
    c = 2.998e8

    if mass_kg <= 0:
        raise ValueError("mass_kg must be positive")

    return 2 * G * mass_kg / c**2

# This calculation is linear in mass. A scaling check is meaningful here;
# a generic log-space branch is not needed for astrophysically plausible masses.
if __name__ == "__main__":
    test_masses = {
        "Earth": 5.972e24,
        "Sun": 1.989e30,
        "Sgr A*": 8.2e36,
    }

    for name, mass in test_masses.items():
        rs = schwarzschild_radius_checked(mass)
        print(f"{name}: Rs = {rs:.2e} m ({rs/1e3:.2f} km)")

    sun_radius_m = schwarzschild_radius_checked(test_masses["Sun"])
    twice_sun_radius_m = schwarzschild_radius_checked(2 * test_masses["Sun"])
    assert math.isclose(twice_sun_radius_m, 2 * sun_radius_m, rel_tol=1e-15)
```

---

## Closing reflection

You've built a foundation for numerical computing. The seemingly simple act of
adding two numbers opens questions about representation, units, scale, and
evidence. Floating-point arithmetic is not broken—it is approximate by design.
The important habit is to connect that approximation to the particular claim a
calculation is meant to support.

Defensive numerical work is not a collection of magic bounds. A domain check,
finite-value test, stable representation, or convergence rule earns trust only
when its threshold and consequence are justified by the model, instrument, or
decision. Working in log space is often useful for products spanning extreme
scales; it is not a universal replacement for ordinary arithmetic.

When `0.1 + 0.2` is not exactly `0.3`, the lesson is not “never trust floats.”
It is to choose a comparison rule and test that fit the quantity at hand. When
you calculate values over many orders of magnitude, ask whether the
representation can overflow. When you subtract nearly equal values, look for
an equivalent stable form. These are habits of numerical judgment.

---

## Reference: quick return checklist

✓ Floating-point arithmetic is approximate by design — use a claim-appropriate tolerance for computed quantities; use `==` only when exact equality is the stated contract

✓ Machine epsilon (~2.2e-16) describes local binary64 spacing near 1.0; use an appropriate local scale or `math.ulp` for a specific value

✓ Catastrophic cancellation occurs when subtracting nearly equal numbers — use mathematical identities

✓ Work in log space to handle extreme scales without overflow/underflow

✓ Python integers have unlimited precision but use more memory than floats

✓ Variables are references to objects, not containers holding values

✓ A numerical guard needs a model-specific reason: quantity, units, failure mode, and consequence

✓ F-strings provide powerful formatting for scientific output

✓ Complex numbers are essential for wave physics and spectral analysis

✓ Always use radians with trigonometric functions

✓ Type conversion can lose information — always validate

---

## Reference: quick tables

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
- `math.isclose(a, b, rel_tol=..., abs_tol=...)` - Compare using tolerances you justify for the quantity and claim
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
