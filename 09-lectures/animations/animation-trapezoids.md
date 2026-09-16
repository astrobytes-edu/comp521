---
title: "Animation · Trapezoids"
subtitle: "Block 2 · Watch, pause, and explain"
---

Join the two endpoint samples with a straight line and integrate that line. The film adds trapezoidal areas for $e^x$ on $[0,1]$ and compares successive uniform refinements.

## Before watching

The curve is convex. Predict whether its endpoint chord lies above or below the curve, and what that implies for the integral estimate.

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-trapezoids-player
:video: ../media/TrapezoidRecall.mp4
:poster: ../media/TrapezoidRecall-poster.png
Join the two endpoint samples with a straight line and integrate that line. The film adds trapezoidal areas for e^x on [0,1] and compares successive uniform refinements.
:::

::::

## Mathematical connection

Let $I=\int_a^{a+h} f(x)\,dx$ be the exact integral over one panel of width $h$. The trapezoid rule is

$$T=\frac{h}{2}[f(a)+f(a+h)].$$

Taylor expansion of the endpoint value and integration of the same series give

$$T=hf(a)+\frac{h^2}{2}f'(a)+\frac{h^3}{4}f''(a)+O(h^4),$$

$$I=hf(a)+\frac{h^2}{2}f'(a)+\frac{h^3}{6}f''(a)+O(h^4).$$

Thus $T-I=\frac{h^3}{12}f''(a)+O(h^4)$. The local error is $O(h^3)$ and the composite error over a fixed interval is $O(h^2)$ for a sufficiently smooth function. The straight-line model integrates constants and linear functions exactly.

## Explain what you saw

Compare the actual errors after each halving of the panel width. Explain why a ratio near four is expected once the leading second-order composite error dominates. This ratio is an asymptotic prediction, not an unconditional guarantee.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#l7-trapezoid-film) · [Full reading](../../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md) · [All animations](animations.md)
