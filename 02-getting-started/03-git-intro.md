---
title: "Chapter 3: Introduction to Git and GitHub"
subtitle: "COMP 536: Computational Modeling for Scientists"
author: "Anna Rosen"
---


# Chapter 3: Introduction to Git and GitHub

## Why Version Control Will Save Your Research

**Imagine this:** It's 2 AM, three days before your thesis defense. You accidentally delete 400 lines of working code while trying to "clean up." Or worse—your laptop dies, taking two years of work with it.

**This happens to someone every semester.**

Git prevents these disasters. It's your safety net, collaboration tool, and scientific record all in one. By the end of this guide, you'll never lose work again.

:::{tip} What You'll Learn

After this guide, you'll be able to:

- Never lose code again (even if your laptop explodes)
- Submit assignments via Classroom50
- Collaborate without fear of overwriting others' work
- Track exactly what changed and when
- Recover from mistakes quickly
:::

## The Version Control Nightmare (Without Git)

We've all been here:

```bash
stellar_evolution.py
stellar_evolution_v2.py
stellar_evolution_v2_FIXED.py
stellar_evolution_v2_FIXED_actually_works.py
stellar_evolution_OLD_DO_NOT_DELETE.py
stellar_evolution_FINAL.py
stellar_evolution_FINAL_REAL.py
stellar_evolution_FINAL_FOR_REAL_USE_THIS_ONE.py
```

With Git, you have ONE file with complete history. Every change is tracked, documented, and reversible.

## Understanding Git: The Mental Model

Think of Git as a **time machine for your code** with three areas:

```{mermaid}
graph LR
    A[Working Directory<br/>Your files] -->|git add| B[Staging Area<br/>Ready to save]
    B -->|git commit| C[Repository<br/>Permanent history]
    C -->|git push| D[GitHub<br/>Cloud backup]
    D -->|git pull| A
```

1. **Working Directory**: Your actual files
2. **Staging Area**: Changes ready to be saved
3. **Local Repository**: Your project's history (on your computer)
4. **Remote Repository**: Cloud backup (GitHub)

## Initial Setup (One Time Only)

### Step 1: Install Git

::: {.panel-tabset}

### macOS

Git comes pre-installed. Verify with:

```bash
git --version
```

If not installed, it will prompt you to install Xcode Command Line Tools.

### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install git

# Fedora
sudo dnf install git
```

### Windows

Download from <https://git-scm.com/downloads>

**Important**: During installation, select:

- "Git from the command line and also from 3rd-party software"
- "Use Visual Studio Code as Git's default editor"
- "Override default branch name" $\to$ type "main"
- "Git Credential Manager" (helps with authentication)

After installation, use **Git Bash** for all Git commands (not Command Prompt).

:::

### Step 2: Configure Your Identity

```bash
# Tell Git who you are (for commit messages)
git config --global user.name "Your Name"
git config --global user.email "your.email@university.edu"

# Set default branch name to 'main' (GitHub's default)
git config --global init.defaultBranch main

# Set default editor (optional but helpful)
git config --global core.editor "code --wait"  # For VS Code

# Verify configuration
git config --list
```

### Step 3: Set Up GitHub Account

1. Go to <https://github.com>
2. Sign up with your **university email** (critical for Student Pack!)
3. Verify your email address
4. Apply for Student Developer Pack: <https://education.github.com/pack>
   - Free GitHub Pro account
   - **GitHub Copilot Pro** (free for students - normally $10/month)
   - GitHub Codespaces hours
   - Access to 100+ developer tools

:::{note} Student Developer Pack Benefits

The pack includes professional tools worth thousands of dollars:

- **GitHub Copilot Pro**: AI pair programmer (disabled for this course initially)
- **Cloud credits**: Azure ($100), DigitalOcean, and more
- **Domain names**: Free .tech, .me domains
- **Learning platforms**: DataCamp, Educative, and others

Verification typically takes 1-72 hours. You'll get an email when approved.
:::

### Step 4: Set Up Authentication

:::{important} Required Since August 2021

GitHub no longer accepts passwords for Git operations. You need either:

1. **Personal Access Token (easier)** - We'll use this
2. SSH Keys (more secure but complex)

We'll use Personal Access Tokens (classic) for simplicity. GitHub also offers "fine-grained" tokens with more security, but classic tokens are simpler for course work.
:::

**Create a Personal Access Token:**

1. Go to GitHub $\to$ Click your profile picture $\to$ Settings
2. In the left sidebar, click **Developer settings**
3. Under **Personal access tokens**, click **Tokens (classic)**
4. Click **Generate new token** $\to$ **Generate new token (classic)**
5. Name it "COMP 536 Course"
6. Set expiration to after the semester ends
7. Check these scopes:
   - ✓ repo (all)
   - ✓ workflow (if using GitHub Actions)
8. Click **Generate token**
9. **COPY THE TOKEN NOW!** You won't see it again!

**Save your token securely:**

```bash
# Configure Git to remember credentials (so you don't paste token every time)
git config --global credential.helper cache  # Linux/Mac: remembers for 15 min
git config --global credential.helper manager  # Windows: saves permanently

# First time you push, Git asks for:
# Username: your-github-username
# Password: paste-your-token-here (NOT your GitHub password!)
```

:::{warning} Token vs Password

When Git asks for "password", paste your TOKEN, not your actual GitHub password!
The token acts as your password for Git operations.
:::

## The Essential Five Commands

Master these five commands and you can use Git for this entire course:

| Command | Purpose |
|---------|---------|
| `git status` | What's changed? (USE THIS CONSTANTLY) |
| `git add .` | Stage all changes for commit |
| `git commit -m "message"` | Save changes with description |
| `git push` | Upload to GitHub |
| `git pull` | Download latest changes |

### ✅ Git Habits We Expect in COMP 536

Git isn't just "submission plumbing" — it's part of your modeling workflow. In this course, we expect a few professional habits:

- **Commit small, commit often.** Aim for *at least* one commit per work session (more when you make meaningful progress).
- **Push early, push often.** Treat GitHub as your offsite backup. If your laptop dies, your work should still exist.
- **One idea per commit.** A commit should represent a single logical change (e.g., "implement leapfrog step," not "did 12 things").
- **Commit messages should be descriptive.** Future-you should understand *what changed* and *why*.
- **Use `git status` constantly.** If you're unsure what's happening, run `git status` before doing anything else.

**Rule of thumb:** if it would hurt to lose the last 30 minutes of work, you should probably commit + push.

:::{warning} This section is being revised
GitHub Classroom was retired by GitHub on **28 August 2026**. This course uses
[Classroom50](https://github.com/foundation50/classroom50/wiki) instead, and the
assignment workflow described below will be updated before you need it. The
`git` and GitHub concepts here — commits, branches, remotes, push/pull — are
unchanged and still exactly what you need to learn.

Follow the workflow demonstrated in class over the steps written here.
:::

## GitHub Classroom: Assignment Workflow

:::{important} How GitHub Classroom Works

GitHub Classroom automates assignment distribution and collection:

1. Professor creates assignment with starter code
2. You get a personalized repository (forked from template)
3. You work and push changes
4. **Your last push before deadline = your submission**
5. Professor sees all submissions automatically

No uploading files, no Canvas submissions, no "did you get my email?"

**Note**: As of 2024, GitHub Classroom creates student repos as forks, allowing professors to update starter code even after you've accepted the assignment.
:::

### Accepting Your First Assignment

1. **Click assignment link** (provided on Canvas/Slack)
   - Link looks like: `https://classroom.github.com/a/xyz123`

2. **Accept the assignment**
   - First time: Authorize GitHub Classroom
   - Select your name from the roster
   - Click "Accept this assignment"

3. **Wait for repository creation** (~30 seconds)
   - You'll see "Your assignment has been created"
   - Click the link to your repository

4. **Your repository is created!**
   - URL format: `github.com/comp536/project1-yourusername`
   - This is YOUR personal copy

### Working on Assignments

```bash
# 1. Clone your assignment repository
git clone https://github.com/comp536/project1-yourusername.git
cd project1-yourusername

# 2. Work on your code
# Edit files, test, debug...

# 3. Check what's changed
git status

# 4. Stage your changes
git add .

# 5. Commit with descriptive message
git commit -m "Implement stellar mass calculation"

# 6. Push to GitHub (this is your submission!)
git push
```

:::{warning} Critical: Submission = Push

**Your submission is whatever is pushed to GitHub by the deadline!**

- No "submit" button needed
- Push early, push often
- You can push unlimited times before deadline
- Check GitHub.com to verify your code is there
:::

### Verifying Your Submission

Always verify your submission:

1. Go to your repository on GitHub.com
2. Check that your latest changes are visible
3. Look for the green checkmark on your commit
4. Check the timestamp (must be before deadline!)

:::{tip} Pro Tip: Push Early and Often

*Don't wait until 11:59 PM to push!* Push every time you make progress:

- Implemented a function? Push.
- Fixed a bug? Push.
- Added comments? Push.

This way you always have a submission, even if something goes wrong at the last minute.
:::

## Basic Git Workflow

Let's practice the complete workflow:

### Creating a New Repository

```bash
# Create project folder
mkdir my_analysis
cd my_analysis

# Initialize Git repository
git init

# Create a Python file
echo "print('Hello COMP 536!')" > hello.py

# Create a .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.ipynb_checkpoints/
.pytest_cache/
.vscode/
.idea/
*.swp
*.swo

# Personal
scratch/
notes_to_self.txt
EOF

# Check status
git status

# Add everything
git add .

# First commit
git commit -m "Initial commit with hello.py and .gitignore"
```

### Daily Workflow Cycle

```bash
# Start of work session
git pull                     # Get latest changes (if working with others)

# ... do your work ...

git status                    # What changed?
git diff                      # See specific changes
git add .                     # Stage everything
git commit -m "Clear message" # Save snapshot
git push                      # Backup to cloud
```

### 🧠 Git History + AI: Why We Care

Later in the semester, you may be allowed to use AI tools in limited, structured ways (see the course **AI Use & Growth Mindset Policy**). When that happens, **Git history becomes part of your scientific record**:

- It shows **how your solution evolved** over time (not just the final answer).
- It helps you **debug responsibly** by identifying exactly when a bug was introduced.
- It supports academic integrity by making your work **traceable and explainable**.

**Practical expectation:** even if you use AI later, you should still be able to explain every line you submit — and your commit history should reflect your own reasoning and decisions.

## Writing Good Commit Messages

:::{tip} Commit Message Best Practices

**Good messages** explain what and why:

- "Fix energy conservation bug in leapfrog integrator"
- "Add mass-luminosity relationship for main sequence stars"
- "Optimize N-body force calculation with spatial hashing"

**Bad messages** are vague or useless:

- "Fixed stuff"
- "asdfasdf"
- "done"
- "why won't this work"

Future you will thank current you for clear messages!
:::

### Commit Message Format

For longer commits:

```bash
git commit
# Opens editor for multi-line message:

# Fix incorrect gravitational constant in N-body simulation
#
# The constant was off by a factor of 4pi due to unit conversion
# error. This affected all orbital period calculations.
#
# Fixes #12
```

## Common Scenarios and Solutions

### "I Forgot to Pull First"

```bash
git push
# Error: failed to push some refs...

# Solution:
git pull
# If there are conflicts, resolve them (see below)
git push
```

### "I Made a Mistake in My Last Commit"

```bash
# Fix the file
# Then amend the commit
git add .
git commit --amend -m "New message"
git push --force  # Only if you already pushed!
```

### "I Need to Undo Changes"

```bash
# Discard changes to specific file (not staged)
git checkout -- file.py

# Undo last commit but keep changes
git reset --soft HEAD~1

# Nuclear option: discard ALL local changes
git reset --hard HEAD
```

### Merge Conflicts

When Git can't automatically merge:

1. Git marks conflicts in files:

```python
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> branch-name
```

2. Edit file to resolve:

```python
# Keep the version you want (or combine them)
combined final version
```

3. Complete the merge:

```bash
git add .
git commit -m "Resolve merge conflict"
git push
```

## Quick Reference Card

| Command | What it does |
|---------|--------------|
| **Basic Workflow** | |
| `git init` | Create new repository |
| `git clone <url>` | Copy repository from GitHub |
| `git status` | Show what's changed |
| `git add <file>` | Stage specific file |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save snapshot with message |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| **Viewing History** | |
| `git log` | Show commit history |
| `git log --oneline` | Compact history view |
| `git log --graph` | Visual branch history |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |
| **Undoing Things** | |
| `git checkout -- <file>` | Discard changes to file |
| `git reset HEAD <file>` | Unstage file |
| `git reset --soft HEAD~1` | Undo last commit, keep changes |
| `git reset --hard HEAD` | Discard ALL local changes |
| `git revert <commit>` | Undo specific commit |
| **Branches** (Advanced) | |
| `git branch` | List branches |
| `git branch <name>` | Create branch |
| `git checkout <branch>` | Switch branches |
| `git merge <branch>` | Merge branch into current |

## Practice Exercises (optional but recommended)

### Exercise 1: Your First Repository (15 min)

1. Create a new repository called `git-practice`
2. Add a Python file with a simple function
3. Create a proper `.gitignore`
4. Make your first commit
5. Create a README.md file
6. Make a second commit
7. View your history with `git log`

### Exercise 2: GitHub Workflow (20 min)

1. Create a repository on GitHub.com (New $\to$ Repository)
2. Clone it locally
3. Add your practice code
4. Push to GitHub
5. Verify on GitHub.com
6. Make changes on GitHub.com (edit README)
7. Pull changes locally

### Exercise 3: Recovery Practice (15 min)

1. Make some changes to a file
2. Use `git diff` to see changes
3. Discard changes with `git checkout`
4. Make new changes and commit them
5. Undo the commit with `git reset --soft HEAD~1`
6. Recommit with a better message

## Git Proficiency Checklist

You're ready for this course when you can:

- [ ] Clone a repository from Classroom50
- [ ] Make changes and commit them with clear messages
- [ ] Push changes to GitHub
- [ ] Check status and diff before committing
- [ ] Recover from basic mistakes
- [ ] Verify your submission on GitHub.com

**All checked?** You're ready to use Git for all assignments!

## Troubleshooting

:::{warning} Common Issues and Fixes
:class: dropdown

### "Permission denied (publickey)"

- You're using SSH but haven't set up keys
- Use HTTPS URLs instead: `https://github.com/...`
- Or set up SSH keys (see GitHub docs)

### "Authentication failed"

- Personal Access Token issue
- Create new token following steps above
- Make sure to paste TOKEN, not password

### "Cannot push to repository"

- Check you're in the right directory: `pwd`
- Verify remote URL: `git remote -v`
- Make sure you have commits: `git log`

### "Large files" error (>100MB)

- Git won't accept huge files
- Add to `.gitignore`: `*.fits`, `*.hdf5`, etc.
- Use `git rm --cached largefile` to remove

### "Accidentally committed sensitive data"

- DO NOT push yet!
- Remove with: `git reset --hard HEAD~1`
- If already pushed, contact instructor immediately
:::

## Beyond Basics: Useful Features

:::{note} Level Up Your Git Skills
:class: dropdown

**Stashing** (temporary storage):

```bash
git stash          # Save changes temporarily
git stash pop      # Restore changes
```

**Viewing specific commits**:

```bash
git show abc123    # Show specific commit
git diff HEAD~2    # Compare with 2 commits ago
```

**Finding bugs with bisect**:

```bash
git bisect start
git bisect bad      # Current version is broken
git bisect good v1.0  # v1.0 was working
# Git helps you find when bug was introduced
```

**Aliases for efficiency**:

```bash
git config --global alias.st status
git config --global alias.cm commit
git config --global alias.br branch
# Now use: git st, git cm, etc.
```
:::

## Resources

- **Official Git Book** (free): <https://git-scm.com/book>
- **GitHub's Tutorial**: <https://try.github.io>
- **Visual Git Guide**: <https://marklodato.github.io/visual-git-guide/>
- **Oh Shit, Git!?!**: <https://ohshitgit.com> (recovery from mistakes)
- **Classroom50 Wiki**: <https://github.com/foundation50/classroom50/wiki>

## Next Steps

1. Git is configured
2. GitHub account ready
3. Can clone, commit, and push
4. $\to$ Accept your first assignment on Classroom50!

---

**Remember:** Git seems complex but you only need ~5 commands for this course. Focus on the essential workflow: `status`, `add`, `commit`, `push`, `pull`. Everything else is optional!
