# Lecture 12: Pandas and exploratory data analysis

Student MyST Reveal source: 24 slides, two prediction pauses, and 30 minutes of
timing targets. Actual classroom delivery has not been timed. Five runnable
notebook tasks support about 45 minutes of subsequent exploration. They add no
assessment or Project 4 deliverable.

`slides.md` owns the public lecture; `pandas-examples.ipynb` owns the executed
examples and practice starters. Instructor speaker notes and response guidance
are maintained only in the separate private instructor repository.

Follow `tools/myst-reveal/AUTHORING.md` and the Lecture 11 MyST source pattern.
From the repository root, rebuild and verify the six student artifacts:

```sh
.venv/bin/python -B scripts/build_pandas_slides.py
```

The verifier executes the notebook in the course tree and again in an isolated
folder with only the student CSV/provenance downloads. It checks synthetic
arithmetic, row pairing, figures, task cells, data hashes, and exact agreement
with the published P4 selection. `_build/verification.json` stores the result.

The builder rejects private notes/paths and unresolved local references before
copying the deck, worked handout, notebook reading, notebook, CSV, and provenance
record to `09-lectures/reveal`. Only these selected exports are public. The
lecture page is the stable student route; no browser Python runtime is added.

Review the deck at projector size, both prediction reveal sequences, the worked
handout at reading width, and the notebook link before publication. P4 counts
describe the saved selected archive table, not population occurrence rates.
