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

## Lectures 1–2 · Random variables, propagation, and shared physics

[Open the slides](/reveal/lecture-14-uncertainty.html) ·
[Read the worked handout](/reveal/lecture-14-uncertainty.handout.html).

The deck follows uncertainty from input distributions through a deterministic
physical model. It introduces probability density, expectation, covariance,
Monte Carlo propagation, local derivative approximations, and the effect of
shared physics on a cohort mean. The examples use labeled teaching models and
reproducible Python figures.

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

[Return to the Lecture Library](index.md).
