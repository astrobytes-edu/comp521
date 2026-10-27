---
title: "Lecture 13 · Measurements, Probability, and Geometry"
subtitle: "Scientific questions, uncertainty, and data representations"
author: Anna Rosen
---

## Measurements, probability, and geometry

```{slide-options}
{"layout":"title","class":"foundation foundation-title","eyebrow":"COMP 521 · DATA AND INFERENCE","transition":"fade"}
```

How do imperfect measurements constrain a physical quantity?

Anna Rosen · San Diego State University

## Today: from light to inference

```{slide-options}
{"class":"foundation","eyebrow":"THE ROAD THROUGH THE FOUNDATIONS"}
```

1. **Light and models:** What produces a transit and what does a detector measure?
2. **Probability:** How do repeated measurements vary, and how can measurements be related?
3. **Geometry:** How do vectors and matrices organize measurements and transformations?

Use **right** for the main sequence and **down** for additional worked details.

## A transit: from geometry to a light curve

```{slide-options}
{"class":"foundation foundation-transit","eyebrow":"THE SCIENTIFIC QUESTION"}
```

A transit occurs when a planet passes in front of its star, blocking some of its light. The curve shows brightness relative to the star’s usual level.

```{slide-media} assets/transit-light-curve.mp4
:title: An opaque planet crosses a uniformly bright star while the corresponding normalized flux changes.
:kind: video
:poster: assets/transit-poster.png
:muted: true
```

:::{slide-element}
:class: small-note
Uniform star; central transit; no limb darkening.
:::

## What is flux?

```{slide-options}
{"class":"foundation","eyebrow":"LIGHT FROM STAR TO DETECTOR"}
```

::::::::{slide-columns}
:ratio: 1 1.15
:gap: 30
:align: center

::::::{slide-column}
**Flux** is the energy arriving per unit time per unit collecting area, in a specified wavelength band.

$$F=\frac{dE}{dA\,dt}.$$

A detector records counts from the light collected during an exposure.
::::::

::::::{slide-column}
```{slide-figure} assets/flux-to-detector.png
:alt: Light travels from a star to a telescope, which collects it; a detector records counts.
```
::::::
::::::::

## From detector counts to a light curve

```{slide-options}
{"class":"foundation","eyebrow":"MEASURE BRIGHTNESS OVER TIME"}
```

After calibration, compare brightness at each time with the out-of-transit brightness:

$$f(t)=\frac{F(t)}{F_{\rm out}}.$$

This **normalized flux** is dimensionless. Outside transit it is near 1; a transit makes a dip.

The measured counts depend on the telescope, detector, exposure time, and background as well as the incoming light.

## What does the depth tell us?

```{slide-options}
{"class":"foundation","eyebrow":"AN IDEALIZED FORWARD MODEL"}
```

For the fully overlapping planet in this model, the blocked fraction of a uniformly bright stellar disk is

$$\text{depth}=\left(\frac{R_p}{R_\star}\right)^2=(0.1)^2=0.01.$$

The normalized flux falls from 1 to 0.99. Real stars have limb darkening, and real light curves include additional variation and measurement error.

## Why are measurements uncertain?

```{slide-options}
{"class":"foundation","eyebrow":"SIGNAL AND VARIATION"}
```

- **Photon counting:** the number of detected photons fluctuates between exposures.
- **Background and detector noise:** sky light and electronic readout add variation.
- **Instrument and star:** changing sensitivity and stellar variability can add patterns to the light curve.

Some variation is random; other patterns can be correlated in time or reflect real stellar behavior. Their size matters when deciding which transit models fit the data.

## What do we actually measure?

```{slide-options}
{"class":"foundation","eyebrow":"FROM A PHYSICAL EVENT TO DATA"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 32
:align: center

::::::{slide-column}
```{slide-figure} assets/synthetic-transit.png
:alt: Synthetic normalized flux measurements over time, with an illustrative box-shaped transit model.
```
::::::

::::::{slide-column}
Each point is a flux measurement at a time.

A transit produces a dip; a forward model predicts its shape. The scatter and remaining patterns need explanation too.
::::::
::::::::

## Forward model and inference

```{slide-options}
{"class":"foundation","eyebrow":"QUESTION → PREDICTION → COMPARISON","auto-animate":true,"auto-animate-id":"model-flow"}
```

::::::::{slide-columns}
:ratio: 1 1.2
:gap: 30
:align: center

::::::{slide-column}
A forward model predicts measurements from physical parameters.

$$y_i=m(t_i;\boldsymbol\theta)+\epsilon_i.$$

$y_i$ is observed flux; $m$ is the predicted flux; $\epsilon_i$ is their discrepancy.

Inference compares predictions with observations.
::::::

::::::{slide-column}
```{slide-figure} assets/forward-inverse-flow.png
:alt: Physical parameters feed a forward model and predicted light curve; inference compares the prediction with observations to constrain parameters.
```
::::::
::::::::

## Forward modeling: predict the observations

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"PHYSICAL PARAMETERS → LIGHT CURVE","auto-animate":true,"auto-animate-id":"model-flow"}
```

::::::::{slide-columns}
:ratio: 1.2 1
:gap: 30
:align: center

::::::{slide-column}
```{slide-figure} assets/forward-inverse-flow.png
:alt: Physical parameters feed a forward model and predicted light curve; inference compares the prediction with observations to constrain parameters.
```
::::::

::::::{slide-column}
Choose the star, planet, orbit, and observation times. The model predicts a flux at each time.

For the uniform-star transit,

$$\delta=\left(\frac{R_p}{R_\star}\right)^2.$$

The radius ratio determines the full-transit depth.
::::::
::::::::

## Project 1: geometry predicts the dip

```{slide-options}
{"class":"foundation","eyebrow":"THE UNIFORM-STAR MODEL"}
```

::::::::{slide-columns}
:ratio: 1.2 1
:gap: 28
:align: center

::::::{slide-column}
$p=R_p/R_\star$ is the radius ratio; $z=d/R_\star$ is the projected separation in stellar radii.

For a smaller planet in front of a uniform star:

$$f(p,z)=\begin{cases}
1 & z\geq 1+p,\\
1-p^2 & z\leq 1-p,\\
1-\dfrac{\text{overlap area}}{\pi R_\star^2} & \text{partial overlap}.
\end{cases}$$
::::::

::::::{slide-column}
```{slide-figure} assets/transit-geometry.png
:alt: A planet overlaps a stellar disk. The arrow from the center of the star to the center of the planet shows projected separation.
```
::::::
::::::::

## Project 1: position becomes a light curve

```{slide-options}
{"class":"foundation","eyebrow":"CIRCULAR, EDGE-ON ORBIT"}
```

For orbital radius $a$ and period $P$, near a primary transit with mid-transit at $t=0$:

$$z(t)=\frac{a}{R_\star}\left|\sin\!\left(\frac{2\pi t}{P}\right)\right|,\qquad f_{\rm model}(t)=f\bigl(p,z(t)\bigr).$$

Time gives the planet's projected position. The overlapping area gives the predicted brightness.

The projected separation alone does not tell us whether the planet is in front of or behind the star.

## Why does position on the star matter?

```{slide-options}
{"class":"foundation","eyebrow":"PROJECT 2 · LIMB DARKENING"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 30
:align: center

::::::{slide-column}
```{slide-figure} assets/limb-darkened-disk.png
:alt: A stellar disk is brightest at its center and dimmer toward its edge, with a small planet covering part of the disk.
```
::::::

::::::{slide-column}
The center of a star's disk can appear brighter than its edge. A planet of the same size blocks more light where the surface is brighter.

The transit shape therefore depends on **both** the planet's path and the star's brightness pattern.
::::::
::::::::

## Project 2: stars are not uniformly bright

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"LIMB DARKENING"}
```

::::::::{slide-columns}
:ratio: 1 1.1
:gap: 30
:align: center

::::::{slide-column}
In the linear limb-darkening model, $r$ is distance from the disk center in units of $R_\star$:

$$I(r)=I_0\left[1-u\left(1-\sqrt{1-r^2}\right)\right].$$

$I_0$ is the central intensity; $u$ sets the strength of limb darkening. For $u>0$, the edge is dimmer.
::::::

::::::{slide-column}
```{slide-figure} assets/transit-model-comparison.png
:alt: Model light curves for a uniform star and a limb-darkened star. The limb-darkened model is deeper at the center of transit.
:caption: Same orbit and planet; two stellar brightness models.
```
::::::
::::::::

## Project 2: add up the blocked light

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"INTEGRATE ACROSS THE STELLAR DISK"}
```

For each annulus, $c(r,z)$ is the fraction covered by the planet. Add the blocked contribution from all annuli:

$$\Delta F(z)=\frac{\int_0^1 I(r)\,2\pi r\,c(r,z)\,dr}{F_{\rm tot}},\qquad F_{\rm tot}=\pi I_0(1-u/3).$$

The normalized model is $f(z)=1-\Delta F(z)$. When $u=0$, it recovers the uniform-disk model.

## Project 3: an eccentric orbit

```{slide-options}
{"class":"foundation","eyebrow":"TIME → ORBIT → LIGHT CURVE"}
```

For eccentricity $e$ and period $P$, take $t=0$ at periastron. The mean anomaly $M$ advances uniformly; solve Kepler's equation for eccentric anomaly $E$:

$$M=\frac{2\pi t}{P},\qquad M=E-e\sin E.$$

Then compute the orbital position and projected separation $z(t)$, check that the planet is in front, and evaluate the transit model.

Changing the orbit changes **when and how** the planet crosses the star. Changing the stellar brightness model changes how much light it blocks.

## Inverse modeling: learn from measurements

```{slide-options}
{"class":"foundation","eyebrow":"LIGHT CURVE → PARAMETER ESTIMATES","auto-animate":true,"auto-animate-id":"model-flow"}
```

::::::::{slide-columns}
:ratio: 1 1.2
:gap: 30
:align: center

::::::{slide-column}
Which parameter values reproduce the observed light curve?

Try parameters, calculate predictions, and compare them with the data.

Different combinations can produce similar curves. Uncertainty determines how precisely the data distinguish them.
::::::

::::::{slide-column}
```{slide-figure} assets/forward-inverse-flow.png
:alt: Physical parameters feed a forward model and predicted light curve; inference compares the prediction with observations to constrain parameters.
```
::::::
::::::::

## From a forward model to Project 5

```{slide-options}
{"class":"foundation","eyebrow":"PREDICTION MEETS KEPLER DATA"}
```

The projects built a path from physical parameters to predicted brightness:

$$\text{orbit}\;\longrightarrow\; z(t)\;\longrightarrow\; f_{\rm model}(t;\boldsymbol\theta).$$

With observations, compare the prediction at each observation time to the measured flux:

$$r_i=y_i-f_{\rm model}(t_i;\boldsymbol\theta).$$

The residuals tell us where the model and the light curve disagree. Project 5 brings this modeling idea to Kepler photometry.

## A simple model for depth

```{slide-options}
{"class":"foundation","eyebrow":"A FIRST INVERSE PROBLEM"}
```

Before fitting a full transit curve, use a fixed-shape model to see how fitting works. Take a baseline of 1 and a fixed transit template:

$$m_i(\delta)=1-\delta T_i,\qquad \mathbf T=(0,1,1,0).$$

$T_i=0$ outside transit; $T_i=1$ inside. The unknown parameter $\delta$ is the depth.

For $\delta=0.01$, the model predicts $(1.00,0.99,0.99,1.00)$. Press **down** for the worked fit.

## Compare candidate light curves

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"FOUR OBSERVATIONS","auto-animate":true,"auto-animate-id":"transit-fit"}
```

::::::::{slide-columns}
:ratio: 1.2 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/candidate-transit-depths.png
:alt: Four flux measurements compared with three box-shaped model curves of different transit depths.
```
::::::

::::::{slide-column}
The data are $(1.00,0.98,0.99,1.00)$.

Each curve uses the same baseline and timing. Only the depth changes.

Which depth best matches the two in-transit measurements?
::::::
::::::::

## Residuals make the comparison quantitative

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"DATA MINUS MODEL","auto-animate":true,"auto-animate-id":"transit-fit"}
```

::::::::{slide-columns}
:ratio: 1 1.15
:gap: 28
:align: center

::::::{slide-column}
For each observation, subtract the model:

$$r_i(\delta)=y_i-m_i(\delta)=y_i-1+\delta T_i.$$

With equal weights, compare candidate depths:

$$S(\delta)=\sum_i r_i(\delta)^2.$$

A fit minimizes this sum.
::::::

::::::{slide-column}
```{slide-figure} assets/candidate-transit-depths.png
:alt: Four flux measurements compared with three box-shaped model curves of different transit depths.
```
::::::
::::::::

## Derive the best-fitting depth

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"MINIMIZE THE RESIDUALS"}
```

$$S(\delta)=\sum_i(y_i-1+\delta T_i)^2.$$

::::{fragment}
:effect: fade-in

$$\frac{dS}{d\delta}=2\sum_iT_i(y_i-1+\delta T_i)=0.$$
::::

::::{fragment}
:effect: fade-in

$$\hat\delta=\frac{\sum_iT_i(1-y_i)}{\sum_iT_i^2}=\frac{0.02+0.01}{2}=0.015.$$
::::

## Inspect the fit and residuals

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"A DEPTH OF 1.5%"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/transit-fit-residuals.png
:alt: Four flux measurements and a fitted transit model, with a lower panel showing residuals of negative and positive 0.005 inside transit.
```
::::::

::::::{slide-column}
The in-transit prediction is $0.985$.

Residuals: $-0.005$ and $+0.005$.

The fitted depth summarizes the dip. The residuals show what remains around the model.
::::::
::::::::

## What did we infer?

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"FROM A FIT TO A PHYSICAL QUANTITY"}
```

For a uniform star and a fully overlapping planet:

$$\hat\delta=0.015\quad\Rightarrow\quad \frac{R_p}{R_\star}=\sqrt{0.015}\approx0.122.$$

The light curve constrains a **radius ratio** through the forward model. To find $R_p$ itself, we also need $R_\star$.

Here we held the transit timing, shape, and baseline fixed. Estimating them changes the inverse problem.

## Probability describes variation

```{slide-options}
{"layout":"section","class":"foundation foundation-section","eyebrow":"PART I"}
```

If we repeated a measurement under the same conditions, how would its outcomes vary?

A probability distribution describes that variation.

## From a measurement to a distribution

```{slide-options}
{"class":"foundation","eyebrow":"RANDOM VARIABLES"}
```

::::::::{slide-columns}
:ratio: 1 1.1
:gap: 28
:align: center

::::::{slide-column}
A random variable $Y$ represents possible measurement outcomes.

For a continuous quantity:

$$P(a<Y<b)=\int_a^b p(y)\,dy.$$

Probability is **area over an interval**.
::::::

::::::{slide-column}
```{slide-figure} assets/density-interval.png
:alt: A probability-density curve with the region between a and b shaded to show the probability of that interval.
```
::::::
::::::::

The density at a single value is not the probability of that exact value.

## What is an expectation value?

```{slide-options}
{"class":"foundation","eyebrow":"AVERAGE OVER POSSIBLE OUTCOMES"}
```

The **expectation** of a random quantity is its probability-weighted average over possible outcomes.

For discrete outcomes $y_k$ with probabilities $P(Y=y_k)$:

$$E[Y]=\sum_k y_k\,P(Y=y_k).$$

It is a property of the probability model. With many independent repetitions from the same distribution, the sample average approaches it when the mean is finite.

## Expectation: a worked example

```{slide-options}
{"class":"foundation","eyebrow":"WEIGHT EACH OUTCOME BY ITS PROBABILITY"}
```

Suppose a repeat measurement of normalized brightness $Y$ is $0.98$ with probability $1/4$ and $1.00$ with probability $3/4$:

$$E[Y]=0.98\left(\frac14\right)+1.00\left(\frac34\right)=0.995.$$

Across repeated measurements, the average approaches $0.995$. In this example, neither individual outcome equals the expectation.

## Expectation of a function

```{slide-options}
{"class":"foundation","eyebrow":"THE SAME IDEA FOR ANY QUANTITY"}
```

To average a function $g(Y)$, weight each value of the function by the same outcome probabilities:

$$E[g(Y)]=\sum_k g(y_k)P(Y=y_k).$$

For a continuous variable with density $p(y)$, replace the sum with an integral:

$$E[g(Y)]=\int_{-\infty}^{\infty}g(y)p(y)\,dy.$$

The expectation exists when the relevant weighted sum or integral is finite.

## Center and spread

```{slide-options}
{"class":"foundation","eyebrow":"SUMMARIZE A DISTRIBUTION"}
```

$$\mu=E[Y],\qquad \operatorname{Var}(Y)=E[(Y-\mu)^2],\qquad \sigma=\sqrt{\operatorname{Var}(Y)}.$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
:::{slide-element}
:class: soft-card
**Mean** $\mu$: center of the distribution.
:::
::::::

::::::{slide-column}
:::{slide-element}
:class: warm-card
**Standard deviation** $\sigma$: scale of the spread, in the same units as $Y$.
:::
::::::
::::::::

## From a density to a mean

```{slide-options}
{"class":"foundation","eyebrow":"EXPECTATION FOR A CONTINUOUS VARIABLE"}
```

$$\mu=E[Y]=\int_{-\infty}^{\infty}y\,p(y)\,dy.$$

Each possible value contributes according to its probability density. The density integrates to one; the mean is a property of the distribution.

The same expectation rule applies to other functions, including squared deviations from the mean.

## From a density to a variance

```{slide-options}
{"class":"foundation","eyebrow":"SPREAD ABOUT THE MEAN"}
```

$$\operatorname{Var}(Y)=\int_{-\infty}^{\infty}(y-\mu)^2p(y)\,dy,\qquad \sigma=\sqrt{\operatorname{Var}(Y)}.$$

The variance is the density-weighted mean **squared deviation**. The standard deviation is in the original units.

## Worked example: a uniform distribution

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"CALCULATING MEAN AND SPREAD"}
```

Let $p(y)=1/2$ for $0\leq y\leq2$, and zero elsewhere. Then

$$\mu=\int_0^2 y\frac12\,dy=1.$$

$$\operatorname{Var}(Y)=\int_0^2(y-1)^2\frac12\,dy=\frac13,\qquad \sigma=\frac1{\sqrt3}.$$

## One dataset, one estimated mean

```{slide-options}
{"class":"foundation","eyebrow":"DISTRIBUTION AND DATA"}
```

Given measurements $y_1,\ldots,y_n$, their sample mean is

$$\bar y=\frac{1}{n}\sum_{i=1}^{n}y_i.$$

$\bar y$ is computed from the observed sample. $\mu$ is the mean of the underlying distribution we are trying to learn about.

For a changing star or changing transit signal, separate measurements may have different expected values. A common mean is a model assumption.

## Sample variance describes observed spread

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"DISTRIBUTION AND DATA"}
```

For $n>1$ observed measurements with sample mean $\bar y$:

$$s^2=\frac{1}{n-1}\sum_{i=1}^n(y_i-\bar y)^2.$$

The sample mean is estimated from the same data. The $n-1$ correction makes $s^2$ unbiased for independent, identically distributed measurements with finite variance.

## Spread of data vs. spread of an estimate

```{slide-options}
{"class":"foundation","eyebrow":"WHY REPEATED MEASUREMENTS HELP"}
```

If independent measurements have a common mean and variance $\sigma^2$:

$$\operatorname{Var}(\bar Y)=\frac{\sigma^2}{n},\qquad
\operatorname{SD}(\bar Y)=\frac{\sigma}{\sqrt n}.$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
$\sigma$: spread of individual outcomes.
::::::

::::::{slide-column}
$\sigma/\sqrt n$: standard error of the mean across repeated samples.
::::::
::::::::

A shared calibration bias need not average away.

## Independence is a model assumption

```{slide-options}
{"class":"foundation","eyebrow":"DEPENDENCE"}
```

::::::::{slide-columns}
:ratio: 1 1.15
:gap: 30
:align: center

::::::{slide-column}
Events $A$ and $B$ are independent if $P(A,B)=P(A)P(B)$.

A shared instrumental drift can make nearby errors dependent.
::::::

::::::{slide-column}
```{slide-figure} assets/shared-drift.png
:alt: Two measurement deviations that rise and fall together because they share an instrumental drift.
```
::::::
::::::::

For random variables, independence means the joint distribution factors into the individual distributions.

## Covariance: how deviations combine

```{slide-options}
{"class":"foundation","eyebrow":"DEPENDENCE AND LINEAR ASSOCIATION","auto-animate":true,"auto-animate-id":"correlation-pairs"}
```

::::::::{slide-columns}
:ratio: 1.05 1
:gap: 30
:align: center

::::::{slide-column}
$$\operatorname{Cov}(X,Y)=E[(X-E[X])(Y-E[Y])].$$

Positive covariance: the average product of deviations is positive.

Negative covariance: the average product is negative.
::::::

::::::{slide-column}
```{slide-figure} assets/correlation-pairs.png
:alt: Four paired deviations showing an upward pattern.
```
::::::
::::::::

Covariance carries the product of the variables' units.

## Correlation puts covariance on a common scale

```{slide-options}
{"class":"foundation","eyebrow":"NORMALIZE BY THE SPREADS","auto-animate":true,"auto-animate-id":"correlation-pairs"}
```

::::::::{slide-columns}
:ratio: 1 1.05
:gap: 30
:align: center

::::::{slide-column}
```{slide-figure} assets/correlation-pairs.png
:alt: Four paired deviations showing an upward pattern.
```
::::::

::::::{slide-column}
$$\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}.$$

Correlation has no units and ranges from $-1$ to $1$ when both standard deviations are nonzero.

The sign and magnitude describe the direction and strength of the linear association.
::::::
::::::::

## What do correlation values mean?

```{slide-options}
{"class":"foundation","eyebrow":"DIRECTION AND STRENGTH"}
```

::::::::{slide-columns}
:ratio: 1 1 1
:gap: 24

::::::{slide-column}
**Near $+1$**

Strong positive linear association.
::::::

::::::{slide-column}
**Near $0$**

Little linear association.
::::::

::::::{slide-column}
**Near $-1$**

Strong negative linear association.
::::::
::::::::

Correlation measures association, not causation. A nonlinear dependence can have zero correlation.

## Calculate correlation from paired data

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"SAMPLE COVARIANCE AND CORRELATION"}
```

$$s_{XY}=\frac{1}{n-1}\sum_i(x_i-\bar x)(y_i-\bar y),\qquad
r_{XY}=\frac{s_{XY}}{s_Xs_Y}.$$

Each product uses the $X$ and $Y$ deviations from the **same observation**.

Divide by the two sample standard deviations to remove units and compare linear associations on the same scale.

## Four pairs: work out the correlation

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"FROM PAIRED DEVIATIONS TO A NUMBER"}
```

::::::::{slide-columns}
:ratio: 1 1.1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/correlation-pairs.png
:alt: Four labeled paired observations, increasing from lower left to upper right, shown relative to the two means.
```
::::::

::::::{slide-column}
$\bar x=\bar y=0$.

::::{fragment}
:effect: fade-in
:index: 0

$\sum x_iy_i=4$, $\sum x_i^2=5$, $\sum y_i^2=4$.
::::

::::{fragment}
:effect: fade-in
:index: 1

$$r=\frac{4}{\sqrt{5\cdot4}}\approx0.894.$$

The positive value matches the upward pattern.
::::
::::::
::::::::

## From covariance to correlation: a second example

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"KEEP THE SCALE AND THE ASSOCIATION DISTINCT"}
```

If $\sigma_X=2$, $\sigma_Y=3$, and $\operatorname{Cov}(X,Y)=3$, then

$$\rho_{XY}=\frac{3}{2\cdot3}=0.5.$$

Covariance carries the product of the variables' units. Correlation divides out their spreads and has no units.

## Three patterns

```{slide-options}
{"class":"foundation","eyebrow":"COVARIANCE IS NOT ALL DEPENDENCE"}
```

```{slide-figure} assets/covariance-patterns.png
:alt: Three synthetic point patterns: increasing, decreasing, and a symmetric curved relation with zero covariance.
:caption: Centered example points. The curved relation has zero covariance.
```

Press down for the worked counterexample.

## Uncorrelated can still be dependent

```{slide-options}
{"class":"foundation","eyebrow":"OPTIONAL DETAIL · A COMPLETE COUNTEREXAMPLE","vertical":true}
```

Let $X$ be $-1$, $0$, or $1$, each with probability $1/3$. Let $Z=X^2$.

$$E[X]=0,\quad E[XZ]=E[X^3]=0,\quad \operatorname{Cov}(X,Z)=0.$$

Yet knowing $X=0$ tells us $Z=0$ with certainty, while $P(Z=0)=1/3$ without that information.

Independence implies zero covariance when the relevant moments exist; the converse fails.

## Why do cross terms appear?

```{slide-options}
{"class":"foundation","eyebrow":"UNCERTAINTY IN A SUM"}
```

Let $Z=X+Y$, and write $\Delta X=X-\mu_X$ and $\Delta Y=Y-\mu_Y$.

Then $Z-E[Z]=\Delta X+\Delta Y$. Its variance starts with the square

$$\operatorname{Var}(Z)=E[(\Delta X+\Delta Y)^2].$$

The two deviations appear together because the result depends on both quantities.

## Expand the square

```{slide-options}
{"class":"foundation","eyebrow":"THE MIXING TERM"}
```

$$\operatorname{Var}(X+Y)=E[(\color{#087e81}{\Delta X}+\color{#486d9f}{\Delta Y})^2].$$

::::{fragment}
:effect: fade-in
:index: 0

$$(\Delta X+\Delta Y)^2=\color{#087e81}{\Delta X^2}+\color{#486d9f}{\Delta Y^2}+\color{#9b6617}{2\Delta X\Delta Y}.$$
::::

::::{fragment}
:effect: fade-in
:index: 1

$$\operatorname{Var}(X+Y)=\color{#087e81}{\operatorname{Var}(X)}+\color{#486d9f}{\operatorname{Var}(Y)}+\color{#9b6617}{2\operatorname{Cov}(X,Y)}.$$

The cross term is the average product of the deviations.
::::

## Sums and differences

```{slide-options}
{"class":"foundation","eyebrow":"THE CROSS TERM CHANGES SIGN"}
```

$$\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y),$$

$$\operatorname{Var}(X-Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)-2\operatorname{Cov}(X,Y).$$

Positive shared variation reinforces the sum and partly cancels in the difference.

## Work the cross terms out

```{slide-options}
{"class":"foundation","eyebrow":"TWO CORRELATED QUANTITIES"}
```

With $\sigma_X=2$, $\sigma_Y=3$, and $\rho=0.5$:

$$\operatorname{Cov}(X,Y)=\rho\sigma_X\sigma_Y=0.5(2)(3)=3.$$

::::{fragment}
:effect: fade-in
:index: 0

$$\operatorname{Var}(X+Y)=4+9+2(3)=19.$$
::::

::::{fragment}
:effect: fade-in
:index: 1

$$\operatorname{Var}(X-Y)=4+9-2(3)=7.$$
::::

At zero covariance, both variances would be $4+9=13$.

## Shared variation changes the spread

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"SUM VS. DIFFERENCE"}
```

```{slide-figure} assets/sum-difference-uncertainty.png
:alt: Horizontal standard-deviation bars comparing the sum and difference of two variables at correlation 0.5 and correlation zero.
:caption: Bars show one standard deviation of each combination.
```

## Derive the uncertainty of an average

```{slide-options}
{"class":"foundation","eyebrow":"APPLY THE SUM FORMULA"}
```

$$\operatorname{Var}\!\left(\frac{Y_1+Y_2}{2}\right)
=\frac{\operatorname{Var}(Y_1)+\operatorname{Var}(Y_2)+2\operatorname{Cov}(Y_1,Y_2)}{4}.$$

The factor $1/4$ comes from squaring the coefficient $1/2$.

The covariance term tells us how the two measurements move together.

## Dependence changes the mean's uncertainty

```{slide-options}
{"class":"foundation","eyebrow":"TWO EQUALLY PRECISE MEASUREMENTS"}
```

For common variance $\sigma^2$ and correlation $\rho$:

$$\operatorname{Var}\!\left(\frac{Y_1+Y_2}{2}\right)=\frac{\sigma^2}{2}(1+\rho).$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
$\rho=0$: variance is $\sigma^2/2$.
::::::

::::::{slide-column}
$\rho>0$: shared variation reduces the gain in precision.
::::::
::::::::

A shared bias shifts the mean; correlation describes shared variation.

## Why Gaussian distributions?

```{slide-options}
{"class":"foundation","eyebrow":"A PROBABILITY MODEL"}
```

$$p(y)=\frac{1}{\sqrt{2\pi}\sigma}\exp\left[-\frac{(y-\mu)^2}{2\sigma^2}\right].$$

The center is $\mu$; $\sigma$ sets the spread.

Many small contributions can produce an approximately Gaussian error under suitable conditions.

## One outcome is not Gaussian

```{slide-options}
{"class":"foundation","eyebrow":"BUILDING TOWARD THE CLT"}
```

Imagine an outcome that is **1** with probability $1/2$ and **0** with probability $1/2$.

One outcome has only two possible values. Its mean is $1/2$, and its variance is $(1/2)(1/2)=1/4$.

Take 100 independent outcomes. Their sample mean is the fraction of 1s.

## What happens as the sample grows?

```{slide-options}
{"class":"foundation","eyebrow":"DISTRIBUTIONS OF SAMPLE MEANS"}
```

```{slide-figure} assets/clt-three-samples.png
:alt: Exact probability distributions of sample means for one, four, and one hundred independent binary outcomes.
:caption: Exact probabilities; each panel has its own vertical scale.
```

Each experiment supplies one mean. Larger samples concentrate those means around $0.5$.

## Repeat the entire experiment

```{slide-options}
{"class":"foundation","eyebrow":"THE DISTRIBUTION OF A SAMPLE MEAN"}
```

::::::::{slide-columns}
:ratio: 1 1.25
:gap: 28
:align: center

::::::{slide-column}
Each experiment produces **one** fraction.

Across repeated experiments, those fractions have mean $0.5$ and standard deviation

$$\sqrt{\frac{1/4}{100}}=0.05.$$
::::::

::::::{slide-column}
```{slide-figure} assets/clt-sample-means.png
:alt: Exact binomial probabilities for the fraction of ones in 100 outcomes compared with a Gaussian approximation.
:caption: Exact binomial probabilities; curve is Gaussian density multiplied by bin width.
```
::::::
::::::::

## The central limit theorem

```{slide-options}
{"class":"foundation","eyebrow":"WHAT APPROACHES A GAUSSIAN?"}
```

For independent, identically distributed variables with finite mean $\mu$ and finite nonzero variance $\sigma^2$:

$$\frac{\bar Y-\mu}{\sigma/\sqrt n}\xrightarrow{\ d\ }\mathcal N(0,1)\quad\text{as }n\to\infty.$$

The distribution of the **standardized mean** approaches a Gaussian. Individual outcomes do not become Gaussian.

## From the CLT to measurement errors

```{slide-options}
{"class":"foundation","eyebrow":"WHY A GAUSSIAN CAN BE USEFUL"}
```

A recorded measurement can combine many small contributions to its error. When those contributions satisfy appropriate independence and balance conditions, their sum can be approximately Gaussian.

The resulting distribution describes **possible errors in a measurement**. A shared instrumental drift or a few dominant effects can change that distribution.

## When is the Gaussian approximation useful?

```{slide-options}
{"class":"foundation","eyebrow":"CONNECT THE MODEL TO THE MEASUREMENTS"}
```

- Strong dependence changes how observations combine.
- Heavy tails or a few dominant effects can make the approximation poor.
- A systematic bias can remain even when random errors average down.
- Selection changes which measurements we see.

The accuracy of the approximation depends on the measurement process and sample size.

## Two brightness measurements

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"WHY SHOULD UNCERTAINTY AFFECT A FIT?"}
```

::::::::{slide-columns}
:ratio: 1.15 1
:gap: 24
:align: center

::::::{slide-column}
```{slide-figure} assets/weighted-measurements.png
:alt: Two normalized brightness measurements with one-standard-deviation error bars and vertical lines for the weighted and unweighted means.
```
::::::

::::::{slide-column}
$0.980\pm0.010$ and $1.000\pm0.020$.

Assume independent, unbiased Gaussian errors, known $\sigma_i$, and one constant brightness.

The ordinary mean is $0.990$. Press **down** for the likelihood and weighted fit.
::::::
::::::::

## A likelihood for two measurements

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"A MODEL FOR MEASUREMENT VARIATION","auto-animate":true,"auto-animate-id":"likelihood"}
```

::::::::{slide-columns}
:ratio: 1 1.15
:gap: 26
:align: center

::::::{slide-column}
With independent Gaussian errors and known $\sigma_i$:

$$L(\mu)=\prod_i\frac{1}{\sqrt{2\pi}\sigma_i}
\exp\!\left[-\frac{(y_i-\mu)^2}{2\sigma_i^2}\right].$$

Each measurement contributes one factor.
::::::

::::::{slide-column}
```{slide-figure} assets/likelihood-comparison.png
:alt: Relative likelihood curves for the two measurements and their joint likelihood, peaking at brightness 0.984.
:caption: Each curve is scaled to its own maximum.
```
::::::
::::::::

## From likelihood to a fitting objective

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"TAKE THE LOGARITHM","auto-animate":true,"auto-animate-id":"likelihood"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/likelihood-comparison.png
:alt: Relative likelihood curves for the two measurements and their joint likelihood, peaking at brightness 0.984.
:caption: Each curve is scaled to its own maximum.
```
::::::

::::::{slide-column}
$$\log L(\mu)=\text{constant}-\frac12\sum_i\frac{(y_i-\mu)^2}{\sigma_i^2}.$$

The constant does not depend on $\mu$ because the uncertainties $\sigma_i$ are fixed.

Maximizing likelihood minimizes the weighted squared residuals.
::::::
::::::::

## Derive the weighted mean

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"FROM A NOISE MODEL TO AN OBJECTIVE"}
```

With independent Gaussian errors, maximizing the likelihood is equivalent to minimizing

$$Q(\mu)=\sum_i\frac{(y_i-\mu)^2}{\sigma_i^2}.$$

::::{fragment}
:effect: fade-in

Differentiating and setting $dQ/d\mu=0$ gives

$$\hat\mu=\frac{\sum_i y_i/\sigma_i^2}{\sum_i1/\sigma_i^2}.$$
::::

Each residual is divided by its uncertainty; the objective sums the squared ratios.

## The weighted result

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"INVERSE-VARIANCE WEIGHTING"}
```

The first measurement has one-quarter the variance and four times the weight:

$$\hat\mu=\frac{4(0.980)+1.000}{5}=0.984.$$

$$\operatorname{SD}(\hat\mu)=\frac{1}{\sqrt{\sum_i1/\sigma_i^2}}\approx0.0089.$$

## Data live in representations

```{slide-options}
{"layout":"section","class":"foundation foundation-section","eyebrow":"PART II"}
```

Vectors and matrices organize the quantities we measure and the operations we perform on them.

## Why vectors?

```{slide-options}
{"class":"foundation","eyebrow":"ONE STAR, MANY TIMES"}
```

A light curve contains measurements at ordered times:

$$\mathbf y=\begin{bmatrix}y_1\\y_2\\\vdots\\y_n\end{bmatrix},\qquad
\mathbf r=\mathbf y-\mathbf m(\boldsymbol\theta).$$

A prediction and a residual have one entry for each observation.

The order, units, and correspondence between time and flux matter.

## Rows are objects; columns are features

```{slide-options}
{"class":"foundation","eyebrow":"A DIFFERENT DATASET"}
```

Two illustrative stars, each measured in two normalized flux bands:

$$X=\begin{bmatrix}0.9&1.1\\1.0&0.8\end{bmatrix}.$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
**Rows:** stars. First star's feature vector: $(0.9,1.1)$.
::::::

::::::{slide-column}
**Columns:** band A and band B. Each is a feature.
::::::
::::::::

Here there are two feature dimensions, not two spatial dimensions.

## Matrix multiplication, one row at a time

```{slide-options}
{"class":"foundation","eyebrow":"HOW A MATRIX COMBINES FEATURES"}
```

::::::::{slide-columns}
:ratio: 1.15 1
:gap: 28
:align: center

::::::{slide-column}
$$\begin{bmatrix}a&b\\c&d\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=\begin{bmatrix}ax_1+bx_2\\cx_1+dx_2\end{bmatrix}.$$

Each row supplies the weights for one output.
::::::

::::::{slide-column}
```{slide-figure} assets/matrix-combines-inputs.png
:alt: Two inputs each contribute to two outputs; each output combines the inputs using one row of a matrix.
```
::::::
::::::::

## What is a matrix transformation?

```{slide-options}
{"class":"foundation","eyebrow":"A RULE THAT MAPS VECTORS TO VECTORS"}
```

$$\mathbf z=A\mathbf x.$$

The columns of $A$ tell us where the input basis directions go. Matrix multiplication combines those directions to produce the output.

Linear transformations preserve addition and scaling:

$$A(a\mathbf x+b\mathbf y)=aA\mathbf x+bA\mathbf y.$$

A matrix can scale, rotate, combine, or project coordinates. The physical model itself need not be linear.

## Put the terms in a covariance matrix

```{slide-options}
{"class":"foundation","eyebrow":"VARIANCES AND COVARIANCES"}
```

For the same pair, $\operatorname{Var}(X)=4$, $\operatorname{Var}(Y)=9$, and $\operatorname{Cov}(X,Y)=3$:

$$\Sigma=\begin{bmatrix}\operatorname{Var}(X)&\operatorname{Cov}(X,Y)\\
\operatorname{Cov}(X,Y)&\operatorname{Var}(Y)\end{bmatrix}
=\begin{bmatrix}4&3\\3&9\end{bmatrix}.$$

The diagonal entries are variances; off-diagonal entries are the mixing terms.

## A matrix computes every mixing term

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"UNCERTAINTY OF A LINEAR COMBINATION"}
```

For $Z=aX+bY$ and $\mathbf a=(a,b)^T$:

$$\operatorname{Var}(Z)=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)+2ab\operatorname{Cov}(X,Y).$$

The same expression is compactly written

$$\operatorname{Var}(Z)=\mathbf a^T\Sigma\mathbf a.$$

Multiplying $\mathbf a^T\Sigma\mathbf a$ produces both variance terms and the covariance cross term.

## How does a transformation change covariance?

```{slide-options}
{"class":"foundation","eyebrow":"TRANSFORMING A RANDOM VECTOR"}
```

If $\mathbf z=A\mathbf x$ and $\mathbf x$ has covariance $\Sigma$, the covariance of $\mathbf z$ is

$$\Sigma_{\mathbf z}=A\Sigma A^T.$$

Each output is a combination of inputs. The multiplication carries their variances **and** covariances into the output.

## Sum and difference as a transformation

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"THE CROSS TERMS REAPPEAR"}
```

Choose $\mathbf z=(X+Y,X-Y)^T$. Then

$$A=\begin{bmatrix}1&1\\1&-1\end{bmatrix},\qquad
\Sigma=\begin{bmatrix}4&3\\3&9\end{bmatrix}.$$

$$A\Sigma A^T=\begin{bmatrix}19&-5\\-5&7\end{bmatrix}.$$

The output variances, 19 and 7, agree with the earlier sum-and-difference calculation.

## A transformation we can compute

```{slide-options}
{"class":"foundation","eyebrow":"AVERAGE TWO BANDS"}
```

$$\mathbf x=\begin{bmatrix}0.9\\1.1\end{bmatrix},\qquad
A=\frac12\begin{bmatrix}1&1\\1&1\end{bmatrix}.$$

$$A\mathbf x=\begin{bmatrix}1.0\\1.0\end{bmatrix}.$$

Both output coordinates equal the average. The result lies on the equal-band line.

## Directions preserved by a matrix

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"EIGENVECTORS AND EIGENVALUES"}
```

A transformation usually changes a vector's direction as well as its length. An **eigenvector** stays on the same line: the matrix can stretch, shrink, or reverse it.

$$A\mathbf v=\lambda\mathbf v.$$

The eigenvalue $\lambda$ gives the scale factor. For a covariance matrix, eigenvectors give the principal directions and eigenvalues give the variances along them.

## The geometry of covariance

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"AN UNCERTAINTY ELLIPSE"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/covariance-ellipse.png
:alt: An upward-tilted ellipse representing a two-dimensional covariance matrix with positive covariance.
:caption: A contour of the covariance matrix, centered on the mean.
```
::::::

::::::{slide-column}
For deviations $\Delta\mathbf x$ from the mean, the ellipse shows $\Delta\mathbf x^T\Sigma^{-1}\Delta\mathbf x=1$.

Its tilt shows the positive covariance: deviations along the longer direction change together.

The principal axes follow the eigenvectors. Their lengths are the square roots of the corresponding eigenvalues.
::::::
::::::::

## Projection retains one component

```{slide-options}
{"class":"foundation","eyebrow":"THE GEOMETRY OF A REPRESENTATION"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 32
:align: center

::::::{slide-column}
```{slide-figure} assets/band-projection.png
:alt: A two-band vector, its orthogonal projection on the equal-band line, and the discarded component connecting projection to original.
```
::::::

::::::{slide-column}
Original = projection + difference.

$$(0.9,1.1)=(1.0,1.0)+(-0.1,0.1).$$

The discarded difference might contain useful color information.
::::::
::::::::

## Why reduce dimensionality?

```{slide-options}
{"class":"foundation","eyebrow":"A CHOICE ABOUT INFORMATION"}
```

A spectrum may have thousands of wavelength features. A smaller representation can make patterns easier to visualize, store, and model.

But compression discards information. A low-variance feature can carry a rare and scientifically important signal.

Later: PCA finds directions of large variance in centered data; SVD provides a way to compute them. Scaling and the scientific question matter.

## Dot products connect geometry and fitting

```{slide-options}
{"class":"foundation","eyebrow":"COMPARING VECTORS"}
```

$$\mathbf x^{\mathsf T}\mathbf y=\sum_i x_i y_i.$$

The dot product combines corresponding entries and describes alignment together with vector lengths.

Suppose a model predicts $a\mathbf x$: a known direction $\mathbf x\ne\mathbf0$, with amplitude $a$ to estimate.

## Fit an amplitude by projection

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"A SIMPLE LEAST-SQUARES MODEL"}
```

Choose $a$ to minimize the squared residual:

$$S(a)=\|\mathbf y-a\mathbf x\|^2.$$

::::{fragment}
:effect: fade-in

$$S'(a)=-2\mathbf x^{\mathsf T}\mathbf y+2a\mathbf x^{\mathsf T}\mathbf x=0.$$
::::

::::{fragment}
:effect: fade-in

$$\hat a=\frac{\mathbf x^{\mathsf T}\mathbf y}{\mathbf x^{\mathsf T}\mathbf x}.$$
::::

This unweighted model has no separate baseline.

## Work through the projection

```{slide-options}
{"class":"foundation","vertical":true,"eyebrow":"DATA = FIT + RESIDUAL"}
```

Let $\mathbf x=(1,2)$ and $\mathbf y=(2,3)$:

$$\hat a=\frac{2+6}{1+4}=1.6,\qquad
\hat a\mathbf x=(1.6,3.2).$$

The residual is $(0.4,-0.2)$ and its dot product with $\mathbf x$ is zero. The fitted vector is the closest point on the model line.

## From foundations to a first fit

```{slide-options}
{"class":"foundation","eyebrow":"THURSDAY"}
```

1. Inspect measurements, units, flags, gaps, and uncertainties.
2. Choose a forward model and calculate residuals.
3. Use a noise model to weight those residuals.
4. Examine what the fit leaves unexplained.

Kepler photometry will provide the application. Today also includes Project 4 questions and completion time.
