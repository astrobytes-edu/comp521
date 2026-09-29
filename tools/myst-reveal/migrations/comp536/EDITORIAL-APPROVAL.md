# Approved editorial changes

Status: Anna approved O1–O7 and S1–S6 in this session. These changes are applied; the before/after record is `approved-editorial-edits.json`. Layout continuations retain the source explanations and examples.

Software Engineering editing is already authorized. Its before/after record is `software-engineering-edits.json`; all original sections are retained, with a six-slide worked example added.

## ODE Methods

### O1 — Bound Euler's failure to the demonstrated problem

Original, “Why Euler Fails”: “Euler's method on conservative systems is fundamentally broken” and “No amount of resolution fixes a structural flaw.”

Proposed: “For the harmonic oscillator, forward Euler increases energy by a factor of 1 + omega² h² each step. Reducing h reduces the error over a fixed time interval, but does not make the method symplectic. For long integrations, examine both convergence and conservation diagnostics.”

Keep the derivation, plots and exact growth formula. Explain that numerical discretization error can be structural; these are not opposites. On the decay warmup, add the stability restriction 0 < h < 2 for y' = -y, with monotone decay for 0 < h <= 1.

### O2 — Correct the Runge–Kutta generalization

Original heading: “The Problem With All Runge-Kutta Methods”; original claim: energy drift is “always in the same direction.”

Proposed heading: “Accuracy and structure are different questions.”

Proposed text: “The explicit midpoint RK2 and classical RK4 methods shown here are not symplectic. Their behavior depends on the problem, timestep and duration. Some implicit Runge–Kutta methods are symplectic. Use this oscillator to compare phase error, trajectory error and energy error separately.”

Keep the RK2/RK4 implementations and all comparisons.

### O3 — Correct leapfrog energy claims and unsupported percentages

Original: modified energy is conserved “exactly”; energy is bounded “forever”; physical energy is “conserved to machine precision”; table asserts percentage drift after 10^6 and 10^9 steps without a specified experiment.

Proposed: “For a separable Hamiltonian and a fixed timestep, kick-drift-kick leapfrog is symplectic and time reversible. In the stable oscillator regime (h omega < 2), its physical-energy error oscillates rather than showing Euler's secular growth. This does not imply exact physical-energy conservation. General long-time bounds require additional assumptions and exclude numerical instabilities.”

Replace the percentage table with a qualitative comparison of order, structure and measured diagnostics. Retain all surrounding explanation of kick/drift shears, formulas and exercises. A numerical drift table would require a separately specified and executed experiment.

### O4 — Correct the integration endpoint behavior

The original `while` loops always take a full h step and can overshoot `t_end`. Proposed: explicitly document the actual final time in the fixed-step comparison. For a general endpoint-targeting solver, use a final shortened step and explain its implications; do not quietly alter the fixed-step symplectic comparison.

### O5 — Adapt the course context without reducing content

Keep the N-body narrative and project-launch material as labelled COMP 536 case-study detail slides. Add a COMP 521 main-path bridge to Project 4: ODE library, hydrostatic equilibrium, surface finding, shooting and order verification. Update “assigned,” reading and deadline language so imported COMP 536 tasks do not become COMP 521 requirements. Proposed split: Euler/RK lecture, then stability/structure and planetary-interior application.

## Statistical Thinking Foundations

### S1 — State assumptions for CLT and Monte Carlo rates

Original: aggregate collision statistics approach Gaussian behavior; precision improves as 1/sqrt(N), without conditions in the slide prose.

Proposed: “For independent identically distributed samples with finite variance, the sample-mean standard error scales as sigma/sqrt(N). Dependence reduces the effective sample size; heavy tails or nonstationarity can invalidate this simple estimate. CLT statements concern the standardized sum or mean under their assumptions, not every distribution becoming Gaussian.”

Keep the existing temperature, pressure, sampling and convergence examples; put mathematical conditions in an optional detail slide.

### S2 — Make the covariance question answerable

Original checkpoint: “If covariance is ignored, are propagated uncertainties usually under- or over-estimated?”

Proposed: “For z = x + y, how does positive versus negative covariance change Var(z)? Compare Var(x) + Var(y) + 2 Cov(x,y) with the independent-input approximation.”

The answer depends on covariance and the observable's derivatives. Retain the predict/play/explain structure.

### S3 — Distinguish raw moments, variance and skewness

Original defines M_n = E[X^n], then describes code computing mean, sample variance and standardized skewness as “first three moments.”

Proposed: keep the raw-moment definition and add the central/standardized definitions. Label the code outputs “mean, variance and skewness”; explain existence of the required moments and why a finite sample does not establish tail behavior. Do not replace or shorten the code.

### S4 — Correct the exit-ticket arithmetic and notation

Original: “You doubled” the sample count from 10^4 to 4 times 10^4.

Proposed: “You quadrupled the sample count from N = 10^4 to N = 4 × 10^4. Under the independent finite-variance sampling model, what happens to standard error?” Correct answer remains a factor of two reduction. Repair doubled LaTeX escapes in the source math.

### S5 — Separate isotropic directions from a spatial model

Original direction sampler returns points on the unit sphere; the exit ticket refers to “isotropic positions,” and the accompanying figure is a Plummer spatial-sampling figure.

Proposed: explicitly state that isotropic angles determine direction only. A spatial population also needs a radial distribution; a mass distribution and isotropic directions alone do not specify full initial conditions. Keep the original Plummer figure as context, with an explanatory caption.

### S6 — Adapt context and qualify the sampling claim

Keep the astrophysical and ML examples. Replace COMP 536 Project 2/3 assignment language with a labelled case study plus a COMP 521 connection to sampling, uncertainty and model-fitting work. Clarify that a power-law sampler generates draws from the declared model; realism depends on the model, limits and evidence. Resolve the roadmap's timing gaps when making a delivery plan.

## Approval

Anna may approve O1–O5 and S1–S6 together, or identify individual items. O1–O5 and S1–S6 were subsequently approved and applied.


## Additional findings from the full pass — approved and applied

### O6 — Timestep arithmetic and convergence conditions

Original: h = 0.01 T is “about 600 points per period.” Proposed: “100 points per period.” The oscillator example h = 0.1, T = 2 pi remains about 63 points per period. Qualify 60–100 points as an illustrative starting point rather than a universal accuracy requirement; establish accuracy by refinement and problem-specific tolerances. On the order slide, say that 2^p error reduction assumes the asymptotic convergence regime with the same final time, and that per-step cost also matters.

### O7 — RK4/Simpson comparison

Original: “Weights 1/6, 2/6, 2/6, 1/6 are Simpson's rule!” Proposed: “The RK4 weights resemble Simpson quadrature when the midpoint contributions are combined, but the stages evaluate derivatives at different estimated states. RK4 is not simply Simpson integration of a known integrand.” Keep the weight formula and the equation-to-code teaching point.
