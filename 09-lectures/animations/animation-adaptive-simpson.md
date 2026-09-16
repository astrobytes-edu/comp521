---
title: "Animation · Adaptive Simpson quadrature"
subtitle: "Block 2 · Watch, pause, and explain"
---

Compare a coarse Simpson estimate with two half-interval estimates. The film follows $f(x)=e^{4x}$, splitting intervals and tolerance budgets, then adding accepted integral contributions.

## Before watching

Where would you expect refinement to concentrate for $e^{4x}$? What information must each interval return so that its parent can assemble an integral?

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-adaptive-simpson-player
:video: ../media/AdaptiveSimpson.mp4
:poster: ../media/AdaptiveSimpson-poster.png
Compare a coarse Simpson estimate with two half-interval estimates. The film follows f(x)=e^{4x}, splitting intervals and tolerance budgets, then adding accepted integral contributions.
:::

::::

## Mathematical connection

On the same interval, let $S$ use one Simpson pair and $S_2$ use two half-width pairs. If the leading smooth-function error term dominates, the fine estimate has about $1/16$ of the coarse estimate's error. Therefore

$$e_{\rm est}=\frac{|S_2-S|}{15},\qquad S_{\rm corrected}=S_2+\frac{S_2-S}{15}.$$

The first quantity estimates the error of $S_2$; it is not a proven error bound for the corrected result. Compare it with the interval's tolerance $\tau$. If refinement is needed, split the interval and give each child budget $\tau/2$. Accepted child contributions are added when returning to the parent.

A depth limit must report unfinished refinement as failure. Sample agreement can miss unsampled structure, even with a small estimated error.

## Explain what you saw

Follow the quantities in each direction: tolerance budgets go down the tree, integral contributions return upward. The film's covered-interval actual error uses a known exact integral for this example; a general adaptive integrator does not know that error.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#l7-adaptive-live-film) · [Full reading](../../05-numerical-methods/02-roots-quadrature/02-mod2-part2-quadrature.md) · [All animations](animations.md)
