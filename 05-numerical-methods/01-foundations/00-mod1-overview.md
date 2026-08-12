---
title: "Overview: Foundations of Discrete Computing"
subtitle: "Numerical Methods Module 1 | COMP 521"
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

## The Big Picture: When Computers Meet Calculus

### A Story That Changes Everything

In 1922, Lewis Fry Richardson attempted something audacious: predict tomorrow's weather using mathematics. Armed with differential equations that governed atmospheric flow, he organized human "computers" into a calculating factory. Each person computed derivatives and changes for their assigned atmospheric cell. After six weeks of calculations, Richardson proudly announced his prediction: the atmospheric pressure would change by 145 millibars in 6 hours.

Reality delivered a crushing blow: the actual change was 1 millibar. Richardson's prediction was wrong by a factor of 145.

But here's the twist: Richardson's equations were correct. His mathematics was sound. The catastrophic failure came from something more fundamental — he was taking finite differences with steps that were too large, and his human computers were rounding numbers to save time. **The errors in numerical approximation completely overwhelmed the physics.**

Richardson's failure revealed a profound truth that shapes all computational physics: when we move from the continuous mathematics of calculus to the discrete world of computers, we enter a realm where $h \to 0$ is impossible, where $0.1 + 0.2 \neq 0.3$, and where tiny errors can avalanche into disasters.

### Your Mission: Master the Art of Approximation

You're about to discover how to navigate the fundamental paradox of computational physics:

- **Calculus requires** taking limits as $h \to 0$
- **Computers can't** represent infinitesimally small numbers
- **Yet somehow** we can simulate galaxies, track spacecraft to Jupiter, and detect gravitational waves

The resolution of this paradox — understanding exactly what errors we introduce and how to control them — is the foundation of all computational astrophysics.

### Why This Matters Now More Than Ever

Modern astrophysics pushes computational limits like never before:

- **LIGO** detects strains of $10^{-21}$ – requiring numerical methods accurate to 20+ decimal places
- **JWST** data pipelines process millions of pixels where round-off errors could hide exoplanets
- **Cosmological simulations** track $10^{12}$ particles over $10^{10}$ years where errors compound exponentially
- **Neural networks** for galaxy classification compute millions of derivatives via backpropagation

You NEED to understand numerical methods at a fundamental level — not just which buttons to push, but why algorithms succeed or fail.

## Learning Philosophy

This module embodies our "glass-box modeling" approach:

- **Understand every approximation:** Know exactly what errors you're introducing and why
- **Build from fundamentals:** Derive methods from Taylor series and error analysis
- **Connect to physics:** Every numerical choice has physical consequences
- **Embrace limitations:** Finite precision isn't a bug; it's a feature that teaches us about our models

## Module Learning Objectives

By completing this module, you will be able to:

- [ ] **Analyze** the fundamental trade-offs between truncation and round-off error in numerical calculations
- [ ] **Design** numerical algorithms that minimize total error for specific astrophysical problems
- [ ] **Predict** error scaling behavior before implementing code
- [ ] **Diagnose** numerical instabilities and reformulate problems for better conditioning
- [ ] **Choose** appropriate numerical methods based on problem characteristics and accuracy requirements
- [ ] **Implement** robust code that handles edge cases and numerical limitations gracefully

## Quick Navigation Guide

### 🎯 Choose Your Learning Path

::::{grid} 1 1 2 3

:::{grid-item}
### 🏃 Fast Track {.unnumbered}
Essential concepts only

- [The core paradox](01-mod1-part1-finite-differences.md#the-core-problem)
- [Optimal h derivation](01-mod1-part1-finite-differences.md#optimal-h)
- [Machine epsilon](02-mod1-part2-numerical-errors.md#machine-epsilon)
- [Error types](02-mod1-part2-numerical-errors.md#three-types)
:::

:::{grid-item}
### 🚶 Standard Path {.unnumbered}
Full conceptual understanding

Everything in Fast Track, plus:

- [All finite difference methods](01-mod1-part1-finite-differences.md#finite-difference-landscape)
- [Catastrophic cancellation](02-mod1-part2-numerical-errors.md#catastrophic-cancellation)
- [Error measurement](02-mod1-part2-numerical-errors.md#measuring-errors)
- [Taylor series applications](03-mod1-part3-taylor-series.md)
:::

:::{grid-item}
### 🧗 Complete Path {.unnumbered}
Deep dive with all details

Complete module including:

- All mathematical derivations
- Custom method design
- Automatic differentiation
- All worked examples
- Historical context
:::

::::

### 🎯 Navigation by Project Needs

:::{tip} Quick Jump to What You Need by Project
:class: dropdown

**For Project 2 (N-body Dynamics)**:
- [Computing derivatives for forces](01-mod1-part1-finite-differences.md#the-core-problem)
- [Choosing timesteps](01-mod1-part1-finite-differences.md#optimal-h)
- [Error accumulation](02-mod1-part2-numerical-errors.md#propagation-error)
- [Unit scaling](02-mod1-part2-numerical-errors.md#scale-appropriately)

**For Project 3 (Monte Carlo Radiative Transfer)**:
- [Round-off in photon tracking](02-mod1-part2-numerical-errors.md#round-off-error)
- [Catastrophic cancellation in optical depth](02-mod1-part2-numerical-errors.md#catastrophic-cancellation)
- [Error propagation in random walks](02-mod1-part2-numerical-errors.md#propagation-error)

**For Project 4 (MCMC)**:
- [Computing likelihood gradients](01-mod1-part1-finite-differences.md#central-difference)
- [Numerical stability](02-mod1-part2-numerical-errors.md#reformulation)
- [Step size selection](01-mod1-part1-finite-differences.md#practical-algorithm)

**For Final Project (Neural Networks)**:
- [Automatic differentiation intro](03-mod1-part3-taylor-series.md#automatic-differentiation)
- [Gradient computation](01-mod1-part1-finite-differences.md#finite-difference-landscape)
- [Learning rate as h](01-mod1-part1-finite-differences.md#optimal-h)
:::

:::{note} 💭 Why This Module Exists: A Personal Note from Your Instructor
:class: dropdown

This module exists because I've seen too many students treat numerical methods as black boxes — using `scipy.integrate` or `np.gradient` without understanding what's happening inside. This leads to disaster when:

- Your energy conservation mysteriously fails after a million timesteps
- Your code gives different answers on different machines
- Your optimization gets stuck because gradients underflow to zero

**What makes this different**: Instead of memorizing formulas, you'll understand the deep principles. When you see that optimal $h \approx \sqrt{\epsilon}$ for forward differences, you'll know WHY — you'll visualize the U-shaped error curve, understand the competition between truncation and round-off, and be able to derive it yourself.

By the end, you'll have the confidence to design your own numerical methods when standard approaches fail. More importantly, you'll know when and why they fail.

This isn't just about passing a course — these principles will serve you whether you're reducing JWST data, running cosmological simulations, or training neural networks to find gravitational lenses.
:::

## Mathematical Foundations

:::{important} 📖 Core Notation and Concepts
Before diving in, let's establish our mathematical language:

### Notation

| Symbol | Meaning | First Appears |
|--------|---------|---------------|
| $h$ | Step size for finite differences | [Part 1](01-mod1-part1-finite-differences.md#the-core-problem) |
| $\epsilon$ | Machine epsilon ($\approx 2.2 \times 10^{-16}$ for float64) | [Part 2](02-mod1-part2-numerical-errors.md#machine-epsilon) |
| $O(h^p)$ | Error scaling with order $p$ | [Part 1](01-mod1-part1-finite-differences.md#forward-difference) |
| $f^{(n)}$ | $n$-th derivative of $f$ | [Part 3](03-mod1-part3-taylor-series.md) |
| $E_{\text{abs}}$, $E_{\text{rel}}$ | Absolute and relative errors | [Part 2](02-mod1-part2-numerical-errors.md#measuring-errors) |

### Key Concepts Preview

**Finite Difference**: Approximating derivatives using function values at discrete points:
$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$

**Taylor Series**: Expanding functions as power series to understand approximation errors:
$$f(x+h) = f(x) + hf'(x) + \frac{h^2}{2}f''(x) + O(h^3)$$

**The Fundamental Trade-off**: 
- Small $h$ $\to$ Better approximation but round-off errors dominate
- Large $h$ $\to$ Avoids round-off but poor approximation
- Optimal $h$ $\to$ Minimizes total error
:::

## Module Contents

### [Part 1: The Fundamental Paradox - Calculus on Computers](01-mod1-part1-finite-differences.md)
- Why computers cannot take true limits
- Forward, backward, and central differences from first principles
- The optimal step size derivation
- Practical algorithms for choosing $h$

### [Part 2: Numbers Aren't Real - Computer Arithmetic & Cosmic Consequences](02-mod1-part2-numerical-errors.md)
- Finding and understanding machine epsilon
- Three types of numerical error
- Catastrophic cancellation and how to avoid it
- Error propagation in long calculations

### [Part 3: Taylor Series - The Bridge from Continuous to Discrete](03-mod1-part3-taylor-series.md)
- Verifying error predictions empirically
- Designing custom finite difference formulas
- When NOT to use numerical derivatives
- Introduction to automatic differentiation

### [Part 4: Module Synthesis](04-mod1-synthesis.md)
- Consolidating concepts
- Quick reference tables
- Connections across projects
- Looking forward

## Prerequisites Check

:::{note} 🔍 Self-Assessment
Before beginning, verify you can:

- [ ] Take the derivative of $f(x) = x^n \sin(x)$ analytically
- [ ] Expand $e^x$ as a Taylor series around $x = 0$
- [ ] Write a Python function that computes the mean of an array
- [ ] Explain what $\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ means geometrically

If you're unsure about any of these, review the prerequisite material or ask for help during office hours.
:::

---

*Ready to begin? Let's start with Part 1 and discover why taking derivatives on a computer is fundamentally different from the calculus you learned.*
