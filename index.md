---
title: "COMP 521: Introduction to Scientific Computing and Data Science"
subtitle: "San Diego State University | Fall 2026"
---

# Welcome to COMP 521

> **Build algorithms from scratch, then leverage libraries for real data.**

This course provides balanced foundations in both numerical methods and
practical data science. You will implement the core algorithms that
computational tools are built from — integrators, root-finders, ODE solvers,
samplers, classifiers — and then apply them to real astronomical datasets from
Gaia and Kepler.

By the end, you will not just *use* `scipy.integrate`; you will know what it is
doing, when it will fail you, and how to tell the difference.

:::{note} Course at a glance
**Units:** 3
**Prerequisites:** MATH 252; MATH 254 or 342A; or equivalent with instructor
permission, or graduate standing.
**Instructor:** Anna Rosen · alrosen@sdsu.edu
:::

## How this course is structured

The semester runs 15 weeks: six two-week projects followed by a three-week
final project.

| Weeks | Project | Focus |
|:--|:--|:--|
| 1–2 | Project 1 | Scientific programming & exploratory data analysis |
| 3–4 | Project 2 | Numerical integration |
| 5–6 | Project 3 | Root finding & data acquisition |
| 7–8 | Project 4 | Linear algebra & statistical methods |
| 9–10 | Project 5 | ODEs & time series analysis |
| 11–12 | Project 6 | Machine learning foundations |
| 13–15 | Final | Complete data science pipeline |

A **Project 0 bootcamp** (environment setup, Git, NumPy, Matplotlib) is due at
the end of Week 1.

## The thread running through everything

Rather than six disconnected assignments, the projects build one continuous
scientific investigation — detecting and characterizing exoplanets in real
Kepler data:

1. **Project 2** — build the transit model equations
2. **Project 3** — download and clean real Kepler light curves
3. **Project 4** — fit the transit model to real data
4. **Project 5** — recover orbital periods from time series
5. **Project 6** — classify planet candidates
6. **Final** — assemble the complete discovery pipeline

You finish the semester having done a genuine piece of observational science
with tools you wrote yourself.

## Where to start

:::{tip} New here? Read in this order
1. [Syllabus](01-course-info/syllabus.md) — policies, grading, expectations
2. [Schedule](01-course-info/schedule.md) — week-by-week plan and due dates
3. [AI Policy](01-course-info/ai-policy.md) — read this one carefully
4. [Getting Started](02-getting-started/index.md) — set up your machine
:::
