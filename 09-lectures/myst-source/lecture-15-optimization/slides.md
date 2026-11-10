---
title: "Optimization for Scientific Models"
subtitle: "Losses, gradients, and reliable parameter fitting"
author: Anna Rosen
---

(opt-title)=
## Optimization for Scientific Models

```{slide-options}
{"class": "optimization optimization-title"}
```

:::{slide-element}
:class: lead
Losses, gradients, and reliable parameter fitting
:::

```{slide-figure} assets/optimization-hero.png
:alt: Synthetic fading observations are shown with initial and fitted models. Beside them, accepted optimization updates move across equal-loss contours in initial brightness and fading timescale, from the starting parameters to the fit.
```

:::{slide-element}
:class: cover-meta
COMP 521 · Guide Lectures 3–4 · Anna Rosen
:::

(opt-question)=
## What does the curve tell us?

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/fading-data.png
:alt: Sixteen synthetic normalized-flux measurements decline with time, with known standard deviation 0.08.
```
:::{slide-question}
:title: Notice
Which feature tells us the initial brightness? Which tells us how quickly it fades?
:::

(opt-fading)=
## Two parameters: height and fading time

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$y(t;A,\tau)=A e^{-t/\tau}.$$
:::

::::::::{slide-columns}
:ratio: 1 1
::::::{slide-column}
### Amplitude $A$
Initial normalized excess flux: $y(0)=A$.
::::::
::::::{slide-column}
### Timescale $\tau$
Larger $\tau$ means slower fading.
::::::
::::::::

:::{slide-element}
:class: support
$y=F/F_0$ and $t=T/t_0$ use fixed reference scales. Synthetic data; exponential relaxation is a teaching model.
:::

(opt-route)=
## Separate prediction, comparison, and updating

```{slide-options}
{"class": "optimization"}
```

::::::::{slide-columns}
:ratio: 1 1 1
:gap: 28
::::::{slide-column}
:::{slide-element}
:class: process-card
### 1 · Predict
$$\mathbf y=\mathcal G(\boldsymbol\theta)$$
Parameters $\boldsymbol\theta$ are adjustable inputs. The forward model $\mathcal G$ predicts observations.
:::
::::::
::::::{slide-column}
:::{slide-element}
:class: process-card
### 2 · Compare
$$\mathcal L(\boldsymbol\theta)$$
The loss is one number scoring mismatch with data.
:::
::::::
::::::{slide-column}
:::{slide-element}
:class: process-card
### 3 · Update
$$\boldsymbol\theta_{k+1}$$
Propose new parameters.
:::
::::::
::::::::

:::{slide-element}
:class: takeaway
The loss states the question. The optimizer chooses the next candidate.
:::

(opt-layers)=
## Physics and data have different residuals

```{slide-options}
{"class": "optimization"}
```

A **residual** measures how far a prediction or equation is from its target.

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Inner physical solve
$$\mathbf R(\mathbf u,\boldsymbol\theta)=\mathbf0$$
**State variables $\mathbf u$** are computed, such as a stellar temperature profile.
::::::
::::::{slide-column}
### Outer data fit
$$\mathbf r=\mathcal G(\boldsymbol\theta)-\mathbf d$$
**Decision variables $\boldsymbol\theta$** are adjusted. Observations $\mathbf d$ stay fixed.
::::::
::::::::

:::{slide-element}
:class: support
Our relaxation model has an analytic solution. A Jaxstro prediction may instead require a numerical physics solve. Measurement residuals can remain because the data contain noise.
:::

(opt-residuals)=
## First, read the sign of a residual

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/residuals.png
:alt: Initial fading predictions and standardized residuals are shown side by side. Positive residuals mean predictions above observations.
```
$$r_i=\text{prediction}_i-\text{observation}_i.$$

:::{slide-element}
:class: takeaway
Positive: model too high. Negative: model too low.
:::

(opt-scale-residual)=
## The same miss can matter more

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: lead
Both measurements miss by $r=0.2$.
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Precise measurement
$$\sigma=0.1,\qquad q=r/\sigma=2.$$
::::::
::::::{slide-column}
### Noisier measurement
$$\sigma=0.4,\qquad q=r/\sigma=0.5.$$
::::::
::::::::

:::{slide-question}
:title: Predict
Which mismatch should count more in the fit?
:::

:::{slide-answer}
The first: its discrepancy is larger in measurement-uncertainty units.
:::

:::{slide-element}
:class: support
$\sigma$ is measurement standard deviation. A standardized residual is $q_i=r_i/\sigma_i$.
:::

(opt-gaussian)=
## Gaussian errors lead to weighted least squares

```{slide-options}
{"class": "optimization"}
```

**Measurement assumption:** independent errors with known, fixed standard deviations.

$$d_i=y_i(\boldsymbol\theta)+\epsilon_i,
\qquad \epsilon_i\sim\mathcal N(0,\sigma_i^2).$$

:::{slide-element}
:class: definition
$\mathcal N(0,\sigma_i^2)$ means Gaussian errors centered on zero, with standard deviation $\sigma_i$.
:::

:::{slide-element}
:class: hero-math
$$\mathcal L=\frac12\sum_i q_i^2=\frac12\chi^2.$$
:::

:::{slide-element}
:class: takeaway
A residual twice as large in uncertainty units contributes four times as much.

$\chi^2$ is called chi-square: the sum of squared standardized residuals.
:::

(opt-likelihood)=
## Hold the data fixed; vary the parameters

```{slide-options}
{"class": "optimization"}
```

**Likelihood:** the probability mass or density for the observed data, evaluated at different parameter choices.

:::{slide-element}
:class: hero-math
$$p(\mathbf d\mid\boldsymbol\theta)$$
:::

For the stated Gaussian model,

$$\mathcal L=-\log p(\mathbf d\mid\boldsymbol\theta)+\text{constant}.$$

:::{slide-element}
:class: takeaway
Maximizing likelihood and minimizing negative log-likelihood choose the same candidate.
:::

(opt-whitening)=
## Correlated errors change the comparison

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/whitening.png
:alt: Correlated Gaussian residual contours become circular after whitening with a Cholesky factor.
```
:::{slide-element}
:class: takeaway
A covariance matrix $\Sigma$ describes error variation: variances on the diagonal, shared variation off the diagonal.
:::

(opt-positive-definite)=
## Positive definite means positive in every direction

```{slide-options}
{"class": "optimization"}
```

For a symmetric matrix $M$,

:::{slide-element}
:class: hero-math
$$\mathbf v^{\mathsf T}M\mathbf v>0\qquad\text{for every }\mathbf v\ne\mathbf0.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Covariance
Every nonzero combination of errors has positive variance.
::::::
::::::{slide-column}
### Loss curvature
A positive-definite curvature matrix makes a local quadratic curve upward in every direction.
::::::
::::::::

:::{slide-element}
:class: definition
**Symmetric:** $M=M^{\mathsf T}$. The transpose $\mathsf T$ swaps rows and columns.

Example: $M=\begin{pmatrix}1&0\\0&4\end{pmatrix}$ gives $\mathbf v^{\mathsf T}M\mathbf v=v_1^2+4v_2^2>0$ for $\mathbf v\ne\mathbf0$.
:::

(opt-cholesky)=
## Cholesky factors the covariance

```{slide-options}
{"class": "optimization"}
```

**Cholesky factorization** writes a symmetric positive-definite covariance as

:::{slide-element}
:class: hero-math
$$\Sigma=C C^{\mathsf T}.$$
:::

For two measurements,

$$C=\begin{pmatrix}c_{11}&0\\c_{21}&c_{22}\end{pmatrix},
\qquad c_{11},c_{22}>0.$$

:::{slide-element}
:class: definition
**Lower triangular:** all entries above the diagonal are zero. A system with this structure can be solved one row at a time, starting at the top.
:::

(opt-whiten-solve)=
## Use the factor to standardize correlated errors

```{slide-options}
{"class": "optimization"}
```

Solve for the **whitened residuals**:

:::{slide-element}
:class: hero-math
$$C\mathbf q=\mathbf r.$$
:::

Whitened errors have variance $1$ in each coordinate and zero correlation between coordinates.

$$\mathcal L=\tfrac12\lVert\mathbf q\rVert_2^2,
\qquad \lVert\mathbf q\rVert_2^2=\sum_iq_i^2.$$

:::{slide-element}
:class: support
For fixed $\Sigma$, reuse $C$ but recompute $\mathbf q$ for each new residual vector. Solve the system rather than constructing an inverse.
:::

(opt-counts)=
## A photon count needs a count model

```{slide-options}
{"class": "optimization visual"}
```

Independent counts $n_i\sim\operatorname{Poisson}(\mu_i)$ have expected counts $\mu_i>0$.

```{slide-figure} assets/counts-observations.png
:alt: Five illustrative positive observed counts are one, two, two, four, and six.
```
$$\mathcal L=\sum_i\left(\mu_i-n_i\log\mu_i\right)+\text{constant}.$$

:::{slide-element}
:class: definition
**Poisson:** a distribution for integer event counts, with mean and variance both equal to $\mu_i$.
:::

(opt-counts-compare)=
## Changing the weights changes the answer

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/counts-losses.png
:alt: Poisson and data-weighted squared-error losses have different minimizing common count rates: three and approximately 2.069.
```
:::{slide-element}
:class: takeaway
**Neyman weighting** uses $1/n_i$. It emphasizes low fluctuations and is undefined at zero counts.
:::

(opt-calibration)=
## Build one loss we can solve by hand

```{slide-options}
{"class": "optimization"}
```

We have chosen how to compare. Now use one parameter to learn how to update.

::::::::{slide-columns}
:ratio: 1 1 1
::::::{slide-column}
### Model
$$y=1+2\theta$$
::::::
::::::{slide-column}
### Observation
$$d=3$$
::::::
::::::{slide-column}
### Uncertainty
$$\sigma=0.5$$
::::::
::::::::

$$\mathcal L=\frac12\left(\frac{1+2\theta-3}{0.5}\right)^2.$$

:::{slide-answer}
This simplifies to $\boxed{\mathcal L=8(\theta-1)^2}$, with a minimum at $\theta=1$.
:::

(opt-objective)=
## A location and a value answer different questions

```{slide-options}
{"class": "optimization"}
```

$$\mathcal L(\theta)=8(\theta-1)^2.$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Minimizing location
:::{slide-element}
:class: hero-math
$$\theta^*=1$$
:::
The **argmin** gives the location or locations.
::::::
::::::{slide-column}
### Minimum value
:::{slide-element}
:class: hero-math
$$\mathcal L(\theta^*)=0$$
:::
The **minimum** gives the best score.
::::::
::::::::

:::{slide-element}
:class: support
The objective is the scalar score; the feasible set contains the allowed parameter values.
:::

(opt-slope)=
## The derivative gives the local direction

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/derivative.png
:alt: The calibration loss and its tangent at minus one show that moving right initially lowers the loss.
```
$$\mathcal L'(\theta)=16(\theta-1).$$

:::{slide-element}
:class: takeaway
A derivative is a local rate of change. At $\theta=-1$, the slope is $-32$.
:::

(opt-gradient)=
## Several parameters give several slopes

```{slide-options}
{"class": "optimization"}
```

A **partial derivative** varies one parameter while holding the others fixed.

For two parameters,

:::{slide-element}
:class: hero-math
$$\mathbf g=\nabla\mathcal L
=\begin{pmatrix}\partial\mathcal L/\partial\theta_1\\[4pt]\partial\mathcal L/\partial\theta_2\end{pmatrix}.$$
:::

:::{slide-element}
:class: takeaway
The gradient has one component per parameter, not per observation.
:::

(opt-descent)=
## Ask whether the local loss should decrease

```{slide-options}
{"class": "optimization"}
```

A small proposed step $\mathbf s$ predicts

$$\Delta\mathcal L\approx\mathbf g^{\mathsf T}\mathbf s.$$

:::{slide-element}
:class: hero-math
$$\mathbf g^{\mathsf T}\mathbf s<0$$
:::

This is a **descent direction**.

:::{slide-element}
:class: support
The dot product sums $g_js_j$ over parameters. Steepest descent depends on the coordinate scales and distance measure.
:::

(opt-chain-rule)=
## The Jacobian has a row for each residual

```{slide-options}
{"class": "optimization"}
```

For the fading fit, choose $\boldsymbol\theta=(a,b)=(\log A,\log\tau)$.

:::{slide-element}
:class: definition
These are **log coordinates**: $A=e^a$ and $\tau=e^b$ stay positive for any finite $a,b$.
:::

$$J_{ij}=\frac{\partial q_i}{\partial\theta_j}.$$

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Rows: measurements
One row per standardized residual.
::::::
::::::{slide-column}
### Columns: parameters
One sensitivity pattern per parameter.
::::::
::::::::

:::{slide-question}
:title: Predict
Sixteen observations, two parameters: what shape is $J$?
:::

:::{slide-answer}
$J$ has 16 rows and 2 columns.
:::

(opt-gradient-chain)=
## Add the residual contributions to each slope

```{slide-options}
{"class": "optimization"}
```

For $\mathcal L=\tfrac12\sum_iq_i^2$, the chain rule gives

:::{slide-element}
:class: hero-math
$$\boxed{\mathbf g=J^{\mathsf T}\mathbf q}.$$
:::

$$\underbrace{J^{\mathsf T}}_{2\times16}
\qquad\underbrace{\mathbf q}_{16\times1}
=\underbrace{\mathbf g}_{2\times1}.$$

:::{slide-element}
:class: support
Each slope combines the current mismatch with its sensitivity. The transpose $\mathsf T$ swaps rows and columns.
:::

(opt-gd)=
## Gradient descent is an update rule

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$\boldsymbol\theta_{k+1}=\boldsymbol\theta_k-\eta\mathbf g_k.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Direction
$-\mathbf g_k$: move against the current slopes.
::::::
::::::{slide-column}
### Distance
$\eta>0$: the step size, also called the learning rate.
::::::
::::::::

:::{slide-element}
:class: support
$k$ counts updates. Recompute the gradient after moving.
:::

(opt-gd-worked)=
## Work the first update

```{slide-options}
{"class": "optimization"}
```

Start at $\theta_0=-1$ with $\eta=1/32$.

::::::{slide-worked}
:title: Calibration loss
:::{slide-step}
**Slope:** $g_0=16(-1-1)=-32$.
:::
:::{slide-step}
**Update:** $\theta_1=-1-(1/32)(-32)=0$.
:::
:::{slide-step}
**Check:** the actual loss falls from $32$ to $8$.
:::
::::::

:::{slide-element}
:class: support
The next update gives $\theta_2=0.5$ and loss $2$.
:::

(opt-step-size)=
## Predict the effect of the step size

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/gd-step-sizes.png
:alt: Four calibration trajectories compare monotone convergence, damped oscillation, a persistent two-point cycle, and divergence.
```
:::{slide-question}
:title: Predict
Which trajectories approach the minimum? Can oscillation still converge?
:::

:::{slide-answer}
The first two converge. Alternating errors can shrink.
:::

(opt-stability)=
## Stability comes from the error multiplier

```{slide-options}
{"class": "optimization"}
```

Define the parameter error $e_k=\theta_k-1$.

:::{slide-element}
:class: hero-math
$$e_{k+1}=(1-16\eta)e_k.$$
:::

The error shrinks when

$$|1-16\eta|<1\quad\Longrightarrow\quad0<\eta<1/8.$$

:::{slide-question}
:title: Explain
Why does $\eta=1/16$ reach the minimum in one update?
:::

:::{slide-answer}
Its error multiplier is zero. This result is specific to this quadratic.
:::

(opt-hessian)=
## Curvature describes how slopes change

```{slide-options}
{"class": "optimization"}
```

The **Hessian** collects second derivatives of one scalar loss:

:::{slide-element}
:class: hero-math
$$H_{jk}=\frac{\partial^2\mathcal L}{\partial\theta_j\,\partial\theta_k}.$$
:::

- $p$ parameters give a $p\times p$ Hessian.
- For the calibration, $\mathcal L''(\theta)=16$ everywhere.

:::{slide-element}
:class: takeaway
The gradient tells us which way. Curvature tells us how quickly the slopes change.
:::

(opt-bowl)=
## One direction can be much steeper

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/curvature-bowl.png
:alt: Elliptical equal-loss contours show curvature one in e1 and fifty in e2.
```
$$\mathcal L=\tfrac12(e_1^2+50e_2^2),\qquad H=\operatorname{diag}(1,50).$$

:::{slide-element}
:class: support
Parameter errors $e_1,e_2$ measure displacement from the minimum. Here $\operatorname{diag}(1,50)$ means diagonal entries $1,50$ and zeros elsewhere.
:::

(opt-eigenvectors)=
## Read curvature one direction at a time

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$H\mathbf v=\lambda\mathbf v.$$
:::

An **eigenvector** $\mathbf v\ne\mathbf0$ keeps the same line under multiplication by $H$. Its **eigenvalue** $\lambda$ is the scale factor.

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Shallow direction
$\mathbf v=(1,0)^{\mathsf T}$ has $\lambda=1$.
::::::
::::::{slide-column}
### Steep direction
$\mathbf v=(0,1)^{\mathsf T}$ has $\lambda=50$.
::::::
::::::::

:::{slide-element}
:class: definition
For a symmetric Hessian and a **unit eigenvector** (length one), $\lambda$ is the curvature along that direction. Positive definite means all eigenvalues are positive.
:::

(opt-conditioning)=
## One step size must serve both directions

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/conditioning-paths.png
:alt: Gradient descent zigzags in a narrow valley and converges slowly along its shallow direction.
```
$$\kappa=\frac{\lambda_{\max}}{\lambda_{\min}}=50,
\qquad 0<\eta<2/50=0.04.$$

:::{slide-element}
:class: support
The **condition number** compares the largest and smallest curvature here. A large ratio means one step size must handle very different directional responses.
:::

(opt-scaling)=
## Rescaling can turn an ellipse into a circle

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/scaling.png
:alt: A coordinate stretch changes the same diagonal quadratic from elliptical contours to circular contours.
```
$$z_1=e_1,\qquad z_2=\sqrt{50}\,e_2.$$

:::{slide-element}
:class: support
**Preconditioning** changes coordinates or step geometry to make directional responses more balanced. **Nondimensionalization** expresses variables relative to fixed physical reference scales. Neither adds observations.
:::

(opt-momentum)=
## Keep some of the previous motion

```{slide-options}
{"class": "optimization"}
```

::::::::{slide-columns}
:ratio: 1.35 1
:gap: 36
:align: center
::::::{slide-column}
```{slide-figure} assets/momentum.png
:alt: Tuned heavy-ball momentum converges faster than fixed-step gradient descent on this specified quadratic.
```
::::::
::::::{slide-column}
$$\mathbf v_{k+1}=\beta\mathbf v_k-\eta\mathbf g_k,$$
$$\boldsymbol\theta_{k+1}=\boldsymbol\theta_k+\mathbf v_{k+1}.$$

**Heavy-ball momentum:** $\mathbf v$ is the update; $\beta$ retains part of the previous update.
::::::
::::::::

:::{slide-element}
:class: support
The plotted tuning is specific to this quadratic. Momentum can overshoot.
:::

(opt-newton-model)=
## Use a local quadratic model of the loss

```{slide-options}
{"class": "optimization"}
```

At the current parameters, approximate the loss after a displacement $\mathbf s$ by

:::{slide-element}
:class: hero-math
$$m(\mathbf s)=\mathcal L+\mathbf g^{\mathsf T}\mathbf s
+\tfrac12\mathbf s^{\mathsf T}H\mathbf s.$$
:::

::::::::{slide-columns}
:ratio: 1 1 1
::::::{slide-column}
### Current value
$\mathcal L$
::::::
::::::{slide-column}
### Local slope
$\mathbf g^{\mathsf T}\mathbf s$
::::::
::::::{slide-column}
### Curvature
$\tfrac12\mathbf s^{\mathsf T}H\mathbf s$
::::::
::::::::

(opt-newton)=
## Solve for the Newton step

```{slide-options}
{"class": "optimization visual"}
```

$$H\mathbf s=-\mathbf g.$$

```{slide-figure} assets/newton-model.png
:alt: For the scalar quadratic, the second-order model equals the actual loss and the Newton step reaches the minimum.
```
:::{slide-element}
:class: support
One exact update solves an unconstrained positive-definite quadratic. Solve the linear system; do not explicitly invert $H$.
:::

(opt-stationary)=
## Zero slope does not identify a minimum

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/stationary-points.png
:alt: The quartic x to the fourth minus two x squared has minima at minus one and one and a maximum at zero.
```
:::{slide-element}
:class: takeaway
A stationary point has zero gradient. It can be a minimum, maximum, or saddle.
:::

:::{slide-element}
:class: definition
A **saddle** rises along some directions and falls along others. This one-dimensional plot shows only minima and a maximum.
:::

(opt-newton-failure)=
## Negative curvature can send Newton uphill

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/newton-failure.png
:alt: A Newton trial from x equals one quarter increases the quartic loss and moves toward its maximum.
```
$$x:0.25\longrightarrow-0.0385,
\qquad \mathcal L:-0.1211\longrightarrow-0.0030.$$

:::{slide-element}
:class: support
The loss increased. A Newton proposal still needs a safeguard.
:::

(opt-safeguards)=
## Limit how far you trust a local prediction

```{slide-options}
{"class": "optimization"}
```

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Line search
Choose a descent direction. Shorten the step until the actual loss decreases enough.
::::::
::::::{slide-column}
### Trust region
Limit the step to a neighborhood where the local model is useful. Compare predicted and actual reduction.
::::::
::::::::

:::{slide-element}
:class: takeaway
Evaluate the actual objective before accepting a proposal.
:::

(opt-gauss-newton)=
## Linearize the residuals

```{slide-options}
{"class": "optimization"}
```

Our loss is a sum of squared residuals. **Linearize:** approximate their changes using first derivatives.

:::{slide-element}
:class: hero-math
$$\mathbf q(\boldsymbol\theta+\mathbf s)\approx\mathbf q+J\mathbf s.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Current mismatch
$\mathbf q$
::::::
::::::{slide-column}
### Predicted change
$J\mathbf s$
::::::
::::::::

:::{slide-element}
:class: support
Gauss–Newton exploits the least-squares structure rather than treating the loss as a black box.
:::

(opt-gn-curvature)=
## The Jacobian gives approximate loss curvature

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$H_{\mathrm{GN}}=J^{\mathsf T}J.$$
:::

$$\mathbf v^{\mathsf T}H_{\mathrm{GN}}\mathbf v=\lVert J\mathbf v\rVert_2^2\ge0.$$

**Positive semidefinite:** curvature is never negative, but flat directions can remain.

:::{slide-element}
:class: support
This omits curvature of the individual residual functions. Unlike positive definite, semidefinite allows zero curvature. A full nonlinear step still needs an acceptance test.
:::

(opt-rank)=
## Can the sensitivity columns distinguish changes?

```{slide-options}
{"class": "optimization"}
```

Recall: one column of $J$ describes how all residuals respond to one parameter.

:::{slide-element}
:class: hero-math
$$J\mathbf v=\mathbf0.$$
:::

If a nonzero parameter change $\mathbf v$ satisfies this equation, it produces no change in the linearized residuals.

:::{slide-element}
:class: definition
**Full column rank:** the columns are linearly independent. No nonzero combination of parameter changes cancels across every residual.
:::

:::{slide-element}
:class: takeaway
Then $J^{\mathsf T}J$ is positive definite. A nonzero gradient gives a Gauss–Newton descent direction, still subject to a trial-loss test.
:::

(opt-gn-step)=
## Solve the linearized least-squares problem

```{slide-options}
{"class": "optimization"}
```

$$\mathbf s_{\mathrm{GN}}\in\underset{\mathbf s}{\operatorname{argmin}}
\frac12\lVert\mathbf q+J\mathbf s\rVert_2^2.$$

```{slide-code} python
:title: Use a least-squares solver
step = np.linalg.lstsq(J, -q, rcond=None)[0]
```

:::{slide-element}
:class: takeaway
Solve $J\mathbf s\approx-\mathbf q$ directly. Forming $J^{\mathsf T}J$ can amplify numerical sensitivity.
:::

:::{slide-element}
:class: definition
**Normal equations:** $J^{\mathsf T}J\mathbf s=-J^{\mathsf T}\mathbf q$. They express the same least-squares stationarity condition; the code avoids forming that product.
:::

(opt-lm)=
## Damping makes the proposal more conservative

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$\bigl(J^{\mathsf T}J+\nu I\bigr)\mathbf s=-\mathbf g.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Large $\nu$
A short step toward the negative gradient.
::::::
::::::{slide-column}
### Small $\nu$
Approach Gauss–Newton when that step is well defined.
::::::
::::::::

:::{slide-element}
:class: support
Levenberg–Marquardt uses positive damping $\nu$. The **identity matrix** leaves vectors unchanged: $I\mathbf v=\mathbf v$. Adding $\nu I$ adds positive curvature in every direction.
:::

(opt-lm-damping)=
## Compare proposals from the same point

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/lm-damping.png
:alt: Three log-parameter proposals from the same starting point use damping one, one hundred, and one thousand. Their actual losses decide acceptance.
```
:::{slide-element}
:class: takeaway
Damping changes a proposal. The actual trial loss decides whether to accept it.
:::

(opt-lm-loop)=
## A rejected trial keeps the current parameters

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/lm-trace.png
:alt: The executed fit separates accepted states and rejected trial losses and shows the adapted damping strength.
```
:::{slide-element}
:class: takeaway
This run: 11 trials, 8 accepted, 3 rejected. Rejected trials still cost evaluations.
:::

(opt-fit)=
## Does the fitted curve explain the data?

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/fit-result.png
:alt: The fitted exponential is compared with synthetic observations, the generating curve, and standardized residuals.
```
:::{slide-question}
:title: Inspect
Look for systematic residual patterns, not just a low loss.
:::

(opt-identifiability)=
## Missing information leaves a flat direction

```{slide-options}
{"class": "optimization visual"}
```

**Identifiability:** can different parameter choices be distinguished by their predictions?

```{slide-figure} assets/identifiability.png
:alt: Loss contours in log amplitude and log timescale are flat in timescale for observations only at time zero; observations spanning time give a two-parameter basin.
```
:::{slide-element}
:class: takeaway
At $t=0$, $y=A$ for every $\tau$. The data cannot distinguish timescales.
:::

(opt-regularization)=
## A penalty changes the question being fitted

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/regularization.png
:alt: A data loss minimized at z equals two and a quadratic penalty centered at zero combine to move the minimizer to one.
```
:::{slide-element}
:class: takeaway
Regularization adds a stated preference. It can move the fitted answer.
:::

(opt-map)=
## A Gaussian prior gives a quadratic penalty

```{slide-options}
{"class": "optimization"}
```

In the chosen coordinates,

$$p(\boldsymbol\theta)=\mathcal N(\boldsymbol\theta_0,I/\lambda)$$

adds the penalty

:::{slide-element}
:class: hero-math
$$\frac{\lambda}{2}\lVert\boldsymbol\theta-\boldsymbol\theta_0\rVert_2^2.$$
:::

**MAP:** maximum a posteriori, the location maximizing posterior density.

**Prior:** parameter density before conditioning on data. **Posterior:** after conditioning.

:::{slide-element}
:class: support
$\boldsymbol\theta_0$ states the preference and $\lambda>0$ its strength. A fixed prior and adaptive LM damping have different roles.
:::

(opt-constraints)=
## Log coordinates enforce strict positivity

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$A=e^a,\qquad\tau=e^b.$$
:::

- Any finite $a,b$ give $A,\tau>0$.
- The optimizer can vary $a,b$ without crossing a zero boundary.

:::{slide-element}
:class: takeaway
Reparameterization changes the coordinates used to search.
:::

:::{slide-element}
:class: support
This changes how we search, while preserving the same predictions and loss at corresponding parameter values.
:::

(opt-boundary)=
## A valid zero needs a boundary-aware method

```{slide-options}
{"class": "optimization"}
```

A separate background parameter may satisfy $B\ge0$, including $B=0$.

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### Exponentiation
$$B=e^z>0$$
Approaches zero but never reaches it at finite $z$.
::::::
::::::{slide-column}
### Projection for this bound
$$B\leftarrow\max(0,B)$$
Projection can represent $B=0$ exactly.
::::::
::::::::

:::{slide-element}
:class: support
Near a boundary, a small transformed gradient can be misleading.
:::

(opt-choose)=
## Match the optimizer to the problem

```{slide-options}
{"class": "optimization"}
```

::::::::{slide-columns}
:ratio: 1 1 1
:gap: 28
::::::{slide-column}
### Residual vector
Gauss–Newton or LM, with safeguards.
::::::
::::::{slide-column}
### General smooth loss
Quasi-Newton methods estimate curvature from changes in gradients.
::::::
::::::{slide-column}
### Noisy sampled gradients
Stochastic methods use gradients estimated from random data subsets. Momentum can help steady the updates.
::::::
::::::::

:::{slide-element}
:class: support
BFGS is a quasi-Newton method. Adam adapts updates using running averages of gradients and squared gradients. Neither supplies missing data information.
:::

(opt-checklist)=
## What would you check before trusting the fit?

```{slide-options}
{"class": "optimization"}
```

:::{slide-question}
:title: Explain
The gradient is small. What evidence would you seek next?
:::

:::{slide-answer}
Check derivatives, residual structure, and predictions beyond the fitted data.
:::

::::::::{slide-columns}
:ratio: 1 1 1
::::::{slide-column}
### Algorithm
Read the stop reason.
::::::
::::::{slide-column}
### Physics
Check model assumptions.
::::::
::::::{slide-column}
### Inference
A point fit is not an uncertainty distribution.
::::::
::::::::
