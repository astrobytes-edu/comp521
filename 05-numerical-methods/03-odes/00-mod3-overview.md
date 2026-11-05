---
title: "Overview: Making Time Flow"
subtitle: "ODE Methods & Conservation | Numerical Methods Module 3 | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is still being revised
This reading is under revision. Use the [ODE lecture overview](../../09-lectures/block-04-odes.md)
for the current lecture and reading sequence. The syllabus and assignment briefs
remain authoritative for dates and requirements.
:::
<!-- prep-banner:end -->

## The Big Picture: Learning Dynamics Through Failure

### A problem we can test before solving an orbit

An isolated harmonic oscillator has an exact solution and constant energy.
That makes it a useful first test for an orbit integrator: if our discrete
update creates energy here, we can identify the mechanism before adding
gravitational encounters or complicated initial conditions.

Start with a position and velocity, advance both along their current
derivatives, and repeat. This is Euler's method. Each step looks reasonable,
yet the phase-space radius grows. A different arrangement of almost the same
force evaluations—leapfrog—has different geometry and different long-time
behavior. We will derive both outcomes rather than infer them from a plot.

The historical difficulty of the many-body problem does not mean every
three-body motion is chaotic or that analytic solutions never exist. The
practical numerical question is narrower: for the equations, initial state,
duration, and observable we chose, what evidence supports the result?

That question leads through the whole module. We compare state error, energy
error, phase error, and computational work because each measures something
different. A trajectory that looks closed may have the wrong period; an energy
that stays bounded may accompany an accumulating phase error.

### Your Mission: Preserve Physics Through Time

Use the exact oscillator to separate several numerical questions:

- **Does forward Euler preserve oscillator energy?** Its discrete update gives an exact energy-growth factor.
- **Does bounded energy imply accurate timing?** Compare phase against the known oscillator frequency.
- **What does a symplectic method preserve?** Derive leapfrog's geometric property and then test its trajectory accuracy.
- **Which steps amplify a stable physical mode?** Compare the update with its stability restriction.

The oscillator is a controlled benchmark. Transfer the diagnostics to a
Kepler orbit or another model, but derive or measure that model's numerical
behavior rather than copying the oscillator's energy-growth law.

The central lesson is that local accuracy, stability, and geometric
preservation answer different questions. None automatically dominates the
others. A second-order symplectic method can be useful for long conservative
integrations; a fourth-order adaptive method can be preferable for a precise
short trajectory. Both choices need an accuracy target and verification.

### Why this matters in computational astrophysics

Orbit propagation, stellar evolution, chemical networks, and radiation
hydrodynamics all involve time evolution. They do not all have the same
conservation laws or timescales. A cooling gas should lose thermal energy; a
conservative oscillator should not. Before selecting a method, state which
equations and diagnostic apply to the system being modeled.

In these readings, the oscillator provides a shared, dimensionless benchmark.
The physical applications explain how to transfer the reasoning, not how to
replace a full scientific model with a toy problem. The goal is to understand
what a solver's accuracy and stability statements actually promise.

## Quick Navigation Guide

### 🎯 Choose Your Learning Path

::::{grid} 1 1 2 3

:::{grid-item}
### 🏃 Fast Track
Essential concepts only

- [Euler's failure](01-module3-part1-euler.md#eulers-method)
- [RK4 basics](02-module3-part2-runge-kutta.md#rk4-classical)
- [Leapfrog method](03-module3-part3-symplectic.md#leapfrog-verlet)
- [Stability regions](04-module3-part4-stability.md#stability-functions)
:::

:::{grid-item}
### 🚶 Standard Path
Full conceptual understanding

Everything in Fast Track, plus:

- [Energy drift analysis](01-module3-part1-euler.md#energy-drift)
- [RK derivations](02-module3-part2-runge-kutta.md#mathematical-formulation)
- [Symplectic proof](03-module3-part3-symplectic.md#proof-symplecticity)
- [Stiff equations](04-module3-part4-stability.md#stiff-equations)
- All "Check Your Understanding" boxes
:::

:::{grid-item}
### 🧗 Complete Path
Deep dive with all details

Complete module including:

- All mathematical derivations
- [Modified Hamiltonian](03-module3-part3-symplectic.md#modified-hamiltonian)
- [Adaptive timesteps](02-module3-part2-runge-kutta.md#adaptive-timestep)
- [Implicit methods](04-module3-part4-stability.md#implicit-methods)
- Higher-order symplectic
- All worked examples
:::

::::

### Navigation by computational question

:::{tip} Find the diagnostic you need
:class: dropdown
- For an energy drift, start with the [Euler derivation](01-module3-part1-euler.md#energy-drift).
- For state accuracy and cost, use the [shared oscillator experiment](02-module3-part2-runge-kutta.md#oscillator-comparison).
- For geometric preservation, read the [leapfrog proof](03-module3-part3-symplectic.md#proof-symplecticity).
- For short and long timescales, read [stiffness](04-module3-part4-stability.md#stiff-equations).
- For choosing a step, compare [stability functions](04-module3-part4-stability.md#stability-functions) with a refinement study.
:::

### A guide to reading the experiments

Before running an example, write down what the exact system should do. For
the oscillator, energy is constant and the phase advances at a known rate.
Then predict which numerical defect should appear and which plot would reveal
it. A trajectory plot is useful, but often hides a small systematic error.

After running, compare at least two resolutions over the same physical time.
Changing both the step and final time makes an error ratio ambiguous. Record
whether the method is in its stable range, whether the predicted leading
order is visible, and whether rounding has become significant.

Finally, ask what the experiment does not establish. Preserving an oscillator
invariant does not validate a gravitational force calculation; passing an
energy test does not prove accurate phase; repeatable output does not prove
the equations match the physical problem. These boundaries are part of the
scientific interpretation, not reasons to avoid numerical experiments.

## Mathematical Foundations

:::{important} 📖 Core Notation and Concepts
Before diving in, let's establish the mathematical language for temporal evolution:

### ODE Notation

| Symbol | Meaning | Physical Example |
|--------|---------|-----------------|
| $\frac{dx}{dt} = f(t,x)$ | General ODE | Equation of motion |
| $x(t_0) = x_0$ | Initial condition | Starting position/velocity |
| $h$ or $\Delta t$ | Timestep | Integration step size |
| $x_{n+1} = \Phi_h(x_n)$ | Discrete map | Numerical integrator |
| $\tau$ | Local truncation error | Per-step error |
| $E$ | Global error | Total accumulated error |

### Hamiltonian Notation

| Symbol | Meaning | Physical Example |
|--------|---------|-----------------|
| $H(q,p)$ | Hamiltonian | Total energy |
| $q$ | Generalized coordinates | Positions |
| $p$ | Conjugate momenta | Momenta |
| $\{f,g\}$ | Poisson bracket | Structure preservation |
| $\omega$ | Symplectic form | Phase space geometry |

### Key Concepts Preview

**Order of accuracy**: How error scales with timestep
- Local: $\tau = O(h^{p+1})$ per step
- Global: $E = O(h^p)$ over interval

**Stability**: When methods remain bounded
- Absolute stability: $|R(h\lambda)| \leq 1$
- A-stability: Stable for entire left half-plane

**Symplecticity**: Preservation of phase space structure
- Volume preservation (Liouville)
- Long-time near-energy conservation under the stated regularity and step conditions
- Time reversibility for symmetric methods such as fixed-step leapfrog

**Why This Matters**: Every simulation creates a discrete approximation to continuous physics. Understanding these approximations — their errors, stability, and structure preservation — determines whether your simulations reveal truth or nonsense.
:::

## Module Contents

### [Part 1: The Failure of Naive Integration](01-module3-part1-euler.md)

Derive Euler’s update, then compare its predicted and measured energy and phase errors on an undamped oscillator. Distinguish this instability from its behavior on a decay problem. Use the equations and the observable to choose the next diagnostic.

### [Part 2: Building Better Methods - Runge-Kutta](02-module3-part2-runge-kutta.md)

Construct the Runge-Kutta family from Taylor series. Connect RK weights to quadrature rules from Module 2. Implement adaptive timestep control. Discover why fourth-order state accuracy does not imply exact energy conservation.

### [Part 3: Symplectic Integration - Geometry Over Accuracy](03-module3-part3-symplectic.md)

Learn what preserving phase-space structure adds to an accuracy calculation. Prove leapfrog's symplecticity. Understand modified Hamiltonians and bounded energy error. Master the art of choosing between accuracy and conservation.

### [Part 4: Stability Analysis](04-module3-part4-stability.md)

Analyze when and why numerical methods explode. Diagnose stiff equations that force tiny timesteps. Understand stability regions in the complex plane. Learn when implicit methods become essential despite their computational cost.

---

*Ready to begin? Let's start with Part 1 and watch Euler's method destroy the physics it's trying to simulate — then learn how to do better!*
