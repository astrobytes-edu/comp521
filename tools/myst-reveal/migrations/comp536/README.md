## Historical ODE review record · October 5, 2026

This record describes the October 5 review and its superseded Quarto draft.
The current COMP 521 lecture uses MyST → Reveal, with source in
`09-lectures/myst-source/lecture-11-odes/` and the stable student page
`09-lectures/lecture-11-odes.md`. Follow `AGENTS.md` and
`tools/myst-reveal/AUTHORING.md` for authoring. The migration here remains
review source and historical context, outside the production ODE export.

The RK2 step and marcher have been removed from the migration notebook.
Oscillator comparison data now come from its analytically derived linear map;
they are reference diagnostics, not general RK implementations. Student prompts
replace the completed code. Current course readings and the independent-variable-first
callable convention govern the revision. Original source-preservation counts
below describe the initial import and are not a check for this intentional revision.

At the time of this review, the revised lecture and readings were local
artifacts awaiting separate authorization for commit, push, and publication.
The production allowlist excludes this MyST ODE migration. The stable Block 4
page now links the current MyST lecture.

Recorded verification for the October 5 revision: all 48 executable numerical-reading cells passed,
including the new Richardson example. The backward Euler check includes a
nonautonomous problem that distinguishes derivative argument order. All 12
remaining ODE notebook code cells executed. The corrected migration passed the
presentation checker across 73 slides with zero errors or warnings.

The superseded Quarto draft contained 53 slides, including optional sections after the
exit questions. Its two reference calculations executed, and all slides passed a
1440-by-900 offline Chrome check with zero network requests, runtime errors,
clipped containers, missing image descriptions, or unconverted math. Native
MathML removed the dynamic math CDN dependency. Sampled visual review covered
RK4 stages, Richardson, and both diagnostic plots. The strict course build and
public/site boundary checks passed; the stable route then linked the matching export.
The textbook comparison remained pending. These are the recorded October 5
outcomes, not fresh verification of the current lecture.

# COMP 536 lecture migrations for COMP 521

Local review drafts, 2026-09-28. Anna approved migration of all three decks, a Software Engineering editing pass without reducing context, and ODE O1–O7 / Statistical Thinking S1–S6. Nothing has been committed, pushed, assigned, or published by this migration.

| Deck | Original sections | Reveal slides including detail | Local preview |
|---|---:|---:|---|
| Software Engineering for Scientists | 32 | 49 | [Slides](http://127.0.0.1:4173/comp521/reveal/migrations/software-engineering.html) |
| ODE Methods | 49 | 68 | [Slides](http://127.0.0.1:4173/comp521/reveal/migrations/ode-methods.html) |
| Statistical Thinking Foundations | 34 | 45 | [Slides](http://127.0.0.1:4173/comp521/reveal/migrations/statistical-thinking.html) |

The MyST Markdown files are the editable slide sources. The two notebooks preserve all 19 original computational cells. Dense explanations and full source listings use vertical continuation slides; Down enters these details. Right advances across main topics. Space follows the staged presentation order. Tools starts collapsed. Each output includes a handout and local executed-source pages.

## Editorial scope and retained context

- `originals/` contains byte-preserved source snapshots. `migration-record.json` records original paths, hashes, sections, and figure provenance. The COMP 536 originals were not changed.
- Software Engineering retains the original principles and stellar examples, with a six-slide arithmetic-mean example that walks through contract, failure, hypothesis, correction, and independent checks. The original Mermaid workflow is presented as a complete text sequence; its original Mermaid source is retained.
- ODE retains the decay and oscillator examples, Euler/RK2/RK4/leapfrog equations, code, plots, exercises, and N-body project context. Approved corrections distinguish stability, convergence and geometric conservation. Imported COMP 536 project/deadline material is historical context; the COMP 521 bridge points to Project 4.
- Statistics retains the emergence, moments, uncertainty, sampling, astrophysics and ML material. Approved additions state statistical assumptions, covariance terms, moment definitions, and the distinction between isotropic directions and a radial model.
- `EDITORIAL-APPROVAL.md` contains the approved proposals. `software-engineering-edits.json` and `approved-editorial-edits.json` record editorial replacements. Subsequent layout splitting preserves the content of each block.
- Reading links retain their original COMP 536 destinations. Videos are external links rather than offline embeds. The standalone slides render without network requests; opening external readings/videos requires a connection.
- The notebooks execute at build time. These decks do not convert every imported cell into a live browser-editable Python exercise. The original incomplete exercise snippets remain intentionally incomplete for students.

## Verification

The later approved SWE revision supersedes its initial migration checks below. See [SWE-REVIEW.md](SWE-REVIEW.md) for the current 49-slide deck, sequence checks and companion reading. The original combined counts below describe the initial migration.

The final HTML hashes in `verification.json` match the checked artifacts. The combined results cover 151 slides and 271 fragment states: zero automated errors and warnings for overflow, small text, missing images, unnamed controls, local links and browser runtime errors. This is automated presentation evidence, not a complete scientific or accessibility audit. Sampled visual review included the RK4 explanation, code-to-figure comparison, code detail, and statistical definitions. Vertical navigation and the copy icon were exercised in the local browser.

The strict MyST build executed 13 ODE and 6 statistics cells. Source-preservation checks pass for all cells and eight figures. The SE example passes independent value checks, input-preservation, and empty/nonfinite rejection checks. Seven renderer tests pass, including converted scientific superscripts. Two large source PNGs produce nonfatal image-conversion warnings during the MyST build.

From `/Users/anna/Teaching/comp521/tools/myst-reveal`:

```sh
PATH=/Users/anna/Teaching/comp521/.venv/bin:$PATH MPLCONFIGDIR=/private/tmp/myst-reveal-mpl node src/build.mjs migrations/comp536 _build/html/reveal/migrations
python3 migrations/comp536/verify_migration.py
node --test test/render.test.mjs
node src/check.mjs _build/html/reveal/migrations/decks.json --out _build/migration-review
```

The build needs a Python/Jupyter environment and permission to bind a local notebook server. The browser check uses installed Chrome via Playwright. Generated HTML, source pages, handouts and provenance are in `_build/html/reveal/migrations/`. To refresh the existing local preview server's copy:

```sh
node --input-type=module -e "import fs from 'node:fs';fs.cpSync('_build/html/reveal/migrations','examples/site/_build/html/reveal/migrations',{recursive:true})"
```

Do not rerun `import_sources.py` over the edited sources: it is the one-time initial import, not the ongoing authoring workflow. Lecture delivery pacing still needs instructor selection; including every vertical detail extends the original session timings.
