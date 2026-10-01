---
title: "Project 3 — Root Finding and Stellar Inference"
subtitle: "COMP 521 | Fall 2026"
---

# Project 3 — Root Finding and Stellar Inference

**Due Wednesday, October 7, 11:59 pm PT** · pairs allowed, own code and own write-up

## What you are building

**How do you find an unknown that appears on both sides of an equation?**

Build a root-finding library to recover Wien's constant, compute orbital
positions, and locate transit contacts. Then use algebra and a `Star` class
to compare equilibrium-temperature zones for your fifteen Project 1 stars.

| Part | You build | Evidence |
|:--|:--|:--|
| **1** | `roots.py` — bisection, Newton, secant | convergence measurements and behavior tests |
| **2** | Wien's constant | the physically relevant root and agreement with tabulated $b$ |
| **3** | Kepler's equation → the orbit → $z(t)$ | small equation residuals and recovery of Project 1's circular limit |
| **4** | Transit contact points and durations | agreement with the circular formula and comparison with grid estimates |
| **5** | `Star` class → simplified habitable zones | temperature round-trip checks and a fifteen-star comparison |

:::{admonition} Suggested pace
:class: tip

Thursday lab: work on Part 5. Build and check the `Star` class, then start the
fifteen-star comparison. By the end of Week 1, finish Parts 1–2 and begin
Part 3. In Week 2, check the circular orbit before finding contacts, then
complete the stellar comparison and rerun the notebook from a fresh kernel.
:::

:::{important} One library, several applications
Keep `roots.py` independent of the applications: each supplies its equation
and parameters through callables. Part 5 uses an algebraic solution.
:::

Answer each part's interpretation questions in **one or two short paragraphs**
after its calculations and figures in `analysis.ipynb`. The Deliverables
callouts summarize the requirements; there is no separate report. They are
completion reminders, not a points rubric. Your work is assessed using the
[course's four project dimensions](../../01-course-info/projects.md#how-each-project-is-graded):
correct model and validation, scientific reasoning, reproducibility and code
design, and communication and figures.

## Check each layer before combining them

| Layer | First check | If it fails, inspect |
|:--|:--|:--|
| Root finder | known root, endpoint root, and failure cases | stopping rule, history, and input validation |
| Physical root | positive Wien root and units of $b$ | domain and bracket, even if the residual is small |
| Orbit | $E=M$ at $e=0$, then Project 1's circular separation | radians, quadrant, array shape, and projection |
| Contacts | circular analytic durations, then eccentric cases | front/back selection, brackets, ordering, and inner Kepler accuracy |
| Stellar model | recover the boundary temperatures by substitution | radius and distance units, albedo, and powers |

A passing check supports that layer; it does not establish that every later
calculation is correct. The required tests and comparisons below implement
this sequence.

## Structure: classes start here

```text
project-3/
├── README.md
├── roots.py           # bisection, Newton, secant — plain functions
├── star.py            # the Star class
├── orbit.py           # Kepler's equation, z(t), contact points
├── transit.py         # your existing transit functions
├── integrate.py       # retained from Project 2
├── conftest.py        # retain the Project 2 test layout
├── tests/
└── analysis.ipynb
```

Use `python -m pytest` from the project directory. Reuse your tested Project 1–2
functions; you do not need to implement another quadrature method here.

| Component | Form | Reason |
|:--|:--|:--|
| Root finders | functions | no persistent state between calls |
| Transit model and orbit | functions | outputs depend on explicit parameters; closures bind application parameters |
| `Star` | class | radius and temperature belong to one object; properties derive consistent quantities from them |

Validate the star's stored radius and temperature. Compute luminosity and peak
wavelength from that state so the derived quantities stay consistent.

:::{admonition} Documentation
:class: tip dropdown

Review the course's functions/modules and testing material. For `Star`, follow
this reading route:

1. In [Chapter 6: OOP Fundamentals](../../03-python/06-oop-fundamentals.md),
   follow the introductory examples in **§§6.1–6.4**: construct an object with
   `__init__`, use `self`, call a method, and compute a derived `@property`.
   Focus on these examples rather than every exercise or extended example.
2. Read **§§10.1 and 10.4** of
   [Designing Small Scientific Types](../../04-scientific-computing/10-advanced-oop.md)
   for state validation and tests of the object's contract.

Inheritance, operator overloading, and other advanced class machinery are not
required. Dataclasses are optional; a small ordinary class is sufficient.

**Python:** [classes](https://docs.python.org/3/tutorial/classes.html),
[`property`](https://docs.python.org/3/library/functions.html#property),
[dataclasses](https://docs.python.org/3/library/dataclasses.html) (optional).

**NumPy:** [`sign`](https://numpy.org/doc/stable/reference/generated/numpy.sign.html),
[`diff`](https://numpy.org/doc/stable/reference/generated/numpy.diff.html),
[`arctan2`](https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html).
Sign changes help locate brackets on a sampled grid. Handle exact sampled
zeros separately so a contact is not counted twice.
:::

## Part 1 — The library

Implement these functions in `roots.py`:

```python
def bisect(f, a, b, atol=1e-12, rtol=0.0, max_iter=200): ...
def newton(f, fprime, x0, atol=1e-12, rtol=0.0, max_iter=200): ...
def secant(f, x0, x1, atol=1e-12, rtol=0.0, max_iter=200): ...
```

Each returns `(root, n_iter, history)`:

- `root`: the final numerical estimate of the root.
- `n_iter`: the integer iteration count, defined for each method below.
- `history`: the ordered sequence of root estimates recorded by the method.

Keep the Lecture 8 bisection contract and use these recording conventions:

- **Bisection:** history contains evaluated midpoints; `n_iter == len(history)`.
  Return the last evaluated midpoint. An endpoint root returns that endpoint,
  zero iterations, and an empty history.
- **Newton:** history begins with `x0`, followed by each updated iterate;
  `n_iter == len(history) - 1`.
- **Secant:** history begins with `x0, x1`, followed by each updated iterate;
  `n_iter == len(history) - 2`. Check both initial residuals before dividing.
  An initial root returns with zero updates and the two initial entries.

Newton and secant may return immediately at a computed zero residual;
otherwise use the stopping rule below. Bisection counts midpoint evaluations;
the open methods count updates. These are **not total function-evaluation costs**.

Use `ValueError` for invalid inputs, an invalid bracket, nonfinite function or
derivative values, a zero Newton derivative at a nonroot, or a zero secant
denominator when neither input is a root. Require finite real scalar inputs and
function values, finite nonnegative tolerances with at least one positive, and a
positive integer `max_iter` excluding Booleans. Bisection requires `a < b`;
secant requires distinct initial inputs.

Use `RuntimeError` for iteration-budget exhaustion or a bisection interval
whose tolerance is unmet but has no representable interior midpoint. Compare
signs directly rather than multiplying function values. Continuity and reliable
signs are mathematical preconditions; input validation cannot establish them.

### What a tolerance means

The allowance at a candidate $x$ is

$$\tau_x = \mathrm{atol} + \mathrm{rtol}\,|x|.$$

`atol` is the **absolute tolerance**, in the same units as the root. A positive
value supplies an allowance near zero. `rtol` is the **relative tolerance**, a
dimensionless fraction that scales the allowance with the candidate root's
magnitude. Near $10^{12}$, an absolute tolerance of $10^{-12}$ is below
double-precision spacing.

For bisection, evaluate the midpoint $m$ of the **current** bracket and use
$B_m=\max(m-a,b-m)$. Accept a computed zero residual or $B_m\le\tau_m$.
For an exact midpoint, $B_m=(b-a)/2$. Use the bracket **before** updating it
to bound that midpoint's error, and record the midpoint before returning.

For Newton and secant, accept an updated iterate if its computed residual is
zero or its last step is no larger than $\tau_x$. A small step does not certify
a small residual or root error; check the defining equation in each application.
A computed zero can also result from rounding or underflow.

### Measure convergence

Use $f(x)=x-5(1-e^{-x})$, with **bisection on $[3,10]$, Newton from $x_0=4$,
and secant from $(x_0,x_1)=(3,6)$**. Use
$x_\star=4.965114231744276$ as the double-precision reference; do not round it
before computing errors.

Plot $e_n=|x_n-x_\star|$ against history index on a log $y$ axis. State which
entries are starting guesses. Report each solver's returned iteration count
and final error. Distinguish satisfying its stopping rule from the first
recorded error below $10^{-12}$. Omit zero errors from the logarithmic plot and
identify them in the caption rather than replacing them with invented values.

- **Newton and secant:** estimate the order using

  $$p_n=\frac{\ln(e_{n+1}/e_n)}{\ln(e_n/e_{n-1})}.$$

  Use and report the last consecutive triple with $10^{-13}<e_n<1$ for all
  three errors and a nonzero denominator. This band avoids the numerical floor
  here but does not establish an asymptotic regime. If no triple qualifies,
  report that. Compare with orders 2 and $(1+\sqrt{5})/2$.
- **Bisection:** reconstruct the first 20 brackets from the initial bracket
  and recorded midpoints without changing the return interface. Measure
  successive width ratios and the slope of $\ln(b_n-a_n)$ against $n$.
  Compare with $1/2$ and $-\ln 2$. Plot the bracket half-width alongside the
  actual errors. Actual midpoint errors need not decrease at every update.

:::{tip} Self-check
Bisection halves the bracket in exact arithmetic. Check this before rounding
dominates; actual midpoint errors need not halve.
:::

:::{attention} Interpret your result — Part 1
- Use your convergence measurements to explain why Newton/secant order and
  bisection bracket contraction measure different quantities.
- Under what assumptions does bisection bound the root error? What does an
  unsafeguarded Newton step fail to preserve?
- Explain `atol` and `rtol` using roots near $1$ and $10^{12}$. Which tolerance
  controls this Wien calculation?
:::

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `roots.py` with the three solvers, histories, and stated failure behavior.
- [ ] A convergence figure, measured orders/width contraction, and iteration counts.
- [ ] Solver tests and one or two paragraphs answering the Part 1 questions.
:::

## Part 2 — Where Wien's constant comes from

The wavelength form of Wien's law is $\lambda_{\max}T=b$, with tabulated
$b\approx0.2897772$ cm·K. Recover this value from the Planck spectrum:

$$x=5(1-e^{-x}),\qquad x\equiv\frac{hc}{\lambda k_BT},\qquad b=\frac{hc}{xk_B}.$$

Use the same CGS constants as Project 2:

$$
\begin{aligned}
h &= 6.62607015\times10^{-27}\ \mathrm{erg\ s},\\
c &= 2.99792458\times10^{10}\ \mathrm{cm\ s^{-1}},\\
k_B &= 1.380649\times10^{-16}\ \mathrm{erg\ K^{-1}}.
\end{aligned}
$$

:::{admonition} Derivation: the wavelength peak
:class: seealso dropdown

Project 2 integrated the Planck function per unit frequency. Per unit wavelength,

$$B_\lambda(T)=\frac{2hc^2}{\lambda^5}\frac{1}{e^{hc/(\lambda k_BT)}-1}.$$

For finite positive $\lambda$ and $T$, differentiate with respect to wavelength
and set the derivative to zero. Substituting $x=hc/(\lambda k_BT)>0$ gives

$$xe^x=5(e^x-1)\quad\Longleftrightarrow\quad x=5(1-e^{-x}).$$

The nonzero root has no elementary inverse. The rearranged equation also holds
at $x=0$, outside the derivation's finite-wavelength domain. Select the positive,
nonzero root using the physics and the function's behavior.
The peaks of $B_\nu$ and $B_\lambda$ are different density maxima; do not obtain
one peak merely by substituting $\lambda=c/\nu$ into the other.
:::

### Investigate root selection

Run your Newton method from $x_0=1$ and inspect its history.

1. Report the returned root and residual. Compute the implied $b$ and
   $\lambda_{\max}$ at **5772 K** if the root is nonzero. If it is exactly zero,
   state why these quantities are undefined instead of dividing by zero.
2. Explain why $f(0)=0$ does not identify a finite-wavelength spectral peak.
3. Recover the desired root using a bracket or starting guess justified by the
   function and its physical domain.
4. Plot $f$ and $f'$ in two panels, marking both roots, the Newton history,
   and the derivative's zero at $x=\ln5$. Run Newton from that point and
   report the outcome. The evaluated derivative may be zero or merely tiny
   in floating point; an enormous step or reported failure is evidence to explain.

The near-zero result depends on how you evaluate $f$; no particular sign or
last digit is expected. A small derivative can send Newton outside the domain.

:::{tip} Self-check
The desired root is approximately $4.965114231744276$, giving
$b\approx0.2897772$ cm·K to the precision of the tabulated value.
:::

:::{attention} Interpret your result — Part 2
- What happened from $x_0=1$, and what information helped you select the
  physically relevant root?
- Why does bisection on $[3,10]$ exclude the zero root? Why would an arbitrary
  sign-changing bracket not necessarily select the root you wanted?
- How do integration in Project 2 and peak finding here connect
  Stefan–Boltzmann's law and Wien's law to the same Planck spectrum?
:::

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] Derived $b$ in cm·K and a comparison with the tabulated value.
- [ ] The two-panel Wien figure, including the $x_0=1$ history and derivative zero.
- [ ] Recorded starting-point outcomes and one or two interpretation paragraphs.
:::

## Part 3 — The orbit

Read the [Science Background](project-3-science-background.md) for diagrams and
derivations of the orbital angles, sky projection, and transit contacts.

Project 1 used $z(t)=(a/R_\star)|\sin(2\pi t/P)|$ for a circular, edge-on
orbit. Now compute the projected separation for an eccentric orbit.

For a bound Kepler orbit, $0\le e<1$. With **$t=0$ at periastron**,

$$M=E-e\sin E,\qquad M=\frac{2\pi t}{P}.$$

Mean anomaly $M$ increases uniformly with time. Eccentric anomaly $E$ is a
geometric parameter on the ellipse. Given $M$ and $e$, solve for $E$.

:::{admonition} Geometry and assumptions
:class: seealso dropdown

For an isolated Newtonian two-body orbit, recover position at a given time
by inverting Kepler's equation. Numerical ODE integration is also valid and
becomes useful when additional forces prevent this reduction.

True anomaly $\nu$ is the angle from periastron measured at the focus. The
orbital radius and sky-projected separation are

$$r=a(1-e\cos E),\qquad
z=\frac{r}{R_\star}\sqrt{1-\sin^2i\,\sin^2(\nu+\omega)}.$$

Inclination $i$ is measured relative to the sky plane; $i=\pi/2$ is edge-on.
Fix $\omega=\pi/2$, and choose the observer orientation so the planet is in
front at periastron. For the required edge-on cases, mid-transit is then $t=0$.
Projected separation alone does not tell you whether the planet is in front.
:::

### What to build

In `orbit.py`:

```python
def solve_kepler(M, e, atol=1e-12, rtol=0.0, max_iter=100): ...  # (E, n_iter)
def true_anomaly(E, e): ...                                 # radians
def separation(t, period, a_over_rstar, e, inc): ...          # scalar or array
```

Use **your own Newton** from Part 1, with closures:

```python
resid  = lambda E: E - e*np.sin(E) - M
dresid = lambda E: 1 - e*np.cos(E)
```

Use the quadrant-aware expression

$$\nu=2\operatorname{atan2}\!\left(\sqrt{1+e}\sin(E/2),
                                  \sqrt{1-e}\cos(E/2)\right).$$

For $\omega=\pi/2$, a stable equivalent projected separation is

$$z=\frac{r}{R_\star}\sqrt{\sin^2\nu+\cos^2i\,\cos^2\nu}.$$

This sum of squares avoids cancellation near an edge-on mid-transit. Explain
its equivalence to the geometric expression above.

**Conventions:** angles in radians; `t` and `period` in the same units (days
for the examples); positive `period` and `a_over_rstar`; $0\le e<1$ and
$0\le i\le\pi/2$. `solve_kepler` takes scalar $M,e$ and returns the solution on
the same unwrapped branch as $M$. If you reduce $M$ modulo $2\pi$ internally,
restore that branch in the returned $E$. `separation` returns a scalar for a
scalar input and preserves an array's shape. Reject nonfinite or out-of-domain
inputs with `ValueError`.

### Compare starting guesses and check the circular limit

Use `M = np.linspace(0, 2*np.pi, 400)` at
$e=0,0.3,0.6,0.9,0.99$. Compare $E_0=M$ with $E_0=\pi$ on this interval,
using the same tolerances and `max_iter=100`. You may call `newton` directly
for this comparison; no extra argument in `solve_kepler` is required.
Report failures, mean and maximum iterations among successful runs, and their
residuals. Use this evidence to choose and document a `solve_kepler` starting
strategy. Failures on this grid do not establish a universal eccentricity
threshold. The high-$e$ cases are solver tests, not viable transit models at
$a/R_\star=10$.

For the circular-limit check, use $P=3.0$, $a/R_\star=10$,
`t = np.linspace(-0.25, 0.25, 501)`, $e=0$, and $i=\pi/2$. Compare with
Project 1's formula using `rtol=0, atol=1e-11`. Report the maximum absolute
error, not a prescribed round-off pattern. Relative error is undefined where
the reference separation is zero.

:::{attention} Interpret your result — Part 3
- How do starting guess and eccentricity affect work and failures? Explain
  using the derivative $1-e\cos E$, and support your choice with the sweep.
- How does your circular limit compare with Project 1? Explain cancellation
  in the subtractive formula and why the sum-of-squares form helps.
- Why can we solve for position through a scalar root here? Give an example
  of a physical change that would require a different orbital model.
:::

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `solve_kepler`, `true_anomaly`, and shape-preserving `separation` in `orbit.py`.
- [ ] A starting-guess comparison table, residual checks, and circular-limit error.
- [ ] The relevant tests and one or two interpretation paragraphs.
:::

## Part 4 — Contact points and duration

Let $p=R_p/R_\star$ be the planet-to-star radius ratio. For a **nongrazing
transit** with $0<p<1$, four contacts mark tangency:

| Contact | Condition | Event |
|:--|:--|:--|
| 1 | $z=1+p$ | overlap begins |
| 2 | $z=1-p$ | planet becomes fully inside the stellar disc |
| 3 | $z=1-p$ | planet begins to leave the stellar disc |
| 4 | $z=1+p$ | overlap ends |

Solve $z(t)-(1\pm p)=0$. Return ordered times $(t_1,t_2,t_3,t_4)$ from
`contact_points(period, a_over_rstar, p, e, inc)`, and report
$T_{14}=t_4-t_1$ and $T_{23}=t_3-t_2$. $T_{23}$ is the full-overlap duration;
it is a flat-bottom duration for the uniform-brightness model used here.

Use $P=3.0$ days, $a/R_\star=10$, $p=0.1$, $i=\pi/2$, and
$e=0,0.3,0.6$, unless a check specifies otherwise. These required configurations
have four distinct contacts. Report failure if four distinct contacts are not
found; a general grazing/no-transit model is not required.

**Bracket first, then solve.** For these configurations, sample
$[-P/4,P/4]$, locate sign changes for each contact equation, and pass each
bracket to bisection. Retain exact sampled roots once. Refine the sampling if
needed and check that the four times are distinct and correctly ordered.

:::{warning} Select the primary transit
Across a full orbit, projected separation can cross the same threshold when
the planet is behind the star. Those crossings belong to the secondary eclipse.
The stated time window isolates the primary event for this project's required
configurations; it is not a universal event-selection rule for arbitrary orbits.
:::

:::{note} Why use a root finder here?
Practice a reusable method: evaluate a trajectory, bracket a threshold
crossing, and refine its time. Each eccentric-orbit evaluation solves Kepler's
equation. Special geometries also allow direct solutions, including an
arcsine for circular, edge-on contacts.
:::

### Circular check and eccentric light curves

At $e=0$, $i=\pi/2$, compare against your Project 1 grid estimates for
$p=0.05$ and $0.25$, and against

$$T_{14,23}=\frac{P}{\pi}\arcsin\!\left[\frac{1\pm p}{a/R_\star}\right].$$

| $p$ | $T_{14}$ (days, rounded) | $T_{23}$ (days, rounded) |
|:--|:--|:--|
| 0.05 | 0.100453 | 0.090855 |
| 0.25 | 0.119679 | 0.071687 |

Compute the analytic reference; the table is rounded. Report the root-found
duration error and the original grid spacing. Errors in **both** contact times
and the nested Kepler solve affect duration: a $10^{-12}$ stopping tolerance
on one time does not promise $10^{-13}$ duration accuracy.

Plot the three required eccentric light curves using your **uniform-disk**
`flux(p, z)` from `transit.py`. Mark all four contacts on each curve and report
$T_{14}$ and $T_{23}$. The period, scaled semimajor axis, inclination, and
periastron orientation remain fixed as eccentricity changes.

:::{attention} Interpret your result — Part 4
- How do the durations change with eccentricity in this fixed orientation?
  Relate the change to orbital speed near periastron.
- Compare your circular duration error with the Project 1 grid estimate.
  What grid spacing would be needed to resolve a similar time scale?
- Why might a circular orbit with a different $a/R_\star$ resemble one of
  these eccentric transits? What does a duration alone fail to determine?
:::

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `contact_points` in `orbit.py`, with ordered times and reported failures.
- [ ] A duration table and comparison with the circular formula and Project 1 grid.
- [ ] One three-eccentricity light-curve figure with contacts, plus interpretation.
:::

## Part 5 — Stars, and where the algebra wins

Implement the complete `Star` class in `star.py` with this interface:

```python
class Star:
    def __init__(self, name, radius, teff): ...  # radius in R_sun; teff in K
    @property
    def luminosity(self): ...                  # L_sun
    @property
    def lambda_max(self): ...                  # cm, using your derived b
    def habitable_zone(self, albedo=0.3): ...   # (inner, outer) in AU
```

Store readable `name`, `radius`, and `teff` attributes; radius is in solar radii
and temperature is in kelvin. Require finite, positive radius and temperature
at construction. If those values can change later, validate each new value; a
read-only design is also acceptable. Compute `luminosity` and `lambda_max` from
the current state rather than storing separate copies.

Reuse your tested Project 1 Stefan–Boltzmann calculation. You may copy its
`luminosity(radius, teff, solar=False)` function into `star.py`, import it from a
submitted module, or refactor it while preserving its units and behavior. The
`Star.luminosity` property must return $L_\odot$ from the object's current
radius and temperature. Check that the Sun gives the same result as in
Project 1.

Use $1\ \mathrm{AU}=1.495979\times10^{13}$ cm and
$R_\odot=6.957\times10^{10}$ cm.

For a planet with Bond albedo $A$, uniform redistribution of absorbed energy,
unit thermal emissivity, and no internal heating, radiative balance gives

$$T_{\rm eq}=T_\star\sqrt{\frac{R_\star}{2d}}(1-A)^{1/4}.$$

Use the existing simplified criterion $273<T_{\rm eq}<373$ K at $A=0.3$.
Require $0\le A<1$. The inner boundary corresponds to 373 K and the outer
boundary to 273 K. **Rearrange this equation for $d$ by hand and implement the
algebraic result.** No root finder is needed.

:::{note} Limits of this model
These are equilibrium-temperature bounds, not a climate-based prediction of
surface liquid water. The model omits atmospheric greenhouse warming and uses
one albedo for all stars and planets. Surface pressure also affects the
liquid-water temperature range. For climate-based habitable-zone calculations,
see [Kopparapu et al. (2013)](https://arxiv.org/abs/1301.6674).
:::

Instantiate **all fifteen Project 1 stars** from the local data. Plot one
horizontal interval per star, ordered and labelled by $T_{\rm eff}$. Use a log
distance axis in AU; mark Earth at 1 AU and identify the Sun and Proxima Centauri.

:::{tip} Self-check
With the Project 1 stellar values, the Sun's bounds are approximately
**0.466–0.870 AU** and Proxima Centauri's **0.020–0.037 AU**. Earth lies outside
this simplified solar interval. Explain the model limitation rather than
adjusting the calculation to put Earth inside.
:::

:::{attention} Interpret your result — Part 5
- Why can this calculation be done algebraically?
- Why does the equilibrium-temperature criterion exclude Earth? Contrast its
  approximate equilibrium temperature of 255 K with its mean surface temperature
  of 288 K, and identify the omitted physical mechanism.
- For an Earth-sized planet ($R_\oplus=0.00916R_\odot$) at the **arithmetic
  midpoint** of each of the Sun's and Proxima's intervals, take a circular orbit
  so $a=d$. Compute the full-overlap transit depth $p^2$ and $a/R_\star$.
  What do these quantities say about transit geometry and signal depth? Why do they not establish surface habitability or, by
  themselves, detection significance?

Then explain in **one or two sentences** why `Star` is a class while the root
finders and orbital calculations remain functions.
:::

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `star.py` with validated stellar state, derived properties, and algebraic bounds.
- [ ] The fifteen-star zone figure and Sun/Proxima transit-depth and distance comparison.
- [ ] Temperature round-trip tests, interpretation, and the class-versus-function rationale.
:::

## One last question

End the notebook with a markdown cell headed `Looking back`:

**Which single number in this notebook do you trust least, and why?**

Answer in two or three sentences. Any honest answer earns full credit.

## Required tests

Include these **eight test cases** in `tests/`, retaining your Lecture 8 solver
contract tests. A case may use several assertions or parameterized inputs.

| # | Test | What it checks |
|:--|:--|:--|
| 1 | All three methods find the positive Wien root and agree to $10^{-10}$ | solver agreement on the selected root |
| 2 | `bisect` raises `ValueError` for same-sign nonzero endpoint values | bracket precondition |
| 3 | Newton on $f(x)=x^2+1$, $f'(x)=2x$, from $x_0=0$ raises `ValueError` | exactly zero derivative at a nonroot |
| 4 | $\lvert E-e\sin E-M\rvert<10^{-12}$ on the Part 3 sweep for your selected strategy | Kepler equation residual |
| 5 | `solve_kepler(M, 0)` returns $E=M$ | circular limit, including negative and multi-period $M$ |
| 6 | Circular edge-on `separation` matches Project 1 with `rtol=0, atol=1e-11`; scalar and array shapes are preserved | orbital geometry and interface |
| 7 | Reinsert the returned zone bounds into $T_{\rm eq}$ and recover 373 and 273 K | algebra and unit conversions |
| 8 | Bisection resolves a root near $10^{12}$ using `rtol` | scale-aware stopping |

Analytic-limit checks and defining-equation residuals catch different errors;
keep both. Use explicit tolerances rather than relying on comparison defaults.

## Required figures

1. **Convergence:** the three error histories and bisection's bracket half-width;
   log error axis, with starting guesses and omitted zero errors identified.
2. **Wien root selection:** $f$ and $f'$ in two panels, both roots, the $x_0=1$
   history, and the derivative zero. Axis limits must contain the displayed iterates.
3. **Transit timing:** uniform-disk light curves at $e=0,0.3,0.6$, with all
   four contacts marked on each.
4. **Fifteen-star zones:** labelled temperature ordering, log distance in AU,
   Earth at 1 AU, and the Sun and Proxima identified.

Use Project 1's figure standards: labelled units, readable mathematical labels,
legends clear of the data, and figures saved to files.

## What you turn in

- The repository with modules and tests, passing under `python -m pytest`.
- `analysis.ipynb` with calculations, the five interpretations, and `Looking back`.
- The four figures saved as files.
- `README.md` explaining the contents and how to run the work.

Pairs are allowed, but each student writes their own code and answers and must
be able to explain every submitted line.

:::{warning} Before your final commit
Restart the notebook kernel and run all cells, then run `python -m pytest`
from the project directory. Check that the notebook and saved figures reproduce.
:::
