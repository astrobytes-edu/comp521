# COMP 536 Low-Breakage Grading Workflow

## Purpose

This workflow is designed to reduce grading friction, discourage last-minute panic submissions, and help students recognize whether they are on track **without building a fragile autograding system**.

The goal is not to fully automate grading. The goal is to create a lightweight structure that catches obvious technical problems early and gives students clear responsibility for monitoring their own progress.

> **Core principle:** Autograding should check the floor. Human grading should evaluate the ceiling.

---

## Why Not Start with Full GitHub Classroom Autograding?

A full autograding system with timed milestones, hidden tests, scheduled GitHub Actions, and multiple grading workflows can become a second course to maintain. It can also break in ways that create more work rather than less.

Common failure modes:

- GitHub Actions YAML breaks.
- Dependencies fail to install.
- Student environments differ from the grader environment.
- Tests are too brittle or too strict.
- Scientific numerical tolerances need constant adjustment.
- Students game the tests instead of learning the science.
- The instructor spends more time maintaining the grader than grading.

For a project-based computational science course, this is not the right first step.

Instead, start with a simpler, more robust system.

---

## Recommended Minimal System

Use three lightweight tools:

| Tool | Purpose | Complexity |
|---|---|---:|
| `validate_project.py` | Checks baseline technical correctness | Low |
| `PROGRESS.md` | Documents weekly progress and blockers | Very low |
| Manual rubric | Evaluates reasoning, interpretation, design, and communication | Necessary |

Optional later:

| Tool | Purpose | When to add |
|---|---|---|
| GitHub Actions | Automatically runs validation on push | After validation scripts are stable |
| Hidden tests | Checks generalization and prevents hard-coding | After public tests are mature |
| Timed milestone autograding | Enforces progress gates | Only if the simple system is not enough |

---

## The Basic Workflow

For each project, include:

```text
project-repo/
├── validate_project.py
├── PROGRESS.md
├── README.md
├── src/ or project files
├── analysis script / notebook
└── report / memo
```

Students are responsible for running:

```bash
python validate_project.py
```

before submission.

The validation script is **not** the full grader. It checks whether the project is technically viable enough to evaluate.

---

## What the Validation Script Should Check

Keep validation scripts intentionally small.

Good checks:

- Required files exist.
- Code imports without crashing.
- Key functions return values with the correct shape/type.
- One or two canonical validation cases pass.
- Edge cases raise appropriate errors.
- Required output files or figures exist.
- A tiny analysis run completes.

Avoid checks that are expensive or fragile:

- Full simulations.
- Large Monte Carlo runs.
- Long MCMC chains.
- Exact plot appearance.
- Long runtime benchmarks.
- Subjective code style.
- Scientific interpretation.

The validation script should answer:

> Is this submission technically coherent enough to grade?

It should not answer:

> Is this an excellent scientific project?

That remains the instructor’s job.

---

## Example: Project 1 Validation Script

```python
# validate_project.py

from pathlib import Path
import numpy as np

required_files = [
    "constants.py",
    "zams.py",
    "star.py",
    "stellar_population.py",
    "astro_plot.py",
]

missing = [f for f in required_files if not Path(f).exists()]
if missing:
    raise FileNotFoundError(f"Missing required files: {missing}")

import zams

# Canonical ZAMS validation case
L_sun_zams = zams.luminosity(1.0)
assert np.isclose(L_sun_zams, 0.698, rtol=0.02), (
    f"Expected L(1 Msun) ≈ 0.698 Lsun, got {L_sun_zams}"
)

# Vectorization check
masses = np.array([0.5, 1.0, 2.0])
L = zams.luminosity(masses)
assert isinstance(L, np.ndarray), "luminosity() should support numpy arrays"
assert L.shape == masses.shape, "Output shape should match input shape"
assert np.all(np.isfinite(L)), "Luminosities must be finite"
assert np.all(L > 0), "Luminosities must be positive"

print("✅ Basic validation passed.")
```

This catches many common problems:

- Missing files.
- Broken imports.
- Incorrect solar ZAMS value.
- Non-vectorized implementation.
- Invalid or nonphysical outputs.

It does **not** evaluate the research memo, plots, code quality, or scientific insight.

---

## Example: Project 2 Validation Ideas

For an N-body project, the validation script might check:

- Package imports.
- Acceleration function returns an `(N, 3)` array.
- Two-body forces are equal and opposite for equal masses.
- Potential energy does not double-count pairs.
- Leapfrog conserves energy on a tiny two-body test.
- Kroupa sampler returns masses in the valid range.
- Plummer sampler returns finite centered positions.

Example snippets:

```python
import numpy as np

from nbody import acceleration, potential_energy


def test_acceleration_shape():
    x = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    m = np.array([1.0, 1.0])
    a = acceleration(x, m, eps=0.01)
    assert a.shape == x.shape


def test_two_body_symmetry():
    x = np.array([[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    m = np.array([1.0, 1.0])
    a = acceleration(x, m, eps=0.0)
    assert np.allclose(a[0], -a[1])


def test_potential_energy_no_double_counting():
    x = np.array([[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    m = np.array([1.0, 1.0])
    W = potential_energy(x, m, G=1.0, eps=0.0)
    assert np.isclose(W, -1.0)
```

These are small scientific sanity checks, not full simulations.

---

## Progress Log Requirement

Each project should include a `PROGRESS.md` file.

This makes student progress visible without requiring complicated timed autograding.

### Template

```markdown
# Progress Log

## Week 1 Checkpoint

### What works
- 

### What is currently broken or incomplete
- 

### Latest validation result
- Command run: `python validate_project.py`
- Result: passing / failing
- If failing, paste the most relevant error message.

### Latest meaningful commit
- Commit hash or link:

### Specific blocker or question
- 

---

## Week 2 Checkpoint

### What works
- 

### What is currently broken or incomplete
- 

### Latest validation result
- Command run: `python validate_project.py`
- Result: passing / failing
- If failing, paste the most relevant error message.

### Latest meaningful commit
- Commit hash or link:

### Specific blocker or question
- 
```

---

## How to Grade the Progress Log

Keep this simple.

Suggested weight: **5–10% of the project grade**.

Example rubric:

| Score | Criteria |
|---:|---|
| Full credit | Updated on time, specific progress, validation result included, meaningful blocker/question identified |
| Partial credit | Present but vague, missing validation result, or updated late |
| No credit | Missing, empty, or clearly created only at the end |

The progress log is not meant to reward perfection. It rewards evidence of sustained engagement.

---

## Suggested Project Grading Split

For a 100-point project:

| Component | Points | Grading mode |
|---|---:|---|
| Baseline validation script | 10–15 | Run `validate_project.py` |
| Progress log | 5–10 | Manual check |
| Technical implementation | 25–35 | Human + validation results |
| Code quality / architecture | 10–15 | Human rubric |
| Figures and scientific validation | 10–15 | Human rubric |
| Research memo / interpretation | 20–25 | Human rubric |
| Growth memo / AI reflection | 5–10 | Human rubric |

This keeps the course focused on reasoning and scientific judgment while reducing time wasted debugging completely broken submissions.

---

## Suggested Course Policy Language

```markdown
## Project Validation and Progress Tracking

Each project includes a lightweight validation script, `validate_project.py`. This script checks baseline technical functionality such as required files, imports, simple physical validation cases, and basic reproducibility.

Students are responsible for running this script before submitting their project:

```bash
python validate_project.py
```

Passing the validation script is not sufficient for full credit. It only indicates that the submission satisfies baseline technical checks. Final grading also includes human evaluation of code quality, scientific validation, figures, research memo, growth memo, AI usage, and assignment-specific requirements.

Failing the validation script is an indication that the technical implementation is not yet at baseline. Students should treat validation failures as early warnings and seek help before the deadline.

Each project also includes a `PROGRESS.md` file. Students must update this file at the required checkpoint(s) with a brief summary of what works, what is incomplete, the latest validation result, and any specific blocker or question. The progress log is part of the project grade and is intended to encourage steady, professional work habits rather than last-minute rescue attempts.
```

---

## Anti-Babysitting Framing

This system is not meant to make the instructor responsible for monitoring every student constantly.

It shifts responsibility to students:

- They must run the validation script.
- They must document progress.
- They must identify blockers early.
- They must seek help before the deadline.
- They must submit a technically coherent project.

The instructor’s role is to provide structure, feedback, and support — not to rescue students after weeks of non-engagement.

---

## Recommended First Implementation

Do this first:

1. Add `validate_project.py` to each project.
2. Add `PROGRESS.md` to each project repo.
3. Make validation worth 10–15%.
4. Make progress logging worth 5–10%.
5. Apply late policies consistently.
6. Use GitHub commit history as supporting evidence of sustained work.

Do **not** start with:

- scheduled GitHub Actions,
- hidden tests,
- complex autograding,
- separate milestone repos,
- large test suites,
- automated timing gates.

Add those only after the validation scripts have stabilized across at least one course offering.

---

## Bottom Line

The goal is to get most of the benefit of autograding without building a fragile autograding machine.

A simple validation script plus a progress log gives students a clear baseline, gives the instructor faster grading triage, and makes disengagement visible early — all while preserving the human evaluation that matters most in a computational science course.
