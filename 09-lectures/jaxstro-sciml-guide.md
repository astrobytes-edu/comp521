---
title: "Probability, Optimization, and Scientific Discovery"
subtitle: "Jaxstro SciML guide · Lecture handouts and full draft"
---

{download}`Read the full draft (PDF, 59 pages) <downloads/jaxstro-sciml-guide/COMP521_Probability_Optimization_Notes_1.pdf>`.

These draft notes connect probability and uncertainty to optimization,
statistical inference, experimental design, and automatic differentiation.
The full draft includes the complete notes, exercises (Appendix A), and worked
solutions (Appendix B).

Slide decks group two guide lectures into one presentation. The PDF handouts
below retain their individual lecture numbers.

[Featured review](#block6-featured-review) · [Books and tutorials](#block6-resources).

(block6-featured-review)=
## Featured review · Physics and learning

:::{card} Bridging Control, Inference, Transport, and Thermodynamics: From Theory to Applications in Learning
Emmy Blumenthal and coauthors (2026).

A physics-based route through optimal control, probabilistic inference,
optimal transport, and nonequilibrium thermodynamics. The review connects these
ideas to sampling, reinforcement learning, and generative models through
constrained optimization.
+++
**Free HTML and PDF.** [Read the review online](https://arxiv.org/html/2609.15897v1) · [Download the review PDF](https://arxiv.org/pdf/2609.15897).
:::

## Lectures 1–2 · Random variables, propagation, and shared physics

[Open the slides](/reveal/lecture-14-uncertainty.html) ·
[Read the worked handout](/reveal/lecture-14-uncertainty.handout.html).

The deck follows uncertainty from input distributions through a deterministic
physical model. It introduces probability density, expectation, covariance,
Monte Carlo propagation, local derivative approximations, and the effect of
shared physics on a cohort mean. The examples use labeled teaching models and
reproducible Python figures.

## Lectures 3–4 · Optimization for Scientific Models

[Open the slides](/reveal/lecture-15-optimization.html) ·
[Read the worked handout](/reveal/lecture-15-optimization.handout.html).

How do we choose model parameters when measurements are imperfect? This deck
builds a loss from a measurement model, works through gradient descent on a
one-parameter example, and uses curvature to develop Newton, Gauss–Newton, and
Levenberg–Marquardt updates. It defines the matrix vocabulary as it appears,
tests proposed steps against the actual loss, and distinguishes a fitted answer
from information the observations can supply. The figures use reproducible
synthetic teaching examples.

## Lecture handouts

Each handout preserves the section, equation, figure, listing, and exercise
numbering of the full draft. The lecture numbers below belong to this guide's
PDF series.

| Guide lecture | Handout (PDF) | Sections in the full draft |
|---|---|---|
| 1 | {download}`Random variables and probability <downloads/jaxstro-sciml-guide/L01_random_variables.pdf>` | How to use these notes; 1.1–1.5 |
| 2 | {download}`Propagating uncertainty and shared physics <downloads/jaxstro-sciml-guide/L02_propagation.pdf>` | 1.6–1.7 |
| 3 | {download}`Losses, gradients, and gradient descent <downloads/jaxstro-sciml-guide/L03_losses_gradient_descent.pdf>` | 2.1–2.4 |
| 4 | {download}`Newton's method, Levenberg–Marquardt, and conditioning <downloads/jaxstro-sciml-guide/L04_newton_conditioning.pdf>` | 2.5–2.7 |
| 5 | {download}`Likelihoods, Bayes' theorem, and the Laplace approximation <downloads/jaxstro-sciml-guide/L05_likelihood_bayes.pdf>` | 3.1–3.4 |
| 6 | {download}`Markov chain Monte Carlo and Hamiltonian Monte Carlo <downloads/jaxstro-sciml-guide/L06_mcmc_hmc.pdf>` | 3.5 |
| 7 | {download}`Hierarchical models, selection effects, and checking inference <downloads/jaxstro-sciml-guide/L07_hierarchical_checking.pdf>` | 3.6–3.7 |
| 8 | {download}`Identifiability and Fisher information <downloads/jaxstro-sciml-guide/L08_identifiability_fisher.pdf>` | 4.1–4.4 |
| 9 | {download}`Experimental design and surrogate models <downloads/jaxstro-sciml-guide/L09_design_surrogates.pdf>` | 4.5–4.6 |
| 10 | {download}`Automatic differentiation and when it fails <downloads/jaxstro-sciml-guide/L10_autodiff.pdf>` | 5.1–5.4 |
| 11 | {download}`Gradients of expectations, ML vocabulary, and research workflows <downloads/jaxstro-sciml-guide/L11_expectations_workflows.pdf>` | 5.5–5.6 and 6.1–6.3 |

(block6-resources)=
## Books and tutorials

These five resources appear in the Guide's **Suggested reading** on page 57.
Each has a free reading option. Use the descriptions to choose a reference for
the topic you are studying.

::::{grid} 1 1 2 2

:::{card} Statistical Machine Learning for Astronomy
Yuan-Sen Ting.

Study probability, Bayesian inference, and machine learning through
astronomical data, with computational tutorials.
+++
**Free HTML book, PDF, and notebooks.** [Open Statistical Machine Learning for Astronomy](https://tingyuansen.github.io/statml/).
:::

:::{card} The Elements of Differentiable Programming
Mathieu Blondel and Vincent Roulet.

Connect automatic differentiation, implicit differentiation, optimization, and
gradients of expectations in one mathematical treatment.
+++
**Free HTML book and PDF.** [Read The Elements of Differentiable Programming](https://diffprog.github.io/).
:::

:::{card} Algorithms for Optimization
Mykel J. Kochenderfer and Tim A. Wheeler.

Explore optimization algorithms through worked examples and supporting
notebooks. The Guide cites the **2019 first edition**; the site also offers a
second-edition preview.
+++
**Free first-edition PDF and teaching materials.** [Open the official Algorithms for Optimization site](https://algorithmsbook.com/optimization/) or [choose the 2019 PDF](https://algorithmsbook.com/optimization/files/optimization-1e.pdf).
:::

:::{card} Gaussian Processes for Machine Learning
Carl Edward Rasmussen and Christopher K. I. Williams.

Learn Gaussian-process regression, covariance functions, and uncertainty-aware
surrogates for expensive scientific calculations.
+++
**Free full-book and chapter PDFs.** [Read Gaussian Processes for Machine Learning](https://gaussianprocess.org/gpml/).
:::

:::{card} Deep Learning for Astrophysics
Contributors to the NASA Cosmic Origins AI/ML lecture series.

Explore neural networks, generative models, and simulation-based inference
through an astrophysics textbook and companion teaching material.
+++
**Free HTML book, notebooks, and lecture recordings.** [Open Deep Learning for Astrophysics](https://deeplearning4astro.com/).
:::

::::

[Return to the Lecture Library](index.md).
