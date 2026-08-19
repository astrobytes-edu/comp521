---
title: "Model Fitting and Uncertainty"
subtitle: "Data, Inference, and Scientific ML | COMP 521"
---

:::{warning} Module in preparation
This module will be finalized before Project 5 begins. The page establishes the
course route; worked examples and project-specific guidance are still being
developed.
:::

## Purpose

Model fitting turns a scientific question into a comparison between data and a
forward model. In COMP 521, that comparison must include diagnostics and an
uncertainty statement, not only a best-fit line or parameter value.

## Planned sequence

1. build and inspect a design matrix;
2. fit a model while checking conditioning and residuals;
3. quantify uncertainty with resampling and model diagnostics;
4. state what the data support, and what they do not.

The foundations are [linear algebra](../00-linear-algebra/00a-linear-algebra-core-module.md),
[probability](../01-probability/01-mod1-part1-foundations.md), and
[statistical tools](../01-probability/02-mod1-part2-statistical-tools.md).
