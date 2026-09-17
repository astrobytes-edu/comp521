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

(secant-static-walkthrough)=
## Static walkthrough: one secant update

**Predict before opening:** start with $f(1)=-1$ and $f(2)=2$. Find the line's slope and zero. Which input will you discard after evaluating the new point?

::::{admonition} Worked explanation: saved values → line zero → new pair
:class: dropdown

### 1. Calculate the slope from saved values

:::{figure} ../media/Secant-slope-1.png
:alt: A line joins the saved curve samples at one and two; its slope is three.
:::

$$s_1=\frac{f(2)-f(1)}{2-1}=\frac{2-(-1)}{2-1}=3.$$

This slope comes from two function values; no derivative is evaluated.

### 2. Find the line's zero

:::{figure} ../media/Secant-step-1.png
:alt: The secant line crosses the axis at four thirds; the displayed update subtracts two thirds from two.
:::

$$0=2+3(x_2-2),\qquad x_2=2-\frac23=\frac43.$$

The line proposes the next input. Evaluate the original function there before constructing another line.

### 3. Evaluate once and keep the latest pair

:::{figure} ../media/Secant-residual-1.png
:alt: The new curve value at four thirds is negative two ninths; retain two and four thirds and discard one.
:::

$$f(4/3)=\frac{16}{9}-2=-\frac29.$$

Retain $2$ and $4/3$, reusing $f(2)$. The next update is

$$s_2=\frac{-2/9-2}{4/3-2}=\frac{10}{3},\qquad
x_3=\frac43-\frac{-2/9}{10/3}=\frac75.$$

Now $f(7/5)=-1/25$. Both retained values are negative: keeping the latest pair does not preserve a sign-changing bracket.
::::

## Explain what you saw

Track the older point, the current point, and the newly proposed point separately. Explain how the next pair differs from the pair that bisection would retain.

Use the player controls to pause, replay, or view fullscreen. The animation has no narration. Burned-in captions explain each action; the static walkthrough above provides the same calculations without playback.

**Continue:** [Lecture 8](../lecture-08-rootfinding-tools.md#watch-which-two-values-secant-keeps) · [Full reading](../../05-numerical-methods/02-roots-quadrature/01-mod2-part1-root-finding.md) · [All animations](animations.md)
