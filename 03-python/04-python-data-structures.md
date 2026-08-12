---
title: "Chapter 4: Data Structures - Organizing Scientific Data"
subtitle: "Python Fundamentals | COMP 521"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
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

## Learning Objectives

By the end of this chapter, you will be able to:

- [ ] (1) **Choose optimal data structures** (`list`, `tuple`, `dict`, `set`) based on algorithmic requirements and **O(n)** vs **O(1)** performance constraints.
- [ ] (2) **Predict operation complexity** using Big-O notation for common operations like search, insertion, and deletion.
- [ ] (3) **Understand Python's reference model** and memory layout explaining why NumPy arrays are often 10-100$\times$ faster than lists for vectorized operations.
- [ ] (4) **Implement defensive copying strategies** using `copy.copy()` and `copy.deepcopy()` to prevent aliasing bugs.
- [ ] (5) **Profile memory usage** with `sys.getsizeof()` and optimize data structure choices for particle simulations.
- [ ] (6) **Master dictionary operations** for O(1) lookups using hash tables for caching expensive calculations.
- [ ] (7) **Apply set operations** (union, intersection, difference) for particle tracking and domain decomposition.
- [ ] (8) **Debug three common bugs**: mutable defaults, aliasing during grid updates, and iteration modification.
- [ ] (9) **Design hybrid data structures** combining lists, dicts, and sets for real physics simulations.

:::{note} ✅ Before Starting This Chapter

- [ ] You can write loops and conditional statements fluently (Chapter 3)
- [ ] You understand the difference between assignment and equality (Chapter 2)
- [ ] You can use IPython for testing and timing code (Chapter 1)
- [ ] You understand floating-point precision issues (Chapter 2)
- [ ] You understand defensive programming principles (Chapter 1)

If any boxes are unchecked, review the indicated chapters first.
:::

## Chapter Overview

Imagine you're simulating the interactions between a million particles - whether they're dark matter particles in a galaxy, molecules in a gas, or nodes in a network. Each timestep, you need to find which particles are close enough to interact strongly. With the wrong data structure, this neighbor search could take hours per timestep. With the right one - a spatial hash table or tree structure - it takes seconds. That's the difference between a simulation finishing in a day versus running for months. This chapter teaches you to make these critical choices that determine whether your code scales to research problems or remains stuck with toy models.

This chapter transforms you from someone who stores data to someone who orchestrates it strategically for scientific computing. You'll discover not just that dictionary lookups are fast, but *why* they're fast - through hash functions that turn particle positions into array indices. You'll understand *when* they might fail - like when hash collisions cluster your data. And you'll learn *how* to verify performance yourself - because in computational science, measurement beats assumption every time.

These concepts directly prepare you for the numerical computing ahead. The memory layout discussions explain why NumPy arrays can be 10-100$\times$ more efficient than Python lists for vectorized operations. The immutability concepts prepare you for functional programming paradigms used in modern frameworks like JAX, where immutable operations enable automatic differentiation. The performance profiling skills will help you identify bottlenecks whether you're solving differential equations or analyzing experimental data. By chapter's end, you'll think about data organization like a computational scientist, architecting for performance from the start.

In Chapter 3, you learned how algorithms *flow* through decisions and loops. In Chapter 4, you'll learn how algorithms *scale*—because data structures determine whether your logic runs in seconds or in days.

:::{important} TL;DR — Why This Chapter Is a Turning Point

Most courses teach data structures as a list of methods to memorize. This chapter teaches something more useful: **how to choose a structure that makes your algorithm feasible**.

If you internalize this chapter, you'll start thinking like a computational scientist:

- You'll design around **access patterns** (what you need to look up, update, or traverse).
- You'll predict when code will **scale** to large problems — and when it will explode.
- You'll avoid whole classes of bugs by using **immutability** and careful copying.
- You'll measure performance instead of guessing (because in science, **measurement beats assumption**).

You do not need to memorize everything here. You *do* want to revisit this chapter all semester—especially when your code starts getting slow, memory-hungry, or mysteriously wrong.
:::

:::{note} How to Use This Chapter

Treat this chapter as a **reference and toolbox**, not something to read once and memorize.

A good workflow is:

1. Identify your problem's access pattern (search, lookup, append, membership, caching).
2. Choose the simplest structure that matches that pattern.
3. Measure performance with small benchmarks when in doubt.
4. Revisit this chapter when your code hits performance or correctness walls.

If this material feels "advanced," that's normal. It clicks fastest when you apply it to real code.
:::

## 4.1 What Is a Data Structure?

:::{margin}
**data structure**
A way of organizing data in memory to enable efficient access and modification
:::

A **data structure** is fundamentally about organizing information to match your access patterns. Think about an N-body simulation where particles interact through forces - these particles could represent stars in a star cluster, molecules in a gas, or charges in a plasma. You could store particles in order of creation (like a **list**), organize them by spatial region for fast neighbor finding (like a **dictionary** of cells), or track unique particle IDs (like a **set**). Each choice profoundly affects your simulation's performance - the difference between **O($\mathrm{n}^{2}$)** all-pairs checks and **O(n log n)** tree-based algorithms.

:::{margin}
**Big-O notation (e.g, O($\mathrm{n}^{2}$), O(n log n))**
Big-O notation describing how runtime scales with input size n.
:::

### Quick Preview: Python's Core Data Structures

| Structure | Mutable | Ordered | Duplicates | Use Case |
|-----------|---------|---------|------------|----------|
| **list** | Yes | Yes | Yes | Particle arrays, time series |
| **tuple** | No | Yes | Yes | Constants, coordinates, dict keys |
| **dict** | Yes | Yes* | Keys: No | Lookup tables, properties |
| **set** | Yes | No | No | Unique particles, membership |

*Dicts maintain insertion order (Python 3.7+ language guarantee)

### Decision Framework: Choosing Your Data Structure

Before diving into each structure, here's the mental model for choosing:

```
Need ordered sequence with duplicates?
├── Yes -> Need to modify it?
│         ├── Yes -> list
│         └── No (constants/config) -> tuple
└── No -> Need key-value mapping?
          ├── Yes -> dict (O(1) lookup by key)
          └── No -> Need uniqueness/set math?
                    ├── Yes -> set (O(1) membership)
                    └── No -> Probably list
```

**Key invariants to remember:**

| Structure | Mutable? | Keys/Elements Must Be... | When to Use |
|-----------|----------|-------------------------|-------------|
| `list` | Yes | Anything | Ordered data, will modify |
| `tuple` | No | Anything | Constants, dict keys, records |
| `dict` | Yes | **Hashable** (immutable) | Fast lookup by key |
| `set` | Yes | **Hashable** (immutable) | Uniqueness, membership tests |

:::{note} What Does "Hashable" Mean?

An object is **hashable** if it has a hash value that never changes during its lifetime. In practice:

- **Hashable**: `int`, `float`, `str`, `tuple` (if contents hashable), `frozenset`
- **Not hashable**: `list`, `dict`, `set` (because they're mutable)

This is why you can use tuples as dict keys but not lists!
:::

:::{tip} Quick Reflection (1 minute)

Think of the last piece of code you wrote (in this course or elsewhere). Where did it spend most of its time: searching, looping, looking up values, or building results? That answer usually tells you which data structure matters most.
:::

:::{tip} 🌟 The More You Know: When Data Structures Cost Billions
:class: dropdown

**Ariane 5 (1996) - $370M lost**: A 64-bit float was cast to 16-bit int without bounds checking. Integer overflow crashed the rocket 39 seconds after launch.[^ariane5]

**Mars Pathfinder (1997) - Near mission loss**: Priority inversion in a task queue caused system resets on Mars. JPL debugged it from 50 million miles away.[^mars-pathfinder]

**Cassini (2006) - Data loss risk**: Wrong buffer structure caused data loss during communication transitions. Fixed with a circular buffer (`deque`-like structure).[^cassini]

Each disaster traces to a data structure choice. Bounds checking, queue design, buffer management - these "basic" concepts have billion-dollar consequences.

***
[^ariane5]: Lions, J.L., et al. (1996). "Ariane 5 Flight 501 Failure Report." ESA/CNES.
[^mars-pathfinder]: Jones, M.B. (1997). "What Really Happened on Mars." Microsoft Research.
[^cassini]: Anderson, Y.Z., et al. (2006). "Solving Cassini's Data Glitch Problem." NASA/JPL.
:::

### Building Intuition: Measuring Speed Empirically

Ready to discover something that will transform how you think about organizing data in your simulations? We're going to measure the dramatic performance difference between different data structures. This empirical approach - measure first, understand why, then optimize - is exactly how computational scientists approach performance optimization.

```{code-cell} python
# Let's discover why data structure choice matters for simulations!
import timeit

def benchmark_membership(n, trials=1000):
    """Compare list vs set membership testing with proper statistics."""
    # Create particle ID collections
    particle_list = list(range(n))
    particle_set = set(range(n))

    # Search for a particle NOT in the collection (worst case for list)
    escaped_particle = -1

    # Time list search - repeat many times for statistical validity
    list_time = timeit.timeit(
        lambda: escaped_particle in particle_list,
        number=trials
    ) / trials

    # Time set search
    set_time = timeit.timeit(
        lambda: escaped_particle in particle_set,
        number=trials
    ) / trials

    return list_time, set_time

print("Membership testing: list (O(n)) vs set (O(1))")
print("=" * 55)
print(f"{'Size':>10} {'List (mus)':>12} {'Set (mus)':>12} {'Speedup':>10}")
print("-" * 55)

for n in [100, 1_000, 10_000, 100_000]:
    list_time, set_time = benchmark_membership(n)
    speedup = list_time / set_time if set_time > 0 else float('inf')
    print(f"{n:>10,} {list_time*1e6:>12.2f} {set_time*1e6:>12.2f} {speedup:>10,.0f}x")

print("\nAs n grows, list time grows proportionally (O(n))")
print("while set time stays nearly constant (O(1)).")
print("\nFor simulations with many membership checks,")
print("this can mean the difference between minutes and hours!")
```

This performance difference isn't just academic - it determines whether your galaxy simulation can evolve for billions of years or gets stuck after a few million. The secret behind this magic is the hash table, which you're about to understand completely.

### Understanding Big-O Notation

Now that you've witnessed this dramatic performance difference empirically, let's understand the mathematical pattern behind it. **Big-O notation** describes how an algorithm's runtime scales with input size - it's the language computational scientists use to discuss whether an algorithm is feasible for large-scale simulations.

Big-O describes how runtime grows with input size—not the exact speed—so constants, memory layout, and access patterns still matter.

**Complexity Scaling for Physics Simulations:**

| Complexity | 1,000 particles | 1,000,000 particles | Example |
|------------|-----------------|---------------------|---------|
| O(1) | 1 op | 1 op | Hash table lookup |
| O(log n) | 10 ops | 20 ops | Tree traversal |
| O(n) | 1,000 ops | 1,000,000 ops | Direct summation |
| O(n log n) | 10,000 ops | 20,000,000 ops | Tree codes (GADGET) |
| O($\mathrm{n}^{2}$) | 1,000,000 ops | 1,000,000,000,000 ops | All-pairs (impossible!) |

:::{note} 📊 Visualization: Big-O Scaling (click to expand)
:class: dropdown

```python

import matplotlib.pyplot as plt
import math

# Visualize how different algorithms scale for physics simulations
n = range(1, 101)
constant = [1 for _ in n]
logarithmic = [math.log2(x) if x > 0 else 0 for x in n]
linear = list(n)
nlogn = [x * math.log2(x) if x > 0 else 0 for x in n]
quadratic = [x**2 for x in n]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(n, constant, label='O(1) - Hash table lookup', linewidth=2)
ax.plot(n, logarithmic, label='O(log n) - Binary search', linewidth=2)
ax.plot(n, linear, label='O(n) - Linear scan', linewidth=2)
ax.plot(n, nlogn, label='O(n log n) - Tree codes', linewidth=2, linestyle='--')
ax.plot(n, quadratic, label='O(n^2) - All-pairs', linewidth=2)

ax.set_xlim(0, 100)
ax.set_ylim(0, 500)
ax.set_xlabel('Number of Particles (thousands)', fontsize=12)
ax.set_ylabel('Operations (arbitrary units)', fontsize=12)
ax.set_title('Algorithm Scaling: Why Data Structures Matter', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```
:::

```{code-cell} python
import math

print("For a million-particle simulation:")
print(f"  O(1):       1 operation           - spatial hash lookup")
print(f"  O(log n):   {math.log2(1e6):.0f} operations         - tree traversal")
print(f"  O(n):       1,000,000 operations  - direct force sum")
print(f"  O(n log n): {1e6 * math.log2(1e6):.0e} operations - tree codes")
print(f"  O(n^2):      1,000,000,000,000 ops - all pairs (impossible!)")

print("\nIn astronomy: This enables galaxy simulations with billions of stars")
print("In chemistry: This allows protein folding with millions of atoms")
print("In climate: This permits global models with millions of grid cells")
```

The table above reveals why algorithmic complexity matters for computational physics. The naive **O($\mathrm{n}^{2}$)** approach that checks all particle pairs becomes impossible beyond a few thousand particles. But with smart **data structures** like trees (**O(n log n)**) or spatial hashing (**O(n)**), we can simulate entire galaxies, proteins, or climate systems!

:::{important} 💡 Computational Thinking: The Time-Space Tradeoff in Physics Simulations

This universal pattern appears throughout computational physics: trading memory for speed.

**The Pattern:**
- Use more memory $\to$ organize data cleverly $\to$ enable faster computation
- Use less memory $\to$ simpler organization $\to$ slower computation

**Real Physics Examples:**
- **Particle mesh methods**: Store density on a grid (memory) to avoid O($\mathrm{n}^{2}$) particle interactions
- **Neighbor lists**: Store nearby particles (memory) vs O($\mathrm{n}^{2}$) distance checks for every step
- **Tree codes**: Store spatial hierarchy (memory) for O(n log n) force calculation
- **Lookup tables**: Store pre-computed values vs recalculating expensive functions
- **FFT methods**: Store complex coefficients for O(n log n) vs O($\mathrm{n}^{2}$) convolution

In astronomy, the GADGET cosmology code uses 200 bytes per particle (vs 24 for just position/velocity) to achieve O(n log n) scaling, enabling billion-particle dark matter simulations. This 8$\times$ memory cost enables 1000$\times$ speedup!
:::

## 4.2 Lists: Python's Workhorse Sequence

**Lists** are Python's most versatile **data structure** - perfect for particle arrays, time series data, or any ordered collection. But here's something crucial for scientific computing: Python **lists** don't store your numbers directly! Understanding this explains why NumPy arrays are so much faster for numerical work.

### How Lists Really Work in Memory

Let's explore how Python actually stores your simulation data in memory. This knowledge will help you understand when to use Python **lists** versus when you need NumPy arrays.

```{code-cell} python
# Stage 1: Basic memory inspection (10 lines)
import sys

# Position of one particle in 3D space
position = [1.5e10, 2.3e10, 0.8e10]  # cm (typical scale for solar system)

# The list container itself
list_size = sys.getsizeof(position)
print(f"List container: {list_size} bytes")

# Each float is a full Python object!
element_sizes = [sys.getsizeof(x) for x in position]
print(f"Each coordinate: {element_sizes[0]} bytes")
```

:::{important} ⚠️ `sys.getsizeof()` Measures Shallow Size Only

`sys.getsizeof()` returns the memory used by the **container object itself**, not including the objects it contains. For nested structures, use recursive measurement:

```python
# Shallow: just the list container
sys.getsizeof(position)  # ~80 bytes

# Deep: container + all contained objects
total = sys.getsizeof(position) + sum(sys.getsizeof(x) for x in position)
```

For accurate deep memory profiling, use `pympler.asizeof()` or write a recursive helper. This distinction is critical when optimizing memory for large simulations.
:::

```{code-cell} python
# Stage 2: Calculate total overhead (10 lines)
# Total memory footprint
total = list_size + sum(element_sizes)
print(f"Total: {total} bytes for 3 floats!")
print(f"That's {total/24:.1f}x more than raw floats would need!")

print("\nWhy so much memory?")
print("- List stores pointers, not values")
print("- Each float is a full object with type info")
print("- Python must track reference counts")
print("\nThis is why NumPy arrays (Chapter 7) store raw values contiguously!")
```

Here's what's actually happening in memory when you store particle positions:

```
Python List of Positions:          Objects in Memory:
┌─────────────────┐               ┌──────────────────┐
│ size: 3         │               │ float: 1.5e10    │
│ capacity: 4     │          ┌───>│ type info        │
├─────────────────┤          │    │ ref count        │
│ pointer ────────┼──────────┘    └──────────────────┘
│ pointer ────────┼──────────────>┌──────────────────┐
│ pointer ────────┼──────┐        │ float: 2.3e10    │
│ (unused)        │    │          └──────────────────┘
└─────────────────┘    └────────>┌──────────────────┐
                                  │ float: 0.8e10    │
                                  └──────────────────┘

NumPy Array (preview):
┌────┬────┬────┐
│1.5 │2.3 │0.8 │  <- Raw values, no pointers!
└────┴────┴────┘
```

### List Operations: Performance for Simulations

Different **list** operations have vastly different costs - critical knowledge when processing particle data or building spatial **data structures**.

```{code-cell} python
import time

# Simulate a growing particle system
particles = list(range(100_000))

# Adding particles at the END (common pattern)
start = time.perf_counter()
particles.append(100_000)  # New particle enters domain
particles.pop()            # Remove for fair comparison
end_time = time.perf_counter() - start

# Adding particles at the BEGINNING (avoid this!)
start = time.perf_counter()
particles.insert(0, -1)    # Insert at front
particles.pop(0)           # Remove from front
begin_time = time.perf_counter() - start

print(f"Adding particle at END:   {end_time*1e6:.2f} microseconds")
print(f"Adding particle at START: {begin_time*1e6:.2f} microseconds")
print(f"\nBeginning is {begin_time/end_time:.0f}x slower!")

print("\nWhy? Inserting at the beginning shifts ALL particles in memory!")
print("For particle systems, use collections.deque if you need")
print("fast operations at both ends (e.g., boundary conditions).")
```

:::{tip} 💡 Performance Tip: When Both Ends Matter

If your simulation needs fast operations at both ends (like particles entering/leaving through boundaries), use `collections.deque`:

```python
from collections import deque
particles = deque(maxlen=1000000)  # Efficient at both ends!
```

This is particularly useful in molecular dynamics where particles cross periodic boundaries, or in astronomical simulations tracking objects entering and leaving a field of view.
:::

### List Growth Strategy: Understanding Dynamic Arrays

Watch how Python manages memory as your particle system grows. This pattern appears in many languages and understanding it helps you write efficient simulation codes.

```{code-cell} python
# Stage 1: Basic growth observation (12 lines)
import sys

particles = []
print("Watch Python's list growth strategy:")
print("(Critical for understanding simulation performance)")
print("Length -> Capacity (overallocation)")
print("-" * 40)

for i in range(10):
    old_size = sys.getsizeof(particles)
    particles.append(i)
    new_size = sys.getsizeof(particles)

    if new_size != old_size:
        print(f"{len(particles):4d} -> larger allocation")
```

```{code-cell} python
# Stage 2: Observe growth pattern (12 lines)
# Note: Exact capacity inference is CPython/64-bit specific
# We observe the PATTERN, not exact numbers
particles = []
previous_size = sys.getsizeof(particles)

print("\nWatch list grow with overallocation:")
print("Length -> Size change")
print("-" * 30)

for i in range(20):
    particles.append(i)
    current_size = sys.getsizeof(particles)

    if current_size != previous_size:
        print(f"Length {len(particles):4d} -> +{current_size - previous_size:4d} bytes")
        previous_size = current_size

print("\nKey insight: Python overallocates to make future")
print("appends O(1) amortized. Exact growth factor is")
print("implementation-dependent (~1.125x in CPython).")
```

This growth pattern is why appending to lists is "**amortized** O(1)" - usually fast, occasionally slow when reallocation happens. For time-critical simulations, pre-allocate your arrays when particle count is known!

:::{margin}
**amortized**
Average cost over many operations, even if individual operations vary
:::

## 4.3 Tuples: The Power of Immutability

:::{margin}
**immutable**
Objects whose state cannot be modified after creation
:::

What if you need to guarantee that initial conditions or physical constants won't change during your simulation? Enter **tuples** - Python's **immutable** sequences. This isn't a limitation - it's protection against an entire category of bugs that plague scientific codes!

:::{warning} ⚠️ Common Bug Alert: The Accidental Modification Disaster

One of the most insidious bugs in computational physics happens when functions unexpectedly modify their inputs. Remember the defensive programming principles from Chapter 1? Here's why they matter:

```python
# THE BUG THAT CORRUPTS YOUR SIMULATION:
def evolve_system(state, dt):
    # Trying to be clever, modifying in-place
    state[0] += state[1] * dt  # Modifies original!
    state[1] += calculate_force(state[0]) * dt
    return state

initial_state = [1.0, 0.0]  # Position, velocity
state_t1 = evolve_system(initial_state, 0.01)
print(initial_state)  # [1.01, ...] - Initial conditions corrupted!

# THE FIX: Use tuples to prevent modification
initial_state = (1.0, 0.0)  # Tuple!
# Now modification attempts raise errors immediately!
```

This connects directly to Chapter 1's defensive programming: catch errors early, fail loudly!
:::

### Understanding Immutability in Physics Simulations

Let's see how **immutability** protects your simulations and enables powerful optimizations:

```{code-cell} python
# Physical constants should NEVER change during simulation
class PhysicsConstants:
    """Demonstrating safe vs unsafe constant storage."""

    # UNSAFE: Mutable list (can be accidentally modified)
    unsafe_constants = [
        6.674e-8,   # G (cm^3/g/s^2)
        2.998e10,   # c (cm/s)
        1.381e-16,  # k_B (erg/K)
    ]

    # SAFE: Immutable tuple (modification attempts fail loudly)
    safe_constants = (
        6.674e-8,   # G (cm^3/g/s^2)
        2.998e10,   # c (cm/s)
        1.381e-16,  # k_B (erg/K)
    )

# Demonstration of the danger
def convert_units_buggy(constants):
    """
    BUG: Accidentally modifies shared constants!

    The programmer intended to CREATE a converted copy,
    but instead MUTATED the original list in-place.
    This is a realistic bug in scientific codes.
    """
    if isinstance(constants, list):
        # BUG: In-place modification when we meant to copy!
        # Programmer forgot to make a copy first
        constants[0] = constants[0] * 1e3  # "Convert G to different units"
        return constants
    else:
        # With tuple, modification fails loudly
        try:
            constants[0] = constants[0] * 1e3
        except TypeError as e:
            return f"Caught bug immediately: {e}"

# Test with both
print("With mutable list:")
original_G = PhysicsConstants.unsafe_constants[0]
result = convert_units_buggy(PhysicsConstants.unsafe_constants)
print(f"  G was: {original_G:.3e}, now: {PhysicsConstants.unsafe_constants[0]:.3e}")
print(f"  Constants CORRUPTED!")

# Reset for tuple demo
PhysicsConstants.unsafe_constants[0] = 6.674e-8

print("\nWith immutable tuple:")
result = convert_units_buggy(PhysicsConstants.safe_constants)
print(f"  {result}")

print("\nLesson: Immutability turns silent corruption into immediate, loud errors!")
```

### Tuples as Dictionary Keys: Caching Expensive Calculations

Here's where **immutability** becomes a superpower for computational physics - **tuples** can be **dictionary** keys, enabling powerful **memoization** patterns for expensive calculations.

:::{warning} ⚠️ Caching with Floats is Dangerous

Never use raw floating-point values as cache keys! Tiny representation differences (e.g., `1.0000000001` vs `1.0`) cause cache misses. Always use:

- **Discrete indices**: `(T_index, rho_index)`
- **Rounded values**: `(round(T, -3), round(rho, 6))`
- **Grid bin IDs**: `(T_bin, rho_bin, composition_id)`
:::

```{code-cell} python
# Equation of State lookup table with discrete grid indices
# This is how real stellar evolution codes work!

eos_cache = {}
calculation_count = 0

def get_pressure(T_index, rho_index, composition_id):
    """
    Look up pressure from equation of state table.

    Keys are discrete indices into pre-computed grids,
    NOT raw floating-point values (which would cause cache misses).
    """
    global calculation_count

    # Cache key uses discrete, hashable indices
    cache_key = (T_index, rho_index, composition_id)

    if cache_key in eos_cache:
        return eos_cache[cache_key]

    calculation_count += 1
    # Simulate expensive EOS calculation
    # Real codes interpolate from pre-computed tables
    T = 1e6 * (1.1 ** T_index)      # Temperature grid
    rho = 1e-3 * (1.2 ** rho_index)  # Density grid

    # Ideal gas approximation (real EOS is much more complex)
    k_B = 1.381e-16  # erg/K
    mu = 0.6 if composition_id == 0 else 1.3  # mean molecular weight
    m_H = 1.673e-24  # g

    pressure = rho * k_B * T / (mu * m_H)

    eos_cache[cache_key] = pressure
    return pressure

# Simulate stellar evolution lookups
print("EOS lookups during stellar evolution:")
print("-" * 45)

# First calculation at this grid point
P1 = get_pressure(T_index=10, rho_index=5, composition_id=0)
print(f"First lookup:  P = {P1:.2e} dyne/cm^2")

# Same grid point - cache hit!
P2 = get_pressure(T_index=10, rho_index=5, composition_id=0)
print(f"Second lookup: P = {P2:.2e} dyne/cm^2 (cache hit!)")

# Different grid point
P3 = get_pressure(T_index=11, rho_index=5, composition_id=0)
print(f"New point:     P = {P3:.2e} dyne/cm^2")

print(f"\nTotal expensive calculations: {calculation_count}")
print("Cache hits avoid recalculation entirely!")
```

This pattern is fundamental to stellar evolution codes like MESA, which use pre-computed opacity and equation of state tables with discrete grid indices for O(1) lookup.

:::{tip} 🤔 Check Your Understanding

You're storing 1 million particle positions. Calculate the memory difference between:

1. List of lists: `[[x, y, z] for _ in range(1_000_000)]`
2. List of tuples: `[(x, y, z) for _ in range(1_000_000)]`
3. Single flat list: `[x1, y1, z1, x2, y2, z2, ...]`

Which is most memory efficient? Which is easiest to use?

**Solution:** Tuples save ~10% memory over lists. Single flat list is most memory efficient but harder to work with. This is why NumPy uses flat arrays internally with views for usability!
:::

:::{note} 🎯 Why This Matters: Lookup Tables Beat Recalculation
:class: dropdown

Stellar evolution codes like MESA use pre-computed opacity and equation of state tables rather than calculating these values from first principles at every timestep[^mesa]. The choice of data structure for storing and accessing these tables matters: O(1) dictionary lookups are faster than O(n) list searches, especially when accessed repeatedly throughout a simulation.

***
[^mesa]: Paxton et al. (2011). "Modules for Experiments in Stellar Astrophysics (MESA)." *ApJS*, 192, 3.
:::

## 4.4 The Mutable vs Immutable Distinction

Time for one of Python's most important concepts for scientific computing! Understanding **mutability** is the key to avoiding mysterious bugs where your simulation state changes unexpectedly. This connects directly to Chapter 1's defensive programming principles - catching errors early prevents corrupted results.

### Python's Reference Model in Physics Simulations

Python doesn't store values in variables - it stores **references** to objects. This has profound implications for simulation codes:

```{code-cell} python
# Critical concept for simulation state management!

print("With IMMUTABLE objects (safe for constants):")
G_constant = 6.674e-8
G_backup = G_constant
print(f"Initially: G={G_constant:.3e}, backup={G_backup:.3e}")
print(f"Same object in memory? {G_constant is G_backup}")

G_backup = 6.674e-7  # Creates NEW object (typo won't affect original)
print(f"After change: G={G_constant:.3e}, backup={G_backup:.3e}")
print("Original constant is safe!")

print("\n" + "="*50)
print("With MUTABLE objects (dangerous for state!):")

# Particle system state
particles = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]  # Positions
backup = particles  # Think you're making a backup?

print(f"Initially: same object? {particles is backup}")

# Modify what you think is the backup
backup[0][0] = 999.0  # Trying to test something

print(f"Original particles: {particles}")
print(f"'Backup': {backup}")
print("You just corrupted your simulation state!")

print("\nLesson: Use copy.deepcopy() for simulation state backups!")
```

:::{tip} 🌟 The More You Know: Knight Capital's $440 Million Software Disaster
:class: dropdown

On August 1, 2012, Knight Capital Group lost $440 million in 45 minutes due to a software deployment error that created unintended feedback loops in their trading $\mathrm{system}^{1}$.

According to SEC filings and news reports, Knight was updating their trading software to handle a new NYSE order type. The deployment went to 7 of their 8 servers correctly, but one server retained old test code from 2003. When the market opened, this server began processing live orders using the old "Power Peg" test functionality, which was designed to continuously buy and sell stocks for **testing purposes**.

The catastrophic interaction occurred because:

- Both old and new code read from the same order queue (shared data structure)
- The old code interpreted a flag differently than the new code
- No validation existed to detect incompatible code versions
- The shared state created a feedback loop of unintended trades

In 45 minutes, the malfunctioning system:

- Executed over 4 million unintended trades
- Accumulated $7 billion in unwanted positions
- Generated 10% of total US market volume that morning
- Lost $10 million per minute

This disaster illustrates critical data structure principles:

- **Shared mutable state** between incompatible systems is dangerous
- **Queue structures** without version validation can corrupt workflows
- **Missing defensive checks** on shared data structures cascade failures
- A single **configuration dictionary** misinterpretation can destroy a company

Knight Capital, once the largest US equity trader, was acquired within a week for a fraction of its previous value. **The lesson**: when multiple systems share data structures, defensive programming and validation aren't optional—they're essential.[^knight-capital]

***
[^knight-capital]: "Knight Capital Says Trading Mishap Cost It $440 Million." [*The New York Times*](https://archive.nytimes.com/dealbook.nytimes.com/2012/08/02/knight-capital-says-trading-mishap-cost-it-440-million/), August 2, 2012. SEC Release No. 70694 (October 16, 2013).
:::

### The Classic Mutable Default Argument Bug

This bug is so dangerous that Python linters specifically check for it. It's particularly insidious in iterative simulations:

```{code-cell} python
# Stage 1: Demonstrate the bug (15 lines)
# THE BUG: Default mutable created ONCE at function definition!
def accumulate_energies_buggy(energy, history=[]):
    """BUGGY: Trying to track energy history."""
    history.append(energy)
    return history

# Simulate multiple independent runs
print("Run 1:")
run1 = accumulate_energies_buggy(100)
run1 = accumulate_energies_buggy(95)
print(f"  Energy history: {run1}")

print("\nRun 2 (should be independent):")
run2 = accumulate_energies_buggy(200)
print(f"  Energy history: {run2}")
print("  Contains Run 1 data! Runs are coupled!")
```

```{code-cell} python
# Stage 2: Show the fix (15 lines)
print("THE FIX: Use None sentinel pattern")

def accumulate_energies_fixed(energy, history=None):
    """Safe version - creates new list for each run."""
    if history is None:
        history = []  # Fresh list for each simulation
    history.append(energy)
    return history

print("\nRun 3:")
run3 = accumulate_energies_fixed(100)
run3 = accumulate_energies_fixed(95)
print(f"  Energy history: {run3}")

print("\nRun 4 (properly independent):")
run4 = accumulate_energies_fixed(200)
print(f"  Energy history: {run4}")
print("  Runs are independent!")
```

### Shallow vs Deep Copies in Grid Simulations

This distinction is critical for grid-based simulations in computational fluid dynamics, stellar atmospheres, or any field-based calculation:

```{code-cell} python
# Stage 1: Set up the problem (12 lines)
import copy

# Create a 2D grid for temperature distribution
print("Simulating heat diffusion on a grid:")
grid = [[20.0, 20.0, 20.0],
        [20.0, 50.0, 20.0],  # Hot spot in center
        [20.0, 20.0, 20.0]]
print(f"Initial grid: {grid[1]}")  # Middle row

# Shallow copy - DANGEROUS for grids!
print("\n--- SHALLOW COPY (aliases inner arrays) ---")
grid_next_shallow = grid.copy()
```

```{code-cell} python
# Stage 2: Show the shallow copy problem (10 lines)
# Try to update center point for next timestep
grid_next_shallow[1][1] = 35.0  # Cooling

print(f"Original grid center: {grid[1][1]} degC")
print(f"Next step grid center: {grid_next_shallow[1][1]} degC")
print("Modified both grids! Simulation is corrupted!")

# Reset for deep copy demo
grid = [[20.0, 20.0, 20.0],
        [20.0, 50.0, 20.0],
        [20.0, 20.0, 20.0]]
```

```{code-cell} python
# Stage 3: Show the deep copy solution (12 lines)
# Deep copy - SAFE for grids!
print("\n--- DEEP COPY (independent arrays) ---")
grid_next_deep = copy.deepcopy(grid)
grid_next_deep[1][1] = 35.0  # Cooling

print(f"Original grid center: {grid[1][1]} degC")
print(f"Next step grid center: {grid_next_deep[1][1]} degC")
print("Grids are independent! Simulation is correct!")

print("\nMemory visualization:")
print("Shallow: grid -> [ref1, ref2, ref3] -> same inner arrays")
print("Deep:    grid -> [ref1, ref2, ref3] -> independent arrays")
```

:::{tip} 💡 Professional Pattern: Ping-Pong Buffers

For iterative grid updates (heat equation, fluid dynamics), `deepcopy` is too slow. Use the **ping-pong buffer** pattern instead:

```python
# Allocate TWO grids once at the start
size = 100
grid_a = [[0.0] * size for _ in range(size)]
grid_b = [[0.0] * size for _ in range(size)]

# Point current/next to the grids
current = grid_a
next_step = grid_b

# Simulation loop
for timestep in range(1000):
    # Compute next_step from current
    for i in range(1, size-1):
        for j in range(1, size-1):
            # Heat diffusion stencil
            next_step[i][j] = 0.25 * (
                current[i+1][j] + current[i-1][j] +
                current[i][j+1] + current[i][j-1]
            )

    # Swap references (O(1), no copying!)
    current, next_step = next_step, current

# current now points to the latest state
```

This swaps two pointers instead of copying millions of values - the canonical pattern in CFD, climate models, and any time-stepping simulation!
:::

:::{note} 🐛 Debug This!

A student's particle simulation is producing inconsistent results. Here's their code:

```python
def update_particles(particles, forces=[]):
    """Update particle positions based on forces."""
    for i, particle in enumerate(particles):
        if i >= len(forces):
            forces.append(calculate_force(particle))
        particle['velocity'] += forces[i] * dt
        particle['position'] += particle['velocity'] * dt
    return particles, forces

# Simulation loop
particles = [{'position': [0,0,0], 'velocity': [1,0,0]} for _ in range(10)]
for timestep in range(100):
    particles, forces = update_particles(particles)
```

Find and fix THREE bugs related to mutable defaults and aliasing:
1. The `forces=[]` default is created once and shared between calls
2. The function modifies the original `particles` list (no defensive copy)
3. The forces list grows unbounded, carrying over between timesteps

**Solution:**
```python
def update_particles(particles, forces=None):
    """Update particle positions based on forces."""
    if forces is None:
        forces = []
    particles = copy.deepcopy(particles)  # Defensive copy
    forces_new = []  # Fresh forces each time

    for particle in particles:
        force = calculate_force(particle)
        forces_new.append(force)
        particle['velocity'] += force * dt
        particle['position'] += particle['velocity'] * dt
    return particles, forces_new
```
:::

## 4.5 Dictionaries: Average-Case O(1) Lookup for Physics

Now we explore one of computer science's most elegant inventions - the **dictionary**! In computational physics, **dictionaries** are perfect for particle properties, lookup tables, and **caching** expensive calculations. You're about to understand exactly how they achieve near-instantaneous lookups regardless of size.

### Organizing Simulation Data with Dictionaries

Let's see how **dictionaries** transform particle management in an N-body simulation:

```{code-cell} python
# Stage 1: Basic dictionary structure (15 lines)
# N-body simulation: Managing particle properties efficiently
import json

# Individual particle data (could have thousands)
particles = {
    'particle_0001': {
        'mass': 1.989e30,  # grams (0.001 solar masses)
        'position': [1.5e13, 0.0, 0.0],  # cm
        'velocity': [0.0, 3.0e6, 0.0],   # cm/s
        'type': 'star'
    },
    'particle_0002': {
        'mass': 5.972e27,  # grams (Earth mass)
        'position': [2.5e13, 0.0, 0.0],
        'velocity': [0.0, 2.5e6, 0.0],
        'type': 'planet'
    }
}
```

```{code-cell} python
# Stage 2: O(1) lookup demonstration (15 lines)
# O(1) lookup by particle ID - instant access!
target = 'particle_0002'
print(f"Accessing {target}:")
print(f"  Mass: {particles[target]['mass']:.2e} g")
print(f"  Type: {particles[target]['type']}")

# Organize by type for efficient group operations
by_type = {}
for pid, data in particles.items():
    ptype = data['type']
    if ptype not in by_type:
        by_type[ptype] = []
    by_type[ptype].append(pid)

print(f"\nParticles by type: {by_type}")
print("In astronomy: Perfect for star/planet/dark matter separation")
```

### Understanding Hash Tables for Physics Applications

Let's demystify how **dictionaries** achieve **O(1)** lookup - critical for lookup tables in equation of state calculations:

:::{warning} ⚠️ Average-Case vs Worst-Case Complexity

Dictionary and set operations are **average-case O(1)**, not guaranteed O(1). In pathological cases with many hash collisions, lookups can degrade to **O(n)**. This happens when:

- Many keys hash to the same bucket (adversarial inputs)
- Poor hash function design
- Hash table needs resizing

For scientific computing, Python's built-in hash functions work well for typical data. The O(1) claim holds in practice for nearly all physics applications.
:::

```{code-cell} python
def demonstrate_hashing_for_physics():
    """Show how hash tables enable fast lookups in physics codes."""

    # Common lookup table keys in physics simulations
    physics_keys = [
        (1.0e6, 1.0e-3),   # (Temperature, Density) for EOS (equation of state)
        (2.0e6, 2.0e-3),
        (5.0e6, 1.0e-2),
        "H_ionization",     # Reaction rates
        "He_ionization",
        "opacity_table"     # Opacity types
    ]

    print("How hash tables accelerate physics lookups:")
    print("=" * 60)
    print("Key                  -> Hash        -> Bucket")
    print("-" * 60)

    for key in physics_keys:
        hash_value = hash(key)
        # Simplified bucket calculation
        bucket = abs(hash_value) % 100
        if isinstance(key, tuple):
            key_str = f"T={key[0]:.0e}, rho={key[1]:.0e}"
        else:
            key_str = str(key)
        print(f"{key_str:20s} -> {hash_value:11d} -> {bucket:3d}")

    print("\nThe O(1) lookup process:")
    print("1. Hash the key -> integer")
    print("2. Map to bucket index")
    print("3. Direct array access!")
    print("\nThis is why equation of state tables are fast!")

demonstrate_hashing_for_physics()
```

:::{note} Note: Hash Values Change Between Python Sessions

Python salts string hashes for security. Running this code multiple times will show different hash values and bucket assignments - that's expected! The key insight is that the **process** (hash $\to$ bucket $\to$ O(1) access) remains constant, even if specific values change.
:::

### Dictionary Performance for Particle Lookups

Time to see the dramatic performance difference for particle system queries:

```python

# Stage 1: Create test data (10 lines)
import time
import random

# Seed for reproducibility - critical for scientific computing!
rng = random.Random(42)

# Create a large particle system
n_particles = 100_000  # Reduced for reasonable runtime
print(f"Creating system with {n_particles:,} particles...")

# List approach (what beginners might try)
particle_list = [(f"particle_{i:07d}", rng.uniform(1e27, 1e30))
                 for i in range(n_particles)]
```

```python

# Stage 2: Create dictionary version (8 lines)
# Reset RNG for same masses
rng = random.Random(42)

# Dictionary approach (professional solution)
particle_dict = {f"particle_{i:07d}": rng.uniform(1e27, 1e30)
                 for i in range(n_particles)}

# Search for specific particle
target = "particle_0050000"

print(f"Finding {target} among {n_particles:,} particles...")
```

```python

# Stage 3: Time the lookups (15 lines)
# Time list search - O(n)
start = time.perf_counter()
for pid, mass in particle_list:
    if pid == target:
        mass_list = mass
        break
list_time = time.perf_counter() - start

# Time dict lookup - O(1)
start = time.perf_counter()
mass_dict = particle_dict[target]
dict_time = time.perf_counter() - start

print(f"\nList search: {list_time*1000:.3f} ms")
print(f"Dict lookup: {dict_time*1000:.6f} ms")
print(f"Dictionary is {list_time/dict_time:,.0f}x faster!")
print("\nFor astronomical catalogs with millions of objects:")
print("This difference determines feasibility!")
```

**Sample output (from 100,000 particles on typical hardware):**
```
Finding particle_0050000 among 100,000 particles...

List search: 2.847 ms
Dict lookup: 0.000312 ms
Dictionary is 9,125x faster!

For astronomical catalogs with millions of objects:
This difference determines feasibility!
```

:::{important} 💡 Computational Thinking: Memoization in Physics Calculations

This **caching** pattern dramatically speeds up physics codes:

```python
from functools import lru_cache

@lru_cache(maxsize=10000)
def equation_of_state(temperature, density):
    # Expensive calculation cached automatically
    return complex_eos_calculation(temperature, density)
```

**Real physics applications:**

- **Nuclear reaction rates**: Cache temperature-dependent rates
- **Opacity calculations**: Cache (T, $\rho$, composition) lookups
- **Molecular dynamics**: Cache pairwise interaction potentials
- **Climate models**: Cache radiative transfer calculations
:::

## 4.6 Sets: Mathematical Operations for Particle Systems

**Sets** are perfect for tracking unique particles, finding neighbors, and performing mathematical operations on particle groups. They provide **O(1)** membership testing plus elegant **set** operations - ideal for computational physics!

### Set Operations in Particle Dynamics

```{code-cell} python
# Particle tracking across domain boundaries
# (Common in parallel simulations with domain decomposition)

# Particles in different processor domains
domain_A = {'p001', 'p002', 'p003', 'p004', 'p005'}
domain_B = {'p004', 'p005', 'p006', 'p007'}
domain_C = {'p003', 'p007', 'p008', 'p009'}

# Particles that need communication (on boundaries)
boundary_particles = (domain_A & domain_B) | (domain_B & domain_C) | (domain_A & domain_C)
print(f"Boundary particles needing communication: {boundary_particles}")

# Particles unique to each domain (no communication needed)
interior_A = domain_A - domain_B - domain_C
interior_B = domain_B - domain_A - domain_C
interior_C = domain_C - domain_A - domain_B
print(f"Interior particles (A): {interior_A}")

# Check particle conservation
all_particles = domain_A | domain_B | domain_C
print(f"Total unique particles: {len(all_particles)}")

# Particles in multiple domains (need consistency check)
duplicated = set()
all_domains = [domain_A, domain_B, domain_C]
for i in range(len(all_domains)):
    for j in range(i+1, len(all_domains)):
        duplicated |= (all_domains[i] & all_domains[j])

print(f"Particles in multiple domains: {duplicated}")
print("\nSets make domain decomposition bookkeeping trivial!")
print("Used in: MPI parallel codes, astronomical survey overlaps")
```

:::{tip} Need a Set as a Dictionary Key?

Regular sets are mutable (unhashable), so they can't be dict keys. Use `frozenset` for an immutable, hashable set:

```python
# Track which particle combinations we've processed
processed = {}
pair = frozenset({'p001', 'p002'})  # Order doesn't matter!
processed[pair] = True

# These are the same pair:
frozenset({'p001', 'p002'}) == frozenset({'p002', 'p001'})  # True
```
:::

### Performance: Sets vs Lists for Neighbor Finding

```{code-cell} python
# Stage 1: Create test data (10 lines)
import time

# Simulate neighbor finding in particle simulation
n_particles = 100_000
n_neighbors = 100

print(f"Finding neighbors among {n_particles:,} particles...")

# Create particle IDs
all_particles = [f"p_{i:06d}" for i in range(n_particles)]
neighbors = [f"p_{i:06d}" for i in range(n_neighbors)]
```

```{code-cell} python
# Stage 2: Time the membership tests (15 lines)
# Convert to set for fast lookup
all_particles_set = set(all_particles)

# Test if neighbors exist - List approach
start = time.perf_counter()
for neighbor in neighbors:
    found = neighbor in all_particles  # O(n) each time!
list_time = time.perf_counter() - start

# Test if neighbors exist - Set approach
start = time.perf_counter()
for neighbor in neighbors:
    found = neighbor in all_particles_set  # O(1) each time!
set_time = time.perf_counter() - start

print(f"\nChecking {n_neighbors} potential neighbors:")
print(f"List approach: {list_time*1000:.2f} ms")
print(f"Set approach:  {set_time*1000:.5f} ms")
print(f"Set is {list_time/set_time:,.0f}x faster!")
```

:::{tip} ✅ Check Your Understanding

Why is checking particle membership **O(n)** with **lists** but **O(1)** with **sets**?

Think about the search process...

**Answer:** **Lists** must check each element sequentially until finding a match (or reaching the end) - this is **O(n)** linear time. **Sets** use **hash tables**: they compute a hash of the particle ID and jump directly to where it would be stored - this is **O(1)** constant time.

For a million-particle simulation, this is the difference between microseconds and seconds per lookup. When you're checking thousands of particle interactions per timestep, this performance difference determines whether your simulation finishes in hours or weeks!
:::

## 4.7 Memory and Performance for Scientific Computing

Now that we understand how different data structures behave algorithmically with sets, dictionaries, and lists, let's examine their actual memory footprint and cache performance implications. Understanding memory layout is crucial for scientific computing because it explains why specialized numerical libraries are so much faster than pure Python and will help you write **cache**-efficient simulation codes.

### Memory Usage in Particle Systems

Let's examine memory costs for different **data structures** in a particle simulation context:

```{code-cell} python
# Stage 1: Basic Memory Measurement (8 lines)
import sys

def measure_particle_memory(n=10000):
    """Compare memory for particle ID storage."""
    ids_list = [f"p_{i:06d}" for i in range(n)]
    ids_set = set(ids_list)

    print(f"Storing {n:,} particle IDs:")
    print(f"  List: {sys.getsizeof(ids_list):,} bytes")
    print(f"  Set:  {sys.getsizeof(ids_set):,} bytes")

measure_particle_memory()
```

```{code-cell} python
# Stage 2: Understanding the Tradeoff (10 lines)
def understand_physics_tradeoffs():
    """Memory vs speed tradeoffs in physics codes."""
    # Small particle system
    n = 100
    positions = [[i*1.0, 0.0, 0.0] for i in range(n)]

    list_bytes = sys.getsizeof(positions)
    # If we used spatial hashing (dict of cells)
    dict_bytes = sys.getsizeof({i: pos for i, pos in enumerate(positions)})

    print(f"100 particles as list: {list_bytes:,} bytes")
    print(f"With spatial hash: ~{dict_bytes:,} bytes")
    print(f"Extra {dict_bytes - list_bytes:,} bytes enables O(1) neighbor finding!")

understand_physics_tradeoffs()
```

```{code-cell} python
# Stage 3: Complete Memory Profile (15 lines)
def profile_simulation_structures(n_particles=1000):
    """Memory comparison for complete particle system."""
    import numpy as np  # Preview of Chapter 7

    # Create structures
    list_of_lists = [[i, i*1.0, 0.0, 0.0] for i in range(n_particles)]
    list_of_tuples = [(i, i*1.0, 0.0, 0.0) for i in range(n_particles)]
    dict_struct = {i: [i*1.0, 0.0, 0.0] for i in range(n_particles)}
    numpy_arr = np.zeros((n_particles, 4))

    print(f"Memory for {n_particles:,} particles (ID, x, y, z):")
    print("-" * 55)

    # Python structures: getsizeof is shallow!
    print(f"{'List of lists':18s}: {sys.getsizeof(list_of_lists):>8,} bytes (container only!)")
    print(f"{'List of tuples':18s}: {sys.getsizeof(list_of_tuples):>8,} bytes (container only!)")
    print(f"{'Dictionary':18s}: {sys.getsizeof(dict_struct):>8,} bytes (container only!)")

    # NumPy: use .nbytes for actual data buffer size
    print(f"{'NumPy .nbytes':18s}: {numpy_arr.nbytes:>8,} bytes (actual data!)")
    print(f"{'NumPy getsizeof':18s}: {sys.getsizeof(numpy_arr):>8,} bytes (header only!)")

    print("\n⚠️  getsizeof() is SHALLOW - it misses contained objects!")
    print("   NumPy's .nbytes gives the actual data buffer size.")

profile_simulation_structures()
```

### Cache Efficiency in Grid Computations

Modern CPUs are fast, but memory access is slow. Understanding cache efficiency is critical for grid-based simulations:

```{code-cell} python
# Stage 1: Setup (8 lines)
import time

# Demonstrate cache effects in finite difference calculations
size = 500  # Grid size for heat equation
grid = [[20.0 + 0.1*i*j for j in range(size)]
        for i in range(size)]

print("Simulating heat diffusion finite differences:")
print("(Common in CFD and atmospheric modeling)")
```

```{code-cell} python
# Stage 2: Row-major access (10 lines)
# Row-major access (cache-friendly in Python)
start = time.perf_counter()
total = 0.0
for i in range(size):
    for j in range(size):
        total += grid[i][j]
row_time = time.perf_counter() - start

print(f"Processing {size}x{size} grid:")
print(f"Row-major (cache-friendly):   {row_time*1000:.1f} ms")
```

```{code-cell} python
# Stage 3: Column-major comparison (12 lines)
# Column-major access (cache-hostile in Python)
start = time.perf_counter()
total = 0.0
for j in range(size):
    for i in range(size):
        total += grid[i][j]
col_time = time.perf_counter() - start

print(f"Column-major (cache-hostile): {col_time*1000:.1f} ms")
if row_time > 0:
    print(f"Ratio: {col_time/row_time:.1f}x")

print("\n⚠️  Important caveat about Python nested lists:")
print("Each row is a SEPARATE list object in memory.")
print("Only the row's pointers are contiguous, not the data.")
print("")
print("In NumPy with contiguous arrays, this effect is 10-100x!")
print("That's why memory layout matters so much in CFD/climate codes.")
```

:::{warning} ⚠️ Common Bug Alert: The Iteration Modification Trap

Never modify a collection while iterating - a common bug in particle removal:

```python
# THE BUG - Skips particles!
particles = [p1, p2, p3, p4, p5]
for p in particles:
    if p.escaped_boundary():
        particles.remove(p)  # WRONG! Skips next particle

# THE FIX 1: Iterate over copy
for p in particles.copy():
    if p.escaped_boundary():
        particles.remove(p)

# THE FIX 2: List comprehension (best for physics)
particles = [p for p in particles if not p.escaped_boundary()]

# THE FIX 3: Build removal list
to_remove = []
for p in particles:
    if p.escaped_boundary():
        to_remove.append(p)
for p in to_remove:
    particles.remove(p)
```

This bug has corrupted many molecular dynamics simulations!
:::

## 4.8 Choosing the Right Structure for Physics

After exploring all options, how do you choose? Here's your decision framework for computational physics:

:::{tip} ✅ Check Your Understanding

For each physics scenario, what **data structure** would you choose?

1. **Tracking unique particle IDs in collision detection** $\to$ ?
2. **Time series of energy measurements** $\to$ ?
3. **Caching expensive equation of state calculations** $\to$ ?
4. **Physical constants that must not change** $\to$ ?

Think before reading...

**Answers:**
1. **Set** (unique particles, **O(1)** collision checks)
2. **List** (ordered by time, allows duplicates)
3. **Dictionary** (**cache** (T,$\rho$) $\to$ pressure with **O(1)** lookup)
4. **Tuple** or namedtuple (**immutable** constants, prevents accidents)
:::

### Performance Quick Reference for Physics

| Operation | List | Tuple | Dict | Set |
|-----------|------|-------|------|-----|
| Access by index | **O(1)** | **O(1)** | N/A | N/A |
| Search for particle | **O(n)** | **O(n)** | **O(1)**†‡ | **O(1)**† |
| Add particle | **O(1)**‡ | N/A | **O(1)**‡ | **O(1)**‡ |
| Remove particle | **O(n)** | N/A | **O(1)**† | **O(1)**† |
| Memory (relative) | 1$\times$ | 0.9$\times$ | 3$\times$ | 3$\times$ |
| Spatial ordering | Yes | Yes | Yes* | No |

\* Dicts maintain insertion order (Python 3.7+)
† **Average-case**; worst-case O(n) with hash collisions
‡ **Amortized** - occasionally O(n) during resize

### Real Example: Combining Data Structures

Let's see how different data structures work together in a simple particle tracking system:

```{code-cell} python
# Simple example: Tracking particles with multiple data structures

# Constants (tuple - can't be changed accidentally!)
CONSTANTS = (6.674e-8, 2.998e10, 1.381e-16)  # G, c, k_B

# Particle data (dictionary for O(1) lookup by ID)
particles = {
    'p001': {'mass': 1e30, 'x': 0.0, 'y': 0.0},
    'p002': {'mass': 2e30, 'x': 10.0, 'y': 0.0},
    'p003': {'mass': 1.5e30, 'x': 5.0, 'y': 5.0},
}

# Active particles (set for fast membership testing)
active = {'p001', 'p002'}  # p003 is inactive

# Time series measurements (list - ordered by time)
measurements = [
    (0.0, 100.5),  # (time, energy)
    (1.0, 99.8),
    (2.0, 99.1),
]

# Example: Find total mass of active particles
total_mass = 0
for pid in active:  # O(1) membership test for each
    if pid in particles:  # O(1) lookup
        total_mass += particles[pid]['mass']

print(f"Total active mass: {total_mass:.1e} g")
print(f"Number of measurements: {len(measurements)}")
print(f"Constants are protected: type(CONSTANTS) = {type(CONSTANTS).__name__}")

# This simple combination shows:
# - Tuple for constants (immutable)
# - Dictionary for particle data (O(1) lookup)
# - Set for active particles (O(1) membership)
# - List for time series (ordered)
```

## Main Takeaways

You've just mastered concepts that will transform your computational physics from toy problems to research-grade simulations! The journey from understanding simple lists to architecting with dictionaries and sets represents a fundamental shift in how you approach scientific computing. You now see data structures not just as containers, but as carefully chosen tools where the right choice can mean the difference between simulations that finish in hours versus weeks.

The most profound insight from this chapter is that data structure choice often matters more than algorithm optimization. We saw how switching from a list to a set for particle lookups gave us a 100,000$\times$ speedup - no amount of code optimization could achieve that! This is the secret that separates research codes from student projects: professionals spend more time architecting their data organization than writing physics equations. The best physics insight in the world is useless if your code can't handle realistic problem sizes.

The mutable versus immutable distinction that seemed abstract at first is actually critical for scientific computing. Every time you use a tuple for physical constants or configuration parameters, you're preventing bugs that have literally crashed spacecraft and corrupted published results. When you properly use defensive copying for your simulation state, you're protecting yourself from the aliasing bugs that have plagued computational physics for decades. Remember: in the Cassini example, a simple data structure choice nearly lost a billion-dollar mission.

The performance principles you've learned extend far beyond Python. The cache efficiency concepts explain why codes like LAMMPS and GADGET obsess over memory layout - it's not premature optimization, it's the difference between simulating thousands versus millions of atoms. The Big-O notation you've mastered is the universal language for discussing whether an algorithm scales to galaxy-sized problems. The hash table concept underlying dictionaries appears in every parallel communication library, every adaptive mesh refinement code, and every spatial indexing scheme you'll encounter.

Most importantly, you now understand the connection between data structures and numerical methods. That O($\mathrm{n}^{2}$) all-pairs particle interaction that's impossible for large systems? It becomes O(n log n) with tree-based structures. The O(n) searching that makes timesteps crawl? It becomes O(1) with spatial hashing. These aren't just computer science concepts - they're the difference between simulating a few hundred particles and modeling entire galaxies with billions of stars.

Remember: every data structure makes trade-offs. Lists give you ordering but slow searches. Dictionaries trade memory for lightning-fast lookups. Sets provide uniqueness and mathematical operations but lose ordering. There's no universally "best" structure - only the best structure for your specific physics problem. As you tackle research simulations, you'll combine multiple structures: NumPy arrays for number crunching, dictionaries for particle properties, sets for collision detection, and spatial data structures for neighbor finding.

With this foundation, you're ready to architect simulations that scale to astronomical proportions. The next chapter on functions and modules will show you how to organize this knowledge into reusable, testable components. After that, NumPy will supercharge your numerical operations using the memory layout principles you now understand. You're no longer just writing code - you're engineering solutions to the computational challenges of modern physics!

Once you can reason about control flow (Chapter 3) and data layout (this chapter), you're ready to start **abstracting** your work: writing functions and modules that hide complexity while preserving correctness and performance. That's the goal of Chapter 5.

## Definitions

**Aliasing**: When two or more variables refer to the same object in memory, causing modifications through one to affect the others.

**Amortized O(1)**: An operation that is usually **O(1)** but occasionally **O(n)**, where the average over many operations remains **O(1)**.

**Big-O Notation**: Mathematical notation describing how an algorithm's runtime scales with input size, focusing on the dominant term.

**Cache**: Small, fast memory close to the CPU that stores recently accessed data for quick retrieval.

**Data Structure**: A way of organizing data in computer memory to enable efficient access and modification.

**Deep Copy**: Creating a completely independent copy of an object and all objects it contains, recursively.

**Dictionary**: A **mutable** mapping type storing key-value pairs with **average-case O(1)** lookup time using **hash tables**. Worst-case O(n) with hash collisions.

**Hash Function**: A function mapping data of arbitrary size to fixed-size values, enabling fast lookups.

**Hash Table**: The underlying implementation for **dictionaries** and **sets**, enabling **average-case O(1)** lookups. Worst-case O(n) when many keys collide.

**Immutable**: Objects whose state cannot be modified after creation (**tuples**, strings, numbers).

**List**: Python's built-in **mutable** sequence type that stores **references** to objects in order.

**Memoization**: **Caching** technique storing function results to avoid recalculating for the same inputs.

**Mutable**: Objects whose state can be modified after creation (**lists**, **dictionaries**, **sets**).

**Named Tuple**: A **tuple** subclass allowing element access by name as well as index.

**O(1) - Constant Time**: An operation whose runtime doesn't depend on input size.

**O(n) - Linear Time**: An operation whose runtime grows proportionally with input size.

**O($\mathrm{n}^{2}$) - Quadratic Time**: An operation whose runtime grows with the square of input size.

**O(log n) - Logarithmic Time**: An operation whose runtime grows logarithmically with input size.

**O(n log n)**: Common complexity for efficient sorting algorithms and tree-based operations.

**Reference**: A variable that points to an object in memory rather than containing the value directly.

**Set**: A **mutable** collection of unique, unordered elements with **O(1)** membership testing.

**Shallow Copy**: Creating a new container with **references** to the same contained objects.

**Spatial Hashing**: Organizing particles by spatial region for **O(1)** neighbor finding.

**Tuple**: An **immutable** sequence type that cannot be changed after creation.

## Key Takeaways

✓ **Data structure** choice can change performance by factors of 1,000,000$\times$ or more for large-scale simulations

✓ **Lists** are versatile but have **O(n)** search - use for ordered particle arrays that you'll vectorize with NumPy

✓ **Dictionaries** and **sets** provide **O(1)** lookup through **hash tables** - essential for particle lookups and caching

✓ **Tuples** prevent modification bugs - use for physical constants and configuration parameters

✓ The **shallow** vs **deep copy** distinction is critical for grid-based simulations

✓ Python stores **references** to objects, explaining why NumPy's contiguous arrays are faster

✓ Memory layout affects **cache** performance by 2-10$\times$ even in Python

✓ Every data structure trades something (memory, speed, flexibility) for something else

✓ **Mutable** default arguments are dangerous - always use the None sentinel pattern (Chapter 1 callback)

✓ Spatial data structures transform **O($\mathrm{n}^{2}$)** physics problems into **O(n)** or **O(n log n)**

✓ **Sets** provide elegant mathematical operations for domain decomposition and particle tracking

✓ **Dictionaries** enable **memoization** that can speed up equation of state calculations 100$\times$

## Python Module & Method Reference

This reference section catalogs all Python modules, functions, and methods introduced in this chapter. Keep this as a quick lookup guide for your physics simulations.

### Standard Library Modules

**`time` module** - High-resolution timing for performance measurement
```python
import time
```
- `time.perf_counter()` - Returns float seconds with highest available resolution
  - Use for timing code segments: `start = time.perf_counter()`
  - Always use for benchmarking (not `time.time()` which can go backwards!)

**`sys` module** - System-specific parameters (expanded from Chapter 1)
```python
import sys
```
- `sys.getsizeof(object)` - Returns **shallow** memory size of object in bytes
  - Measures container overhead only, **not** contained objects
  - For deep size: sum recursively or use `pympler.asizeof()`
  - Use for comparing container overhead, not total memory

**`copy` module** - Create object copies with control over depth
```python
import copy
```
- `copy.copy(x)` - Creates shallow copy (new container, same contents)
- `copy.deepcopy(x)` - Creates deep copy (recursively copies all contents)
  - Critical for grid simulations to avoid aliasing bugs
  - Use for simulation state backups

**`random` module** - Generate random numbers for Monte Carlo
```python
import random
```
- `random.random()` - Random float in [0.0, 1.0)
- `random.uniform(a, b)` - Random float in [a, b]
- `random.choice(seq)` - Random element from sequence
- `random.sample(population, k)` - k unique random elements

**`json` module** - Save/load structured data
```python
import json
```
- `json.dump(obj, file, indent=2)` - Write object to file with formatting
- `json.load(file)` - Read object from file
- `json.dumps(obj)` - Convert object to JSON string
- `json.loads(string)` - Parse JSON string to object

**`math` module** - Mathematical functions (review from Chapter 2)
```python
import math
```
- `math.sqrt(x)` - Square root (use for distances)
- `math.log(x)` - Natural logarithm
- `math.log2(x)` - Base-2 logarithm (for Big-O analysis)

### Collections Module

**`collections` module** - Specialized container datatypes
```python
from collections import OrderedDict, Counter, defaultdict, deque, namedtuple
```

**`OrderedDict`** - Dictionary that remembers insertion order
- `.move_to_end(key, last=True)` - Move key to end (or beginning if last=False)
- `.popitem(last=True)` - Remove and return (key, value) pair from end/beginning
- Use for LRU caches in physics calculations

**`Counter`** - Dictionary subclass for counting hashable objects
- `Counter(iterable)` - Create from iterable
- `.most_common(n)` - Returns n most common (element, count) pairs
- `.update(iterable)` - Add counts from iterable
- Perfect for histogram analysis of particle properties

**`defaultdict`** - Dictionary with default value factory
- `defaultdict(list)` - Missing keys default to empty list
- `defaultdict(int)` - Missing keys default to 0
- Eliminates KeyError in particle grouping

**`deque`** - Double-ended queue with O(1) operations at both ends
- `deque(maxlen=n)` - Fixed-size queue (old elements dropped)
- `.append(x)` / `.appendleft(x)` - Add to right/left end
- `.pop()` / `.popleft()` - Remove from right/left end
- Essential for boundary conditions in simulations

**`namedtuple`** - Tuple subclass with named fields
```python
Particle = namedtuple('Particle', ['id', 'mass', 'x', 'y', 'z'])
p = Particle(1, 1.0e30, 0, 0, 0)
print(p.mass)  # Access by name
```

### Functools Module

**`functools` module** - Higher-order functions and operations
```python
from functools import lru_cache
```

**`@lru_cache(maxsize=128)`** - Decorator for automatic memoization
```python
@lru_cache(maxsize=1000)
def expensive_calculation(T, rho):
    return complex_physics_calculation(T, rho)
```
- Caches function results automatically
- `maxsize=None` for unlimited cache
- `.cache_info()` - Returns cache statistics
- `.cache_clear()` - Clear the cache

### Built-in Functions for Data Structures

**Type Checking**
- `type(obj)` - Returns object's type
- `isinstance(obj, type)` - Check if obj is instance of type
- `id(obj)` - Returns unique identifier (memory address)
- `obj1 is obj2` - Check if same object (identity)

**Container Operations**
- `len(container)` - Number of elements
- `x in container` - Membership test (O(1) for sets/dicts, O(n) for lists)
- `sorted(iterable)` - Returns new sorted list
- `reversed(sequence)` - Returns reverse iterator
- `enumerate(iterable, start=0)` - Returns (index, value) pairs
- `zip(iter1, iter2, ...)` - Parallel iteration

**Copying**
- `list(iterable)` - Create new list from iterable
- `tuple(iterable)` - Create new tuple from iterable
- `set(iterable)` - Create new set from iterable
- `dict(pairs)` - Create dictionary from (key, value) pairs

### Data Structure Methods Summary

**List Methods** (Expanded)
- `.append(x)` - Add to end (amortized O(1))
- `.extend(iterable)` - Add all elements from iterable
- `.insert(i, x)` - Insert at position i (O(n))
- `.remove(x)` - Remove first x (O(n))
- `.pop(i=-1)` - Remove and return element at i
- `.clear()` - Remove all elements
- `.index(x)` - Find position of x (O(n))
- `.count(x)` - Count occurrences of x
- `.sort()` - Sort in-place
- `.reverse()` - Reverse in-place
- `.copy()` - Create shallow copy

**Dictionary Methods** (Expanded)
- `.get(key, default=None)` - Safe access with default
- `.setdefault(key, default)` - Get or set with default
- `.pop(key, default)` - Remove and return value
- `.popitem()` - Remove and return arbitrary (key, value)
- `.update(other)` - Update with other dict/pairs
- `.keys()` - View of keys
- `.values()` - View of values
- `.items()` - View of (key, value) pairs
- `.clear()` - Remove all items
- `.copy()` - Shallow copy

**Set Methods** (Expanded)
- `.add(x)` - Add element
- `.remove(x)` - Remove element (raises KeyError if missing)
- `.discard(x)` - Remove element (no error if missing)
- `.pop()` - Remove and return arbitrary element
- `.clear()` - Remove all elements
- `.union(other)` or `|` - Elements in either set
- `.intersection(other)` or `&` - Elements in both sets
- `.difference(other)` or `-` - Elements in first but not second
- `.symmetric_difference(other)` or `^` - Elements in either but not both
- `.update(other)` or `|=` - Add elements from other
- `.intersection_update(other)` or `&=` - Keep only elements in both
- `.difference_update(other)` or `-=` - Remove elements in other
- `.symmetric_difference_update(other)` or `^=` - Keep elements in either but not both
- `.issubset(other)` - Check if all elements in other
- `.issuperset(other)` - Check if contains all elements of other
- `.isdisjoint(other)` - Check if no elements in common
- `.copy()` - Create shallow copy

## Quick Reference Tables

### Data Structure Operations

| Operation | List | Tuple | Dict | Set |
|-----------|------|-------|------|-----|
| Create empty | `[]` | `()` | `{}` | `set()` |
| Create with items | `[1,2,3]` | `(1,2,3)` | `{'a':1}` | `{1,2,3}` |
| Add item | `.append(x)` | N/A | `d[k]=v` | `.add(x)` |
| Remove item | `.remove(x)` | N/A | `del d[k]` | `.remove(x)` |
| Check membership | `x in list` | `x in tuple` | `k in dict` | `x in set` |
| Get by index | `list[i]` | `tuple[i]` | N/A | N/A |

### Performance Quick Reference

| Operation | List | Tuple | Dict | Set | Deque |
|-----------|------|-------|------|-----|-------|
| Access by index | O(1) | O(1) | N/A | N/A | O(n) |
| Search for value | O(n) | O(n) | O(1)* | O(1) | O(n) |
| Add to end | O(1)† | N/A | O(1)† | O(1)† | O(1) |
| Add to beginning | O(n) | N/A | O(1)† | O(1)† | O(1) |
| Remove from end | O(1) | N/A | N/A | N/A | O(1) |
| Remove from beginning | O(n) | N/A | N/A | N/A | O(1) |
| Remove specific | O(n) | N/A | O(1) | O(1) | O(n) |

\* Dict searches by key, not value
† Amortized - occasionally O(n) during resize

### Common Methods for Physics

| Structure | Method | Physics Use Case |
|-----------|--------|------------------|
| list | `.append(x)` | Add new particle |
| list | `.extend(iter)` | Merge particle lists |
| dict | `.get(k, default)` | Safe parameter lookup |
| dict | `@lru_cache` | Automatic memoization |
| set | `.union(other)` | Combine particle domains |
| set | `.intersection(other)` | Find boundary particles |
| deque | `.appendleft()` | Boundary conditions |
| OrderedDict | `.move_to_end()` | LRU cache management |

### When to Use Each Structure

| Physics Task | Best Choice | Why |
|--------------|------------|-----|
| Particle positions | List $\to$ NumPy array | Vectorizable operations |
| Particle lookup by ID | Dictionary | O(1) access |
| Active particles | Set | Fast membership, uniqueness |
| Physical constants | Tuple/NamedTuple | Immutable, safe |
| EOS cache | Dictionary/LRU cache | Fast lookup by (T,$\rho$) |
| Collision candidates | Set | No duplicates, set operations |
| Time series | List | Ordered, allows duplicates |
| Spatial grid | Dict of sets | O(1) cell access |
| Boundary particles | Deque | Fast operations at both ends |
| Particle counts | Counter | Automatic histogram creation |

## Next Chapter Preview

With data structures mastered, Chapter 5 will explore functions and modules - how to organize code for reusability, testing, and collaboration. You'll learn how Python's function model, with first-class functions and closure support, enables powerful patterns like decorators and functional programming techniques. These concepts prepare you for building modular physics engines, creating reusable analysis pipelines, and understanding the functional programming paradigm used in modern frameworks like JAX where functions transform into automatically differentiable computational graphs. Get ready to transform your scripts into professional-quality scientific libraries!
