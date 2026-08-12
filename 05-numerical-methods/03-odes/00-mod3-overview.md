---
title: "Overview: Making Time Flow"
subtitle: "ODE Methods & Conservation | Numerical Methods Module 3 | COMP 521"
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

## The Big Picture: Learning Dynamics Through Failure

### A Story That Changes Everything

In 1889, King Oscar II of Sweden offered a prize for solving the n-body problem — predicting the motion of multiple gravitationally interacting bodies forever into the future. Henri Poincaré won by proving something shocking: the problem was *impossible* to solve analytically for n $\geq$ 3. Even worse, he showed that tiny differences in initial conditions led to completely different outcomes. Chaos was born.

But here's what happened next: Instead of giving up, astronomers turned to numerical integration. By 1960, they were using computers to track planetary positions centuries into the future. By 1990, they could simulate the solar system for millions of years. Today, we simulate galaxy collisions over billions of years and track spacecraft to Jupiter with meter precision.

The key insight that made this possible wasn't faster computers or better mathematics — it was discovering that **not all integration methods are created equal**. Some methods that seem accurate destroy the physics they're trying to simulate. Others that seem crude preserve what matters. The difference between a planet spiraling into the sun and orbiting stably for a billion years isn't computational power — it's choosing the right algorithm.

This is the heart of what you're about to learn: **how to make time flow numerically while preserving the fundamental laws of physics**.

### Your Mission: Preserve Physics Through Time

You're about to discover that simulating the universe's evolution is a battle against accumulating errors:

- **Why does Earth's orbit spiral outward with Euler's method?** Energy systematically increases
- **Why do pulsars lose synchronization in simulations?** Phase errors accumulate relentlessly
- **How can we simulate galaxies for cosmic time?** Symplectic integrators preserve geometry
- **When do numerical methods explode?** Stability analysis predicts catastrophic failure

But here's the revelation: **geometric structure matters more than local accuracy**. A second-order method that preserves phase space beats a tenth-order method that violates conservation laws. Master this principle, and you can simulate anything from binary pulsars to galaxy mergers.

### Why This Matters Now More Than Ever

Modern astrophysics runs on temporal evolution:

- **LIGO detections** require integrating Einstein's equations to generate waveform templates
- **Gaia's billion-star catalog** needs orbit integration to detect perturbations from dark matter
- **JWST observations** of early galaxies require N-body simulations for comparison
- **Exoplanet discoveries** depend on integrating orbital dynamics with extreme precision
- **Dark energy constraints** come from simulating structure formation over cosmic time

**You NEED these methods** to do modern astrophysics. This module ensures you understand not just how to call `scipy.integrate.odeint`, but *why* symplectic integrators keep planets stable, *when* implicit methods become essential, and *how* to diagnose numerical disasters before they happen.

## Quick Navigation Guide

### 🎯 Choose Your Learning Path

::::{grid} 1 1 2 3

:::{grid-item}
### 🏃 Fast Track {.unnumbered}
Essential concepts only

- [Euler's failure](01-module3-part1-euler.qmd#eulers-method)
- [RK4 basics](02-module3-part2-runge-kutta.qmd#rk4-classical)
- [Leapfrog method](03-module3-part3-symplectic.qmd#leapfrog-verlet)
- [Stability regions](04-module3-part4-stability.qmd#stability-regions)
:::

:::{grid-item}
### 🚶 Standard Path {.unnumbered}
Full conceptual understanding

Everything in Fast Track, plus:

- [Energy drift analysis](01-module3-part1-euler.qmd#energy-drift)
- [RK derivations](02-module3-part2-runge-kutta.qmd#mathematical-formulation)
- [Symplectic proof](03-module3-part3-symplectic.qmd#proof-symplecticity)
- [Stiff equations](04-module3-part4-stability.qmd#stiff-equations)
- All "Check Your Understanding" boxes
:::

:::{grid-item}
### 🧗 Complete Path {.unnumbered}
Deep dive with all details

Complete module including:

- All mathematical derivations
- [Modified Hamiltonian](03-module3-part3-symplectic.qmd#modified-hamiltonian)
- [Adaptive timesteps](02-module3-part2-runge-kutta.qmd#adaptive-timestep)
- [Implicit methods](04-module3-part4-stability.qmd#implicit-methods)
- Higher-order symplectic
- All worked examples
:::

::::

### 🎯 Navigation by Project Needs

:::{tip} Quick Jump to What You Need by Project
:class: dropdown

**For Project 2 (N-body Dynamics)**:
- [Leapfrog implementation](03-module3-part3-symplectic.qmd#the-algorithm) - Your main integrator
- [Energy monitoring](01-module3-part1-euler.qmd#energy-drift-catastrophe) - Conservation checks
- [Timestep selection](01-module3-part1-euler.qmd#dimensional-analysis) - Setting h appropriately
- [Close encounters](03-module3-part3-symplectic.qmd#implementation-tips) - Handling singularities
- [Phase space structure](03-module3-part3-symplectic.qmd#phase-space-perspective) - Understanding orbits

**For Project 3 (Monte Carlo Radiative Transfer)**:
- [Ray integration](02-module3-part2-runge-kutta.qmd#rk4-classical) - Path through varying media
- [Adaptive methods](02-module3-part2-runge-kutta.qmd#adaptive-timestep) - Efficiency in varying opacity
- [Stability for stiff cooling](04-module3-part4-stability.qmd#stiff-equations) - Radiative processes

**For Project 4 (MCMC)**:
- [Hamiltonian Monte Carlo](03-module3-part3-symplectic.qmd#hamiltonian-mechanics) - Symplectic integration
- [Detailed balance](03-module3-part3-symplectic.qmd#time-reversibility) - Preserving equilibrium
- [Trajectory length](04-module3-part4-stability.qmd#stability-regions) - Choosing integration time

**For Project 5 (Gaussian Processes)**:
- [SDE integration](04-module3-part4-stability.qmd#implicit-methods) - Stochastic differential equations
- [Kernel evolution](02-module3-part2-runge-kutta.qmd#general-framework) - Time-dependent covariance
- [Stability analysis](04-module3-part4-stability.qmd#linear-stability) - Numerical convergence

**For Final Project (Neural Networks)**:
- [Gradient descent as ODE](01-module3-part1-euler.qmd#from-continuous-discrete) - Training dynamics
- [Learning rate as timestep](02-module3-part2-runge-kutta.qmd#adaptive-timestep) - Adaptive optimization
- [Momentum methods](03-module3-part3-symplectic.qmd#hamiltonian-mechanics) - Accelerated convergence
- [Stability of SGD](04-module3-part4-stability.qmd#stability-functions) - When training diverges
:::

:::{note} 💭 Why This Module Exists: A Personal Note from Your Instructor
:class: dropdown

**This module has a secret mission**: teaching you that numerical integration isn't about memorizing Runge-Kutta coefficients — it's about understanding the deep conflict between discrete computation and continuous physics.

I've watched too many students implement RK4 perfectly, then wonder why their solar system flies apart after a million years. They increase the order to RK8, use smaller timesteps, switch to adaptive methods — nothing works. The planets still spiral into the sun or escape to infinity.

**What makes this different**: We start with failure. You'll watch Euler's method destroy a simple harmonic oscillator, see energy grow exponentially when it should be constant. This isn't a bug — it's a fundamental property of the discretization. Then you'll discover that symplectic methods, which look almost identical to Euler, preserve energy for billions of years.

**The revelation students have**:
- *Wait, higher accuracy makes things WORSE for long-term integration?* **Sometimes!**
- *A second-order method beats fourth-order for orbits?* **If it's symplectic!**
- *The same equations that govern planets also train neural networks?* **Exactly!**

This module makes those connections explicit from the start.

**Here's what ODE integration actually is**: creating alternate realities with slightly different physics. Euler creates a universe where energy spontaneously appears. RK4 creates one where energy slowly leaks away. Leapfrog creates one where energy oscillates but stays bounded. Your job is choosing which alternate reality best preserves the physics you care about.

By the end, you'll understand not just the formulas but the deep principles: why geometric structure beats local accuracy, when stability matters more than precision, and how the same mathematical framework spans from planetary dynamics to machine learning. These aren't separate topics — they're all facets of making time flow while preserving what matters.
:::

## Mathematical Foundations

:::{important} 📖 Core Notation and Concepts
Before diving in, let's establish the mathematical language for temporal evolution:

### ODE Notation

| Symbol | Meaning | Physical Example |
|--------|---------|-----------------|
| $\frac{dx}{dt} = f(x,t)$ | General ODE | Equation of motion |
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
- Bounded energy error
- Time reversibility

**Why This Matters**: Every simulation creates a discrete approximation to continuous physics. Understanding these approximations — their errors, stability, and structure preservation — determines whether your simulations reveal truth or nonsense.
:::

## Module Contents

### [Part 1: The Failure of Naive Integration](01-module3-part1-euler.qmd)

Witness Euler's method catastrophically violate energy conservation. Understand why local accuracy doesn't guarantee global stability. See how systematic geometric errors compound until physics is destroyed. Learn to recognize failure modes before they corrupt your simulations.

### [Part 2: Building Better Methods - Runge-Kutta](02-module3-part2-runge-kutta.qmd)

Construct the Runge-Kutta family from Taylor series. Connect RK weights to quadrature rules from Module 2. Implement adaptive timestep control. Discover why even fourth-order accuracy can't preserve energy over cosmic timescales.

### [Part 3: Symplectic Integration - Geometry Over Accuracy](03-module3-part3-symplectic.qmd)

Learn why preserving phase space structure matters more than minimizing error. Prove leapfrog's symplecticity. Understand modified Hamiltonians and bounded energy error. Master the art of choosing between accuracy and conservation.

### [Part 4: Stability Analysis](04-module3-part4-stability.qmd)

Analyze when and why numerical methods explode. Diagnose stiff equations that force tiny timesteps. Understand stability regions in the complex plane. Learn when implicit methods become essential despite their computational cost.

---

*Ready to begin? Let's start with Part 1 and watch Euler's method destroy the physics it's trying to simulate — then learn how to do better!*
