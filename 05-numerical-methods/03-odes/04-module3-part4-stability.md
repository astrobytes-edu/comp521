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

## Linear Stability Theory

To understand when methods fail catastrophically, we analyze their behavior on the test equation:

$$\frac{dy}{dt} = \lambda y$$

where $\lambda \in \mathbb{C}$. The true solution is $y(t) = y_0 e^{\lambda t}$.

:::{margin}
**Stability function**: The amplification factor $R(z)$ relating consecutive numerical solution values: $y_{n+1} = R(h\lambda)y_n$.
:::

When we apply a numerical method, we get:

$$y_{n+1} = R(h\lambda) y_n$$

where $R(z)$ is the **stability function** with $z = h\lambda$.

:::{margin}
**Stability region**: The set of complex values $z = h\lambda$ for which $|R(z)| \leq 1$, ensuring bounded solutions.
:::

For bounded solutions, we need $|R(h\lambda)| \leq 1$. The **stability region** is the set of $z$ values where this holds.

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

This matches the Taylor series of $e^z$ through fourth order, but is not exactly $e^z$ truncated!

<!-- Figure: Stability Regions Comparison
Create a complex plane plot showing:
- Euler: small circle centered at (-1,0) with radius 1
- RK2: larger kidney-shaped region
- RK4: even larger region extending to about -2.8 on real axis
- Leapfrog: segment on imaginary axis from -2i to 2i
- Backward Euler: entire left half-plane
Include axes labels, shading for stable regions
Why: Visual comparison of stability regions is essential for method selection
Caption: "Stability regions in the complex z-plane where z = hλ. Shaded regions show where |R(z)| $\leq$ 1. Euler has smallest region, RK4 extends further along negative real axis, Leapfrog covers imaginary axis (oscillatory problems), and implicit methods cover entire left half-plane."
-->

## Physical Interpretation

For different types of problems, we need different stability characteristics:

### Oscillatory Systems (Circular Orbits)

For a harmonic oscillator with frequency $\omega$:

- Eigenvalues: $\lambda = \pm i\omega$ (purely imaginary)
- Stability requires the **imaginary axis** to be in the stability region
- **Euler**: Marginally stable for $h < 2/\omega$, but introduces artificial damping
- **RK4**: Stable for $h < 2.8/\omega$
- **Leapfrog**: Stable for $h < 2/\omega$ with no damping!

### Dissipative Systems (Damped Motion)

For exponential decay with rate $\gamma$:

- Eigenvalue: $\lambda = -\gamma$ (negative real)
- Stability requires the **negative real axis** in the stability region
- **Euler**: Stable for $h < 2/\gamma$
- **RK4**: Stable for $h < 2.78/\gamma$

## Stiff Equations - When Stability Dominates

:::{margin}
**Stiff equation**: An ODE where stability requirements force much smaller timesteps than accuracy requirements. Named because they arise in stiff mechanical systems.
:::

### What Makes an Equation Stiff?

A **stiff equation** contains widely separated timescales. After fast transients die out, we're left tracking slow evolution, but explicit methods still need tiny timesteps for stability.

### Understanding Stiffness Through Examples

#### Example 1: Chemical Kinetics

Consider a reaction where species A slowly converts to B, but B rapidly equilibrates:

$$\frac{dA}{dt} = -0.04A$$
$$\frac{dB}{dt} = 0.04A - 10^4 B$$

The eigenvalues are $\lambda_1 = -0.04$ (slow) and $\lambda_2 = -10^4$ (fast).

After the initial transient ($t > 0.001$), B has equilibrated and we're just tracking the slow decay of A. But explicit methods need $h < 2/10^4 = 0.0002$ for stability, even though nothing interesting happens on this timescale!

#### Example 2: Stellar Interior with Radiative Cooling

In stellar shocks, radiative cooling can create extreme stiffness:

$$\frac{dT}{dt} = \text{heating} - \text{cooling}(T)$$

where cooling $\propto T^4$ for high temperatures. Near equilibrium:

- Heating timescale: years
- Cooling timescale: seconds
- Stiffness ratio: $10^7$!

:::{margin}
**Non-stiff equation**: An ODE where accuracy requirements determine the timestep, with stability easily satisfied. Most orbital mechanics problems are non-stiff.
:::

### Non-Stiff vs Stiff: The Key Distinction

**Non-stiff equations** have eigenvalues with similar magnitudes. The timestep is chosen for accuracy, and stability is automatically satisfied. Examples:

- Planetary orbits (all periods within a few orders of magnitude)
- Pendulum oscillations
- Wave propagation in uniform media

**Stiff equations** have eigenvalues with vastly different magnitudes. The timestep is forced by stability of the fastest mode, even after it has decayed. Examples:

- Chemical reaction networks
- Radiative transfer with cooling
- Electrical circuits with multiple timescales

## Implicit Methods for Stiff Problems

:::{margin}
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

<!-- Figure: Implicit vs Explicit Stability
Create a figure with two panels:
Left: Show stability regions for Forward Euler (small circle) vs Backward Euler (entire left half-plane)
Right: Solution behavior for stiff equation showing Forward Euler explosion vs Backward Euler stability
Include example trajectories for y' = -1000(y-cos(t)) - sin(t)
Why: Dramatically shows advantage of implicit methods for stiff problems
Caption: "Implicit methods transform stability. (Left) Backward Euler is stable for entire left half-plane while Forward Euler has tiny stability region. (Right) For stiff equation y' = -1000(y-cos(t)) - sin(t), Forward Euler explodes while Backward Euler remains stable with large timesteps."
-->

### Solving the Implicit Equation

The challenge: we must solve $y_{n+1} = y_n + hf(y_{n+1}, t_{n+1})$ for $y_{n+1}$.

For nonlinear $f$, this requires iteration. Newton's method is typical:

```python
def backward_euler_step(y, t, h, f, df_dy, tol=1e-10):
    """
    Single backward Euler step
    Requires Jacobian df/dy for Newton iteration
    """
    y_new = y  # Initial guess
    
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

This is A-stable AND symplectic! It preserves geometric structure while handling stiffness.

## The CFL Condition

:::{margin}
**CFL condition**: Courant-Friedrichs-Lewy condition - information cannot propagate more than one grid cell per timestep. Named after the mathematicians who discovered it in 1928.
:::

The **CFL condition** is a necessary stability criterion for hyperbolic PDEs that also applies to ODEs from spatial discretization:

$$h \leq \frac{\Delta x}{c_{max}}$$

where $\Delta x$ is the spatial grid spacing and $c_{max}$ is the maximum wave speed.

For the wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$ discretized in space:

- Eigenvalues: $\lambda \approx \pm ic/\Delta x$
- Stability requires: $h < \Delta x/c$

This means finer spatial grids require smaller timesteps!

## Diagnosing Integration Problems

### Systematic Debugging Approach

When your integration fails, follow this diagnostic sequence:

1. **Check for NaN/Inf**: Immediate indicator of instability
2. **Plot the solution**: Look for oscillations growing exponentially
3. **Compute eigenvalues**: Estimate $\lambda_{max}$
4. **Check stability limit**: Is $h|\lambda_{max}| < \text{stability limit}$?
5. **Test with smaller h**: Does halving h fix the problem?
6. **Monitor energy**: For conservative systems, is energy bounded?

### Stability Test Code

```python
def stability_test(method, lambda_val, h_values):
    """Test stability for different timesteps"""
    results = []
    
    for h in h_values:
        y = 1.0  # Initial condition
        stable = True
        
        for n in range(1000):
            y = method(y, lambda_val, h)
            
            if abs(y) > 1e10:  # Explosion detected
                stable = False
                break
        
        results.append((h, stable, abs(y)))
    
    return results
```

:::{warning} Common Mistakes in Stability Analysis
1. **Ignoring complex eigenvalues** - Oscillatory systems have imaginary parts!
2. **Using wrong stability limit** - Each method has different limits
3. **Not checking all eigenvalues** - The largest magnitude dominates
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

---

## Bridge to Part 5: From Stability to Speed

Understanding stability tells us what timesteps are allowed, but performance determines whether our simulations finish in reasonable time. Even the most stable method is useless if it takes years to run.

In Part 5, we'll explore performance optimization through vectorization. Modern processors can perform multiple operations simultaneously, but only if we structure our code correctly. The difference between naive loops and optimized array operations can be 100$\times$ in execution speed — the difference between waiting hours and waiting weeks for results.

*Next: Part 5 - Performance Optimization*