# Lecture 12: Pandas and exploratory data analysis

The MyST lecture has 24 slides, two prediction pauses, and 30 minutes of timing
targets. Actual delivery has not been timed. Students install Pandas in their
comp521 environment, create their own notebook, and explore the saved NASA CSV.
No student starter notebook or prepared task sheet is distributed.

`slides.md` owns the public lecture. `pandas-examples.ipynb` is the internal
calculation source for executed examples and six figures, not a student
handout. All 24 slides have private embedded presenter notes in the separate
instructor repository, including answers and likely student responses.

Follow `tools/myst-reveal/AUTHORING.md` and the Lecture 11 export pattern.
From the course root:

```sh
.venv/bin/python -B scripts/build_pandas_slides.py
```

The verifier executes 32 calculation cells, checks arithmetic, paired rows,
uncertainty arrays, source hashes, and equality to the P4 selection. It also
checks loading the CSV in a fresh blank notebook outside the repository.
The builder strips calculation-source links, rejects private notes/paths and
unresolved references, and publishes only the deck, worked handout, CSV, and
provenance record. It removes the two retired public notebook artifacts.
Generated calculation readings remain inside the ignored build workspace.

The lecture page supplies the Conda setup and data download. Check slide 23,
both prediction reveals, and the worked handout at reading width. Private
verification requires nonempty embedded presenter notes on every slide.
