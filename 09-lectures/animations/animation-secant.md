---
title: "Animation · The secant method"
subtitle: "Block 2 · Watch, pause, and explain"
---

Approximate Newton's derivative using the two most recent function values. The film follows $f(x)=x^2-2$ from the initial inputs $1$ and $2$, showing which point is retained after each update.

## Before watching

Draw the line through the two initial samples. Predict its zero, then decide which two points should define the next secant line.

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-secant-player
:video: ../media/Secant.mp4
:poster: ../media/Secant-poster.png
Approximate Newton's derivative using the two most recent function values. The film follows f(x)=x^2-2 from the initial inputs 1 and 2, showing which point is retained after each update.
:::

::::

## Mathematical connection

Use the slope

$$d_k=\frac{f(x_k)-f(x_{k-1})}{x_k-x_{k-1}}$$

in a Newton-style update:

$$x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.$$

Keep $x_k$ and $x_{k+1}$ for the next step, reusing $f(x_k)$. After initialization, each successful update needs one new function evaluation. Equal function values make the update undefined; near-equal values can cause a large or unreliable step. Check finite values and the function's domain. Ordinary secant does not preserve opposite signs or guarantee convergence.

## Explain what you saw

Track the older point, the current point, and the newly proposed point separately. Explain how the next pair differs from the pair that bisection would retain.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 8](../lecture-08-rootfinding-tools.md#watch-which-two-values-secant-keeps) · [Full reading](../../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md) · [All animations](animations.md)
