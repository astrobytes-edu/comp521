# COMP 521 — status

next: Complete the separate Project 1 fresh-account release gate.
blocker: Project 1 fresh-account verification remains open. SWE title slide and lecture Blocks 3–4 are publicly verified as of 2026-09-30.
due: Not scheduled

## Current focus

COMP 521 is an active Fall 2026 MyST course site. The public course repository
owns student-facing materials; `_instructor/` remains a separate private
workspace. The Brain reads this status file for portfolio planning, but course
sessions report discrete outcomes through `brain "comp521: ..."` rather than
editing Brain pages directly.

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
