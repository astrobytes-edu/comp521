---
title: From code to a figure
subtitle: Computational science · Authoring example
---
(comp-start)=
## From code to a figure

```{slide-options}
{"layout":"title", "eyebrow":"Computational science", "takeaway":"One executed source supplies the code, result, and figure."}
```

Predict a result. Trace the calculation. Inspect the evidence.

## Make the calculation visible

```{slide-options}
{"layout":"section", "eyebrow":"01 · Reasoning with code"}
```

Use each reveal to expose one decision.

## Predict before running

::::{slide-question}
:title: Predict
What will this code print?

```python
values = [0, 1, 2, 3]
print([x * x for x in values])
```

:::{slide-answer}
:title: Reveal and explain
The result is `[0, 1, 4, 9]`. Each output uses the corresponding input twice in a multiplication.
:::
::::

## Trace the calculation

```{slide-code} python
:title: squares.py
:steps: [{"lines":"1","explain":"Choose the input values."},{"lines":"2","explain":"Transform each input independently."},{"lines":"3","explain":"Inspect the resulting sequence."}]
values = [0, 1, 2, 3]
squares = [x * x for x in values]
print(squares)
```

Step through the highlighted lines. The explanation follows the active step.

## Execute the same source

```{slide-options}
{"layout":"code", "takeaway":"Displayed code and displayed output come from the same executed cell."}
```

```{slide-code-example} analysis.ipynb#squares-cell
:title: Executed Python
:steps: [{"lines":"1","explain":"Inputs"},{"lines":"2","explain":"Transformation"},{"lines":"3","explain":"Observed output"}]
```

## Code becomes a figure

```{slide-options}
{"layout":"code"}
```

```{slide-code-example} analysis.ipynb#quadratic-cell
:title: Generate the quadratic plot
:lines: 1-2|3-4|5-7
:alt: A parabola showing y equals x squared for x from minus two to two, with labelled axes.
```

## Inspect a region of the result

```{slide-options}
{"layout":"figure"}
```

```{slide-figure} analysis.ipynb#quadratic-cell
:alt: The graph of y equals x squared is symmetric about x equals zero and has its minimum there.
:caption: The inset magnifies the upper-right region of the same generated image.
:focus: 62 12 30 38
[{"x":54,"y":82,"text":"Locate the minimum.","step":0},{"x":78,"y":30,"text":"Compare the two sides of the parabola.","step":1}]
```

## Build the derivation in steps

```{slide-options}
{"layout":"derivation"}
```

::::{slide-worked}
:title: Difference quotient for a quadratic
For $f(x)=x^2$ and $h\ne0$:

:::{slide-step}
:title: Substitute
$\displaystyle \frac{f(x+h)-f(x)}{h}=\frac{(x+h)^2-x^2}{h}$
:::

:::{slide-step}
:title: Simplify
$\displaystyle \frac{2xh+h^2}{h}=2x+h$
:::

:::{slide-step}
:title: Take the limit
As $h\to0$, the quotient approaches $2x$.
:::
::::

## Compare two representations

```{slide-options}
{"layout":"compare", "takeaway":"The two representations express the same input-output relationship."}
```

:::{slide-panel}
:title: Algebra
$y=x^2$

A compact statement of the relationship.
:::

:::{slide-panel}
:title: Code
```python
def square(x):
    return x * x
```
An executable expression of the relationship.
:::

## Check your understanding

::::{slide-question}
:title: Concept check
For $f(x)=x^2$, compare the difference quotients at $x=1$ for $h=0.1$ and $h=0.01$.

:::{slide-answer}
:title: Worked answer
They are $2.1$ and $2.01$. The exact derivative at $x=1$ is $2$.
:::
::::

```{slide-timer} 90
:title: Work individually, then compare
```

## Edit code and generate a plot

```{slide-python}
:packages: numpy,matplotlib
:fallback: analysis.ipynb#quadratic-cell
:alt: A Python-generated plot of y equals x squared; editing the expression changes the curve.
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-2, 2, 50)
plt.plot(x, x**2)
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

This optional experiment downloads its runtime and plotting packages.

## Carry the result into another context

```{slide-options}
{"layout":"summary", "takeaway":"Reuse the result with its source attached."}
```

- The [astronomy example](#astro-start) reuses a labelled notebook figure.
- The [methods page](#synthetic-method) records what the example represents.
- Footnotes can carry a short qualification.[^source]

[^source]: These examples demonstrate software behavior; they are not measurements of an astronomical source.

## Sources

Python syntax follows the Python documentation [@python-classes].

:::{bibliography}
:::
