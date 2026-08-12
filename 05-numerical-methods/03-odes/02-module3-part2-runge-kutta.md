---
title: "Part 2: Building Better Methods - Runge-Kutta"
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

- [ ] **Derive** RK2 and RK4 from multivariate Taylor expansions
- [ ] **Connect** RK weights to quadrature rules from Module 2
- [ ] **Implement** adaptive timestep control
- [ ] **Analyze** when higher-order methods help vs harm
- [ ] **Choose** appropriate RK methods based on problem requirements

---

## The Key Insight: Sample Multiple Points

Euler's fatal flaw is assuming the derivative stays constant over the entire timestep. Real functions curve. **Runge-Kutta methods** evaluate the derivative at carefully chosen intermediate points, then combine these samples with specific weights to achieve higher-order accuracy.

This is exactly the same principle as quadrature from Module 2! We're essentially performing numerical integration on:

$$x_{n+1} = x_n + \int_{t_n}^{t_{n+1}} f(x(t), t) dt$$

But now the integrand depends on the unknown solution $x(t)$ itself, requiring us to estimate intermediate values.

## RK2 - The Midpoint Method

### Geometric Intuition

Instead of blindly following the tangent from the starting point, we:

1. Take a half-step using the initial derivative
2. Evaluate the derivative at this midpoint
3. Use this midpoint derivative for the full step

This is analogous to the midpoint rule for integration, which we know from Module 2 is second-order accurate!

(mathematical-formulation)=
### Complete Mathematical Formulation

:::{margin}
**Predictor-corrector method**: A two-stage process where an initial estimate (predictor) is refined using better information (corrector).
:::

The RK2 midpoint method is a **predictor-corrector method**:

**Stage 1 - Predictor:**
$$k_1 = f(x_n, t_n)$$
$$x_{mid} = x_n + \frac{h}{2}k_1$$

**Stage 2 - Corrector:**
$$k_2 = f(x_{mid}, t_n + \frac{h}{2})$$
$$x_{n+1} = x_n + h k_2$$

![RK2 midpoint method: First evaluate derivative at start (k_{1}), use it to estimate midpoint, evaluate derivative there (k_{2}), then use midpoint derivative for full step. This captures solution curvature much better than Euler's single-point sampling, achieving O(h^{2}) global accuracy. The midpoint derivative (green) provides a better approximation to the average slope over the interval than the initial derivative alone.](figures/3_3_rk2_midpoint.webp){#fig-3-3-rk2-midpoint width="800px"}

### Error Analysis via Taylor Series

Using multivariate Taylor expansion, the midpoint derivative becomes:
$$f(x_{mid}, t_{mid}) = f + \frac{h}{2}\left(\frac{\partial f}{\partial t} + f\frac{\partial f}{\partial x}\right) + O(h^2)$$

The RK2 update matches the true solution through $O(h^2)$:

- **Local truncation error**: $O(h^3)$
- **Global error**: $O(h^2)$

RK2 is second-order accurate — halving the timestep reduces error by a factor of 4.

### Implementation

```python
def rk2_step(x, t, h, f):
    """Single RK2 (midpoint) step"""
    k1 = f(x, t)
    
    # Predictor to midpoint
    x_mid = x + 0.5 * h * k1
    t_mid = t + 0.5 * h
    
    # Evaluate at midpoint
    k2 = f(x_mid, t_mid)
    
    # Full step using midpoint derivative
    return x + h * k2
```

(rk4-classical)=
## RK4 - The Classical Workhorse

:::{margin}
**Runge-Kutta 4 (RK4)**: The most popular ODE method, achieving 4th-order accuracy with 4 function evaluations. Discovered independently by Runge (1895) and Kutta (1901).
:::

**RK4** samples the derivative at four carefully chosen points:

**Stage 1:** $k_1 = f(x_n, t_n)$ (derivative at start)

**Stage 2:** $k_2 = f(x_n + \frac{h}{2}k_1, t_n + \frac{h}{2})$ (derivative at midpoint using $k_1$)

**Stage 3:** $k_3 = f(x_n + \frac{h}{2}k_2, t_n + \frac{h}{2})$ (derivative at midpoint using $k_2$)

**Stage 4:** $k_4 = f(x_n + hk_3, t_n + h)$ (derivative at endpoint using $k_3$)

**Final update:**
$$\boxed{x_{n+1} = x_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)}$$

### The Connection to Simpson's Rule

The weights $\frac{1}{6}, \frac{2}{6}, \frac{2}{6}, \frac{1}{6}$ are precisely Simpson's rule weights from Module 2! This is not a coincidence:

- **Euler = Rectangle rule**: Sample at left endpoint only
- **RK2 = Midpoint rule**: Sample at center
- **RK4 = Simpson's rule**: Weighted average with parabolic fit

RK4 is essentially applying Simpson's quadrature to the integral $\int_{t_n}^{t_{n+1}} f(x(t), t) dt$, but with the complication that we must estimate $x(t)$ at intermediate points.

### Error Analysis

Through Taylor series expansion to fourth order:

- **Local truncation error**: $O(h^5)$
- **Global error**: $O(h^4)$

This means halving the timestep reduces error by a factor of 16!

(general-framework)=
## The General Runge-Kutta Framework

:::{margin}
**Butcher tableau**: A compact notation for Runge-Kutta methods invented by John Butcher (1964), organizing the coefficients that define each method.
:::

All explicit RK methods follow this pattern:

$$k_i = f\left(x_n + h\sum_{j=1}^{i-1} a_{ij}k_j, t_n + c_ih\right)$$

$$x_{n+1} = x_n + h\sum_{i=1}^s b_i k_i$$

The coefficients $(a_{ij}, b_i, c_i)$ define the method and are displayed in a **Butcher tableau**:

```markdown
c₁ |
c₂ | a₂₁
c₃ | a₃₁ a₃₂
⋮  | ⋮
cₛ | aₛ₁ aₛ₂ ... aₛ,ₛ₋₁
---|--------------------
   | b₁  b₂  ...  bₛ
```

For RK4:

```markdown
0   |
1/2 | 1/2
1/2 | 0   1/2
1   | 0   0   1
----|----------------
    | 1/6 2/6 2/6 1/6
```

(adaptive-timestep)=
## Adaptive Timestep Control

Real problems have varying timescales. When a planet is far from the sun, we can take large steps. During close encounters, we need tiny steps. Adaptive methods adjust $h$ dynamically.

### The Embedded Runge-Kutta Approach

The idea: compute two different order estimates using the same function evaluations, then use their difference to estimate error.

### Runge-Kutta-Fehlberg Method (RK45)

RK45 computes both 4th and 5th order solutions:

1. Compute six $k_i$ values (shared between both estimates)
2. Combine with 4th-order weights $\to$ $x_{(4)}$
3. Combine with 5th-order weights $\to$ $x_{(5)}$
4. Error estimate: $\epsilon = ||x_{(5)} - x_{(4)}||$
5. Optimal timestep: $h_{new} = h \cdot 0.9 \cdot (\text{tolerance}/\epsilon)^{1/5}$

If error is acceptable, accept the step and continue. Otherwise, reject and retry with smaller $h$.

![Adaptive timestep control for eccentric orbit (e=0.9). Small steps near perihelion where velocity is high, large steps near aphelion where motion is slow. The top panel shows the elliptical orbit with color-coded timestep sizes, while the bottom panel shows how the timestep varies continuously around the orbit. This concentrates computational effort where dynamics are fastest while maintaining constant error throughout.](figures/3_4_adaptive_timestep.webp){#fig-3-4-adaptive-timestep width="800px"}

### When to Use Adaptive Methods

**Good for:**

- Problems with varying timescales
- Unknown dynamics
- Achieving specified accuracy efficiently
- Initial exploration of new systems

**Bad for:**

- Long-term Hamiltonian systems (destroys symplecticity)
- Problems requiring uniform time grid
- Parallel simulations (variable timesteps complicate synchronization)

## Performance Comparison

Let's compare methods on the Kepler problem (elliptical orbit with $e = 0.017$):

| Method | Order | Steps/Orbit | Energy Error After 100 Orbits | CPU Time |
|--------|-------|-------------|-------------------------------|----------|
| Euler | 1 | 1000 | +10% | 1.0$\times$ |
| RK2 | 2 | 100 | +0.1% | 0.2$\times$ |
| RK4 | 4 | 30 | +0.0001% | 0.12$\times$ |
| RK45 | 4/5 | 15-50 | +0.00001% | 0.15$\times$ |

RK4 achieves 100,000$\times$ better accuracy than Euler with 8$\times$ less computation!

## The Dark Side of High-Order Methods

Despite their impressive local accuracy, RK methods have a fatal flaw for long-term integration:

### Energy Drift Comparison

After 10,000 orbits with timestep $h = 0.01 \times t_\text{orbit}$:

- **Euler**: +100% energy drift (orbit doubled!)
- **RK2**: +10% energy drift (significant growth)
- **RK4**: +0.1% energy drift (small but systematic)

Even RK4, accurate to $O(h^4)$ per step, exhibits systematic energy drift! After millions of orbits (typical for solar system simulations), even this tiny drift becomes catastrophic.

### Why RK Methods Drift

The fundamental issue: RK methods don't preserve the geometric structure of phase space. They slightly expand or contract volumes, violating Liouville's theorem. Each step compounds this violation until energy drifts unboundedly.

Higher order reduces the drift rate but doesn't eliminate it. For billion-year simulations, we need qualitatively different methods.

:::{warning} Common Mistakes with RK Methods
1. **Using RK4 for billion-year simulations** - Energy will still drift!
2. **Assuming higher order is always better** - RK8 isn't necessarily more stable than RK4
3. **Using adaptive timesteps carelessly** - Can destroy conservation properties
4. **Not checking the stability region** - RK4 can still go unstable for large h
5. **Implementing RK4 with wrong weights** - The 1,2,2,1 pattern divided by 6 is crucial
:::

:::{note} Check Your Understanding
1. Why does RK2 sample at the midpoint rather than the endpoint?
2. What's the connection between RK4 weights and Simpson's rule?
3. When would adaptive timesteps be essential vs harmful?
4. Why doesn't higher order eliminate energy drift?
5. How many function evaluations does RK4 require per step?
6. Can you explain why RK methods violate Liouville's theorem?
:::

---

## Bridge to Part 3: The Need for Geometric Integration

The Runge-Kutta family achieves impressive local accuracy through careful sampling of derivatives. RK4's fourth-order accuracy seems like it should be sufficient for any problem. Yet for long-term integration of Hamiltonian systems, even this isn't enough.

The issue isn't accuracy — it's structure preservation. RK methods focus on minimizing the local truncation error, but they ignore the geometric properties that make physical systems special. Conservation laws, symmetries, and phase space structure are not preserved.

In Part 3, we'll explore symplectic integrators that sacrifice local accuracy for global stability. These methods preserve the fundamental geometry of phase space, keeping energy bounded even over cosmic timescales. We'll discover that a second-order symplectic method that keeps your solar system stable for a billion years beats a tenth-order method that spirals planets into the sun.

The transition from RK to symplectic methods represents a philosophical shift: from minimizing error to preserving physics.

*Next: Part 3 - Symplectic Integration*