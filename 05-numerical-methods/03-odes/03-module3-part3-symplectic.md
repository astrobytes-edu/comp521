---
title: "Part 3: Symplectic Integration - Geometry Over Accuracy"
subtitle: "Module 3: ODE Methods & Conservation | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is being revised for COMP 521
This chapter was adapted from COMP 536 and is still under review. You may find
references to the wrong course number, setup instructions that do not match
ours, or examples that assume material we have not covered yet.

The Python and the science are sound — it is the packaging that is catching up.
Where this page disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
:::
<!-- prep-banner:end -->

## Learning Objectives

By the end of this section, you will be able to:

- **Explain** Hamiltonian mechanics and phase space structure
- **Prove** symplecticity of leapfrog/Verlet methods
- **Understand** modified Hamiltonians and bounded energy error
- **Implement** symplectic integrators for conservative systems
- **Choose** between accuracy and structure preservation

---

## The Fundamental Insight

:::{margin}
**Symplectic integrator**: A numerical method that preserves the symplectic structure (phase space volume and geometric properties) of Hamiltonian systems.
:::

Instead of minimizing local truncation error, **symplectic integrators** preserve geometric properties:

1. **Phase space volume** (Liouville's theorem)
2. **Time reversibility**
3. **Bounded energy error** (oscillates but doesn't grow)
4. **Poincaré invariants** (action integrals)

The profound trade-off: symplectic methods may be less accurate locally but maintain qualitative correctness globally.

## Hamiltonian Mechanics Refresher

:::{margin}
**Hamiltonian**: A function $H(q,p,t)$ that represents the total energy of a system, where $q$ are generalized coordinates and $p$ are conjugate momenta.
:::

Before diving into symplectic integration, let's recall the **Hamiltonian** formulation of mechanics. For a system with positions $q$ and momenta $p$, the Hamiltonian $H(q,p,t)$ represents total energy:

$$H(q,p) = T(p) + V(q)$$

where $T(p)$ is kinetic energy and $V(q)$ is potential energy.

For a particle of mass $m$ in potential $V(q)$:
$$H = \frac{p^2}{2m} + V(q)$$

Hamilton's equations govern the evolution:

$$\boxed{\frac{dq}{dt} = \frac{\partial H}{\partial p}, \quad \frac{dp}{dt} = -\frac{\partial H}{\partial q}}$$

These equations have remarkable properties:
- **Energy conservation**: $\frac{dH}{dt} = 0$ for time-independent $H$
- **Phase space volume preservation**: Liouville's theorem
- **Symplectic structure**: The flow preserves a geometric structure

## The Phase Space Perspective

:::{margin}
**Phase space**: The space of all possible states of a system, with position and momentum (or velocity) as coordinates.
:::

In **phase space**, each point $(q,p)$ represents a complete state of the system. Trajectories follow contours of constant energy $H = E$.

![Phase space structure of Hamiltonian systems. (Left) Harmonic oscillator: closed orbits on energy surfaces. (Middle) Pendulum: separatrix divides oscillation from rotation. (Right) Liouville's theorem: phase space volume is preserved under Hamiltonian flow—areas deform but don't change size. This geometric structure is what symplectic integrators preserve, ensuring long-term stability.](figures/3_5_phase_space_structure.png){#fig-3-5-phase-space-structure width="800px"}

### Liouville's Theorem

:::{margin}
**Liouville's theorem**: The phase space volume occupied by an ensemble of states is preserved under Hamiltonian evolution.
:::

**Liouville's theorem** states that phase space volume is preserved under Hamiltonian flow. Mathematically, for a volume element $dV = dq\,dp$:

$$\frac{d(dV)}{dt} = 0$$

This is equivalent to saying the flow is incompressible. Standard numerical methods violate this theorem! They artificially compress or expand phase space, leading to systematic errors.

## The Leapfrog/Verlet Method

The leapfrog method (also called Verlet or Störmer-Verlet) staggers position and velocity updates to preserve symplectic structure.

### The Algorithm

For a Hamiltonian $H(q,p) = T(p) + V(q)$ where $T(p) = p^2/(2m)$:

$$\boxed{
\begin{align}
\text{Algorithm: Leapfrog Integration} \\
\hline
&\text{Input: } q_n, p_n, h, \text{force function } F(q) = -\nabla V(q) \\
&\text{Step 1 (kick):} \quad p_{n+1/2} = p_n + \frac{h}{2}F(q_n) \\
&\text{Step 2 (drift):} \quad q_{n+1} = q_n + \frac{h}{m}p_{n+1/2} \\
&\text{Step 3 (kick):} \quad p_{n+1} = p_{n+1/2} + \frac{h}{2}F(q_{n+1}) \\
&\text{Output: } q_{n+1}, p_{n+1}
\end{align}
}$$

### Why "Leapfrog"?

Positions and momenta "leapfrog" over each other in time:

```
Time:     t₀    t₁/₂    t₁    t₃/₂    t₂
          |      |      |      |      |
Position: q₀            q₁            q₂
Momentum:       p₁/₂          p₃/₂
```

This staggering is key to symplecticity!

### Implementation Tips for Your N-body Project

:::{tip} N-body Implementation Advice
For your Project 2 N-body simulation:

1. **Avoid the diagonal bug**: When computing pairwise forces, set diagonal distances to infinity, not 1!
2. **Use half-timestep trick**: Store velocities at half-timesteps for leapfrog
3. **Vectorize force calculation**: Compute all pairwise forces simultaneously
4. **Monitor energy**: Check $|E(t) - E(0)|/|E(0)| < 10^{-10}$ for stability
5. **Start simple**: Test with 2-body system before scaling up
:::

## Proof of Symplecticity

:::{margin}
**Symplectic condition**: A transformation preserves phase space structure if its Jacobian $J$ satisfies $J^T \Omega J = \Omega$ where $\Omega = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$.
:::

A transformation is symplectic if it preserves the symplectic 2-form. We'll prove leapfrog is symplectic by showing each sub-step preserves the symplectic structure.

### Step 1: Analyze Each Sub-step

The leapfrog map can be decomposed into three **shear transformations**:

1. **First kick**: $(q,p) \mapsto (q, p + \frac{h}{2}F(q))$
2. **Drift**: $(q,p) \mapsto (q + \frac{h}{m}p, p)$
3. **Second kick**: $(q,p) \mapsto (q, p + \frac{h}{2}F(q))$

### Step 2: Show Each Shear is Symplectic

For the momentum kick $(q,p) \mapsto (q, p - \frac{h}{2}\nabla V(q))$:

The Jacobian is:
$$J_{\text{kick}} = \begin{pmatrix} I & 0 \\ -\frac{h}{2}\nabla^2 V & I \end{pmatrix}$$

Verify the symplectic condition:
$$J^T \Omega J = \begin{pmatrix} I & -\frac{h}{2}(\nabla^2 V)^T \\ 0 & I \end{pmatrix} \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix} \begin{pmatrix} I & 0 \\ -\frac{h}{2}\nabla^2 V & I \end{pmatrix}$$

$$= \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix} = \Omega \quad \checkmark$$

Similarly for the drift step.

### Step 3: Composition Preserves Symplecticity

Since the composition of symplectic maps is symplectic:
$$J_{\text{total}} = J_{\text{kick}} \cdot J_{\text{drift}} \cdot J_{\text{kick}}$$

is symplectic. Therefore, leapfrog preserves phase space structure exactly!

### Volume Preservation

The determinant of each Jacobian is 1:
$$\det(J) = 1$$

Phase space volume is exactly preserved, satisfying Liouville's theorem.

## The Modified Hamiltonian

:::{margin}
**Modified Hamiltonian**: The exactly conserved quantity for a symplectic integrator, differing from the original Hamiltonian by small bounded terms.
:::

Leapfrog doesn't conserve the original Hamiltonian $H$ exactly. Instead, it exactly conserves a **modified Hamiltonian**:

$$\tilde{H} = H + h^2 H_2 + h^4 H_4 + \ldots$$

The correction terms can be computed using backward error analysis. For the harmonic oscillator with $H = \frac{1}{2}(p^2 + \omega^2 q^2)$:

$$H_2 = \frac{\omega^2}{24}\{H, \{H, H\}\}$$

where $\{f,g\} = \frac{\partial f}{\partial q}\frac{\partial g}{\partial p} - \frac{\partial f}{\partial p}\frac{\partial g}{\partial q}$ is the Poisson bracket.

The key insight: $\tilde{H} - H = O(h^2)$ is bounded! Energy oscillates within a band but never drifts away.

![Energy behavior comparison. (Top) RK4 exhibits monotonic energy drift while Leapfrog energy oscillates within bounded envelope. (Bottom) Phase space trajectories: RK4 spirals outward, Leapfrog remains on a nearby invariant torus of the modified Hamiltonian. This demonstrates the fundamental advantage of symplectic methods—trading local accuracy for global stability.](figures/3_6_modified_hamiltonian.png){#fig-3-6-modified-hamiltonian width="800px"}

## Higher-Order Symplectic Methods

### Yoshida's Fourth-Order Method

By composing leapfrog steps with carefully chosen timesteps, we can achieve higher-order accuracy while maintaining symplecticity. The coefficients come from solving order conditions to eliminate $O(h^3)$ errors.

The strange values involving $2^{1/3}$ arise from the algebraic constraints of maintaining symplecticity while achieving fourth-order accuracy:

$$w_0 = -\frac{2^{1/3}}{2 - 2^{1/3}}, \quad w_1 = \frac{1}{2 - 2^{1/3}}$$

The algorithm combines leapfrog steps with timesteps $c_i h$ where:
$$c_1 = c_4 = w_1/2, \quad c_2 = c_3 = (w_0 + w_1)/2$$

### Forest-Ruth Method

An alternative fourth-order symplectic integrator with different stability properties. The choice between methods depends on the specific problem's characteristics.

## Performance Comparison: 1000-Year Integration

Testing on Earth's orbit (eccentricity $e = 0.017$, period = 365.25 days):

| Method | Order | Energy Error | Phase Error | Stable? |
|--------|-------|--------------|-------------|---------|
| Euler | 1 | +100% | 100 radians | No |
| RK2 | 2 | +10% | 10 radians | No |
| RK4 | 4 | +0.1% | 0.1 radians | No |
| Leapfrog | 2 | ±0.01% (bounded) | 0.01 radians | Yes |
| Yoshida4 | 4 | ±0.0001% (bounded) | 0.0001 radians | Yes |

Leapfrog with only second-order accuracy outperforms fourth-order RK4 for long-term stability!

## When to Use Symplectic Methods

| Problem Type | Requirement | Best Method | Reason |
|--------------|------------|-------------|---------|
| Solar system (Gyr) | Long-term stability | Symplectic | Bounded energy error |
| Satellite (days) | Trajectory accuracy | RK45 adaptive | Short duration |
| Galaxy merger | Phase space structure | Symplectic | Preserve invariants |
| Molecular dynamics | Energy conservation | Symplectic | $10^{15}$ timesteps |
| Dissipative system | Include friction | RK4 | No Hamiltonian structure |

## Simple Example: Pendulum Dynamics

Let's see symplectic integration in action with a nonlinear pendulum:

```python
import numpy as np

def pendulum_leapfrog(theta0, omega0, g, L, h, n_steps):
    """
    Integrate pendulum with leapfrog
    Preserves energy for nonlinear oscillations
    """
    theta, omega = theta0, omega0
    energies = []
    
    for _ in range(n_steps):
        # Initial energy
        E = 0.5*L**2*omega**2 - g*L*np.cos(theta)
        energies.append(E)
        
        # Leapfrog update
        omega_half = omega - 0.5*h*(g/L)*np.sin(theta)
        theta_new = theta + h*omega_half
        omega_new = omega_half - 0.5*h*(g/L)*np.sin(theta_new)
        
        theta, omega = theta_new, omega_new
    
    return energies
```

The energy remains bounded even for large amplitude oscillations where linearization fails!

:::{tip} Physical Example: Binary Pulsar PSR B1913+16
This system has been observed for 40+ years with microsecond timing precision:

- Orbital period: 7.75 hours
- Number of orbits over 40 years: ~45,000
- Required phase accuracy: ~0.001 radians per orbit
- Energy conservation needed: better than 1 part in $10^{10}$

Only symplectic integrators maintain this precision. The Nobel Prize-winning detection of gravitational wave energy loss required comparing observations with symplectic integration predictions!
:::

:::{warning} Common Mistakes with Symplectic Methods
1. **Using adaptive timesteps** - This destroys symplecticity!
2. **Mixing with dissipation** - Friction breaks Hamiltonian structure
3. **Applying to non-conservative forces** - Only works for gradient systems
4. **Expecting local accuracy** - They preserve geometry, not trajectories
5. **Wrong force evaluation** - Must use forces at correct time levels
:::

:::{note} Check Your Understanding
1. Why does leapfrog conserve phase space volume but not exact energy?
2. What's the trade-off between RK4 and leapfrog for 100-year integrations?
3. Why are symplectic methods time-reversible?
4. How does the modified Hamiltonian differ from the original?
5. Can we make leapfrog adaptive while preserving symplecticity?
6. Why do the Yoshida coefficients involve $2^{1/3}$?
:::

---

## Bridge to Part 4: Stability Analysis

You've seen the profound difference between local accuracy and geometric preservation. Symplectic methods sacrifice pointwise precision for global stability, keeping simulations physically meaningful over cosmic timescales.

But choosing the right integrator is only part of the challenge. We also need to understand when methods become unstable, how to diagnose problems, and what limits our timestep choices. In Part 4, we'll analyze stability regions to predict when methods explode and understand the special challenges of stiff equations.

*Next: Part 4 - Stability Analysis*