---
title: "LLM Primer: Learn Faster Without Outsourcing Your Thinking"
subtitle: "Read difficult math, connect ideas across fields, and prepare your Final Project"
site:
  hide_outline: true
---

Use AI to get feedback sooner while you work through a hard idea. Ask it to
unpack a symbol, question a step, or give you a new case to try. Then make
the prediction or explanation yourself and check it. You can use the same
routine with a classmate or the course materials. AI is optional.

::::{grid} 1 1 2 3

:::{card} Final Project
Start with the review and work toward one presentation your group can teach
together.
+++
[Plan the group talk](#final-project-example)
:::

:::{card} Study session
Choose a learning goal, make a first attempt, and get feedback.
+++
[Use the study loop](#study-loop)
:::

:::{card} Prompt library
Find a question that helps you work through an equation, connect two ideas,
or rehearse an explanation.
+++
[Find a prompt](#prompt-library)
:::

::::

:::{tip} Check what you can do with the chat closed
Explain one idea from memory. Change one assumption and predict what happens.
If you can describe why the prediction follows, you have something you can
use in the next section or teach to your group.
:::

(final-project-example)=
## Final Project · From the review to a shared presentation

Start with the introduction and Figure 1 of Blumenthal et al.’s
*Bridging Control, Inference, Transport, and Thermodynamics*. The figure
maps links among **control, inference, transport, thermodynamics, and
learning**. The authors use optimization under constraints as a common
language. Pick a connection you want to understand well enough to teach,
then follow the references or bring in sources that help you explain it.
[Read the review](https://arxiv.org/html/2609.15897v1)

The three of you give **one presentation**, roughly an hour including
discussion. The brief budgets about 15 minutes per person, including a
short science application, and five minutes together for your shared
question and Python example, followed by discussion. You choose the
topics, depth, examples, and organization.
[Final Project brief](../08-assessments/final-project.md#presentation)

### Read a hard equation from first principles

1. **Say what the equation answers.** What quantity are the authors
   explaining or solving for? Which symbols describe data, a state, a
   parameter, or a variable you can choose?
2. **Rebuild one consequential step.** Start from a definition, a stated
   assumption, or a principle such as conservation of probability. Write
   the next line yourself. If you get stuck, ask for one prerequisite or
   a hint at that line, then return to the source.
3. **Test your reading.** Check the units where they apply or try a limit
   you can reason through. Say what changes if you relax an assumption.
   A textbook or another paper can fill a missing derivation, challenge
   an assumption, or show where the idea is used.

:::{note} Keep track of which source supports each idea
Treat a fluent reply as a claim to check. If it cites a paper, confirm
that the reference is real, then find the definition, equation, or figure
that supports the claim. Read the surrounding text for assumptions.
A study of earlier ChatGPT models found invented references and errors
in references to real papers.
[Walters and Wilder, 2023](https://www.nature.com/articles/s41598-023-41032-5)
:::

### Think in systems

Start with a sketch. What changes over time, and what governs that change?
Mark what you can observe and what you can change through a control or
intervention. Where do the constraints enter? If an observation is noisier
or a boundary changes, trace the effect through the model to what you can
infer, predict, or control.

When comparing two fields, match the quantities and assumptions. A model
for an individual path and a model for a probability distribution can
describe the same system at different levels. Check what each description
can tell you. For example, compare maximum-entropy inference in § I.2.2
with equilibrium thermodynamics in § III.1. What distribution does each
description select? What are the constraints, and where does the
physical assumption about energy enter? If you claim an equivalence,
identify the mathematical step and assumptions that make it work.

### Make the three parts build on one another

Agree on a shared question and the connection you want classmates to
understand. For each handoff, ask **what does this part let the next
person explain?** Share notation where it helps the audience follow. Use
the Python example to test a prediction, compare two cases, or make a
relationship visible. Explain what the review contributes, what each
additional source helps you establish, and what your example leaves open.

### Worked exchange · The Brownian bridge

In § I.4.3, a particle starts at zero and undergoes Brownian motion. We
observe its exact final position $y$ at time $1$. How does knowing the
endpoint change what we can infer about earlier positions? Before asking
for help, sketch how the spread of possible positions might change with time.
[Blumenthal et al., § I.4.3](https://arxiv.org/html/2609.15897v1#S1.SS4.SSS3)

| Asking for a finished solution | Asking for help getting unstuck |
|---|---|
| “Explain how the Brownian bridge connects inference and control and give us the derivation.” | “We predict less spread halfway through when the endpoint is known. Starting from a free Brownian path, how could we construct a path that ends exactly at $y$? Give us one hint.” |

:::{admonition} Sample hint · Try the endpoints first
:class: dropdown

Start with a free Brownian path $W_t$. Add a straight-line correction
that is zero at the start and equals the endpoint error $y-W_1$ at the
finish. Check the start and finish, then ask what happens to the spread
between them.
:::

:::{admonition} Check the derivation and the prediction
:class: dropdown

For standard Brownian motion, $X_t=W_t+t(y-W_1)$ starts at zero and ends
at $y$. Many paths meet those endpoints. To check this construction,
notice that $W_t$ and $W_1$ share increments up to time $t$, so their
covariance is $t$. The residual $W_t-tW_1$ has zero covariance with $W_1$.
They are jointly Gaussian, so conditioning on $W_1=y$ leaves the residual
distribution unchanged. The mean of the bridge is $ty$ and its variance
is $t(1-t)$, compared with variance $t$ for free Brownian motion. At the
midpoint the variances are $1/4$ and $1/2$.

The review describes the same conditioned path law using a drift toward
the target. The drift is the mathematical link between endpoint inference
and steering the dynamics. A claim about a physical force on the original
particle would require separate evidence.
:::

**Change one assumption.** Now suppose the endpoint measurement has
independent Gaussian noise with nonzero variance. Which step used the
endpoint as an exact constraint? Should the inferred spread still shrink
to zero at the last time? Try explaining the change with the chat closed.

(study-loop)=
## Use AI to get feedback and practice

Start with a goal you can check, such as “I can explain what is optimized,
state the constraint, and predict what happens when it changes.”
**Metacognition** means planning the work, monitoring what you understand,
and using that evidence to decide what to try next.

[Open the study tools](#start-a-study-session) if you want to try the loop with AI.

1. **Make a first attempt.** Sketch the system, start the derivation, or
   make a prediction. Mark the first step you can’t justify.
2. **Ask for one kind of help.** Ask for a hint, a counterexample, or one
   question. If the response gives away the answer, go back to your attempt
   and ask about a smaller step.
3. **Check and revise.** What evidence would tell you whether the reply
   holds? Use the original text, a limiting case, or a calculation you
   can do independently. Keep track of what actually changed your mind.
4. **Recall and apply.** Close the chat and explain the idea. Return to it
   later and try a case with one assumption changed. Use what you miss to
   choose your next study goal.

(how-we-learn)=
### What makes the practice stick

- **Try before you get feedback.** In the
  [oscillating optimizer exercise](../01-course-info/this-week.md#paired-ai-practice-why-wont-the-loss-settle),
  predict one update before you look at the hint. If you have no starting
  point, study a small worked example first, then try another yourself.
  In two math studies, first attempts followed by instruction helped
  students understand concepts and apply them to new problems.
  [Kapur, 2014](https://doi.org/10.1111/cogs.12107)
- **Recall before you reread.** Reconstruct the rule or sketch the model
  from memory, then check it. Retrieval practice helped students answer
  recall and inference questions about science texts a week later. Spacing
  several recall attempts across study sessions can also help retention.
  [Karpicke and Blunt, 2011](https://pubmed.ncbi.nlm.nih.gov/21252317/) ·
  [Karpicke and Bauernschmidt, 2011](https://pubmed.ncbi.nlm.nih.gov/21574747/)
- **Explain why, then change the case.** State why a step works and which
  assumption it needs. Experiments in undergraduate physics found that
  self-explanation and some structured comparisons of worked examples
  helped students solve a new problem that combined several concepts.
  Practicing retrieval across varied examples also helped students
  transfer an idea to a new case in a separate study.
  [Badeau et al., 2017](https://journals.aps.org/prper/abstract/10.1103/PhysRevPhysEducRes.13.020112) ·
  [Butler et al., 2017](https://pubmed.ncbi.nlm.nih.gov/29265856/)

:::{admonition} What AI learning studies measured
:class: dropdown

- **Guided practice can help.** A course-specific AI tutor led to higher
  immediate post-test scores across two undergraduate physics lessons.
  That study measured near-term learning with a structured tutor. Try
  asking for feedback on a step you’ve already attempted.
  [Kestin et al., 2025](https://www.nature.com/articles/s41598-025-97652-6.pdf)
- **Prompts can support metacognition.** In one undergraduate Python
  course, a Jupyter tool prompted students to plan, inspect errors, and
  check intermediate results. The intervention group scored higher on a
  similar task after the intervention. Try asking a tutor to question your
  plan, then decide for yourself how to check it.
  [Hou et al., 2026](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1790196/full)
- **Assisted performance can hide gaps.** In a high-school math trial,
  students with a general GPT interface did better on assisted practice
  and worse on a later unaided exam. Similarly, a small programming study
  found lower unaided quiz scores after participants learned a Python
  library with AI assistance. Try one fresh problem with the chat closed
  to see what you can do independently.
  [Bastani et al., 2025](https://doi.org/10.1073/pnas.2422633122) ·
  [Shen and Tamkin, 2026 preprint](https://arxiv.org/abs/2601.20245)
:::

(start-a-study-session)=
## Start a study session

**ChatGPT Edu through SDSU.** Sign in with your SDSUid. In a regular web
chat, type `@study` and choose **Study**, or [open Study mode](https://chatgpt.com/studymode).
Give it your learning goal and first attempt. Ask it to wait for your
answer before offering feedback. Study mode can still make mistakes.
[SDSU access](https://it.sdsu.edu/services/ai/chatgpt-edu) ·
[OpenAI’s Study mode guide](https://help.openai.com/en/articles/11780217-using-study-mode-in-chatgpt)

**Gemini Notebook, formerly NotebookLM.** As we did in class,
[open Gemini Notebook](https://notebook.google.com/) and select the public
sources you want to ask about. Try **Chat → Configure Chat → Learning Guide**.
Open a cited passage and check the text or math in context. Use **Studio →
Flashcards** or **Quizzes** for recall practice. Answer first, then check the
key. In the Gemini web app you can also try **More tools → Guided Learning**.
Some accounts offer **Study and learn** when creating a notebook.
[Chat and citations](https://support.google.com/gemininotebook/answer/16179559?hl=en) ·
[Flashcards and quizzes](https://support.google.com/gemininotebook/answer/16958963?hl=en) ·
[Guided Learning](https://support.google.com/gemini/answer/16448384?hl=en) ·
[Study notebooks](https://support.google.com/gemini/answer/16972047?hl=en)

**Without an account.** Take turns asking one of the questions below or
critique the sample reply in the
[November 19 exercise](../01-course-info/this-week.md#paired-ai-practice-why-wont-the-loss-settle).

(prompt-library)=
## Prompt library

Pick a prompt for where you’re stuck. Add your current explanation or
prediction and the specific public passage you’re working from.

:::{admonition} Read the review and work through the math
:class: dropdown

**Get oriented in the review**

```text
I can explain [idea] and want to understand how it connects to [topic].
Using the review, point me to one section that might help. Ask me
what I think the connection is and wait for my answer.
```

**Ask a Socratic tutor for a hint**

```text
Here's what I think the authors are doing [attempt]. Ask me one
question about the step I'm least sure of. Wait for my answer
before offering a hint.
```

**Find the prerequisite**

```text
I can follow the argument through [step]. What one definition or
principle should I review for the next step? Give me one small
practice question and wait while I try it.
```

**Rebuild a step from first principles**

```text
Here are my definitions, assumptions, and first two lines [work].
Point out the first step I haven't justified. Give me one way
to check it, then pause while I work it out.
```
:::

:::{admonition} Connect fields and trace the system
:class: dropdown

**Map the system**

```text
Here's my sketch of what enters, what changes over time, what we
can observe, and what constrains the system [sketch]. Ask me one
question about how two of those pieces depend on each other.
```

**Pressure-test a connection**

```text
We think [quantity or principle in A] corresponds to [quantity or
principle in B] under [assumptions]. Challenge one assumption.
Wait for us to predict where the correspondence would break.
```

**Trace a change**

```text
We predict [change] in [observable or inference] when we change
[condition]. Here's how we think the effect propagates [steps].
Which link in this chain should we check first, and how?
```

**Compare two sources**

```text
Here are two public passages and my reading of them. Help me check
whether the authors use different definitions, assumptions, or
evidence. Point to a passage I can read to resolve the difference.
```
:::

:::{admonition} Check the evidence and plan the shared example
:class: dropdown

**Find the supporting passage**

```text
From the selected sources, find the passage or figure that bears
on [claim]. State what the authors show and what you'd have to
infer. If the sources don't cover the claim, say so.
```

**Ask a skeptical reviewer**

```text
Our claim is [claim], and our evidence is [evidence]. Give one
plausible alternative explanation. What observation or limiting
case would help us tell the two explanations apart?
```

**Scope the shared example**

```text
Our question is [question], and we expect [prediction]. Suggest
one small comparison that would make our reasoning visible to
the class. Ask us what each outcome would let us conclude.
```

**Investigate a surprising result**

```text
We predicted [X], observed [Y], and changed [one thing]. Help us
choose one check that could distinguish a problem with the model
from a problem with the calculation. Leave the fix to us.
```
:::

:::{admonition} Rehearse, recall, and transfer
:class: dropdown

**Connect the three parts of the talk**

```text
Here is the question each of us is answering [three questions].
Ask how the answer to one informs the next. Flag one term we
might be using differently and ask us to clarify it.
```

**Practice the discussion**

```text
Ask one question about the assumptions behind our explanation.
Wait for our answer, then change one assumption and ask us to
predict how that would affect our conclusion.
```

**Check what you still understand**

```text
Here's my explanation from memory [explanation]. Ask me one
question that exposes a gap. Wait while I check the original
and tell you what evidence changes my answer.
```
:::

## Before you paste or present

Use public sources and synthetic examples. Keep grades, identifiable
student data, credentials, other students’ work, and private or unpublished
research out of chatbots, including campus accounts.

Make your own slides, verify claims and results, and acknowledge meaningful
AI assistance. Follow the [Final Project AI guidance](../08-assessments/final-project.md#ai-and-authorship)
and the [course AI policy](../01-course-info/ai-policy.md).
