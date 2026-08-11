---
title: "Getting Started"
subtitle: "COMP 536: Computational Modeling for Scientists"
author: "Anna Rosen"
---


**Your Foundation for Computational Science**

Before we model complex systems, we need to set up our computational laboratory. This module establishes the professional development environment and essential skills you'll use throughout COMP 536 and your research career.

:::{tip} Module Philosophy: Tools Shape Thinking

The difference between a computational scientist and someone who codes isn't knowledge of Python syntax — it's mastery of the ecosystem. Version control, environment management, and command-line fluency aren't just "nice to have" skills; they fundamentally change how you approach problems, collaborate, and think about reproducible science.
:::

## Module Overview

::: {.grid}

::: {.g-col-12 .g-col-md-4}
::: {.card .h-100}
::: {.card-header}
**Command Line Interface**
:::
::: {.card-body}
Master the terminal with essential commands for file management, navigation, and automation

[Start Guide $\to$](01-cli-intro.qmd){.btn .btn-primary .btn-sm}
:::
:::
:::

::: {.g-col-12 .g-col-md-4}
::: {.card .h-100}
::: {.card-header}
**Software Setup**
:::
::: {.card-body}
Install Python with Miniforge, configure VS Code, and create your isolated course environment

[Start Guide $\to$](02-software-setup.qmd){.btn .btn-primary .btn-sm}
:::
:::
:::

::: {.g-col-12 .g-col-md-4}
::: {.card .h-100}
::: {.card-header}
**Git & GitHub**
:::
::: {.card-body}
Version control fundamentals, GitHub Classroom workflow, and collaboration best practices

[Start Guide $\to$](03-git-intro.qmd){.btn .btn-primary .btn-sm}
:::
:::
:::

:::

:::{note} Daily Workflow Companion

Before you code, open the [**Scientific Software Workflow Cheatsheet**](05-scientific-software-workflow-cheatsheet.qmd). It compresses the reproducibility contract, evidence model, and debugging ladder into one page you can keep beside your editor.
:::

## Why This Order Matters

```{mermaid}
graph LR
    A[CLI Skills] --> B[Software Setup]
    B --> C[Version Control]
    C --> D[Ready for Projects]

    A1[Navigate & Execute] --> A
    B1[Run Install Commands] --> B
    C1[Use Git in Terminal] --> C
    D1[Submit Assignments] --> D

    style A fill:#e3f2fd
    style D fill:#f3e5f5
```

**Complete these guides in order**. Each builds on the previous:

1. [**CLI first**](01-cli-intro.qmd): Learn to navigate before installing anything.
2. [**Setup second**](02-software-setup.qmd): Use your CLI skills to install tools.
3. [**Git last**](03-git-intro.qmd): Apply everything to manage your code.

## Learning Path

:::{important} Module Goals

After completing this module in order, you will:

- **Navigate** the terminal with confidence using pwd, ls, cd, and Tab completion.
- **Have** a fully configured Python environment isolated from system Python.
- **Understand** conda environments and why they prevent dependency conflicts.
- **Use** Git for every assignment submission via GitHub Classroom.
- **Debug** common issues independently using error messages.
- **Appreciate** why every computational scientist relies on these tools daily.
:::

## Time Investment

| Component | Time |
|-----------|------|
| **Module Total** | 3-4 hours (estimated) |
| CLI Introduction | 45 minutes |
| Software Setup | 30 minutes |
| Git Introduction | 45 minutes |
| Practice | 60+ minutes |
| **Daily Practice** | 5-10 min/day |

## Common Challenges (and Solutions)

:::{warning} Expected Hurdles

**Challenge 1: "The terminal is scary"**
*Solution*: Start with just 3 commands (pwd, ls, cd). Everything else builds on these.

**Challenge 2: "Command not found" errors**
*Solution*: Usually means wrong environment. Check for `(comp536)` in your prompt.

**Challenge 3: Git says "failed to push"**
*Solution*: Someone else pushed first. Pull, resolve conflicts, then push.

**Challenge 4: "This doesn't work on Windows"**
*Solution*: Use Git Bash for Unix-like commands. We've noted all platform differences.

**Challenge 5: "I accidentally deleted files with rm"**
*Solution*: Why we emphasize backups and teach safe deletion practices first!
:::

## Your First Week Checklist

:::{note} Setup Verification

Complete these milestones in order:

**After CLI Guide**

- [ ] Can navigate directories without clicking
- [ ] Understand pwd, ls, cd, and Tab completion
- [ ] Know the dangers of rm -rf

**After Software Setup**

- [ ] Miniforge installed and working
- [ ] VS Code configured with Python extension
- [ ] Can activate comp536 environment
- [ ] Test script runs successfully

**After Git Guide**

- [ ] GitHub account with Student Developer Pack
- [ ] Personal Access Token configured
- [ ] Can clone, commit, and push
- [ ] Understand GitHub Classroom workflow

**Ready for Project 1**

- [ ] Clone assignment from GitHub Classroom
- [ ] Make commits with meaningful messages
- [ ] Push changes to submit work
:::

## Quick Command Reference

| Command | What It Does |
|---------|--------------|
| **Terminal Basics** | |
| `pwd` | Show current directory location |
| `ls -la` | List all files with details |
| `cd folder_name` | Change to different directory |
| `Tab` key | Autocomplete (use constantly!) |
| **Python Environment** | |
| `conda activate comp536` | Enter your course environment |
| `python script.py` | Run your Python code |
| `which python` | Verify correct Python is active |
| **Git Workflow** | |
| `git status` | Check what's changed |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save your work |
| `git push` | Submit to GitHub |

## Getting Help

:::{note} Support Resources

**Setup Issues**:

- Read error messages carefully (they usually tell you what's wrong).
- Google the exact error message in quotes.
- Check our troubleshooting sections in each guide.
- Post on course Slack with: OS, command tried, full error.

**Conceptual Questions**:

- Why do we need virtual environments?
- How does Git track changes?
- What's the difference between terminal and shell?
$\to$ Great office hours questions!

**Platform-Specific Issues**:

- **Windows**: Use Git Bash for Unix commands
- **Mac**: If commands fail, check if you need to install Xcode tools
- **Linux**: Usually works out of the box

**Remember**: Everyone struggles with setup. Once it's working, it just works.
:::

## Module Completion

:::{important} Success Indicators

You're ready for [*Python Fundamentals*](../03-scientific-computing-with-python/01-python-fundamentals/index.qmd) when you can:

1. **Open terminal** and navigate to any folder using cd and ls
2. **Activate your environment** with `conda activate comp536`
3. **Create a Git repository**, make commits, and push to GitHub
4. **Run Python scripts** from the command line
5. **Fix basic issues** using error messages and documentation

If you can do these five things, you have the foundation for everything in this course!
:::

## What's Next?

After completing this module, you'll begin the [*Python Fundamentals*](../03-scientific-computing-with-python/01-python-fundamentals/index.qmd) module where you'll:

- Write your first object-oriented simulation
- Use the terminal skills daily for running scripts
- Submit all work via Git and GitHub Classroom
- Build on this foundation for the rest of your career

---

:::{tip} How to Succeed in This Module

**Don't Rush**: Setup problems compound. Better to spend an extra hour now than fight your environment all semester.

**Practice Daily**: Spend 10 minutes each day using the terminal. Muscle memory develops quickly with consistent practice.

**Commit Often**: Make Git commits after every small success. You can't over-commit, but you can under-commit.

**Read Error Messages**: They usually tell you exactly what's wrong. Copy the full error when asking for help.

**Keep Notes**: Document what worked for your specific system. You'll need these notes again for future projects.

**Remember**: These tools aren't just course requirements—they're essential skills for any scientific research career. The more you invest in mastering them now, the more prepared you'll be for real research challenges ahead.
:::

Ready to begin? Start with [Chapter 1: Command Line Interface](01-cli-intro.qmd) $\to$
