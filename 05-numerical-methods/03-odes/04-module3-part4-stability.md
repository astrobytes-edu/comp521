---
title: "Part 4: Stability Analysis"
subtitle: "Module 3: ODE Methods & Conservation | COMP 521"
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

- [ ] **Analyze** stability regions for different integration methods
- [ ] **Diagnose** and handle stiff equations
- [ ] **Predict** when numerical methods will become unstable
- [ ] **Choose** appropriate methods based on stability requirements
- [ ] **Implement** implicit methods for challenging problems

---

(linear-stability)=
## Linear Stability Theory

To understand when methods fail catastrophically, we analyze their behavior on the test equation:

$$\frac{dy}{dt} = \lambda y$$

where $\lambda \in \mathbb{C}$. The true solution is $y(t) = y_0 e^{\lambda t}$.

:::{div}
:class: reading-definition
**Stability function**: The amplification factor $R(z)$ relating consecutive numerical solution values: $y_{n+1} = R(h\lambda)y_n$.
:::

When we apply a numerical method, we get:

$$y_{n+1} = R(h\lambda) y_n$$

where $R(z)$ is the **stability function** with $z = h\lambda$.

:::{div}
:class: reading-definition
**Stability region**: The set of complex values $z = h\lambda$ for which $|R(z)| \leq 1$, ensuring bounded solutions.
:::

For bounded solutions, we need $|R(h\lambda)| \leq 1$. The **stability region** is the set of $z$ values where this holds.

(stability-functions)=
## Stability Functions for Common Methods

Let's derive the stability functions for our methods:

### Euler's Method

Applying Euler to $y' = \lambda y$:
$$y_{n+1} = y_n + h\lambda y_n = (1 + h\lambda)y_n$$

Therefore: $\boxed{R(z) = 1 + z}$

This is stable when $|1 + z| \leq 1$, which defines a circle of radius 1 centered at $z = -1$.

### RK2 (Midpoint)

Following through the RK2 steps:
$$k_1 = \lambda y_n$$
$$k_2 = \lambda(y_n + \frac{h}{2}k_1) = \lambda y_n(1 + \frac{z}{2})$$
$$y_{n+1} = y_n + hk_2 = y_n(1 + z + \frac{z^2}{2})$$

Therefore: $\boxed{R(z) = 1 + z + \frac{z^2}{2}}$

### RK4

Through similar analysis (but more algebra):
$$\boxed{R(z) = 1 + z + \frac{z^2}{2} + \frac{z^3}{6} + \frac{z^4}{24}}$$

For this linear test equation, it is exactly the degree-four Taylor polynomial of $e^z$. That does not make the general state-dependent RK4 update a scalar exponential polynomial.

:::{figure} figures/stability-regions.png
:alt: Shaded stability regions show forward Euler's disk, RK4's bounded region, and backward Euler's exterior region including the left half-plane.

Shading marks $|R(z)|\le1$ for the scalar test equation. Forward Euler's
region touches the imaginary axis only at zero. Backward Euler covers the
left half-plane but can still introduce substantial artificial damping.

[Open full-size figure](figures/stability-regions.png)
:::


## Physical Interpretation

For different types of problems, we need different stability characteristics:

### Oscillatory Systems (Circular Orbits)

For a harmonic oscillator with frequency $\omega$:

- Eigenvalues: $\lambda = \pm i\omega$ (purely imaginary)
- Stability requires the particular points $\pm ih\omega$ to lie in the method's stable set
- **Euler**: Unstable for every $h>0$, since $|1+i\omega h|=\sqrt{1+\omega^2h^2}>1$; it amplifies the oscillator
- **RK4**: Stable on this linear oscillator for $0<h\omega\le\sqrt8$; generally damps inside that interval
- **Leapfrog**: Stable for $h < 2/\omega$ with no damping!

### Dissipative Systems (Damped Motion)

For exponential decay with rate $\gamma$:

- Eigenvalue: $\lambda = -\gamma$ (negative real)
- Stability requires the particular negative-real point $-h\gamma$ in the stability region
- **Euler**: Stable for $h < 2/\gamma$
- **RK4**: Stable for $h < 2.78/\gamma$

(stiff-equations)=
## Stiff Equations - When Stability Dominates

:::{div}
:class: reading-definition
**Stiff equation**: An ODE where stability requirements force much smaller timesteps than accuracy requirements. Named because they arise in stiff mechanical systems.
:::

### What Makes an Equation Stiff?

Widely separated timescales are a common source of **stiffness**, not a necessary definition. After fast transients decay, we may be tracking slow evolution while an explicit method still requires tiny timesteps for stability. The comparison is between the step needed for accuracy on the interval of interest and the step allowed by the chosen method's stability region.

### Understanding Stiffness Through Examples

#### Example 1: Chemical Kinetics

Consider a reaction where species A slowly converts to B, but B rapidly equilibrates:

$$\frac{dA}{dt} = -0.04A$$
$$\frac{dB}{dt} = 0.04A - 10^4 B$$

The eigenvalues are $\lambda_1 = -0.04$ (slow) and $\lambda_2 = -10^4$ (fast).

The fast transient decays as $e^{-10^4t}$; after $t=0.001$ its amplitude is about $4.5\times10^{-5}$ of its initial value. For initial data and error targets that make this remnant negligible, $B$ then follows the slowly decaying $A$. Forward Euler still needs $h<2/10^4=0.0002$ to damp the fast numerical mode, even when the slow evolution could meet the accuracy target with a much larger step.

#### Example 2: Stellar Interior with Radiative Cooling

A thermal model can contain a cooling relaxation timescale much shorter than
the duration of interest. For a stated toy model $T'=A-BT^4$, linearization
about $T_{\rm eq}=(A/B)^{1/4}$ gives

$$\delta T'=-4BT_{\rm eq}^3\delta T,\qquad
\tau_{\rm relax}=\frac{1}{4BT_{\rm eq}^3}.$$

An explicit method may need to resolve this fast relaxation even while the
equilibrium changes slowly. The $T^4$ law here is a pedagogical cooling model,
not a universal prescription for stellar shocks; real cooling depends on
opacity, density, ionization, and radiation transport.

:::{div}
:class: reading-definition
**Non-stiff equation**: An ODE where accuracy requirements determine the timestep, with stability easily satisfied. Most orbital mechanics problems are non-stiff.
:::

### Non-Stiff vs Stiff: The Key Distinction

**Non-stiff problems**, for the chosen method and interval, allow accuracy to set the step without a much stricter stability restriction. Similar eigenvalue magnitudes are not a sufficient definition; even the scalar equation $y'=-1000y$ can be stiff over a long interval after its transient decays. Examples:

- Planetary orbits (all periods within a few orders of magnitude)
- Pendulum oscillations
- Wave propagation in uniform media

Widely separated decay rates are one common source of **stiffness**. The timestep can be forced by stability of the fastest mode even after it has decayed; a scalar fast-decay problem can also be stiff over a long interval. Examples:

- Chemical reaction networks
- Radiative transfer with cooling
- Electrical circuits with multiple timescales

(implicit-methods)=
## Implicit Methods for Stiff Problems

:::{div}
:class: reading-definition
**Implicit method**: A numerical scheme where the unknown appears on both sides of the equation, requiring solution of an algebraic system at each step.
:::

**Implicit methods** evaluate the derivative at the future point, giving superior stability at the cost of solving equations.

### Backward Euler

Instead of $y_{n+1} = y_n + hf(y_n, t_n)$, we use:

$$\boxed{y_{n+1} = y_n + hf(y_{n+1}, t_{n+1})}$$

This is implicit because $y_{n+1}$ appears on both sides!

#### Stability Analysis

For the test equation $y' = \lambda y$:
$$y_{n+1} = y_n + h\lambda y_{n+1}$$
$$y_{n+1}(1 - h\lambda) = y_n$$
$$y_{n+1} = \frac{y_n}{1 - h\lambda}$$

Stability function: $\boxed{R(z) = \frac{1}{1-z}}$

This is stable for the **entire left half-plane**! We call this A-stable.

**A limiting check:** for $y'=-1000y$ with $h=0.01$, forward Euler's
factor is $-9$, while backward Euler's is $1/11$. The exact factor is
$e^{-10}$. The implicit result is bounded and decays, but one step still
does not resolve the actual fast transient accurately.

### Solving the Implicit Equation

The challenge: we must solve $y_{n+1} = y_n + hf(y_{n+1}, t_{n+1})$ for $y_{n+1}$.

For nonlinear $f$, this requires iteration. Newton's method is typical:

```python
import numpy as np

def backward_euler_step(y, t, h, f, df_dy, tol=1e-10):
    """
    Single backward Euler step
    Requires a one-dimensional state array and its square Jacobian df/dy.
    tol bounds the algebraic residual norm, not the time-integration error.
    """
    y = np.asarray(y, dtype=float)
    y_new = y.copy()  # Initial guess
    
    for _ in range(10):  # Newton iterations
        # Residual: R(y_new) = y_new - y - h*f(y_new, t+h)
        residual = y_new - y - h*f(y_new, t + h)
        
        if np.linalg.norm(residual) < tol:
            return y_new
        
        # Jacobian of residual
        J = np.eye(len(y)) - h*df_dy(y_new, t + h)
        
        # Newton update
        delta = np.linalg.solve(J, -residual)
        y_new = y_new + delta
    
    raise RuntimeError("Newton iteration failed to converge")
```

### Implicit Midpoint Rule

A second-order implicit method:

$$y_{n+1} = y_n + hf\left(\frac{y_n + y_{n+1}}{2}, t_n + \frac{h}{2}\right)$$

Implicit midpoint is A-stable and symplectic for canonical Hamiltonian systems when the implicit solve is exact. It is not L-stable: its amplification tends to -1 for very stiff decay, so it can retain alternating unresolved transients. A-stability does not guarantee good damping or accuracy, and a loose nonlinear solve can spoil the structure.

## The CFL Condition

:::{div}
:class: reading-definition
**CFL condition**: Courant-Friedrichs-Lewy condition - the numerical domain of dependence must contain the physical one; its numerical coefficient depends on the scheme. Named after the mathematicians who discovered it in 1928.
:::

The **CFL condition** is a necessary stability criterion for hyperbolic PDEs that also applies to ODEs from spatial discretization:

$$h \leq C_{\rm CFL}\frac{\Delta x}{c_{max}}$$

where $\Delta x$ is the spatial grid spacing, $c_{max}$ is the maximum wave speed, and $C_{\rm CFL}$ depends on the spatial and temporal discretizations and dimension. A CFL bound alone is not a sufficient stability proof.

For the wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$ discretized in space:

- Centered second differences in one dimension give frequencies up to $2c/\Delta x$.
- Coupling that semidiscretization to leapfrog gives $ch/\Delta x<1$ away from the boundary; coupling it to forward Euler remains unstable on the imaginary axis.

This means finer spatial grids require smaller timesteps!

## Diagnosing Integration Problems

### Systematic Debugging Approach

When your integration fails, follow this diagnostic sequence:

1. **Check for NaN/Inf**: Could indicate instability, an invalid function domain, division by zero, or overflow
2. **Plot the solution**: Look for oscillations growing exponentially
3. **Compute eigenvalues**: Estimate $\lambda_{max}$
4. **Check stability region**: Do all relevant complex values $h\lambda_j$ lie inside it? For non-normal systems, eigenvalues alone can miss transient amplification.
5. **Test with smaller h**: Does halving h fix the problem?
6. **Monitor energy**: For conservative systems, is energy bounded?

### Stability Test Code

```python
import numpy as np

def stability_test(method, lambda_val, h_values):
    """Flag non-finite or large finite-run outputs; not a stability proof."""
    results = []
    
    for h in h_values:
        y = 1.0  # Initial condition
        stable = True
        
        for n in range(1000):
            y = method(y, lambda_val, h)
            
            if not np.isfinite(y) or abs(y) > 1e10:  # Failure of this finite-run check
                stable = False
                break
        
        results.append((h, stable, abs(y)))
    
    return results
```

A `True` flag means only that this run stayed finite and below the stated
threshold for 1000 steps. Slow growth can pass that check. Use the analytical
$|R(h\lambda)|$ condition for this test equation and report the finite-run
diagnostic separately. A `nan` result is always a failure of this check.

:::{warning} Common Mistakes in Stability Analysis
1. **Ignoring complex eigenvalues** - Oscillatory systems have imaginary parts!
2. **Using wrong stability limit** - Each method has different limits
3. **Checking only eigenvalue magnitude** - Direction in the complex plane matters as well
4. **Confusing local and global stability** - Local stability doesn't guarantee global behavior
5. **Forgetting about stiffness** - Accuracy and stability have different requirements
:::

:::{note} Check Your Understanding
1. Why is the imaginary axis important for orbital problems?
2. What makes an equation "stiff" from a stability perspective?
3. Why don't we always use implicit methods if they're so stable?
4. How does the CFL condition relate to stability regions?
5. What's the trade-off between explicit and implicit methods?
6. Can a method be too stable? (Hint: think about damping)
:::

:::{tip} Answers and reasoning
:class: dropdown

1. Oscillatory linear modes have eigenvalues $\pm i\omega$; their amplification is tested at $\pm ih\omega$, not on the negative real axis.
2. Stiffness means stability forces steps much shorter than accuracy needs over the interval of interest, often after a fast transient has decayed.
3. Implicit steps require algebraic solves and do not remove accuracy requirements. Their damping can also distort oscillations.
4. Spatial discretization produces modes whose eigenvalues depend on grid spacing. The time integrator must stably advance those modes; the CFL coefficient depends on both discretizations.
5. Explicit steps are simpler and often cheaper individually; implicit steps can permit much larger stable advances on stiff problems but require reliable solves.
6. Strong numerical damping can erase an oscillation that the physical system preserves. Backward Euler is stable there but not necessarily accurate; boundedness alone is insufficient.
:::

---

## Bridge to the synthesis: choose and verify a method

Stability identifies restrictions that an error tolerance alone cannot enforce.
The synthesis brings together step size, accuracy, conservation, and cost.
Before optimizing a solver, establish a reference problem and a diagnostic
that would reveal the failure mode you care about. A faster unstable solution
is still an incorrect calculation; a stable result can still have unacceptable
phase or trajectory error.

*Next: Summary and Synthesis*
