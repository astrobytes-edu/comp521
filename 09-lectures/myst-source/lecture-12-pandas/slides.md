---
title: "Lecture 12 · Pandas and Exploratory Data Analysis"
subtitle: "COMP 521 · Tables, selections, and scientific plots"
author: Anna Rosen
---

(pandas-title)=

## Pandas and exploratory data analysis

```{slide-options}
{"layout":"title","class":"pandas-deck pandas-title","eyebrow":"COMP 521 · 30-minute introduction","timing":15}
```

:::{slide-element}
:class: pandas-subtitle
From labelled observations to inspectable evidence
:::

:::{slide-element}
:class: pandas-byline
Anna Rosen · San Diego State University
:::


(pandas-introduction)=
## What is Pandas?

```{slide-options}
{"class":"pandas-deck","eyebrow":"A Python library for labelled data","timing":60}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 28

::::::{slide-column}
### What it provides

- **DataFrame:** a table with row and column labels.
- **Series:** one labelled sequence, such as a column.
- Tools to read files, select records, handle missing values, and summarize data.
::::::

::::::{slide-column}
### Where it fits

NumPy computes with arrays. Pandas adds table labels and column types. Matplotlib draws the plots.

```{slide-code} python
:title: The usual import
import pandas as pd
```

`pd` is an alias for the library, not a dataset.
::::::
::::::::


(pandas-containers)=
## Compare the data containers

```{slide-options}
{"class":"pandas-deck","eyebrow":"Choose a representation for the task","timing":60}
```

| Container | How you address data | What it organizes |
|:--|:--|:--|
| Python list | Positions | A sequence of objects |
| Python dictionary | Keys | Key–value associations |
| NumPy array | Positions in a shape | An array with one dtype |
| Pandas Series | Index labels or positions | One labelled sequence with one dtype |
| Pandas DataFrame | Row/column labels or positions | A table with one dtype per column |

A dictionary can supply a table's columns. A DataFrame adds a shared row index and table operations; each column is a Series.


(pandas-create)=
## A dictionary of columns becomes a DataFrame

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Synthetic teaching data","timing":90}
```

::::::::{slide-columns}
:ratio: 1.2 1
:gap: 28

::::::{slide-column}
```{slide-code-example} pandas-examples.ipynb#toy-columns
:title: Dictionary keys name the columns
:view: code
```
::::::

::::::{slide-column}
```{slide-code-example} pandas-examples.ipynb#toy-table
:title: Give the table its row labels
:view: code
```

Each list supplies one column. Entries at the same position form one row.
::::::
::::::::

These equal-length lists describe five synthetic exposures. Signal uses arbitrary units; exposure uses seconds.


(pandas-table)=
## Inspect the records

```{slide-options}
{"class":"pandas-deck","eyebrow":"What the representation preserves","timing":90}
```

```{slide-code-example} pandas-examples.ipynb#toy-table
:title: Executed table
:view: output
```

Sample D lacks an exposure. Sample E carries a flag. Keep both facts visible.

`toy.shape` is `(5, 4)`. Inspect `toy.index`, `toy.columns`, and `toy.dtypes`. Types do not supply units.


(pandas-series)=
## One column is a Series

```{slide-options}
{"class":"pandas-deck","eyebrow":"The brackets specify the result","timing":60}
```

```{slide-code-example} pandas-examples.ipynb#series-frame
:title: A column and a subtable
:view: code
```

| Expression | Result |
|:--|:--|
| `toy['signal']` | A labelled Series |
| `toy[['sample', 'signal']]` | A two-column DataFrame |

The inner list names the columns to keep.


(pandas-address)=
## Labels and positions are different

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Addressing a record","timing":75}
```

```{slide-code-example} pandas-examples.ipynb#labels-positions
:title: .loc uses labels; .iloc uses positions
:view: both
```

The first row's label is `r10`, while its position is `0`.


(pandas-arithmetic)=
## Columns support row-wise arithmetic

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Keep quantities paired","timing":75}
```

```{slide-code-example} pandas-examples.ipynb#column-arithmetic
:title: Signal divided by its own exposure
:view: both
```

Pandas matches row labels before dividing. These columns come from the same table. The result uses arbitrary signal units per second.


(pandas-missing)=
## Missing is a state, not a measured zero

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Preserve missingness","timing":75}
```

`isna()` marks missing cells `True`. `.sum()` counts those marks down each column: `True` contributes 1; `False` contributes 0.

```{slide-code-example} pandas-examples.ipynb#missing-values
:title: Find and count missing entries
:view: both
```

D's rate is missing because its exposure is unknown. Replacing the exposure with zero would invent a value and change the calculation.


(pandas-mask)=
## A comparison gives one decision per row

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"A boolean mask","timing":75}
```

```{slide-code-example} pandas-examples.ipynb#toy-mask
:title: A named condition
:view: both
```

`.eq('ok')` compares each value with `'ok'`. The result is a boolean Series with the table's row labels. `True` means keep that row for this rule.

Combine conditions with `&` (both), `|` (either), and `~` (reverse). Put comparisons in parentheses.


(pandas-loc)=
## Read `.loc[rows, columns]`

```{slide-options}
{"class":"pandas-deck","eyebrow":"Selection preserves the rule","timing":60}
```

```{slide-code} python
:title: Select records and variables
toy.loc[is_ok, ['sample', 'exposure_s', 'signal']]
```

- Before the comma: a row label, list of labels, or mask.
- After the comma: the columns to retain.
- Build the mask from the same table's labelled columns.


(pandas-check)=
## Explain the selection before running it

```{slide-options}
{"class":"pandas-deck","eyebrow":"In-class reasoning","timing":120}
```

`is_ok` marks the rows with an “ok” quality flag. Compare these two selections:

```{slide-code} python
:title: Two row-selection rules
toy.loc[is_ok]
toy.loc[is_ok & toy['exposure_s'].notna()]
```

::::{fragment}
:index: 0

:::{slide-question}
Which row labels will each expression retain? Explain the difference.
:::
::::

:::{slide-answer}
:index: 1
The first keeps `r10`–`r13`. The second keeps `r10`–`r12`. Selection does not renumber labels or fill missing values.
:::


(pandas-summary)=
## Start EDA with counts and ranges

```{slide-options}
{"class":"pandas-deck","eyebrow":"Describe what is available","timing":90}
```

```{slide-code-example} pandas-examples.ipynb#toy-summary
:title: Descriptive summaries from the same table
:view: both
```

`count` reports available values in each column. `50%` is the median. Different columns can summarize different numbers of observations.


(pandas-denominator)=
## The denominator matters

```{slide-options}
{"class":"pandas-deck","eyebrow":"Missing values change the available count","timing":90}
```

The four known exposures are 1, 2, 2.5, and 4 seconds.

::::{fragment}
:index: 0

:::{slide-question}
Is their mean $9.5/4$ or $9.5/5$? What would the other denominator imply?
:::
::::

:::{slide-answer}
:index: 1
$$\bar t=\frac{1+2+2.5+4}{4}=2.375\ {\rm s}.$$

Dividing by five would effectively count the missing exposure as zero. The available-value mean does not establish that missingness is harmless.
:::


(pandas-distribution)=
## Plot a distribution, not just one number

```{slide-options}
{"layout":"figure","class":"pandas-deck pandas-wide","eyebrow":"EDA · one variable","timing":60}
```

```{slide-figure} pandas-examples.ipynb#toy-histogram
:alt: Histogram of five synthetic signals. Four values lie between zero and five, one near eighteen. The mean is six and the median three.
:caption: A bin is an interval of signal values. Its height counts stored values in that interval.
```


(pandas-pairs)=
## A relationship requires paired records

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"EDA · two variables","timing":90}
```

`notna()` checks each cell. `.all(axis=1)` checks across columns within one row; both fields must be known.

```{slide-code-example} pandas-examples.ipynb#paired-rows
:title: Select rows with both variables
:view: both
```

For this plot, retain rows with exposure **and** signal. Do not remove missing values separately from the two columns and then pair positions.


(pandas-source)=
## The CSV has a source contract

```{slide-options}
{"class":"pandas-deck","eyebrow":"One published parameter set per planet","timing":75}
```

The saved NASA **Planetary Systems (`ps`)** query retains one default published parameter set per planet, with names and source references.

```{slide-code} python
:title: Read your saved Project 4 file
raw = pd.read_csv(
    'project4-nasa-exoplanets.csv',
    comment='#')
```

CSV is a text format with a header and comma-separated records. `read_csv` returns a DataFrame. Blank fields usually become missing values; check inferred types.

Save the CSV beside your own notebook. Keep the query and retrieval date.


(pandas-csv)=
## Inspect what was read

```{slide-options}
{"class":"pandas-deck","eyebrow":"Source before selection","timing":45}
```

```{slide-code-example} pandas-examples.ipynb#read-csv
:title: The saved snapshot
:view: output
```

`raw.shape` gives the dimensions. `raw.head(4)` previews the four rows shown here; `raw.head()` defaults to five. Inspect column types with `raw.dtypes`.

This snapshot has 437 rows and 15 columns. A later live query may differ.


(pandas-nasa-selection)=
## Apply the rule and report the counts

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Make selection reproducible","timing":105}
```

```{slide-code-example} pandas-examples.ipynb#nasa-selection
:title: Preserve raw; select planets
:view: both
```

The Project 4 brief supplies the comparison rule: finite central estimates, the mass window, signed uncertainty offsets, and positive lower endpoints.

This snapshot retains 371 of 437 rows. Failed conditions can overlap; their excluded counts should not be added independently.


(pandas-nasa-hist)=
## Explore one variable

```{slide-options}
{"layout":"figure","class":"pandas-deck pandas-wide","eyebrow":"EDA · selected radii","timing":45}
```

```{slide-figure} pandas-examples.ipynb#nasa-histogram
:alt: Histogram of radii in Earth units for the 371 selected NASA rows, with counts per equal-width bin.
:caption: The shape depends on the selected table, available measurements, and binning.
```


(pandas-nasa-bars)=
## Read the relationship with its uncertainties

```{slide-options}
{"layout":"figure","class":"pandas-deck pandas-wide","eyebrow":"An estimate includes precision information","timing":90}
```

```{slide-figure} pandas-examples.ipynb#nasa-errorbars
:alt: Logarithmic NASA mass–radius plot with asymmetric uncertainty bars, Earth marked, and TRAPPIST-1 e and Kepler-51 b highlighted.
:caption: The supplied offsets follow their source studies; a common confidence level is not established here.
```


(pandas-errors)=
## Reference recipe: preserve both uncertainties

```{slide-options}
{"layout":"code","class":"pandas-deck","eyebrow":"Bridge Pandas to NumPy and Matplotlib","timing":90}
```

::::::::{slide-columns}
:ratio: 1.3 1
:gap: 28

::::::{slide-column}
```{slide-code-example} pandas-examples.ipynb#error-arrays
:title: Lower row, then upper row
:view: code
```
::::::

::::::{slide-column}
### Two rows, $N$ planets

$$\begin{pmatrix}
\text{lower lengths}\\
\text{upper lengths}
\end{pmatrix}$$

For Kepler-51 b, one column is $\begin{pmatrix}0.8\\1.5\end{pmatrix}$ Earth masses.

`.to_numpy()` extracts the values. `np.vstack` stacks them as rows.
::::::
::::::::

One column per selected planet. Every array comes from the same selected rows in the same order.


(pandas-launch)=
## Your turn: create your own notebook

```{slide-options}
{"class":"pandas-deck","eyebrow":"Install, load, and explore","timing":135}
```

```{slide-code} bash
:title: In your course terminal
conda activate comp521
conda install -c conda-forge pandas
```

1. Create a blank Jupyter notebook beside the saved NASA CSV.
2. Import Pandas and load the CSV with `pd.read_csv`.
3. Inspect the table, choose columns, and try selections, summaries, and plots.
4. Discuss one result and one question with a neighbor.

[Download the CSV and read the setup instructions](https://astrobytes-edu.github.io/comp521/lecture-12-pandas/). This is class exploration, with no new submission.

(pandas-references)=
## References for your own notebook

```{slide-options}
{"class":"pandas-deck","eyebrow":"Inspect the source","timing":30}
```

- [Pandas table fundamentals](https://pandas.pydata.org/docs/user_guide/dsintro.html)
- [CSV reading](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html), [`.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html), and [descriptive summaries](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
- [Matplotlib error bars](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html)
- [NASA column definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- [Install Pandas](https://pandas.pydata.org/docs/getting_started/install.html) and [download the class CSV](https://astrobytes-edu.github.io/comp521/lecture-12-pandas/)
- [Project 4](https://astrobytes-edu.github.io/comp521/project-4/)
