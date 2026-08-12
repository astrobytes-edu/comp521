---
title: "Chapter 4: Software Engineering for Scientists"
subtitle: "COMP 521"
author: "Anna Rosen"
---

<!-- prep-banner:start -->
:::{warning} This reading is still being revised
Readings are reviewed and finalized **at least one week before they are
assigned**, so you will always have a settled version before you need it. Until
then, expect rough edges — wording, examples, and cross-references may change.

Where a reading disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
:::
<!-- prep-banner:end -->

## Why This Matters

Most scientists learn to code by trial and error. This works for small scripts, but fails catastrophically for:

- Code that must be **correct** (not just "seems to work")
- Code that others must **read and trust**
- Code that you must **debug at 2am before a deadline**

This guide covers what CS students learn over 4 years, compressed into what you actually need.

:::{note} How to use this chapter
This is a course-wide reference, not a one-off assignment handout. We’ll use **Project 1** as a running example because it’s the first time you’ll be required to meet the full reproducibility contract (CI, `run.py`, deterministic runs, and non-interactive figure generation). Keep this open and return to it throughout the semester — these habits apply to every project and to real research code.

:::{tip} Need the one-page version?
Use the [Scientific Software Workflow Cheatsheet](05-scientific-software-workflow-cheatsheet.md) before each coding session, and come back to this full chapter when you need deeper examples.
:::
:::

---

## TL;DR — Read This Every Week

:::{important} The Commandments of Scientific Software

1. **Think before you type.** The keyboard is the last step, not the first.

2. **Write down the contract.** Inputs, outputs, units, valid ranges — before coding.

3. **Assume your code is wrong.** Prove otherwise with validation, not hope.

4. **Fail fast.** Check inputs immediately. A clear error beats silent garbage.

5. **Plot first, not last.** Plots are currency. Every plot is validation.

6. **Test requirements, not code.** "Does it meet the spec?" not "Does it run?"

7. **Debug with hypotheses.** "I think X is wrong because Y" — then test it.

8. **Delete bad code.** 3 hours spent doesn't justify keeping garbage. Rewrite.

9. **One source of truth.** Every constant, every formula — one canonical location.

10. **Read more than you write.** Understanding existing code is half the job.

11. **Commit before you experiment.** Git is your safety net. Use it.

:::

**Read this list before every coding session until it becomes instinct.**

---

## Part 0: The Reproducibility Contract (COMP 521)

In COMP 521, reproducibility is not an “extra” — it is a core requirement. Your code must be runnable by someone who has never met you, on a clean clone, without clicking around or guessing which cell to run.

Here is the standard you should design for from day one (and the standard Project 1 will grade directly):

- **One-command entrypoint:** your repository has a single, clear entrypoint (`run.py`) at the repo root.
- **Deterministic by default:** runs are reproducible (fixed random seeds unless explicitly overridden).
- **Non-interactive by default:** no prompts, no manual steps, no “open this notebook and run cells 3–17”.
- **Separation of concerns:** keep fast numerical sanity checks separate from tests, and keep both separate from slow plotting/figure generation.

Concretely, that means you should be able to run:

```bash
python run.py validate
python run.py test
python run.py make-figures
```

:::{note} Three command families, three evidence types
Treat these command families as different evidence streams:

- `python run.py validate` = **scientific evidence** (physics/trend/anchor checks)
- `python run.py test` = **behavioral evidence** (contract and error-handling checks)
- `python run.py make-figures` = **diagnostic evidence** (where output shape or scale goes wrong)

The commands are complementary, not interchangeable.
:::

```{mermaid}
flowchart LR
    S["Spec"] --> C["Contract"]
    C --> V["Validate<br/>(scientific evidence)"]
    V --> T["Test<br/>(behavioral evidence)"]
    T --> P["Plot<br/>(diagnostic evidence)"]
    P --> I["Iterate"]
    I --> S

    classDef core fill:#e8f3ff,stroke:#1f4b99,stroke-width:2px,color:#0f274f;
    classDef evidence fill:#fff4e5,stroke:#a35a00,stroke-width:2px,color:#4a2a00;
    class S,C,I core;
    class V,T,P evidence;
```

:::{tip} Structure is part of your evidence
Students usually copy directory structure before they copy process. Start with a structure that makes your evidence pipeline obvious.

**Bad repo (ambiguous responsibilities):**

```text
project/
├── analysis_final_v3.ipynb
├── final_code_really.py
├── tmp2.py
├── plot_latest_new.png
└── test_script.py
```

**Good repo (reproducible by design):**

```text
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
:::

If you build your workflow around these commands, everything else in this guide becomes easier: debugging is faster, your repo stays reviewable, and CI can run your project automatically. See **Project 1** for the exact submission contract.

:::{tip} Design for the grader you haven’t met yet
If your work only runs “on your laptop, in your current directory, after you manually ran three cells”, it is not reproducible. The goal is a clean clone and a single, documented workflow.
:::

## Part 1: Think Before You Code

### The #1 Mistake

> "Let me just start coding and figure it out as I go."

This is how you end up debugging for 6 hours instead of thinking for 20 minutes.

**Professional developers spend more time reading and thinking than typing.** The keyboard is the last step, not the first.

### The Pre-Coding Checklist

Before you write a single line of code, answer these questions **in writing** (paper, notes app, comments — anywhere):

| Question | Why it matters |
|----------|----------------|
| **What are the inputs?** | Types, units, valid ranges, edge cases |
| **What are the outputs?** | Types, units, format, precision |
| **What could go wrong?** | Invalid inputs, edge cases, numerical issues |
| **How will I know it's correct?** | Test cases, validation values, sanity checks |
| **What are the units?** | CGS? SI? Solar units? Mixed? |

:::{tip} The 20-minute rule
If you can't explain your approach in plain English in 20 minutes, you don't understand the problem well enough to code it.
:::

### Example: Before Implementing $L(M)$

**Bad approach:** "I'll just translate the equation to Python."

**Good approach:**

```
INPUTS:
- mass: float or array, in solar units (M/M_sun)
- Z: float, metallicity, range [0.0001, 0.03]

OUTPUTS:
- luminosity: same shape as mass, in solar units (L/L_sun)

WHAT COULD GO WRONG:
- Mass outside valid range [0.1, 100] — formula becomes unphysical
- Z outside range — coefficients not calibrated
- Negative mass — physically meaningless
- Array vs scalar confusion

HOW I'LL KNOW IT'S CORRECT:
- L(1.0 M_sun) ~ 0.698 L_sun (from validation table)
- L increases with M (physical requirement)
- L at low Z > L at high Z for same mass
```

Now you can code. You know what to check, what to handle, what to test.

---

## Part 2: Contracts and Invariants

### What is a Contract?

A **contract** is a formal agreement between your function and its callers:

- **Preconditions:** What must be true *before* calling the function
- **Postconditions:** What will be true *after* the function returns
- **Invariants:** What must *always* be true

Think of it like a legal contract: "If you give me valid inputs (preconditions), I guarantee valid outputs (postconditions)."

### Example Contract

```python
def luminosity(mass, Z=0.02):
    """ZAMS luminosity from Tout et al. (1996) Eq. 1.

    CONTRACT:
    ---------
    Preconditions:
        - 0.1 <= mass <= 100 (solar units)
        - 0.0001 <= Z <= 0.03
        - mass is float or numpy array

    Postconditions:
        - Returns luminosity in solar units (L/L_sun)
        - Output shape matches input shape
        - All values are positive
        - L increases monotonically with M

    Invariants:
        - Uses Tout et al. (1996) coefficients (never modified)
        - Z_sun = 0.02 (fixed reference)
    """
```

### Why Contracts Matter

1. **You know what to validate:** Check preconditions at function entry
2. **You know what to test:** Test that postconditions hold
3. **You know what NOT to change:** Invariants are sacred

### Enforcing Contracts in Code

```python
def luminosity(mass, Z=0.02):
    # Enforce preconditions (fail fast)
    mass = np.asarray(mass)
    if np.any(mass < 0.1) or np.any(mass > 100):
        raise ValueError("Mass must be in [0.1, 100] M_sun")
    if Z < 0.0001 or Z > 0.03:
        raise ValueError("Z must be in [0.0001, 0.03]")

    # ... compute result ...

    # Postcondition check (optional, for debugging)
    assert np.all(result > 0), "Luminosity must be positive"
    assert result.shape == mass.shape, "Shape mismatch"

    return result
```

:::{note} Fail fast
**Fail fast** means: detect errors as early as possible, as close to the source as possible. Don't let bad data propagate through your code.

A clear error at the input is infinitely better than garbage output that "looks reasonable."
:::

:::{tip} Check yourself (2 minutes)
1. Write a contract for `radius(mass, Z)` in 6 lines: inputs (types/units), outputs (units/shape), and two edge cases.
2. Name one invariant in your Project 1 implementation — something you will treat as “sacred” and never silently change.
:::

---

## Part 3: Reasoning from Specs

### What "Specs" Means

A **specification** is a precise description of what code must do. It can be:

- A scientific paper (equations, tables, valid ranges)
- A project assignment (requirements, deliverables)
- A docstring or contract (inputs, outputs, behavior)

### The Process

1. **Read the spec carefully** — Every word matters
2. **Identify the requirements** — What MUST the code do?
3. **Identify the constraints** — What are the limits?
4. **Derive test cases** — How would you verify each requirement?
5. **Then implement** — Translate requirements to code

### Example: Reading a Paper as a Spec

From Tout et al. (1996):

> "The fits are valid for $0.1 \leq M/M_\odot \leq 100$ and $0.0001 \leq Z \leq 0.03$"

**What this tells you:**

- Precondition: mass in [0.1, 100] solar units
- Precondition: Z in [0.0001, 0.03]
- Implication: Raise error outside these ranges (don't extrapolate!)

> "The coefficients are given in Table 1"

**What this tells you:**

- You must transcribe Table 1 exactly
- A single wrong digit = wrong answers
- Double-check every coefficient

### Don't Guess — Derive

**Bad:** "I think it should return an array..."

**Good:** "The spec says input can be array-like, so output must match input shape."

**Bad:** "This probably uses natural log..."

**Good:** "Equation 3 explicitly shows $\log_{10}$, so I'll use `np.log10()`."

---

## Part 4: Validation-First Development

### The Mindset Shift

> **Assume your code is wrong until proven otherwise.**

Not "assume it works if it runs." Not "assume it's correct if the output looks reasonable."

Assume it's wrong. Then prove yourself wrong by finding evidence of correctness.

### The Validation Workflow

1. **Before coding:** Identify validation checkpoints
2. **After each function:** Run validation immediately
3. **Before making plots:** Validate the underlying data
4. **Before submission:** Run full validation suite

### What Makes a Good Validation Check?

| Good validation | Bad validation |
|-----------------|----------------|
| Compare to known values from paper | "The plot looks right" |
| Check physical trends (L increases with M) | "It runs without errors" |
| Verify edge cases (M = 0.1, M = 100) | "The numbers seem reasonable" |
| Cross-check with independent calculation | "It matches my intuition" |

### Example Validation Strategy

```python
def validate_luminosity():
    """Validate luminosity function against known values."""

    # Anchor check: known value from paper
    L_solar = luminosity(1.0)
    assert abs(L_solar - 0.698) < 0.01, f"L(1 M_sun) = {L_solar}, expected 0.698"

    # Trend check: L increases with M
    masses = np.logspace(-1, 2, 100)
    L = luminosity(masses)
    assert np.all(np.diff(L) > 0), "L must increase with M"

    # Physics check: low Z -> higher L
    L_solar_Z = luminosity(1.0, Z=0.02)
    L_low_Z = luminosity(1.0, Z=0.0001)
    assert L_low_Z > L_solar_Z, "Low-Z stars should be more luminous"

    print("All validation checks passed!")
```

:::{note} Validation vs. tests vs. plots (don’t blur these)
These three tools have different jobs. You want all three — but you don’t want to confuse them.

- **Validation = scientific evidence.** Validation answers: “Does the science make sense?” These are fast physics or ground-truth checks (anchor values, trends, limiting cases). In COMP 521 this is typically `python run.py validate`.
- **Unit tests = behavioral evidence.** Unit tests answer: “Does the code meet its contract?” These are automated, fast checks of behavior and error handling (usually via `pytest` or `python run.py test`).
- **Plots = diagnostic evidence.** Plots answer: “Where is it going wrong?” Plots are diagnostic checkpoints and sanity checks — often the fastest way to spot unit/shape mistakes. In COMP 521 this is typically `python run.py make-figures`.

Not everything belongs in a unit test. If a check is slow, visual, or requires generating figures, it probably belongs in validation or in your figure pipeline — not in `pytest`.
:::

:::{tip} Check yourself (2 minutes)
List three validation checks for your Project 1 model:
1. One **anchor value** (from the paper).
2. One **trend** (what must increase/decrease).
3. One **limiting case** (behavior at an endpoint or simple regime).
:::

---

## Part 5: Debugging Systematically

### The Wrong Way to Debug

1. Stare at code hoping to spot the bug
2. Add random print statements everywhere
3. Change things and see if it helps
4. Google the error message and copy-paste solutions

### The Right Way to Debug

**Step 1: Reproduce the bug**

- What exact input causes the problem?
- Can you write a minimal test case?

**Step 2: Isolate the bug**

- Which function is failing?
- What are the inputs to that function?
- What is the output vs. expected output?

**Step 3: Form a hypothesis**

- "I think the bug is because X"
- Not "something is wrong somewhere"

**Step 4: Test the hypothesis**

- Add ONE targeted check
- Confirm or refute your hypothesis
- Repeat until found

### How to Read a Stack Trace (Traceback)

When Python crashes, the traceback is telling you a story: which function called which function, and where things went wrong.

Use this rule of thumb:

1. **Read bottom-up.** The last line is the exception type and message.
2. **Find the first frame in your code.** Skip frames inside libraries unless the bug is truly in the library.
3. **Capture the inputs that triggered it.** Your next move is to reproduce the crash with the smallest possible input.

### Use a Debugger When Print Isn’t Enough

Print statements are fine for quick checks, but if you need to inspect state step-by-step, use a debugger.

The simplest built-in option is `breakpoint()`:

```python
def luminosity(mass, Z=0.02):
    mass = np.asarray(mass)
    breakpoint()  # inspect variables, then step through
    # ...
```

If you run your code and it drops into the debugger, you can inspect variables, step line-by-line, and test hypotheses quickly. If you prefer a GUI, VS Code’s debugger does the same thing with a visual interface.

### The Binary Search Method

If you don't know where the bug is:

1. Check the output at the **end** — is it wrong? (Yes)
2. Check the output at the **middle** — is it wrong?
   - Yes -> Bug is in first half
   - No -> Bug is in second half
3. Repeat until you find the exact line

This is $O(\log n)$ instead of $O(n)$ — much faster for long code paths.

### Common Bug Categories

| Symptom | Likely cause |
|---------|--------------|
| Off by factor of ~2.3 | `log` vs `log10` confusion |
| Off by powers of 10 | Unit conversion error |
| Wrong sign | Subtraction order, angle convention |
| NaN or Inf | Division by zero, log of negative |
| Shape mismatch | Scalar vs array confusion |
| "Looks reasonable but wrong" | Coefficient transcription error |

---

## Part 6: Testing That Actually Tests

### What Tests Are For

Tests encode **requirements as code**. A passing test suite means: "All requirements I wrote down are satisfied."

### What Tests Are NOT For

- Proving your code is correct (impossible)
- Testing implementation details (fragile)
- Achieving 100% coverage (meaningless metric)

### Good Tests vs. Bad Tests

**Bad test:** Tests that the code does what the code does

```python
def test_luminosity():
    # This tests nothing — just verifies code runs
    L = luminosity(1.0)
    assert L == luminosity(1.0)  # Tautology!
```

**Good test:** Tests that the code meets requirements

```python
def test_luminosity_solar_mass():
    # Tests against INDEPENDENT known value from paper
    L = luminosity(1.0)
    assert L == pytest.approx(0.698, rel=0.02)
```

**Good test:** Tests physical constraints

```python
def test_luminosity_increases_with_mass():
    # Tests that physics makes sense
    masses = np.logspace(-1, 2, 100)
    L = luminosity(masses)
    assert np.all(np.diff(L) > 0)
```

**Good test:** Tests error handling

```python
def test_invalid_mass_raises():
    # Tests that preconditions are enforced
    with pytest.raises(ValueError):
        luminosity(-1.0)
```

### Test Independence

Each test should:

- Run independently (no order dependence)
- Test ONE thing (single assertion focus)
- Be fast (milliseconds, not seconds)
- Have a clear name (`test_luminosity_solar_mass`, not `test1`)

:::{warning} Numerical gotchas: floats and randomness
Scientific code almost always involves floating-point arithmetic and (sometimes) randomness. Treat both as first-class engineering concerns.

- **Never assert exact float equality.** Use tolerances (e.g., `pytest.approx`) and choose them intentionally. Use a **relative tolerance** when values span orders of magnitude, and add an **absolute tolerance** when values can be near zero.
- **Be deterministic by default.** If you use randomness (Monte Carlo, sampling, noise models), fix the seed for `validate` and `test` so bugs are reproducible. Make “override the seed” an explicit option — not an implicit accident.
:::

:::{tip} Check yourself (2 minutes)
1. Write one good test and one bad test for your Project 1 repo. In one sentence each, explain why the good test is good and why the bad test is bad.
2. Pick a tolerance for one numerical check. Explain whether it is a relative tolerance, an absolute tolerance, or both — and why.
:::

---

## Part 7: Code Organization

### Single Source of Truth

Every piece of information should live in exactly ONE place.

**Bad:**

```python
# In file1.py
SOLAR_MASS = 1.989e33

# In file2.py
SOLAR_MASS_G = 1.989e33  # Same value, different name!

# In file3.py
mass_solar = 1.989e33  # Copied again!
```

**Good:**

```python
# In constants.py (the ONLY place)
MSUN = 1.989e33

# In every other file
from constants import MSUN
```

### Separation of Concerns

Each module should do ONE thing:

| Module | Responsibility |
|--------|----------------|
| `constants.py` | Define constants (no computation) |
| `zams.py` | Compute L(M,Z) and R(M,Z) |
| `star.py` | Represent a single star |
| `astro_plot.py` | Create plots (no physics) |
| `run.py` | CLI interface (no logic) |

### Why This Matters

- **Easier to test:** Test `zams.py` without plotting
- **Easier to debug:** Bug in plot? Check `astro_plot.py`
- **Easier to change:** New constant source? Edit ONE file
- **Easier to read:** Know where to look

---

## Part 8: Delete, Rewrite, Iterate

### The Sunk Cost Trap

You've spent 3 hours on a function. It's ugly, buggy, and you hate it. But you keep patching it because:

> "I've already put so much time into this..."

This is the **sunk cost fallacy**. Those 3 hours are gone whether you keep the code or not. The only question is: what's the fastest path to working code *from here*?

Often the answer is: **delete it and start over.**

### Why Rewriting is Faster

Your first attempt taught you:

- What the problem actually is (not what you thought it was)
- Which approaches don't work
- What edge cases exist
- What the code should look like

Armed with this knowledge, your second attempt will be:

- Cleaner (you know the structure now)
- Faster (no more exploration)
- More correct (you know the pitfalls)

:::{tip} The rewrite rule
If you've been debugging the same code for more than 30 minutes without progress, **stop**. Ask yourself: "Would it be faster to rewrite this from scratch with what I now know?"

The answer is often yes.
:::

### What Students Get Wrong

| Fear | Reality |
|------|---------|
| "I'll lose my work" | Git remembers everything. Commit first, then delete. |
| "Starting over means I failed" | Starting over means you learned. |
| "I'm so close to fixing it" | You've been "so close" for an hour. |
| "The new version might have bugs too" | Yes, but different bugs you'll understand. |

### Permission to Delete

You have permission to:

- **Delete functions** that aren't working
- **Rewrite modules** that got too tangled
- **Throw away** your first approach entirely
- **Start fresh** after learning what doesn't work

Code is cheap. Your time and sanity are expensive.

### The Iteration Mindset

Professional software development is iterative:

1. **Write** something that works (ugly is fine)
2. **Validate** that it's correct
3. **Refactor** to make it clean
4. **Repeat** as requirements evolve

Your first version is a draft, not a final product. Drafts get rewritten. That's the process, not a failure.

:::{important} Git is your safety net
Before deleting or rewriting, **commit your current state**:

```bash
git add -A
git commit -m "WIP: saving before rewrite"
```

Now you can delete freely. If the rewrite goes badly, you can always get back:

```bash
git checkout HEAD~1 -- filename.py
```

Nothing is ever truly lost if it's in git.
:::

---

## Part 9: Getting Unstuck

### The Walk Away Rule

If you've been stuck for 30+ minutes:

1. **Stop typing**
2. **Go do something else** — walk, shower, eat, sleep
3. **Come back with fresh eyes**

This isn't procrastination. Your brain continues working on problems in the background. The breakthrough often comes *away from the keyboard*.

:::{tip} The shower phenomenon
There's a reason so many bugs get solved in the shower. Your conscious mind stops forcing a solution, and your subconscious makes connections you missed.

If you're stuck: walk away. Set a timer for 20 minutes. Do something completely unrelated. Come back.
:::

### Rubber Duck Debugging

Before asking for help, **explain the problem out loud** — to a rubber duck, a stuffed animal, an empty chair, or a wall.

The act of articulating the problem often reveals the solution. You'll say "and then this happens because..." and suddenly realize that's exactly where the bug is.

This works because:

- Talking forces linear, step-by-step thinking
- You can't hand-wave past gaps in your understanding
- Your brain processes differently when speaking vs. thinking

### How to Ask for Help (The Right Way)

When you do need help, a good question gets answered faster. A bad question gets "what have you tried?"

**The Minimal Reproducible Example (MRE):**

1. **Minimal** — Smallest code that shows the problem
2. **Reproducible** — Someone else can run it and see the issue
3. **Example** — Actual code, not "my function doesn't work"

**Bad question:**
> "My luminosity function gives wrong values. Help?"

**Good question:**
> "My `luminosity(1.0)` returns 0.45, but the paper says it should be ~0.698.
> Here's my code: [10 lines that reproduce the problem].
> I've checked: coefficients match Table 1, using log10 not ln, mass is in solar units.
> What am I missing?"

### What to Include When Asking for Help

| Include | Why |
|---------|-----|
| What you expected | "I expected L ~ 0.698" |
| What you got | "I got L = 0.45" |
| What you tried | "I checked X, Y, Z" |
| Minimal code | 10-20 lines that reproduce it |
| Error message (if any) | Exact text, not paraphrased |

The better your question, the faster the answer. Putting effort into the question often solves it yourself.

:::{tip} Check yourself (2 minutes)
Draft a “help request” message that includes:

- what you expected,
- what you got,
- what you tried,
- and a minimal reproducible example (10–20 lines).
:::

---

## Part 10: Plot First, Not Last

### Plots Are Currency

In software engineering, **working software** is the measure of progress.

In scientific computing, **plots are currency** — they're how you:

- **Validate** — Does the curve look right?
- **Debug** — Where exactly does it go wrong?
- **Communicate** — Papers, talks, reports
- **Convince** — Prove to yourself and others that it works

A function that runs without errors means nothing. A plot showing correct behavior means *everything*.

### The Anti-Pattern

Most students do this:

1. Write all the code
2. Debug until it runs
3. Make plots at the end
4. Discover something is fundamentally wrong
5. Start over

### The Right Way

**Plot as soon as you have plottable output:**

```
Implement luminosity() -> Plot L vs M -> Does it look right?
    -> YES
Implement radius() -> Plot R vs M -> Does it look right?
    -> YES
Implement T_eff -> Plot HR diagram -> Does it look right?
    -> YES
Continue...
```

Each plot is a **checkpoint**. If it looks wrong, stop. Debug *now*, while you know exactly which function caused the problem.

### What "Looks Right" Means

You're not just looking for "a curve." You're checking:

| Check | What to look for |
|-------|------------------|
| **Trend** | Does it go up/down as physics predicts? |
| **Magnitude** | Is the y-axis in the right ballpark? |
| **Smoothness** | Are there weird kinks or discontinuities? |
| **Endpoints** | Do the edges behave sensibly? |
| **Comparison** | Does it match the paper's figure? |

:::{tip} Plot early, plot often
Every plot is diagnostic evidence. Many plots also support validation, but keep figure-generation checks separate from unit tests.

If you can't plot it yet, you're not ready to move on.
:::

---

## Appendix: Agile Principles for Scientists

:::{note} Optional background
**Agile software development** is a set of principles that emerged from decades of failed software projects. The core ideas translate well to scientific computing.
:::

### The Agile Manifesto (Paraphrased for Science)

| Agile principle | For scientists |
|-----------------|----------------|
| **Working software** over comprehensive documentation | A running script beats a perfect plan |
| **Responding to change** over following a plan | Your understanding evolves — let your code evolve too |
| **Individuals and interactions** over processes and tools | Talk to your advisor/collaborators early and often |
| **Customer collaboration** over contract negotiation | Get feedback on results before polishing details |

### The Key Insight: Iterate

Agile's core insight is that **you can't know everything upfront**. Instead of planning everything, then building everything, then testing everything:

```
Plan a little -> Build a little -> Test a little -> Repeat
```

This is why we emphasize:

- **Plot first, not last** (get feedback early)
- **Validate after each function** (don't batch)
- **Commit before experiments** (safe iteration)
- **Delete and rewrite** (iteration, not perfection)

You're not building a cathedral. You're iterating toward correctness.

---

## Summary: The Professional Workflow

1. **Understand** — Read specs, identify requirements
2. **Plan** — Write contracts, identify validation checks
3. **Implement** — One function at a time, validate immediately
4. **Test** — Encode requirements as tests
5. **Debug** — Systematically, with hypotheses

The keyboard is the **last** step, not the first.

:::{important} The key insight
Amateur programmers debug their code. Professional programmers debug their **understanding**.

If you deeply understand the problem, the code writes itself. If you don't, no amount of debugging will save you.
:::
