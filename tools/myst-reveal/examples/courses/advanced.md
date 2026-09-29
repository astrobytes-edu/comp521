---
title: Presentation tools for teaching and research
subtitle: Synthetic examples · Research workflow demonstration
---
## Presentation tools for teaching and research

```{slide-options}
{"layout":"title","tags":["core"],"timing":20,"cue":"This is a software demonstration, not a research result."}
```

Compose the evidence. Rehearse the argument. Inspect the exported deck.

## Flexible columns

```{slide-options}
{"tags":["core"],"timing":30,"fit":"bounded","min-font":28}
```

::::{slide-columns}
:ratio: 2 1 1
:gap: 24
:align: start
:::{slide-column}
### Explain
Use wider space for the main argument. Columns preserve the source reading order.
:::
:::{slide-column}
### Show
$y=x^2$
:::
:::{slide-column}
### Check
At $x=2$, $y=4$.
:::
::::

## Give the figure room

```{slide-options}
{"layout":"figure-wide","tags":["core"],"timing":30,"limit":"Synthetic values; the inset adds no data or resolution."}
```

```{slide-figure} analysis.ipynb#sample-figure
:alt: Synthetic flux oscillating between 0.9 and 1.1 in arbitrary time units.
:focus: 12 12 24 55
[]
```

## Compare images deliberately

```{slide-options}
{"tags":["detail"],"timing":30}
```

```{slide-image-compare}
{"title":"Two copies of the same figure","images":[{"source":"analysis.ipynb#sample-figure","alt":"Synthetic flux curve, first copy","label":"First copy"},{"source":"analysis.ipynb#sample-figure","alt":"The same synthetic flux curve, second copy","label":"Second copy"}],"caption":"Identical copies demonstrate blending. Real comparisons require registered coordinates and consistent color scales."}
```

## Synchronize playback

```{slide-options}
{"tags":["detail"],"timing":30}
```

```{slide-movies}
{"title":"Synchronized synthetic motion","movies":[{"source":"motion.mp4","poster":"rectangle.svg","label":"Synthetic animation A"},{"source":"motion.mp4","poster":"rectangle.svg","label":"Identical animation B"}],"caption":"Identical test movies; elapsed video time is synchronized. These are not physical simulations."}
```

## Change a parameter and compute

```{slide-options}
{"tags":["detail"],"timing":60}
```

```{slide-python}
:packages: numpy,matplotlib
:parameters: [{"name":"amplitude","label":"Amplitude","min":0.1,"max":2,"step":0.1,"value":1}]
:alt: A parabola scaled by the selected amplitude, with labelled x and y axes.
:fallback: analysis.ipynb#quadratic-cell
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-2, 2, 50)
plt.plot(x, amplitude * x**2)
plt.xlabel("x"); plt.ylabel("y")
plt.show()
```

The fallback uses amplitude one. Run computes the current edit and slider value.

## Trace actual Python state

```{slide-options}
{"tags":["detail"],"timing":45}
```

```{slide-python}
:trace: true
values = [1, 2, 3]
squares = []
for value in values:
    squares.append(value * value)
print(squares)
```

Run first, then inspect the recorded line events and variable snapshots.

## Follow the evidence into questions

```{slide-options}
{"tags":["core"],"timing":20,"cue":"Demonstrate Tools, Backups, Return to talk, then the rehearsal timer.","evidence":"https://docs.python.org/3/library/sys.html#sys.settrace","limit":"The trace is bounded to small teaching examples, not a debugger for research simulations."}
```

The full version includes **Tools → Backups** and **Return to talk**.
The short variant retains only the core slides.

Rehearsal records time spent on each slide and exports a local JSON file.

## Backup: what the trace records

```{slide-options}
{"backup":true,"tags":["detail"],"timing":30}
```

- Actual Python `line` and `return` events for the displayed source.
- State before each line executes; return events expose final state.
- At most 300 events, 20 list elements, and shortened scalar values.
- Arrays and complex objects are identified by type, not fully expanded.
