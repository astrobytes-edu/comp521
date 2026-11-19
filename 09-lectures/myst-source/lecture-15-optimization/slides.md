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

:::{speaker-note}
- **Connect to Lectures 1–2:** We propagated uncertain inputs through a physical model to uncertain outputs. Today we start with measured outputs and ask which model inputs explain them.
- **Read the left panel:** The same synthetic measurements are compared with initial and fitted predictions. Improving agreement is the observable goal, not collecting optimizer names.
- **Read the right panel:** The axes are initial brightness $A$ and fading timescale $\tau$. Each point is a physical parameter choice. Equal-loss contours show its score; the path connects accepted updates from this executed fit.
- **State the narrative:** Choose the loss, understand derivatives, construct a proposal, check its actual result, and interpret the fitted answer.
- **Qualify:** These are synthetic relaxation data, not a complete stellar calculation or a benchmark.
- **Segue:** “First, read what the measurements ask us to explain.”
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

:::{speaker-note}
- **Read the observable first:** Point to the measurement times, normalized excess-flux values, and uncertainty bars. Sixteen synthetic observations span zero through six normalized time units.
- **Prompt:** “Which features of the decline need explaining?” Invite initial height, fading rate, and scatter around a smooth trend.
- **Separate the jobs:** The smooth physical prediction describes the trend. The measurement model describes why observed points need not lie exactly on it.
- **Avoid a misconception:** A curve passing through every noisy point is not automatically a better physical explanation. We will compare disagreements with their stated uncertainty.
- **Segue:** “Two parameters will describe the height and time scale of this particular trend.”
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

:::{speaker-note}
- **Define the formula:** $y(t)=A\exp(-t/\tau)$. The amplitude $A$ sets the initial excess flux, and positive $\tau$ sets how slowly the signal relaxes.
- **Define the units:** $t=T/t_0$ and $y=F/F_0$ are dimensionless. Here $\tau$ is a time scale in units of $t_0$; “excess” means a background has already been removed.
- **Explain the physics:** The curve solves $dy/dt=-y/\tau$ with initial value $A$.
- **State the synthetic setup:** Generating values are $A=1.8$, $\tau=2.4$, and independent Gaussian measurement standard deviation $0.08$.
- **Predict:** Increasing $\tau$ at fixed $A$ slows the fading.
- **Segue:** “Now organize the fitting calculation into separate responsibilities.”
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

:::{speaker-note}
- **Define the inputs:** Parameters $\boldsymbol\theta$ are adjustable model inputs. A forward model $\mathcal G$ maps them to predictions, such as brightnesses at observed times.
- **Define the comparison:** A scalar loss assigns one score to a candidate. Its measurement assumptions and any penalties specify the question being fitted.
- **Define the update:** The optimizer proposes another parameter point. A successful numerical update does not establish that the physical or measurement model is adequate.
- **Prompt:** “Which stage changes when we choose another optimizer?” The proposal strategy can change while the model, data, and objective remain fixed.
- **Segue:** “In a Jaxstro model, even making the prediction may require a physical solve.”
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

:::{speaker-note}
- **Define residual first:** A residual measures disagreement with a stated target. An equation residual and an observation residual can have different targets and units.
- **Name the inner job:** For chosen parameters, a physical solver computes state variables $\mathbf u$ while enforcing differential equations, conservation conditions, and boundary conditions to numerical tolerance. Reserve $\mathbf s$ later for an optimizer step.
- **Name the outer job:** The optimizer changes parameters; observations remain fixed. Measurement residuals need not vanish because the observations contain noise.
- **Use our simplification:** The relaxation solution is analytic, so this example has no iterative inner solve to conceal.
- **Keep the formulation qualified:** Simultaneous constrained approaches can also be legitimate. An arbitrary soft penalty is not automatically equivalent to enforcing a required physical equation.
- **Check and segue:** An optimizer can fit numerical error from an inaccurate prediction. “Now read the sign of the data residual.”
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
The plot shows $q_i=r_i/\sigma_i$. Because $\sigma_i>0$, a positive value means the model is too high.
:::

:::{speaker-note}
- **Define the sign:** $r_i=y(t_i;\boldsymbol\theta)-d_i$ is prediction minus the fixed observation. A positive residual means the prediction lies above datum $d_i$.
- **Read the panels:** The initial curve misses the observations systematically. The right panel already shows standardized residuals $q_i=r_i/0.08$, rather than raw flux or parameter errors.
- **Prompt:** “Why are these plotted residuals negative?” The initial prediction lies below the corresponding data.
- **Keep the bookkeeping clear:** There is one residual per observation, even though only two parameters are fitted.
- **Misconception:** Reversing both residual and Jacobian signs consistently is harmless for squared error; reversing only one gives a wrong gradient.
- **Segue:** “Explain why the measurement uncertainty belongs in that comparison.”
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

:::{speaker-note}
- **Define standardization:** $q_i=r_i/\sigma_i$ expresses a mismatch in measurement-standard-deviation units. It is dimensionless when residual and uncertainty use the same units.
- **Predict:** “Hold the raw mismatch fixed. What happens if its stated uncertainty increases?” The magnitude of the standardized mismatch decreases.
- **Explain the weighting:** Under the coming Gaussian model, the same raw discrepancy contributes less when that measurement is less precise.
- **Preserve the assumption:** The uncertainty scale describes a measurement model. Changing it arbitrarily to make a fit look better changes the question.
- **Segue:** “A probability model now explains why we add the squared standardized discrepancies.”
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

:::{speaker-note}
- **Read the distribution:** $\epsilon_i\sim\mathcal N(0,\sigma_i^2)$ means Gaussian measurement errors centered on zero, with variance $\sigma_i^2$ and standard deviation $\sigma_i$.
- **State the example:** Our synthetic fading measurements have independent errors with known, fixed $\sigma=0.08$. Thus $q_i=[y_i(\boldsymbol\theta)-d_i]/\sigma_i$.
- **Read the loss:** Dropping parameter-independent terms from the negative log-likelihood gives $\mathcal L=\tfrac12\sum_iq_i^2$. Chi-square is the sum without the half.
- **Explain the half:** It simplifies differentiation. Removing it preserves the minimizer but rescales gradients, curvature, and a fixed learning rate's meaning.
- **Check:** Noise in the fixed observations does not make each full-data objective evaluation random.
- **Caveat and segue:** Parameter-dependent covariance requires its determinant term and derivatives. “Why is this a likelihood?”
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

:::{speaker-note}
- **Read the conditional statement:** A likelihood evaluates the measurement model at the observed data while varying candidate parameters.
- **Define the log transformation:** Taking a logarithm turns products of independent density factors into sums. Negating that logarithm turns maximization into minimization.
- **Prompt:** “Are we assigning a probability distribution to parameters merely by plotting the likelihood?” No. A likelihood is not automatically a posterior distribution.
- **Recall density:** For continuous measurements, density at one observed value is not the probability of that exact point.
- **Connect to the loss:** Our weighted squares follow from the declared Gaussian model, rather than from a universal rule that every objective must be squared error.
- **Segue:** “Correlated measurement errors require a joint comparison.”
:::

(opt-whitening)=
## Correlated errors change the comparison

```{slide-options}
{"class": "optimization visual"}
```

:::{slide-element}
:class: definition
**Whitening** changes residual coordinates so the assumed measurement errors have variance $1$ in each coordinate and zero correlation between coordinates.
:::

```{slide-figure} assets/whitening.png
:alt: Correlated Gaussian residual contours become circular after whitening with a Cholesky factor.
```
:::{slide-element}
:class: support
Here $\mathbf r$ denotes raw residuals (predictions minus observations), and $\mathbf q$ denotes whitened residuals. The covariance matrix $\Sigma$ stores variances on the diagonal and shared error variation off the diagonal.
:::

:::{speaker-note}
- **Read covariance:** A covariance matrix contains error variances on its diagonal. Off-diagonal entries describe errors varying together; covariance is not automatically a dimensionless correlation coefficient.
- **Read the left panel:** The tilted equal-distance ellipse says some combinations of measurement errors are more plausible than others. Dividing each component by its own standard deviation does not generally remove that correlation.
- **Read the right panel:** Whitening changes residual coordinates so each modeled error coordinate has variance one and different coordinates have zero correlation. Equal error-model distance then becomes round.
- **State the limit:** Variance one describes the assumed measurement-error distribution. A finite set of fitted residuals need not have sample variance exactly one; fitting and model mismatch can also affect their empirical pattern.
- **Caution:** These are quadratic-distance contours. A two-dimensional contour does not automatically enclose the one-dimensional 68-percent probability.
- **Prompt and segue:** The same raw residual can get a different loss under a different covariance model. “Define the matrix property the factorization requires.”
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

:::{speaker-note}
- **Read the definition:** Transpose $\mathsf T$ swaps rows and columns. A symmetric matrix satisfies $M=M^{\mathsf T}$. It is positive definite when $\mathbf v^{\mathsf T}M\mathbf v>0$ for every nonzero vector $\mathbf v$.
- **Use the example:** With diagonal entries one and four, the expression is $v_1^2+4v_2^2$. It is positive unless both entries of $\mathbf v$ vanish.
- **Connect to covariance:** This expression is the variance of a linear combination of errors. Positive definite excludes an exactly zero-variance combination.
- **Connect to curvature:** A positive-definite Hessian makes the local quadratic curve upward in every direction. At a smooth stationary point it is sufficient for a strict local minimum, not global uniqueness.
- **Contrast:** Positive semidefinite allows equality in a nonzero direction. We will see that distinction again in Gauss–Newton.
- **Segue:** “Now factor this covariance into a convenient shape.”
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

:::{speaker-note}
- **Define the operation:** Cholesky factorization writes a symmetric positive-definite covariance as $\Sigma=CC^{\mathsf T}$. This is a factorization, not an inverse.
- **Read the structure:** Lower triangular means zero above the diagonal. The displayed two-measurement factor has positive diagonal entries $c_{11},c_{22}$.
- **Show the solve:** In $C\mathbf q=\mathbf r$, the first row gives $q_1=r_1/c_{11}$. The second gives $q_2=(r_2-c_{21}q_1)/c_{22}$. Each row uses values already computed. This is forward substitution.
- **Bound the assumption:** Ordinary Cholesky here requires strict positive definiteness. Singular covariance needs separate treatment, not an unexplained inverse.
- **Prompt:** “Why can we solve from the first row downward?” Entries above the diagonal vanish.
- **Segue:** “Use that factor to standardize the correlated errors.”
:::

(opt-whiten-solve)=
## Use the factor to standardize correlated errors

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: definition
**Given:** known measurement-error covariance $\Sigma$ and its lower-triangular Cholesky factor $C$, with $\Sigma=CC^{\mathsf T}$.
:::

:::{slide-element}
:class: hero-math
$$C\mathbf q=\mathbf r.$$
:::

::::::::{slide-columns}
:ratio: 1 1
:gap: 48
::::::{slide-column}
### $\mathbf r$ · Raw residual vector
Model predictions minus observations.
::::::
::::::{slide-column}
### $\mathbf q$ · Whitened residual vector
The unknown vector we solve for.
::::::
::::::::

For Gaussian errors with fixed $\Sigma$, the fit loss is ordinary squares in these coordinates.

$$\mathcal L=\tfrac12\lVert\mathbf q\rVert_2^2
=\tfrac12\sum_iq_i^2.$$

:::{slide-element}
:class: support
For fixed $\Sigma$, reuse $C$. Recompute $\mathbf r$ from each new model prediction, then solve for $\mathbf q$ again instead of constructing an inverse.
:::

:::{speaker-note}
- **Identify the known quantities:** $\Sigma$ is the stated measurement-error covariance. $C$ is its lower-triangular Cholesky factor, satisfying $\Sigma=CC^{\mathsf T}$. The raw residual vector $\mathbf r$ is model predictions minus observations at the current parameter candidate.
- **Identify the unknown:** $\mathbf q$ is the whitened residual vector. Solve $C\mathbf q=\mathbf r$ for $\mathbf q$; we are not fitting $C$ or the observed data in this step.
- **Read the repeated calculation:** Reuse $C$ while the covariance remains fixed. Every new model prediction changes $\mathbf r$, so solve for a new $\mathbf q$ at each candidate.
- **Explain the coordinates:** After whitening, each modeled error coordinate has variance one and different coordinates have zero correlation. For Gaussian errors this also gives independent components. Zero correlation alone would not imply independence for an arbitrary distribution.
- **Read the norm:** $\lVert\mathbf q\rVert_2$ is Euclidean length. Squaring it gives $\sum_iq_i^2$, so the loss is the ordinary half-sum of whitened squares.
- **Connect the special case:** Independent errors make $C$ diagonal and the solve becomes $q_i=r_i/\sigma_i$.
- **Check:** Whitening adds no observations and makes no extra covariance weighting necessary afterward. Solve rather than explicitly constructing an inverse.
- **Segue:** “Some observables need a different probability model entirely.”
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

:::{speaker-note}
- **Define the observable:** Photon or event counts are nonnegative integers. A Poisson model has a nonnegative mean $\mu$ that also specifies its variance.
- **Read the objective:** Omitting parameter-independent terms gives the sum of $\mu_i-n_i\log\mu_i$.
- **Explain the roles:** Counts $n_i$ are observed; means $\mu_i$ depend on the candidate model. The uncertainty model therefore differs from fixed-variance Gaussian errors.
- **Check zero correctly:** A zero observation contributes $\mu_i$ to this loss. A positive observed count requires a positive predicted mean.
- **Prompt:** “Should we automatically reuse Gaussian weights derived from each observed count?” That choice needs examination.
- **Segue:** “A small example makes the effect of those weights visible.”
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
**Neyman weighting** gives larger weights to smaller observed counts, including downward fluctuations. It is undefined at $n_i=0$, which is valid Poisson data.
:::

:::{speaker-note}
- **Name the separate example:** The counts $1,2,2,4,6$ share one unknown common mean. They are not the Gaussian fading dataset.
- **Read the Poisson result:** Its optimum is the arithmetic mean, three.
- **Explain the competing construction:** Neyman weighting minimizes squared mismatches divided by the observed counts. For these positive counts, its common-mean optimum is the harmonic mean, approximately $2.069$.
- **Predict the mechanism:** Smaller counts receive larger weights and pull this fitted mean downward.
- **Bound the claim:** This fixed example is not an ensemble study or a universal bias measured in standard errors. The Neyman expression is undefined for a zero count.
- **Name the comparison curve:** For positive counts, the plotted Neyman loss is $\mathcal L_N=\tfrac12\sum_i(\mu-n_i)^2/n_i$. It substitutes observed counts for noise variances. The figure subtracts each curve's own minimum for display; that shift does not change either minimizer.
- **Segue:** “Use a scalar calibration problem to understand derivatives and updates exactly.”
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

:::{speaker-note}
- **Announce the transition:** We have chosen a comparison using a measurement model. Now use one parameter to understand how an optimizer moves.
- **Name the separate example:** Here $\theta$ is a scalar dimensionless calibration parameter, not the fading fit's two-component parameter vector.
- **Read the ingredients:** Prediction $y=1+2\theta$, fixed observation $d=3$, and known measurement standard deviation $\sigma=0.5$.
- **Work the residual:** Subtract the datum and divide by its uncertainty to obtain $q=4(\theta-1)$.
- **Work the objective:** Half its square is $\mathcal L=8(\theta-1)^2$. It is minimized at $\theta=1$.
- **Check:** The uncertainty sets curvature even though this one-datum calibration's exact matching parameter is unchanged.
- **Segue:** “Before differentiating, distinguish the minimizing location from its loss value.”
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

:::{speaker-note}
- **Keep the current example:** This is the scalar calibration just derived, with $\mathcal L(\theta)=8(\theta-1)^2$. We have not changed the model or data.
- **Separate value and location:** The minimum is the smallest loss value, here zero. The argmin gives the parameter location or locations attaining it, here $\theta^*=1$.
- **Define the domain:** The feasible set contains allowed parameter values. Existence and uniqueness are properties of the problem, not guaranteed by an optimizer's return value.
- **Prompt:** “Does a returned point have to be the only equally good answer?” No. Later examples will show two minimizing locations and a flat direction.
- **Keep the inference bounded:** A fitted location is not a distribution over uncertain parameters.
- **Segue:** “Use the derivative to decide which direction improves this loss locally.”
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

:::{speaker-note}
- **Define the derivative:** $\mathcal L'(\theta)$ is the local change in loss per small change in this scalar coordinate. Here it is $16(\theta-1)$.
- **Read the tangent:** Left of one, the slope is negative, so a sufficiently small move right lowers the loss. Right of one, the sign reverses.
- **Prompt:** “Does a negative slope mean the descent update should be negative?” No. Subtracting a negative derivative moves the parameter upward.
- **Keep the limit visible:** A tangent describes local behavior. Extending its prediction over a large displacement can be misleading.
- **Segue:** “Several parameter slopes form a gradient vector.”
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

:::{speaker-note}
- **Define the entries:** Each component of $\mathbf g=\nabla\mathcal L$ is a partial derivative, changing one parameter while holding the others fixed.
- **Check the dimension:** Our fading fit has two gradient entries, despite having sixteen observations.
- **Read the interpretation:** In the chosen Euclidean coordinates, the gradient points toward steepest local increase per unit distance. The negative gradient is a local descent direction when nonzero.
- **Misconception:** “Steepest” depends on parameter scaling and the distance measure. It is not independent of coordinates.
- **Connect forward:** The bowl contours later in the deck will make those directional slopes visible.
- **Segue:** “A dot product tests a more general proposed direction.”
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

:::{speaker-note}
- **Define the dot product:** $\mathbf g^T\mathbf s$ adds the products of corresponding gradient and displacement components. Its result is a scalar predicted first-order change.
- **Read the local test:** A direction with $\mathbf g^T\mathbf s<0$ lowers a smooth objective for sufficiently small positive travel along that direction.
- **Prompt:** “Does a negative dot product guarantee the full proposed displacement is safe?” No. Curvature can defeat the local prediction over a long step.
- **Mention zero:** A zero gradient gives no first-order preference. It can occur at a minimum, maximum, saddle, or flat direction.
- **Segue:** “Build the gradient efficiently from the residual sensitivities.”
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

:::{speaker-note}
- **Return to the fading fit:** Our two optimized coordinates are $a=\log A$ and $b=\log\tau$. Thus $A=e^a$ and $\tau=e^b$ remain strictly positive at finite coordinates.
- **Define this Jacobian:** $J_{ij}=\partial q_i/\partial\theta_j$ differentiates standardized residuals. It has one row per observation and one column per parameter.
- **Pause for the shape:** Sixteen observations and two parameters give a $16\times2$ matrix. Each column is a pattern of residual responses across all observations.
- **Use the analytic example:** For $y=Ae^{-t/\tau}$, derivatives with respect to $a,b$ are $y$ and $yt/\tau$. Divide by $\sigma$ for residual derivatives.
- **Check:** The timescale derivative vanishes at zero time. Log coordinates do not create missing sensitivity.
- **Segue:** “Combine each sensitivity pattern with the present mismatch.”
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

:::{speaker-note}
- **Apply the chain rule:** For $\mathcal L=\tfrac12\mathbf q^T\mathbf q$, the gradient is $\mathbf g=\mathbf J^T\mathbf q$.
- **Check the matrix shapes:** The transpose is $2\times16$ and the residual vector has sixteen entries. Their product gives the two parameter derivatives.
- **Explain the sum:** Each parameter slope combines all data mismatches, weighted by how sensitively those residuals respond to that parameter.
- **Misconception:** Do not add another covariance weighting after defining both $\mathbf q$ and $\mathbf J$ in whitened coordinates.
- **Prompt:** A small parameter gradient does not require every individual residual to vanish.
- **Segue:** “Turn this gradient into a concrete update.”
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
### Step scale
$\eta>0$ scales the gradient. The step length is $\eta\lVert\mathbf g_k\rVert_2$.
::::::
::::::::

:::{slide-element}
:class: support
$k$ counts updates. Recompute the gradient after moving.
:::

:::{speaker-note}
- **Read the rule:** $\boldsymbol\theta_{k+1}=\boldsymbol\theta_k-\eta_k\mathbf g_k$. The index $k$ counts updates; positive $\eta_k$ controls the step length.
- **Separate two decisions:** The negative gradient supplies a direction. The learning rate controls travel along it.
- **Connect to descent:** For a nonzero gradient, its negative has a negative dot product with the gradient. A sufficiently short step lowers a smooth objective.
- **Check:** A correct direction can still overshoot with too large a learning rate.
- **Define terminology:** One iteration is one update. An epoch is a pass through a finite training dataset; they need not coincide.
- **Segue:** “Compute two updates without treating the optimizer as a black box.”
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

:::{speaker-note}
- **Fix the exercise:** Start the scalar calibration at $\theta_0=-1$ with learning rate $\eta=1/32$.
- **Work the first slope:** The derivative is $16(-1-1)=-32$. Subtracting $\eta$ times that derivative adds one, so $\theta_1=0$.
- **Read the loss decrease:** The loss changes from $32$ to $8$.
- **Work the second update:** At zero the derivative is $-16$, giving $\theta_2=0.5$ and loss two.
- **Prompt:** “Why have we not reached one exactly?” This chosen rate halves the parameter error each update; it does not eliminate it immediately.
- **Segue:** “Changing the step size can produce a different qualitative trajectory.”
:::

(opt-step-size)=
## Predict the effect of the step size

```{slide-options}
{"class": "optimization visual predict-figure"}
```

For the calibration loss, $e_k=\theta_k-1$ and $e_{k+1}=(1-16\eta)e_k$.

:::{slide-question}
:title: Predict
Try $\eta=0.03,\ 0.09,\ 0.125,\ 0.14$. When does the error alternate? When does its magnitude shrink?
:::

::::{slide-answer}
```{slide-figure} assets/gd-step-sizes.png
:alt: Parameter traces show monotone convergence, damped alternation, a persistent two-point cycle, and growing alternation.
```
The first two converge. At $\eta=0.125$ the parameter alternates with constant loss.
::::

:::{speaker-note}
- **Say.** All four runs use the same calibration loss, start at $\theta_0=-1$, and aim for $\theta^*=1$. The initial gradient is $-32$. The only change is the learning rate.
- **Ask.** Before showing the trajectories, use $\eta=0.03$, $0.09$, $0.125$, and $0.14$. What is the first update at each rate? For each result, did it cross the minimum, and is its distance from the minimum smaller, equal, or larger?
- **Wait.** Give pairs 45–60 seconds. Each pair can start with one of the rates and compare with a neighbor.
- **Reveal.** The first updates are $-0.04$, $1.88$, $3$, and $3.48$. The distances from one are $1.04$, $0.88$, $2$, and $2.48$, compared with the initial distance $2$. On this quadratic, the same multiplier applies at every update. Trace monotone convergence, damped oscillation, a two-point cycle, and growing oscillations in that order.
- **Misconception check.** The parameter can alternate sides while the loss falls. In the two-point cycle the parameter alternates and the loss stays constant, since both points are equally far from the minimum.
- **Segue.** Derive the error multiplier from the update rule. Use it to predict what is special about $\eta=1/16$ and $\eta=1/8$.
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

:::{speaker-note}
- **Define the error:** $e_k=\theta_k-1$. Substituting the calibration derivative gives $e_{k+1}=(1-16\eta)e_k$.
- **Read the criterion:** Error shrinks precisely when the multiplier's magnitude is below one. Solving $|1-16\eta|<1$ gives $0<\eta<1/8$.
- **Explain the sign:** A negative multiplier alternates the side of the minimum; its magnitude determines shrinking or growth.
- **Check the boundary:** At $1/8$, a nonzero starting error persists rather than converging.
- **State the scope:** The numerical threshold belongs to this loss and normalization. It is not a universal learning-rate recommendation.
- **Segue:** “The second derivative identifies the curvature behind that coefficient sixteen.”
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

:::{speaker-note}
- **Define the matrix:** The Hessian contains second partial derivatives of a scalar loss. It measures how gradient entries change when parameters change.
- **Check the shape:** With $p$ fitted parameters, the Hessian is $p\times p$. Sufficient smoothness makes the mixed derivatives symmetric.
- **Connect the scalar example:** The calibration's second derivative is sixteen everywhere, explaining its exact fixed-step stability limit.
- **Prompt:** “Does a zero first derivative identify the bowl's shape?” No. Curvature distinguishes some kinds of stationary points.
- **Avoid a misconception:** A Hessian describes local geometry; positive curvature at one point does not rule out another distant basin.
- **Segue:** “Use a two-direction bowl to see unequal curvatures.”
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

:::{speaker-note}
- **Read the controlled loss:** $\mathcal L=\tfrac12(e_1^2+50e_2^2)$, with parameter errors measured from the minimum. This is a separate quadratic teaching example.
- **Read the Hessian:** $\operatorname{diag}(1,50)$ means diagonal entries one and fifty, with zeros elsewhere. Cross-coordinate second derivatives are zero here.
- **Read the contours:** Each ellipse connects equal-loss points. The same displacement costs fifty times as much along $e_2$ as along $e_1$.
- **Connect the earlier definition:** Both directional curvatures are positive, so this Hessian is positive definite. The bowl has no flat or downward-curving direction.
- **Predict:** “Should one step size be equally convenient in both directions?” The steep direction will restrict the update.
- **Segue:** “Give these directional curvatures their linear-algebra names.”
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

:::{speaker-note}
- **Read the equation:** An eigenvector $\mathbf v\ne\mathbf0$ satisfies $H\mathbf v=\lambda\mathbf v$. Matrix multiplication leaves it on the same line; a negative eigenvalue would reverse its orientation.
- **Use the displayed directions:** For $H=\operatorname{diag}(1,50)$, the coordinate vectors have eigenvalues one and fifty.
- **Define unit direction:** A unit vector has length one. For a symmetric Hessian and unit eigenvector, $\mathbf v^{\mathsf T}H\mathbf v=\lambda$ is the directional curvature of the local quadratic.
- **Recall positive definite:** All eigenvalues of a real symmetric positive-definite matrix are positive. A zero eigenvalue permits a flat quadratic direction.
- **Prompt:** “Which direction changes slope faster?” The direction with eigenvalue fifty.
- **Segue:** “One gradient-descent step size must accommodate both curvatures.”
:::

(opt-conditioning)=
## One step size must serve both directions

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/conditioning-paths.png
:alt: Gradient descent zigzags in a narrow valley and converges slowly along its shallow direction.
```
$$e_{j,k+1}=(1-\eta\lambda_j)e_{j,k},
\qquad \kappa=\frac{\lambda_{\max}}{\lambda_{\min}}=50.$$

:::{slide-element}
:class: support
The steep direction forces $\eta<0.04$. In the shallow direction ($\lambda=1$), $1-\eta$ stays close to one.
:::

:::{speaker-note}
- **Say.** The two directions have curvatures one and fifty, so the condition number is $\kappa=50$. The scalar multiplier carries over to an eigenvector of curvature $\lambda$: its error is multiplied by $1-\eta\lambda$ each step.
- **Ask.** With $\eta=0.03$, compute the multipliers along the shallow and steep directions. Which direction crosses the minimum? Which keeps more of its old error?
- **Wait.** Give students about 30 seconds to calculate two numbers.
- **Reveal.** The multipliers are $0.97$ and $-0.50$. The shallow direction keeps 97 percent of its previous error on the same side. The steep direction halves its error and crosses the minimum. To shrink both directions we need $0<\eta<2/50=0.04$.
- **Read the plots.** The trajectory for $\eta=2/51$ shows zigzags across the valley. Here that optimal fixed rate gives both directions a contraction in magnitude of $49/51$ per update. The $0.03$ calculation was a separate prediction for the same bowl.
- **Misconception check.** Raising $\eta$ can speed shallow motion while making steep motion unstable. The rate limit depends on the actual curvature and coordinate scaling.
- **Segue.** Change the coordinates before trying to tune one rate for two very different directions.
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

:::{speaker-note}
- **Read the transformation:** Set $z_1=e_1$ and $z_2=\sqrt{50}\,e_2$. The same loss becomes $\tfrac12(z_1^2+z_2^2)$.
- **Explain the picture:** Elliptical and circular contours describe the same parameter problem in different coordinates. Predictions and available information have not changed.
- **Define preconditioning:** Change coordinates or step geometry to reduce numerical difficulty. This simple stretch balances the quadratic's directional curvatures.
- **Define nondimensionalization:** Express variables relative to fixed, meaningful physical reference scales. It gives deliberate units and numerical sizes; it is not always the same as curvature balancing.
- **Use the exact case:** A unit gradient-descent step solves this round quadratic in exact arithmetic. That is not a universal step-size choice.
- **Segue:** “Memory supplies another way to alter a first-order trajectory.”
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

:::{speaker-note}
- **Read the stored vector:** Heavy-ball momentum retains a fraction of the previous update and combines it with the current negative gradient.
- **Name it correctly:** This rule evaluates the gradient at the current point. Nesterov's look-ahead construction is related but different.
- **Explain the mechanism:** Alternating steep-direction motion can partly cancel while consistent shallow-direction motion accumulates.
- **Prompt:** “Does memory make any learning rate safe?” No. Momentum has its own stability conditions; the earlier bound applied specifically to ordinary gradient descent.
- **Qualify the comparison:** The plotted settings are tuned for this positive-definite quadratic. Favorable acceleration is not unconditional on a nonconvex model.
- **Segue:** “Curvature can also determine a step directly.”
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

:::{speaker-note}
- **Read the approximation:** The local quadratic combines current loss, the linear term $\mathbf g^T\mathbf s$, and curvature $\tfrac12\mathbf s^T\mathbf H\mathbf s$.
- **Define the displacement:** $\mathbf s$ describes a proposed change, rather than the final parameter vector.
- **Interpret the terms:** The gradient gives the tangent; the Hessian adds how the slope itself varies.
- **Prompt:** “When would this approximation coincide with the whole objective?” For a quadratic loss with its exact derivatives.
- **Give the caveat:** A quadratic stationary point need not minimize that local model if its curvature is not positive definite.
- **Segue:** “Set the local model's gradient to zero and solve the resulting system.”
:::

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

:::{speaker-note}
- **Read the solve:** $\mathbf H\mathbf s=-\mathbf g$, followed by $\boldsymbol\theta_{\mathrm{new}}=\boldsymbol\theta+\mathbf s$.
- **Implementation cue:** Solve the linear system rather than explicitly forming an inverse. Dense factorization and derivative construction have their own costs.
- **State the exact result:** A positive-definite quadratic reaches its unique minimum in one full Newton step with exact arithmetic and an exact solve.
- **Qualify nonlinear behavior:** Near a sufficiently regular nondegenerate minimum, Newton can converge quadratically: the next error scales like the current error squared.
- **Prompt:** “Does that local result make every starting point safe?” No.
- **Segue:** “Inspect the kind of stationary point the method is approaching.”
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

:::{speaker-note}
- **Read the example:** For $x^4-2x^2$, stationary points occur at zero and at plus or minus one. Stationary means the gradient is zero.
- **Classify the displayed points:** Zero is a local maximum. Plus and minus one are equal global minima of this quartic. The minimum value is minus one, but there are two minimizing locations.
- **Define saddle separately:** In several dimensions, a saddle has nearby rising and falling directions. This one-dimensional plot does not display one.
- **Prompt:** “What happens if ordinary gradient descent starts exactly at zero?” The gradient vanishes, so the update does not move.
- **State the lesson:** A small-gradient stopping flag does not classify the stationary point.
- **Segue:** “Newton can actively move toward that unwanted maximum.”
:::

(opt-newton-failure)=
## Negative curvature can send Newton uphill

```{slide-options}
{"class": "optimization visual predict-figure"}
```

For $\mathcal L(x)=x^4-2x^2$ at $x=0.25$, both the slope and curvature are negative.

:::{slide-question}
:title: Predict
Which way does $s=-g/H$ point? Is that a descent direction?
:::

::::{slide-answer}
```{slide-figure} assets/newton-failure.png
:alt: A Newton trial from x equals one quarter increases the quartic loss and moves toward its maximum.
```
$$x:0.25\longrightarrow-0.0385,
\qquad \mathcal L:-0.1211\longrightarrow-0.0030.$$
::::

:::{speaker-note}
- **Say.** Keep the quartic $\mathcal L=x^4-2x^2$ and start at $x=0.25$. The slope is $g=-0.9375$ and the curvature is $H=-3.25$.
- **Ask.** Which way is locally downhill? Which way does the equation $Hs=-g$ send the Newton step? Vote left or right separately for the two questions before showing the trial.
- **Wait.** Give pairs 45–60 seconds. Ask them to justify their votes with the sign of $g$ and the sign of $H$.
- **Reveal.** A small move to the right lowers the actual loss. Newton instead moves left by about $0.28846$ to $x\approx-0.03846$. The actual loss rises from $-0.1211$ to $-0.0030$. Follow the dashed local quadratic to its stationary point. It is a maximum because the curvature is negative.
- **Misconception check.** Solving the linear system accurately can produce an uphill direction. Here $gs>0$, so shortening the step preserves its uphill first-order sign. In several dimensions, indefinite curvature can cause a related failure.
- **Segue.** Check the direction before choosing how far to travel, then evaluate the actual result.
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

:::{speaker-note}
- **Check direction first:** Standard descent backtracking requires $\mathbf g^T\mathbf s<0$. Merely shortening an uphill direction does not repair its sign.
- **Read Armijo:** With $0<c<1$ and positive step length $\alpha$, require

$$
\begin{aligned}
\mathcal L(\boldsymbol\theta+\alpha\mathbf s)
&\le \mathcal L(\boldsymbol\theta)\\
&\quad+c\alpha\,\mathbf g^T\mathbf s.
\end{aligned}
$$

- **Explain the alternative:** A trust region limits the displacement to a neighborhood where the local model is useful. Actual versus predicted improvement informs the next radius.
- **Prompt:** A rejected trial leaves the current parameters unchanged.
- **Segue:** “Least-squares residual structure supplies a useful curvature model.”
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
Square the predicted residuals to get the local loss model $m(\mathbf s)=\tfrac12\lVert\mathbf q+J\mathbf s\rVert_2^2$.
:::

:::{speaker-note}
- **Say.** Keep the squared-residual objective. At the current parameters, approximate the new standardized residual vector by $\mathbf q+J\mathbf s$. This gives the local loss model $m_{\rm GN}(\mathbf s)=\tfrac12\lVert\mathbf q+J\mathbf s\rVert_2^2$.
- **Ask.** With $\mathbf s=\mathbf 0$, what objective value do we get? Which term in the expanded square gives the slope at zero?
- **Reveal.** The model has current value $\tfrac12\lVert\mathbf q\rVert^2$, linear term $(J^{\mathsf T}\mathbf q)^{\mathsf T}\mathbf s$, and quadratic term $\tfrac12\mathbf s^{\mathsf T}J^{\mathsf T}J\mathbf s$. The slope at the current point is the same as the full least-squares gradient.
- **Check.** Affine residual functions make the linearization exact. With nonlinear residuals, test the proposed step on the actual loss. Our prediction-minus-data sign convention gives the target $J\mathbf s\approx-\mathbf q$.
- **Segue.** Compare this curvature model with the full Hessian.
:::

(opt-gn-curvature)=
## The Jacobian gives approximate loss curvature

```{slide-options}
{"class": "optimization"}
```

:::{slide-element}
:class: hero-math
$$\mathbf g=J^{\mathsf T}\mathbf q,
\qquad H_{\mathrm{GN}}=J^{\mathsf T}J.$$
:::

$$\mathbf v^{\mathsf T}H_{\mathrm{GN}}\mathbf v=\lVert J\mathbf v\rVert_2^2\ge0.$$

**Positive semidefinite:** curvature is never negative, but flat directions can remain.

:::{slide-element}
:class: support
The approximation omits the curvature of individual residual functions. Evaluate the actual loss before accepting a nonlinear trial.
:::

:::{speaker-note}
- **Read the approximation:** Gauss–Newton uses $H_{\mathrm{GN}}=J^{\mathsf T}J$. The full Hessian also contains $\sum_iq_i\nabla^2q_i$, curvature of the individual residual functions.
- **Prove the sign:** For any $\mathbf v$, the quadratic form is $\mathbf v^{\mathsf T}J^{\mathsf T}J\mathbf v=\lVert J\mathbf v\rVert_2^2\ge0$.
- **Recall the contrast:** Positive semidefinite allows equality for a nonzero direction; positive definite requires strict positivity. Nonnegative curvature does not imply an invertible matrix.
- **Qualify the approximation:** Small residuals with controlled smooth curvature can make the omitted term small. Nonzero residuals do not generically give quadratic convergence.
- **Check:** Positive curvature alone establishes neither approximation accuracy nor acceptance of a full nonlinear step.
- **Segue:** “Ask whether the sensitivity columns leave any direction invisible.”
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

:::{speaker-note}
- **Recall the columns:** Each Jacobian column describes how all residuals respond to one parameter. A combined parameter change $\mathbf v$ produces linearized change $J\mathbf v$.
- **Read a hidden direction:** If $J\mathbf v=\mathbf0$ for a nonzero $\mathbf v$, parameter responses cancel across every residual. The local linearized problem cannot distinguish that change.
- **Define rank:** Rank counts independent columns. Full column rank means all parameter columns are independent, so only $\mathbf v=\mathbf0$ satisfies this equation.
- **Connect curvature:** Then $\lVert J\mathbf v\rVert^2>0$ for nonzero $\mathbf v$, making $J^{\mathsf T}J$ positive definite. A nonzero gradient yields a Gauss–Newton descent direction.
- **Qualify:** This is local. Full rank alone proves neither global uniqueness nor precise parameter determination; the actual trial still needs checking.
- **Segue:** “Solve the linearized residual problem directly.”
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

:::{speaker-note}
- **Read the target:** Find a displacement minimizing $\tfrac12\lVert\mathbf q+J\mathbf s\rVert^2$. The sign follows our prediction-minus-data residual convention: $J\mathbf s\approx-\mathbf q$.
- **Read the code:** The least-squares solver factors the residual matrix directly instead of explicitly constructing its normal matrix.
- **Define normal equations:** Differentiating this linearized objective gives $J^{\mathsf T}J\mathbf s=-J^{\mathsf T}\mathbf q$. For full column rank, forming that product squares the 2-norm condition number.
- **Optional methods:** QR uses orthonormal columns and a triangular factor. Singular-value decomposition exposes response directions and stretch factors, including weak or zero directions.
- **Qualify:** A minimum-norm numerical step can be returned under rank deficiency; this does not make every parameter identifiable. A transpose is not an inverse physical model.
- **Segue:** “Damping changes the proposal when a conservative step is useful.”
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

:::{speaker-note}
- **Read the system:** $(J^{\mathsf T}J+\nu I)\mathbf s=-\mathbf g$, with positive damping $\nu$ in our chosen log coordinates. The identity matrix satisfies $I\mathbf v=\mathbf v$.
- **Connect positive definite:** Adding $\nu I$ adds strictly positive curvature in every direction, even if $J^{\mathsf T}J$ has a flat direction. This gives a well-defined linear solve, not guaranteed nonlinear improvement.
- **Read the limits:** Large damping approaches a short negative-gradient proposal. Small damping approaches Gauss–Newton when that limit is well defined.
- **Implementation cue:** One can solve the augmented least-squares system stacking $J$ above $\sqrt\nu I$, with right-hand side $-\mathbf q$ followed by zeros.
- **Misconception:** Adaptive damping regulates the trial step; it is not automatically a prior on the final parameters.
- **Segue:** “Compare different damping choices from one point.”
:::

(opt-lm-damping)=
## Compare proposals from the same point

```{slide-options}
{"class": "optimization visual predict-figure"}
```

:::{slide-question}
:title: Predict
For $\nu=1,\ 100,\ 1000$, which proposal should move least? What measurement decides whether a trial is accepted?
:::

::::{slide-answer}
```{slide-figure} assets/lm-damping.png
:alt: Three log-parameter proposals from the same starting point use damping one, one hundred, and one thousand. Their actual losses decide acceptance.
```
::::

:::{speaker-note}
- **Say.** Every arrow starts at the same log-parameter point, corresponding to $A=\tau=0.7$. The values $\nu=1$, $100$, and $1000$ give three alternative proposals from that one start.
- **Ask.** Which damping value should produce the shortest step? What comparison decides acceptance?
- **Wait.** Give pairs 30 seconds to predict before revealing the figure.
- **Reveal.** Compare each bar with the dashed initial-loss line. The $\nu=1$ proposal raises the loss. The other two lower it. Among these three trials, $\nu=100$ gives the lowest actual loss.
- **Misconception check.** Damping changes direction as well as step size. The shortest arrow is the most conservative one here. It gives less improvement than the middle trial, and the actual adaptive run uses a different sequence of damping values.
- **Segue.** Follow the actual adaptive run one attempt at a time.
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

:::{speaker-note}
- **Say.** The left staircase tracks the loss at the current accepted parameters. Points mark the attempted trial losses. The right panel shows the damping used on each attempt.
- **Ask.** Track attempts 3 and 4. Does the state move after attempt 3? Which damping is used on attempt 4, and what happens to the loss then?
- **Reveal.** Attempt 3 uses $\nu=25$ and is rejected. Attempt 4 uses $\nu=125$ and is accepted. Under this demonstration's rule, a rejection multiplies damping by five for the next attempt. An acceptance reduces it by a factor of three.
- **Count.** There are eleven trial attempts, with eight accepted and three rejected. The initial state is the starting point. Each rejection still uses a model evaluation.
- **Misconception check.** Heavy damping can produce a short step even with a substantial gradient. Read the stopping reason and check the gradient or an appropriate optimality measure.
- **Segue.** Inspect the fitted prediction and the residuals after the algorithm stops.
:::

(opt-fit)=
## Does the fitted curve explain the data?

```{slide-options}
{"class": "optimization visual"}
```

```{slide-figure} assets/fit-result.png
:alt: The fitted exponential and generating curve appear beside standardized residuals. At time two the residual is about plus 2.5, outside the band marking one measurement standard deviation.
```
:::{slide-question}
:title: Inspect
At $t=2$, is the prediction high or low, and by how many measurement standard deviations? What pattern would make you question the model?
:::

:::{speaker-note}
- **Say.** The executed synthetic fit gives $A\approx1.7933$ and $\tau\approx2.4191$. The generating values are $1.8$ and $2.4$, known because we constructed this dataset. Measurement noise can shift the fitted values.
- **Ask.** At $t\approx2$, did the model overpredict or underpredict the measurement? By roughly how many measurement standard deviations? What pattern across times would make you suspect a problem with the model?
- **Wait.** Give pairs about 30 seconds to read the sign and scale and to name one pattern.
- **Reveal.** The residual there is positive, about $+2.5$ in measurement standard-deviation units, so the model overpredicts. A sustained run of residuals on one side or a trend over time would motivate checking the model or noise assumptions. One visibly large residual is limited evidence on its own.
- **Misconception check.** The shaded region marks $|q_i|\le1$. It guides reading of the measurement-residual scale. An uncertainty band for the fit would require a separate calculation.
- **Optional notebook diagnostics.** The final loss is about $6.7887$. The notebook records the stop reason and gradient. Use those to check the algorithm and the plot to check the residual pattern.
- **Segue.** Ask what the observing times let us learn about both fitted parameters.
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
:::{slide-question}
:title: Choose the next measurement
You already measured $A$. Which gives new information about $\tau$: 100 more observations at $t=0$, or one at $t>0$?
:::

:::{speaker-note}
- **Say.** Identifiability asks which changes in the parameters produce distinguishable predictions. Keep the exponential fading model $y(t)=A e^{-t/\tau}$.
- **Ask.** If we have measurements at $t=0$ already, which additional observation teaches us about $\tau$: one hundred more measurements at zero or one measurement at a well-chosen later time? Ask students to justify their choice from the formula.
- **Wait.** Give students 45–60 seconds to substitute $t=0$ and name which Jacobian column vanishes.
- **Reveal.** At zero, $y=A$ for every $\tau$. The timescale sensitivity column is zero, so the left plot is flat along log timescale. At a positive time, changing $\tau$ changes the prediction. In this example the time-spanning design has two independent sensitivity directions.
- **Misconception check.** More measurements at zero can improve the estimate of $A$. They leave the timescale flat direction intact. Local full rank says a small change can affect predictions. Precision also depends on noise and the strength of the responses, and global uniqueness takes a separate argument.
- **Segue.** A penalty may select among weakly constrained answers. State what preference it introduces.
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

:::{speaker-note}
- **Name the separate illustration:** The plotted scalar coordinate is $z$. This is not another fit of the fading dataset.
- **Read the three curves:** The data term is $\tfrac12(z-2)^2$, minimized at two. The penalty is $\tfrac12z^2$, centered at zero. Their sum is minimized at one.
- **Prompt:** “Did the optimizer fail by returning a different value?” No. The objective changed, so the question being answered changed.
- **Explain the role:** A penalty can stabilize a weakly determined direction by adding a preference. It does not make the original observations more informative.
- **Segue:** “When the data term is a negative log-likelihood, this preference can be written as a prior.”
:::

(opt-map)=
## A Gaussian prior gives a quadratic penalty

```{slide-options}
{"class": "optimization"}
```

In the chosen coordinates, a prior $\boldsymbol\theta\sim\mathcal N(\boldsymbol\theta_0,I/\lambda)$ adds a penalty to the negative log-likelihood, up to a constant.

:::{slide-element}
:class: hero-math
$$\frac{\lambda}{2}\lVert\boldsymbol\theta-\boldsymbol\theta_0\rVert_2^2.$$
:::

**MAP:** maximum a posteriori, the location maximizing posterior density.

**Prior:** parameter density before conditioning on data. **Posterior:** after conditioning.

:::{slide-element}
:class: support
$\boldsymbol\theta_0$ is the prior center and $\lambda>0$ sets its strength. LM damping penalizes the trial step $\mathbf s$ in the local model.
:::

:::{speaker-note}
- **Say.** A Gaussian prior $\boldsymbol\theta\sim\mathcal N(\boldsymbol\theta_0,I/\lambda)$ contributes $\tfrac\lambda2\lVert\boldsymbol\theta-\boldsymbol\theta_0\rVert^2$ to the negative log-posterior, up to a constant. This assumes the data term is the negative log-likelihood and $\lambda>0$.
- **Define.** The prior is the parameter distribution before conditioning. The posterior combines it with the likelihood under the statistical model. MAP selects a mode of that posterior density.
- **Ask.** Which expression penalizes a proposed move from the current point? Which penalizes a candidate's distance from a fixed reference value?
- **Reveal.** LM adds $\tfrac\nu2\lVert\mathbf s\rVert^2$ to the current step model. The Gaussian prior adds $\tfrac\lambda2\lVert\boldsymbol\theta-\boldsymbol\theta_0\rVert^2$ to the fitting objective. The prior can change the fitted answer. The LM damping can change which steps are proposed for that objective.
- **Misconception check.** A Gaussian prior on $\log A$ implies a different distribution on $A$. Transforming a parameter density uses a Jacobian factor, and the location maximizing its density depends on the chosen coordinates. A MAP location alone gives no posterior spread.
- **Segue.** A constraint determines which values are feasible.
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
The predictions and likelihood agree at corresponding values. State which coordinates you use for any prior.
:::

:::{speaker-note}
- **Recall the earlier choice:** $A=e^a$ and $\tau=e^b$ enforce the strictly positive domain of our fading model. Corresponding coordinates give the same predictions and the same loss value.
- **Explain the search:** The optimizer can vary unconstrained log coordinates without crossing the physical zero boundary. The parameter-space gradient and step geometry still change.
- **Distinguish density transformations:** Rewriting the optimization coordinates adds no likelihood density-Jacobian term: likelihood is still a density in the fixed data. Transforming a parameter probability density is a different operation and does require its measure factor.
- **Computational caveat:** Extreme exponentials can overflow or underflow in floating-point arithmetic. Finite-value checks still matter.
- **Prompt and segue:** “Can finite log coordinates represent an exactly zero physical parameter?” No. “Consider a separate background parameter whose zero boundary is valid.”
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

:::{speaker-note}
- **Define the new example:** $B$ is a separate nonnegative background parameter. It is not an additional parameter in our two-parameter fading fit.
- **Read the boundary:** A valid optimum may lie at $B=0$. The transformation $B=\exp(z)$ cannot reach it at finite $z$.
- **Explain the stopping trap:** The transformed derivative can become small as $B$ approaches zero, even while the physical-coordinate derivative is substantial.
- **Describe projection:** For this simple lower bound, project an update using $B\leftarrow\max(0,B)$. General constraints require their own projection or constrained method.
- **Prompt:** A small transformed gradient alone is not proof of constrained optimality.
- **Segue:** “Choose algorithms from the problem's actual structure.”
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

:::{speaker-note}
- **Start with structure:** Smooth residual least squares suggests Gauss–Newton or LM with safeguards. A smooth general loss can suit a quasi-Newton method, estimating curvature from parameter and gradient changes.
- **Name without another derivation:** BFGS is one such method; limited-memory BFGS keeps a bounded recent history rather than a dense curvature matrix.
- **Define stochastic gradients:** Estimates from randomly selected data subsets can vary between evaluations. Noise already present in our fixed measurements does not make its full-data gradient stochastic.
- **Define Adam:** Adaptive moment estimation uses running averages of gradients and squared gradients to scale updates. Momentum retains prior motion. Neither is universally best or guaranteed to steady every trajectory.
- **Compare fairly:** Without usable derivatives, consider derivative-free methods and evaluation cost. Judge achieved solution quality and computation, not iteration count alone.
- **Segue:** “End with checks that survive the algorithm choice.”
:::

(opt-checklist)=
## What would you check before trusting the fit?

```{slide-options}
{"class": "optimization"}
```

:::{slide-question}
:title: Exit check
The gradient is small. Give one check each for the solver, the physical model, and what the data can tell you.
:::

::::::::::{slide-answer}
::::::::{slide-columns}
:ratio: 1 1 1
::::::{slide-column}
### Solver
Read the stop reason. Check the derivatives.
::::::
::::::{slide-column}
### Physical model
Inspect residuals for patterns.
::::::
::::::{slide-column}
### Inference
Check whether the data constrain the parameters.
::::::
::::::::
::::::::::

:::{speaker-note}
- **Ask.** “The optimizer stopped with a small gradient. What one check would you make on the algorithm, one on the physical or measurement model, and one on inference? Say what each check could reveal.”
- **Wait.** Give students 60 seconds to think, or to compare with a neighbor. Invite a different answer for each category.
- **Reveal.** Read the stop reason and verify a derivative or actual loss change. Inspect residuals against time and check a physical assumption or a prediction beyond the fitted data. Ask which parameter changes the data can distinguish and what separate calculation would quantify uncertainty.
- **Misconception check.** A small gradient measures local change in the chosen coordinates. Robust scientific interpretation also needs evidence that the model is adequate and the observations constrain the claim.
- **Connect forward.** Try the same checks on the paired optimization exercise or use one to prepare for the Final Project.
:::
