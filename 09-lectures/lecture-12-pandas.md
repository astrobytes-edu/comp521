---
title: "Lecture 12 · Pandas and Exploratory Data Analysis"
subtitle: "Tables, selections, and plots, followed by your own exploration"
---

[Open the slides](/reveal/lecture-12-pandas.html) ·
[Read the worked handout](/reveal/lecture-12-pandas.handout.html).

The 30-minute introduction covers DataFrames and Series, labels and positions,
missing values, boolean selection, column arithmetic, summaries, and plots.
It applies these operations to the saved NASA exoplanet table used in
[Project 4](../08-assessments/projects/project-4.md). The handout includes the
two prediction answers.

## Install Pandas

In the course terminal, activate your existing environment and install Pandas:

```bash
conda activate comp521
conda install -c conda-forge pandas
```

Review Conda's proposed package plan before confirming. Use the existing
[course environment](../02-getting-started/02-software-setup.md), rather than
installing into base or mixing package managers. The
[Pandas installation guide](https://pandas.pydata.org/docs/getting_started/install.html)
provides the package reference.

## Create your own notebook and load the data

Download the [saved NASA CSV](/reveal/sources/project4-nasa-exoplanets.csv)
and its [provenance record](/reveal/sources/project4-nasa-exoplanets.provenance.json)
into your working folder. Start Jupyter there:

```bash
jupyter notebook
```

Create a blank Python notebook, choose your `comp521` kernel, and save it in
that folder. In your own code cell, load the table:

```python
import pandas as pd

raw = pd.read_csv('project4-nasa-exoplanets.csv', comment='#')
raw.head()
```

The saved snapshot has 437 rows and 15 columns. Inspect `raw.shape`,
`raw.dtypes`, and `raw.isna().sum()` to see what was loaded. Consult the
[NASA definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
for units and flags. No live archive query is needed.

## Experiment with the table

Choose a question about the table. Try different columns, row selections,
summaries, and plots using the lecture examples as references. Keep `raw`
unchanged and save experiment selections under new variable names. Describe
one result and one question to a neighbor. Counts describe the selected
archive rows, not exoplanet occurrence rates.

You create the notebook yourself; there is no starter notebook to download.
This is in-class exploration with no new submission. Project 4's brief
continues to define its required work.

Use [Pandas fundamentals](../04-scientific-computing/11-pandas-fundamentals.md)
for further reference. [Return to the Lecture Library](index.md).
