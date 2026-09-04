# `.brain/` — COMP 521 planning home

Canonical home for this course's specs, design notes, and session reports, per Anna's brain-hub convention
(ADR-0024, `~/brain/work/decisions/ADR-0024-spoke-canonical-dotbrain.md`). The hub holds no copies — it
indexes this folder. Format: plain markdown + YAML frontmatter (`title`/`type`/`status`/`date`); reference hub
pages by path or URL, never MyST `#label` syntax. Sessions in this repo may write here freely; use the
brain-spoke plugin's `/spec` and `/report` commands for templates.

- `specs/`   — what to build (one file per discrete piece of work: a lecture rebuild, an assessment, a tooling change)
- `notes/`   — design/pedagogy thinking scoped to this course
- `reports/` — dated session reports and reviews (`YYYY-MM-DD-<slug>.md`), permanent

## What belongs here, and what does not

This is a **course**, not a code spoke, so the boundary needs stating explicitly:

- **Here:** lecture design rationale, adversarial-review reports, assessment design notes, decisions about
  sequencing and scaffolding, and the reasoning behind a rebuild. The things that explain *why* the course
  looks the way it does.
- **Not here — it stays canonical where it already lives:** student-facing course content (`09-lectures/`,
  the numbered content directories), course code, build artifacts, and `STATUS.md`.
- **Never here:** student PII, grades, or anything identifying an individual student. Those stay in the
  private instructor workspace and the vault. This folder is committed to the course repo's history.

The hub keeps only the cross-course view: the `proj-comp521` dashboard and anything genuinely cross-project.
Course outcomes still report to the hub through the sanctioned capture path (`brain "comp521: …"`), which is
unchanged by this folder.
