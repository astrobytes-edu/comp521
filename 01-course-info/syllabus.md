---
title: "COMP 521 Syllabus"
subtitle: "Introduction to Scientific Computing and Data Science | Fall 2026"
author: "Dr. Anna Rosen"
---

:::{warning} This syllabus is still being finalized
This version is provisional through **Thu Sep 24**. Policies, dates, and course
details may change; Canvas announcements are the authoritative record of updates.
:::

(sec-course-info)=
## Course Information

|  |  |
|---|---|
| **Instructor** | Dr. Anna Rosen |
| **Email** | <alrosen@sdsu.edu> |
| **Office** | Physics 239 |
| **Office Hours** | Thursdays 4:00–5:00 pm, Physics 239 (and by appointment) |
| **Class meetings** | Tue/Thu 5:30–6:45 pm |
| **Location** | LSN 134 |
| **Course website** | <https://astrobytes-edu.github.io/comp521> |
| **Platforms:** <br>*(where things happen)* | [Canvas](https://sdsu.instructure.com) *(announcements, gradebook)*<br>[Course website](https://astrobytes-edu.github.io/comp521) *(course materials, handouts, assignments)*<br>[Classroom50](https://github.com/foundation50/classroom50/wiki) *(project submissions)* |

:::{note} Start Here
- **Due first:** **Project 0** — get your machine and Classroom50 working — by **Thu Aug 27**, our second class meeting. **Growth Memo 1** follows on **Mon Aug 31**.
- **Read the [AI Policy](ai-policy.md) before beginning Project 1.** AI is
  optional, but you must write and be able to explain your own core solution
  code.
- **Bring your laptop to every class.** Sessions mix instruction with hands-on work — there are no separate lab days, and much of what happens in the room is not posted anywhere.
- **Cadence:** projects are posted **Tuesdays** and due **Mondays at 11:59 pm PT**. A new block's readings are for **Thursday**, not the Tuesday it is assigned. See [Important Dates](#sec-important-dates).
- **Grading is by letter, not points.** One grade for each assignment as a whole, no itemized rubrics — see [Grading](grading.md), which includes a calculator you can run.
- **You will work in rotating pairs** on Projects 1–6 while writing and submitting your own code. The final project is solo.
- **Getting help:** office hours are **Thursdays 4–5 pm, Physics 239**. Use
  Canvas Inbox for course-related messages; reserve email for genuine emergencies
  or confidential matters.
:::

### Course Description

Introduction to computational methods for scientific problem-solving and data
analysis using Python. Students implement fundamental algorithms from first
principles including numerical integrators, root-finders, optimization methods,
and Monte Carlo samplers before utilizing professional libraries. Emphasizes
software engineering practices, test-driven development, version control,
documentation, and reproducible research. Topics include data wrangling with
pandas, statistical analysis, visualization, regression methods, and performance
optimization.

**Units:** 3
**Prerequisites:** MATH 252; MATH 254 or 342A; or equivalent with instructor
permission, or graduate standing.

:::{note} Do I need to already know Python?
**No.** The course begins with Python from the ground up — environment setup,
syntax, control flow, data structures, and object-oriented programming — before
any numerical methods appear. If you have programmed before, the first two weeks
will be review and you should use them to get ahead.

What you *do* need is the mathematics. **MATH 252 is multivariable calculus**,
and this course leans on it directly: Taylor expansion is where every numerical
method in the course comes from, derivatives and gradients drive root finding and
optimization, and integrals are what quadrature approximates. Linear algebra
(MATH 254 or 342A) carries the second half — solving systems, least squares, and
everything built on them.

The algorithms here are applied calculus and linear algebra. If those are shaky,
the programming will not be your problem.
:::

### Course Materials & Technology

**There is no textbook to buy.** All readings are on the
[course website](https://astrobytes-edu.github.io/comp521) and are free.

**You need a laptop you can bring to every class.** Class sessions interleave
instruction with hands-on work, so a laptop is not optional equipment here. Any
machine running macOS, Windows, or Linux that can install Python will do — this
course is not computationally demanding, and nothing we do requires a GPU or a
large amount of memory.

Software (Python, `git`, and the scientific stack) is free, open-source, and
installed in Week 1 — see [Getting Started](../02-getting-started/index.md).

:::{note} Course throughline
**Build methods. Test their limits. Use them on real data.** The goal is
evidence-backed scientific computing: clear methods, useful tests, and claims
that survive checks.
:::

### Class Format

This course does not separate lecture days from lab days. Each 75-minute session
combines short instruction with hands-on work, and the balance shifts depending
on where we are in a project — heavier on instruction when a new method is
introduced, heavier on working time as a deadline approaches.

Bring your laptop. Much of the instruction happens through hands-on work and
discussion that responds to the class's current questions.

(sec-outcomes)=
## Student Learning Outcomes

By the end of this course, students will be able to:

1. **Build modular, testable, and reproducible scientific software in Python**
   that implements core numerical algorithms from first principles, using
   functions, modules, version control, and classes when state and invariants
   require them.

2. **Analyze and validate numerical methods** by quantifying error, convergence,
   stability, and failure modes; using analytic limits, reference solutions, and
   library comparisons to establish reliability.

3. **Acquire, clean, analyze, and visualize real scientific data** with
   defensible treatment of quality flags, missing values, units, assumptions,
   and limitations.

4. **Apply statistical inference, model fitting, uncertainty quantification, and
   introductory machine-learning methods** to evaluate scientific models and
   hypotheses.

5. **Formulate, scope, and carry out a computational investigation** by selecting
   appropriate models, data, methods, validation evidence, and tradeoffs among
   correctness, performance, and clarity.

6. **Communicate reproducible computational work professionally** through code,
   tests, documentation, figures, notebooks, and presentations; clearly stating
   methods, evidence, limitations, and meaningful collaboration or AI use.

**Where these outcomes are assessed:** Projects 1–6, the final-project proposal
pitch, the Final Project, and the Growth Reflections.

(sec-grading)=
## Grading & Assessments

| Component | Weight |
|---|-:|
| Projects (6 total; ~8.3% each) | 50% |
| Final-Project Proposal Pitch | 5% |
| Final Project | 25% |
| Growth Reflections (3 total) | 10% |
| Scholarly Engagement | 10% |

The three Growth Reflections are spaced across the semester: a **baseline**
Growth Memo in Week 1, a **mid-semester** Growth Memo, and the **Growth
Synthesis** at the start of finals week. See
[Growth Reflections](#sec-reflections).

(sec-important-dates)=
### Important Dates

Projects are assigned on **Tuesdays** and due **Mondays at 11:59 pm PT**. A Monday
deadline means you arrive at Tuesday class having submitted, rather than
finishing in the room.

| Project | Assigned | Due |
|---|---|---|
| Project 0 (Bootcamp) | Tue **Aug 25** | Thu **Aug 27** |
| Growth Memo 1 (baseline) | Tue **Aug 25** | Mon **Aug 31** |
| Project 1 — Scientific Programming & the Transit Model | Tue **Aug 25** | Tue **Sep 8** † |
| Project 2 — Numerical Integration | Tue **Sep 8** | Mon **Sep 21** |
| Project 3 — Root Finding & Stellar Inference | Tue **Sep 22** | Mon **Oct 5** |
| Project 4 — ODE Methods & Exoplanet Interiors | Tue **Oct 6** | Mon **Oct 19** |
| Project 5 — Real Data & Model Fitting | Tue **Oct 20** | Mon **Nov 2** |
| Project 6 — Machine Learning & Scientific Classification | Tue **Nov 3** | Mon **Nov 16** |
| Final-Project Proposal Pitch | Tue **Nov 17** | Thu **Nov 19**, in class |
| Final Project | Tue **Nov 17** | Thu **Dec 17**, end of day |

† **Project 1 is due Tuesday**, not Monday — Mon Sep 7 is Labor Day. It is the
only project not due on a Monday, and the extra days are deliberate: it is the
first project and the one where students are least likely to know when they are
stuck.

**End-of-semester sequence:**

| | Date | |
|---|---|---|
| Final presentation | Thu **Dec 10** | in class |
| **Growth Synthesis** | Mon **Dec 14** | 11:59 pm PT |
| **Final report + repository** | Thu **Dec 17** | end of day — our final exam date |

**University dates that affect you:**

| Date | |
|---|---|
| Tue **Aug 25** | First class meeting |
| Fri **Sep 4** | Last day to add/drop without penalty |
| Mon **Sep 7** | **Labor Day** — campus closed |
| Sun **Nov 1** | Late withdrawal deadline |
| Thu **Nov 26** | **No class** — Thanksgiving |
| Thu **Dec 10** | Last class meeting — final presentations |
| Thu **Dec 17** | Final exam date — final report due, end of day |

Week-by-week topics and readings are on the [Course Schedule](schedule.md).
Topics are listed by week rather than by day, so that class time can follow
where the class actually is.

(sec-grade-scale)=
### Grading Scale

Work in this course is graded with **letters, not points**. Each assignment
receives a single letter for the work as a whole — there are no itemized
rubrics and no point breakdowns. See [Grading](grading.md) for what each letter
means for each kind of work.

| A+ | A | A− | B+ | B | B− | C+ | C | C− | D+ | D | D− | F |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 4.3 | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0.7 | 0 |

Your grade in each component is the average of the letters earned in it; your
course grade is the weighted average of those, using the weights above. Letters
average as you would expect — an A+ and an A− come out to an A. Grades are
recorded as these numbers in Canvas.

**SDSU does not award A+ as a final grade**, so the highest course grade is an
**A**. An A+ on an assignment still counts as 4.3, which lifts your average and
can offset a weaker piece of work elsewhere.

See [Grading](grading.md) for the table converting your weighted average into a
final letter.

The instructor may curve final course grades at their discretion, and reserves
the right to adjust borderline grades upward based on effort, improvement, and
engagement.
[Click here for SDSU's explanation of grades.](https://registrar.sdsu.edu/faculty_staff/courses_grades/explanation-grades)

(sec-late)=
### Late Work & Extensions

- **One free extension per semester.** Request it at least **24 hours** before
  the deadline and you get a **2-day grace period** with no penalty, no reason
  required. You do not have to justify it — that is the point of having one.
- **No late submissions beyond that.** If you miss a deadline without having
  arranged your extension in advance, the submission is **not accepted** unless
  there is a documented emergency.
- **Your last commit before the deadline is your submission.** Commit timestamps
  are the record — not when you meant to push, and not what is sitting unpushed
  on your laptop. Push early and often.

(sec-regrades)=
### Regrade Requests

- Submit a request within **7 calendar days** of the grade release.
- Provide a $\leq$200-word written justification that argues against the
  **grade description** in [Grading](grading.md) and the assignment
  expectations — that is, make the case that the work meets a higher
  description than the one I applied.
- I will re-evaluate the **entire submission**; the grade may go **up, down, or
  remain unchanged**.

(sec-components)=
## Course Components

Per SDSU policy, students are expected to spend at least 6 hours per week (a
minimum of 2 hours per course credit hour/unit) on coursework outside of class,
including reading, project work, and preparation for class.
[Click here for SDSU's explanation of *Credit Hour or Unit*.](https://catalog.sdsu.edu/content.php?catoid=10&navoid=924#credit-hour-or-unit)

(sec-projects)=
### Projects

COMP 521 includes a setup bootcamp, six two-week projects, and a four-week solo
final project. See [Projects](projects.md) for project sequence, submissions,
and collaboration expectations.

:::{important} Every project must be submitted
**You must submit all six projects and the final project to pass this course.**
A missing project cannot be averaged away by strong work elsewhere — absent a
documented emergency, skipping one means you do not pass, whatever your other
grades look like.

:::

(sec-engagement)=
### Scholarly Engagement (10%)

Scholarly engagement means prepared participation, productive collaboration,
and visible reasoning: questions, tests, debugging, and the ability to explain
your code. You receive one engagement grade for the term as a whole.

**Classroom norms.** We are all members of a professional academic community.
Treat classmates and the instructor with respect. Spirited, courteous debate
about ideas is welcome; disrespectful behavior is not. Because active reasoning
is the point of being in the room, off-task device use during class is
distracting and will negatively affect your engagement grade.

I do not take formal attendance, but preparation, participation, and repeated
absence are reflected in this grade.

(sec-final-project)=
### Final-Project Proposal Pitch (5%)

On **Thu Nov 19**, give a five-minute in-class proposal using a short slide deck.
State your scientific question, data or source, computational approach,
validation plan, bounded minimum result, and immediate next step. Commit the
slides to your repository before class. The pitch is graded as one whole for
clarity, feasibility, and a credible plan to test the result.

### Final Project (25%)

The final project is a four-week, solo computational investigation. Choose a
bounded scientific question and use the course toolkit to produce and defend a
result. You may extend a course project, analyze a curated scientific data set,
or propose a small project from your own field. Custom projects require approval
at the proposal pitch.

Your project must:

- state a focused scientific question;
- make its data, model, methods, and assumptions explicit;
- include reproducible code and evidence that the result is trustworthy; and
- communicate the result, its limitations, and what you would investigate next.

The final-project brief will define the available project pathways and submission
format. **This project is solo.** See
[Project Pairs & Collaboration](projects.md#sec-pairs).

**Deliverables and dates:**

| Deliverable | Due |
|---|---|
| Final presentation (8 minutes + 2 minutes for questions) | Thu **Dec 10** |
| Growth Synthesis | Mon **Dec 14**, 11:59 pm PT |
| Final report (5–7 pages) + repository | Thu **Dec 17**, end of day |

The final presentation explains what you built, the evidence that it works, and
its limits. The report covers background, methods, results, and conclusions.

The final project is graded on the same description as the other projects (see
[Grading](grading.md)), applied to a larger piece of work. You should expect to
defend your design and verification choices.

(sec-reflections)=
### Growth Reflections (10% total)

Growth Reflections build **metacognition** — thinking about how you learn so you
can improve your workflow, debugging habits, and verification discipline over
time. Write them in an **informal, memo-like voice** (not an essay). Honesty and
specific evidence matter more than polished prose.

There are three:

| | Due | Purpose |
|---|---|---|
| **Growth Memo 1** | Mon **Aug 31** | **Baseline** — how you work *before* this course changes it |
| **Growth Memo 2** | Mon **Oct 19** | **Course correction** — what has changed, what has not |
| **Growth Synthesis** | Mon **Dec 14** | **Synthesis** — the whole arc |

All three are graded on honesty and specificity rather than polish or length;
see [Growth Reflections](growth-reflections.md) for the prompts.

(sec-ai-policy)=
## Academic Integrity & Generative AI Policy

All submitted work must reflect your own understanding and reasoning. AI is
optional; core solution code remains yours in every phase. Disclose meaningful
use, and do not submit work you cannot explain. Read the full
[AI Use & Growth Mindset Policy](ai-policy.md) before Project 1; its staged
rules and documentation requirements are enforced.

(sec-materials)=
## Course Materials (Sharing Policy)

Lecture notes, slides, projects, and course handouts are the intellectual
property of the instructor. You may use course materials for your own
educational purposes in this course, but you may not reproduce, distribute,
share, or post them on any public platform (e.g., Chegg, Course Hero, Discord
servers, public GitHub repos) without written permission.

Unauthorized recording or redistribution of class sessions or office hours is
prohibited.

(sec-communication)=
## Communication & Getting Help

**Use Canvas Inbox for all routine course-related messages**, including questions
about assignments, deadlines, grades, extensions, missed work, and appointments.
Use the Canvas discussion board when your question may help others. I aim to
respond to Canvas messages within **24–48 hours on weekdays**.

Do **not** send routine course questions to my SDSU email. If you do, I will
reply only to direct you to Canvas; I will not provide a separate substantive
response by email. Email is reserved for a genuine emergency or a confidential
matter that cannot appropriately be handled through Canvas.

If you encounter difficulties with the assignments or find yourself falling
behind, seek help immediately by:

- posting your questions on the course Canvas discussion page,
- speaking with me during class or office hours (preferred),
- collaborating with classmates (while ensuring your submission reflects your
  own understanding).

(sec-getting-help)=
### Getting Help (Office Hours)

Office hours are for learning — bring what you have tried (notes, attempts,
questions) and we will work from there. I will often guide you by asking
questions so you build your own problem-solving skills. You are welcome to come
even if you are not sure what to ask, or have non-course-related questions.

(sec-study-tools)=
### Study Tools (Build Your Own)

I will show you how to build a private, grounded study notebook from course
materials. It remains subject to the [AI Use & Growth Mindset Policy](ai-policy.md):
keep it private and do not use it to generate solution code.

(sec-growth-mindset)=
## Fostering a Growth Mindset

A **growth mindset** is the belief that intelligence, abilities, and talents are
malleable and can be developed through effort and persistence, not fixed traits
you are born with. This mindset is key to succeeding in this course. In COMP 521
you will encounter challenging concepts that may initially seem overwhelming.
**This is normal and expected: it means you are learning.**

*Trust the process, embrace the challenge, and discover that you are capable of
doing hard things.*

(sec-inclusion)=
## Diversity and Inclusivity Statement

I consider this classroom to be a place where you will be treated with respect,
and I welcome individuals of all ages, backgrounds, beliefs, ethnicities,
genders, gender identities, gender expressions, national origins, religious
affiliations, sexual orientations, ability, and other visible and non-visible
differences. All members of this class are expected to contribute to a
respectful, welcoming and inclusive environment for every other member of the
class.

(sec-student-info)=
## Essential Student Information

For essential information about student academic success, please see the
[SDSU Student Academic Success Handbook](https://docs.google.com/document/d/1rXNpNGs1K7nIxcS73o6R-fxZqPIWQwS9gHD7XpIqjhM/edit?tab=t.0#heading=h.apbuhr7p11ak).

SDSU provides disability-related accommodations via Student Disability Services:
<https://sds.sdsu.edu> (email: <sds@sdsu.edu>). Please allow 10–14 business days
for processing.

Class rosters are provided to the instructor with the student's legal name.
Please let me know if you prefer an alternate name and/or gender pronoun.

If you need to be absent from class for a religious observance, please notify me
in writing during the first two weeks of the semester so that we can make any
necessary arrangements.

(sec-land)=
## Land Acknowledgement

San Diego State University sits on Kumeyaay land. The Kumeyaay people have lived
in this region for over 10,000 years and continue to live here today.

(sec-responsibility)=
## Your Responsibility

This syllabus constitutes our course contract. You are responsible for reading
and understanding all policies stated here.
