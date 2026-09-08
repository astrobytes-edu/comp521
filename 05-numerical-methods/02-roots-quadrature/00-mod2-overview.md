---
title: "Overview: Root Finding and Quadrature"
subtitle: "Numerical Methods Module 2 | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{note} Block 2 sequence
This overview links two related method families, but they are not taught as one
project. Project 2 uses [Part 2: Quadrature](02-mod2-part2-quadrature.md):
composite rules, convergence tests, adaptive Simpson, and substitution. Monte
Carlo remains optional conceptual enrichment, with no assigned deliverable. Root finding begins in Block 3 and supports Project 3. The
`Star` class also belongs to Project 3, not Project 2.
:::
<!-- prep-banner:end -->

## The Big Picture: Learning Equilibrium Through Mathematics

### A motivating physical problem

Lagrange's 1772 analysis identified five equilibrium configurations in the
restricted three-body problem. A spacecraft near $L_2$ follows an orbit around
that configuration rather than remaining at a static point; the calculation
uses a model, a coordinate convention, and numerical solution procedures.

That example separates two tasks that recur in computational physics:

- solve $f(x)=0$ for an equilibrium or event location;
- approximate $\int_a^b f(x)\,dx$ for an accumulated quantity.

They use some shared ideas—contracts, convergence evidence, and sensitivity—but
they are different numerical problems.

### What this module provides

You're about to discover that the cosmos is filled with equilibrium points and measurable quantities:

- **Where does a stellar model reach its surface?** Root finding locates the boundary of a pressure-supported model
- **How much energy does a galaxy radiate?** Integration across the spectrum
- **Where can spacecraft orbit with minimal fuel?** Finding Lagrange points
- **What's the total mass of a dark matter halo?** Integrating density profiles

Root finding and quadrature recur in many models. Correct use depends on the
regularity of the function, available information, required error measure, and
the cost of evaluating the model.

### Why the distinction matters

Examples include integrating a luminosity density, evaluating a transit flux,
and solving an equilibrium condition. A library call does not remove the need
to define a method's inputs, assumptions, and verification test.

## Quick Navigation Guide

### Choose your learning path

::::{grid} 1 1 2 3

:::{grid-item}
### 🏃 Fast Track
Essential concepts only

- [Left rectangle rule](02-mod2-part2-quadrature.md#method-1-left-rectangle-rule)
- [Trapezoidal rule](02-mod2-part2-quadrature.md#method-2-trapezoidal)
- [Composite Simpson's rule](02-mod2-part2-quadrature.md#method-3-simpson)
- [Adaptive Simpson](02-mod2-part2-quadrature.md#adaptive-quadrature)
:::

:::{grid-item}
### 🚶 Standard Path
Full conceptual understanding

Everything in Fast Track, plus:

- [Convergence testing](../01-foundations/02-mod1-part2-numerical-errors.md#convergence-testing-without-true-values)
- [Simpson's rule](02-mod2-part2-quadrature.md#method-3-simpson)
- [Quadrature error analysis](02-mod2-part2-quadrature.md#method-2-trapezoidal)
- [Method selection](03-mod2-synthesis.md#method-selection)
- [Quadrature investigation](02-mod2-part2-quadrature.md#quadrature-investigation)
- All "Check Your Understanding" boxes
:::

:::{grid-item}
### 🧗 Complete Path
Deep dive with all details

Complete module including:

- All mathematical derivations
- [Optional Monte Carlo integration](02-mod2-part2-quadrature.md#method-5-monte-carlo)
- [Gaussian quadrature](02-mod2-part2-quadrature.md#method-4-gaussian)
- [Richardson extrapolation](02-mod2-part2-quadrature.md#richardson-extrapolation)
- [Root-finding investigation for Block 3](01-mod2-part1-root-finding.md#root-investigation)
- [An integral inside a root problem](03-mod2-synthesis.md#shared-error-budget), after both topics
- All worked examples
:::

::::

### Navigation by Project Needs

:::{tip} Quick Jump to What You Need by Project
:class: dropdown

**For Project 2 (numerical integration)**:
- [Reusable function contract and `pytest`](02-mod2-part2-quadrature.md#building-a-reusable-numerical-method)
- [Composite rules and their orders](02-mod2-part2-quadrature.md#building-integration-methods-from-rectangles-to-optimality)
- [Adaptive Simpson's rule](02-mod2-part2-quadrature.md#adaptive-quadrature)
- [Substitution and endpoint behavior](02-mod2-part2-quadrature.md#project-2-applications-endpoints-and-branch-points)
- Optional conceptual enrichment: [Monte Carlo RMS error](02-mod2-part2-quadrature.md#method-5-monte-carlo)

**For Project 3 (root finding and classes)**:
- [Root-finding methods](01-mod2-part1-root-finding.md)
- [Taylor expansions and local error](../01-foundations/03-mod1-part3-taylor-series.md)
- [Floating-point error and conditioning](../01-foundations/02-mod1-part2-numerical-errors.md)
:::

:::{note} Method-selection rule
:class: dropdown

Do not choose a numerical method by its name or nominal order. State the
quantity, the function contract or data model, the error measure, and a test.
A result needs investigation when:
- Their root finder diverges on a "simple" equation
- Integration gives wildly different answers with different methods
- Monte Carlo takes forever to converge

A bracket gives bisection a convergence guarantee for a continuous function
with a sign change. Newton's method uses a local linear model; it is not
gradient descent. Monte Carlo has a root-mean-square rate proportional to
$N^{-1/2}$ under independent, finite-variance sampling, but whether it is the
best method depends on variance, dimension, structure, and cost.
:::

## Mathematical Foundations

:::{important} 📖 Core Notation and Concepts
Before diving in, let's establish the mathematical language for static problems:

### Root Finding Notation

| Symbol | Meaning | Physical Example |
|--------|---------|-----------------|
| $f(x) = 0$ | Residual equation to solve | A discretized equilibrium or boundary condition |
| $x^*$ or $r$ | Root/zero of function | Stellar radius |
| $[a,b]$ | Bracketing interval | Search region |
| $\epsilon$ | Tolerance | Desired accuracy |
| $e_n = x_n - r$ | Error at iteration n | Distance from true root |

### Integration Notation

| Symbol | Meaning | Physical Example |
|---------|---------|-----------------|
| $\int_a^b f(x)dx$ | Definite integral | Total luminosity |
| $w_i$ | Quadrature weights | Sample contributions |
| $x_i$ | Quadrature points | Where to evaluate |
| $h$ | Step size | Wavelength spacing |
| $O(h^p)$ | Error order | Convergence rate |

### Key Relationships

**Root Finding Convergence Rates**:
- Bisection: bracket half-width $B_{n+1}=B_n/2$; actual midpoint error need not halve.
- Secant near a smooth simple root: $|e_{n+1}|\approx C|e_n|^{1.618}$.
- Newton near a smooth simple root: $|e_{n+1}|\approx C|e_n|^2$ when the quadratic term is nonzero.

**Integration Error Scaling**:
- Trapezoidal: $E \propto h^2$
- Simpson: $E \propto h^4$
- Monte Carlo: RMS error $\propto N^{-1/2}$ for independent finite-variance samples

These patterns recur in scientific computing, but each application still needs
an explicit model and a convergence check.
:::

## Module Contents

### [Part 1: Root Finding](01-mod2-part1-root-finding.md)

Learn three fundamental approaches to finding zeros: bracketing (bisection), tangent following (Newton), and interpolation (secant). Discover why different methods excel in different situations and how to combine them for robustness. Apply these to Kepler's equation, Lagrange points, and stellar structure.

### [Part 2: Quadrature — Discrete Sums, Error, and Adaptation](02-mod2-part2-quadrature.md)

Build composite rules from panels, measure their convergence, and implement a
tested module. Compare deterministic and Monte Carlo estimators using their
actual assumptions and cost.

### [Part 3: Synthesis and Method Selection](03-mod2-synthesis.md)

Separate root-finding and integration contracts, then compare their convergence
claims and failure modes.

---

For Block 2, begin with Part 2. Return to Part 1 when Block 3 introduces root
finding.
