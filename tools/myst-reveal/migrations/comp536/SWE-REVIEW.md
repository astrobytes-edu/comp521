# SWE presentation and companion reading revision

Anna approved option A: repair staging, add commandment transitions, standardize presentation, reorder the closing, and migrate the full reading while preserving the existing COMP 521 guide.

## Changes

- Eleven numbered transition slides state the full commandment. Section transitions no longer repeat their headings. The deck has 49 slides.
- Good/bad comparison labels reveal with their associated code or quotation. Lists reveal in order; follow-up explanations and conclusions wait for preceding material. Backward navigation reverses those reveals.
- Code examples use titled, syntax-highlighted cards with copy controls. Fragment timing no longer adds decorative borders or indentation. SWE-specific styling is scoped to this deck.
- The worked example and transfer exercise precede the takeaway, reading assignment and questions.
- `02-getting-started/software-engineering-for-scientists.md` is a full companion reading, retaining all 58 original section/subsection headings and the extended examples. `reading-migration.json` records provenance and editorial replacements. The COMP 536 reproducibility contract is explicitly historical context; COMP 521 project briefs remain authoritative.
- The existing COMP 521 guide is preserved, with only a companion link added. Both readings are in Tools & Workflow. The slide links to the COMP 521 companion route.
- The exporter accepts single-slash site-root links while rejecting protocol-relative URLs. The offline checker reports these as requiring an HTTP check rather than treating them as local filesystem paths.

## Evidence

`AUTHORING.md`, “Compose a slide,” supplies the section layout and slide options. The original source's fragment pauses motivated grouping labels with the complete example. The existing COMP 521 guide's “The course workflow changes after P1” remains the course-specific requirements boundary.

Fresh checks:

- Eight renderer tests pass, including allowed course-root URLs and rejected protocol-relative URLs.
- 17 staged slides pass 131 forward/backward state checks against an explicit teaching sequence. Eleven commandment transitions and the closing order pass structural assertions.
- All 49 slides / 132 presentation states pass layout checks with zero errors. One site-route warning is resolved separately by opening the rendered companion reading in the local browser; it is not a missing standalone asset.
- The full site HTML build completes. Its log contains duplicate citation warnings from existing prototype/example bibliographies; this is not a clean strict whole-site build claim.
- Both edited MyST sources pass directive-fence checks. Original COMP 536 files and the 19 notebook computational cells remain unchanged. The SE worked-example checks pass.
- Browser inspection confirmed the transition, hidden/revealed good-test block, reading route, and rendered companion reading.

From `tools/myst-reveal`:

```sh
node --test test/render.test.mjs
node migrations/comp536/check-swe-sequence.mjs
node src/check.mjs _build/html/reveal/migrations/decks.json --deck software-engineering --out _build/swe-review-final
python3 migrations/comp536/verify_migration.py
```

From the course root, rebuild the reading with:

```sh
BASE_URL=/comp521 PATH="$PWD/.venv/bin:$PATH" tools/myst-reveal/node_modules/.bin/myst build --html
```

Local review only. No commit, push or publication. These checks validate the presentation sequence and sampled rendering, not every possible classroom delivery choice or scientific claim in the retained reading.
