---
title: "Overview: Foundations of Discrete Computing"
subtitle: "Numerical Methods Module 1 | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{note} Connection to quadrature
Use this module as error-analysis preparation for the quadrature reading. The
Taylor series reading explains why the composite rules have orders 1, 2, and 4.
The same local-to-global reasoning applies whenever a numerical method is built
from repeated discrete panels.
:::
<!-- prep-banner:end -->

## The Big Picture: When Computers Meet Calculus

### A Story That Changes Everything

In 1922, Lewis Fry Richardson published a numerical weather prediction experiment based on atmospheric observations from 1910. He calculated a pressure change of about 145 millibars in six hours, although the observed pressure changed little. He also imagined a forecast factory in which thousands of human computers would coordinate the calculations. That factory was a proposal, not the team that carried out his experiment.

The important question is why the calculation failed. The initial pressure and wind fields were not adequately balanced, exciting rapid atmospheric oscillations that overwhelmed the slower weather signal. Peter Lynch's reconstruction shows that filtering the initial data greatly improves the forecast. The failure cannot be attributed simply to large finite-difference steps or rounding. [Source: Lynch's reconstruction](https://maths.ucd.ie/~plynch/Publications/JCP.pdf).

This story gives us a useful habit: identify the mechanism before choosing a numerical repair. Smaller steps cannot repair an inappropriate initial state, just as a better initial state cannot repair an unstable method. In this module, we isolate approximation and floating-point errors so that each experiment tests a specific explanation.

### Your Mission: Master the Art of Approximation

You're about to discover how to navigate the fundamental paradox of computational physics:

- **Calculus requires** taking limits as $h \to 0$
- **Computers can't** represent infinitesimally small numbers
- **Yet somehow** we can simulate galaxies, track spacecraft to Jupiter, and detect gravitational waves

The resolution of this paradox — understanding exactly what errors we introduce and how to control them — is the foundation of all computational astrophysics.

### Why This Matters Now More Than Ever

Modern astrophysics pushes computational limits like never before:

- **LIGO** measures strains of order $10^{-21}$. That magnitude is within binary64's representable range; it does not require 21 significant digits. Storing a small strain directly is different from resolving it by subtracting two numbers near 1.
- **JWST** data analysis combines many pixel measurements to estimate faint signals. Numerical error must be assessed alongside detector noise, calibration uncertainty, and the assumptions of the analysis; signal size alone does not tell us which contribution dominates.
- **Cosmological simulations** follow many interacting particles over cosmic time. Numerical errors can accumulate or be amplified; the growth depends on the dynamics, algorithm, and observable being measured. Exponential separation of nearby chaotic trajectories does not imply that every observable error grows exponentially.
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
### 🏃 Fast Track
Essential concepts only

- [The core paradox](01-mod1-part1-finite-differences.md#the-core-problem)
- [Optimal h derivation](01-mod1-part1-finite-differences.md#optimal-h)
- [Machine epsilon](02-mod1-part2-numerical-errors.md#machine-epsilon)
- [Error types](02-mod1-part2-numerical-errors.md#three-types)
:::

:::{grid-item}
### 🚶 Standard Path
Full conceptual understanding

Everything in Fast Track, plus:

- [All finite difference methods](01-mod1-part1-finite-differences.md#finite-difference-landscape)
- [Catastrophic cancellation](02-mod1-part2-numerical-errors.md#catastrophic-cancellation)
- [Error measurement](02-mod1-part2-numerical-errors.md#measuring-errors)
- [Taylor series applications](03-mod1-part3-taylor-series.md)
:::

:::{grid-item}
### 🧗 Complete Path
Deep dive with all details

Complete module including:

- All mathematical derivations
- Custom method design
- Automatic differentiation
- All worked examples
- Historical context
:::

::::

### Navigation by Project Needs

:::{tip} Quick Jump to What You Need by Project
:class: dropdown

**For numerical integration**:
- [Taylor expansions and quadrature panels](03-mod1-part3-taylor-series.md#from-taylor-expansions-to-quadrature-panels)
- [Absolute and relative error](02-mod1-part2-numerical-errors.md#measuring-errors)
- [Convergence without a reference value](02-mod1-part2-numerical-errors.md#convergence-testing-without-true-values)
- [Quadrature and tests](../02-roots-quadrature/02-mod2-part2-quadrature.md#building-a-reusable-numerical-method)

**For root finding and stateful models**:
- [Taylor series as a local model](03-mod1-part3-taylor-series.md#introduction-from-theory-to-practice)
- [Sensitivity and cancellation](02-mod1-part2-numerical-errors.md#catastrophic-cancellation)
- [Root-finding reading](../02-roots-quadrature/01-mod2-part1-root-finding.md)

**For later time-evolution work**:
- [Truncation, round-off, and accumulated error](02-mod1-part2-numerical-errors.md#three-types)
- [Choosing a scale-aware step](01-mod1-part1-finite-differences.md#practical-algorithm)
:::

:::{note} Why this module exists
:class: dropdown

Numerical software has assumptions. You need to recognize them before you use a result. A method needs checking when:

- Your energy conservation mysteriously fails after a million timesteps
- Your code gives different answers on different machines
- Your optimization gets stuck because gradients underflow to zero

The aim is to derive the leading error, measure the observed convergence, and
state the regime in which a method is reliable. For example, the forward
difference has a truncation term that decreases with $h$ and a round-off term
that eventually increases as $h$ becomes too small. The optimal scale follows
from that competition; it is not a universal constant.
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

### [Part 1: Finite Differences and Discrete Calculus](01-mod1-part1-finite-differences.md)
- Why computers cannot take true limits
- Forward, backward, and central differences from first principles
- The optimal step size derivation
- Practical algorithms for choosing $h$

### [Part 2: Floating-Point Arithmetic and Numerical Error](02-mod1-part2-numerical-errors.md)
- Finding and understanding machine epsilon
- Three types of numerical error
- Catastrophic cancellation and how to avoid it
- Error propagation in long calculations

### [Part 3: Taylor Series, Error Order, and Derivative Methods](03-mod1-part3-taylor-series.md)
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

Start with Part 1, then use Part 3 before implementing quadrature rules.
