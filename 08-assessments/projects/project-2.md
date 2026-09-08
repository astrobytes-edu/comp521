---
title: "Project 2 — Numerical Integration"
subtitle: "COMP 521 | Fall 2026"
---

# Project 2 — Numerical Integration

**Due Monday, September 21, 11:59 pm PT** · pairs allowed; each student submits
independently written code and explanations.

## What you are building

In Project 1, a uniform stellar disk gave a central transit depth of $p^2$.
A limb-darkened disk is brighter near its centre, so the blocked light depends
on where the planet is. Computing that light requires an integral.

### Learning outcomes

By completing this project, you will be able to:

- Implement reusable quadrature functions and verify them with justified tests.
- Measure convergence and use it to predict a useful resolution.
- Formulate and validate integrals for blackbody radiation and transit photometry.
- Diagnose how an integrand's smoothness affects numerical accuracy.
- Compare fixed and adaptive quadrature using measured error and function-evaluation counts.

### Project overview

| Part | Task | Required evidence |
|:--|:--|:--|
| **1** | Build and validate a quadrature library | smooth convergence, a panel-count prediction, tests |
| **2** | Recover the Stefan–Boltzmann constant | cutoff/refinement table and dimensional check |
| **3** | Model a limb-darkened transit | uniform-disk validation, light curves, central depths |
| **4** | Diagnose lost convergence | transit and smooth-control studies, branch-point behavior |
| **5** | Implement and assess adaptive Simpson | accuracy versus actual function evaluations |

**The common interface matters:** each fixed rule accepts `f`, rather than
containing a particular integrand. The same library must handle all applications
without integrand-specific branches. Correcting a bug is expected when evidence
reveals one; rerun your tests after changing the implementation.

### Organize the work

```text
project-2/
├── README.md
├── integrate.py       # fixed rules and adaptive Simpson
├── planck.py          # blackbody integrands
├── transit.py         # Project 1 functions and limb darkening
├── tests/
│   └── test_*.py
└── analysis.ipynb     # imports, experiments, figures, interpretation
```

Use plain functions. Move your Project 1 transit functions into `transit.py`
and make any changes needed to import them without executing notebook analysis.
Keep reusable calculations in modules and figures and explanations in the
notebook. The [modules and tests reading](https://astrobytes-edu.github.io/comp521/python-functions-modules/)
and Lecture 6 provide the workflow.

**Two-week pace:** finish Parts 1–2 and begin transit validation in Week 1.
Complete Parts 3–5 in Week 2, reserving the final session for tests and a clean
notebook run. This is guidance, not a separate submission.

Each part ends with an interpretation prompt. Answer it in one or two concise
markdown paragraphs beside the relevant results; use your figures and tables
rather than repeating every number. There is no separate report.

## Part 1 — Build and validate your library

Implement these functions in `integrate.py`:

```python
def rectangle(f, a, b, n): ...
def trapezoid(f, a, b, n): ...
def simpson(f, a, b, n): ...
```

Each returns a float. Here `n` is the number of equal subintervals, not sample
positions. `f` accepts a NumPy array and returns finite real values with matching
shape. Document the rule, parameters, return value, and invalid-input behavior.

- Use the **left** rectangle rule, with first-order composite error for a
  sufficiently smooth integrand.
- Require a positive Python or NumPy integer `n`. Reject Booleans, floats
  including `4.0`, and non-positive counts with `ValueError`.
- Simpson also requires even `n`; reject odd counts with `ValueError`.
- Assume finite real limits with `a < b` and a valid callable. These are caller
  preconditions; additional general-purpose validation is not required.
- Do not hard-code integrands, use global problem parameters, or print from
  these functions. Implement the rules yourself; library integrators may be
  used only for optional comparisons.

If an integrand needs extra parameters, bind them in a lambda, nested function,
or `functools.partial` before passing it to the integrator. For example,
`lambda nu: planck_nu(nu, T)` presents a one-argument callable. Do not add
problem-specific parameters or an `args=` argument to the fixed-rule interface.

A **lambda expression** creates a small function without a `def` statement:
`lambda x: x**2` takes `x` and returns `x**2`. Its body is a single expression,
whose value is returned automatically. In `lambda nu: planck_nu(nu, T)`, `nu`
is the argument and `T` comes from the surrounding scope; keep `T` fixed during
the integration. See the [Python tutorial on lambda expressions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions).

### Measure convergence, then use it

Use $\int_0^{\pi/2}\sin x\,dx=1$. For each rule, evaluate
$n=16,32,64,128,256,512,1024$ and plot absolute error against $h=(b-a)/n$ on log–log axes.
Fit $\log |\mathrm{error}|$ against $\log h$ with `np.polyfit`; report each
measured order $q$ to one decimal place and compare with the expected orders
1, 2, and 4. We use $q$ because $p$ will denote the planet-to-star radius ratio.

Inspect the points before fitting. Fit only the truncation regime, where a
power-law trend is resolved. Do not take the logarithm of zero or add an offset
to manufacture a nonzero error. Report any zero separately. A rounding-floor
sweep is not required; the readings and Lecture 5 explain that regime.

From the Simpson fit $|\mathrm{error}|\approx Ch^q$, predict an even panel count
that will achieve absolute error $10^{-10}$. Record the prediction **before**
evaluating that grid, then check it once. Explain whether it meets the target.
The fitted model is neither a guaranteed error bound nor a proof of the minimum
count. No neighboring-grid search is required.

**Figure 1:** the three smooth convergence curves. Throughout the project,
label quantities and units (or identify them as dimensionless), use mathtext for
symbols, keep legends clear of the data, and save each figure as well as
displaying it in the notebook.

### Test the interfaces as you build them

Use **pytest** for the required tests. Put integration tests in
`tests/test_integrate.py`, import your functions from `integrate.py`, and name
each test `test_...` so pytest discovers it. For example:

```python
import pytest
from integrate import simpson


def test_simpson_rejects_odd_panel_count():
    with pytest.raises(ValueError):
        simpson(lambda x: x**2, 0.0, 1.0, 3)
```

`pytest.raises(ValueError)` checks that invalid input produces the expected
exception. For numerical answers, use `assert` with `pytest.approx` and an
explicitly justified tolerance, as described below. Add tests as you complete
each part. When one fails, read the failure message, investigate the cause,
and rerun it. The [pytest getting-started guide](https://docs.pytest.org/en/stable/getting-started.html)
explains discovery and assertions.

Write the following eight test groups in `tests/`. Groups 1–4 belong to this
part; add groups 5–8 when you reach the corresponding application or method.
Parametrization may produce more than eight collected tests.

| # | Case | Required check |
|:--|:--|:--|
| 1 | Rectangle and trapezoid on the sine integral, $n=1000$ | agreement with 1, each with a justified tolerance |
| 2 | Simpson on the same integral and grid | agreement with a tighter justified tolerance |
| 3 | Simpson on $\int_0^1x^3dx$, $n=2$ | agreement with $0.25$ to a stated floating-point tolerance |
| 4 | All fixed rules with `0`, `-2`, `2.5`, `4.0`, `True`; Simpson also with odd `n` | `ValueError` |
| 5 | Part 2 dimensionless Planck integral | agreement with $\pi^4/15$; state cutoff, count, and tolerance |
| 6 | Part 3, $u=0$, $p=0.1$, $z=0,0.5,1,1.1,1.2$ | finite results and agreement with the uniform-disk reference |
| 7 | Adaptive Simpson on sine; invalid `tol` and `max_depth` | known-value accuracy and `ValueError` for invalid controls |
| 8 | Adaptive Simpson with deliberately insufficient depth | `RuntimeError` when its acceptance test still fails |

Choose accuracy tolerances from an error bound, resolved refinement evidence,
or a stated floating-point allowance. Do not simply copy defaults. For an
absolute criterion, use `pytest.approx(expected, rel=0.0, abs=chosen_tolerance)`.
Explain the basis in a comment. Polynomial exactness is a property of the rule
in exact arithmetic, not a universal guarantee about floating-point execution.

From the repository root, using the active course environment, run:

```bash
python -m pytest
```

Keep these tests separate from notebook execution.

:::{tip} Optional checks with NumPy and SciPy
:class: dropdown

You may compare results with established libraries while debugging. No extra
figure, benchmark, written response, or SciPy installation is required for credit.

| Function and documentation | How to compare |
|:--|:--|
| [`numpy.trapezoid`](https://numpy.org/doc/stable/reference/generated/numpy.trapezoid.html) | Pass sampled values `y=f(x)` and the same nodes through `x=x`; compare with your trapezoid rule. |
| [`scipy.integrate.simpson`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simpson.html) | Pass sampled values and `x=x`. Use your same uniform grid with even `n` panels and therefore odd `n+1` samples. |
| [`scipy.integrate.quad`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html) | Pass a scalar callable and limits. It returns an integral and an estimated absolute error; it uses QUADPACK, not your adaptive Simpson algorithm. |

For the sampled-data checks, construct `x=np.linspace(a,b,n+1)`. Read the
parameters before comparing: sample values and a callable are different
interfaces. NumPy's `trapezoid` requires NumPy 2.0 or later; consult the
documentation matching your installed version.

For `quad`, set `epsabs` and `epsrel` deliberately and inspect warnings and the
returned error estimate. Known interior trouble points can be supplied through
`points` on a finite interval. Giving a reference method this information changes
what it knows about the problem; document that choice if you use it.

Agreement supports an implementation check, but two methods can share an
incorrect integrand or miss a feature. These comparisons supplement the required
analytic tests and do not replace your implementations. An estimated error is
not a guaranteed bound.
:::

**Interpret your result:** explain what the measured orders and panel-count
trial establish, how you chose your test tolerances, and why accepting a callable
allows the same rules to serve both physical applications.

## Part 2 — Recover the Stefan–Boltzmann constant

The Planck function gives blackbody intensity per unit frequency:

$$B_\nu(T)=\frac{2h\nu^3}{c^2}\frac{1}{e^{h\nu/k_BT}-1}
\qquad [\mathrm{erg\ cm^{-2}\ s^{-1}\ Hz^{-1}\ sr^{-1}}].$$

Integrating over frequency gives

$$\int_0^\infty B_\nu(T)\,d\nu=\frac{\sigma T^4}{\pi}.$$

Use CGS constants $h=6.62607015\times10^{-27}$ erg s,
$k_B=1.380649\times10^{-16}$ erg K⁻¹, and
$c=2.99792458\times10^{10}$ cm s⁻¹.

First substitute $x=h\nu/(k_BT)$ and evaluate the dimensionless integral:

$$\int_0^\infty\frac{x^3}{e^x-1}\,dx=\frac{\pi^4}{15}.$$

Implement its integrand in `planck.py`. Derive and implement its limiting value
at zero. For positive arguments, use
[`np.expm1`](https://numpy.org/doc/stable/reference/generated/numpy.expm1.html)
to evaluate $e^x-1$ accurately near zero. `expm1(0)` is still zero; evaluate the
positive subset separately so an intermediate `0/0` does not enter the sum.

Your integrator needs a finite upper limit. Make a compact table for
$b=10,20,40,60$ using Simpson with $n=20{,}000$. Compare with $\pi^4/15$,
select a cutoff, and repeat at that cutoff with $2n$. Increasing $b$ at fixed
$n$ also increases the spacing, so the cutoff table alone does not isolate the
tail error. Use the analytic reference and refinement together to justify the
accuracy you claim. Add test group 5.

Next implement $B_\nu(T)$, including its zero-frequency limit, and integrate
it for **one temperature**, $T=5772$ K. Set $\nu_{\max}=b k_BT/h$ using your
selected cutoff and panel count. Recover $\sigma$ and compare with both
Project 1's rounded constant $5.670374419\times10^{-5}$
erg cm⁻² s⁻¹ K⁻⁴ and

$$\sigma=\frac{2\pi^5 k_B^4}{15h^3c^2}.$$

The factor of $\pi$ converts isotropic outward intensity to surface flux through
an angular integral, $\int_{\rm hemisphere}\cos\theta\,d\Omega=\pi$.
Keep track of it when recovering $\sigma$. No spectrum figure or temperature
sweep is required.

**Interpret your result:** justify your endpoint treatment and cutoff, then
state how many digits of $\sigma$ your evidence supports. Distinguish omitted-tail,
quadrature, and floating-point errors from rounding of the supplied constant.

## Part 3 — Model a limb-darkened transit

Let $r$ be distance from the disk centre in units of $R_\star$, with
$0\le r\le1$. Use the linear limb-darkening model

$$I(r)=I_0[1-u(1-\mu)],\qquad \mu=\sqrt{1-r^2}.$$

At $u=0$ the disk is uniform. Positive $u$ makes the limb dimmer than the centre.
This approximates the effect of viewing cooler, shallower photospheric layers
near the limb. In this project $u$ is a supplied model parameter.

For a planet of radius $p$ at separation $z$, both in stellar-radius units, the
covered fraction of an annulus is

$$f(r,z)=\begin{cases}
1 & z+r\le p,\\
0 & z>r+p\ \text{or}\ z<r-p,\\
\dfrac{1}{\pi}\arccos\!\left(\dfrac{r^2+z^2-p^2}{2rz}\right)
& \text{otherwise}.
\end{cases}$$

The normalized blocked flux and observed flux are

$$\Delta F(z)=\frac{1}{F_{\rm tot}}\int_0^1 I(r)\,2\pi r\,f(r,z)\,dr,
\qquad F_{\rm tot}=\pi I_0(1-u/3),\qquad F(z)=1-\Delta F(z).$$

Implement the coverage and flux calculations in `transit.py`, calling your
Simpson rule. Set $I_0=1$; it cancels in the normalization. Use $0<p\le1$, $z\ge0$.
Handle these cases explicitly:

- At $z=0$, annuli with $r<p$ are covered and those with $r>p$ are not. The value
  at the single boundary radius does not change the exact integral. You may
  integrate only the covered interval $[0,p]$; state this choice.
- At $r=0$, set the radial integrand to zero because its area factor vanishes.
- For $z>0$, evaluate `arccos` only on the partial-overlap subset. Clip rounding
  excursions of its argument to $[-1,1]$. Clipping does not replace geometry masks.

### Validate, then make the light curves

Set $u=0$, $p=0.1$ and compare with Project 1's uniform-disk `flux(p,z)` at
$z=0,0.5,1,1.1,1.2$. Start with $n=4000$ and repeat with $2n$ before choosing
the tolerance for test group 6. Report the largest discrepancy over these cases.
The geometric formula supplies an independent mathematical reference, but its
implementation also needs to be correct. Do not increase $n$ solely to satisfy
an arbitrary tolerance.

For **Figure 2**, use $p=0.1$, $a/R_\star=10$, period 3 days, and
`times=np.linspace(-0.22,0.22,400)` in days. Reuse Project 1's central-transit
separation model and plot light curves for $u=0,0.3,0.6,0.9$ with $n=4000$.
Evaluate depths separately at $t=0$ and put them in a small table: the even time
grid does not include zero. Central geometry must work independently of the grid.

**Interpret your result:** describe what the uniform-disk check establishes and
its largest discrepancy. Explain the effect of positive $u$ on the depth and
shape of this central transit, using the intensity weighting in the integral.

## Part 4 — Diagnose lost convergence

Use only $z=0.5$, $p=0.1$, $u=0.6$ for this investigation. Define the
**normalized radial integrand**

$$g(r)=I(r)\,2\pi r\,f(r,0.5)/F_{\rm tot},\qquad
Q=\int_0^1g(r)\,dr=\Delta F(0.5).$$

A supplied numerical reference is

$$Q_{\rm ref}=0.011469823932502.$$

This is the **blocked fraction**, not the observed flux $1-Q$. For this project,
use an empirical reference uncertainty allowance of $10^{-12}$ in blocked-flux
units. Separate calculations using direct adaptive integration and a transformed
Gaussian rule agree well within that allowance. It is a conservative numerical
comparison allowance, not a rigorous mathematical bound.

Compute Simpson results for $n=200,400,800,1600,3200$. Plot
$|Q-Q_{\rm ref}|$ against $h=1/n$ and label it as discrepancy from a numerical
reference. Fit only discrepancies well above $10^{-12}$; if no clear power-law
regime appears, report that rather than forcing an order. No high-resolution
reference construction is required.

Use a smooth control on the same interval:

$$\int_0^1 2\pi r e^{-r}\,dr=2\pi(1-2/e).$$

Run it at $n=50,100,200,400$ and check for a regime consistent with fourth
order before rounding becomes important. If the smooth control fails, investigate
your implementation before attributing the transit behavior to its integrand.

Next inspect the outer branch point $r_+=z+p$. Evaluate $g(r_+-d)$ for
$d=10^{-3},10^{-4},10^{-5},10^{-6}$. Compare division by $d$ and by $\sqrt d$
to identify the leading power. What does that behavior imply about the derivative?
Simpson's usual fourth-order bound assumes sufficient smoothness, such as a
continuous fourth derivative. Losing that assumption does not by itself specify
an observed order; your measurements provide the evidence.

**Figure 3:** two panels showing the transit and smooth-control convergence,
and the local branch-point behavior. Use appropriate labels for their different
integrands. Do not repeat the convergence study at $u=0$ or $z=0$; central transit
has a different coverage discontinuity and was handled in Part 3.

**Interpret your result:** report the convergence behavior, the smooth-control
result, and the local exponent. Explain whether those observations support a
regularity limitation, an implementation problem, or unresolved evidence. A
specific transit slope is not a grading target.

## Part 5 — Implement and assess adaptive Simpson

Read [Adaptive Quadrature](https://astrobytes-edu.github.io/comp521/mod2-part2-quadrature/#adaptive-quadrature)
for the refinement logic, error estimate, and failure conditions. Use the
algorithm below to write your own recursive implementation.

A fixed grid uses equal spacing everywhere. Adaptive quadrature compares local
estimates and subdivides intervals whose estimated errors exceed their budgets.
Implement the following recursive function in `integrate.py`:

```python
def adaptive_simpson(f, a, b, tol, max_depth=50): ...
```

Return a float. For this interface, `f` accepts a scalar and returns a finite
real scalar; ensure your transit callable also supports that use. Assume finite
real limits with `a < b`.

Require finite positive `tol` and a non-negative Python or NumPy integer
`max_depth`, excluding Booleans. Invalid controls raise `ValueError`.
Count the initial interval as depth zero.

1. Compute a three-point Simpson estimate `whole` on the interval.
2. Compute estimates `left` and `right` on its halves.
3. If `abs(left + right - whole) <= 15*tol`, return the corrected estimate
   `left + right + (left + right - whole)/15`.
4. Otherwise recurse on each half with half the tolerance and add their results.

If the estimate still fails at `max_depth`, raise `RuntimeError` before
subdividing. Acceptance at that depth is allowed when the test passes.
If rounding makes a required midpoint indistinguishable from an endpoint,
report failure rather than continue subdivision. Do not return a partial answer.
Add test groups 7–8, including a deliberately unresolved depth-limited call.

The factor 15 comes from the leading smooth local Simpson error: two half
intervals have about $1/16$ of the whole-interval error. Their difference then
estimates 15 times the fine-rule error. The correction removes that leading
term when the model applies. Dividing `tol` between children allocates the
estimated-error budget; it does not guarantee the true error across a singularity
or an unsampled feature.

### Compare accuracy at a measured cost

For the same normalized $g(r)$ and $Q_{\rm ref}$ as Part 4, compare:

- fixed Simpson at $n=50,100,200,400,800,1600,3200$;
- adaptive Simpson at `tol` values $10^{-4},10^{-5},\ldots,10^{-10}$.

Reuse the $n=1600,3200$ results from Part 4; record their evaluation counts
with the same counting method, rerunning through your wrapper if necessary.
These finer grids extend the range of comparable accuracy.

**Figure 4:** reference discrepancy versus actual function evaluations on
log–log axes. Count scalar sample evaluations, including repeats: one vectorized
call containing $n+1$ positions counts as $n+1$ evaluations. A wrapper can record
this without changing the integrator interface. Reusing computed samples is
encouraged; state whether your implementation does so.

Compare costs at overlapping observed discrepancies, not at equal `tol` and
$n`. Mark depth failures and reference-limited points. A requested tolerance is
not a measured error, and evaluation count is not a timing measurement. No
particular speedup or adaptive convergence order is required.

A sampling limitation matters here: if all five initial positions miss a narrow
nonzero region, both estimates can be zero and the method accepts. Tightening
`tol` alone cannot reveal it. The prescribed geometry has nonzero coverage at
the midpoint; that does not establish reliability for other geometries. Known
support boundaries or a suitable change of variables can help, but implementing
those alternatives is not required in this project.

**Interpret your result:** use your measured costs to assess what adaptivity
buys at comparable accuracy. Explain what the tolerance estimate can and cannot
establish, including the possibility of a missed feature.

## What you turn in

Push your completed project to GitHub, then submit its repository URL to the
**Project 2 assignment in Canvas** by the deadline. Follow any repository setup
or invitation instructions provided there. Each student submits their own
repository URL. Your submission is the latest commit pushed by the deadline;
files left only on your computer are not submitted.

The [course project rubric](https://astrobytes-edu.github.io/comp521/projects/#how-each-project-is-graded)
applies: correct model and validation (40%), scientific reasoning (25%),
reproducibility and code design (20%), and communication and figures (15%).


- Your repository with the modules, tests, notebook, and a README explaining
  the environment and commands needed to run them.
- Eight required test groups passing with `python -m pytest`.
- Four saved figures: smooth convergence; limb-darkened light curves;
  convergence/branch-point diagnosis; fixed/adaptive accuracy versus evaluations.
- Compact Planck cutoff/refinement and transit validation/depth tables.
- Each part's interpretation, plus a final `Looking back` cell: identify the
  result you trust least and explain its specific uncertainty in two or three sentences.

Restart the notebook kernel and run every cell after your final module edits,
then run `python -m pytest`. Check that saved figures match that execution.
Submit your own code and explanations even when discussing the work with a
partner; you should be able to explain every line you submit.

The grading evidence is your general callable interface, justified tests,
resolved convergence measurements, physical validation, and interpretation of
limits. Optional library comparisons earn no separate credit and are not needed
for a complete submission. No rounding-floor sweep, substitution implementation,
or Monte Carlo experiment is assigned. Monte Carlo estimates integrals through
random sampling; it remains a conceptual comparison in the course readings.
