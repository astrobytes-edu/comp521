---
title: "Chapter 3: Git, GitHub, and Classroom50"
subtitle: "Record, push, and verify your work"
author: "Anna Rosen"
---

Git records snapshots of a project on your computer. GitHub stores the commits
you push to a remote repository. Classroom50 gives each student the assigned
course repository.

:::{important} What Git protects
Committed work is recorded locally; pushed work is also stored on GitHub.
Uncommitted and untracked files are not protected by Git, so inspect, commit,
and push meaningful progress regularly.
:::

## Step 1: Install and verify Git

::::::{tab-set}

:::::{tab-item} macOS
Run:

```bash
git --version
```

If macOS offers to install its command-line developer tools, accept that
installation, then open a fresh terminal and run the check again.
:::::

:::::{tab-item} Linux
Try `git --version` first. If Git is absent, install it with your
distribution's package manager, for example `sudo apt install git` on
Ubuntu/Debian or `sudo dnf install git` on Fedora. These commands install a
named system package; do not generalize `sudo` to ordinary course commands.
:::::

:::::{tab-item} Windows
If you installed Git Bash in Chapter 1, Git is already installed. Open Git Bash
and run:

```bash
git --version
```

If the command is absent, install [Git for
Windows](https://git-scm.com/download/win) using its default options and reopen
Git Bash.
:::::

::::::

## Step 2: Identify your commits

Configure the name and email that Git writes into new commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git config --global init.defaultBranch main
git config --global --list
```

Use an email connected to your GitHub account, or a GitHub-provided private
commit email if you do not want a personal address in commit metadata.

## Step 3: Sign in safely

Create a GitHub account if you do not already have one and enable two-factor
authentication. Joining the course does **not** require the Student Developer
Pack, GitHub Copilot, or a classic personal access token.

Activate the course environment and use the installed GitHub CLI to configure
one cross-platform HTTPS credential path:

```bash
conda activate comp521
gh auth login --web --git-protocol https
gh auth setup-git
gh auth status
```

Follow the browser or device-code prompt and sign into the GitHub account you
will use for the course. `gh auth setup-git` configures GitHub CLI as Git's
credential helper; `gh auth status` confirms the account and reports where
the credential is stored. The P1 invitation separately asks you to authorize
Classroom50 with that GitHub account.

:::{warning} Do not improvise a broad token
If a terminal asks for a password or authentication fails, do not create a
classic token with broad `repo` or `workflow` access just to get past the
prompt. Preserve the exact message and use GitHub's current
[authentication documentation](https://docs.github.com/en/authentication) or
the course help route. Never paste a token, password, or recovery code into
Canvas, an AI tool, or a screenshot.

If `gh auth status` reports that it stored a credential in plain text rather
than an operating-system credential store, stop and bring that exact output to
the instructor before cloning the course repository.
:::

## The five-part Git loop

| Step | Command | Question it answers |
|---|---|---|
| Inspect | `git status` | Which files changed, and what is staged? |
| Review | `git diff` | What changed in tracked text files? |
| Stage | `git add <path>` or `git add -A` | Which changes belong in this commit? |
| Record | `git commit -m "message"` | What project state am I preserving? |
| Share | `git push` | Which local commits am I sending to GitHub? |

`git add` does not upload anything. It selects content for the next commit.
`git commit` records that staged state locally. `git push` transfers commits
to GitHub.

### Choose the staging scope deliberately

All three of these forms are useful:

| Command | What it stages | When to use it |
|---|---|---|
| `git add analysis.ipynb README.md` | Only the named paths | The commit should contain a specific subset of the work. |
| `git add .` | Changes at and below the current directory | You are at the repository root and all visible changes belong to one coherent checkpoint. |
| `git add -A` | All additions, modifications, and deletions anywhere in the repository | The whole repository state belongs in the checkpoint, even if your terminal is in a subdirectory. |

`git add .` and `git add -A` are normal course-workflow commands, not mistakes.
Their scope is simply broader than naming files. Inspect that scope before and
after staging:

```bash
git status
git diff
git add .
git status
git diff --staged
git commit -m "Complete transit branch checks"
git push
```

Run `git add .` from the repository root when you mean “this whole project.” If
unrelated files appear in `git status`, stage named paths instead. For readable
text files, `git diff --staged` shows the exact staged lines. A notebook is
structured JSON, so `git diff --staged --stat` plus a clean restart-and-run
check is usually more useful. Never stage credentials, excluded datasets, or
machine-specific files merely because a broad command found them.

## Classroom50 and Project 1

:::{warning} Course-specific acceptance UI
The invitation and acceptance screens are scheduled for a fresh-student
rehearsal on **August 20**. The durable route below is the current course
contract; the final invitation link and any interface-specific directions will
be posted in Canvas after that rehearsal.
:::

Classroom50 is the assignment-distribution service for COMP 521. Its current
[student web guide](https://github.com/foundation50/classroom50/wiki/Web-Student-Guide)
describes GitHub authorization and repository creation. The course-specific
project brief and Canvas invitation take precedence over a generic service
example.

### Accept and clone P1

1. Open the **Project 1 Classroom50 invitation** in Canvas.
2. Follow the Classroom50 acceptance prompts and open the repository assigned to
   your GitHub account.
3. On that repository's GitHub page, copy its HTTPS clone URL.
4. In Git Bash or Terminal, go to the parent directory where you keep course
   projects, then clone the URL:

   ```bash
   git clone PASTE_THE_HTTPS_URL_HERE
   cd NAME_OF_THE_CLONED_FOLDER
   git status
   ```

Use the actual URL and folder name shown for your repository. Do not create,
fork, or rename a substitute repository.

### Complete the P1 readiness checkpoint

1. Activate the course environment:

   ```bash
   conda activate comp521
   ```

2. Open the cloned folder in VS Code, select the `comp521` notebook kernel,
   open `analysis.ipynb`, run its tagged readiness cell, and save the notebook
   with the success message visible.
3. Return to the terminal in that repository and run:

   ```bash
   git status
   git add analysis.ipynb
   git diff --staged --stat
   git commit -m "Complete P1 technical readiness check"
   git push
   ```

4. Open the repository on GitHub. Verify all three observations:
   - the new commit appears;
   - `analysis.ipynb` contains the saved success output; and
   - the **P1 readiness** GitHub Actions check is green.

For this checkpoint, a successful push plus the green check records completion;
there is no separate file upload. For later assignments, follow the exact
project brief: Classroom50 can also support configurations with an explicit
submission action, so “last push always equals submission” is not a universal
rule.

## A daily project workflow

At the beginning of a work session:

```bash
cd path/to/your/project
conda activate comp521
git status
```

During the session, work in one coherent slice and run the smallest relevant
check. At a useful checkpoint, choose a staging command whose scope matches the
checkpoint:

```bash
git status
git diff
git add .
```

From the repository root, `git add .` stages the project changes shown by
`git status`. Use `git add -A` when you intend to stage the complete repository
state from any subdirectory, or name paths when the commit should contain only
part of the work. Then inspect and record the staged state:

```bash
git status
git diff --staged
git commit -m "Explain the completed change"
git push
```

Good messages name the outcome:

- `Implement all four transit overlap cases`
- `Add boundary checks for flux model`
- `Interpret HR diagram radius trends`

Messages such as `stuff`, `done`, or `final final` do not help you recover
the reasoning later.

### When should you pull?

`git pull` incorporates commits already on GitHub that your local branch does
not have. In an individual course repository, you usually need it only if you
edited on GitHub, worked from another computer, or the instructor explicitly
added a commit. Do not use `pull` as a generic response to every push error;
read the error first.

## Safe beginner recovery

Always start with `git status`. If you are unsure whether work is recoverable,
make a copy outside the repository or ask for help before running an undo
command.

### I staged the wrong file

```bash
git restore --staged path/to/file
```

This removes the file from the next commit but keeps its working copy.

### I want to discard an uncommitted edit to one tracked file

First inspect `git diff path/to/file`. If you are certain none of those edits
should survive:

```bash
git restore path/to/file
```

This is destructive for that file's uncommitted edits. It does not recover
untracked files.

### A committed change needs to be undone

Locate it with `git log --oneline`. In a shared or already-pushed history,
`git revert COMMIT_ID` creates a new commit that reverses the selected change.
Ask for help before doing this the first time.

### A push is rejected

Save the entire error and run:

```bash
git status
git remote -v
git log --oneline -5
```

Do **not** use `--force` or `reset --hard`. Those commands can discard work
or rewrite shared history and are not part of the course's normal recovery
path.

### A credential or secret entered a commit

Revoke or rotate the credential immediately, even if you have not pushed it.
Then contact the instructor for history-cleanup help. Deleting the visible line
does not make an exposed secret safe again.

## Individual work and collaboration

Course projects may include paired scientific discussion, but each student
writes, understands, and submits their own implementation and interpretation.
Do not add classmates as code collaborators or exchange solution repositories
unless a project brief explicitly changes that rule. See the
[project collaboration policy](../01-course-info/projects.md#sec-pairs).

## Readiness checklist

- [ ] `git --version` works.
- [ ] My Git name and email are configured.
- [ ] `gh auth status` shows the GitHub account I use for the course.
- [ ] I can distinguish working, staged, committed, and pushed changes.
- [ ] I use `git status`, choose an appropriate staging scope (`<path>`, `.`,
      or `-A`), and inspect the staged result before each commit.
- [ ] I cloned the assigned P1 repository from its actual Classroom50 route.
- [ ] My saved readiness notebook is visible on GitHub.
- [ ] The **P1 readiness** check is green.

## References

- [Pro Git book](https://git-scm.com/book/en/v2)
- [Git reference manual](https://git-scm.com/docs)
- [GitHub authentication documentation](https://docs.github.com/en/authentication)
- [Classroom50 student web guide](https://github.com/foundation50/classroom50/wiki/Web-Student-Guide)

:::{important} The essential habit
Use `status` to observe, choose the right staging scope, inspect what is staged,
describe the checkpoint in the commit message, push, and verify the result on
GitHub.
:::
