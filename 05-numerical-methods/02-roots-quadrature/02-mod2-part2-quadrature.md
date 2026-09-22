---
title: "Part 2: Quadrature — Discrete Sums, Error, and Adaptation"
subtitle: "Module 2: Static Problems & Quadrature | COMP 521"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

:::{note} Project 2 connection
This is the course reading for Project 2. The project requires a left rectangle
rule, trapezoid rule, Simpson's rule, and adaptive Simpson quadrature. Monte
Carlo is conceptual enrichment, with no assigned implementation, tests, figure,
or written response. Gaussian quadrature and spectrum integration also extend
the ideas without adding Project 2 deliverables.
:::

## Learning Objectives

By the end of this section, you will be able to:

- [ ] **Derive** rectangular, trapezoidal, and Simpson's rules from Taylor series
- [ ] **Understand** optimal point placement through Gaussian quadrature basics
- [ ] **Implement** a quadrature rule as a reusable function of a callable,
  interval, and panel count, then test its contract with `pytest`.
- [ ] **Explain** adaptive refinement, a change of variables at a branch point,
  and Monte Carlo's root-mean-square error model.
- [ ] **Choose** an appropriate method from smoothness, sampling access,
  dimension, and a measured error regime rather than a fixed dimension cutoff.
- [ ] **Analyze** error scaling and **predict** convergence behavior before
  floating-point round-off dominates.

---

## Building a reusable numerical method

Project 2 is the first course project in which reusable code belongs in Python
modules rather than only in a notebook. The central interface is

```python
rule(f, a, b, n)
```

where `f` is a callable that accepts a NumPy array of sample positions and
returns matching numeric values; `a` and `b` are integration limits; and `n` is
the positive integer number of subintervals. The algorithm must not know whether
`f` represents a sine wave, a Planck spectrum, or a limb-darkened stellar disk.

Put the rules in `integrate.py`, write the figures and interpretation in
`analysis.ipynb`, and run `python -m pytest` from the project root. A test makes
one part of the contract visible: a known integral, an exactness property, an
invalid panel count, or a predicted convergence ratio. The course
[software engineering guide](../../02-getting-started/04-software-engineering-guide.md#part-iv-reusable-modules-and-tests-from-p2-onward)
and [workflow checklist](../../02-getting-started/05-scientific-software-workflow-cheatsheet.md)
give the corresponding repository workflow.

Do not introduce a class for these rules. A rule has no persistent state: every
call receives its callable, interval, and panel count. Project 3 introduces
classes when a `Star` owns related state and invariants that must remain
consistent.

:::{note} Predict before coding
For increasing `np.sin(x)` on $[0,\pi/2]$, will a left-endpoint rectangle sum
underestimate or overestimate the exact integral $1$? State the geometric reason
before running the next cell.
:::

---

## The Fundamental Challenge

While differentiation is a local operation (needing only nearby points), integration is global — we must consider the entire domain. **Quadrature** (numerical integration) transforms the continuous integral:

$$I = \int_a^b f(x) dx$$

into a discrete sum:

$$I \approx \sum_{i=0}^n w_i f(x_i)$$

The numerical question is not only how to choose:

- The points $x_i$ (where to sample)
- The weights $w_i$ (how much each sample contributes)  
- The number $n$ (balancing accuracy vs computation)

It is also how to state and test the rule's inputs, preconditions, and expected
error. A correct answer for one integrand does not establish a reusable method.

## Physical Motivation: Why Astronomers Integrate

Integration is everywhere in astronomy because we observe integrated quantities:

1. **Spectroscopy**: A finite wavelength band collects integrated spectral flux
   $$F = \int_{\lambda_1}^{\lambda_2} F_\lambda d\lambda$$

2. **Photometry**: CCD pixels integrate photons over exposure time
   $$N_\text{photons} = \int_0^T \Phi(t) dt$$

3. **Structure**: Mass distributions require volume integrals
   $$M(<r) = \int_0^r 4\pi r'^2 \rho(r') dr'$$

4. **Cosmology**: In a spatially flat cosmology, luminosity distance involves integrating through expanding space
   $$d_L = (1+z) \int_0^z \frac{c\,dz'}{H(z')}$$

Each context demands different accuracy, and the function properties (smooth vs oscillatory, bounded vs singular) determine the best method.

:::{div}
:class: reading-definition
**Resolution is not conditioning**: An oscillatory or rapidly varying integrand
may need many samples to resolve. That is not, by itself, a statement that the
integral is ill-conditioned; conditioning asks how strongly the exact integral
changes when the input function is perturbed.
:::

---

## Building Integration Methods: From Rectangles to Optimality

### The Riemann Sum Foundation

The definition of the Riemann integral suggests the simplest approximation:

$$\int_a^b f(x)dx = \lim_{n \to \infty} \sum_{i=0}^{n-1} f(x_i^*) \Delta x_i$$

where $x_i^* \in [x_i, x_{i+1}]$ and $\Delta x_i = x_{i+1} - x_i$.

Different choices of $x_i^*$ give different methods:

- Left endpoint: Rectangle rule (left)
- Right endpoint: Rectangle rule (right)
- Midpoint: Midpoint rule
- Average of endpoint heights: Trapezoidal rule (an average of two samples, rather than one Riemann sample)

:::{figure} figures/2_4_integration_methods_geometry.webp
:label: fig-integration-methods-geometry
:width: 100%
:alt: Four quadrature approximations to the dimensionless integral of $f(x)=e^{-x/2}\cos(2x)+1$ from 0 to 2

Four quadrature approximations to the dimensionless integral of $f(x)=e^{-x/2}\cos(2x)+1$ from 0 to 2, all with six panels. Left and midpoint rules use six sample values; trapezoid and Simpson use seven. Colored areas show the actual constant, linear, or quadratic interpolants used by the rule. The black curve is the integrand. Reported errors use its analytic antiderivative as a common reference.

[Open full-size figure](figures/2_4_integration_methods_geometry.webp)
:::

---

## Method 1: Left Rectangle Rule

**Purpose:** This baseline rule makes the local-to-global error calculation
visible.

### Mathematical Formulation

For uniform spacing $h = (b-a)/n$:

$$I \approx h \sum_{i=0}^{n-1} f(a + ih) \quad \text{(left rectangle)}$$

### Error Analysis via Taylor Series

On each subinterval $[x_i, x_{i+1}]$:

$$\int_{x_i}^{x_{i+1}} f(x)dx = \int_{x_i}^{x_{i+1}} \left[f(x_i) + f'(x_i)(x-x_i) + \frac{f''(\xi)}{2}(x-x_i)^2\right]dx$$

Evaluating:
$$= f(x_i)h + f'(x_i)\frac{h^2}{2} + O(h^3)$$

The rectangle rule uses only $f(x_i)h$, so the signed local error
$I_i-Q_i$ is

$$E_{local} = \frac{h^2}{2}f'(\xi)$$

Over $n$ intervals:

$$E_{total} = n \cdot O(h^2) = \frac{b-a}{h} \cdot O(h^2) = O(h)$$

:::{div}
:class: reading-definition
**First-order method**: Global error proportional to step size.
:::

This is a **first-order method**: in the truncation-dominated regime, halving
$h$ halves the leading global error.

### Turn a slope bound into a panel count

Suppose $a<b$, $f$ is continuously differentiable, and $|f'|\le M_1$ on
$[a,b]$. Within a panel, the mean value theorem gives
$|f(x_i+s)-f(x_i)|\le M_1s$. Integrating the height discrepancy gives

$$|E_i|\le\int_0^hM_1s\,ds=\frac{M_1h^2}{2}.$$

Geometrically, this is a triangle of base $h$ and maximum height $M_1h$.
Summing the absolute panel bounds and using $nh=b-a$ yields

$$|I-L_n|\le\frac{nM_1h^2}{2}=\frac{M_1(b-a)^2}{2n}.$$

For a target absolute quadrature error $\tau>0$, a sufficient integer count is
$n\ge\max(1,\lceil M_1(b-a)^2/(2\tau)\rceil)$. A bound may be conservative:
it permits the largest slope on every panel and ignores cancellation. A maximum
observed on a sampled plot is not automatically a rigorous derivative bound.

For sine on $[0,\pi/2]$, $f'=\cos x$ and $M_1=1$, so the bound is
$\pi^2/(8n)$. At $n=128$ it is below 0.01, which justifies the accuracy scale
in the module test below. This bound concerns quadrature in exact arithmetic;
check that floating-point effects are small compared with the test margin.

### Move the sample, keep the panels

Right rectangles use $a+(i+1)h$; midpoint rectangles use $a+(i+1/2)h$.
For increasing functions the left sum is below the integral and the right sum
is above it. Their difference telescopes to $R_n-L_n=h[f(b)-f(a)]$.
Midpoint symmetry cancels the first-derivative contribution, giving composite
$O(h^2)$ error when the second derivative is bounded. Averaging the left and
right sums gives the trapezoid rule, which we derive next.

:::{figure} figures/rectangle-variants.png
:alt: Left, right, and midpoint rectangles use the same six sine panels with different sampled heights.

For sine on $[0,\pi/2]$, left rectangles underestimate and right rectangles
overestimate. Midpoint rectangles slightly overestimate because the curve is
concave down; they do not have the same first-order bias as endpoint rectangles.

[Open full-size figure](figures/rectangle-variants.png)
:::


### Implementation

```{code-cell} python
import numpy as np


def rectangle(f, a: float, b: float, n: int) -> float:
    """Approximate an integral with the left rectangle rule (global order 1)."""
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("n must be a positive integer.")

    a_float = float(a)
    b_float = float(b)
    if not (np.isfinite(a_float) and np.isfinite(b_float)):
        raise ValueError("a and b must be finite.")

    h = (b_float - a_float) / n
    x = a_float + h * np.arange(n)
    values = np.asarray(f(x), dtype=float)
    if values.shape != x.shape:
        raise ValueError("f must return one numeric value for each sample position.")
    if not np.all(np.isfinite(values)):
        raise ValueError("f returned a non-finite sample value.")
    return float(h * np.sum(values))


exact_sine_integral = 1.0
for panel_count in (8, 16, 32):
    approximation = rectangle(np.sin, 0.0, np.pi / 2.0, panel_count)
    absolute_error = abs(approximation - exact_sine_integral)
    print(
        f"n = {panel_count:2d}; "
        f"left rectangle = {approximation:.10f}; "
        f"absolute error = {absolute_error:.3e}"
    )
```

### What the rectangle rule can and cannot establish

- Its global error is only first order for smooth functions.
- For a monotonic function it has a one-sided bias: it underestimates an
  increasing function and overestimates a decreasing function when $a<b$.
- It is a useful baseline in Project 2 because its measured order of $1$ makes
  the improvement to orders $2$ and $4$ visible.
- It is not automatically the right choice when higher accuracy per function
  evaluation is needed.

### First tests for a module

Put the implementation in `integrate.py` and a separate test file in `tests/`.
The test below checks a known integral and one invalid input. It checks the
public behavior, not the rule's internal loop or array construction.

```python
# tests/test_integrate.py
import numpy as np
import pytest

from integrate import rectangle


def test_left_rectangle_sine_is_a_lower_estimate() -> None:
    approximation = rectangle(np.sin, 0.0, np.pi / 2.0, 128)
    assert approximation < 1.0
    assert 1.0 - approximation < 0.01


def test_rectangle_rejects_nonpositive_panel_count() -> None:
    with pytest.raises(ValueError):
        rectangle(np.sin, 0.0, np.pi / 2.0, 0)
```

Add comparable tests for `trapezoid` and `simpson`: an exactly integrated
polynomial where appropriate, a convergence comparison on a smooth function,
and each rule's invalid-input behavior. The test tolerance must follow a stated
error scale, not an arbitrary number of decimal places.

---

(method-2-trapezoidal)=
## Method 2: Trapezoidal Rule

**Why we care:** The trapezoid rule is a clear second-order rule for a smooth
callable and a natural rule for already tabulated data.

### Geometric Intuition

Instead of rectangles, connect consecutive points with straight lines, creating trapezoids. The area of each trapezoid averages the function values at its endpoints.

### Mathematical Formulation

The area of a trapezoid with parallel sides $f(x_i)$ and $f(x_{i+1})$ and height $h$ is:

$$A_i = \frac{h}{2}[f(x_i) + f(x_{i+1})]$$

Summing over all intervals:

$$I \approx \sum_{i=0}^{n-1} \frac{h}{2}[f(x_i) + f(x_{i+1})] = h\left[\frac{f(a)}{2} + \sum_{i=1}^{n-1} f(x_i) + \frac{f(b)}{2}\right]$$

(error-analysis)=
### Error Analysis

Using Taylor expansion around the midpoint $x_i + h/2$:

$$f(x_i) = f(x_i + h/2) - \frac{h}{2}f'(x_i + h/2) + \frac{h^2}{8}f''(x_i + h/2) + O(h^3)$$

$$f(x_{i+1}) = f(x_i + h/2) + \frac{h}{2}f'(x_i + h/2) + \frac{h^2}{8}f''(x_i + h/2) + O(h^3)$$

The trapezoidal approximation on $[x_i, x_{i+1}]$:

$$\frac{h}{2}[f(x_i) + f(x_{i+1})] = hf(x_i + h/2) + \frac{h^3}{8}f''(x_i + h/2) + O(h^4)$$

Put $m=x_i+h/2$ and integrate the same Taylor polynomial from $-h/2$ to $h/2$. The odd term vanishes:

$$I_i=\int_{-h/2}^{h/2}\left[f(m)+s f'(m)+\frac{s^2}{2}f''(m)+O(s^3)\right]ds
=h f(m)+\frac{h^3}{24}f''(m)+O(h^4).$$

Subtracting the trapezoid gives $h^3(1/24-1/8)f''(m)=-h^3f''(m)/12$ at leading order. With continuous $f''$, the exact remainder can be expressed at some point $\xi$ in the panel:

Local error: $E_{local} = -\frac{h^3}{12}f''(\xi)$

:::{div}
:class: reading-definition
**Second-order method**: Global error is proportional to step size squared.
:::

Global error: $\boxed{E_{total} = -\frac{(b-a)h^2}{12}f''(\xi)}$ for some $\xi \in [a,b]$

This is a **second-order method**: doubling the number of panels reduces the
leading error by about a factor of $4$ while the asymptotic model holds.

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| Endpoint singularity | Non-finite sample or order loss | Use a limiting value, a justified cutoff, or a change of variables |
| Oscillations | Poor convergence | Resolve the oscillation, split the domain, or use a method designed for it |
| Noisy sampled data | A noisy integral estimate | Report data uncertainty; smoothing is a modeling decision, not an automatic numerical fix |
| Discontinuity or kink | Error changes; a derivative kink can retain order $2$, while a jump can reduce it | Split at the known feature and measure the resulting convergence |

---

(method-3-simpson)=
## Method 3: Composite Simpson's Rule

**Why we care:** For a sufficiently smooth integrand, Simpson's symmetric
two-panel construction gives fourth-order global error.

### The Key Insight

Instead of linear interpolation (trapezoids), use quadratic interpolation (parabolas) through consecutive triplets of points.

### Derivation via Interpolation

For three equally-spaced points $x_0, x_1, x_2$ with $x_1 = x_0 + h$ and $x_2 = x_0 + 2h$, the unique parabola through $(x_i, f(x_i))$ is:

$$p(x) = f(x_0)\frac{(x-x_1)(x-x_2)}{2h^2} - f(x_1)\frac{(x-x_0)(x-x_2)}{h^2} + f(x_2)\frac{(x-x_0)(x-x_1)}{2h^2}$$

Integrating this parabola from $x_0$ to $x_2$:

$$\int_{x_0}^{x_2} p(x)dx = \frac{h}{3}[f(x_0) + 4f(x_1) + f(x_2)]$$

These are the famous Simpson weights: 1, 4, 1.

### Composite Simpson's Rule

For $n$ intervals (must be even):

$$\boxed{I \approx \frac{h}{3}\left[f(a) + 4\sum_{i=1,3,5...}^{n-1} f(x_i) + 2\sum_{i=2,4,6...}^{n-2} f(x_i) + f(b)\right]}$$

The pattern of weights is:
- Endpoints: 1
- Odd indices (1,3,5,...,n-1): 4
- Even indices (2,4,6,...,n-2): 2

### Error Analysis and Fourth-Order Accuracy

Through careful Taylor series analysis, the local error for Simpson's rule on interval $[x_i, x_{i+2}]$ is:

$$E_{local} = -\frac{h^5}{90}f^{(4)}(\xi)$$

:::{div}
:class: reading-definition
**Fourth-order method:** The leading global truncation error is proportional to
$h^4$ when the smoothness assumptions hold.
:::

Global error: $\boxed{E_{total} = -\frac{(b-a)h^4}{180}f^{(4)}(\xi)}$

Simpson's rule is fourth-order accurate under these assumptions.

### Why Simpson's Rule is Fourth-Order

Expand about the fixed midpoint $m=x_1$, writing $x=m+s$ with $-h\le s\le h$.
For $f$ with a continuous fourth derivative, Taylor's theorem gives

$$f(m+s)=f(m)+s f'(m)+\frac{s^2}{2}f''(m)
 +\frac{s^3}{6}f'''(m)+O(s^4).$$

Both the exact integral and Simpson's symmetric weighted sum cancel the odd
terms. In particular, $f'''(m)$ is one fixed coefficient, so

$$\frac{f'''(m)}{6}\int_{-h}^{h}s^3\,ds=0.$$

Simpson's rule also integrates the constant and quadratic terms exactly.
The remaining $O(s^4)$ contribution gives $O(h^5)$ error over this panel pair;
summing $O(1/h)$ pairs gives $O(h^4)$ composite error. This establishes the
order; the error formula above supplies its coefficient and sign. For a cubic
polynomial the remainder is zero, so Simpson is exact in exact arithmetic.

The interpolation remainder instead contains $f'''(\xi_x)$, whose evaluation
point can vary with $x$. We cannot assume that entire remainder is odd. The
fixed-midpoint Taylor expansion is what justifies the cancellation.

### Recover the error coefficient, not only the order

For a sufficiently smooth function, the quartic Taylor term at midpoint $m$
is $f^{(4)}(m)s^4/24$. Over $[-h,h]$, its exact integral is

$$\frac{f^{(4)}(m)}{24}\frac{2h^5}{5}
=\frac{f^{(4)}(m)h^5}{60}.$$

Simpson's weighted sum of that term is

$$\frac h3\frac{f^{(4)}(m)}{24}(h^4+4\cdot0+h^4)
=\frac{f^{(4)}(m)h^5}{36}.$$

Subtracting gives $h^5f^{(4)}(m)(1/60-1/36)=-h^5f^{(4)}(m)/90$ at leading
order. There are $(b-a)/(2h)$ panel pairs, which explains the composite
coefficient $1/180$. This Taylor calculation explains the coefficient;
the exact remainder theorem with continuous fourth derivative places its
evaluation at an appropriate $\xi$ rather than necessarily at the midpoint.

For $f(x)=x^4$ on $[-h,h]$, the difference is exactly $-4h^5/15$:
$f^{(4)}=24$ makes the same prediction. This is a useful sign and coefficient
check, distinct from checking exactness on cubics.

### When Simpson's Rule Shines

- Smooth functions with continuous fourth derivative
- Smooth functions without exploitable periodic endpoint matching; see the periodic comparison below
- When high accuracy is needed with moderate $n$
- Physical models whose regularity has been checked, including at boundaries

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| Odd `n` | The panel pairing is undefined | Raise `ValueError`; Project 2 requires an even panel count |
| Noisy sampled data | Higher order does not remove uncertainty | Use an uncertainty model; choose a rule appropriate to the samples |
| Insufficient regularity for the quoted remainder theorem | Its theorem no longer certifies the order | Inspect the actual feature and measure convergence; discontinuity of $f^{(4)}$ alone does not force order loss |
| Sharp local features | Fixed panels miss the feature | Refine locally or use adaptive quadrature |

:::{note} Check Your Understanding
1. Why must n be even for Simpson's rule?
2. What happens if f(x) is exactly a cubic polynomial?
3. How does the error scale if we double n?
4. When would Simpson's rule perform poorly?
:::

:::{tip} Answers and reasoning
:class: dropdown

1. Each quadratic interpolant spans two subintervals, so composite Simpson pairs an even number of subintervals.
2. Simpson integrates a cubic exactly in exact arithmetic: the symmetric odd remainder cancels, even though the interpolant is quadratic. Floating-point evaluation can still leave a small discrepancy.
3. Doubling $n$ halves $h$ and reduces a nonzero dominant fourth-order error by approximately 16. This prediction fails outside the smooth, resolved truncation regime.
4. Discontinuities, endpoint singularities, unresolved oscillations, or noisy data can violate that regime. Inspect the integrand and refine; the method name is not evidence that the assumptions hold.
:::

:::{figure} figures/2_5_simpson_vs_trapezoid_scaling.webp
:label: fig-simpson-vs-trapezoid-scaling
:width: 100%
:alt: Error scaling for the dimensionless integral $\int_0^1 e^x\,dx$

Error scaling for the dimensionless integral $\int_0^1 e^x\,dx$. The left log-log panel plots absolute error against the number of panels $n$; the trapezoid and Simpson trends have slopes $-2$ and $-4$ before the floating-point floor. The right panel compares the panel counts required for stated absolute-error targets. Circle and square markers, and dashed and solid lines, distinguish the rules as well as color.

[Open full-size figure](figures/2_5_simpson_vs_trapezoid_scaling.webp)
:::

---

### Extension: periodic endpoints can change the comparison

The second-order trapezoid formula is a general smooth-function result, not
an upper limit on what a particular problem can achieve. For smooth periodic
functions integrated over a complete period, matching endpoint derivatives can
cancel successive error terms. Analytic periodic functions can exhibit
exponential convergence with the number of equally spaced samples.
[Further reading: spectrally accurate integration](https://fncbook.com/spectral-integration/).

For a controlled dimensionless example, take $0<\rho<1$ and

$$g(x)=\frac{1-\rho^2}{1-2\rho\cos x+\rho^2}
=1+2\sum_{k=1}^{\infty}\rho^k\cos(kx).$$

Its integral on $[0,2\pi]$ is $2\pi$. The periodic trapezoid sum averages
all nonaliased cosine modes to zero, leaving an exact-arithmetic error

$$T_n-2\pi=\frac{4\pi\rho^n}{1-\rho^n}.$$

For $\rho=1/2$, the reference comparison below uses the same uniform samples
for trapezoid and Simpson. Neither method receives an advantage in sample
count. Do not interpret a result near floating-point precision as an indefinitely
continuing exponential trend.

<!-- periodic-data:start -->
| Panels $n$ | Trapezoid absolute error | Simpson absolute error |
|---|---|---|
| 4 | 8.378e-01 | 2.793e-01 |
| 8 | 4.928e-02 | 2.135e-01 |
| 16 | 1.918e-04 | 1.617e-02 |
| 32 | 2.926e-09 | 6.391e-05 |

<!-- periodic-data:end -->

Simpson combines nested trapezoid estimates as $S_n=(4T_n-T_{n/2})/3$.
Here the coarser trapezoid contribution can dominate its error: cancelling an
$h^2$ term is unhelpful when that term was already absent. The lesson is to
inspect the problem's structure and measured cost, not to replace one universal
method ranking with another.

---

(method-4-gaussian)=
## Method 4: Gaussian Quadrature

**Why we care:** When samples can be chosen, their placement and weights can
carry more information than a uniform grid with the same number of evaluations.

### The main idea

The previous composite rules used equally spaced points. Gaussian rules instead
choose both nodes and weights for a specified weight function.

For $n$ points, Gauss--Legendre quadrature is exact for every polynomial up to
degree $2n-1$ when it uses the roots of the Legendre polynomial of degree $n$
and their associated weights. This exactness statement is more precise than an
`O(h^p)` order claim: a fixed $n$-point rule has no grid spacing $h$.

### Example: 2-Point Gaussian Quadrature

Instead of evaluating at equally-spaced points, Gaussian quadrature uses special points. For 2 points on $[-1,1]$:
- Points: $x_1 = -\frac{1}{\sqrt{3}} \approx -0.577$, $x_2 = \frac{1}{\sqrt{3}} \approx 0.577$
- Weights: $w_1 = w_2 = 1$

This choice makes the rule exact for all cubic polynomials.

<!-- Lecture-figure public copies retain their basenames. Sources: _instructor/python/figures/generate_lecture9_overview.py and generate_lecture9_gauss.py. -->
::::{figure} figures/l9-gauss-nodes.svg
:alt: On minus one to one, an endpoint trapezoid uses the two endpoints while two-node Gauss-Legendre uses plus and minus one over square root of three. Each displayed weight is one.

Both rules evaluate twice. Their sample locations differ, and the Gaussian
weights apply to function values rather than to fixed-width panels.

[Open full-size figure](figures/l9-gauss-nodes.svg)
::::

For $f(x)=x^2$, the endpoint trapezoid gives $2$, while these Gaussian nodes
give $1/3+1/3=2/3$, the exact integral on $[-1,1]$.

::::{figure} figures/l9-gauss-area.svg
:alt: Two panels for x squared on minus one to one. Endpoint trapezoid shading has area two; the actual area under the curve is two thirds, matched by the two Gaussian weighted samples of value one third each.

The right-hand shading is the true integral, not a collection of Gaussian
panels. Gaussian quadrature combines the two sampled values with their weights.

[Open full-size figure](figures/l9-gauss-area.svg)
::::

### In Practice

NumPy provides the nodes and weights. This is an extension, not a Project 2
implementation target.

```{code-cell} python
from numpy.polynomial.legendre import leggauss


def gauss_legendre(f, a: float, b: float, n: int) -> float:
    """Apply an n-point Gauss--Legendre rule on [a, b]."""
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("n must be a positive integer.")
    points, weights = leggauss(n)
    x_gauss = (b - a) * points / 2.0 + (a + b) / 2.0
    return float((b - a) * np.sum(weights * f(x_gauss)) / 2.0)


print(f"2-point rule on x**3 over [0, 1]: {gauss_legendre(lambda x: x**3, 0.0, 1.0, 2):.16f}")
```

### When Gaussian Quadrature Matters

- When you control where to sample (not experimental data)
- For very smooth functions
- When function evaluations are expensive (fewer points needed)
- As the foundation for spectral methods in advanced simulations

The general lesson is that sample placement is part of a numerical method, not a
detail to leave implicit.

---

(method-5-monte-carlo)=
## Method 5: Monte Carlo Integration

**Why we care:** Monte Carlo replaces a grid by a random average. Its
$N^{-1/2}$ root-mean-square rate does not explicitly depend on dimension, but
its usefulness still depends on the integrand variance and sampling strategy.

(understanding-dimensions)=
### Understanding Dimensions in Integration

:::{div}
:class: reading-definition
**Integration dimension**: The number of independent variables being integrated over. A triple integral $\int\int\int$ f(x,y,z) dxdydz is 3-dimensional, not because it's in 3D space, but because we integrate over 3 variables.
:::

When we talk about "dimensions" in Monte Carlo integration, we mean the number of integration variables, not spatial dimensions:

- **1D integral**: $\int_a^b f(x) dx$ (one integration variable)
- **2D integral**: $\int \int_R f(x,y) dxdy$ (two integration variables)
- **6N-D integral**: Phase space integral over N particles with 3 position and 3 momentum components each

For example, a classical configurational partition function for 100 atoms has 300 position coordinates. The full phase-space formulation also includes momenta; for a separable quadratic kinetic energy, those momentum integrals can be done analytically.

### The Curse of Dimensionality

:::{div}
:class: reading-definition
**Curse of dimensionality**: Exponential growth of computational cost with dimension for grid-based methods.
:::

For a $d$-dimensional integral with $n$ points per dimension, a full tensor-product grid needs $n^d$ evaluations:

- 1D: 100 points
- 2D: $100^{2}$ = 10,000 points
- 3D: $100^{3}$ = 1,000,000 points
- 10D: $100^{10}$ = $10^{20}$ points (impossible!)

This exponential growth is why tensor-product grids become expensive quickly.
It does **not** establish one dimension at which every deterministic method
fails or Monte Carlo becomes best: smoothness, structure, error target, and
available variance reduction all matter.

### The Monte Carlo Solution

Draw $N$ independent, identically distributed points $\vec{x}_i$ uniformly
from a domain $\Omega$ with finite, nonzero volume:

$$I = \int_\Omega f(\vec{x})d\vec{x} \approx \hat{I} = \frac{V(\Omega)}{N}\sum_{i=1}^N f(\vec{x}_i)$$

where $V(\Omega)$ is the volume of the domain. Uniform sampling is essential
to this formula. Sampling from a nonuniform density $p$ instead requires
importance weights $f(\vec{x}_i)/p(\vec{x}_i)$, with $p>0$ wherever the integrand
contributes.

### Error Analysis

:::{div}
:class: reading-definition
**Central Limit Theorem**: For independent, identically distributed samples with finite variance, the centered and appropriately scaled sample mean approaches a normal distribution.
:::

For the Monte Carlo estimator $\hat{I} = \frac{V(\Omega)}{N}\sum_{i=1}^N f(\vec{x}_i)$:

**Step 1**: The expected value of our estimator is the true integral:
$$\mathbb{E}[\hat{I}] = \frac{V(\Omega)}{N} \sum_{i=1}^N \mathbb{E}[f(\vec{x}_i)] = V(\Omega) \cdot \mathbb{E}[f] = I$$

**Step 2**: The variance of the estimator is:
$$\text{Var}[\hat{I}] = \text{Var}\left[\frac{V(\Omega)}{N}\sum_{i=1}^N f(\vec{x}_i)\right] = \frac{V(\Omega)^2}{N^2} \cdot N \cdot \text{Var}[f] = \frac{V(\Omega)^2 \sigma_f^2}{N}$$

where $\sigma_f^2 = \text{Var}[f] = \mathbb{E}[f^2] - \mathbb{E}[f]^2$ is the finite variance of $f$ under uniform sampling over the domain.

**Step 3**: The standard error (standard deviation of the estimator) is:
$$\boxed{\sigma_I = \sqrt{\text{Var}[\hat{I}]} = \frac{V(\Omega)\sigma_f}{\sqrt{N}}}$$

:::{div}
:class: reading-definition
**Dimension-independent convergence**: Monte Carlo error scales as $N^{-1/2}$ regardless of dimension d!
:::

**Key insight**: Error $\propto N^{-1/2}$ independent of dimension $d$!

This model assumes:
- Independent random samples
- Finite variance of the integrand ($\sigma_f < \infty$)
- A sample size large enough that the observed estimator distribution is in the
  regime being summarized; there is no universal cutoff such as $N=30$

The rate says nothing about the constant $V(\Omega)\sigma_f$. A high-variance
integrand can have a large error even when the $N^{-1/2}$ slope is correct.

### Choosing Monte Carlo honestly

In one dimension, the deterministic rules in this project usually beat plain
Monte Carlo on smooth integrands. Monte Carlo becomes attractive when a useful
deterministic grid would require many samples across many integration variables,
or when a sampling distribution can reduce variance. Compare methods at a stated
evaluation budget; do not choose from a dimension cutoff alone.

:::{figure} figures/2_6_monte_carlo_convergence.webp
:label: fig-monte-carlo-convergence
:width: 100%
:alt: Random integration samples and repeated-run errors illustrate Monte Carlo sampling and its inverse-square-root reference rate.

Monte Carlo integration. The left panel shows random samples of a two-dimensional integrand over a square domain; their average, multiplied by the domain area, estimates the integral. The right log-log panel reports RMS error from 256 independent trials at each sample count, with reproducible seed 521. For this integrand, the variance under uniform sampling is $128/45$, so the estimator standard deviation is $\sqrt{128/(45N)}$. The theoretical curve has slope $-1/2$; measured RMS fluctuates around it. This statement requires independent finite-variance sampling and does not describe every individual error.

[Open full-size figure](figures/2_6_monte_carlo_convergence.webp)
:::

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| Infinite variance | The usual standard-error model fails | Change variables or construct an estimator with finite variance |
| Rare events | High-variance estimate | Use importance or stratified sampling with a justified proposal |
| Correlated samples | Fewer effective samples than $N$ | Diagnose autocorrelation and report effective sample size when applicable |
| One run happens to be close | An uninformative small signed error | Use independent seeded trials and summarize RMS error or a standard error |

:::{note} Optional conceptual comparison — no Project 2 deliverable
Independent repeats distinguish sampling uncertainty from one lucky estimate.
If a reference integral $I$ is known, the repeated-run statistic

$$\operatorname{RMS\ error}=\sqrt{\frac1R\sum_{j=1}^R(\widehat I_j-I)^2}$$

can be compared with the $N^{-1/2}$ prediction. A fixed seed makes a run
repeatable; it does not establish its accuracy. Project 2 does not assign a
Monte Carlo implementation or a convergence experiment.
:::

---

(adaptive-methods)=
## Adaptive Methods and Richardson Extrapolation

### Adaptive Quadrature

Adaptive quadrature changes the number and location of panels rather than using
one fixed spacing everywhere. For composite Simpson's rule, compare one Simpson
estimate on $[a,b]$, $S_{\mathrm{whole}}$, with the sum of two Simpson estimates
on its halves, $S_{\mathrm{two}}=S_{\mathrm{left}}+S_{\mathrm{right}}$. Since
Simpson's leading global error is proportional to $h^4$,

$$
\left|I-S_{\mathrm{two}}\right|
\approx \frac{\left|S_{\mathrm{two}}-S_{\mathrm{whole}}\right|}{2^4-1}
= \frac{\left|S_{\mathrm{two}}-S_{\mathrm{whole}}\right|}{15}.
$$

Under the leading-error model, the finer-grid estimate uses the factor $1/15$. Comparing the two approximations
directly to `tol` uses the wrong scale and rejects intervals more often than the
stated tolerance requires.

::::{figure} figures/l9-local-refinement.svg
:alt: Two partitions of a unit interval around a narrow positive peak. The upper partition samples uniformly; the lower one has more boundaries near the peak's known location.

Local refinement spends more samples near a feature. This illustrative
partition uses its known location; it is not an adaptive solver trace.

[Open full-size figure](figures/l9-local-refinement.svg)
::::

For Project 2, the public interface is

```python
adaptive_simpson(f, a, b, tol, max_depth=50)
```

The algorithm is recursive but its contract is ordinary and testable:

1. Validate that `tol` is positive and that `max_depth` is a non-negative
   integer; otherwise raise `ValueError`.
2. Compute $S_{\mathrm{whole}}$, $S_{\mathrm{left}}$, and
   $S_{\mathrm{right}}$ from their shared endpoint and midpoint values.
3. If the $1/15$ error estimate meets the local tolerance, return the corrected
   estimate $S_{\mathrm{two}}+(S_{\mathrm{two}}-S_{\mathrm{whole}})/15$.
4. Otherwise, if no recursion depth remains, raise `RuntimeError`; a partial
   integral is not a valid answer.
5. Recurse on the two halves with `tol / 2` for each, then add their estimates.

Halving the tolerance is a simple equal allocation: the two child error budgets add to the
parent budget. A `max_depth` guard is equally necessary because a singularity,
non-finite value, or unrealistically small tolerance can otherwise recurse until
Python fails without explaining the numerical problem.

Adaptive subdivision is not root finding. It bisects intervals to control an
integral-error estimate; it does not require a sign-changing bracket or select a
solution of $f(x)=0$. Root-finding methods and their contracts begin in Block 3.

### Absolute and relative error budgets

The Project 2 `tol` is an **absolute integral-error budget**, in units of
$f(x)\,dx$. It is not the root-position tolerance used by a root finder.
A more general integrator can compare an estimated error with

$$\tau_I=\mathrm{atol}_I+\mathrm{rtol}_I|Q|,$$

where $Q$ estimates the integral, $\mathrm{atol}_I$ carries the integral's
units, and $\mathrm{rtol}_I$ is dimensionless. This explains a common library
interface; it does not change Project 2's required signature.

If positive and negative contributions nearly cancel, $|Q|$ may be tiny even
when $\int|f|\,dx$ is large. A purely relative target based on $|Q|$ can then
be unrealistic. Choose an absolute scale from the question and the uncertainty
in the supplied function; do not promise relative digits that cancellation and
round-off cannot support.

Local budgets must also support the global claim. The Project 2 allocation
`tol/2` makes child absolute budgets sum to their parent's budget. Giving every
subinterval the full tolerance does not preserve that bound. Separately
accepting relative errors against each subintegral can likewise overstate
accuracy in a strongly cancelling sum. A general absolute/relative controller
needs to account for accumulated error estimates and the total-result scale.

The $1/15$ estimate assumes a resolved smooth-error regime. It estimates the
error of the finer Simpson value; applying the correction does not turn the
estimate into a rigorous error bound for every integrand. Check refinement,
known breakpoints, analytic cases, and recursion failures. The missed-feature
example below shows why tightening a tolerance alone may not help.

See FNC's [adaptive integration chapter](https://fncbook.com/adaptive/) for the
connection between extrapolation, error estimation, cancellation, and mixed
absolute/relative criteria.

:::{note} Two tests define the failure boundary
Test `adaptive_simpson(np.sin, 0, np.pi / 2, tol=...)` against the exact value
$1$, then deliberately set `max_depth` too small for a difficult valid input and
assert `RuntimeError`. A routine that returns its best partial estimate silently
has not met its interface.
:::

### Predict → Run → Explain: an adaptive estimate can miss structure

Error estimation compares what was sampled. It cannot see an oscillation whose
zeros coincide with all of its first sample positions. Consider
$f(x)=\sin^2(4\pi x)$ on $[0,1]$. Its exact integral is $1/2$.
Predict the initial Simpson estimates at $0,1/4,1/2,3/4,1$.

```{code-cell} python
def simpson_panel(f, a, b):
    midpoint = (a + b) / 2
    return (b-a) * (f(a) + 4*f(midpoint) + f(b)) / 6

hidden_wave = lambda x: np.sin(4*np.pi*x)**2
whole = simpson_panel(hidden_wave, 0.0, 1.0)
two = simpson_panel(hidden_wave, 0.0, 0.5) + simpson_panel(hidden_wave, 0.5, 1.0)
estimated_error = abs(two-whole) / 15
corrected = two + (two-whole) / 15
print("estimated error:", estimated_error)
print("actual error:", abs(corrected - 0.5))
print("values between original samples:", hidden_wave(np.array([0.125, 0.375])))
```

:::{figure} figures/adaptive-unresolved-wave.png
:alt: The sine-squared wave has four peaks between five initial Simpson samples that all lie at zeros.

The initial sample values are nearly zero in floating point, while the curve
has substantial area between them. Agreement between two unresolved estimates
does not establish an accurate integral.

[Open full-size figure](figures/adaptive-unresolved-wave.png)
:::

The $1/15$ estimate is effectively zero, yet the corrected answer misses about
0.5. The leading-error model has not been reached. Known oscillation scales,
domain splitting, minimum resolution, shifted diagnostic samples, and independent
refinement can reveal this failure. No finite collection of samples can
guarantee an integral for every unrestricted continuous function. A theorem
needs additional information, such as derivative bounds or known structure.

:::{tip} Answer: what would a smaller tolerance change?
:class: dropdown
An ordinary tolerance smaller than $10^{-8}$ can still accept this initial
estimate: both sampled approximations are near zero. More stringent acceptance
of the same misleading estimate is not the repair. Sampling between the old
nodes reveals the peaks; then refine enough to measure the expected regime.
The stopping rule controls an estimate, not an unconditional true-error bound.
:::

Now change the sampling rather than the acceptance threshold. A separate
fixed-grid reference calculation for this same wave gives:

| Composite Simpson panels | Distinct sample positions | Integral estimate |
|---|---|---|
| 4 | 5 | approximately 0 |
| 8 | 9 | approximately $2/3$ |
| 16 | 17 | approximately $1/2$ |
| 32 | 33 | approximately $1/2$ |

The first refinement reveals the missed area but overestimates it. The next
resolves enough of this particular trigonometric function to obtain its exact
integral up to rounding. This is evidence about the stated wave and grids,
not a universal minimum panel count. The check changes what the algorithm can
observe; shrinking a tolerance applied to the original samples does not.


(richardson-extrapolation)=
### Richardson Extrapolation

:::{div}
:class: reading-definition
**Richardson Extrapolation**: Using results at different resolutions to cancel leading error terms and achieve higher accuracy.
:::

If your method has error $I(h) = I_{exact} + Ch^p + O(h^{p+1})$, compute at two resolutions:

$$I_{better} = \frac{2^p I(h/2) - I(h)}{2^p - 1}$$

This cancels the leading error term! For trapezoidal rule (p=2):

$$I_{better} = \frac{4 I(h/2) - I(h)}{3}$$

For a sufficiently smooth integrand on nested uniform grids, the trapezoid error expansion has even powers: after cancelling the $h^2$ term, the next term is $O(h^4)$. The general expansion written above alone would promise only $O(h^{p+1})$; the extra order comes from symmetry.

::::{figure} figures/l9-richardson.svg
:alt: Log-log plot of measured trapezoid and Richardson-combined absolute errors for integrating cosine from zero to one against sine of one. The combined error falls faster as coarse spacing decreases.

For this smooth, resolved cosine example, the measured combination follows a
steeper error trend. The plot is evidence for this example, not a universal
error guarantee.

[Open full-size figure](figures/l9-richardson.svg)
::::

---

(quadrature-investigation)=
## Investigation: why did the expected order disappear?

A correct implementation can fail to show its nominal order on a particular
integrand. To tell a bug from a violated assumption, keep the rule fixed and
change one feature of the problem. We will use composite Simpson and return
to the smooth reference $\int_0^1e^x\,dx=e-1$.

### Predict: connect the shape to the error model

Compare two dimensionless integrands on $[0,1]$:

$$f_0(x)=e^x,\qquad f_1(x)=e^x+|x-c|,\qquad c=1/5.$$

The second has a kink at $c$. Its integral is also known:

$$I_1=e-1+\frac{c^2+(1-c)^2}{2}.$$

Before inspecting the figure, predict which of these statements is justified:

- Halving the panel width should reduce a nonzero leading Simpson error by 16
  on a sufficiently smooth, resolved problem.
- The same factor must hold for $f_1$ because its function values are finite.
- Splitting at the kink makes each piece smooth, allowing the fourth-order
  model to be tested separately on the two pieces.

The location $1/5$ never lies on these dyadic unsplit grids. This avoids hiding
the feature accidentally at a node. The split calculation uses half of the
panels on each side and reuses the common endpoint. Both calculations therefore
have the same total panel count and $n+1$ distinct function samples; their local
widths differ. The comparison asks what sample placement and regularity change
at equal evaluation count.

:::{figure} figures/quadrature-kink-investigation.png
:label: quadrature-kink-investigation
:alt: The integrand exp(x) plus an absolute-value kink at one fifth is shown with sample positions. Unsplit Simpson error decreases roughly quadratically, while splitting at the kink recovers a fourth-order trend before rounding.

The unsplit calculation has a changing derivative inside one panel. Splitting
puts that feature at the boundary of two smooth problems. The curves are
measured against the stated analytic integrals. At the smallest errors,
subtraction and summation round-off limit the interpretation of a fitted order.

[Open full-size figure](figures/quadrature-kink-investigation.png)
:::

The following are reference errors for $n=16,32,64$ from the plotted
calculations. They are supplied data for interpreting convergence, not a
Simpson implementation. The full comparison figure was generated separately.

<!-- quadrature-data:start -->
```{code-cell} python
# Reference errors; the comparison algorithms remain student implementation work.
panel_counts = np.array([16, 32, 64])
reference_errors = {
    "smooth": np.array([1.4559284666759709e-07, 9.102726128418226e-09, 5.689699822397642e-10]),
    "kink": np.array([0.0004165210738205083, 0.00010417576939314444, 2.6041097696882787e-05]),
    "split": np.array([8.310909613840067e-07, 5.198953223484182e-08, 3.250070435001362e-09]),
}

# Slices pair adjacent resolutions. log2(error ratio) measures the observed order.
for name, errors in reference_errors.items():
    orders = np.log2(errors[:-1] / errors[1:])
    print(f"{name:6s}: orders {orders[0]:.3f}, {orders[1]:.3f}")
```
<!-- quadrature-data:end -->

Do the observed orders identify the cause by themselves? State a comparison
that would distinguish an incorrect weight pattern from insufficient regularity.

:::{tip} Answer: choose a test that separates the explanations
:class: dropdown
The smooth reference and polynomial-exactness checks test different properties
of the implementation. Passing them, losing order only on the kinked function,
and recovering the expected trend after splitting support the regularity
explanation. A single failed convergence ratio does not establish a bug.
Splitting is effective here because each piece is smooth. It is not a universal
repair for an endpoint singularity or branch point. Recheck the assumptions and
the observed regime after any transformation.
:::

:::{note} A grid-alignment transfer question
Move the kink from $1/5$ to $1/3$ while retaining $n=4,8,16,\ldots$. Could
an observed fourth-order trend prove that the new integrand is smooth?
:::

:::{tip} Answer: a correct order can have an unexpected cause
:class: dropdown
No. On these particular grids, Simpson integrates $|x-1/3|$ exactly in exact
arithmetic, even though the kink lies between nodes. The remaining error comes
from $e^x$ and has its fourth-order trend. Moving the kink to $1/5$ breaks
that special cancellation. Smoothness is a sufficient condition for the quoted
theorem, not a fact we can infer from one convergence plot. A change in grid
alignment is a useful discriminating check.
:::

### Transfer: what if the samples are measurements?

A measured spectrum supplies values at fixed wavelengths. Interpolating those
same values onto a denser grid does not add measurements. A quadrature result
can converge for that interpolant while the inferred band flux remains limited
by measurement uncertainty or unresolved lines.

For a fixed weighted sum $Q=\sum_i w_i y_i$, a covariance model $C$ for the
measurements gives

$$\operatorname{Var}(Q)=\sum_{i,j}w_i C_{ij}w_j.$$

For independent errors with known standard deviations $\sigma_i$, this reduces
to $\sum_i w_i^2\sigma_i^2$. These are statistical uncertainties, not
truncation-error bounds. Values interpolated from the same data are correlated;
treating them as additional independent measurements would invent information.
The formula also does not account for an unobserved feature between samples.

Which action addresses each limitation: refining quadrature, obtaining more
spectral samples, improving measurement precision, or revising the interpolation
model? Explain what evidence would make you choose it.

:::{tip} Answer: distinguish the computed curve from the observed source
:class: dropdown
Refinement reduces numerical integration error for a chosen curve. More
observations can resolve a missed feature; more precise observations can reduce
measurement uncertainty. Changing interpolation changes the model between the
observations and requires justification. Agreement among dense-grid integrals
of one interpolant establishes none of those improvements by itself.
:::


## Project 2 applications: endpoints and branch points

The formal order of a rule is conditional. The following applications make the
conditions visible before you put the rules in a more complicated model.

### A removable endpoint in the Planck integral

After the substitution $x=h\nu/(k_B T)$, the Planck integral includes

$$
\int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}.
$$

Near $x=0$, $e^x-1\sim x$, so the integrand tends to $x^2$ and its limiting
value is $0$. The mathematical integrand is finite at the endpoint, but the
literal floating-point expression at `x == 0` is `0.0 / 0.0`, which is `nan`.
`np.expm1(x)` evaluates $e^x-1$ accurately for small nonzero `x`; it does not
make division by zero at exactly `x == 0` valid.

For a vectorized integrand, assign the analytic endpoint value explicitly or
construct a grid that excludes the endpoint and account for the omitted interval.
Do not accept a quiet `nan`, and do not call a small lower cutoff harmless
without bounding its contribution. The upper limit is also a numerical choice:
replace infinity with a finite $b$, then show that increasing $b$ no longer
changes the answer at the precision you claim. The exact value $\pi^4/15$ is a
test target for this dimensionless stage before dimensional constants enter.

### A radial transit integral and a regression limit

For the limb-darkened stellar disk, the radial integrand contains the factor

$$
I(r)\,2\pi r\,f(r,z),
$$

where $r$ is stellar radius in units of $R_\star$, $z$ is the projected
separation in the same units, and $f(r,z)$ is the occulted fraction of an
annulus. The numerical rule should receive this integrand as a callable; it
does not need a special transit branch inside `simpson`.

The limit $u=0$ makes the intensity uniform. In that limit, the numerical
limb-darkened calculation must reproduce the uniform-disk result from Project
1. This is a regression test: an earlier analytic model defines a known
behaviour of the newer numerical model.

### What a change of variables repairs

At the geometric contact radii $r=z\pm p$, the occulted-annulus factor has a
square-root branch point. A fixed Simpson grid can therefore lose fourth-order
convergence even though it is correct on smooth functions. Splitting the domain
at a known contact point isolates the feature but leaves it at a Simpson
endpoint, so splitting alone need not restore the order.

If the relevant local behaviour is $g(r)\sim\sqrt{r-r_0}$, set
$r=r_0+t^2$ on that panel. Then

$$
g\bigl(r(t)\bigr)\frac{dr}{dt}\sim t\,(2t)=2t^2,
$$

which is smooth at $t=0$. The substitution changes both the variable and the
Jacobian; omitting $dr/dt$ changes the integral. In Project 2, measure the
order after the substitution rather than assuming that a mathematically
plausible transformation restored it.

---

## Real Application: Galaxy Luminosity from Spectrum

Astronomers measure galaxy spectra as discrete samples at wavelengths $\lambda_i$ with fluxes $F_i$. Under an isotropic nearby-source model, the luminosity in the measured wavelength band is:

$$L_{\mathrm{band}} = 4\pi d^2 \int_{\lambda_{min}}^{\lambda_{max}} F_\lambda d\lambda$$

### Challenges

1. **Irregular wavelength spacing** from different instruments
2. **Noise** in flux measurements  
3. **Missing data** from atmospheric absorption
4. **Emission lines** need high resolution

### Solution Strategy

For irregular spacing, use trapezoidal rule with variable h:

```python
def integrate_spectrum(wavelengths, fluxes):
    """Integrate spectrum with irregular spacing"""
    total = 0
    for i in range(len(wavelengths) - 1):
        dλ = wavelengths[i+1] - wavelengths[i]
        f_avg = (fluxes[i+1] + fluxes[i]) / 2
        total += dλ * f_avg
    return total
```

A gap bridged by this calculation assumes a straight-line interpolant across the missing interval. It does not establish the unobserved flux there. The finite-band result is not a bolometric luminosity without information about wavelengths outside the band.

For an emission line, choose the sampling density from the required integrated
flux accuracy and the line shape; a fixed number of points per width is a
starting diagnostic, not a guarantee.

---

## Choosing the Right Integration Method



### Method Comparison Summary

| Method | Order | Pros | Cons | Best For |
|--------|-------|------|------|----------|
| Rectangle | $O(h)$ on smooth functions | Simple; monotone left/right sums can bound an integral | More samples may be needed for a target | Baseline approximation, one-sided sampling, or monotonicity bounds |
| Trapezoid | $O(h^2)$ on a smooth uniform grid | Directly applies to tabulated values | Lower order than Simpson for smooth callables | Sampled or irregularly spaced data |
| Simpson | $O(h^4)$ for sufficient smoothness | Accurate per evaluation on smooth problems | Needs even `n`; loses order at non-smooth features | Smooth theoretical functions |
| Gaussian | Exact through polynomial degree $2n-1$ | Efficient when nodes can be chosen | Special nodes and weights | Smooth callable, controlled sampling |
| Monte Carlo | RMS $O(N^{-1/2})$ | Rate does not explicitly depend on dimension | Variance can make the constant large | Many integration variables or an effective variance-reduction strategy |

### Practical Guidelines

1. **State the data model**: do you have a callable or already sampled values,
   and is the spacing uniform?
2. **Check regularity**: plot the integrand and locate discontinuities, sharp
   features, and endpoints before assigning an order.
3. **Measure convergence**: refine only in a range where the expected trend is
   visible, then identify the round-off floor.
4. **Compare cost fairly**: use function evaluations for deterministic rules and
   independent trials plus RMS error for Monte Carlo.
5. **Use library routines deliberately**: in production, read the library
   routine's sampling, tolerance, and failure contracts rather than assuming it
   implements the classroom rule.

---

## Debugging Integration

Common integration bugs and their diagnosis:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Error does not decrease with n | Bug, unresolved structure, invalid error model, or rounding | First test polynomial exactness, then inspect sample locations and change the refinement range |
| Error plateaus near a floating-point floor | Round-off dominance | Stop claiming refinement will help; reassess scaling or precision if the target remains unmet |
| Oscillating convergence | Grid alignment or unresolved features | Shift diagnostic samples, locate known features, and compare split and unsplit refinement |
| Simpson gives weird results | Odd n | Ensure even intervals |
| Negative result for positive f | Reversed limits, incorrect weights, or inappropriate dtype | Check orientation, weights, and sampled values; overflow produces non-finite results and needs scaling or a different representation |
| Monte Carlo results fluctuate | Ordinary sampling variation, rare events, correlation, or invalid variance model | Compare independent repeats with a justified standard-error model before selecting a repair |

---

## Bridge to the next block

Quadrature and root finding are distinct problems. They share useful habits:
state the approximation, check preconditions, measure convergence in a valid
regime, and report a failure rather than inventing a result.

This block ends with an integral estimate and an error claim. Block 3 begins a
different contract: finding a value where $f(x)=0$, with bracketing, derivative,
and initial-guess failure modes that quadrature does not have.

Later ODE methods reuse the local-to-global error distinction, but their step
acceptance and stability requirements are separate again.

*Next: Block 3 — Root Finding and Stellar Inference*
