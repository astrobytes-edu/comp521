---
title: "Part 1: Root Finding - Where Physics Reaches Equilibrium"
subtitle: "Static Problems & Quadrature | Numerical Methods Module 2 | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is still being revised
Readings are reviewed and finalized **at least one week before they are
assigned**, so you will always have a settled version before you need it. Until
then, expect rough edges — wording, examples, and cross-references may change.

Where a reading disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
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

## The Fundamental Problem

:::{margin}
**Root/Zero**: A value $x^*$ where $f(x^*) = 0$. The x-intercept of the function. In physics, often represents equilibrium points.
:::

:::{margin}
**Transcendental equation**: An equation involving transcendental functions (sin, cos, exp, log) that cannot be solved algebraically.
:::

In physics, equilibrium occurs where the net force vanishes, where energy is minimized, or where competing effects balance. Mathematically, these all reduce to finding **roots** of equations: solving $f(x) = 0$.

But here's the challenge: most astrophysical equations are **transcendental equations** that cannot be solved analytically. Consider finding where a star's pressure balances gravity:

$$\frac{dP}{dr} = -\frac{GM(r)\rho(r)}{r^2}$$

With realistic equations of state and composition gradients, this becomes a transcendental equation with no closed-form solution. We need numerical methods.

:::{margin}
**Condition number**: For root finding, $\kappa = \frac{1}{|f'(r)|}$. Large $\kappa$ means the problem is sensitive to small changes — ill-conditioned.
:::

:::{note} Connection to Module 1
Root finding uses the same error analysis framework from Module 1:

- **Truncation error**: From stopping iterations early (like truncating Taylor series)
- **Round-off error**: From finite precision (especially near f'(x) = 0)
- **Optimal parameters**: Balancing accuracy vs computation (like choosing h)

The secant method even uses finite differences to approximate f'(x)!
:::

## Building Intuition: The Geometry of Root Finding

Before diving into algorithms, let's understand the geometry. Finding roots is about discovering where a curve crosses the x-axis. Different methods use different geometric insights:

:::{margin}
**Bracketing**: Having two points where the function has opposite signs, guaranteeing a root between them by the Intermediate Value Theorem.
:::

:::{margin}
**Interpolation**: Approximating a function between known points using simpler functions (lines, parabolas, etc.).
:::

1. **Bracketing methods** (Bisection): Trap the root between two points and squeeze — when you absolutely must find the root, even if slowly
2. **Local approximation methods** (Newton): Follow the tangent line to the axis — when you need maximum speed and have derivatives
3. **Interpolation methods** (Secant): Approximate the curve with simpler functions — the practical compromise when derivatives are expensive

Each approach has trade-offs between:

- **Reliability**: Will it always find a root?
- **Speed**: How many iterations to converge?
- **Requirements**: Do we need derivatives? Good initial guesses?

![**Three geometric approaches to root finding.** The top panels show how bisection (bracketing), Newton (tangent lines), and secant (interpolation) methods work geometrically on the function $f(x) = x^3 - 2x - 5$. The bottom-right convergence plot reveals the mathematical power of each approach: bisection's reliable but slow linear convergence, secant's faster superlinear convergence, and Newton's rapid quadratic convergence when conditions are favorable. Note how the different slopes on the log-scale plot correspond to different convergence orders—a key signature for identifying method performance in practice.](figures/2_1_root_methods_comparison.png){#fig-root-methods-comparison width="100%"}

---

## Method 1: Bisection - The Reliable Workhorse

### The Mathematical Foundation

:::{margin}
**Intermediate Value Theorem**: If $f$ is continuous on $[a,b]$ and $k$ is any value between $f(a)$ and $f(b)$, then there exists at least one $c \in (a,b)$ where $f(c) = k$.
:::

The bisection method is based on the **Intermediate Value Theorem**: 

> If $f$ is continuous on $[a,b]$ and $f(a) \cdot f(b) < 0$, then there exists at least one root $r \in (a,b)$ where $f(r) = 0$.

The algorithm repeatedly halves the interval, keeping the half that contains the root.

### Algorithm Analysis

Starting with interval $[a_0, b_0]$ where $f(a_0) \cdot f(b_0) < 0$:

1. Compute midpoint: $c_n = \frac{a_n + b_n}{2}$
2. Evaluate $f(c_n)$
3. Update interval:
   - If $|f(c_n)| < \epsilon_{tol}$: Found root to desired accuracy
   - If $f(a_n) \cdot f(c_n) < 0$: root in $[a_n, c_n]$, so set $b_{n+1} = c_n$, $a_{n+1} = a_n$
   - Otherwise: root in $[c_n, b_n]$, so set $a_{n+1} = c_n$, $b_{n+1} = b_n$

After $n$ iterations, the interval width is:

$$|b_n - a_n| = \frac{|b_0 - a_0|}{2^n}$$

:::{margin}
**Linear convergence**: Error decreases by a constant factor each iteration. Here, that factor is 1/2.
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

So we need 33 iterations — slow but guaranteed!

### Implementation

Here's a complete bisection implementation to understand the algorithm:

```python
def bisection(f, a, b, tol=1e-10, max_iter=100):
    """Find root of f in [a,b] by bisection"""
    # Check initial bracket
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError("Need f(a) and f(b) with opposite signs")
    if abs(fa) < tol: return a
    if abs(fb) < tol: return b
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol or abs(b - a) < 2*tol:
            return c
            
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
            
    raise RuntimeError(f"Failed to converge in {max_iter} iterations")
```

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| No sign change | Won't start | Scan interval for brackets first |
| Multiple roots | Finds arbitrary one | Use smaller initial intervals |
| Discontinuity | False bracket | Check continuity requirement |
| $f$ touches zero | No sign change | Use $f^{2}(x)$ which has same roots |

:::{note} Check Your Understanding
1. Why does bisection require $f(a) \cdot f(b) < 0$?
2. What happens if there are multiple roots in $[a,b]$?
3. Can bisection find roots where $f$ touches but doesn't cross zero?
4. If you need 6 decimal places and start with $[0, 10]$, how many iterations?
:::

---

## Method 2: Newton-Raphson - The Speed Demon

### The Geometric Insight

:::{margin}
**Tangent line approximation**: Replacing a curve with its tangent line at a point, valid for small deviations.
:::

Newton's method uses calculus to accelerate convergence. The key insight: near any point, a smooth function looks approximately linear. We can follow the **tangent line** to where it crosses the axis, getting much closer to the root in a single step.

### Mathematical Derivation

Starting at point $x_n$, the tangent line to $f(x)$ has equation:

$$y - f(x_n) = f'(x_n)(x - x_n)$$

This line crosses the x-axis (where $y = 0$) at:

$$0 - f(x_n) = f'(x_n)(x_{n+1} - x_n)$$

Solving for $x_{n+1}$:

$$\boxed{x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}}$$

This is the Newton-Raphson iteration formula.

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

:::{margin}
**Quadratic convergence**: Error is squared each iteration, doubling the number of correct digits.
:::

This shows **quadratic convergence**! The error is squared each iteration, meaning the number of correct digits approximately doubles.

### When Newton Fails

Despite its speed, Newton's method can fail spectacularly:

1. **Zero derivative**: If $f'(x_n) = 0$, the tangent is horizontal and never crosses the axis
2. **Poor initial guess**: May diverge or converge to wrong root
3. **Cycles**: Can oscillate between points without converging
4. **Ill-conditioned**: When $|f'(r)|$ is very small, round-off errors dominate

![**When Newton's method fails.** Four critical failure modes illustrate why Newton's method, despite its speed, requires careful application: (a) **Cycling behavior** occurs when iterates bounce between points without converging; (b) **Divergence** from poor initial guesses sends the method away from the root; (c) **Vertical tangents** (infinite derivatives) cause division by zero; (d) **Repeated roots** reduce convergence from quadratic to merely linear. Understanding these failure patterns is essential for robust algorithm design—they explain why production codes often combine Newton with bracketing methods for reliability.](figures/2_2_newton_failure_modes.png){#fig-newton-failure-modes width="100%"}

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| f'(x) $\approx$ 0 | Division by small number | Switch to bisection |
| Bad initial guess | Divergence | Use bisection to bracket first |
| Oscillation | Repeating values | Detect cycles, switch methods |
| Repeated root | Slow convergence | Use modified Newton: $x_{n+1} = x_n - m\frac{f(x_n)}{f'(x_n)}$ |

:::{tip} Physical Example: Finding Lagrange Points
In the circular restricted three-body problem, the effective potential is:
$$\Phi_{eff} = -\frac{GM_1}{r_1} - \frac{GM_2}{r_2} - \frac{1}{2}\omega^2(x^2 + y^2)$$

Lagrange points occur where $\nabla\Phi_{eff} = 0$. Newton's method excels here because we can analytically compute the gradient and Hessian!
:::

---

## Method 3: Secant - The Practical Compromise

### Motivation: No Derivatives Required

:::{margin}
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

The convergence of the secant method is more complex. Through detailed analysis (involving difference equations), one can show that the order of convergence is:

$$\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618$$

This is the golden ratio! The error satisfies:

$$|e_{n+1}| \approx C|e_n|^{1.618}$$

:::{margin}
**Superlinear convergence**: Faster than linear but slower than quadratic. The golden ratio appears because the error recurrence relation has Fibonacci-like structure.
:::

This **superlinear convergence** is slower than Newton's quadratic rate but faster than bisection's linear rate.

### Comparison of Convergence Rates

| Method | Order | Error Reduction | Digits Gained/Iteration | Function Evals |
|--------|-------|----------------|------------------------|----------------|
| Bisection | 1.0 | $e_{n+1} = \frac{1}{2}e_n$ | 0.30 | 1 |
| Secant | 1.618 | $e_{n+1} \approx Ce_n^{1.618}$ | ~0.62 | 1 |
| Newton | 2.0 | $e_{n+1} \approx Ce_n^2$ | Doubles | 2 (f and f') |

### Common Failure Modes and Fixes

| Problem | Symptom | Solution |
|---------|---------|----------|
| f(x₀) $\approx$ f(x_{1}) | Near-zero denominator | Perturb one point slightly |
| Parallel secants | No convergence | Restart with different points |
| Leaves bracket | May miss root | Combine with bisection (Brent's method) |

:::{note} Check Your Understanding
1. What is the main advantage of secant over Newton's method?
2. Why might secant converge faster than bisection but slower than Newton?
3. How many previous points does secant method need to compute the next?
4. When would you choose secant over the other methods?
:::

---

## Hybrid Methods: Best of All Worlds

In practice, we often combine methods to leverage their strengths:

### Brent's Method

Combines bisection's reliability with inverse quadratic interpolation's speed:
- Maintains a bracketing interval like bisection
- Tries fast interpolation when possible  
- Falls back to bisection if interpolation fails
- Never worse than bisection, often much faster

### Practical Strategy for Robust Root Finding

```
1. Start with bisection to bracket the root
2. Switch to Newton/Secant once close enough  
3. Fall back to bisection if Newton diverges
4. Monitor condition number throughout
```

![**Why production codes use hybrid methods.** Testing on the challenging function $f(x) = x^{20} - 1$ near $x = 1$ reveals the power of combining methods. **Pure Newton** (red) fails catastrophically from poor initial guesses due to the extreme conditioning of this function. **Pure bisection** (pink) is reliable but painfully slow, requiring dozens of iterations. The **hybrid approach** (blue) intelligently switches between methods: it uses bisection to establish a safe bracket, then switches to Newton for rapid final convergence, falling back to bisection if Newton steps become unreliable. This adaptive strategy delivers both robustness and speed—explaining why sophisticated root-finding libraries like those in SciPy implement such hybrid algorithms.](figures/2_3_hybrid_method_performance.png){#fig-hybrid-method-performance width="100%"}

---

## Application: Units and Scaling

Always non-dimensionalize your equations before root finding. Working with $x \sim 1$ rather than $x \sim 10^{23}$ improves numerical stability:

**Bad**: Finding radius where $\rho(r) = 10^{-7}$ g/cm$^3$ with $r$ in cm
**Good**: Define $\tilde{r} = r/R_{\odot}$, $\tilde{\rho} = \rho/\rho_0$ and solve $\tilde{\rho}(\tilde{r}) = 1$

This keeps all numbers near unity, avoiding overflow/underflow and improving conditioning.

---

## Physical Example: Stellar Structure Equilibrium

In stellar interiors, hydrostatic equilibrium requires:
$$\frac{dP}{dr} = -\frac{GM(r)\rho(r)}{r^2}$$

For a polytrope with $P = K\rho^{1+1/n}$, the Lane-Emden equation describes stellar structure:
$$\frac{1}{\xi^2}\frac{d}{d\xi}\left(\xi^2\frac{d\theta}{d\xi}\right) + \theta^n = 0$$

where $\xi$ is dimensionless radius and $\theta$ is related to density.

The stellar surface occurs where $\theta(\xi_1) = 0$—a root-finding problem!

For different polytropic indices:
- $n = 0$ (constant density): $\xi_1 = \pi$ exactly
- $n = 1$ (isothermal core): $\xi_1 = \pi/\sqrt{2}$
- $n = 3$ (Eddington standard model): $\xi_1 \approx 6.897$
- $n = 5$ (minimum mass star): $\xi_1 \to \infty$ (infinite radius!)

Newton's method excels here because we can compute $\theta$ and $d\theta/d\xi$ from the differential equation. The convergence is rapid even for the sensitive $n = 3$ case.

---

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

Note: $f'(E) = 0$ when $e\cos(E) = 1$, which can happen for high eccentricity!

### Initial Guess Strategy

Good initial guesses are crucial:
- For $e < 0.8$: Use $E_0 = M$ (nearly circular)
- For $e \geq 0.8$: Use $E_0 = \pi$ (highly eccentric)

### Convergence Analysis

| Eccentricity | Iterations (typical) | Condition Number | Why |
|--------------|---------------------|------------------|-----|
| 0.0 (circle) | 0 | 1 | E = M exactly |
| 0.1 | 2-3 | ~1.1 | Nearly linear problem |
| 0.5 | 3-4 | ~2 | Moderate nonlinearity |
| 0.9 | 5-7 | ~10 | Strong nonlinearity |
| 0.99 | 10-15 | ~100 | Near-parabolic, poorly conditioned |

:::{tip} Connection to Project 2 (N-body)
In your N-body simulation, you might need Kepler's equation to:
- Convert orbital elements to positions
- Set up initial conditions for binary systems
- Verify conservation of orbital elements
:::

---

## Practical Algorithm for Finding Initial Brackets

To find initial brackets for bisection:

```python
def find_brackets(f, x_min, x_max, n_scan=100):
    """Scan interval for sign changes"""
    dx = (x_max - x_min) / n_scan
    brackets = []
    
    x_prev = x_min
    f_prev = f(x_prev)
    
    for i in range(1, n_scan + 1):
        x = x_min + i * dx
        fx = f(x)
        
        if f_prev * fx < 0:
            brackets.append([x_prev, x])
        
        x_prev, f_prev = x, fx
    
    return brackets
```

---

## Debugging Root Finding

Common root-finding bugs and their diagnosis:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Bisection won't start | Same sign at endpoints | Scan for sign changes first |
| Newton diverges | Poor initial guess or $f'(x) \approx 0$ | Use bisection first to bracket |
| Secant oscillates | Nearly parallel secant lines | Check $\|f(x_1) - f(x_0)\|$ threshold |
| Wrong root found | Multiple roots in region | Narrow search interval |
| Infinite loop | Tolerance too small | Use relative tolerance: $\epsilon_{rel} \times \|x\|$ |
| No convergence | Discontinuous function | Check function continuity |

---

## Bridge to Part 2: From Finding Zeros to Measuring Areas

You now command three powerful methods for finding where functions equal zero. Each has its place: bisection for reliability, Newton for speed, secant for practicality.

But finding equilibrium points is only half the story. Next, we tackle integration — measuring quantities across space and time. You'll discover how the same principles of approximation and error analysis apply to computing areas under curves, volumes of regions, and integrals over high-dimensional spaces.

The connection runs deep: integration is the inverse of differentiation, and many integration methods rely on root finding. The error analysis skills you've developed here will guide your understanding of quadrature methods.

*Next: Part 2 - Quadrature*