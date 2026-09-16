---
title: "Animation · Bisection"
subtitle: "Block 2 · Watch, pause, and explain"
---

For $f(x)=x^2-2$, start with $[1,2]$. Each midpoint evaluation identifies a half-interval that retains opposite endpoint signs. The film follows three decisions.

## Before watching

At the first midpoint, $m=1.5$. Calculate the sign of $f(m)$ and predict which half-interval will remain.

::::{div}
:class: animation-page

:::{lecture-film}
:id: animation-bisection-player
:video: ../media/Bisection.mp4
:poster: ../media/Bisection-poster.png
For f(x)=x^2-2, start with [1,2]. Each midpoint evaluation identifies a half-interval that retains opposite endpoint signs. The film follows three decisions.
:::

::::

## Mathematical connection

If $f$ is continuous on $[a,b]$ and the endpoints have opposite signs, at least one root lies inside. Check endpoint roots before requiring opposite signs.

After $k$ halvings of an initial width $W_0$, the retained width and its midpoint error satisfy

$$W_k=\frac{W_0}{2^k},\qquad |m_k-r|\leq\frac{W_0}{2^{k+1}}.$$

Here $m_k$ is the midpoint of the **new retained interval** and $r$ is a root inside it. This bound does not describe the old midpoint discarded or retained as an endpoint. Opposite signs across a discontinuity do not establish the theorem; a sign change also does not establish uniqueness.

## Explain what you saw

Separate the sign test from the width bound. Which justifies retaining a half-interval, and which supports a claim about root location? Explain why a small residual is a different statement.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration; its labels and the explanation above carry the content.

**Continue:** [Lecture 7](../lecture-07-adaptivity-roots.md#watch-the-bracket-shrink) · [Full reading](../../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md) · [All animations](animations.md)
