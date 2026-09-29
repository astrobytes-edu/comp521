---
title: Explore an explanation
subtitle: Synthetic mathematics · No astronomical inference
---
## One expression, three views

```{slide-options}
{"fit":"bounded","min-font":28,"cue":"Select each term. Ask which part of the curve the highlighted code determines."}
```

```{slide-explanation}
{"title": "Connect a parabola to its implementation", "source": "analysis.ipynb#quadratic-cell", "alt": "The synthetic curve y equals x squared over minus two to two.", "code": "import numpy as np\nimport matplotlib.pyplot as plt\na = 1\nx = np.linspace(-2, 2, 81)\ny = a * x**2\nplt.plot(x, y)\nplt.show()", "terms": [{"label": "Amplitude a", "math": "a", "lines": [3, 5], "region": [0.14, 0.1, 0.8, 0.64], "explain": "Doubling a doubles every y value. The minimum stays at x = 0."}, {"label": "Squared coordinate", "math": "x^2", "lines": [4, 5], "region": [0.44, 0.67, 0.18, 0.14], "explain": "Opposite x values give the same y. Squaring sets the symmetry and the minimum at zero."}], "equation": "y = a x^2", "prompt": "Predict: if a doubles, what happens to y at x = 1?"}
```

```{slide-paths}
{"paths":[{"label":"Why this shape?","audience":"Conceptual","target":"slide-why-this-shape"},{"label":"Try the calculation","audience":"Implementation","target":"slide-try-the-calculation"}]}
```

## Why this shape?

```{slide-options}
{"vertical":true,"fit":"bounded","min-font":28,"cue":"Keep this derivation optional. The return control restores the original highlighted term."}
```

For the synthetic function $y=ax^2$ with $a>0$,

$$\frac{dy}{dx}=2ax, \qquad \frac{d^2y}{dx^2}=2a>0.$$

The slope vanishes at zero, where the curvature is positive. This establishes a minimum; it is not a model of an astronomical system.

```{slide-paths}
{"paths":[{"label":"Inspect numerical values","audience":"Implementation","target":"slide-try-the-calculation"}]}
```

:::{slide-evidence}
:title: Assumptions behind the derivation
:claim: The synthetic parabola has a minimum at zero when a is positive.
:status: illustrative

**Assumption:** real x, positive scalar a. The derivatives follow algebraically from the displayed polynomial.

**Boundary:** at a = 0 the function is constant; for a < 0 the stationary point is a maximum. No measurement or physical calibration is claimed.
:::

## Try the calculation

```{slide-options}
{"vertical":true,"class":"exploration-workbench","cue":"Run with amplitude one. Save a step, change amplitude and run again, save another. Replay, explore, and return."}
```

```{slide-python}
:packages: numpy,matplotlib
:alt: A synthetic parabola with labelled x and y axes.
:fallback: analysis.ipynb#quadratic-cell
:parameters: [{"name":"amplitude","label":"Amplitude","min":0.5,"max":2,"step":0.5,"value":1}]
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-2, 2, 81)
plt.plot(x, amplitude * x**2)
plt.xlabel("x"); plt.ylabel("y")
plt.show()
```

```{slide-replay}
```

```{slide-paths}
{"paths":[{"label":"Revisit the derivation","audience":"Mathematical","target":"slide-why-this-shape"}]}
```

## Inspect the evidence before the claim

```{slide-options}
{"layout":"figure-wide","cue":"Open evidence and distinguish a demonstration from a scientific result."}
```

```{slide-figure} analysis.ipynb#sample-figure
:alt: A synthetic oscillating curve with relative flux and arbitrary time labels.
:caption: An executed synthetic figure, reused from the shared notebook.
```

:::{slide-evidence}
:title: Source, assumptions and limitations
:claim: This figure demonstrates reuse of an executed notebook output.
:status: illustrative

**Source:** [](analysis.ipynb#sample-figure).

**Method:** the source notebook constructs an illustrative oscillating signal.

**Units:** time is arbitrary; relative flux is dimensionless.

**Limitation:** this is not observed photometry and does not support an astronomical inference.

**Audience question:** what evidence would be needed before interpreting a similar curve as a transit?
:::

## Return with the argument intact

Use the right arrow for the main story and the down arrow for native vertical details. Explicit explanation links can form deeper detours; their return button restores the previous slide, fragment and supported exploration state.

```{slide-replay}
```

Saved states last only for this open page. They do not capture a Python process, third-party widget, or external service.
