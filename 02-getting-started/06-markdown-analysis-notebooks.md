---
title: "Markdown for Analysis Notebooks"
subtitle: "A submission-focused reference for COMP 521"
author: "Anna Rosen"
---

An analysis notebook is both a computational record and a scientific argument.
Code produces evidence; Markdown tells a reader what question you asked, what
you did, what happened, and what the result means.

:::{important} Follow the current project brief
Project 1 places interpretation immediately after each part and ends with
`Looking back`; it does not require a separate final report. From Project 2
onward, follow the headings and final `Discussion` requirements in that
project's brief. The brief wins if a generic example on this page differs.
:::

## Give Markdown and code different jobs

| Cell type | Its job |
|---|---|
| **Markdown** | State the question, explain the method, identify assumptions and units, cite sources, introduce evidence, and interpret it. |
| **Code** | Perform one coherent computational step and produce the evidence discussed nearby. |

Do not narrate every Python line. Explain the scientific or computational
choice that the code implements.

## Build a visible notebook spine

A reader should understand the analysis by scanning the headings. Use `#` once
for the notebook title, `##` for major sections, and `###` only when a major
section genuinely needs subsections.

For a later project, a useful pattern might be:

```markdown
# Project title

## Question and approach
What am I trying to determine, and what is my plan?

## Setup and assumptions
What inputs, units, constants, sources, and conventions do I use?

## Method and verification
What computation am I performing, and what could reveal a mistake?

## Results
What did the computation produce?

## Discussion
What does the result mean, how trustworthy is it, and what are its limits?
```

Do not impose that template on P1. Use its required Part 1–4 structure, answer
each **Interpret your result** prompt next to the evidence it discusses, and end
with the required `Looking back` heading.

## Markdown syntax you will use

### Paragraphs and emphasis

Separate paragraphs with a blank line. Use **bold** for a small number of terms
or conclusions and *italics* for genuine emphasis. Bold text is not a substitute
for a heading.

### Lists

Use a list when items are parallel:

```markdown
The verification checks are:

- the solar luminosity anchor;
- agreement at the transit branch boundaries; and
- agreement between loop and vectorized curves.
```

Use prose when the relationship among ideas is the important part.

### Mathematics

Use dollar signs in Markdown cells:

```markdown
The expected mid-transit depth is $\delta = p^2$.

$$
L = 4\pi R^2 \sigma T_{\mathrm{eff}}^4.
$$
```

Define symbols before using them and state units for dimensional quantities.
An equation is not self-documenting: cite or derive it and state the
approximation under which it applies.

### Links and citations

Use meaningful link text:

```markdown
[NumPy broadcasting documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html)
```

For an external equation, dataset, coefficient, or comparison value, identify
the author or organization, title or dataset name, year/version when available,
and a stable link or citation. Put the source near the analysis that depends on
it. “Found online” and a bare URL do not establish provenance.

### Tables

Use small tables for compact comparisons:

```markdown
| Check | Expected | Obtained |
|---|---:|---:|
| Solar luminosity [$L_\odot$] | 1.000 | 1.000 |
| Transit depth | $p^2$ | 0.0100 |
```

Put units in a heading or value instead of leaving them implicit.

## Write around the evidence

Introduce a computation **before** its code cell and interpret its output
**after** it. A strong interpretation names:

1. the expectation;
2. the observation;
3. the comparison or discrepancy;
4. the claim the evidence supports; and
5. a limitation or alternative not ruled out.

Weak:

> Here is my plot. It looks right.

Stronger:

> The uniform-disk model predicts a mid-transit depth of
> `p^2 = 0.0100`. The computed minimum flux is 0.9900, agreeing to the displayed
> precision. This checks the depth in the fully overlapping branch; it does not
> test the partial-overlap geometry, which I check separately at contact.

The stronger version tells a reader exactly why the output matters.

## Make figures readable and accessible

For every notebook-generated figure:

- label axes with the physical quantity and units;
- use text, ticks, and line weights that remain readable at normal page size;
- distinguish multiple series with markers, linestyles, or direct labels as
  well as color;
- use a legend only when its mapping is unambiguous;
- avoid screenshots when the notebook can generate the figure; and
- add nearby prose stating the main visual pattern and an important limitation.

Matplotlib output in a notebook does not provide ordinary Markdown alt text.
The nearby prose is therefore part of making the scientific point available to
a reader who cannot rely on color or detailed visual inspection.

When embedding a separate image file, use a relative path and descriptive alt
text:

```markdown
![Normalized transit flux decreases during ingress, remains flat at full
overlap, and returns symmetrically during egress.](figures/transit-curve.png)
```

The alt text should communicate the purpose or pattern, not begin with “image
of.” Do not paste screenshots of code, equations, tables, or error messages
that could be represented as text.

## Keep the execution path obvious

- Put imports and configuration near the top.
- Use paths relative to the repository.
- Do not require a reader to edit a variable manually between cells.
- Keep each code cell focused enough that its output has a clear purpose.
- Remove abandoned experiments and dead cells before submission.
- Report an expected runtime when a cell is meaningfully slow.
- Preserve useful checks and explain warnings instead of hiding them.
- From P2 onward, import reusable implementation from the modules required by
  the brief; do not duplicate it in the notebook.

## Before you submit

1. Follow the current brief's required headings, filenames, and written prompts.
2. Confirm sources and units are visible where used.
3. Use **Kernel → Restart Kernel and Run All Cells**.
4. Confirm every cell runs in order without manual intervention.
5. Check that figures, tables, and numerical outputs appear where the prose says
   they do.
6. Read only the headings and first sentence of each section; the argument
   should still be recognizable.
7. Run any additional reproduction or test command named in the project brief.
8. Save, stage the intended files, commit, and push.
9. Open the repository on GitHub and verify that it contains the final notebook,
   figures, README, and every other required file.

:::{note} Reader independence
The notebook is ready when the instructor can clone the repository, follow its
instructions, run the notebook from a clean kernel, and understand both the
analysis and its limits without asking what a section was meant to do.
:::
