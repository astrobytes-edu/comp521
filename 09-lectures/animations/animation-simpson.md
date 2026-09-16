---
title: "Animation · Simpson's rule"
subtitle: "Block 2 · Watch, pause, and explain"
---

Use three equally spaced samples to fit a quadratic and integrate it over a pair of panels. The film accumulates successive pairs for $e^x$ on $[0,1]$, refines the grid, and connects the error to Taylor symmetry.

## Before watching

A quadratic has degree two. Could its integration rule nevertheless integrate every cubic exactly? Think about the integral of an odd function over a symmetric interval.

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-simpson-player
:video: ../media/SimpsonRecall.mp4
:poster: ../media/SimpsonRecall-poster.png
Use three equally spaced samples to fit a quadratic and integrate it over a pair of panels. The film accumulates successive pairs for e^x on [0,1], refines the grid, and connects the error to Taylor symmetry.
:::

::::

## Mathematical connection

Let $m$ be the midpoint of a pair $[m-h,m+h]$. Let $I$ be the exact integral over this pair. The pair width is $2h$:

$$S=\frac{h}{3}[f(m-h)+4f(m)+f(m+h)].$$

Expand about $m$. Odd terms cancel in both the symmetric integral and the weighted samples. The constant and quadratic terms agree; the first mismatch is

$$I-S=-\frac{h^5}{90}f^{(4)}(m)+O(h^7)$$

when enough derivatives exist for this expansion. More generally, for continuous $f^{(4)}$, the exact remainder is $-h^5 f^{(4)}(\xi)/90$ for some point $\xi$ inside the pair. The local pair error is $O(h^5)$; summing over a fixed interval gives composite error $O(h^4)$. Cubic exactness comes from symmetry.

## Explain what you saw

Identify the two elementary panels belonging to each Simpson pair. Explain why halving $h$ predicts a factor of sixteen reduction in the leading composite error, and why the number of elementary panels must be even.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#l7-simpson-film) · [Full reading](../../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md) · [All animations](animations.md)
