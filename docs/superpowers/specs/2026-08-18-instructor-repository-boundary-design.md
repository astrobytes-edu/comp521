# COMP 521 instructor-repository boundary design

## Decision

Keep one working directory, `/Users/anna/Teaching/comp521`, while separating
instructor-only material into a local-only nested repository at
`_instructor/`. The outer `comp521` repository remains the student-facing
course repository and retains its GitHub remote.

The exact directory layout after migration is:

```text
comp521/
├── _instructor/              # independent local Git repo; no remote
│   ├── course-outline.md
│   ├── projects/
│   ├── solutions/
│   ├── grading-harness/
│   ├── papers/
│   └── myst.yml
├── 01-course-info/           # student-facing
├── docs/
└── myst.yml                  # student-facing MyST project
```

`_instructor/` is ignored by the outer repository. It is neither a Git
submodule nor a dependency of the public MyST site.

## Current safety facts

- `astrobytes-edu/comp521` is currently **private** on GitHub, verified on
  2026-08-18. Its visibility will not be changed by this migration.
- The local `main` branch is ahead of `origin/main`; the planning material is
  not present in `origin/main` from this checkout.
- Fifty-seven local commits touch `planning/`. A future ordinary push of the
  current branch would therefore expose their snapshots to every authorized
  reader of the outer repository.

## Migration design

1. Create and verify a local recovery bundle outside the outer working tree.
2. Split the existing `planning/` history into an independent local Git
   history, then materialize it at `_instructor/`. This preserves the
   instructor work's meaningful commit history. Locally stored, ignored source
   PDFs move with the working tree but remain ignored within `_instructor/`.
3. Use `git filter-repo --path planning --invert-paths` on the outer
   repository's unpushed history, so `planning/` is absent from every commit
   reachable from the public `main` branch. Preserve every other commit rather
   than replacing the branch with a single squash commit.
4. Restore the outer `origin` configuration if the history-filtering tool
   removes it. Do not push, alter GitHub visibility, or create a remote for
   `_instructor/`.
5. Add `_instructor/` to the outer `.gitignore`, move the planning-specific
   ignore rules into `_instructor/.gitignore`, and revise the public README's
   stale `_planning/` entry to describe the local instructor workspace without
   linking it into the public build.

## Invariants and verification

After the migration:

- `git -C _instructor remote -v` has no output; its history and working tree
  are intact.
- `git ls-files _instructor` in the outer repository has no output, and
  `_instructor/` is ignored by the outer `.gitignore`.
- `git log origin/main..HEAD -- planning` has no output, so no unpushed public
  commit retains instructor files under their former path.
- The outer MyST table of contents has no `_instructor/` reference, and its
  student-facing build configuration remains independent of the instructor
  site.
- `origin` still points to `https://github.com/astrobytes-edu/comp521.git`,
  and GitHub visibility remains private. No push is part of this migration.

## Scope boundary

This migration does not modify syllabus content, policies, assignments, or
student-facing materials beyond the root README's repository-layout note. A
separate approved pass will audit and finalize the syllabus, schedule, grading,
and AI-policy pages.
