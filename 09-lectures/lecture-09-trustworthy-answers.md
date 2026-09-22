---
title: "Lecture 9 · Trustworthy Numerical Answers"
subtitle: "Week 5 · September 22, 2026"
site:
  hide_toc: true
  hide_outline: true
---

:::{lecture-controls}
:id: lecture-09-controls
:::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## When should we trust a numerical answer?

**Last time:** build a root finder and explain its stopping rule.

**Today:** **propose → test → accept or revise → verify**.

We will connect each advanced method to the problem it helps solve.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Recall · what does “small” mean?

- **Residual magnitude:** $|f(x_n)|$ measures equation mismatch; a signed residual keeps the sign.
- **Update:** $s_n=|x_n-x_{n-1}|$ measures the last move.
- **Bracket:** a valid $[a_n,b_n]$ containing $x_*$ bounds midpoint error:

$$
m_n=\frac{a_n+b_n}{2},\qquad |m_n-x_*|\leq\frac{b_n-a_n}{2}.
$$

:::{div}
:class: lecture-prompt

**Pair prompt:** which assumptions turn each observation into evidence?
:::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Why go beyond the basic methods?

The basic methods show how approximation, iteration, and stopping work.

Advanced methods become useful when:

- A fast local step is unreliable from your starting guess.
- Each function evaluation is expensive.
- You fit many observations with a few parameters.
- An integrand has structure that uniform sampling resolves inefficiently.

**Goal:** recognize the problem, choose a method, and check its answer.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Ask what information the problem gives you

| What you have | What it enables |
|:--|:--|
| A continuous function and opposite endpoint signs | Bracket-based root control |
| Slopes or a local linear approximation | Fast trial steps |
| Predictions and observations | A least-squares objective |
| A callable integrand | Choosing new sample locations |

:::{div}
:class: lecture-prompt

**Discuss:** if you only have fixed sampled data, can you freely choose Gaussian nodes?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## A local model of $f(x)$ proposes a step

The tangent line near $x_n$ is our **local model** of $f(x)$:

$$
\ell_n(x)=f(x_n)+f'(x_n)(x-x_n),\qquad \ell_n(x_{\rm trial})=0.
$$

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-newton-proposal.svg
:class: tangent-model-figure
:alt: Arctangent curve and tangent at x equals two. The tangent root is near minus 3.536, far from the true root at zero.
:::

:::{div}
:class: lecture-prompt

**Predict:** Newton proposes the line’s zero. Will this step reduce $|f(x)|$?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Separate direction from distance

$$
p=-\frac{f(x)}{f'(x)},\qquad x_{\rm trial}=x+\alpha p.
$$

- **Direction:** Newton supplies $p$.
- **Step length:** a line search chooses $\alpha$.

**Trial rule:** try the full step; shorten it if the acceptance test fails.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Define progress before accepting a step

Use a residual objective: $\phi(x)=\tfrac12 f(x)^2$.

For an exact Newton direction at a nonroot,

$$
\phi'(x)p=-f(x)^2<0.
$$

A short enough step decreases this objective under the differentiability assumptions. A full step may not.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## A half-step can be more useful

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-backtracking.svg
:alt: Residual merit along the Newton direction, with full step rejected and half-step accepted by the sufficient-decrease threshold.
:::

:::{div}
:class: lecture-prompt

**Explain:** acceptance is progress. What would establish convergence?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Demonstration · compare the trial steps

For $f(x)=\arctan x$ at $x=2$, the initial residual magnitude is $1.107$.

| Step fraction $\alpha$ | Trial input | Residual magnitude | Sufficient decrease? |
|:--|:--|:--|:--|
| $1$ | $-3.536$ | $1.295$ | No |
| $1/2$ | $-0.768$ | $0.655$ | Yes |
| $1/4$ | $0.616$ | $0.552$ | Yes |

Backtracking accepts the **first** passing trial. It need not find the best step.

:::{div}
:class: lecture-prompt

**Explain:** why is acceptance not convergence?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## When is a line search useful?

- **Use when:** a local direction is promising but the full step overshoots.
- **Example:** nonlinear calibration from an uncertain starting guess.
- **Check:** actual objective decrease, not just the tangent’s prediction.
- **Cost:** rejected trials require extra evaluations.
- **Limit:** shorter steps cannot create a root. Check the domain, residual, and stopping conditions.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## A bracket gives a different kind of protection



:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-bracket-safeguard.svg
:alt: Arctangent with a verified bracket from minus one to two. The Newton proposal from two lies outside the bracket; the midpoint one half is an available fallback.
:::

:::{div}
:class: lecture-prompt

**Predict:** which endpoint should be replaced after evaluating $f(0.5)>0$?
:::

Keep opposite signs. A fallback bisection step reduces the bracket width.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Safeguarded methods · fast proposals, controlled progress

Use a hybrid method when you have a valid bracket and want faster progress than bisection alone.

1. Propose a fast step using local information.
2. Check that it is safe and makes adequate progress.
3. Otherwise, take a bracket-reducing step.

Brent-type methods combine interpolation and bisection; the preceding tangent example illustrates the safeguard idea, not Brent’s exact algorithm.

Continuity and reliable signs still matter.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## From roots to fitting data

A residual is prediction minus observation: $r_i(\theta)=g(t_i;\theta)-y_i$.

Choose parameters $\theta$ to reduce $\Phi(\theta)=\tfrac12\sum_i r_i(\theta)^2$.

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-fit-residuals.svg
:class: lm-overview-figure
:alt: Illustrative observations and a candidate exponential curve. Vertical segments show prediction minus observation; changing curve parameters changes all residuals.
:::

Noisy observations generally cannot all have zero residual.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## The Jacobian · one slope for each input–output pair

Let $r(\theta)$ have $m$ outputs and $\theta$ have $n$ parameters.

$$
J(\theta)=\begin{bmatrix}
\dfrac{\partial r_1}{\partial\theta_1}&\cdots&\dfrac{\partial r_1}{\partial\theta_n}\\
\vdots&\ddots&\vdots\\
\dfrac{\partial r_m}{\partial\theta_1}&\cdots&\dfrac{\partial r_m}{\partial\theta_n}
\end{bmatrix}\in\mathbb R^{m\times n}.
$$

- **Row:** one output’s sensitivity to all parameters.
- **Column:** all outputs’ sensitivity to one parameter.

A partial derivative changes one parameter while holding the others fixed.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## The matrix is a local input–output map

For a small parameter update $p$,

$$
r(\theta+p)\approx r(\theta)+J(\theta)p.
$$

The dimensions tell us what this means:

$$
\underbrace{J}_{m\times n}\;\underbrace{p}_{n\times1}=\underbrace{\Delta r_{\rm predicted}}_{m\times1}.
$$

Component by component: $\Delta r_i\approx\sum_j J_{ij}p_j$.

Each entry has units “output $i$ per unit of parameter $j$.”

:::{div}
:class: lecture-prompt

**Predict:** is the Jacobian necessarily square?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Example · three observations, two parameters

Fit $g(t;A,k)=Ae^{-kt}$ to fixed observations $y_i$ at $t=0,1,2$.

For $r_i=Ae^{-kt_i}-y_i$,

$$
\frac{\partial r_i}{\partial A}=e^{-kt_i},\qquad
\frac{\partial r_i}{\partial k}=-At_i e^{-kt_i}.
$$

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Evaluate the slopes at the current parameters

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

At $A=2$, $k=\ln2$, and $t=0,1,2$:

$$
J=\begin{bmatrix}1&0\\1/2&-1\\1/4&-1\end{bmatrix}
$$

Inputs are scaled and dimensionless.
:::::

:::::{div}
:class: lecture-column

**Rows:** observation times $t=0,1,2$.

**Columns:** parameters $A$ and $k$.

:::{div}
:class: lecture-prompt

**Explain:** why is the top-right entry zero?
:::
:::::
::::::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Use the Jacobian to predict a change

Increase $A$ by $0.10$ and $k$ by $0.02$:

$$
p=\begin{bmatrix}0.10\\0.02\end{bmatrix},\qquad
Jp=\begin{bmatrix}1&0\\1/2&-1\\1/4&-1\end{bmatrix}
\begin{bmatrix}0.10\\0.02\end{bmatrix}
=\begin{bmatrix}0.10\\0.03\\0.005\end{bmatrix}.
$$

These are predicted **changes in residuals**, not the residuals themselves.

Increasing amplitude raises the curve; increasing decay rate lowers later values. The effects partly cancel.

:::{div}
:class: lecture-prompt

**Check:** compare $r(\theta+p)-r(\theta)$ with $Jp$, then reduce the step.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Check the local prediction against the actual change

For $p=(0.10,0.02)$, evaluate the exponential again:

| Time | Predicted $Jp$ | Actual change |
|:--|--:|--:|
| $0$ | $0.100000$ | $0.100000$ |
| $1$ | $0.030000$ | $0.029209$ |
| $2$ | $0.005000$ | $0.004414$ |

For $0.1p$, the largest discrepancy falls from $7.91\times10^{-4}$ to $7.99\times10^{-6}$: about $99\times$ smaller.

:::{div}
:class: lecture-prompt

**Explain:** why does shrinking the step improve this linear prediction?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Read the least-squares notation

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

**Transpose** exchanges rows and columns:

$$
r^{\mathsf T}=[r_1,\ldots,r_m].
$$

**Squared norm** adds squared entries:

$$
\lVert r\rVert^2=r^{\mathsf T}r=\sum_i r_i^2.
$$
:::::

:::::{div}
:class: lecture-column

**Gradient:** $\nabla_\theta\Phi$ has one loss derivative per parameter.

**Nonsingular:** a square matrix for which every right-hand side has exactly one solution.

$J$ describes separate outputs; $\nabla\Phi$ describes one scalar loss.
:::::
::::::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## DS/ML · from many outputs to one loss

For least-squares loss $\Phi(\theta)=\tfrac12 r(\theta)^{\mathsf T}r(\theta)$,

$$
\nabla_\theta\Phi=J^{\mathsf T}r.
$$

The Jacobian describes how parameters affect predictions; the loss gradient combines those effects into one direction of change.

**Where it appears:** nonlinear regression, calibration, and sensitivity of model predictions.

Backpropagation applies the chain rule through a model. It can compute products such as $J^{\mathsf T}r$ without storing the full Jacobian.

This connection does not mean neural networks are usually trained with Levenberg–Marquardt.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Computational science · coupled equations

A steady state or implicit time step can require solving $F(u)=0$ for many unknowns.

Linearize the coupled equations:

$$
F(u+p)\approx F(u)+J_F(u)p.
$$

For a square, nonsingular Jacobian, Newton’s proposal solves

$$
J_F(u)p=-F(u).
$$

**Examples:** chemical equilibrium and coupled transport equations. Inverse problems instead often fit observations by minimizing a loss.

The Jacobian shows which variables affect which equations. Weak or dependent sensitivities can make the solve difficult.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Gauss–Newton · fit the local residual model

For a root, Newton sets a local approximation to zero.

For a fit, Gauss–Newton minimizes its squared mismatch:

$$
\underset{p}{\operatorname{minimize}}\;\tfrac12\lVert r+Jp\rVert^2.
$$

At a minimizer, $J^{\mathsf T}Jp=-J^{\mathsf T}r$.

A local fit can propose a large step where the approximation is poor.

:::{div}
:class: lecture-prompt

**Next question:** can we discourage such large steps?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Derive a penalty on the proposed step

**1. Define** the penalized local fit in scaled parameters:

$$
q_\lambda(p)=\tfrac12\lVert r+Jp\rVert^2+\tfrac\lambda2\lVert p\rVert^2.
$$

**2. Differentiate** with respect to the update $p$:

$$
\nabla_pq_\lambda=J^{\mathsf T}(r+Jp)+\lambda p.
$$

**3. Solve** where the gradient is zero:

$$
(J^{\mathsf T}J+\lambda I)p=-J^{\mathsf T}r.
$$

The penalty limits the **current step**; it does not require parameters near zero.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Levenberg–Marquardt · damp the local fit

**Local model:** $r(\theta+p)\approx r(\theta)+Jp$.

**Levenberg step:**

$$
(J^{\mathsf T}J+\lambda I)p=-J^{\mathsf T}r,\qquad \theta_{\rm trial}=\theta+p.
$$

::::::{div}
:class: lecture-two-column

:::::{div}
:class: lecture-column

- **Jacobian:** $J_{ij}=\partial r_i/\partial\theta_j$.
- **Update:** $p$ changes the parameters.
:::::

:::::{div}
:class: lecture-column

- **Damping:** $\lambda>0$ controls the penalty.
- **Identity:** $I$ leaves a vector unchanged.
:::::
::::::

Marquardt variants add scaling.

**Accept only after checking:** evaluate the actual fit improvement.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Read the contour plot before comparing steps

::::::{div}
:class: lecture-two-column lecture-figure-columns

:::::{div}
:class: lecture-column

**Contours:** equal local squared mismatch.

$$
q(p)=\tfrac12\lVert r+Jp\rVert^2
$$

**Cross:** the local-model minimum.

**Arrows:** alternative damping choices from the same starting point, not successive iterations.
:::::

:::::{div}
:class: lecture-column

:::{figure} figures/l9-levenberg-damping-columns.svg
:alt: Contours of equal local squared mismatch. A cross marks the local-model minimum; four arrows start at zero and show alternative damping choices.
:::
:::::
::::::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Damping changes the proposed direction

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-levenberg-damping.svg
:class: lm-overview-figure
:alt: Labeled contours of the exponential model’s local squared residual and its minimum, with alternative damped proposals from zero. Increasing damping shortens and rotates the step toward the negative gradient direction.
:::

**Small damping:** near the **Gauss–Newton** step when $J^{\mathsf T}J$ is nonsingular.

**Large damping:** $p\approx-J^{\mathsf T}r/\lambda$, a small gradient-like step.

:::{div}
:class: lecture-prompt

**Predict:** does a tiny update establish a good fit?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## When is Levenberg–Marquardt useful?

- **Use when:** fitting smooth nonlinear models by least squares.
- **Example:** calibration, decay curves, or parameter fitting.
- **Check:** actual loss reduction, residual patterns, and parameter sensitivity.
- **Limit:** a small residual does not establish unique or well-determined parameters.

**Trial rule:** scale parameters sensibly; adjust damping after checking each trial.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Decision case · fitting a decay curve

You fit noisy observations with $Ae^{-kt}$ from a poor initial guess.

- **Poor local prediction:** damp the trial; compare predicted and actual loss reduction.
- **Different parameter scales:** choose meaningful scales before applying $\lambda I$.
- **Only very early observations:** sensitivity to $k$ is weak because $\partial g/\partial k=-At e^{-kt}$.

:::{div}
:class: lecture-prompt

**Discuss:** can damping replace later observations that constrain the decay rate?
:::

A stable numerical step does not establish that the data identify both parameters.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Three different ways to control a step

- **Line search:** shorten a direction until it produces sufficient decrease.
- **Bracket safeguard:** retain a valid bracket and replace unsafe proposals.
- **Levenberg damping:** change the linear system proposing the direction.

**Invariant:** only the bracketed method carries a root bracket.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Integration · check the error model too

**Adaptive quadrature:** refine where local estimates indicate difficulty.

**Richardson:** cancel a leading error term when its expansion applies.

:::{div}
:class: lecture-prompt

**Predict:** can two estimates agree because both missed the same feature?
:::

Smaller reported error is evidence to investigate, not an unconditional certificate.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Where should we spend the next evaluation?



:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-local-refinement.svg
:class: refinement-figure
:alt: Uniform partition compared with an illustrative partition refined near a known localized feature. The partitions are supplied for explanation, not the output of an adaptive solver.
:::

- **Uniform refinement:** sample everywhere.
- **Local refinement:** concentrate samples where needed.

The partition uses a known feature location; it is not an adaptive solver trace.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Agreement can mean that both estimates missed it



:::{figure} figures/l9-missed-feature.svg
:alt: A narrow positive pulse lies between coarse nodes. All five sampled values are exactly zero, although the integral is positive.
:::

:::{div}
:class: lecture-prompt

**Predict:** what would coarse and refined rules report if both only see zeros?
:::

Use known feature locations, interval splitting, and independent checks. An error estimator only sees what was sampled.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Richardson · use the error pattern

**1. Assume** $Q(h)=I+Ch^p+\text{higher-order terms}$.

**2. Refine** to $Q(h/2)=I+Ch^p/2^p+\cdots$.

**3. Cancel** the leading error:

$$
R(h)=\frac{2^p Q(h/2)-Q(h)}{2^p-1}.
$$

**Symbols:** $h$ is spacing; $p$ is leading error order; $I$ is the integral.

:::{div}
:class: lecture-prompt

**Predict:** why would the wrong $p$ spoil cancellation?
:::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Richardson works when the assumed pattern applies



:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-richardson.svg
:alt: Measured trapezoid and Richardson-combined absolute errors for the integral of cosine from zero to one, compared with sine of one. The smooth example shows second- and fourth-order refinement behavior.
:::

Useful when a smooth problem has a stable error expansion at these resolutions.

Sharp features, insufficient resolution, or rounding can break that pattern.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Gauss–Legendre · choose nodes and weights

$$
\int_{-1}^{1}f(x)\,dx\approx Q_n=\sum_{i=1}^{n}w_i f(x_i).
$$

**Nodes:** $x_i$ specify where to evaluate. **Weights:** $w_i$ set each contribution.

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-gauss-nodes.svg
:class: gauss-node-figure
:alt: Two horizontal intervals from minus one to one. The endpoint trapezoid samples minus one and one, while two-node Gauss–Legendre samples plus and minus one over square root of three. All four displayed weights equal one.
:::

:::{div}
:class: lecture-prompt

**Predict:** for $f(x)=x^2$, which sample locations give a better integral?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Two evaluations · compare the answers

For $f(x)=x^2$, the exact integral on $[-1,1]$ is $2/3$.

**Endpoint trapezoid:** $Q_T=f(-1)+f(1)=2$.

**Two-node Gauss–Legendre:**

$$
Q_G=f(-1/\sqrt3)+f(1/\sqrt3)=\tfrac13+\tfrac13=\tfrac23.
$$

With $n$ nodes, Gauss–Legendre is exact for polynomials through degree $2n-1$ in exact arithmetic.

**Limit:** two nodes handle cubics exactly, but not every function. What check would you use for a new integrand?
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## See what the two rules measure



:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-gauss-area.svg
:class: area-comparison-figure
:alt: Left: endpoint trapezoid for x squared shades a rectangle of area two. Right: the true area under x squared is shaded, and Gaussian nodes have value one third with weights one, producing two thirds.
:::

- **Left shading:** trapezoid approximation.
- **Right shading:** true integral.

Gaussian weights combine sampled values; they are not automatically widths of little panels.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## When is Gauss–Legendre useful?

- **Use when:** a smooth function can be evaluated at chosen nodes.
- **Example:** an expensive integrand on a finite interval.
- **Check:** compare orders or split the interval.
- **Limit:** no built-in error estimate; treat discontinuities and endpoint singularities explicitly.

**Exactness:** $n$ nodes integrate polynomials through degree $2n-1$ in exact arithmetic. This does not extend to every smooth function.

Fixed measured samples usually require a different approach.

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Map the nodes to your interval

Library nodes $x_i$ and weights $w_i$ are defined on $[-1,1]$.

**1. Map nodes** to $[a,b]$:

$$
t_i=\frac{a+b}{2}+\frac{b-a}{2}x_i.
$$

**2. Scale weights** by half the interval length:

$$
\int_a^b f(t)\,dt\approx\frac{b-a}{2}\sum_i w_i f(t_i).
$$

:::{div}
:class: lecture-prompt

**Check:** for $f=1$, the answer must be $b-a$. Both transformations matter.
:::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Convergence · which quantity contracts?

:::{figure} ../05-numerical-methods/02-roots-quadrature/figures/l9-convergence.svg
:alt: Actual bisection midpoint errors, bracket bounds, and Newton root errors for x squared minus two. Only positive measured errors are shown; zero cannot appear on a logarithmic axis.
:::

:::{div}
:class: lecture-prompt

**Predict:** can a midpoint become worse while its bracket becomes better?
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Estimate order from three errors

Suppose consecutive errors are $10^{-1},10^{-2},10^{-4}$.

$$
p\approx\frac{\log(e_{n+1}/e_n)}{\log(e_n/e_{n-1})}=2.
$$

Three errors support this estimate. A zero error cannot enter the logarithm.

A short triple suggests local behavior; it does not prove asymptotic order.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## A bracket measures something different

Widths $1,1/2,1/4,1/8$ have ratio $1/2$.

The slope of log width against iteration is $-\log2$.

Actual midpoint errors need not decrease at every update.

:::{div}
:class: lecture-prompt

**Pair task:** return to the convergence plot. Identify three consecutive positive Newton errors suitable for an order estimate. Find a bisection update where midpoint error rises while its bracket bound halves.
:::
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Fast convergence is not the same as low cost

Compare work at the **same meaningful accuracy**.

**Count:**

- Function evaluations, including rejected trials.
- Derivative evaluations.
- Linear-system solves.

A higher-order quadrature rule uses more nodes per call. Cost also depends on what each evaluation computes.

:::{div}
:class: lecture-prompt

**Discuss:** when could fewer iterations take longer?
:::

:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Choose a method and a check

For one case, propose a method and an independent check:

1. A continuous scalar equation with a sign-changing bracket.
2. A nonlinear curve fitted to noisy observations.
3. An integral with a known narrow feature.

Project 3 will implement and apply **bisection, Newton, and secant**. Today’s advanced methods are an overview.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-teaching

## Project 2 · protected work time

**Due Wednesday, September 23, 11:59 pm PT**

Choose your first unresolved check:

- Separate cutoff error from quadrature refinement.
- Recover the uniform-disk limit.
- Explain convergence near a branch point.
- Compare adaptive accuracy with actual evaluation counts.

Show the predicted result, measured result, and the smallest case that disagrees.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-reference

## the acceptance rule

Armijo sufficient decrease:

$$
\phi(x+\alpha p)\le\phi(x)-c\alpha f(x)^2.
$$

The example uses $c=10^{-4}$ and halves $\alpha$ after rejection.

These are step-control settings, not root-accuracy tolerances. The reading contains the derivation and failure contract.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-reference

## what a line search cannot promise

The merit function can have a stationary point with $f\ne0$.

For $f(x)=x^2+1$, no real root exists, although $\phi$ has a minimum at zero.

Inspect the equation, domain, and sensitivity. Treat stagnation and exhausted budgets as failures, not successful convergence.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-reference

## Method overview

- [FNC §4.6 · Quasi-Newton methods](https://fncbook.com/python/quasinewton/): focus on **Levenberg’s method** and the damped system.
- [FNC §5.7 · Adaptive integration](https://fncbook.com/python/adaptive/): error estimation and adaptive refinement.
- [FNC §9.6 · Spectrally accurate integration](https://fncbook.com/python/spectral-integration/): focus on **Gauss–Legendre integration** and the two-node example.

Optional conceptual follow-up; textbook implementations do not replace your project code.

[SciPy’s least-squares documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) describes `method="lm"` (Levenberg–Marquardt). It does not support parameter bounds.

Course readings: **Backtracking**, **Hybrid Methods**, **Adaptive Methods and Richardson Extrapolation**.
:::::::

:::::::{div}
:class: projector-lecture lecture-78 lecture-9 projector-slide lecture-reference

## Gaussian nodes in Python

[NumPy `leggauss(n)`](https://numpy.org/doc/stable/reference/generated/numpy.polynomial.legendre.leggauss.html) returns $n$ nodes and weights on $[-1,1]$.

[SciPy `roots_legendre(n)`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.roots_legendre.html) provides the same ingredients, with a worked interval-mapping example.

These functions **do not evaluate your integrand or return its integral**. You evaluate the function and form the weighted sum.

Optional exploration; does not replace required project implementations.

[PyTorch: Jacobians and Jacobian products](https://docs.pytorch.org/tutorials/intermediate/jacobians_hessians.html) explains the automatic-differentiation connection.
:::::::
