---
title: "This Week"
subtitle: "COMP 521 | Current week and earlier material links"
site:
  hide_outline: true
---

# This Week

The current week appears first and starts open. Expand earlier weeks to recover
lecture, reading, and project links. Earlier entries are review routes; current
project briefs and the [Schedule](schedule.md) govern requirements and deadlines.

**Preparation** identifies a bounded reading focus. **Reference** supports work
on a specific problem. **Enrichment** is optional. Follow the [Projects](projects.md)
page and your project brief for what to implement and submit.

(week-10)=
::::{admonition} Current · Week 10 · October 27–29 · Project 4 completion and real data
:class: dropdown
:open: true

### Preparation and project context

Finish [Project 4](../08-assessments/projects/project-4.md), due
**Wednesday, October 28, 11:59 pm PT**. The project brief defines the required
work; use the [Schedule](schedule.md#week-10-oct-27-29-project-4-completion-and-real-data)
for this week's dates.

### Tuesday, October 27 — Foundations for scientific Data Science

How do noisy observations let us infer a physical quantity? Begin with the
connection between a forward model, measurements, and inference. Review random
variables, distributions, expectations, variance, and covariance, then connect
vectors, data matrices, dot products, and projections to model predictions.
Use a simple scientific measurement example to connect the ideas. Class also
includes Project 4 questions and completion time.

### Thursday, October 29 — Begin the methods

Move from the scientific question to data inspection and a first model fit:
provenance, units, missing values, residuals, and uncertainty weights. Introduce
the real Kepler photometry workflow, including quality flags and gaps, as the
application for Project 5. The project brief will define the implementation
scope and required work.

### Focused reference

- [Measurements, probability, and geometry](../06-linear-algebra-stats/00-linear-algebra/00d-measurements-probability-and-geometry.md):
  the primer for this week's foundations.
- [Statistical tools](../06-linear-algebra-stats/01-probability/02-mod1-part2-statistical-tools.md):
  Section 2.6 for variance and standard deviation; Section 2.1 for covariance,
  correlation, and independence.
- [Dot products and projections](../06-linear-algebra-stats/00-linear-algebra/00a-linear-algebra-core-module.md#dot-product)
  and [covariance matrices](../06-linear-algebra-stats/00-linear-algebra/00b-linear-algebra-stats-module.md#covariance-matrices):
  connect the geometry of data to statistical variation.
- [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md):
  review column inspection, types, boolean masks, and missing values.

These are selected reference sections, not whole-chapter assignments. Current
project briefs govern requirements and deadlines.

### Lecture and reference links

- [Lecture 13 · Measurements, Probability, and Geometry](../09-lectures/lecture-13-measurements.md):
  slides and worked handout for today's foundations.
- [Lecture 11 · ODE Methods](../09-lectures/lecture-11-odes.md):
  slides and worked handout for Euler, explicit midpoint RK2, RK4, and convergence.
- [Lecture 12 · Pandas and Exploratory Data Analysis](../09-lectures/lecture-12-pandas.md):
  slides, worked handout, and the saved NASA CSV. Use your own notebook to
  inspect and explore the table; there is no separate exploration submission.
- [Project 4's NASA data selection](../08-assessments/projects/project-4.md#select-usable-rows):
  the required columns, flags, uncertainty checks, and row counts for Part 3.
- [Data acquisition and cleaning](../04-scientific-computing/12-data-acquisition-cleaning.md)
  is an in-development scope note, not a completed technical lesson.

### Project work

Use [Project 4's required tests and submission](../08-assessments/projects/project-4.md#required-tests-and-submission)
to check your remaining work:

1. Verify the ODE methods against the exact SHO solution and check EOS unit
   conversions.
2. Check the constant-density planet, surface bracket, and numerical sensitivity
   to step size and starting radius.
3. Complete the three-material mass–radius comparison, including the Seager fit
   differences, NASA uncertainties, two named exoplanets, and selection counts.
4. Complete the interpretation answers and README, save the three required
   figures and NASA CSV, then restart the notebook and run all cells. Run
   `python -m pytest` from the project directory before submission.

Bring your current code and the first check you cannot yet explain. Keep
numerical refinement evidence separate from agreement with a published fit
and from comparison with observed planets.

### Looking ahead

Project 5 continues from the foundations and first fitting methods into data
preparation, transit-model fitting, uncertainty, and diagnostics. The
[Schedule](schedule.md#block-5-project-5-real-data-model-fitting) lists
Project 5 for **Thursday, October 29**, due **Wednesday, November 18,
11:59 pm PT**. Its public brief is not yet available; use the
[Projects page](projects.md) and Schedule for the current sequence and dates.
::::

(week-6)=
::::{admonition} Week 6 · September 29–October 1 · Kepler geometry and Project 3
:class: dropdown

### Preparation and project context

Use [Project 3 Science Background](../08-assessments/projects/project-3-science-background.md)
alongside the corresponding project parts:

- **Parts 1–2:** Sections 1–2 explain spectral density and the physically
  relevant Wien root. Why can a small residual still select the wrong root?
- **Parts 3–4:** Sections 3–8 connect orbital parameters, mean/eccentric/true
  anomaly, sky projection, and transit contacts. Trace the calculation from
  a trial time to a contact residual; distinguish orbital distance from
  projected separation and distinguish front from back.
- **Part 5:** Use the [stellar temperature-zone calculation](../08-assessments/projects/project-3.md#part-5-stars-and-where-the-algebra-wins)
  to identify the stored quantities, derived quantities, and round-trip checks
  for your `Star` class.

### Lecture and reference links

- [Software Engineering for Scientists](../09-lectures/software-engineering.md):
  slides, handout, and companion reading for contracts, independent checks,
  debugging, and reproducible results.
- [Lecture 10](../09-lectures/lecture-10-classes-lab.md): scientific classes and
  the Project 3 Part 5 lab.
- [Root-finding investigation](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#root-investigation):
  interpret residuals, updates, and brackets.
- [Class basics](../03-python/06-oop-fundamentals.md#week5-class-basics),
  [properties](../03-python/06-oop-fundamentals.md#week5-properties), and
  [type-contract tests](../04-scientific-computing/10-advanced-oop.md#week5-type-tests):
  return to the examples needed for `Star`; inheritance and operator overloading
  are not Project 3 requirements.

### Project work

Work through [Project 3](../08-assessments/projects/project-3.md), using its
[check-each-layer table](../08-assessments/projects/project-3.md#check-each-layer-before-combining-them)
to choose your next calculation:

1. Check the root library before relying on it in an application.
2. Recover the circular orbit before computing eccentric transit contacts.
3. Check contact selection and ordering, then compare circular durations with
   the analytic formula.
4. Check the `Star` temperature round trip and complete the fifteen-star comparison.
5. Restart the notebook and run all cells before your final commit and submission.

Bring your current code and the first check you cannot yet explain. Use the
[Schedule](schedule.md#block-3-project-3-root-finding-stellar-inference) for the
current project deadline and the [project rubric](projects.md#how-each-project-is-graded)
for the assessment dimensions. There is no separate lab submission.

### Enrichment and looking ahead

Advanced root-finding methods and dataclasses remain optional enrichment.
Next week's [Block 4](../09-lectures/block-04-odes.md) begins ODE methods;
its lecture pages are being prepared. Existing Euler and Runge–Kutta readings
are available for reference and remain under revision.
::::

(week-5)=
::::{admonition} Week 5 · September 22–24 · Trustworthy answers and scientific classes
:class: dropdown

### Preparation and reference


#### Prepare for Tuesday

Read [convergence rates](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-convergence) and the [root-evidence investigation](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#root-investigation). Be ready to distinguish residual, update, and root error.

#### Review after Tuesday

- [Backtracking](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#backtracking-newton): direction, distance, and acceptance.
- [Jacobians and local fitting](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-jacobians): matrix dimensions, predicted changes, and damping.
- [Safeguarded methods](../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md#week5-hybrids): preserve a bracket while using local proposals.
- [Adaptive estimates](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#adaptive-methods), [Richardson extrapolation](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#richardson-extrapolation), and [Gaussian quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#method-4-gaussian): match the method to the available information.

Focus on the explanations and worked examples. Implementations of advanced methods are optional enrichment; Project 3 requires the basic solvers specified in its brief.

#### Prepare for Thursday

1. Read [class basics and `self`](../03-python/06-oop-fundamentals.md#week5-class-basics), [methods](../03-python/06-oop-fundamentals.md#week5-methods), and [properties](../03-python/06-oop-fundamentals.md#week5-properties). Follow the introductory examples; extended examples and exercises are optional.
2. Read the [type contract](../04-scientific-computing/10-advanced-oop.md#week5-type-contract) and [tests of that contract](../04-scientific-computing/10-advanced-oop.md#week5-type-tests). The example uses a dataclass; understand its stored fields and validation, but implementing a dataclass is optional. An ordinary class is sufficient for Project 3.

Inheritance and operator overloading are not required. Review imports and `python -m pytest` in [Functions and Modules](../03-python/05-python-functions-modules.md) if needed.

### In class

- **Tuesday, September 22:** [Lecture 9](../09-lectures/lecture-09-trustworthy-answers.md) surveys methods including backtracking,
  Levenberg–Marquardt, integration, and convergence evidence; then Project 2 work time. Advanced methods are conceptual context, not new
  implementation requirements.
- **Thursday, September 24:** [Lecture 10](../09-lectures/lecture-10-classes-lab.md) develops methods, attributes, constructors, public and internal names, properties, and scientific classes; then Project 3 Part 5 lab.

Bring your Python environment, Project 1 stellar data and luminosity code,
and any completed Project 3 Part 2 work. In lab, build the `Star` class for
Part 5, reject invalid state, check derived values, and start the fifteen-star
comparison.

### Project work

[Project 2 · Numerical Integration](../08-assessments/projects/project-2.md)
connects quadrature to transit models. Its past deadline is recorded in the
[Schedule](schedule.md).

[Project 3 · Root Finding and Stellar Inference](../08-assessments/projects/project-3.md)
uses the current deadline in the [Schedule](schedule.md). Build reusable root
finders, investigate Wien's law, compute
Keplerian positions and transit contacts, and use a `Star` class for simplified
equilibrium-temperature zones. The project brief governs requirements and
submission; use the [course project rubric](projects.md#how-each-project-is-graded)
for the assessment dimensions.

Use the [Science Background](../08-assessments/projects/project-3-science-background.md)
for the spectral-density explanation, worked orbital example, and contact diagrams.
Read those sections alongside the corresponding project parts.

By the end of this week, aim to finish Parts 1–2 and begin Part 3. Test the root
library before using it for orbital calculations. These are pacing milestones;
the required submission is defined in the project brief.
::::

(week-4)=
::::{admonition} Week 4 · September 15–17 · Quadrature
:class: dropdown

**Lecture reference:** [Lecture 7](../09-lectures/lecture-07-adaptivity-roots.md)
and [Lecture 8](../09-lectures/lecture-08-rootfinding-tools.md) bridge adaptive
quadrature and root-finding tools. Use the [Lecture Library](../09-lectures/index.md)
for the complete sequence.

**Reading focus:** review [trapezoidal](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#method-2-trapezoidal)
and [Simpson](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#method-3-simpson)
rules, [adaptive quadrature](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#adaptive-methods),
and the [quadrature investigation](../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md#quadrature-investigation).
How does a refinement experiment distinguish observed convergence from nominal order?

**Project connection:** [Project 2](../08-assessments/projects/project-2.md).
Gaussian quadrature and Monte Carlo are optional enrichment; the brief defines
the integration methods to implement.
::::

(week-3)=
::::{admonition} Week 3 · September 8–10 · Approximations, errors, and reusable methods
:class: dropdown

**Lecture reference:** [Lecture 5](../09-lectures/lecture-05-approximation-errors-quadrature.md)
and [Lecture 6](../09-lectures/lecture-06-quadrature-modules-tests.md).

**Reading focus:** [forward and central differences](../05-numerical-methods/01-foundations/01-mod1-part1-finite-differences.md#forward-difference),
[error types](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md#three-types),
[absolute/relative error](../05-numerical-methods/01-foundations/02-mod1-part2-numerical-errors.md#measuring-errors),
and [Taylor polynomial and remainder](../05-numerical-methods/01-foundations/03-mod1-part3-taylor-series.md#taylor-polynomial-remainder).
What changes when the step becomes smaller, and which error mechanism sets a limit?

**Reference:** [function contracts](../03-python/05-python-functions-modules.md#function-contracts)
and [modules](../03-python/05-python-functions-modules.md#modules-as-reusable-scientific-boundaries).

**Project connection:** [Project 2](../08-assessments/projects/project-2.md),
including meaningful tests and convergence evidence. Automatic differentiation
and custom higher-order formulas are reference/enrichment routes.
::::

(week-2)=
::::{admonition} Week 2 · September 1–3 · Functions, arrays, and figures
:class: dropdown

**Lecture reference:** [Lecture 3](../03-python/bootcamp-03-data-functions.md)
and [Lecture 4](../03-python/bootcamp-04-arrays-figures.md).

**Reading focus:** [lists and tuples](../03-python/04-python-data-structures.md#lists-and-tuples),
[mutability and aliasing](../03-python/04-python-data-structures.md#mutability-and-aliasing),
and [function contracts](../03-python/05-python-functions-modules.md#function-contracts).
Use the first-reading routes in [NumPy](../04-scientific-computing/07-numpy-fundamentals.md)
and [Matplotlib](../04-scientific-computing/08-matplotlib-fundamentals.md) for
array shapes, vectorization, labeled axes, and figures. What quantity does each
array axis represent, and what can a reader infer from the figure?

**Project connection:** [Project 1](../08-assessments/projects/project-1.md).
Class design is later reference; Project 1 permits its functions in the notebook.
::::

(week-1)=
::::{admonition} Week 1 · August 25–27 · Python foundations and setup
:class: dropdown

**Lecture reference:** [Lecture 1](../03-python/bootcamp-01-run-calculate-inspect.md)
and [Lecture 2](../03-python/bootcamp-02-procedures-decisions.md).

**Reading focus:** use [Getting Started](../02-getting-started/getting-started.md)
for software setup and Git; use the [Part I guide](../03-python/index.md) to
find the initial routes through [environments](../03-python/01-python-environment.md),
[legible calculations](../03-python/02-python-calculator.md#legible-calculation),
[floating-point comparisons](../03-python/02-python-calculator.md#floating-comparisons),
and [pseudocode and state](../03-python/03-python-control-flow.md#pseudocode-and-state).
Which interpreter ran the calculation, and what makes the procedure stop?

**Project connection:** [Project 1](../08-assessments/projects/project-1.md).
The [Schedule](schedule.md) records the original setup and repository-check dates;
the brief and Canvas assignment govern the repository submission route.
::::
