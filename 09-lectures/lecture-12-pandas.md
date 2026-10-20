---
title: "Lecture 12 · Pandas and Exploratory Data Analysis"
subtitle: "Tables, selections, and plots, followed by hands-on exploration"
---

[Open the slides](/reveal/lecture-12-pandas.html) ·
[Read the worked handout](/reveal/lecture-12-pandas.handout.html) ·
[Read the executed examples and practice tasks](/reveal/sources/pandas-examples.html#hands-on).

The 30-minute introduction covers DataFrames and Series, labels and positions,
missing values, boolean selection, column arithmetic, summaries, and plots.
It applies those operations to the saved NASA exoplanet table used in
[Project 4](../08-assessments/projects/project-4.md). Two short prediction
questions include answers in the worked handout.

## Work with the notebook

Download these three files into the same folder:

- [Pandas examples and hands-on notebook](/reveal/sources/pandas-examples.ipynb)
- [Saved NASA CSV](/reveal/sources/project4-nasa-exoplanets.csv)
- [CSV provenance record](/reveal/sources/project4-nasa-exoplanets.provenance.json)

Start Jupyter in that folder using your course Python environment with NumPy,
Pandas, and Matplotlib. Open the notebook and run the reference cells in order,
then work in **Hands-on exploration**. Running inside a course repository
checkout also works. No live archive request is needed.

## Hands-on exploration

Allow about 45 minutes after the introduction. Work with a neighbor if useful.
Each task starts with runnable code that you can change and inspect.

1. Inspect the snapshot: shape, preview, types, and missing values.
2. Add a calculated column and select rows and columns from the synthetic table.
3. Change a NASA practice selection and compare the retained counts.
4. Compare summaries and inspect the largest radii and their source references.
5. Change histogram bins, make a paired scatter plot, and explain one result.

Keep `raw` and the supplied P4 selection `planets` unchanged; use `practice`
for experiments. These are ungraded in-class tasks with no new submission.
The Project 4 brief continues to set its own required work.

Use [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md)
for further reference. [Return to the Lecture Library](index.md).
