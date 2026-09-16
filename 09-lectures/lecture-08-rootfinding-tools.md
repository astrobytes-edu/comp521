---
title: "Lecture 8 · Finite Differences and Root-Finding Tools"
subtitle: "Block 2 · Week 4"
site:
  hide_toc: true
  hide_outline: true
kernelspec:
  name: python3
  display_name: Python 3
---

:::{lecture-controls}
:id: lecture-08-controls
:::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## From geometric steps to reusable code

1. **Approximate a slope** using function values and Taylor expansion.
2. **Reuse information** to construct a secant update.
3. **Interpret small quantities** before declaring convergence.
4. **Build a module** whose tests check the mathematical contract.

**Jump to:** [Finite differences](#l8-difference) · [Secant](#l8-secant) · [Stopping](#l8-stopping) · [Module activity](#l8-lab) · [Advanced reference](#l8-advanced)
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Today's question

How do we turn a root-finding formula into a calculation whose result we can explain?

Equilibria, thresholds, and implicit model outputs can require repeated solves. Reusable methods need meaningful stopping and inspectable evidence.

By the end of class, you should be able to:

- derive a forward difference and explain its competing errors;
- derive secant from Newton and trace one update;
- distinguish root error, step size, and residual; and
- implement and test bisection in an importable module.

**Plan:** 3 min motivation/retrieval · 6 min finite differences · 6 min secant · 10 min stopping · 8 min briefing · 2 min questions. Then **40 minutes of module work**.
Newton and secant are extensions; Lecture 9 develops the methods further.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Recall: what information does each method use?

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

### Bisection

Two endpoints with opposite signs.

Which half retains a root, assuming continuity?
::::

::::{div}
:class: lecture-column

### Newton

A point and a derivative.

Where does the tangent cross zero?
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

(l8-difference)=
## I · Approximate a derivative from values

**Question:** what if we can evaluate $f(x)$ but do not have a derivative routine?

**Retrieve from Lecture 5:** a derivative is the limiting slope of a secant line:

$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.$$

A computer uses a finite, nonzero $h$. The leading forward-difference error is $hf''(x)/2$ for a smooth function; floating-point arithmetic limits how small $h$ can be.

[Full Taylor derivation](#l8-taylor-reference).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Predict: is the smallest step best?

For $f(x)=e^x$ at zero, the exact derivative is 1.

```python
# lecture-example: difference
import numpy as np
steps = 10.0 ** (-np.arange(1, 17))
slopes = (np.exp(steps) - 1.0) / steps
errors = np.abs(slopes - 1.0)
for h, slope, error in zip(steps[::3], slopes[::3], errors[::3]):
    print(f"h={h:.0e}: slope={slope:.8f}, error={error:.2e}")
```

`arange` excludes 17; array arithmetic evaluates all 16 steps.
`np.abs` gives the absolute error at each step.

**Predict before running.** The next slide supplies a prepared plot if live execution is unavailable.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Smaller helps until rounding interferes

:::{figure} figures/difference-error.png
:alt: A log-log plot shows derivative error decreasing with step size, then rising at the smallest steps; the h over two line shows the truncation prediction.

Read leftward for smaller steps. Subtraction and division amplify floating-point effects; truncation alone does not describe the total error.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Two errors pull the step size in opposite directions

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

### Truncation

Write $D_hf=[f(x+h)-f(x)]/h$. Forward difference drops Taylor terms:

$$D_hf-f'\approx\frac{h}{2}f''.$$

Smaller $h$ reduces this error in the smooth regime.
::::

::::{div}
:class: lecture-column

### Floating-point effects

The function values are rounded. Subtracting nearby values exposes those errors; division by $h$ magnifies them.

A common model is

$$E(h)\approx C_1|h|+C_2\frac{\varepsilon}{|h|}.$$

Here $\varepsilon$ denotes machine precision. The constants depend on the function and its scale; there is no universally best fixed step.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

(l8-secant)=
## II · Secant obtains its slope from the iteration

**Question:** can we reuse values we already paid to calculate?

Finite-difference Newton samples a new nearby point to approximate the derivative.
Secant instead uses the two most recent iterates.

Both use a straight-line model. Secant changes the line as the pair of iterates changes; it does not keep a prescribed differentiation step.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Secant reuses two iterates

Approximate Newton's derivative using two previous points:

$$f'(x_k)\approx\frac{f(x_k)-f(x_{k-1})}{x_k-x_{k-1}}.$$

Substitute into Newton's step:

$$x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.$$

The separation comes from the iterates. We do not prescribe a separate fixed $h$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Predict the secant intersection

For $f(x)=x^2-2$, start with $x_0=1$ and $x_1=2$.

$$f(x_0)=-1,\qquad f(x_1)=2.$$

Use the update to find $x_2$. Which two points will define the following line?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Watch which two values secant keeps

:::{lecture-film}
:id: film-Secant
:video: media/Secant.mp4
:poster: media/Secant-poster.png

A secant through the two retained points proposes a zero, then replaces the older point with a newly evaluated one.
:::

**Interpret:** which value is reused? Which point is discarded? Ordinary secant does not enforce opposite signs.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Translate the geometry into an update

For the two points $(1,-1)$ and $(2,2)$, the slope is

$$s=\frac{2-(-1)}{2-1}=3.$$

The line through the newest point is $\ell(x)=2+3(x-2)$.
Set $\ell(x)=0$ to obtain $x_2=4/3$.

Now evaluate $f(4/3)$ and retain the previous value $f(2)$ for the next line.
Only one new function value is needed. Unlike bisection, we keep recent points rather than opposite signs.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Compare what must be evaluated

| Method | Starting information | New information per ordinary step |
| --- | --- | --- |
| Bisection | Two endpoint values | One midpoint value |
| Newton | One starting point | Function and derivative |
| Secant | Two starting values | One new function value, reusing the previous value |

Count the actual work: evaluating a derivative may be cheap or expensive.
A zero secant denominator makes the update undefined. Distinct inputs can have equal function values. A tiny difference can produce an unreliable step; an arbitrary perturbation is not a guaranteed repair.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

(l8-stopping)=
## III · Decide what convergence means

**Question:** small in which quantity, and relative to which scale?

In Lecture 5, `atol` and `rtol` expressed a comparison allowance.
Here we must also decide **what evidence** to compare with that allowance.

A root-error bound, a small update, and a small residual answer different questions. A solver's stopping rule belongs in its documented interface.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Three different meanings of small

| Quantity | What it measures |
| --- | --- |
| $(b-a)/2$ | A midpoint root-error bound for a valid bracket |
| $\vert x_{k+1}-x_k\vert $ | Movement between iterates |
| $\vert f(x_k)\vert $ | How well the equation is satisfied |

The residual has the units of $f$. The root error and step have the units of $x$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## A small residual need not locate the root

A **simple root** has $f(r)=0$ and $f'(r)\ne0$. Near it, Taylor gives

$$f(x)\approx f'(r)(x-r),\qquad
|x-r|\approx\frac{|f(x)|}{|f'(r)|}.$$

For a stated function-error scale, dividing by a small slope amplifies position uncertainty. This is a local approximation, not a global error bound.

**Predict:** for $f(x)=10^{-12}(x-1)$ at $x=2$, what are the residual and root error?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Scaling the function changes the residual

:::{figure} figures/residual-position.png
:alt: Two rescaled linear functions have the same root and the same horizontal position error, but different vertical residuals.

Both inputs and the reference root are dimensionless; the panels explicitly use different residual scales.
:::

Multiplying by a **nonzero constant** leaves roots unchanged. Choose a residual criterion using the equation’s scale and units.

[Optional live rescaling check](#l8-rescale-live).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Give tolerances a meaning

A root-location criterion can use

$$\tau_x=\mathrm{atol}+\mathrm{rtol}|x|.$$

- `atol`: an absolute allowance in the units of $x$.
- `rtol`: a dimensionless relative allowance.
- Near zero, a nonzero absolute scale may be necessary.

Bisection compares a bound with $\tau_x$. Newton and secant compare their step,
then inspect the residual separately. A tiny step can also mean stagnation.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Work out the allowance before running the solver

Suppose $x$ is measured in seconds. Choose, for illustration,
$\mathrm{atol}=10^{-6}\,\mathrm{s}$ and $\mathrm{rtol}=10^{-6}$.

| Current estimate | $\tau_x=\mathrm{atol}+\mathrm{rtol}\vert x\vert $ |
| --- | --- |
| $x=0$ | $10^{-6}\,\mathrm{s}$ |
| $x=1\,\mathrm{s}$ | $2\times10^{-6}\,\mathrm{s}$ |
| $x=10^6\,\mathrm{s}$ | $1.000001\,\mathrm{s}$ |

The same relative allowance permits a larger absolute difference at larger scales.
Choose these values from the task's accuracy needs; the example is not a universal default.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

(l8-lab)=
## IV · Lab briefing · minutes 25–33

Finish the interface and test briefing inside the first 35 minutes. Then begin the protected **40-minute implementation block**.

**Core:** implement and test bisection on a non-project equation.

**Extension:** add Newton or secant and compare iteration histories.

This module can carry into Project 3 when it is posted next week.
Today does not introduce a separate graded submission.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Give the code an importable home

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

```text
root-lab/
├── roots.py
├── tests/
│   └── test_roots.py
└── exploration.ipynb
```
::::

::::{div}
:class: lecture-column

- `roots.py`: numerical methods.
- Tests: behavior and failure cases.
- Notebook: plots and interpretation.

Keep plots and demonstration runs out of the module's top level.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Plan the 40 minutes around observable checkpoints

| Time | Work | Check before moving on |
| --- | --- | --- |
| First 10 min | Interface, inputs, and first midpoint | Trace the bracket on paper |
| Next 15 min | Bisection loop and stopping | Width shrinks; the root stays bracketed |
| Next 10 min | Behavior and failure tests | Run `python -m pytest` |
| Final 5 min | Inspect a history and explain a result | State the tolerance and supporting evidence |

If the core works early, try Newton or secant. A tested bisection implementation is the core outcome; speed is not the completion criterion.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Agree on the interface before the loop

```python
def bisect(f, a, b, atol=1e-12, rtol=0.0, max_iter=200):
    """Return (root, n_iter, history); implement the method yourself."""
    raise NotImplementedError
```

For this lab, history records each evaluated midpoint in order; `n_iter` counts
those evaluations. An endpoint with zero computed residual returns zero iterations and an empty history.

Otherwise the returned root is the last evaluated midpoint. Use `ValueError`
for an invalid bracket or exhausted iteration budget, using this activity’s interface.

[Input and failure contract](#l8-contract-reference). Check the **current** bracket half-width for the midpoint just evaluated; do not apply an updated half-width to the old midpoint.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Implement the invariant, not just the update

1. Check inputs and endpoint roots; establish a valid bracket.
2. Evaluate its midpoint and record it.
3. Check a zero computed residual or the current midpoint error bound.
4. Otherwise retain the half with opposite endpoint signs.
5. Stop with a useful failure message if the iteration budget is exhausted.

Work on continuous functions. Input checks cannot prove continuity.
Do not silently replace a missing bracket with a guessed interval.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Test a known root without solving the project

```python
import numpy as np
from roots import bisect

def test_known_root():
    root, n_iter, history = bisect(
        lambda x: x*x - 2, 1.0, 2.0, atol=1e-8, rtol=0.0
    )
    assert abs(root - np.sqrt(2)) <= 1e-8
    assert n_iter == len(history)
    assert history[-1] == root
```

A `lambda` is a small anonymous function. Here it supplies the residual.
Run from the lab directory with `python -m pytest`.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Add tests that could expose a mistake

| Case | Evidence to check |
| --- | --- |
| $x^2-2$ on $[1,2]$ | Root agrees with $\sqrt2$ within the stated absolute target |
| $x-1$ on $[1,2]$ | Endpoint root: zero midpoint evaluations |
| $x^2+1$ on $[-1,1]$ | `ValueError`: no sign-changing bracket |
| $x^2-2$, one iteration, tight tolerance | `ValueError`: insufficient iterations |

Trace the first three brackets on paper. Check their signs and widths against
intermediate values in your implementation. A root-only test cannot verify the invariant.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## Compare histories when the core works

Add Newton or secant for the same equation.

- Plot $|x_k-\sqrt2|$ against iteration number.
- Count function and derivative evaluations separately.
- Try a second starting point; explain changed behavior.

A faster example is not a universal ranking. Next lecture develops convergence
conditions, failure modes, and safeguards.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

(l8-start-lab)=
## Begin the 40-minute implementation block

Need a refresher? Use [bisection’s mathematical foundation](https://astrobytes-edu.github.io/comp521/mod2-part1-root-finding/#method-1-bisection),
[module boundaries](https://astrobytes-edu.github.io/comp521/python-functions-modules/#modules-as-reusable-scientific-boundaries),
and [documentation and tests](https://astrobytes-edu.github.io/comp521/python-functions-modules/#documentation-tests-and-public-type-hints).
Build from the invariant before comparing with the reading’s implementation; use today’s interface. Advanced root-finding sections are Lecture 9/reference.

Before leaving, show one passing behavior test and one intentional failure case.

Keep your module and iteration evidence for Project 3. We continue root finding
in Lecture 9; the scientific project is posted next week.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching

## V · Reference for Lecture 9 and the lab

Keep the following material accessible. It is outside today’s 35-minute instruction and briefing path.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

(l8-taylor-reference)=
## A derivative from two nearby values

For sufficiently smooth $f$, Taylor expansion gives

$$f(x+h)=f(x)+hf'(x)+\frac{h^2}{2}f''(x)+O(h^3).$$

Subtract $f(x)$ and divide by $h\ne0$:

$$\frac{f(x+h)-f(x)}{h}=f'(x)+\frac{h}{2}f''(x)+O(h^2).$$

The leading truncation error is first order when $f''(x)\ne0$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## Static companion: the first secant

:::{figure} figures/secant.png
:alt: The secant through one and two intersects at four thirds.

$x_2=4/3$. Next use $x_1=2$ and $x_2=4/3$.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## Stop or report failure?

| Evidence | Response |
| --- | --- |
| Zero computed residual | Return the sampled zero; do not claim exact real-arithmetic equality |
| Valid bracket sufficiently narrow | Return its midpoint |
| Small Newton/secant step | Check the residual and whether progress stalled |
| Invalid bracket, unusable slope, non-finite value | Report why the calculation cannot proceed |
| Iteration limit reached without meeting the criterion | Report non-convergence |

A solver should not disguise failure as an ordinary root.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

(l8-advanced)=
## Keep the model; add safeguards

**Question:** can we combine a fast proposal with a reliable fallback?

Bisection supplies interval evidence. Newton and secant supply model-based proposals.
Practical methods can use both.

This is an overview: identify the ingredients today. We will examine convergence and failure behavior in the next lectures.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## Advanced methods combine useful ideas

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

### Safeguarded Newton

Maintain a bracket. Use a Newton proposal when it satisfies the safeguard;
otherwise take a reliable bracket-reducing step.
::::

::::{div}
:class: lecture-column

### Brent's method

Combine bisection with secant and inverse-quadratic interpolation proposals.

A maintained bracket and acceptance conditions provide reliability under the
method's assumptions.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## The same Taylor idea extends to systems

For several unknowns, $F$ contains one residual per equation. The Jacobian records how each residual responds to each unknown: $J_{ij}=\partial F_i/\partial x_j$. Then

$$F(x+\Delta x)\approx F(x)+J(x)\Delta x.$$

Choose the step by solving

$$J(x)\Delta x=-F(x).$$

Solve this linear system for the correction $\Delta x$; do not explicitly form an inverse. The scalar Newton step is the one-equation version.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## Why this matters for data science

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

### Quantiles are inverse problems

For a continuous, strictly increasing CDF $C(x)$ and $0<q<1$, the unique quantile satisfies

$$C(x)-q=0.$$

A numerical bracket must span the target probability. Discrete CDFs instead need a generalized inverse. We know the desired probability $q$ and seek its input $x$. Numerical inversion is useful when an explicit inverse is unavailable.
::::

::::{div}
:class: lecture-column

### Optimization uses related equations

A differentiable loss has stationary points where $\nabla L=0$.

Newton applied to this equation uses the **Hessian**, the matrix of second derivatives of $L$.

A root of the gradient may be a minimum, maximum, or saddle; locating it does not classify it.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

(l8-contract-reference)=
## Input and numerical failure contract

- Endpoints: finite scalars with $a<b$; endpoint zeros handled first.
- Tolerances: finite, nonnegative; at least one positive.
- `max_iter`: a positive integer (not a Boolean).
- Function values: finite real scalars; use direct sign comparisons rather than products.
- Report `ValueError` with a useful message for invalid inputs, unusable function values, or exhaustion.
- If the requested width remains unmet and no interior midpoint is representable, report numerical failure.

Continuity is a mathematical precondition; finite input checks cannot prove it. History stores evaluated midpoints, not an unevaluated midpoint of the updated bracket.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

(l8-rescale-live)=
## Optional run: scale the function, keep the root

Predict the two residuals before running. Here both functions have root 1.

```python
# lecture-example: rescaling
x, root = 2.0, 1.0
for scale in (1.0, 1e-12):
    residual = scale * (x - root)
    print(f"scale={scale:.0e}, residual={residual:.0e}, "
          f"root error={abs(x-root):.0e}")
```

:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## Prepared output: rescaling

Residuals: **1** and **1e−12**. Root error: **1** in both cases.

**Interpret:** why does scaling the residual leave the root location unchanged?

The reference root is available for this teaching example; a general solver usually cannot calculate its actual error.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 projector-slide lecture-teaching lecture-reference

## When a residual gives a bound

Suppose $f$ is continuously differentiable between $x$ and a root $r$, and a justified bound satisfies $|f'|\ge m>0$ throughout that interval.

The mean value theorem gives

$$|x-r|\le |f(x)|/m.$$

If the computed residual has error at most $\eta$, replace the numerator by $|\widehat f(x)|+\eta$. A derivative at one point alone is not the required interval bound.

Lecture 9 connects this with root sensitivity and nested numerical calculations.
:::::::
