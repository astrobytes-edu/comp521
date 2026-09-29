---
title: "ODE Methods: The Beautiful Failure"
subtitle: "COMP 521 adaptation · editorial draft"
author: Anna Rosen
---

## Learning Objectives

By the end of this lecture, you will be able to:

::::::::::::::::::::::::{slide-incremental}

- **Derive** Euler's method from a Taylor series and explain why it fails
- **Translate** mathematical formulas into working Python code (RK2)
- **Explain** why higher-order methods (RK4) and symplectic methods (Leapfrog) exist
- **Predict** which integrator to choose for a given problem
- **Connect** these methods to COMP 521 Project 4; compare with the original N-body case study

::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 0-1 min. Read objectives aloud. Emphasize the equation-to-code skill.
::::::::::::::::::::::::

## The Dynamic Universe

::::::::::::::::::::::::{speaker-note}
Time: 1-5 min. Hook: everything in science changes with time.
::::::::::::::::::::::::

## From Stars to Star Clusters

In the COMP 536 case study, COMP 536 Project 1 modeled **stellar populations** — where stars land on the HR diagram:

[Watch the original lecture video](https://www.youtube.com/watch?v=mY2edzGYWyU)

*External video; internet connection required.*

::::::::::::::::::::::::{fragment}
But real stars **move.** They orbit, interact, and evolve dynamically. That was the COMP 536 Project 2 application.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 1-2 min. "This is what COMP 536 Project 1 was about — the static picture. Now we add time."
::::::::::::::::::::::::

## The N-body Problem in Action

In COMP 536 Project 2, you'll simulate **gravitational dynamics** — stars moving under each other's gravity:

[Watch the original lecture video](https://www.youtube.com/watch?v=QI3FDzn7p3k)

*External video; internet connection required.*

::::::::::::::::::::::::{fragment}
To make this work, we need to solve **ordinary differential equations** numerically. That's today's lecture.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 2-4 min. "This is Omega Centauri — a real globular cluster with millions of stars. Your COMP 536 Project 2 code will simulate the same physics, just with fewer particles. The methods you learn today are how we bridge the gap from Newton's laws to this."
::::::::::::::::::::::::

## The Language of Change

::::::::::::::::::::::::{slide-columns}
:::::::::::::::::::::::{slide-column}

### Everywhere in Science

- Population growth: $\frac{dN}{dt} = rN$
- Radioactive decay: $\frac{dN}{dt} = -\lambda N$
- Newton's 2nd law: $m\frac{d^2x}{dt^2} = F$
- Heat flow: $\frac{\partial T}{\partial t} = \kappa \nabla^2 T$

:::::::::::::::::::::::

:::::::::::::::::::::::{slide-column}

::::::::::::::::::::::{fragment}

### The Common Pattern

Every one of these has the form:

$$\frac{d\mathbf{y}}{dt} = \mathbf{f}(t, \mathbf{y})$$

**Ordinary Differential Equations** (ODEs) are the language of change.

::::::::::::::::::::::

:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 1-3 min. "If it changes with time, it is an ODE."
::::::::::::::::::::::::

## The Fundamental Problem

::::::::::::::::::::::::{note}
### The Initial Value Problem (IVP)

Given a rate of change and a starting point, predict the future:

$$\frac{d\mathbf{y}}{dt} = \mathbf{f}(t, \mathbf{y}), \qquad \mathbf{y}(t_0) = \mathbf{y}_0$$
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
Mathematics gives us the recipe for change. Computers can only do arithmetic.

**How do we bridge the gap?**
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 3-5 min. "This is the problem we solve today. Three different ways, with three different failure modes."
::::::::::::::::::::::::

## From Continuous to Discrete

::::::::::::::::::::::::{speaker-note}
Time: 5-12 min. The fundamental discretization idea.
::::::::::::::::::::::::

## What Is a State Vector?

A **state vector** captures *everything* about the system right now.

For a mass on a spring: $\;\mathbf{y} = [x,\, v]^T$ — position and velocity. That's it.

::::::::::::::::::::::::{fragment}
Physics tells us how the state changes:

$$\frac{d}{dt}\begin{bmatrix} x \\ v \end{bmatrix} = \begin{bmatrix} v \\ -\omega^2 x \end{bmatrix}$$

- $\dot{x} = v$ (velocity *is* the rate of position change)
- $\dot{v} = -\omega^2 x$ (acceleration from the spring force)
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 5-6 min. "This is the pattern. Position derivative is velocity. Velocity derivative comes from physics."
::::::::::::::::::::::::

## The Key Trick: Converting to First-Order

Physics gives us a **2nd-order** equation: $\;\ddot{x} = -\omega^2 x$

Computers need **1st-order** systems: $\;\dot{\mathbf{y}} = \mathbf{f}(\mathbf{y})$

::::::::::::::::::::::::{fragment}
**The recipe** (you will use this for every project):

1. **Identify your variables:** position $x$ and velocity $v = \dot{x}$
2. **Write the first derivative:** $\dot{x} = v$ (this is just a definition)
3. **Write the second derivative:** $\dot{v} = \ddot{x} = -\omega^2 x$ (this is the physics)
4. **Combine into a system:** $\dot{\mathbf{y}} = \mathbf{f}(\mathbf{y})$ where $\mathbf{y} = [x, v]^T$
::::::::::::::::::::::::


## First-order systems: the N-body case study

```{slide-options}
{"vertical":true}
```

::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{note}
**For COMP 536 Project 2:** Newton's law $m\ddot{\vec{r}} = \vec{F}$ converts the same way. Your state vector will be $[\vec{r}_1, \vec{r}_2, \ldots, \vec{v}_1, \vec{v}_2, \ldots]$ with $6N$ components for $N$ particles.
:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 6-8 min. "This conversion is a core skill. Every 2nd-order physics equation becomes a 1st-order system by introducing velocity as a new variable. You'll do this for gravity in COMP 536 Project 2."
::::::::::::::::::::::::

## The Discretization Idea

The derivative is defined as a limit:

$$\frac{dy}{dt} = \lim_{h \to 0} \frac{y(t+h) - y(t)}{h}$$

::::::::::::::::::::::::{fragment}
Computers cannot take limits. So we **drop the limit** and use finite $h$:

$$\frac{y(t+h) - y(t)}{h} \approx f(t, y)$$
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
**Rearrange** to get a recipe for the future:

$$\boxed{y_{n+1} = y_n + h \cdot f(t_n, y_n)}$$

We just derived **Euler's method.**
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 7-9 min. "This single rearrangement IS Euler's method. The rest is consequences."
::::::::::::::::::::::::

## What Could Possibly Go Wrong?

::::::::::::::::::::::::{slide-incremental}
- We assumed $f$ is **constant** over $[t, t+h]$ — what if it changes?
- We made an error of order $O(h^2)$ **every single step** (Taylor remainder)
- We take $N = T/h$ steps, so errors **accumulate**
- Some errors compound. Some cancel. **The method determines which.**
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 9-10 min. Build tension before the demo.
::::::::::::::::::::::::

## Choosing $h$: The Timestep

How large should $h$ be? Dimensional analysis gives us a rule of thumb:

::::::::::::::::::::::::{slide-incremental}
- Your system has a **characteristic timescale** $T$ (e.g., orbital period, oscillation period)
- About 60–100 points per period can be an illustrative starting point; verify accuracy by refinement and problem-specific tolerances.
- $h = 0.01 T$ gives **100 points per period**; this alone does not establish accuracy.
- **Too large:** solution is inaccurate or unstable
- **Too small:** wastes computation and accumulates round-off error
::::::::::::::::::::::::


## Timestep examples

```{slide-options}
{"vertical":true}
```

::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{note}
**For today's SHO** ($\omega = 1$, period $T = 2\pi$): $h = 0.1$ gives about 63 points per period. Good enough to see the methods' behavior clearly.

**For COMP 536 Project 2** (Earth orbit, period $T = 1$ yr): start with $h = 0.01$ yr.
:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 10-11 min. "This is a practical skill. You'll calibrate timesteps for every simulation."
::::::::::::::::::::::::

## Our Two Test Problems

::::::::::::::::::::::::{slide-columns}
:::::::::::::::::::::::{slide-column}
### Exponential Decay (Warmup)

$$\frac{dy}{dt} = -y, \quad y(0) = 1$$

Exact: $y(t) = e^{-t}$

Simple, monotonic, forgiving.

*Good for building intuition.*
:::::::::::::::::::::::

:::::::::::::::::::::::{slide-column}
### Harmonic Oscillator (Main Event)

$$\ddot{x} = -\omega^2 x$$

State: $\mathbf{y} = [x, v]^T$

Exact: $x(t) = \cos(\omega t)$

Oscillatory, energy-conserving, **punishing**.

*Reveals fundamental flaws.*
:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{note}
We choose these because they have **exact analytical solutions**. If the method fails here, it will fail on harder problems.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 10-12 min. "The SHO is the diagnostic tool of computational physics. If your integrator can't handle a spring, don't trust it with galaxies."
::::::::::::::::::::::::

## Euler's Method

*The simplest idea. The most spectacular failure.*

::::::::::::::::::::::::{speaker-note}
Time: 12-27 min. This is the core of the lecture.
::::::::::::::::::::::::

## The Derivation

Taylor-expand $y(t + h)$ around $t$:

$$\begin{aligned}y(t+h) &= y(t) + h\,y'(t)\\ &\quad + \frac{h^2}{2}\,y''(t) + \cdots\end{aligned}$$

Since $y'(t) = f(t, y)$, **truncate** after the first derivative:

$$\boxed{y_{n+1} = y_n + h \cdot f(t_n, y_n)}$$


## Euler: local and global error

```{slide-options}
{"vertical":true}
```

::::::::::::::::::::::::{fragment}
**Error analysis:**

- **Local** truncation error: $O(h^2)$ — the piece we dropped from Taylor
- We take $N = T/h$ steps, each contributing $O(h^2)$ error
- **Global** error: $N\,O(h^2)=O(h)$ for fixed $T$, since $N=T/h$ — this is a **first-order method**
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 12-13 min. "Everything in numerical methods comes back to Taylor series."
::::::::::::::::::::::::

## What Does "Order" Mean?

The **order** of a method tells you how fast the error shrinks when you reduce $h$:


### The Rule

In the asymptotic convergence regime, at the **same final time**, halving $h$ reduces global error by approximately $2^p$:

| Method | Order $p$ | Halve $h$ → |
|--------|-----------|-------------|
| Euler | 1 | $2\times$ less error |
| RK2 | 2 | $4\times$ less error |
| RK4 | 4 | $16\times$ less error |


## Order and computational cost

```{slide-options}
{"vertical":true}
```

### Why It Matters

To get $10\times$ more accuracy:

- **Euler:** need $10\times$ more steps ($10\times$ slower)
- **RK2:** need $\sim 3\times$ more steps
- **RK4:** need $\sim 1.8\times$ more steps

Higher order can reduce the steps needed for a target error. Compare **cost per step** as well as convergence order.


::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{note}
Where does the order come from? Taylor series. Euler keeps **one** term ($h$). RK4 matches **four** terms ($h, h^2, h^3, h^4$). More terms → error starts at a higher power of $h$.
:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 13-15 min. "This is the single most important concept in numerical methods. Order tells you how efficiently your method converts computational effort into accuracy."
::::::::::::::::::::::::

## Euler in Three Lines of Code

```python
def euler_step(f, t, y, h):
    """One step of Euler's method."""
    return y + h * f(t, y)
```


::::::::::::::::::::::::{fragment}
That is literally all of Euler's method. Three lines.

The rest is choosing $f$ and $h$.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 14-15 min. "Appreciate the simplicity. Now let's see what it does."
::::::::::::::::::::::::

## Warmup: Euler on $\dot{y} = -y$

Exponential decay: $\;\dfrac{dy}{dt} = -y, \quad y(0) = 1 \quad \Longrightarrow \quad y(t) = e^{-t}$


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-2
:view: code
:alt: Executed output for Warmup: Euler on $\dot{y} = -y$.
```


::::::::::::::::::::::::{speaker-note}
Time: 15-16 min. "Simple ODE, exact solution known. Let's see how Euler does."
::::::::::::::::::::::::

## Warmup Result: Euler Works... Okay


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-3
:view: output
:alt: Executed output for Warmup Result: Euler Works... Okay.
```


::::::::::::::::::::::::{speaker-note}
Time: 16-18 min. "Not perfect, but it tracks the solution. Euler looks fine here. Now let's try something harder."
::::::::::::::::::::::::


## Warmup Result: Euler Works... Okay — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-3
:start: 1
t_exact = np.linspace(0, t_end, 200)
fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(t_exact, np.exp(-t_exact), 'k-', lw=2, label='Exact: $e^{-t}$')
ax.plot(t_vals, y_vals, 'ro-', label=f'Euler ($h = {h}$)', markersize=8)
ax.set(xlabel='Time', ylabel='$y(t)$',
       title='Exponential Decay: Euler Works... Okay')
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-3)
## Now the Real Test

For $\dot y=-y$, forward Euler is stable for $0<h<2$ and decays monotonically for $0<h\leq1$. Outside the stability interval, even a decaying exact solution can have growing numerical errors.

::::::::::::::::::::::::{fragment}
What happens when the solution **oscillates** and energy should be **conserved**?
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 18-19 min. Build anticipation before the failure.
::::::::::::::::::::::::

## SHO: Setting Up the Code


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-4
:view: code
:alt: Executed output for SHO: Setting Up the Code.
```


::::::::::::::::::::::::{speaker-note}
Time: 19-20 min. "Same structure as the decay example. The only difference is f_sho returns a 2-component array — the state vector."
::::::::::::::::::::::::


## Numerical detail: where the integration ends

```{slide-options}
{"vertical":true}
```

The source teaching loops take full steps of size $h$ until the requested endpoint is reached or exceeded. When the interval is not divisible by $h$, the last sample lies beyond `t_end`.

Report the **actual returned time** when comparing a numerical sample with the exact solution. The phase-space and energy plots use the returned samples.

A general endpoint-targeting solver can shorten its last step. That is a different stepping policy; do not quietly use variable steps while claiming a fixed-step symplectic comparison.


## SHO: The Diagnostic

$$x(0)=1,\quad v(0)=0$$

$$x(t)=\cos(t),\quad v(t)=-\sin(t)$$

::::::::::::::::::::::::{fragment}
**Our diagnostic** — total energy should be constant:

$$E=\underbrace{\tfrac12v^2}_{\text{kinetic}}+\underbrace{\tfrac12\omega^2x^2}_{\text{potential}}$$

For our initial conditions with $\omega=1$, $E=\tfrac12(v^2+x^2)=0.5$.

If $E$ changes → the method is injecting or removing energy.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 20-21 min. "Energy is the diagnostic. If it changes, the method is lying. This is the same diagnostic you'll use in COMP 536 Project 2 with gravitational energy."
::::::::::::::::::::::::

## The Beautiful Failure: Trajectory




```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-6
:view: output
:alt: Executed output for The Beautiful Failure: Trajectory.
```


::::::::::::::::::::::::{speaker-note}
Time: 21-23 min. "Two things to see: (1) The amplitude is growing — that's energy error, Euler is injecting energy. (2) The peaks are shifting — that's phase error, Euler gets the timing wrong too. Both get worse with time."
::::::::::::::::::::::::


## The Beautiful Failure: Trajectory — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-6
:start: 1
h = 0.1; t_end = 20 * np.pi  # 10 periods
t_euler, y_euler = euler_integrate(f_sho, y0_sho, [0, t_end], h)

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(np.linspace(0, t_end, 2000), np.cos(np.linspace(0, t_end, 2000)),
        'k-', alpha=0.5, lw=1.5, label='Exact')
ax.plot(t_euler, y_euler[:, 0], 'r-', lw=1, label=f'Euler ($h={h}$)')
ax.set(xlabel='Time', ylabel='$x(t)$')
ax.legend()
plt.tight_layout()
plt.show()
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-6)
## Phase Space Reveals the Crime


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-7
:view: output
:alt: Executed output for Phase Space Reveals the Crime.
```


::::::::::::::::::::::::{speaker-note}
Time: 22-24 min. "The circle is the physical orbit in phase space. Euler spirals outward because every step overshoots — the tangent line always lands OUTSIDE the true circle."
::::::::::::::::::::::::


## Phase Space Reveals the Crime — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-7
:start: 1
fig, ax = plt.subplots(figsize=(5, 4))
theta = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(theta), -np.sin(theta), 'k--', lw=2, label='Exact (circle)')
ax.plot(y_euler[:, 0], y_euler[:, 1], 'r-', lw=0.5, alpha=0.7,
        label='Euler (spiral)')
ax.set(xlabel='Position $x$', ylabel='Velocity $v$',
       title='Phase Space: Euler Spirals Outward')
ax.set_aspect('equal')
ax.legend()
plt.tight_layout()
plt.show()
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-7)
## Energy Tells the Story


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-8
:view: output
:alt: Executed output for Energy Tells the Story.
```


::::::::::::::::::::::::{speaker-note}
Time: 24-26 min. "The displayed formula establishes energy growth for forward Euler on this harmonic oscillator. Do not generalize it to every Hamiltonian system."
::::::::::::::::::::::::


## Energy Tells the Story — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-8
:start: 1
# Total energy: E = (1/2)(v^2 + omega^2 * x^2). For omega=1: E = (x^2 + v^2)/2
E_euler = 0.5 * (y_euler[:, 0]**2 + y_euler[:, 1]**2)

fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(t_euler, E_euler, 'r-', lw=2, label='Euler')
ax.axhline(0.5, color='k', ls='--', lw=1.5, label='Exact ($E = 0.5$)')
ax.set(xlabel='Time', ylabel='Total Energy $E$',
       title='Energy Conservation: Euler FAILS')
ax.legend()
ax.set_ylim(0, min(E_euler[-1] * 1.1, E_euler[-1] + 50))
plt.tight_layout()
plt.show()

print(f"Energy at start: {E_euler[0]:.4f}")
print(f"Energy at end:   {E_euler[-1]:.1f}")
print(f"Energy grew by:  {(E_euler[-1] / E_euler[0] - 1) * 100:.0f}%")
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-8)
## Why Euler Fails

Euler follows the **tangent line** at each point. For the oscillator, the true orbit curves inward (it's a circle). The tangent is always *outside* the circle.

::::::::::::::::::::::::{slide-incremental}
- Each step **overshoots** slightly
- The overshoot **compounds** — positive feedback
- Energy grows as $E_n = E_0(1 + \omega^2 h^2)^n$
- This is **exponential growth** in the step count $n$
::::::::::::::::::::::::


## Euler: refinement and long-time structure

```{slide-options}
{"vertical":true}
```

::::::::::::::::::::::::{note}
For this harmonic oscillator, every positive fixed step increases energy. Reducing $h$ reduces the error over a fixed time interval, but does not make forward Euler symplectic. Test convergence and long-time conservation separately.
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
*(Forward Euler remains useful for learning and for suitable problems within its stability limits. The oscillator illustrates a specific long-time failure; this is not a verdict on every conservative system.)*
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 26-27 min. "This numerical error reflects the method’s structure. Refinement improves finite-time accuracy, while a different integrator may better preserve long-time geometry."
::::::::::::::::::::::::

## From Equations to Code: RK2

*The real skill: translating math into programs.*

::::::::::::::::::::::::{speaker-note}
Time: 27-42 min. Core pedagogical section — equation-to-code translation.
::::::::::::::::::::::::

## Euler's Problem, Visually

Euler uses the slope at the **start** of the interval and assumes it's constant:

$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

::::::::::::::::::::::::{fragment}
But the slope **changes** across the interval!

What if we could **peek ahead** to the middle and use a better slope estimate?
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 27-29 min. "Imagine walking through fog. Euler takes one look, walks straight for h steps. What if you could check your bearing at the midpoint?"
::::::::::::::::::::::::

## The Midpoint Method (RK2)

**Step 1:** Use Euler to estimate the state at the midpoint:

$$k_1 = f(t_n, y_n)$$

::::::::::::::::::::::::{fragment}
**Step 2:** Evaluate the slope **at the midpoint**:

$$k_2 = f\!\left(t_n + \frac{h}{2},\; y_n + \frac{h}{2}\,k_1\right)$$
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
**Step 3:** Use the midpoint slope for the full step:

$$\boxed{y_{n+1} = y_n + h \cdot k_2}$$
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
Local error: $O(h^3)$. Global error: $O(h^2)$. **Second-order method.** Cost: 2 evaluations per step.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 29-32 min. "Three formulas. Each one becomes one line of code. Let's do it."
::::::::::::::::::::::::

## Equation to Code: Step by Step

The equations:

| Math | Code |
|------|------|
| $k_1 = f(t_n, y_n)$ | `k1 = f(t, y)` |
| $k_2 = f(t_n + h/2,\; y_n + (h/2)\,k_1)$ | `k2 = f(t + h/2, y + h/2 * k1)` |
| $y_{n+1} = y_n + h\,k_2$ | `return y + h * k2` |

::::::::::::::::::::::::{fragment}


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-9
:view: code
:alt: Executed output for Equation to Code: Step by Step.
```


::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
Every symbol in the math has a **one-to-one** correspondence in the code.

**This is the skill.** RK4 and Leapfrog follow the exact same translation process.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 32-35 min. "Walk through each line. Math left, code right. This is the core skill for COMP 536 Project 2."
::::::::::::::::::::::::

## Full RK2 Integrator


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-10
:view: code
:alt: Executed output for Full RK2 Integrator.
```


::::::::::::::::::::::::{fragment}
Compare with `euler_integrate` — the **only difference** is calling `rk2_step` instead of computing `y + h * f(t, y)` directly.

The integration loop is **method-agnostic.** Swap the step function, get a different method.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 35-36 min. "This design pattern is powerful. You'll use the same loop structure for RK4 and Leapfrog."
::::::::::::::::::::::::

## Why Should RK2 Be Better?

Recall the Taylor series: $\;y(t+h) = y + hy' + \frac{h^2}{2}y'' + \frac{h^3}{6}y''' + \cdots$

::::::::::::::::::::::::{slide-incremental}
- **Euler** matches the first **1 term** ($h$). Everything from $h^2$ onward is error.
- **RK2** matches the first **2 terms** ($h$ and $h^2$). Error starts at $h^3$.
- Each additional matched term pushes the leading error to a **higher power of $h$**.
- Since $h < 1$ (typically $h \approx 0.01$), higher powers shrink *fast*: $0.01^2 = 10^{-4}$, $0.01^4 = 10^{-8}$.
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{note}
**The recipe for accuracy:** Sample the slope at more points → match more Taylor terms → push the error to a higher power of $h$. That's the entire Runge-Kutta idea.
:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
Let's verify this prediction...
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 36-37 min. "This is the deep reason. Now let's see if the prediction holds."
::::::::::::::::::::::::

## RK2 vs Euler: Trajectory


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-11
:view: output
:alt: Executed output for RK2 vs Euler: Trajectory.
```


::::::::::::::::::::::::{speaker-note}
Time: 36-38 min. "RK2 tracks the solution far better. Two evaluations per step instead of one — and we go from first-order to second-order."
::::::::::::::::::::::::


## RK2 vs Euler: Trajectory — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-11
:start: 1
t_rk2, y_rk2 = rk2_integrate(f_sho, y0_sho, [0, t_end], h)

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t_exact, np.cos(t_exact), 'k-', alpha=0.4, lw=1.5, label='Exact')
ax.plot(t_euler, y_euler[:, 0], 'r-', lw=0.8, alpha=0.5, label='Euler')
ax.plot(t_rk2, y_rk2[:, 0], 'b-', lw=1.5, label='RK2')
ax.set(xlabel='Time', ylabel='$x(t)$',
       title='RK2 vs Euler: Night and Day')
ax.legend()
plt.tight_layout()
plt.show()
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-11)
## RK2 vs Euler: Phase Space


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-12
:view: output
:alt: Executed output for RK2 vs Euler: Phase Space.
```


::::::::::::::::::::::::{speaker-note}
Time: 38-39 min. "RK2's orbit stays much closer to the circle. But zoom in — it still drifts. Can we do even better?"
::::::::::::::::::::::::


## RK2 vs Euler: Phase Space — code

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-12
:start: 1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.5))
theta = np.linspace(0, 2 * np.pi, 200)

ax1.plot(np.cos(theta), -np.sin(theta), 'k--', lw=2)
ax1.plot(y_euler[:, 0], y_euler[:, 1], 'r-', lw=0.3, alpha=0.6)
ax1.set(title='Euler: Spiral Out', xlabel='$x$', ylabel='$v$')
ax1.set_aspect('equal')

ax2.plot(np.cos(theta), -np.sin(theta), 'k--', lw=2)
ax2.plot(y_rk2[:, 0], y_rk2[:, 1], 'b-', lw=0.5, alpha=0.7)
ax2.set(title='RK2: Much Tighter', xlabel='$x$', ylabel='$v$')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-12)
## RK2 vs Euler: Energy


```{slide-code-example} ode-methods-computations.ipynb#ode-methods-cell-13
:view: output
:alt: Executed output for RK2 vs Euler: Energy.
```


::::::::::::::::::::::::{fragment}
RK2 is **vastly** better. But it still drifts. Over millions of timesteps — the kind you'll run for COMP 536 Project 2 — that drift adds up. Is there something better?
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 39-42 min. "RK2 reduced the error by orders of magnitude. But zoom in — it still drifts monotonically. For a million-step simulation, we need to compare long-time structure and physical-energy error."
::::::::::::::::::::::::


## RK2 vs Euler: Energy — code 1/2

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-13
:start: 1
E_rk2 = 0.5 * (y_rk2[:, 0]**2 + y_rk2[:, 1]**2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3))

# Left: both on same scale
ax1.plot(t_euler, E_euler, 'r-', lw=1.5, label='Euler')
ax1.plot(t_rk2, E_rk2, 'b-', lw=1.5, label='RK2')
ax1.axhline(0.5, color='k', ls='--', lw=1)
ax1.set(xlabel='Time', ylabel='Energy $E$', title='Full Scale')
ax1.legend()

# Right: zoom on RK2
ax2.plot(t_rk2, E_rk2 - 0.5, 'b-', lw=1.5)
ax2.axhline(0, color='k', ls='--', lw=1)
ax2.set(xlabel='Time', ylabel='$E - E_0$', title='RK2 Energy Error (Zoomed)')

```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-13)


## RK2 vs Euler: Energy — code 2/2

```{slide-options}
{"vertical":true}
```

```{slide-code} python
:title: ode-methods-cell-13
:start: 17
plt.tight_layout()
plt.show()

print(f"Euler final energy error: {abs(E_euler[-1] - 0.5):.1f}")
print(f"RK2 final energy error:   {abs(E_rk2[-1] - 0.5):.2e}")
print(f"RK2 is {abs(E_euler[-1] - 0.5) / abs(E_rk2[-1] - 0.5):.0f}x better")
```

[Complete executed source](ode-methods-computations.ipynb#ode-methods-cell-13)
## Higher-Order Methods: Your Turn

*Now you have the skill. Apply it.*

::::::::::::::::::::::::{speaker-note}
Time: 42-52 min. Show formulas, don't code — students implement for COMP 536 Project 2.
::::::::::::::::::::::::

## RK4: Four Slopes, Fourth-Order


$$k_1 = f(t_n,\, y_n)$$
$$k_2 = f\!\left(t_n + \tfrac{h}{2},\; y_n + \tfrac{h}{2}\,k_1\right)$$
$$k_3 = f\!\left(t_n + \tfrac{h}{2},\; y_n + \tfrac{h}{2}\,k_2\right)$$
$$k_4 = f(t_n + h,\; y_n + h\,k_3)$$

$$\boxed{y_{n+1} = y_n + \frac{h}{6}\left(k_1 + 2k_2 + 2k_3 + k_4\right)}$$


## RK4: order and quadrature weights

```{slide-options}
{"vertical":true}
```


::::::::::::::::::::::{fragment}
Matches Taylor series through **$h^4$** — error starts at $h^5$.

| Halve $h$ | Error drops by |
|-----------|----------------|
| Euler ($p=1$) | $2\times$ |
| RK2 ($p=2$) | $4\times$ |
| **RK4** ($p=4$) | $16\times$ |

Same pattern as RK2 — each $k$ formula becomes one line of code.

The weights $\frac{1}{6}, \frac{2}{6}, \frac{2}{6}, \frac{1}{6}$ resemble Simpson quadrature when midpoint contributions are combined. The stages use **different estimated states**; RK4 is not simply Simpson integration of a known integrand.
::::::::::::::::::::::


::::::::::::::::::::::::{speaker-note}
Time: 44-46 min. "4 evaluations per step, but each halving of h gives 16x improvement. The weights resemble Simpson quadrature, but the two midpoint stages use different estimated states."
::::::::::::::::::::::::

## Accuracy and structure are different questions

The explicit midpoint RK2 and classical RK4 methods shown here are not symplectic.

:::{slide-incremental}
- Local accuracy and long-time geometric behavior are different properties.
- For Hamiltonian dynamics, the exact flow preserves symplectic structure and phase-space volume.
- Numerical behavior depends on the problem, timestep and integration duration.
- Some **implicit Runge–Kutta methods are symplectic**; the statement is not about every RK method.
:::

Compare **trajectory error, phase error and energy error** separately for the oscillator.

:::{speaker-note}
Original teaching slot: 46–48 min. Keep the distinction between accuracy and structure. Do not claim that drift always has one sign or that a simultaneous state update itself explains the defect.
:::


## Leapfrog: Structure Over Accuracy

A fundamentally different idea: update position and velocity **alternately**, not simultaneously.

**Kick-Drift-Kick:**

$$\vec{v}_{n+1/2} = \vec{v}_n + \frac{h}{2}\,\vec{a}(\vec{r}_n) $$

$$\vec{r}_{n+1} = \vec{r}_n + h\,\vec{v}_{n+1/2} $$

$$\vec{v}_{n+1} = \vec{v}_{n+1/2} + \frac{h}{2}\,\vec{a}(\vec{r}_{n+1}) $$

::::::::::::::::::::::::{speaker-note}
Time: 48-49 min.
::::::::::::::::::::::::

## What leapfrog preserves

For a separable Hamiltonian and a fixed timestep, kick-drift-kick leapfrog is symplectic and time reversible.

:::{slide-incremental}
- **Kick:** changes velocity while position stays fixed, a shear in velocity.
- **Drift:** changes position while velocity stays fixed, a shear in position.
- In the one-dimensional phase plane, these shears preserve area.
- Their composition retains the symplectic structure of the substeps.
:::

This does **not** imply exact conservation of the physical energy.

:::{speaker-note}
Keep the deck-of-cards analogy for area preservation. Area preservation alone is not a general proof of bounded physical-energy error.
:::

## Leapfrog: energy error and its limits

```{slide-options}
{"vertical":true}
```

For the harmonic oscillator in the stable regime $h\omega<2$, physical-energy error oscillates rather than showing forward Euler’s secular growth.

- The energy error is typically $O(h^2)$ in this setting.
- Modified-Hamiltonian analysis explains long-time behavior under additional assumptions.
- It is not a universal statement of exact modified-energy conservation for arbitrary systems.
- Instability, changing timesteps and finite precision require separate analysis.

| Question | Classical RK4 | Fixed-step leapfrog |
|---|---|---|
| Formal order | Fourth | Second |
| Symplectic for this separable problem? | No | Yes |
| Diagnostic to inspect | Phase and energy error | Phase and energy error |

:::{speaker-note}
This replaces unsupported percentage claims at a million or billion steps. No numerical drift percentage is asserted without a specified experiment. A second-order method is not automatically preferable: match method, problem, duration and accuracy needs.
:::


## Your Turn: RK4

### Formulas

$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2}k_1)$$
$$k_3 = f(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2}k_2)$$
$$k_4 = f(t_n + h, y_n + hk_3)$$
$$y_{n+1} = y_n + \tfrac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

## Your turn: implement the RK4 stages

```{slide-options}
{"vertical":true}
```

### Your Code

```python
def rk4_step(f, t, y, h):
    k1 = ???
    k2 = ???
    k3 = ???
    k4 = ???
    return ???
```


::::::::::::::::::::::{fragment}
Same pattern as RK2 — each $k$ formula becomes one line.
::::::::::::::::::::::


::::::::::::::::::::::::{speaker-note}
Time: 52-53 min. "You practiced this with RK2. Each formula maps to one line of code."
::::::::::::::::::::::::

## Your Turn: Leapfrog

::::::::::::::::::::::::{slide-columns}
:::::::::::::::::::::::{slide-column}
### Formulas (Kick-Drift-Kick)

$$v_{n+1/2} = v_n + \tfrac{h}{2}\,a(x_n)$$
$$x_{n+1} = x_n + h\,v_{n+1/2}$$
$$v_{n+1} = v_{n+1/2} + \tfrac{h}{2}\,a(x_{n+1})$$

where $a(x) = -\omega^2 x$ (or $= F/m$ for gravity)
:::::::::::::::::::::::

:::::::::::::::::::::::{slide-column}
### Your Code

```python
def leapfrog_step(x, v, a_func, h):
    v_half = ???      # half kick
    x_new  = ???      # full drift
    a_new  = ???      # force at new position
    v_new  = ???      # half kick
    return x_new, v_new
```


::::::::::::::::::::::{fragment}
Notice: Leapfrog takes $(x, v)$ **separately** — not a single state vector.

The alternating kick/drift composition is symplectic for a separable Hamiltonian at fixed step. It does not conserve physical energy exactly.
::::::::::::::::::::::

:::::::::::::::::::::::
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 53-54 min. "Leapfrog has a different API. It updates x and v separately, not as one vector. The alternating kick/drift composition, rather than the API alone, makes it symplectic under the stated assumptions."
::::::::::::::::::::::::

## Method Comparison

::::::::::::::::::::::::{div}
| Method | Order | Energy Behavior | Symplectic? | Evals/Step | Best For |
|--------|-------|----------------|-------------|------------|----------|
| **Euler** | 1st | Growth for this oscillator | No | 1 | Learning |
| **RK2** | 2nd | Moderate drift | No | 2 | Quick tests |
| **RK4** | 4th | Slow drift | No | 4 | Short-time accuracy |
| **Leapfrog** | 2nd | Oscillation in the stable fixed-step regime | **Yes** | 1* | **Long-time dynamics** |
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
\* Leapfrog reuses the last acceleration, so effectively 1 new evaluation per step.

In the original COMP 536 Project 2, students implemented **three** of these (Euler, RK4, Leapfrog). Keep that comparison as context; follow the COMP 521 Project 4 specification for required methods.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 50-52 min. "This table summarizes the whole lecture. You should be able to explain every entry by the time you finish COMP 536 Project 2."
::::::::::::::::::::::::

## COMP 536 case study: N-body Dynamics

> **Case-study context:** the following N-body tasks and timeline are retained from COMP 536. They are not new COMP 521 assignments or deadlines.

::::::::::::::::::::::::{speaker-note}
Time: 52-60 min. Project launch.
::::::::::::::::::::::::

## The Challenge

Build a **gravitational N-body simulator** from scratch.

::::::::::::::::::::::::{slide-incremental}
- Build the **complete pipeline** with Euler first (force calc → integration → diagnostics → plots)
- Add **RK4 and Leapfrog** as drop-in replacements — compare energy behavior
- Generate **Plummer sphere** initial conditions for realistic star clusters
- Compare **loops vs. vectorized NumPy** ($10$–$100\times$ speedup)
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 52-54 min. "The key idea: build one working pipeline first, then upgrade pieces. Phase 1 is all about getting Euler working end-to-end."
::::::::::::::::::::::::

## COMP 536 case study: the pipeline-first approach

| Phase | What You Build | What You Validate |
|-------|---------------|-------------------|
| **1** | Euler pipeline ($N=2$, $N=3$) | Force calc, energy diagnostics, plotting |
| **2** | Add RK4 + Leapfrog | Integrator comparison on same $N=2$ problem |
| **3** | Plummer sphere ICs ($N=10$–$100$) | Virial equilibrium, cluster dynamics |
| **4** | Vectorized forces ($N=1000+$) | Performance scaling, loop vs. NumPy |

::::::::::::::::::::::::{note}
Each phase adds **one new idea** on top of a validated foundation. Phase 1 is the hardest — once your pipeline works end-to-end, everything else is incremental.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Original COMP 536 delivery note (not a COMP 521 deadline). Time: 54-56 min. "Phase 1 is your priority this week. Get Euler working end-to-end on a Sun-Earth orbit. The rest builds on that foundation."
::::::::::::::::::::::::

## What You Should Observe

Use the harmonic oscillator to motivate diagnostics for the gravitational case study:

::::::::::::::::::::::::{slide-incremental}
- **Euler:** our oscillator gains energy every step. Measure energy and orbital error separately in the gravitational problem.
- **RK4:** test finite-time convergence; the drift depends on step size, trajectory and duration.
- **Leapfrog:** stable fixed-step integrations can have bounded oscillatory energy error. Phase error remains; closed orbits are not guaranteed.
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}
The physics is different (gravity vs. spring). Transfer the **diagnostics**, and test the numerical behavior for each problem.

"Today's spring = tomorrow's gravity."
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 56-57 min. "This connection is the whole point. The same methods and diagnostics apply, but the stability and error behavior must be tested for the new problem."
::::::::::::::::::::::::

## Original COMP 536 timeline and milestones

::::::::::::::::::::::::{slide-incremental}
- **Check-in 1 (Wed Feb 18):** Phase 1 complete — Euler pipeline working end-to-end, $N=2$ orbit plot, energy diagnostics. *At least 3 meaningful commits.*
- **Check-in 2 (Wed Feb 25):** Phase 2 complete — all three integrators compared on $N=2$, energy error plot. Phase 3 started (Plummer ICs).
- **Due: Tue Mar 3, 11:59 PM.** Phases 3–4 complete — cluster simulations, vectorization, all plots, both memos.
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Original COMP 536 delivery note (not a COMP 521 deadline). Time: 57-58 min. "Check-in 1 is the critical one. If you can't get Euler working on a Kepler orbit by next Wednesday, come to office hours immediately."
::::::::::::::::::::::::

## Background reading from COMP 536

These original readings support the retained examples; they are not new COMP 521 assignments:

::::::::::::::::::::::::{slide-incremental}
- **Module 3, Part 1:** [Failure of Naive Integration](https://astrobytes-edu.github.io/comp536-sp26/07-numerical-methods/module-3-ODE-methods-and-conservation/01-module3-part1-euler.html) — full Euler derivation, error analysis
- **Module 3, Part 2:** [Runge-Kutta Methods](https://astrobytes-edu.github.io/comp536-sp26/07-numerical-methods/module-3-ODE-methods-and-conservation/02-module3-part2-runge-kutta.html) — complete RK4 derivation, adaptive stepping
- **Module 3, Part 3:** [Symplectic Integration](https://astrobytes-edu.github.io/comp536-sp26/07-numerical-methods/module-3-ODE-methods-and-conservation/03-module3-part3-symplectic.html) — Hamiltonian mechanics, Leapfrog, phase space
::::::::::::::::::::::::

::::::::::::::::::::::::{fragment}

### The Takeaway

:::::::::::::::::::::::{div}
**Structure > Accuracy**
:::::::::::::::::::::::

::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Time: 58-60 min. "Today you saw the failure. The readings explain WHY it fails mathematically. By next class, you should be coding Phase 1 — get Euler running on a Sun-Earth orbit."
::::::::::::::::::::::::


## COMP 521: ODEs for planetary interiors

Project 4 uses the same computational pattern: choose a state, define its derivatives, supply initial or boundary information, and measure error.

- Main method sequence: Euler, midpoint RK2 and RK4.
- Verify observed order with controlled step refinement.
- Continue to hydrostatic equilibrium, an equation of state, surface finding and shooting.
- Diagnose order loss when locating a moving surface.

The N-body material remains an optional comparison of long-time dynamics. It is not the planetary-interior model.

## COMP 521: two teaching sessions

**Session 1:** initial-value problems, state vectors, Euler/RK2/RK4 and independent error checks.

**Session 2:** stability and conservation diagnostics, then the planetary-interior boundary-value problem and surface location.

Use the current COMP 521 Project 4 specification for deliverables and dates. Original COMP 536 milestones remain labelled case-study material.
