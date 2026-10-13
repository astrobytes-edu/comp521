---
title: "Project 4 — ODEs and Exoplanet Mass–Radius Relations"
subtitle: "COMP 521 | Fall 2026"
---

# Project 4 — ODEs and Exoplanet Mass–Radius Relations

**Assigned Wednesday, October 14** · **Due Wednesday, October 28, 11:59 pm PT**

Pairs allowed, own code and own write-up.

## What you are building

Test an ODE solver against a known solution, then use it to reproduce a published
mass–radius relation for solid exoplanets.

| Part | You build | Evidence |
|:--|:--|:--|
| **1** | Euler, explicit midpoint RK2, and RK4 | convergence against the simple harmonic oscillator (SHO) |
| **2** | A planet model with adaptive surface finding | agreement with a constant-density analytic planet |
| **3** | Iron, silicate, and water-ice mass–radius curves | comparison with Seager et al. (2007), numerical refinement, and NASA exoplanet observations |

All equations, coefficients, constants, and numerical procedures are below,
including a NASA data download and local CSV fallback. No code or data from
Projects 1–3 is needed. Answer each part's two interpretation questions in one
or two short paragraphs after its calculations in `analysis.ipynb`. No separate
report is required.

Suggested pace: SHO checks, constant-density planet, then the three-material sweep.

## Structure

```text
project-4/
├── README.md
├── ode.py             # euler, rk2, rk4, rk4_step
├── eos.py             # SI-to-CGS conversion and make_eos
├── structure.py       # make_rhs, find_surface, integrate_planet
├── tests/
├── data/
│   └── project4-nasa-exoplanets.csv
└── analysis.ipynb
```

Keep reusable functions in modules and calculations, figures, and interpretation
in the notebook. Use NumPy, Matplotlib, pytest, and Pandas; run `python -m pytest`
from the project directory. Pandas is limited to reading and selecting NASA rows
in Part 3. Project 5 develops the broader data-analysis workflow.

## Part 1 — Validate the ODE methods

Implement these functions, using NumPy arrays for the state:

```python
def rk4_step(f, x, y, h): ...          # state after one RK4 step

def euler(f, y0, x0, x1, h): ...       # (final x, final state)
def rk2(f, y0, x0, x1, h): ...         # explicit midpoint

def rk4(f, y0, x0, x1, h): ...        # uses rk4_step
```

`f(x, y)` returns the derivative vector. Require `h > 0` and `x1 >= x0`.
Shorten a final partial step to land on `x1`; do not round away the remaining interval.

For a step from $(x,\mathbf y)$:

- **Euler:** $\mathbf y_{\rm new}=\mathbf y+h f(x,\mathbf y)$.
- **Explicit midpoint RK2:** $k_1=f(x,\mathbf y)$,
  $k_2=f(x+h/2,\mathbf y+h k_1/2)$, then
  $\mathbf y_{\rm new}=\mathbf y+h k_2$.
- **Classical RK4:** $k_1=f(x,\mathbf y)$,
  $k_2=f(x+h/2,\mathbf y+h k_1/2)$,
  $k_3=f(x+h/2,\mathbf y+h k_2/2)$,
  $k_4=f(x+h,\mathbf y+h k_3)$, then
  $\mathbf y_{\rm new}=\mathbf y+h(k_1+2k_2+2k_3+k_4)/6$.

### The idealized check: SHO

Use dimensionless time and state, with $q''=-q$, $q(0)=1$, and $q'(0)=0$:

$$\mathbf y=(q,v),\qquad \mathbf y'=(v,-q),\qquad
\mathbf y_{\rm exact}(t)=(\cos t,-\sin t).$$

Integrate to $t=2$ using $h=0.1/2^j$ for $j=0,1,2,3,4$. Measure the endpoint
error over both components:

```python
error = np.max(np.abs(y_final - np.array([np.cos(2), -np.sin(2)])))
```

Plot error versus $h$ on log–log axes and fit slopes with `np.polyfit`.
Expect orders near 1, 2, and 4; label the methods and reference slopes.
This checks the ODE methods, not planetary physics or surface finding.

**Interpret — Part 1**

1. Report your three measured orders. How does halving $h$ change the error for
   each method in the convergence regime?
2. RK4 evaluates the derivative four times per step. Why can it still require
   less total work than Euler at a specified accuracy? What evidence would you
   need to choose a method for another problem?

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `ode.py` with Euler, explicit midpoint RK2, RK4, and `rk4_step`.
- [ ] One SHO convergence figure, with the three measured orders.
- [ ] The ODE-method checks and one or two interpretation paragraphs.
:::

## Part 2 — Build and check one planet

Assume a spherical, static planet of uniform composition, with no atmosphere,
rotation, or temperature evolution. Integrate $(m,P)$, enclosed mass and
pressure, with radius as the independent variable.

$$\frac{dm}{dr}=4\pi r^2\rho(P),\qquad
\frac{dP}{dr}=-\frac{Gm\rho(P)}{r^2}.$$

These equations accumulate shell mass and balance the pressure gradient against
gravity. At the centre, $m(0)=0$ and $P(0)=P_c$;
the surface is the first outward radius $R$ where $P(R)=0$, and $M=m(R)$.

### Constants and equation of state

Use CGS throughout the planet calculation:

| Constant | Value |
|:--|:--|
| $G$ | $6.674\times10^{-8}$ cm³ g⁻¹ s⁻² |
| $M_\oplus$ | $5.972\times10^{27}$ g |
| $R_\oplus$ | $6.371\times10^8$ cm |

Use the modified-polytrope EOS from Seager et al. (2007), Table 3:

$$\rho(P)=\rho_0+cP^n.$$

| Material | $\rho_0$ [kg m⁻³] | $c$ [kg m⁻³ Pa⁻ⁿ] | $n$ |
|:--|--:|--:|--:|
| Fe (α) | 8300.00 | 0.00349 | 0.528 |
| MgSiO₃ (perovskite) | 4100.00 | 0.00161 | 0.541 |
| H₂O (ice) | 1460.00 | 0.00311 | 0.513 |

These coefficients are **SI**. Since $\rho_{\rm CGS}=10^{-3}\rho_{\rm SI}$ and
$P_{\rm CGS}=10P_{\rm SI}$,

$$\rho_{0,\rm CGS}=10^{-3}\rho_{0,\rm SI},\qquad
c_{\rm CGS}=10^{-(3+n)}c_{\rm SI}.$$

Show this conversion by substitution in your notebook. Implement
`make_eos(rho0, c, n)` returning a callable `rho(P)` for nonnegative pressure,
and `make_rhs(rho)` returning the derivative vector for $(m,P)$. The material
changes the callable; the RK4 step stays the same.

Check $\rho(0)=\rho_0$ and a nonzero pressure: evaluate the
published SI formula at $10^{11}$ Pa and the converted CGS formula at $10^{12}$
dyn cm⁻², then compare the densities in the same units. A zero-pressure test
alone cannot detect a wrong conversion of $c$.

### Starting near the centre

Do not evaluate $m/r^2$ at $r=0$. Start at $r_{\rm start}=10^6$ cm (10 km),
using the leading central series:

$$\rho_c=\rho(P_c),\qquad
m(r_{\rm start})=\frac{4\pi}{3}\rho_c r_{\rm start}^3,$$

$$P(r_{\rm start})=P_c-\frac{2\pi}{3}G\rho_c^2r_{\rm start}^2.$$

These approximate the compressible model near the centre. The starting radius
must be small compared with the planet, and its pressure positive. Use
$h=2\times10^5$ cm; Part 3 checks step and starting-radius sensitivity.
Record the analytic centre $(r,m,P,\rho)=(0,0,P_c,\rho_c)$ for plotting,
then the starting state and accepted states.

### Planet integration contract

Implement `integrate_planet(Pc, material, h=2e5, r_start=1e6,
surface_tol_cm=1.0)`, where `material` is `(rho0, c, n)` in CGS. It uses
`make_eos` and `make_rhs` and returns `(R, M, profile, surface_width_cm)`:

- `R` is the surface radius in cm; `M` is its enclosed mass in g.
- `profile` is a NumPy array with columns `(radius_cm, mass_g,
  pressure_dyn_cm2, density_g_cm3)`, in increasing radius order. Include the
  centre, starting state, accepted steps, and refined surface. Retain the small
  signed surface pressure residual.
- `surface_width_cm` is the final bracket width from `find_surface`, not the
  uncertainty of the physical radius.

Require finite positive `Pc`, `h`, `r_start`, and `surface_tol_cm`, and positive
starting pressure. Set an iteration limit; report failure if no surface is
found, a state is non-finite, or a step cannot advance the radius.

### Adaptive surface finding: solve the last step

March outward with RK4 while pressure is positive. When a trial full step gives
$P\le0$, keep the **last positive state** $(r,\mathbf y)$ unchanged. Define

$$g(\delta)=\left[\operatorname{rk4\_step}(f,r,\mathbf y,\delta)\right]_P,
\qquad 0\le\delta\le h.$$

With $g(0)>0$ and $g(h)\le0$, bisect in
`find_surface(f, r, y, h, surface_tol_cm)`:

1. Set `lo = 0` and `hi = h`.
2. Compute `mid = (lo + hi)/2` and one RK4 step of length `mid` from the same
   last positive state.
3. If its pressure is positive, replace `lo`; otherwise replace `hi`.
4. Repeat until `hi - lo <= surface_tol_cm`, using **1 cm** here. Return
   `(radius, state, bracket_width)` at the bracket midpoint.

Every trial evaluates $g$ from the same last positive state. Raise an error if
the sign bracket is missing or refinement cannot progress.

RK stages may sample negative pressure while bracketing. In the RHS only,
evaluate the EOS with `max(P, 0.0)` to keep fractional powers real. This numerical
extension does not represent physical negative pressure. Keep the evolved
pressure unclipped and omit full overshooting steps from the profile. Record
the final midpoint state, including its signed pressure residual.

This **adaptive event location** adjusts the final step to solve the surface
condition. It is neither adaptive error control nor implicit ODE integration.
The 1 cm bracket locates the numerical zero; it does not establish 1 cm accuracy
for the physical radius.

### Constant-density analytic check

Before using the physical EOS, set $c=0$, $\rho_0=8.3$ g cm⁻³, and
$P_c=1.5\times10^{12}$ dyn cm⁻². Then

$$m(r)=\frac{4\pi}{3}\rho_0r^3,\qquad
P(r)=P_c-\frac{2\pi}{3}G\rho_0^2r^2,$$

$$R_{\rm exact}=\sqrt{\frac{3P_c}{2\pi G\rho_0^2}},\qquad
M_{\rm exact}=\frac{4\pi}{3}\rho_0R_{\rm exact}^3.$$

Derive these expressions from the ODEs. Require radius and mass relative errors
below $10^{-4}$ at the stated settings. Report the bracket width and
$|P_{\rm surface}|/P_c$; require width at most 1 cm and residual below $10^{-8}$.
These measure different errors.

Integrate one **iron** planet at the same $P_c$. Make a three-panel
profile of $P/P_c$, $m/M$, and $\rho$ versus $r/R$. Label the dimensionless
ratios and the density units. Its mass is an output, not a prescribed Earth mass.

**Interpret — Part 2**

1. Report the constant-density radius and mass errors, surface bracket width,
   and normalized pressure residual. What does the SHO test check, and what does
   this planet test add?
2. Explain why a small surface residual alone does not establish an accurate
   radius. Use the iron profiles to describe how pressure, mass, and density
   change outward, and name one physical assumption of the model.

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] `eos.py` and `structure.py`, with CGS conversion, profiles, and final-step surface bisection.
- [ ] Unit-conversion algebra and the constant-density derivation and comparison.
- [ ] One three-panel iron profile figure, surface diagnostics, and the relevant tests.
- [ ] One or two paragraphs answering the Part 2 questions.
:::

## Part 3 — Reproduce the mass–radius relation

For each material, integrate at these **25 central pressures**:

```python
central_pressures = np.logspace(11, 14, 25)  # dyn cm^-2
```

Each integration returns an $(M,R)$ pair. Retain points with
$0.25\le M/M_\oplus\le10$ and plot them in increasing mass order. The three
materials need not sample the same masses. Sweep central pressure rather than
solving for specified masses.

Compare each retained radius with Seager's equation 23 evaluated at **your
computed mass**:

$$M_s=\frac{M/M_\oplus}{m_1},\qquad
\frac{R_{\rm fit}}{R_\oplus}=r_1\,10^{k_1+\frac13\log_{10}M_s-k_2M_s^{k_3}}.$$

Use the Table 4 **modified-polytropic EOS** rows:

| Material | $m_1$ [$M_\oplus$] | $r_1$ [$R_\oplus$] | $k_1$ | $k_2$ | $k_3$ |
|:--|--:|--:|--:|--:|--:|
| Fe (α) | 5.80 | 2.52 | −0.209490 | 0.0804 | 0.394 |
| MgSiO₃ | 10.55 | 3.90 | −0.209594 | 0.0799 | 0.413 |
| H₂O | 5.52 | 4.43 | −0.209396 | 0.0807 | 0.375 |

The paper's common-coefficient form is accurate to about 1% for $M_s<4$.
Here we use material-specific coefficients; all retained points satisfy
$M_s<4$. We reproduce the simplified homogeneous models, not layered planets
or full EOS models. The fit is approximate, not an exact numerical solution.

Make one two-panel mass–radius figure: your curves and the published fits above,
and $100(R-R_{\rm fit})/R_{\rm fit}$ below. Use logarithmic mass axes in both
panels, a logarithmic radius axis above, and a linear percentage axis below.
Mark Earth at $(1,1)$ on the upper
panel as a reference; Earth has a layered composition. Report the largest
absolute fractional disagreement for each material; the target is agreement
within 1%.

### Separate numerical sensitivity from fit disagreement

For each material, take its lowest-mass, middle, and highest-mass retained
points. At the same central pressures, rerun:

- with $h=10^5$ cm and the original $r_{\rm start}$;
- with $r_{\rm start}=5\times10^5$ cm and the original $h$.

Tabulate relative changes in $M$ and $R$ against the baseline. Require each
change below $10^{-4}$, well below the 1% fit target.
For all baseline retained points, check surface width at most 1 cm and
$|P_{\rm surface}|/P_c<10^{-8}$. If a check fails, diagnose it before claiming
agreement. These checks establish neither fourth-order planetary convergence
nor a rigorous total-error bound.

### Compare with known exoplanets

Read the NASA CSV with Pandas, apply the supplied selection, and plot mass and
radius estimates beside your composition curves. No archive client, catalog
merging, or new mass–radius fit is required.

#### Download once, then work locally

Use [Download the NASA CSV](https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name%2Cpl_masse%2Cpl_masseerr1%2Cpl_masseerr2%2Cpl_masselim%2Cpl_rade%2Cpl_radeerr1%2Cpl_radeerr2%2Cpl_radelim%2Cpl_bmassprov%2Cpl_refname%2Cdefault_flag%2Crv_flag%2Cttv_flag%2Ctran_flag+from+ps+where+default_flag%3D1+and+pl_masse+between+0.25+and+10+and+pl_rade%3E0+order+by+pl_masse&format=csv) and save the response as
`data/project4-nasa-exoplanets.csv`. The **Planetary Systems (`ps`) table** query
selects one default parameter set per planet:

```sql
select pl_name,pl_masse,pl_masseerr1,pl_masseerr2,pl_masselim,pl_rade,pl_radeerr1,pl_radeerr2,pl_radelim,pl_bmassprov,pl_refname,default_flag,rv_flag,ttv_flag,tran_flag
from ps
where default_flag=1 and pl_masse between 0.25 and 10 and pl_rade>0
order by pl_masse
```

Record the query and retrieval date in your README. If NASA is unavailable,
use the [provided CSV snapshot](data/project4-nasa-exoplanets.csv) and note that
choice. Its [provenance record](data/project4-nasa-exoplanets.provenance.json)
contains the source URL, query, retrieval timestamp, and checksum. Rerun the
notebook from the saved CSV.

#### Select usable rows

`pl_masse` and `pl_rade` use Earth masses and radii, matching the plot axes.
Their `err1` and `err2` fields give positive upper and negative lower uncertainty
offsets. Central estimates require `pl_masselim = pl_radelim = 0`.
`pl_name` identifies the planet; `pl_refname` records its source publication.

Use or adapt this supplied selection block:

```python
import numpy as np
import pandas as pd

raw = pd.read_csv("data/project4-nasa-exoplanets.csv", comment="#")
columns = ["pl_masse", "pl_masseerr1", "pl_masseerr2",
           "pl_rade", "pl_radeerr1", "pl_radeerr2"]
finite = np.isfinite(raw[columns]).all(axis=1)
keep = (finite & raw["default_flag"].eq(1)
        & raw["pl_masselim"].eq(0) & raw["pl_radelim"].eq(0)
        & raw["pl_bmassprov"].eq("Mass")
        & raw["pl_masse"].between(0.25, 10) & raw["pl_rade"].gt(0)
        & raw["pl_masseerr1"].gt(0) & raw["pl_masseerr2"].lt(0)
        & raw["pl_radeerr1"].gt(0) & raw["pl_radeerr2"].lt(0)
        & (raw["pl_masse"] + raw["pl_masseerr2"]).gt(0)
        & (raw["pl_rade"] + raw["pl_radeerr2"]).gt(0))
planets = raw.loc[keep].copy()
if planets.empty or not planets["pl_name"].is_unique:
    raise ValueError("Need a nonempty table with one selected row per planet")
print(f"Downloaded: {len(raw)}; plotted: {len(planets)}; excluded: {len(raw)-len(planets)}")
```

The mask keeps the models' central-mass window and excludes missing estimates,
limits, unusable error bars, and nonpositive lower endpoints on log axes. Retain
`pl_name` and `pl_refname`; never infer missing mass from radius or vice versa.

Use published `ps` parameter sets: `pscomppars` can fill missing values from an
empirical mass–radius relation, making comparisons with those entries circular. "Best mass"
fields can contain $M\sin i$; we use `pl_masse` with `pl_bmassprov == "Mass"`.
Literature estimates may still depend on model assumptions. See the
[NASA column definitions](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
and [calculated-value documentation](https://exoplanetarchive.ipac.caltech.edu/docs/pscp_calc.html).

#### Add the observations to the existing figure

Add faint catalog points and error bars to the **upper panel**, with clear
composition curves. Label two exoplanets for discussion and keep Earth marked.
Retain the lower panel's Seager comparison; no fourth figure is required.

Matplotlib needs nonnegative lower and upper error magnitudes. For example:

```python
mass_errors = np.vstack((-planets["pl_masseerr2"].to_numpy(),
                          planets["pl_masseerr1"].to_numpy()))
radius_errors = np.vstack((-planets["pl_radeerr2"].to_numpy(),
                            planets["pl_radeerr1"].to_numpy()))
# On the upper panel, after creating its Matplotlib axis:
ax.errorbar(planets["pl_masse"], planets["pl_rade"],
            xerr=mass_errors, yerr=radius_errors,
            fmt=".", color="0.5", alpha=0.3, elinewidth=0.5,
            label="NASA published estimates", zorder=1)
```

These cold, homogeneous, atmosphere-free models may not describe an observed
planet. Account for observational uncertainties; proximity to a curve does not
uniquely identify composition. This selected, heterogeneous sample cannot
establish population frequencies. The 1% target applies to Seager's simplified
models, not observed planets.

**Interpret — Part 3**

1. Report the largest fit disagreement for each material and the largest
   changes from halving $h$ and $r_{\rm start}$. Why are those different kinds of
   evidence? Why does sweeping $P_c$ generate a mass–radius relation?
2. Compare two named exoplanets with the composition curves, using their mass
   and radius uncertainties. What can you constrain, and what remains ambiguous?
   Explain one mismatch or limitation in terms of the physical assumptions.
   Report the downloaded and selected row counts and the source references for
   your two examples.

:::{admonition} TL;DR — Deliverables
:class: tip

- [ ] Three central-pressure model sweeps, Seager fit disagreements, and the refinement table.
- [ ] A saved NASA CSV, its query/retrieval record, and the downloaded/selected row counts.
- [ ] One two-panel mass–radius figure: NASA error bars and two labelled planets above, Seager differences below.
- [ ] The surface/refinement test and one or two interpretation paragraphs.
:::

## Required tests and submission

Cover these four test groups in `tests/`. You may split checks across functions
or use pytest parametrization:

| Test | Required checks |
|:--|:--|
| ODE methods | SHO fitted slopes within 0.1 of 1, 2, 4 on the stated sweep; explicit midpoint gives $1.11025$ for one $h=0.1$ step of $y'=y^2$, $y(0)=1$ (absolute tolerance $10^{-12}$); a constant RHS lands correctly on a non-grid endpoint |
| EOS conversion | all three materials agree between SI and CGS at the stated nonzero pressure (relative tolerance $10^{-12}$), and $\rho(0)=\rho_0$ |
| Constant-density planet | the stated $M,R$ relative errors are below $10^{-4}$ |
| Surface and refinement | bracket widths and pressure residuals meet the stated criteria; the nine retained control points meet both step and central-start sensitivity criteria |

Submit:

- `ode.py`, `eos.py`, `structure.py`, and passing tests covering all four groups;
- `analysis.ipynb` with calculations, unit-conversion algebra, analytic-check
  derivation, the refinement table, and three sets of interpretation answers;
- three saved figures: SHO convergence, iron interior profiles, and the
  two-panel mass–radius comparison with NASA observations;
- the saved NASA CSV, source query and retrieval date, and references for the
  two named examples;
- `README.md` with dependencies and exact commands to run tests and the notebook.

Use readable labels, units, and distinct markers or line styles.
**Restart Kernel and Run All Cells**, then run `python -m pytest`.
Each student submits their own code and explanations, including in pairs.
Assessment uses the [course project dimensions](../../01-course-info/projects.md#how-each-project-is-graded).

## References

- [NASA Exoplanet Archive TAP guide](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html) and [Pandas table reading](../../04-scientific-computing/11-pandas-fundamentals.md): only CSV reading and row selection are used here.

- [Seager et al. (2007), *Mass–Radius Relationships for Solid Exoplanets*](https://militzer.berkeley.edu/papers/34_seager_kuchner_hier-majumder_militzer_2007.pdf): structure equations 1–2; EOS equation 11/Table 3; equation 23/Table 4.
- [Runge–Kutta reading](../../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md): explicit midpoint and classical RK4.
