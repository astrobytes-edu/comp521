---
title: "Lecture 5 · Approximation, Errors, and Quadrature"
subtitle: "Block 2 · Week 3"
site:
  hide_toc: true
  hide_outline: true
kernelspec:
  name: python3
  display_name: Python 3
---

:::{projector-controls}
:id: lecture-05-controls
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Approximation, errors, and quadrature

### From continuous mathematics to finite calculations

A computer stores finitely many digits and evaluates finitely many operations.
Calculus defines derivatives through limits and integrals through continuous
accumulation. Today we connect these descriptions.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## The through-line

:::{div}
:class: lecture-through-line

1. Represent a number.
2. Approximate a function locally.
3. Identify the omitted terms.
4. Measure an error and choose a comparison tolerance.
5. Approximate an integral with a sum.
:::

State the approximation before interpreting its numerical error.
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Today's question

How do finite representations and finite approximations affect the calculations
we make from continuous mathematics?

By the end of class, you should be able to:

- distinguish representation, arithmetic rounding, and truncation;
- use a Taylor remainder to explain a leading error term;
- explain why a smaller step can hurt a finite difference;
- choose `atol` and `rtol` for a stated comparison; and
- implement left-rectangle quadrature and check its first-order prediction.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## I · Numbers and operations have finite precision

### Question

What changes between a real number on paper and a number stored in a computer?

### You will leave this section able to

- distinguish representable values from rounded approximations;
- relate absolute spacing to the scale of a number; and
- separate representation and arithmetic errors from method truncation.

**Through-line focus:** mathematical value $\rightarrow$ stored value and operation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Predict · which sums are exactly represented?

In Block 1, we saw that a mathematical expression, its Python implementation,
and its floating-point result are distinct things.

**Predict:** will both of these print `True`?

```{code-cell} python
import numpy as np

print(0.1 + 0.2 == 0.3)
print(0.5 + 0.25 == 0.75)
print(f"0.1 + 0.2 = {0.1 + 0.2:.17g}")
```

The second sum uses fractions with finite binary representations. The first
sum rounds both represented inputs and the arithmetic result.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Spacing depends on the scale of the number

```{code-cell} python
for value in (1.0, 1.0e8):
    spacing = np.spacing(value)
    print(f"value={value:.1e}, next-float spacing={spacing:.3e}")

print("binary64 epsilon:", np.finfo(np.float64).eps)
```

Machine epsilon is the gap from `1.0` to the next larger binary64 number.
It is not a universal absolute error or a guarantee about a calculation.

**Explain:** why would one fixed absolute tolerance mean different things at
scales of 1 and $10^8$?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Three sources of numerical discrepancy

| Source | Example | What we can change |
| --- | --- | --- |
| Representation | Store a decimal fraction in binary | Precision; scaling when appropriate |
| Rounding during arithmetic | Subtract nearly equal approximations | Algebraic formulation; precision |
| Truncation of a mathematical procedure | Replace a derivative by a finite difference | Step size; approximation order |

Measurement uncertainty and model error are additional questions. They are not
automatically measured by any of these numerical errors.

An accurate implementation can still calculate an inadequate model.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · finite precision

| Pattern | What it reveals |
| --- | --- |
| `np.finfo(np.float64).eps` | Spacing immediately above 1 for binary64 |
| `np.spacing(value)` | Local floating-point spacing |
| `f"{value:.17g}"` | More digits than a short default display may show |
| `np.isfinite(value)` | Whether the value is neither infinity nor `nan` |

**Rule:** the precision of a representation is not the accuracy of a calculation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## II · Taylor expansion describes a local approximation

### Question

How much of a function can we reconstruct from its value and derivatives at one point?

### You will leave this section able to

- construct constant, linear, and quadratic local approximations;
- interpret the remainder and an order statement;
- predict an error ratio under refinement; and
- derive a forward difference and explain its rounding tradeoff.

**Through-line focus:** local shape $\rightarrow$ approximation and omitted terms.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Build the polynomial one derivative at a time

Near $x_0$, write $x=x_0+h$. Taylor's theorem gives

$$
f(x_0+h)=f(x_0)+h f'(x_0)+\frac{h^2}{2!}f''(x_0)
+\cdots+\frac{h^m}{m!}f^{(m)}(x_0)+R_{m+1}.
$$

Each derivative describes another aspect of the local shape.

- Constant: the value at the expansion point.
- Linear: value and slope.
- Quadratic: value, slope, and curvature.

The equality includes $R_{m+1}$, the part the polynomial does not capture.
Dropping the remainder gives an approximation, $f(x_0+h)\approx P_m(h)$.

For the remainder formula used here, assume $f$ has continuous derivatives
through order $m+1$ on the interval between $x_0$ and $x_0+h$.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Why these coefficients reproduce the local shape

Start with an unknown polynomial in the displacement $h$:

$$P_m(h)=a_0+a_1h+a_2h^2+\cdots+a_mh^m.$$

Choose its derivatives at $h=0$ to match those of $f$ at $x_0$:

| Match | Condition | Coefficient |
| --- | --- | --- |
| Value | $P_m(0)=f(x_0)$ | $a_0=f(x_0)$ |
| Slope | $P_m'(0)=f'(x_0)$ | $a_1=f'(x_0)$ |
| Curvature | $P_m''(0)=f''(x_0)$ | $2a_2=f''(x_0)$ |
| Derivative $k\le m$ | $P_m^{(k)}(0)=f^{(k)}(x_0)$ | $k!a_k=f^{(k)}(x_0)$ |

Differentiating $h^k$ exactly $k$ times produces $k!$. That is why the
coefficient is $f^{(k)}(x_0)/k!$.

Matching at one point does not make the functions identical everywhere.
Taylor's theorem tells us how to express the remaining difference.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Work out a local model for the exponential

For $f(x)=e^x$ at $x_0=0$, every derivative equals 1:

$$P_0(h)=1,\qquad P_1(h)=1+h,\qquad P_2(h)=1+h+\frac{h^2}{2}.$$

**Predict:** which approximation should be best near zero? Does that promise
the same accuracy one unit away?

```{code-cell} python
for step in (0.5, 0.1, 0.01):
    exact = np.exp(step)
    approximations = (1.0, 1.0 + step, 1.0 + step + step**2 / 2)
    errors = [abs(exact - value) for value in approximations]
    print(f"h={step:.2f}: errors P0, P1, P2 =", np.array(errors))
```
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## See the value, slope, and curvature

```{code-cell} python
:tags: [remove-input, remove-output]

import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 14})
x_plot = np.linspace(-1.0, 1.0, 401)
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(x_plot, np.exp(x_plot), color="#122b38", lw=3, label=r"$e^x$")
ax.plot(x_plot, np.ones_like(x_plot), ":", color="#0072B2", lw=2, label=r"$P_0$")
ax.plot(x_plot, 1 + x_plot, "--", color="#D55E00", lw=2, label=r"$P_1$")
ax.plot(x_plot, 1 + x_plot + x_plot**2/2, "-.", color="#009E73", lw=2, label=r"$P_2$")
ax.plot(0, 1, "ko", ms=7)
ax.set(xlabel=r"$x$ (dimensionless)", ylabel="Function value (dimensionless)")
ax.grid(alpha=0.2)
ax.legend(ncol=2)
fig.savefig("lecture-05-taylor.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-05-taylor.png
:alt: The exponential and its constant, linear, and quadratic Taylor polynomials agree at zero and separate away from zero. The quadratic tracks the curvature most closely near zero. Line styles and labels distinguish the curves.

Each polynomial uses information at the same expansion point, $x_0=0$.
:::

**Explain:** what feature does the quadratic capture that the line cannot?
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## The remainder tells us what we omitted

For some $\xi$ between $x_0$ and $x_0+h$,

$$R_{m+1}=\frac{f^{(m+1)}(\xi)}{(m+1)!}h^{m+1}.$$

If the derivative is bounded there, the remainder is $O(h^{m+1})$.
This means there is a constant $C$ such that

$$\lvert R_{m+1}\rvert\le C\lvert h\rvert^{m+1}$$

for sufficiently small $h$ in the stated region.

This is a finite polynomial plus a remainder. We do not need an infinite
Taylor series to converge to use this local result.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## More terms: accuracy costs arithmetic

For $e^h$ with $0\le h\le r$, every derivative is bounded by $e^r$, so

$$|e^h-P_m(h)|\le e^r\frac{h^{m+1}}{(m+1)!}.$$

For a fixed positive $h$, adding terms reduces the truncation error in this
example. Farther from the expansion point, more terms are needed for the same
absolute accuracy.

```{code-cell} python
:tags: [remove-input, remove-output]

taylor_degrees = np.arange(9)
taylor_cost_errors = {}
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
for offset, color, marker in ((0.5, "#0072B2", "o"), (2.0, "#D55E00", "s")):
    term = total = 1.0
    values = [total]
    for k in range(1, 9):
        term = term * offset / k
        total = total + term
        values.append(total)
    taylor_cost_errors[offset] = np.abs(np.exp(offset) - np.array(values))
    ax.semilogy(taylor_degrees, taylor_cost_errors[offset], marker=marker,
                color=color, lw=2, label=fr"$h={offset}$")
ax.set(xlabel="Polynomial degree m (m + 1 terms)",
       ylabel="Absolute error (dimensionless)", xticks=taylor_degrees)
ax.grid(alpha=0.2, which="both")
ax.legend(title="Distance from expansion point")
fig.savefig("lecture-05-taylor-cost.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-05-taylor-cost.png
:alt: Absolute exponential approximation error decreases from degree zero through eight. At every degree the error at h equals two is larger than at h equals one half; circles and squares distinguish the two curves.

Both approximations use derivatives at zero. More terms improve these results,
but evaluating those terms requires additional operations.
:::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Count the work before claiming a speed improvement

For this exponential polynomial, reuse the previous term:

```python
term = total = 1.0           # Start with the constant term, P0 = 1.
for k in range(1, m + 1):    # Add terms 1 through m; stop is excluded.
    term = term * h / k      # One multiplication and one division.
    total = total + term     # One addition accumulates the next term.
```

| Degree $m$ | Terms retained | Arithmetic operations in this loop |
| --- | --- | --- |
| 2 | 3 | 6 |
| 4 | 5 | 12 |
| 8 | 9 | 24 |

This counts scalar arithmetic, excluding loop overhead; it is not a timing
measurement. For a general function, obtaining derivatives can add substantial
cost. Library functions such as `np.exp` use their own optimized algorithms.

**Decision:** choose enough terms for a justified error target. More terms do
not always improve a general function's approximation at a fixed point, and
floating-point rounding can eventually limit improvement even here.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## An order predicts a refinement ratio

If the leading error is nonzero and dominates,

$$E(h)\approx C h^q,\qquad E(h/2)\approx \frac{E(h)}{2^q}.$$

| Leading order $q$ | Error after halving $h$ |
| --- | --- |
| 1 | Approximately one half |
| 2 | Approximately one quarter |
| 4 | Approximately one sixteenth |

An $O(h^q)$ bound alone does not establish an exact slope. Cancellation can
remove a leading term, and rounding can obscure it.

**Predict:** if a first-order error is $0.02$, what error do you expect after
halving $h$, while the same leading term dominates?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Taylor expansion gives a finite difference

Start with

$$f(x+h)=f(x)+h f'(x)+\frac{h^2}{2}f''(x)+O(h^3).$$

Subtract $f(x)$ and divide by $h\ne0$:

$$\frac{f(x+h)-f(x)}{h}
=f'(x)+\frac{h}{2}f''(x)+O(h^2).$$

The forward difference has a leading truncation error of order $h$ when
$f''(x)\ne0$. We can calculate it without taking a limit in code.

**Predict:** does this imply that the smallest representable step is best?
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Run · smaller steps eventually stop helping

For $f(x)=e^x$ at $x=0$, the exact derivative is 1.

```{code-cell} python
# arange(1, 17) makes the integer array [1, 2, ..., 16]; 17 is excluded.
# Array arithmetic produces all step sizes: 10^-1, 10^-2, ..., 10^-16.
steps = 10.0 ** (-np.arange(1, 17))
# Vectorization: exp, subtraction, and division act element by element.
forward = (np.exp(steps) - 1.0) / steps
# np.abs takes each absolute value: compare every estimate with f'(0) = 1.
derivative_errors = np.abs(forward - 1.0)

# [::3] selects every third entry; zip pairs matching h, estimate, and error.
for step, value, error in zip(steps[::3], forward[::3], derivative_errors[::3]):
    print(f"h={step:.0e}: derivative={value:.8f}, error={error:.3e}")
```

```{code-cell} python
:tags: [remove-input, remove-output]

fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
positive = derivative_errors > 0
ax.loglog(steps[positive], derivative_errors[positive], "o-", color="#0072B2", label="Computed absolute error")
ax.loglog(steps, steps/2, "--", color="#D55E00", label=r"Leading truncation term $h/2$")
ax.set(xlabel=r"$h$ (dimensionless)", ylabel="Derivative error (dimensionless)")
ax.grid(alpha=0.2, which="both")
ax.legend()
fig.savefig("lecture-05-difference-error.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-05-difference-error.png
:alt: On logarithmic axes, the forward-difference error decreases as h is reduced from one tenth, then becomes irregular and increases for very small h. A dashed h over two line shows the truncation prediction.

Read toward the left for smaller steps. Exact printed values depend on the
floating-point implementation; the truncation prediction does not include rounding.
:::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Why two small errors can produce a larger one

The numerator subtracts values close to 1. Their absolute representation and
evaluation errors may be small compared with 1, but large compared with the
small difference. Division by $h$ amplifies that discrepancy.

A useful local model for this example is

$$E(h)\ \text{of size}\ C_1h+C_2\frac{\epsilon_{\rm mach}}{h}.$$

The constants depend on the function, point, and implementation. This model
explains competing trends; it does not give a universal best step size.

For this particular expression, `np.expm1(h) / h` avoids subtracting 1 from
a rounded exponential. Stable algebra can change the rounding behavior while
leaving the truncation order unchanged.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · Taylor approximation and error order

| Statement | Interpretation |
| --- | --- |
| $f(x_0+h)=P_m(h)+R_{m+1}$ | An approximation plus its remainder |
| $R_{m+1}=O(h^{m+1})$ | A local bound under the stated smoothness conditions |
| $E(h)\approx Ch^q$ | A dominant, nonzero error term predicts a refinement ratio |
| $E(h)/E(h/2)\approx2^q$ | An observable to compare with that prediction |

**Rule:** state the region and assumptions before interpreting an observed order.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## III · Measure the error before deciding what is acceptable

### Question

What does it mean for a result to agree with a reference closely enough?

### You will leave this section able to

- compute absolute and relative discrepancies;
- state the units and roles of `atol` and `rtol`;
- handle a zero or very small reference deliberately; and
- justify a tolerance independently of whether a test passes.

**Through-line focus:** discrepancy $\rightarrow$ a stated comparison criterion.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Absolute and relative errors answer different questions

For a computed value $Q$ and a reference $Q_\star$,

$$E_{\rm abs}=\lvert Q-Q_\star\rvert,\qquad
E_{\rm rel}=\frac{\lvert Q-Q_\star\rvert}{\lvert Q_\star\rvert}
\quad(Q_\star\ne0).$$

- Absolute error has the same units as $Q$.
- Relative error is dimensionless; multiply by 100 for percent error.
- At a zero reference, relative error is undefined.
- Against an approximate reference, these are discrepancies that also contain
  the reference's error.

A tolerance is an acceptance criterion. It does not measure or reduce error.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## `atol` and `rtol` state two scales of agreement

For finite values, NumPy evaluates

$$\lvert Q-Q_\star\rvert\le
\underbrace{\mathrm{atol}}_{\text{absolute allowance}}
+\underbrace{\mathrm{rtol}\,\lvert Q_\star\rvert}_{\text{scale-dependent allowance}}.$$

```python
np.isclose(computed, reference, rtol=relative_allowance,
           atol=absolute_allowance)
```

`atol` has the quantity's units. `rtol` is a fraction: `0.01` means 1%.
Put the reference second: NumPy uses it to set the relative scale.

With both nonzero, NumPy adds the allowances. Agreement need not satisfy
each allowance separately.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## See the tolerance as an acceptance region

**Predict:** with `atol=0.1` cm and `rtol=0.1`, how much discrepancy is
allowed at a reference of zero? At a reference of 2 cm?

:::{figure} reading-tolerance-acceptance.png
:alt: A shaded acceptance region includes zero residual and widens from plus or minus 0.1 cm at a zero reference to plus or minus 0.4 cm at references of plus or minus 3 cm. Dashed lines mark the absolute allowance.
:width: 850px

NumPy accepts finite comparisons inside the shaded region, including its
boundary. The allowed absolute discrepancy is 0.1 cm at zero and 0.3 cm at
2 cm. These illustrative tolerances are choices for this comparison, not
properties of floating-point arithmetic.
:::

[Open full-size figure](reading-tolerance-acceptance.png).

**Explain:** does passing this comparison tell us whether a model describes
its physical system correctly?
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Predict · the same absolute error at different scales

Suppose our stated criterion is relative agreement within one part in a million,
with no separate absolute allowance.

```{code-cell} python
reference = np.array([1.0, 1.0e6])
computed = reference + 0.1
rtol = 1.0e-6
atol = 0.0

print("absolute error:", np.abs(computed - reference))
print("allowed error:", atol + rtol * np.abs(reference))
print("accepted:", np.isclose(computed, reference, rtol=rtol, atol=atol))
```

**Explain:** why does one comparison fail and the other pass? Would changing
the tolerance change either computed value?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Near zero, the absolute scale matters

Suppose an example calculation has an independently chosen absolute accuracy
target of $10^{-8}$ cm. Compare its residual with zero:

```{code-cell} python
residual_cm = 3.0e-9
print("relative only:", np.isclose(residual_cm, 0.0, rtol=0.01, atol=0.0))
print("absolute target:", np.isclose(residual_cm, 0.0, rtol=0.0, atol=1.0e-8))
```

No finite relative tolerance permits a nonzero discrepancy against exactly
zero when `atol=0`. Choose an absolute scale from the question being tested.

The $10^{-8}$ cm here is a stated example target, not a universal recommendation.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## A default absolute tolerance can hide a large relative error

These example fluxes differ by 100% of the reference value:

```{code-cell} python
reference_flux = 1.0e-12  # erg / (s cm^2)
computed_flux = 2.0e-12
print("NumPy defaults:", np.isclose(computed_flux, reference_flux))
print("stated 1% target:", np.isclose(
    computed_flux, reference_flux, rtol=0.01, atol=0.0
))
```

NumPy's default `atol=1e-8` is larger than either value in these units.
Always check the tolerance against the scale and units of the calculation.

Source: [NumPy `isclose` documentation](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html).
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Similar comparison functions have different rules

For finite scalar values $a$ and $b$:

| Function | Permitted discrepancy |
| --- | --- |
| `np.isclose(a, b, rtol=r, atol=t)` | $t+r\lvert b\rvert$ |
| `math.isclose(a, b, rel_tol=r, abs_tol=t)` | $\max(t,r\max(\lvert a\rvert,\lvert b\rvert))$ |

Lecture 1 used `math.isclose`; today we use NumPy for arrays. The formulas
are different, so do not treat a name change as the whole conversion.

`np.isclose` returns one Boolean per element. `np.allclose` asks whether
all elementwise comparisons pass. Ensure arrays have the intended shapes
before comparing: NumPy can broadcast them.

Sources: [NumPy](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) ·
[Python `math.isclose`](https://docs.python.org/3/library/math.html#math.isclose).
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Choose a tolerance from the claim

1. Identify the reference and its accuracy.
2. State the units and whether an absolute or fractional discrepancy matters.
3. Use a method error bound, a convergence study, or a stated accuracy target.
4. Set the tolerance before inspecting whether the result passes.
5. If it fails, investigate the calculation and the criterion.

Check that quantities expected to be finite are finite. A comparison is not a
substitute for that contract.

**Explain:** if a method is first order, does asking for `rtol=1e-12` make it
more accurate? What would you actually need to change?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · tolerances and error measurements

| Quantity or choice | Meaning |
| --- | --- |
| `abs(computed - reference)` | Absolute discrepancy, in the quantity's units |
| Absolute discrepancy divided by `abs(reference)` | Fractional discrepancy for a nonzero reference |
| `rtol=0.0` | Only the absolute allowance contributes |
| `atol=0.0` | Only the relative allowance contributes |
| Both nonzero in `np.isclose` | NumPy adds the absolute and reference-scaled allowances |

**Rule:** a tolerance expresses a claim. Increasing it does not improve the result.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## IV · Quadrature replaces an integral with a finite sum

### Question

How can local function approximations give a numerical value for an integral?

### You will leave this section able to

- distinguish the interval, panels, nodes, heights, and weights;
- implement a callable-based left-rectangle rule;
- connect local area error to composite error; and
- compare computed errors with a ratio prediction and a bound.

**Through-line focus:** local polynomial $\rightarrow$ panel areas $\rightarrow$ integral.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Approximate one panel, then add the areas

Consider a fixed interval $[a,b]$, with $a<b$. Divide it into $n$ equal panels:

$$h=\frac{b-a}{n},\qquad x_i=a+ih,\qquad i=0,1,\ldots,n.$$

There are $n$ panels and $n+1$ boundary points.

On panel $[x_i,x_{i+1}]$, use the constant approximation $f(x)\approx f(x_i)$:

$$\int_{x_i}^{x_{i+1}} f(x)\,dx\approx h f(x_i).$$

Adding the panel contributions gives the left-rectangle rule:

$$L_n=h\sum_{i=0}^{n-1}f(x_i).$$
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Predict · which area is missing?

For $f(x)=\sin x$ on $[0,\pi/2]$, the function is increasing and the exact
integral is 1. Predict the sign of $L_n-1$.

```{code-cell} python
:tags: [remove-input, remove-output]

fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
panel_count = 6
width = (np.pi/2) / panel_count
left_nodes = width * np.arange(panel_count)
x_plot = np.linspace(0, np.pi/2, 301)
ax.bar(left_nodes, np.sin(left_nodes), width=width, align="edge",
       color="#0072B2", alpha=0.25, edgecolor="#0072B2", label="Left rectangles")
ax.plot(x_plot, np.sin(x_plot), color="#122b38", lw=2.5, label=r"$\sin x$")
ax.plot(left_nodes, np.sin(left_nodes), "o", color="#0072B2", label="Sample positions")
ax.set(xlabel=r"$x$ (radians)", ylabel=r"$\sin x$ (dimensionless)", xlim=(0, np.pi/2))
ax.legend()
fig.savefig("lecture-05-rectangles.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-05-rectangles.png
:alt: Six left-endpoint rectangles lie below the increasing sine curve between zero and pi over two. Dots mark the sampled left endpoints, and the rightmost boundary is not a sampled height.

The first rectangle has height zero. That panel still contributes to the
integral, which explains part of the underestimate.
:::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Build the nodes before the function

```{code-cell} python
a, b, n = 0.0, np.pi/2, 6
width = (b - a) / n
nodes = a + width * np.arange(n)
heights = np.sin(nodes)

print("panels:", n, "sampled heights:", heights.size)
print("left endpoints:", nodes)
print("rectangle sum:", width * np.sum(heights))
```

`np.arange(n)` supplies the integers 0 through `n-1`. The last sample is
$b-h$, not $b$.

**Explain:** why would `np.linspace(a, b, n)` give the wrong node spacing here?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## One function implements the rule

```{code-cell} python
def rectangle(f, a, b, n):
    """Left rectangles; first-order composite error for smooth f.

    f accepts and returns arrays of matching shape.
    n is a positive integer; a and b are finite scalar limits.
    """
    # Reject Boolean values, then require a Python or NumPy integer.
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer)):
        raise ValueError("n must be a positive integer")
    # A valid integer type can still have an invalid value.
    if n <= 0:
        raise ValueError("n must be a positive integer")
    width = (b - a) / n
    nodes = a + width * np.arange(n)
    return float(width * np.sum(f(nodes)))

print(rectangle(np.sin, 0.0, np.pi/2, 100))
```

Here the integrand contract also requires finite sampled values. Boolean
values are excluded even though Python treats `bool` as a kind of integer.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Why use `isinstance` for input checks?

`isinstance(value, type)` asks whether a value belongs to a type, including its
subclasses. A tuple of types accepts any of the listed types.

```{code-cell} python
print(isinstance(6, int))                      # True: a Python integer.
print(isinstance(6.0, int))                    # False: a float, even if whole.
print(isinstance(np.int64(6), (int, np.integer)))  # True: a NumPy integer.
print(isinstance(True, int))                   # True: bool subclasses int!
```

A panel count describes a number of intervals. The rule accepts positive
integers and rejects `True`, `6.0`, and `6.5` under its stated contract.
Silently applying `int(n)` could turn `6.5` into 6 and change the requested grid.

The first check rejects unsuitable types; `n <= 0` rejects unsuitable values.
`raise ValueError(...)` stops the calculation and tells the caller which
input requirement was violated. This example checks `n`; finite limits and
finite, matching integrand arrays remain caller preconditions here.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Passing a function is different from calling one

| Expression | What it supplies |
| --- | --- |
| `np.sin` | A callable: the rule can choose where to evaluate it |
| `np.sin(nodes)` | Values at nodes already chosen |
| `rectangle(np.sin, a, b, n)` | A quadrature calculation using the sine function |

The rule owns the grid. The callable owns the mathematical function.

**Predict:** what must change inside `rectangle` to integrate $e^x$ instead?

```{code-cell} python
print("sine:", rectangle(np.sin, 0.0, np.pi/2, 100))
print("exponential:", rectangle(np.exp, 0.0, 1.0, 100))
```
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Taylor expansion explains the rectangle error

Within one panel, put $x=x_i+s$ with $0\le s\le h$:

$$f(x_i+s)=f(x_i)+s f'(x_i)+O(s^2).$$

Integrate each term:

$$\int_{x_i}^{x_i+h}f(x)\,dx
=h f(x_i)+\frac{h^2}{2}f'(x_i)+O(h^3).$$

The rectangle retains the first term. Its one-panel error is $O(h^2)$.
For an increasing function, the missing leading area is positive.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## One-panel error and whole-interval error differ

The interval length $b-a$ stays fixed while $n=(b-a)/h$ increases.
If panel errors are uniformly bounded by $C h^2$, their sum is bounded by

$$n C h^2=C(b-a)h.$$

Thus the composite left-rectangle rule has an $O(h)$ error bound.

We can replace the unspecified constant $C$ by a bound on the slope. The next
slide derives that bound for any continuously differentiable $f$ on $[a,b]$.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Derive a bound for any smooth integrand

Assume $a<b$ and $|f'(x)|\le M_1$ throughout $[a,b]$. The mean value theorem
bounds the change in height inside panel $i$:

$$|f(x_i+s)-f(x_i)|\le M_1s,\qquad 0\le s\le h.$$

The panel's signed area error is the integral of that height difference:

$$E_i=\int_0^h[f(x_i+s)-f(x_i)]\,ds.$$

Take the absolute value, bound the integrand, and integrate:

$$|E_i|\le\int_0^h|f(x_i+s)-f(x_i)|\,ds
\le\int_0^h M_1s\,ds=\frac{M_1h^2}{2}.$$

The factor $1/2$ is the area of a triangle with base $h$ and height $M_1h$.
Adding the absolute panel bounds gives

$$\lvert I-L_n\rvert=\left|\sum_{i=0}^{n-1}E_i\right|
\le\sum_{i=0}^{n-1}|E_i|\le\frac{nM_1h^2}{2}
=\frac{(b-a)^2}{2n}M_1.$$

These statements concern quadrature error in exact arithmetic. A numerical
test must also allow for relevant floating-point effects.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Choose a panel count from an error target

For a requested absolute quadrature error $\tau>0$, it is sufficient that

$$\frac{M_1(b-a)^2}{2n}\le\tau
\quad\Longrightarrow\quad
n\ge\frac{M_1(b-a)^2}{2\tau}.$$

Choose a positive integer:

$$n_{\rm sufficient}=\max\left(1,
\left\lceil\frac{M_1(b-a)^2}{2\tau}\right\rceil\right).$$

The ceiling rounds upward. This gives a sufficient count, not necessarily the
smallest count that works: the bound allows the largest slope on every panel
and ignores cancellation between panel errors.

This requires a justified derivative bound. Sampling $f'$ at a few points does
not prove that no larger slope occurs between them. Floating-point error is
a separate contribution to the total error budget.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Run · test the first-order prediction

```{code-cell} python
previous_error = None
for n in (20, 40, 80, 160):
    estimate = rectangle(np.sin, 0.0, np.pi/2, n)
    error = abs(estimate - 1.0)
    ratio = "—" if previous_error is None else f"{previous_error/error:.3f}"
    print(f"n={n:3d}: estimate={estimate:.7f}, error={error:.3e}, ratio={ratio}")
    previous_error = error
```

Compare $E_n/E_{2n}$ with 2. One accurate answer would not show this pattern.

**Explain:** why would changing the integrand change the error magnitude even
if the leading order stayed the same?
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Use the error bound to choose an absolute tolerance

For sine on $[0,\pi/2]$, $f'(x)=\cos x$, so $M_1=1$ and $b-a=\pi/2$:

$$\frac{M_1(b-a)^2}{2n}
=\frac{1\cdot(\pi/2)^2}{2n}=\frac{\pi^2}{8n}.$$

At $n=100$,

$$\lvert I-L_{100}\rvert\le\frac{\pi^2}{8(100)}\approx0.01234.$$

```{code-cell} python
n = 100
error_bound = np.pi**2 / (8*n)
estimate = rectangle(np.sin, 0.0, np.pi/2, n)
print("observed error:", abs(estimate - 1.0))
print("theoretical bound:", error_bound)
print("within bound:", np.isclose(estimate, 1.0, rtol=0.0, atol=error_bound))

# Conversely, choose n to make the quadrature bound at most 0.01.
target = 0.01
required_n = max(1, int(np.ceil(np.pi**2 / (8*target))))
print("sufficient panels for target 0.01:", required_n)  # 124 panels.
```

The observed error has substantial room below the bound here; rounding is much
smaller. Passing supports this bounded check. It does not prove the general rule.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Reference · left-rectangle quadrature

| Component | Expression |
| --- | --- |
| Panel width | `width = (b - a) / n` |
| Left endpoints | `nodes = a + width * np.arange(n)` |
| Heights | `f(nodes)` |
| Weighted sum | `width * np.sum(f(nodes))` |
| Expected leading composite order | 1 for a nonvanishing leading term and a smooth integrand |

**Rule:** the integrator selects the grid; the callable supplies the function values.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Same panels, different rectangle heights

Keep $h=(b-a)/n$ and the same panel boundaries. Change only where each height
is sampled, with $i=0,\ldots,n-1$:

| Rule | Sample location | Composite sum |
| --- | --- | --- |
| Left | $a+ih$ | $L_n=h\sum_i f(a+ih)$ |
| Right | $a+(i+1)h$ | $R_n=h\sum_i f(a+(i+1)h)$ |
| Midpoint | $a+(i+\tfrac12)h$ | $M_n=h\sum_i f(a+(i+\tfrac12)h)$ |

```{code-cell} python
:tags: [remove-input, remove-output]

variant_n = 6
variant_h = (np.pi/2) / variant_n
panel_left = variant_h * np.arange(variant_n)
curve_x = np.linspace(0, np.pi/2, 301)
rectangle_variants = {}
fig, axes = plt.subplots(1, 3, figsize=(12, 4.4), sharey=True, layout="constrained")
for ax, name, shift, color, marker in zip(
    axes, ("Left", "Right", "Midpoint"), (0.0, 1.0, 0.5),
    ("#0072B2", "#D55E00", "#009E73"), ("o", "s", "^")
):
    sample_x = panel_left + shift * variant_h
    heights = np.sin(sample_x)
    rectangle_variants[name] = float(variant_h * np.sum(heights))
    ax.bar(panel_left, heights, width=variant_h, align="edge", color=color,
           alpha=0.25, edgecolor=color)
    ax.plot(curve_x, np.sin(curve_x), color="#122b38", lw=2)
    ax.plot(sample_x, heights, marker, color=color, ms=6)
    ax.set(title=f"{name}: {rectangle_variants[name]:.4f}",
           xlabel=r"$x$ (radians)", xlim=(0, np.pi/2))
axes[0].set_ylabel(r"$\sin x$ (dimensionless)")
fig.savefig("lecture-05-rectangle-variants.png", dpi=160)
plt.close(fig)
```

:::{figure} lecture-05-rectangle-variants.png
:alt: Three panels show six rectangles on the same sine curve from zero to pi over two. Circles, squares, and triangles mark samples on the curve at left endpoints, right endpoints, and midpoints. Left rectangles lie below the curve, right rectangles lie above it, and midpoint rectangles cross it. Titles give each area estimate; the exact integral is one.

All three rules use six heights. The rectangles retain the same bases; moving
the sample changes their heights and the estimated area.
:::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## What changes when we move the sample?

For an increasing function and $a<b$,

$$L_n\le I\le R_n,\qquad R_n-L_n=h[f(b)-f(a)].$$

The sum in the difference telescopes: interior samples cancel, leaving only
the endpoint values. For a decreasing function, the inequalities reverse.

The midpoint rule cancels the linear contribution about each panel's center,
so its composite error is $O(h^2)$ when the second derivative is bounded.
It need not lie on the same side of the integral as the left rule.

**Predict:** sine is concave down on this interval. Does midpoint sampling
underestimate or overestimate its area? A tangent at each midpoint lies above
the curve, and its integral over the symmetric panel equals the midpoint
rectangle area: here the midpoint rule overestimates.

Next lecture, connecting endpoint heights gives trapezoids. In fact,
$T_n=(L_n+R_n)/2$ on this uniform grid. We will derive why that average also
improves the order.
:::

:::::{div}
:class: projector-lecture projector-slide lecture-scroll

## Documentation for the next question

::::{div}
:class: lecture-two-column

:::{div}
:class: lecture-column

| Resource | Use it for |
| --- | --- |
| [NumPy `finfo`](https://numpy.org/doc/stable/reference/generated/numpy.finfo.html) | Floating-point representation limits |
| [NumPy `isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) | Exact tolerance semantics |
| [NumPy `expm1`](https://numpy.org/doc/stable/reference/generated/numpy.expm1.html) | Stable evaluation near zero |
| [Python `isinstance`](https://docs.python.org/3/library/functions.html#isinstance) | Type checks, tuples of types, and subclasses |
| [NumPy `arange`](https://numpy.org/doc/stable/reference/generated/numpy.arange.html) and [`abs`](https://numpy.org/doc/stable/reference/generated/numpy.absolute.html) | Array indices and elementwise absolute values |
:::

:::{div}
:class: lecture-column

Use the course readings for derivations and worked examples. Use official API
documentation to check parameter meanings, assumptions, and return values.

When a comparison surprises you, print the discrepancy and the allowed
discrepancy before changing either tolerance.
:::
::::
:::::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Exit check

1. What is the difference between truncation error and rounding error?
2. Why can reducing $h$ hurt a forward difference?
3. Against a zero reference, which tolerance sets the allowed discrepancy?
4. Why is a one-panel $O(h^2)$ error consistent with a composite $O(h)$ error?
5. What should happen to a first-order error when the panel count doubles?

Use the mechanism in each answer, not only the name of the error.
:::

:::{div}
:class: projector-lecture projector-slide lecture-scroll

## Carry forward

Next class: replace each constant panel approximation with a line, then a
quadratic. We will organize the rectangle rule in a module and test it on
$\sin x$ using `pytest`.

Project 2 uses these ideas to build and assess numerical integrators. The
assignment brief specifies the deliverables; today's rule and error comparison
give you a starting point.

Reading guide in Numerical Methods: *Foundations*, Part 1, “Forward
Difference”; Part 2, the absolute/relative error and tolerance discussions;
Part 3, “Taylor polynomial and remainder.” In *Roots and Quadrature*, Part 2,
review the rectangle-rule section. The longer chapters are references; the
other methods are not preparation for today's rectangle implementation.
:::
