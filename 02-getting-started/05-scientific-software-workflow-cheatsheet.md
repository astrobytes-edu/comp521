---
title: "Scientific Software Workflow Checklist"
subtitle: "A one-page companion for COMP 521 projects"
author: "Anna Rosen"
---

Keep this page beside your editor. It is a working aid, not a grading rubric;
the current project brief defines the deliverables.

## First: identify the project phase

| Project | Where implementation belongs | Final execution check |
|---|---|---|
| **P1** | Functions may remain in `analysis.ipynb`. | Restart the kernel and run all cells; save, commit, push, and verify. |
| **P2 onward** | Reusable code belongs in the modules named by the brief; the notebook imports it. | Run the brief's exact tests and reproduction commands, then restart and run the notebook. |

There is no course-wide `run.py` command. Do not substitute a generic workflow
for the repository's instructions.

## Before coding

Write down:

- **Claim:** What quantity or behavior am I trying to establish?
- **Inputs:** Meanings, units, shapes, and valid range.
- **Output:** Meaning, units, shape, and normalization.
- **Model:** Equation, approximation, or algorithm—and its source.
- **Boundary:** One limiting or edge case I can predict independently.
- **Failure signal:** What observation would make me doubt the implementation?
- **Cheapest check:** The smallest calculation that distinguishes the likely
  explanations.

If the project or reference does not specify an interface choice, label it as
your decision instead of presenting it as a scientific requirement.

## Build in small slices

1. Implement one scalar or boundary case.
2. Compare it with a value you can derive or trust.
3. Add the neighboring case.
4. Generalize to arrays or repeated evaluation.
5. Create the diagnostic figure.
6. Interpret what the evidence supports and what it does not.
7. Commit a coherent checkpoint.

## Use claim-matched evidence

| Evidence | Use it for |
|---|---|
| **Reference or analytic comparison** | anchor values, limiting cases, known solutions |
| **Behavioral check/test** | interfaces, shapes, bounds, branches, error behavior |
| **Visual diagnostic** | trends, discontinuities, outliers, residual structure |
| **Clean rerun** | reproducibility from the submitted repository |

- A smooth plot is not proof of the formula.
- A passing test is not proof that the model represents nature.
- One anchor value does not validate every regime.
- State numerical tolerances and why they are appropriate.

For P1, place compact checks directly in the notebook. From P2 onward, preserve
repeatable behavior checks in the project-required test suite.

## Debug with one hypothesis at a time

1. Save the exact input, output, warning, or traceback.
2. Reduce it to the smallest failing case.
3. State one hypothesis in a sentence.
4. Choose one observation that could disconfirm it.
5. Change one cause and rerun the same case.
6. Keep a successful regression check.

If you are stuck, bring the contract, the smallest failing input, the complete
error, and what you tried. Use the Canvas discussion board for a shared
question, Canvas Inbox for a private matter, or office hours. Follow the
[course AI policy](../01-course-info/ai-policy.md) for tutoring and verification
uses.

## Before every commit

```bash
git status
git diff
git add path/to/the-files-you-intend
git diff --staged
git commit -m "Describe the completed change"
git push
```

- Stage named files rather than everything by reflex.
- Never commit credentials, downloaded data that the brief excludes, or
  machine-specific paths.
- Do not use force-push or `reset --hard` as routine recovery.
- Verify important commits on GitHub.

## Before submitting any notebook

- [ ] The notebook's headings match the current project brief.
- [ ] Imports and configuration appear near the top.
- [ ] Paths are relative to the repository.
- [ ] Equations, data, constants, and reference values have provenance.
- [ ] Every figure has labeled quantities and units, readable text, and a
  color-independent way to distinguish series.
- [ ] Nearby prose states each figure's main pattern and a limitation.
- [ ] Numerical checks name an expectation, obtained value, and tolerance.
- [ ] Abandoned cells and hidden manual steps are gone.
- [ ] **Kernel → Restart Kernel and Run All Cells** succeeds in order.
- [ ] Saved outputs agree with the current code.
- [ ] The required files are committed, pushed, and visible on GitHub.

## P2+ additions

- [ ] Reusable implementation lives in the required `.py` modules.
- [ ] The notebook imports rather than duplicates that implementation.
- [ ] Each formula and constant has one canonical definition.
- [ ] Project-required `pytest` checks pass.
- [ ] Any random behavior uses a documented seed when reproducibility matters.
- [ ] The repository's stated reproduction command works from a fresh terminal.

:::{important} The final question
What exact claim does this result support, what evidence supports it, and what
important possibility has not been ruled out?
:::
