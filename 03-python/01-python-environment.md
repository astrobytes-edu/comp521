---
title: "Chapter 1: Computational Environments & Scientific Workflows"
subtitle: "COMP 536: Scientific Modeling for Scientists | Python Fundamentals"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---


## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] **(1) Configure and navigate IPython as your primary interactive computing environment** for scientific projects and data analysis.
- [ ] **(2) Diagnose and fix** three common causes of environment-dependent behavior in scientific code.
- [ ] **(3) Explain step-by-step how Python's import system** locates and loads modules when you type `import module`.
- [ ] **(4) Identify** five specific dangers of Jupyter notebooks that can corrupt scientific results.
- [ ] **(5) Create** fully reproducible computational environments using `conda` with proper version pinning.
- [ ] **(6) Debug environment problems systematically** using a four-stage diagnostic protocol.
- [ ] **(7) Transform notebook explorations into reproducible Python scripts** following best practices.
- [ ] **(8) Execute Python code effectively** from both terminal and IPython environments.

## Prerequisites Check

:::{important} Prerequisites Self-Assessment

Before starting this chapter, verify you have completed these items:

- [ ] You can open a terminal/command prompt and are able to navigate directories (via `cd`, `ls`, `lsdir`, `pwd`).
- [ ] You have Miniforge installed and created a `comp536` python conda environment for this course.
- [ ] You have a text editor (e.g., Vim) or IDE (e.g., VS Code) installed.
- [ ] You have `git` installed and can you use basic `git` commands (e.g.,`clone`, `add`, `commit`, `pull`).

If you checked 'no' to any item, see the [Getting Started](../../02-getting-started/index.qmd) module.
:::

## Chapter Overview

Picture this: You download code from a groundbreaking scientific paper, eager to reproduce their analysis. You run it exactly as instructed. Instead of the published results, you get error messages, or worse — completely different values with no indication why. This frustrating scenario happens to nearly every computational scientist, from graduate students to professors. The problem isn't bad code or user error; it's that scientific computing happens in complex **environments** where tiny differences can cascade into complete failures.

This chapter reveals the hidden machinery that makes Python work (or not work) on your computer. You'll discover why the same analysis code produces different results on different machines, master **IPython** as your computational laboratory for rapid prototyping, understand the dangers of **Jupyter notebooks** in scientific computing, and learn to create truly reproducible computational environments for your research. These aren't just technical skills — they're the foundation of trustworthy scientific research.

By chapter's end, you'll transform from someone who hopes code works to someone who knows exactly why it works (or doesn't). You'll diagnose "No module named" errors in seconds, create environments that work identically on any computing cluster, and understand the critical difference between exploration and reproducible science. Let's begin by exploring the tool that will become your new best friend: **IPython**.

:::{warning} 🚫 Jupyter Notebooks Are Not Allowed in COMP 536

From **Day 1**, this course does **not** permit the use of Jupyter notebooks for assignments, projects, or submissions.

This is not a stylistic preference — it is a **scientific integrity decision**.

Notebooks encourage hidden state, ambiguous execution order, and results that cannot be reliably reproduced. Those properties directly conflict with the goals of computational modeling and scientific inference.

In this course:

- **IPython** is used for *interactive exploration*
- **Python scripts** are used for *all scientific work*
- **Reproducibility and traceability** matter more than convenience

You may encounter notebooks in tutorials or online resources. You may read them.
But **you may not submit notebook-based work** in this course.

This chapter explains *why* — and gives you the professional tools used in real research instead.
:::

:::{note} How to Use These Readings

These chapters are written as **references**, not as material you are expected to memorize or read linearly.

You should:

- Read sections when you need them
- Return to examples while debugging
- Use this chapter as a *toolbox*, not a checklist

Mastery comes from **using** these ideas in code — not from memorizing definitions.
:::

---

## 1.1 IPython: Your Computational Laboratory

While you could use the basic Python interpreter by typing `python`, **IPython** (type `ipython` at the terminal instead) transforms your terminal into a powerful environment for scientific computing and **exploratory data analysis** (EDA). Think of it as the difference between a basic calculator and one with advanced scientific functions — both compute, but one is designed for serious scientific work. In most scientific workflows, IPython becomes the default interactive “scratchpad” because it makes exploration faster and debugging more transparent.

### Launching Your Laboratory

First, ensure you're in the right environment, then launch IPython. Here's how to do it properly:

:::{note} Terminal Commands vs Python Code

Throughout this book:

- Lines starting with `$` are terminal/shell commands
- Lines starting with `In []:` are IPython commands
- Regular code blocks are Python scripts
:::

```bash
# Terminal commands (type these in your terminal, not in Python!)
$ conda activate comp536
$ ipython

# You'll see something like this appear:
Python 3.11.5 | packaged by conda-forge
IPython 8.14.0 -- An enhanced Interactive Python
In [1]:
```

Notice the prompt says `In [1]:` instead of `>>>` (which is what basic Python shows). This numbering system is your first hint that IPython is different — it remembers everything. Each command you type gets a number, making it easy to reference previous work.

### The Power of Memory

IPython maintains a complete history of your session, accessible through special variables:

```python
# Type these commands one at a time in IPython
import numpy as np

# Example: Calculate something useful
H0 = 70.0  # Hubble constant in km/s/Mpc

# H0 has units (km/s)/Mpc, so 1/H0 is a time.
# Approx conversion: 1 (km/s/Mpc)^-1 approx 9.78 Gyr, so multiply by ~978 to get Gyr.
t_hubble = 1.0 / H0
t_hubble_gyr = t_hubble * 978  # Approx: 9.78 * (100/H0) Gyr

print(f"Hubble time: {t_hubble_gyr:.1f} Gyr")

# In IPython, you can reference previous work:
print("In IPython, Out[n] stores outputs, In[n] stores inputs")
print("The underscore _ references the last output")
```

:::{tip} Check Your Understanding
:class: dropdown

What's the difference between `In[5]` and `Out[5]` in IPython?

**Solution:**

- `In[5]` contains the actual text/code you typed in cell 5 (as a string)
- `Out[5]` contains the result/value that cell 5 produced (if any)

For example:

- `In[5]` might be `"np.sqrt(2)"`
- `Out[5]` would be `1.4142135623730951`

This history system lets you reference and reuse previous computations without retyping — crucial when analyzing large datasets or iterating on algorithms.
:::

### Tab Completion: Your Exploration Tool

Tab completion helps you discover libraries without memorizing everything:

```{code-cell} python
import numpy as np

# In real IPython, type: np.<TAB>
# Shows all available functions

available_functions = [item for item in dir(np) if not item.startswith('_')]
print("NumPy contains:", len(available_functions), "functions/attributes")
print("Sample:", available_functions[:10])

# To see functions for FFT analysis (np.*fft*?<TAB> in IPython):
fft_functions = [item for item in dir(np) if 'fft' in item.lower()]
print("\nFFT-related functions:", fft_functions)
```

### Magic Commands: IPython's Superpowers

IPython's **magic commands** give you capabilities far beyond standard Python. Here's a practical example comparing different approaches:

```{code-cell} python
# In IPython, you would use: %timeit
# Here we simulate timing different approaches

import timeit
import numpy as np

# Method 1: List comprehension
def calc_list_comp(values):
    return [x**2 for x in values if x > 0]

# Method 2: NumPy vectorized
def calc_numpy(values):
    return values[values > 0]**2

# Generate test data
rng = np.random.default_rng(42)
test_values = rng.standard_normal(1000)

# Time both methods
time1 = timeit.timeit(lambda: calc_list_comp(test_values), number=100)
time2 = timeit.timeit(lambda: calc_numpy(test_values), number=100)

print(f"List comprehension: {time1*10:.4f} ms per call")
print(f"NumPy vectorized:   {time2*10:.4f} ms per call")
print(f"\nNumPy is {time1/time2:.1f}x faster!")
```

:::{warning} Common Bug Alert: Platform-Specific Timing
:class: dropdown

Timing results vary significantly between machines due to:

- CPU speed and architecture (Intel vs AMD vs ARM)
- NumPy compilation (MKL vs OpenBLAS vs BLIS)
- System load and background processes
- Python version and compilation options

**Best Practice**: Always benchmark on your target system (laptop vs cluster)
:::

### Getting Help Instantly

IPython makes documentation accessible without leaving your workflow:

```{code-cell} python
# Demonstrating IPython's help system
print("In IPython, use ? for quick help:")
print("  np.fft.fft?  - shows documentation")
print("  np.fft.fft?? - shows source code (if available)")
print("\nExample documentation for np.fft.fft:")
print("  Compute the one-dimensional discrete Fourier Transform.")
print("  Used for: spectral analysis, period finding, filtering")
print("  Returns: complex array of Fourier coefficients")
```

:::{important} Computational Thinking: Interactive Exploration

The ability to quickly test ideas and explore APIs interactively is fundamental to computational science. IPython's environment encourages experimentation:

**Explore** $\to$ **Test** $\to$ **Refine** $\to$ **Validate**

This rapid iteration cycle is how algorithms are born and bugs are discovered. You might:

1. Explore a new library's API
2. Test different algorithms
3. Refine parameters for optimal performance
4. Validate against known results

This pattern appears everywhere: from testing simulations to debugging data processing software.
:::

### Managing Your Workspace

```{code-cell} python
import sys
import numpy as np

# Create some variables for demonstration
redshift = 0.5
distance = 2590.3  # Mpc
magnitude = 18.5
filters = ['u', 'g', 'r', 'i', 'z']

# Show variables (simulating %who in IPython)
current_vars = [var for var in dir()
                if not var.startswith('_') and not var.startswith('__')]
print("Variables in workspace (%who in IPython):")
print(", ".join(current_vars[:8]))

# Detailed info (simulating %whos in IPython)
print("\nDetailed variable info (%whos in IPython):")
print(f"{'Variable':<20} {'Type':<15} {'Value/Info'}")
print("-"*55)
print(f"{'redshift':<20} {'float':<15} {redshift}")
print(f"{'distance':<20} {'float':<15} {distance:.1f} Mpc")
print(f"{'filters':<20} {'list':<15} {len(filters)} items")
```

:::{important} Why This Matters: Your First Day of Research
:class: dropdown

When your advisor hands you a data file and says "can you check if this is interesting?", you'll open IPython and in 5 minutes:

- Load the data
- Check the structure with tab completion
- Plot a quick visualization
- Test a hypothesis

Without IPython, this becomes a 30-minute script-writing exercise. With IPython, you'll have an answer before your advisor finishes their coffee.
:::

:::{tip} The More You Know: The Reproducibility Crisis in Science
:class: dropdown

A 2018 study attempted to obtain data and code from 204 computational papers in *Science* magazine, finding that materials were available for only 26% of articles, with many of those still having reproducibility issues ([Stodden et al., 2018](https://doi.org/10.1073/pnas.1708290115)). Common reproducibility barriers included:

- Missing dependencies and software versions
- Hardcoded file paths to data
- Undocumented parameter choices
- Missing random seeds for simulations

Tools like IPython's `%history` and `%save` commands create an audit trail that helps ensure your future self (and others) can reproduce your analysis.

**Additional Resources:**

- [Nature's reproducibility survey (2016)](https://doi.org/10.1038/533452a) - More than 70% of researchers have failed to reproduce another scientist's experiments
:::

---

## Section 1.2: Understanding Python's Hidden Machinery

When you type `import numpy`, a complex process unfolds behind the scenes. Understanding this machinery is the difference between guessing why `ImportError: No module named 'scipy'` fails and knowing exactly how to fix it.

**Why Import Systems Matter:** Modern scientific analysis relies on dozens of specialized packages. A typical data processing pipeline might import `numpy` for arrays, `scipy` for algorithms, and `matplotlib` for visualization. When you're running code on a deadline, understanding how Python finds and loads these packages can save your project.

### The Import System Exposed

Python's **import system** is like a librarian searching through a card catalog. When you request a book (module), the librarian (Python) has a specific search order (`sys.path`) and won't randomly guess where to look. This systematic approach ensures consistency but can cause confusion when multiple versions exist.

Let's peek behind the curtain to understand this process. Every time Python starts, it builds a search path based on your environment, installation method, and current directory. This path determines everything about which code gets loaded:

```{code-cell} python
import sys
from pathlib import Path

# Where is Python running from?
print(f"Python executable: {sys.executable}")

# What version are we using?
print(f"Python version: {sys.version.split()[0]}")

# Where will Python look for modules?
print("\nPython searches these locations (in order):")
for i, path in enumerate(sys.path[:5], 1):
    # Shorten paths for readability
    display_path = str(path).replace(str(Path.home()), "~")
    print(f"  {i}. {display_path}")
print("  ... and more")

# Check for key packages
print("\nChecking for key packages:")
for pkg in ['numpy', 'scipy', 'matplotlib']:
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'unknown')
        print(f"  ✓ {pkg:12} version {version}")
    except ImportError:
        print(f"  ✗ {pkg:12} NOT INSTALLED")
```

The search path (`sys.path`) acts as Python's roadmap for finding modules. Python follows `sys.path` in order, using the first matching module it finds. This is why having multiple versions of the same package can cause confusion—Python doesn't look for the "best" version, just the first one.

This ordered search has important implications for software development. If you have a file named `numpy.py` in your current directory, Python will import that instead of the real numpy package. This is a common source of mysterious errors when students name their test scripts after the packages they're learning.

:::{important} Computational Thinking: The Import Resolution Algorithm

When Python executes `import numpy`, it follows this algorithm:

1. **Check cache**: Is `numpy` already in `sys.modules`?
2. **Search paths**: For each directory in `sys.path`:
   - Look for `numpy/` directory with `__init__.py`
   - Look for `numpy.py` file
   - Look for compiled extension `numpy.so/.pyd`
3. **Load module**: Execute the module code once
4. **Cache result**: Store in `sys.modules` to avoid reloading
5. **Access submodule**: Repeat for submodules within `numpy`

Understanding this algorithm helps you debug why `import numpy` works but `from numpy import linalg` might fail (missing subpackage installation).
:::

:::{tip} Check Your Understanding: Import System Diagnostics
:class: dropdown

You run `import mypackage` and get `ModuleNotFoundError`. Your colleague runs the same command and it works. Both of you have the package installed according to `pip list`.

Before reading the solution, write down:

1. Three possible causes for this difference
2. The diagnostic commands you'd run (in order)
3. How you'd fix each potential cause

**Solution:**

**Possible causes and diagnostics:**

1. **Different Python interpreters**
   - Diagnostic: `which python` and `sys.executable`
   - Fix: Activate the correct environment

2. **Different sys.path**
   - Diagnostic: Compare `sys.path` between systems
   - Fix: Add missing directory with `sys.path.append()` or PYTHONPATH

3. **Package installed in different location**
   - Diagnostic: `pip show mypackage` for installation path
   - Fix: Reinstall in correct environment with `pip install --user` or `conda install`

**The systematic debugging approach:**

```python
# Step 1: Which Python?
import sys
print(sys.executable)

# Step 2: Where does Python look?
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

# Step 3: Where is package actually installed?
# Run in terminal: pip show mypackage

# Step 4: Is there a name conflict?
import os
print(os.listdir('.'))  # Check for local mypackage.py
```

The key insight: Import problems are usually environment problems, not code problems!
:::

```{mermaid}
flowchart TD
    A[import numpy] --> B{Is 'numpy' in<br/>sys.modules cache?}
    B -->|Yes| H[Use cached module]
    B -->|No| C[Search sys.path directories]
    C --> D{Found<br/>numpy/?}
    D -->|No| E{Found<br/>numpy.py?}
    E -->|No| F{Found<br/>numpy.so?}
    F -->|No| G[ImportError!]
    D -->|Yes| I[Load & execute module]
    E -->|Yes| I
    F -->|Yes| I
    I --> J[Store in sys.modules]
    J --> K[Look for submodules]
    H --> K

    style G fill:#ff6b6b
    style I fill:#51cf66
    style J fill:#339af0
```

### Debugging Import Problems

:::{tip} Check Your Understanding
:class: dropdown

You get `ModuleNotFoundError: No module named 'scipy.optimize'`. What are three possible causes and their solutions?

**Solution:**

Three possible causes and solutions:

1. **Incomplete scipy installation**: Some distributions split scipy
   - Solution: `conda install -c conda-forge scipy` (get complete package)

2. **Old scipy version**: Older versions had different structure
   - Check: `python -c "import scipy; print(scipy.__version__)"`
   - Solution: `conda update scipy`

3. **Mixed pip/conda installation**: Conflicting installations
   - Check: `conda list scipy` vs `pip list | grep scipy`
   - Solution: Stick to conda for scientific packages

The most robust fix:

```bash
conda create -n clean_env python=3.11
conda activate clean_env
conda install -c conda-forge numpy scipy matplotlib
```
:::

### Multiple Pythons: A Common Disaster

Most systems have multiple Python installations, especially on shared computing clusters:

```{code-cell} python
from pathlib import Path
import sys

# Common Python locations
common_pythons = {
    'System Python': '/usr/bin/python3',
    'Conda (base)': '~/miniforge3/bin/python',
    'Conda (env)': '~/miniforge3/envs/comp536/bin/python',
    'Homebrew (Mac)': '/usr/local/bin/python3',
    'Module system': '/software/python/bin/python'
}

print("Common Python locations on systems:")
print("-" * 50)
for name, path in common_pythons.items():
    expanded_path = Path(path).expanduser()
    exists = "✓" if expanded_path.exists() else "✗"
    current = "<- CURRENT" if str(expanded_path) in sys.executable else ""
    print(f"  {exists} {name:20} {path:30} {current}")

print("\n⚠️  This is why 'conda activate' is crucial!")
print("📚 Each Python has its own packages - they don't share!")
```

:::{warning} Common Bug Alert: The Cluster Python Confusion
:class: dropdown

**Symptom**: Code works on laptop but fails on computing cluster

**Cause**: Different Python modules loaded by default

**Example**: On many clusters:

```bash
$ module load python  # Loads system Python
$ python script.py    # Uses wrong Python!
```

**Fix**: Always use explicit paths or conda:

```bash
$ conda activate comp536
$ which python  # Verify it's YOUR Python
$ python script.py
```

**Best Practice**: Add to your job scripts:

```bash
#!/bin/bash
#SBATCH --job-name=analysis

# Always activate your environment first!
source ~/miniforge3/etc/profile.d/conda.sh
conda activate comp536
python your_script.py
```
:::

---

## 1.3 Jupyter Notebooks: Beautiful Disasters Waiting to Happen

**Jupyter notebooks** seem perfect for scientific computing and data analysis - you can mix code, plots, and explanations in one streamlined document. You'll see them in tutorials and even published papers. If you're like most students, notebooks are probably how you learned Python, and there's good reason for that - they're excellent for learning concepts and exploring data interactively.

However, as your projects grow more complex - think large simulations, Monte Carlo methods, or processing gigabytes of data - notebooks reveal serious limitations that can corrupt results and make debugging nearly impossible. The hidden state problems we're about to explore aren't academic edge cases; they're issues that every computational scientist eventually faces.

This course will expand your toolkit beyond notebooks. You can use them for `Project 1` since that's likely your comfort zone - and honestly, notebooks *are* great for initial exploration. But then we'll transition to writing scripts and using IPython, the approach used by every major data processing pipeline, every Python analysis framework from `numpy` to `scipy`, and every production machine learning pipeline. Even when the heavy numerical lifting happens in C++ or Fortran, the analysis, visualization, and workflow orchestration happens through Python scripts, not notebooks.

Here's what you'll gain: **modular design** where functions can be reused across projects, **testable code** where each component can be verified independently, **version control** that actually works (no more JSON merge conflicts!), and **true reproducibility**. By Chapter 5, you'll be building your own professional libraries - versatile toolkits you can import into any project. Yes, the transition might feel awkward initially, but this course is designed to transform you from notebook-only coding to professional-level development - but first we must begin by understanding what notebooks actually do behind the scenes...

### The Seductive Power of Notebooks

To start Jupyter (after activating your environment):

```bash
# Terminal commands:
$ conda activate comp536
$ jupyter lab

# Opens browser at http://localhost:8888
# You can create notebooks, write code, see plots inline
```

### The Hidden State Monster

The most insidious problem: notebooks maintain hidden state between cell executions. Here's a subtle Python gotcha that can make notebook state bugs *feel* like “the function captured old variables.”

In Python, **global variables are looked up at call time**. But **default argument values are evaluated once, when the function is defined**. In a notebook, it’s easy to redefine a function in one cell, then change parameters in another, and accidentally keep using frozen defaults.

```{code-cell} python
# Simulating notebook cells with execution order problems

# Cell 1: Set parameters
param_a = 70.0
param_b = 0.3
print(f"Cell 1: Set param_a = {param_a}, param_b = {param_b}")

# Cell 2: Define calculation
def calculate_result(x, param_a=param_a, param_b=param_b):
    """Calculate result using parameters."""
    # Default arguments freeze values at *definition* time.
    return (x / param_a) * (1 + param_b)

print(f"Cell 2: Defined function with param_a = {param_a}")

# Cell 3: User updates parameters
param_a = 67.4  # Updated value
param_b = 0.315  # Updated value
print(f"Cell 3: Updated to param_a = {param_a}")

# Cell 4: Calculate - which param_a does this use?
x_value = 1000
result = calculate_result(x_value)
print(f"Cell 4: Result = {result:.2f}")
print(f"  But function still uses OLD param_a = 70!")
print(f"  This gives WRONG result by {(70/67.4-1)*100:.1f}%!")
```

:::{important} Debug This!

A student's notebook analyzes data:

```python
Cell 1: values = [0.5, 1.2, 2.3]
        weights = [1.0, 1.0, 1.0]

Cell 2: mean_value = np.mean(values)
        weighted_mean = np.average(values, weights=weights)

Cell 3: values.append(5.4)  # Add new data
        weights.append(2.0)

Cell 4: print(f"Average: {mean_value:.2f}")
        print(f"Weighted average: {weighted_mean:.2f}")

Cell 5: # Classify based on mean
        if mean_value < 1:
            print("Low values")
        elif mean_value < 3:
            print("Medium values")
```

They run cells: 1, 2, 3, 4, 2, 4, 5. What's the classification? Is it correct?

**Solution:**

**Execution trace:**

1. Cell 1: `values = [0.5, 1.2, 2.3]`, `weights = [1.0, 1.0, 1.0]`
2. Cell 2: `mean_value = 1.33`
3. Cell 3: Lists become `[0.5, 1.2, 2.3, 5.4]` and `[1.0, 1.0, 1.0, 2.0]`
4. Cell 4: Prints "Average: 1.33" (OLD value!)
5. Cell 2 again: `mean_value = 2.35` (NEW value)
6. Cell 4 again: Prints "Average: 2.35"
7. Cell 5: Classifies as "Medium values" (1 < 2.35 < 3)

**Problems:**

- Classification uses updated mean (2.35) but that includes the new data point
- This is circular reasoning - using the data to classify the data
- The correct mean without the new point is 1.33

**This demonstrates how notebook state corruption leads to incorrect scientific conclusions!**
:::

### Memory Accumulation in Data Analysis

```{code-cell} python
import sys
import numpy as np

# Simulating repeated cell execution with data
data_list = []

print("Initial memory state")

# First run: Load batch 1
for i in range(100):
    # Simulate 100 data points, 4000 features each
    data_point = np.random.randn(4000)
    data_list.append(data_point)

# Calculate memory usage
n_points = len(data_list)
n_values = n_points * 4000
memory_mb = (n_values * 8) / (1024 * 1024)  # 8 bytes per float64
print(f"After batch 1: {n_points} points, ~{memory_mb:.1f} MB")

# Second run (cell executed again) - adds MORE data!
for i in range(100):
    data_point = np.random.randn(4000)
    data_list.append(data_point)

n_points = len(data_list)
n_values = n_points * 4000
memory_mb = (n_values * 8) / (1024 * 1024)
print(f"After re-run: {n_points} points, ~{memory_mb:.1f} MB")

print("\n⚠️  Each run ADDS data - notebook doesn't reset!")
print("📈 With real datasets (millions of points),")
print("   this crashes your kernel and loses all work!")
```

:::{tip} The More You Know: The $125 Billion Excel Error
:class: dropdown

In 2013, graduate student Thomas Herndon couldn't reproduce the results from a highly influential economics paper by Carmen Reinhart and Kenneth Rogoff. This paper, ["Growth in a Time of Debt,"](https://www.aeaweb.org/articles?id=10.1257/aer.100.2.573) had been cited by politicians worldwide to justify austerity policies affecting millions of people.

When Herndon finally obtained the original Excel spreadsheet, he discovered a coding error: five countries were accidentally excluded from a calculation due to an Excel formula that didn't include all rows. This simple mistake skewed the results, showing that high debt caused negative growth when the corrected analysis showed much weaker effects ([Herndon, Ash, and Pollin, 2014](https://doi.org/10.1093/cje/bet075)). The implications were staggering — this spreadsheet error influenced global economic policy.

Just like hidden state in Jupyter notebooks, the error was invisible in the final spreadsheet. The lesson? Computational transparency and reproducibility aren't just academic exercises — they have real-world consequences. Always make your computational process visible and reproducible!
:::

### The Notebook-to-Script Transition

After Project 1, we'll abandon notebooks for **scripts**. Here's why scripts are superior for scientific research:

| Aspect | Notebooks | Scripts |
|--------|-----------|---------|
| Execution Order | Ambiguous, user-determined | Top-to-bottom, always |
| Hidden State | Accumulates invisibly | Fresh start each run |
| Large Data Processing | Memory leaks common | Controlled memory usage |
| Cluster Jobs | Possible but awkward (e.g., `papermill`, `nbconvert`) | Easy batch submission |
| Version Control | JSON mess with outputs | Clean text diffs |
| Pipeline Integration | Nearly impossible | Straightforward |
| Reproducible Results | Easy to accidentally break | Much more reliable (with pinned deps + fixed inputs + seeds) |

```{mermaid}
graph TD
    subgraph "Notebook Execution"
        N1[Any cell] --> N2[Any cell]
        N2 --> N3[Any cell]
        N3 --> N1
        N1 -.->|Hidden State| NS[(Persistent Memory)]
        N2 -.->|Hidden State| NS
        N3 -.->|Hidden State| NS
    end

    subgraph "Script Execution"
        S1[Line 1] --> S2[Line 2]
        S2 --> S3[Line 3]
        S3 --> S4[Line 4]
        S4 --> S5[Fresh start each run]
    end

    style NS fill:#ff6b6b
    style S5 fill:#51cf66
```

:::{important} Why This Matters: Your Analysis Must Be Bulletproof
:class: dropdown

When you submit your first paper. The referee may ask: "Can you verify that your algorithm consistently identifies the pattern in your data sample?"

With a **notebook**, you'll panic:

- Which cells did you run to get that result?
- Did you update the preprocessing before or after running the analysis?
- Your memory says one thing, but re-running gives different results

With a **script**, you'll confidently respond:

- "Run `python analyze.py --input data/sample.csv --method algorithm1`"
- "Results are identical: value = 0.5673 $\pm$ 0.0002"
- "See our GitHub repository for version-controlled analysis code"

Real example: Major scientific collaborations require discoveries to be verified with independent analysis pipelines. In practice, those checks are run as **scripts/pipelines**, not as ad-hoc interactive notebooks, because there’s no room for hidden state corruption. Your career depends on reproducible results.

Remember: **Notebooks are for exploration. Scripts are for science.**
:::

:::{important} Computational Thinking: Reproducible Analysis Pipelines

Modern scientific projects process terabytes of data through complex pipelines.

**Data Flow**: Raw data $\to$ Preprocessing $\to$ Analysis $\to$ Feature extraction $\to$ Results

Each step must be:

- **Deterministic**: Same input = same output
- **Versioned**: Track software versions
- **Logged**: Record all parameters
- **Testable**: Unit tests for each component

Notebooks tend to fight these requirements unless you impose extra structure; scripts make them much easier to satisfy. This is why major projects often use workflow managers (Snakemake, Pegasus) orchestrating Python scripts rather than manually re-running notebook cells.

Remember: *"If it's not reproducible, it's not science."*
:::

---

## 1.4 Scripts: Write Once, Run Anywhere (Correctly)

Python scripts are simple text files containing Python code, executed from top to bottom, the same way every time. No hidden state, no ambiguity, just predictable execution - essential for scientific computing.

### From IPython to Scripting

Start by experimenting in IPython with a real scientific calculation:

```{code-cell} python
# Quick calculation in IPython
import numpy as np

# Constants (SI units)
G = 6.67430e-11   # m^3 kg^-1 s^-2
c = 2.99792458e8  # m/s
M_sun = 1.98847e30  # kg

# Calculate for a 10 solar mass black hole
M_bh = 10 * M_sun
r_s = 2 * G * M_bh / c**2

print(f"Schwarzschild radius for 10 M_sun: {r_s/1e3:.1f} km")
```

Now create a proper script. Save this as `calculation.py`:

:::{note} Complete calculation.py Script
:class: dropdown

```python
#!/usr/bin/env python
"""
Calculate Schwarzschild radii for various objects.

This module provides functions to calculate the Schwarzschild radius
(event horizon) for black holes of different masses.
"""

	import numpy as np

# Physical constants (SI units)
G = 6.67430e-11     # Gravitational constant [m^3 kg^-1 s^-2]
c = 2.99792458e8    # Speed of light [m/s]
M_sun = 1.98847e30  # Solar mass [kg]

def schwarzschild_radius(mass_kg):
    """
    Calculate Schwarzschild radius for a given mass.

    The Schwarzschild radius is the radius of the event horizon
    for a non-rotating black hole.

    Parameters
    ----------
    mass_kg : float
        Mass in kilograms

    Returns
    -------
    float
        Schwarzschild radius in meters

    Examples
    --------
    >>> r_s = schwarzschild_radius(10 * M_sun)
    >>> print(f"{r_s/1e3:.1f} km")
    29.5 km
    """
    if mass_kg <= 0:
        raise ValueError("Mass must be positive")
    return 2 * G * mass_kg / c**2

def classify_object(mass_solar):
    """
    Classify object by mass.

    Parameters
    ----------
    mass_solar : float
        Mass in solar masses

    Returns
    -------
    str
        Classification (stellar, intermediate, supermassive)
    """
    if mass_solar < 100:
        return "Stellar-mass"
    elif mass_solar < 1e5:
        return "Intermediate-mass"
    else:
        return "Supermassive"

def main():
    """Main execution function with example calculations."""

    # Example objects
    objects = {
        "Cygnus X-1": 21.2,           # Solar masses
        "GW150914 remnant": 62,       # First LIGO detection
        "Sagittarius A*": 4.154e6,    # Milky Way center
        "M87*": 6.5e9,                # First black hole image
    }

    print("Schwarzschild Radii of Famous Black Holes")
    print("=" * 50)

    for name, mass_solar in objects.items():
        mass_kg = mass_solar * M_sun
        r_s = schwarzschild_radius(mass_kg)
        classification = classify_object(mass_solar)

        # Convert to appropriate units
        if r_s < 1e3:
            r_s_display = f"{r_s:.1f} m"
        elif r_s < 1e6:
            r_s_display = f"{r_s/1e3:.1f} km"
        elif r_s < 1.5e11:  # 1 AU in m
            r_s_display = f"{r_s/1e9:.1f} million km"
        else:
            r_s_display = f"{r_s/1.496e11:.2f} AU"

        print(f"\n{name}:")
        print(f"  Mass: {mass_solar:.2e} M_sun")
        print(f"  Type: {classification}")
        print(f"  Event horizon: {r_s_display}")

# This pattern makes the script both runnable and importable
if __name__ == "__main__":
    main()
```
:::

### The `if __name__ == "__main__"` Pattern for Python Scripts

This crucial pattern makes your code both runnable and importable:

```{code-cell} python
# Understanding __name__ in scientific context
def planck_function(wavelength_nm, temperature_K):
    """
    Calculate Planck function for blackbody radiation.

    Used for stellar spectra modeling.
    """
    import numpy as np

    # Constants (SI units)
    h = 6.62607015e-34  # Planck constant [J*s]
    c = 2.99792458e8    # Speed of light [m/s]
    k_B = 1.380649e-23  # Boltzmann constant [J/K]

    # Convert wavelength to meters
    wavelength = wavelength_nm * 1e-9

    # Planck function
    exp_term = np.exp(h * c / (wavelength * k_B * temperature_K))
    B = (2 * h * c**2 / wavelength**5) / (exp_term - 1)

    return B

# Python sets __name__ based on how the file is used
print(f"Current __name__ is: {__name__}")

if __name__ == "__main__":
    # This runs ONLY when script is executed directly
    # Perfect for testing your functions
    print("\nTesting Planck function for the Sun:")

    # Sun's peak wavelength should be ~500 nm (green)
    wavelengths = [400, 500, 600, 700]  # nm (violet to red)
    T_sun = 5778  # K

    for wl in wavelengths:
        B = planck_function(wl, T_sun)
        print(f"  lambda={wl}nm: B={B:.2e} W/m^2/sr/m")

    # When others import this file, this test code won't run
    # They can just use: from your_module import planck_function
```

:::{tip} Check Your Understanding
:class: dropdown

Why is the `if __name__ == "__main__"` pattern crucial for scientific instrument control software?

**Solution:**

In scientific instrument control and data acquisition:

1. **Safety**: Test functions without activating equipment

   ```python
   def move_to_position(x, y, z):
       # Moves expensive/dangerous equipment!
       pass

   if __name__ == "__main__":
       # Safe testing with simulated coordinates
       print("Testing movement (not really moving):")
       # move_to_position(10.0, 20.0, 5.0)  # Commented for safety
   ```

2. **Module Testing**: Test detector readout without taking real data
3. **Pipeline Components**: Each script works standalone or in pipeline
4. **Calibration Scripts**: Can process test data or real observations
:::

---

## 1.5 Creating Reproducible Environments

Your scientific analysis depends on its **environment** — Python version, numpy version, even the linear algebra backend. Creating reproducible environments ensures your code produces identical results on any system, from your laptop to a supercomputer.

### The Conda Solution

**Conda** creates isolated environments — separate Python installations with their own packages. This is essential for research where different projects need different package versions:

```bash
# Essential conda commands

# Create environment for one project
$ conda create -n project_a python=3.11
$ conda activate project_a
$ conda install -c conda-forge numpy scipy matplotlib

# Create separate environment for another project
$ conda create -n project_b python=3.10
$ conda activate project_b
$ conda install -c conda-forge numpy scipy pandas

# List all your environments
$ conda env list

# Switch between projects
$ conda deactivate
$ conda activate project_a
```

:::{important} Why This Matters: Cluster Time = Money
:class: dropdown

Your university pays ~$0.10 per CPU-hour on the cluster. A typical research project uses 10,000+ hours. If your code crashes after 8 hours because of environment issues, you've wasted:

- $80 in compute time
- 8 hours of waiting
- Your queue priority (back to the end of the line!)

Get your environment right ONCE, and every subsequent run just works. This chapter will literally save you hundreds of dollars and weeks of time.
:::

### Environment Files: Share Your Exact Setup

Create an `environment.yml` file for your research project:

:::{tip} Example environment.yml for data analysis
:class: dropdown

```yaml
name: data_analysis
channels:
  - conda-forge
dependencies:
  # Core scientific stack
  - python=3.11
  - numpy=1.24.*
  - scipy=1.11.*
  - matplotlib=3.7.*
  - pandas=2.0.*

  # Additional packages
  - scikit-learn=1.3.*
  - h5py=3.9.*

  # Development tools
  - ipython
  - jupyter
  - pytest

  # Additional packages via pip
  - pip
  - pip:
    - specialized-package==1.2.3
```

Collaborators recreate your exact environment:

```bash
$ conda env create -f environment.yml
$ conda activate data_analysis
```
:::

### environment.yml vs lockfiles (what “reproducible” really means)

An `environment.yml` is a great **sharing format**, but it is not a true lockfile: the exact solved set of packages can vary across OSes and across time. In practice you often want two levels:

- **Level 1 (portable-ish):** `environment.yml` with major/minor pins and `conda env export --from-history` to avoid freezing every transient dependency.
- **Level 2 (as deterministic as possible):** a lockfile (e.g., via `conda-lock`) or an explicit spec export for the platform you will run on.

### Proper Path Management

Stop hardcoding paths that break when moving between laptop and cluster:

```python
from pathlib import Path
import os

# BAD: Hardcoded path
bad_path = '/Users/jane/Desktop/data/2024-03-15/raw/file_001.csv'
print(f"BAD (hardcoded): {bad_path}")
print("  Problem: Doesn't exist on cluster or collaborator's machine!")

# GOOD (scripts): Anchor paths to the script location (not the current working directory)
SCRIPT_DIR = Path(__file__).resolve().parent  # works in scripts; __file__ is not set in notebooks
data_root = SCRIPT_DIR / "data"

# If you're in a notebook, you can *choose* to rely on the working directory:
# data_root = Path.cwd() / "data"  # only if you started Jupyter in the project root

date = "2024-03-15"
data_file = data_root / date / "raw" / "file_001.csv"
print(f"\nGOOD (script-anchored): {data_file}")

# BETTER: Configuration-based approach
# In your script or config file:
DATA_DIR = Path(os.getenv('PROJECT_DATA', './data'))
PROCESSED_DIR = Path(os.getenv('PROJECT_PROCESSED', './processed'))

def get_data_path(date_str, file_num, data_type='raw'):
    """
    Construct path to data file.

    Parameters
    ----------
    date_str : str
        Date (YYYY-MM-DD)
    file_num : int
        File number
    data_type : str
        'raw', 'processed', or 'final'
    """
    filename = f"file_{file_num:03d}.csv"
    return DATA_DIR / date_str / data_type / filename

# Usage
data_path = get_data_path('2024-03-15', 1)
print(f"\nBEST (configurable): {data_path}")

# Check if file exists before processing
if data_path.exists():
    print(f"  ✓ Ready to process: {data_path.name}")
else:
    print(f"  ✗ File not found - check DATA_DIR environment variable")
    print(f"    Expected location: {data_path}")
```

### Random Seed Control for Monte Carlo

Make Monte Carlo simulations reproducible by using a default random number generator seed value:

```{code-cell} python
import numpy as np

def simulate_with_errors(n_samples=100, seed=42):
    """
    Simulate measurements with realistic errors.

    Parameters
    ----------
    n_samples : int
        Number of samples to simulate
    seed : int
        Random seed for reproducibility

    Returns
    -------
    tuple
        True values, observed values, errors
    """
    # Prefer a local RNG over global state
    rng = np.random.default_rng(seed)

    # True values (some distribution)
    true_values = rng.uniform(10, 20, n_samples)

    # Errors increase with value
    base_error = 0.01
    errors = base_error * np.exp((true_values - 10) / 4)

    # Add Gaussian noise
    observed_values = true_values + rng.normal(0, errors)

    return true_values, observed_values, errors

# Run simulation multiple times - same results!
for run in range(3):
    true, obs, err = simulate_with_errors(n_samples=5, seed=42)
    print(f"Run {run+1}: First obs = {obs[0]:.3f} +/- {err[0]:.3f}")

print("\n⚠️  Different seed = different results:")
true2, obs2, err2 = simulate_with_errors(n_samples=5, seed=137)
print(f"Seed 137: First obs = {obs2[0]:.3f} +/- {err2[0]:.3f}")

print("\n🔍 Always document seeds in papers for reproducibility!")
```

:::{tip} The More You Know: When Code Sharing Isn't Enough
:class: dropdown

In 2022, researchers attempted to run over 9,000 R scripts from 2,000+ publicly shared research datasets in the Harvard Dataverse repository ([Trisovic et al., 2022](https://doi.org/10.1038/s41597-022-01143-6)). The results were sobering: **74% of the R files failed to run** on the first attempt. Even after automated code cleaning to fix common issues, **56% still failed**.

The most common errors weren't complex algorithmic problems but basic issues:

- Missing package imports (`library()` statements)
- Hardcoded file paths that don't exist on other systems
- Dependencies on variables defined in other scripts
- Assuming specific working directories

What makes this particularly striking is that these researchers had already taken the crucial step of sharing their code—they were trying to do the right thing! But code availability alone doesn't guarantee reproducibility.

The study found that simple practices could have prevented most failures:

- Using relative paths instead of absolute paths
- Explicitly loading all required libraries at the script beginning
- Setting random seeds for any stochastic processes
- Including session information (Python version, package versions)

This echoes our discussion about environments: sharing code without documenting its environment is like sharing a recipe without mentioning it's for a high-altitude kitchen. The code might be perfect, but it still won't work!
:::

---

## Section 1.6: Essential Debugging Strategies

When your simulation produces unphysical results after running for 12 hours, or if your data processing pipeline crashes during a critical analysis, **systematic debugging** saves the day. Debugging isn't just about fixing errors—**it's about understanding why they occurred and preventing them in the future**. Here are battle-tested strategies from computational laboratories that will serve you throughout your research career.

**The Psychology of Debugging:** When code fails, especially if you're new to Python or transitioning from Jupyter notebooks, the problem is often a bug in your code—a typo, incorrect indentation, wrong variable name, or logical error. These are normal and expected! However, before diving into line-by-line debugging, a quick environment check can save you hours if the problem is actually a missing package or wrong Python version. Think of it as triage: the environment check takes 5 seconds and catches ~30% of problems immediately. The other 70%? Those are real bugs that require careful debugging.

### The Universal First Check

Before examining your algorithm, before questioning whether your integrator is correctly implemented, before doubting your understanding of the equations—always, *always* verify your environment first. This simple discipline will save you hours of frustration:

**Why Environment Checks Matter:** Your code doesn't exist in isolation. It runs within a complex ecosystem of Python interpreters, installed packages, system libraries, and configuration files. A mismatch in any of these layers can cause mysterious failures. This is especially critical when moving code between laptops, workstations, and high-performance computing clusters.

:::{tip} Build Your Own Diagnostic Suite
:class: dropdown

```python
def check_python_location():
    """
    Step 1: Verify Python interpreter location.
    Build on this: Add your project-specific checks!

    Returns
    -------
    tuple
        (is_conda, environment_name)
    """
    import sys
    import os

    print("=" * 60)
    print("PYTHON LOCATION CHECK")
    print("=" * 60)

    exe_path = sys.executable
    print(f"Python path: {exe_path}")
    print(f"Version: {sys.version.split()[0]}")

    # Detect conda environment
    if 'conda' in exe_path or 'miniforge' in exe_path:
        env_name = exe_path.split(os.sep)[-3] if 'envs' in exe_path else "base"
        print(f"✓ Conda environment: {env_name}")
        return True, env_name
    else:
        print("✗ Not in conda environment")
        return False, None

# Example usage
is_conda, env = check_python_location()
```

```python
def check_critical_packages():
    """
    Step 2: Test essential packages.
    Customize this: Add your project-specific packages!

    Returns
    -------
    dict
        Package availability status
    """
    packages = {
        'numpy': 'Numerical arrays',
        'scipy': 'Scientific algorithms',
        'matplotlib': 'Visualization'
    }

    print("\nPACKAGE STATUS:")
    print("-" * 40)

    status = {}
    for pkg, desc in packages.items():
        try:
            mod = __import__(pkg)
            ver = getattr(mod, '__version__', '?')
            print(f"✓ {pkg:10} v{ver:8} - {desc}")
            status[pkg] = True
        except ImportError:
            print(f"✗ {pkg:10} MISSING   - {desc}")
            status[pkg] = False

    return status

# Build on this for your specific needs
package_status = check_critical_packages()
```

```python
def validate_computation_environment():
    """
    Step 3: Validate numerical computation settings.
    Extend this: Add checks for your specific calculations!

    Returns
    -------
    bool
        True if environment suitable for scientific computing
    """
    import numpy as np

    print("\nNUMERICAL ENVIRONMENT:")
    print("-" * 40)

    # Python "float" is (almost always) IEEE-754 float64, but your arrays may not be.
    print("float64 eps:", np.finfo(np.float64).eps)
    print("float32 eps:", np.finfo(np.float32).eps)

    arr = np.asarray([1.0])
    print("Example array dtype:", arr.dtype)

    print("✓ Environment suitable for numerical work")
    return True

# Combine all checks for complete validation
validated = validate_computation_environment()
```

These functions are starting points! For your research:

- Add checks for GPU libraries if doing simulations
- Include MPI validation for parallel codes
- Test specific numerical libraries
- Verify cluster-specific modules are loaded

Copy these functions and customize them for your specific computational needs throughout the semester! The few seconds it takes to run these can save hours of misguided debugging.
:::

### Using IPython's Debugger

When your code does crash — *and it will* — IPython's `%debug` magic command lets you perform a post-mortem examination. Think of it as having a time machine that takes you back to the moment of failure, letting you inspect all variables and understand exactly what went wrong:

**The Power of Post-Mortem Debugging:** Unlike adding print statements everywhere (which changes your code's behavior and timing), the debugger lets you explore the crash site without modifications. You can examine variables, test hypotheses, and even run new code in the context of the failure. This is invaluable when debugging complex algorithms.

```python
def process_data(values, threshold=0.0, *, raise_on_invalid=False):
    """
    Process values with threshold.

    Parameters
    ----------
    values : array-like
        Input values
    threshold : float
        Minimum valid value

    Returns
    -------
    array
        Processed results
    """
    import numpy as np

    values = np.asarray(values, dtype=float)
    x = values - threshold

    if raise_on_invalid:
        # By default, NumPy typically emits a RuntimeWarning and returns nan/-inf.
        # For debugging, it's often better to *raise* on invalid operations.
        with np.errstate(invalid="raise", divide="raise"):
            return np.log(x)

    return np.log(x)

# Example of debugging workflow
print("""When this crashes in IPython:

>>> values = [10, 5, -2, 20]  # Bad data!
>>> result = process_data(values, raise_on_invalid=True)
FloatingPointError: invalid value encountered in log

>>> %debug  # Enter debugger

ipdb> p values
[10, 5, -2, 20]

ipdb> p values[2]
-2  # Found the problem!

ipdb> import numpy as np
ipdb> threshold = 0.0
ipdb> np.where(np.array(values) - threshold <= 0)
(array([2]),)  # Index of bad value

ipdb> q  # Quit debugger

# Fix: Ensure log argument is positive (values - threshold > 0)
>>> threshold = 0.0
>>> good_values = [v for v in values if v - threshold > 0]
>>> result = process_data(good_values, threshold=threshold)
""")
```

---

## Section 1.7: Defensive Programming

You've spent the entire afternoon coding a complex calculation from scratch for tomorrow's homework. Every equation matches the textbook. You've triple-checked the math. This is it - your code will generate beautiful results.

You run it:

```bash
$ python calculation.py
Traceback (most recent call last):
  File "calculation.py", line 23, in calculate
    result = math.sqrt(term1 + term2)
ValueError: math domain error
```

Your heart sinks. But the equation is *right there* in the textbook, you *tripled checked* it! You add print statements. Run again. Different error. Now it's overflowing. *But it worked for small values! Why are large values breaking everything?*

**Welcome to the reality of scientific computing.** Your code will crash - not because you're bad at programming, but because tiny bugs are *invisible*. Maybe you typed `a + b` instead of `a * b`. Maybe there's a minus sign where there should be a plus. You can check it five times against the textbook and your brain will still autocorrect what you're reading to what you *meant* to write.

This is why we practice **defensive programming** - not because we're paranoid, but because *we're realistic*. The following strategies will transform your code from "works on my test case" to "works everywhere with any reasonable input." Every infinity you catch before it propagates, every convergence failure you detect early - these are the hallmarks of professional scientific software.

**Stage 1: Validate Physical Parameters**

```{code-cell} python
def validate_parameters(param_a, param_b, param_c):
    """Ensure parameters are in valid range."""
    # param_a reasonable range
    if not 0 < param_a < 100:
        raise ValueError(f"param_a={param_a} outside reasonable range (0,100)")

    # param_b must be positive
    if param_b < 0:
        raise ValueError("param_b must be positive")

    # Check constraint
    total = param_b + param_c
    if abs(total - 1.0) > 0.01:  # Allow 1% deviation
        print(f"Warning: Constraint violated (total = {total:.3f})")

    return True
```

**Stage 2: Protect Against Numerical Hazards**

```{code-cell} python
def safe_calculation(x, param_a, param_b):
    """
    Compute result with overflow protection.
    """
    import math

    # Validate input
    if x < 0:
        raise ValueError(f"x must be non-negative: {x}")
    if x > 1000:
        raise ValueError(f"x {x} exceeds maximum")

    # Protect against overflow for large x
    term1 = param_a * (1 + x)**3

    if term1 > 1e100:  # Would cause overflow
        # Use log space for extreme values
        log_result = 0.5 * (math.log10(param_a) + 3*math.log10(1+x))
        return 10**log_result

    result = math.sqrt(term1 + param_b)
    return result
```

**Stage 3: Monitor Convergence in Iterative Calculations**

```{code-cell} python
def iterative_calculation(x, param_a=0.3, param_b=0.7, tol=1e-6):
    """
    Calculate result with adaptive iteration.
    Shows defensive practices for iterative algorithms.
    """
    import math

    # Start with coarse iteration
    n_steps = 100
    converged = False
    max_iterations = 10

    for iteration in range(max_iterations):
        # Numerical integration
        dx = x / n_steps
        integral = 0.0

        for i in range(n_steps):
            x_i = i * dx
            x_next = (i + 1) * dx
            # Integrand
            f_i = safe_calculation(x_i, param_a, param_b)
            f_next = safe_calculation(x_next, param_a, param_b)
            integral += 0.5 * (1/f_i + 1/f_next) * dx

        # Check convergence (compare with previous iteration)
        if iteration > 0:
            rel_change = abs(integral - prev_integral) / abs(integral)
            if rel_change < tol:
                converged = True
                break

        prev_integral = integral
        n_steps *= 2  # Double resolution

    if not converged:
        print(f"Warning: Not converged after {iteration+1} iterations")

    result = (1 + x) * integral
    return result
```

Notice how most of this code isn't implementing the algorithm - it's protecting the algorithm from numerical disasters.

:::{important} Computational Thinking: Building Robust Code

These **defensive programming** patterns apply to ANY numerical work you'll implement:

**Parameter Validation**: Always check physical bounds

- Values must be in valid ranges
- Parameters must satisfy constraints
- Inputs must be appropriate types

**Overflow Protection**: Use appropriate representations

- Log space for products of large numbers
- Scaled units to keep numbers reasonable
- Early detection of problematic values

**Convergence Monitoring**: Don't trust, verify

- Compare successive iterations
- Set maximum iteration limits
- Warn when convergence fails
- Adaptive step sizes for efficiency
:::

---

## Main Takeaways

This chapter has revealed the hidden complexity underlying every Python analysis you'll perform. You've learned that when your code fails or produces different results on different systems, it's often the **environment** surrounding that code. Understanding this distinction transforms you from someone frustrated by `ImportError` to someone who systematically diagnoses and fixes environment issues in seconds.

**IPython** is more than an enhanced prompt - it's your scientific computing and data exploration laboratory. The ability to quickly test algorithms, explore new libraries, and time different approaches is fundamental to computational science. The **magic commands** like `%timeit` for benchmarking and `%debug` for post-mortem analysis aren't conveniences; they're essential tools for developing robust pipelines. Master IPython now, because you'll use it every day.

The **Jupyter notebook** trap is particularly dangerous in scientific computing where we often explore large datasets interactively. While notebooks seem perfect for examining data or creating plots, hidden state can make serious analysis fragile. That beautiful notebook showing your results might give different values each time it's run due to out-of-order execution. After Project 1, you'll transition to **scripts/pipelines** that make reproducibility much more reliable — especially when combined with pinned dependencies, fixed inputs, and controlled randomness.

Scripts enforce **reproducibility** through predictable execution. The `if __name__ == "__main__"` pattern enables you to build modular analysis tools that work both standalone and as part of larger pipelines — crucial for large projects where individual components must integrate into massive data processing systems.

Creating reproducible environments is about scientific integrity, not just convenience. When you can't reproduce your own results from six months ago because NumPy updated and changed its random number generator, you've lost crucial research continuity. The tools you've learned — **conda** environments with version pinning, `environment.yml` files for exact reproduction, proper path handling for cluster compatibility — are the foundation of trustworthy computational science.

---

## Key Takeaways

✓ **IPython is your primary scientific computing tool**: Use it for testing algorithms, exploring data, and rapid prototyping — not the basic Python REPL

✓ **Environment problems cause most "broken" analysis code**: When imports fail, check your environment first with `sys.executable` and `conda list`

✓ **Notebooks can corrupt scientific analysis**: Hidden state and execution ambiguity can make results irreproducible — use them only for initial exploration

✓ **Scripts support reproducibility**: Top-to-bottom execution eliminates a major source of ambiguity; reproducibility still requires pinned deps, fixed inputs, and controlled randomness

✓ **The `__name__` pattern enables pipeline integration**: Code can be both a standalone tool and an importable module

✓ **Conda environments isolate projects**: Each project can have its own package versions without conflicts

✓ **Always version-pin packages**: Use `environment.yml` files to ensure collaborators can reproduce your exact analysis

✓ **Paths must be configurable**: Use environment variables and Path objects for code that works on both laptops and clusters

✓ **Control randomness with seeds**: Always set and document random seeds for Monte Carlo simulations

✓ **Systematic debugging saves time**: Environment check $\to$ verify imports $\to$ test with known data

✓ **Defensive programming handles messy data**: Assume bad values, missing data, and edge cases

---

## Quick Reference Tables

### Essential IPython Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `%timeit` | Time code execution | `%timeit process(data)` |
| `%run` | Run script keeping variables | `%run analysis.py` |
| `%debug` | Debug after error | Debug failed extraction |
| `%who` | List variables | Check loaded data |
| `%whos` | Detailed variable info | Inspect array dimensions |
| `%matplotlib` | Configure plotting | `%matplotlib inline` |
| `%load` | Load code file | `%load utils.py` |
| `%save` | Save session code | `%save session.py 1-50` |
| `?` | Quick help | `np.fft.fft?` |
| `??` | Show source | `function??` |

### Environment Debugging

| Check | Command | What to Look For |
|-------|---------|------------------|
| Python location | `which python` | Should show conda environment |
| Package version | `python -c "import pkg; print(pkg.__version__)"` | Correct version |
| Environment name | `conda info --envs` | Asterisk marks active |
| Packages | `conda list | grep pkg` | Package present |
| Import works | `python -c "from pkg import mod"` | Should import without error |
| Data paths | `echo $PROJECT_DATA` | Your data directory |

---

## Next Chapter Preview

Now that you've mastered your computational environment, Chapter 2 will transform Python into a powerful scientific calculator. You'll discover why `0.1 + 0.2 $\neq$ 0.3` matters when doing numerical calculations, learn how floating-point errors compound during numerical integration, and understand why some calculations require extra precision. You'll implement algorithms for transformations, conversions, and computations — all while managing the numerical precision that separates successful results from incorrect ones. Get ready to understand why numerical errors happen and how to prevent similar problems in your computations!
