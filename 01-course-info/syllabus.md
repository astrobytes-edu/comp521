---
title: "COMP 521 Syllabus"
subtitle: "Introduction to Scientific Computing and Data Science | Fall 2026"
author: "Dr. Anna Rosen"
---

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
| **Platforms:** <br>*(where things happen)* | [Canvas](https://sdsu.instructure.com) *(announcements, gradebook, Project 1 repository link)*<br>[Course website](https://astrobytes-edu.github.io/comp521) *(course materials, handouts, assignments)*<br>[GitHub](https://github.com) *(project repositories; Classroom50 may distribute individual repositories)* |

:::{note} Start Here
- **Before class Thu Aug 27:** complete the laptop setup so that you can use
  Python and Jupyter in class.
- **Due Fri Aug 28 at 11:59 pm PT:** complete the **Project 1 GitHub Repository
  Check**. Push one setup commit; it is
  completion-only and does not assess Project 1 progress. **Growth Memo 1**
  follows on **Mon Aug 31**.
- **Read the [AI Policy](ai-policy.md) before beginning Project 1.** AI is
  optional, but you are responsible for your own code and written answers and
  must be able to explain both.
- **Bring your laptop to every class.** Sessions mix instruction with hands-on
  work. There are no separate lab days, and much of what happens in the room is
  not posted anywhere.
- **Cadence:** projects are typically posted **Tuesdays** and due
  **Wednesdays at 11:59 pm PT**. The schedule lists each specific deadline.
  Come to class prepared to discuss and use the assigned readings. See
  [Important Dates](#sec-important-dates).
- **Grading is by letter, not points.** Projects use four broad weighted letter
  categories; other assignments receive one holistic letter. See
  [Grading](grading.md) for the shared scale and calculation.
- **You will work in rotating pairs** on Projects 1–5 while writing and
  submitting your own code. The two code review presentations and final
  project are individual work.
- **Getting help:** office hours are **Thursdays 4–5 pm, Physics 239**. Use
  Canvas Inbox for course-related messages; reserve email for genuine emergencies
  or confidential matters.
:::

### Course Description

Introduction to computational methods and data science using Python. Numerical
algorithms, optimization, Monte Carlo methods, data wrangling with pandas,
exploratory data analysis, regression and classification. Emphasizes software
engineering practices including object-oriented programming, modular design,
version control, testing, and documentation.

**Units:** 3
**Prerequisites:** MATH 252; MATH 254 or 342A; or equivalent with instructor
permission, or graduate standing.

:::{note} Do I need to already know Python?
**Knowing Python is helpful, but not necessary.** We begin with the Python
foundations you will need: environment setup, syntax, control flow, data
structures, functions, and modules. If you have programmed before, the first two
weeks will be review.

What you *do* need is the mathematics. **MATH 252 is multivariable calculus**,
and this course leans on it directly: Taylor expansions underpin numerical
methods, derivatives drive root finding, and integrals are what quadrature
approximates. Linear algebra (**MATH 254 or 342A**) carries the second half:
solving systems, least squares, and everything built on them.
:::

### Course Materials & Technology

**There is no textbook to buy.** All required readings are free on the
[**course website**](https://astrobytes-edu.github.io/comp521). Readings will be
added as the semester progresses and posted at least one week before they are
due.

**You need a laptop you can bring to every class.** Class sessions interleave
instruction with hands-on work, so a laptop is not optional equipment here. Any
machine running macOS, Windows, or Linux that can install Python will do. This
course is not computationally demanding, and nothing we do requires a GPU or a
large amount of memory.

Software (Python, `git`, and the scientific stack) is free, open-source, and
installed in Week 1. See [Getting Started](../02-getting-started/getting-started.md).

:::{note} Optional: SDSU JupyterHub
Using your own computer is preferred, but the class also has access to
[SDSU JupyterHub](https://jupyterhub.sdsu.edu/). Sign in with your SDSUid. Save
your work under `/home/jovyan`, which provides 75 GiB of persistent storage, and
keep your project pushed to GitHub. Access follows the official course roster
through the schedule adjustment deadline. The server stops after your browser
has been disconnected for one hour, and changes outside `/home/jovyan`,
including many software installs, disappear when the container restarts. See the
[JupyterHub documentation](https://sdsu-research-ci.github.io/instructionalcluster/)
for login and usage instructions.
:::

:::{note} Course throughline
**Build methods. Test their limits. Use them on real data.** The goal is
evidence-backed scientific computing: clear methods, useful tests, and claims
that survive checks.
:::

### Class Format

This course does not separate lecture days from lab days. Each 75-minute session
combines short instruction with hands-on work, and the balance shifts depending
on where we are in a project: heavier on instruction when a new method is
introduced and heavier on working time as a deadline approaches.

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

**Where these outcomes are assessed:** Projects 1–5, the two Code Review
Presentations, the Final Project (including the proposal pitch), and the
Growth Reflections.

(sec-grading)=
## Grading & Assessments

| Component | Weight |
|---|-:|
| Projects 1–5 (8% each) | 40% |
| Code Review Presentations (2; 5% each) | 10% |
| Final Project (proposal pitch 5%; finished project 25%) | 30% |
| Growth Reflections (3 total) | 10% |
| Scholarly Engagement | 10% |

The three Growth Reflections are spaced across the semester: a **baseline**
Growth Memo in Week 1, a **mid-semester** Growth Memo, and the **Growth
Synthesis** at the start of finals week. See
[Growth Reflections](#sec-reflections).

(sec-important-dates)=
### Important Dates

Projects are typically assigned on **Tuesdays** and due on
**Wednesdays at 11:59 pm PT**. See the [Course Schedule](schedule.md) for each
assignment and submission date, including exceptions, and [Projects](projects.md)
for deliverables and submission expectations.

| Code review presentation | Date |
|---|---|
| Scientific computing | Thu **Oct 22**, in class |
| Data science / machine learning | Thu **Nov 12**, in class |

See [Code Review Presentations](../08-assessments/code-review-presentations.md)
for the individual presentation and submission requirements.

**End-of-semester sequence:**

| | Date | |
|---|---|---|
| Final presentation | Thu **Dec 10** | in class |
| **Growth Synthesis** | Mon **Dec 14** | 11:59 pm PT |
| **Final report + repository** | Thu **Dec 17** | 11:59 pm PT; our final exam date |

**University dates that affect you:**

| Date | |
|---|---|
| Tue **Aug 25** | First class meeting |
| Fri **Sep 4** | Last day to add/drop without penalty |
| Mon **Sep 7** | **Labor Day**; campus closed |
| Thu **Nov 26** | **No class**; Thanksgiving |
| Thu **Dec 10** | Last class meeting; final presentations |
| Thu **Dec 17** | Final exam date; final report due, 11:59 pm PT |

Week-by-week topics and readings are on the [Course Schedule](schedule.md).
Topics are listed by week rather than by day, so that class time can follow
where the class actually is.

:::{note} Course adjustments
I may adjust the sequence of topics, readings, or activities in response to class
progress or unforeseen circumstances. Changes will be announced through Canvas
and reflected on the course website. Major changes to learning outcomes, major
due dates, final presentation or report dates, or grading policies will be made
only for compelling reasons and communicated as early as possible.
:::

(sec-grade-scale)=
### Grading Scale

Work in this course is graded with **letters, not points**. Each assignment
receives a single letter for the work as a whole. There are no itemized
rubrics and no point breakdowns. See [Grading](grading.md) for what each letter
means for each kind of work.

| A+ | A | A− | B+ | B | B− | C+ | C | C− | D+ | D | D− | F |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 4.3 | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0.7 | 0 |

Your grade in each component is the average of the letters earned in it; your
course grade is the weighted average of those, using the weights above. Letters
average as you would expect: an A+ and an A− come out to an A. Grades are
recorded as these numbers in Canvas.

**SDSU does not award A+ as a final grade**, so the highest course grade is an
**A**. An A+ on an assignment still counts as 4.3, which lifts your average.

See [Grading](grading.md) for the table converting your weighted average into a
final letter.

[Click here for SDSU's explanation of grades.](https://registrar.sdsu.edu/faculty_staff/courses_grades/explanation-grades)

(sec-late)=
### Late Work & Extensions

- **One free extension per semester, for Projects 1–5 only.** Request it at least
  **24 hours** before the deadline and you get a **2-day grace period** with no
  penalty and no reason required.
- **No late submissions beyond that.** If you miss a deadline without an
  advance arrangement, the submission is **not accepted** unless there is a
  documented emergency. If you cannot give a code review presentation on its
  scheduled date, contact me promptly through Canvas Inbox to arrange an
  equivalent individual presentation and a deadline for its materials. The
  project extension does not apply to presentations.
- **For projects, your submission is the latest commit pushed to GitHub by the
  deadline.** Work that remains only on your computer has not been submitted.
  Push early and often. Code review materials are submitted through Canvas by
  the start of class on the presentation date.

(sec-regrades)=
### Regrade Requests

- Submit a request within **7 calendar days** of the grade release.
- Provide a $\leq$200-word written justification that argues against the
  **grade description** in [Grading](grading.md) and the assignment
  expectations. Make the case that the work meets a higher
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

COMP 521 includes a required repository check at the start of Project 1,
five two-week projects, two individual code review presentations, and a
four-week solo final project. See
[Projects](projects.md) for the checkpoint, project sequence, submissions, and
collaboration expectations.

### Code Review Presentations (10% total)

Choose one open source computational science/scientific computing package and,
later in the semester, a different data science or machine-learning package.
Present a brief map of each package's architecture, then examine one code path,
teach a small example, and explain what a focused check supports. Each
individual presentation counts for 5%. See the
[assessment brief](../08-assessments/code-review-presentations.md) for the dates,
submission route, grading, and assignment-specific AI rules.

(sec-engagement)=
### Scholarly Engagement (10%)

Scholarly engagement means prepared participation, productive collaboration,
and visible reasoning: questions, tests, debugging, and the ability to explain
your code. You can demonstrate it through discussion, written reasoning, pair
work, and project check-ins; frequent speaking is not required. You receive one
engagement grade for the term as a whole.

**Classroom norms.** We are all members of a professional academic community.
Treat classmates and the instructor with respect. Spirited, courteous debate
about ideas is welcome; disrespectful behavior is not. Because active reasoning
is the point of being in the room, off-task device use during class is
distracting and will negatively affect your engagement grade.

Attendance itself is not graded. However, excessive absences will affect
Scholarly Engagement because they limit prepared participation, collaboration,
substantive check-ins, and other visible engagement with the course.

(sec-final-project)=
### Final Project (30% total)

The final project counts for 30% of your grade: 5% for the proposal pitch and
25% for the finished project.

| Component | Weight | Due |
|---|---:|---|
| Proposal pitch | 5% | Thu **Nov 19**, in class |
| Finished project: presentation, report, and code | 25% | Presentation: Thu **Dec 10**<br>Report + repository: Thu **Dec 17**, 11:59 pm PT |

The presentation, report, and repository receive one holistic final-project
grade.

For the proposal pitch, give a five-minute presentation using a short slide
deck. State your scientific question, data or source, computational approach,
validation plan, bounded minimum result, and immediate next step. Commit the
slides to your repository before class. The pitch is graded for clarity,
feasibility, and a credible plan to test the result.

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

The final presentation is eight minutes, followed by two minutes for questions.
Explain what you built, the evidence that it works, and its limits. The report is
5–7 pages and covers the background, methods, results, and conclusions.

The final project is graded on the same description as the other projects (see
[Grading](grading.md)), applied to a larger piece of work. You should expect to
defend your design and verification choices.

(sec-reflections)=
### Growth Reflections (10% total)

Growth Reflections build **metacognition**, or thinking about how you learn so you
can improve your workflow, debugging habits, and verification discipline over
time. Write them in an **informal, memo-like voice** (not an essay). Honesty and
specific evidence matter more than polished prose.

There are three:

| | Assigned | Due | Purpose |
|---|---|---|---|
| **Growth Memo 1** | Tue **Aug 25** | Mon **Aug 31**, 11:59 pm PT | **Baseline:** how you work *before* this course changes it |
| **Growth Memo 2** | Tue **Oct 6** | Mon **Oct 19**, 11:59 pm PT | **Course correction:** what has changed, what has not |
| **Growth Synthesis** | Tue **Nov 17** | Mon **Dec 14**, 11:59 pm PT | **Synthesis:** the whole arc |

Growth Memos 1 and 2 should each be **1–2 pages**, with a minimum of one full
page. The Growth Synthesis should be **2–3 pages**, with a minimum of two full
pages. All three are graded on specificity, reflection, and evidence rather than
polished prose; see [Growth Reflections](growth-reflections.md) for the prompts.

Submit each reflection through the corresponding **Canvas assignment** as a
**single-spaced PDF** using a readable **12-point font** and **1-inch margins**.

(sec-ai-policy)=
## Generative AI: Student and Instructor Use

### Student use

All submitted work must reflect your own understanding and reasoning. AI is
optional; you are responsible for the code and written answers you submit and
must be able to explain both. Core solution code remains yours in every phase.
Disclose meaningful use. Read the full
[AI Use & Growth Mindset Policy](ai-policy.md) before Project 1; its staged
permissions and documentation requirements are enforced. The
[Code Review Presentations](../08-assessments/code-review-presentations.md#ai-use-for-this-assessment)
have additional rules for package discovery and student-authored explanations.

### How I use generative AI

I use generative AI as a drafting, technical, and pedagogical assistant when
developing readings, projects, examples, code, and website text. I direct and
review the process, verify claims and code, and personally vet all course
materials.

**Use in grading:** I use my SDSU ChatGPT Edu account to assist with holistic
review of submitted code. I independently verify its output and determine every
final grade. It does not make academic-integrity decisions. You may challenge a
grade through [Regrade Requests](#sec-regrades).

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

Office hours are for learning. Bring what you have tried (notes, attempts,
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

SDSU provides disability-related accommodations through the
[Student Ability Success Center](https://sdsu.edu/sasc) (SASC). Contact
<sascinfo@sdsu.edu> as early as possible. Accommodations are not retroactive and
begin after I receive an authorized accommodation letter. Approval may take
10–14 business days.

Class rosters are provided to the instructor with the student's legal name.
Please let me know if you prefer an alternate name and/or gender pronoun.

If you need to be absent from class for a religious observance, please notify me
in writing during the first two weeks of the semester so that we can make any
necessary arrangements.

(sec-land)=
## Land Acknowledgement

San Diego State University sits on Kumeyaay land. The Kumeyaay people have lived
in this region for over 10,000 years and continue to live here today.
