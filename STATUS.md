# COMP 521 — status

next: Complete the separate Project 1 fresh-account release gate and the ODE reading textbook comparison.
blocker: ODE reading textbook comparison remains pending. Project 1 fresh-account verification remains open.
due: Not scheduled

## Current focus

COMP 521 is an active Fall 2026 MyST course site. The public course repository
owns student-facing materials; `_instructor/` remains a separate private
workspace. The Brain reads this status file for portfolio planning, but course
sessions report discrete outcomes through `brain "comp521: ..."` rather than
editing Brain pages directly.

## Block 6 release preparation: 2026-11-05

The guide now has its own Block 6, with separate PDF handouts and a full draft.
The guide page links a 30-slide MyST Reveal deck and worked handout covering
guide Lectures 1–2. Future guide decks will group two lectures per presentation.
The reference PDF and detailed presenter notes remain in the private instructor
repository.

Local review covered 82 projector states and three native speaker-note cases.
The focused visible-layout checks passed; the shared checker retains five
reports caused by clipped, nonvisual KaTeX MathML. The numerical figures and
executed notebook were checked against the stated analytic teaching examples.
The ODE reading verifier passed all 48 executable cells. Publication and live
verification of this release remain pending.

## Verified Project 3 publication — 2026-10-01

Release `b290bfc` publishes the science background, interactive Kepler and
stellar-radiation figures, and both captioned orbital films. Pages
[run 36929094851](https://github.com/astrobytes-edu/comp521/actions/runs/36929094851)
succeeded. The independent review and final film inspection corrected the
circular scene's heading to state constant speed.

The [public reading](https://astrobytes-edu.github.io/comp521/project-3-science-background/)
and eight other course/slide routes returned HTTP 200. All 74 media, module,
and bundled math files matched their reviewed source hashes. Both films
returned HTTP 206 for seeking. Instructor, prototype, and unselected
ODE/statistics slide paths returned HTTP 404.

All 10 geometry/radiation tests and the final media/publication checks passed.
Two unchanged legacy lecture-widget tests still expect the removed ND Array
Evidence Check or its link; the assessment was not restored.

## Release boundary

Do not mark the course or Project 1 release-ready until the real invitation,
acceptance, clone, local README edit, commit, push, and visible remote commit have
been observed with a fresh student account.


## Verified ODE lecture publication: 2026-10-08

Release `b4c64a4` publishes the independently reviewed MyST ODE slides and
worked handout: 40 main slides and four optional references. The rejected
Quarto draft was removed from the course workspace. Spring illustrations and
first-use parameter definitions are included; instructor notes are excluded.
Pages [run 37831821024](https://github.com/astrobytes-edu/comp521/actions/runs/37831821024)
succeeded. The live slides and handout returned HTTP 200 and matched the
reviewed release hashes; the lecture page links both. This release does not
include the separate locally edited readings or claim a textbook comparison.

Slide 27 phase-diagram and conserved-energy clarification published as
`6578132`; Pages run `37833234986` passed and live exports match release hashes.

Euler/RK2/RK4 phase comparisons and the symplectic leapfrog introduction
published as `868ecea`; Pages run `37842712196` passed and live exports
match the checked release. The deck remains 40 main plus four optional slides.

## ODE comparison figure visibility — 2026-10-08

Release `c104593` publishes logarithmic energy and phase error magnitudes, retains the signed RK4 energy detail, and adds an equally scaled RK4 phase-plane endpoint zoom. The original numerical experiments and frozen reference checks are unchanged. Pages run `37845381426` succeeded; public slides and handout returned HTTP 200 and exactly matched local exports. Eighteen affected-view observations (including the live slide) had no clipping, missing images, or math errors. The narrow student handout also passed.

## ODE final plot visibility release: 2026-10-08

Release `48e2927` publishes faint gray Euler comparison curves, prominent teal
RK2 and purple RK4 curves, tighter equal phase-plane limits, distinct endpoint
markers, and endpoint zooms. The preceding decay and error-axis improvements
are included. Numerical experiments remain unchanged; all 33 executable code
cells and frozen numerical reference checks passed. Six affected projector
views at 1280 by 720 and the student handout had no clipping, missing images,
or math errors. The deck remains 40 main slides plus four optional references.
Pages run `37849272594` succeeded; live slides and handout returned HTTP 200
and matched the checked exports exactly.


## Pandas lecture release: 2026-10-20

The student release contains 24 MyST slides with 30 minutes of timing targets,
two prediction questions with worked answers, and five runnable notebook tasks
for subsequent class exploration. Instructor response notes remain private.
The notebook passes fresh execution in the course tree and an isolated student
download folder: 37 code cells, seven figures, and exact agreement with the
published P4 selection (437 input, 371 selected). All 28 projector states,
notebook links, and handout reading widths pass. Timing remains a planned
allocation rather than a measured classroom delivery. Deployment status is
recorded by the release's GitHub Pages workflow.


## Pandas delivery correction: 2026-10-22

Students install Pandas in comp521, create their own notebook, load the saved
exoplanet CSV, and choose experiments. The supplied student notebook and
prepared-task downloads are retired. The lecture remains 24 slides with
30 minutes of timing targets; all 24 instructor slides have embedded native
presenter notes. Calculation checks cover 32 cells and six figures, and the
CSV load is tested in a separate fresh kernel. Public source links and the
Block 4 overview reflect the create-your-own-notebook workflow.
