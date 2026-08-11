---
title: "Module 1a: Core Linear Algebra for Computational Astrophysics"
subtitle: "Mathematical Foundations | ASTR 596: Modeling the Universe"
exports:
  - format: pdf
---

## Quick Navigation Guide

### 📚 Choose Your Learning Path

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} 🏃 **Fast Track**
Just starting the course? Read only sections marked with 🔴

- [Linear Algebra Overview](#overview)
- [Vectors Essentials](#part-2-vectors)
- [Matrix Fundamentals](#part-3-matrices)
- [Numerics](#part-5-numerics)
- [Quick Reference](#quickref)
:::

:::{grid-item-card} 🚶 **Standard Path**
Preparing for projects? Read 🔴 and 🟡 sections

- Everything in Fast Track, plus:
- [Eigenvalues & Eigenvectors](#part-4-eigenvalues)
- [Implementation Examples](#numerical-implementation)
:::

:::{grid-item-card} 🧗 **Complete Path**
Want deep understanding? Read all sections including 🟢

- Complete module with:
- Historical contexts
- Mathematical proofs
- All worked examples
:::
::::

### 🎯 Navigation by Project Needs

:::{important} Quick Jump to What You Need by Project
:class: dropdown

**For Project 1 (Stellar Populations)**:

- [](#part-2-vectors) - State representation
- [](#part-3-matrices) - Vectorization

**For Project 2 (N-body Dynamics)**:

- [Section 2.3-2.4: Cross Products](#cross-product) - Angular momentum
- [Section 4: Eigenvalues](#part-4-eigenvalues) - Stability analysis
- [Section 3.3: Matrix Multiplication](#matrix-multiplication) - Transformations

**For Project 3 (Monte Carlo Radiative Transfer)**:
- [Section 3.2: Transformation Matrices](#building-intuition-concrete) - Scattering
- [Section 2.1: Vector Spaces](#vector-spaces) - Photon directions
:::

---

## Prerequisites Self-Check

::::{admonition} 📚 Can You Start? Quick Self-Assessment
:class: important

**Priority: 🔴 Essential** - Complete before starting

Try these without help (solutions provided):

1. Compute $(2,3) \cdot (4,1) = ?$
2. What's special about matrix $I$ where $I\vec{x} = \vec{x}$?
3. If $\det(A) = 0$, what does this mean physically?

:::{tip} Solutions with Explanations
:class: dropdown

1. **Dot product**: $(2,3) \cdot (4,1) = 2(4) + 3(1) = 8 + 3 = 11$
   - This measures projection of one vector onto another

2. **Identity matrix**: $I$ is the "do nothing" transformation
   - Like multiplying by 1 in regular arithmetic
   - Has 1s on diagonal, 0s elsewhere

3. **Zero determinant**: The matrix is singular (non-invertible)
   - Physically: Information is lost, dimension collapses
   - Example: Projecting 3D onto 2D loses depth

If any of these were unclear, review basic matrix arithmetic before proceeding.
:::
::::

---

## Learning Objectives

:::{hint} 📅 When to Read This Module
:class: dropdown

- [ ] **Initial Reading**: Before starting Project 1, read sections marked 🔴
- [ ] **Deep Dive**: Return to 🟡 sections as you start Project 2
- [ ] **Reference**: Use throughout Projects 1-3 as questions arise

**Tip:** This module provides the foundation for Projects 1-3. Module 0b covers the statistical methods needed for Projects 4-6.
:::

By the end of this module, you will be able to:

- [ ] **(1) Translate** physical problems into vector and matrix representations 🔴
- [ ] **(2) Apply** conservation laws to identify invariant mathematical structures 🟡
- [ ] **(3) Calculate** eigenvalues and eigenvectors for 2×2 and 3×3 matrices by hand 🟡
- [ ] **(4) Choose** the appropriate matrix operations for computational efficiency 🔴
- [ ] **(5) Connect** linear algebra concepts to N-body dynamics and Monte Carlo methods 🟡
- [ ] **(6) Debug** numerical issues using condition numbers and matrix properties 🔴

---

## Prerequisites Review

:::{note} 📚 Mathematical Prerequisites Check

**Priority: 🔴 Essential** - Review this before starting

Before diving into the module, ensure you're comfortable with:

- [ ] Basic matrix arithmetic (addition, multiplication)
- [ ] Solving quadratic equations
- [ ] Summation notation $(∑)$
- [ ] Basic trigonometry (sin, cos, radians)
- [ ] Complex numbers (for eigenvalues)

If any are unfamiliar, review the provided examples in each section.
:::

---
(overview)=
## Module Overview

```{margin}
**linear algebra**
The branch of mathematics concerning vector spaces and linear transformations between them
```

:::{important} 🎯 Core Message

**Priority: 🔴 Essential**:

**Linear algebra** is the mathematical foundation that makes computational astrophysics possible. This module covers the core concepts needed for Projects 1-3: vectors for representing physical states, matrices for transformations, and eigenvalues for understanding stability and dynamics.
:::

This module builds your understanding from first principles, following the progression of Projects 1-3. We start with **scalars and vectors** describing individual stellar properties and positions (Project 1), build to **matrices** transforming entire systems (Project 2), and explore how eigenvalues reveal stability and oscillation modes (Project 3). Module 0b will extend these foundations to statistical methods and machine learning.

:::{important} 🎯 Why This Module Matters

For Projects 1-3, you'll need:

- **Project 1**: Vector operations for stellar populations, matrix multiplication for vectorized calculations
- **Project 2**: Cross products for angular momentum, eigenvalues for orbital stability analysis
- **Project 3**: Transformation matrices for photon scattering, vector spaces for directional sampling

Master these foundations first, then advance to Module 0b for the statistical methods of Projects 4-6.
:::

---

## Part 1: The Opening - A Globular Cluster as a Mathematical Universe

**Priority: 🟡 Important** - Provides physical context for abstract concepts

:::{hint} 📅 When You'll Use This
:class: dropdown

- **First appears in**: Project 2 (N-body dynamics)
- **Critical for**: Understanding phase space throughout the course
- **Returns in**: Every project dealing with multi-particle systems
:::

### 1.1 The Physical System That Motivates Everything

```{margin}
**globular cluster**
A spherical collection of 10⁴ to 10⁶ stars bound by gravity, orbiting as satellites of galaxies
```

Consider Omega Centauri, the most massive **globular cluster** orbiting our galaxy. It contains approximately 10 million stars, all gravitationally bound, orbiting their common center of mass for the past 12 billion years. At its core, stellar densities reach thousands of stars per cubic parsec – if Earth orbited a star there, our night sky would blaze with thousands of stars brighter than Venus.

%```{figure}[](images/OmegaCen.jpg)
%:label: omegaCen
%:alt: Omega Centauri Globular Cluster
%:align: center

%Zoom-in HST image of the Omega Centauri Globular Cluster located at a distance of $\sim$4.8 kpc.<br> *Credit: NASA* 

%```

To simulate this cluster, we need to track for each star:

- **Position:** $\vec{r}_i = (x_i, y_i, z_i)$ measured from the cluster center
- **Velocity:** $\vec{v}_i = (v_{x,i}, v_{y,i}, v_{z,i})$ relative to the cluster's motion

That's 6 million numbers evolving according to Newton's laws. The gravitational force on star $i$ is:

$$
\vec{F}_i = -G m_i \sum_{j \neq i} \frac{m_j (\vec{r}_i - \vec{r}_j)}{|\vec{r}_i - \vec{r}_j|^3}
$$

Each star feels forces from all others. For $N = 10^7$ stars (Omega Centauri's estimated count), the number of unique pairwise interactions is $N(N-1)/2 ≈ 5×10^{13}$. That's approximately 50 trillion unique force pair calculations per timestep! Without linear algebra, this would be impossible. With it, we can organize these calculations efficiently, identify conserved quantities, and understand the cluster's long-term evolution.

::::{admonition} 🤔 Check Your Understanding
:class: hint

A small globular cluster has 100,000 stars. How many unique force pair calculations are needed per timestep if we compute all pairwise interactions?

:::{admonition} Solution
:class: tip, dropdown

Each star feels forces from all others, so we need to count unique pairs. The binomial coefficient $\binom{n}{2}$ (read "n choose 2") counts the number of ways to choose 2 items from n total items:

$$
\binom{100,000}{2} = \frac{100,000!}{2!(100,000-2)!} = \frac{100,000 \times 99,999}{2 \times 1} \approx 5 \times 10^9
$$

The factorial notation cancels nicely: the (100,000-2)! in the denominator cancels all but the first two terms of 100,000! in the numerator, leaving us with the simple formula N(N-1)/2.

That's 5 billion unique force pair calculations per timestep! Note that while each star experiences 99,999 forces, we can use Newton's third law (action-reaction) to compute each pair only once. This is why we need efficient matrix operations and clever algorithms like tree codes.
:::
::::

### 1.2 Conservation Laws: The Hidden Structure

**Priority: 🟡 Important** - Fundamental for understanding physical constraints

```{margin}
**conservation law**
A physical quantity that remains constant over time due to an underlying symmetry
```

The cluster's apparent chaos hides profound order. Despite the complex individual stellar orbits, certain quantities never change:

Here are the updated equations with terms properly introduced at first appearance:

**Total Energy**:
$$E = \sum_i \frac{1}{2} m_i |\vec{v}_i|^2 - G \sum_{i<j} \frac{m_i m_j}{|\vec{r}_i - \vec{r}_j|}$$

where $m_i$ is the mass of star $i$, $\vec{v}_i$ is its velocity vector, $G$ is the gravitational constant, and $|\vec{r}_i - \vec{r}_j|$ is the distance between stars $i$ and $j$. The first term is the total kinetic energy and the second term is the total gravitational potential energy (summed over all unique pairs).

**Total Momentum**:
$$\vec{P} = \sum_i m_i \vec{v}_i$$

This vector sum represents the net momentum of the entire cluster.

**Total Angular Momentum**:
$$\vec{L} = \sum_i m_i (\vec{r}_i \times \vec{v}_i)$$

where $\vec{r}_i$ is the position vector of star $i$ from the cluster center and $\times$ denotes the cross product. This measures the total rotational momentum of the system.

These **conservation laws** aren't accidents – they arise from fundamental symmetries of space and time. Emmy Noether proved that every continuous symmetry implies a conservation law:

| Symmetry | Conservation Law | Mathematical Structure |
|----------|-----------------|----------------------|
| Time translation invariance | Energy | Quadratic forms |
| Space translation invariance | Momentum | Vector addition |
| Rotational invariance | Angular momentum | Cross products, orthogonal matrices |

These symmetries manifest mathematically as properties of vectors and matrices. Translation invariance means physics doesn't change when we add the same vector to all positions. Rotational invariance means physics is preserved under **orthogonal transformations**.

:::{note} 💡 Deeper Insight: Noether's Theorem in Action
**Priority: 🟢 Enrichment**

Noether's theorem tells us that symmetries and conservation laws are two sides of the same coin. In your Project 2, you'll discover that symplectic integrators (which preserve phase space volume) automatically conserve energy over long timescales. This isn't a coincidence – it's Noether's theorem at work! The symplectic structure (preserved determinant) encodes time-translation symmetry, which guarantees energy conservation.
:::

:::{tip} 🌟 The More You Know: Emmy Noether's Revolutionary Theorem
:class: dropdown

**Priority: 🟢 Enrichment**

Emmy Noether (1882-1935) fundamentally changed physics with her 1915 theorem connecting symmetries to conservation laws. Despite facing discrimination that prevented her from holding a paid position for years, she persisted in her work at the University of Göttingen.

When Einstein's general relativity seemed to violate energy conservation, it was Noether who resolved the paradox. She proved that in general relativity, energy conservation becomes local rather than global—a subtle but profound insight. Einstein wrote to Hilbert: "Yesterday I received from Miss Noether a very interesting paper on invariant forms. I'm impressed that such things can be understood in such a general way" (Letter from Einstein to Hilbert, May 24, 1918, as documented in *The Collected Papers of Albert Einstein*, Volume 8).

Her theorem now underlies all of modern physics. Every conservation law you use — energy, momentum, angular momentum, electric charge — exists because of an underlying symmetry. When you implement conservation checks in your N-body code, you're using Noether's profound insight that geometry determines physics.

*Source: Osen, L. M. (1974). Women in Mathematics. MIT Press. pp. 141–152.*
:::

### 1.3 The Phase Space Perspective

**Priority: 🟡 Important** - Conceptual foundation for Projects 2-6

```{margin}
**trajectory**
The path traced by a system's state through phase space as it evolves in time

**phase space**
The space of all possible states of a system; for N particles in 3D, has 6N dimensions (3 position + 3 velocity per particle)
```

Here's the profound insight that changes everything: the million-star cluster isn't really moving through 3D space. It's tracing a **trajectory** through a 6-million-dimensional **phase space** where each axis represents one position or velocity component. The system's entire state is a single point in this vast space, and its time evolution is a trajectory through it.

This perspective reveals hidden simplicities:

- **Conservation laws constrain the trajectory to a lower-dimensional surface** - Just as a ball rolling in a bowl is confined to the bowl's 2D surface despite existing in 3D space, the cluster's evolution is restricted to a much smaller subspace where energy, momentum, and angular momentum remain constant. The 6-million dimensions collapse to far fewer effective dimensions.

- **Near equilibrium, motion decomposes into independent oscillation modes (eigenvectors)** - Like a drum that vibrates in distinct patterns (fundamental, overtones), the cluster has natural oscillation modes. Small disturbances trigger these modes independently, each oscillating at its own characteristic frequency - these are the **eigenvectors** and **eigenvalues** of the system.

- **Statistical properties emerge from the geometry of this high-dimensional space** - Velocity dispersion, dynamical stability, and evolution rates aren't separate properties but geometric features of how the system explores phase space. The volume it occupies relates to entropy, the shape of its trajectory relates to energy distribution, and the curvature of energy surfaces determines bound vs. unbound orbits. (See [Module 1a, Section 4](./01a-stat-mech-module.md) for the deep connection between stellar dynamics and statistical mechanics.)

:::{admonition} 🚀 Real-World Application
:class: tip

The Gaia space telescope measures positions and velocities for over 1 billion stars in our galaxy. That's a 6-billion-dimensional phase space! Linear algebra makes it possible to:

- Identify moving groups and stellar streams (eigenanalysis)
- Reconstruct the galaxy's gravitational potential (matrix inversion)
- Find hidden structures like dissolved star clusters (principal components)

Without linear algebra, Gaia's data would be incomprehensible noise.
:::

:::{admonition} 📌 Key Distinction: Phase Space vs. Parameter Space
:class: important

**Phase space** contains dynamical variables (positions, velocities) that evolve with time according to equations of motion. A trajectory through phase space represents the system's time evolution.

**Parameter space** contains fixed quantities that define the system but don't evolve dynamically. When you do MCMC in Project 4, you'll explore parameter space to find optimal values of cosmological parameters (Ωm, h). When you train neural networks, you'll search weight space (a type of parameter space) for optimal network configurations.

The key difference:

- **Phase space:** Where systems evolve (dynamics)
- **Parameter space:** What defines systems (characteristics)
:::

```{margin}
**parameter space**
The space of all possible **parameter** values; each point represents a different configuration or model of the system

**parameter**
Most fundamentally: a number that controls the behavior of a mathematical function or system. In physics: quantities like mass, temperature, or coupling constants that define system properties but are not the variables being solved for
```

:::{important} 📌 Key Takeaway

Phase space transforms complexity into geometry. Instead of tracking millions of individual trajectories, we can understand the system through the geometry of its phase space – its conserved surfaces, its stable manifolds, its eigenstructure. This geometric view is what makes the seemingly impossible (simulating millions of stars) actually tractable.

*Remember the distinction:* **phase space** (where systems evolve dynamically) vs. **parameter space** (the values that define the system). In Project 2, you'll watch star clusters evolve through phase space. In Project 4, you'll explore parameter space to find the Universe's composition. Both use the same mathematical machinery of linear algebra, but for fundamentally different purposes – one tracks dynamics, the other searches for optimal models.
:::

---
(part-2-vectors)=
## Part 2: Vectors - The Atoms of Physical Description

**Priority: 🔴 Essential** - Foundation for everything that follows

:::{admonition} 📅 When You'll Use This
:class: dropdown, hint

- **First appears in**: Project 1 (representing stellar properties)
- **Used throughout**: Every single project
- **Most critical for**: Understanding state representation and transformations
:::

:::{admonition} 🔭 Where We're Going
:class: note

We begin with scalars – quantities with only magnitude – then advance to vectors that encode both magnitude and direction. We'll explore vectors' three complementary interpretations (physical, geometric, algebraic) and the operations that let us combine and manipulate them. By the end of this section, you'll see vectors not as lists of numbers but as the natural way to encode any quantity requiring directional information.
:::

### 2.1 From Scalars to Vectors: Building Deep Understanding {#part-2-vectors}

```{margin}
**scalar**
A quantity with magnitude only, represented by a single number

**vector**
A mathematical object with both magnitude and direction that transforms according to specific rules

**components**
The scalar coefficients representing a vector in a chosen basis
```

The simplest quantities in physics are **scalars** – single numbers that have magnitude but no direction. Mass ($2×10^{33}$ g), temperature (5800 K), luminosity ($3.8×10^{33}$ erg/s), and density (1.4 g/cm³) are all scalars. They tell us "how much" but not "which way." For many physical quantities, however, magnitude alone is insufficient – we need direction too. This is where vectors enter.

A **vector** is simultaneously three complementary things, and masterful computational scientists fluidly shift between these perspectives:

- **Physical Perspective**: A vector represents any quantity with both magnitude and direction. The velocity of Earth orbiting the Sun is a vector — it has a speed (30 km/s) and a direction (tangent to the orbit). Forces, electric fields, angular momenta — all are vectors because they have this magnitude-direction character that scalars cannot express.

- **Geometric Perspective**: A vector is an arrow in space. Crucially, this arrow is **free** — it doesn't have a fixed starting point. The displacement "3 km north" is the same vector whether you start from your house or from campus. This freedom is what allows us to add forces acting at different points on a rigid body.

- **Algebraic Perspective**: A vector is an ordered list of numbers — its **components** in some coordinate system. Earth's velocity might be written as:

$$\vec{v} = \begin{pmatrix} -15.2 \\ 25.8 \\ 0.0 \end{pmatrix} \text{ km/s (in ecliptic coordinates)}$$

But here's the crucial insight: these numbers are not the vector itself – they're just one representation. The vector exists *independently* of any coordinate system.

:::{warning} ⚠️ Common Misconception Alert

Students often think a vector IS its components. This is wrong! A vector is a geometric object that exists independently of coordinates. When you rotate your coordinate system, the components change but the vector itself doesn't. Think of it like describing a person's location: "3 blocks north, 2 blocks east" versus "3.6 blocks northeast" – different descriptions, same displacement.
:::

:::{note} 💡 Building Intuition: Vectors as Instructions

Think of a vector as an instruction for movement. The vector $\vec{v} = (3, 4, 0)$ says: "Go 3 units east, 4 units north, stay at the same height." No matter where you start, following this instruction produces the same displacement. This is why we can slide vectors around freely — they're instructions, not fixed objects.

This becomes powerful in physics: a force vector tells you which way to accelerate and how strongly. A velocity vector tells you which way you're moving and how fast. The vector nature captures both pieces of information in one mathematical object.
:::

::::{note} 🧠 Build Your Intuition: Vector Components

Without calculating, predict what happens to vector components when you:

1. Rotate the coordinate system 90° clockwise: The x-component becomes the ___ component
2. Double all coordinate axes scales: Components are ___
3. Flip the x-axis direction: The x-component ___

:::{tip} Answers:
:class: dropdown
(1) becomes the negative y-component, (2) halved, (3) changes sign

This shows components depend on your coordinate choice, but the vector itself doesn't change!
:::
::::

(vector-spaces)=
### 2.2 Vector Spaces: The Mathematical Framework

```{margin}
**vector space**
A set equipped with addition and scalar multiplication operations satisfying eight specific axioms

**linear independence**
Vectors that cannot be written as linear combinations of each other
```

**Priority: 🟡 Important** - Theoretical foundation

A **vector space** is a set equipped with two operations (vector addition and scalar multiplication) that satisfy eight axioms. These axioms aren't arbitrary mathematical rules – each captures an essential physical property:

| Axiom | Mathematical Statement | Physical Meaning |
|-------|------------------------|------------------|
| **Closure under addition** | $\vec{u} + \vec{v} \in V$ | Adding velocities gives velocity |
| **Commutativity** | $\vec{u} + \vec{v} = \vec{v} + \vec{u}$ | Order of displacements doesn't matter |
| **Associativity** | $(\vec{u} + \vec{v}) + \vec{w} = \vec{u} + (\vec{v} + \vec{w})$ | Grouping of forces doesn't affect total |
| **Zero vector** | $\exists \vec{0}: \vec{v} + \vec{0} = \vec{v}$ | State of no motion or displacement |
| **Additive inverse** | $\forall \vec{v}, \exists -\vec{v}: \vec{v} + (-\vec{v}) = \vec{0}$ | Every motion has an opposite |
| **Scalar closure** | $c\vec{v} \in V$ | Scaling a force gives another force |
| **Distributivity** | $c(\vec{u} + \vec{v}) = c\vec{u} + c\vec{v}$ | Scaling preserves addition |
| **Identity** | $1 \cdot \vec{v} = \vec{v}$ | Multiplying by 1 changes nothing |

**Linear independence** means vectors cannot be written as combinations of each other - they represent truly independent directions in space.

(dot-product)=
### 2.3 The Dot Product: Projection, Angle, and Energy

**Priority: 🔴 Essential** - Used constantly throughout all projects

```{margin}
**dot product**
Scalar operation on vectors:<br> $\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$
```

The **dot product** is perhaps the most important operation in physics because it answers a fundamental question: "How much does one vector contribute in the direction of another?"

**Definition and Formula**:
$$\vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z = |\vec{a}||\vec{b}|\cos\theta$$

But why are these two formulas equal? Let's derive this connection from first principles.

:::{admonition} 📝 Mathematical Derivation: Dot Product Formula
:class: note, dropdown

**Priority: 🟢 Enrichment**

**Starting from the Law of Cosines:**

Consider vectors $\vec{a}$ and $\vec{b}$ with angle $\theta$ between them. The vector from tip of $\vec{a}$ to tip of $\vec{b}$ is $\vec{b} - \vec{a}$.

By the law of cosines:
$$|\vec{b} - \vec{a}|^2 = |\vec{a}|^2 + |\vec{b}|^2 - 2|\vec{a}||\vec{b}|\cos\theta$$

Expanding the left side:
$$|\vec{b} - \vec{a}|^2 = (b_x - a_x)^2 + (b_y - a_y)^2 + (b_z - a_z)^2$$
$$= |\vec{a}|^2 + |\vec{b}|^2 - 2(a_x b_x + a_y b_y + a_z b_z)$$

Comparing both expressions:
$$a_x b_x + a_y b_y + a_z b_z = |\vec{a}||\vec{b}|\cos\theta$$

This proves the component formula equals the geometric formula!
:::

**Physical Applications of the Dot Product**:

<!-- Suggested figure: Visual showing force vector, displacement vector, and the component of force along displacement -->

**Work Done by a Force**:
$$W = \vec{F} \cdot \vec{d} = |\vec{F}||\vec{d}|\cos\theta$$

Only the component of force along the displacement does work. A force perpendicular to motion (like the normal force on a sliding block) does zero work.

**Power from Solar Panels**:
$$P = \vec{S} \cdot \hat{n} = |\vec{S}|\cos\theta$$

where $\vec{S}$ is the solar flux vector and $\hat{n}$ is the panel's normal. Maximum power when facing the sun ($\theta = 0$), zero when edge-on ($\theta = 90°$).

::::{admonition} 🤔 Check Your Understanding
:class: hint

Two stars have velocities $\vec{v}_1 = (200, 100, 50)$ km/s and $\vec{v}_2 = (150, -100, 100)$ km/s.

1. Calculate their relative velocity
2. Are they approaching or receding? (Hint: use the dot product)

:::{admonition} Solution
:class: tip, dropdown

1. Relative velocity: $\vec{v}_{\text{rel}} = \vec{v}_1 - \vec{v}_2 = (50, 200, -50)$ km/s

2. To determine if approaching or receding, we need the dot product of relative velocity with separation vector. If we assume star 2 is at origin and star 1 at position $\vec{r}$:
   - If $\vec{v}_{\text{rel}} \cdot \vec{r} > 0$: receding
   - If $\vec{v}_{\text{rel}} \cdot \vec{r} < 0$: approaching
   - If $\vec{v}_{\text{rel}} \cdot \vec{r} = 0$: constant separation

Without knowing positions, we can't determine if they're approaching or receding – we need both position and velocity information!

**Complete Physics Analysis**:

To fully determine whether stars are approaching or receding, we need their position vectors. If star 1 is at position $\vec{r}_1$ and star 2 at position $\vec{r}_2$:

**Separation vector**: $\Delta\vec{r} = \vec{r}_1 - \vec{r}_2$

**The key test**:

Compare the relative velocity with the separation:

- If $\vec{v}_{\text{rel}} \cdot \Delta\vec{r} > 0$: Stars are separating (receding)
  - The relative velocity points in the same general direction as the separation
- If $\vec{v}_{\text{rel}} \cdot \Delta\vec{r} < 0$: Stars are approaching
  - The relative velocity points opposite to the current separation
- If $\vec{v}_{\text{rel}} \cdot \Delta\vec{r} = 0$: Maintaining constant separation
  - The relative velocity is perpendicular to the line joining them

**Why this works**: The dot product $\vec{v}_{\text{rel}} \cdot \Delta\vec{r}$ gives the component of relative velocity along the line connecting the stars. Positive means moving apart along this line, negative means moving together.

**Project 2 Connection**: This dot product test becomes essential for collision detection in your N-body simulations. You'll use it to identify close encounters and potential binary formation!
:::
::::

(cross-product)=
### 2.4 The Cross Product: Creating Perpendicularity

**Priority: 🔴 Essential** - Critical for angular momentum in Project 2

```{margin}
**cross product**
Vector operation producing a perpendicular vector: $\vec{a} \times \vec{b}$
```

The **cross product** creates a vector perpendicular to two input vectors:

$$\vec{a} \times \vec{b} = \begin{pmatrix} a_y b_z - a_z b_y \\ a_z b_x - a_x b_z \\ a_x b_y - a_y b_x \end{pmatrix}$$

**Memory Aid - The Determinant Method**:

The cross product can be computed as a determinant:

$$\vec{a} \times \vec{b} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ a_x & a_y & a_z \\ b_x & b_y & b_z \end{vmatrix}$$

Expanding this determinant along the first row:

$$\vec{a} \times \vec{b} = \hat{i}(a_y b_z - a_z b_y) - \hat{j}(a_x b_z - a_z b_x) + \hat{k}(a_x b_y - a_y b_x)$$

**Alternative Pattern Method**:

- **i-component**: Take the y and z components: $(a_y b_z - a_z b_y)$
- **j-component**: Take the x and z components with a minus sign: $-(a_x b_z - a_z b_x)$
- **k-component**: Take the x and y components: $(a_x b_y - a_y b_x)$

Notice the pattern: each component uses the two coordinates that aren't its own, and the j-component has a negative sign (this comes from the alternating signs in determinant expansion).

**Geometric Intuition**: To find the direction of $\vec{a} \times \vec{b}$, use the right-hand rule: curl your right hand's fingers from the first vector $\vec{a}$ toward the second vector $\vec{b}$ through the smaller angle. Your thumb points in the direction of the cross product. This isn't arbitrary - it ensures consistency with our choice of right-handed coordinate systems.

**Key Properties**:

- **Magnitude**: $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$ (area of parallelogram)
- **Direction**: Right-hand rule
- **Anti-commutative**: $\vec{a} \times \vec{b} = -\vec{b} \times \vec{a}$

**Physical Meaning - Angular Momentum**:

For a star at position $\vec{r}$ with momentum $\vec{p} = m\vec{v}$:
$$\vec{L} = \vec{r} \times \vec{p}$$

This vector is perpendicular to the orbital plane. Its magnitude equals twice the rate of area swept out—this is Kepler's second law!

:::{warning} ⚠️ Common Pitfall: Cross Product Order
:class: warning

Students often forget that cross product order matters!
$\vec{a} \times \vec{b} = -\vec{b} \times \vec{a}$ (they point in opposite directions)

This is crucial in physics:

- Torque: $\vec{\tau} = \vec{r} \times \vec{F}$ (position THEN force)
- Angular momentum: $\vec{L} = \vec{r} \times \vec{p}$ (position THEN momentum)

Getting the order wrong flips the direction - your planet orbits backward!
:::

### 2.5 Orthogonality: When Vectors Don't Talk

**Priority: 🟡 Important** - Essential for understanding basis vectors

```{margin}
**orthogonal**
Perpendicular; vectors with zero dot product

**orthonormal**
Basis vectors that are both orthogonal (perpendicular) and normalized (unit length)
```

Two vectors are **orthogonal** (perpendicular) when their dot product is zero: $\vec{a} \cdot \vec{b} = 0$. This isn't just a geometric curiosity - orthogonality is why we can decompose complex systems into independent components.

**Why Orthogonal Bases Are Special**:

When basis vectors are **orthonormal** (orthogonal AND unit length), calculations become dramatically simpler:

- **Projections are independent**: The component along one axis doesn't affect others
- **Pythagoras works**: $|\vec{v}|^2 = v_x^2 + v_y^2 + v_z^2$
- **Rotations preserve dot products**: Orthogonal transformations preserve angles and lengths

**Physical Example**: In quantum mechanics, energy eigenstates are orthogonal. This means measuring one energy level doesn't affect the probability of finding the system in another level. The orthogonality of spherical harmonics is why we can decompose the cosmic microwave background into independent multipole moments!

**Astrophysical Application**: When tracking stellar proper motions, observations often come in non-orthogonal coordinate systems (right ascension, declination, radial velocity). Orthogonalization creates independent velocity components where each represents truly independent motion - essential for understanding 3D stellar kinematics and discovering moving groups in the solar neighborhood.

:::{tip} 💻 Computational Reality Check: Vectorization

**THIS PATTERN IS EVERYTHING!**

Orthogonal decomposition isn't just mathematically elegant – it's computationally essential. Let's see why with a stellar clustering analysis:

```python
# Finding nearest neighbors for N stars (e.g., identifying binary pairs)

# Slow nested loops (DON'T DO THIS):
nearest_distances = np.zeros(N)
nearest_indices = np.zeros(N, dtype=int)
for i in range(N):
    min_dist = np.inf
    min_idx = -1
    for j in range(N):
        if i != j:
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < min_dist:
                min_dist = dist
                min_idx = j
    nearest_distances[i] = min_dist
    nearest_indices[i] = min_idx
# Time for N=1000: ~1.8 seconds

# Fast vectorized version (DO THIS):
# Compute all pairwise distances at once using broadcasting
pos_i = positions[:, np.newaxis, :]  # Shape: (N, 1, 3)
pos_j = positions[np.newaxis, :, :]  # Shape: (1, N, 3)
separations = pos_i - pos_j           # Broadcasting! Shape: (N, N, 3)
distances = np.linalg.norm(separations, axis=2)  # Shape: (N, N)

# Mask out self-distances
np.fill_diagonal(distances, np.inf)

# Find nearest neighbor for each star
nearest_distances = np.min(distances, axis=1)
nearest_indices = np.argmin(distances, axis=1)
# Time for N=1000: ~0.015 seconds (120x faster!)

# The speedup comes from:
# 1. NumPy operations run in optimized C code
# 2. CPU vector instructions (SIMD) process multiple values simultaneously
# 3. Better cache usage from processing contiguous memory blocks
# 4. Broadcasting eliminates Python loop overhead

# Key insight for Project 2: This SAME broadcasting pattern works for ANY 
# pairwise calculation. Think about how you could adapt this structure 
# for computing interactions between particles...

```

**Understanding the broadcasting magic**:

- `positions[:, np.newaxis, :]` adds a new axis, creating shape (N, 1, 3)
- When NumPy sees shapes (N, 1, 3) and (1, N, 3), it "broadcasts" to (N, N, 3)
- This creates all N² pairwise differences in one operation!
- No Python loops = no Python overhead = massive speedup

**Why this matters**: In Project 2, you'll need similar pairwise calculations. Master this broadcasting pattern and your code will run 100x faster than nested loops!

You'll use this exact structure in:

- **Project 1:** Stellar property calculations
- **Project 2:** N-body force calculations  
- **Project 3:** Photon-matter interactions

*Master this once, use it everywhere!*

:::

### 2.6 Basis Vectors and Coordinate Systems

**Priority: 🟡 Important** - Needed when changing coordinate systems

```{margin}
**basis**
A set of linearly independent vectors that span the entire vector space
```

A **basis** is a set of linearly independent vectors that span the entire space. The familiar Cartesian basis:

$$\hat{x} = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \quad \hat{y} = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \quad \hat{z} = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}$$

These are **orthonormal**: mutually perpendicular and unit length.

Any vector can be decomposed:
$$\vec{v} = v_x \hat{x} + v_y \hat{y} + v_z \hat{z}$$

The coefficients are found by projection (via the dot product):
$$v_x = \vec{v} \cdot \hat{x}, \quad v_y = \vec{v} \cdot \hat{y}, \quad v_z = \vec{v} \cdot \hat{z}$$

:::{admonition} 💡 Practical Insight: Choosing the Right Coordinates
:class: note

**Priority: 🟡 Important for Project 2**<br>
Different problems benefit from different coordinate systems:

| System | Best Coordinates | Why |
|--------|-----------------|-----|
| Binary star orbit | Centered on barycenter | Simplifies equations of motion |
| Spiral galaxy | Cylindrical (R, φ, z) | Matches galaxy symmetry |
| Globular cluster | Spherical (r, θ, φ) | Exploits spherical symmetry |
| Stellar stream | Along stream trajectory | Reveals stream structure |

In Project 2, you'll transform between coordinate systems to simplify your N-body calculations.
:::

:::{note} 📝 Worked Example: Gram-Schmidt Orthogonalization
:class: dropdown

**Priority: 🟢 Enrichment** - Helps understand QR decomposition

**Physical Motivation**: You're observing a galaxy and measure velocities in a skewed coordinate system. Gram-Schmidt creates an orthonormal basis where velocity components are independent - essential for understanding the true motion patterns!

The **Gram-Schmidt process** creates an orthonormal basis from any linearly independent set. This is essential for understanding QR decomposition.

**Given vectors**: $\vec{v}_1 = (1, 1, 0)$, $\vec{v}_2 = (1, 0, 1)$, $\vec{v}_3 = (0, 1, 1)$

**Step 1**: Normalize first vector
$$\vec{u}_1 = \frac{\vec{v}_1}{|\vec{v}_1|} = \frac{(1, 1, 0)}{\sqrt{2}} = \left(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\right)$$

**Step 2**: Remove $\vec{u}_1$ component from $\vec{v}_2$
$$\vec{w}_2 = \vec{v}_2 - (\vec{v}_2 \cdot \vec{u}_1)\vec{u}_1$$
$$= (1, 0, 1) - \frac{1}{\sqrt{2}} \cdot \left(\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}, 0\right)$$
$$= (1, 0, 1) - \left(\frac{1}{2}, \frac{1}{2}, 0\right) = \left(\frac{1}{2}, -\frac{1}{2}, 1\right)$$

Normalize: $\vec{u}_2 = \vec{w}_2/|\vec{w}_2| = \left(\frac{1}{\sqrt{6}}, -\frac{1}{\sqrt{6}}, \frac{2}{\sqrt{6}}\right)$

**Step 3**: Remove $\vec{u}_1$ and $\vec{u}_2$ components from $\vec{v}_3$
$$\vec{w}_3 = \vec{v}_3 - (\vec{v}_3 \cdot \vec{u}_1)\vec{u}_1 - (\vec{v}_3 \cdot \vec{u}_2)\vec{u}_2$$

After calculation: $\vec{u}_3 = \left(-\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}\right)$

The result is an orthonormal basis that spans the same space as the original vectors!
:::

::::{hint} ✅ Test Your Understanding: Vectors

Before moving on, can you answer these conceptual questions?

1. Why can we slide vectors around freely in space?
2. What does it mean physically when two vectors are orthogonal?
3. Why does the dot product give us work done by a force?
4. What information does the cross product magnitude tell us?

Think about these before checking the answers!

:::{tip} Answers
:class: dropdown

1. Vectors represent displacements/instructions, not fixed positions. The instruction "go 3 km north" is the same regardless of starting point.

2. The vectors represent independent directions - no component of one lies along the other. Physically: perpendicular forces, independent measurements.

3. Work is energy transferred along the direction of motion. The dot product extracts exactly the component of force along displacement.

4. The area of the parallelogram formed by the vectors. In physics: angular momentum magnitude, torque strength, rate of area swept in orbit.
:::
::::

### Progressive Problems: Vectors

::::{note} 📝 Practice Problems

**Level 1 (Conceptual)**:

Verify that the vectors $\vec{a} = (1, 0, 0)$ and $\vec{b} = (0, 1, 0)$ are orthogonal.

**Level 2 (Computational)**:
Find a unit vector perpendicular to both $\vec{a} = (1, 2, 3)$ and $\vec{b} = (4, 5, 6)$.

**Level 3 (Theoretical)**:
Prove that for any vectors $\vec{a}$, $\vec{b}$, $\vec{c}$, the scalar triple product is cyclic:
  $$\vec{a} \cdot (\vec{b} \times \vec{c}) = \vec{b} \cdot (\vec{c} \times \vec{a}) = \vec{c} \cdot (\vec{a} \times \vec{b}).$$

:::{tip} Solutions
:class: dropdown

**Level 1**:

$\vec{a} \cdot \vec{b} = (1)(0) + (0)(1) + (0)(0) = 0$ ✓ They're orthogonal.

**Level 2**:

- $\vec{a} \times \vec{b} = (2·6-3·5, 3·4-1·6, 1·5-2·4) = (-3, 6, -3)$
- Magnitude: $|\vec{a} \times \vec{b}| = \sqrt{9+36+9} = \sqrt{54} = 3\sqrt{6}$
- Unit vector: $\hat{n} = \frac{1}{3\sqrt{6}}(-3, 6, -3) = \frac{1}{\sqrt{6}}(-1, 2, -1)$

**Level 3**:

The scalar triple product represents the volume of the parallelepiped formed by the three vectors. Since volume doesn't depend on which face you consider as the base, the product is cyclic. Algebraically, this follows from the determinant representation of the triple product.
:::
::::

:::{important} 📌 Key Takeaway

Vectors are not just arrows or lists of numbers - they're the natural language for any quantity with magnitude and direction. Master the dot product (projection/angle), cross product (perpendicularity/rotation), and basis decomposition, and you can describe any physical system from stellar velocities to electromagnetic fields.
:::

---
(part-3-matrices)=
## Part 3: Matrices - Transformations That Preserve Structure

**Priority: 🔴 Essential** - Core to all computational methods

:::{admonition} 📅 When You'll Use This
:class: dropdown, hint

- **First appears in**: Project 1 (vectorization with matrices)
- **Critical for**: All projects, especially neural networks
- **Most important**: Understanding matrices as transformations, not just number grids
:::

:::{note} 🔭 Where We're Going

Matrices are where linear algebra becomes powerful. We'll discover that matrices aren't just rectangular arrays of numbers - they're transformations that reshape space while preserving its linear structure. You'll learn to read a matrix and immediately understand what it does geometrically, setting the foundation for everything from N-body dynamics to neural networks.
:::

:::{admonition} 📚 Prerequisites Check
:class: hint

Before proceeding, can you:

- [ ] Multiply two 2×2 matrices by hand?
- [ ] Explain why matrix multiplication order matters?
- [ ] Calculate the determinant of a 2×2 matrix?

If not, review the Prerequisites section before continuing.
:::

### 3.1 Matrices ARE Linear Transformations

```{margin}
**matrix**
A linear transformation represented as a rectangular array of numbers

**transformation**
A function mapping vectors to vectors that preserves vector space structure

**linearity**
Property where $f(αx + βy) = αf(x) + βf(y)$ for all scalars α, β and vectors x, y
```

You've mastered vectors - quantities with magnitude and direction. But what happens when you need to transform many vectors simultaneously? This is where **matrices** emerge naturally. A matrix isn't just a grid of numbers - it's a machine that transforms entire vector spaces. When you multiply a matrix by a vector, you're asking: "Where does this vector go under this **transformation**?" This perspective transforms matrices from abstract number arrays into concrete geometric operations. When we multiply matrix $A$ by vector $\vec{v}$, we get a new vector $A\vec{v}$. The crucial property is **linearity**:

$$A(α\vec{u} + β\vec{v}) = α A\vec{u} + β A\vec{v}$$

:::{admonition} 💡 Building Intuition: Why Row-Times-Column?
:class: note

The strange-looking matrix multiplication rule (row times column) ensures that transformation composition works correctly. Here's why:

When you apply transformation $A$ to vector $\vec{v}$, each component of the output is a linear combination of input components. The first row of $A$ tells you how to compute the first output component:

$$\text{output}_1 = a_{11} v_1 + a_{12} v_2 + a_{13} v_3$$

This is exactly a dot product of row 1 with the vector! Each row defines how one output component depends on all input components. This structure ensures that composing transformations (multiplying matrices) gives the same result as applying them sequentially.
:::

(building-intuition-concrete)=
### 3.2 Building Intuition with Concrete Examples 

**Priority: 🔴 Essential** - Recognize these patterns in your code

Let's see actual matrices and understand what they do:

**The Identity Matrix** (the "do nothing" transformation):
$$I = \begin{pmatrix} 
\boxed{1} & 0 & 0 \\ 
0 & \boxed{1} & 0 \\ 
0 & 0 & \boxed{1} 
\end{pmatrix}$$

Notice the diagonal of ones! For any vector: $I\vec{v} = \vec{v}$. Visually, this leaves all vectors exactly where they are - no rotation, no scaling, no shearing.

**A Rotation Matrix** (30° around z-axis):
$$R_{30°} = \begin{pmatrix} 
\cos(30°) & -\sin(30°) & 0 \\
\sin(30°) & \cos(30°) & 0 \\
0 & 0 & 1 
\end{pmatrix} = \begin{pmatrix} 
\frac{\sqrt{3}}{2} & -\frac{1}{2} & 0 \\
\frac{1}{2} & \frac{\sqrt{3}}{2} & 0 \\
0 & 0 & 1 
\end{pmatrix}$$

Note: $\frac{\sqrt{3}}{2} \approx 0.866$ and $\frac{1}{2} = 0.5$. The $z$-component is unchanged (last row is [0, 0, 1]) because we rotate around $z$. Imagine looking down the $z$-axis: this matrix spins everything counterclockwise by 30° like a record player, preserving all lengths.

**A Diagonal Matrix** (scaling transformation):
$$D = \begin{pmatrix}
\boxed{2} & 0 & 0 \\
0 & \boxed{3} & 0 \\
0 & 0 & \boxed{1}
\end{pmatrix}$$

Doubles $x$, triples $y$, leaves $z$ unchanged. Only diagonal elements are non-zero! This stretches space non-uniformly - imagine stretching a rubber sheet more in one direction than another.

**A Symmetric Matrix** (moment of inertia):
$$I = \begin{pmatrix}
5 & \boxed{2} & 0 \\
\boxed{2} & 8 & \boxed{1} \\
0 & \boxed{1} & 6
\end{pmatrix}$$

Notice $I_{ij} = I_{ji}$ (boxed elements show symmetry). Symmetric matrices represent reciprocal relationships - if $x$ affects $y$, then $y$ affects $x$ equally.

**The Transpose Matrix**:

```{margin}
**transpose**
Operation swapping rows and columns: $(A^T)_{ij} = A_{ji}$
```

The **transpose** swaps rows and columns: $(A^T)_{ij} = A_{ji}$.

Critical for covariance matrices where $\Sigma = \Sigma^T$ (symmetry). The transpose appears everywhere in physics:
- Inner products: $\vec{u} \cdot \vec{v} = \vec{u}^T \vec{v}$
- Quadratic forms: $\vec{x}^T A \vec{x}$
- Normal equations: $A^T A \vec{x} = A^T \vec{b}$

::::{hint} 🤔 Check Your Understanding

What does this matrix do to vectors?
$$M = \begin{pmatrix}
-1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix}$$

:::{tip} Solution
:class: dropdown

This matrix flips the x-component while leaving y and z unchanged. It's a reflection through the yz-plane! If you apply it twice, you get back the original vector (since $(-1) \times (-1) = 1$).

Test with $\vec{v} = (3, 4, 5)$:
$$M\vec{v} = \begin{pmatrix} -3 \\ 4 \\ 5 \end{pmatrix}$$

This transformation appears in physics when dealing with parity operations or mirror symmetries.
:::
::::

(matrix-multiplication)=
### 3.3 Matrix Multiplication: Composition of Transformations

**Priority: 🔴 Essential** - Fundamental operation

```{margin}
**matrix multiplication**
Operation combining two transformations into one: $(AB)\vec{v} = A(B\vec{v})$
```

Matrix multiplication encodes function composition. The element in row $i$, column $j$ of product $AB$ is:

$$(AB)_{ij} = \sum_k A_{ik}B_{kj}$$

This seemingly weird formula ensures that:
$$(AB)\vec{v} = A(B\vec{v})$$

**Why Order Matters**:

Consider rotating 90° around x-axis, then 90° around z-axis, versus the opposite order:

<!-- Suggested figure: Show a cube being rotated in both orders, ending in different orientations -->

Different orders give different results! This is why $AB \neq BA$ in general.

:::{warning} ⚠️ Common Pitfall: Matrix Multiplication Order
:class: warning

Students often try: $A \cdot B \cdot C = A \cdot C \cdot B$ (wrong!)

Matrix multiplication is NOT commutative. Order matters because each matrix is a transformation applied in sequence. Rotating then scaling gives different results than scaling then rotating!

Remember: When you see $ABC\vec{v}$, read it right-to-left: "First apply C, then B, then A to vector v."
:::

**Understanding Determinants - Three Levels**:

**Level 1 (Concrete):** Det = 0 means "information is lost"
- Example: Projecting 3D onto 2D loses depth information

**Level 2 (Geometric):** Det measures volume scaling
- Example: det=2 means volumes double under transformation

**Level 3 (Abstract):** Det is the product of eigenvalues
- This connects spectrum to geometry to invertibility!

:::{note} 📝 Worked Example: 3×3 Matrix Inversion by Hand
:class: dropdown

**Priority: 🟢 Enrichment** - Useful for understanding numerical methods

Let's invert a 3×3 matrix using the cofactor method. Given:
$$A = \begin{pmatrix}
2 & 1 & 0 \\
1 & 2 & 1 \\
0 & 1 & 2
\end{pmatrix}$$

**Step 1**: Calculate the determinant
$$\det(A) = 2\begin{vmatrix}2&1\\1&2\end{vmatrix} - 1\begin{vmatrix}1&1\\0&2\end{vmatrix} + 0$$
$$= 2(4-1) - 1(2-0) = 6 - 2 = 4$$

Since $\det(A) \neq 0$, the matrix is invertible.

**Step 2**: Calculate the matrix of minors
For element $(1,1)$: $M_{11} = \begin{vmatrix}2&1\\1&2\end{vmatrix} = 3$

For element $(1,2)$: $M_{12} = \begin{vmatrix}1&1\\0&2\end{vmatrix} = 2$

For element $(1,3)$: $M_{13} = \begin{vmatrix}1&2\\0&1\end{vmatrix} = 1$

Continue for all nine elements to get the complete matrix of minors.

**Step 3**: Apply cofactor signs (checkerboard pattern)
$$C = \begin{pmatrix}
+3 & -2 & +1 \\
-2 & +4 & -2 \\
+1 & -2 & +3
\end{pmatrix}$$

**Step 4**: Transpose and divide by determinant
$$A^{-1} = \frac{1}{4}C^T = \frac{1}{4}\begin{pmatrix}
3 & -2 & 1 \\
-2 & 4 & -2 \\
1 & -2 & 3
\end{pmatrix}$$

**Verify**: Multiply $AA^{-1}$ to confirm it equals $I$ ✓
:::

### 3.4 The Determinant: Volume, Orientation, and Information

**Priority: 🟡 Important** - Helps understand singularity and numerical stability

```{margin}
**determinant**
Scalar value measuring how a linear transformation scales volumes

**symplectic**
Transformation preserving phase space volume (determinant = 1)

**rank**
The number of linearly independent rows (or columns) in a matrix; the dimension of the space the matrix actually maps to

**regularization**
TODO: add def
```

The **determinant** tells us three crucial things:

| $\det(A)$ | Meaning | Physical Interpretation |
|-----------|---------|------------------------|
| $\|\det(A)\|$ | Volume scaling factor | How much the transformation stretches/shrinks space |
| $\det(A) > 0$ | Preserves orientation | Right-handed stays right-handed |
| $\det(A) < 0$ | Flips orientation | Right-handed becomes left-handed |
| $\det(A) = 0$ | Singular (non-invertible) | Information is lost, dimension collapses |

When $\det(A) = 0$, the matrix is singular and has **rank** less than its dimension. Let's understand what this really means:

**Intuitive Understanding of Rank**:
- **Full rank** (rank = n for n×n matrix): All rows/columns point in independent directions. The matrix preserves dimensionality—3D space stays 3D.
- **Rank deficient** (rank < n): Some rows/columns are linear combinations of others. The matrix collapses space—maybe 3D becomes a 2D plane or even a 1D line.

**Physical Example**: Consider measuring stellar properties:
```python
# Columns: [mass, luminosity, log(luminosity)]
data = np.array([
    [1.0,  1.0,  0.0],
    [2.0,  8.0,  0.9],
    [0.5,  0.125, -0.9]
])
```
This matrix has rank 2, not 3! The third column (log luminosity) is completely determined by the second column. We're really only measuring 2 independent quantities, not 3. The covariance matrix of this data would be singular—we can't invert it because one dimension is redundant.

**Geometric Interpretation**:
- Rank 3 matrix: Maps 3D space to full 3D space
- Rank 2 matrix: Squashes 3D space onto a 2D plane
- Rank 1 matrix: Collapses 3D space onto a 1D line
- Rank 0 matrix: Maps everything to a single point (zero matrix)

Specifically, an $n \times n$ matrix with rank $r < n$ maps $n$-dimensional space onto an $r$-dimensional subspace, losing $(n-r)$ dimensions of information.

For a 2×2 matrix:
$$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

**Geometric interpretation**: For 2×2 matrices, the determinant equals the (signed) area of the parallelogram formed by the column vectors. For 3×3 matrices, it's the (signed) volume of the parallelepiped.

For a 3×3 matrix, the determinant can be computed by cofactor expansion along any row or column. The pattern extends to larger matrices, though computation becomes expensive ($O(n!)$ operations).

:::{warning} Numerical Caution
Computing determinants directly is numerically unstable for large matrices. Use `np.linalg.slogdet()` for the log-determinant when you only need the sign and magnitude separately — this avoids overflow/underflow issues.
:::

:::{important} 🎯 Why This Matters for Your Projects

**In Project 2**: Leapfrog integrator is **symplectic** – preserves phase space volume (det = 1), conserving energy over millions of orbits.

**In Project 4-5**: Rank-deficient covariance matrices indicate perfectly correlated parameters — you're not learning independent information about all variables. This is why **regularization** (adding small values to diagonal) is needed to ensure full rank.

**In Neural Networks**: Rank of weight matrices determines information bottlenecks—low rank layers compress information, potentially losing important features.
:::


### 3.5 The Inverse: Undoing Transformations

**Priority: 🟡 Important** - Critical for solving systems

```{margin}
**matrix inverse**
The transformation that undoes another: $A^{-1}A = I$

```

The **inverse** matrix $A^{-1}$ satisfies:
$$A^{-1}A = AA^{-1} = I$$

For a 2×2 matrix:
$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \implies A^{-1} = \frac{1}{\det(A)}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

Notice you divide by the determinant – this is why singular matrices (det = 0) have no inverse!

**Bridge to Module 0b**: These matrix operations become statistical in Module 0b, where $A^T A$ creates covariance matrices encoding correlations. The transpose operation you learned here will be essential for understanding how data matrices generate covariance structures.

### Progressive Problems: Matrices

::::{note} 📝 Practice Problems

**Level 1**: Show that rotation matrices preserve lengths (hint: check that $|R\vec{v}| = |\vec{v}|$).

**Level 2**: Prove that the determinant of a product equals the product of determinants: $\det(AB) = \det(A)\det(B)$.

**Level 3**: Find conditions on matrix $A$ such that $A^2 = I$ (such matrices are called involutions).

:::{tip} Solutions
:class: dropdown

**Level 1**: For rotation matrix $R$, we have $R^TR = I$ (orthogonal property). Then:
$|R\vec{v}|^2 = (R\vec{v})^T(R\vec{v}) = \vec{v}^TR^TR\vec{v} = \vec{v}^T\vec{v} = |\vec{v}|^2$ ✓

**Level 2**: This follows from the multiplicative property of determinants. Geometrically: if $A$ scales volumes by factor $\det(A)$ and $B$ by $\det(B)$, then $AB$ scales by $\det(A) \cdot \det(B)$.

**Level 3**: $A^2 = I$ means $A = A^{-1}$. This requires eigenvalues to be ±1 (since if $A\vec{v} = \lambda\vec{v}$, then $A^2\vec{v} = \lambda^2\vec{v} = \vec{v}$, so $\lambda^2 = 1$). Examples: reflections, 180° rotations.
:::
::::

:::{admonition} 📌 Key Takeaway
:class: important

Matrices are **transformations**, not just number grids. Every matrix tells a geometric story: rotations preserve lengths, scalings stretch space, projections collapse dimensions. When you multiply matrices, you're composing transformations. This geometric view transforms abstract calculations into visual understanding. These matrix operations become statistical in Module 0b,
where $A^T A$ creates covariance matrices encoding correlations.
:::

---
(part-4-eigenvalues)=
## Part 4: Eigenvalues and Eigenvectors - Finding Invariant Structure

**Priority: 🟡 Important** - Critical for stability analysis and convergence

:::{hint} 📅 When You'll Use This
:class: dropdown

- **First appears in**: Project 2 (orbital stability)
- **Critical for**: Projects 4-5 (convergence, optimization)
- **Returns in**: Final Project (neural network training dynamics)

Skip on first reading if time-constrained, return when starting Project 2.
:::

:::{admonition} 🔭 Where We're Going
:class: note

**Eigenvalues** and **eigenvectors** reveal the hidden skeleton of a transformation. We'll discover special directions that don't rotate (only stretch or shrink), and see how these invariant directions determine everything from system stability to convergence rates. This is where linear algebra reveals the deep structure of physical systems.
:::

:::{admonition} 📚 Prerequisites Check
:class: hint

Before this section, ensure you can:
- [ ] Explain why matrix multiplication is not commutative
- [ ] Identify when a matrix is singular by its determinant
- [ ] Calculate determinants of 2×2 and 3×3 matrices

Review Section 3 if needed.
:::

### 4.1 The Eigenvalue Equation: Directions That Don't Rotate {#part-4-eigenvalues}

```{margin}
**eigenvector**
A vector that is only scaled (not rotated) by a transformation

**eigenvalue**
The scaling factor for an eigenvector
```

Some special vectors are only scaled by a transformation:

$$A\vec{v} = \lambda\vec{v}$$

These **eigenvectors** $\vec{v}$ and their **eigenvalues** $\lambda$ reveal fundamental structure.

**Geometric Intuition**: Imagine stretching a rubber sheet. Most directions get rotated as the sheet deforms, but along eigenvector directions, points only move closer to or farther from the origin without changing direction. These are the "natural axes" of the transformation.

**Physical Example - Spinning Objects**:

Consider a football. It has three principal axes:
- Long axis (through the points)
- Two short axes (perpendicular to long axis)
  - Spin it around the long axis → stable rotation
  - Spin it around a short axis → stable rotation
  - Spin it at any other angle → it wobbles!

The principal axes are eigenvectors of the moment of inertia tensor.

::::{note} 🧠 Build Your Intuition: Eigenvalues

Without calculating, predict the eigenvalues:
1. Identity matrix I → eigenvalues are all ___?
2. Matrix 2I (doubles all vectors) → eigenvalues are all ___?
3. Rotation matrix (90°) → eigenvalues are ___? (Hint: what real vectors don't change direction?)

::::{tip} Answers
:class: dropdown
1. All 1
2. All 2
3. Complex with |λ|=1. For a 90° rotation in 2D, eigenvalues are $e^{±iπ/2} = ±i$. No real vectors maintain their direction under 90° rotation, hence complex eigenvalues that explicitly encode the rotation angle!
:::
::::

### 4.2 Finding Eigenvalues: The Characteristic Equation

```{margin}
**characteristic equation**
$\det(A - \lambda I) = 0$, whose roots are eigenvalues

**trace**
Sum of diagonal elements, equals sum of eigenvalues
```

To find eigenvalues:

1. Rearrange: $(A - \lambda I)\vec{v} = \vec{0}$
2. For non-trivial solutions: $\det(A - \lambda I) = 0$
3. This gives the **characteristic equation**

For an $n×n$ matrix, the characteristic polynomial has degree $n$, potentially yielding $n$ eigenvalues (counting multiplicity) in the complex numbers. The **trace** (sum of diagonal elements) equals the sum of eigenvalues.

:::{admonition} 📝 Worked Example: Complete Eigenvalue and Eigenvector Calculation
:class: note

**Priority: 🟡 Important** - You'll do this for stability analysis

Find eigenvalues AND eigenvectors of:
$$A = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$$

**Step 1**: Set up characteristic equation:
$$\det(A - \lambda I) = \det\begin{pmatrix} 3-\lambda & 1 \\ 1 & 3-\lambda \end{pmatrix} = 0$$

**Step 2**: Calculate determinant:
$$(3-\lambda)^2 - 1 = 0$$
$$\lambda^2 - 6\lambda + 8 = 0$$

**Step 3**: Solve quadratic:
$$\lambda = \frac{6 \pm \sqrt{36-32}}{2} = \frac{6 \pm 2}{2}$$

Therefore: $\lambda_1 = 4$, $\lambda_2 = 2$

**Step 4**: Find eigenvector for $\lambda_1 = 4$:

Solve $(A - 4I)\vec{v} = \vec{0}$:
$$\begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

This gives: $-v_1 + v_2 = 0$, so $v_1 = v_2$

Eigenvector: $\vec{v}_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$ (or any scalar multiple)

**Step 5**: Find eigenvector for $\lambda_2 = 2$:

Solve $(A - 2I)\vec{v} = \vec{0}$:
$$\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

This gives: $v_1 + v_2 = 0$, so $v_1 = -v_2$

Eigenvector: $\vec{v}_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$

**Verification**: Check $A\vec{v}_1 = 4\vec{v}_1$ ✓ and $A\vec{v}_2 = 2\vec{v}_2$ ✓

**Physical Meaning**: This matrix stretches by factor 4 along the diagonal direction $(1,1)$ and by factor 2 along the anti-diagonal $(1,-1)$.
:::

### 4.3 Physical Meaning Throughout Your Projects

**Physical Intuition: Why eigenvalues determine stability**

Consider a star cluster near equilibrium. Small perturbations evolve as:
$$\delta x(t) = e^{\lambda t} v$$

- If $\lambda < 0$: perturbation decays → stable (like a ball in a valley)
- If $\lambda > 0$: perturbation grows → unstable (like a ball on a hill)  
- If $\lambda$ is complex: oscillation with growth/decay (spiral behavior)

The largest eigenvalue determines the fate: even one positive eigenvalue means the system will eventually fly apart!

For instance, a 2D rotation matrix has eigenvalues $e^{±iθ}$, where the imaginary unit explicitly encodes the rotation angle $θ$. This shows how complex eigenvalues naturally describe oscillatory behavior in physical systems.

Eigenvalues appear in most projects in this course:

| Project | Where Eigenvalues Appear | What They Tell You |
|---------|-------------------------|-------------------|
| Project 2 | Linearized dynamics near equilibrium | Orbital stability (stable if all $\lambda < 0$) |
| Project 3 | Scattering matrix | Preferred scattering directions |
| Project 4 | MCMC transition matrix | Convergence rate: $\sim 1/\|1-\lambda_2\|$ where $\lambda_2$ is the second-largest eigenvalue by absolute value (with $\|\lambda_2\| < 1$) |
| Project 5 | GP kernel matrix | Effective degrees of freedom |
| Final Project | Neural network Hessian | Optimization landscape curvature |

:::{admonition} 💡 Deep Connection: Why Symmetric Matrices Are Special
:class: note

**Priority: 🟡 Important for Projects 4-5**

**The Spectral Theorem** guarantees that symmetric matrices have:
1. All real eigenvalues
2. Orthogonal eigenvectors

This isn't mathematical coincidence – it's physical necessity! Symmetric matrices represent quantities where direction doesn't matter for the relationship (like forces between particles). If eigenvalues could be complex, we'd have complex energies or distances, which is nonsensical. Mathematics enforces physical reasonableness!
:::

:::{tip} 🌟 The More You Know: Jacobi's Method Born from Astronomy
:class: dropdown

**Priority: 🟢 Enrichment**

Carl Gustav Jacob Jacobi (1804-1851) developed his famous eigenvalue algorithm while studying the rotation of celestial bodies. In 1846, he published "Über ein leichtes Verfahren die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen" (*On an easy method to numerically solve equations occurring in the theory of secular perturbations*).

The problem arose from calculating planetary perturbations — small gravitational influences planets exert on each other. These perturbations accumulate over centuries (hence "secular") and are described by symmetric matrices whose eigenvalues determine the long-term stability of orbits.

Jacobi's insight was to diagonalize the matrix through a sequence of rotations, each zeroing out one off-diagonal element. Though computers didn't exist, his method was designed for hand calculation — each step is simple enough to do with pencil and paper. Today, variants of Jacobi's method run on every supercomputer simulating galaxy collisions or climate models.

The next time your code calls `numpy.linalg.eigh()`, remember: you're using an algorithm invented to predict whether the solar system is stable over millions of years!

*Source: Jacobi, C.G.J. (1846). Journal für die reine und angewandte Mathematik (Crelle's Journal), 30, pp. 51-94.*
:::

:::{note} 📚 Mathematical Deep Dive: Proof that Symmetric Matrices Have Real Eigenvalues
:class: dropdown

**Priority: 🟢 Enrichment**

This proof reveals why physics "prefers" symmetric matrices.

**Theorem**: Every real symmetric matrix has only real eigenvalues.

**Proof**:
Let $A$ be a real symmetric matrix and suppose $\lambda$ is an eigenvalue with eigenvector $\vec{v}$. We'll show $\lambda$ must be real.

Consider the complex conjugate of the eigenvalue equation:
$$A\vec{v} = \lambda\vec{v}$$

Taking complex conjugates:
$$\overline{A\vec{v}} = \overline{\lambda\vec{v}}$$

Since $A$ is real: $A\overline{\vec{v}} = \overline{\lambda}\overline{\vec{v}}$

Now compute $\vec{v}^* A \vec{v}$ in two ways:

**Method 1:** $\vec{v}^* A \vec{v} = \vec{v}^* (\lambda \vec{v}) = \lambda (\vec{v}^* \vec{v}) = \lambda |\vec{v}|^2$

**Method 2:** $\vec{v}^* A \vec{v} = (A^T \vec{v})^* \vec{v} = (A\vec{v})^* \vec{v}$ (since $A = A^T$)
         $= (\lambda\vec{v})^* \vec{v} = \overline{\lambda} \vec{v}^* \vec{v} = \overline{\lambda} |\vec{v}|^2$

Therefore: $\lambda |\vec{v}|^2 = \overline{\lambda} |\vec{v}|^2$

Since $|\vec{v}|^2 > 0$ (eigenvector is non-zero):
$$\lambda = \overline{\lambda}$$

This means $\lambda$ is real! ∎

**Physical Interpretation**: Symmetric matrices represent measurements where the order doesn't matter (distance from A to B equals distance from B to A). Complex eigenvalues would imply complex measurements, violating physical reality.
:::

### Progressive Problems: Eigenvalues

::::{note} 📝 Practice Problems

**Level 1**: Find the eigenvalues of $\begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix}$ by inspection.

**Level 2**: Prove that if $\lambda$ is an eigenvalue of $A$, then $\lambda^2$ is an eigenvalue of $A^2$.

**Level 3**: Show that positive definite matrices have all positive eigenvalues.

:::{tip} Solutions
:class: dropdown

**Level 1**: For diagonal matrices, eigenvalues are the diagonal elements: $\lambda_1 = 2$, $\lambda_2 = 3$. The eigenvectors are the standard basis vectors.

**Level 2**: If $A\vec{v} = \lambda\vec{v}$, then $A^2\vec{v} = A(A\vec{v}) = A(\lambda\vec{v}) = \lambda(A\vec{v}) = \lambda(\lambda\vec{v}) = \lambda^2\vec{v}$. Thus $\lambda^2$ is an eigenvalue of $A^2$ with the same eigenvector.

**Level 3**: For positive definite $A$, we have $\vec{v}^TA\vec{v} > 0$ for all $\vec{v} \neq 0$. For eigenvector $\vec{v}$ with eigenvalue $\lambda$: $\vec{v}^TA\vec{v} = \vec{v}^T(\lambda\vec{v}) = \lambda|\vec{v}|^2 > 0$. Since $|\vec{v}|^2 > 0$, we must have $\lambda > 0$.
:::
::::

:::{admonition} 📌 Key Takeaway
:class: important

Eigenvalues and eigenvectors are the DNA of a matrix. They reveal invariant directions (eigenvectors) and scaling factors (eigenvalues) that determine stability, convergence, and long-term behavior. When all eigenvalues are negative, systems are stable. When they're positive, systems grow. When they're complex, systems oscillate. Master this concept and you can predict the fate of any linear system.
:::

---

(part-5-numerics)=
## Part 5: Numerical Reality - When Mathematics Meets Silicon (Essential Sections)

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

(floating-point-truth)=
### 7.1 The Harsh Truth About Floating-Point Arithmetic

```{margin}
**floating-point**
Computer representation of real numbers with finite precision using scientific notation in binary
```

```{margin}
**machine epsilon**
Smallest distinguishable floating-point increment (~2.2×10⁻¹⁶ for float64); the gap between 1 and the next representable number
```

Computers can't store infinite decimals, so they approximate real numbers using a finite representation:
$$x = \pm m \times 2^e$$

where $m$ is the mantissa (fractional part) and $e$ is the exponent. Think of it as scientific notation in binary.

**What This Means for 64-bit Doubles**:
- 15-17 significant decimal digits (53 bits of mantissa precision, guaranteeing at least 15 decimal digits)
- Largest number: ~10^308 (exponent can go up to 1023)
- Smallest positive normal: ~10^-308 (exponent down to -1022)
- **Machine epsilon**: ~2.22×10^-16 (smallest distinguishable relative difference near 1.0)

**The Shocking Truth About 0.1**:
```python
0.1 + 0.2 == 0.3  # False!
print(f"{0.1 + 0.2:.17f}")  # 0.30000000000000004

# Why? 0.1 in binary is actually:
# 0.00011001100110011001100110011... (repeating forever!)
# The computer truncates this at 53 bits, creating rounding error
```

Just like 1/3 = 0.333... repeats forever in decimal, 1/10 repeats forever in binary. The computer must truncate, introducing tiny errors that compound.

**Catastrophic Cancellation - The Silent Killer**:

When you subtract nearly equal numbers, you lose precision catastrophically. Here's why:

```python
# Example: Computing small angles in astronomy
star_position_1 = 89.99999999  # degrees (16 digits total)
star_position_2 = 90.00000001  # degrees (16 digits total)

angle_difference = star_position_2 - star_position_1
# Result: 0.00000002 (only 1 significant digit!)
# We went from 16 digits of precision to 1!

# Better approach: Reformulate to avoid subtraction
# Instead of (A + small) - A, compute small directly
```

**Real Project 2 Example - Gravitational Forces**:
```python
# BAD: Force between very close stars
def gravitational_force_bad(pos1, pos2, m1, m2):
    dx = pos2[0] - pos1[0]  # Catastrophic if positions nearly equal!
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    r_squared = dx**2 + dy**2 + dz**2  # Can become 0 or negative!
    return G * m1 * m2 / r_squared  # Division by ~0!

# GOOD: With softening parameter (regularization)
def gravitational_force_good(pos1, pos2, m1, m2, epsilon=1e-4):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    r_squared = dx**2 + dy**2 + dz**2 + epsilon**2  # Never zero!
    return G * m1 * m2 / r_squared
```

:::{admonition} 📝 Understanding Floating-Point Spacing
:class: note

Floating-point numbers aren't evenly spaced! The gap between consecutive numbers grows with magnitude:

- Near 1: gap ≈ 2.2×10^-16
- Near 1000: gap ≈ 2.2×10^-13
- Near 10^6: gap ≈ 2.2×10^-10

This means:
```python
1.0 + 1e-16 == 1.0  # True! Gap too small to represent
1000.0 + 1e-13 == 1000.0  # True! 
1e6 + 1e-10 == 1e6  # True!
```

**Why this matters**: In Project 2, if your star cluster has positions at ~10^6 cm from origin, you can't resolve position changes smaller than 10^-10 cm. This affects your timestep choice and integration accuracy!
:::

:::{warning} 🎯 Project-Specific Numerical Gotchas

**Project 1**: Fitting power laws to IMF
- Log-transform creates infinities for zero masses
- **Fix:** Add small offset or use robust fitting

**Project 2**: N-body integration
- Close encounters cause force singularities
- **Fix:** Gravitational softening parameter

**Project 3**: Monte Carlo sampling
- Random numbers in [0,1) can give $\log(0) = -∞$
- **Fix:** Use (0,1] or add tiny epsilon
:::
(condition-numbers)=
### 7.2 Condition Numbers: Measuring Numerical Danger

```{margin}
**condition number**
κ(A) = σ_max/σ_min, ratio of largest to smallest singular value; measures how much errors amplify
```

The condition number tells you how much input errors get amplified:

$$\frac{||\delta x||}{||x||} \leq \kappa(A) \frac{||\delta b||}{||b||}$$

This means: relative error in solution ≤ condition number × relative error in input.

**Intuitive Understanding**:
- κ = 1: Perfect! Errors don't amplify
- κ = 100: 1% input error → up to 100% output error
- κ = 10^6: Lose 6 digits of accuracy
- κ = 10^16: Complete garbage (for float64)

| κ(A) | Interpretation | What It Means for You |
|------|----------------|----------------------|
| < 10 | Excellent | Trust your results |
| 10-100 | Good | Minor accuracy loss |
| 100-1000 | Acceptable | Check residuals |
| 10^3-10^6 | Problematic | Need careful algorithms |
| > 10^6 | Dangerous | Consider reformulation |
| > 10^10 | Numerically singular | Add regularization |
| ≈ 10^16 | Complete failure | Matrix is effectively rank-deficient |

**Real Example - Why Your Stellar Population Fits Fail**:
```python
# Fitting mass-luminosity relation: L = a*M^b
# Taking logs: log(L) = log(a) + b*log(M)

# Design matrix for 3 stars with similar masses
M = np.array([0.99, 1.00, 1.01])  # Solar masses
X = np.column_stack([np.ones(3), np.log(M)])

# Check condition number
print(f"Condition number: {np.linalg.cond(X):.1e}")
# Output: 4.5e+03 (problematic!)

# Why? The log(M) values are nearly identical!
# log(0.99) ≈ -0.0101, log(1.00) = 0, log(1.01) ≈ 0.0100
# The columns are nearly parallel → high condition number

# Fix: Use centered/scaled variables
M_scaled = (M - M.mean()) / M.std()
X_better = np.column_stack([np.ones(3), M_scaled])
print(f"Better condition number: {np.linalg.cond(X_better):.1e}")
# Output: 2.4e+00 (excellent!)
```

## Emergency Debugging Checklist

:::{admonition} 🚨 When Your Code Breaks: Emergency Fixes
:class: warning

When things go wrong, check these in order:

```python
# 1. Check for singular matrix
assert np.linalg.det(A) != 0, "Matrix is singular"

# 2. Check condition number
assert np.linalg.cond(A) < 1e10, f"Poorly conditioned: κ={np.linalg.cond(A):.2e}"

# 3. Check for symmetry (if expected)
assert np.allclose(A, A.T), "Matrix not symmetric"

# 4. Check positive definiteness (for covariance)
assert np.linalg.eigvalsh(A).min() > 0, "Not positive definite"

# 5. Common fixes:
# Add regularization
A_reg = A + 1e-6 * np.eye(len(A))

# Force symmetry
A_sym = (A + A.T) / 2

# Use least squares instead of solve
x = np.linalg.lstsq(A, b, rcond=None)[0]
```
:::

:::{admonition} 📌 Key Takeaway
:class: important

Computers aren't mathematical ideals—they're finite machines with finite precision. Every number is approximate, every operation loses accuracy, and errors compound rapidly. But with awareness and proper techniques, you can write robust code that handles numerical reality gracefully.

Remember:
- Check condition numbers before trusting results
- Never compute explicit inverses
- Add regularization when matrices are near-singular
- Test your code with pathological cases
- When in doubt, use SVD (see [Module 0b](./00b-linear-algebra-module.md)) — it's the most stable decomposition

These aren't edge cases you might encounter — these are daily realities in computational astrophysics. Master them now, and save yourself countless debugging hours later!
:::

---

## Essential SciPy Linear Algebra Reference {#essential-scipy-reference}

**Priority: 🔴 Essential** - Keep this open while coding

```{list-table} Quick Function Reference
:header-rows: 1

* - Task
  - Function
  - When to Use
  - Numerical Stability
* - Solve $A\vec{x}=\vec{b}$
  - `scipy.linalg.solve(A, b)`
  - General square systems
  - ⭐⭐⭐⭐
* - Solve positive definite
  - `scipy.linalg.cho_solve()`
  - Covariance matrices
  - ⭐⭐⭐⭐⭐
* - Least squares
  - `scipy.linalg.lstsq()`
  - Overdetermined systems
  - ⭐⭐⭐⭐⭐
* - Eigenvalues (general)
  - `scipy.linalg.eig()`
  - Non-symmetric matrices
  - ⭐⭐⭐
* - Eigenvalues (symmetric)
  - `scipy.linalg.eigh()`
  - Symmetric/Hermitian
  - ⭐⭐⭐⭐⭐
* - SVD
  - `scipy.linalg.svd()`
  - Any matrix, rank
  - ⭐⭐⭐⭐⭐
* - Matrix exponential
  - `scipy.linalg.expm()`
  - Time evolution
  - ⭐⭐⭐⭐
* - Condition number
  - `numpy.linalg.cond()`
  - Check stability
  - N/A
```

---

(cheat-sheet)=
## One-Page Cheat Sheet

:::{admonition} 📋 Linear Algebra Quick Reference
:class: tip

### Essential Formulas

**Vector Operations**
- Dot product: $\vec{a} \cdot \vec{b} = \sum_i a_i b_i = |\vec{a}||\vec{b}|\cos\theta$
- Cross product magnitude: $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$
- Vector norm: $|\vec{v}| = \sqrt{\vec{v} \cdot \vec{v}}$

**Matrix Operations**
- Matrix multiplication: $(AB)_{ij} = \sum_k A_{ik}B_{kj}$
- Transpose: $(A^T)_{ij} = A_{ji}$
- Inverse (2×2): $\begin{pmatrix}a&b\\c&d\end{pmatrix}^{-1} = \frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$
- Determinant (2×2): $\det\begin{pmatrix}a&b\\c&d\end{pmatrix} = ad-bc$

**Eigenvalues & Eigenvectors**
- Definition: $A\vec{v} = \lambda\vec{v}$
- Characteristic equation: $\det(A - \lambda I) = 0$
- For symmetric matrices: real eigenvalues, orthogonal eigenvectors

### Critical NumPy/SciPy Commands

| Task | Command | When to Use |
|------|---------|-------------|
| Solve $A\vec{x}=\vec{b}$ | `np.linalg.solve(A, b)` | Linear systems |
| Eigenvalues (symmetric) | `np.linalg.eigh(A)` | Symmetric matrices |
| Condition number | `np.linalg.cond(A)` | Check numerical stability |
| Pseudoinverse | `np.linalg.pinv(A)` | Rank-deficient systems |

### Numerical Stability Rules

1. **Never invert matrices**: Use `solve()` not `inv()`
2. **Check condition numbers**: κ > 10^6 means trouble
3. **Add jitter for stability**: `A_stable = A + 1e-6 * I`
4. **Symmetrize when needed**: `A_sym = (A + A.T) / 2`
5. **Use appropriate precision**: float64 for science, float32 for ML

### Physical Interpretations

| Mathematical Object | Physical Meaning |
|-------------------|------------------|
| Dot product | Work done, projection |
| Cross product | Angular momentum, torque |
| Eigenvalues | Natural frequencies, stability |
| Eigenvectors | Principal axes, normal modes |
| Determinant | Volume scaling, invertibility |
| Symmetric matrix | Reciprocal relationships |
| Orthogonal matrix | Rotation, preserves lengths |

### Key Insights by Project

**Project 1**: Vectorization = matrix operations on entire arrays  
**Project 2**: Conservation laws = preserved matrix properties  
**Project 3**: Scattering = transformation matrices  
**Project 4**: MCMC convergence = second eigenvalue  

### Emergency Debugging

```python
# Matrix is singular or near-singular
if np.linalg.cond(A) > 1e10:
    A = A + 1e-6 * np.eye(len(A))  # Add regularization

# Eigenvalues should be real but aren't
if not np.allclose(A, A.T):
    A = (A + A.T) / 2  # Force symmetry
```
:::

---

## Glossary of Terms

All terms introduced in this module:

- **basis**: A set of linearly independent vectors that span the entire vector space
- **characteristic equation**: $\det(A - \lambda I) = 0$, whose roots are eigenvalues
- **components**: The scalar coefficients representing a vector in a chosen basis
- **condition number**: κ(A) = σ_max/σ_min, ratio of largest to smallest singular value; measures how much errors amplify
- **conservation law**: A physical quantity that remains constant over time due to an underlying symmetry
- **cross product**: Vector operation producing a perpendicular vector: $\vec{a} \times \vec{b}$
- **determinant**: Scalar value measuring how a linear transformation scales volumes
- **dot product**: Scalar operation on vectors: $\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$
- **eigenvalue**: The scaling factor for an eigenvector
- **eigenvector**: A vector that is only scaled (not rotated) by a transformation
- **floating-point**: Computer representation of real numbers with finite precision using scientific notation in binary
- **globular cluster**: A spherical collection of 10⁴ to 10⁶ stars bound by gravity, orbiting as satellites of galaxies
- **linear algebra**: The branch of mathematics concerning vector spaces and linear transformations between them
- **linear independence**: Vectors that cannot be written as linear combinations of each other
- **linearity**: Property where $f(αx + βy) = αf(x) + βf(y)$ for all scalars α, β and vectors x, y
- **machine epsilon**: Smallest distinguishable floating-point increment (~2.2×10⁻¹⁶ for float64); the gap between 1 and the next representable number
- **matrix**: A linear transformation represented as a rectangular array of numbers
- **matrix inverse**: The transformation that undoes another: $A^{-1}A = I$
- **matrix multiplication**: Operation combining two transformations into one: $(AB)\vec{v} = A(B\vec{v})$
- **orthogonal**: Perpendicular; vectors with zero dot product
- **orthonormal**: Basis vectors that are both orthogonal (perpendicular) and normalized (unit length)
- **parameter**: Most fundamentally: a number that controls the behavior of a mathematical function or system. In physics: quantities like mass, temperature, or coupling constants that define system properties but are not the variables being solved for
- **parameter space**: The space of all possible parameter values; each point represents a different configuration or model of the system
- **phase space**: The space of all possible states of a system; for N particles in 3D, has 6N dimensions (3 position + 3 velocity per particle)
- **rank**: The number of linearly independent rows (or columns) in a matrix; the dimension of the space the matrix actually maps to
- **scalar**: A quantity with magnitude only, represented by a single number
- **symplectic**: Transformation preserving phase space volume (determinant = 1)
- **trace**: Sum of diagonal elements, equals sum of eigenvalues
- **trajectory**: The path traced by a system's state through phase space as it evolves in time
- **transformation**: A function mapping vectors to vectors that preserves vector space structure
- **transpose**: Operation swapping rows and columns: $(A^T)_{ij} = A_{ji}$
- **vector**: A mathematical object with both magnitude and direction that transforms according to specific rules
- **vector space**: A set equipped with addition and scalar multiplication operations satisfying eight specific axioms

---

## Main Takeaways

:::{admonition} 🎯 Essential Points to Remember
:class: important

Core linear algebra is the mathematical infrastructure of classical computational astrophysics:

1. **Vectors encode physical quantities** with magnitude and direction, existing independently of coordinate systems

2. **Matrices are transformations**, not just number grids – they preserve linear structure while changing representations

3. **Eigenvalues and eigenvectors reveal invariant properties** that determine stability, convergence, and fundamental modes

4. **Conservation laws manifest as mathematical structures** – symmetries become properties of vectors and matrices

5. **Matrix operations enable vectorization** – transforming slow loops into fast array operations

6. **The dot and cross products** encode fundamental physics: work/projection and angular momentum/rotation

7. **Numerical precision requires care** – understand determinants, condition numbers, and when matrices fail

8. **The same mathematics spans classical, statistical, and machine learning domains** – linear algebra unifies all.

*Continue to Module 0b for positive definite matrices, covariance, and the statistical foundations needed for Projects 4-6.*
:::

---

## Essential NumPy/SciPy Reference for Module 0a

**Priority: 🔴 Essential** - Keep this open while coding Projects 1-3

```{list-table} Core Linear Algebra Functions
:header-rows: 1

* - Task
  - Function
  - When to Use
  - Project
* - Dot product
  - `np.dot(a, b)` or `a @ b`
  - Work, projections
  - All
* - Cross product
  - `np.cross(a, b)`
  - Angular momentum
  - P2
* - Matrix multiply
  - `A @ B` or `np.matmul(A, B)`
  - Transformations
  - All
* - Solve Ax=b
  - `np.linalg.solve(A, b)`
  - Linear systems
  - P2-3
* - Eigenvalues
  - `np.linalg.eig(A)`
  - Stability analysis
  - P2
* - Determinant
  - `np.linalg.det(A)`
  - Check invertibility
  - P2-3
* - Matrix norm
  - `np.linalg.norm(A)`
  - Error estimates
  - All
* - Inverse (avoid!)
  - `np.linalg.inv(A)`
  - Use solve() instead
  - -
```

---

(quickref)=
## Module 0a Quick Reference Card

:::{admonition} 📋 Classical Linear Algebra Quick Reference
:class: tip

### Essential Formulas

**Vector Operations**
- Dot product: $\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta$
- Cross product: $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$
- Vector norm: $|\vec{v}| = \sqrt{\vec{v} \cdot \vec{v}}$

**Matrix Properties**
- Determinant = 0 → Singular (non-invertible)
- Eigenvalue equation: $A\vec{v} = \lambda\vec{v}$
- Trace = Sum of eigenvalues

**Conservation Laws**
- Energy → Quadratic forms
- Momentum → Vector sums
- Angular momentum → Cross products

### Physical Interpretations

| Math Object | Project 1 | Project 2 | Project 3 |
|-------------|-----------|-----------|-----------|
| Vectors | Star properties | Positions, velocities | Photon directions |
| Matrices | Population transforms | Rotation, scaling | Scattering |
| Eigenvalues | - | Orbital stability | Scattering modes |
| Dot product | - | Work, energy | Intensity |
| Cross product | - | Angular momentum | - |

### Vectorization Pattern
```python
# Slow (avoid):
for i in range(N):
    result[i] = operation(data[i])

# Fast (use):
result = operation(data)  # NumPy operates on entire array
```

### Common Bugs & Fixes

**Problem**: Matrix is singular
**Fix**: Check determinant, add small regularization

**Problem**: Cross product gives wrong direction  
**Fix**: Check order: $\vec{a} \times \vec{b} = -\vec{b} \times \vec{a}$

**Problem**: Eigenvalues are complex for physical system
**Fix**: Ensure matrix is symmetric: `A = (A + A.T) / 2`
:::

## Next Steps

With this mathematical foundation firmly in place, you're ready to tackle the computational challenges of modern astrophysics. In Project 1, you'll immediately apply vector operations and matrix manipulations to handle stellar populations efficiently. In Project 2, you'll see how eigenvalues determine orbital stability. 

Module 0b continues with positive definite matrices, advanced topics, and the bridge to machine learning. Together, these modules provide the complete linear algebra foundation for computational astrophysics.

**Remember:** every algorithm you implement ultimately reduces to linear algebra. When numerical issues arise – and they will – return to these foundations. Check condition numbers, verify matrix properties, use appropriate decompositions. The mathematics you've learned here isn't separate from computation – it IS computation in its purest form.

---

*Welcome to computational astrophysics. You now speak its language.*