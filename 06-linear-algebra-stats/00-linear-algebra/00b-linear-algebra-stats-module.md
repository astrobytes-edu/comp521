---
title: "Module 1b: Statistical Linear Algebra and Numerical Methods"
subtitle: "Advanced Mathematical Foundations for Computational Astrophysics | ASTR 596"
exports:
  - format: pdf
---

## Quick Navigation Guide

### 📚 Choose Your Learning Path

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} 🏃 **Fast Track**
Starting Project 4? Read sections marked 🔴

- [Positive Definiteness](#part-1-positive-definite)
- [Covariance Matrices](#covariance-matrices)
- [Numerical Reality](#part-3-numerical-reality)
- [Quick Reference](#quickref)
:::

:::{grid-item-card} 🚶 **Standard Path**
Preparing for Projects 4-5? Read 🔴 and 🟡

- Everything in Fast Track, plus:
- [Multivariate Gaussian](#multivariate-gaussian)
- [Cholesky Decomposition](#cholesky-decomposition)
- [SVD and Applications](#svd-swiss-army)
:::

:::{grid-item-card} 🧗 **Complete Path**
Want mastery? Read all sections including 🟢

- Complete module with:
- Advanced decompositions
- Numerical implementations
- ML connections
:::
::::

### 🎯 Navigation by Project Needs

:::{important} Quick Jump to What You Need by Project
:class: dropdown

**For Project 4 (MCMC)**:
- [Section 1.3: Covariance Matrices](#covariance-matrices) - Proposal distributions
- [Section 1.4: Multivariate Gaussian](#multivariate-gaussian) - Sampling
- [Section 3: Numerical Reality](#part-7-numerical-reality) - Stability

**For Project 5 (Gaussian Processes)**:
- [Section 5: Positive Definite Matrices](#part-5-positive-definite) - Kernel matrices
- [Section 5.5: Cholesky Decomposition](#cholesky-decomposition) - GP implementation
- [Section 6.2: Schur Complement](#block-matrices) - Efficient updates

**For Final Project (Neural Networks)**:
- [Section 6: Advanced Topics](#part-6-advanced) - Matrix norms, Jacobians
- [Section 8: Bridge to ML](#part-8-bridge) - Connecting everything
- [Section 8.5: Matrix Calculus](#matrix-calculus-nn) - Backpropagation
:::

---

## Learning Objectives

:::{hint} 📅 When to Read This Module
:class: dropdown

- [ ] **Before Project 4**: Read sections marked 🔴 (3-4 hours)
- [ ] **During Projects 4-5**: Deep dive into 🟡 sections
- [ ] **For Final Project**: Review Section 8 connections
- [ ] **Reference**: Return when debugging numerical issues

**Prerequisites**: Complete Module 0a or be comfortable with vectors, matrices, and eigenvalues.
:::

By the end of this module, you will be able to:

- [ ] **Determine** whether a matrix is positive definite using multiple methods 🔴
- [ ] **Construct and interpret** covariance matrices from data 🔴
- [ ] **Apply** Cholesky decomposition for sampling and solving 🟡
- [ ] **Debug** numerical failures in statistical computations 🔴
- [ ] **Connect** linear algebra to MCMC, Gaussian Processes, and neural networks 🟡
- [ ] **Implement** robust algorithms that handle finite precision 🟢

---

## Prerequisites from Module 0a

:::{note} 📚 Required Knowledge from Module 0a
:class: dropdown

**Priority: 🔴 Essential** - Review if needed

Before starting this module, ensure you understand:

- [ ] Matrix multiplication and transposition
- [ ] Eigenvalues and eigenvectors
- [ ] Symmetric matrices and their properties
- [ ] Matrix determinants and rank
- [ ] Basic floating-point arithmetic concepts

If unfamiliar, review Module 0a first. This module builds on numerical foundations from Module 0a, focusing on advanced topics specific to statistical methods and machine learning.
:::

---

## Module Overview

:::{important} 🎯 Core Message
:class:

**Priority: 🔴 Essential**:

This module bridges deterministic linear algebra with statistical methods and machine learning. You'll master the mathematical foundations for uncertainty quantification, probabilistic inference, and learning algorithms—essential for Projects 4-6. Building on Module 0a's numerical foundations, we explore advanced numerical methods specific to statistical computations.
:::

Building on Module 0a's foundations, this module explores how linear algebra enables statistical computation and machine learning. We cover **positive definite matrices** that ensure physical validity (Project 4), **covariance structures** that encode correlations (Project 5), and **advanced numerical methods** that keep statistical computations stable despite finite precision (all projects). The module culminates by showing how these concepts unite classical physics with modern machine learning (Final Project).

:::{admonition} 🎯 Why This Module Matters
:class: important

For Projects 4-6, you'll need:

- **Project 4 (MCMC)**: Covariance matrices for proposals, multivariate Gaussians for sampling
- **Project 5 (Gaussian Processes)**: Positive definite kernels, Cholesky decomposition, numerical stability
- **Final Project (Neural Networks)**: Matrix norms for convergence, Jacobians for backpropagation, matrix calculus

These aren't just mathematical abstractions—they're the tools that let you quantify uncertainty in cosmological parameters, interpolate sparse astronomical data, and train neural networks to discover patterns in observations.
:::

## Part 1: Positive Definite Matrices and Statistical Foundations

**Priority: 🟡 Important** - Essential for Projects 4-5

:::{admonition} 📅 When You'll Use This
:class: dropdown, hint

- **First appears in**: Project 4 (MCMC covariance matrices)
- **Critical for**: Project 5 (Gaussian Process kernels)
- **Why it matters**: Ensures physical validity of statistical methods

Can skip initially, but must understand before Project 4.
:::

:::{admonition} 🔭 Where We're Going
:class: note

**Positive definite matrices** are where linear algebra meets statistics and optimization. We'll see why these special matrices guarantee that energies are positive, distances make sense, and probability distributions are valid. This section bridges deterministic physics with statistical methods, preparing you for MCMC and Gaussian Processes.
:::

### 1.1 Quadratic Forms and Energy {#part-5-positive-definite}

```{margin}
**quadratic form**
Expression $Q(\vec{x}) = \vec{x}^T A \vec{x}$ where A is symmetric
```

A **quadratic form** is:
$$Q(\vec{x}) = \vec{x}^T A \vec{x} = \sum_{i,j} A_{ij} x_i x_j$$

These appear as energy expressions throughout physics:

| Type | Formula | Physical Meaning |
|------|---------|------------------|
| Kinetic Energy | $T = \frac{1}{2}\vec{v}^T M \vec{v}$ | M is mass matrix |
| Potential Energy | $V = \frac{1}{2}\vec{x}^T K \vec{x}$ | K is stiffness matrix |
| Statistical Distance | $d^2 = (\vec{x}-\vec{\mu})^T \Sigma^{-1} (\vec{x}-\vec{\mu})$ | Mahalanobis distance |

**Physical Example: The kinetic energy of a rotating rigid body**
$$T = \frac{1}{2}\vec{\omega}^T I \vec{\omega}$$
where $\vec{\omega}$ is angular velocity and $I$ is the moment of inertia tensor. This quadratic form is always positive (energy can't be negative), making $I$ positive definite. The eigenvectors of $I$ are the principal axes - spin around these and the object doesn't wobble!

### 1.2 Positive Definiteness: Ensuring Physical Reality {#positive-definiteness}

```{margin}
**positive definite**
Matrix where $\vec{x}^T A \vec{x} > 0$ for all $\vec{x} \neq \vec{0}$

**positive semi-definite**
Matrix where $\vec{x}^T A \vec{x} \geq 0$ for all $\vec{x}$
```

```{margin}
**Cholesky decomposition**
Factorization of a positive definite matrix $A = LL^T$ where $L$ is lower triangular with positive diagonal entries
```

A symmetric matrix is **positive definite** if its quadratic form is always positive. This property ensures physical validity—energies are positive, distances are non-negative, and covariance matrices represent valid uncertainties.

**Four Equivalent Tests for Positive Definiteness**:

1. ✅ All eigenvalues > 0
2. ✅ All leading principal minors > 0
3. ✅ Has Cholesky decomposition $A = LL^T$ (requires strict positive definiteness)
4. ✅ Can write as $A = B^T B$ for some invertible matrix $B$

**Quick check**: Positive definite matrices always have positive diagonal elements. Proof: For standard basis vector $\vec{e}_i$, we have $\vec{e}_i^T A \vec{e}_i = A_{ii} > 0$.

**Important Distinction**:
- **Positive definite** (all eigenvalues > 0): Standard Cholesky works
- **Positive semi-definite** (eigenvalues ≥ 0): May have rank deficiency (rank < dimension), requiring modified Cholesky or eigendecomposition
- **Why it matters**: Zero eigenvalues mean the matrix maps some directions to zero—information is lost

```{margin}
**regularization**
Adding small positive values (often to diagonals) to improve numerical stability or prevent singularities
```

:::{warning} ⚠️ Regularization Bias Throughout Your Projects

**The Art of Regularization**: While regularization stabilizes computations, it introduces bias:

**Too little regularization (λ → 0)**:
- Numerical instability
- Matrix singularities
- Overfitting in ML

**Too much regularization (large λ)**:

- Biased estimates (shrinking toward zero)
- Loss of fine structure
- Underfitting in ML

**Finding the sweet spot**:

- Cross-validation for ML problems
- Physical constraints (noise levels) for GPs
- Condition number monitoring for numerical stability

In Project 5, your GP's noise term σ²ₙ acts as natural regularization — set it based on actual measurement uncertainty, not arbitrary numerical convenience.
:::

:::{warning} ⚠️ Common Bug in Project 5

When implementing Gaussian Processes, your kernel matrix might lose positive definiteness due to numerical errors. 

**Symptoms**:

- Cholesky decomposition fails with `numpy.linalg.LinAlgError`
- Negative variance predictions (physically impossible!)
- Eigenvalues that should be positive show as tiny negatives (e.g., -1e-15)

**Why this happens**: Floating-point arithmetic accumulates tiny errors. A mathematically positive definite matrix can become numerically indefinite.

**Fix**: Add small "jitter" to diagonal

```python
K_stable = K + 1e-6 * np.eye(n)  # Add small positive value to diagonal
# np.eye(n) creates an n×n identity matrix (1s on diagonal, 0s elsewhere)
```

This is **regularization**, not a hack! It accounts for numerical precision limits and is standard practice in GP implementations.
:::

:::{note} 📝 Regularization Throughout Your Projects

**Regularization**—adding small terms to prevent numerical issues—appears everywhere in computational astrophysics:

**Project 2 (N-body)**: Gravitational softening prevents $r \to 0$ singularities.

```python
F = GMm/(r^2 + epsilon^2)  # epsilon prevents division by zero
```

**Project 4 (MCMC)**: Ridge regression adds $\lambda ||w||^2$ to prevent overfitting.

```python
loss = data_term + lambda * np.sum(weights**2)  # L2 regularization
```

**Project 5 (GPs)**: Jitter term ensures positive definiteness.

```python
K = K + sigma_n^2 * I  # Noise term regularizes covariance
```

**Final Project (Neural Networks)**: Weight decay prevents overfitting.

```python
loss = cross_entropy + weight_decay * sum_of_squared_weights
```

Regularization isn't cheating – it's acknowledging that perfect mathematical conditions don't exist in finite-precision computation. The art is choosing regularization strength: too little fails to stabilize, too much distorts your physics.
:::

:::{admonition} 💡 Building Intuition: The Bowl Analogy
:class: note

A positive definite matrix creates a bowl-shaped quadratic form. Imagine the function $f(\vec{x}) = \vec{x}^T A \vec{x}$ as a landscape:

- **Positive definite**: Bowl opening upward (unique minimum at origin)
- **Negative definite**: Bowl opening downward (unique maximum at origin)
- **Indefinite**: Saddle shape (some directions go up, others down)
- **Positive semi-definite**: Bowl with flat bottom (minimum not unique)

This is why positive definite matrices guarantee unique solutions in optimization—there's only one bottom of the bowl!
:::

### 1.3 Covariance Matrices: The Bridge to Statistics {#covariance-matrices}

**Priority: 🟡 Important** - Foundation for Projects 4-5

```{margin}
**covariance**
Measure of how two variables change together; positive means they increase together, negative means one increases as the other decreases

**covariance matrix**
Matrix containing all pairwise covariances between random variables; encodes all linear relationships in your data
```

Before diving into matrices, let's understand what **covariance** actually tells us:

**Intuitive Understanding**:
- **Positive covariance**: Variables tend to increase together (mass and luminosity in stars)
- **Negative covariance**: One increases as the other decreases (stellar temperature and radius for giants)
- **Zero covariance**: No linear relationship (doesn't mean independent!)

**Mathematical Definition**:
$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

This measures the average product of deviations from the mean. When both variables are above (or below) their means together, the products are positive, giving positive covariance.

**Relationship to Correlation**:
$$\text{Correlation} = \rho_{XY} = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$$

Correlation is just normalized covariance! It ranges from -1 to +1, making it easier to interpret than raw covariance.

**The Covariance Matrix**:

For multiple variables $X_1, ..., X_n$, we organize all pairwise covariances into a matrix:

$$\Sigma_{ij} = \text{Cov}(X_i, X_j) = E[(X_i - \mu_i)(X_j - \mu_j)]$$

**Structure and Properties**:

- **Diagonal elements**: $\Sigma_{ii} = \text{Var}(X_i)$ (variances are "self-covariance")
- **Off-diagonal elements**: $\Sigma_{ij}$ (covariances between different variables)
- **Always symmetric**: $\Sigma_{ij} = \Sigma_{ji}$ (order doesn't matter)
- **Always positive semi-definite**: All eigenvalues ≥ 0 (why? see below)

**Why Positive Semi-Definite?**

For any linear combination of variables $Y = a^T X$:
$$\text{Var}(Y) = a^T \Sigma a \geq 0$$

Variance can't be negative! This forces $\Sigma$ to be positive semi-definite. If it has negative eigenvalues, you could construct a linear combination with negative variance—physically impossible!

:::{admonition} 📝 Worked Example: Constructing a Covariance Matrix from Data
:class: note

**Priority: 🟡 Important for Project 4**
Given stellar measurements for 4 stars (mass and luminosity):

```python
# Data: each row is a star, columns are [mass, luminosity]
data = np.array([
    [1.0, 1.2],   # Star 1
    [1.5, 3.1],   # Star 2
    [0.8, 0.6],   # Star 3
    [1.2, 1.9]    # Star 4
])

# Step 1: Compute means
means = np.mean(data, axis=0)  # [1.125, 1.7]

# Step 2: Center the data (subtract means)
centered = data - means
# [[-0.125, -0.5],   # Star 1 below avg mass, below avg lum
#  [ 0.375,  1.4],   # Star 2 above avg mass, above avg lum
#  [-0.325, -1.1],   # Star 3 below avg mass, below avg lum
#  [ 0.075,  0.2]]   # Star 4 slightly above both

# Step 3: Compute covariance matrix
n = len(data)

# Why n-1? This is Bessel's correction for unbiased sample covariance
# When we estimate the mean from the same data, we lose one degree of freedom
# Using n would systematically underestimate the true population variance
# The n-1 divisor corrects this bias, giving an unbiased estimator
cov = (centered.T @ centered) / (n - 1)
# [[0.0892, 0.3242],
#  [0.3242, 1.2867]]

# Mathematical justification: E[S²] = σ² only when we divide by (n-1)
# This comes from the fact that Σ(xi - x̄)² has only n-1 independent terms
# since the deviations must sum to zero: Σ(xi - x̄) = 0

# Note: numpy.cov() uses n-1 by default (ddof=1) for this reason
# You can verify: np.allclose(cov, np.cov(data.T))

# Interpretation:
# - Var(mass) = 0.0892 (spread in masses)
# - Var(luminosity) = 1.2867 (larger spread in luminosities)
# - Cov(mass, lum) = 0.3242 > 0 (positive correlation!)

# Correlation coefficient:
correlation = 0.3242 / (np.sqrt(0.0892) * np.sqrt(1.2867))
# correlation ≈ 0.96 (very strong!)
```

The positive covariance confirms the mass-luminosity relation! More massive stars are more luminous.
:::

:::{note} 📝 Geometric Interpretation of Covariance

The covariance matrix defines an **uncertainty ellipsoid** in parameter space:

- **Eigenvectors**: Principal axes of the ellipsoid (directions of maximum/minimum variance)
- **Eigenvalues**: Variance along each principal axis (squared semi-axis lengths)
- **Off-diagonal terms**: Tilt of the ellipsoid (correlations rotate the axes)

In Project 4 (MCMC), you'll sample from multivariate Gaussians with covariance $\Sigma$. Your samples will form an elliptical cloud with shape determined by $\Sigma$!

In Project 5 (GPs), the kernel matrix IS a covariance matrix – it encodes how correlated function values are at different points.
:::

### 1.4 The Multivariate Gaussian Distribution {#multivariate-gaussian}

**Priority: 🟡 Important** - Core of Projects 4-5

```{margin}
**multivariate Gaussian**
Multi-dimensional bell curve defined by mean vector and covariance matrix

**Mahalanobis distance**
Scale-invariant distance that accounts for correlations; measures "how many standard deviations away" in correlated space

**precision matrix**
Inverse of covariance matrix: $\Sigma^{-1}$; encodes conditional independence structure
```

The **multivariate Gaussian** extends the familiar bell curve to multiple dimensions. In 1D, you know the Gaussian as the bell-shaped $e^{-x^2}$ curve. In higher dimensions, it becomes an ellipsoidal cloud of probability.

**The Formula Decoded**:

$$p(\vec{x}) = \frac{1}{(2\pi)^{n/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})\right)$$

Let's understand each piece intuitively:

**The Exponent**: $-\frac{1}{2}(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})$

- This is the **Mahalanobis distance** squared
- In 1D with variance $\sigma^2$: reduces to $-(x-\mu)^2/(2\sigma^2)$
- Measures "how many standard deviations away" but accounts for correlations
- If variables are correlated, being far in one direction might be "cheaper" than another

**The Normalization**: $(2\pi)^{n/2}|\Sigma|^{1/2}$

- Ensures total probability integrates to 1
- $|\Sigma|$ is the determinant—the "volume" of the uncertainty ellipsoid
- Larger determinant = more spread out = lower peak height (volume conserved)

**Geometric Picture**:

- **Mean $\vec{\mu}$**: Center of the probability cloud
- **Covariance $\Sigma$**: Shape and orientation of the ellipsoid
  - Eigenvalues: Lengths of ellipsoid axes
  - Eigenvectors: Directions of axes
- **Contours of constant probability**: Ellipsoids defined by $(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu}) = c$

:::{admonition} 📝 Why $\Sigma^{-1}$ Appears (Not Just $\Sigma$)
:class: note

The inverse covariance $\Sigma^{-1}$ (called the **precision matrix**) appears because we need to "undo" the correlations to measure true distance.

**Analogy**: Imagine measuring distance on a stretched map. If the map stretches 2× horizontally, a 2cm horizontal distance on the map represents only 1cm in reality. You need to divide by the stretch factor (inverse transform) to get true distance.

Similarly, $\Sigma$ stretches space according to variances and correlations. To measure how "far" a point is from the mean in a statistically meaningful way, we need $\Sigma^{-1}$ to undo this stretching.

**In your projects**:

- **Project 4**: MCMC proposals use multivariate Gaussians—the covariance determines step sizes and directions
- **Project 5**: GP predictions are multivariate Gaussians—the kernel determines the covariance structure
:::

(cholesky-decomposition)=
### 1.5 Cholesky Decomposition: The Matrix Square Root 

**Priority: 🟡 Important** - Essential for Project 5

```{margin}
**Cholesky decomposition**
Factorization $A = LL^T$ where L is lower triangular; geometrically, finds the "square root" of a positive definite matrix

**forward substitution**
Solving lower triangular systems from top to bottom

**back substitution**
Solving upper triangular systems from bottom to top
```

Every positive definite matrix can be factored as:

$$A = LL^T$$

where $L$ is lower triangular with positive diagonal entries.

**Uniqueness Property**: The Cholesky decomposition is unique — for any positive definite matrix $A$, there exists exactly one lower triangular matrix $L$ with positive diagonal entries such that $A = LL^T$.

This uniqueness is crucial for numerical methods: no matter which algorithm you use (whether the classical Cholesky-Banachiewicz or the Cholesky-Crout variant), you'll always get the same $L$ matrix (up to numerical precision). This deterministic property makes Cholesky decomposition ideal for reproducible scientific computing.

**Why uniqueness matters**: When you use Cholesky in your MCMC proposals (Project 4) or GP implementations (Project 5), you're guaranteed consistent results across different machines and libraries. This isn't true for eigendecomposition, where eigenvectors can differ by sign or be arbitrarily chosen when eigenvalues are repeated.

**Intuitive Understanding**: Think of Cholesky as finding the "square root" of a matrix

- Just as $9 = 3 \times 3$, we have $A = L \times L^T$
- $L$ transforms uncorrelated unit variance variables into correlated variables with covariance $A$

**Why Lower Triangular?**
The triangular structure means each variable depends only on previous ones:

- Variable 1: Independent
- Variable 2: Depends on variable 1
- Variable 3: Depends on variables 1 and 2
- And so on...

This sequential dependency structure makes computation efficient!

**Two Key Applications**:

**1. Solving Linear Systems** (faster than computing inverse):

```python
# Problem: Solve Ax = b where A is positive definite

# Slow way: x = inv(A) @ b (NEVER DO THIS!)
# - Computing inverse: O(n³) operations
# - Numerically unstable
# - Loses sparsity structure

# Fast way using Cholesky:
L = np.linalg.cholesky(A)      # A = LL^T
# Now Ax = b becomes LL^T x = b

# Step 1: Solve Ly = b (forward substitution)
y = np.linalg.solve(L, b)

# Step 2: Solve L^T x = y (back substitution)
x = np.linalg.solve(L.T, y)

# Why faster? Triangular systems solve in O(n²) not O(n³)!
```

**2. Generating Correlated Random Variables** (Projects 4-5):

```python
# Generate samples from N(mu, Sigma)

# The magic: If z ~ N(0, I), then Lz ~ N(0, LL^T) = N(0, Sigma)
L = np.linalg.cholesky(Sigma)
z = np.random.randn(n)          # Standard normal (uncorrelated)
x = mu + L @ z                  # Has mean mu, covariance Sigma

# Why does this work?
# - z has covariance I (independent unit variance)
# - Lz has covariance L·I·L^T = LL^T = Sigma
# - Adding mu shifts the mean without changing covariance
```

:::{note} 💡 Geometric Interpretation

**Cholesky geometrically transforms a sphere into an ellipsoid**:

1. Start with standard normal samples (spherical cloud)
2. $L$ stretches and rotates to create the correlation structure
3. Result matches the desired covariance ellipsoid

This is why Cholesky is essential for:

- **MCMC** (Project 4): Generate proposal steps with correct correlations
- **GP sampling** (Project 5): Generate functions from the GP prior
- **Data augmentation**: Create synthetic data with realistic correlations

The triangular structure of $L$ means the transformation happens sequentially—each dimension adds its contribution based on previous dimensions.
:::

### Progressive Problems: Positive Definiteness

::::{admonition} 📝 Practice Problems
:class: note

**Level 1**: Verify that the identity matrix is positive definite.

**Level 2**: Prove that if $A$ is positive definite, then $A^{-1}$ is also positive definite.

**Level 3**: Show that the sum of two positive definite matrices is positive definite.

:::{tip} Solutions
:class: dropdown

**Level 1**: For identity matrix $I$ and any $\vec{x} \neq 0$: $\vec{x}^T I \vec{x} = |\vec{x}|^2 > 0$ ✓

**Level 2**: Let $\vec{y} = A^{-1}\vec{x}$ where $\vec{x} \neq 0$. Then $\vec{x} = A\vec{y}$ and $\vec{y} \neq 0$. We have: $\vec{x}^T A^{-1} \vec{x} = \vec{y}^T A \vec{y} > 0$ (since $A$ is positive definite).

**Level 3**: For positive definite $A$ and $B$: $\vec{x}^T(A+B)\vec{x} = \vec{x}^T A\vec{x} + \vec{x}^T B\vec{x} > 0 + 0 = 0$ for all $\vec{x} \neq 0$.
:::
::::

:::{admonition} 📌 Key Takeaway
:class: important

**Positive definite matrices** guarantee physical validity. They ensure energies are positive, distances are non-negative, and probability distributions integrate to 1. When you see a positive definite matrix, think "this represents something that must be positive in the real world."

The **multivariate Gaussian** shows how mean vectors and **covariance matrices** fully characterize multi-dimensional uncertainty. **Cholesky decomposition** is your Swiss Army knife for working with these structures – it's the bridge between uncorrelated randomness and structured correlations, making it essential for sampling, solving, and simulating throughout your projects.
:::

---

## Part 2: Advanced Topics for Your Projects

**Priority: 🟢 Enrichment** - Read as needed for specific projects

:::{hint} 📅 When You'll Use This
:class: dropdown

These advanced topics appear in later projects or when optimizing code. Read as needed rather than all at once. Revisit these sections after completing related projects — they'll make more sense with practical experience.
:::

### 2.1 Singular Value Decomposition - The Swiss Army Knife {#svd-swiss-army}

```{margin}
**SVD**
Universal decomposition $A = U\Sigma V^T$ that reveals the fundamental action of any matrix

**singular values**
Non-negative values σ₁ ≥ σ₂ ≥ ... ≥ 0 measuring importance of each component

**pseudoinverse**
Generalized inverse $A^+ = V\Sigma^+ U^T$ that gives least-squares solution for overdetermined systems
```

Every matrix has a **singular value decomposition**:
$$A = U\Sigma V^T$$

where:

- $U$: Left singular vectors (orthonormal output directions)
- $\Sigma$: Diagonal matrix of singular values (stretching factors)
- $V^T$: Right singular vectors (orthonormal input directions)

**SVD for Non-Square Matrices**: For an $m \times n$ matrix $A$:

- $U$ is $m \times m$ (square, orthogonal)
- $\Sigma$ is $m \times n$ (rectangular!)
- $V^T$ is $n \times n$ (square, orthogonal)

Only $\min(m,n)$ singular values exist; the rest of $\Sigma$ is padded with zeros. This is crucial for understanding rank and dimensionality reduction.

**Geometric Intuition**: Any matrix transformation can be broken into three steps:

1. **Rotate** (by $V^T$): Align input to principal axes
2. **Stretch** (by $\Sigma$): Scale along each axis by σᵢ
3. **Rotate** (by $U$): Align to output space

This means ANY linear transformation—no matter how complex—is just rotate-stretch-rotate! This decomposition is unique (up to sign ambiguities) and always exists.

**Understanding Rank Through SVD**:
The rank of a matrix equals the number of non-zero singular values. This tells you the true dimensionality:

- Full rank: All $σᵢ > 0$, no information lost
- Rank deficient: Some $σᵢ = 0$, transformation loses dimensions
- Numerical rank: Count $σᵢ >$ tolerance (e.g., 10⁻¹⁰) for finite precision

**The Pseudoinverse and Least Squares**:

The **pseudoinverse** $A^+ = V\Sigma^+ U^T$ where $\Sigma^+$ inverts non-zero singular values:

- For overdetermined systems (more equations than unknowns): Gives least-squares solution
- For underdetermined systems (more unknowns than equations): Gives minimum-norm solution
- Robust via truncation: Ignore singular values < threshold

```python
# Computing pseudoinverse via SVD
U, s, Vt = np.linalg.svd(A, full_matrices=False)

# Threshold small singular values (regularization)
threshold = 1e-10 * s.max()
s_inv = np.where(s > threshold, 1/s, 0)

# Construct pseudoinverse
A_pseudo = Vt.T @ np.diag(s_inv) @ U.T

# Now x = A_pseudo @ b gives:
# - Least-squares solution if overdetermined
# - Minimum-norm solution if underdetermined
```

**Why SVD Beats Eigendecomposition**:

| Property | Eigendecomposition | SVD |
|----------|-------------------|-----|
| Works for | Square matrices only | ANY matrix shape |
| Requires | Diagonalizable | Always works |
| Vectors | May be complex | Always real for real matrices |
| Values | Can be negative/complex | Always non-negative real |
| Numerical stability | Can be unstable | Very stable algorithms |

**The Deep Connection**:
For any matrix $A$:

- $A^T A$ has eigenvalues $\lambda_i = \sigma_i^2$ and eigenvectors = columns of $V$
- $AA^T$ has eigenvalues $\lambda_i = \sigma_i^2$ and eigenvectors = columns of $U$
- This is why SVD always exists—symmetric matrices always have eigendecompositions!

:::{note} 📝 Principal Component Analysis (PCA) = SVD of Data

**PCA is just SVD applied to centered data!**

Given data matrix $X$ (each row = observation, column = feature):

1. Center the data: $X_c = X - \text{mean}(X)$
2. Apply SVD: $X_c = U\Sigma V^T$
3. Principal components = columns of $V$ (right singular vectors)
4. Variance explained by component $i$ = $\sigma_i^2/(n-1)$
5. Fraction of total variance = $\sigma_i^2 / \sum_j \sigma_j^2$

**Concrete Astrophysical Example**: Decomposing 1000 galaxy spectra

```python
# Each row = one galaxy's spectrum (flux at 4000 wavelengths)
spectra = np.array([...])  # Shape: (1000, 4000)

# Center the data
mean_spectrum = np.mean(spectra, axis=0)
centered = spectra - mean_spectrum

# Apply SVD
U, s, Vt = np.linalg.svd(centered, full_matrices=False)

# First 3 components might capture 95% of variation:
# Component 1: Old stellar population (red, smooth)
# Component 2: Star formation (blue, emission lines)
# Component 3: AGN activity (broad lines, power-law continuum)

# Reconstruct using only k components (dimensionality reduction):
k = 10  # Keep first 10 components
compressed = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
# 1000×4000 matrix stored as 1000×10 + 10 + 10×4000 = 54,010 numbers
# Instead of 4,000,000 numbers—74× compression!
```

The singular values tell you how many components you really need—often just 10-20 capture 99% of thousands of dimensions!
:::

(block-matrices)=
### 2.2 Block Matrices and the Schur Complement

```{margin}
**block matrix**
Matrix partitioned into submatrices, often reflecting natural system structure

**Schur complement**
The "effective" matrix after eliminating some variables: $S = A - BD^{-1}C$
```

Large systems often have natural block structure:
$$M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$$

**Physical Motivation**: Different parts of your system interact differently.

**Concrete Example: Triple Star System**
Consider a close binary with a distant third star:
$$\begin{pmatrix}
F_{11} & F_{12} & F_{13} \\
F_{21} & F_{22} & F_{23} \\
F_{31} & F_{32} & F_{33}
\end{pmatrix} = 
\begin{pmatrix}
\begin{array}{cc|c}
0 & \text{strong} & \text{weak} \\
\text{strong} & 0 & \text{weak} \\
\hline
\text{weak} & \text{weak} & 0
\end{array}
\end{pmatrix}$$

The 2×2 upper-left block represents strong binary interactions, while off-diagonal blocks show weak coupling to the distant star.

**The Schur Complement in Action**:

Let's solve $\begin{pmatrix} A & B \\ C & D \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} f \\ g \end{pmatrix}$

Instead of solving the full system, we can eliminate $y$:
1. From bottom equation: $y = D^{-1}(g - Cx)$
2. Substitute into top: $Ax + BD^{-1}(g - Cx) = f$
3. Rearrange: $(A - BD^{-1}C)x = f - BD^{-1}g$

The matrix $S = A - BD^{-1}C$ is the Schur complement—it's the "effective $A$" after accounting for $y$'s influence through $D$.

**Physical Intuition**: Think of the Schur complement as "marginalizing out" variables. It's like projecting 3D motion onto 2D while accounting for the 3rd dimension's influence. When you eliminate variables, their effect doesn't disappear—it gets encoded in the effective interactions between remaining variables.

**Simple 2×2 Example**:
$$\begin{pmatrix} 3 & 1 \\ 2 & 4 \end{pmatrix} = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$$

Schur complement of $D$: $S = 3 - (1)(1/4)(2) = 3 - 0.5 = 2.5$

This 2.5 is the "effective resistance" in the first variable after the second adjusts optimally.

**Why It Matters for Project 5 (GPs)**:
When you add a new observation to a Gaussian Process:
- Old observations = block $A$
- Covariance with new point = blocks $B, C$  
- New point variance = block $D$
- Prediction uses the Schur complement to efficiently update without re-inverting everything!

### 2.3 The Jacobian Matrix: Local Linear Approximation {#jacobian-matrix}

```{margin}
**Jacobian**
Matrix of all first-order partial derivatives; the best linear approximation at a point
```

For vector function $\vec{f}: \mathbb{R}^n \to \mathbb{R}^m$:
$$J_{ij} = \frac{\partial f_i}{\partial x_j}$$

**Intuitive Understanding**: Near any point, nonlinear functions look linear. The Jacobian is that linear approximation:
$$\vec{f}(\vec{x} + \delta\vec{x}) \approx \vec{f}(\vec{x}) + J\cdot\delta\vec{x}$$

**Concrete 2D Example**: 
For the transformation $f(r, \theta) = (r\cos\theta, r\sin\theta)$ (polar to Cartesian):
$$J = \begin{pmatrix} 
\frac{\partial x}{\partial r} & \frac{\partial x}{\partial \theta} \\
\frac{\partial y}{\partial r} & \frac{\partial y}{\partial \theta}
\end{pmatrix} = \begin{pmatrix}
\cos\theta & -r\sin\theta \\
\sin\theta & r\cos\theta
\end{pmatrix}$$

The determinant $|J| = r$ tells you area scaling—this is why polar area elements are $r\,dr\,d\theta$!

**In Project 2 (N-body Stability)**:
Near an equilibrium configuration $\vec{s}_0$, perturbations $\delta\vec{s}$ evolve as:
$$\frac{d(\delta\vec{s})}{dt} = J|_{\vec{s}_0} \cdot \delta\vec{s}$$

The eigenvalues of $J$ determine the fate:
- All Re(λ) < 0: Stable (perturbations decay)
- Any Re(λ) > 0: Unstable (perturbations grow)
- Re(λ) = 0, Im(λ) ≠ 0: Neutral oscillations

Example: For a star orbiting at Lagrange point L4:
- Eigenvalues have small negative real parts → weakly stable
- Large imaginary parts → oscillates if perturbed
- This is why Trojan asteroids librate around L4/L5!

### 2.4 Matrix Exponentials: Solving Linear Evolution {#matrix-exponentials}

```{margin}
**matrix exponential**
$e^{At}$ propagates linear systems forward in time
```

The matrix exponential solves any linear ODE system:
$$\frac{d\vec{x}}{dt} = A\vec{x} \implies \vec{x}(t) = e^{At}\vec{x}(0)$$

**Three Ways to Understand $e^{At}$**:

**1. Series Definition** (like scalar exponential):
$$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + ...$$

**2. Through Eigenvalues** (if $A$ is diagonalizable):
If $A = PDP^{-1}$ where $D$ is diagonal with eigenvalues:
$$e^{At} = Pe^{Dt}P^{-1} = P\begin{pmatrix} e^{\lambda_1 t} & & \\ & e^{\lambda_2 t} & \\ & & \ddots \end{pmatrix}P^{-1}$$

**3. Physical Interpretation**: $e^{At}$ is the propagator—it evolves the system from time 0 to time $t$.

**Practical Computation**:
```python
# Never use the series directly—it's inefficient and can be inaccurate
# Instead, use specialized algorithms:

import scipy.linalg as la

A = np.array([[0, 1], [-1, -0.1]])  # Damped oscillator
t = 5.0

# Method 1: Direct computation (best for dense matrices)
expAt = la.expm(A * t)

# Method 2: Via eigendecomposition (good for understanding)
eigvals, eigvecs = la.eig(A)
D = np.diag(np.exp(eigvals * t))
expAt_eig = eigvecs @ D @ la.inv(eigvecs)

# Method 3: For solving ODEs, use ODE solvers instead!
# They're more efficient than computing e^{At} explicitly
```

:::{warning} ⚠️ Numerical Stability Warning
For large t or poorly conditioned A, computing e^{At} directly can be numerically unstable. The eigenvalues get exponentiated, so if Re(λ) > 0, e^{λt} grows exponentially. For time evolution problems, prefer ODE solvers with adaptive timestepping:

```python
from scipy.integrate import solve_ivp

def system(t, x):
    return A @ x

sol = solve_ivp(system, [0, t_final], x0, method='DOP853')
# Adaptive stepping maintains accuracy without computing e^{At}
```
:::

**Example: Damped Harmonic Oscillator**:
For $\ddot{x} + \gamma\dot{x} + \omega_0^2 x = 0$, rewrite as first-order system:
$$\frac{d}{dt}\begin{pmatrix} x \\ v \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ -\omega_0^2 & -\gamma \end{pmatrix} \begin{pmatrix} x \\ v \end{pmatrix}$$

The eigenvalues $\lambda = \frac{-\gamma \pm \sqrt{\gamma^2 - 4\omega_0^2}}{2}$ determine behavior:
- Underdamped ($\gamma < 2\omega_0$): Complex λ → oscillatory decay
- Critically damped ($\gamma = 2\omega_0$): Repeated real λ → fastest decay
- Overdamped ($\gamma > 2\omega_0$): Two real λ → slow decay

### 2.5 Matrix Norms: How Big is a Matrix?

**Priority: 🟢 Enrichment** - Crucial for understanding stability and convergence

```{margin}
**Frobenius norm**
Sum of squared elements: $||A||_F = \sqrt{\sum_{i,j} |a_{ij}|^2}$

**spectral norm**
Maximum amplification factor: $||A||_2 = \sigma_{\max}$
```

Matrix norms measure "size" but different norms capture different aspects:

**Frobenius Norm** (total "energy"):
$$||A||_F = \sqrt{\sum_{i,j} |a_{ij}|^2} = \sqrt{\text{trace}(A^T A)}$$
- Like treating matrix as a long vector
- All elements contribute equally
- Easy to compute but ignores structure

**Spectral Norm** (worst-case amplification):
$$||A||_2 = \max_{||\vec{x}||=1} ||A\vec{x}|| = \sigma_{\max}$$
- Maximum stretch factor for any unit vector
- Equals largest singular value
- Determines stability and convergence

**Why Spectral Norm Matters**:
1. **Stability**: System $x_{n+1} = Ax_n$ is stable iff $||A||_2 < 1$
2. **Error amplification**: Input error $\epsilon$ → output error ≤ $||A||_2 \cdot \epsilon$
3. **Condition number**: $\kappa = ||A||_2 \cdot ||A^{-1}||_2 = \sigma_{\max}/\sigma_{\min}$
4. **Convergence rate**: Iterations converge like $(||A||_2)^n$

**Example: Why Deep Networks Are Hard to Train**:
Consider a 10-layer network where each layer multiplies by matrix $W$:
- If $||W||_2 = 1.1$: Gradients grow as $(1.1)^{10} \approx 2.6×$
- If $||W||_2 = 0.9$: Gradients shrink as $(0.9)^{10} \approx 0.35×$
- Need $||W||_2 \approx 1$ for stable training!

This is why techniques like batch normalization and careful initialization are crucial.

 (numerical-implementation)=
## 2.6: Numerical Implementation Examples

:::{note} 💻 Implementation: Power Method for Largest Eigenvalue

**Priority: 🟢 Enrichment** - Foundation for many iterative algorithms

The power method finds the dominant eigenvalue through repeated multiplication:

```python
def power_method(A, num_iterations=100, tolerance=1e-10):
    """
    Find largest eigenvalue and corresponding eigenvector.

    Why it works: Any vector can be written as a combination
    of eigenvectors. Repeated multiplication by A amplifies
    the component along the largest eigenvector most strongly.

    Convergence rate: |λ₂/λ₁|^k where λ₁, λ₂ are largest eigenvalues
    - If λ₂/λ₁ ≈ 1: Slow convergence (many iterations)
    - If λ₂/λ₁ ≈ 0: Fast convergence (few iterations)
    """
    n = len(A)
    # Random start (likely has component along dominant eigenvector)
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)

    lambda_old = 0
    convergence_history = []

    for iteration in range(num_iterations):
        # The key step: multiply by A
        # After k steps: A^k v ≈ λ₁^k (c₁v₁ + (λ₂/λ₁)^k c₂v₂ + ...)
        # As k→∞, only v₁ term survives
        Av = A @ v

        # Normalize to prevent overflow/underflow
        v_new = Av / np.linalg.norm(Av)

        # Rayleigh quotient gives best eigenvalue estimate
        # For eigenvector: v^T A v / v^T v = λ
        lambda_est = v_new.T @ A @ v_new

        # Track convergence
        error = abs(lambda_est - lambda_old)
        convergence_history.append(error)

        if error < tolerance:
            print(f"Converged after {iteration} iterations")
            print(f"Convergence rate: {error/convergence_history[-2]:.3f}")
            break

        v = v_new
        lambda_old = lambda_est

    return lambda_est, v

# Example: Find dominant mode of coupled oscillators
# Mass-spring system: d²x/dt² = -Kx where K is stiffness matrix
K = np.array([[2, -1, 0],   # Spring between masses 1-2
              [-1, 3, -1],   # Springs on both sides of mass 2
              [0, -1, 2]])   # Spring between masses 2-3

lambda_max, v_max = power_method(K)
print(f"Highest frequency mode: ω = {np.sqrt(lambda_max):.3f}")
print(f"Mode shape: {v_max}")
# This finds the highest frequency oscillation pattern!

# Variant: Inverse power method finds SMALLEST eigenvalue
# Just apply power method to A^(-1)!
```

:::{warning} When the Power Method Fails

The power method has specific failure modes you should understand:

**1. Equal Magnitude Eigenvalues**: If $|\lambda_1| = |\lambda_2|$
- The method won't converge to a single eigenvector
- Instead, it oscillates between the eigenspaces
- Example: Rotation matrices where eigenvalues are complex conjugates with equal magnitude

**2. Complex Dominant Eigenvalues**: If $\lambda_1$ and $\lambda_2$ are complex conjugates
- The iteration vectors rotate rather than converge
- You'll see oscillatory behavior in the eigenvalue estimates
- Common in systems with rotational symmetry

**3. Defective Matrices**: When the matrix isn't diagonalizable
- Convergence becomes extremely slow or may fail entirely
- The geometric multiplicity is less than the algebraic multiplicity
- Rare in practice for physical systems

**4. Near-Degenerate Eigenvalues**: If $|\lambda_1| \approx |\lambda_2|$
- Convergence rate is proportional to $|\lambda_2/\lambda_1|^k$
- When this ratio is close to 1, you need many iterations
- Can require thousands of iterations for convergence

**Good News for Symmetric Matrices**: For real symmetric matrices (which appear frequently in physics):
- All eigenvalues are real
- The matrix is always diagonalizable
- Power method always works if $|\lambda_1| > |\lambda_2|$
- This covers covariance matrices, moment of inertia tensors, and Hamiltonians

**Alternative When Power Method Fails**: Use `np.linalg.eig()` or `scipy.linalg.eig()` which use QR algorithm — more robust but less intuitive than power iteration.
:::

:::{tip} 🌟 The More You Know: How Cholesky Decomposition Powers GPS
:class: dropdown

**Priority: 🟢 Enrichment**

Every GPS satellite continuously solves navigation equations using Kalman filters, which require Cholesky decomposition thousands of times per day. The Kalman filter updates position estimates by combining predictions with measurements, requiring the factorization of covariance matrices at each step.

André-Louis Cholesky (1875-1918) developed his decomposition method while working on geodesy and map surveying for the French military. Tragically, he died in World War I just months before the war ended, never seeing his method's full impact. His work, published posthumously in 1924, remained relatively obscure until the computer age.

The connection to GPS is profound: the Extended Kalman Filter (EKF) used in GPS receivers must update the covariance matrix P at each timestep:
$P_{k+1} = (I - K_k H_k)P_k$

where the Kalman gain $K_k$ requires solving systems involving the innovation covariance $S = HP_kH^T + R$. Cholesky decomposition makes this numerically stable—without it, rounding errors would accumulate and your GPS would drift by kilometers within hours!

Today, your smartphone performs Cholesky decomposition hundreds of times per second to fuse GPS, accelerometer, and gyroscope data, giving you meter-level positioning accuracy. Cholesky's century-old algorithm guides you home every day.

*Sources: Benoit, C. (1924). "Note sur une méthode de résolution des équations normales provenant de l'application de la méthode des moindres carrés à un système d'équations linéaires en nombre inférieur à celui des inconnues." Bulletin Géodésique, 2, 67-77; Grewal, M. S., & Andrews, A. P. (2014). "Kalman Filtering: Theory and Practice Using MATLAB" (4th ed.). Wiley.*
:::

:::{tip} 🌟 The More You Know: How SVD Revolutionized Netflix
:class: dropdown

**Priority: 🟢 Enrichment**

The Netflix Prize (2006-2009) offered $1 million to anyone who could improve their recommendation system by 10%. The winning solution? Sophisticated use of SVD to compress millions of user-movie ratings into meaningful patterns.

The problem: Netflix had a sparse matrix of 100 million ratings from 480,000 users rating 17,770 movies—a matrix that would require 8.5 billion entries if complete, but was 98.8% empty! Direct storage and computation were impossible.

SVD to the rescue: By decomposing the ratings matrix $R \approx U\Sigma V^T$ and keeping only the top k singular values (typically 20-40), teams could:
- Compress 8.5 billion potential entries into ~20 million parameters
- Identify latent factors (genres, moods, themes) automatically
- Predict missing ratings as $\hat{r}_{ui} = \vec{u}_i^T \vec{v}_j$

The "FunkSVD" algorithm by Simon Funk used gradient descent to compute SVD on sparse data without filling in missing values—a breakthrough that influenced all subsequent solutions. The final winning team "BellKor's Pragmatic Chaos" used an ensemble including multiple SVD variants.

This same SVD approach now powers recommendations at YouTube (1 billion users × millions of videos), Spotify (500 million users × 100 million songs), and every major content platform. When Netflix suggests your next binge-watch, it's using the same linear algebra you're learning now!

*Sources: Bennett, J., & Lanning, S. (2007). "The Netflix Prize." Proceedings of KDD Cup and Workshop; Koren, Y., Bell, R., & Volinsky, C. (2009). "Matrix Factorization Techniques for Recommender Systems." Computer, 42(8), 30-37.*
:::

:::{important} 🔌 Key Takeaway

These advanced topics aren't just mathematical curiosities—they're the computational workhorses of modern astrophysics:

- **SVD** reveals hidden structure and enables massive data compression (galaxy spectra, CMB analysis)
- **Block matrices** exploit natural hierarchies to solve huge systems efficiently  
- **Jacobians** determine stability of everything from orbits to numerical methods
- **Matrix exponentials** solve linear evolution exactly—the foundation for understanding nonlinear dynamics
- **Matrix norms** quantify stability, convergence, and error propagation
- **Power method** underlies iterative algorithms from PageRank to finding vibrational modes

The beauty is that these tools interconnect: SVD uses eigenvalues, matrix exponentials need eigendecomposition, stability analysis uses Jacobians and norms together. Master these connections and you'll see how a small set of linear algebra concepts powers all of computational astrophysics.

As you progress through projects, return to these sections—concepts that seem abstract now will crystallize when you need them to debug unstable orbits or understand why your neural network won't converge.
:::

---

## Part 3: Numerical Reality - When Mathematics Meets Silicon

**Priority: 🔴 Essential** - Critical for debugging all projects

:::{admonition} 📅 When You'll Use This
:class: dropdown, hint

**Needed from**: Day 1 of coding
**Most critical for**: Debugging numerical errors
**Returns in**: Every project when things go wrong

Read this section early and refer back when debugging.
:::

:::{admonition} 🔭 Where We're Going
:class: note

Pure mathematics assumes infinite precision, but computers work with finite bits. This section reveals the harsh realities of floating-point arithmetic and teaches you to recognize and fix numerical disasters before they ruin your simulations. These aren't edge cases—you WILL encounter these issues in your projects.
:::

### 7.1 Condition Numbers Revisited: Statistical Context {#condition-numbers}

Building on Module 0a's introduction to condition numbers, let's explore their specific implications for statistical computations:

**Condition Numbers in Statistical Methods**:

For covariance matrices, the condition number has special meaning:
$$\kappa(\Sigma) = \frac{\lambda_{\max}}{\lambda_{\min}}$$

This ratio tells you:
- **Near 1**: Variables have similar scales and low correlation
- **Large**: Either variables have vastly different scales OR near-perfect correlation
- **Infinite**: Perfect correlation (singular covariance)

**MCMC Implications (Project 4)**:
```python
# Poorly conditioned proposal covariance slows convergence
Sigma_bad = np.array([[1, 0.999], [0.999, 1]])  # κ ≈ 2000
# MCMC needs ~κ steps to explore the distribution

# Well-conditioned after reparameterization
L = np.linalg.cholesky(Sigma_bad)
# Sample in transformed space where κ = 1, then transform back
```

**GP Implications (Project 5)**:
```python
# Kernel matrices become ill-conditioned when:
# 1. Data points are very close (duplicate measurements)
# 2. Length scale is too small (overfitting)
# 3. Noise term is too small (numerical instability)

# Check your GP's condition number:
kappa = np.linalg.cond(K)
if kappa > 1e12:
    print("Warning: GP may give nonsense predictions!")
    # Solutions:
    # - Increase noise term σ²
    # - Remove duplicate points
    # - Adjust length scale
```

### 7.2 When Statistical Computations Fail

Understanding failure modes specific to statistical methods helps you recognize and fix problems:

**Covariance Matrix Not Positive Semi-Definite**:
```python
# Computing sample covariance with insufficient data
n_samples = 3
n_features = 5  # More features than samples!

X = np.random.randn(n_samples, n_features)
Sigma = np.cov(X.T)  # Shape: (5, 5)

# This is rank-deficient: rank ≤ min(n_samples-1, n_features) = 2
print(f"Rank: {np.linalg.matrix_rank(Sigma)}")  # 2, not 5!

# Cholesky will fail:
try:
    L = np.linalg.cholesky(Sigma)
except np.linalg.LinAlgError:
    print("Covariance is singular!")

    # Fix: Regularization (add prior belief about variance)
    Sigma_reg = Sigma + 0.01 * np.eye(n_features)
    L = np.linalg.cholesky(Sigma_reg)  # Now works
```

**Numerical Underflow in Likelihoods**:
```python
# Computing likelihood of many data points
log_likelihoods = []
for x in data:
    # BAD: Probability underflows to zero
    p = multivariate_normal.pdf(x, mu, Sigma)

    # GOOD: Work in log space
    log_p = multivariate_normal.logpdf(x, mu, Sigma)
    log_likelihoods.append(log_p)

# Sum log-likelihoods instead of multiplying probabilities
total_log_likelihood = np.sum(log_likelihoods)
```

**Cholesky Decomposition Failures**:
```python
def safe_cholesky(A, max_tries=5):
    """
    Robust Cholesky with automatic regularization.
    """
    jitter = 1e-6

    for i in range(max_tries):
        try:
            L = np.linalg.cholesky(A + jitter * np.eye(len(A)))
            return L
        except np.linalg.LinAlgError:
            if i == max_tries - 1:
                # Last resort: eigenvalue thresholding
                eigvals, eigvecs = np.linalg.eigh(A)
                eigvals = np.maximum(eigvals, jitter)
                A_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T
                return np.linalg.cholesky(A_fixed)
            else:
                jitter *= 10  # Increase regularization

    return None
```

### 7.3 Statistical-Specific Numerical Guidelines

:::{admonition} 🔧 Debugging Workflow: When Cholesky Fails
:class: important

Follow this systematic workflow when encountering Cholesky decomposition failures:

```python
def debug_cholesky_failure(A):
    """Systematic debugging when np.linalg.cholesky(A) fails."""
    
    print("=== Cholesky Debugging Workflow ===")
    
    # Step 1: Check symmetry
    asymmetry = np.max(np.abs(A - A.T))
    print(f"1. Symmetry check: max|A - A^T| = {asymmetry:.2e}")
    if asymmetry > 1e-10:
        print("   FIX: A = (A + A.T) / 2")
        A = (A + A.T) / 2

    # Step 2: Check diagonal elements
    min_diag = np.min(np.diag(A))
    print(f"2. Diagonal check: min(diag(A)) = {min_diag:.2e}")
    if min_diag <= 0:
        print("   ERROR: Non-positive diagonal elements!")
        return None

    # Step 3: Check eigenvalues
    eigvals = np.linalg.eigvalsh(A)
    print(f"3. Eigenvalue range: [{eigvals.min():.2e}, {eigvals.max():.2e}]")

    # Step 4: Check condition number
    cond = eigvals.max() / max(eigvals.min(), 1e-15)
    print(f"4. Condition number: {cond:.2e}")

    # Step 5: Apply fixes based on diagnosis
    if eigvals.min() < -1e-10:
        print("   FIX: Matrix is not PSD. Using eigenvalue thresholding...")
        eigvecs = np.linalg.eigh(A)[1]
        eigvals = np.maximum(eigvals, 1e-10)
        A = eigvecs @ np.diag(eigvals) @ eigvecs.T
    elif eigvals.min() < 1e-10:
        print("   FIX: Near-singular. Adding regularization...")
        A = A + 1e-6 * np.eye(len(A))
    
    # Step 6: Retry Cholesky
    try:
        L = np.linalg.cholesky(A)
        print("✓ Cholesky successful after fixes!")
        return L
    except np.linalg.LinAlgError:
        print("✗ Still failing. Consider stronger regularization or SVD approach.")
        return None
```

**Quick Decision Tree**:
1. Symmetry error? → Force symmetry
2. Negative diagonal? → Data/math error, check upstream
3. Negative eigenvalues? → Eigenvalue thresholding
4. Tiny eigenvalues? → Add regularization
5. Large condition number? → Standardize data or reformulate
:::

:::{admonition} 🔧 Best Practices for Statistical Computations
:class: important

**Always Work in Log Space for Probabilities**:
```python
# BAD: Product of probabilities
prob = 1.0
for p in probabilities:
    prob *= p  # Underflows to 0

# GOOD: Sum of log probabilities
log_prob = 0.0
for p in probabilities:
    log_prob += np.log(p)
```

**Use Stable Parameterizations**:
```python
# BAD: Parameterize by standard deviation
sigma = optimizer.optimize(sigma_init)

# GOOD: Parameterize by log(sigma)
log_sigma = optimizer.optimize(np.log(sigma_init))
sigma = np.exp(log_sigma)  # Always positive!
```

**Standardize Your Data**:
```python
# BAD: Raw features with different scales
X = data  # columns might range from 0.001 to 1000000

# GOOD: Standardized features
X = (data - data.mean(axis=0)) / data.std(axis=0)
# Now all features have mean=0, std=1
# Covariance matrix will be well-conditioned
```

**Monitor Numerical Health**:
```python
def check_matrix_health(A, name="Matrix"):
    """
    Diagnostic function for matrix numerical health.
    """
    print(f"\n{name} Health Check:")
    print(f"  Shape: {A.shape}")
    print(f"  Rank: {np.linalg.matrix_rank(A)}")
    print(f"  Condition number: {np.linalg.cond(A):.2e}")
    
    eigvals = np.linalg.eigvalsh(A)
    print(f"  Eigenvalue range: [{eigvals.min():.2e}, {eigvals.max():.2e}]")
    
    if eigvals.min() < 0:
        print(f"  ⚠️ WARNING: Negative eigenvalues detected!")
    if np.linalg.cond(A) > 1e10:
        print(f"  ⚠️ WARNING: Poorly conditioned!")
```

**Library Choice Guidance**:

| Library | When to Use | Why |
|---------|------------|-----|
| `numpy.linalg` | Quick prototyping, small matrices | Convenient, always available |
| `scipy.linalg` | Production code, edge cases | More robust algorithms, better error handling |
| `scipy.sparse` | Sparse matrices (>90% zeros) | Memory efficient, specialized algorithms |
| `sklearn` | Machine learning pipelines | Integrated preprocessing, cross-validation |
| `JAX` | Differentiable operations | Autodiff, JIT compilation, GPU acceleration |

**Performance Profiling Notes**:

Cholesky decomposition has O(n³/3) complexity but with excellent cache performance. Here's why it beats other factorizations:

| Operation | Complexity | Cache Performance | When to Use |
|-----------|------------|-------------------|-------------|
| Cholesky | O(n³/3) | Excellent | Positive definite systems |
| LU | O(2n³/3) | Good | General square systems |
| QR | O(2n³) | Fair | Least squares, rank-deficient |
| Eigendecomposition | O(10n³) | Poor | Need all eigenvalues/vectors |
| SVD | O(11n³) | Poor | Rank analysis, pseudoinverse |

The factor of 3 difference between Cholesky and LU matters: for n=1000, Cholesky needs ~167 million operations vs 667 million for LU!
:::

:::{admonition} 🚀 Looking Ahead: From Statistical to Deep Learning
:class: note

The concepts in this module directly extend to cutting-edge research:

**Gaussian Processes → Neural Tangent Kernels**: Recent work shows that infinitely wide neural networks behave exactly like Gaussian Processes with specific kernels. Your GP understanding directly transfers to understanding deep learning theory!

**Covariance Matrices → Attention Mechanisms**: The attention matrices in transformers (like GPT) are essentially learned covariance structures that capture which tokens should "pay attention" to each other.

**SVD → Model Compression**: Modern large language models use SVD-based techniques to compress billion-parameter models to run on phones while maintaining performance.

**Matrix Exponentials → Neural ODEs**: Instead of discrete layers, Neural ODEs use continuous transformations via matrix exponentials, enabling memory-efficient deep networks.

These aren't distant connections—they're active research areas where your linear algebra foundation enables breakthrough science!
:::

:::{warning} ⚠️ Failure Case Study: The Ariane 5 Explosion
:class: warning

On June 4, 1996, the European Space Agency's Ariane 5 rocket exploded 39 seconds after launch, destroying $370 million of satellites. The cause? A floating-point overflow in the navigation software.

The horizontal velocity value (a 64-bit float) was converted to a 16-bit signed integer. When the velocity exceeded 32,767 (the maximum for 16-bit signed integers), the conversion caused an overflow, leading to a hardware exception. The backup system had the same bug, so both failed simultaneously.

**Lessons for your projects**:
1. **Check value ranges**: Before type conversions, verify values fit in the target type
2. **Test edge cases**: The Ariane 4 software worked fine—Ariane 5's faster acceleration triggered the bug
3. **Don't assume backup = different**: Redundant systems with identical code have identical bugs
4. **Understand your precision limits**: Know when float32 vs float64 matters

In your projects:
- Project 2: Check for position overflows in long integrations
- Project 4: Monitor log-probability underflows in MCMC
- Project 5: Watch for precision loss in badly-scaled kernels

*Source: Lions, J. L. (1996). ["Ariane 5 Flight 501 Failure: Report by the Inquiry Board."](http://sunnyday.mit.edu/nasa-class/Ariane5-report.html) European Space Agency.*
:::

---

## Part 4: Bridge to Machine Learning

**Priority: 🟡 Important** - Helps see the big picture

:::{admonition} 📅 When You'll Use This
:class: dropdown, hint

Read this section when transitioning between course phases to understand connections. Return to it after Projects 1-3 to see how classical methods connect to modern ML.
:::

### 8.1 From Classical to Statistical to Learning

Linear algebra provides the mathematical continuity across your entire journey. Watch how the same mathematical objects evolve in meaning as you progress through different computational paradigms:

**The Evolution of Mathematical Objects**:

| Mathematical Object | Classical Physics (Projects 1-3) | Statistical Methods (Projects 4-5) | Machine Learning (Final Project) |
|-------------------|----------------------------------|-------------------------------------|----------------------------------|
| **Vectors** | Positions, velocities, forces | Parameter samples, data points | Feature vectors, gradients |
| **Matrices** | Transformations, rotations | Covariance, kernels | Weight matrices, Jacobians |
| **Eigenvalues** | Stability, oscillation modes | Convergence rates, principal components | Learning rates, network dynamics |
| **Dot products** | Work, projections | Correlations, similarities | Attention scores, kernels |
| **Norms** | Distances, magnitudes | Errors, uncertainties | Loss functions, regularization |
| **Decompositions** | Solving dynamics | Statistical inference | Network compression, analysis |

This isn't coincidence—it's the deep unity of mathematics. The same linear algebra that predicts planetary orbits also powers Google's search algorithm and ChatGPT's language understanding.

### 8.2 Matrix Calculus for Neural Networks {#matrix-calculus-nn}

**Priority: 🟡 Important for Final Project**

Your final project requires understanding how gradients flow through matrix operations. Here's the essential matrix calculus:

**Basic Matrix Derivatives**:

For scalar function $f$ of matrix $W$:
$$\frac{\partial f}{\partial W} \text{ is a matrix with } \left[\frac{\partial f}{\partial W}\right]_{ij} = \frac{\partial f}{\partial W_{ij}}$$

**Key Results You'll Need**:

1. **Linear layer**: $f(W) = W\vec{x}$
   $$\frac{\partial}{\partial W}(W\vec{x}) = \vec{x}^T$$

2. **Quadratic form**: $f(W) = \vec{x}^T W \vec{x}$
   $$\frac{\partial}{\partial W}(\vec{x}^T W \vec{x}) = \vec{x}\vec{x}^T$$

3. **Frobenius norm**: $f(W) = ||W||_F^2 = \text{trace}(W^T W)$
   $$\frac{\partial}{\partial W}||W||_F^2 = 2W$$

**Chain Rule for Matrices**:

For composition $f(g(W))$:
$$\frac{\partial f}{\partial W_{ij}} = \sum_{k,l} \frac{\partial f}{\partial g_{kl}} \frac{\partial g_{kl}}{\partial W_{ij}}$$

This is what happens during backpropagation—gradients flow backward through the network via chain rule!

**Example: Simple Two-Layer Network**:

```python
# Forward pass:
# Layer 1: z₁ = W₁x + b₁
# Activation: a₁ = relu(z₁)
# Layer 2: z₂ = W₂a₁ + b₂
# Loss: L = ||z₂ - y||²

# Backward pass (what JAX computes automatically):
# ∂L/∂z₂ = 2(z₂ - y)
# ∂L/∂W₂ = (∂L/∂z₂) @ a₁ᵀ
# ∂L/∂a₁ = W₂ᵀ @ (∂L/∂z₂)
# ∂L/∂z₁ = (∂L/∂a₁) ⊙ relu'(z₁)  # Element-wise product
# ∂L/∂W₁ = (∂L/∂z₁) @ xᵀ

# The pattern: gradients with respect to weights = (upstream gradient) @ (input)ᵀ
```

### 8.3 Connecting Everything: The Big Picture

The techniques in this module power every major simulation and discovery in modern astrophysics:

**Your Learning Journey**:
1. **Classical** (Projects 1-3): Deterministic systems, exact solutions
2. **Statistical** (Projects 4-5): Uncertainty quantification, probabilistic inference
3. **Learning** (Final Project): Pattern discovery, function approximation

**The Mathematical Thread**:
- Same linear algebra throughout
- Increasing complexity of applications
- Growing appreciation for numerical stability
- Deepening understanding of connections

**Why This Matters**:
Every breakthrough in computational astrophysics builds on these foundations:
- **Gaia**: 1 billion stars → massive covariance matrices
- **LIGO**: Gravitational waves → matched filtering in high dimensions
- **JWST**: Spectroscopy → dimensionality reduction via SVD
- **Vera Rubin**: 20 TB/night → statistical methods at scale

---

## Numerical Recipes Quick Reference

:::{tip} 🔧 Copy-Paste Solutions for Common Problems

**When Matrices Misbehave - Immediate Fixes**:

```python
# Force symmetry (when you know A should be symmetric)
A_sym = (A + A.T) / 2

# Add jitter for positive definiteness
A_stable = A + 1e-6 * np.eye(len(A))

# Robust Cholesky with automatic jitter
def safe_cholesky(A, initial_jitter=1e-6):
    jitter = initial_jitter
    max_tries = 5

    for i in range(max_tries):
        try:
            L = np.linalg.cholesky(A + jitter * np.eye(len(A)))
            return L
        except np.linalg.LinAlgError:
            jitter *= 10

    # Last resort: eigenvalue thresholding
    eigvals, eigvecs = np.linalg.eigh(A)
    eigvals = np.maximum(eigvals, initial_jitter)
    A_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T
    return np.linalg.cholesky(A_fixed)

# Work in log space for probabilities
log_prob = multivariate_normal.logpdf(x, mu, Sigma)  # Not .pdf()!

# Stable parameterization for optimization
log_sigma = optimizer.param  # Optimize log
sigma = np.exp(log_sigma)    # Always positive!

# Standardize data before any statistical analysis
X_std = (X - X.mean(axis=0)) / X.std(axis=0)

# Robust matrix inversion via SVD
def robust_inverse(A, threshold=1e-10):
    U, s, Vt = np.linalg.svd(A)
    s_inv = np.where(s > threshold * s.max(), 1/s, 0)
    return Vt.T @ np.diag(s_inv) @ U.T

# Check before trusting
def is_positive_definite(A):
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False
```

**Emergency Diagnostics**:
```python
def matrix_health_report(A):
    """Quick health check - run this when things break."""
    print(f"Shape: {A.shape}")
    print(f"Symmetric: {np.allclose(A, A.T)}")
    print(f"Condition: {np.linalg.cond(A):.2e}")

    if A.shape[0] == A.shape[1]:  # Square matrix
        eigvals = np.linalg.eigvalsh(A) if np.allclose(A, A.T) else np.linalg.eigvals(A)
        print(f"Eigenvalues: [{np.min(eigvals):.2e}, {np.max(eigvals):.2e}]")
        print(f"Positive definite: {np.all(eigvals > 0)}")
```
:::

---

## Glossary of Terms

All terms introduced in this module, arranged alphabetically:

- **back substitution**: Solving upper triangular systems from bottom to top, used in the second phase of solving systems via Cholesky decomposition
- **block matrix**: Matrix partitioned into submatrices, often reflecting natural system structure (e.g., strong/weak interactions in multi-body systems)
- **Cholesky decomposition**: Factorization of a positive definite matrix $A = LL^T$ where $L$ is lower triangular with positive diagonal entries; geometrically finds the "square root" of a positive definite matrix
- **condition number**: For statistical context: $\kappa(A) = \sigma_{\max}/\sigma_{\min}$, ratio of largest to smallest singular value; measures how much errors amplify in statistical computations
- **covariance**: Measure of how two variables change together; positive means they increase together, negative means one increases as the other decreases, zero means no linear relationship
- **covariance matrix**: Matrix $\Sigma$ containing all pairwise covariances between random variables; $\Sigma_{ij} = \text{Cov}(X_i, X_j)$; encodes all linear relationships in your data
- **forward substitution**: Solving lower triangular systems from top to bottom, used in the first phase of solving systems via Cholesky decomposition
- **Frobenius norm**: Matrix norm defined as $||A||_F = \sqrt{\sum_{i,j} |a_{ij}|^2}$; treats matrix like a vector and sums all squared elements
- **Jacobian**: Matrix of all first-order partial derivatives $J_{ij} = \partial f_i/\partial x_j$; represents the best linear approximation of a vector function at a point
- **Mahalanobis distance**: Scale-invariant distance that accounts for correlations: $d = \sqrt{(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})}$; measures "how many standard deviations away" in correlated space
- **matrix exponential**: The operator $e^{At}$ that propagates linear systems forward in time; solution to $\dot{x} = Ax$ is $x(t) = e^{At}x(0)$
- **multivariate Gaussian**: Multi-dimensional generalization of the bell curve, defined by mean vector $\mu$ and covariance matrix $\Sigma$; probability density involves $\exp(-\frac{1}{2}(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu}))$
- **positive definite**: Property of a symmetric matrix where $\vec{x}^T A \vec{x} > 0$ for all $\vec{x} \neq \vec{0}$; ensures energies are positive and covariances are valid
- **positive semi-definite**: Property of a symmetric matrix where $\vec{x}^T A \vec{x} \geq 0$ for all $\vec{x}$; allows for zero eigenvalues (rank deficiency)
- **precision matrix**: Inverse of the covariance matrix: $\Sigma^{-1}$; encodes conditional independence structure (zero entries indicate conditional independence)
- **pseudoinverse**: Generalized inverse $A^+ = V\Sigma^+ U^T$ obtained via SVD; gives least-squares solution for overdetermined systems and minimum-norm solution for underdetermined systems
- **quadratic form**: Expression $Q(\vec{x}) = \vec{x}^T A \vec{x}$ where $A$ is symmetric; represents energies, distances, and other positive quantities in physics
- **regularization**: Adding small positive values (often to diagonal elements) to improve numerical stability or prevent singularities; balances stability with bias
- **Schur complement**: The "effective" matrix after eliminating some variables: $S = A - BD^{-1}C$; represents how eliminated variables influence remaining ones
- **singular values**: Non-negative values $\sigma_1 \geq \sigma_2 \geq ... \geq 0$ from SVD; measure importance/variance explained by each component
- **spectral norm**: Matrix norm defined as $||A||_2 = \sigma_{\max}$; equals maximum amplification factor for any unit vector
- **SVD (Singular Value Decomposition)**: Universal matrix factorization $A = U\Sigma V^T$ that reveals the fundamental action of any matrix as rotate-stretch-rotate

---

## Main Takeaways

:::{admonition} 🎯 Essential Points to Remember
:class: important

This module bridged classical linear algebra with statistical methods and machine learning:

1. **Positive definite matrices guarantee physical validity** - they ensure energies are positive, distances are non-negative, and probability distributions are valid

2. **Covariance matrices encode all linear relationships** between random variables, with diagonal elements as variances and off-diagonal as covariances

3. **Cholesky decomposition is the bridge** between uncorrelated randomness and structured correlations - essential for sampling and solving

4. **Numerical precision is finite** - always check condition numbers, work in log space for probabilities, and add regularization when needed

5. **Advanced decompositions reveal hidden structure** - SVD for dimensionality reduction, Schur complement for efficient updates, Jacobian for stability analysis

6. **Matrix calculus underlies neural networks** - gradients flow through matrix operations via the chain rule during backpropagation

7. **Statistical computations require special care** - work in log space, use stable parameterizations, standardize data, monitor numerical health

8. **The same mathematics spans all domains** - eigenvalues determine both orbital stability and MCMC convergence rates

Master these concepts and you're ready for the statistical challenges of Projects 4-6!
:::

---

## Essential NumPy/SciPy Reference for Module 0b

**Priority: 🔴 Essential** - Keep this open while coding Projects 4-6

```{list-table} Statistical Linear Algebra Functions
:header-rows: 1

* - Task
  - Function
  - When to Use
  - Project
* - Cholesky decomposition
  - `np.linalg.cholesky(A)`
  - Positive definite systems
  - P4-5
* - Check positive definite
  - `np.linalg.eigvalsh(A).min() > 0`
  - Before Cholesky
  - P4-5
* - Sample covariance
  - `np.cov(X.T)`
  - Compute from data
  - P4
* - Multivariate normal
  - `scipy.stats.multivariate_normal`
  - Sampling, likelihood
  - P4-5
* - Log probability
  - `.logpdf()` not `.pdf()`
  - Avoid underflow
  - P4-5
* - Pseudoinverse
  - `np.linalg.pinv(A)`
  - Rank-deficient systems
  - P5
* - SVD
  - `np.linalg.svd(A)`
  - Decomposition, PCA
  - All
* - Matrix exponential
  - `scipy.linalg.expm(A)`
  - Time evolution
  - P2,5
* - Force symmetry
  - `(A + A.T) / 2`
  - Fix rounding errors
  - P4-5
* - Add regularization
  - `A + lambda * np.eye(n)`
  - Improve conditioning
  - P4-5
```

```{list-table} Numerical Stability Patterns
:header-rows: 1

* - Problem
  - Solution
  - Code Pattern
* - Cholesky fails
  - Add jitter
  - `K + 1e-6 * np.eye(n)`
* - Negative eigenvalues
  - Threshold to zero
  - `np.maximum(eigvals, 0)`
* - Probability underflow
  - Work in log space
  - Use `logpdf`, sum logs
* - Ill-conditioned
  - Regularize
  - Add to diagonal
* - Not symmetric
  - Force symmetry
  - `(A + A.T) / 2`
* - Different scales
  - Standardize
  - `(X - mean) / std`
```

---

## Quick Reference Card

:::{admonition} 📋 Statistical Linear Algebra Quick Reference
:class: tip

### Positive Definiteness
- Test: All eigenvalues > 0
- Fix: Add jitter `A + 1e-6 * I`
- Check: `np.linalg.eigvalsh(A).min() > 0`

### Covariance Matrices
- Diagonal: Variances
- Off-diagonal: Covariances  
- Always symmetric and PSD
- Correlation: `ρ = Σᵢⱼ/√(ΣᵢᵢΣⱼⱼ)`

### Multivariate Gaussian
- PDF: `N(μ, Σ)`
- Sample: `x = μ + L @ randn()` where `L = cholesky(Σ)`
- Log-likelihood: Use `logpdf` to avoid underflow

### Numerical Guidelines
- Always check condition numbers
- Work in log space for probabilities
- Standardize data before analysis
- Monitor eigenvalue ranges

### Key Functions
```python
np.linalg.cholesky()    # Cholesky decomposition
np.linalg.eigvalsh()    # Eigenvalues (symmetric)
np.linalg.cond()        # Condition number
np.linalg.lstsq()       # Least squares
scipy.linalg.expm()     # Matrix exponential
```
:::

---

*With these foundations, you're equipped to tackle the statistical and machine learning challenges ahead!*