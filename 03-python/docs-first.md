---
title: "Docs First: Use Scientific Python Documentation Efficiently"
subtitle: "Python reference | A course rule for reliable code"
kernelspec:
  name: python3
  display_name: Python 3
---

## The hard rule

**Docs First is a hard rule in COMP 521.** Before copying code from a search
result, asking an AI assistant, or guessing how an unfamiliar function behaves,
check the primary documentation for the exact tool you are using.

Documentation is the closest authority on an API’s inputs, defaults, returned
object, exceptions, and version-specific behavior. It does not prove that your
model is scientifically adequate. It tells you what the software promises, so
you can test whether that behavior serves the scientific question.

## Official documentation routes

### Python

- [Python documentation home](https://docs.python.org/3/) — version choices,
  search, glossary, and table of contents.
- [Python tutorial](https://docs.python.org/3/tutorial/) — a guided language
  introduction when you need a concept, not merely a method name.
- [Python language reference](https://docs.python.org/3/reference/) — precise
  syntax and language semantics.
- [Python standard library](https://docs.python.org/3/library/) — built-ins and
  modules distributed with Python.
- [Built-in types](https://docs.python.org/3/library/stdtypes.html) — lists,
  dictionaries, strings, `range`, truth values, and methods.
- [`math`](https://docs.python.org/3/library/math.html) — mathematical
  functions and numerical comparison helpers such as `math.isclose`.
- [Built-in exceptions](https://docs.python.org/3/library/exceptions.html) —
  what a traceback is reporting and what failures a function may raise.

### NumPy

- [NumPy documentation home](https://numpy.org/doc/stable/) — beginner guide,
  user guide, and API reference.
- [Absolute beginner’s guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
  — fast orientation to arrays.
- [NumPy user guide](https://numpy.org/doc/stable/user/) — shape, axes,
  indexing, broadcasting, dtypes, and copies/views.
- [NumPy API reference](https://numpy.org/doc/stable/reference/) — exact
  signatures, parameters, return values, and examples.
- [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html),
  [indexing](https://numpy.org/doc/stable/user/basics.indexing.html), and
  [copies/views](https://numpy.org/doc/stable/user/basics.copies.html) — core
  concepts for this course.

### Matplotlib

- [Matplotlib documentation home](https://matplotlib.org/stable/) — quick
  start, tutorials, gallery, API reference, and release notes.
- [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html)
  — the `Figure`/`Axes` model used in this course.
- [Tutorials](https://matplotlib.org/stable/tutorials/index.html) — guided
  visual patterns.
- [API reference](https://matplotlib.org/stable/api/index.html) — exact plot
  object and method behavior.
- [`pyplot.subplots`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
  — the standard course entry point for a figure and axes.

## A fast documentation workflow

When you encounter `np.mean(flux, axis=0)` or `ax.set_xlim(0, 10)`, do this
before changing code.

1. **Name the exact question.** Example: “What does `axis=0` mean for an array
   with shape `(stars, times)`?”
2. **Check your environment and version.** Record `sys.version` and, where
   relevant, `np.__version__` or `matplotlib.__version__`. Online docs may be
   newer than your installed release.
3. **Read signature, parameters, returns, and exceptions.** Do not stop at the
   first example that appears to work.
4. **Read one conceptual guide** when an option changes meaning: `axis`, shape,
   broadcasting, copying, normalization, and scale are not parameters to guess.
5. **Run a smallest possible experiment.** Use a tiny array or toy figure whose
   answer you can predict, then compare the behavior with the documentation.
6. **Ask a precise follow-up.** Say what you read, expected, observed, and show
   the smallest code and full traceback or output.

## What to read on a reference page

| Read this | Why it matters |
|---|---|
| Signature | What inputs are permitted and their order |
| Parameters and defaults | Which choices occur if you omit an argument |
| Return value and shape | What object comes back, including dimensions/dtype when relevant |
| Exceptions and warnings | How invalid inputs or questionable behavior are reported |
| Examples | A pattern to adapt, never a substitute for understanding |
| Version notes | Whether the behavior changed between releases |

## Docs before AI or search results

AI assistants, Q&A sites, tutorials, and code snippets can help generate
questions and alternatives. They are not the authority for API behavior: they
can omit version context, use deprecated behavior, invent parameters, or solve a
different problem.

1. Read the official docs first.
2. Use outside help to clarify or compare approaches.
3. Verify every suggested function, parameter, and claimed behavior against the
   docs and a small runnable check.
4. Keep a documentation link or a short note in your notebook when library
   behavior is consequential to an analysis.

:::{important} Documentation answers a software question, not a science question

NumPy documentation can establish how a Boolean mask selects entries. It cannot
establish that your threshold finds planets. You still need a stated model, data
provenance, validation evidence, and an honest limitation.
:::

## A small documentation check

Look up [`math.isclose`](https://docs.python.org/3/library/math.html#math.isclose),
identify its tolerance parameters, then run this predictable example:

```{code-cell} python
import math

print(math.isclose(0.1 + 0.2, 0.3, rel_tol=0.0, abs_tol=1e-12))
print(math.isclose(0.1 + 0.2, 0.3, rel_tol=0.0, abs_tol=0.0))
```

The first call states an allowed absolute difference; the second demands exact
floating-point equality. A valid tolerance depends on quantity, units, and
claim—not a magic constant.
