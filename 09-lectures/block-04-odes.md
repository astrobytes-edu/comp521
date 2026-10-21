---
title: "Block 4 · ODE Methods & Exoplanet Interiors"
subtitle: "COMP 521 · Time stepping, stability, and conservation"
---

How do we solve equations for change, whether the independent variable is time,
depth, or radius? What evidence supports the computed solution?

**Project connection:** the ODE library and exoplanet-interior notebook in
[Block 4 of the course schedule](../01-course-info/schedule.md).

## Lecture 11 · October 8

[Open the ODE slides](/reveal/lecture-11-odes.html) ·
[Read the worked handout](/reveal/lecture-11-odes.handout.html).

The 40 main slides introduce ODEs, state variables, and physical modeling;
derive exact growth and decay solutions; connect finite differences and Taylor
expansions to Euler, midpoint RK2, and RK4; and compare accuracy, stability,
energy, and phase. Richardson extrapolation and symplectic leapfrog complete
the method comparison. A radial pressure-balance example connects the methods
to planetary interiors. Four optional references follow the exit questions.

Start with Euler and Runge–Kutta below. Use the later readings for extensions.
Assignment briefs set deliverables and dates.

## Lecture 12 · Pandas and exploratory data analysis

[Open the Pandas slides](/reveal/lecture-12-pandas.html) ·
[Read the worked handout](/reveal/lecture-12-pandas.handout.html) ·
[Open the lecture page and notebook downloads](lecture-12-pandas.md).

The 30-minute introduction covers labelled tables, missing values, row
selection, summaries, and plots using the saved NASA exoplanet dataset.
Five runnable notebook tasks provide hands-on exploration after the lecture.

## Readings

| Reading | Topic |
|---|---|
| [Overview: Making Time Flow](../05-numerical-methods/03-odes/00-mod3-overview.md) | ODE methods and conservation |
| [Euler methods](../05-numerical-methods/03-odes/01-module3-part1-euler.md) | First time-stepping methods |
| [Runge–Kutta methods](../05-numerical-methods/03-odes/02-module3-part2-runge-kutta.md) | Building higher-order updates |
| [Symplectic methods](../05-numerical-methods/03-odes/03-module3-part3-symplectic.md) | Integrator geometry and conservation |
| [Stability analysis](../05-numerical-methods/03-odes/04-module3-part4-stability.md) | Step size and numerical stability |
| [Summary and synthesis](../05-numerical-methods/03-odes/05-mod3-synthesis.md) | Comparing methods and interpreting checks |

[Return to the Lecture Library](index.md).
