---
title: "Practice Lab: Design a Trustworthy Grade Calculator"
subtitle: "Python Bootcamp | Chapters 1–5"
---

This is a required, low-stakes Bootcamp Design Check. Work with a partner while
planning, then submit your own completed design packet. Use the fictional course
data below; do not enter your real grades or another person’s grades.

## The problem

Design a calculator that reports a course percentage and letter grade from these
fictional categories:

| Category | Weight | Example score |
|---|---:|---:|
| Labs | 25% | 92 |
| Projects | 45% | 84 |
| Quizzes | 15% | 88 |
| Final report | 15% | 91 |

Use this letter scale: A for 90–100, B for 80–89.999..., C for 70–79.999...,
D for 60–69.999..., and F below 60. Your program should reject a score outside
the inclusive range 0–100 and reject weights that do not sum to 100%.

:::{important} The goal is a trustworthy specification

Do not start with syntax. A calculator can run without errors and still answer
the wrong question if its inputs, rounding rule, boundary behavior, or missing
score policy are vague.
:::

## Part 1 — State the contract

Write a compact answer to each question.

1. What inputs does the calculator accept? Include their units or scales.
2. What outputs does it return?
3. What does it do with a score of `-1` or `101`?
4. What does it do if weights total `95%` or `105%`?
5. When, if ever, does it round the numerical percentage?

## Part 2 — Write the calculation in pseudocode

The numerical course percentage is

$$
P = \sum_i w_i s_i,
$$

where weights must be converted from percentages to fractions before they are
multiplied by scores. Write pseudocode that checks inputs, calculates $P$, and
assigns a letter grade. Be explicit about the order of checks.

```text
START
... your algorithm here ...
END
```

## Part 3 — Trace one ordinary case by hand

Using the fictional data above, fill in a trace table that shows each weighted
contribution and the final percentage. Then state the expected letter grade.

| Category | Weight as fraction | Score | Contribution to P |
|---|---:|---:|---:|
| Labs |  | 92 |  |
| Projects |  | 84 |  |
| Quizzes |  | 88 |  |
| Final report |  | 91 |  |
| **Total** |  |  |  |

## Part 4 — Design tests before implementation

Complete at least these five cases. Add a sixth case of your own.

| Test case | Inputs or condition | Expected result | Why this test matters |
|---|---|---|---|
| ordinary valid record |  |  |  |
| exactly 90.0 |  | A | boundary |
| just below 90.0 |  | B | boundary |
| score outside 0–100 |  | reject | invalid input |
| weights do not total 100% |  | reject | invalid input |
| your case |  |  |  |

## Part 5 — Implement after review

After Chapter 5, implement two small functions:

```python
def weighted_percentage(scores, weights):
    """Return a course percentage or reject an invalid record."""

def letter_grade(percentage):
    """Return one letter grade for a validated percentage."""
```

Keep the numerical calculation and the letter-grade policy separate. That makes
it possible to test or change one policy without silently changing the other.

:::{lecture-checkpoint}
:id: grade-calculator-design-checkpoint
:prompt: Name the most consequential ambiguity you resolved in your calculator design and the test that would catch an incorrect implementation.
:rows: 4
:::

## Submission

Submit your individual design packet using the course’s stated class workflow.
This check is completion-based. Its purpose is to make your reasoning visible
before you implement the calculator in the next bootcamp meeting.
