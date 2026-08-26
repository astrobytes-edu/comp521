---
title: "Project 1 — Python and the Transit Model"
subtitle: "COMP 521 | Fall 2026"
author: "Anna Rosen"
---

# Project 1 — Python and the Transit Model

**Due Tuesday, September 8, 11:59 pm PT** · pairs allowed, own code and own
write-up · GitHub repository check due Fri Aug 28 at 11:59 pm PT

---

(sec-p1-repository-check)=
## First milestone — Project 1 GitHub Repository Check

**Due Friday, August 28 at 11:59 pm PT.** Complete this individual,
completion-only checkpoint in the same Project 1 repository you will submit on
September 8. It is not a separate Project 0 and does not count in the project
average.

1. Use the Project 1 GitHub repository assigned through Classroom50 **or** the
   individual repository you will link in the Canvas Project 1 assignment.
   Clone that repository to your computer. If you are new to GitHub, use
   [Git, GitHub, and Classroom50](../../02-getting-started/03-git-intro.md)
   before guessing at a command.
2. Change the repository-check box in `README.md` from `[ ]` to `[x]`.
3. Commit that README change locally and push it to GitHub.
4. Open the repository on GitHub and confirm that the commit is visible.

Your Project 1 repository contains the supplied `analysis.ipynb` scaffold and
matching `README.md`. The visible setup commit records completion; no separate
upload or automated readiness test is needed. The check assesses only a working
GitHub path—not effort, code quality, Python setup, or progress on P1.

:::{important} Project 1 submission route

For Project 1, submit the URL of your GitHub repository in the Canvas Project 1
assignment by the deadline. I will grade the last commit pushed before the
deadline. If Classroom50 successfully assigned your individual repository, it
may also serve as the submission route; Canvas announcements will state any
change to that workflow. Do not wait for Classroom50 in order to begin or
submit Project 1.

The deadline remains Tuesday, September 8. A repository problem discovered at
or after that deadline is not grounds for an extension. The exceptions are an
approved accommodation or a documented GitHub/Canvas outage; if an outage
occurs, contact the instructor through Canvas before the deadline.
:::

---

## What you are building

**What does a planet crossing a star actually look like?** You will answer it
from first principles — no data, no library that does it for you — and write the
model the rest of this course spends thirteen weeks making real.

| Part | You build | It is right when |
|:--|:--|:--|
| **1** | `luminosity(radius, teff, solar=False)` | it reproduces the Sun |
| **2** | Theoretical HR diagram, 15 real stars on it | the Sun sits **on** the $R=1\,R_\odot$ line |
| **3** | `flux(p, z)` — the transit, four cases | branches agree at the boundaries |
| **4** | `transit_curve(...)` — loop **and** vectorized | both agree; depth $= p^2$ |

**Deliverable:** one repository containing `analysis.ipynb` (that filename),
both figures saved as files, and `README.md`.

:::{admonition} Suggested pace
:class: tip dropdown

By the end of Week 1, aim to have Parts 1–2 complete and the four cases for
`flux(p, z)` planned or started. Part 4 depends on getting that geometry right.
This is a planning check, not a separate submission.
:::

:::{important} Every part ends with questions you must answer in writing
Each part ends with an **Interpret your result** box naming two or three things
to address. Answer them together, as **one or two short paragraphs of prose**, in
a markdown cell immediately after that part's code.

Not a numbered list mirroring mine — a paragraph. The points are related, and
saying how they relate is most of what I am reading for.

There is no separate report at the end. The interpretation belongs next to the
thing it interprets, because that is where you actually have to look at your own
output and decide what it means — which is the part of computing that does not
get easier with practice unless you practise it.

**A notebook of correct code with no interpretation is not a complete
submission.**
:::

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

Read [Markdown for Analysis Notebooks](../../02-getting-started/06-markdown-analysis-notebooks.md)
before drafting your first written answer. Its heading, mathematics,
figure, narrative, and clean-execution conventions apply to this submission.
For cloning, committing, pushing, and checking the visible result, use
[Git, GitHub, and Classroom50](../../02-getting-started/03-git-intro.md).

(p1-docs)=
:::{admonition} The documentation you need — read the page before you write the line
:class: tip dropdown

This is the actual skill. The course AI policy
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

**NumPy — comparing and inspecting results.** The ones you will actually reach
for in Parts 3 and 4:

| For | Function |
|:--|:--|
| Compare two floats with a tolerance **you choose** | [`isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) |
| The same, for whole arrays, one answer | [`allclose`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html) |
| Assert closeness and get a *useful* failure message | [`testing.assert_allclose`](https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html) |
| Find `nan` values | [`isnan`](https://numpy.org/doc/stable/reference/generated/numpy.isnan.html) |
| Find `nan` **and** `inf` in one go | [`isfinite`](https://numpy.org/doc/stable/reference/generated/numpy.isfinite.html) |
| Count how many | [`count_nonzero`](https://numpy.org/doc/stable/reference/generated/numpy.count_nonzero.html) |
| Max/min ignoring `nan` | [`nanmax`](https://numpy.org/doc/stable/reference/generated/numpy.nanmax.html) |
| Step to the next representable float | [`nextafter`](https://numpy.org/doc/stable/reference/generated/numpy.nextafter.html) |

**Every one of these takes a tolerance or a condition you control.** `isclose`
defaults to `rtol=1e-5`, which is far looser than anything in this project —
so pass your own. A comparison you did not choose the tolerance for is not a
test.

**Prefer `assert_allclose` to a bare `assert`.** `assert np.allclose(a, b)`
tells you only that *something* failed. `np.testing.assert_allclose(a, b,
rtol=...)` tells you **by how much, where, and how many elements** — the
difference between a test that reports a bug and a test that reports its own
existence.

**Matplotlib** — [quick start](https://matplotlib.org/stable/users/explain/quick_start.html) ·
[`subplots`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html) ·
[`plot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html) ·
[`loglog`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.loglog.html) ·
[`invert_xaxis`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.invert_xaxis.html) ·
[`axvspan`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.axvspan.html) ·
[`annotate`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html) ·
[`text`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html) ·
[mathtext (LaTeX in labels)](https://matplotlib.org/stable/users/explain/text/mathtext.html) ·
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

:::{admonition} Deep Dive: where the Stefan–Boltzmann law comes from
:class: seealso dropdown

**You do not need any of this to write the code.** It is here so the
equation is not a magic string you are transcribing.

**What the symbols are**

| | | |
|:--|:--|:--|
| $L$ | **luminosity** | total energy the star radiates per second, everywhere, in all directions. Units: erg s⁻¹. It is a *power*, like watts. |
| $R$ | radius | the star, treated as a sphere. |
| $T_{\rm eff}$ | **effective temperature** | the surface temperature, in kelvin. |
| $\sigma$ | Stefan–Boltzmann constant | a fixed number of nature, like $c$ or $G$. |

**Why it has this shape.** Any warm object glows. A *blackbody* is the idealized
version — an object that absorbs all light hitting it and re-emits purely
according to its temperature. Stars are close enough to blackbodies that this
works remarkably well.

The physics result (Stefan–Boltzmann law) is that a blackbody radiates
$\sigma T^4$ of power **per unit surface area**. So:

$$\underbrace{4\pi R^2}_{\text{surface area of a sphere}} \times \underbrace{\sigma T_{\rm eff}^4}_{\text{power per unit area}} \;=\; \text{total power}$$

That is the whole derivation. **The $R^2$ is just geometry** — a bigger sphere
has more surface to radiate from. **The $T^4$ is the physics**, and it is the
interesting part: temperature is an enormously powerful lever. A star twice as
hot as the Sun, at the same size, is *sixteen* times brighter.

**What "effective temperature" really means.** A star has no solid surface, and
it gets hotter with depth. $T_{\rm eff}$ is defined as *the temperature a perfect
blackbody of the same radius would need to have in order to emit the same total
power*. It is a defined quantity, not a thermometer reading — which is why this
equation is exactly true rather than approximately true. It is closer to a
definition than a discovery.

**The Sun, for scale:** $R_\odot = 6.957\times10^{10}$ cm (109 Earth radii),
$T_{\rm eff,\odot} = 5772$ K, giving $L_\odot = 3.828\times10^{33}$ erg s⁻¹. The
subscript $\odot$ always means "of the Sun."
:::

Build `luminosity(radius, teff, solar=False)` in **three passes**, each working
before the next. Its contract is:

- `radius`: a positive, finite real scalar or NumPy array. It is in **cm** when
  `solar=False` and in **solar radii** when `solar=True`.
- `teff`: a positive, finite real scalar or NumPy array in **K in both modes**.
- `solar`: a Boolean. The result is in erg s⁻¹ when false and $L_\odot$ when
  true.
- output: a scalar for scalar inputs, otherwise the broadcasted array shape of
  `radius` and `teff`.
- invalid input: non-positive, non-finite, or non-numeric inputs must raise
  `ValueError` with a useful message.

1. **Compute it.** Radius in cm, returns erg s⁻¹.
2. **Add `solar=True`** — radius in $R_\odot$, returns $L_\odot$.
3. **Add validation.** A non-positive radius or temperature raises `ValueError`
   with a message saying what was wrong.

:::{warning} Your function must also work on arrays
Part 2 calls `luminosity` once with whole *arrays* of radii and temperatures. So
`if radius <= 0:` will not do — on an array that raises *"truth value of an array
with more than one element is ambiguous"*, from a line that is not the bug.

Use [`np.any`](https://numpy.org/doc/stable/reference/generated/numpy.any.html)
on the condition instead. Getting this wrong in Part 1 and discovering it in
Part 2 is the most expensive hour in this project, and it is entirely avoidable.
:::

:::{tip} Self-check
```
luminosity(1.0, 5772, solar=True)  ->  1.00   (to two decimals)
luminosity(6.957e10, 5772)         ->  3.83e33 erg/s
```
That is the Sun. Then loop over bad inputs — `(-1, 5772)`, `(1, 0)`,
`(1, "hot")` — catch each `ValueError` and print the message.
:::

:::{attention} Interpret your result — Part 1
One short paragraph addressing both:

- Your Sun check does not return exactly `1.000000`. **What is the last digit
  you actually believe, and what sets that limit?**
- $L \propto R^2 T^4$. **Which is the more efficient way to make a star
  bright** — heating it or growing it? By how much, for a doubling of each?
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

:::{warning} Budget real time for this figure — and take it seriously all semester
**A figure is an instrument, not an illustration.** The self-check below is not
decoration: if the Sun does not land exactly on your $R = 1\,R_\odot$ line, you
have a units bug — and the *plot* is what tells you, not the numbers. You will
find bugs this way for the rest of the course.

Expect the figure to take **longer than the code that generates the data.** That
is normal and it is not wasted time. Log axes, a reversed axis, shaded bands
behind everything, a legend that does not cover the data — each is a decision,
and every one of them is reusable.

The standard set here is the standard for the semester. A figure that is
unreadable, unlabelled, or that hides its own units is not a finished result,
and it will not be marked as one. **Every figure you submit should be one you
would be willing to put in front of a room.**
:::

Build a **theoretical HR diagram**: $L$ against $T_{\rm eff}$, with lines of
constant radius. Use **five lines**, at $R = 0.01,\ 0.1,\ 1,\ 10,\ 100\,R_\odot$,
over temperatures from **2,000 to 45,000 K**.

Requirements:

- **Both axes logarithmic**, in solar units
- **Temperature increasing to the left** — the astronomical convention, not optional
- Every line labelled, axes labelled with units, readable legend
- **Axis labels and legend entries use LaTeX**, via Matplotlib's
  [mathtext](https://matplotlib.org/stable/users/explain/text/mathtext.html):
  `r"$T_{\rm eff}$ [K]"`, not `"Teff (K)"`
- **All fifteen stars below plotted as points.** Do *not* label them
  individually — a plot with fifteen text labels is a plot nobody can read. Mark
  the **Sun** distinctly (different colour or marker) so you can find it
- **Spectral-class bands shaded** across the temperature axis with
  [`axvspan`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.axvspan.html)
  — alternating light shading, each band labelled with its letter using
  [`text`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html).
  Keep the shading behind everything else (`zorder`) and faint enough to read
  through
- Use [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html),
  not nested loops — radii down one axis, temperatures across the other, one call
- **The star table lives in one data structure**, and everything else loops over
  it. Adding a sixteenth star must be a one-line change

:::{admonition} Which data structure? Your call — but justify it
:class: note dropdown
I am not telling you whether to use a dict keyed by name, a list of tuples, or a
list of dicts. **All three are defensible**, and choosing is the exercise. Say in
one sentence why you picked yours.

What the requirement rules out is fifteen separate variables, or a plotting call
written out fifteen times. If adding a star means editing more than one line,
the structure is wrong — and you will feel it immediately, because you have to
loop over these stars at least three times (luminosity, plotting, labelling).

Worth knowing while you decide: **dictionaries preserve insertion order** in
modern Python, so a dict does not cost you control of the plotting order the way
it once would have.
:::

:::{admonition} Writing maths in labels — mathtext, and why the `r` matters
:class: tip dropdown

Matplotlib renders LaTeX inside `$...$` in any string it draws — axis labels,
legends, titles, annotations. This is
[**mathtext**](https://matplotlib.org/stable/users/explain/text/mathtext.html);
it needs no LaTeX installation.

| Write | Get |
|:--|:--|
| `r"$T_{\rm eff}$ [K]"` | $T_{\rm eff}$ [K] |
| `r"$L\ [L_\odot]$"` | $L\ [L_\odot]$ |
| `r"$R = 1\,R_\odot$"` | $R = 1\,R_\odot$ |
| `r"$p = R_p/R_\star$"` | $p = R_p/R_\star$ |

**Always prefix the string with `r`.** That makes it a
[raw string](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals),
so Python leaves the backslashes alone. Without it, in `"$T_{\rm eff}$"` the
`\r` is read as a **carriage return** before Matplotlib ever sees it, and what
arrives is `$T_{` + a control character + `m eff}$`.

The failure is nasty in a specific way: you get a `ValueError` **when the figure
is drawn**, not on the line where you wrote the string, and the error message
quotes `'$T_{'` — a string you never typed. This is the single most common
LaTeX-in-Matplotlib bug, and it is unrecognisable if you have not seen it once.

Useful pieces: `\rm` for upright (non-italic) text inside maths — variables are
italic, *labels* like "eff" are not; `\odot` for $\odot$; `\,` and `\ ` for
thin and normal spaces; `_{}` and `^{}` for sub- and superscripts.

**Why bother.** $T_{\rm eff}$ is a quantity with a standard printed form, and
writing `Teff` is the visual equivalent of writing `1.5e33 ergs` in a sentence.
You are already reading papers in this course; your figures should look like
they belong in one. It is also two extra characters, and you will reuse the same
strings all semester.
:::

### Spectral classes

Stars are classified by the letters **O B A F G K M**, hottest to coolest. The
boundaries are conventional rather than physical, so use these:

| Class | $T_{\rm eff}$ range [K] |
|:--|:--|
| O | 30000 – 45000 |
| B | 10000 – 30000 |
| A | 7500 – 10000 |
| F | 6000 – 7500 |
| G | 5200 – 6000 |
| K | 3700 – 5200 |
| M | 2000 – 3700 |

**Check that each star lands in the band its `Class` column claims.** Sirius A
is class A, so it should fall in the A band; the Sun is G and should fall in G.

:::{admonition} Deep Dive: what a spectral class actually is
:class: seealso dropdown

The letters are not a temperature scale. They came first — from the
**absorption lines** in stellar spectra, before anyone knew what set them.

Nineteenth-century astronomers sorted stars by how strong their hydrogen lines
were and labelled the groups A, B, C, ... in order. Later work showed the
sequence was really about **temperature**, that some classes were duplicates or
mistakes, and that the temperature ordering scrambled the alphabet. Rather than
renaming everything, astronomers dropped the redundant letters and reordered the
survivors by temperature — leaving **O B A F G K M**, a sequence that is *out of*
alphabetical order for reasons that are pure historical accident.

The numbers subdivide each class (A0 hotter than A9), and the Roman numeral is
the **luminosity class**: V is a main-sequence star, III a giant, I a
supergiant. So "G2 V" reads as *slightly-cooler-than-average G, on the main
sequence* — which is the Sun.

Why lines rather than temperature? Because a star's spectrum is what you can
*measure* from far away. Temperature is inferred. The classification survives
because it is closer to the observation.

**This is also the answer to why your temperature axis is reversed.** The
original diagram had spectral class on the x-axis, running O to M — hot to cool,
left to right. When temperature replaced the letters, the direction was kept so
old and new figures could be laid side by side. Your shaded bands are that
history, drawn.
:::

:::{admonition} The fifteen stars — open for the table
:class: important dropdown

Compute each luminosity **with your own function**. The last column is there to
check yourself against, not to copy.

The **Class** column is the spectral letter on its own — use that for the band
check; the **Type** column is the full classification, for reference only.

| Star | Class | Type | $R\ [R_\odot]$ | $T_{\rm eff}$ [K] | $L\ [L_\odot]$ (check) |
|:--|:--|:--|--:|--:|--:|
| Sirius B | — | white dwarf | 0.0084 | 25000 | 0.025 |
| Proxima Centauri | M | M5.5 V | 0.1542 | 3042 | 0.0016 |
| Barnard's Star | M | M4 V | 0.187 | 3223 | 0.0035 |
| α Centauri B | K | K1 V | 0.8632 | 5231 | 0.50 |
| **Sun** | G | G2 V | 1.0 | 5772 | 1.00 |
| α Centauri A | G | G2 V | 1.2234 | 5795 | 1.52 |
| Sirius A | A | A1 V | 1.711 | 9940 | 25.4 |
| Fomalhaut | A | A3 V | 1.842 | 8590 | 16.6 |
| Procyon A | F | F5 IV–V | 2.048 | 6530 | 6.9 |
| Vega | A | A0 V | 2.362 | 9602 | 40.1 |
| Spica A | B | B1 III–IV | 7.47 | 25300 | 20500 |
| Arcturus | K | K1.5 III | 25.4 | 4286 | 170 |
| Aldebaran | K | K5 III | 44.13 | 3910 | 439 |
| Rigel | B | B8 Ia | 78.9 | 12100 | 120000 |
| Betelgeuse | M | M1–2 Ia–Iab | 764 | 3590 | 90000 |

**Where these came from, and why other sources disagree.** Interferometric and spectroscopic measurements, mostly: Sirius B — Barstow et
al. (2005); Proxima and Barnard's — Boyajian et al. (2012); α Cen A and B —
Kervella et al. (2017); Sirius A — Liebert et al. (2005); Procyon A —
Aufdenberg et al. (2005); Vega — Aufdenberg et al. (2006); Fomalhaut — Mamajek
(2012); Spica — Tkachenko et al. (2016); Arcturus — Ramírez & Allende Prieto
(2011); Aldebaran — Richichi & Roccatagliata (2005); Rigel — Moravveji et al.
(2012); Betelgeuse — Dolan et al. (2016); Sun — IAU 2015 nominal values.

If you look these up elsewhere you will find different numbers, sometimes very
different — Betelgeuse's radius varies by more than 20% across the literature,
because a supergiant does not have a sharp edge. That is not sloppiness. It is
what measuring a real star is like, and it is worth knowing before Project 5,
where you measure one yourself.
:::

:::{tip} Self-check
The Sun must land at $(5772\ \mathrm{K},\ 1\,L_\odot)$ and sit **exactly on**
your $R = 1\,R_\odot$ line. Beside it means your grid and your point disagree
about units.

Fourteen of the fifteen stars carry a spectral class (Sirius B is a white dwarf
and has none). **Thirteen of those fourteen land inside the band they claim.**
If you get thirteen, your band code is right — do not go hunting for a bug in
the fourteenth.

Your computed $L$ should match the check column to within about 20%. Larger
than that is a bug; smaller differences are measurement uncertainty.
:::

:::{attention} Interpret your result — Part 2
One or two paragraphs addressing all three:

- **What the figure shows.** Where do the stars fall relative to your
  constant-radius lines — scattered, or concentrated? Your lines cover the whole
  plane and the stars do not. What does that tell you about real stars that the
  Stefan–Boltzmann law does not?
- **Sirius A and Sirius B** are a binary pair — same age, same distance, and far
  apart on your figure. Compute how many times fainter B is than A, and how many
  times *hotter*. Reconcile those two numbers: what must be true of B?
- **One star lands outside the band its Class column claims.** Which, by how
  much, and why is that neither a bug in your code nor an error in the table?

Then, separately — **one or two sentences, not part of the paragraph** — what
data structure did you use for the star table, and how many lines would change
if I asked you to add a sixteenth star? If the answer is more than one, say so
honestly; that is more useful to me than a structure you rearranged afterwards.
:::
:::{admonition} Keep this figure — Project 6 draws the same axes
:class: note dropdown
What you are plotting is *what the equation permits*: smooth lines of constant
radius. In Project 6 you plot the same axes from real Gaia measurements of
thousands of stars — lumpy, with a main sequence and a giant branch, none of
which is anywhere in the Stefan–Boltzmann law.

Your fifteen stars are a preview. With thousands, the structure becomes
unmissable.
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

:::{admonition} Deep Dive: the transit as a two-circle overlap problem
:class: seealso dropdown

**This is a geometry problem, not an astronomy problem.** Strip the physics away
and it is: *two circles overlap; how much area do they share?*

**The setup.** A planet passes in front of its star, as seen from Earth. Both
look like flat discs on the sky. The planet blocks some of the starlight, so the
star briefly looks dimmer. Plot brightness against time and you get a dip — a
**transit**. Thousands of planets have been found exactly this way.

**Why everything is a ratio.** We measure the star's radius as 1 and express
everything relative to it:

- $p = R_p/R_\star$ — planet radius in units of stellar radii. A Jupiter-like
  planet around a Sun-like star has $p \approx 0.1$.
- $z = d/R_\star$ — how far the *centre* of the planet's disc is from the
  *centre* of the star's disc, on the sky. $z=0$ is dead centre; $z > 1+p$ means
  the discs do not touch at all.
- $F$ — brightness now, divided by brightness with nothing in the way. So $F=1$
  means unobscured and $F = 0.99$ means 1% of the light is blocked.

**Why four cases.** Two circles have exactly four possible arrangements, and
that is all this piecewise function is:

1. **Apart** ($z \ge 1+p$) — no overlap, nothing blocked, $F=1$.
2. **Small circle entirely inside the big one** ($z \le 1-p$) — the planet
   blocks its own full area. Area of planet over area of star is
   $\pi R_p^2/\pi R_\star^2 = p^2$, so $F = 1-p^2$. **This is the flat bottom of
   the transit.**
3. **Big circle entirely inside the small one** ($z \le p-1$) — only possible if
   the planet is larger than the star. Total eclipse, $F=0$. Never happens for
   real planets; include it so the function is complete.
4. **Partially overlapping** — the messy one, and the only one needing the
   formula. This is **ingress and egress**, the sloped sides of the dip.

**What the formula is doing.** The shared region of two overlapping circles is a
*lens* shape. The standard way to get its area: cut it into two circular
segments — one from each circle — and add them.

- $\kappa_0$ and $\kappa_1$ are **half-angles**, obtained from the law of
  cosines applied to the triangle joining the two centres and one intersection
  point. $\kappa_1$ is the half-angle at the star's centre, $\kappa_0$ at the
  planet's. That is where the $\arccos$ comes from — it is the law of cosines
  solved for an angle.
- The square-root term is **twice** the area of that triangle — $2A$, where $A$
  is Heron's formula. It is subtracted because there are *two* circular sectors,
  one from each circle, and each overcounts by one triangle.
- Dividing by $\pi$ converts the blocked area into a fraction of the star's
  total area ($\pi \cdot 1^2 = \pi$), which is what "fraction of light blocked"
  means for a uniformly bright disc.

**The one astronomy assumption**, and it is a bad one: the star is *equally
bright everywhere on its disc*. Real stars are dimmer at the edges. Project 2
fixes exactly that.
:::

### Write three functions, not one

```python
def kappa0(p, z): ...      # arccos((p^2 + z^2 - 1) / (2*p*z))
def kappa1(p, z): ...      # arccos((1 - p^2 + z^2) / (2*z))
def flux(p, z):   ...      # the four cases; calls kappa0 and kappa1
```

Each with a docstring. `flux` handles the case logic and calls the other two —
it should not contain an `arccos` itself.

For this part, `p` is a positive finite scalar and `z` is a non-negative finite
scalar. `flux(p, z)` returns one scalar normalized flux. Part 4 is where you
extend the same physical model to arrays; do not quietly accept invalid scalar
inputs or change their meaning.

Write the cases in `flux` as `if`/`elif` with **the partial-overlap formula
last**, and **note which comparison operators you used** (`<` vs `<=` at each
boundary). One sentence. You will need it in Part 4.

:::{admonition} Why the course boundary convention is deliberate
:class: note dropdown

Mandel & Agol's printed Eq. (1) can place a contact point in the partial-
overlap line. At exact contact, the neighboring formulas have the same physical
flux, so this is not a disagreement about the model.

For this project, put contact points in the earlier non-partial branches:
`z >= 1 + p` gives `1`, `z <= 1 - p` gives `1 - p**2` when `p < 1`, and
`z <= p - 1` gives `0` when `p > 1`. Reserve the partial-overlap formula for
strictly interior points, `abs(1 - p) < z < 1 + p`.

That convention avoids evaluating an `arccos` argument at its floating-point
edge or dividing by a zero separation. It is a numerical-safety choice that
preserves the same mathematical light curve.
:::

:::{admonition} Why split it up
:class: note dropdown
Three reasons, and the third is the real one.

**You can test them separately.** $\kappa_0$ and $\kappa_1$ have known values you
can check by hand — at $z = 1-p$, $\kappa_0$ should come out to $\pi$ exactly.
Debugging a wrong $\kappa_0$ inside a four-branch function is much harder.

**`flux` stays readable.** The case logic is the interesting part and it fits on
a screen without the trigonometry in the way.

**Both `arccos` calls end up in exactly two places.** In Part 4 you have to fix a
domain problem. Two small functions is two edits; the same expressions inlined
and repeated is a hunt. This is what people mean by code being "maintainable" —
not that it looks tidy, but that a change lands in one place.
:::

:::{tip} Self-check — three tests
1. `flux(p, 0)` equals `1 - p**2`
2. `flux(p, 5)` equals `1` exactly
3. **Continuity.** Using $p = 0.1$, evaluate at $z = (1-p)\pm10^{-9}$ and
   $z = (1+p)\pm10^{-9}$. The two branches should agree to better than
   $10^{-11}$ — you will see something in the range $10^{-14}$ to $10^{-12}$

Test 3 finds real bugs. A backwards comparison or a sign error in $\kappa_0$
passes 1 and 2 and produces a light curve with a visible step in it.

**For test 3, print the actual difference.** You need the number itself for the
questions below, and a bare `True`/`False` throws it away.

You may *also* assert it — but if you do, **set the tolerance explicitly**:

```python
np.isclose(lo, hi, rtol=0, atol=1e-11)     # a claim you can defend
np.isclose(lo, hi)                          # rtol=1e-5: cannot fail here
```

The defaults would call your two values equal even if the branches disagreed by
a millionth, which is exactly the bug you are hunting. The function is fine; the
defaults are wrong for this problem. Knowing the difference is the skill.
:::

:::{attention} Interpret your result — Part 3
One short paragraph addressing both:

- **Why is test 3 a better test than tests 1 and 2?** Name a specific bug it
  catches that they miss.
- Test 3 agrees to something around $10^{-13}$ — not zero, and not $10^{-16}$.
  **Where does the number you got come from?** Shrink the $10^{-9}$ offset and
  say what happens to it.
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
code is the most transferable skill in this course. **Cite it in your Part 3
answers.**
:::

---

## Part 4 — The light curve, twice

For a circular edge-on orbit, mid-transit at $t=0$:

$$z(t) = \frac{a}{R_\star}\,\left| \sin\!\left(\frac{2\pi t}{P}\right) \right|$$

:::{admonition} Deep Dive: from orbital position to observed time
:class: seealso dropdown

Part 3 gives you flux as a function of **position**. An observation gives you
flux as a function of **time**. This equation is the bridge, and it is
trigonometry.

**The symbols**

- $a$ — the orbit's radius (its "semi-major axis"). Earth's is $1.5\times10^{13}$ cm.
- $P$ — the **orbital period**, how long one full circuit takes.
- $a/R_\star$ — the orbit's size in units of the star's radius. A hot Jupiter has
  $a/R_\star \approx 5\text{–}10$; Earth around the Sun is about 215.

**The derivation.** Put the star at the origin and let the planet go round a
circle of radius $a$ at constant speed. After time $t$ it has swept through
angle $\theta = 2\pi t/P$ — a full $2\pi$ per period, by definition. So its
position is

$$x = a\sin\theta, \qquad y = a\cos\theta$$

Now: **you are looking at this system edge-on**, so the orbit's plane is nearly
in your line of sight. You cannot perceive depth. All you see is the *sideways*
offset $x$ — the component perpendicular to your line of sight. The other
coordinate, $y$, points toward or away from you and is invisible.

So the apparent separation on the sky is $|x| = a|\sin\theta|$, and dividing by
$R_\star$ to match Part 3's units gives the formula.

**Why the absolute value.** $z$ is a distance and cannot be negative. Without it
you would get negative $z$ for half the orbit and your `arccos` arguments would
be nonsense.

**What the two halves of the sine mean.** $\theta = 0$ puts the planet directly
between you and the star — that is the transit. Half an orbit later,
$\theta = \pi$, $\sin\theta = 0$ again and $z = 0$ again — but now the planet is
*behind* the star. That is a **secondary eclipse**, a real and separately
observable event, and this simplified model cannot tell it apart from a transit.
Keep your time range near $t=0$ and it will not bite you.

**Assumptions being made**, all of which real analyses eventually drop:
perfectly circular orbit (real ones are ellipses), exactly edge-on (real ones
are tilted, so the planet cuts a chord rather than crossing the middle), and a
star that does not move (it actually wobbles slightly — which is how a
completely different planet-detection method works).
:::

Write it **twice**, with these two names:

```python
def transit_curve_loop(times, p, a_over_rstar, period): ...   # Version A
def transit_curve_vec(times, p, a_over_rstar, period):  ...   # Version B
```

- **Version A** — a Python `for` loop calling `flux` once per time
- **Version B** — vectorized with NumPy: build the `z` array, then masks

Use **`period = 3.0`** and **`a_over_rstar = 10`** throughout. For the figure use
`times = np.linspace(-0.25, 0.25, 2001)`; for the timing comparison use
$10^5$ points.

### Version B will not work the first time

Build the obvious version — compute the formula over the whole `z` array, then
[`np.where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
to pick each case. Run it. **You will get a `RuntimeWarning: invalid value encountered in
arccos`.** Your loop, running the same formula, was silent.

1. **Count the invalid calls.** Apply `arccos` to the whole argument array and
   count the `nan` it produces — that is how many times your code asked for
   something undefined. Then count the `nan` in your *final output*. **The two
   numbers will not match**, and the gap is the interesting part.
   [`isnan`](https://numpy.org/doc/stable/reference/generated/numpy.isnan.html) +
   [`count_nonzero`](https://numpy.org/doc/stable/reference/generated/numpy.count_nonzero.html)
   counts either in one line. Depending on how you wrote your `np.where`, your
   output may contain **no `nan` at all** — that is a legitimate result, not a
   failure to reproduce the bug. Say which you got and why
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

Then confirm the two versions agree —
[`allclose`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html)
compares whole arrays at once — and **time both** on $10^5$ points with
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

**In your code it is not.** You will find a disagreement of about $10^{-17}$,
because your function stores $1-p^2$ and you recover the depth as $1-(1-p^2)$ —
two roundings that do not cancel. `depth == p**2` is `False` for four of the
five values of $p$ you plot.

So compare with
[`np.isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html)
— and **set the tolerance yourself**. The defaults are `rtol=1e-5`, `atol=1e-8`,
which are about $10^{9}$ times looser than the discrepancy you are actually
seeing.
Passing by that margin is not the same as passing.

Read the page and state what you asked for. `rtol=1e-12` is defensible here and
you should be able to say why.

*The algebra is exact, the arithmetic is not, and knowing which claim you are
making is the skill.*
:::

:::{attention} Interpret your result — Part 4
One or two paragraphs addressing all three:

- **Why did your loop run clean and your array version raise a warning?** One
  sentence on what `if` does that an array expression does not — then how you
  know your fix is right rather than merely quiet.
- **Depth versus duration.** Measure both the total duration and the
  flat-bottom duration for $p = 0.05$ and $p = 0.25$. Depth grows $25\times$
  between them — do the durations? What does that say about whether a small
  planet is *shallow* or *quick*?
- **An Earth around a Sun-like star gives $p \approx 0.009$.** Compute that
  depth in parts per million, and say what it demands of a telescope.
:::
---

## One last question

Add a short markdown cell at the very end, under the heading `Looking back`:

**Which single number in this notebook do you trust least, and why?**

Two or three sentences. Any honest answer earns full credit; there is no answer
I am fishing for. Some of you will name the Betelgeuse radius, some the $10^{-17}$
in the depth check, some your own `arccos` fix.

:::{note} Why this question exists
Nothing you computed can settle it. Knowing where your own result is weakest is
a different skill from getting it right, and it is the one that separates people
who can be trusted with a result from people who merely produced one.

You will be asked this at the end of every project.
:::

---

## What you turn in

- `analysis.ipynb` — **use that filename** — with your four
  *Interpret your result* answers in place and `Looking back` at the end
- Both figures, saved as files as well as displayed
- `README.md` — what is here and how to run it

Pairs are fine. **You each write your own code and your own answers, and you
each have to explain every line of what you submit.**

:::{admonition} What a strong submission looks like
:class: note dropdown

Project 1 uses the course [project grading dimensions](../../01-course-info/projects.md#how-each-project-is-graded),
not a checklist. Strong work shows evidence across all four dimensions.

A strong Project 1 is one a stranger could still read: functions do one thing,
names say what they mean, and the self-checks are present and passing rather
than described. The figures are readable without being explained aloud. The
written answers say something the code does not, and where they are uncertain,
they say so.

The most common way to lose ground is a notebook that runs but that you cannot
defend line by line — which usually means it was assembled rather than written.
:::
