---
title: "Animation · Left rectangles"
subtitle: "Block 2 · Watch, pause, and explain"
---

A left rectangle replaces the function on each panel by its value at the left endpoint. The film accumulates these areas and then refines the partition for $f(x)=e^x$ on $[0,1]$.

## Before watching

As the panels get narrower, which changes: the area of each rectangle, the number of rectangles, or both? Predict whether left rectangles underestimate or overestimate this increasing function.

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-rectangles-player
:video: ../media/RectangleRecall.mp4
:poster: ../media/RectangleRecall-poster.png
A left rectangle replaces the function on each panel by its value at the left endpoint. The film accumulates these areas and then refines the partition for f(x)=e^x on [0,1].
:::

::::

## Mathematical connection

For a panel $[a,a+h]$, write $x=a+t$. Taylor expansion gives

$$f(a+t)=f(a)+tf'(a)+O(t^2).$$

Integrating from $t=0$ to $h$ gives

$$\int_a^{a+h}f(x)\,dx=hf(a)+\frac{h^2}{2}f'(a)+O(h^3).$$

The rectangle keeps $hf(a)$. Its local truncation error is $O(h^2)$. Over a fixed interval of length $L$, there are $L/h$ panels, giving composite error $O(h)$ for a sufficiently smooth function. These orders describe truncation error, not floating-point error.

## Explain what you saw

The running sum covers only the shaded panels. Explain why its error must be compared with the exact integral over that same covered interval. When the entire interval is covered, the exact integral is $e-1$.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#l7-rectangle-film) · [Full reading](../../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md) · [All animations](animations.md)
