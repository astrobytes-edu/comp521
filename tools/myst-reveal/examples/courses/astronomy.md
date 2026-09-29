---
title: Reading a synthetic light curve
subtitle: Astronomy · Authoring example
---
(astro-start)=
## Reading a synthetic light curve

```{slide-options}
{"layout":"title", "eyebrow":"Astronomy", "takeaway":"Separate what the plot shows from what the data can establish."}
```

A presentation demonstration using synthetic values.

## Begin with the observable

```{slide-options}
{"layout":"figure"}
```

```{slide-figure} analysis.ipynb#sample-figure
:alt: A synthetic relative-flux curve oscillates from 0.9 to 1.1 over four cycles in arbitrary time units.
:caption: Synthetic demonstration data; not an observation or physical stellar model.
[{"x":15,"y":45,"text":"Read the vertical axis before interpreting the curve.","step":0}]
```

## Predict a repeated value

::::{slide-question}
:title: Predict
At which displayed times does this synthetic curve return to its maximum?

:::{slide-answer}
:title: Reveal
At $t=0,1,2,3,4$ in the example's arbitrary time units. That spacing was chosen when generating the data.
:::
::::

## Inspect two linked views

```{slide-linked-plot} analysis.ipynb#plot-data
:title: Synthetic flux and offset from unity
```

Move the sample cursor. Both panels identify the same sample. The shaded band is an illustrative $\pm0.02$ range, not a confidence interval.

## Compare claim and evidence

```{slide-options}
{"layout":"compare"}
```

:::{slide-panel}
:title: What is visible
The plotted values repeat.

The axis labels define how to read the values.
:::

:::{slide-panel}
:title: What is not established
No star was observed.

The demonstration does not identify an astrophysical mechanism.
:::

## Reuse the notebook output

```{slide-options}
{"layout":"figure"}
```

![](#sample-figure)

Native MyST embedding retains a link to the source notebook.

## Magnify without regenerating

```{slide-figure} analysis.ipynb#sample-figure
:alt: Synthetic relative flux with a magnified region from the same notebook-generated figure.
:focus: 12 12 24 55
:caption: The inset uses the same figure pixels. Enlarging it adds no data.
[]
```

## Keep an interactive example printable

```{slide-embed} area-widget.html
:title: Interactive rectangle area
:fallback: rectangle.svg
:alt: A static diagram showing width five times height two equals area ten.
```

The PDF substitutes the authored diagram for the interactive controls.

## Discuss the interpretation

::::{slide-question}
:title: Concept check
What additional evidence would be needed before interpreting a repeating observed signal?

:::{slide-answer}
:title: Discussion prompts
Consider measurement uncertainty, sampling, calibration, and independent observations. The appropriate test depends on the actual data and proposed explanation.
:::
::::

```{slide-timer} 60
:title: Pair discussion
```

## Leave a clear takeaway

```{slide-options}
{"layout":"summary", "takeaway":"Describe the observable, identify the source, and state the limit of the claim."}
```

The [computational example](#comp-start) shows how code and output stay connected.

The [methods](#synthetic-method) identify these values as synthetic.[^synthetic]

[^synthetic]: Arbitrary time units and illustrative bounds are used solely to demonstrate presentation features.
