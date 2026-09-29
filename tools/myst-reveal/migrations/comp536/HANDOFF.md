# SWE review and publication handoff — 2026-09-29

## Published release update — 2026-09-29

The earlier checkpoint account below is historical. Anna subsequently approved
the bounded SWE content and integration changes, then explicitly requested
commit, push, and immediate publication. Release `a07daa8` is public; Pages
[run 36647592472](https://github.com/astrobytes-edu/comp521/actions/runs/36647592472)
succeeded. The student route, full chapter, shorter guide, slides, and handout
returned HTTP 200. Public slide/handout bytes match the reviewed final artifacts.

The deck remains 49 slides with 11 commandment transitions. New predictions,
NaN-safe guards, both requested workflows, claim-based evidence, reproducibility
explanation, Git protection, and nonfinite mean tests are implemented. The
reading retains the plot-as-proof passage and adds a smooth but incorrect plot
example. The package remains tracked here. ODE/statistics are excluded from
the public slide export. See `SWE-REVIEW.md` for final checks and public URLs.

---

Anna requested this local checkpoint, a Brain capture, and a new session to review the Software Engineering slides and reading, integrate the slides with the real course site, and make both public. This checkpoint is not publication. No push was performed.

## Canonical files

- `tools/myst-reveal/migrations/comp536/software-engineering.md`: 49-slide MyST deck, including 11 commandment transitions.
- `02-getting-started/software-engineering-for-scientists.md`: full companion reading migrated from COMP 536, retaining all 58 section/subsection headings.
- `02-getting-started/04-software-engineering-guide.md`: existing COMP 521 guide, preserved with a companion link.
- `myst.yml`: companion reading added to Tools & Workflow.
- `tools/myst-reveal/migrations/comp536/SWE-REVIEW.md`: prior implementation/verification record.
- `tools/myst-reveal/migrations/comp536/EDITORIAL-APPROVAL.md`: earlier ODE/statistics approvals; those migrations are retained but are not the next publication target.

## Decisions and approvals

Anna confirmed that `tools/myst-reveal/` should remain tracked inside COMP 521 for the pilot. Extracting it into its own MyST plugin package is deferred; do not move it or create a separate repository during this publication task.

Use MyST authoring and the Reveal exporter, not Quarto. Preserve context and substantive content. Keep the commandments and their transitions. Anna explicitly rejected using the count of 40 sparse slides as a pacing objection. Better short examples throughout the commandments are the preferred direction; the complete arithmetic-mean walkthrough can remain near the end.

Anna approved the previous reveal repairs, transitions, code-card formatting, closing-order change, and companion-reading migration. Those are implemented. She subsequently asked to remove the COMP 536 explanatory statement under the slides' contract example; it was removed. Do not restore it or add repeated disclaimers.

The most recent adversarial suggestions are NOT implemented or separately approved as exact content edits: improve examples throughout, distinguish purposeful exploratory coding from uncontrolled changes, qualify absolute wording where necessary, fix the NaN range-guard example, align the closing workflow with implementation/checking, and connect evidence types to claims rather than command names. Follow the repository approval rule for substantive proposed edits. Do not infer blanket authorization for every brainstormed example.

## Verification boundaries

At closeout, eight renderer tests, 131 forward/backward states on 17 slides, source/asset preservation checks, and the SE mean-example checks passed again. No fresh full visual sweep was performed during closeout.

Previous checks: eight renderer tests; 17 staged slides with 131 forward/backward states; 49-slide layout check with zero errors and one site-route warning independently checked in the local browser. The final removal of the COMP 536 statement was rebuilt and checked for absence but did not receive a new full visual sweep. Reverify current artifacts rather than treating reports as release qualification.

The full MyST site built locally, with duplicate citation warnings from prototype bibliographies. Assess and resolve production-discovery/build issues before publishing. Rendered outputs and local review screenshots are ignored and must be rebuilt. Original source snapshots and assets are committed; dependencies and caches are not.

## Next session

1. Inspect current checkout, course instructions, public/private boundary, source and deployment workflow.
2. Review SWE content and reading together; preserve the existing shorter guide. Visually and interactively inspect initial/revealed/backward states, transitions, code, mobile/projector layouts, handout, reading navigation and links.
3. Propose bounded content corrections/examples for Anna's approval; then implement approved changes.
4. Integrate the deck into production build/deployment, give it a stable MyST student route, and link it from the actual course navigation/lecture listing. Copying HTML into the local prototype server is not production integration.
5. Verify a clean reproducible build, source/link correctness, fragment sequencing and visual quality. Ensure instructor-only material, prototype demos and local caches are not accidentally exposed.
6. Commit final approved changes, publish within Anna's authorization, and verify the actual public slide and reading URLs. Report deployed evidence, not only local success. Check the current request and approval boundary before the final release.

Build/check from `tools/myst-reveal`:

```sh
npm ci
PATH=/Users/anna/Teaching/comp521/.venv/bin:$PATH MPLCONFIGDIR=/private/tmp/myst-reveal-mpl node src/build.mjs migrations/comp536 _build/html/reveal/migrations
node --test test/render.test.mjs
node migrations/comp536/check-swe-sequence.mjs
node src/check.mjs _build/html/reveal/migrations/decks.json --deck software-engineering --out _build/swe-review-final
python3 migrations/comp536/verify_migration.py
```

Course build from root:

```sh
BASE_URL=/comp521 PATH="$PWD/.venv/bin:$PATH" tools/myst-reveal/node_modules/.bin/myst build --html
```

Do not rerun the one-time import script over edited sources. Do not publish the ODE/statistics migrations as a side effect of SWE integration. Review source examples with explicit placeholders as teaching snippets, not production implementations.
