---
title: "Lecture 6 · Trapezoids, Simpson, Modules, and Tests"
subtitle: "Block 2 · Week 3"
site:
  hide_toc: true
  hide_outline: true
kernelspec:
  name: python3
  display_name: Python 3
---

:::{projector-controls}
:id: lecture-06-controls
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Trapezoids, Simpson, modules, and tests

### Improve a local approximation, then make its implementation reusable

Last class we replaced the function on each panel with a constant. Today we
use a line and a quadratic, then organize and test the rectangle rule in a lab.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## The through-line

**Jump to:** [Trapezoid](#l6-trapezoid) · [Simpson](#l6-simpson) · [Modules and tests](#l6-modules) · [Sine lab](#l6-lab)

:::{div}
:class: lecture-through-line

1. Approximate the function on one panel.
2. Integrate that approximation.
3. Assemble a composite rule and explain its error order.
4. Put a reusable function in a module.
5. Write a test whose reference and tolerance have a stated basis.
:::

The same choices apply to many scientific integrands.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Today's question

How do better local approximations lead to better quadrature rules, and how
can we make those rules reusable and testable?

By the end of class, you should be able to:

- derive trapezoid and Simpson weights from local polynomials;
- explain their composite orders and smoothness conditions;
- organize a numerical function in an importable module;
- run `pytest` tests from the project root; and
- justify an accuracy assertion and test invalid inputs.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Recall · what a left rectangle retains

On a panel of width $h$,

$$\int_{x_i}^{x_i+h}f(x)\,dx
=h f(x_i)+\frac{h^2}{2}f'(x_i)+O(h^3).$$

The left rectangle keeps $h f(x_i)$ and omits the slope contribution.

**Predict:** if we use both endpoint heights and join them with a line, which
term can we capture? What kind of function would the new rule integrate exactly?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

(l6-trapezoid)=
## I · Trapezoids retain the local slope

What accuracy do we gain by connecting the two endpoint heights?

### Goals

- integrate a linear interpolant on one panel;
- assemble the endpoint and interior weights; and
- derive the local and composite error orders with Taylor expansion.

:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Integrate the line between the endpoints

With $s=x-x_i$ on $0\le s\le h$, the interpolating line is

$$\ell(s)=f(x_i)+\frac{s}{h}\bigl[f(x_{i+1})-f(x_i)\bigr].$$

Its area is

$$T_i=\int_0^h\ell(s)\,ds
=\frac{h}{2}\bigl[f(x_i)+f(x_{i+1})\bigr].$$

This is the trapezoidal rule on one panel. A linear function is reproduced
exactly by its endpoint interpolant.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Interior nodes belong to two neighboring trapezoids

Adding the panel contributions gives

$$T_n=h\left[\frac12 f(x_0)+\sum_{i=1}^{n-1}f(x_i)
+\frac12 f(x_n)\right].$$

| Node | Number of neighboring panels | Composite weight |
| --- | --- | --- |
| $x_0$ | 1 | $h/2$ |
| $x_1,\ldots,x_{n-1}$ | 2 | $h$ |
| $x_n$ | 1 | $h/2$ |

There are $n$ panels and $n+1$ sampled heights. The weights carry the units of
the integration variable.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Taylor expansion identifies the trapezoid error

Expand around the left endpoint:

$$T_i=h f_i+\frac{h^2}{2}f'_i+\frac{h^3}{4}f''_i+O(h^4),$$

whereas the exact panel integral is

$$I_i=h f_i+\frac{h^2}{2}f'_i+\frac{h^3}{6}f''_i+O(h^4).$$

Therefore $T_i-I_i=\frac{h^3}{12}f''_i+O(h^4)$.
The local error is $O(h^3)$; summing over a fixed interval gives $O(h^2)$.

**Predict:** sine is concave down on $[0,\pi/2]$. Does the chord lie above or
below the curve, and what sign should $T_n-I$ have?
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Compare the local approximations

```{code-cell} python
:tags: [remove-input, remove-output]

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})
x = np.linspace(0.0, 1.0, 301)
# The quadratic interpolates exp(x) at 0, 1/2, and 1.
quadratic = (2*(x-0.5)*(x-1)
             - 4*np.exp(0.5)*x*(x-1) + 2*np.exp(1)*x*(x-0.5))
approximations = (np.ones_like(x), 1+(np.e-1)*x, quadratic)
fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=True, layout="constrained")
for ax, approximation, title in zip(axes, approximations, ("Constant", "Linear", "Quadratic")):
    ax.plot(x, np.exp(x), color="#122b38", lw=2.5, label=r"$e^x$")
    ax.plot(x, approximation, "--", color="#D55E00", lw=2, label="Interpolant")
    ax.fill_between(x, approximation, alpha=0.15, color="#0072B2")
    ax.set(title=title, xlabel=r"$x$ (dimensionless)")
    ax.grid(alpha=0.2)
axes[0].set_ylabel("Function value (dimensionless)")
axes[0].legend(fontsize=11)
fig.savefig("lecture-06-interpolants.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-06-interpolants.png
:alt: Three panels compare the exponential on zero to one with a left-endpoint constant, an endpoint line, and a quadratic through zero, one half, and one. Shading shows the area under each approximating polynomial.

Quadrature integrates the approximating polynomial. The difference between
that polynomial and the function determines the quadrature error.
:::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Reference · trapezoid geometry and error

| Feature | Consequence |
| --- | --- |
| Line through two endpoints | Exact for linear functions in exact arithmetic |
| Interior node shared by two panels | Full interior weight, half endpoint weights |
| Leading local error proportional to $h^3 f''$ | Composite error bounded by a constant times $h^2$ |
| Concave-down integrand | Chords underestimate the area |

**Rule:** use curvature to predict the error sign before running the calculation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

(l6-simpson)=
## II · Simpson uses a quadratic and symmetry

Why can an integral gain accuracy beyond the pointwise degree of its interpolant?

### Goals

- derive weights $1,4,1$ across a pair of panels;
- explain why composite Simpson requires an even panel count;
- use symmetry to explain cubic exactness; and
- state the smoothness assumptions behind fourth-order accuracy.

:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Fit a quadratic across two panels

Let $m$ be the midpoint of a two-panel interval $[m-h,m+h]$.
Write its interpolating quadratic as

$$P(s)=A+Bs+Cs^2,\qquad s=x-m.$$

The three sample values determine the coefficients:

$$A=f(m),\qquad
C=\frac{f(m-h)-2f(m)+f(m+h)}{2h^2}.$$

The integral of $Bs$ over $[-h,h]$ is zero. Therefore

$$\int_{-h}^{h}P(s)\,ds=2hA+\frac{2h^3}{3}C.$$
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## The coefficients give Simpson's weights

Substitute $A$ and $C$ into the integral:

$$S_{\rm pair}=\frac{h}{3}\bigl[f(m-h)+4f(m)+f(m+h)\bigr].$$

Here $h$ is the width of one panel. The pair has width $2h$.

**Check the units and weights:** for $f(x)=1$, the result must be the interval
length, $2h$. The weights sum to $(h/3)(1+4+1)=2h$.

**Predict:** is a cubic integrated exactly? A quadratic interpolant does not
reproduce a cubic point by point, so explain your reasoning about its integral.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Symmetry cancels the cubic contribution to the error

Expand a smooth function about the midpoint:

$$f(m+s)=f_m+s f'_m+\frac{s^2}{2}f''_m
+\frac{s^3}{6}f'''_m+\frac{s^4}{24}f^{(4)}_m+\cdots.$$

Both the symmetric integral and Simpson's symmetric weights cancel odd terms.
The constant and quadratic contributions agree. The first possible mismatch
is the fourth-derivative term.

:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Derive the Simpson error coefficient

For the fourth-order term, the integral contributes
$h^5 f^{(4)}_m/60$ and Simpson contributes $h^5 f^{(4)}_m/36$.
Their difference is $(1/60-1/36)h^5 f^{(4)}_m=-h^5 f^{(4)}_m/90$.
This identifies the coefficient. The error theorem makes the remainder exact:
for $f\in C^4$ on the pair, there is a point $\xi$ in it such that

$$I_{\rm pair}-S_{\rm pair}=-\frac{h^5}{90}f^{(4)}(\xi).$$

The paired local error is $O(h^5)$ and the composite error is $O(h^4)$.
For a cubic, the fourth derivative vanishes: Simpson is exact in exact arithmetic.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Pair the panels to build composite Simpson

$$S_n=\frac{h}{3}\left[f(x_0)
+4\sum_{\substack{i=1\\i\text{ odd}}}^{n-1}f(x_i)
+2\sum_{\substack{i=2\\i\text{ even}}}^{n-2}f(x_i)+f(x_n)\right].$$

- Endpoint weights: 1.
- Odd-index interior weights: 4.
- Even-index interior weights: 2 because they join adjacent pairs.
- Multiply the sum by $h/3$.

The panel count $n$ must be positive and even for this composite rule.
An odd count is an invalid input, not a reason to silently change the grid.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Translate the weights into array slices

Suppose `y = f(nodes)` contains the $n+1$ endpoint heights:

| Expression | Selected values |
| --- | --- |
| `y[0]`, `y[-1]` | Endpoints |
| `y[1:-1]` | All interior heights, for trapezoid |
| `y[1:-1:2]` | Odd-index interior heights, for Simpson |
| `y[2:-1:2]` | Even-index interior heights, for Simpson |

For $n=4$, write the five weights on paper. Check that neither endpoint appears
inside an interior sum. The complete implementations are your next exercise.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Compare the rectangle samples

Same integrand, same six panels: $f(x)=e^{-x/2}\cos(2x)+1$ on $[0,2]$.

```{code-cell} python
:tags: [remove-input, remove-output]

# Plot local interpolants; this is an illustration, not a quadrature library.
from numpy.polynomial import Polynomial
plot_edges = np.linspace(0.0, 2.0, 7)
plot_h = plot_edges[1] - plot_edges[0]
plot_f = lambda x: np.exp(-x/2) * np.cos(2*x) + 1
primitive = lambda x: np.exp(-x/2) * (-0.5*np.cos(2*x) + 2*np.sin(2*x)) / 4.25
plot_exact = 2 + primitive(2) - primitive(0)
for pair, names in enumerate((("Left", "Midpoint"), ("Trapezoid", "Simpson"))):
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.5), layout="constrained")
    for ax, name, color in zip(axes, names, ("#0072B2", "#D55E00")):
        xx = np.linspace(0, 2, 501)
        ax.plot(xx, plot_f(xx), color="#122b38", lw=2)
        area = 0.0
        if pair == 0:
            samples = plot_edges[:-1] + (plot_h/2 if name == "Midpoint" else 0)
            heights = plot_f(samples)
            ax.bar(plot_edges[:-1], heights, width=plot_h, align="edge",
                   color=color, edgecolor=color, alpha=0.25)
            area = plot_h * np.sum(heights)
        else:
            samples = plot_edges
            degree = 1 if name == "Trapezoid" else 2
            for i in range(0, 6, degree):
                nodes = plot_edges[i:i+degree+1]
                poly = Polynomial.fit(nodes, plot_f(nodes), degree)
                xx = np.linspace(nodes[0], nodes[-1], 101)
                ax.fill_between(xx, 0, poly(xx), color=color, alpha=0.25)
                ax.plot(xx, poly(xx), color=color)
                integral = poly.integ()
                area += integral(nodes[-1]) - integral(nodes[0])
        ax.plot(samples, plot_f(samples), "o", color=color)
        ax.set(xlabel="x (dimensionless)", ylabel="f(x)",
               title=f"{name}: {len(samples)} samples\nAbsolute error {abs(area-plot_exact):.3g}")
        ax.tick_params(labelsize=13)
    fig.savefig(f"lecture-06-geometry-{pair}.png", dpi=160)
    plt.close(fig)
```

:::{figure} lecture-06-geometry-0.png
:alt: Left and midpoint rectangles on the same six panels; their sample positions differ. The midpoint estimate has a smaller absolute error on this grid.

**Explain:** why does midpoint sampling give the smaller error on this grid?
:::
:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Compare the endpoint interpolants

:::{figure} lecture-06-geometry-1.png
:alt: Trapezoid chords and paired Simpson quadratics use the same seven endpoints. The quadratic tracks this integrand more closely on these six panels.

**Explain:** why do both rules use seven heights for six panels?
:::

[Reference: all four methods and numerical values](reading-quadrature-geometry.webp).

:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Explain the sample count

On this grid, Simpson has the smallest error; midpoint beats trapezoid.
One grid does not establish convergence order or a universal ranking.

**Explain:** why do the endpoint rules need seven sampled heights for six
panels? Where do neighboring Simpson pairs reuse a height?
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Orders need a smoothness condition

For equal panel widths on a fixed interval:

| Rule | Sufficient derivative bound | Composite error bound |
| --- | --- | --- |
| Left rectangle | $M_1=\max\lvert f'\rvert$ | $(b-a)hM_1/2$ |
| Trapezoid | $M_2=\max\lvert f''\rvert$ | $(b-a)h^2M_2/12$ |
| Simpson | $M_4=\max\lvert f^{(4)}\rvert$ | $(b-a)h^4M_4/180$ |

Assume the corresponding derivatives are continuous on $[a,b]$, with $a<b$.
The bounds concern exact-arithmetic quadrature, not floating-point rounding.

When a needed derivative is unbounded or discontinuous, the usual error theorem
does not supply that guarantee. We will investigate such an example later.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Reference · a corner changes the error pattern

**Interpret:** why does the corner in $g(x)=e^x+|x-0.2|$ invalidate the usual
Simpson bound on $[0,1]$? Explain the effect of splitting at 0.2.

```{code-cell} python
:tags: [remove-input, remove-output]

# Library quadrature produces this illustration; students write their own rules.
from scipy.integrate import simpson as reference_simpson
corner = 0.2
corner_f = lambda x: np.exp(x) + np.abs(x-corner)
corner_exact = np.expm1(1) + (corner**2 + (1-corner)**2)/2
corner_ns = 2**np.arange(2, 11)
corner_errors = [[], [], []]
for panels in corner_ns:
    grid = np.linspace(0, 1, panels+1)
    left = np.linspace(0, corner, panels//2+1)
    right = np.linspace(corner, 1, panels//2+1)
    # Sample the shared endpoint once and reuse its value.
    values = corner_f(np.concatenate((left, right[1:])))
    split_area = (reference_simpson(values[:panels//2+1], x=left)
                  + reference_simpson(values[panels//2:], x=right))
    corner_errors[0].append(abs(reference_simpson(np.exp(grid), x=grid)-np.expm1(1)))
    corner_errors[1].append(abs(reference_simpson(corner_f(grid), x=grid)-corner_exact))
    corner_errors[2].append(abs(split_area-corner_exact))
fig, axes = plt.subplots(1, 2, figsize=(12, 3.7), layout="constrained")
xx = np.linspace(0, 1, 501)
axes[0].plot(xx, corner_f(xx), color="#122b38", lw=2)
axes[0].axvline(corner, color="#D55E00", ls="--")
axes[0].set(xlabel="x", ylabel="g(x)", title="Split at the corner")
for errors, label, color in zip(corner_errors, ("Smooth", "Corner", "Split corner"),
                                ("#0072B2", "#D55E00", "#009E73")):
    axes[1].loglog(corner_ns+1, errors, "o-", label=label, color=color)
axes[1].set(xlabel="Distinct samples", ylabel="Absolute error")
axes[1].legend(fontsize=13)
axes[1].grid(alpha=0.2)
fig.savefig("lecture-06-corner.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-06-corner.png
:alt: The left panel shows a corner at 0.2, marked by a dashed vertical line. The right log-log panel compares smooth exponential, unsplit corner, and split corner Simpson errors. Splitting restores fourth-order decay on this sequence, while the unsplit corner has roughly second-order decay.
:width: 900px

Compare the smooth, unsplit, and split error curves at the same total panel count.
:::

[Open full-size figure](reading-quadrature-kink.png).

:::::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Reference · why splitting at a corner helps

Each calculation uses $n+1$ distinct samples. The split rule uses half the
panels on each side and reuses the shared endpoint.

Each side is smooth: the quadratic no longer crosses the corner.
This previews the reading's investigation. Grid alignment can
cancel an error term, so an observed slope alone does not prove smoothness.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Reference · composite Simpson

| Feature | Meaning |
| --- | --- |
| `n` positive and even | Every panel belongs to a pair |
| `n + 1` heights | Both boundaries and all interior nodes are sampled |
| Weights `1, 4, 2, ..., 4, 1` | Pair weights accumulated across the grid |
| Overall factor `h / 3` | `h` is one panel's width, not a pair's width |
| Exact cubic integral | A check of weights and indexing, up to rounding |

**Rule:** polynomial exactness and measured convergence order are different checks.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

(l6-modules)=
## III · A module gives a function an importable home

How can a notebook and a test call the same numerical implementation?

### Goals

- separate method definitions from analysis and tests;
- import a local module and account for cached notebook imports;
- recognize how pytest finds and runs tests; and
- translate a stated tolerance into a `pytest.approx` assertion.

:::

:::::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Give each file one role

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

```text
quadrature-lab/
├── integrate.py
├── tests/
│   └── test_integrate.py
└── analysis.ipynb
```


::::

::::{div}
:class: lecture-column

- `integrate.py` defines numerical methods.
- The notebook imports them, makes figures, and explains results.
- Test files import them and check specified behavior.

A notebook can contain assertions and be tested by execution. Modules make
functions easier to import and test independently of notebook state.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Imports connect the files

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

In a notebook located in the lab directory:

```python
import numpy as np
from integrate import rectangle

estimate = rectangle(np.sin, 0.0, np.pi/2, 100)
```


::::

::::{div}
:class: lecture-column

Python executes a module's top-level statements when it first imports it in
a process. Keep demonstration runs and plotting out of the module's top level.

After editing the module, restart the notebook kernel and run from the top.
Importing again does not normally reload a module already in memory.
::::
:::::
:::::::

:::::::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## What `pytest` does

:::::{div}
:class: lecture-two-column

::::{div}
:class: lecture-column

`pytest` discovers test functions, calls them, and reports failed assertions
and unexpected exceptions.

```python
def test_example():
    result = 2 + 3
    assert result == 5
```


::::

::::{div}
:class: lecture-column

For this lab, use files named `test_*.py` and functions named `test_*`.
An assertion should test a behavior you can explain.

Run from the directory containing `integrate.py`:

```bash
python -m pytest
```

If pytest is missing, install it in the same course environment with
`python -m pip install pytest`, then rerun the command.
::::
:::::
:::::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Carry `rtol` and `atol` into tests carefully

NumPy uses `rtol` and `atol`. `pytest.approx` uses `rel` and `abs`:

```python
assert actual == pytest.approx(expected, rel=0.0, abs=error_bound)
```

For finite scalar values and both allowances explicitly supplied,
`pytest.approx` permits a discrepancy up to

$$\max(\mathrm{abs},\mathrm{rel}\,\lvert\mathrm{expected}\rvert).$$

NumPy adds its allowances. These APIs therefore differ when both allowances
are nonzero. With `rel=0.0`, our test has one explicit absolute criterion.

Source: [pytest `approx` documentation](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx).
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Reference · modules and tests

| Pattern | Purpose |
| --- | --- |
| `from integrate import rectangle` | Import the shared implementation |
| `tests/test_integrate.py` | A discoverable home for lab tests |
| `def test_rectangle_sine():` | One named behavior check |
| `pytest.approx(reference, rel=0.0, abs=bound)` | An explicit absolute comparison |
| `python -m pytest` | Run tests using this Python environment |

**Rule:** a test should expose a plausible mistake, not repeat the implementation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

(l6-lab)=
## IV · Lab: rectangle integration of sine

Can another file import your rule and verify a claim about its result?

### Goals

- complete an importable rectangle module;
- justify a sine-integral test with a derivative bound;
- test an invalid-input contract; and
- interpret a deliberate failure without weakening a justified criterion.

:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Predict · the sine integral and the module contract

Work with a partner to discuss the design; write and run your own implementation.

$$\int_0^{\pi/2}\sin x\,dx=1.$$

Before typing:

1. Sketch the curve and two left rectangles.
2. Predict whether the result is above or below 1.
3. State which endpoint is omitted from the sampled heights.
4. Write the input and output contract for `rectangle(f, a, b, n)`.

Use the known rectangle mathematics to concentrate on modules and tests.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Lab step 1 · Create `integrate.py`

Start with this skeleton and complete it using Lecture 5:

```python
import numpy as np

def rectangle(f, a, b, n):
    """Approximate an integral using n left rectangles.

    f accepts and returns matching arrays of finite values.
    a and b are finite scalar limits; n is a positive integer.
    Return one float. Invalid n raises ValueError.
    """
    # Validate n, excluding bool and non-integer values.
    # Compute the panel width and n left endpoints.
    # Evaluate f at those endpoints and return the weighted sum.
    raise NotImplementedError("Complete the rectangle rule")
```

The placeholder is intentional; replace it with your implementation.
Do not hard-code `np.sin` inside the rule.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Lab step 2 · Choose the tolerance before running the test

Lecture 5 established

$$\lvert I-L_n\rvert\le\frac{(b-a)^2}{2n}M_1.$$

For $\sin x$ on $[0,\pi/2]$, $M_1=\max\lvert\cos x\rvert=1$.
At $n=100$, the bound is $\pi^2/800\approx0.01234$.

Use this absolute bound for the known-integral test. The sine result has
room below this conservative bound, much larger than rounding effects here.

**Explain:** a correct left-rectangle rule at $n=100$ fails a $10^{-12}$
accuracy demand here. Why is that a tolerance problem rather than evidence
of an implementation bug?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Lab step 3 · Write the known-integral test

Save this in `tests/test_integrate.py`:

```python
import numpy as np
import pytest
from integrate import rectangle

def test_rectangle_sine():
    n = 100
    estimate = rectangle(np.sin, 0.0, np.pi/2, n)
    error_bound = np.pi**2 / (8*n)
    assert np.isfinite(estimate)
    assert estimate < 1.0  # increasing sine: left rectangles underestimate
    assert estimate == pytest.approx(1.0, rel=0.0, abs=error_bound)
```

Run `python -m pytest`. If the test fails, read the actual value and expected
range before changing any code or tolerance.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Lab step 4 · Check invalid inputs

Append this test to the same file:

```python
@pytest.mark.parametrize("bad_n", [0, -2, 2.5, True])
def test_rectangle_rejects_invalid_panel_count(bad_n):
    with pytest.raises(ValueError, match="positive integer"):
        rectangle(np.sin, 0.0, np.pi/2, bad_n)
```

`parametrize` runs the function once for each listed value. `raises` checks the
exception type; `match` checks the message for the named problem.

If validation is missing, a division error is not the required `ValueError`.
An error message is part of making the function usable.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Lab step 5 · Make a failure informative

Temporarily change the accuracy tolerance to `abs=1e-12`, leaving `rel=0.0`.
Run the test and read the discrepancy it reports.

- Is the calculation inconsistent with the first-order bound?
- Or is this new accuracy demand unsupported at $n=100$?

Restore the justified bound, rerun the tests, and import the rule into a clean
notebook. Print the estimate and its absolute error.

If time remains, double `n` and compare the error ratio with the first-order
prediction. The bound test alone does not establish convergence order.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## What the lab establishes

| Evidence | Supported claim | Remaining limitation |
| --- | --- | --- |
| Imported function runs | This module is usable from this environment | Other input contracts still need checking |
| Sine test passes | This case meets a justified bound and has the expected sign | One case cannot establish general correctness |
| Invalid counts raise | The listed invalid inputs fail as specified | Other invalid inputs were not tested |
| Error ratio approaches 2 | This sequence is consistent with first-order error | The conclusion is local to the tested regime |

Testing a function, measuring its convergence, and validating a physical model
answer different questions.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Documentation for the next question

| Resource | Use it for |
| --- | --- |
| [Python modules tutorial](https://docs.python.org/3/tutorial/modules.html) | Imports and module behavior |
| [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html) | Test discovery and a first run |
| [pytest assertions](https://docs.pytest.org/en/stable/how-to/assert.html) | Failure reports and expected exceptions |
| [pytest `approx`](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx) | Absolute and relative comparison semantics |

Read a failure report alongside the test's stated claim and the function's
contract. Check the documented API before changing the implementation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Exit check

1. Why does the trapezoid rule have half weights at the two endpoints?
2. Why must composite Simpson use an even panel count?
3. Why can Simpson integrate cubics exactly using quadratic interpolation?
4. Where do reusable functions, figures, and tests belong?
5. Why did the lab use `rel=0.0` and an absolute error bound?

:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll lecture-teaching

## Carry forward

Implement trapezoid and Simpson with the same callable interface, then
measure their convergence. Use a cubic integral as an independent Simpson check.

Your notebook imports the methods and explains their results. Your tests make
specific contracts executable. Next class we will use error measurements to
assess convergence and choose how much work an accuracy target requires.
:::
