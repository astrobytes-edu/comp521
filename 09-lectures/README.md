# Lecture slide workflow

**All lecture authoring and revisions use MyST → Reveal through
`tools/myst-reveal/`. Do not use Quarto.** Follow `tools/myst-reveal/AUTHORING.md` and Lecture 11's
source, notebook figures, and staged explanations. Teach the subject from its
core concepts; use the course project as an application.

The Software Engineering pilot uses **MyST → Reveal** from the tracked
`tools/myst-reveal/` package. Keep the canonical source in
`tools/myst-reveal/migrations/comp536/software-engineering.md`; do not reimport
the COMP 536 source over it. The package remains here until Anna extracts it.

Lecture 10 retains its existing Quarto export as a historical artifact. Any
revision must use the MyST plug-in. Existing MyST projector lectures
remain available until individually revised.

## Software Engineering production build

The student route is `software-engineering.md`. It links the slides, handout,
full companion reading, and preserved shorter COMP 521 guide. Production
installs the package lock and exports only this deck. ODE/statistics migrations,
prototype demos, exporter manifests, and local review outputs stay outside the
upload artifact.

From the repository root:

```sh
npm ci --prefix tools/myst-reveal
BASE_URL=/comp521 PATH="$PWD/.venv/bin:$PATH" tools/myst-reveal/node_modules/.bin/myst build --html --execute
BASE_URL=/comp521 PATH="$PWD/.venv/bin:$PATH" tools/myst-reveal/node_modules/.bin/myst build --html --execute
PATH="$PWD/.venv/bin:$PATH" node tools/myst-reveal/src/build.mjs tools/myst-reveal/migrations/comp536 tools/myst-reveal/_build/production --deck software-engineering
mkdir -p _build/html/reveal
cp tools/myst-reveal/_build/production/software-engineering.html _build/html/reveal/
cp tools/myst-reveal/_build/production/software-engineering.handout.html _build/html/reveal/
python3 scripts/check_public_boundary.py --site
```

The second course render incorporates newly executed outputs, matching the
deployment workflow. Use `tools/myst-reveal/AUTHORING.md` for the authoring
contract and `.github/workflows/deploy.yml` for the full runtime/media build.
After an authorized push, verify the Pages job and the actual student, reading,
slide, and handout URLs.

## ODE lecture production export

Lecture 11 uses the reviewed MyST source in
`09-lectures/myst-source/lecture-11-odes/`. The rejected Quarto ODE draft has
been removed. This deck contains 40 main slides plus four optional references.
Instructor speaker notes are excluded from both the public source and export.

```sh
PATH="$PWD/.venv/bin:$PATH" python3 scripts/build_ode_slides.py
```

The script executes the figure notebook through the existing MyST build,
rejects instructor notes and unresolved local assets, and writes the
self-contained deck and worked handout to `09-lectures/reveal/`. MyST copies
this static directory into the course site. The stable page is
`block-04-odes.md`; its links use `/reveal/lecture-11-odes.html` and
`/reveal/lecture-11-odes.handout.html` so the course base path is applied.
The build omits undeployed notebook companion links.

## Historical Lecture 10 artifacts

The source in `09-lectures/reveal-source/` records the provenance of Lecture 10's
published export. Preserve it as historical input. An approved revision must
move the lecture to the MyST plug-in workflow above. Keep the existing MyST
lecture page as the student route and link its deck at `/reveal/<lecture>.html`.

## Check before release

1. Build the MyST deck with the course Python environment, using the owning
   deck's README and `tools/myst-reveal/AUTHORING.md`. Check executed notebook
   cells for errors.
2. Inspect the deck in a browser at a projector-sized viewport. Check text,
   code, figures, math, slide overflow, keyboard navigation, and speaker notes
   where used.
3. Run `BASE_URL=/comp521 myst build --html --execute`. Confirm the built
   lecture page links to `/comp521/reveal/<lecture>.html` and that the static
   HTML is present in `_build/html/reveal/`.
4. After an authorized push, confirm the Pages deployment succeeds and open
   both the published lecture page and deck. A successful local render alone
   does not establish publication.

Use the lesson's learning goals and project context to choose examples and
pacing. Put instructor-only solutions and planning in `_instructor/`, never in
the public deck or its static assets.
