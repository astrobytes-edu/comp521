# Optimization for Scientific Models

Fifty-two MyST Reveal slides and a worked handout for guide Lectures 3–4,
Sections 2.1–2.7. The student source contains no instructor speaker notes.
Detailed presenter notes and reference materials remain in the private
instructor workspace.

## Teaching sequence

The deck starts with observations and a two-parameter prediction. It builds
residuals and losses from Gaussian and Poisson measurement models, then derives
a scalar calibration loss before teaching derivatives and gradient descent.
Curvature, conditioning, and Newton's failure example motivate safeguards.
Gauss–Newton and Levenberg–Marquardt use the residual structure and test actual
trial losses. The final section separates fitting, identifiability, stated
preferences, physical constraints, and model checking.

Short definition frames explain positive definiteness, Cholesky factorization,
eigenvalues/eigenvectors, and rank before their algorithmic use. Smaller
definition callouts supply other first-use vocabulary. The cover connects the
same observations to the actual parameter-loss landscape and accepted updates.

The layout follows the preceding paired lecture and
`tools/myst-reveal/AUTHORING.md`: light navy/teal styling, staged questions,
readable KaTeX equations, and executed Python figures. Slides use 44 px titles,
30 px body text, 24 px definition callouts, and 22 px supporting text.

## Build locally

From the course root:

```sh
PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -B scripts/build_optimization_slides.py
```

The build freshly executes all 22 notebook code cells in the course Python
environment, exports the MyST slides and worked handout, checks the student
publication boundary, and writes only those two HTML files to
`09-lectures/reveal/`. It does not require private notes. Neither export
contains speaker-note blocks or the private presenter extension.

`figures.py` owns the calculations and plot construction.
`numerical-checks.json` records analytic checks, the float64 setup, the
reference-solver comparison, and the numerical qualifications. All observations
are synthetic. The fading model is dimensionless exponential relaxation, not
a full stellar model. Damping controls the algorithm; it is distinct from a
physical prior. A small gradient or a successful stopping test does not establish
model validity or supply a posterior distribution.

The stable student route is `09-lectures/jaxstro-sciml-guide.md`, with paired
links to `/reveal/lecture-15-optimization.html` and
`/reveal/lecture-15-optimization.handout.html`.

## Review and publication

The approved draft was reviewed across all 52 PDF pages, 122 projector states
at 1440 × 900 and 1280 × 720, and both worked handouts. Its focused visible-layout
and role-based font checks passed. The unmodified shared checker retains three
horizontal-width reports on two slides; visible review found no clipping.
This limitation is not reported as a passing shared check.

For a fresh shared report and review PDF:

```sh
node tools/myst-reveal/src/check.mjs 09-lectures/myst-source/lecture-15-optimization/_build/reveal/decks.json --out 09-lectures/myst-source/lecture-15-optimization/_build/review
```

The build command is local. Commit, push, publication, and any private-repository
CI require their own authorization. After an authorized deployment, verify the
lecture-page links, both live exports, their release hashes, and the absence of
instructor notes in the served HTML.
