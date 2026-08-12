---
title: "COMP 521: Introduction to Scientific Computing and Data Science"
subtitle: "San Diego State University | Fall 2026"
---

<!-- prep-banner:start -->
:::{warning} This page is still being prepared
COMP 521 begins **Tuesday, August 25**. This page is being written and revised
until then — dates, policies, and details may still change. It is published
early so you can see the shape of the course, not because it is finished.

Anything still under discussion is settled by **Monday, August 24**. After that,
what is written here is what the course does.
:::
<!-- prep-banner:end -->

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

The semester runs 16 weeks: six two-week projects followed by a four-week final
project. Class meets **Tue/Thu 5:30–6:45 pm in LSN 134**, and every session
mixes instruction with hands-on work — bring your laptop.

| Weeks | Project | Focus | Due |
|:--|:--|:--|:--|
| 1–2 | Project 1 | Scientific programming & exploratory data analysis | Tue Sep 8 |
| 3–4 | Project 2 | Numerical integration | Mon Sep 21 |
| 5–6 | Project 3 | Root finding & data acquisition | Mon Oct 5 |
| 7–8 | Project 4 | Linear algebra & statistical methods | Mon Oct 19 |
| 9–10 | Project 5 | ODEs & time series analysis | Mon Nov 2 |
| 11–12 | Project 6 | Machine learning foundations | Mon Nov 16 |
| 13–16 | Final | Complete data science pipeline | Thu Dec 17 |

A **Project 0 setup bootcamp** (Python environment, command line, Git and
GitHub, Classroom50) is due **Thu Aug 27**, our second class meeting — you need
a working machine before we start writing code. Everything after that is due
**Mondays at 11:59 pm PT**.

Projects are done in **rotating pairs** — you will work with everyone in the
class over the semester — but each of you writes, submits, and must be able to
explain your own code.

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
