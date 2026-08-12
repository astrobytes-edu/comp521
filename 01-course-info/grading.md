---
title: "Grading"
subtitle: "COMP 521 | Fall 2026"
kernelspec:
  name: python3
  display_name: Python 3
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

# Grading

## How grading works in this course

**Everything is graded with letters, and each assignment gets one letter.**

There are no point breakdowns, no percentage subscores, and no itemized
rubrics. When I grade your project I read the whole thing — code, validation,
figures, memo — and judge it as a piece of work, the way a referee assesses a
paper.

:::{note} Why it works this way
An itemized rubric tells you exactly what to optimize, and people optimize what
they are shown. That produces submissions assembled to satisfy a checklist
rather than to be correct, which is the opposite of what this course is for.

What you get instead is a clear description of what each grade *means* — below —
plus a written comment on every submission explaining the grade you got. If you
want to know how to do better, that comment is the answer, and it will tell you
more than a number would.
:::

## The scale

| A+ | A | A− | B+ | B | B− | C+ | C | C− | D+ | D | D− | F |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 4.3 | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0.7 | 0 |

Your grade in each component is the average of the letters you earned in it, and
your course grade is the weighted average of those. Letters average the way you
would expect: an A+ and an A− come out to an A. Grades are recorded as these
numbers in Canvas, so you can see where you stand at any point.

**A+ is not "did extra."** It is for work showing judgment beyond what was asked
— a validation you thought of yourself, a failure mode you found and explained,
a simpler approach than the one specified. Volume does not earn it.

:::{note} A+ on an assignment, but not as a course grade
SDSU does not award A+ as a final grade, so **the highest course grade is an
A** — a semester of straight A+ work earns an A.

An A+ is still worth having. Because it counts as 4.3, it lifts your average and
can offset a weaker piece of work elsewhere. That is the point of it: not a
higher ceiling, but room to recover from one bad week.
:::

### Turning your average into a course grade

Each cutoff sits **0.2 below** that grade's own value, so you can fall a little
short of straight-A work and still earn an A. What it will not do is round you
up a whole step: consistent A− work earns an A−.

| Average | Grade | | Average | Grade |
|:--|:--|--|:--|:--|
| ≥ 3.80 | **A** | | 1.80 – 2.09 | **C** |
| 3.50 – 3.79 | **A−** | | 1.50 – 1.79 | **C−** |
| 3.10 – 3.49 | **B+** | | 1.10 – 1.49 | **D+** |
| 2.80 – 3.09 | **B** | | 0.80 – 1.09 | **D** |
| 2.50 – 2.79 | **B−** | | 0.50 – 0.79 | **D−** |
| 2.10 – 2.49 | **C+** | | < 0.50 | **F** |

### Work it out yourself

Nothing here is hidden — you can compute your own grade at any point. The code
below is live: it runs when this page is built, and the output is what it
actually produced.

```{code-cell} python
GRADE_POINTS = {
    "A+": 4.3, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0,
}

WEIGHTS = {
    "projects": 0.50,
    "final": 0.20,
    "presentations": 0.10,
    "reflections": 0.10,
    "engagement": 0.10,
}

# Highest cutoff first, so the first match wins.
CUTOFFS = [
    (3.80, "A"),  (3.50, "A-"), (3.10, "B+"), (2.80, "B"),
    (2.50, "B-"), (2.10, "C+"), (1.80, "C"),  (1.50, "C-"),
    (1.10, "D+"), (0.80, "D"),  (0.50, "D-"), (0.00, "F"),
]


def average(letters):
    """Mean grade point of a list of letter grades."""
    return sum(GRADE_POINTS[letter] for letter in letters) / len(letters)


def course_grade(components):
    """Weighted average across components, and the letter it earns."""
    total = sum(WEIGHTS[name] * average(letters)
                for name, letters in components.items())
    letter = next(grade for cutoff, grade in CUTOFFS if total >= cutoff)
    return total, letter


me = {
    "projects":      ["B+", "A-", "A", "A", "A+", "A-"],
    "final":         ["B+"],
    "presentations": ["B+", "A"],
    "reflections":   ["A", "B", "A"],
    "engagement":    ["A"],
}

for name, letters in me.items():
    print(f"{name:>14}: {average(letters):.2f}   {letters}")

total, letter = course_grade(me)
print(f"\n{'weighted':>14}: {total:.2f}   ->  {letter}")
```

Notice what an A+ does here and what it does not. It pulls the projects average
up, which can rescue a weaker component — but the course grade still tops out at
A no matter how many you collect.

## Weights

| Component | Weight |
|:--|--:|
| Projects (6) | 50% |
| Final project | 20% |
| SE presentations (2) | 10% |
| Growth Reflections (3) | 10% |
| Scholarly engagement | 10% |

## What the grades mean

### Projects and the final project

Judged as a whole: does the code do the right thing, do you know that it does,
and could someone else follow it?

| | |
|:--|:--|
| **A** | It works, you showed that it works, and someone else could pick it up and run it. The validation is real — convergence at the expected order, a limiting case checked, a comparison against something that could have disagreed. The memo says what you did and what it means. |
| **B** | It works and you checked it, but the evidence is thinner than the claim, or the code takes effort to follow, or the writing leaves me guessing about a choice you made. |
| **C** | It runs, but there is little evidence it is right — tests that would pass for a broken implementation, or results reported without any check that could have caught an error. Or pieces are missing. |
| **D** | Substantially incomplete, not working, or missing what was asked for. |
| **F** | Not submitted, or not your own work. |

:::{important} Every project must be submitted
Submitting all six projects and the final project is a requirement to pass,
independent of your average — see the
[Syllabus](syllabus.md#sec-projects). The arithmetic on this page assumes you
turned everything in.
:::

:::{important} Validation is where the grade is decided
Code that runs is the starting point, not the finish line. The difference
between a B and an A in this course is almost always whether you can show your
result is *right* — not whether you produced one.
:::

Each project's **analysis notebook** ends with a written **Discussion** section
(prose only, ~500–800 words) where you say what your results mean. It is not
graded separately — it is part of the work I am reading, and it is usually the
first thing I read.

### SE presentations

Judged on whether the class can use the tool afterward.

| | |
|:--|:--|
| **A** | The room ran the tool and left able to use it. Your repository worked on other people's machines. You knew where the tool breaks down and said so. |
| **B** | A solid walkthrough, but some people got stuck and stayed stuck, or the setup needed hand-holding, or you could not say much about the tool's limits. |
| **C** | Mostly a demo you performed rather than one we did, or a repository that did not really work outside your own laptop. |
| **D / F** | Unprepared, or not delivered. |

Full assignment and topic list:
[Software Engineering Presentation](../assignments/se-presentation.md).

### Growth Reflections

Judged on honesty and specificity, not polish or length.

| | |
|:--|:--|
| **A** | Specific and honest. Names things you actually got wrong and what you did about them. Someone reading it would learn something real about how you work. |
| **B** | Genuine but general — true statements that could have been written by anyone in the class. |
| **C** | Phoned in. |
| **F** | Not submitted. |

*"I did not understand why Newton's method diverged until I plotted the
iterates"* is worth more than a page of general statements about learning a lot.

| | Due |
|---|---|
| Growth Memo 1 — baseline | Mon **Aug 31** |
| Growth Memo 2 — mid-semester | Mon **Oct 19** |
| Growth Synthesis | Mon **Dec 14** |

### Scholarly engagement

One grade, at the end of the semester, for the term as a whole.

| | |
|:--|:--|
| **A** | Prepared and present. Contributes and asks real questions. Arrives at classmates' presentations already set up. Comes to check-ins with work to show. |
| **B** | Steady and cooperative, with some quiet stretches or occasional unpreparedness. |
| **C** | Frequently unprepared or disengaged; participates mainly when prompted. |
| **D / F** | Habitually absent or habitually disengaged. |

## Submission

Submission is via GitHub, using
[Classroom50](https://github.com/foundation50/classroom50/wiki). Projects are due
**Mondays at 11:59 PM PT** (Project 1 excepted — see the
[Schedule](schedule.md)).

**Your last commit before the deadline is your submission.** Commit timestamps
are unambiguous, which cuts both ways: there is never a dispute about what you
turned in and when, and "I finished it but forgot to push" is not recoverable.
Push early and often — a pushed work-in-progress always beats a perfect
uncommitted local copy.
