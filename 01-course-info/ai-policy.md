---
title: "AI Use & Growth Mindset Policy"
subtitle: "COMP 521: Introduction to Scientific Computing and Data Science | Fall 2026"
author: "Dr. Anna Rosen"
---

This document explains how artificial intelligence (AI) fits into **COMP 521: Introduction to Scientific Computing and Data Science**. It is intentionally separate from the syllabus so it can be read carefully, revisited, and treated as a shared agreement about *how learning happens in this course*.

I’m going to be transparent up front:

> **This course is about learning how to think computationally and analyze real scientific data.**
> **AI is optional.** **Struggle is expected.** **Understanding is the point.**

We’re living in a moment where “vibe coding” (prompt $\to$ code $\to$ it runs) is popular and sometimes genuinely productive. But it also has severe limitations: it can generate code that runs while being fragile, inefficient, or conceptually wrong.

I don’t pretend to know exactly what the future of AI-assisted coding looks like in scientific research. But I do know this: if you want to benefit from these tools (now or later), you need higher-level skills—judgment, verification, debugging instincts, and adaptability. This policy exists to protect the time you need to develop those skills.

---

## Non‑Negotiables (Read These First)

1. **AI is optional.** You can earn full credit without using AI at all.
2. **You are responsible for your code and written answers.** You must understand
   and be able to explain everything you submit.
3. **No AI refactoring / restructuring.** If AI changes the structure of your solution, your work is no longer assessable.
4. **No AI-written “core solution” code.** AI may support learning and presentation (in later phases), but the algorithmic logic must remain yours.
5. **Disclosure is required.** Meaningful AI use must be documented.

If you’re unsure whether something is allowed, ask **before** submitting.

---

## Why This Policy Exists

Scientific computing is not about typing the right thing into Python and getting a plot that looks reasonable. It’s about building intuition:

- what algorithms are actually doing,
- how numerical methods fail,
- how bugs sneak in,
- how plots can mislead you,
- and how small choices propagate into big consequences.

Those skills only develop if you spend time *inside the confusion*. Reading documentation, trying things that don’t work, and debugging code you wrote yourself are not obstacles—they are the learning process.

Used too early, AI replaces that process with something that looks like competence but isn’t. This policy is designed to protect the time you need to build real understanding first.

---

## Growth Mindset (How I Expect You to Learn)

Struggle is normal. Feeling slow is normal. Being confused at first is normal.

If something feels hard, that does **not** mean you’re bad at this—it usually means you’re doing exactly what you should be doing.

### The Struggle‑First Protocol (Before AI)

Before turning to AI, you are expected to do **all** of the following:

1. **Try first.** Make a real attempt. Write *something*.
2. **Docs next.** Read the relevant documentation (or docstring / API reference).
3. **Experiment.** Change one thing at a time. Build a minimal reproducible example.
4. **Hypothesize.** Write down what you think is wrong before you ask a tool.

#### 20–30 minutes of productive struggle (use judgment)

In this course, “struggle first” usually means **~20–30 minutes** of genuine effort *before* asking an AI tool for help with coding work. The goal is productive struggle, not watching the clock.

Use judgment based on what kind of stuck you are:

- **Simple syntax/typo errors:** 5–10 minutes is enough.
- **Conceptual confusion:** 15–30 minutes builds understanding.
- **Complex algorithmic/numerical issues:** up to ~45 minutes if you’re making progress.
- **Environment/installation issues:** ~10 minutes, then seek help (these can waste hours).

If you’re genuinely stuck with no new ideas after ~20 minutes, that counts as productive struggle. Document what you tried and then ask a *focused* question.

AI should come **after** effort, not instead of it.

When you do use AI, treat it like you’d treat Google / Stack Overflow / a colleague:

- useful for clarification,
- good for a second perspective,
- not a substitute for doing the work.

The goal here is not speed. The goal is durable understanding.

---

## Definitions (So There’s No Ambiguity)

- **AI tool:** any system that generates or transforms text/code (e.g., ChatGPT, Claude, Gemini, Copilot/Cursor-style code assistants, NotebookLM, etc.).
- **Core solution code:** code that implements the main algorithmic logic of an assignment/project (model equations, numerical methods, data pipeline logic that determines results, simulation loop, inference workflow, etc.).
- **Refactoring / restructuring:** changing the structure of a solution (function boundaries, class design, algorithm decomposition, control flow, vectorization rewrites, architectural reorganization, renaming that changes meaning, etc.).
- **Tutoring:** explanations, conceptual guidance, interpreting errors, clarifying docs, suggesting tests, helping you reason—without writing or restructuring your core solution.

---

## AI Is Optional

You are **not required** to use AI in this course.

You can complete every assignment, project, and the final without AI and still earn full credit. This is not an AI class. The learning objectives do not depend on AI.

This policy exists to guide responsible use *if* you choose to use AI—not to push you toward it.

---

## The “Traffic Light” Rules (How to Use AI Without Losing the Learning)

### Use AI as a Socratic tutor (copy/paste prompt)

If you use an AI tool, start the conversation by telling it to help you learn rather than generate solutions. For example:

> Act as a Socratic tutor for scientific computing. Don’t give me direct solutions or write my core code. Instead, guide me with questions. When I’m stuck, give hints, not answers. Help me build intuition by asking what I think should happen physically/mathematically and how I would test it. If I ask for an explanation, first ask what I already understand and what specifically confuses me.

### Green (Encouraged: tutoring + verification)

Use AI to increase understanding and rigor:

- explaining an error message *and likely causes*,
- helping interpret documentation you already tried to read,
- clarifying a concept (“what does stability mean here?”),
- proposing tests, edge cases, and sanity checks,
- critiquing your explanation (“what’s unclear or missing?”),
- generating a verification checklist (“how would you validate this model?”).

### Yellow (Allowed with constraints: you remain the author)

Use AI for support that improves communication or workflow, **after** you have baseline competence:

- drafting/polishing docstrings or comments **after you wrote a first pass**,
- plot formatting **after you can already produce the plot yourself**,
- git reminders and commit message drafts (you still decide what the commit does),
- small, minimal API examples to learn a library pattern (you must be able to explain and adapt it).

### Red (Not allowed)

These uses undermine learning and/or fairness:

- AI-written first-draft solutions for **core solution code**,
- AI choosing the algorithm/design and you implementing it without independent understanding,
- **any AI refactoring/restructuring** that changes the shape of your solution (even if the output “looks nicer”),
- using AI during a **live explainability check** — when I ask you to walk
  through your code, modify it on the spot, or defend a design choice (including
  final-project presentation questions). These are oral, and they are the point
  at which "can you explain it" stops being rhetorical.

### Examples: good vs. bad AI requests

**Debugging (all phases, after struggle):**

- ✅ Good: “I’m getting an `IndexError` in this loop. I checked shapes and bounds, and the error happens when `i == n`. What are the most likely causes, and what minimal checks should I run next?”
- ❌ Not good: “Fix this” + paste your entire project.

**Concept understanding (always allowed):**

- ✅ Good: “I know Euler accumulates error, but I don’t see why RK methods do better. Can you guide me through the intuition and what I should look for in a Taylor expansion?”
- ❌ Not good: “Explain RK4” (too vague; no targeted confusion).

**Optimization (Phase 2–3 only, with a working baseline):**

- ✅ Good: “My code works, but force calculation is slow. Here’s the specific function and what I’ve tried. What optimization strategies should I consider, and how can I verify I didn’t change the physics?”
- ❌ Not good: “Make it faster” (no context; invites random rewrites).

### The Cognitive Ownership Principle

After consulting AI, **close it and re‑implement the idea from your own understanding**. Don’t paste generated code into your project and hope. If you can’t write (and explain) the key parts yourself, you don’t understand it yet—and you shouldn’t submit it.

---

## The Three‑Phase AI Policy

AI permissions change over the semester to match where you should be cognitively at that point. These phases apply to everyone. There are **no early opt‑ins**.

Phase transitions are tied to project blocks, not to calendar convenience:

| Phase | Projects | Weeks | Dates (Fall 2026) |
|:--|:--|:--|:--|
| **Phase 1** — Skill Formation | Projects 1–3 | 1–6 | Aug 25 – Oct 5 |
| **Phase 2** — Assisted Fluency | Projects 4–6 | 7–12 | Oct 6 – Nov 16 |
| **Phase 3** — Supervised Tool Use | Final Project | 13–16 | Nov 17 – Dec 10 |

:::{danger} What the phases do *not* change
**You write your own core solution code in every phase of this course. That
never loosens.**

The phases govern what happens *around* your code — documentation, plot
formatting, git workflow, test scaffolding. They never authorize AI to write the
algorithmic logic that produces your results. There is no point in the semester
at which it becomes acceptable to have AI implement your integrator, your root
finder, your ODE solver, or your classifier.

If you reach the final project expecting the restrictions to lift, re-read this
box.
:::

:::{important} COMP 521 is where the habits form
This is an introductory course, and that makes Phase 1 matter *more*, not less —
which is why it covers the first three projects, nearly half the semester.

The algorithms you implement early — loops, accumulation, a trapezoid rule — are
exactly the ones an AI can produce instantly and perfectly. That is precisely
why you have to write them yourself. If you outsource the easy algorithms, you
will have no basis for judging the hard ones in November, or in COMP 536, or at
work. You cannot supervise a tool whose job you have never done.
:::

### Phase 1 — Skill Formation (Projects 1–3 · Weeks 1–6)

**What this phase is about:** building basic coding skills, computational intuition, and comfort with documentation, errors, and debugging.

This is nearly half the semester, and that is deliberate.

This is the phase where automation is most harmful to learning.

**AI may be used for (tutoring only):**

- conceptual clarification (e.g., “what does this error mean?”),
- help interpreting documentation you have already tried to read,
- high-level questions like “what tests should I run?” or “why might this approach fail?”.

**AI may NOT be used for:**

- writing any core solution code,
- refactoring/restructuring any code,
- generating plots for assignments,
- writing docstrings/comments,
- automating git workflows.

### Phase 2 — Assisted Fluency (Projects 4–6 · Weeks 7–12)

**What this phase is about:** becoming more efficient *after* you’ve built foundations.

By this point, you should have written many docstrings, made plots from scratch, read plotting documentation, and used git directly.

**AI may be used for:**

- tutoring (as in Phase 1),
- drafting or polishing docstrings/comments **after you have written many on your own**,
- plot formatting and visualization details **after you can already produce the plot yourself**,
- writing git commit messages or reminding you of git commands.

**AI may NOT be used for:**

- refactoring/restructuring code,
- writing or rewriting core solution code,
- transforming code in ways that make it unclear what you wrote.

AI can help with presentation and efficiency—but **structure and logic must remain yours**.

### Phase 3 — Supervised Tool Use (Final Project · Weeks 13–16)

**What this phase is about:** using tools the way a competent researcher does—under your own supervision, with verification you can defend.

This phase applies **only to the final project**, and only because by this point you have implemented six projects' worth of algorithms yourself. The final project largely extends code *you already wrote*.

AI may be used for productivity, including:

- documentation,
- plot templates,
- test scaffolds,
- exploring alternative approaches *conceptually*.

However, **AI‑driven refactoring/restructuring of core code remains prohibited**, unless explicitly assigned.

You must be able to:

- explain every major design decision,
- modify your own code without AI assistance,
- clearly defend your modeling choices.

If you cannot explain it, you should not submit it.

---

## Documentation Requirements (Strict)

If AI meaningfully contributes to your work, you must include an **AI Use Log** (brief, but specific) with your submission.

Your log must include:

- **Tool** used (name) and whether it was a chat assistant / code assistant,
- **Purpose** (tutoring? docstring polish? plot formatting? git help?),
- **What you asked** (short prompt summary or key prompts),
- **What you changed** in your work as a result,
- **How you verified** correctness (tests, sanity checks, limit cases, comparisons, docs, etc.).

If you did not use AI, you do not need to submit a log.

### In‑code attribution option (recommended for AI‑influenced code)

When AI influences a specific code block or function, add a short note directly above it (and refer to it in your AI Use Log):

```python
# AI: [Tool] suggested [very short what]
# Verified: [what you checked: docs/tests/limit case/sanity check]
# Because: [why you accepted it / what you changed]
```

### AI Use Log Template

```markdown
### AI Use Log
- Tool(s):
- Purpose:
- What I did before AI (Struggle‑First Protocol):
- Key prompt(s) / summary:
- What changed in my work:
- Verification performed:
```

---

## When in Doubt (Get Help)

If you’re uncertain about what’s allowed, or you’re stuck in a way that isn’t productive:

- Ask in class or during office hours (see the syllabus).
- Talk with classmates and compare debugging hypotheses (two brains often beat one model).
- If it’s urgent, send me a Canvas message with a short description of what you
  tried and what you think is happening.

**Stuck outside office hours:** if it’s late and you’re genuinely blocked after **~45+ minutes** of documented effort, you may use AI *minimally* to get unstuck (e.g., interpret an error, suggest tests). You still may not generate core solution code or refactor/restructure your solution. Bring the issue to office hours or class afterward so we can make sure the understanding is solid.

---

## Should I Use AI for This? Quick Decision Flow

```{mermaid}
flowchart TD
  Start[I need help] --> Q0{Live explainability check\nor presentation Q&A?}
  Q0 -->|Yes| Stop1[No AI. Answer from your own understanding]
  Q0 -->|No| Q1{Conceptual question?}
  Q1 -->|Yes| Green1[Use AI as a Socratic tutor\nAsk focused questions]
  Q1 -->|No| Q2{Coding/debugging?}
  Q2 -->|No| Green2[Use course materials\nAsk instructor/peers]
  Q2 -->|Yes| Q3{Tried 20–30 min + docs?\nMinimal repro / hypothesis?}
  Q3 -->|No| Struggle[Do Struggle‑First Protocol\nthen reconsider]
  Q3 -->|Yes| Q4{Is this asking for core solution code\nor restructuring/refactoring?}
  Q4 -->|Yes| Stop2[Not allowed\nAsk for hints/tests instead]
  Q4 -->|No| Go[OK to ask AI for debugging guidance\nDocument + verify]
```

## Ownership & Explainability Checks

Because AI can create plausible output quickly, this course emphasizes *explainability*.

At any time, you may be asked to:

- walk through your code,
- explain why a particular approach works or fails,
- modify your code without AI assistance,
- justify design choices and tests.

This is not meant to be punitive—it’s how we make sure learning is actually happening.

---

## Academic Integrity & Enforcement (Strict)

- **Undisclosed AI use** on any meaningful part of an assignment is an integrity violation.
- **Prohibited AI use** (core solution code generation, refactoring/restructuring, etc.) is an integrity violation.

Consequences may include (depending on severity):

- a **zero** on the affected portion or assignment,
- a required meeting and/or oral explainability check,
- resubmission with a penalty at instructor discretion,
- and/or referral under university academic integrity procedures.

If you are unsure whether something is allowed, ask **before** submitting.

---

## Equity, Access, and Privacy

- You are not required to use paid AI tools.
- Do not paste private data, sensitive information, or unpublished research into third‑party tools.
- Do not paste other students’ work into AI tools.
- If you choose to use AI, you are responsible for verifying correctness and meeting the same learning expectations.

---

## Final Thoughts

Scientists use powerful tools effectively *because* they understand what correct behavior looks like.

This course is about building that understanding.

You are expected to struggle first, build fluency second, and only then lean on automation. That progression is not a punishment—it’s how real expertise forms.
