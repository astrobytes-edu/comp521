---
title: MyST Reveal Feature Tour
subtitle: COMP 521 · Authoring and presentation features
math:
  '\area': A
kernelspec:
  name: python3
  display_name: Python 3
---

## Presenter controls

Use the toolbar for **Slides**, **Notes**, **Search**, **Overview**, and a **Pointer**.

- **S** opens the presenter window; **Esc** opens the overview.
- **B** pauses with a black screen; **F** requests fullscreen.
- Arrow keys navigate; **Alt + click** zooms into a detail.

The handout link opens a scrolling copy with answers visible and presenter notes removed.

:::{speaker-note}
Feature tour: confirm that the current and upcoming slides appear here.
The clock and elapsed timer belong to Reveal's presenter view.
:::

## Ordered and grouped fragments

:::{fragment}
:effect: fade-out
:index: 0

This prompt begins visible and disappears on the first step.
:::

:::{fragment}
:effect: fade-up
:index: 0

This explanation appears on that same step.
:::

:::{fragment}
:effect: highlight-blue
:index: 1

This line begins visible and changes color on the second step.
:::

:::{fragment}
:effect: fade-in-then-out
:index: 2

This comment appears briefly, then disappears on the next step.
:::

## Incremental lists

:::{slide-incremental}
- Predict the result.
- Run the calculation.
- Compare the evidence with the prediction.
:::

One list item appears per step.

## Walk through the code

```{slide-code} python
:lines: 1|2-3|4
:start: 1
width = 5
height = 2
area = width * height
print(area)
```

Each step highlights the next part of the calculation.

## Evolve the implementation

```{slide-options}
{"auto-animate": true, "auto-animate-id": "rectangle-code"}
```

```{slide-code} python
:id: rectangle-code
:lines:
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
```

Start with the stored dimensions.

## Evolve the implementation

```{slide-options}
{"auto-animate": true, "auto-animate-id": "rectangle-code"}
```

```{slide-code} python
:id: rectangle-code
:lines:
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height
```

Add behavior; Reveal animates the matched code block.

## Animate a shared element

```{slide-options}
{"auto-animate": true, "auto-animate-id": "shared-box"}
```

:::{slide-element}
:id: shared-box
:style: width: 35%; background: #eef1f5; padding: 1em; border-radius: 8px;

Same element
:::

Advance to change its width and position.

## Animate a shared element

```{slide-options}
{"auto-animate": true, "auto-animate-id": "shared-box"}
```

:::{slide-element}
:id: shared-box
:style: width: 70%; margin-left: 15%; background: #d8eaea; padding: 1em; border-radius: 8px;

Same element
:::

The element retains its identity across the two slides.

## Section backgrounds

```{slide-options}
{"background-color": "#25253c", "transition": "zoom", "class": "dark"}
```

Background and transition settings belong to this slide.

The text uses a light foreground for contrast.

## Image background

```{slide-options}
{"background-image": "rectangle.svg", "background-size": "contain", "background-opacity": 0.15}
```

A local image is embedded in the exported file.

The low opacity leaves the explanation readable.

## Flexible columns and callouts

:::::{slide-columns}
:ratio: 2 1
::::{slide-column}
### Explain the relationship

The left column receives twice the available width.

```{math}
\area = w h
```

The macro comes from this document's MyST frontmatter.
::::
::::{slide-column}
:::{note} Teaching cue
Ask for a prediction before showing the result.
:::
::::
:::::

## Tabbed examples

::::{tab-set}
:::{tab-item} Stored
```python
self.area = width * height
```
An assignment stores a value.
:::
:::{tab-item} Computed
```python
@property
def area(self):
    return self.width * self.height
```
A property computes on access.
:::
::::

Use the tab buttons or focus a tab and press the left/right arrow keys.

## Overlay a staged explanation

::::{slide-stack}
:::{fragment}
:effect: fade-in-then-out
:index: 0

First: identify the changing state.
:::
:::{fragment}
:effect: current-visible
:index: 1

Next: compute the quantity from that state.
:::
::::

The two explanations share the same space.

## Optional vertical detail

Press the **down arrow** for the supporting example, or the **right arrow** to continue.

Vertical slides group an explanation with optional detail.

## Supporting example

```{slide-options}
{"vertical": true}
```

For a width of 5 and height of 2, the computed area is 10.

The up arrow returns to the main explanation.

## Interactive browser component

```{slide-embed} area-widget.html
:title: Interactive rectangle area
```

This local HTML component is bundled and runs in an isolated frame.

## Video with captions

```{slide-media} motion.mp4
:title: A marker moving from left to right
:kind: video
:captions: motion.vtt
:muted: true
:loop: true
```

**Description:** a teal marker moves across a light background. Use the playback controls.

## Audio playback

```{slide-media} tone.wav
:title: One-second demonstration tone
:kind: audio
```

The clip is a quiet, one-second tone. It has no spoken content.

Playback is user-controlled.

## Executed HTML output

```{code-cell} python
from IPython.display import HTML, display
display(HTML('<table style="font:24px system-ui;border-spacing:20px"><caption>Computed area</caption><tr><th>Width</th><th>Height</th><th>Area</th></tr><tr><td>5</td><td>2</td><td>10</td></tr></table>'))
```

The table comes from the executed cell, not a handwritten result.

## Sources and bibliography

The examples use Python class syntax [@python-classes]. Presentation controls and animation are provided by Reveal [@reveal-docs].

:::{slide-bibliography}
:::

## Print and offline delivery

- The HTML bundles the presentation runtime and local media.
- The handout displays the staged explanations in reading order.
- The PDF includes the slide content and revealed answers.
- Interactive controls remain interactive in HTML; a PDF is a static record.

Use this tour to review the authoring and presentation behavior before migrating a lecture.

## Video background

```{slide-options}
{"background-video": "motion.mp4", "background-video-muted": true, "background-video-loop": true, "background-opacity": 0.25}
```

A decorative background video plays without sound.

The moving marker is the same locally generated example shown earlier.

## Executed vector figure

```{code-cell} python
from IPython.display import SVG, display
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 120"><title>Two rectangles with equal areas</title><rect x="20" y="20" width="160" height="80" fill="#2f6f6f"/><rect x="260" y="40" width="320" height="40" fill="#5a5a8a"/></svg>'
display(SVG(svg))
```

The two rectangles have equal areas, despite their different shapes.

## Interactive background

```{slide-options}
{"background-iframe": "area-widget.html", "background-interactive": true, "class": "background-widget"}
```

The bundled component occupies the slide background. Its slider remains interactive.

## Live Python in the browser

```{slide-python}
width = 5
height = 2
print(width * height)
```

Edit and run the code. This optional component downloads its Python runtime on first use.

## Interactive plot

```{slide-embed} plot-widget.html
:title: Interactive quadratic plot
```

Predict how changing $a$ changes $y=a x^2$, then move the slider.
