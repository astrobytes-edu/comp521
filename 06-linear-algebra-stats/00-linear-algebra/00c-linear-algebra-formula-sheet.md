---
title: "Module 1c: Linear Algebra Formula Sheet"
subtitle: "Mathematical Foundations | ASTR 596: Modeling the Universe"
exports:
  - format: pdf
---

## Module 0a Quick Formula Sheet

### Essential Vector Operations

**Dot Product:**

$$\vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z = |\vec{a}||\vec{b}|\cos\theta$$

**Physical Applications:**

- Work: $W = \vec{F} \cdot \vec{d}$
- Power: $P = \vec{F} \cdot \vec{v}$
- Projection of $\vec{a}$ onto $\vec{b}$: $\text{proj}_{\vec{b}}\vec{a} = \frac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2}\vec{b}$

**Cross Product:**

$$\vec{a} \times \vec{b} = \begin{pmatrix} a_y b_z - a_z b_y \\ a_z b_x - a_x b_z \\ a_x b_y - a_y b_x \end{pmatrix}$$

**Magnitude:** $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$

**Physical Applications:**

- Angular momentum: $\vec{L} = \vec{r} \times \vec{p}$
- Torque: $\vec{\tau} = \vec{r} \times \vec{F}$
- Area of parallelogram: $A = |\vec{a} \times \vec{b}|$

**Vector Norms and Properties:**

- Magnitude: $|\vec{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}$
- Unit vector: $\hat{v} = \vec{v}/|\vec{v}|$
- Orthogonal if: $\vec{a} \cdot \vec{b} = 0$

### Essential Matrix Operations

**Basic Operations:**

- Matrix multiplication: $(AB)_{ij} = \sum_k A_{ik}B_{kj}$
- Transpose: $(A^T)_{ij} = A_{ji}$
- Identity: $I\vec{x} = \vec{x}$ for all $\vec{x}$

**Determinant:**

**2×2 Matrix:**
$$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

**Properties:**

- $\det(AB) = \det(A)\det(B)$
- $\det(A^T) = \det(A)$
- $\det(A^{-1}) = 1/\det(A)$
- Singular if $\det(A) = 0$

**Matrix Inverse:**

**2×2 Matrix:**
$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = \frac{1}{ad-bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

**General Properties:**

- $(AB)^{-1} = B^{-1}A^{-1}$
- $(A^T)^{-1} = (A^{-1})^T$
- $(A^{-1})^{-1} = A$

### Eigenvalues and Eigenvectors

**Definition:**
$$A\vec{v} = \lambda\vec{v}$$

**Characteristic Equation:**
$$\det(A - \lambda I) = 0$$

**Properties:**

- Trace: $\text{tr}(A) = \sum_i A_{ii} = \sum_i \lambda_i$
- Determinant: $\det(A) = \prod_i \lambda_i$
- For symmetric matrices: all eigenvalues are real

## Numerical Stability Quick Checks

### Condition Number

$$\kappa(A) = ||A|| \cdot ||A^{-1}|| = \frac{\sigma_{\max}}{\sigma_{\min}}$$

**Interpretation:**

- $\kappa < 10$: Excellent
- $10 < \kappa < 10^3$: Good
- $10^3 < \kappa < 10^6$: Use caution
- $\kappa > 10^6$: Ill-conditioned

### Machine Epsilon

- Float64: $\epsilon \approx 2.2 \times 10^{-16}$
- Float32: $\epsilon \approx 1.2 \times 10^{-7}$

## Python/NumPy Quick Reference

```python
# Vectors
np.dot(a, b)              # Dot product
np.cross(a, b)            # Cross product
np.linalg.norm(v)         # Vector magnitude

# Matrices
A @ B                     # Matrix multiplication
A.T                       # Transpose
np.linalg.inv(A)          # Inverse (avoid!)
np.linalg.solve(A, b)     # Solve Ax = b (preferred)
np.linalg.det(A)          # Determinant
np.linalg.eig(A)          # Eigenvalues & eigenvectors
np.linalg.cond(A)         # Condition number

# Numerical fixes
A_sym = (A + A.T) / 2     # Force symmetry
A_reg = A + eps * I       # Regularization
```

---

## Module 0b Quick Formula Sheet

### Positive Definite Matrices

**Definition**
A symmetric matrix $A$ is positive definite if:
$$\vec{x}^T A \vec{x} > 0 \quad \forall \vec{x} \neq \vec{0}$$

**Tests for Positive Definiteness:**

1. All eigenvalues > 0
2. All leading principal minors > 0
3. Cholesky decomposition exists
4. Can write as $A = B^TB$ for invertible $B$

**Quadratic Forms:**

$$Q(\vec{x}) = \vec{x}^T A \vec{x} = \sum_{i,j} A_{ij} x_i x_j$$

**Physical Examples:**
- Kinetic energy: $T = \frac{1}{2}\vec{v}^T M \vec{v}$
- Potential energy: $V = \frac{1}{2}\vec{x}^T K \vec{x}$

### Covariance and Statistical Matrices

**Covariance:**
$$\text{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)] = E[XY] - E[X]E[Y]$$

**Correlation:**
$$\rho_{XY} = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y}$$

**Covariance Matrix:**
$$\Sigma_{ij} = \text{Cov}(X_i, X_j)$$

**Properties:**

- Diagonal: $\Sigma_{ii} = \text{Var}(X_i)$
- Symmetric: $\Sigma_{ij} = \Sigma_{ji}$
- Positive semi-definite: all eigenvalues ≥ 0

**Sample Covariance:**

$$\Sigma = \frac{1}{n-1} \sum_{i=1}^n (\vec{x}_i - \bar{\vec{x}})(\vec{x}_i - \bar{\vec{x}})^T$$

Or in matrix form:
$$\Sigma = \frac{1}{n-1} X_c^T X_c$$
where $X_c$ is centered data matrix

### Multivariate Gaussian Distribution

**Probability Density:**
$$p(\vec{x}) = \frac{1}{(2\pi)^{n/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})\right)$$

**Mahalanobis Distance:**
$$d_M(\vec{x}) = \sqrt{(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})}$$

**Log-likelihood** (numerical stability)
$$\log p(\vec{x}) = -\frac{n}{2}\log(2\pi) - \frac{1}{2}\log|\Sigma| - \frac{1}{2}(\vec{x}-\vec{\mu})^T\Sigma^{-1}(\vec{x}-\vec{\mu})$$

### Matrix Decompositions

**Cholesky Decomposition**
For positive definite $A$:
$$A = LL^T$$
where $L$ is lower triangular with positive diagonal

**Applications:**

- Solving: $A\vec{x} = \vec{b}$ via $L\vec{y} = \vec{b}$, then $L^T\vec{x} = \vec{y}$
- Sampling: If $\vec{z} \sim N(0,I)$, then $\vec{\mu} + L\vec{z} \sim N(\vec{\mu}, \Sigma)$

**Singular Value Decomposition (SVD)**
$$A = U\Sigma V^T$$

**Components:**

- $U$: Left singular vectors (orthonormal)
- $\Sigma$: Singular values (diagonal, non-negative)
- $V^T$: Right singular vectors (orthonormal)

**Pseudoinverse:**
$$A^+ = V\Sigma^+ U^T$$
where $\Sigma^+$ inverts non-zero singular values

### Advanced Topics

**Matrix Exponential**
$$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$

**Solution to linear ODE:**
$$\frac{d\vec{x}}{dt} = A\vec{x} \implies \vec{x}(t) = e^{At}\vec{x}(0)$$

**Jacobian Matrix**
$$J_{ij} = \frac{\partial f_i}{\partial x_j}$$

**Linear approximation:**
$$\vec{f}(\vec{x} + \delta\vec{x}) \approx \vec{f}(\vec{x}) + J\delta\vec{x}$$

**Schur Complement**
For block matrix $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$:
$$S = A - BD^{-1}C$$

### Matrix Norms

**Frobenius Norm**
$$||A||_F = \sqrt{\sum_{i,j} |a_{ij}|^2} = \sqrt{\text{tr}(A^T A)}$$

**Spectral Norm**
$$||A||_2 = \max_{||\vec{x}||=1} ||A\vec{x}|| = \sigma_{\max}$$

### Numerical Stability Patterns

**Safe Numerical Practices:**

```python
# Cholesky with automatic regularization
def safe_cholesky(A, jitter=1e-6):
    try:
        return np.linalg.cholesky(A + jitter * np.eye(len(A)))
    except:
        eigvals, eigvecs = np.linalg.eigh(A)
        eigvals = np.maximum(eigvals, jitter)
        A_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T
        return np.linalg.cholesky(A_fixed)

# Work in log space
log_prob = multivariate_normal.logpdf(x, mu, Sigma)

# Stable parameterization
log_param = optimizer.param
param = np.exp(log_param)  # Always positive

# Standardize data
X_std = (X - X.mean(axis=0)) / X.std(axis=0)
```

**Common Fixes:**

| Problem | Solution |
|---------|----------|
| Cholesky fails | Add jitter: `A + 1e-6 * I` |
| Not symmetric | Force: `(A + A.T) / 2` |
| Ill-conditioned | Regularize diagonal |
| Probability underflow | Use log space |
| Negative eigenvalues | Threshold: `np.maximum(eigvals, 0)` |

### Python/SciPy Quick Reference

```python
# Statistical
np.cov(X.T)                          # Covariance matrix
scipy.stats.multivariate_normal      # Multivariate Gaussian
.logpdf(x, mean, cov)                # Log probability

# Decompositions
np.linalg.cholesky(A)                # Cholesky (A must be PD)
np.linalg.svd(A)                     # SVD
scipy.linalg.expm(A)                 # Matrix exponential

# Checks
np.linalg.eigvalsh(A).min() > 0      # Is positive definite?
np.allclose(A, A.T)                  # Is symmetric?
np.linalg.cond(A)                    # Condition number

# Solving systems
np.linalg.solve(A, b)                # When A is square
np.linalg.lstsq(A, b)                # Least squares
np.linalg.pinv(A)                    # Pseudoinverse
```
