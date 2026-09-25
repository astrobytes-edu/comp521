# Lecture slide workflow

New and substantially revised COMP 521 lecture slide decks use **Quarto Reveal**.
Lecture 10 is the working example. Existing MyST projector lectures remain
available until each lecture is revised; this convention does not change their
content or links.

## Source, output, and site page

- Write the deck in `09-lectures/reveal-source/<lecture>.qmd`. Use the shared
  `assets/theme/slides/theme.scss` relative to that source directory. Keep code
  cells, speaker notes, alt text, and citations in the source.
- Set `embed-resources: true` under `format.revealjs`. Run
  `python3 scripts/build_reveal_slides.py <lecture>.qmd` from the repository
  root. The command executes Quarto cells, checks for local asset references,
  and writes `09-lectures/reveal/<lecture>.html`.
- Commit **both** the `.qmd` source and generated `.html`. The regular MyST build
  does not run Quarto; `myst.yml` copies `09-lectures/reveal` as a static folder.
- Keep a short MyST lecture page in the existing lecture route. Link to the deck
  at `/reveal/<lecture>.html` so MyST applies the site's `/comp521` base path.
  Use that page for the lecture summary, readings, and project connection. Do
  not duplicate the deck as MyST projector slides.

Quarto must render from `reveal-source`; sending output to another directory
can leave Reveal asset links unresolved. The build script renders there first
and copies the self-contained HTML afterward. It also assigns stable IDs to
executed cells so repeat builds produce the same file.

## Check before release

1. Run `python3 scripts/build_reveal_slides.py <lecture>.qmd` and check the
   executed cells for errors.
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
