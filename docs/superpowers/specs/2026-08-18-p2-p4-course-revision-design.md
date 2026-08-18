# COMP 521 Projects 2–4 revision design

## Decision

Project 1 is retained as written. Projects 2–4 are a cumulative scientific
computing sequence whose scope fits two weeks each:

```text
P2: integrate a physical model
P3: solve nonlinear equations in that model and apply them to stars
P4: solve an exoplanet-interior model with ODEs
```

The projects intentionally build on student-owned prior code. They are
curricularly self-contained, not independent take-home packets: P2 starts from
P1's transit functions, P3 starts from P1–P2 code, and P4 starts from P1–P3
code. The eventual course design must state a recovery path for a student whose
earlier implementation is not usable, without treating an instructor solution
as ordinary starter code.

## Project 1

Retain Project 1's scope, deliverables, and two-figure structure. It remains
the first-project foundation after Project 0 and needs only a final
student-facing consistency pass.

## Project 2 — Numerical integration

Keep the core scientific arc:

1. Implement rectangle, trapezoid, and Simpson quadrature as reusable
   functions, then measure their convergence and test them.
2. Integrate the Planck function to derive the Stefan–Boltzmann constant.
3. Compute a limb-darkened transit and recover the uniform-disk result at
   `u = 0`.
4. Implement recursive adaptive Simpson and compare error against function
   evaluations with fixed Simpson.
5. Diagnose the reduced order caused by the transit integrand's branch point,
   then repair it with the specified substitution.
6. Implement a seeded, one-dimensional Monte Carlo estimator and verify its
   empirical `N^(-1/2)` rate against the deterministic methods.

Keep recursive adaptive Simpson: it is the general-purpose answer for an
integrand whose structure is not yet understood, whereas the substitution is
the more efficient answer once that structure is known. The point-distribution
histogram is enrichment rather than a required deliverable. Remove only the
high-dimensional tensor-grid-versus-Monte-Carlo crossover experiment; it is an
interesting lecture or enrichment demonstration, not a required project
deliverable.

## Project 3 — Root finding and stellar inference

Retain the current Project 3 core:

- bisection, Newton, and secant methods with convergence/failure analysis;
- Wien's-law and Kepler-equation applications;
- transit contact points and duration; and
- the `Star` class plus the 15-star habitable-zone figure.

The 15-star figure stays. It is the intended bridge from a student making one
object work to applying that object to the real stellar measurements already
curated in Project 1. It is not a live-data or archive-access assignment;
network-dependent data acquisition begins in Project 5.

## Project 4 — Exoplanet interiors

Project 4 remains an exoplanet-interior project:

1. Implement Euler, RK2, and RK4 with measured-order validation.
2. Implement the published equation of state, including the required SI-to-CGS
   conversion, and integrate a rocky planet.
3. Locate the planetary surface with P3's root-finding machinery and diagnose
   the observed loss of order caused by the moving endpoint.
4. Use shooting on central pressure to produce planetary mass–radius curves and
   compare them with Seager's published relations.

Retain the `rho0 = 0` analytic limit only as a concise regression/validation
check. It is not a separate Lane–Emden lesson: students do not derive or solve
stellar structure, build a star model, or produce a planet-versus-star figure.

Remove the stellar equation-of-state swap, stellar profiles, and all language
that frames the project as applying one solver to a star. The interior-profile
figure becomes planet-only; the mass–radius figure remains planet-only.

## Downstream public contract

The student-facing syllabus and schedule must eventually state the sequence
accurately:

| Block | Student-facing title |
|:--|:--|
| P2 | Numerical Integration |
| P3 | Root Finding and Stellar Inference |
| P4 | ODE Methods and Exoplanet Interiors |
| P5 | Real Data and Model Fitting |
| P6 | Machine Learning and Scientific Classification |

Project 5 and Project 6 are not made final by this decision. They remain
explicitly separate design-and-authoring work; the syllabus must not overclaim
their unbuilt particulars.

## Verification after implementation

- The P2 brief requires recursive adaptive Simpson, its fixed-grid comparison,
  the substitution repair, and one-dimensional seeded Monte Carlo; it has no
  required high-dimensional crossover or adaptive-point histogram deliverable.
- The P3 brief retains the `Star` class and 15-star habitable-zone figure, and
  contains no data-download/Lightkurve requirement.
- The P4 brief and solution contain no required star-model section, star
  profiles, or planet-versus-star figure; the analytic limit is labelled only
  as validation.
- The syllabus, schedule, grading, and AI-policy pages use the same project
  sequence and do not call P5/P6 detailed assignment briefs final before they
  exist.
