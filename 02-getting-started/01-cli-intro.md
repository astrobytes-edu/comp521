---
title: "Chapter 1: The Command Line"
subtitle: "Navigate, inspect, and run a project safely"
author: "Anna Rosen"
---

The terminal is a text interface to your computer. In COMP 521 you will use it
for a small, repeatable set of tasks: enter a project directory, activate an
environment, run code, and use Git. You do not need to memorize a catalog of
commands.

## Before you begin

### Open the course terminal

::::::{tab-set}

:::::{tab-item} macOS
Open **Terminal** from Applications → Utilities, or search for it with
`Command + Space`.
:::::

:::::{tab-item} Linux
Open your distribution's **Terminal** application. `Ctrl + Alt + T` works on
many systems.
:::::

:::::{tab-item} Windows
The examples on this page use Bash commands. If **Git Bash** is not installed,
install [Git for Windows](https://git-scm.com/download/win) using its default
options, then open **Git Bash** from the Start menu. This also installs Git for
Chapter 3.

Do not use Command Prompt for this reading: its file commands and path syntax
are different. PowerShell is a capable shell, but it is not the course's
documented beginner path.
:::::

::::::

:::{important} A safe terminal habit
Commands can change files immediately. Before deleting anything, run `pwd`,
list the exact target, and prefer `rm -i` while practicing. Never paste a
deletion command you do not understand. If a path or wildcard surprises you,
stop.
:::

## Terminal, shell, and prompt

- The **terminal** is the application window.
- The **shell** reads the commands you type. This page uses Bash-compatible
  commands.
- The **prompt** is the text before your cursor. It may show your computer,
  current folder, or active environment.
- The **command line** is where you enter a command.

A command usually has this shape:

```text
command  option  argument
ls       -la     project
```

Here `ls` is the action, `-la` changes how it behaves, and `project` is
the target. Type only the command—not the explanatory prompt characters shown
in some documentation.

## Your navigation loop

These three commands answer the questions you will ask most often.

### Where am I? — `pwd`

```bash
pwd
```

`pwd` prints the full path to your current directory.

### What is here? — `ls`

```bash
ls
ls -la
```

`ls` lists visible files. `ls -la` adds hidden files and details. A name
beginning with `.`, such as `.gitignore`, is hidden by convention.

### How do I move? — `cd`

```bash
cd Documents
cd ..
cd ~
```

- `cd Documents` enters a directory named `Documents`.
- `cd ..` moves to its parent.
- `cd ~` returns to your home directory.

Directory names are case-sensitive in the course examples. Use **Tab
completion** instead of retyping a long path: type its first few characters,
then press `Tab`.

:::{tip} First checkpoint
Move into one directory and back. After every `cd`, run `pwd` and `ls`
until the path changes make sense. If you can recover with `cd ~`, you have
the core skill.
:::

## Paths: directions to a file

An **absolute path** starts at the filesystem root and identifies one location:

```text
/Users/yourname/Documents/comp521/project-1
```

A **relative path** starts from your current directory:

```text
project-1/analysis.ipynb
```

Useful path symbols are:

| Symbol | Meaning |
|---|---|
| `~` | your home directory |
| `.` | the current directory |
| `..` | the parent directory |
| `-` | the previous directory when used as `cd -` |

Paths containing spaces need quotes:

```bash
cd "My Projects"
```

For course work, prefer simple directory names such as `comp521` and
`project-1`.

## Create, inspect, copy, and move

Make a harmless practice workspace:

```bash
cd ~
mkdir comp521_cli_practice
cd comp521_cli_practice
touch notes.txt
ls -la
```

Now inspect and rename the file:

```bash
cat notes.txt
cp notes.txt notes-backup.txt
mv notes.txt observations.txt
ls -la
```

| Command | Purpose |
|---|---|
| `mkdir directory` | create a directory |
| `touch file` | create an empty file, or update its timestamp |
| `cat file` | print a short text file |
| `cp source target` | copy a file |
| `mv source target` | move or rename a file |

Use `less file.txt` for a long text file; press `q` to quit. Use
`head file.txt` or `tail file.txt` to inspect its beginning or end.

### Remove only what you have identified

```bash
rm -i observations.txt
rmdir an_empty_directory
```

`rm -i` asks before removing each file. `rmdir` removes only an empty
directory, so it is the right teaching tool for an empty-directory example.

:::{warning} Stop before recursive or forced deletion
`rm -r`, `rm -f`, and especially `rm -rf` can remove many files without
an ordinary undo path. They are not needed for this module. If instructions
seem to require one of them, verify the exact directory with the instructor
first.
:::

## Find files and text

You do not need to click through every directory to locate something:

```bash
find . -name "*.py"
grep -n "flux" analysis.py
grep -r -n "TODO" .
```

- `find . -name "*.py"` finds Python files below the current directory.
- `grep -n` prints matching lines and their line numbers.
- `grep -r` searches recursively.

The `*` is a **wildcard**: it matches multiple characters. Quote the pattern
in the `find` command so the shell does not expand it too early.

## Run Python from the project directory

After you create the course environment in Chapter 2, the usual loop is:

```bash
cd path/to/your/project
conda activate comp521
which python
python script.py
```

On Windows Git Bash, `which python` may print a path under Miniforge. On all
platforms, the important observation is that the active Python belongs to the
`comp521` environment.

Use `Ctrl + C` to interrupt a running command. This asks the program to stop;
it does not undo work the program already completed.

## Read errors before changing anything

| Message | What it establishes | First evidence to collect |
|---|---|---|
| `command not found` | This shell could not locate that executable. | Check spelling, installation, `echo $PATH`, and the active environment. |
| `No such file or directory` | The path given does not resolve here. | Run `pwd` and `ls`; inspect one path component at a time. |
| `Permission denied` | The requested action is not allowed for this user or file. | Run `ls -l` and ask for help; do not add `sudo` as a guess. |
| Python traceback | Python reports the call path and final exception. | Save the complete traceback and read the final line first. |

A fresh terminal starts a fresh shell session. It can reset session state such
as the active conda environment, but it does **not** undo commands or restore
files.

## Keyboard shortcuts worth learning

| Key | Effect |
|---|---|
| `Tab` | complete a file or command name |
| `↑` / `↓` | move through command history |
| `Ctrl + C` | interrupt the current command |
| `Ctrl + A` / `Ctrl + E` | move to the beginning/end of the line |
| `Ctrl + L` | clear the visible terminal |

## Optional: combine small commands

A pipe sends one command's output to the next:

```bash
ls -la | grep -E '\.ipynb$'
```

Redirection saves output:

```bash
python script.py > output.txt
```

`>` replaces the target file; `>>` appends. Inspect the target name before
using either. These are reference skills, not prerequisites for P1 readiness.

## Proof task

Without using Finder or File Explorer:

1. Go to your home directory.
2. Create `comp521_cli_practice/project-1`.
3. Enter `project-1` and confirm its absolute path.
4. Create `notes.txt`, copy it to `notes-backup.txt`, and list both files.
5. Return to your home directory using one command.

Keep the practice directory; you can revisit it without deleting anything.

:::{important} Ready for software setup
Continue when you can explain what `pwd`, `ls`, and `cd` tell you, use Tab
completion, and identify a file before moving or removing it.
:::
