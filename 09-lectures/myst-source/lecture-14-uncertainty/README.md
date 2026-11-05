# Random variables, propagation, and shared physics

Thirty MyST Reveal slides for guide Lectures 1–2, Sections 1.1–1.7. The deck
follows the 21-slide NotebookLM reference's order: probability representations,
transformations, three propagation methods, approximation limits, and shared
physics. Added slides define terms and work the mass–luminosity example. The
reference PDF and detailed presenter notes remain in the private instructor
repository.

The visual style follows Lecture 13's light indigo/teal theme, columns, readable
equations, and staged explanations. Prediction questions reveal answers only
after the prompt. Mathematical content is rendered with KaTeX. Figures are
reproducible Python calculations, not generated illustrations or model results.

## Build locally

From the course root:

```sh
PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -B scripts/build_uncertainty_slides.py
```

The build executes `calculations.ipynb` in the course environment, generates the
figures, and creates a self-contained student deck and worked handout in
`09-lectures/reveal/`. It also creates a private instructor deck with 30 native
speaker-note blocks. The student source owns the slide content; private notes
are injected by slide ID into a generated private project.

`figures.py` owns the numerical calculations and figure construction.
`numerical-checks.json` records the executed seed, Monte Carlo uncertainty,
analytic comparisons, and stated numerical checks. These are checks of the
teaching calculations, not qualification of a stellar model. All synthetic
parameters and the local fourth-power mass–luminosity approximation are labeled.

## Review the exports

The private instructor README gives the localhost server command. With that
server running, check projector layouts, staging, the handout, and native notes:

```sh
node _instructor/lectures/lecture-14-uncertainty/verify-presentation.mjs
```

The focused check visits all 30 slides and 11 reveal steps at both 1440×900 and
1280×720, for 82 observed states. It retains the 32-pixel slide body font. It
also opens the native notes window and checks bold text, lists, math styling,
and scroll access to the final note. Speaker-note bytes remain private.

The shared checker below generates the 30-page review PDF in `_build/review/`.
It currently reports five false horizontal overflows because its fitter measures
descendants of KaTeX's clipped, nonvisual MathML. The visible KaTeX HTML fits.
The focused check tests visible geometry while preserving accessible MathML and
copies the shared report without modification. Both reports record the checked
export hashes; this limitation is not reported as a passing shared check.

```sh
node tools/myst-reveal/src/check.mjs 09-lectures/myst-source/lecture-14-uncertainty/_build/reveal/decks.json --out 09-lectures/myst-source/lecture-14-uncertainty/_build/review
```

The shared command currently exits with a failure status for those five reports.
Do not interpret that status as a numerical or scientific verdict. The scoped
visible-geometry and notes checks are separate evidence.

## Scientific limits preserved in the adaptation

- Density transformations need the stated invertibility and dimensionality;
  a many-to-one map requires all inverse branches.
- A covariance transpose is not an inverse physical map.
- First-order propagation is exact for affine maps; curvature corrections retain
  higher-order error. Monte Carlo has finite-sample and rare-event limits.
- The shared-offset floor concerns the predictive variance of the cohort mean
  while shared-parameter uncertainty stays fixed. Informative data can constrain
  an identifiable shared parameter. Single-object scatter does not shrink with
  the number of other objects.

No GitHub CI, commit, push, or publication is part of the local build command.
Private-repository CI requires explicit permission for the repository and run.

## Adding another paired lecture deck

Group two consecutive guide lectures in one deck, and identify both guide
numbers in its heading on `09-lectures/jaxstro-sciml-guide.md`. Add links to the
student slides and worked handout there. Preserve the separate PDF handouts and
their numbering. Use the same MyST authoring workflow and keep the reference
PDF and detailed presenter notes in the private instructor repository.
