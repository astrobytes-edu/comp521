# Scientific Computing with Python Textbook Design

## Status

**Status:** Approved direction; living design, revision 1.

This document defines the independent textbook identity of *Scientific
Computing with Python*. It is deliberately separate from COMP 521's weekly
schedule, projects, grading, and classroom logistics. The course may provide
reading maps and application overlays that point into the textbook, but those
overlays must not become part of the textbook's instructional contract.

## Purpose

The textbook teaches students and research trainees how to build, inspect,
test, and communicate scientific computations. It should remain useful when:

- used in a different course with different projects;
- read by a research student outside a course;
- consulted later as a diagnostic reference; or
- adapted to a different scientific domain.

The book's core promise is not “learn Python syntax.” It is:

> Build computational evidence that another scientist can inspect, rerun, and
> challenge.

Astrophysical examples remain valuable illustrations, but no chapter depends on
astronomy knowledge or presents astronomy as its only intended domain.

## Non-negotiable design constraints

1. The textbook contains **no expected-time estimates**.
2. The textbook contains **no course project names, course deadlines, grading
   rules, or submission requirements**.
3. The course-facing site may supply separate reading maps, lecture pages,
   practice labs, and assessments that link to exact textbook sections.
4. `Part` is the sole top-level textbook hierarchy. `Chapter` identifies a
   numbered instructional unit. `Guide` identifies a part entry page. `Recap`
   identifies an unnumbered integrative reference page.
5. Guides and recaps are not chapters and must never be numbered as though they
   were peer instructional units.
6. A chapter cannot claim to be complete merely because it has a title and a
   place in the table of contents. It must satisfy the shared chapter contract
   below.
7. Advanced material is useful only when its scope, prerequisites, and reason
   for deferral are visible. Depth is not an excuse for obscuring the core.

## Canonical information architecture

```text
Scientific Computing with Python
├── Part I · Foundations for Scientific Programming
│   ├── Start Here: Part I Guide
│   ├── Chapter 1 · Computational Environments & Scientific Workflows
│   ├── Chapter 2 · Python as Your Scientific Calculator
│   ├── Chapter 3 · Control Flow & Logic
│   ├── Chapter 4 · Data Structures: Organizing Scientific Data
│   ├── Chapter 5 · Functions & Modules: Building Reusable Scientific Code
│   ├── Chapter 6 · Object-Oriented Programming Fundamentals
│   └── Part I Recap · Trustworthy Scientific Programming
├── Part II · Arrays, Visualization, and Reliable Computing
│   ├── Start Here: Part II Guide
│   ├── Chapter 7 · NumPy Fundamentals
│   ├── Chapter 8 · Matplotlib: Visualizing Scientific Evidence
│   ├── Chapter 9 · Testing, Failure Modes, and Reproducible Scientific Code
│   └── Chapter 10 · Designing Small Scientific Types
├── Part III · Tabular Data and Reproducible Workflows
│   ├── Start Here: Part III Guide
│   ├── Chapter 11 · Pandas: Organizing Scientific Data
│   └── Chapter 12 · From Raw Data to a Defensible Dataset
└── Part IV · Research Software Practice
    ├── Guide: Quality Workflow for Scientific Python
    ├── Packages, Environments, and Reproducible Releases
    ├── Numerical Testing and Performance Measurement
    ├── Scientific Data Formats, Metadata, and Provenance
    └── APIs, Parallelism, and Larger Research Software
```

Parts I–III are the canonical numbered textbook. Part IV is a research-software
reference expansion: its architecture is approved now, but it does not make
unwritten pages appear as completed instruction. Its first published component
will follow the Chapter 9 hardening pass.

## Current pages and renamed roles

| Current source | New role and title | Required change |
| --- | --- | --- |
| `03-python/index.md` | **Start Here: Part I Guide — Foundations for Scientific Programming** | Remove course-specific policy and project route language; retain the purpose, chapter map, diagnostic lookup table, and general “how to use this book” guidance. |
| `03-python/synthesis.md` | **Part I Recap — Trustworthy Scientific Programming** | Keep its diagnostic-manual role; remove all “module” terminology and make it an unnumbered recap. |
| `04-scientific-computing/index.md` | **Start Here: Part II Guide — Arrays, Visualization, and Reliable Computing** | Limit its route to Chapters 7–10; remove Chapter 11 and promises not supported by Chapter 10. |
| `04-scientific-computing/part-3-data-workflows.md` | **Start Here: Part III Guide — Tabular Data and Reproducible Workflows** | Retain the data-to-evidence framing and reading sequence; remove course-project references. |
| `04-scientific-computing/12-data-acquisition-cleaning.md` | **Chapter 12 — From Raw Data to a Defensible Dataset** | Keep an explicit availability status until the chapter meets the shared contract; do not represent a scope note as finished instruction. |

## Course overlays versus textbook content

The course site owns:

- weekly preparation routes;
- lecture pages and in-class prompts;
- practice labs;
- project briefs, submission instructions, and grading; and
- course-specific technology policy.

The textbook owns:

- durable conceptual explanations;
- runnable, domain-transferable examples;
- common misconceptions and diagnostic cues;
- exercises and application prompts that do not assume a particular course;
- concise reference material; and
- scientific software practices with their assumptions and limits.

A course overlay may say “read Sections 3.1 and 3.4 before this activity.” The
textbook may say “apply this pattern to a convergence algorithm.” Neither
should copy the other’s prose.

## Shared chapter contract

Every completed numbered chapter must present the following structure near the
top of the page, in this order:

1. **Scientific question and why it matters** — a concrete problem or
   misconception, stated without career-scale or disaster rhetoric.
2. **Core ideas** — the small conceptual set needed to use the chapter safely.
3. **Prerequisites** — links to concepts actually needed, not a generic list of
   earlier chapters.
4. **Learning objectives** — three to five observable outcomes, using verbs
   such as predict, implement, diagnose, compare, and justify.
5. **Worked scientific example** — a bounded example with variables, units,
   assumptions, and expected behavior made visible.
6. **Predict → run → explain check** — a small activity in which the reader
   predicts an output or failure mode, runs or inspects a result, and explains
   the observation.
7. **Apply or extend** — a domain-transferable prompt, such as adapting a
   tolerance test, checking a shape invariant, or documenting a cleaning
   choice. It must not mention a course project.
8. **Recap and honest next connection** — a diagnostic summary plus a link to
   the actual next chapter or relevant guide.

Chapters may include a visibly marked **Deep dive / reference** section after
the core material. Deep dives contain advanced patterns, less-common APIs,
implementation internals, or specialized domain examples. They must not be
presented as required to understand the core chapter.

## Chapter-level content decisions

### Part I: foundations

**Chapter 1 — Computational Environments & Scientific Workflows**

- Core: interpreter/environment identity, reproducible execution, clean
  notebook kernels, and the difference between exploratory notebooks and
  reusable code.
- Deep dive: import internals, cluster modules, environment-file mechanics,
  and detailed environment debugging.
- Remove course setup requirements from the prerequisite checklist; the guide
  may link to an optional setup companion.

**Chapter 2 — Python as Your Scientific Calculator**

- Core: arithmetic, variables, units-aware naming, floating-point comparison,
  finite values, and simple numerical checks.
- Deep dive: complex numbers, Fourier illustrations, cancellation,
  overflow/underflow, and advanced numerical strategies.

**Chapter 3 — Control Flow & Logic**

- Core: pseudocode, conditionals, loops, guard clauses, explicit termination,
  and bounded convergence patterns.
- Deep dive: advanced loop syntax, comprehensions beyond the core cases, and
  debugger-specific tooling.

**Chapter 4 — Data Structures: Organizing Scientific Data**

- Core: selecting list, tuple, dictionary, or set; mutability and aliasing;
  membership and lookup behavior; simple complexity reasoning.
- Deep dive: memory-layout internals, caching, spatial structures, and
  benchmark design.

**Chapter 5 — Functions & Modules: Building Reusable Scientific Code**

- Core: function contracts, input/output units, pure versus stateful behavior,
  module boundaries, documentation, and lightweight type annotations on public
  functions.
- Deep dive: closures, decorators, advanced argument rules, package internals,
  and advanced typing.

**Chapter 6 — Object-Oriented Programming Fundamentals**

- Core: stateful entities, validation/invariants, small classes, and explicit
  cases where a function or data structure is simpler.
- Deep dive: inheritance and special-method catalogues.

### Part II: arrays, figures, and trustworthy code

**Chapter 7 — NumPy Fundamentals**

- Core: array shape, axes, dtype, copies versus views, vectorization,
  broadcasting, masking, and reproducible random generators.
- Deep dive: FFT, interpolation, Monte Carlo, numerical differentiation, and
  integration. The FFT material must either explain frequency-bin ordering and
  normalization accurately or move out of this chapter.

**Chapter 8 — Matplotlib: Visualizing Scientific Evidence**

- Core: the object-oriented `Figure`/`Axes` model; labels and units; scale
  choices; uncertainty representation; accessible color; export; and the
  difference between a plot and a justified claim.
- Deep dive: WCS, interactive ecosystems, domain packages, and specialized
  rendering.

**Chapter 9 — Testing, Failure Modes, and Reproducible Scientific Code**

- Reframe the current robust-computing material around evidence for behavior.
- Core: validation, exceptions used deliberately, assertions, deterministic
  random generators, logging as diagnosis, `pytest` discovery, arrange-act-
  assert tests, parameterized boundary tests, tolerances, known solutions, and
  convergence tests.
- Required distinction: passing tests demonstrates stated behavior; it does
  not establish physical adequacy, calibration, or scientific validity.
- Tooling: introduce Ruff formatting/linting as a readable feedback loop and
  type checking as an incremental boundary-contract check. Do not require
  strict typing or a particular type-checker for basic use.

**Chapter 10 — Designing Small Scientific Types**

- Rebuild around dataclasses or similarly small types, invariants, validation,
  composition, readable representations, and a single bounded scientific
  entity.
- Move abstract base classes, multiple inheritance, mixins, async,
  metaclasses, descriptor internals, architecture catalogues, and universal
  performance claims to Part IV reference.
- Replace claims about NumPy/Matplotlib internals and fixed speed or memory
  multipliers with local, reproducible measurements or qualified language.

### Part III: data to evidence

**Chapter 11 — Pandas: Organizing Scientific Data**

- Core: tables, schema/metadata inspection, selecting and filtering,
  aggregation, joins when warranted, time-indexed data, and plots that inspect
  rather than overstate.
- Remove advanced-OOP prerequisites and generic simulation-first framing.
- Preserve missingness by default. Any interpolation, imputation, or row
  exclusion requires a stated domain rationale and sensitivity check.

**Chapter 12 — From Raw Data to a Defensible Dataset**

- Build a completed chapter before presenting it as a normal chapter.
- Core: source/query provenance, raw versus derived artifacts, schemas/data
  dictionaries, quality flags, missingness, cleaning decision records,
  row-count/checksum checks, exploratory diagnostics, and an analysis-ready
  dataset that another reader can trace.
- Include one complete, runnable workflow using a public scientific dataset or
  a small bundled example with durable provenance.

## Research software practice: Part IV

Part IV is intentionally a reference expansion rather than early required
material. It provides durable answers for students whose work has grown beyond
a notebook or a single module.

### Guide: Quality Workflow for Scientific Python

This first Part IV page is the likely earliest publication. It explains a
small, interoperable feedback loop:

| Practice | Scientific purpose | Initial scope |
| --- | --- | --- |
| formatter and linter | readable diffs and likely-bug detection | Ruff format and Ruff check |
| tests | behavioral and numerical contracts | pytest, tolerances, regression cases |
| type hints | clear function and class boundaries | annotations on public APIs |
| static checking | detect incompatible interfaces before execution | one configured checker, introduced incrementally |
| continuous integration | rerun the same checks outside one laptop | template/instructor infrastructure first |

Ruff is the recommended starter formatter/linter because it unifies both
operations through project configuration. Pytest is the recommended testing
framework. The book describes static typing in tool-neutral terms and may show
one checker configuration at a time; it does not present strict typing as a
marker of professional worth.

Tooling rationale is grounded in the primary guidance for
[Ruff](https://docs.astral.sh/ruff/),
[pytest](https://docs.pytest.org/en/stable/), and the
[Scientific Python Development Guide on testing](https://learn.scientific-python.org/development/guides/pytest/),
[style checks](https://learn.scientific-python.org/development/guides/style/),
and [static typing](https://learn.scientific-python.org/development/guides/typing/).

### Later Part IV references

- **Packages, Environments, and Reproducible Releases:** `pyproject.toml`,
  dependencies, lockfiles, command-line interfaces, configuration, and release
  artifacts.
- **Numerical Testing and Performance Measurement:** property/metamorphic
  checks, convergence studies, benchmarks, profiling, and performance claims
  tied to a measured workload.
- **Scientific Data Formats, Metadata, and Provenance:** CSV, Parquet, FITS,
  HDF5, Zarr, dimensions/units, coordinate metadata, and preservation of raw
  inputs.
- **APIs, Parallelism, and Larger Research Software:** interfaces, protocols,
  concurrency, parallelism, and larger-codebase architecture. Async and
  metaprogramming belong here, not in the first path through the book.

## Terminology and accuracy remediation

The hardening pass must remove or correct the following current defects:

- Replace book-level use of `module` with `part`, `chapter`, `guide`, or
  `recap` according to the hierarchy above.
- Correct Part II so it names only Chapters 7–10; Chapter 11 belongs only in
  Part III.
- Rewrite Chapter 9's stale “final chapter of Module 2 / Module 3” preview and
  Chapter 10's forward link so they reflect the real Part III boundary.
- Correct cross-references that claim Chapter 6 taught file I/O when it did
  not. A prerequisite link must point to the chapter or section that actually
  teaches the concept.
- Replace overconfident claims, fixed universal speedups, and unverified
  statements about third-party-library internals with evidence, reproducible
  local demonstrations, or qualified wording.
- Remove generic “still being revised” banners from completed chapters once
  their hardening pass is complete. Retain a concise status card only for a
  genuinely incomplete page such as Chapter 12.
- Use the Part III subtitle for Chapter 11 rather than “Scientific Computing
  Core.”

## Accessibility and scientific integrity

- Code examples must state assumptions, units, and expected qualitative or
  numerical behavior where those are relevant.
- Figures must have descriptive captions, readable labels, color-safe
  encodings, and explicit axes/units.
- Examples should prefer a small number of realistic decisions over a long
  parade of APIs.
- Claims about models, performance, library internals, and incidents require
  a source, an executable demonstration, or clearly qualified language.
- Exercises must never reward plotting without interpretation, passing tests
  without a behavioral claim, or a numerical result without a tolerance or
  validation argument.

## Completion and release criteria

### A completed chapter

A numbered chapter is complete when it satisfies the shared chapter contract,
has accurate prerequisites and next links, renders correctly, and its examples
run in the declared environment or are visibly marked as pseudocode.

### A completed part

A part is complete when its guide points only to its own actual chapters, its
terminology agrees with the navigation, and it provides a diagnostic route for
returning readers.

### A textbook release slice

For each hardening slice:

1. perform a content and technical cross-reference audit;
2. execute or otherwise qualify changed code examples;
3. build MyST in strict mode and run math/link checks;
4. inspect desktop and narrow-screen rendered pages; and
5. perform an adversarial pedagogy review before claiming the affected chapter
   or part is student-ready.

## Migration order

1. Apply the hierarchy and guide/recap naming convention; fix Part II/III
   routing and stale terminology.
2. Harden the Part I Guide and Recap as independent book pages; remove COMP
   521 policy and project language from textbook pages.
3. Harden Chapters 9 and 10 first, because testing and restrained scientific
   type design provide the highest reusable value for the current book.
4. Establish the shared chapter contract across Chapters 1–8 and 11, beginning
   with core/deep-dive separation and accurate prerequisite/next links.
5. Author Chapter 12 fully before calling Part III complete.
6. Publish the Part IV Quality Workflow guide after Chapter 9 establishes the
   conceptual base; stage later Part IV references as substantive pages, not
   empty placeholders.

## Open iteration questions

These are intentional design choices to revisit with evidence, not blockers:

- Whether Part IV uses numbered chapters or unnumbered reference guides after
  the first Quality Workflow page is drafted.
- Which public, durable dataset best supports Chapter 12 without making the
  book astronomy-only.
- Which single type checker receives executable examples once the supported
  environment and editor pathway are frozen.
- Whether selected deep dives remain in long chapter pages or become separate
  appendix/reference pages after a reader walkthrough reveals navigation load.
