---
title: "COMP 521 Syllabus"
subtitle: "Introduction to Scientific Computing and Data Science | Fall 2026"
author: "Dr. Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This page is still being prepared
COMP 521 begins **Tuesday, August 25**. This page is being written and revised
until then — dates, policies, and details may still change. It is published
early so you can see the shape of the course, not because it is finished.

Anything still under discussion is settled by **Monday, August 24**. After that,
what is written here is what the course does.
:::
<!-- prep-banner:end -->

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
- **Read the [AI Policy](ai-policy.md).** It is probably stricter than you expect, and what is allowed changes as the semester goes on.
- **Bring your laptop to every class.** Sessions mix instruction with hands-on work — there are no separate lab days, and much of what happens in the room is not posted anywhere.
- **Cadence:** projects are posted **Tuesdays** and due **Mondays at 11:59 pm PT**. A new block's readings are for **Thursday**, not the Tuesday it is assigned. See [Important Dates](#sec-important-dates).
- **Grading is by letter, not points.** One grade for each assignment as a whole, no itemized rubrics — see [Grading](grading.md), which includes a calculator you can run.
- **You will work in rotating pairs** on Projects 1–6 (writing your own code), and **teach the class twice** — see [SE Presentations](../assignments/se-presentation.md).
- **Getting help:** office hours **Thursdays 4–5 pm, Physics 239**. Before emailing, check this syllabus and recent Canvas announcements.
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

:::{note} Core Course Throughline
> Build algorithms from scratch, then leverage libraries for real data.

There are two ways to learn scientific computing. One is to learn which library
function to call. The other is to understand what that function does, so you can
recognize when it is lying to you. This course takes the second path, then hands
you the libraries once you have earned them.

The goal is not "making code run." The goal is durable skill: designing
algorithms, debugging methodically, checking limits and invariants, and making
claims only when you have evidence.
:::

### Class Format

This course does not separate lecture days from lab days. Each 75-minute session
combines short instruction with hands-on work, and the balance shifts depending
on where we are in a project — heavier on instruction when a new method is
introduced, heavier on working time as a deadline approaches.

**This means class attendance matters more than in a lecture course.** Much of
the instruction happens in response to what you are actually stuck on, and that
does not get posted anywhere afterward.

(sec-outcomes)=
## Student Learning Outcomes

By the end of this course, students will be able to:

1. **Implement core numerical algorithms in Python from first principles** —
   including numerical integration, root finding, ODE solvers, linear solvers,
   and basic machine learning — using modular design, clear function interfaces,
   and object-oriented programming where appropriate.

2. **Analyze the error, stability, and convergence behavior** of a numerical
   method, predict where it will fail, and verify that an implementation
   achieves its theoretically expected order of accuracy.

3. **Acquire, clean, and validate real scientific datasets**, handling missing
   values, quality flags, and outliers with defensible, documented choices.

4. **Apply statistical methods** to assess model fits, test hypotheses, and
   quantify uncertainty in derived results.

5. **Visualize data and results** using the scientific Python ecosystem
   (`NumPy`, `SciPy`, `pandas`, `matplotlib`), producing figures that make
   assumptions, units, and failure modes visible.

6. **Compare your own implementations against professional libraries**, and make
   defensible tradeoffs between correctness, stability, performance, and clarity.

7. **Practice reproducible research** — version control with `git`, testing,
   documentation, and environment management — so that your results can be
   regenerated by someone else.

8. **Communicate computational work professionally** through code
   documentation, READMEs, and concise research-style writing, clearly
   explaining design decisions, verification evidence, and limitations.

9. **Use AI tools responsibly and transparently** (per course policy): as a
   tutor and verification assistant, not a solution engine; documenting
   meaningful use and independently verifying outputs so that submissions
   reflect your own understanding.

**Where these outcomes are assessed:** Projects 1–6, the Final Project, the
Software Engineering Presentations, and the Growth Reflections.

(sec-grading)=
## Grading & Assessments

| Component | Weight |
|---|-:|
| Projects (6 total; ~8.3% each) | 50% |
| Final Project | 20% |
| SE Presentations (2 total; 5% each) | 10% |
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
| Final Project | Tue **Nov 17** | Thu **Dec 17**, end of day |

† **Project 1 is due Tuesday**, not Monday — Mon Sep 7 is Labor Day. It is the
only project not due on a Monday, and the extra days are deliberate: it is the
first project and the one where students are least likely to know when they are
stuck.

**End-of-semester sequence:**

| | Date | |
|---|---|---|
| Final presentations | Thu **Dec 10** | in class |
| **Growth Synthesis** | Mon **Dec 14** | 11:59 pm PT |
| **Final report + repository** | Thu **Dec 17** | end of day — our final exam date |

The Growth Synthesis is due **before** the report on purpose. If both were due
the same day, the reflection would get written in the last hour and be worth
nothing to you. Submitting it after your presentation and before your final push
means writing it while the semester is genuinely in view.

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
### Projects Overview

Projects are the core of COMP 521. The goal is not "getting code to run once" —
it is learning how to design, debug, verify, and explain computation you
actually understand. In an era where AI can generate plausible-looking code
quickly, the bar has shifted: what matters is judgment — correctness,
verification, and scientific reasoning — not typing speed.

**Structure:** a one-week bootcamp (Project 0), six two-week projects, then a
four-week final project.

:::{important} Every project must be submitted
**You must submit all six projects and the final project to pass this course.**
A missing project cannot be averaged away by strong work elsewhere — absent a
documented emergency, skipping one means you do not pass, whatever your other
grades look like.

This exists because the projects *are* the course. Six two-week projects is not
a set of assignments you can sample; it is the sequence the whole thing is built
on, and each one assumes the last.
:::

Each two-week project runs in two halves:

- **Week A** — theory, implementation, validation against known results
- **Week B** — application to real data, comparison with library implementations

(sec-project-zero)=
#### Project 0 — Setup Bootcamp (ungraded, required)

Due **Thu Aug 27** — our second class meeting. Project 0 is not about Python;
it is about making sure the machinery works before any real work depends on it.
You will:

- install and verify your Python environment,
- get comfortable enough at the command line to navigate and run things,
- set up `git` and GitHub,
- join the course on **Classroom50** and push a first commit through it,
- confirm your submission actually arrived.

Work through [Getting Started](../02-getting-started/index.md) alongside it.

It is **graded on completion only** and does not count toward your project
average — but it is genuinely required, and the deadline is early on purpose.
By Thursday of Week 1 you need to be able to work: if your environment is broken
on the day we start writing code, you lose that session and the next. Environment
and submission problems are the single most common reason students fall behind
in the first weeks, and this is how we prevent that.

If you get stuck on setup, come to office hours or tell me before Thursday.
Being stuck is expected; being quietly stuck is the problem.

(sec-thread)=
#### The thread running through the projects

Rather than six disconnected assignments, the projects build one continuous
scientific investigation — detecting and characterizing exoplanets in real
Kepler data:

| Project | Contribution to the investigation |
|---|---|
| 1 | Build and validate a transit model; place 15 real stars on a theoretical HR diagram |
| 2 | Integrate a limb-darkened transit model and derive the Stefan–Boltzmann constant |
| 3 | Solve orbital and transit-contact problems; infer habitable zones for those 15 stars |
| 4 | Build exoplanet interiors and test mass–radius relations against Seager et al. |
| 5 | Download, clean, and fit a transit model to real Kepler photometry |
| 6 | Classify a Gaia stellar sample with machine-learning methods |
| Final | Assemble the complete discovery pipeline |

(sec-submissions)=
#### What a project submission includes

- a code repository with a runnable workflow (README + reproduction instructions),
- verification evidence (tests, sanity checks, convergence diagnostics),
- an **analysis notebook** that runs top to bottom and ends with a written
  **Discussion**,
- a **Growth Memo** with Project 4 only (see [Growth Reflections](#sec-reflections)).

**The notebook is the report.** There is no separate document to write. Your
Jupyter notebook is the thing I read: it contains your analysis, your figures,
and your argument, in the order a reader needs them. From Project 2 onward your
code lives in `.py` modules and the notebook imports them, so the notebook is
narrative and results rather than a wall of implementation.

**Every notebook must end with a section titled `Discussion`.** Prose only — no
code cells in it. This is where you answer the project's questions and say what
your results mean. Roughly 500–800 words; Project 1's is shorter.

:::{important} Run it top to bottom before you submit
**Kernel → Restart Kernel and Run All Cells**, every time, before your final
commit. A notebook whose stored output was produced by code you have since
changed is worse than one that fails outright, because it looks fine.

I re-execute submitted notebooks. If yours does not run from a clean kernel, it
does not count as running.
:::

:::{note} Why a notebook and not a PDF report
Because your claims and the evidence for them belong on the same page. A report
can describe results the code does not produce; a notebook that re-executes
cannot. It also means one artifact instead of two, and no exporting.

The exception is the **final project**, which requires a standalone written
report. Writing for a reader who will not run your code is a genuinely different
skill, and by December you will have had a semester of practice at the
argument-making part.
:::

(sec-pairs)=
### Project Pairs & Collaboration

**Projects 1–6 are done in pairs**, and **pairs rotate each project** so that
over the semester you work with everyone in the class. Pair work is how
computational science actually happens, and rotating partners means you see more
than one way of approaching a problem.

**The final project is solo.** It is the capstone, it is where you demonstrate
individual command of the whole toolkit, and the three options push people
toward different datasets and questions anyway. You may still talk through
design and debug with classmates — the collaboration rules below continue to
apply — but the work and the submission are yours alone.

:::{important} You are responsible for your own code
Working in a pair does **not** mean submitting shared work. **Each student
writes, submits, and must be able to explain their own implementation.**

- **Encouraged:** designing algorithms together, whiteboarding equations,
  debugging side by side, comparing strategies, sharing **tests you wrote**.
- **Not allowed:** sharing or copying solution code — even from your partner,
  even when you worked out the approach together.
- **Required:** credit your partner and describe what you worked on together in
  your project `README.md`.
:::

**On the natural convergence of paired work.** If you and your partner spend
forty minutes at a whiteboard designing an algorithm, your implementations will
end up structurally similar — same decomposition, similar names, comparable
logic. That is what collaboration produces, and it is not a violation. The line
that matters is whether **you** typed it and whether **you** can explain it. I
will ask.

If a pairing is not working, tell me and I will re-pair you. Do not suffer
through it silently.

(sec-se-presentations)=
### Software Engineering Presentations (10% total; 2 × 5%)

Twice during the semester you teach the class a software engineering tool or
practice — not by talking at us, but by walking the room through it while
everyone follows along on their own laptop. You publish a GitHub repository,
everyone clones it beforehand, and you lead a 12-minute hands-on walkthrough
with 3 minutes of questions. No slides.

When someone else is presenting, cloning and setting up their repository before
class is part of your Scholarly Engagement.

The goal is that your classmates can use the tool afterward. Topics range across
testing, code quality, debugging, performance, and reproducibility; you present
two different ones, in two rounds.

Full details, the topic list, and what each grade means are on the
[Software Engineering Presentation](../assignments/se-presentation.md) page.

(sec-engagement)=
### Scholarly Engagement (10%)

This is a small class, and it runs closer to a research group meeting than a
lecture course. Scholarly engagement means showing up prepared and making your
thinking *visible*: asking questions, contributing to discussion, debugging
systematically, verifying results, and being able to explain your code. It also
means arriving at a classmate's presentation with their repository already
cloned and working, and coming to check-ins with something to show.

In a class this size everyone's participation is load-bearing — if two people
disengage, the discussion stops working for everyone.

You receive **one engagement grade at the end of the semester** for the term as
a whole. See [Grading](grading.md) for what each letter means. Thinking out loud
and thinking quietly both count, as long as your reasoning becomes visible
somewhere.

**Classroom norms.** We are all members of a professional academic community.
Treat classmates and the instructor with respect. Spirited, courteous debate
about ideas is welcome; disrespectful behavior is not. Because active reasoning
is the point of being in the room, off-task device use during class is
distracting and will negatively affect your engagement grade.

I will not take formal attendance, but in a class of this size I will absolutely
notice. Because instruction is interleaved with working time, missing class
means missing material that is not posted anywhere. Please arrive on time.

(sec-final-project)=
### Final Project (20%)

The final project synthesizes the course into a complete data science pipeline.
You will choose one of:

1. **Exoplanet discovery pipeline** — apply your full toolkit to unseen Kepler
   data, with statistical validation of candidates.
2. **Custom scientific data analysis** — a dataset from your own field, using
   numerical methods plus machine learning.
3. **Algorithm comparison study** — your implementations versus libraries, with
   computational complexity analysis.

All options require: data acquisition and cleaning, exploratory analysis with
visualizations, statistical testing, at least two numerical methods you
implemented, a machine learning application, and comparison against library
implementations.

**This project is solo.** See [Project Pairs & Collaboration](#sec-pairs).

**Deliverables and dates:**

| Deliverable | Due |
|---|---|
| In-class presentation | Thu **Dec 10** |
| Growth Synthesis | Mon **Dec 14**, 11:59 pm PT |
| Research report (5–7 pages) + repository | Thu **Dec 17**, end of day |

The report covers background and motivation, methods, results, and conclusions.

Presentations are **10 minutes** — roughly 8 to present and 2 for questions.
Short, so plan it: enough to say what you built, show that it works, and say
where it breaks. Everyone presents on Dec 10.

Shorter than an SE presentation, and deliberately so: those are hands-on
workshops where the whole room follows along on their own machines, which takes
time. This one is a report-out. You are telling us what you did and what you
found, not teaching us to do it.

The final project is graded on the same description as the other projects (see
[Grading](grading.md)), applied to a larger piece of work. You should expect to
defend your design and verification choices.

(sec-reflections)=
### Growth Reflections (10% total)

Growth Reflections build **metacognition** — thinking about how you learn so you
can improve your workflow, debugging habits, and verification discipline over
time. Write them in an **informal, memo-like voice** (not an essay). Honesty and
specific evidence matter more than polished prose.

There are three, deliberately spaced so they form a trajectory rather than a
chore:

| | Due | Purpose |
|---|---|---|
| **Growth Memo 1** | Mon **Aug 31** | **Baseline** — how you work *before* this course changes it |
| **Growth Memo 2** | Mon **Oct 19** | **Course correction** — what has changed, what has not |
| **Growth Synthesis** | Mon **Dec 14** | **Synthesis** — the whole arc |

All three are graded on honesty and specificity rather than polish or length —
see [Grading](grading.md). Be specific throughout. "I did not understand why Newton's method diverged until
I plotted the iterates" is worth more than a page of general statements about
learning a lot.

(sec-growth-memo-1)=
#### Growth Memo 1 — Baseline (due Mon Aug 31)

This one is different from the others: it is written in the first week, before
you have done any real work in this course. That is the point. It is a record of
how you thought *before*, and it only exists because nobody can reconstruct that
honestly in December.

Write about half a page on:

- **How you currently work.** When you sit down to write code, what do you
  actually do first? Be honest rather than aspirational.
- **How you currently know your code is right.** What convinces you? Running it
  once? Eyeballing a plot? Something else?
- **What you expect to be hard** about this course, and why.
- **What you want to be able to do** by December that you cannot do now.

:::{tip} Do not skip this one
It is tempting to treat a week-1 memo as a formality. It is the opposite: it is
the only record of how you actually thought before this course changed how you
think. In December you will be asked what changed — and a specific, honest
baseline is what makes that question answerable instead of guesswork.
:::

(sec-growth-memo-2)=
#### Growth Memo 2 — Mid-semester (due Mon Oct 19)

By now you have finished four projects. This one looks backward at real work.
Include:

- evidence of how your work evolved (what you tried, what failed, what changed),
- 2–3 recurring patterns and their likely causes,
- 2–3 concrete next-step habits ("When I…, I will…"),
- a verification plan (how you will know your results are correct),
- a brief AI and collaboration reflection and disclosure (even if "none"),
- **a look back at Growth Memo 1** — where were you right about yourself, and
  where were you wrong?

Returned before the **Nov 1 late withdrawal deadline**, so that if something is
going badly you find out while you still have options.

(sec-growth-synthesis)=
#### Growth Synthesis (due Mon Dec 14)

Submitted at the start of finals week, synthesizing your learning across the
semester: how your habits changed, how your verification strategies matured, and
what you can do now that you could not do in August.

**Write it against your own earlier memos.** Re-read what you wrote in August and
October, quote yourself, and say where you were right, where you were wrong, and
what you did not yet know to worry about. Guidance posted in Week 13.

(sec-ai-policy)=
## Academic Integrity & Generative AI Policy

All submitted work in this course must reflect **your own understanding**.
Collaboration is strongly encouraged for discussing concepts and strategies.
However, what you submit must be written independently and must represent your
own reasoning. Copying solutions (from classmates, the internet, generative AI,
or solution manuals) is not permitted. Violations of academic integrity will be
handled according to university procedures and may be reported to the
[Center for Student Rights and Responsibilities](https://sacd.sdsu.edu/student-rights/academic-dishonesty/cheating-and-plagiarism).

For full details — including the staged three-phase rules and documentation
requirements — read the [AI Use & Growth Mindset Policy](ai-policy.md).

:::{important} Generative AI rules (enforced)
- **AI is optional.** You can earn full credit without using AI.
- **Understanding is required.** If you can't explain it, don't submit it.
- **No AI refactoring / restructuring** of your solution unless explicitly assigned.
- **No AI-written core solution code** (the algorithmic logic that produces the result).
- **Struggle first, then ask.** Do ~20–30 minutes of productive effort (try, check docs, minimal repro, hypothesis) before using AI for coding help.
- **Disclose meaningful AI use** whenever a submission asks for AI/collaboration disclosure.
:::

Generative AI can produce fluent explanations and plausible-looking solutions
that are subtly wrong. In a quantitative, model-based course, "sounds right" is
not a standard of truth. If you do not have the quantitative discipline to
verify an AI output, you risk learning the wrong thing confidently.

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

All course-related communication should be sent through Canvas messaging when
possible. Include "COMP 521" in the subject line. I aim to respond within 24–48
hours on weekdays. **Before emailing, check this syllabus and recent Canvas
announcements.**

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

I am **not** providing a course AI notebook. Instead, I will show you how to
build your own — because assembling one is itself a study technique, and because
a tool you built from materials you selected is one whose limits you understand.

**NotebookLM** (or a similar grounded tool) lets you upload the course readings
and ask questions answered *from those sources* rather than from the open
internet. That grounding matters: a general chatbot will confidently invent a
convergence rate, whereas a notebook restricted to your readings will tell you
what the readings actually say. I will demo the setup in class.

:::{note} This does not conflict with the materials policy
Building a **private** notebook from course readings for your own studying is
exactly the personal educational use the [Course Materials](#sec-materials)
policy permits. What that policy prohibits is publishing or redistributing the
materials — so keep your notebook private and do not share it outside the class.
:::

Study tools remain subject to the
[AI Use & Growth Mindset Policy](ai-policy.md): a notebook is an AI tool, and
using it to generate solution code is prohibited in every phase, the same as any
other.

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
