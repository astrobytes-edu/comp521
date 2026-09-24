---
title: "Practice Lab: Design and Build a COMP 521 Course-Grade Calculator"
subtitle: "Python Bootcamp | Chapters 1–5 | 30-minute implementation activity"
---

# Practice Lab: Design and Build a COMP 521 Course-Grade Calculator

This is a required, low-stakes Bootcamp activity. Work with a partner while
planning and testing, then write and run your own implementation. It uses the
published COMP 521 grading policy, but **only with the fictional record below**.
Do not enter your own grades, a classmate's grades, or Canvas data.

The fictional record and weights below reflect the current five-project,
two-presentation course plan. If you completed this activity earlier in the
semester, you do not need to redo it.

:::{important} Two phases, two class meetings

Complete Parts 1–4 during Week 1 or before Lecture 3. The **30-minute in-class
activity begins at Part 5**: implementation, direct boundary tests, and a
clean-kernel run. If your design is incomplete, finish it before writing code.
:::

## The problem

Design and build a calculator that reports an unrounded **grade-point average**
and final course letter from the actual COMP 521 component weights:

| Category | Weight | Fictional letter grades |
|---|---:|---|
| Projects (average of five) | 40% | `A`, `B+`, `A−`, `B`, `A` |
| Code Review Presentations (average of two) | 10% | `A`, `B+` |
| Final-project proposal pitch | 5% | `B+` |
| Finished final project | 25% | `A−` |
| Growth Reflections (average of three) | 10% | `A`, `A−`, `B+` |
| Scholarly Engagement | 10% | `A` |

Use the course's letter-to-point scale:

| Letter | A+ | A | A− | B+ | B | B− | C+ | C | C− | D+ | D | D− | F |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Points | 4.3 | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0.7 | 0.0 |

In Python strings, use the ASCII tokens shown in the code examples, such as
`"A-"`, rather than the typographic minus sign used in prose tables.

The final-course cutoffs are `A` at 3.80 or above, then `A−` at 3.50,
`B+` at 3.10, `B` at 2.80, `B−` at 2.50, `C+` at 2.10, `C` at 1.80,
`C−` at 1.50, `D+` at 1.10, `D` at 0.80, and `D−` at 0.50. Below 0.50 is
`F`. An assignment can earn `A+`, but an overall COMP 521 course grade cannot:
the highest final letter is `A`.

:::{important} The goal is a trustworthy specification

Do not start with syntax. A calculator can run without errors and still answer
the wrong question if its letter scale, component counts, weights, rounding
rule, or boundary behavior are vague. Canvas remains the authoritative grade
record; this activity models the published policy only.
:::

## Part 1 — State the contract

Write a compact answer to each question.

1. What inputs does the calculator accept? Name the expected number of projects
   and Growth Reflections.
2. What outputs does it return?
3. What does it do with an unknown letter such as `"E"`?
4. What does it do with four projects, one presentation, or two Growth Reflections?
5. When, if ever, does it round the numerical average?

## Part 2 — Write the calculation in pseudocode

The numerical course average is

$$
G = 0.40\overline{P} + 0.10\overline{C} + 0.05Q + 0.25F + 0.10\overline{R} + 0.10E,
$$

where $\overline{P}$ is the mean grade-point value for five projects,
$\overline{C}$ is the mean for two Code Review Presentations, $Q$ is the
proposal-pitch grade point, $F$ is the finished-final-project grade point,
$\overline{R}$ is the mean for three Growth Reflections, and $E$ is the
Scholarly Engagement grade point. Write pseudocode that checks inputs,
calculates $G$, and assigns a final-course letter. Be explicit about the order
of checks and do not round before applying a cutoff.

```text
START
... your algorithm here ...
END
```

## Part 3 — Trace one ordinary case by hand

Using the fictional data above, fill in a trace table that shows each weighted
contribution and the final unrounded average. Then state the expected final
course letter.

| Category | Component grade points | Weight | Contribution to G |
|---|---:|---:|---:|
| Projects |  | 0.40 |  |
| Code Review Presentations |  | 0.10 |  |
| Proposal pitch |  | 0.05 |  |
| Finished final project |  | 0.25 |  |
| Growth Reflections |  | 0.10 |  |
| Scholarly Engagement |  | 0.10 |  |
| **Total** |  |  |  |

Your unrounded result should be approximately `3.662`, which is an `A−`.

## Part 4 — Design tests before implementation

Complete at least these six cases. Add a seventh case of your own.

| Test case | Inputs or condition | Expected result | Why this test matters |
|---|---|---|---|
| ordinary complete fictional record |  | `3.661666...`, `A−` | ordinary |
| `final_course_letter(3.80)` |  | `A` | final-course boundary |
| `final_course_letter(3.79)` |  | `A−` | final-course boundary |
| unknown letter, such as `"E"` |  | reject | invalid input |
| four projects, one presentation, or two reflections |  | reject | incomplete component |
| `final_course_letter(4.30)` |  | `A`, never `A+` | final-course policy |
| your case |  |  |  |

## Part 5 — Build the calculator · 30 minutes

After your design review, implement these four small functions:

```python
def grade_points(letter):
    """Return the COMP 521 grade-point value for one valid letter."""


def mean_component_grade(letters, *, expected_count, component_name):
    """Return the mean grade points for one complete component."""


def course_average(record):
    """Return the unrounded COMP 521 weighted course average."""


def final_course_letter(average):
    """Return the COMP 521 final-course letter; never return A+."""
```

Represent the supplied fictional record with named fields:

```python
fictional_record = {
    "projects": ["A", "B+", "A-", "B", "A"],
    "code_reviews": ["A", "B+"],
    "proposal_pitch": "B+",
    "final_project": "A-",
    "growth_reflections": ["A", "A-", "B+"],
    "scholarly_engagement": "A",
}
```

Use ordinary or keyword calls deliberately. `expected_count` and
`component_name` are keyword-only because a call such as
`mean_component_grade(projects, expected_count=5, component_name="projects")`
is easier to inspect than two unexplained positional values.

Keep these jobs separate: mapping letters, averaging a component, calculating
the course average, and assigning the final-course letter. That makes the
policy testable and makes a future revision local rather than hidden.

| Time | Work |
|---:|---|
| 0–3 min | Open your completed Parts 1–4 and restate the four function contracts. |
| 3–15 min | Implement `grade_points(...)` and `mean_component_grade(...)`. |
| 15–23 min | Implement `course_average(...)` and `final_course_letter(...)`. |
| 23–30 min | Run the fictional record, direct boundary tests, and invalid-input tests; restart the kernel; write the checkpoint sentence. |

## Part 6 — Show the policy is implemented

During the final seven minutes, run your test table, restart the kernel, and run
all cells from top to bottom. Then write one checkpoint sentence that states:

1. one course-policy rule your calculator makes visible;
2. one boundary test that could catch a wrong implementation; and
3. why the calculator is not the authoritative grade record.

:::{lecture-checkpoint}
:id: grade-calculator-design-checkpoint
:prompt: Name the course-policy boundary that was easiest to implement incorrectly and the test that would catch it.
:rows: 4
:::

## You are done when

You can run your own notebook from a clean kernel; it computes the fictional
record, passes the ordinary, boundary, and invalid-input tests, and contains
your short policy explanation. This is an in-class practice activity, not a
Canvas submission or an official grade record.
