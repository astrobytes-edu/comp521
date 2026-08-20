# COMP 521: Introduction to Scientific Computing and Data Science

Course site for COMP 521 at San Diego State University, Fall 2026.
Built with [MyST](https://mystmd.org).

## Local development

```bash
uv sync
npm install -g mystmd
source .venv/bin/activate
myst start
```

To reproduce a production build (executes all code cells):

```bash
myst build --html --execute
```

## Why the Python environment is required

The readings contain **203 executable code cells** that run at build time. Their
printed output — arrays, timings, convergence tables, figures — is part of the
course content, not decoration. A build without `--execute` will render the
pages but strip those results, so always use `--execute` when checking
correctness.

## Repository layout

| Path | Contents |
|:--|:--|
| `01-course-info/` | Syllabus, schedule, AI policy, grading |
| `02-getting-started/` | CLI, environment setup, Git, software engineering |
| `03-python/` | Python fundamentals (chapters 1–6) |
| `04-scientific-computing/` | NumPy, Matplotlib, pandas, robust computing, OOP |
| `05-numerical-methods/` | Finite differences, root finding, quadrature, ODEs |
| `06-linear-algebra-stats/` | Linear algebra, probability, statistical inference |
| `scripts/` | `qmd2myst.py` — Quarto → MyST converter; `check_landing_page.py` — landing-page source-of-truth check |
| `_instructor/` | Local-only instructor workspace; separate Git repository, never tracked or published by this repository |

## Content provenance

Readings were migrated from
[`comp536-sp26`](https://github.com/astrobytes-edu/comp536-sp26) using
`scripts/qmd2myst.py`. Prose is preserved **verbatim**; only Quarto-specific
syntax was translated (callout divs, executable cell fences, cell options,
frontmatter).

The converter is idempotent and re-runnable: it reads `.qmd` from a source tree
and writes `.md` to a destination tree, never editing in place. To re-sync after
an upstream fix in `comp536-sp26`:

```bash
python3 scripts/qmd2myst.py ../comp536-sp26/03-scientific-computing-with-python/01-python-fundamentals 03-python
```

### Local overrides — re-syncing will clobber these

Some converted files carry hand edits that do **not** exist upstream. Re-running
the converter over their directories will overwrite them. Re-apply after any
re-sync:

| File | Local edit |
|:--|:--|
| `02-getting-started/*.md` | Course-local Fall 2026 rewrite: P1 readiness route, minimal environment, GitHub CLI authentication, Classroom50, notebook-first P1/P2+ contract, safe Git recovery, engineering workflow, and notebook-writing guide |

Treat the entire Getting Started module as locally owned; do not overwrite it
from the older source course. GitHub Classroom stopped accepting new sign-ups
in May 2026 and is scheduled for decommissioning on **28 August 2026**. COMP 521
uses Classroom50 and publishes only the course-specific steps verified in the
fresh-student rehearsal.

## Still to be written

These readings do not exist in any source repo and must be authored:

- **Data acquisition and cleaning** (Week 6) — APIs, Lightkurve, quality flags
- **Time series analysis** (Week 10) — autocorrelation, periodograms
- **Supervised learning from scratch** (Week 11) — k-NN, decision trees
- **Clustering, PCA, and model evaluation** (Week 12)

The ODE module (`05-numerical-methods/03-odes/`) is also noticeably thinner than
its neighbors and warrants expansion before Week 9.
