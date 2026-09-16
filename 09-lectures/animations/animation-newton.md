---
title: "Animation · Newton's method"
subtitle: "Block 2 · Watch, pause, and explain"
---

Starting at $x_0=2$ for $f(x)=x^2-2$, replace the curve locally by its tangent, find the tangent's zero, and return to the original curve. The film shows two updates.

## Before watching

The first tangent starts at $(2,2)$ and has slope $4$. Predict its horizontal displacement to the axis. After moving, can the same tangent supply the next update?

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-newton-player
:video: ../media/Newton.mp4
:poster: ../media/Newton-poster.png
Starting at x_0=2 for f(x)=x^2-2, replace the curve locally by its tangent, find the tangent's zero, and return to the original curve. The film shows two updates.
:::

::::

## Mathematical connection

The first-order Taylor model near $x_k$ is

$$f(x_k+\Delta x)\approx f(x_k)+f'(x_k)\Delta x.$$

Set this model to zero and solve:

$$x_{k+1}=x_k-\frac{f(x_k)}{f'(x_k)}.$$

The model is approximate, even though its zero is calculated exactly in real arithmetic. The derivative must be nonzero and the proposed point must remain in the function's domain. Sufficient smoothness, a simple root, and a sufficiently close starting point give local quadratic convergence. Newton does not preserve a bracket by itself.

## Explain what you saw

Find the moment when the animation returns from the axis to the curve. Explain why both the remaining residual and the tangent slope must be recomputed there.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#watch-the-tangent-then-return-to-the-curve) · [Full reading](../../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md) · [All animations](animations.md)
