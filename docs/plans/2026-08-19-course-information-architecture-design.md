# COMP 521 course information architecture

**Status:** approved for implementation on 2026-08-19.

## Decision

COMP 521 will use two coordinated student paths rather than one flat
collection of pages:

1. **Course Roadmap** answers “what do I need to do this week?” It contains
   policies, schedule, assessments, and student-support information.
2. **Textbook and methods sequence** answers “how do I learn or revisit this
   idea?” It is organized by transferable concepts rather than due dates.

The course throughline is: **Build methods. Test their limits. Use them on
real data.**

## Student-facing structure

```text
Course Roadmap
Start Here
Scientific Computing with Python
  Part I — Programming for Scientific Work
  Part II — The Scientific Python Toolkit
  Part III — Real Data Workflows
Numerical Modeling
Data, Inference, and Scientific ML
```

The schedule provides the week-by-week route through these materials; projects
link to the readings needed to begin them. The textbook does not duplicate
deadlines or project specifications.

## Implementation boundaries

- Preserve existing URLs and teaching content during this structural pass.
- Add short, clearly marked placeholder pages only for readings already
  promised by the Fall 2026 schedule.
- Record the complete course-production and verification work in the local,
  nested `_instructor` repository.
- Defer the substantive reading rewrite, project-5/6 design, and page-level
  accessibility/content audit to later focused passes.

## Validation

- MyST navigation must build without unresolved page references.
- Every scheduled formerly “to be posted” reading must have a visible,
  accurate landing page.
- The student site must not expose instructor planning material.
