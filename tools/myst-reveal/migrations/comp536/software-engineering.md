---
title: "Software Engineering for Scientists"
subtitle: "COMP 521 adaptation · editorial draft"
author: Anna Rosen
---


## Why This Matters

```{slide-options}
{"class":"swe-deck"}
```

Most scientists learn to code by trial and error.


::::::::::::::::::::::::::{fragment}
This works for small scripts, but fails for:
::::::::::::::::::::::::::


::::::::::::::::::::::::{slide-incremental}
- Code that must be **correct** (not just "seems to work")
- Code that others must **read and trust**
- Code you must **debug at 2am before a deadline**
::::::::::::::::::::::::

::::::::::::::::::::::::{speaker-note}
Ask: "Who has spent 6 hours debugging something that turned out to be a one-character typo?"
::::::::::::::::::::::::

## The Core Insight

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{div}
**Think $\to$ Plan $\to$ Code**
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
The keyboard is the **last** step, not the first.
::::::::::::::::::::::::::


::::::::::::::::::::::::{speaker-note}
This is the single most important message. Professional developers spend more time reading and thinking than typing.
::::::::::::::::::::::::

## The 11 Commandments

```{slide-options}
{"layout": "section", "eyebrow": "Principles for scientific software", "class": "swe-deck swe-transition"}
```

*Read these every week until they become instinct*

## Think Before You Type

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 01 / 11", "class": "swe-deck swe-transition"}
```

## 1. Think Before You Type

```{slide-options}
{"class":"swe-deck"}
```

> "Let me just start coding and figure it out as I go."


::::::::::::::::::::::::::{fragment}
This is how you end up debugging for 6 hours instead of thinking for 20 minutes.
::::::::::::::::::::::::::

## Write Down the Contract

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 02 / 11", "class": "swe-deck swe-transition"}
```

## 2. Write Down the Contract

```{slide-options}
{"class":"swe-deck"}
```

Before coding, answer **in writing**:

| Question | Example |
|----------|---------|
| What are the inputs? | mass: float, [0.1, 100] $M_\odot$ |
| What are the outputs? | luminosity: float, $L_\odot$ |
| What could go wrong? | Negative mass, wrong units |
| How will I validate? | L(1.0) $\approx$ 0.698 |







## Assume Your Code is Wrong

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 03 / 11", "class": "swe-deck swe-transition"}
```

## 3. Assume Your Code is Wrong

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{div}
**Support correctness claims with tests and validation evidence.**
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
Not "it runs without errors."
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
Not "the output looks reasonable."
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
**Show me the evidence.**
::::::::::::::::::::::::::


## Three Kinds of Evidence

```{slide-options}
{"class":"swe-deck"}
```

Different commands produce different kinds of evidence. Keep them separate so failures are easier to interpret.

::::::::::::::::::::::::{slide-columns}
:::::::::::::::::::::::{slide-column}
::::::::::::::::::::::{note}

**Scientific Evidence**

A validation command, for example `python run.py validate`

Checks whether results match scientific expectations (anchor values, trends, limits).
::::::::::::::::::::::
:::::::::::::::::::::::
:::::::::::::::::::::::{slide-column}
::::::::::::::::::::::{note}

**Behavioral Evidence**

A test command, for example `python -m pytest`

Checks whether code behavior matches the function contract.
::::::::::::::::::::::
:::::::::::::::::::::::
:::::::::::::::::::::::{slide-column}
::::::::::::::::::::::{note}

**Diagnostic Evidence**

A figure-generation command, for example `python run.py make-figures`

Checks where model output looks wrong so you can localize bugs quickly.
::::::::::::::::::::::
:::::::::::::::::::::::
::::::::::::::::::::::::

## Bad Repo vs Good Repo

```{slide-options}
{"class":"swe-deck"}
```

Students usually copy structure before they copy principles.

::::::::::::::::::::::::{slide-columns}
:::::::::::::::::::::::{slide-column}
**Bad (hard to grade, hard to debug)**

```{slide-code} text
:title: Repository layout
project/
├── analysis_final_v3.ipynb
├── final_code_really.py
├── tmp2.py
├── plot_latest_new.png
└── test_script.py
```

:::::::::::::::::::::::
:::::::::::::::::::::::{slide-column}
**Good (reproducible by design)**

```{slide-code} text
:title: Repository layout
project/
├── run.py
├── src/
│   ├── model.py
│   └── physics.py
├── notebooks/
├── tests/
├── validation/
└── figures/
```

:::::::::::::::::::::::
::::::::::::::::::::::::

## Fail Fast

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 04 / 11", "class": "swe-deck swe-transition"}
```

## 4. Fail Fast

```{slide-options}
{"class":"swe-deck"}
```

```{slide-code} python
:title: Python example
def luminosity(mass, Z=0.02):
    # Check inputs FIRST
    if mass < 0.1 or mass > 100:
        raise ValueError("Mass must be in [0.1, 100] M_sun")

    # ... then compute
```



::::::::::::::::::::::::::{fragment}
A clear error at the input beats garbage output that "looks reasonable."
::::::::::::::::::::::::::

## Plot First, Not Last

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 05 / 11", "class": "swe-deck swe-transition"}
```

## 5. Plot First, Not Last

```{slide-options}
{"class":"swe-deck"}
```

In software engineering: **working software** is progress.

In scientific computing: **plots are currency.**



::::::::::::::::::::::::{slide-incremental}
- Diagnose — Where does it go wrong?
- Validate — Does the pattern match known trends?
- Communicate — Papers, talks, reports
::::::::::::::::::::::::

## The Anti-Pattern

```{slide-options}
{"class":"swe-deck"}
```

Most students:

::::::::::::::::::::::::{slide-incremental}
1. Write all the code
2. Debug until it runs
3. Make plots at the end
4. Discover something is fundamentally wrong
5. Start over 😱
::::::::::::::::::::::::


## The Right Way

```{slide-options}
{"class":"swe-deck"}
```

Plot as soon as you have plottable output:

```{slide-code} text
:title: Workflow
luminosity() -> Plot L vs M -> Look right?
    v YES
radius() -> Plot R vs M -> Look right?
    v YES
T_eff() -> Plot HR diagram -> Look right?
    v YES
Continue...
```




::::::::::::::::::::::::::{fragment}
Each plot is a **checkpoint**.
::::::::::::::::::::::::::


## Test Requirements, Not Code

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 06 / 11", "class": "swe-deck swe-transition"}
```

## 6. Test Requirements, Not Code

```{slide-options}
{"class":"swe-deck"}
```

**Bad test:**

```{slide-code} python
:title: Python example
def test_luminosity():
    L = luminosity(1.0)
    assert L == luminosity(1.0)  # Tautology!
```





::::::::::::::::::::::::::{fragment}
**Good test:**

```{slide-code} python
:title: Python example
def test_luminosity_solar_mass():
    L = luminosity(1.0)
    assert L == pytest.approx(0.698, rel=0.02)
```
::::::::::::::::::::::::::


## Debug with Hypotheses

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 07 / 11", "class": "swe-deck swe-transition"}
```

## 7. Debug with Hypotheses

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{div}
**"I think X is wrong because Y"**
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
Not "something is broken somewhere."
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
Form a hypothesis. Test it. Repeat.
::::::::::::::::::::::::::


## The Binary Search Method

```{slide-options}
{"class":"swe-deck"}
```

If you don't know where the bug is:

::::::::::::::::::::::::{slide-incremental}
1. Check output at the **end** — wrong?
2. Check output at the **middle** — wrong?
   - Yes $\to$ Bug in first half
   - No $\to$ Bug in second half
3. Repeat until found
::::::::::::::::::::::::
::::::::::::::::::::::::::{fragment}
With ordered checkpoints and a failure you can localize to one half, the number of checkpoint decisions grows as $O(\log n)$. Arbitrary bugs do not automatically satisfy that assumption.
::::::::::::::::::::::::::


## Common Bug Symptoms

```{slide-options}
{"class":"swe-deck"}
```

| Symptom | Likely cause |
|---------|--------------|
| Off by factor of ~2.3 | `log` vs `log10` |
| Off by powers of 10 | Unit conversion |
| Wrong sign | Subtraction order |
| NaN or Inf | Division by zero, invalid domains, overflow, or earlier nonfinite input |
| Shape mismatch | Scalar vs array |

## Delete Bad Code

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 08 / 11", "class": "swe-deck swe-transition"}
```

## 8. Delete Bad Code

```{slide-options}
{"class":"swe-deck"}
```

You've spent 3 hours on a function. It's ugly and buggy.


::::::::::::::::::::::::::{fragment}
> "I've already put so much time into this..."
::::::::::::::::::::::::::



::::::::::::::::::::::::::{fragment}
**This is the sunk cost fallacy.**
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
Those 3 hours are gone. What's fastest *from here*?
::::::::::::::::::::::::::


## Permission to Delete

```{slide-options}
{"class":"swe-deck"}
```

You have permission to:

::::::::::::::::::::::::{slide-incremental}
- **Delete functions** that aren't working
- **Rewrite modules** that got tangled
- **Throw away** your first approach entirely
- **Start fresh** with what you learned
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
Code is cheap. Your time and sanity are expensive.
::::::::::::::::::::::::::

## One Source of Truth

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 09 / 11", "class": "swe-deck swe-transition"}
```

## 9. One Source of Truth

```{slide-options}
{"class":"swe-deck"}
```

**Bad:**

```{slide-code} python
:title: Python example
# file1.py
SOLAR_MASS = 1.989e33

# file2.py
M_SUN = 1.989e33  # Same value, different name!
```





::::::::::::::::::::::::::{fragment}
**Good:**

```{slide-code} python
:title: Python example
# constants.py (the ONLY place)
MSUN = 1.989e33
```
::::::::::::::::::::::::::


## Read More Than You Write

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 10 / 11", "class": "swe-deck swe-transition"}
```

## 10. Read More Than You Write

```{slide-options}
{"class":"swe-deck"}
```

Professional developers spend **more time reading** than writing.


::::::::::::::::::::::::::{fragment}
Before changing code:
::::::::::::::::::::::::::


::::::::::::::::::::::::{slide-incremental}
- Understand what it does now
- Understand why it was written that way
- *Then* modify
::::::::::::::::::::::::

## Commit Before You Experiment

```{slide-options}
{"layout": "section", "eyebrow": "Commandment 11 / 11", "class": "swe-deck swe-transition"}
```

## 11. Commit Before You Experiment

```{slide-options}
{"class":"swe-deck"}
```

```{slide-code} bash
:title: Git commands
git status
git diff
git add path/to/changed_file.py
git commit -m "Save working baseline before experiment"
```



::::::::::::::::::::::::::{fragment}
Now you can delete freely.
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
If it goes badly:

```{slide-code} bash
:title: Git commands
git log --oneline -- filename.py
git diff <baseline-commit> -- filename.py
# After inspecting the change:
git restore --source=<baseline-commit> -- filename.py
```


Committed content can be recovered. Uncommitted or ignored files are not protected by a commit; restoring a file replaces its current uncommitted contents.
::::::::::::::::::::::::::


## Getting Unstuck

```{slide-options}
{"layout": "section", "eyebrow": "Recover a useful next step", "class": "swe-deck swe-transition"}
```



## The Walk Away Rule

```{slide-options}
{"class":"swe-deck"}
```

If you've been stuck for 30+ minutes:

::::::::::::::::::::::::{slide-incremental}
1. **Stop typing**
2. **Go do something else** — walk, shower, eat
3. **Come back with fresh eyes**
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
This isn't procrastination. Your brain works on problems in the background.
::::::::::::::::::::::::::

## Rubber Duck Debugging

```{slide-options}
{"class":"swe-deck"}
```

Before asking for help, **explain the problem out loud**.


::::::::::::::::::::::::::{fragment}
To a rubber duck. A stuffed animal. An empty chair.
::::::::::::::::::::::::::



::::::::::::::::::::::::::{fragment}
The act of articulating often reveals the solution.
::::::::::::::::::::::::::

## How to Ask for Help

```{slide-options}
{"class":"swe-deck"}
```

**Bad:**

> "My luminosity function gives wrong values. Help?"




::::::::::::::::::::::::::{fragment}
**Good:**

> "My `luminosity(1.0)` returns 0.45, but should be ~0.698.
> Here's my code: [10 lines].
> I checked: coefficients, log10 vs ln, units.
> What am I missing?"
::::::::::::::::::::::::::


## The Professional Workflow

```{slide-options}
{"layout": "section", "eyebrow": "Put the principles into practice", "class": "swe-deck swe-transition"}
```



## The 5-Step Process

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{slide-incremental}
1. **Understand** — Read specs, identify requirements

2. **Plan** — Write contracts, identify validation

3. **Implement** — One function at a time, validate immediately

4. **Test** — Encode requirements as tests

5. **Debug** — Systematically, with hypotheses
::::::::::::::::::::::::


## The Professional Loop

```{slide-options}
{"class":"swe-deck"}
```

**Spec → Contract → Validate (scientific evidence) → Test (behavioral evidence) → Plot (diagnostic evidence) → Iterate → Spec.**

## The Key Insight

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{div}
**Debug your understanding, not your code.**
:::::::::::::::::::::::
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
Understanding the problem gives you a contract and predictions to test. Implementation still requires careful work.
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
When repeated patches fail, revisit the assumptions and the smallest case you can explain by hand.
::::::::::::::::::::::::::


## Worked example: specify the result first

```{slide-options}
{"class":"swe-deck"}
```

We want the arithmetic mean of a nonempty sequence of finite real values.

::::::::::::::::::::::::{slide-incremental}
- Input: a sequence of finite numbers; the sequence is not modified.
- Output: the arithmetic mean in the same units as the input.
- Empty or nonfinite input: raise `ValueError`.
- Independent checks: `[1, 3]` gives `2`; one value returns itself.
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
This small example lets us practice the workflow before applying it to a numerical solver.
::::::::::::::::::::::::::


## Worked example: a plausible implementation fails

```{slide-options}
{"class":"swe-deck"}
```

```{slide-code} python
:title: Deliberately incorrect implementation
def mean_bug(values):
    return sum(values) / (len(values) - 1)

print(mean_bug([1.0, 3.0]))  # 4.0, expected 2.0
```



Predict the result for a one-element input before running it.

::::::::::::::::::::::::::{fragment}
The result is finite and the program runs. Neither observation establishes correctness.
::::::::::::::::::::::::::




## Worked example: test a causal hypothesis

```{slide-options}
{"class":"swe-deck"}
```

**Hypothesis:** the denominator uses `n - 1` instead of `n`.



::::::::::::::::::::::::::{fragment}
For `[1, 3]`, the sum is `4`. The correct denominator is `2`, so the mean is `2`.
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
Changing only that denominator predicts that this test will pass. It does not yet address empty or nonfinite input.
::::::::::::::::::::::::::




::::::::::::::::::::::::::{fragment}
Test the prediction first, then add the missing contract checks.
::::::::::::::::::::::::::


## Worked example: implement the contract

```{slide-options}
{"class":"swe-deck"}
```

```{slide-code} python
:title: A checked arithmetic mean
import math

def finite_mean(values):
    values = tuple(values)
    if not values:
        raise ValueError("At least one value is required")
    if not all(math.isfinite(x) for x in values):
        raise ValueError("All values must be finite")
    return math.fsum(values) / len(values)
```



::::::::::::::::::::::::::{fragment}
The numerical range must also be representable in the chosen floating-point type. This is a teaching example, not an overflow-proof reduction.
::::::::::::::::::::::::::


## Worked example: independent checks

```{slide-options}
{"class":"swe-deck"}
```

```{slide-code} python
:title: Check requirements, not implementation
assert finite_mean([1.0, 3.0]) == 2.0
assert finite_mean([7.0]) == 7.0
assert finite_mean([4.0, 6.0]) == 5.0

try:
    finite_mean([])
except ValueError:
    pass
else:
    raise AssertionError("Empty input must be rejected")
```



::::::::::::::::::::::::::{fragment}
The translated inputs `[4, 6]` shift the mean by `3`. Each check has an expected result independent of calling the implementation twice.
::::::::::::::::::::::::::


## Transfer the workflow to your project

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{slide-incremental}
1. Write the input, output, domain and failure contract.
2. Pick one reference case you can calculate independently.
3. Run the smallest implementation that can fail that check.
4. State a hypothesis, predict the outcome, and change one cause.
5. Check limits, convergence and diagnostics relevant to the method.
6. Save the configuration, commands and evidence needed to reproduce it.
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
Keep the original stellar examples as a second context: the same workflow applies, but the reference values and validity domain come from that model.
::::::::::::::::::::::::::


## The Takeaway

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{fragment}
:::::::::::::::::::::::{div}
**Think $\to$ Plan $\to$ Validate $\to$ Code**
:::::::::::::::::::::::
::::::::::::::::::::::::


::::::::::::::::::::::::::{fragment}
The keyboard is the last step, not the first.
::::::::::::::::::::::::::

## Before Next Class

```{slide-options}
{"class":"swe-deck"}
```

::::::::::::::::::::::::{slide-incremental}
1. **Read** the full guide: [Software Engineering for Scientists](/comp521/software-engineering-for-scientists/)

2. **Keep** the 11 principles available while you work; printing them is optional

3. **Apply** these principles to your current COMP 521 project
::::::::::::::::::::::::


## Questions?

```{slide-options}
{"class":"swe-deck"}
```

Common questions:

::::::::::::::::::::::::{slide-incremental}
- "What if I've already started coding the wrong way?"
- "How do I know when to rewrite vs. keep debugging?"
- "What counts as a 'good' validation check?"
::::::::::::::::::::::::
