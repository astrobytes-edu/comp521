---
title: "Chapter 2: Software Setup"
subtitle: "A minimal Python and notebook environment for COMP 521"
author: "Anna Rosen"
---

This chapter installs the supported course baseline:

- **Miniforge**, which provides Python and the `conda` environment manager;
- one isolated environment named `comp521`; and
- **VS Code** with the Python and Jupyter extensions.

Project 1 needs NumPy, Matplotlib, and a notebook kernel. Later project briefs
will name any additional packages they require.

:::{note} If you cannot install software
The normal Miniforge installation is per-user and should not need administrator
access. If you use a managed computer, lack installation permission, or need an
accessible alternative, contact the instructor through Canvas Inbox instead of
trying system-level workarounds.
:::

## Why use an environment?

An environment is a named collection of one Python interpreter and its
packages. Activating `comp521` gives course work a stable place without
modifying the Python that your operating system may use.

```text
computer
├── system software        ← leave this alone
└── comp521 environment    ← course Python and packages
```

Isolation prevents many package conflicts. It does not, by itself, make every
computer byte-for-byte identical; project repositories and project-specific
instructions own any stricter dependency contract.

## Step 1: Install Miniforge

Download the installer for your operating system and processor from the
[official Miniforge download page](https://conda-forge.org/download/).

::::::{tab-set}

:::::{tab-item} macOS
1. If you are unsure which processor you have, run `uname -m` in Terminal.
   `arm64` means Apple Silicon; `x86_64` means Intel.
2. Download the official signed `.pkg` installer for
   [Apple Silicon](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.pkg)
   or
   [Intel](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.pkg),
   then open the downloaded package.
3. Install for your user, accept the default location, and allow the installer
   to initialize your shell.
4. Close every Terminal window and open a new one.
:::::

:::::{tab-item} Linux
1. Download the matching Linux shell installer.
2. In Terminal, go to the directory containing it, usually
   `cd ~/Downloads`.
3. Run the downloaded installer, for example:

   ```bash
   bash Miniforge3-Linux-x86_64.sh
   ```

   Use the actual filename you downloaded. Accept the default user location and
   answer yes when asked to initialize conda.
4. Close the terminal and open a new one.
:::::

:::::{tab-item} Windows
1. Install the matching Windows Miniforge installer for **Just Me**, using the
   default location.
2. Open **Miniforge Prompt** from the Start menu and run:

   ```bash
   conda init bash
   ```

3. Close Miniforge Prompt and all Git Bash windows, then open a new **Git
   Bash** window.

This connects the Miniforge installation to the Bash terminal used in Chapter
1. The route will receive its required clean-Windows rehearsal before release;
if `conda` is not found, preserve the exact message and use the help route
below instead of changing system `PATH` entries by guesswork.
:::::

::::::

Verify the installation in a fresh terminal:

```bash
conda --version
```

A version number is success. If the command is not found, first confirm that
you opened a new terminal after installation.

## Step 2: Create the course environment

Create the minimal P1 environment once:

```bash
conda create --name comp521 python=3.11 numpy matplotlib jupyter ipykernel gh
```

Review the proposed package plan, then enter `y` when conda asks whether to
proceed. Activate the environment:

```bash
conda activate comp521
```

Your prompt should now include `(comp521)`. Verify the interpreter and core
imports:

```bash
which python
python --version
python -c "import numpy, matplotlib; print('COMP 521 imports work')"
gh --version
```

The Python path should point inside the `comp521` environment, Python should
report version 3.11, the import command should print its success message, and
`gh` should report a GitHub CLI version. Installing `gh` in the same
cross-platform environment gives every supported operating system the browser
authentication path used in Chapter 3.

### Daily environment commands

| Command | Purpose |
|---|---|
| `conda activate comp521` | enter the course environment |
| `conda deactivate` | leave the current environment |
| `conda env list` | show available environments |
| `conda list` | show packages in the active environment |
| `which python` | show which Python this shell will run |

:::{important} Add packages only when the course asks for them
Do not run `conda update --all`, mix in arbitrary `pip install` commands, or
install the entire scientific Python ecosystem preemptively. When a later
project needs another package, follow that project's exact instruction. This
keeps the environment smaller and troubleshooting evidence clearer.
:::

## Step 3: Install VS Code

1. Download and install [Visual Studio Code](https://code.visualstudio.com/).
2. Open the Extensions view with `Ctrl + Shift + X` (Windows/Linux) or
   `Command + Shift + X` (macOS).
3. Install these two extensions from Microsoft:
   - **Python**
   - **Jupyter**

No theme, formatter, AI assistant, or extension bundle is required.

### Open a project and select its kernel

From a project directory, try:

```bash
code .
```

If `code` is not available in your shell, use **File → Open Folder** in VS
Code. On macOS you may optionally install the shell command from the Command
Palette with **Shell Command: Install 'code' command in PATH**.

For a Python file, open the Command Palette and choose **Python: Select
Interpreter**, then select `comp521`. For a notebook, use the kernel picker at
the upper right and select the Python kernel from `comp521`. VS Code records
this choice per project folder.

### Local notebook check

Create an untitled notebook only for this check, select the `comp521` kernel,
and run:

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.0, 1.0, 5)
plt.plot(x, x**2, marker="o")
plt.xlabel("x")
plt.ylabel("x²")
plt.show()
```

Success means the cell completes and displays one labeled curve. Close the
untitled notebook without saving; the official readiness evidence must be run
and saved in your assigned P1 `analysis.ipynb`.

## AI completion settings

The authoritative rules are in the [AI Use & Growth Mindset
Policy](../01-course-info/ai-policy.md). During Projects 1–3, automatic
AI-generated code completions must be disabled because core solution code is
your work. Disable Copilot, Cursor-style completion, or any comparable
generative extension if it is installed.

Normal editor features such as syntax highlighting, bracket matching,
documentation pop-ups, and ordinary IntelliSense may remain enabled. The policy
also permits defined tutoring and verification uses after a genuine attempt;
it does not impose a blanket ban on asking for explanations.

## Setup evidence

Before continuing, confirm:

- [ ] A new terminal recognizes `conda`.
- [ ] `conda activate comp521` changes the prompt.
- [ ] `which python` points inside the `comp521` environment.
- [ ] NumPy and Matplotlib import without error.
- [ ] `gh --version` reports a GitHub CLI version.
- [ ] VS Code has the Microsoft Python and Jupyter extensions.
- [ ] A notebook can select the `comp521` kernel and display the test plot.
- [ ] Automatic AI code completion is disabled for the Phase 1 projects.

This is the **local setup check**. The recorded P1 technical-readiness check is
completed after you receive and push your assigned repository in Chapter 3.

## Troubleshooting from evidence

| Symptom | Bounded next step |
|---|---|
| `conda: command not found` | Open a new terminal. Confirm Miniforge installed for your user. On Windows, try the exact `conda init bash` step from Miniforge Prompt once. |
| `EnvironmentNameNotFound: comp521` | Run `conda env list`. If the environment is absent, repeat the create command; if it exists under another name, preserve the output and ask for help. |
| `ModuleNotFoundError` | Run `conda activate comp521`, `which python`, and `conda list <package>`. |
| VS Code shows the wrong Python | Open the project folder, then select the `comp521` interpreter or kernel again. |
| Kernel will not start | Record the VS Code notification and Jupyter output; confirm `python -c "import ipykernel"` works in the active environment. |
| Installation stalls or cannot reach a server | Save the complete network error and try the same command once on a stable network. Do not add an unknown proxy or clear caches blindly. |

Post a shared setup question on the Canvas discussion board or use Canvas Inbox
for a private issue. Include your operating system, exact command or UI action,
complete error, and the outputs of `conda env list` and `which python` when
relevant.

:::{important} Ready for Git
Continue when a fresh terminal can activate `comp521` and VS Code can run a
notebook using that kernel.
:::
