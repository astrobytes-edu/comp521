---
title: "Random Variables, Propagation, and Shared Physics"
subtitle: "COMP 521 · Block 6 · Guide Lectures 1–2"
author: Anna Rosen
---

(unc-title)=
## Random variables, propagation, and shared physics

```{slide-options}
{"layout":"title","class":"uncertainty uncertainty-title","eyebrow":"COMP 521 · PROBABILITY, OPTIMIZATION, AND SCIENTIFIC DISCOVERY","transition":"fade"}
```

How does uncertainty in a physical model's inputs reach its predictions?

$$\boldsymbol\Theta\sim p(\boldsymbol\theta)
\quad\longrightarrow\quad
\mathbf Y=\mathcal G(\boldsymbol\Theta)
\quad\longrightarrow\quad p(\mathbf y).$$

Anna Rosen · San Diego State University

(unc-physics)=
## Deterministic physics, uncertain inputs

```{slide-options}
{"class":"uncertainty","eyebrow":"THE STATE OF PHYSICS AND THE STATE OF KNOWLEDGE"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
### The physical model

$$\mathbf y=\mathcal G(M,Z,t,\boldsymbol\phi).$$

- $M$: initial mass; $Z$: metallicity.
- $t$: age; $\boldsymbol\phi$: other physics parameters.
- Fixed inputs and algorithm give a fixed prediction, up to numerical error.
::::::

::::::{slide-column}
### Our information

:::{slide-element}
:class: soft-card
Uncertain inputs are represented by a **distribution of possible inputs**.
:::

Different plausible inputs produce different predictions through the same model.

Probability can describe missing knowledge as well as variation between objects.
::::::
::::::::

(unc-random-variable)=
## A random variable is a rule; a realization is a value

```{slide-options}
{"class":"uncertainty","eyebrow":"DEFINE THE OBJECT BEFORE USING ITS DISTRIBUTION"}
```

$$X:\Omega\longrightarrow\mathbb R.$$

- **Sample space $\Omega$:** the possible outcomes in the probability model.
- **Random variable $X$:** a rule assigning a number to each outcome.
- **Realization $x$:** one value obtained from that rule.

:::{slide-element}
:class: soft-card
Example: $X=M/M_\odot$ is the uncertain mass in solar units. A draw might give $x=1.03$.
:::

Uppercase letters denote random variables; lowercase letters denote their values.

(unc-taxonomy)=
## Identify what creates the uncertainty

```{slide-options}
{"class":"uncertainty","eyebrow":"DIFFERENT SOURCES REQUIRE DIFFERENT RESPONSES"}
```

::::::::{slide-columns}
:ratio: 1 1 1
:gap: 24

::::::{slide-column}
### Variability

**Aleatoric:** variation under a fixed model and conditioning information.

A different star or a repeated exposure can give a different outcome.

Model and sample the variability.
::::::

::::::{slide-column}
### Missing knowledge

**Epistemic:** uncertainty about a parameter or model.

A shared calibration or opacity law may be uncertain.

Informative data can constrain an identifiable parameter.
::::::

::::::{slide-column}
### Numerical error

An unconverged solver or incorrect derivative is a computational error.

It is not automatically random noise with a known distribution.

Check convergence, references, and the implementation.
::::::
::::::::

(unc-discrete)=
## Discrete probability assigns weight to outcomes

```{slide-options}
{"class":"uncertainty","eyebrow":"A PROBABILITY MASS FUNCTION"}
```

A **discrete random variable** takes values in a countable set.

::::::::{slide-columns}
:ratio: 1 1
:gap: 30

::::::{slide-column}
| Illustrative category $c$ | $P(C=c)$ |
|---|---:|
| White dwarf | $0.70$ |
| Neutron star | $0.20$ |
| Black hole | $0.10$ |

$$\sum_c P(C=c)=1.$$

These are teaching probabilities, not a measured remnant population.
::::::

::::::{slide-column}

:::{slide-question}
:title: Predict
Does density height give the probability of one exact mass?
:::

:::{slide-answer}
A point has probability zero for a continuous density. An interval's probability is its area under the curve.
:::
::::::
::::::::

(unc-pdf-cdf)=
## A density gives areas; a CDF gives accumulated probability

```{slide-options}
{"class":"uncertainty","eyebrow":"PDF, CDF, AND QUANTILES"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/pdf-cdf.png
:alt: Gaussian mass density with the interval from 0.95 to 1.05 shaded, and its cumulative distribution showing the same interval probability and the median at one.
```
::::::

::::::{slide-column}
**PDF:** probability density function $p_X$.

$$P(a\le X\le b)=\int_a^b p_X(x)\,dx.$$

**CDF:** cumulative distribution function.

$$F_X(x)=P(X\le x).$$

A **quantile** $x_q$ satisfies $F_X(x_q)=q$ when the CDF is continuous and increasing.

Density has inverse units of its input. Here $X=M/M_\odot$ is dimensionless.
::::::
::::::::

(unc-moments)=
## Mean, variance, and standard deviation describe different features

```{slide-options}
{"class":"uncertainty","eyebrow":"MOMENTS OF A DISTRIBUTION"}
```

**Expectation or mean:** the probability-weighted average.

$$\mu_X=\mathbb E[X]=\int x\,p_X(x)\,dx.$$

**Variance:** the mean squared distance from the mean.

$$\operatorname{Var}(X)=\mathbb E[(X-\mu_X)^2].$$

**Standard deviation:** the square root of the variance, in the units of $X$.

$$\sigma_X=\sqrt{\operatorname{Var}(X)}.$$

(unc-lotus)=
## Average the model without deriving the output density

```{slide-options}
{"class":"uncertainty","eyebrow":"THE LAW OF THE UNCONSCIOUS STATISTICIAN"}
```

:::{slide-element}
:class: soft-card
$$\mathbb E[g(X)]=\int g(x)\,p_X(x)\,dx.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 32

::::::{slide-column}
### What is being averaged?

- $g(x)$ is the model prediction at input $x$.
- $p_X(x)\,dx$ supplies its probability weight.
- Average **predictions across inputs**.
::::::

::::::{slide-column}
### What does this avoid?

You can compute the mean of $Y=g(X)$ without first finding a formula for $p_Y(y)$.

Monte Carlo replaces this weighted integral with an average of sampled predictions.
::::::
::::::::

(unc-joint)=
## Joint, marginal, and conditional probability

```{slide-options}
{"class":"uncertainty","eyebrow":"KEEP THE CONDITIONING INFORMATION VISIBLE"}
```

::::::::{slide-columns}
:ratio: 1.15 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/joint-conditional.png
:alt: An illustrative correlated Gaussian joint density. A vertical line fixes the first coordinate at one; the second panel compares the marginal density of Y with the normalized conditional density of Y given X equals one.
```
::::::

::::::{slide-column}
- **Joint** $p(x,y)$: combinations of values.
- **Marginal:** integrate out the coordinate you do not retain.
- **Conditional** $p(y\mid x)$: fix $x$ and normalize the slice.

$$p(y\mid x)=\frac{p(x,y)}{p(x)},\qquad p(x)>0.$$

These are synthetic standardized coordinates.
::::::
::::::::

(unc-covariance)=
## Covariance records how deviations occur together

```{slide-options}
{"class":"uncertainty","eyebrow":"DEPENDENCE IS PART OF THE INPUT MODEL"}
```

$$\operatorname{Cov}(X_1,X_2)
=\mathbb E[(X_1-\mu_1)(X_2-\mu_2)].$$

- **Positive covariance:** same-sign deviations tend to occur together.
- **Negative covariance:** opposite-sign deviations tend to occur together.
- **Correlation** rescales covariance: $\rho=\operatorname{Cov}(X_1,X_2)/(\sigma_1\sigma_2)$.

The **covariance matrix** collects variances on its diagonal and covariances elsewhere:

$$\Sigma_X=\begin{pmatrix}
\sigma_1^2 & \rho\sigma_1\sigma_2\\
\rho\sigma_1\sigma_2 & \sigma_2^2
\end{pmatrix}.$$

Zero covariance alone does not imply independence.

(unc-density-map)=
## A change of variables preserves probability, not density height

```{slide-options}
{"class":"uncertainty uncertainty-compact-figure","eyebrow":"ACCOUNT FOR THE STRETCH OF THE COORDINATE"}
```

```{slide-figure} assets/change-of-variables.png
:alt: A positive uniform input is mapped through the fourth power. Corresponding shaded input and output intervals contain equal probability although their widths and density heights differ.
:caption: Smooth invertible map on positive inputs. The inverse derivative corrects interval stretching.
```

$$p_Y(y)=p_X\!\left(g^{-1}(y)\right)
\left|\frac{d g^{-1}(y)}{dy}\right|.$$

The **inverse map** $g^{-1}$ returns the input corresponding to an output.

(unc-jacobian-volume)=
## A Jacobian describes local stretching in several dimensions

```{slide-options}
{"class":"uncertainty","eyebrow":"A MATRIX OF FIRST DERIVATIVES"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/jacobian-grid.png
:alt: A square coordinate grid and a unit square are transformed by a two by two matrix. The mapped square is a parallelogram with area 0.86.
```
::::::

::::::{slide-column}
$$J_{ij}=\frac{\partial y_i}{\partial\theta_j}.$$

$J_{ij}$ measures how output $i$ responds to input $j$ locally.

The **determinant** gives the signed local volume factor. Density uses its absolute value.

For a smooth invertible equal-dimensional map,

$$p_Y(\mathcal G(\boldsymbol\theta))
=\frac{p_\Theta(\boldsymbol\theta)}{|\det J|}.$$
::::::
::::::::

(unc-pushforward)=
## The pushforward is the distribution of mapped inputs

```{slide-options}
{"class":"uncertainty","eyebrow":"ONE MODEL, MANY PLAUSIBLE INPUTS"}
```

$$\boldsymbol\Theta^{(i)}\sim p(\boldsymbol\theta)
\quad\longrightarrow\quad
\mathbf Y^{(i)}=\mathcal G(\boldsymbol\Theta^{(i)}).$$

The **pushforward distribution** describes these output values and their probabilities.

We often need its mean and covariance rather than a closed-form density.

| Strategy | Main idea |
|---|---|
| Monte Carlo | Sample inputs and evaluate the full model. |
| First-order delta method | Approximate the model locally by its tangent. |
| Second-order delta method | Add the leading effect of curvature. |

(unc-toy-star)=
## One worked example: uncertain mass, uncertain luminosity

```{slide-options}
{"class":"uncertainty","eyebrow":"AN EXPLICIT LOCAL TEACHING MODEL"}
```

Define dimensionless mass and luminosity:

$$X=\frac{M}{M_\odot},\qquad Y=\frac{L}{L_\odot}=g(X)=X^4.$$

Let

$$X\sim\mathcal N(1,0.05^2).$$

- $\mathcal N(\mu,\sigma^2)$ denotes a Gaussian with mean $\mu$ and variance $\sigma^2$.
- The input mean is $1\,M_\odot$ and its standard deviation is $0.05\,M_\odot$.
- The fourth-power relation is a local approximation for teaching, not a universal stellar law.

The Gaussian is also a local approximation. Zero mass is 20 standard deviations below its mean.

(unc-monte-carlo)=
## Strategy 1: send sampled inputs through the full model

```{slide-options}
{"class":"uncertainty uncertainty-compact-figure","eyebrow":"MONTE CARLO PROPAGATION"}
```

```{slide-figure} assets/pushforward.png
:alt: A seeded ensemble of Gaussian mass draws is raised to the fourth power. Its luminosity histogram is skewed, and it is compared with the exact transformed density and the first-order Gaussian approximation.
:caption: Synthetic outputs from the local fourth-power teaching model.
```

For independent draws $x_i$, estimate $\bar y=N^{-1}\sum_i g(x_i)$.

**Executed result:** $1.01521\pm0.00045$ (MC standard error; 200,000 draws).

(unc-reparameterize)=
## Separate a distribution's parameters from its random draws

```{slide-options}
{"class":"uncertainty","eyebrow":"REPARAMETERIZATION: FIX THE NOISE, CHANGE THE INPUT MODEL"}
```

::::::::{slide-columns}
:ratio: .85 1.15
:gap: 28

::::::{slide-column}
$$X=\mu+\sigma\epsilon,$$

$$\epsilon\sim\mathcal N(0,1).$$

Draw standard-normal noise once. Scaling and shifting give draws with the desired mean and standard deviation.

Keep the same noise when comparing nearby parameter values.
::::::

::::::{slide-column}
```{slide-code} python
:title: Reuse one set of standard-normal draws
import numpy as np

rng = np.random.default_rng(20261105)
eps = rng.normal(size=200_000)
sigma = 0.05

def mean_luminosity(mu):
    x = mu + sigma * eps
    return np.mean(x**4)
```

This is a deterministic function of `mu` once `eps` is fixed. Differentiating it is a later topic.
::::::
::::::::

(unc-standard-error)=
## Output spread and Monte Carlo error are different quantities

```{slide-options}
{"class":"uncertainty","eyebrow":"STANDARD DEVIATION VERSUS STANDARD ERROR"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/mean-standard-error.png
:alt: One mass draw has a broad distribution. Means of 25 and 100 independent draws have narrower distributions, while the individual mass distribution keeps its original width.
```
::::::

::::::{slide-column}
**Standard deviation** $\sigma_Y$: spread of individual model outputs.

**Standard error** of their mean:

$$\operatorname{SE}(\bar Y)=\frac{\sigma_Y}{\sqrt N}.$$

For independent, identically distributed draws with finite variance, estimate this with $s_Y/\sqrt N$.

More draws improve the estimated mean. They do not narrow the modeled population.
::::::
::::::::

(unc-delta-one)=
## Strategy 2: use the local tangent

```{slide-options}
{"class":"uncertainty","eyebrow":"FIRST-ORDER DELTA METHOD"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/quartic-tangent.png
:alt: The fourth-power luminosity curve and its tangent at mean mass one agree locally but separate as the input moves away from the mean.
```
::::::

::::::{slide-column}
$$\begin{aligned}g(X)&\approx g(\mu)\\
&\quad+g'(\mu)(X-\mu).\end{aligned}$$

- $\mu=\mathbb E[X]$ is the expansion point.
- $g'(\mu)$ is the local slope or **sensitivity**.

$$\mathbb E[Y]\approx g(\mu),$$

$$\sigma_Y\approx |g'(\mu)|\sigma_X.$$

This works when the map is nearly linear across the input distribution's width.
::::::
::::::::

(unc-amplification)=
## How much does luminosity uncertainty grow?

```{slide-options}
{"class":"uncertainty","eyebrow":"WORK THE PROPAGATION BEFORE TRUSTING THE FORMULA"}
```

:::::{slide-worked}
::::{slide-step}
:title: 1 · Differentiate the model
$$g(x)=x^4,\qquad g'(x)=4x^3,\qquad g'(1)=4.$$
::::
::::{slide-step}
:title: 2 · Multiply the input spread by the local sensitivity
$$\sigma_Y\approx 4(0.05)=0.20.$$
::::
::::{slide-step}
:title: 3 · Express the result as relative uncertainty
$$\frac{\sigma_L}{L}\approx
\left|\frac{d\ln L}{d\ln M}\right|\frac{\sigma_M}{M}
=4(5\%)=20\%.$$
::::
:::::

This is a first-order approximation evaluated at the mean input.

(unc-covariance-map)=
## In several dimensions, propagate the whole covariance matrix

```{slide-options}
{"class":"uncertainty","eyebrow":"THE JACOBIAN SANDWICH"}
```

$$\delta\mathbf Y\approx J\,\delta\boldsymbol\Theta
\quad\Longrightarrow\quad
\Sigma_Y\approx J\Sigma_\Theta J^{\mathsf T}.$$

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/covariance-map.png
:alt: Constant-density contours of a correlated Gaussian input are mapped by a linear two by two Jacobian into transformed output contours with the covariance orientation given by J Sigma J transpose.
```
::::::

::::::{slide-column}
- $J$: local output sensitivities.
- $\Sigma_\Theta$: input variances and covariances.
- $J^{\mathsf T}$: **transpose**, which swaps rows and columns; it is not an inverse map.

The covariance identity is exact for a linear map with finite second moments. For a nonlinear map, it is local.
::::::
::::::::

(unc-jensen)=
## Curvature changes the mean prediction

```{slide-options}
{"class":"uncertainty","eyebrow":"PREDICT BEFORE REVEALING THE CORRECTION"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 28
:align: center

::::::{slide-column}
```{slide-figure} assets/quartic-tangent.png
:alt: The convex fourth-power curve lies above its tangent at the mean input, showing why the positive and negative deviations do not cancel after a nonlinear transformation.
```
::::::

::::::{slide-column}
The **convex** fourth-power curve lies above its tangents.

:::{slide-question}
:title: Predict
Is $\mathbb E[X^4]$ above, below, or equal to $(\mathbb E[X])^4$?
:::

:::{slide-answer}
Above here. Jensen's inequality gives

$$\mathbb E[g(X)]\ge g(\mathbb E[X])$$

for convex $g$. The inequality reverses for concave $g$.
:::
::::::
::::::::

(unc-delta-two)=
## Strategy 3: correct the leading effect of curvature

```{slide-options}
{"class":"uncertainty","eyebrow":"SECOND-ORDER DELTA METHOD"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 30

::::::{slide-column}
### One uncertain input

$$\mathbb E[g(X)]\approx
g(\mu)+\tfrac12 g''(\mu)\sigma_X^2.$$

$g''$ is the **second derivative**, measuring curvature.

For $g(x)=x^4$ at $\mu=1$,

$$1+\tfrac12(12)(0.05^2)=1.015.$$

The exact mean is $1.01501875$. Higher-order terms remain.
::::::

::::::{slide-column}
### Several inputs, one scalar output

$$\begin{aligned}\mathbb E[g(\boldsymbol\Theta)]&\approx g(\boldsymbol\mu)\\
&\quad+\tfrac12\operatorname{tr}(H_g\Sigma_\Theta).\end{aligned}$$

- **Hessian** $H_g$: matrix of second partial derivatives of $g$.
- **Trace** $\operatorname{tr}$: sum of a matrix's diagonal entries.
- $\Sigma_\Theta$: input covariance matrix.

Higher-order terms remain.
::::::
::::::::

(unc-methods)=
## Choose an evaluator by its assumptions and the needed accuracy

```{slide-options}
{"class":"uncertainty","eyebrow":"COMPARE AGAINST THE SAME INPUT MODEL"}
```

| Method | Mean in this example | Spread | Main limitation |
|---|---|---|---|
| Monte Carlo | $1.01521\pm0.00045$ (SE) | Sample distribution | Finite draws can miss rare regimes. |
| First order | $g(\mu)=1$ | Jacobian propagation | Misses curvature and regime changes. |
| Second order | $1.015$ | Additional approximation | Neglected higher-order terms. |

Exact mean: $1.01501875$.

An **affine map** is a linear map plus a constant offset. First-order propagation is exact for such a map.

(unc-boundary)=
## A local derivative cannot describe an unseen branch

```{slide-options}
{"class":"uncertainty","eyebrow":"WHEN LINEARIZATION BREAKS DOWN"}
```

```{slide-figure} assets/phase-boundary.png
:alt: A synthetic two-regime model changes branch within the uncertain input range. A tangent from one branch misses the outputs from the other branch, while full-model samples reach both.
```

A distribution can span a qualitative transition even when a derivative exists at its mean.

Stellar examples include changes of ignition regime or remnant outcome. This figure is a synthetic example, not a physical transition-mass calibration.

(unc-targeted)=
## Check the approximation where the model changes behavior

```{slide-options}
{"class":"uncertainty","eyebrow":"TARGETED ENSEMBLES NEAR KNOWN BOUNDARIES"}
```

:::::{slide-worked}
::::{slide-step}
:title: 1 · Locate the relevant regime boundary
Can plausible inputs reach both sides of the boundary?
::::
::::{slide-step}
:title: 2 · Evaluate the full model across that range
Use a targeted ensemble with explicit input probabilities or weights.
::::
::::{slide-step}
:title: 3 · Compare the quantities you intend to report
Compare means, spread, and regime probabilities. A mean can hide a branch.
::::
:::::

Check sampling error and coverage of rare regimes.

(unc-shared)=
## Independent scatter and shared physics affect a cohort differently

```{slide-options}
{"class":"uncertainty uncertainty-compact-figure","eyebrow":"DRAW A SHARED PARAMETER ONCE FOR THE WHOLE COHORT"}
```

```{slide-figure} assets/shared-shifts.png
:alt: Independent residuals move different objects separately; an additive shared offset moves all objects in one cohort together. Separate cohorts can have different shared offsets.
:caption: Colors identify cohorts. Right-panel offsets are −0.15, 0, and 0.15; identical residuals are reused.
```

$$Y_i=\theta+\epsilon_i.$$

Shared offset: $\operatorname{Var}(\theta)=\sigma_\theta^2$. Independent zero-mean residuals: $\operatorname{Var}(\epsilon_i)=\sigma_\epsilon^2$. Residuals are independent of $\theta$.

(unc-total-variance)=
## Total variance separates within-model and between-model spread

```{slide-options}
{"class":"uncertainty","eyebrow":"FIRST ASK WHICH RANDOM QUANTITY THE VARIANCE DESCRIBES"}
```

$$\begin{aligned}\operatorname{Var}(Y)
&=\mathbb E_\theta[\operatorname{Var}(Y\mid\theta)]\\
&\quad+\operatorname{Var}_\theta(\mathbb E[Y\mid\theta]).\end{aligned}$$

- $Y\mid\theta$ means: hold the shared physics fixed.
- $\mathbb E_\theta$ and $\operatorname{Var}_\theta$ average or measure spread over the uncertain shared parameter.
- This identity concerns the specified $Y$. For one object, it does not contain a sample-size factor.

In the additive model,

$$\operatorname{Var}(Y_i)=\sigma_\epsilon^2+\sigma_\theta^2.$$

(unc-cohort-mean)=
## Apply total variance to the cohort mean

```{slide-options}
{"class":"uncertainty","eyebrow":"THE QUANTITY BEING AVERAGED MUST BE NAMED"}
```

$$\bar Y=\frac1N\sum_{i=1}^N Y_i
=\theta+\frac1N\sum_{i=1}^N\epsilon_i.$$

:::::{slide-worked}
::::{slide-step}
:title: At fixed shared offset
$$\mathbb E[\bar Y\mid\theta]=\theta,\qquad
\operatorname{Var}(\bar Y\mid\theta)=\frac{\sigma_\epsilon^2}{N}.$$
::::
::::{slide-step}
:title: Across uncertain shared offsets
$$\operatorname{Var}(\bar Y)
=\frac{\sigma_\epsilon^2}{N}+\sigma_\theta^2.$$
::::
:::::

The independent part averages down. The shared contribution remains while its uncertainty is held fixed.

(unc-floor)=
## An unconstrained shared offset does not average away

```{slide-options}
{"class":"uncertainty","eyebrow":"PREDICTIVE UNCERTAINTY WITH FIXED SHARED-PARAMETER UNCERTAINTY"}
```

::::::::{slide-columns}
:ratio: 1.1 1
:gap: 26
:align: center

::::::{slide-column}
```{slide-figure} assets/shared-floor.png
:alt: Standard deviation of the cohort mean approaches the fixed shared-offset uncertainty of 0.1. Incorrectly treating that offset as independent predicts a continuing decrease. At 100 objects the correct value is about 0.102 rather than 0.022.
```
::::::

::::::{slide-column}
For $\sigma_\theta=0.1$, $\sigma_\epsilon=0.2$, and $N=100$:

$$\operatorname{sd}(\bar Y)=\sqrt{0.0104}\approx0.102.$$

Treating everything as independent would give about $0.022$.

**More informative kinds of data** can constrain an identifiable $\theta$. This floor is conditional on leaving its uncertainty fixed.
::::::
::::::::

(unc-synthesis)=
## What should survive the calculation?

```{slide-options}
{"class":"uncertainty","eyebrow":"LECTURES 1–2 · RETRIEVE, EXPLAIN, THEN CHECK"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 30

::::::{slide-column}
:::{slide-question}
:title: Explain to a partner
1. What is preserved under a coordinate change?
2. How can curvature shift a mean prediction?
3. Which term resists averaging in our shared-offset model?
:::
::::::

::::::{slide-column}
:::{slide-answer}
1. **Probability** in corresponding regions.
2. **Curvature** changes the average prediction.
3. **Shared variance** $\sigma_\theta^2$, while it stays fixed.
:::
::::::
::::::::

Reading: guide Lecture 1, Sections 1.1–1.5; Lecture 2, Sections 1.6–1.7.
