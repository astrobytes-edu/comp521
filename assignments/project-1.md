---
title: "Project 1 — Python and the Transit Model"
subtitle: "COMP 521 | Fall 2026"
---

# Project 1 — Python and the Transit Model

**Due Tuesday, September 8, 11:59 pm PT** · pairs allowed, own code and own
write-up · [Project 0](../02-getting-started/index.md) must be done first

---

## What you are building

**What does a planet crossing a star actually look like?** You will answer it
from first principles — no data, no library that does it for you — and write the
model the rest of this course spends thirteen weeks making real.

| Part | You build | It is right when |
|:--|:--|:--|
| **1** | `luminosity(radius, teff, solar=False)` | it reproduces the Sun |
| **2** | Theoretical HR diagram | the Sun sits **on** the $R=1\,R_\odot$ line |
| **3** | `flux(p, z)` — the transit, four cases | branches agree at the boundaries |
| **4** | `transit_curve(...)` — loop **and** vectorized | both agree; depth $= p^2$ |
| **5** | `Discussion` section, ~400 words | — |

**Deliverable:** one repository containing `analysis.ipynb` (that filename),
both figures saved as files, and `README.md`.

:::{important} Work in a notebook — this is the only project where that is enough
No modules, no classes. Write functions, in order, with the story in between.

From Project 2 on you write `.py` modules and **import these transit functions
into them** — moved, not rewritten. So write them as though a stranger has to
use them. One does: you, in three weeks.
:::

:::{warning} Restart and Run All before your final commit
**Kernel → Restart Kernel and Run All Cells**, then commit. I re-execute what
you submit; a notebook whose saved output came from code you have since edited
looks fine and is worthless.
:::

---

## Before you start

:::{admonition} The documentation you need — read the page before you write the line
:class: tip dropdown

This is the actual skill. The [AI policy](../01-course-info/ai-policy.md)
permits AI in Phase 1 for *"help interpreting documentation you have already
tried to read"* — these links make that a real condition. Reference docs are
terse and occasionally hostile, and they are the only source that is current,
complete, and correct. Every tool you meet after this course has documentation
and no tutorial.

**How to read a NumPy page:** jump to **Examples** at the bottom first, then back
up to **Parameters**. Prose last. If it mentions `dtype`, `axis`, or
"array_like" and you do not know what those are, that is normal — note it and
keep going.

**Python** — [f-strings and output](https://docs.python.org/3/tutorial/inputoutput.html) ·
[errors and exceptions](https://docs.python.org/3/tutorial/errors.html) ·
[`ValueError`](https://docs.python.org/3/library/exceptions.html) ·
[built-in functions](https://docs.python.org/3/library/functions.html) ·
[`math`](https://docs.python.org/3/library/math.html)

**NumPy** — [`linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html) ·
[`logspace`](https://numpy.org/doc/stable/reference/generated/numpy.logspace.html) ·
[broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) ·
[indexing](https://numpy.org/doc/stable/user/basics.indexing.html) ·
[`where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html) ·
[`arccos`](https://numpy.org/doc/stable/reference/generated/numpy.arccos.html) ·
[`clip`](https://numpy.org/doc/stable/reference/generated/numpy.clip.html) ·
[constants](https://numpy.org/doc/stable/reference/constants.html)

**Matplotlib** — [quick start](https://matplotlib.org/stable/users/explain/quick_start.html) ·
[`subplots`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html) ·
[`plot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html) ·
[`loglog`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.loglog.html) ·
[`invert_xaxis`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.invert_xaxis.html) ·
[`annotate`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html) ·
[`legend`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html) ·
[`savefig`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)

**Jupyter** — [`%timeit`](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
:::

### Constants — all CGS

| Quantity | Value |
|:--|:--|
| $\sigma$ | $5.670374419\times10^{-5}$ erg cm⁻² s⁻¹ K⁻⁴ |
| $R_\odot$ | $6.957\times10^{10}$ cm |
| $L_\odot$ | $3.828\times10^{33}$ erg s⁻¹ |
| $T_{{\rm eff},\odot}$ | $5772$ K |
| $R_\oplus$ | $6.371\times10^{8}$ cm |
| $R_{\rm J}$ | $7.1492\times10^{9}$ cm |

:::{admonition} Why CGS, why solar units, and why the transit has no units at all
:class: note dropdown

**Most wrong answers in computational astrophysics are unit errors**, and they
are wrong by factors of $10^7$ or $10^{33}$ rather than by a little — which is
good news, because you can catch them by looking.

**CGS.** You were probably taught SI. Astronomy uses centimetres, grams,
seconds, and **ergs**: $1\ \mathrm{erg} = 10^{-7}$ J. Partly historical inertia,
partly that astrophysical constants come out with exponents you can carry in
your head. Not optional: in SI your constants will not match the literature.

**Solar units** exist for **error detection**. You can see at a glance that
$0.001\,L_\odot$ is wrong for a Sun-like star. You cannot see a bad exponent in
$3.8\times10^{33}$. That is what `solar=True` is for, and you will use it for
every self-check in this project.

**Dimensionless.** Part 3 has no units in it anywhere: $p = R_p/R_\star$ and
$z = d/R_\star$ are lengths over lengths, and flux is a ratio. That is not
convenience, it is the physics — it is *why* a transit measures $R_p/R_\star$
and never $R_p$. To get kilometres you need $R_\star$ from somewhere else
entirely, a limitation you run into for real in Project 5.

**Do not use `astropy.units`.** Carrying units by hand is the exercise. The habit
that saves you: put units in the parameter name. `radius_cm` and `radius_rsun`
cannot be confused; `radius` can, and eventually will be.
:::

---

## Part 1 — A function you can trust

$$L = 4\pi R^2 \sigma T_{\rm eff}^4$$

Build `luminosity(radius, teff, solar=False)` in **three passes**, each working
before the next:

1. **Compute it.** Radius in cm, returns erg s⁻¹.
2. **Add `solar=True`** — radius in $R_\odot$, returns $L_\odot$.
3. **Add validation.** Negative radius, non-positive temperature, or non-numeric
   input raises `ValueError` with a message saying what was wrong.

:::{tip} Self-check
```
luminosity(1.0, 5772, solar=True)  ->  1.00   (to two decimals)
luminosity(6.957e10, 5772)         ->  3.83e33 erg/s
```
That is the Sun. Then loop over bad inputs — `(-1, 5772)`, `(1, 0)`,
`(1, "hot")` — catch each `ValueError` and print the message.
:::

:::{admonition} Why validation, in week two
:class: note dropdown
You use this function again in Project 3, for a star you did not choose. By then
you will not remember what it does with a negative radius. Functions that fail
loudly are how you come to trust your own code from six weeks ago.

A `ValueError` is right; returning `None` or `nan` is not. Silent wrong answers
are the thing this whole course is against.
:::

---

## Part 2 — Broadcasting, and your first figure

Build a **theoretical HR diagram**: $L$ against $T_{\rm eff}$, with lines of
constant radius. Radii from $0.01$ to $100\,R_\odot$, temperatures from 2,000 to
40,000 K.

Requirements:

- **Both axes logarithmic**, in solar units
- **Temperature increasing to the left** — the astronomical convention, not optional
- Every line labelled, axes labelled with units, readable legend
- **Four real stars annotated** — Sun, Sirius A, Betelgeuse, Proxima Centauri.
  Look up $R$ and $T_{\rm eff}$ and **cite your source**
- Use [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html),
  not nested loops — radii down one axis, temperatures across the other, one call

:::{tip} Self-check
The Sun must land at $(5772\ \mathrm{K},\ 1\,L_\odot)$ and sit **exactly on** your
$R = 1\,R_\odot$ line. Beside it means your grid and your annotation disagree
about units.
:::

:::{admonition} Keep this figure — Project 6 draws the same axes
:class: note dropdown
What you are plotting is *what the equation permits*. In Project 6 you plot the
same axes from real Gaia measurements of thousands of stars: lumpy, with a main
sequence and a giant branch, none of which is anywhere in the Stefan–Boltzmann
law.

*Here is what the physics allows; here is what nature actually did.*
:::

---

## Part 3 — The transit, as four cases

Star as a **uniform disk** (it isn't — that's Project 2). With
$p = R_p/R_\star$ and $z = d/R_\star$, write `flux(p, z)`:

| Case | Condition | Flux |
|:--|:--|:--|
| No overlap | $z \ge 1+p$ | $1$ |
| Fully on the disk | $z \le 1-p$ | $1 - p^2$ |
| Planet covers the star | $z \le p-1$ | $0$ |
| Partial overlap | $\lvert 1-p \rvert < z < 1+p$ | formula below |

$$F = 1 - \frac{1}{\pi}\left[\, p^2 \kappa_0 + \kappa_1 - \sqrt{\tfrac{1}{4}\left(4z^2 - (1+z^2-p^2)^2\right)} \,\right]$$

$$\kappa_0 = \arccos\!\left(\frac{p^2+z^2-1}{2pz}\right), \qquad
  \kappa_1 = \arccos\!\left(\frac{1-p^2+z^2}{2z}\right)$$

Write the cases as `if`/`elif` with **the partial-overlap formula last**, and
**note which comparison operators you used** (`<` vs `<=` at each boundary). One
sentence. You will need it in Part 4.

:::{tip} Self-check — three tests
1. `flux(p, 0)` equals `1 - p**2`
2. `flux(p, 5)` equals `1` exactly
3. **Continuity.** At $z = (1-p)\pm10^{-9}$ and $z = (1+p)\pm10^{-9}$, the two
   branches agree to better than $10^{-11}$

Test 3 finds real bugs. A backwards comparison or a sign error in $\kappa_0$
passes 1 and 2 and produces a light curve with a visible step in it.
:::

:::{admonition} Why the order of your `if` statements is load-bearing
:class: warning dropdown
At $z = 1-p$ exactly, $\kappa_0$'s argument works out to $-1$ — right at the edge
of what `arccos` accepts. Get the comparisons right and the earlier branches
catch every value that would overshoot, so the dangerous expression is never
evaluated at all. Get one backwards and you find out what your library does with
an out-of-domain argument.

This protection is a property of `if`, and it does not survive Part 4.
:::

:::{admonition} You are reading a paper in week two
:class: note dropdown
This is the uniform-source limit from **Mandel & Agol (2002)**, *ApJ* **580**,
L171 — [iopscience.iop.org/article/10.1086/345520](https://iopscience.iop.org/article/10.1086/345520).
Four pages; §2 and Eq. 1 are what you are implementing.

Almost nothing you compute in your career will come from a textbook. It comes
from a paper written for people who already know the field, with what you need
buried in a sentence. Getting one equation out of one paper and into working
code is the most transferable skill in this course. **Cite it in your
Discussion.**
:::

---

## Part 4 — The light curve, twice

For a circular edge-on orbit, mid-transit at $t=0$:

$$z(t) = \frac{a}{R_\star}\,\left| \sin\!\left(\frac{2\pi t}{P}\right) \right|$$

Write `transit_curve(times, p, a_over_rstar, period)` **twice**:

- **Version A** — a Python `for` loop calling `flux` once per time
- **Version B** — vectorized with NumPy: build the `z` array, then masks

### Version B will not work the first time

Build the obvious version — compute the formula over the whole `z` array, then
[`np.where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
to pick each case. Run it. **You will get `nan`** — a lot of them, plus a
`RuntimeWarning` that scrolls past. Your loop, same formula, was fine.

1. **Report how many** output points are `nan`, and where
2. **Explain why the loop was safe and the array version is not** — one sentence
   about what `if` does that an array expression does not. Your Part 3 note is the hint
3. **Fix it**, and say why the fix is right rather than merely quiet
4. There is a **second hazard at exactly $z = 0$** — mid-transit, a point you
   plot on purpose. Find it and say what causes it

:::{warning} Making the warning go away is not fixing it
`np.nan_to_num` and a bare `try/except` both silence the symptom and keep the
bug. So does clamping every argument into $[-1,1]$ without asking how far
outside it was — a clamp that quietly absorbs an argument of $24$ is hiding a
real error, not handling round-off.

**One `nan` propagates.** Every mean, sum, or fit downstream becomes `nan`, and
nothing tells you where it started.
:::

Then confirm the two versions agree and **time both** on $10^5$ points with
[`%timeit`](https://ipython.readthedocs.io/en/stable/interactive/magics.html).
Report the speedup.

:::{admonition} Why this exercise is the whole course in miniature
:class: note dropdown
You will get tens of times faster — the exact number depends on your machine.
The physics did not change and the arithmetic is identical. The loop moved into
compiled code.

That is the honest answer to "why not just use the library?" Libraries are not
smarter than you, they are *compiled*. In Project 6 you race your own
machine-learning code against scikit-learn and find the same thing. Knowing what
a library does, and knowing it will beat your version, are not in conflict.
:::

### Your second figure

Light curves for $p = 0.05,\ 0.10,\ 0.15,\ 0.20,\ 0.25$ on one set of axes,
$a/R_\star = 10$. Label everything.

:::{tip} Self-check — and a warning about the word "exactly"
Mid-transit depth is **exactly $p^2$ in the mathematics** — a uniform disk is
equally bright everywhere, so the planet blocks precisely its area fraction.

**In your code it is not.** Compare with a tolerance, not `==`. You will find a
disagreement of about $10^{-17}$, because your function stores $1-p^2$ and you
recover the depth as $1-(1-p^2)$ — two roundings that do not cancel.

Worth one line in your Discussion: *the algebra is exact, the arithmetic is not,
and knowing which claim you are making is the skill.*
:::

---

## Part 5 — Discussion

Last section of your notebook, titled `Discussion`. **Prose only, no code
cells**, about 400 words. Not a narration of what you did — the cells above show
that. What your results *mean*:

- **How does transit depth scale with planet size, and what does that demand of
  a telescope?** An Earth around a Sun-like star gives $p \approx 0.009$.
- **Why did your loop work and your vectorized version return `nan`?** How do you
  know your fix is right rather than merely quiet?
- **Your HR diagram shows lines of constant radius. Real stars cluster on a main
  sequence instead.** What does that tell you that Stefan–Boltzmann alone does not?

:::{note} The third question is deliberate
Nothing you computed can answer it. Say what you can support and be honest about
the rest. That is a skill, not a failure.
:::

---

## What you turn in

- `analysis.ipynb` — **use that filename** — ending with your `Discussion`
- Both figures, saved as files as well as displayed
- `README.md` — what is here and how to run it

Pairs are fine. **You each write your own code and your own Discussion, and you
each have to explain every line of what you submit.**

:::{admonition} What a strong submission looks like
:class: note dropdown
Not a checklist — I grade the project as a whole.

A strong Project 1 is one a stranger could still read: functions do one thing,
names say what they mean, and the self-checks are present and passing rather
than described. The figures are readable without being explained aloud. The
Discussion says something the code does not, and where it is uncertain, says so.

The most common way to lose ground is a notebook that runs but that you cannot
defend line by line — which usually means it was assembled rather than written.
:::
