---
title: "Part 3: Moments - The Statistical Bridge to Physics"
subtitle: "How Nature Computes | Statistical Thinking Module 1 | COMP 536"
author: "Anna Rosen"
---


## Learning Outcomes

By the end of Part 3, you will be able to:

- [ ] **Define** moments mathematically and explain their role in characterizing probability distributions
- [ ] **Calculate** the first four moments of a distribution and interpret their physical significance
- [ ] **Connect** temperature to the second moment of velocity distributions through the Maxwell-Boltzmann framework
- [ ] **Apply** moment calculations to extract macroscopic properties from microscopic distributions
- [ ] **Recognize** how moments appear in machine learning algorithms like batch normalization and optimization

---

:::{tip} Core Path in 45 Minutes

**Must-read blocks**:
1. Section 3.1: moment definitions
2. Section 3.3: physics interpretation
3. [Section 3.4](#moments-ml): ML transfer

**Optional deep dive**:
- Compare higher-order moments for non-Gaussian distributions before Project 4 diagnostics.
:::

## 3.1 What Are Moments? The Information Extractors

**Priority: 🔴 Essential**

:::{note} Observable -> Model -> Inference

- **Observable**: A large sample of particle velocities drawn from a distribution $p(v)$.
- **Model**: A normalized probability density and expectation operator.
- **Inference**: Low-order raw moments $\mu_n^{\text{raw}}$ summarize center, spread, asymmetry, and tails.
:::

You have a distribution with $10^{57}$ particles. How do you extract useful information without tracking every particle? The answer is **moments** – weighted averages that capture essential features.
Moments feel like compression; precisely, low-order moments summarize constrained information.
**Catchphrase -> Precision**: "Moments compress information" means expectation operators retain specific distribution features while discarding others.

For any probability density $p(v)$, the $n$-th raw moment is:

$$\boxed{\mu_n^{\text{raw}} = \int_{-\infty}^{\infty} v^n p(v)\, dv = \langle v^n \rangle = E[v^n]}$$

Think of moments as increasingly sophisticated summaries:

- **1st moment**: Where is the distribution centered? (mean)
- **2nd moment**: How spread out is it? (variance is the 2nd central moment)
- **3rd moment**: Is it skewed? (asymmetry)
- **4th moment**: How heavy are the tails? (extreme events)

## 3.2 Why Moments Matter Statistically

**Priority: 🔴 Essential**

:::{note} Observable -> Model -> Inference

- **Observable**: Samples from a random variable $X$ (for example velocities, fluxes, losses).
- **Model**: Distribution families characterized by moments and, when valid, moment-generating machinery.
- **Inference**: Mean, variance, skewness, and excess kurtosis map directly to physical and algorithmic behavior.
:::

Moments are the fundamental tools for characterizing distributions:

| Type | Definition | Why we use it |
|------|------------|---------------|
| Raw moment | $E[X^n]$ | Directly tracks powers and appears in expansions like the MGF |
| Central moment | $E[(X-\mu)^n]$ | Isolates shape around the mean by removing location shifts |
| Standardized moment | $E[((X-\mu)/\sigma)^n]$ | Enables scale-free comparisons across datasets |

Central moments are invariant to shifts in origin; standardized moments are invariant to both shifts and rescalings.

| Moment | Statistical Name | Physical Meaning | Formula |
|--------|-----------------|------------------|---------|
| 1st | Mean | Average value | $\mu = E[X]$ |
| 2nd central | Variance | Spread around mean | $\sigma^2 = E[(X-\mu)^2]$ |
| 3rd standardized | Skewness | Asymmetry | $\gamma_1 = E[(X-\mu)^3]/\sigma^3$ |
| 4th standardized | Excess kurtosis | Tail weight beyond Gaussian baseline | $\gamma_2 = E[(X-\mu)^4]/\sigma^4 - 3$ |

**The moment generating function** (when it exists) encodes all moments:
$$M_X(t) = E[e^{tX}] = \sum_{n=0}^{\infty} \frac{t^n}{n!}\mu_n^{\text{raw}}$$

Taylor expand and each coefficient gives a moment!

**Why few moments often suffice (with caveats)**:
- **Gaussian**: Completely determined by first two moments
- **Near-Gaussian or smooth unimodal distributions**: Low-order moments often capture dominant behavior
- **Heavy-tailed or multimodal distributions**: Higher moments or full distribution modeling may be required
- **Physics**: Many conservation laws involve low moments, but closure assumptions must be checked

:::{note} 🌟 Moments in Astronomical Observations
:class: dropdown

| Observable | What We Measure | Statistical Moment |
|------------|-----------------|-------------------|
| Radial velocity | Mean stellar motion | 1st moment of spectrum |
| Velocity dispersion | Random motions | 2nd moment $(\sqrt{\text{variance}})$ |
| Line asymmetry | Inflow/outflow | 3rd moment (skewness) |
| Wing strength | Extreme velocities | 4th moment (kurtosis) |

We rarely need moments beyond 4th order - measurement noise dominates!
:::

## 3.3 Example: Moments of Maxwell-Boltzmann

**Priority: 🔴 Essential**

:::{note} Observable -> Model -> Inference

- **Observable**: Velocity-component samples from a thermal gas.
- **Model**: Normalized 1D Maxwell-Boltzmann component PDF for $v_x$.
- **Inference**: Second central moment sets temperature and pressure relations.
:::

Let's extract physics from the Maxwell-Boltzmann distribution using moments.

For the normalized 1D velocity-component PDF, use:
$$p(v_x) = \sqrt{\frac{m}{2\pi k_B T}} \exp\left(-\frac{m v_x^2}{2k_B T}\right)$$
If you want number density form, $f(v_x) = n\,p(v_x)$.

:::{note} Precision reminder
Components $v_x$, $v_y$, and $v_z$ are Gaussian with $\mathrm{Var}(v_x)=k_B T/m$; the speed $v=|\vec{v}|$ follows the Maxwell speed distribution and is not Gaussian.
:::

**First moment** (mean velocity):
$$\langle v_x \rangle = 0$$
Symmetric distribution – no net flow.

**Second moment** (mean square velocity):
$$\langle v_x^2 \rangle = \frac{k_B T}{m}$$

This IS temperature! Temperature literally is the second moment of velocity.
More generally, temperature is tied to the variance $\langle (v_x - \langle v_x \rangle)^2\rangle$ (the second central moment); for equilibrium with zero mean flow, this equals $\langle v_x^2\rangle$.

**Connection to pressure**:
$$P = nm\langle v_x^2 \rangle = nk_B T$$

Pressure is mass density times velocity variance!

**Project Hook**: This appears in **Project 2** when you validate whether sampled velocities match target dispersion before N-body integration.

**The profound realization**:

- Temperature = variance parameter
- Pressure = density $\times$ variance
- Not analogies – mathematical identities!

(moments-ml)=
## 3.4 Moments in Machine Learning

**Priority: 🔴 Essential**

:::{note} Observable -> Model -> Inference

- **Observable**: Mini-batch activations and stochastic gradients during training.
- **Model**: Batch-statistics estimators and exponential moving averages of gradient moments.
- **Inference**: Moment estimates control numerical scale, update direction, and optimizer stability.
:::

ML uses moment estimators to stabilize training. You can read modern training loops as repeated moment estimation: normalize batch statistics so layers stay well-scaled, then accumulate gradient moments so updates are both directional and adaptive.

### Batch Normalization: First and Second Central Moments

**Code Reliability Contract**
- **Purpose**: compute and use first and second central moments for stable optimization.
- **Inputs/Outputs**: input is mini-batch tensor `x`; output is normalized activations and optimizer moment estimates.
- **Pitfall**: forgetting to define `eps` or using tiny batch sizes that destabilize moment estimates.
- **Quick fix**: define `eps = 1e-8` and verify batch statistics over multiple iterations.

```python
import numpy as np

# Minimal runnable setup for one mini-batch
rng = np.random.default_rng(536)
x = rng.normal(loc=0.0, scale=1.0, size=(32, 8))

# For each mini-batch
eps = 1e-8
batch_mean = np.mean(x, axis=0)        # 1st moment
batch_var = np.var(x, axis=0)          # 2nd central moment
normalized = (x - batch_mean) / np.sqrt(batch_var + eps)
```

BatchNorm keeps layer activations centered and comparably scaled, which improves gradient flow and reduces training instability.

### Optimizers (Momentum/Adam): First and Second Gradient Moments

Optimization also runs on moment logic: momentum tracks a first-moment trend in gradients, while Adam pairs first- and second-moment estimates to adapt step sizes dimension by dimension.

```python
import numpy as np

# Minimal runnable setup for gradient moments
rng = np.random.default_rng(536)
x = rng.normal(loc=0.0, scale=1.0, size=(32, 8))
gradient = rng.normal(loc=0.0, scale=1.0, size=x.shape[1])
velocity = np.zeros_like(gradient)
m = np.zeros_like(gradient)
v = np.zeros_like(gradient)
lr = 1e-3
momentum = 0.9
beta1 = 0.9
beta2 = 0.999

# SGD with momentum (1st moment)
velocity = momentum * velocity - lr * gradient

# Adam (1st and 2nd moments)
m = beta1 * m + (1-beta1) * gradient     # 1st moment
v = beta2 * v + (1-beta2) * gradient**2  # 2nd moment
```

**Copy/paste quick-check**: Imports: `numpy`. Seed: use `rng = np.random.default_rng(536)` for reproducible toy tensors and gradients. Variability: changing the seed changes batch statistics and moment values.

**Feature extraction IS moment computation**:

- Image statistics: mean, variance of pixels
- Time series: statistical moments over windows
- NLP: tf-idf is essentially first moment weighting

**The universal principle**: Whether extracting features from data or deriving physics from distributions, moments compress information while preserving what matters.

:::{note} Worked Micro-Example (30-60 seconds): Same Mean/Variance, Different Tails

Take two datasets with matched mean and variance: one Gaussian, one Student-t with heavier tails (rescaled to match variance). A mean/variance-based inference like "typical energy scale" stays mostly stable across both. But tail-risk inference fails: extreme-event probability and excess kurtosis diverge, so outlier-driven conclusions can flip.

```python
import numpy as np
rng = np.random.default_rng(536)
g = rng.normal(0.0, 1.0, 50_000)
t = rng.standard_t(df=5, size=50_000) * np.sqrt((5 - 2) / 5)
excess_g = np.mean((g - g.mean())**4) / np.var(g)**2 - 3
excess_t = np.mean((t - t.mean())**4) / np.var(t)**2 - 3
print(f"Gaussian excess kurtosis ~ {excess_g:.2f}, Student-t excess kurtosis ~ {excess_t:.2f}")
```
:::

:::{tip} Micro-Challenge: Same Moments, Different Physics (60-90 seconds)

Construct two distributions with matched mean and variance but different tail behavior (for example Gaussian vs. heavy-tailed).

Required output:
1. Name one physical inference that stays robust.
2. Name one inference that fails if you only trust low-order moments.

**Feedback cue**: Full credit requires mentioning kurtosis/tail risk or multimodality.
:::

:::{note} Assumptions and Failure Modes (Moments)

- **Assumptions**: finite moments for the order you use, stable normalization, and representative sampling.
- **Failure mode**: heavy tails can make high-order moments unstable or undefined.
- **Failure mode**: multimodal distributions can share low moments but differ physically.
- **Practice**: when in doubt, inspect the full distribution in addition to moment summaries.
:::

:::{important} Mastery Artifact: Moment Audit Mini-Protocol (2-5 minutes)

Run this checklist on one dataset or simulation output:
1. Compute mean, variance, skewness, and excess kurtosis.
2. Plot a histogram and check whether tails/modes agree with your moment summary.
3. Check stability versus sample size using bootstrap resamples or repeated subsampling.
4. Write one justified conclusion supported by the audit.
5. Write one non-justified conclusion you cannot claim from moments alone.
:::

```text
Moment Ladder
p(v) distribution
    -> apply E[v^n]
    -> scalar summaries (mean, variance, skewness, kurtosis)
    -> interpretation (physics state or ML training behavior)
```

## Part 3 Synthesis: Moments Bridge Statistics and Physics

:::{important} 🎯 What We Just Learned

**Moments are universal information extractors**:

1. **Definition**: $\mu_n^{\text{raw}} = E[X^n]$ captures increasingly detailed distribution features
2. **Few moments = much information**: Often 2-4 moments suffice
3. **Physical meaning**: Temperature IS variance, pressure IS second moment
4. **ML applications**: From batch norm to optimization
5. **The bridge**: Same math extracts physics from particles or features from data

In Module 2b, you'll see how taking moments of the Boltzmann equation gives conservation laws. But conceptually, it's just statistical summarization – exactly what you do in data analysis!
:::

:::{note} 🎯 Conceptual Checkpoint

Before moving to computational applications, check your understanding:

- What information does each moment extract from a distribution?
- Why is temperature related to the second moment of velocity?
- How do moments appear in machine learning algorithms you know?

Ready? Let's make these ideas computational!
:::

:::{important} Predict - Play - Explain (Part 3)

- **Predict**: Which physical observable changes first when skewness increases at fixed mean and variance?
- **Play**: Compare two synthetic distributions with identical first two moments but different tails.
- **Explain**: Identify which inferred physics is robust to low-order moments and which is not.
:::

---

## Bridge to Part 4: From Understanding to Implementation

You understand the principles and can extract information using moments. Now comes the crucial step: generating samples from these distributions computationally. This bridges theory to simulation.
All of this collapses if your samples don't represent the distribution — Part 4 is how we manufacture representative samples on purpose.

---

:::{tip} Minimum Mastery Checklist

- I can define a moment using normalized-pdf notation and interpret it physically.
- I can explain why temperature tracks a second central moment (variance) in equilibrium.
- I can identify when low-order moments are insufficient for trustworthy inference.
:::
