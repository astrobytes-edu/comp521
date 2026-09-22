---
title: "Part 1: Root Finding"
subtitle: "Numerical Methods Module 2 | COMP 521"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

<!-- prep-banner:start -->
:::{note} Block 3 connection
This reading is the root-finding foundation for Project 3. Project 2 uses the
quadrature reading and functions in `integrate.py`; do not add root finding or
a class to that project. Project 3 introduces a `Star` class because its data
and invariants belong together.
:::
<!-- prep-banner:end -->

## Learning Objectives

By the end of this section, you will be able to:

- [ ] **Implement** bisection, Newton-Raphson, and secant methods from scratch
- [ ] **Analyze** convergence rates (linear, superlinear, quadratic) mathematically
- [ ] **Diagnose** method failures and **design** robust hybrid approaches
- [ ] **Apply** root finding to Kepler's equation, Lagrange points, and stellar structure
- [ ] **Predict** iteration counts and **verify** convergence behavior

---

(the-fundamental-problem)=
## The Fundamental Problem

:::{div}
:class: reading-definition
**Root/Zero**: A value $x^*$ where $f(x^*) = 0$. The x-intercept of the function. In physics, often represents equilibrium points.
:::

:::{div}
:class: reading-definition
**Transcendental equation**: An equation involving transcendental functions such as sine, exponential, or logarithm. Many require numerical solution, but some have explicit solutions: $e^x=2$ gives $x=\ln 2$.
:::

In physics, equilibrium occurs where the net force vanishes, where a differentiable potential energy is stationary, or where competing effects balance. Mathematically, these all reduce to finding **roots** of equations: solving $f(x) = 0$.

Many equations in computational physics have no closed-form solution. For
example, a stellar model must satisfy hydrostatic equilibrium:

$$\frac{dP}{dr} = -\frac{GM(r)\rho(r)}{r^2}$$

This is a differential equation, not itself a scalar root equation. Once we discretize a stellar model or impose a boundary condition, root finding can determine an unknown central value, radius, or model parameter. We need to distinguish solving the ODE from solving that resulting residual equation.

:::{div}
:class: reading-definition
**Root sensitivity**: For a simple scalar root $r$, $1/|f'(r)|$ describes the
sensitivity to an additive perturbation in the function value. Its numerical
meaning depends on the chosen units and on the error model.
:::

:::{note} Connection to Module 1
Root finding uses the same error analysis framework from Module 1:

- **Truncation error**: From stopping iterations early (like truncating Taylor series)
- **Round-off error**: From finite precision, including cancellation and a
  small derivative in a Newton update
- **Stopping criteria**: An interval-width or residual criterion matched to
  the quantity being controlled

The secant method even uses finite differences to approximate f'(x)!
:::

## Building Intuition: The Geometry of Root Finding

Before diving into algorithms, let's understand the geometry. Finding roots is about locating zeros; a curve can cross the x-axis or touch it without crossing. Different methods use different geometric insights:

:::{div}
:class: reading-definition
**Bracketing**: Maintaining an interval whose endpoint values have opposite signs. If the function is continuous on that interval, the Intermediate Value Theorem guarantees at least one root inside.
:::

:::{div}
:class: reading-definition
**Interpolation**: Approximating a function between known points using simpler functions (lines, parabolas, etc.).
:::

1. **Bracketing methods** (bisection) maintain an interval with a sign change.
2. **Local methods** (Newton) use a tangent-line model near an iterate.
3. **Interpolation methods** (secant) replace the analytic derivative with a
   slope from two evaluations.

Each approach has trade-offs between:

- **Reliability**: Will it always find a root?
- **Speed**: How many iterations to converge?
- **Requirements**: Do we need derivatives? Good initial guesses?

:::{figure} figures/2_1_root_methods_comparison.webp
:label: fig-root-methods-comparison
:width: 100%
:alt: Root-finding geometry for $f(x)=x^3-2x-5$

Root-finding geometry for $f(x)=x^3-2x-5$. Bisection starts on
$[1.5,2.5]$, Newton at 2.3, and secant with 1.5 and 2.3. The first three
iterates show how each method obtains its next position. The fourth panel
compares errors against a reference bracketed in 70-digit decimal arithmetic,
then rounded to binary64. The horizontal axis counts function and derivative
calls separately, with one unit for each; these calls need not have equal
runtime. Bracket half-width tolerance is $10^{-10}$ and the cap is 40 iterations.
Zero computed residuals and floating-point stagnation end a run. Zero plotted
errors are omitted, not replaced by an invented floor.

[Open full-size figure](figures/2_1_root_methods_comparison.webp)
:::

---

(method-1-bisection)=
## Method 1: Bisection

### The Mathematical Foundation

:::{div}
:class: reading-definition
**Intermediate Value Theorem**: If $f$ is continuous on $[a,b]$ and $k$ is any value between $f(a)$ and $f(b)$, then there exists at least one $c \in [a,b]$ where $f(c) = k$. Strictly intermediate values occur in the open interval.
:::

The bisection method is based on the **Intermediate Value Theorem**: 

> If $f$ is continuous on $[a,b]$ and $f(a) \cdot f(b) < 0$, then there exists at least one root $r \in (a,b)$ where $f(r) = 0$.

The algorithm repeatedly halves the interval, keeping the half that contains the root.

### Algorithm Analysis

Starting with interval $[a_0, b_0]$ where $f(a_0) \cdot f(b_0) < 0$:

1. Compute midpoint: $c_n = \frac{a_n + b_n}{2}$
2. Evaluate $f(c_n)$
3. Update interval:
   - If $f(c_n)=0$: return the sampled zero; otherwise stop only when the half-width meets the requested position tolerance
   - If $f(a_n) \cdot f(c_n) < 0$: root in $[a_n, c_n]$, so set $b_{n+1} = c_n$, $a_{n+1} = a_n$
   - Otherwise: root in $[c_n, b_n]$, so set $a_{n+1} = c_n$, $b_{n+1} = b_n$

After $n$ iterations, the interval width is:

$$|b_n - a_n| = \frac{|b_0 - a_0|}{2^n}$$

:::{div}
:class: reading-definition
**Linear convergence of the bound**: Bisection halves its bracket half-width at each update. Its actual midpoint error need not decrease by exactly one half, or even decrease at every update.
:::

The error in our approximation is bounded by half the interval width:

$$|c_n - r| \leq \frac{|b_n - a_n|}{2} = \frac{|b_0 - a_0|}{2^{n+1}}$$

This is **linear convergence** with rate $\frac{1}{2}$.

### Iterations Required

To achieve error $< \epsilon$, we need:

$$\frac{|b_0 - a_0|}{2^{n+1}} < \epsilon$$

Solving for $n$:

$$n > \log_2\left(\frac{|b_0 - a_0|}{\epsilon}\right) - 1$$

For example, to find a root in $[0, 1]$ to 10 decimal places ($\epsilon = 10^{-10}$):

$$n > \log_2(10^{10}) - 1 \approx 33.2 - 1 = 32.2$$

So 33 interval halvings suffice, followed by the new midpoint, provided continuity and reliable function signs hold. Count midpoint evaluations separately from interval updates.

### Implementation

This reading uses a compact reference interface to illustrate bracket reduction.
It differs from the [Project 3 contract](../../08-assessments/projects/project-3.md):

| Reading example | Project 3 |
|:--|:--|
| `bisection(..., tol=...)` returns one scalar | `bisect(..., atol=..., rtol=...)` returns `(root, n_iter, history)` |
| An exact sampled root may be passed as `(x, x)` | Require `a < b`; retain exact sampled roots separately |
| Absolute position tolerance only | Absolute plus relative position allowance |

Use the project brief for submitted interfaces, history recording, and failure
behavior. The example below is a reading reference, not a replacement module.

```{code-cell} python
import math
import numpy as np


def bisection(f, a, b, tol=1e-10, max_iter=100):
    """Return a bracket midpoint with absolute position tolerance tol.

    f must be continuous, finite, scalar-valued, and reliably signed.
    tol has x's units; it is not a tolerance on the residual f(x).
    """
    if not (math.isfinite(a) and math.isfinite(b) and a <= b):
        raise ValueError("Need finite ordered endpoints")
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("tol must be positive and finite")
    if isinstance(max_iter, (bool, np.bool_)) or not isinstance(max_iter, (int, np.integer)) or max_iter <= 0:
        raise ValueError("max_iter must be a positive integer")

    def evaluate(x):
        value = float(f(x))
        if not math.isfinite(value):
            raise ValueError("f must return finite values")
        return value

    fa, fb = evaluate(a), evaluate(b)
    if fa == 0.0:
        return a
    if fb == 0.0:
        return b
    # Comparing signs avoids overflow/underflow from multiplying values.
    if (fa < 0) == (fb < 0):
        raise ValueError("Need opposite signs at the endpoints")

    for _ in range(max_iter):
        c = a / 2 + b / 2   # Avoid overflow in a + b.
        if max(c - a, b - c) <= tol:
            return c
        if c == a or c == b:
            raise RuntimeError("No representable interior point; tolerance unmet")
        fc = evaluate(c)
        if fc == 0.0:
            return c
        if (fa < 0) != (fc < 0):
            b, fb = c, fc
        else:
            a, fa = c, fc
    raise RuntimeError(f"Failed to converge in {max_iter} iterations")
```

An exactly zero *computed* function value is accepted here. If evaluating the
function can underflow to zero or produce unreliable signs, the bracket is no
longer certified by these values. Rescale the evaluation or use higher precision;
changing the stopping criterion cannot repair the function evaluation.

### Predict → Run → Explain: small residual or well-located root?

Multiplying a function by a positive constant does not move its root. Predict
whether the same position tolerance should give the same answer for both rows.

```{code-cell} python
for scale in (1.0, 1e-12, 1e-200):
    f_scaled = lambda x: scale * (x - 0.9)
    root = bisection(f_scaled, 0.0, 1.0, tol=1e-10)
    print(f"scale={scale:.0e}: root={root:.12f}, "
          f"position error={abs(root-0.9):.3e}, residual={abs(f_scaled(root)):.3e}")
```

The position errors agree although the residuals differ by many orders of
magnitude. Near a simple root, $f(x)\approx f'(r)(x-r)$: a residual measures
position error only after accounting for the slope and the function's units.
If $|f'|\ge m>0$ on the relevant interval, the mean value theorem gives
$|x-r|\le |f(x)|/m$. A bracket gives a position bound without estimating that slope.

:::{figure} figures/root-residual-width.png
:alt: Rescaling a linear function changes its residual while the bisection half-width is unchanged.

Both functions have root 0.9 and use the same sequence of brackets. Residual
size depends on the vertical scale; bracket width measures uncertainty in x.

[Open full-size figure](figures/root-residual-width.png)
:::


### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| No sign change | Won't start | Scan interval for brackets first |
| Multiple roots | Finds arbitrary one | Use smaller initial intervals |
| Discontinuity | False bracket | Check continuity requirement |
| $f$ touches zero | No sign change | Bisection cannot certify this root; use a method with different assumptions or bracket a related sign-changing quantity |

:::{note} Check Your Understanding
1. Why does bisection require $f(a) \cdot f(b) < 0$?
2. What happens if there are multiple roots in $[a,b]$?
3. Can bisection find roots where $f$ touches but doesn't cross zero?
4. If you need 6 decimal places and start with $[0, 10]$, how many iterations?
:::

:::{tip} Answers and reasoning
:class: dropdown

1. Opposite signs plus continuity establish at least one crossing. Compare signs in code instead of multiplying tiny values.
2. The interval may contain several roots; bisection narrows toward a crossing without identifying which physical root you intended.
3. A sampled zero can be returned, but an even-multiplicity root without a sign change cannot be certified by a surrounding bisection bracket.
4. For absolute position error below $10^{-6}$, $10/2^{n+1}<10^{-6}$ requires $n\ge23$ interval halvings, followed by that bracket's midpoint. The first midpoint is index zero; count evaluations separately.
:::

---

(method-2-newton-raphson)=
## Method 2: Newton-Raphson — using a local slope

(the-geometric-insight)=
### The Geometric Insight

:::{div}
:class: reading-definition
**Tangent line approximation**: Replacing a curve with its tangent line at a point, valid for small deviations.
:::

Newton's method uses calculus to accelerate convergence. The key insight: near any point, a smooth function looks approximately linear. We follow the **tangent line** to where it crosses the axis. Sufficiently near a simple root, under suitable smoothness conditions, this can provide a much more accurate estimate. A tangent step from an arbitrary starting point need not improve the estimate.

### Mathematical Derivation

Starting at point $x_n$, the tangent line to $f(x)$ has equation:

$$y - f(x_n) = f'(x_n)(x - x_n)$$

This line crosses the x-axis (where $y = 0$) at:

$$0 - f(x_n) = f'(x_n)(x_{n+1} - x_n)$$

Solving for $x_{n+1}$:

$$\boxed{x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}}$$

This is the Newton-Raphson iteration formula.

(convergence-analysis)=
### Convergence Analysis

To understand the convergence rate, we analyze the error $e_n = x_n - r$ where $r$ is the true root.

Using Taylor series around $r$:

$$f(x_n) = f(r) + f'(r)(x_n - r) + \frac{f''(r)}{2}(x_n - r)^2 + O((x_n - r)^3)$$

Since $f(r) = 0$:

$$f(x_n) = f'(r)e_n + \frac{f''(r)}{2}e_n^2 + O(e_n^3)$$

Similarly:

$$f'(x_n) = f'(r) + f''(r)e_n + O(e_n^2)$$

Through algebraic manipulation of the Newton iteration formula:

$$e_{n+1} = \frac{f''(r)}{2f'(r)}e_n^2 + O(e_n^3)$$

:::{div}
:class: reading-definition
**Quadratic convergence**: Error is squared each iteration, doubling the number of correct digits.
:::

For a sufficiently smooth function, a simple root with $f'(r)\ne0$, and a sufficiently close initial guess, this shows **quadratic convergence**! The error is squared each iteration, meaning the number of correct digits approximately doubles.

(when-newton-fails)=
### When Newton Fails

The tangent model can fail for several distinct reasons:

1. **Zero derivative away from a root**: If $f'(x_n)=0$ and $f(x_n)\ne0$, the horizontal tangent has no zero
2. **Poor initial guess**: May diverge or converge to wrong root
3. **Cycles**: Can oscillate between points without converging
4. **Sensitive root**: A small $|f'(r)|$ amplifies a given absolute function error; interpret that error together with units and function scaling

:::{figure} figures/2_2_newton_failure_modes.webp
:label: fig-newton-failure-modes
:width: 100%
:alt: Four panels show Newton cycling, divergence from a poor guess, a non-differentiable cube-root zero, and linear convergence at a repeated root.

Four directly computed Newton histories isolate different mechanisms.
For $x^3-2x+2$, the initial value 0 cycles exactly between 0 and 1.
For $\arctan x$, starting at 2 gives rapidly growing iterate magnitudes.
For the real cube root, every nonzero iterate obeys $x_{k+1}=-2x_k$;
the derivative is undefined at the root, and starting nearby does not help.
For $(x-1)^2$, Newton halves the position error rather than squaring it.
These are separate failure or convergence mechanisms; a small derivative at
an arbitrary iterate is not the same thing as a sensitive root.

[Open full-size figure](figures/2_2_newton_failure_modes.webp)
:::

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| f'(x) $\approx$ 0 | Division by small number | Use bisection if a valid sign-changing bracket is available |
| Bad initial guess | Divergence | Find and verify a sign-changing bracket, then use bisection |
| Oscillation | Repeating values | Detect cycles, switch methods |
| Repeated root | Slow convergence | Use modified Newton: $x_{n+1} = x_n - m\frac{f(x_n)}{f'(x_n)}$ |

:::{tip} Physical Example: Finding Lagrange Points
In the circular restricted three-body problem, the effective potential is:
$$\Phi_{eff} = -\frac{GM_1}{r_1} - \frac{GM_2}{r_2} - \frac{1}{2}\omega^2(x^2 + y^2)$$

Lagrange points occur where $\nabla\Phi_{eff} = 0$. Newton's method excels here because we can analytically compute the gradient and Hessian!
:::

---

(method-3-secant)=
## Method 3: Secant - The Practical Compromise

### Motivation: No Derivatives Required

:::{div}
:class: reading-definition
**Finite difference approximation**: Estimating derivatives using function values at nearby points.
:::

Newton's method requires $f'(x)$, but what if:
- The derivative is expensive to compute?
- We only have $f(x)$ as a black box?
- The function comes from experimental data?

The secant method approximates the derivative using a **finite difference**:

$$f'(x_n) \approx \frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}$$

### The Iteration Formula

Substituting this approximation into Newton's formula:

$$\boxed{x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}}$$

Geometrically, we're replacing the tangent line with a secant line through two points.

### Convergence Analysis

For a sufficiently smooth function with a simple root and sufficiently close starting points, the convergence of the secant method is more complex. Through detailed analysis (involving difference equations), one can show that the order of convergence is:

$$\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618$$

This is the golden ratio! The error satisfies:

$$|e_{n+1}| \approx C|e_n|^{1.618}$$

:::{div}
:class: reading-definition
**Superlinear convergence**: $|e_{k+1}|/|e_k|\to0$ as the root is approached. Quadratic convergence is also superlinear; secant convergence is specifically superlinear and subquadratic.
:::

This **superlinear convergence** is slower than Newton's quadratic rate but faster than bisection's linear rate.

### Where the golden ratio comes from

The secant slope contains information from two previous errors. Expanding
$f(r+e)=a e+b e^2+O(e^3)$, with $a=f'(r)\ne0$ and $b=f''(r)/2$, gives

$$\frac{f(x_k)-f(x_{k-1})}{x_k-x_{k-1}}
=a+b(e_k+e_{k-1})+\cdots.$$

Substituting in the secant update and cancelling the leading linear term gives

$$e_{k+1}\approx\frac{b}{a}e_k e_{k-1}.$$

Suppose this nonzero leading term controls the iteration and the errors obey
$|e_k|\sim K|e_{k-1}|^p$. Then $|e_{k-1}|$ scales like $|e_k|^{1/p}$, so

$$|e_{k+1}|\propto |e_k|^{1+1/p},\qquad p=1+1/p.$$

Thus $p^2-p-1=0$, and the positive root is $(1+\sqrt5)/2$. The result comes
from reusing two iterates, not from a universal empirical ranking of solvers.
If the leading coefficient vanishes, the root is repeated, or rounding dominates,
this particular asymptotic calculation does not describe the measured sequence.

:::{note} Predict before comparing costs
Newton uses a derivative; secant reuses a previous function evaluation. If one
derivative evaluation costs ten function evaluations, does quadratic order alone
establish that Newton needs less work? Explain which convergence regime and
initialization costs you would need to measure.
:::

:::{tip} Answer: an order is not a timing result
:class: dropdown
Count the work needed to reach the same justified error target, including
initialization and failed steps. Newton may need fewer iterations but more
expensive evaluations. The local order describes an asymptotic error relation;
it does not supply the constants, basin of convergence, or runtime of an
application's derivative calculation.
:::

(week5-convergence)=
### Comparison of Convergence Rates

| Method | Order | Error Reduction | Digits Gained/Iteration | Function Evals |
|--------|-------|----------------|------------------------|----------------|
| Bisection | 1.0 (bound) | Half-width halves; actual error need not | About 0.30 in the bound | 1 |
| Secant | 1.618 | $\lvert e_{n+1}\rvert \approx C\lvert e_n\rvert^{1.618}$ | Correct-digit count grows by roughly 1.618 | 1 new, after initialization |
| Newton | 2.0 | $e_{n+1} \approx Ce_n^2$ | Doubles | 2 (f and f') |

The bracket bound can contract even when successive midpoint errors do not.
The computed example below uses $f(x)=x^2-2$; it compares actual errors with
the bisection bound, not with residuals or update sizes.

<!-- Lecture-figure public copies retain their basenames. Sources: _instructor/python/figures/generate_lecture910.py, generate_lecture9_overview.py, and generate_lecture9_levenberg.py. -->
::::{figure} figures/l9-convergence.svg
:alt: Log plot for the root of x squared minus two. Bisection midpoint errors sometimes rise, while the dashed bracket-error bound halves each iteration; Newton errors fall rapidly until zero errors are omitted from the log axis.

The measured midpoint error can rise while its guaranteed bracket bound falls.
Zero error cannot be displayed on a logarithmic axis.

[Open full-size figure](figures/l9-convergence.svg)
::::

There is no universal absolute cutoff for a "small" secant denominator:
multiplying the equation by a constant scales that denominator while leaving
the exact secant step unchanged. Compare evaluation uncertainty with the local
function-value scale and inspect the proposed step. If function error dominates
the difference, report an unreliable slope or use a justified safeguard.
Project 3 requires explicit handling of zero denominators and nonfinite values;
it does not prescribe an extra arbitrary near-zero threshold.

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| f(x₀) $\approx$ f(x_{1}) | Near-zero denominator | Report an unusable slope; restart with justified points or use a bracketed safeguard |
| Parallel secants | No convergence | Restart with different points |
| Leaves bracket | May miss root | Use a bracket-preserving hybrid; Brent is one specific algorithm, not any secant/bisection combination |

:::{note} Check Your Understanding
1. What is the main advantage of secant over Newton's method?
2. Why might secant converge faster than bisection but slower than Newton?
3. How many previous points does secant method need to compute the next?
4. When would you choose secant over the other methods?
:::

:::{tip} Answers and reasoning
:class: dropdown

1. Secant needs function values but no analytic derivative.
2. Near a smooth simple root its two-point error recurrence gives superlinear order about 1.618. Newton uses derivative information to reach quadratic order; bisection instead guarantees a halving bracket bound.
3. Two previous points and their function values; after initialization, only one new function value is needed per update.
4. Secant is useful when derivatives are expensive and starting points are credible. If maintaining a bracket is essential, use a safeguarded method rather than assuming secant retains it.
:::

---

(backtracking-newton)=
## Backtracking: choose how far to follow Newton

Newton proposes a direction $p=-f(x)/f'(x)$. A **line search** chooses a step
length $\alpha$ along that direction:

$$x_{\rm trial}=x+\alpha p,\qquad 0<\alpha\le1.$$

The full Newton step uses $\alpha=1$. Backtracking starts there and shortens the
step when it fails an acceptance test. This controls a local proposal; it does
not preserve a root bracket or select a physically meaningful root.

::::{figure} figures/l9-newton-proposal.svg
:alt: Arctangent curve at x equals two with a tangent whose zero is near minus 3.536, far beyond the true root at zero.

Newton finds the zero of a local tangent. That proposal still needs an actual
function evaluation before it can be accepted.

[Open full-size figure](figures/l9-newton-proposal.svg)
::::

### Define progress before testing a step

For a scalar equation, use the merit function $\phi(x)=\tfrac12 f(x)^2$.
With a differentiable $f$ and finite nonzero $f'(x)$, an exact Newton direction
satisfies

$$\phi'(x)p=f(x)f'(x)\left(-\frac{f(x)}{f'(x)}\right)=-f(x)^2<0$$

at a nonroot. It is a descent direction locally, although a full step can
increase the merit function. The Armijo sufficient-decrease test is

$$\phi(x+\alpha p)\le\phi(x)+c\alpha\phi'(x)p
=\phi(x)-c\alpha f(x)^2.$$

Choose $0<c<1/2$ here; the example uses $c=10^{-4}$ and halves $\alpha$
after each rejection. These are illustrative algorithm settings, not accuracy
tolerances. Under the differentiability and descent assumptions, sufficiently
small positive steps satisfy this test in exact arithmetic. A finite search
budget, floating-point stagnation, or unreliable evaluations can still prevent
an implementation from accepting a step.

### Predict, compare, explain: one accepted step

For $f(x)=\arctan x$, start at $x=2$. Predict whether the full Newton step reduces $|f|$, then compare these candidate trials (including an extra quarter-step for comparison). This is one step, not a complete solve.

| Step fraction $\alpha$ | Trial $x+\alpha p$ | Residual magnitude | Armijo test |
|:--|:--|:--|:--|
| $1$ | $-3.535744$ | $1.295169$ | Reject |
| $1/2$ | $-0.767872$ | $0.654841$ | Accept |
| $1/4$ | $0.616064$ | $0.552148$ | Accept |

::::{figure} figures/l9-backtracking.svg
:alt: Merit function along the Newton direction from x equals two. The full step fails the sufficient-decrease line; the half-step passes it, so backtracking accepts that first passing trial.

The acceptance test compares the actual merit value with the sufficient-decrease
threshold. The quarter-step is shown only to compare candidates; an ordinary
backtracking search would stop at the accepted half-step.

[Open full-size figure](figures/l9-backtracking.svg)
::::

Backtracking accepts the first passing trial, not necessarily the best point on the line. Explain why an accepted step neither identifies a root nor preserves a bracket. No line-search implementation is assigned.

The full step reaches approximately −3.536 and increases the residual
magnitude. One halving reaches approximately −0.768 and satisfies sufficient
decrease. This is progress, not a converged root. A complete solver still needs
an outer iteration budget, stopping rules, diagnostics, and a physical-domain
check. Domain-restricted functions also need an explicit feasible-trial policy;
this example does not turn arbitrary domain errors into successful steps.

:::{warning} Decrease is not a root certificate
A line search can approach a stationary point of $\phi$ with $f\ne0$.
For example, $f(x)=x^2+1$ has no real root, although $\phi$ has a minimum at
zero. Small accepted steps can indicate stagnation. Inspect the defining
equation and its sensitivity, not just whether steps were accepted. A computed
zero can arise from underflow here as in the other methods.
:::

### Three different ways to control a proposal

| Approach | What it controls | What it does not establish by itself |
|:--|:--|:--|
| Backtracking line search | Distance along a direction, using sufficient decrease | A root-error bound, a bracket, or the physical root |
| Bracket-preserving hybrid | Proposed steps plus reliable bracket reduction | Continuity or correctness of supplied function signs |
| Levenberg regularization | The linear system that defines the direction | A zero residual or a globally successful solve |

FNC's [quasi-Newton chapter](https://fncbook.com/quasinewton/) develops
Levenberg's method for nonlinear systems: regularization changes the proposed
step, and residual reduction governs acceptance. It is related to step control
but is not the scalar backtracking algorithm above. For a production
Newton/line-search interface, see [PETSc](https://petsc.org/release/manualpages/SNES/SNESNEWTONLS/).
Levenberg's method is a preview for later nonlinear least squares, not another
algorithm to implement this week.

(week5-jacobians)=
### Jacobians and local fitting · Week 5 companion

For observations $y_i$ and a model $g(t_i;\theta)$, define residuals $r_i=g(t_i;\theta)-y_i$. With $m$ observations and $n$ parameters, the Jacobian $J$ has shape $m\times n$ and entries $J_{ij}=\partial r_i/\partial\theta_j$. Each row describes one observation; each column describes sensitivity to one parameter.

::::{figure} figures/l9-fit-residuals.svg
:alt: Constructed observations beside a candidate exponential decay curve. Vertical segments show each prediction minus observation and therefore the residuals used in the fit.

Changing either parameter changes several residuals at once. These points are
constructed for illustration, not measured data or the three-point Jacobian
example that follows.

[Open full-size figure](figures/l9-fit-residuals.svg)
::::

For a small parameter update $p$, $r(\theta+p)\approx r(\theta)+Jp$. The product predicts a **change**, not the new residual itself.

For $g(t;A,k)=Ae^{-kt}$ at $A=2$, $k=\ln2$, and $t=0,1,2$ (scaled, dimensionless coordinates),
$$J=\begin{bmatrix}1&0\\1/2&-1\\1/4&-1\end{bmatrix}.$$
The update $p=(0.10,0.02)^{\mathsf T}$ predicts changes $(0.10,0.03,0.005)^{\mathsf T}$. Actual changes are approximately $(0.10,0.029209,0.004414)^{\mathsf T}$. Reducing the step by ten reduces the largest discrepancy by about 99: the linear approximation improves locally.

The least-squares loss is $\Phi=\tfrac12\lVert r\rVert^2$, where $\lVert r\rVert^2=\sum_i r_i^2$. Transpose, written $\mathsf T$, exchanges rows and columns. The loss gradient (its parameter partial derivatives) is $J^{\mathsf T}r$.

Gauss–Newton minimizes $\tfrac12\lVert r+Jp\rVert^2$. A Levenberg step adds a penalty on the current update:
$$q_\lambda(p)=\tfrac12\lVert r+Jp\rVert^2+\tfrac\lambda2\lVert p\rVert^2.$$
Setting $\nabla_p q_\lambda=J^{\mathsf T}(r+Jp)+\lambda p=0$ gives
$$(J^{\mathsf T}J+\lambda I)p=-J^{\mathsf T}r.$$
Here $I$ is the identity matrix and $\lambda>0$ controls damping. The parameters must be scaled sensibly; Marquardt variants incorporate scaling. This is a penalty on an update, not a fixed prior on the parameters. Check actual loss reduction before accepting a trial. The displayed normal equations explain the method; production solvers can use QR or SVD to avoid the conditioning penalty of explicitly forming $J^{\mathsf T}J$.

::::{figure} figures/l9-levenberg-damping.svg
:alt: Contours of a constructed exponential fit's local squared residual. A cross marks the local-model minimum; arrows from zero show alternative damped proposals, not successive iterations. Larger damping shortens and rotates the proposal.

Contours show the **local** squared-residual model in scaled parameter updates.
Each arrow starts at zero and represents a different damping choice, not the
next point of one trajectory. Actual loss must be checked separately.

[Open full-size figure](figures/l9-levenberg-damping.svg)
::::

In regression and calibration, noisy data generally cannot all have zero residual. This differs from solving a square system $F(u)=0$, where a nonsingular (invertible) Jacobian gives the Newton proposal $J_Fp=-F$. Damping can control a poor step but cannot create information absent from the observations. For example, early observations of a decay curve weakly constrain $k$ because $\partial g/\partial k=-At e^{-kt}$ is small near $t=0$.

**Explain:** why can a tiny damped step coexist with a large residual? No implementation of these advanced fitting methods is required for Project 3.

(week5-hybrids)=
## Hybrid Methods: preserve a bracket while using local models

A safeguarded method uses interpolation or a derivative when the proposed step is acceptable and falls back to bracket reduction when it is not.

::::{figure} figures/l9-bracket-safeguard.svg
:alt: Arctangent curve with a sign-changing bracket from minus one to two. The Newton proposal from two falls outside it; midpoint one half stays inside and supplies a bracket-reducing fallback.

The fallback protects the sign-changing bracket. It does not claim that every
accepted local proposal is a root.

[Open full-size figure](figures/l9-bracket-safeguard.svg)
::::

### Brent's Method

Combines bisection's reliability with inverse quadratic interpolation's speed:
- Maintains a bracketing interval like bisection
- Tries fast interpolation when possible  
- Falls back to bisection if interpolation fails
- Safeguards maintain convergence from a valid continuous bracket; often needs fewer evaluations than bisection

### Practical Strategy for Robust Root Finding

```
1. Find a continuous sign-change bracket by physics or a scan, then use bisection
2. Propose a local Newton or interpolation step while retaining the bracket
3. Reject unsafe proposals and enforce regular bracket reduction
4. Monitor bracket width, residual scale, stagnation, and evaluation cost
```

:::{figure} figures/2_3_hybrid_method_performance.webp
:label: fig-hybrid-method-performance
:width: 100%
:alt: A function plot and recorded error histories compare bisection, Newton, and safeguarded Newton under a twenty-iteration cap; curves stop at termination.

Measured histories for $f(x)=x^{20}-1$, with root 1. Bisection and the
safeguarded Newton method start with $[0.8,1.3]$; Newton starts at $x_0=0.8$.
All runs have a 20-iteration cap. Bracketed methods stop at half-width
$10^{-10}$ or a sampled zero. Newton stops at a sampled zero, floating-point
stagnation, or the cap. The hybrid takes a midpoint at least every other update. On intervening
updates it accepts a finite Newton proposal only strictly inside the bracket;
otherwise it also takes the midpoint. This is an
illustrative safeguarded Newton method, not Brent's algorithm. Curves end at
termination; zero errors are omitted from the logarithmic axis. A large early
Newton step or an unmet iteration cap does not prove eventual divergence.
The reference root is exact; this plot reports measured outcomes rather than
assigning a universal speed ranking.

[Open full-size figure](figures/2_3_hybrid_method_performance.webp)
:::

All three hard-example runs reach the stated 20-iteration cap. Their final
position errors are different; none should be reported as satisfying its
stopping contract merely because one plotted error is small.


---

(root-investigation)=
## Investigation: which root estimate is justified?

Suppose three methods report nearly the same root. One stopped because the
residual was small, one because the last step was small, and one because a
bracket was narrow. These are different observations. Which one controls the
position of the root, and what additional information does each require?

Return to the cubic $f(x)=x^3-2x-5$ from the opening figure. It is continuous,
and $f'(x)=3x^2-2\ge10$ on $[2,2.5]$, so a sign-changing bracket there
contains one root. Before inspecting the recorded histories, predict:

1. Must a bisection midpoint become more accurate at every iteration?
2. Can Newton make a small step without a small position error?
3. Does one Newton iteration cost the same as one secant iteration?
4. Which conclusion survives multiplying the whole equation by $10^{-12}$?

For this problem, a bracket midpoint has position error at most the
half-width. At a candidate in $[2,2.5]$, the derivative bound also gives
$|x-r|\le |f(x)|/10$. The last step $|x_k-x_{k-1}|$ is neither of these
bounds. It measures what the algorithm just did, not its distance from the
answer. Stagnation can make it zero even when a target remains unmet.

<!-- root-data:start -->
The final recorded rows from the cubic comparison are:

| Method | $\lvert f(x)\rvert$ | Last recorded step | Actual position error | $f$ calls | $f'$ calls | Stop |
|---|---|---|---|---|---|---|
| bisection | 6.168e-10 | 5.821e-11 | 5.526e-11 | 36 | 0 | width tolerance |
| newton | 8.882e-16 | 4.441e-16 | 0.000e+00 | 6 | 6 | floating-point stagnation |
| secant | 8.882e-16 | 8.882e-16 | 0.000e+00 | 9 | 0 | floating-point stagnation |

A printed zero position error means agreement with the binary64 reference, not
an exact representation of the mathematical root. A sampled zero residual also
requires the function-evaluation caveat discussed with bisection.


<!-- root-data:end -->

The comparison figure reports real errors against an independent decimal
reference. Those errors are available for this teaching example; the method
cannot normally inspect them. Its stopping condition must use information
available during the calculation. Count calls to $f$ and $f'$ separately:
a derivative may be cheaper, more expensive, or computed together with $f$.
An iteration count by itself does not settle the cost comparison.

:::{tip} Explain the evidence before choosing a method
:class: dropdown
Bisection guarantees that its bound shrinks, not that every midpoint is better
than the last. Newton's last step is a useful diagnostic, but it is not a
position certificate. A residual becomes a position bound only with a valid
slope bound and reliable function values. Rescaling $f$ changes both its
residual and derivative scale; the ratio $|f(x)|/m$ is unchanged when both are
scaled consistently. Bracket widths are unchanged too. The physical question
and its units determine which reported digits matter.
:::

### Transfer: an accurate solve of an uncertain function

Now suppose the function values themselves have a bounded additive uncertainty
$\eta$. This is a different experiment from multiplying an exact equation by a
constant. Keep $x$ and function values dimensionless, and consider

$$f_s(x)=s(x-1),\qquad |\delta f(x)|\le\eta.$$

The unperturbed root is 1. Any perturbed zero obeys
$|x-1|\le\eta/|s|$. A smaller slope therefore permits a wider range of root
positions for the **same absolute uncertainty**. A tighter iteration tolerance
cannot distinguish among those possible input functions.

:::{figure} figures/root-uncertainty-band.png
:label: root-uncertainty-band
:alt: Two linear functions with slopes one and 0.05 have the same vertical uncertainty of 0.002; their possible root half-ranges are 0.002 and 0.04.

The vertical band represents allowed changes to the supplied function. Its
intersection with the horizontal axis gives possible root positions, not
iteration histories or statistical confidence intervals. The same uncertainty
produces different position ranges because the slopes differ.

[Open full-size figure](figures/root-uncertainty-band.png)
:::

```{code-cell} python
# These are possible-input bounds, not errors measured from a root solver.
slopes = np.array([1.0, 0.05])
function_uncertainty = 0.002
root_half_ranges = function_uncertainty / np.abs(slopes)
for slope, half_range in zip(slopes, root_half_ranges):
    print(f"slope={slope:g}: possible roots in [{1-half_range:.3f}, {1+half_range:.3f}]")
```

Predict what happens to this range if we halve the solver tolerance, halve
$\eta$, or multiply both $f_s$ and its uncertainty by 100. Only one of those
changes improves the information supplied about the root.

A repeated root makes the issue sharper. For $f(x)=(x-1)^2$, a downward
constant perturbation of size $\eta>0$ produces two zeros,
$1\pm\sqrt{\eta}$, while an upward perturbation removes the real zero.
There is no nonzero derivative lower bound at the original root. For the
unperturbed function, Newton's exact recurrence is

$$x_{k+1}-1=\frac12(x_k-1).$$

A tiny residual is especially easy to obtain here because it is the square of
the position error. For example, residual $10^{-12}$ corresponds to position
error $10^{-6}$, not $10^{-12}$.

:::{tip} Answer: what would justify another digit?
:class: dropdown
Halving the solver tolerance only refines a solve of the supplied function.
Halving the input uncertainty narrows the possible-root interval. Multiplying
both the function and its uncertainty by 100 leaves the interval unchanged.
For a repeated root, a smooth-simple-root theorem cannot justify quadratic
convergence or convert the residual through a nonzero slope bound. Before
reporting more digits, distinguish iteration error from uncertainty in the
function being solved; then identify which independent calculation or better
measurement would reduce the limiting contribution.
:::

[Further reading: conditioning, residuals, and multiple roots](https://fncbook.com/rootproblem/).


## Application: Units and Scaling

Choose scales that make the variables and tolerances interpretable. Non-dimensionalization can avoid extreme arithmetic and improve numerical balancing, but it does not remove intrinsic sensitivity:

**Dimensional form**: Finding radius where $\rho(r) = 10^{-7}$ g/cm$^3$ with $r$ in cm
**Scaled form**: Define $\tilde{r} = r/R_{\odot}$, $\tilde{\rho} = \rho/\rho_0$ and solve $\tilde{\rho}(\tilde{r}) = 10^{-7}\,\mathrm{g\,cm^{-3}}/\rho_0$ (equal to 1 only if that target is the chosen $\rho_0$)

Track the units of the position tolerance and transform it with the variable. Rescaling an equation changes its residual values; it does not by itself make a root better determined by the physical data.

---

(physical-example)=
## Physical Example: Stellar Structure Equilibrium

In stellar interiors, hydrostatic equilibrium requires:
$$\frac{dP}{dr} = -\frac{GM(r)\rho(r)}{r^2}$$

For a polytrope with $P = K\rho^{1+1/n}$, the Lane-Emden equation describes stellar structure:
$$\frac{1}{\xi^2}\frac{d}{d\xi}\left(\xi^2\frac{d\theta}{d\xi}\right) + \theta^n = 0$$

where $\xi$ is dimensionless radius and $\theta$ is related to density.

The stellar surface occurs where $\theta(\xi_1) = 0$—a root-finding problem!

For different polytropic indices:
- $n=0$ is the constant-density Lane–Emden limit: $\theta=1-\xi^2/6$, so $\xi_1=\sqrt6$.
- $n=1$ has $\theta=\sin\xi/\xi$, with its central value defined by the limit 1; $\xi_1=\pi$. This is a $P=K\rho^2$ polytrope, not an isothermal core.
- $n=3$ has $\xi_1\approx6.897$ and appears in idealized radiation-supported and relativistically degenerate models.
- $n=5$ has $\theta=(1+\xi^2/3)^{-1/2}$: it approaches zero only at infinite radius, although its total mass is finite. It is not a minimum-mass-star model.

These solutions use $\theta(0)=1$ and $\theta'(0)=0$.
[Reference: analytic polytropes](https://www.astro.princeton.edu/~gk/A403/polytrop.pdf).

A computed Lane–Emden trajectory can supply both $\theta$ and its derivative near the surface. Root refinement then depends on the accuracy of that trajectory as well as on the root solver. Tightening a root tolerance cannot remove the ODE or interpolation error. Preserve a credible surface bracket and refine the underlying trajectory before claiming additional digits.

---

(worked-example-keplers-equation)=
## Worked Example: Kepler's Equation

The most famous root-finding problem in astronomy is Kepler's equation, which relates mean anomaly $M$ (proportional to time) to eccentric anomaly $E$ (related to position):

$$E - e\sin(E) = M$$

where $e$ is the orbital eccentricity and both $M$ and $E$ are in radians.

### Why This Is Hard

- Transcendental equation (no algebraic solution)
- Must be solved millions of times in orbit propagation
- High eccentricity makes convergence difficult
- Conditioning worsens as $e \to 1$ (parabolic orbit)

### Newton's Method Applied

Define $f(E) = E - e\sin(E) - M$

Then $f'(E) = 1 - e\cos(E)$

Newton iteration:
$$E_{n+1} = E_n - \frac{E_n - e\sin(E_n) - M}{1 - e\cos(E_n)}$$

For an ellipse, $0\le e<1$, so $f'(E)=1-e\cos E\ge1-e>0$. The derivative can become small near periapsis as $e$ approaches 1, but it cannot vanish in this domain.

### Initial Guess Strategy

One heuristic on a reduced mean-anomaly interval is to start with $E_0=M$
for $e<0.8$ and $E_0=\pi$ otherwise. The value 0.8 is not a convergence
threshold, and the first regime is not uniformly nearly circular. Compare
both guesses over the project's sweep and report failures and iteration counts.
If reducing $M$ modulo $2\pi$, restore its branch in the returned $E$.

### Convergence Analysis

The absolute sensitivity to mean anomaly is

$$\frac{dE}{dM}=\frac{1}{1-e\cos E}\le\frac{1}{1-e}.$$

For $e=0$, $E=M$ exactly. For $e=0.9$ the upper bound is 10, and for
$e=0.99$ it is 100; these are bounds, not the sensitivity at every orbital
phase. Iteration counts also depend on $M$, the initial guess, and the stopping
criterion. Normalize $M$ to $[0,2\pi]$ for the initial-guess choices above.
Because the residual is increasing and changes sign on $[0,2\pi]$ for an
interior $M$, bisection provides a useful independent check on Newton's answer.

:::{tip} Orbital application
Kepler's equation converts orbital elements into positions and supplies a
two-body reference for later orbit calculations. It is an application of this
reading, not an additional Project 2 deliverable.
:::

---

## Practical Algorithm for Finding Initial Brackets

To find initial brackets for bisection:

```{code-cell} python
def find_brackets(f, x_min, x_max, n_scan=100):
    """Return sign-change intervals and (x, x) pairs for sampled zeros."""
    if isinstance(n_scan, (bool, np.bool_)) or not isinstance(n_scan, (int, np.integer)) or n_scan <= 0:
        raise ValueError("n_scan must be a positive integer")
    if not (np.isfinite(x_min) and np.isfinite(x_max) and x_min < x_max):
        raise ValueError("Need finite increasing scan limits")
    nodes = np.linspace(x_min, x_max, n_scan + 1)
    values = np.array([float(f(x)) for x in nodes])
    if not np.all(np.isfinite(values)):
        raise ValueError("Non-finite value in scan")
    brackets = []
    for i, (x, fx) in enumerate(zip(nodes, values)):
        if fx == 0.0:
            brackets.append((x, x))
        elif i > 0 and values[i-1] != 0.0 and (values[i-1] < 0) != (fx < 0):
            brackets.append((nodes[i-1], x))
    return brackets

print(find_brackets(lambda x: x - 0.5, 0.0, 1.0))
```

A scan can miss an even-multiplicity root between samples or several crossings
within one cell. A sampled zero is reported once, as a zero-width pair; the
reading's `bisection` accepts it. Project 3's `bisect` requires `a < b`,
so retain these sampled roots separately and send only positive-width brackets
to that solver. Neither a sign scan nor bisection proves
continuity or verifies that a computed zero did not arise from underflow.


---

## Debugging Root Finding

Common root-finding bugs and their diagnosis:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Bisection won't start | Same sign at endpoints | Scan for sign changes first |
| Newton diverges | Poor initial guess or a small derivative | Find and verify a sign-changing bracket first, then apply bisection; a line search is another step-control option with different guarantees |
| Secant oscillates | An unreliable slope or poor starting points | Inspect the function-value scale, separation of inputs, and proposed step; reject zero/nonfinite denominators or unusable updates, then restart or safeguard |
| Wrong root found | Multiple roots in region | Narrow search interval |
| No progress | No representable interior point or unmet iteration cap | Report failure; reassess position tolerance and scaling |
| No convergence | Discontinuous function | Check function continuity |

---

## Bridge to Part 2: From Finding Zeros to Measuring Areas

You can now compare three kinds of evidence: a shrinking bracket, a local iteration model, and a residual interpreted through sensitivity. A method choice should identify which of these supports the reported root.

But finding equilibrium points is only half the story. Next, we tackle integration — measuring quantities across space and time. You'll discover how the same principles of approximation and error analysis apply to computing areas under curves, volumes of regions, and integrals over high-dimensional spaces.

The synthesis returns to a problem in which an integral defines the root residual. The two algorithms have separate jobs, but their errors contribute to one final answer.

*Next: Part 2 - Quadrature*
