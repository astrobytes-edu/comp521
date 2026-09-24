---
title: "Code Review Presentations"
subtitle: "COMP 521 | Fall 2026"
---

# Code Review Presentations

| Round | Date | Course weight |
|:--|:--|--:|
| Scientific computing | Thu **Oct 22**, in class | 5% |
| Data science / machine learning | Thu **Nov 12**, in class | 5% |

Each student presents individually for **12 minutes**, followed by **3 minutes
for questions**. The two presentations replace Project 6 and count for **10%
total**. Projects 1–5 count for 40% of the course grade.

## The question

**How do you decide whether to trust code you did not write?**

Choose two different open source packages or repositories that interest you:
one related to computational science/scientific computing and one related to
data science or machine learning. Give the class a brief map of each package's
architecture: what it is for, its main components, how inputs move through
them, and where your example fits. Then zoom into one useful example, trace a
relevant code path, and check a claim about its behavior. You do not need to
master every part of the repository or find a bug.

This is a chance to follow your interests. A paper, a scientific question, a
GitHub search, documentation, or a conversation may lead you to a package. AI
may suggest candidates under the rules below. **Tell us why you chose this
particular package** and what made you want to understand it.

| Round | Choose code related to | Questions worth asking |
|:--|:--|:--|
| **1 · Scientific computing** | A numerical method, simulation, analysis pipeline, or other computational science task | What model or method is implemented? What do its inputs and units mean? What approximation, numerical error, or regime limit matters? |
| **2 · Data science / ML** | Data processing, statistical modeling, classification, clustering, or another DS/ML task | Where do the data come from? How are they prepared and separated for evaluation? What baseline and metric support the reported result? Could leakage or an unsuitable metric mislead us? |

These questions are starting points. Choose the ones that matter for your code
path; you do not need to cover every item in the table.

## Choose a manageable piece of code

Select a publicly available repository with an open source license. Record its
authors or project organization, repository link, license, and the commit or
release you reviewed.
Choose **one specific function, class, or pipeline step** that connects an input
to an output you can explain. Look for a small example or test that does not
require special hardware, credentials, or a large download. If the full package
is too large to run, narrow the part you review.

You may compare several candidates before choosing. The final choice is yours;
package popularity and finding the most complex code are not goals.

## Teach one example, then review it

Use your 12 minutes to guide us through a small case. The times are guides,
not grading rules:

1. **Package and choice (~2 minutes).** Why did you choose it? Explain its
   purpose and sketch its architecture: main components, input-to-output flow,
   and where your example fits. A simple diagram is welcome but not required.
2. **Zoom into the code (~4 minutes).** Show the exact function, class, or
   pipeline step you reviewed. Trace an input to an output, explain the method
   in plain language, and identify one implementation choice or assumption
   that affects the result.
3. **Predict and check (~4 minutes).** Ask classmates to predict a result or
   diagnose a plausible failure. State what you expect and why before showing
   evidence. Use a small case that could have contradicted your expectation;
   explain what the check catches and what it misses.
4. **Judgment (~2 minutes).** Say what the evidence supports, what remains
   uncertain, and which next check would be most useful.

In the **scientific computing round**, run your check when practical. If setup
prevents that, examine a specific upstream test closely: show its input,
expected result, and assertion, and state clearly that you did not run it. In
the **DS/ML round**, run a small data-to-output example yourself. If setup or
data access prevents this, contact me before the presentation to agree on an
equivalent check. You may show prepared results; you do not need to run code
live in class. A documentation example alone is not a check.

A passing test supports the behavior it actually checks. It does not establish
every scientific or data claim made by the package. A well-supported judgment
may be positive; you are not expected to find a defect.

:::{tip} Keep the tutorial small
Teach one complete example that a classmate could revisit. You may present
from a short slide deck **or** an annotated notebook; you do not need both or
a separate written report. If you use a notebook, run it from a fresh kernel
before class. Keep the architecture overview brief enough to leave room for
the code and evidence.
:::

After your talk, allow three minutes for questions. Explain your reasoning
without reading an AI-generated answer. Classmates will take part in the
prediction and discussion, but they do not grade your work.

## What to submit

Submit your slide deck or annotated notebook through the corresponding Canvas
assignment **by 5:30 pm PT on your presentation date**. Include a final sources
section in that file with the upstream repository URL, authors or project
organization, license, exact commit or release reviewed, and links to the code
and check you discussed. If you used AI meaningfully, include the brief
[AI Use Log](../01-course-info/ai-policy.md#documentation-requirements-strict)
there too. Your reason for choosing the package belongs in the presentation.

You may quote upstream source code or an existing example with clear credit.
Any demonstration code you write must be your own. No fork of the upstream
repository or separate report is required. If you cannot present on your
assigned date, contact me promptly through Canvas Inbox to arrange an
equivalent individual presentation.

## How your presentations are graded

I assign one holistic letter grade to each presentation. Each letter counts
for 5% of the course grade. I look for these forms of evidence:

| | Strong evidence |
|:--|:--|
| **Choice and understanding** | You explain why you selected the package, sketch its architecture and workflow, and place your chosen method within it. |
| **Code and evidence** | You explain a consequential part of the source and compare a concrete expectation with a check that could have disagreed. You state what the evidence supports and where it stops. |
| **Teaching and questions** | Your small example and audience prompt make a method or review habit understandable; you can answer questions in your own words. |
| **Attribution and repeatability** | A classmate can find the exact upstream version, code path, and check you discussed. |

An **A** presentation connects the package map to a specific code path, uses a
check that could have disagreed with its expectation, and makes a conclusion
limited to the evidence. A **B** presentation is accurate and useful but leaves
the code connection, check, or limit underexplained. A **C** presentation is
mostly a package overview or recipe, with little source-level or checking
evidence. Work that is substantially incomplete falls below that. These are
descriptions, not a points checklist. I grade your reasoning and teaching, not
the package's popularity, polished slides, or whether you found a bug. See
[Grading](../01-course-info/grading.md) for the shared letter scale.

## AI use for this assessment

AI is optional. You may use it to discover candidate packages, locate
documentation or tests, clarify concepts, troubleshoot a small example,
suggest possible ways to organize your talk, and ask questions that expose
gaps in an explanation you have written. Treat its suggestions as leads to
check against the repository, documentation, paper, or a small test.

You choose the package and code path, decide what the evidence supports, and
write the final outline, notebook, slides, and review in your own words and
style. AI may flag an unclear or unsupported claim but may not write or
rewrite these materials, provide replacement wording, or supply answers for
the presentation. AI may not write demonstration code for you. Do not use AI
during the presentation or questions.

If you use AI meaningfully, follow the [course AI Use Log requirements](../01-course-info/ai-policy.md#documentation-requirements-strict).
You do not need to document ordinary searches or submit a transcript. Package
discovery does not require waiting through the coding-focused “struggle first”
period; if you used AI for discovery, say so in your log's “What I did before
AI” field. The usual struggle-first guidance still applies to coding help.
