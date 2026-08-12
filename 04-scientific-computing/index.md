---
title: "Part 2: Scientific Computing Core"
subtitle: "Scientific Computing with Python | COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is being revised for COMP 521
This chapter was adapted from COMP 536 and is still under review. You may find
references to the wrong course number, setup instructions that do not match
ours, or examples that assume material we have not covered yet.

The Python and the science are sound — it is the packaging that is catching up.
Where this page disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
:::
<!-- prep-banner:end -->

## Deepening Your Computational Toolkit

This module builds on the `Python Fundamentals` material and teaches the high-performance numerical tools and workflows used in real research: array programming with NumPy, visualization with Matplotlib, robust numerical computing practices, and performance-aware algorithms.

:::{tip} 📚 How to Use This Module

Treat these chapters as practical, reusable resources: read the concept sections, run the code examples in IPython, complete the exercises to solidify performance and numerical best practices, and refer back to these pages often as your go-to references during assignments and projects.
:::

## Module Overview

### [🧮 Chapter 7: NumPy - The Foundation of Scientific Computing in Python](./07-numpy-fundamentals.qmd)

NumPy arrays, vectorization, broadcasting, indexing, and memory/layout considerations — the foundation for efficient astronomical computation.

### [🖼️ Chapter 8: Matplotlib - Visualizing Your Universe](./08-matplotlib-fundamentals.qmd)

Create publication-quality figures from NumPy arrays: line plots, images, colormaps, multi-panel layouts, and WCS-aware displays for astronomical data.

### [🔧 Chapter 9: Robust Numerical Computing & Best Practices](./09-robust-computing.qmd)

Numerical stability, defensive algorithms, error propagation, and techniques for writing reliable scientific code that produces trustworthy results.

### [🚀 Chapter 10: Advanced Patterns & Performance](./10-advanced-oop.qmd)

Advanced object-oriented patterns, performance profiling, C/Fortran integration paths, and packaging/testing strategies for production-grade scientific software.

### [📊 Chapter 11: Pandas Fundamentals](./11-pandas-fundamentals.qmd)

Data manipulation and analysis with Pandas: DataFrames, series operations, grouping, merging, and time series analysis for scientific datasets.

## Learning Strategy

1. **Run examples interactively** to observe performance differences between naive and vectorized implementations.
2. **Profile before optimizing** — use small benchmarks to find hotspots.
3. **Prefer NumPy idioms** (vectorize, mask, broadcast) over Python loops for data-heavy tasks.
4. **Write tests** for numerical code to guard against subtle regressions.

## Quick Navigation Guide

- Fix performance bottlenecks $\to$ [Ch 7: NumPy](./07-numpy-fundamentals.qmd)
- Improve plots and figures $\to$ [Ch 8: Matplotlib](./08-matplotlib-fundamentals.qmd)
- Ensure numerical stability $\to$ [Ch 9: Robust Computing](./09-robust-computing.qmd)
- Productionize code $\to$ [Ch 10: Advanced Patterns](./10-advanced-oop.qmd)
- Data analysis workflows $\to$ [Ch 11: Pandas](./11-pandas-fundamentals.qmd)

## Core Competencies

- Efficient array programming with NumPy
- Vectorized algorithms and broadcasting
- Memory-aware data handling (views vs copies)
- Numerical stability and defensive programming
- Creating publication-quality visualizations with Matplotlib
- Profiling and optimizing performance-critical code
- Packaging and testing scientific libraries
- Data manipulation with Pandas

---

**Next:** Start with [Chapter 7: NumPy](./07-numpy-fundamentals.qmd)
