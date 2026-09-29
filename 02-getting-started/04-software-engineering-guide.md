---
title: "Scientific Software: From Claim to Evidence"
subtitle: "A practical guide for COMP 521 projects"
author: "Anna Rosen"
---

Scientific software connects a claim about the world to evidence a reader can
inspect. “The code ran” is only the beginning: you also need to know what the
calculation was meant to do, which checks could reveal a mistake, and what the
result does—and does not—support.

For the full eleven-commandment treatment, extended stellar-model examples, and
debugging reference, see [Software Engineering for Scientists](software-engineering-for-scientists.md).

## The course workflow changes after P1

| Phase | Implementation | Required execution path |
|---|---|---|
| **Project 1** | Functions may live in `analysis.ipynb`. No modules or classes are required. | Restart the kernel, run all cells, interpret each part, save, commit, and push. |
| **Project 2 onward** | Reusable implementation moves into `.py` modules; the notebook imports it. | Run the checks, tests, and reproduction commands named in that project's brief. |

The project brief owns the exact filenames and commands. There is no universal
`run.py validate/test/make-figures` interface in COMP 521.

:::{important} A useful working loop
Define the claim → write the contract → implement the smallest case → collect
claim-matched evidence → interpret the result → commit a state worth keeping.
:::

## Part I: From question to contract

### 1. Start from the scientific question

Before writing a function, answer:

1. What quantity or behavior am I trying to determine?
2. Which inputs are measured, chosen, or derived?
3. What approximation or model connects them to the output?
4. Which result would surprise me enough to suspect a mistake?
5. What is the cheapest check that could distinguish “working” from “plausible
   but wrong”?

For P1's uniform-source transit, the question is not merely “can I evaluate an
overlap formula?” It is “what fraction of a uniformly bright stellar disk
remains visible for a given radius ratio and projected separation?” That
wording identifies the observable—normalized flux—and the approximation—a
uniform stellar disk.

### 2. Write a contract before an implementation

A function contract makes assumptions visible. Use this compact template:

```text
Purpose:
Inputs: names, meanings, units, scalar/array shape
Output: meaning, units, shape
Valid domain:
Expected boundaries or limiting cases:
Invalid-input behavior required by the brief:
Reference or derivation:
```

Separate three sources of authority:

- A **scientific source** may establish an equation, coefficient, calibration,
  or validity range.
- A **project brief** establishes the assignment's required interface and
  deliverables.
- You make **implementation decisions** only where those sources leave room.

A paper rarely specifies a Python API. A coefficient is a model assumption, not
an invariant. A published validity range does not automatically mean your
function must raise `ValueError`; enforce that behavior only when the project
or your documented interface requires it.

#### P1 example: `flux(p, z)`

The project defines:

- `p = R_p/R_★`, a dimensionless radius ratio;
- `z = d/R_★`, a dimensionless projected center separation; and
- `flux(p, z)`, normalized stellar flux.

Before coding, record the consequences:

- normalized flux must remain between 0 and 1 for physical inputs;
- no overlap must give 1;
- a smaller disk fully inside the star blocks an area fraction `p**2`;
- a sufficiently large foreground disk can cover the star completely;
- partial overlap must meet its neighboring branches at the contact points.

Those statements are testable consequences of the model. Whether the P1
function accepts arrays, clips invalid values, or raises an error is a separate
interface question; follow the brief instead of adding unrequested behavior.

## Part II: Scientific evidence and numerical comparison

### 3. Match evidence to the claim

Different checks answer different questions and sometimes overlap:

| Evidence | A question it can answer | A question it cannot answer alone |
|---|---|---|
| Reference or analytic comparison | Does this result reproduce a trusted value or derived limit? | Does every branch and shape behave correctly? |
| Behavioral check or automated test | Does the implementation meet this stated contract for these cases? | Is the scientific model appropriate for the real system? |
| Visual diagnostic | Are trends, discontinuities, outliers, or structure visible? | Is a curve correct merely because it looks smooth? |
| Clean reproduction | Can another reader generate the same evidence from the repository? | Is the evidence scientifically persuasive? |

A check supports only the claim it actually probes. One solar-luminosity anchor
does not validate an entire HR diagram; a passing boundary test does not show
that the uniform-disk approximation describes a limb-darkened star.

#### Strong P1 checks

For the current project, useful evidence includes:

- **Stefan–Boltzmann anchor:** the nominal solar radius and temperature recover
  the nominal solar luminosity under the chosen normalization.
- **Physical bounds:** representative transit fluxes satisfy
  `0 <= flux <= 1`.
- **Branch boundaries:** evaluate just below, at, and just above each contact
  for representative `p < 1` and `p > 1`.
- **Transit depth:** for `p < 1` at full overlap, the depth agrees with
  `p**2`.
- **Two implementations:** the loop and vectorized transit curves agree within
  a stated numerical tolerance.
- **Figure diagnosis:** the light curve shows the predicted baseline, ingress,
  flat or curved interior implied by the model, and egress—but the plot is not
  a substitute for the numerical checks above.

The best check is often a limiting case you can derive independently of the
full implementation.

### 4. Compare floating-point results intentionally

Computed floating-point values should usually be compared with a tolerance:

```python
np.isclose(actual, expected, rtol=1e-12, atol=0.0)
```

Choose `rtol` and `atol` from the scale of the quantity, the numerical
operations involved, and the claim you need to support. Do not copy a tolerance
only because it makes a test pass. Report or inspect the discrepancy:

```python
error = abs(actual - expected)
relative_error = error / abs(expected)  # only when expected != 0
```

When the expected value is zero, use the absolute error rather than dividing by
zero.

Exact equality is appropriate when exactness is part of the contract—for
example, a branch deliberately returns the literal state `1`. Computed
analytic or iterative results generally need an explicit tolerance.

## Part III: Small implementations and systematic debugging

### 5. Implement the smallest discriminating case

Build one behavior that can be checked before generalizing:

1. implement one branch or one scalar case;
2. compare it with a value you can derive by hand;
3. add the neighboring boundary;
4. only then add arrays, plotting, performance, or abstraction.

This ordering keeps the source of a disagreement small. Vectorization does not
repair an incorrect scalar formula; it makes that formula fail faster.

Use descriptive names that keep the model visible:

```python
radius_ratio = planet_radius / stellar_radius
projected_separation = distance / stellar_radius
```

Names such as `p` and `z` are fine once the notebook defines them and uses
them consistently. Units belong in the surrounding prose, docstring, or name
when ambiguity is likely.

### 6. Debug by testing a hypothesis

When a result is wrong:

1. **Preserve the observation.** Save the exact input, output, warning, or
   traceback.
2. **Reduce the case.** Find the smallest input that still fails.
3. **State one hypothesis.** “The partial-overlap expression receives an
   out-of-domain arccos argument near contact” is testable; “NumPy is broken” is
   not.
4. **Choose a discriminating check.** Print the arccos argument, compare both
   sides of the boundary, or evaluate the scalar formula independently.
5. **Change one cause.** Re-run the same case and compare.
6. **Keep the check.** If the failure could return, preserve it as a notebook
   check or—starting in P2—an automated test.

For a sequential pipeline, inspect an intermediate near the middle and then
narrow toward the first disagreement. This is often efficient, but it has no
guaranteed `O(log n)` complexity: stages may interact and one fault may create
several symptoms.

#### Read warnings as data

Suppressing a warning is not the same as fixing its cause. First identify which
inputs reach the warned operation and whether that operation should have been
evaluated. Array expressions can evaluate multiple branches even when a later
`where` selects only one result; a scalar `if` does not. A correct repair
must preserve the intended values, not merely make the warning quiet.

## Part IV: Reusable modules and tests from P2 onward

### 7. Move reusable code into modules from P2 onward

P1 is deliberately notebook-first. Starting with P2:

- put reusable functions and constants in the modules named by the brief;
- import them into the notebook rather than copying their definitions;
- keep exploratory orchestration, figures, and interpretation in the notebook;
- use one canonical definition for each formula or constant; and
- run the project-required tests with `pytest` when the brief supplies that
  contract.

One test should focus on one behavior, but it may use several related assertions
to establish that behavior. Name the behavior:

```python
def test_flux_is_continuous_at_first_contact():
    ...
```

A green suite means the encoded behaviors passed under that configuration. It
does not prove that every relevant behavior was encoded or that the scientific
model is valid.

## Part V: Readable, reproducible results

### 8. Make diagnostics readable and attributable

A scientific figure should work without an oral explanation:

- label axes with quantities and units;
- use readable text and line weights;
- distinguish series with markers, linestyles, or direct labels—not color
  alone;
- state the expected pattern before the figure and interpret the observed
  pattern after it;
- name a limitation or unresolved feature; and
- cite external data, equations, or reference values near the analysis that
  uses them.

Notebook-generated plots do not have ordinary Markdown alt text. Put a nearby
sentence that states the main visual pattern and its limitation so the
scientific point is available without relying on color or visual inspection
alone.

### 9. Preserve a reproducible path

Before submitting:

- use paths relative to the repository;
- keep imports and configuration near the top of the notebook;
- record random seeds when randomness affects the result;
- remove hidden manual state and abandoned cells;
- generate every submitted figure from the repository;
- follow the project brief's exact reproduction commands; and
- restart the kernel and run the notebook from top to bottom.

If a clean run fails, the saved output is not evidence that the current code
works.

## Part VI: Safe iteration and effective help

### 10. Use Git as a checkpoint, not an undo gamble

Before a risky experiment, preserve the exact files that currently work:

```bash
git status
git add -A
git diff --staged
git commit -m "Checkpoint before vectorizing transit model"
git push
```

`git add -A` is appropriate here when every repository change shown by
`git status` belongs to the checkpoint. Use `git add .` from the repository
root for the same project-wide intent, or name paths when only a subset belongs
in the commit. Inspect the staged diff whichever form you choose.

If an experiment changes a tracked file and you decide to discard those
uncommitted edits, inspect `git diff` and then restore the committed version:

```bash
git restore path/to/file
```

That restores the file from `HEAD`—the checkpoint you just committed. Do not
use `HEAD~1`, which means the commit *before* that checkpoint. Untracked files
need separate care; `git restore` cannot recover them.

### 11. Ask for help with a scientific debugging packet

Bring:

- the claim or expected behavior;
- the smallest failing input;
- the exact output, warning, or traceback;
- the relevant contract or equation;
- one hypothesis and the check you tried; and
- `git status` plus the active Python path when environment state matters.

Use the Canvas discussion board when the answer may help others, Canvas Inbox
for a private matter, or bring the packet to class or office hours. If you use
AI for tutoring or verification, follow the [course AI
policy](../01-course-info/ai-policy.md) and remain the author of the core
solution.

## Final readiness review

- [ ] I can state the scientific question and approximation.
- [ ] Inputs, outputs, units, shapes, and valid domain are visible.
- [ ] Each important claim has evidence that actually probes it.
- [ ] Numerical tolerances are stated and justified.
- [ ] Figures are labeled, readable, color-independent, and interpreted.
- [ ] External equations, values, and data have provenance.
- [ ] P1 runs top to bottom in `analysis.ipynb`; P2+ code follows the current
  brief's module and test contract.
- [ ] The intended files are committed, pushed, and visible on GitHub.

:::{tip} Trust is built in layers
A reference comparison, a behavioral check, a diagnostic figure, and a clean
rerun each remove a different reason to doubt the result. None should claim
more than it tested.
:::
