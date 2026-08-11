---
title: "Chapter 2: Software Setup Guide"
subtitle: "COMP 536: Computational Modeling for Scientists"
author: "Anna Rosen"
---


# Chapter 2: Software Setup Guide

:::{note} Before You Start

**System Requirements**:

- 3 GB free disk space (Miniforge ~400 MB + packages ~1-2 GB)
- Stable internet connection (will download ~800 MB total)
- Administrator privileges on your computer
- ~30 minutes of uninterrupted time

**If on campus**: Use eduroam WiFi, not guest network (firewall issues)

**Want more details?** See the [official conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
:::

## Setup Roadmap

Total time: ~30 minutes

:::{tip} Your Setup Journey

1. **Step 1**: Install Python with Miniforge
2. **Step 2**: Create your course environment
3. **Step 3**: Install VS Code editor
4. **Step 4**: Verify everything works
5. **Step 5**: Quick practice session
:::

## Understanding the Setup (2-minute read)

Your computer probably already has Python, but it's used by your operating system. Touching it could break things. We need:

- **Our own Python**: Separate from system Python (that's what Miniforge provides)
- **Isolated workspace**: A bubble for course packages (that's the conda environment)
- **Code editor**: A professional tool for writing code (that's VS Code)

Think of it like setting up a chemistry lab—you need the right equipment in a clean, isolated space where experiments won't affect anything else.

:::{note} Want to Learn More?
:class: dropdown

For deeper understanding of conda and environments, see:

- [Official conda user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Why use conda environments?](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html)
:::

:::{note} Keep This Open

**Terminal Basics** (you'll need these commands throughout):

- Where am I? $\to$ `pwd`
- What's here? $\to$ `ls`
- Move to folder $\to$ `cd foldername`
- Go back $\to$ `cd ..`
- Copy-paste works! (Ctrl+Shift+V on Linux/Windows, Cmd+V on Mac)
:::

### 🧪 When Setup Fails: Treat Errors as Data (not as a verdict)

If something breaks during setup, you didn't "do it wrong." You just learned something specific about your machine.

Use this quick recovery loop:

1. **Read the last 3–5 lines** of the error (the useful part is usually at the bottom).
2. **Copy the exact error text** (screenshots are fine too).
3. Try the simplest reset:
   - Close and reopen your terminal
   - Re-run: `conda activate comp536`
4. If it still fails, ask for help **with the full error text** (not "it doesn't work").

**Rule:** vague errors get vague answers. Precise errors get fast fixes.

## Step 1: Install Python via Miniforge

Miniforge gives us:

- Python + conda package manager (same as Anaconda/Miniconda)
- Free, open-source, no licensing issues
- Works identically on all operating systems
- Default conda-forge channel (community-maintained, most comprehensive)
- Minimal installation (~400 MB vs Anaconda's ~3 GB)

:::{note} Why Miniforge instead of Anaconda?
:class: dropdown

**Miniforge** (~400 MB): Just Python + conda + pip. You install only what you need.
**Anaconda** (~3 GB): Pre-installs 250+ packages (Spyder, Qt, R packages, etc.) you won't use.
**Miniconda** (~400 MB): Minimal like Miniforge but defaults to Anaconda's channel (fewer packages).

Anaconda also has commercial licensing restrictions for organizations >200 people.

For academic work, Miniforge is the best choice: minimal, free, and access to the most packages. [Learn more about conda variants](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
:::

:::{note} Optional (Advanced): What about `uv`?
:class: dropdown

You may see modern Python workflows using **`uv`** (a very fast package + environment tool). It's excellent for many research codebases.

**Why COMP 536 uses Miniforge/conda instead:** conda handles cross-platform scientific packages (compiled libraries) more reliably for a mixed classroom, and it makes everyone's environment consistent.

**When `uv` is a good choice:** once you're comfortable with environments, and you're working on a Python-only project where speed and lockfiles matter. We may revisit `uv` later in the semester as an "industry-style" alternative.
:::

::: {.panel-tabset}

### macOS/Linux

**1. Download Miniforge:**

- Visit <https://conda-forge.org/download/>
- Find and click the installer for your system:
  - **macOS Apple Silicon**: For M1/M2/M3 Macs
  - **macOS x86_64**: For Intel Macs
  - **Linux x86_64**: For standard Linux systems
  - **Linux aarch64**: For ARM-based Linux
- The installer (.sh file) will download to your Downloads folder

:::{note} Not sure which Mac you have?
:class: dropdown

Run `uname -m` in Terminal:

- `arm64` = Apple Silicon (use "macOS Apple Silicon" installer)
- `x86_64` = Intel (use "macOS x86_64" installer)
:::

**2. Navigate to Downloads and run installer:**

```bash
# Go to Downloads folder
cd ~/Downloads

# Check the file downloaded (should be ~80-100 MB)
ls -lh Miniforge3*.sh

# Make it executable (required on some systems)
chmod +x Miniforge3-*.sh

# Run the installer
bash Miniforge3-*.sh
```

**3. Follow prompts:**

- Press ENTER to review license
- Type `yes` to accept
- Press ENTER for default location (recommended)
- Type `yes` for conda init

**4. Activate changes:**

```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS
```

**5. Verify installation:**

```bash
conda --version
```

**Success**: Shows version number like `conda 24.7.1`

### Windows

:::{warning} Windows Users: Important Notes

1. The instructor uses macOS/Linux and hasn't personally tested these Windows instructions
2. Most commands work in "Git Bash" (install Git first if needed)
3. Use "Miniforge Prompt" for pure conda operations
4. If you encounter issues:
   - Google the exact error message (in quotes)
   - Ask ChatGPT/Claude with the full error text
   - Post on Slack with screenshots
   - Find a Windows-using classmate!
:::

**1. Download installer:**

- Visit <https://conda-forge.org/download/>
- Click the "Windows x86_64" installer
- The .exe file (~80 MB) will download to your Downloads folder

**2. Verify download:**

- Open File Explorer $\to$ Downloads folder
- Look for Miniforge3-Windows-x86_64.exe
- If the file is <70 MB, the download failed - try again

**3. Run the installer:**

- Double-click the .exe file
- If you get security warnings, click "Run anyway"
- Right-click $\to$ "Run as Administrator" if you encounter permission issues

**4. Installation wizard:**

- Click Next
- Accept license
- Select "Just Me" (recommended)
- Use default location
- Check "Add Miniforge3 to PATH"
- Install

**5. Open "Miniforge Prompt" from Start Menu**

**6. Verify installation:**

```bash
conda --version
```

**Success**: Shows version number like `conda 24.7.1`

:::

:::{warning} Didn't Work?

If `conda --version` gives "command not found":

1. **Restart your terminal** (most common fix)
2. Check installation path matches what you selected
3. On Windows, use "Miniforge Prompt" not regular Command Prompt
:::

## Step 2: Create Your Course Environment

:::{warning} Keep Your Terminal Open!

Use the same terminal window throughout setup. If you accidentally close it:

1. Open a new terminal
2. Run `conda activate comp536` (after creating it)
3. Continue where you left off
:::

An environment is an isolated workspace. Think of it as a clean room where we can install packages without affecting anything else on your computer.

```bash
# Create environment with Python 3.11
conda create -n comp536 python=3.11
```

When prompted "Proceed ([y]/n)?", type `y` and press Enter.

```bash
# Activate your environment
conda activate comp536
```

**Success Check**: Your prompt now shows `(comp536)` at the beginning

:::{warning} Common Mistake #1

**Forgetting to activate the environment!**

Every time you open a new terminal, you MUST run:

```bash
conda activate comp536
```

No (comp536) in prompt = wrong environment = packages "not found"!
:::

### Install Essential Packages

:::{note} Installation Time

Package installation takes 5-10 minutes depending on internet speed.
If it's taking longer than 15 minutes:

1. Press `Ctrl+C` to cancel
2. Check your internet connection
3. Try again with fewer packages at once
:::

You have two options for package installation:

#### Option 1: Install Everything Now (Recommended)

```bash
# Install all course packages at once
conda install numpy scipy matplotlib pandas jupyter ipython astropy h5py scikit-learn

# Install JAX and jax-related packages separately (can be finicky)
conda install jax jaxlib -c conda-forge
conda install flax optax diffrax lineax optimistix -c conda-forge

# If JAX fails with conda, use pip as fallback:
# pip install --upgrade jax jaxlib
```

*This ensures you won't forget to install something later when you need it!*

#### Option 2: Progressive Installation

Start with core packages and add others as needed:

```bash
# Essential packages (install these now)
conda install numpy matplotlib jupyter ipython
```

Add more when you need them:

```bash
# Scientific computing (Project 2+)
conda install scipy pandas astropy

# Machine learning (Project 3+)
conda install scikit-learn h5py
conda install jax jaxlib -c conda-forge
```

### Managing Packages

:::{tip} Package Management Commands

**Update packages** (do this periodically):

```bash
conda update numpy
conda update --all  # Update everything
```

**Uninstall packages** (useful for troubleshooting):

```bash
conda uninstall package_name
# Then reinstall fresh:
conda install package_name
```

**Check what's installed**:

```bash
conda list  # All packages
conda list numpy  # Specific package version
```
:::

**Quick Test**:

```bash
python -c "import numpy; print('NumPy works!')"
```

## Step 3: Install and Configure VS Code

### Installation

1. Download from: <https://code.visualstudio.com/>
2. Run installer for your operating system
3. Launch VS Code

### Minimal Setup (That's All You Need!)

1. **Install Python Extension**:
   - Click Extensions icon in sidebar (or press `Ctrl+Shift+X`)
   - Search "Python"
   - Install "Python" by Microsoft (first result)

2. **Select Your Environment**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Python: Select Interpreter"
   - Choose `comp536` from the list
   - **Note**: VS Code remembers this choice per folder - set once per project!

That's it! Add other extensions only as you need them.

### Disable AI Assistants (Course Requirement)

:::{important} Critical: Disable ALL AI Coding Tools

**Why this matters**: AI assistants like GitHub Copilot will autocomplete your code, often suggesting entire functions or completing lines automatically. While this seems helpful, it's catastrophic for learning because:

- You'll type `def` and Copilot writes the entire function (often incorrectly)
- You won't develop problem-solving skills or debugging abilities
- You'll become dependent on suggestions rather than understanding
- The AI often suggests plausible-looking but subtly wrong code

**This course's philosophy**: Learn to think computationally first, then use AI as a tool later (after Week 8).

**To disable**:

1. Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac) for Settings
2. Search "copilot" $\to$ Uncheck ALL "Enable" options
3. Search "intellicode" $\to$ Uncheck "Enable"
4. Search "ai" $\to$ Disable any AI suggestions or completions
5. Search "suggest" $\to$ Consider disabling autocompletion entirely for maximum learning

You're here to train your brain, not to train an AI to write code for you.
:::

## Step 4: Test Your Setup

Create a simple test file to verify everything works:

**1. Create `test_setup.py`:**

```python
"""Quick setup test for COMP 536"""
print("Testing imports...")

import numpy as np
print("✓ NumPy works!")

import matplotlib.pyplot as plt
print("✓ Matplotlib works!")

# Only test JAX if you installed it
try:
    import jax
    print("✓ JAX works!")
except ImportError:
    print("○ JAX not installed (that's okay for now)")

print("\n🎉 Everything is installed correctly!")
print("Your environment is ready for COMP 536!")
```

**2. Run the test:**

```bash
python test_setup.py
```

**Success**: You see checkmarks and the success message!

## Step 5: Quick Practice

Let's make sure you're comfortable with the basics:

```bash
# 1. Check your environment is active
conda activate comp536

# 2. Check what's installed
conda list

# 3. Create a simple plot
python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('test.png'); print('Created test.png')"

# 4. Open VS Code in current folder
code .
```

## Setup Complete Checklist

You're ready for the course when:

- [ ] Opening a new terminal and typing `conda activate comp536` works
- [ ] The prompt shows `(comp536)` after activation
- [ ] Running `python -c "import numpy"` produces no errors
- [ ] VS Code opens when you type `code .`
- [ ] The test script runs successfully

**All checked?** You're ready!

## Congratulations!

You've just accomplished what many graduate students struggle with for weeks. Your professional development environment is now:

- **Isolated** from system Python (no conflicts!)
- **Reproducible** (same setup works on any machine)
- **Professional-grade** (same tools as research scientists)

Take a screenshot of your successful test script output—you've earned this victory!

## Troubleshooting

### 🔧 Error Triage (60 seconds)

When you hit a problem, classify it first — it tells you what to do next.

- **`command not found`** $\to$ the tool isn't installed *or* your terminal doesn't know where it is.
  Fix: restart terminal $\to$ verify install $\to$ check you're using Miniforge Prompt (Windows).

- **`ModuleNotFoundError`** $\to$ you're in the wrong environment *or* the package isn't installed.
  Fix: does your prompt show `(comp536)`? If not: `conda activate comp536`. Then `conda list package`.

- **Permission / admin errors** $\to$ installer needs permissions, but **don't use `sudo` with conda**.
  Fix: reinstall "Just Me" / default location; on Windows run installer as admin if needed.

- **Long installs / timeouts** $\to$ network or resolver pain.
  Fix: try again later, install fewer packages at once, or switch networks.

:::{tip} Common Issues and Solutions
:class: dropdown

**"Command not found: conda"**

- Restart your terminal (most common fix!)
- On Windows, use "Miniforge Prompt" not regular Command Prompt
- Check if installation completed successfully

**"ModuleNotFoundError: No module named numpy"**

- Check prompt shows `(comp536)` - if not, run `conda activate comp536`
- Verify package is installed: `conda list numpy`
- Reinstall if needed: `conda install numpy`

**VS Code can't find Python**

- Open Command Palette (Ctrl/Cmd+Shift+P)
- Run "Python: Select Interpreter"
- Choose the comp536 environment
- Restart VS Code if needed

**"Permission denied" errors**

- Don't use `sudo` with conda (ever!)
- On Windows, try "Run as Administrator" for installer only
- Check you own the Miniforge directory

**Package installation fails**

- Update conda first: `conda update conda`
- Clear cache: `conda clean --all`
- Try installing packages one at a time
- Last resort for specific package: `pip install packagename`

**Behind a corporate/university firewall?**

```bash
# Configure proxy (replace with your proxy details)
conda config --set proxy_servers.http http://proxy.yourorg.com:8080
conda config --set proxy_servers.https https://proxy.yourorg.com:8080
```

**Need to start over completely?**

```bash
# Remove environment and start fresh
conda deactivate
conda env remove -n comp536
# Then go back to Step 2
```

**Low on disk space?**

```bash
# Remove unused packages and cache
conda clean --all
# Check environment size
du -sh ~/miniforge3/envs/comp536
```
:::

## What's Next?

:::{tip} Feeling Overwhelmed?
:class: dropdown

It's okay to take a break after Step 2 (environment creation) and continue tomorrow.
Your progress is saved! When you return:

1. Open a new terminal
2. Run `conda activate comp536`
3. Continue from where you left off
:::

1. Environment is ready
2. $\to$ Continue to [Git and GitHub Guide](03-git-intro.qmd)
3. $\to$ Start working on Project 1

:::{tip} Pro Tips

**Save Time**: Add this to your terminal config file (.bashrc/.zshrc):

```bash
alias comp="conda activate comp536"
```

Now just type `comp` to activate!

**Stay Organized**: Create a folder structure:

```bash
mkdir -p ~/comp536/{projects,notes,data}
```

**Practice Daily**: Open terminal every day, even for 5 minutes. Muscle memory develops fast!
:::

## Quick Reference Card

| Command | What it does |
|---------|--------------|
| `conda activate comp536` | Enter course environment |
| `conda deactivate` | Exit environment |
| `conda list` | Show installed packages |
| `conda install package_name` | Install new package |
| `python script.py` | Run Python script |
| `which python` | Check which Python is active |
| `conda env list` | Show all environments |
| `code .` | Open VS Code in current folder |
