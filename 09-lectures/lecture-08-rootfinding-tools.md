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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## From geometric steps to reusable code

1. **Approximate a slope** using function values and Taylor expansion.
2. **Rebuild Newton’s update**, then reuse information in secant.
3. **Interpret small quantities** before declaring convergence.
4. **Build a module** whose tests check the mathematical contract.

**Jump to:** [Finite differences](#l8-difference) · [Newton to secant](#l8-newton) · [Stopping](#l8-stopping) · [Module activity](#l8-lab) · [Advanced reference](#l8-advanced)
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Today's question

How do we turn a root-finding formula into a result we can explain?

**Recall quantile inversion:** solve $C(x)-q=0$. Each new target probability $q$ requires another solve.

Equilibrium models and implicit ML predictions also reuse root finders. We need **accuracy evidence and clear failure behavior**.

**Today:** approximate a slope → reuse values → decide when to stop → build a tested module.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Recall bisection: keep a root bracketed

:::{figure} figures/l8-bisection-recap.png
:alt: For x squared minus two, evaluate each midpoint and retain the half with opposite endpoint signs: one to two, one to one point five, then one point two five to one point five.
:::

$$m=\frac{a+b}{2},\qquad |m-r|\le\frac{b-a}{2}.$$

For continuous $f$, retain opposite endpoint signs to keep a root $r$ bracketed. **Evaluate $m$; retain a half; repeat.**
:::::::


:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Can local shape suggest the next input?

Bisection uses signs to retain a bracket. Newton uses a **local slope** to propose a new input.

To use a slope, we first need to understand how a computer approximates a derivative from function values.

**Route:** approximate a derivative → rebuild Newton's update → reuse samples in secant.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-difference)=
## I · Approximate a derivative from values


:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

:::{figure} figures/l8-difference-geometry.png
:alt: Two samples form a secant. The horizontal separation is h and the vertical change is delta f.
:::
::::

::::{div}
:class: lecture-column

**What if we can evaluate $f$, but have no derivative routine?**

Use two nearby values:

$$D_hf=\frac{\Delta f}{h}=\frac{f(x+h)-f(x)}{h}.$$

As $h\to0$, this secant slope tends to $f'(x)$ when the derivative exists.

A computer uses $h\ne0$. Taylor expansion explains the error.
::::
:::::

:::::::


:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Taylor explains the derivative error

For sufficiently smooth $f$ near $x$,

$$f(x+h)=f(x)+hf'(x)+\frac{h^2}{2}f''(x)+O(h^3).$$

Subtract $f(x)$ and divide **every remaining term** by $h\ne0$:

$$\underbrace{\frac{f(x+h)-f(x)}{h}}_{D_hf}
=f'(x)+\underbrace{\frac{h}{2}f''(x)}_{\text{leading error}}+O(h^2).$$

When $f''(x)\ne0$, the leading error is **first order**: halving $h$ approximately halves it. [Derivation reference](#l8-taylor-reference).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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

`arange` excludes 17. `np.abs` measures error; `zip` pairs entries. `[::3]` prints every third step.

**Predict:** which step gives the smallest error? Run, then compare with the next plot.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Smaller helps until rounding interferes

:::{figure} figures/difference-error.png
:alt: A log-log plot shows derivative error decreasing with step size, then rising at the smallest steps; the h over two line shows the truncation prediction.

Read leftward for smaller steps. Rounding eventually outweighs the reduction in truncation error.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-newton)=
## II · From Newton to secant

Near the current estimate $x_k$, replace the curve by its **tangent model**:

$$\ell_k(x)=f(x_k)+f'(x_k)(x-x_k).$$

Set $\ell_k(x_{k+1})=0$ and solve for the correction:

$$\Delta x_k=-\frac{f(x_k)}{f'(x_k)},\qquad x_{k+1}=x_k+\Delta x_k.$$

Here $k$ counts updates, $f(x_k)$ is the **residual**, and $f'(x_k)$ is the **local slope**. We solve the linear model exactly; the curve is only approximated.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Predict Newton's next input

For $f(x)=x^2-2$, use $f'(x)=2x$ and start at $x_0=2$.

$$f(2)=2,\qquad f'(2)=4,\qquad x_1=2-\frac{2}{4}.$$

**Predict:** where does the tangent cross zero? Is the original curve also zero at that input?

What must we recompute before taking another step?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Watch Newton calculate, move, and rebuild

:::{lecture-film}
:id: l8-film-Newton
:video: media/Newton.mp4
:poster: media/Newton-poster.png
Newton substitutes the residual and slope into each correction, moves to the tangent's zero, then reevaluates the curve.
:::

**Pause after the first update:** why must we reevaluate the curve? Replay, then compare corrections. [Explanation](animations/animation-newton.md).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## The next step needs a new tangent

:::::{div}
:class: lecture-two-column
::::{div}
:class: lecture-column
:::{figure} figures/l8-newton-rebuild.png
:alt: The rebuilt tangent at one point five has slope three and crosses zero at seventeen twelfths.
:::
::::
::::{div}
:class: lecture-column
At $x_1=3/2$, evaluate the **curve** again:

$$f(3/2)=1/4,\qquad f'(3/2)=3.$$

$$x_2=\frac32-\frac{1/4}{3}=\frac{17}{12}.$$

A nonzero derivative permits the update; it does not guarantee convergence. The new point must remain in the domain. Newton does not preserve a bracket.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Put our derivative approximation into Newton

When a derivative routine is unavailable, Part I supplies

$$D_hf(x_k)=\frac{f(x_k+h)-f(x_k)}{h}.$$

Replace the derivative in Newton's update:

$$x_{k+1}=x_k-\frac{f(x_k)}{D_hf(x_k)}.$$

We choose $h\ne0$ and evaluate an **extra nearby sample** $f(x_k+h)$. The slope estimate must be usable and nonzero; truncation and rounding affect it.

**Next idea:** we already know the previous iterate's function value. Can we reuse it instead?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-secant)=
## Secant obtains its slope from the iteration

:::{figure} figures/l8-slope-sampling.png
:alt: Finite-difference Newton chooses a new nearby sample; secant uses the two latest iterates.
:::

**Finite-difference Newton:** choose a new sample near the current iterate.

**Secant:** reuse the previous iterate and its function value. The separation changes with the iteration; there is no separately prescribed $h$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Secant reuses two iterates

Approximate Newton's derivative using two previous points:

$$f'(x_k)\approx\frac{f(x_k)-f(x_{k-1})}{x_k-x_{k-1}}.$$

Substitute into Newton's step:

$$x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.$$

A **secant line** joins two samples. The **secant method** specifically reuses successive iterates; their separation replaces a separately chosen $h$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Predict the secant intersection

For $f(x)=x^2-2$, start with $x_0=1$ and $x_1=2$.

$$f(x_0)=-1,\qquad f(x_1)=2.$$

Use the update to find $x_2$. Which two points will define the following line?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Watch which two values secant keeps

:::{lecture-film}
:id: film-Secant
:video: media/Secant.mp4
:poster: media/Secant-poster.png

A secant through the two retained points proposes a zero, then replaces the older point with a newly evaluated one.
:::

**Pause after the first update:** which point is retained, and which is discarded? Replay to check. [Explanation](animations/animation-secant.md).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Translate the geometry into an update

For the two points $(1,-1)$ and $(2,2)$, the slope is

$$s=\frac{2-(-1)}{2-1}=3.$$

The line through the newest point is $\ell(x)=2+3(x-2)$.
Set $\ell(x)=0$: $x_2=4/3$.

Now evaluate $f(4/3)$ and retain the previous value $f(2)$ for the next line.
Only one new function value is needed. Unlike bisection, we keep recent points rather than opposite signs.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Compare what must be evaluated

| Method | Starting information | New information per ordinary step |
| --- | --- | --- |
| Bisection | Two endpoint values | One midpoint value |
| Newton | One starting point | Function and derivative |
| Secant | Two starting values | One new function value, reusing the previous value |

Count actual evaluations: derivatives may be cheap or expensive.
:::::::


:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Distinct inputs can have equal function values

For $f(x)=x^2-2$, choose $x_0=-1$ and $x_1=1$:

$$f(-1)=f(1)=-1,\qquad f(x_1)-f(x_0)=0.$$

The secant is horizontal at $y=-1$: it never crosses zero. The update divides by zero.

A tiny value difference can also produce an unreliable step. Report the failure; an arbitrary perturbation is not a guaranteed repair.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-stopping)=
## III · Decide what convergence means

**Question:** small in which quantity, and relative to which scale?

In Lecture 5, `atol` and `rtol` expressed a comparison allowance.
Here we must also decide **what evidence** to compare with that allowance.

A root-error bound, a small update, and a small residual answer different questions. A solver's stopping rule belongs in its documented interface.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Three different meanings of small

:::{figure} figures/l8-stopping-geometry.png
:alt: A bracket bound measures distance from its midpoint to its endpoints, a step measures horizontal movement, and a residual measures vertical distance to zero.
:::

**Bound:** limits root error for a valid bracket. **Step:** measures movement. **Residual:** measures how well the equation is satisfied.

Root error and step have $x$'s units; residual has $f$'s units.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## A small residual need not locate the root

A **simple root** has $f(r)=0$ and $f'(r)\ne0$. Near it, Taylor gives

$$f(x)\approx f'(r)(x-r),\qquad
|x-r|\approx\frac{|f(x)|}{|f'(r)|}.$$

For a stated function-error scale, dividing by a small slope amplifies position uncertainty. This is a local approximation, not a global error bound.

**Predict:** for $f(x)=10^{-12}(x-1)$ at $x=2$, what are the residual and root error?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Scaling the function changes the residual

:::{figure} figures/residual-position.png
:alt: Two rescaled linear functions have the same root and the same horizontal position error, but different vertical residuals.

Same input scale; different vertical scales. All quantities here are dimensionless.
:::

**Same root, different residual.** Choose residual tolerances using the equation’s scale and units.

[Optional live rescaling check](#l8-rescale-live).
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Give tolerances a meaning

A root-location criterion can use

$$\tau_x=\mathrm{atol}+\mathrm{rtol}|x|.$$

- `atol`: an absolute allowance in the units of $x$.
- `rtol`: a dimensionless relative allowance.
- Near zero, a nonzero absolute scale may be necessary.

Bisection compares a bound with $\tau_x$. Newton and secant compare their step,
then inspect the residual separately. A tiny step can also mean stagnation.

In this lab, use the **current evaluated midpoint** $m$: compare its bracket bound with $\tau_m$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Predict: does the smaller bracket certify the old midpoint?

For $f(x)=x-0.9$ on $[0,1]$, take $\mathrm{atol}=0.25$ and $\mathrm{rtol}=0$.

The evaluated midpoint is $m=0.5$. Its negative value retains the bracket $[0.5,1]$, whose half-width is $0.25$.

**Predict:** can we now return the already evaluated $m=0.5$ with a root-error bound of $0.25$?

Which point is the center of the new bracket?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## A bound belongs to a particular midpoint

:::{figure} figures/l8-midpoint-bound.png
:alt: The original bracket has midpoint 0.5 and bound 0.5. After retaining the right half, its midpoint is 0.75 and its bound is 0.25. The old midpoint is not the new center.

Old midpoint: error $0.4>0.25$. New midpoint: error $0.15\le0.25$.
:::

Here the root is known. A general solver uses the **current bracket bound** to certify its midpoint.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-lab)=
## IV · Build and test a root-finding module

Work from a mathematical invariant to an interface, then test both success and failure.

**Core:** implement and test bisection on a non-project equation.

**Extension:** add Newton or secant and compare iteration histories.

This module can carry into Project 3 when it is posted next week.
Today does not introduce a separate graded submission.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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

**`tests/` → imports → `roots.py`**

Checks behavior and expected failures.

**Notebook → imports → `roots.py`**

Plots histories and interprets results.

Keep plots and demonstration runs out of the module's top level.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Trace → implement → harden

| Stage | Work | Completion check |
| --- | --- | --- |
| Trace | Follow three brackets on paper | Explain retained signs and the current midpoint bound |
| Implement | Build the loop and record midpoints | Known-root and endpoint-root tests pass |
| Harden | Complete input checks and failure tests | Invalid inputs fail; tolerance and iteration limits behave as documented |

Keep the [required contract](#l8-contract-reference) open while working. A first successful root is a checkpoint; complete all three stages before Newton or secant.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Trace first: explain each decision

Use $f(x)=x^2-2$ on $[1,2]$. Before coding, make three rows:

$$[a,b],\quad m,\quad \operatorname{sign}f(m),\quad B_m,\quad\text{retained half}.$$

For each row, explain why the retained endpoints still have opposite signs. The bound belongs to the midpoint evaluated in that row.

**Check:** a partner can reconstruct your next bracket from your recorded evidence.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Implement: agree on the interface before the loop

```python
def bisect(f, a, b, atol=1e-12, rtol=0.0, max_iter=200):
    """Return (root, n_iter, history); implement the method yourself."""
    raise NotImplementedError
```

**History:** evaluated midpoints, in order.

**Count:** `n_iter == len(history)`.

**Return:** the last evaluated midpoint, `history[-1]`.

**Endpoint zero:** return that endpoint with `n_iter=0` and `history=[]`.
:::::::


:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-contract-reference)=
## Required lab contract: inputs and failures

- Endpoints: finite real scalars with $a<b$; handle endpoint zeros before the sign test.
- Tolerances: finite, nonnegative; at least one positive.
- `max_iter`: a positive integer, excluding Boolean values.
- Function values: finite real scalars; compare signs directly rather than multiplying values.

Use **`ValueError`** for invalid inputs, an invalid bracket, or unusable function values. Use **`RuntimeError`** for an exhausted iteration budget or an unmet tolerance when no interior midpoint is representable.

Continuity and reliable function signs are mathematical preconditions; input checks cannot establish them.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Required lab contract: stopping and recorded evidence

At the evaluated midpoint $m$ of the **current** bracket $[a,b]$, use

$$\tau_m=\mathrm{atol}+\mathrm{rtol}|m|,\qquad
B_m=\max(m-a,b-m).$$

For an exact midpoint, $B_m=(b-a)/2$. The maximum distance also covers a rounded, off-center midpoint.

- Accept a zero computed residual or $B_m\le\tau_m$; record this midpoint before returning.
- Otherwise retain the sign-changing half and continue. Its new width does not certify the old midpoint.
- If evaluation underflows to zero or signs are unreliable, the numerical bracket is not a real-arithmetic guarantee.

Record evaluated midpoints only. Endpoint roots have an empty history.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Translate the reading interface deliberately

| Choice | Reading | Lab |
| --- | --- | --- |
| Function | `bisection` | `bisect` |
| Tolerance | Absolute `tol` | `atol + rtol*abs(m)` |
| Return | Root estimate | `(root, n_iter, history)` |

Both use a bracket-based position criterion. The lab also records evidence for inspection.

**Shared exceptions:** `ValueError` for invalid inputs; `RuntimeError` for non-convergence.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Reading and lab: evaluation conventions

**Reading:** may accept the width before evaluating the midpoint. Allows $a=b$ for an endpoint root.

**Lab:** requires $a<b$. Evaluate and record the accepted midpoint so `root == history[-1]`.

**Endpoint exception:** return the endpoint with zero midpoint evaluations and an empty history.

Use the lab contract when writing your tests.
:::::::


:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## An expected failure is a passing test

```python
import pytest
from roots import bisect

def test_invalid_bracket():
    with pytest.raises(ValueError):
        bisect(lambda x: x*x + 1, -1.0, 1.0)
```

`pytest.raises` passes only if the enclosed call raises the expected exception. Returning a number here is a failure of the solver's contract.

**Save:** `tests/test_roots.py`. **Run from `root-lab/`:** `python -m pytest`.

After module edits, restart the notebook kernel and rerun imports.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Harden: test the contract beyond one root

Use the [input and failure contract](#l8-contract-reference) as your checklist:

- Reject invalid endpoints, tolerances, iteration limits, and unusable function values.
- Distinguish a missing bracket from exhausted iterations or numerical stagnation.
- Check endpoint history and the midpoint to which the bound belongs.

**Check:** each rejection has an expected exception test. Exercise the relative tolerance before adding another method.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Add tests that could expose a mistake

| Case | Evidence to check |
| --- | --- |
| $x^2-2$ on $[1,2]$ | Root agrees with $\sqrt2$ within the stated absolute target |
| $x-1$ on $[1,2]$ | Endpoint root: zero midpoint evaluations and empty history |
| $x-0.9$ on $[0,1]$, `atol=0.25`, `rtol=0` | Return $0.75$ after two midpoint evaluations, not $0.5$ |
| $x^2+1$ on $[-1,1]$ | `ValueError`: no sign-changing bracket |
| $x^2-2$, one iteration, tight tolerance | `RuntimeError`: insufficient iterations |

Trace three brackets on paper; compare signs and widths with your code. Checking only the final root misses invariant failures.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Test the relative term

$$\tau_m=\mathrm{atol}+\mathrm{rtol}|m|.$$

Design a case where a nonzero `rtol` changes midpoint acceptance.

- Hold the function, bracket, and `atol` fixed; compare with `rtol=0`.
- Predict which run should stop first, then compare the histories.
- Explain why tests using only `rtol=0` cannot detect an ignored relative term.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## Extend only after bisection is hardened

After the required contract checks pass, add Newton or secant for the same equation.

- Plot $|x_k-\sqrt2|$ against iteration number.
- Count function and derivative evaluations separately.
- Try a second starting point; explain changed behavior.

A faster example is not a universal ranking. Next lecture develops convergence
conditions, failure modes, and safeguards.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

(l8-start-lab)=
## Build, test, and explain your module

Need a refresher? Use [bisection’s mathematical foundation](https://astrobytes-edu.github.io/comp521/mod2-part1-root-finding/#method-1-bisection),
[module boundaries](https://astrobytes-edu.github.io/comp521/python-functions-modules/#modules-as-reusable-scientific-boundaries),
and [documentation and tests](https://astrobytes-edu.github.io/comp521/python-functions-modules/#documentation-tests-and-public-type-hints).
Build from the invariant before comparing with the reading’s implementation; use today’s interface. Advanced root-finding sections are Lecture 9/reference.

Show your paper trace, passing behavior tests, and required failure checks. Explain what the stopping evidence establishes. Finish hardening bisection before starting an extension.

Keep your module and iteration evidence for Project 3. We continue root finding
in Lecture 9; the scientific project is posted next week.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching

## V · Reference for Lecture 9 and the lab

Keep the following material accessible for review and Lecture 9. The required lab contract is in the activity section above.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

(l8-taylor-reference)=
## A derivative from two nearby values

For sufficiently smooth $f$, Taylor expansion gives

$$f(x+h)=f(x)+hf'(x)+\frac{h^2}{2}f''(x)+O(h^3).$$

Subtract $f(x)$ and divide by $h\ne0$:

$$\frac{f(x+h)-f(x)}{h}=f'(x)+\frac{h}{2}f''(x)+O(h^2).$$

The leading truncation error is first order when $f''(x)\ne0$.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

## Static companion: the first secant

:::{figure} figures/secant.png
:alt: The secant through one and two intersects at four thirds.

$x_2=4/3$. Next use $x_1=2$ and $x_2=4/3$.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

## Stop or report failure?

| Evidence | Response |
| --- | --- |
| Zero computed residual | Return the sampled zero; distinguish computed from exact zero |
| Valid bracket sufficiently narrow | Return its midpoint |
| Small Newton/secant step | Inspect residual and stagnation |
| Invalid bracket, slope, or function value | Report the cause |
| Iteration limit; criterion unmet | Report non-convergence |

A solver should not disguise failure as an ordinary root.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

(l8-advanced)=
## Keep the model; add safeguards

**Question:** can we combine a fast proposal with a reliable fallback?

Bisection supplies interval evidence. Newton and secant supply model-based proposals.
Practical methods can use both.

This is an overview: identify the ingredients today. We will examine convergence and failure behavior in the next lectures.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

## The same Taylor idea extends to systems

For several unknowns, $F$ contains one residual per equation. The Jacobian records how each residual responds to each unknown: $J_{ij}=\partial F_i/\partial x_j$. Then

$$F(x+\Delta x)\approx F(x)+J(x)\Delta x.$$

Choose the step by solving

$$J(x)\Delta x=-F(x).$$

Solve this linear system for the correction $\Delta x$; do not explicitly form an inverse. The scalar Newton step is the one-equation version.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

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
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

## Prepared output: rescaling

Residuals: **1** and **1e−12**. Root error: **1** in both cases.

**Interpret:** why does scaling the residual leave the root location unchanged?

The reference root is available for this teaching example; a general solver usually cannot calculate its actual error.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-8 projector-slide lecture-teaching lecture-reference

## When a residual gives a bound

Suppose $f$ is continuously differentiable between $x$ and a root $r$, and a justified bound satisfies $|f'|\ge m>0$ throughout that interval.

The mean value theorem gives

$$|x-r|\le |f(x)|/m.$$

If the computed residual has error at most $\eta$, replace the numerator by $|\widehat f(x)|+\eta$. A derivative at one point alone is not the required interval bound.

Lecture 9 connects this with root sensitivity and nested numerical calculations.
:::::::
