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
