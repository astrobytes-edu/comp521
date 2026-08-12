---
title: "Overview: Inferential Thinking"
subtitle: "Statistical Thinking Module 5 | COMP 521"
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

## The Big Picture: From Simulation to Inference

In Modules 1–4, you learned to simulate the universe — building statistical descriptions of particles, stars, and photons, then solving the governing equations numerically. But science doesn't end with simulation. **The central question of observational science is the inverse problem: given noisy, incomplete data, what can we infer about the underlying physics?**

Consider a concrete example: you observe the spectrum of a distant star. The photon counts at each wavelength are noisy, the dust along the line of sight has absorbed and reddened the signal, and your instrument has finite resolution. Somewhere buried in that data is the star's temperature, surface gravity, chemical composition, and distance. How do you extract those parameters — and how confident should you be in the answers?

This is the domain of **statistical inference**, and specifically **Bayesian inference** — a framework that treats unknown parameters as probability distributions rather than fixed values. It is the mathematical backbone of modern astrophysics, from cosmological parameter estimation to exoplanet characterization.

## Your Mission: Learn to Think Inferentially

You're about to discover that:

- **Every measurement is an act of inference** — we never observe parameters directly, only noisy functions of them
- **Bayes' theorem** provides a principled framework for updating beliefs with data
- **The likelihood function** encodes the physics connecting parameters to observations
- **Prior distributions** represent what we know before collecting data — and choosing them wisely matters
- **MCMC methods** make Bayesian inference computationally tractable for real problems
- **Hamiltonian Monte Carlo** exploits gradient information to explore high-dimensional parameter spaces efficiently

## Module Learning Objectives

By the end of this module, you will:

- [ ] **Explain** why astronomical measurement is fundamentally an inverse problem
- [ ] **Derive** Bayes' theorem and identify each component (prior, likelihood, evidence, posterior)
- [ ] **Construct** likelihood functions for common observational scenarios
- [ ] **Implement** the Metropolis-Hastings algorithm and diagnose convergence
- [ ] **Apply** Hamiltonian Monte Carlo to multi-dimensional parameter estimation
- [ ] **Interpret** posterior distributions, credible intervals, and model comparison via Bayes factors
- [ ] **Connect** computational inference to the statistical foundations from Modules 1–4

## Your Learning Path

### Part 1: The Philosophy of Measuring the Universe

What does it mean to measure something we cannot touch? Explore the philosophical foundations of scientific inference — models as compressed representations of reality, the role of prior beliefs, and why the inverse problem requires a statistical framework. This part establishes *what* we're doing before we learn *how*.

### Part 2: Inferential Thinking — Bayes' Theorem and Beyond

The mathematical heart of the module. Derive Bayes' theorem, understand likelihoods and priors, work through conjugate examples, and see how the posterior distribution answers scientific questions. Learn model comparison through the Bayesian evidence.

### Part 3: Markov Chain Monte Carlo

When posteriors can't be computed analytically — which is almost always in real science — we sample them. Learn the Metropolis-Hastings algorithm, understand detailed balance and ergodicity, diagnose convergence, and see MCMC applied to astrophysical parameter estimation.

### Part 4: Advanced MCMC Methods

Standard MCMC struggles in high dimensions. Hamiltonian Monte Carlo (HMC) and the No-U-Turn Sampler (NUTS) exploit the geometry of the posterior to explore parameter space efficiently. Learn the physics analogy behind HMC, implement it, and understand modern diagnostics.

## The Bridge You're Building

This module completes the five-module arc of statistical thinking:

1. **Module 1**: Statistics creates macroscopic properties from microscopic chaos
2. **Module 2**: $10^{57}$ particles $\to$ stellar structure through statistical mechanics
3. **Module 3**: $10^{5}$ stars $\to$ galactic dynamics through collisionless statistics
4. **Module 4**: $10^{9}$ photon packets $\to$ radiative transfer through Monte Carlo sampling
5. **Module 5**: Noisy data $\to$ physical parameters through Bayesian inference

The common thread deepens: Modules 1–4 taught you to go from physics to observables (the **forward problem**). Module 5 teaches you to go from observables back to physics (the **inverse problem**). Together, they form the complete scientific workflow — simulate, observe, infer.

## A Note on Perspective

Traditional statistics courses teach Bayesian methods abstractly. We take a different approach: **start with the scientific question** (what is this star's temperature?), **build the mathematical framework** (Bayes' theorem emerges from asking how to update beliefs), and **solve computationally** (MCMC turns intractable integrals into tractable sampling). The philosophy, mathematics, and computation reinforce each other at every step.
