---
title: "Lecture 2 · Python Bootcamp: Procedures and Decisions"
subtitle: "Block 1 · Week 1 | Chapter 3 and the Grade Calculator"
---

# Lecture 2 · Procedures and decisions

This is the second class meeting in the Python Bootcamp. We will use an
intentionally simple light-curve rule to practice a bigger idea: Python does
exactly the procedure we specify—including an incomplete or ambiguous one.

## Today’s question

How do we turn a human rule into a procedure that a computer can carry out and
that another person can check?

By the end of class, you should be able to plan a branch before writing syntax,
explain a boundary choice, and trace a loop without guessing.

## 1. A rule must be explicit · 12 minutes

Suppose we call a measurement a **candidate low-flux observation** when its
normalized flux is below `0.99`. Before writing code, write the rule in plain
language:

```text
For each flux measurement:
    If the flux is below 0.99,
    report it as a candidate low-flux observation.
```

This is pseudocode: a precise plan, not Python syntax. It answers an important
question before code can answer anything: is “below” strict, or should exactly
`0.99` count? Here we have intentionally chosen a strict rule. A real transit
search requires uncertainties, observation cadence, systematic effects, and a
defined detection procedure; this exercise only practices the computational
decision.

:::{note} Predict

For `[1.000, 0.993, 0.990, 0.989, 0.975]`, which values pass a rule written as
“below `0.99`”? What small change would include `0.990`?
:::

## 2. Compare, then branch · 15 minutes

```python
flux = 0.989
threshold = 0.99

if flux < threshold:
    print("candidate low-flux measurement")
else:
    print("not below the stated threshold")
```

The expression `flux < threshold` evaluates to either `True` or `False`.
Indentation is not decoration: it tells Python which statements belong to the
`if` branch and which belong to the `else` branch. With this rule, `0.990` does
not pass because it is equal to the threshold, not less than it.

### Boundary questions are model questions

When you choose `<` rather than `<=`, you choose what happens at a boundary.
Neither operator is universally “right.” The correct choice is the one that
matches a stated rule and is tested at the boundary. This is why the Grade
Calculator lab begins with a decision table instead of a pile of `if`s.

## 3. Apply one rule to many observations · 18 minutes

```python
flux_measurements = [1.000, 0.993, 0.989, 0.975]
threshold = 0.99
candidate_count = 0

for flux in flux_measurements:
    if flux < threshold:
        candidate_count = candidate_count + 1
        print(f"candidate: {flux:.3f}")

print("number of candidates:", candidate_count)
```

Read the loop once by hand. The name `flux` takes the first value, then the
second, and so on. `candidate_count` is an **accumulator**: it keeps track of a
quantity that changes as the loop advances. At each step, ask: what is the
current `flux`, what does the comparison produce, and what must the count be
after this step?

| Current `flux` | Is `flux < 0.99`? | `candidate_count` after this step |
|---:|---:|---:|
| `1.000` | `False` | `0` |
| `0.993` | `False` | `0` |
| `0.989` | `True` | `1` |
| `0.975` | `True` | `2` |

## 4. Design before implementation · 30 minutes

Begin the [Grade Calculator Design Lab](../07-practice-labs/grade-calculator-design.md).
Do not rush to code. Your group should produce a small design packet that
states:

1. the inputs and their allowed ranges;
2. the exact percentage formula;
3. the letter-grade boundaries, including what happens at each boundary; and
4. a test table with ordinary, boundary, and invalid cases.

The program becomes easy to grade and easy to debug when the decisions are
visible before the syntax appears.

## Exit check

Write one Grade Calculator rule in two forms:

1. Plain language: “If ________, then ________.”
2. Pseudocode with an explicit comparison.

Then name one test at the exact boundary of your rule.

## Before Lecture 3

Read [Chapter 4](04-python-data-structures.md) and
[Chapter 5](05-python-functions-modules.md) through their first core examples.
Bring your Grade Calculator design packet.
