---
title: "Project 3 — Science Background"
subtitle: "Wien's law, Kepler geometry, and transit contacts"
---

# Project 3 — Science Background

Project 3 uses roots to find a spectral peak, recover orbital positions, and
locate transit contacts. This companion explains the physics and geometry
behind Parts 2–4 of [Project 3](project-3.md). The brief specifies the code,
tests, and submissions; this page adds no deliverables.

## 1. Light and the electromagnetic spectrum

Visible light is the small part of electromagnetic radiation our eyes detect.
Radio, infrared, ultraviolet, X-rays, and gamma rays are the same kind of
radiation at different wavelengths. Wavelength $\lambda$ is the distance
between successive wave crests; frequency $\nu$ counts cycles per second.
In vacuum,

$$c=\lambda\nu,\qquad E_{\rm photon}=h\nu=\frac{hc}{\lambda}.$$

Shorter wavelengths mean higher frequency and more energy **per photon**.
They do not, by themselves, mean a brighter source: brightness also depends
on how much radiation arrives. Here $\nu$ denotes light frequency; in the
orbit sections the same conventional symbol denotes true anomaly. The units
and context distinguish them.

```{figure} figures/project3-em-spectrum.svg
:alt: Electromagnetic spectrum ordered from gamma rays at short wavelength to radio at long wavelength on a logarithmic scale. An expanded visible strip spans approximately 380 to 700 nanometers. Frequency and photon energy increase toward shorter wavelengths.
:width: 850px

Each tick interval on the upper axis spans a factor of 1000 in wavelength.
Visible light occupies only a narrow interval. The lower strip expands it on
a linear scale; its colors are illustrative. Band boundaries are conventional,
and microwaves are part of the broader radio band. See NASA's
[electromagnetic spectrum overview](https://science.nasa.gov/asset/webb/the-electromagnetic-spectrum/)
and [visible-light guide](https://science.nasa.gov/ems/09_visiblelight/).
```

Useful conversions are $1\ \mathrm{nm}=10^{-7}$ cm and
$1\ \mu\mathrm{m}=10^{-4}$ cm. A peak at $0.58\ \mu\mathrm{m}=580$ nm
lies in the visible band; one at $0.97\ \mu\mathrm{m}=970$ nm lies in the
infrared. These examples connect the spectrum map to the Planck curves below.

### A spectrum is a density

Think of a histogram: its bin height can be a count divided by bin width.
Likewise, $B_\lambda\,d\lambda$ measures radiance in a small wavelength
interval. $B_\lambda$ alone is radiance **per unit wavelength**, not the
radiance in the whole spectrum. Changing from equal wavelength bins to equal
frequency bins changes their widths unevenly because $\nu=c/\lambda$.
The density and the location of its maximum can therefore change, while the
radiation in corresponding intervals stays the same.

## 2. Wien's law: find the wavelength peak

A blackbody at temperature $T$ emits over a range of wavelengths. Its spectral
radiance per unit wavelength is the Planck function

$$B_\lambda(T)=\frac{2hc^2}{\lambda^5}
\frac{1}{\exp[hc/(\lambda k_BT)]-1}.$$

Here $h$ is Planck's constant, $c$ is the speed of light, and $k_B$ is Boltzmann's
constant. Use the CGS values in Part 2: $\lambda$ in cm and $T$ in K. Then
$B_\lambda$ has units of energy per time, area, solid angle, and wavelength:
$\mathrm{erg\,s^{-1}\,cm^{-2}\,sr^{-1}\,cm^{-1}}$.

**Wien's displacement law** locates the maximum of this wavelength density:

$$\lambda_{\max}T=b,\qquad b\approx0.2897772\ \mathrm{cm\,K}.$$

Doubling the temperature halves the peak wavelength. The spectrum remains
broad; the peak does not mean that all photons have that wavelength. Treating
a stellar spectrum as a blackbody is an approximation: real spectra include
absorption lines and atmospheric effects.

```{figure} figures/project3-wien-spectra.svg
:alt: Absolute Planck spectral radiance at 3000, 5000, and 8000 K. The vertical axis is logarithmic. Hotter curves are higher at every wavelength and peak at shorter wavelengths.
:width: 850px

The plot shows the **absolute Planck function**, with no individual curve
normalization. Hotter blackbodies emit more at every wavelength and peak at
shorter wavelengths. The logarithmic vertical axis makes the cooler spectrum
visible; values below the displayed range are clipped.
Markers locate the wavelength peaks. Wavelength is labelled in micrometers
($1\ \mu\mathrm{m}=10^{-4}$ cm), while radiance remains **per cm of wavelength**
in the CGS units of the equation above. These are ideal blackbody spectra,
not measured stellar spectra.
```

### Derive the equation to solve

At fixed $T>0$, define the dimensionless variable

$$x=\frac{hc}{\lambda k_BT},\qquad
\frac{dx}{d\lambda}=-\frac{x}{\lambda}.$$

Logarithmic differentiation keeps the algebra short:

$$\frac{1}{B_\lambda}\frac{dB_\lambda}{d\lambda}
=\frac{1}{\lambda}\left[-5+\frac{x e^x}{e^x-1}\right].$$

For finite $\lambda>0$, set this derivative to zero and rearrange:

$$\frac{x e^x}{e^x-1}=5
\quad\Longrightarrow\quad x=5(1-e^{-x}).$$

The positive solution $x_\star$ is independent of temperature, giving

$$b=\frac{hc}{k_Bx_\star}.$$

This connects Parts 1–2: the generic root finder solves
$f(x)=x-5(1-e^{-x})=0$, and the application converts its answer into a physical
constant. At fixed temperature, $B_\lambda$ tends to zero at both wavelength
extremes. Its unique positive stationary point is therefore the maximum.

### Why a zero residual can select the wrong root

The rearranged equation also has the root $x=0$. But the step above assumed
$x>0$: at zero, the denominator $e^x-1$ vanishes. For finite positive $T$,
$x\to0$ corresponds to $\lambda\to\infty$, not a finite-wavelength peak.

The derivative of the root-finding function is

$$f'(x)=1-5e^{-x}.$$

It vanishes at $x=\ln5$. The function decreases up to that minimum and then
increases, crossing zero once more at the desired positive root. This geometry
explains both the unwanted zero root and the risk of a large Newton step near
a small derivative.

```{figure} figures/project3-wien-roots.svg
:alt: Upper panel shows the rearranged Wien function crossing zero at x equals zero and near 4.965. Lower panel shows its derivative crossing zero at ln 5. A vertical dotted line joins that derivative zero to the function's minimum; negative x is shaded.
:width: 850px

A small residual does not select the physical root. Negative $x$ is outside
the finite positive wavelength and temperature domain; $x=0$ is its limiting
boundary. The dotted line marks a zero derivative, not a root of $f$.
```

:::{tip} Predict, then check
If temperature triples, how should the peak wavelength change? Before running
Newton from $x_0=1$, inspect the signs of $f(1)$ and $f'(1)$. Does its first
step move toward the positive peak root or toward zero?
:::

### Wavelength and frequency peaks are different

Project 2 used $B_\nu$, the radiance **per unit frequency**. Conservation of
radiance over corresponding spectral intervals gives

$$B_\lambda\,|d\lambda|=B_\nu\,|d\nu|,
\qquad B_\lambda=\frac{c}{\lambda^2}B_\nu\!\left(\frac{c}{\lambda},T\right).$$

The factor $c/\lambda^2$ varies with wavelength, so converting the location
of the $B_\nu$ maximum using $\lambda=c/\nu$ does not locate the $B_\lambda$
maximum. The underlying radiation is the same; the spectral interval used to
define the density changes. See [Marr and Wilkin (2012)](https://arxiv.org/abs/1109.3822)
for a discussion of this distinction.

Integrating the spectrum in Project 2 measures the total emitted flux;
finding its peak here measures where the wavelength density is largest.
These give Stefan–Boltzmann's law and Wien's law, respectively.

## 3. The model and its coordinates

Treat the star and planet as an isolated Newtonian two-body system. Their
relative orbit is an ellipse with semimajor axis $a$ and eccentricity
$0\le e<1$. The position below is the planet's displacement **relative to the
star**; the star need not be stationary in an inertial frame. For the transit,
use spherical bodies and a distant observer, so their projected outlines are
circles. Project 3 uses a uniform-brightness stellar disk for its light curves.

| Symbol | Meaning |
|:--|:--|
| $P$, $t$ | orbital period and time since periastron, in the same units |
| $a$, $r$ | semimajor axis and instantaneous star–planet distance |
| $e$ | eccentricity; zero gives a circle |
| $M$, $E$, $\nu$ | mean, eccentric, and true anomaly, in radians |
| $i$ | angle between the orbital plane and sky plane; $\pi/2$ is edge-on |
| $\omega$ | argument of periastron, measured in the orbital plane from the ascending node |
| $R_\star$, $R_p$ | stellar and planetary radii |
| $p=R_p/R_\star$ | planet-to-star radius ratio |
| $z$ | sky-projected center separation divided by $R_\star$ |

We fix $\omega=\pi/2$ and put $t=0$ at periastron. In the required edge-on
cases, the planet is then directly in front of the star at $t=0$. For a
circular orbit there is no unique periastron; retain this orientation and time
origin by convention.

The calculation proceeds as

$$
\begin{aligned}
t&\longrightarrow M\xrightarrow{\text{solve Kepler}}E\longrightarrow(r,\nu),\\
(r,\nu)&\longrightarrow z(t)\xrightarrow{\text{solve contacts}}(t_1,t_2,t_3,t_4).
\end{aligned}
$$

## 4. Three angles with different jobs

**Mean anomaly is a clock:**

$$M=nt,\qquad n=\frac{2\pi}{P}.$$

It advances by equal amounts in equal time intervals. For an eccentric orbit,
it is not the planet's physical angle around the star.

**Eccentric anomaly parametrizes the ellipse.** Draw an auxiliary circle of
radius $a$ centered on the ellipse's center $C$. A point $Q$ at angle $E$ on
that circle has coordinates $(a\cos E,a\sin E)$. Compress its vertical
coordinate by $\sqrt{1-e^2}$ to obtain the planet's position on the ellipse.
The star is at the focus $S$, displaced by $ae$ from $C$ toward periastron.
Measured from the star, the orbital-plane coordinates are therefore

$$x_{\rm orb}=a(\cos E-e),\qquad
  y_{\rm orb}=a\sqrt{1-e^2}\sin E.$$

**True anomaly is the physical angle at the focus:**
$\nu=\operatorname{atan2}(y_{\rm orb},x_{\rm orb})$, modulo a full turn.

```{figure} figures/project3-kepler-geometry.svg
:alt: An ellipse inside its auxiliary circle. E is measured at the ellipse center C toward circle point Q. True anomaly is measured at stellar focus S toward the planet below Q; the two points have the same horizontal coordinate.
:width: 760px

The two geometric angles have different origins. The auxiliary circle is a
construction, not another orbit. The illustration uses $e=0.55$.
```

The distance from the focus is

$$
\begin{aligned}
r^2&=x_{\rm orb}^2+y_{\rm orb}^2\\
   &=a^2\left[(\cos E-e)^2+(1-e^2)\sin^2E\right]\\
   &=a^2(1-e\cos E)^2,
\end{aligned}
$$

so $r=a(1-e\cos E)$. At periastron $E=0$, $r=a(1-e)$; at apastron
$E=\pi$, $r=a(1+e)$.

The half-angle expression used in the project is

$$\nu=2\operatorname{atan2}\!\left(
\sqrt{1+e}\sin(E/2),\sqrt{1-e}\cos(E/2)\right).$$

Use a two-argument arctangent to retain quadrant information. Angles differing
by $2\pi$ describe the same position, but the project's Kepler solver must
return $E$ on the same **unwrapped branch** as its input $M$.

:::{tip} Predict, then check
When $e=0$, the focus and center coincide. What should happen to $M$, $E$,
$\nu$, and $r$? Simplify the formulas before checking your program.
:::

## 5. Why time leads to a root-finding problem

Kepler's second law says the line joining star and planet sweeps equal areas
in equal times. Let $b_{\rm ell}=a\sqrt{1-e^2}$ be the ellipse's semiminor
axis. From periastron to eccentric anomaly $E$, the swept area is

$$A(E)=\frac{ab_{\rm ell}}{2}(E-e\sin E).$$

Compress the auxiliary circle's sector area by $b_{\rm ell}/a$, then subtract
the signed triangle area associated with the focus's offset $ae$. The ellipse
has area $\pi ab_{\rm ell}$, so equal-area motion gives

$$\frac{t}{P}=\frac{A(E)}{\pi ab_{\rm ell}}
\quad\Longrightarrow\quad M=E-e\sin E.$$

For multiple revolutions, interpret area as accumulated swept area. For
negative time, use signed area. The same equation remains valid without
wrapping the angles.

Given $E$, calculating $M$ is direct. Given $M$, we instead solve

$$f(E)=E-e\sin E-M=0,\qquad f'(E)=1-e\cos E.$$

For a bound ellipse, $f'(E)\ge1-e>0$, so $f$ increases strictly and has one
real root for each unwrapped $M$ (its limits as $E\to\pm\infty$ have opposite
signs). Uniqueness does **not** guarantee Newton convergence. Near periastron
at large $e$, a small derivative can produce a large update.

The residual also needs interpretation. For an approximate solution
$\widehat E$ and exact solution $E_\ast$, the mean value theorem gives

$$|\widehat E-E_\ast|\le
\frac{|f(\widehat E)|}{1-e}.$$

This is a bound for the exact mathematical residual. Floating-point evaluation
adds round-off error. A small computed residual is useful evidence, but becomes
a weaker guarantee of angular accuracy as $e$ approaches one.

:::{note} A mathematical orbit is not automatically a viable transit system
A planet that stays outside the star requires $a(1-e)>R_\star+R_p$. The
project's high-eccentricity solver tests need not satisfy this physical
condition; they test the equation, not a viable transit system.
:::

## 6. From the orbit to the observer's sky

Place the star at the origin. Let $X,Y$ span the sky plane and let positive
$Z$ point **toward the observer**. Choose the sky's $X$ axis along the ascending
node. With $u=\nu+\omega$, rotating the orbital plane through inclination $i$
gives

$$X=r\cos u,\qquad Y=r\sin u\cos i,\qquad Z=r\sin u\sin i.$$

Only $X,Y$ determine the projected center separation:

$$
\begin{aligned}
z&=\frac{\sqrt{X^2+Y^2}}{R_\star}\\
 &=\frac{r}{R_\star}\sqrt{\cos^2u+\cos^2i\sin^2u}\\
 &=\frac{r}{R_\star}\sqrt{1-\sin^2i\sin^2u}.
\end{aligned}
$$

At the project's fixed $\omega=\pi/2$,

$$
\begin{aligned}
X&=-r\sin\nu,\quad Y=r\cos\nu\cos i,\quad Z=r\cos\nu\sin i,\\
z&=\frac{r}{R_\star}\sqrt{\sin^2\nu+\cos^2i\cos^2\nu}.
\end{aligned}
$$

The final sum of squares avoids subtracting nearly equal numbers near an
edge-on mid-transit. At $i=\pi/2$, it reduces to
$z=(r/R_\star)|\sin\nu|$.

```{figure} figures/project3-sky-projection.svg
:alt: Left: a side view shows the orbital line tilted by inclination i from the sky axis Y toward the observer axis Z. Right: the projected ellipse has a solid front segment and dashed rear segment, with the projected periastron offset from the stellar center.
:width: 850px

Tilting the orbit changes its sky projection. The illustrative $65^\circ$
inclination makes the tilt visible. The stellar radius is $0.12a$ in the sky
view, and the projected track misses the stellar disk. Project 3's required
contact calculations use $90^\circ$.
```

A transit needs both projected overlap and the planet in front: $z<1+p$ and
$Z>0$. Projected overlap with $Z<0$ is a secondary eclipse. Because $z$ is a
distance, it loses this front/back information.

**Recover Project 1.** In a circular, edge-on orbit, $r=a$ and
$\nu=M=2\pi t/P$ modulo a full turn. Thus

$$z(t)=\frac{a}{R_\star}\left|\sin\frac{2\pi t}{P}\right|.$$

This is a check of the whole chain: time convention, Kepler solution, angular
conversion, and projection. Near $z=0$, compare absolute errors because a
relative error divides by a vanishing reference.

### Worked example: one supplied orbital position

Take $e=0.4$, $a/R_\star=8$, $i=60^\circ$, $\omega=90^\circ$, and a
supplied eccentric anomaly $E=30^\circ=\pi/6$ radians. This illustrative
position is separate from the required edge-on benchmarks. No root solve is
needed for this example.

| Step | Calculation | Result |
|:--|:--|:--|
| Orbital position | $x_{\rm orb}/a=\cos E-e$; $y_{\rm orb}/a=\sqrt{1-e^2}\sin E$ | $0.466025$, $0.458258$ |
| Distance | $r/a=1-e\cos E$ | $0.653590$ |
| Physical angle | $\nu=\operatorname{atan2}(y_{\rm orb},x_{\rm orb})$ | $44.52^\circ$ |
| Sky position | $X/a=-y_{\rm orb}/a$; $Y/a=(x_{\rm orb}/a)\cos i$ | $-0.458258$, $0.233013$ |
| Front/back | $Z/a=(x_{\rm orb}/a)\sin i$ | $+0.403590$: toward the observer |
| Projected separation | $z=8\sqrt{(X/a)^2+(Y/a)^2}$ | $4.112770$ |

The planet is on the observer's side, but it is far from the stellar disk in
projection. Being in front is necessary for a transit, not sufficient.
Check the rotation by verifying $X^2+Y^2+Z^2=r^2$ before rounding.

## 7. Contacts are tangencies between two circles

Scale lengths by $R_\star$: the stellar radius is one, the planetary radius is
$p$, and their center separation is $z$. External tangency occurs at the sum
of radii, $1+p$. Internal tangency occurs at their difference, $1-p$, for
$0<p<1$.

```{figure} figures/project3-four-contacts.svg
:alt: Four numbered panels, read across each row, show a planet moving right to left across the stellar center. Orange rings mark tangency points. At contacts one and four the circles touch externally; at contacts two and three the planet is internally tangent to the stellar boundary.
:width: 900px

Four distinct contacts for a central transit, read left to right across each
row. Orange rings mark the tangency points; arrows show planet motion in our
sky coordinates. The illustrative planet has $p=0.18$.
```

| Contact | Geometry | What follows |
|:--|:--|:--|
| $t_1$: $z=1+p$ | first external tangency | ingress: overlap grows |
| $t_2$: $z=1-p$ | first internal tangency | the planet is fully inside the stellar disk |
| $t_3$: $z=1-p$ | second internal tangency | egress: overlap shrinks |
| $t_4$: $z=1+p$ | second external tangency | overlap has ended |

For a nongrazing transit, $t_1<t_2<t_3<t_4$. The two durations are

$$T_{14}=t_4-t_1,\qquad T_{23}=t_3-t_2.$$

The second is the **full-overlap duration**. For a uniformly bright star and
an opaque planet with negligible flux of its own, full overlap blocks a
fraction $p^2$ of the starlight: normalized flux is $1-p^2$. With limb darkening,
the planet crosses regions of different brightness, so this segment need not
be flat.

A grazing transit lacks a full-overlap interval. At the boundary where the
planet just reaches internal tangency, the two inner contacts merge. Project
3 requires four distinct contacts for its supplied configurations; it asks
for a reported failure if that condition is not met elsewhere.

## 8. Turn the geometry into event equations

Define two functions:

$$g_{\rm out}(t)=z(t)-(1+p),\qquad
  g_{\rm in}(t)=z(t)-(1-p).$$

Each crosses zero twice during a nongrazing primary transit. At ingress,
$z$ decreases: the outer crossing comes first, then the inner crossing. At
egress the order reverses. Sorting all four times restores chronological order.

```{figure} figures/project3-contact-roots.svg
:alt: Upper panel shows projected separation dipping below the two contact thresholds, with four numbered crossings and duration arrows. Lower panel shows the two contact residuals crossing zero and two opposite-sign square markers in a shaded interval bracketing the first contact.
:width: 850px

The same event appears as a threshold crossing above and a zero below.
Squares mark opposite-sign evaluations that bracket contact 1. The illustrative
parameters are $e=0.4$, $a/R_\star=8$, $p=0.15$, and $i=\omega=90^\circ$;
they differ from the project's benchmarks. Time is a fraction of the period.
```

Use a grid to **locate brackets**, then refine each crossing with bisection.
Compare signs directly, as in the brief; retain exact sampled zeros once.
A grid can miss two crossings within one interval, so no detected sign change
does not prove there is no transit. Check event selection, refine the grid
when needed, and verify the number and order of contacts.

The brief's window $[-P/4,P/4]$ isolates the primary event for its required
configurations. It is not a general rule for arbitrary eccentricity,
inclination, or periastron orientation. A general event selector also needs
the line-of-sight information.

### Two numerical solves contribute to the answer

Each evaluation of a contact function includes a Kepler solve. An error in
$E$ changes the computed position and therefore the contact residual. Near a
simple crossing, linearization gives the useful sensitivity estimate

$$|\delta t|\approx\frac{|\delta z|}{|dz/dt|}.$$

A shallow crossing is more sensitive to separation error. This estimate
assumes a nonzero slope and sufficiently small errors; it does not apply at
a tangency where contacts merge. Bisection bounds a root only when continuity
and reliable signs preserve a bracket. Inner-solve errors can shift the contact
function or make its signs unreliable near zero.

Finally, both endpoints contribute to duration error:

$$|\delta T_{14}|\le |\delta t_4|+|\delta t_1|.$$

The required circular-duration comparison checks the full calculation.
Optionally, repeat with tighter inner and outer tolerances to see whether the
duration stabilizes. A stopping tolerance alone does not establish accuracy.

### Why eccentricity changes the duration here

At fixed $a$ and $P$, the periastron speed is

$$v_{\rm peri}=\frac{2\pi a}{P}\sqrt{\frac{1+e}{1-e}}.$$

Our edge-on orientation puts mid-transit at periastron, with velocity in the
sky plane. Increasing eccentricity therefore increases the crossing speed
near mid-transit, explaining the shorter durations in the project's cases.
Do not generalize this trend to every orientation: a transit near apastron
samples a slower part of the orbit. The contact calculation uses the changing
position throughout the event, without assuming constant speed.

:::{tip} Explain before implementing
Trace one trial contact time through the calculation. Which equation does the
inner root finder solve? Which equation does the outer root finder solve?
Then explain why a correct Kepler solution at the wrong front/back event can
still produce the wrong transit duration.
:::

## Further reading

Joshua N. Winn, [*Transits and Occultations*, §2](https://arxiv.org/abs/1001.2010),
provides a broader treatment of eclipse geometry. Its radius ratio $k$ is our
$p$, and its true anomaly $f$ is our $\nu$. It chooses the opposite directions
for both sky axes; this changes the signs of $X,Y$ but leaves $z$ unchanged.
The figures on this page were generated for this course from the equations
shown here.


## Model assumptions at a glance

| Calculation | Assumption | What the result means |
|:--|:--|:--|
| Wien peak | ideal blackbody; density per wavelength | peak of $B_\lambda$, not a single emitted color |
| Orbit | isolated Newtonian two-body ellipse | relative star–planet position; no perturbations |
| Transit | distant observer, spherical bodies, uniform stellar brightness | geometric contacts and idealized flux, without limb darkening or noise |
| Temperature zone | equilibrium, full heat redistribution, emissivity one, fixed albedo, no internal heating | temperature bounds, not a climate or habitability prediction |

The eccentricity comparison holds $P$ and $a/R_\star$ fixed to isolate the
change in orbital shape and speed along the orbit. For the same star and
planet masses, fixed $a$ fixes $P$ through Kepler's third law; changing $e$
does not require changing either. Check the non-intersection condition above
before interpreting a mathematical orbit as a physical star–planet system.
