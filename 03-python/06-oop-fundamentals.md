---
title: "Chapter 6: OOP Fundamentals - Organizing Scientific Code"
subtitle: "Foundations for Scientific Programming"
author: "Anna Rosen"
kernelspec:
  name: python3
  display_name: Python 3
---

## Learning objectives

By the end of this chapter, you will be able to:

- [ ] **(1) Transform functions and data** into cohesive classes that model scientific concepts
- [ ] **(2) Distinguish between** instance and class attributes and choose appropriately for scientific data
- [ ] **(3) Create methods that operate** on object state while understanding the role of `self`
- [ ] **(4) Implement properties** to compute derived values and validate scientific constraints
- [ ] **(5) Write special methods** (`__init__`, `__str__`, `__repr__`) to make objects Pythonic
- [ ] **(6) Debug** common OOP errors using introspection tools and error messages
- [ ] **(7) Recognize when OOP improves** code organization versus when functions suffice
- [ ] **(8) Connect the transition** from procedural to object-oriented thinking in scientific computing

## Prerequisites

Before starting this chapter, verify you can:

- [ ] Define and call functions with various parameter types (Chapter 5)
- [ ] Understand scope and namespaces (Chapter 5)
- [ ] Work with dictionaries and their methods (Chapter 4)
- [ ] Create and import modules (Chapter 5)
- [ ] Handle mutable vs immutable objects (Chapter 4)

**Quick diagnostic:**

```{code-cell} python
# Can you predict what this prints?
def modify(data):
    data['value'] = data['value'] * 2
    return data

measurement = {'value': 100, 'unit': 'K'}
result = modify(measurement)
print(f"Original: {measurement['value']}")  # What value?
print(f"Result: {result['value']}")         # What value?
```

If you said both print "200", you're ready! Python uses **call-by-sharing**:
the function receives a reference to the same object, so mutating a mutable
object is visible to the caller; rebinding the local parameter is not.

## Why this chapter matters

You've mastered functions to organize behavior and modules to organize related functions. But what happens when data and the functions that operate on it are inseparable? When tracking particles in a simulation, each particle has position, velocity, and mass, along with methods to update position, calculate kinetic energy, and check collisions. Passing all this data between separate functions becomes error-prone and verbose. This is where Object-Oriented Programming transforms your code from a collection of functions to a model of your problem domain.

**Object-Oriented Programming** (OOP) isn't just another way to organize code - it's a fundamental shift in how we think about programs. Instead of viewing code as a sequence of operations on data, we model it as interactions between objects that combine data and behavior. A thermometer knows its temperature and how to convert units. A dataset knows its values and how to calculate statistics. A simulation particle knows its state and how to evolve. This paradigm mirrors how we naturally think about scientific systems, making complex programs more intuitive and maintainable.

This chapter introduces OOP's essential concepts through practical scientific examples. You'll learn to create classes (blueprints for objects), instantiate objects (specific instances), and define methods (functions attached to objects). We'll explore how properties provide computed attributes and validation, making declared local scientific constraints visible and enforceable along the paths a class controls. Most importantly, you'll develop judgment about when OOP clarifies code (managing stateful systems, modeling entities) versus when it adds unnecessary complexity (simple calculations, stateless transformations). By the end, you'll understand why NumPy arrays are objects with methods, setting the foundation for leveraging Python's scientific ecosystem.

```{figure} ../assets/textbook-figures/ch06-object-state.svg
:name: ch06-object-state
:alt: A Particle class blueprint specifies state, an invariant, and methods; an instance holds one particle's mass, position, and velocity and can update its own state.
:width: 100%

A class can keep related state, behavior, and local invariants together when that makes the model easier to inspect.
```

What to notice: an invariant enforced by a class is a software promise about the
paths the class controls. It cannot, by itself, establish that the chosen model
or measurements are physically adequate.

:::{tip} TL;DR — Why This Chapter Matters

OOP isn't about syntax — it can help manage systems where data and behavior must
stay synchronized. Well-designed properties and validation can enforce declared
invariants, but they do not do so automatically: the class must define the
invariant, validate every relevant path, and be tested.

**The real lesson:** classes can make selected invalid states harder to create;
they are one design tool among several, not a guarantee of correctness.
:::

:::{note} 📖 How to Use This Chapter

**Read actively, not passively.** When you see a class definition:

1. **Trace the state** — What attributes does `__init__` create? How do methods change them?
2. **Identify the invariants** — What must always be true about this object? (e.g., radius > 0, energy $\geq$ 0)
3. **Find the contracts** — Which methods *mutate* state vs *compute* values?
4. **Question the design** — Could this be a simple function instead? What would break?

Run a few representative blocks, especially the early state and validation
examples. Treat longer historical and extension examples as reference; modify
values and observe the resulting behavior rather than trying to execute the
whole chapter linearly.
:::

For a first reading, follow the transformation from a particle dictionary to a
small object, then focus on `self`, method contracts, and properties. Return
later to the protocol and design-choice Deep Dives when a class needs to work
with Python syntax or you are deciding whether a class is warranted.

## Try this chapter

- [**Browser Python lab · Temperature invariant**](jupyterlite/ch06-temperature-invariant.html): predict whether construction accepts a temperature below absolute zero, run the local check, then explain both the boundary the class enforces and one measurement question it cannot answer. The activity is optional; the static example below remains complete without browser Python.

---

(from-functions-to-objects)=
## 6.1 From Functions to Objects: The Conceptual Leap

:::{margin}
**Object-Oriented Programming**
A programming paradigm that organizes code around objects (data) and methods (behavior) rather than functions and logic.
:::

Let's start with a problem you've already solved with functions, then transform it into objects to see the difference. In Python, everything is actually an object - even functions and modules! But some objects are more complex than others, and creating your own classes lets you model your specific problem domain.

```{code-cell} python
# Approach 1: Functions with dictionaries (what you know)
def create_particle(mass, x, y, vx, vy):
    """Create a particle dictionary."""
    return {
        'mass': mass,  # grams
        'x': x, 'y': y,  # cm
        'vx': vx, 'vy': vy  # cm/s
    }

def kinetic_energy(particle):
    """Calculate kinetic energy in ergs."""
    v_squared = particle['vx']**2 + particle['vy']**2
    return 0.5 * particle['mass'] * v_squared

def update_position(particle, dt):
    """Update position based on velocity."""
    particle['x'] += particle['vx'] * dt
    particle['y'] += particle['vy'] * dt
    return particle

# Using functions
p1 = create_particle(1.0, 0, 0, 10, 5)
energy = kinetic_energy(p1)
p1 = update_position(p1, 0.1)
print(f"Energy: {energy:.1f} ergs")
```

Now let's see the same problem with OOP:

```{code-cell} python
# Approach 2: Object-Oriented (what you're learning)
class Particle:
    """A particle with position and velocity."""

    def __init__(self, mass, x, y, vx, vy):
        """Initialize particle state."""
        self.mass = mass  # grams
        self.x = x        # cm
        self.y = y        # cm
        self.vx = vx      # cm/s
        self.vy = vy      # cm/s

    def kinetic_energy(self):
        """Calculate kinetic energy in ergs."""
        v_squared = self.vx**2 + self.vy**2
        return 0.5 * self.mass * v_squared

    def update_position(self, dt):
        """Update position using constant-velocity kinematics.

        Contract: MUTATES self.x and self.y in place; returns None.

        This is not a force-integrating simulation. With fixed vx and vy,
        kinetic energy remains constant by construction. For long simulations
        with forces, choose an integrator appropriate to the model.
        """
        self.x += self.vx * dt
        self.y += self.vy * dt

# Using objects
p2 = Particle(1.0, 0, 0, 10, 5)
energy = p2.kinetic_energy()
p2.update_position(0.1)
print(f"Energy: {energy:.1f} ergs")
```

Both approaches solve the problem, but notice the differences:

- **Organization**: Data and methods stay together in the class
- **Syntax**: Methods are called on objects (`p2.kinetic_energy()`)
- **State**: The object maintains its own state between method calls
- **Clarity**: The object-oriented version reads more naturally

:::{important} Design decision: give a class a job

The `Particle` class earns its existence only when position, velocity, mass,
and the operations that maintain them must travel together. For one
stateless calculation, the dictionary-and-function form is often clearer.
The class is a design boundary, not an automatic improvement or a replacement
for testing the physical model.
:::

:::{note} 🌟 The More You Know: Spirit's Flash-Memory Recovery and State Management
:class: dropdown

In January 2004, shortly after Spirit began science operations on Mars, the
rover entered a repetitive reset and re-initialization loop. NASA's anomaly
account traces the incident to incorrect configuration parameters in operating
system modules responsible for system and flash-memory files; the overloaded
file systems had not been recognized or tested in the relevant ground testing.

Mission operations first worked around flash-memory use, then deleted files,
reallocated memory, and rebuilt the file system. This was a recovery and
operations problem, not evidence that object-oriented programming would by
itself have prevented the failure. It does, however, motivate a narrower
design question: can a software component make its lifecycle state explicit
enough that invalid transitions are easier to inspect and test?

```python
# FICTIONAL classroom pattern, not Spirit flight software.
class RoverComponent:
    def __init__(self, name):
        self.name = name
        self.initialized = False
        self.error_count = 0

    def initialize(self):
        if not self.initialized:
            # Safe initialization
            self.initialized = True
```

The pattern makes one local state contract visible; it does not substitute for
requirements, file-system limits, integration testing, or operations
procedures. Spirit nevertheless returned to normal operations and ultimately
worked for more than six years, far beyond its planned 90-Martian-day mission.

That distinction is the useful lesson for scientific code: a class can help
name and protect a local state boundary, while real reliability depends on the
larger system around it.

**Sources:** NASA's [Spirit mission account](https://science.nasa.gov/mission/mer-spirit/),
NASA's [lessons-learned summary](https://llis.nasa.gov/lesson/1483), and Reeves,
Neilson, and Litwin (2005), *The Mars Rover Spirit FLASH Anomaly*.
:::

---

## 6.2 Classes and Objects: Building Blocks

:::{margin}
**Class**
A blueprint or template for creating objects that defines attributes and methods.
:::

Before we dive into creating classes, let's understand why we need them beyond the simple example we just saw. As your programs grow, you face several challenges that classes elegantly solve:

**Namespace pollution**: Without classes, you might have functions like `calculate_star_luminosity()`, `calculate_planet_mass()`, `calculate_galaxy_distance()` - your namespace becomes cluttered with hundreds of related functions.

:::{margin}
**Object**
A specific instance of a class containing data (attributes) and behavior (methods).
:::

**Data consistency**: When data and functions are separate, nothing prevents you from passing a galaxy's data to a star's calculation function, potentially causing silent errors or crashes.

:::{margin}
**Constructor**
The `__init__` method that initializes new objects when they're created.
:::

**Code reusability**: With functions alone, similar behaviors must be duplicated. Every object type needs its own set of functions even when the logic is similar.

**Conceptual clarity**: We naturally think of stars, planets, and galaxies as entities with properties and behaviors. Classes let us model this intuition directly in code.

A **class** is a blueprint for creating objects. An **object** (or _instance_) is a specific realization of that blueprint. Think of a class as the concept "thermometer" and objects as specific thermometers in your lab.

```{code-cell} python
import math

# Define a class (blueprint)
class Measurement:
    """A scientific measurement with uncertainty."""

    def __init__(self, value, error):
        """Initialize a finite numeric value with a non-negative uncertainty."""
        if (
            isinstance(value, bool)
            or isinstance(error, bool)
            or not isinstance(value, (int, float))
            or not isinstance(error, (int, float))
            or not math.isfinite(value)
            or not math.isfinite(error)
        ):
            raise ValueError("value and error must be finite numbers")
        if error < 0:
            raise ValueError(f"Error must be non-negative, got {error}")
        self.value = value
        self.error = error

    def relative_error(self):
        """Calculate relative error as percentage.

        Note: Returns infinity if value is exactly zero. For values
        very close to zero, the relative error may be misleadingly large.
        """
        if self.value == 0:
            return float('inf')
        return abs(self.error / self.value) * 100

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"Measurement({self.value}, {self.error})"

# Create objects (instances)
temp = Measurement(293.15, 0.1)  # Temperature in Kelvin
# Pressure in dyne/cm^2 (CGS unit for pressure)
# Note: CGS (centimeter-gram-second) is traditional in astronomy
pressure = Measurement(1.01325e6, 500)  # 1 atm = 1.01325e6 dyne/cm^2

print(f"Temperature: {temp.value} +/- {temp.error} K")
print(f"Pressure: {pressure.value:.2e} +/- {pressure.error} dyne/cm^2")
print(f"Pressure relative error: {pressure.relative_error():.3f}%")
```

### Understanding `self`

:::{margin}
**self**
The first parameter of instance methods, referring to the specific object being operated on.
:::

The `self` parameter is how each object keeps track of its own data. When you call `temp.relative_error()`, Python automatically passes `temp` as the first argument. Here's what happens behind the scenes:

```{code-cell} python
class Counter:
    """Demonstrates how self works."""

    def __init__(self):
        """Initialize counter at zero."""
        self.count = 0  # Each object gets its own count

    def increment(self):
        """Increment this counter by one."""
        self.count += 1  # self refers to the specific object

    def get_count(self):
        """Return current count value."""
        return self.count

# Each object maintains independent state
c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()
c2.increment()

print(f"Counter 1: {c1.get_count()}")  # 2
print(f"Counter 2: {c2.get_count()}")  # 1

# What Python actually does when you call c1.increment():
# Counter.increment(c1)  # c1 becomes 'self' in the method
```

This seemingly simple concept of bundling data with behavior revolutionized programming. Let me tell you how it started...

:::{note} 🌟 The More You Know: How Norwegian Scientists Invented OOP to Simulate Complex Systems
:class: dropdown

In 1962, Norwegian computer scientists Kristen Nygaard and Ole-Johan Dahl faced a mounting challenge at the Norwegian Computing Center. Nygaard had been developing simulations since 1957 - first for nuclear reactor calculations, then for operations research problems. Their early projects included analyzing factory layouts, airport departure systems, and harbor operations. The existing approaches using ALGOL 60 were becoming unwieldy for modeling these complex, interconnected systems with hundreds of interacting components.

Their revolutionary solution? Create "objects" that bundled data with behavior. In 1965, they successfully used [SIMULA](http://kristennygaard.org/FORSKNINGSDOK_MAPPE/F_OO_start.html) I to analyze the Raufoss ammunitions factory layout - determining optimal arrangements for cranes and storage points. The program, punched on 1,130 cards, could simulate 2.5 days of factory operations in just 22 seconds. Each crane, storage point, and workstation became an object that knew its own state and could respond to events.

```python
# Simplified concept in modern Python:
class FactoryStation:
    def __init__(self, name, capacity, processing_time):
        self.name = name
        self.capacity = capacity
        self.queue = []

    def receive_item(self, item):
        # Each station manages its own queue and processing
        self.queue.append(item)
```

By 1967, Simula 67 formalized these concepts into classes, inheritance, and virtual methods - the foundation of modern OOP. Alan Kay, influenced by Simula (along with Sketchpad and his biology background), coined "object-oriented programming" around the same time. He later explained: "I thought of objects being like biological cells and/or individual computers on a network, only able to communicate with messages."

The impact was profound but gradual. Simula influenced Smalltalk in the 1970s, then C++ in the 1980s, and eventually Java in the 1990s. The Norwegian Computing Center, initially focused on practical simulation problems, had accidentally created one of computing's most transformative paradigms. Today, when you create a Particle class or a Galaxy object, you're using concepts born from the need to simulate factories, airports, and harbors in 1960s Norway!

*[Sources: Dahl & Nygaard (1978). "The development of the SIMULA languages." ACM SIGPLAN Notices; Kay, A. (2003). Email to Stefan Ram on OOP definition]*
:::

:::{important} Common Bug Alert: Forgetting self

```python
# WRONG - Missing self parameter
class BadClass:
    def method():  # Missing self!
        return "something"

# This fails:
# obj = BadClass()
# obj.method()  # TypeError: takes 0 arguments but 1 given

# CORRECT - Always include self
class GoodClass:
    def method(self):  # self is required
        return "something"

obj = GoodClass()
print(obj.method())  # Works!
```

This is probably the most common OOP error. An instance method needs a first
parameter that receives the instance when it is called through an object; by
convention, that parameter is named `self`.
:::

### Instance vs Class Attributes

:::{margin}
**Instance Attribute**
Data unique to each object, defined with `self.attribute`.
:::

Instance attributes belong to specific objects. Class attributes are shared by all instances. This bundling of data and methods is called **encapsulation** - a core principle of OOP:

:::{margin}
**Class Attribute**
Data shared by all instances of a class, defined directly in the class body.
:::

```{code-cell} python
class Simulation:
    """Demonstrates instance vs class attributes."""

    # Class attribute - shared by all simulations
    speed_of_light = 2.998e10  # cm/s (CGS)
    total_runs = 0

    def __init__(self, name, particle_count):
        """Initialize a new simulation."""
        # Instance attributes - unique to each simulation
        self.name = name
        self.particle_count = particle_count
        self.time = 0.0
        self.box_size_cm = 1.0e-4  # 1 micron box
        # Increment shared counter
        Simulation.total_runs += 1

    def advance(self, dt):
        """Advance simulation by dt seconds."""
        self.time += dt

# Create simulations
sim1 = Simulation("Test A", 1000)
sim2 = Simulation("Test B", 5000)

print(f"Total simulations: {Simulation.total_runs}")
print(f"Sim1 particles: {sim1.particle_count}")
print(f"Sim2 particles: {sim2.particle_count}")
print(f"Speed of light: {Simulation.speed_of_light:.2e} cm/s")
print(f"Box size: {sim1.box_size_cm:.2e} cm")
```

::::{note} 🔍 Check Your Understanding

What's the output of this code? Why?

```python
class DataPoint:
    count = 0  # Class attribute

    def __init__(self, value):
        self.value = value  # Instance attribute
        DataPoint.count += 1

p1 = DataPoint(10)
p2 = DataPoint(20)
p1.count = 100  # What happens here?

print(f"p1.count: {p1.count}")
print(f"p2.count: {p2.count}")
print(f"DataPoint.count: {DataPoint.count}")
```

:::{tip} Answer
:class: dropdown

Output:

- `p1.count: 100`
- `p2.count: 2`
- `DataPoint.count: 2`

When you write `p1.count = 100`, you create a new instance attribute that shadows the class attribute for `p1` only. The class attribute remains unchanged at 2, and `p2` still sees the class attribute. This is a common source of confusion - instance attributes can hide class attributes with the same name!
:::
::::

:::{tip} 💡 Attribute Lookup Order

For an ordinary attribute, a useful first approximation is:

1. **Instance `__dict__`** — attributes specific to this object
2. **Class attributes** — shared by all instances
3. **Base classes** — inherited attributes (Chapter 10)

This is why `p1.count = 100` creates a *new* instance attribute that shadows
the class attribute. The class attribute still exists at `DataPoint.count`.

Properties are an important refinement: a property with a setter is a *data
descriptor*, so it takes precedence over an entry in the instance dictionary.
That is why `circle.radius = 10` runs the property's setter rather than simply
creating an unrelated `radius` attribute. Python's full lookup rules also
involve descriptors and `__getattribute__`; use the simplified order above for
the ordinary class-attribute case shown here.
:::

:::{margin}
**Encapsulation**
The bundling of data and methods that operate on that data within a single unit (class).
:::

---

## 6.3 Methods: Functions Attached to Objects

:::{margin}
**Method**
A function defined inside a class that operates on instances of that class.
:::

Methods are functions that belong to a class. They can access and modify the object's state through `self`. Let's build up from simple to complex.

```{code-cell} python
import math  # Import at the top of your files in production code

# First: A simple class with basic methods
class Sample:
    """Scientific sample with basic operations."""

    def __init__(self, mass_g, volume_cm3):
        """Initialize with mass in grams, volume in cm^3."""
        self.mass = mass_g
        self.volume = volume_cm3

    def density(self):
        """Calculate density in g/cm^3."""
        return self.mass / self.volume

    def is_denser_than_water(self):
        """Check if denser than water (1 g/cm^3)."""
        return self.density() > 1.0

# Using simple methods
iron = Sample(7.87, 1.0)  # Iron sample
print(f"Iron density: {iron.density()} g/cm^3")
print(f"Sinks in water: {iron.is_denser_than_water()}")
```

Now let's advance to more complex mathematical methods:

```{code-cell} python
import math

class Vector2D:
    """A 2D vector for physics calculations."""

    def __init__(self, x, y):
        """Initialize vector components in cm."""
        self.x = x
        self.y = y

    def magnitude(self):
        """Calculate vector magnitude (length)."""
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        """Scale vector to unit length (magnitude = 1).

        Contract: MUTATES self.x and self.y in place; returns None.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        self.x /= mag
        self.y /= mag

    def dot(self, other):
        """Calculate dot product with another vector."""
        return self.x * other.x + self.y * other.y

    def angle_with(self, other):
        """Calculate angle with another vector in radians."""
        dot_product = self.dot(other)
        mags = self.magnitude() * other.magnitude()
        if mags == 0:
            raise ValueError("Angle is undefined when either vector has zero magnitude")
        cos_angle = dot_product / mags
        # Clamp to [-1, 1] to avoid numerical errors
        cos_angle = max(-1, min(1, cos_angle))
        return math.acos(cos_angle)

# Using vector methods
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 0)

print(f"v1 magnitude: {v1.magnitude()} cm")
print(f"Dot product: {v1.dot(v2)} cm^2")
print(f"Angle: {v1.angle_with(v2):.2f} radians")

v1.normalize()  # Makes magnitude = 1
print(f"After normalization: ({v1.x:.2f}, {v1.y:.2f})")
print(f"New magnitude: {v1.magnitude():.2f}")
```

:::{tip} Predict before running

What should `Vector2D(0, 0).angle_with(v2)` return? A zero vector has no
direction, so this implementation raises `ValueError` instead of inventing an
angle. Try the call, then explain why returning `0` would make a false geometric
claim.
:::

::::{note} 🔍 Check Your Understanding

Why does `normalize()` modify the vector in place while `magnitude()` returns a value?

:::{tip} Answer
:class: dropdown

This follows a fundamental **method contract** convention:

- **Mutation methods** modify object state in place and return `None` (like `list.sort()`, `v.normalize()`)
- **Computation methods** return values without changing the object (like `sorted(list)`, `v.magnitude()`)

**Why this matters for scientific code:** When you call `particle.update_position(dt)`, you expect the particle's state to change. When you call `particle.kinetic_energy()`, you expect to get a number back without side effects. Mixing these contracts leads to bugs: if `kinetic_energy()` secretly modified velocity, your simulation would be wrong.

The names hint at intent: *verbs* ("normalize", "update", "add") suggest mutation; *nouns* ("magnitude", "energy", "mean") suggest computation. Document the contract explicitly in docstrings when the name is ambiguous.

Some libraries return `self` from mutation methods to enable chaining (`v.normalize().scale(2)`). This breaks the "mutate $\to$ None" convention but is consistent within those libraries. Pick one convention and be consistent.
:::
::::

### Method Types: Instance, Class, and Static

```{code-cell} python
import math

class DataProcessor:
    """Demonstrates different method types."""

    version = "1.0"

    def __init__(self, data):
        """Materialize and validate one finite numeric input sequence."""
        try:
            values = list(data)
        except TypeError as error:
            raise ValueError("data must be an iterable of finite numbers") from error
        if not self.validate_data(values):
            raise ValueError("data must be a non-empty sequence of finite numbers")
        self.data = values

    # Instance method - needs self
    def process(self):
        """Process this object's data."""
        return sum(self.data) / len(self.data)

    # Class method - gets class, not instance
    @classmethod
    def from_values(cls, values):
        """Create an instance from an iterable of values."""
        return cls(values)

    # Static method - doesn't need self or cls
    @staticmethod
    def validate_data(values):
        """Check a materialized sequence of finite, non-Boolean numbers."""
        return len(values) > 0 and all(
            isinstance(x, (int, float))
            and not isinstance(x, bool)
            and math.isfinite(x)
            for x in values
        )

    # Static method with physics example
    @staticmethod
    def celsius_to_kelvin(celsius):
        """Convert Celsius to a finite, physically meaningful Kelvin value."""
        kelvin = celsius + 273.15
        if not math.isfinite(kelvin) or kelvin < 0:
            raise ValueError("temperature must be finite and not below absolute zero")
        return kelvin

# Using different method types
processor = DataProcessor([10, 20, 30])
print(f"Average: {processor.process()}")

# Class method creates a new instance
processor2 = DataProcessor.from_values([1, 2, 3, 4, 5])
print(f"Factory average: {processor2.process()}")

# Static methods work without instance
valid = DataProcessor.validate_data([1, 2, 3])
print(f"Data valid: {valid}")

# Physics static method
temp_k = DataProcessor.celsius_to_kelvin(25)
print(f"Temperature: {temp_k} K")
```

:::{tip} 💡 Computational Thinking Box: Methods as Interface

**PATTERN: Public Interface vs Private Implementation**

In scientific software, methods define how objects interact. Think of methods as the object's "API" - what it promises to do regardless of internal implementation.

**Public Interface** (what users see):

- `particle.update_position(dt)`
- `measurement.get_uncertainty()`
- `simulation.run_steps(100)`

**Private Implementation** (internal details):

- How position is stored (Cartesian? polar?)
- How uncertainty is calculated
- What algorithm updates the simulation

This separation allows you to change implementation without breaking code that uses your objects. NumPy arrays exemplify this: `arr.mean()` works the same whether the array is stored in row-major or column-major order, in RAM or memory-mapped.

**Best Practice**: Start method names with underscore (`_`) to indicate internal methods not meant for external use.
:::

:::{important} 🌟 Why This Matters: Real Astropy OOP
:class: dropdown

Here's how Astropy uses the OOP patterns you're learning:

```python
from astropy.coordinates import SkyCoord
from astropy import units as u

# SkyCoord is a class with properties and methods!
m31 = SkyCoord(ra=10.68*u.degree, dec=41.27*u.degree)
m33 = SkyCoord(ra=23.4621*u.degree, dec=30.6602*u.degree)
print(m31.galactic)  # Property with coordinate transformation
print(m31.separation(m33))  # Method for angular distance

# You're learning the same patterns that power professional astronomy code!
```
:::

---

## 6.4 Properties: Smart Attributes

:::{margin}
**Property**
A special attribute that executes code when accessed or set, created with the `@property` decorator.
:::

:::{margin}
**Setter**
A property method that validates and sets attribute values, defined with `@attribute.setter`.
:::

Properties can enforce **declared invariants** through a controlled public interface. A circle's radius must be positive. A temperature can't go below absolute zero. A probability must be between 0 and 1. Without a controlled setter, any code could set `circle.radius = -5` and corrupt your simulation. With one, the class can reject values it explicitly recognizes as invalid:

**What properties give you:**

1. **Validation on assignment** — Reject invalid values immediately, not when they cause cryptic errors downstream
2. **Computed attributes** — Derive area from radius automatically, guaranteeing consistency
3. **Encapsulation** — Hide internal storage (`_radius`) while exposing a clean interface (`radius`)
4. **Invariant enforcement through the public interface** — Reject invalid
   assignments where the class controls updates; this is not a proof that every
   scientific assumption or internal mutation is valid

```{code-cell} python
import math

class Circle:
    """Circle with computed properties."""

    def __init__(self, radius):
        """Initialize with radius, using validation."""
        # This now uses the setter for validation!
        self.radius = radius

    @property
    def radius(self):
        """Get radius in cm."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius with validation."""
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value <= 0
        ):
            raise ValueError(f"Radius must be a finite positive number, got {value}")
        self._radius = value

    @property
    def area(self):
        """Computed area in cm^2 using $\\pi r^2$."""
        return math.pi * self._radius**2

    @property
    def circumference(self):
        """Computed circumference in cm using $2\\pi r$."""
        return 2 * math.pi * self._radius

# Properties look like attributes but run code
circle = Circle(5)
print(f"Radius: {circle.radius} cm")
print(f"Area: {circle.area:.2f} cm^2")
print(f"Circumference: {circle.circumference:.2f} cm")

# Changing radius automatically updates computed properties
circle.radius = 10
print(f"New area: {circle.area:.2f} cm^2")

# Validation prevents invalid states (even in __init__ now!)
try:
    bad_circle = Circle(-5)  # This will raise an error
except ValueError as e:
    print(f"Error: {e}")
```

### Properties for Unit Safety

```{code-cell} python
import math

class Temperature:
    """Temperature with automatic unit conversion."""

    def __init__(self, kelvin):
        """Initialize with temperature in Kelvin."""
        self.kelvin = kelvin  # Route construction through the same validation.

    @property
    def kelvin(self):
        """Get temperature in Kelvin."""
        return self._kelvin

    @kelvin.setter
    def kelvin(self, value):
        """Set temperature with validation."""
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError(f"Kelvin temperature must be finite and non-negative, got {value}")
        self._kelvin = value

    @property
    def celsius(self):
        """Get temperature in Celsius."""
        return self._kelvin - 273.15

    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius."""
        # Use kelvin setter for validation
        self.kelvin = value + 273.15

    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit."""
        return self._kelvin * 9/5 - 459.67

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature in Fahrenheit."""
        # Convert to Kelvin, using kelvin setter for validation
        self.kelvin = (value + 459.67) * 5/9

# Same temperature, different units
temp = Temperature(300)
print(f"Water at {temp.kelvin:.1f} K")
print(f"  = {temp.celsius:.1f}  degC")
print(f"  = {temp.fahrenheit:.1f}  degF")

# Set in any unit, always consistent
temp.celsius = 100
print(f"Boiling: {temp.kelvin:.1f} K")
```

:::{note} Predict → run → explain → revise: constructor validation

**Predict.** Should `Temperature(-1)` construct an object, or raise a
`ValueError`? Why must `__init__` assign through `self.kelvin` rather than
directly to `self._kelvin`?

**Static check.** Run this immediately after the `Temperature` definition
above; it should print the expected exception:

```python
try:
    Temperature(-1)
except ValueError as error:
    print(type(error).__name__, error)
```

**Explain.** The setter establishes the local invariant for construction and
later assignments. It does not validate a thermometer, its calibration, or the
meaning of a measurement.

**Revise.** Change `-1` to `0`, predict the result, then test it in the
browser lab below.
:::

::::{admonition} Browser Python lab · Temperature invariant
:class: tip

**Make a commitment before you run anything.** Will `Temperature(-1)` raise a
`ValueError`, and why does construction assign through `self.kelvin` instead of
directly setting `_kelvin`?

1. Open the short browser-local experiment.
2. Run the supplied check and compare its output with your prediction.
3. Change `-1` to `0` or `273.15`, predict again, and explain what the class
   verifies — and what it cannot, such as sensor calibration.

[Open the temperature-invariant experiment →](jupyterlite/ch06-temperature-invariant.html)

No installation or account is required. The activity source is Markdown in
`tools/jupyterlite/activities/ch06-temperature-invariant.md`; its executable
notebook is generated only when JupyterLite is built.
::::

### Astronomy-Specific Properties Example

```{code-cell} python
import math

class Observation:
    """Astronomical observation with computed conditions."""

    def __init__(self, target, altitude_deg, moon_days_since_new=0):
        """Initialize observation with target and conditions."""
        self.target = target
        self.altitude_deg = altitude_deg  # Object altitude in degrees
        self.moon_days = moon_days_since_new

    @property
    def airmass(self):
        """Calculate airmass from altitude (plane-parallel approximation).

        Note: This simplified sec(z) formula diverges at low altitudes.
        Production code should use Pickering (2002) or similar.
        """
        if not 10 <= self.altitude_deg <= 90:
            raise ValueError(
                "This plane-parallel toy model is only used here for "
                "10 <= altitude_deg <= 90; choose a validated airmass model outside that range."
            )
        # Convert to zenith angle
        zenith_deg = 90 - self.altitude_deg
        zenith_rad = math.radians(zenith_deg)
        # Plane-parallel approximation: X = sec(z).
        # Its stated domain guard above avoids presenting a low-altitude clamp
        # as a physical result.
        return 1.0 / math.cos(zenith_rad)

    @property
    def moon_phase(self):
        """Calculate moon illumination fraction (0=new, 1=full)."""
        # Simplified: actual calculations need ephemeris
        # Moon cycle is ~29.53 days
        phase_angle = 2 * math.pi * self.moon_days / 29.53
        # Illumination: 0 at new moon (day 0), 1 at full moon (day ~14.76)
        return (1 - math.cos(phase_angle)) / 2

    @property
    def moon_illumination_category(self):
        """Categorize lunar illumination, not total sky brightness."""
        if self.moon_phase < 0.25:
            return "Dark"
        elif self.moon_phase < 0.75:
            return "Grey"
        else:
            return "Bright"

# Example observation
obs = Observation("M31", altitude_deg=60, moon_days_since_new=7)
print(f"Observing {obs.target}:")
print(f"  Airmass: {obs.airmass:.2f}")
print(f"  Moon illumination: {obs.moon_phase:.1%}")
print(f"  Moon illumination category: {obs.moon_illumination_category}")
```

:::{note} Pedagogical Simplification

The `airmass` and `moon_phase` properties above are toy models for teaching
purposes. Moon illumination alone does not determine sky brightness: separation
from the target, lunar altitude, extinction, and site conditions also matter.
Real astronomical calculations use ephemeris data and more sophisticated
formulas. For production work, use [Astropy](https://www.astropy.org/) and a
validated observing model for the question at hand.
:::

:::{important} 🌟 Why This Matters: The Therac-25 and the Importance of Validation
:class: dropdown

The Therac-25 accidents show why a local validation rule is not enough for a
safety-critical system. Between 1985 and 1987, the machine caused at least six
accidents involving massive radiation overdoses; three patients died directly
from the overdoses.

The investigation identified multiple unsafe conditions: race conditions, unsafe state transitions, poor error reporting, and inadequate system engineering. The machine could operate in electron-beam mode (low power) or X-ray mode (high power with a metal target); in a dangerous configuration, high power could be delivered without that target.

The class below is a **fictional local-invariant illustration**, not a
reconstruction of Therac-25 software and not a claim that Python properties
would have prevented the accidents:

```python
# PSEUDOCODE: this deliberately omits the device's real state model and the
# value of ELECTRON_MAX. It is not runnable Python or a Therac reconstruction.
class RadiationTherapyMachine:
    def __init__(self):
        self._mode = None
        self._power_level = 0
        self._target_in_place = False

    @property
    def power_level(self):
        return self._power_level

    @power_level.setter
    def power_level(self, value):
        # Reject one modeled unsafe configuration; this is not the device's model.
        if self._mode == "electron" and value > ELECTRON_MAX:
            raise ValueError("Power too high for electron mode!")
        if self._mode == "xray" and not self._target_in_place:
            raise ValueError("X-ray mode requires target!")
        self._power_level = value
```

Setter validation can make one local state transition explicit. It cannot by
itself establish concurrency safety, hardware interlocks, requirements
traceability, or independent system verification—the broader controls that
safety-critical software needs.

[Source: Leveson, N.G. & Turner, C.S. (1993). "An Investigation of the Therac-25 Accidents". IEEE Computer, 26(7), 18-41.]
:::

:::{note} 🌟 The More You Know: Hubble's Mirror and Independent Measurement
:class: dropdown

In 1990, the Hubble Space Telescope reached orbit with a catastrophic optical
flaw: its primary mirror was ground to the wrong shape. The incident shows why
independent measurements, explicit interfaces, and careful investigation of
disagreement matter in scientific work.

The class below is a **fictional classroom illustration**, not a reconstruction
of Hubble's testing software and not evidence that a Python property alone would
have prevented the failure. It illustrates a narrower design question: how might
a program reject an input outside a documented range and flag disagreement with
an independent expectation?

Use the example to discuss the limits of validation: a check is only as useful
as its assumptions, tolerances, independent evidence, and response when it
finds a disagreement.

```python
# ILLUSTRATIVE Python: the values below are classroom values, not Hubble
# specifications or a reconstruction of the mirror-testing software.
import warnings

class MirrorMeasurement:
    def __init__(self, expected_value, allowed_range, relative_tolerance):
        self.expected_value = expected_value
        self.allowed_range = allowed_range
        self.relative_tolerance = relative_tolerance
        self._measured_value = None

    @property
    def measured_value(self):
        return self._measured_value

    @measured_value.setter
    def measured_value(self, value):
        low, high = self.allowed_range
        if not low <= value <= high:
            raise ValueError(f"Outside the declared design range: {value}")

        deviation = abs(value - self.expected_value) / self.expected_value
        if deviation > self.relative_tolerance:
            warnings.warn(
                f"Measurement deviates {deviation * 100:.2f}% from expectation",
                UserWarning,
                stacklevel=2,
            )

        self._measured_value = value
```

Validation code can make a local contract visible and testable. It cannot replace
independent measurement, system-level verification, or scientific judgment.

:::

:::{important} 🌟 Why This Matters: Mars Climate Orbiter
:class: dropdown

In 1999, Mars Climate Orbiter was lost after ground navigation calculations
received angular-momentum-desaturation impulse data in pound-force seconds
(lbf-s) while another interface expected newton-seconds (N-s). The mismatch
introduced an approximately 4.45 conversion factor into navigation
calculations; it was not a claim that the physical thrusters fired at
4.45$\times$ their intended force.

The class below is a classroom illustration of a single unit-conversion boundary,
not a reconstruction of the mission or a claim that a property alone prevents
system-level interface failures. It deliberately names *impulse* rather than
thrust: newton-seconds and pound-force seconds are impulse units. See NASA's [Mars Climate Orbiter Mishap
Investigation Board report](https://discovery.larc.nasa.gov/pdf_files/MCO_report_2.pdf)
for the actual failure analysis.

```python
import math

class NavigationImpulse:
    def __init__(self, impulse_newton_seconds=0.0):
        self.impulse_newton_seconds = impulse_newton_seconds

    @property
    def impulse_newton_seconds(self):
        return self._impulse_ns

    @impulse_newton_seconds.setter
    def impulse_newton_seconds(self, value):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError("impulse must be a finite number")
        self._impulse_ns = value

    @property
    def impulse_pound_force_seconds(self):
        return self._impulse_ns * 0.224809

    @impulse_pound_force_seconds.setter
    def impulse_pound_force_seconds(self, value):
        self.impulse_newton_seconds = value / 0.224809
```

The lesson is narrower: a class can store one documented internal unit and
convert at a well-defined boundary. That convention helps only when every input
path is validated and the interface is tested; a Python property does not itself
guarantee unit consistency or prevent a system-level interface error.
:::

::::{note} 🔍 Check Your Understanding

What happens if you create a property without a setter but try to assign to it?

```python
class ReadOnly:
    @property
    def value(self):
        return 42

obj = ReadOnly()
obj.value = 100  # What happens?
```

:::{tip} Answer
:class: dropdown

You get an `AttributeError` because the property has no setter (the exact message is Python-version dependent). Properties without setters are read-only. This is useful for computed values that should never be directly modified, like the area of a circle (which should only change when the radius changes). This pattern can protect a declared local relationship from accidental assignment.
:::
::::

:::{important} Common Bug Alert: Property Recursion

```python
# WRONG - Infinite recursion!
class BadExample:
    @property
    def value(self):
        return self.value  # Calls itself forever!

# CORRECT - Use different internal name
class GoodExample:
    def __init__(self):
        """Initialize with internal storage."""
        self._value = 0  # Underscore prefix

    @property
    def value(self):
        """Access the value."""
        return self._value  # Different name

example = GoodExample()
print(f"Value: {example.value}")
```

Always use a different internal name (usually with underscore) for the actual storage.
:::

---

(deep-dive-python-protocols)=
## Deep Dive: Python Protocols and Special Methods

:::{margin}
**Special Method**
Methods with double underscores (like `__init__`, `__str__`) that define object behavior for built-in operations.
:::

Special methods (also called "magic methods" or "dunder methods") let your
objects work with Python's built-in functions and operators. The phrase "duck
typing" is shorthand for a related idea: an operation can depend on the
capability an object supplies, rather than on one nominal class alone. Code may
still make explicit type checks when a scientific interface needs them.

:::{margin}
**Duck Typing**
A style in which an operation depends on supported behavior or a protocol,
rather than only on a declared class.
:::

:::{note} 🌟 The More You Know: How Python Made Protocols Visible
:class: dropdown

In December 1989, Guido van Rossum began developing Python at CWI in Amsterdam,
building on ideas from ABC and work around the Amoeba distributed operating
system. He named the language after *Monty Python's Flying Circus*. Python's
history is not a story in which one language suddenly made operator overloading
possible—C++ and other languages already had related mechanisms. The useful
Python design lesson is more specific: common operations are exposed through
documented methods that ordinary classes can implement.

Want an object to work with `len()`? Implement `__len__()`. Want it to support
addition? Implement `__add__()`. Python's interpreter dispatches the operation
through those protocol methods. That visible connection is valuable for a
reader: syntax such as `a + b` has an inspectable object-level contract.

For a user-defined Python class, for example:

```python
class Vector:
    def __add__(self, other):
        # Define a documented operation for this class.
        return Vector(self.x + other.x, self.y + other.y)

v1 + v2  # Calls Vector.__add__
```

Scientific libraries take advantage of the same protocol hooks. Numeric, an
ancestor of NumPy, used operations such as addition, slicing, length, and
printing to make arrays work naturally in Python:

```python
# Scientific arrays that feel built in.
array1 + array2    # Element-wise addition via __add__
array[5:10]        # Slicing via __getitem__
len(array)         # Size via __len__
print(array)       # Readable output via __str__
```

When you implement `__str__` or `__add__`, you are making your class participate
in one of Python's protocols. The obligation is not merely to add a magic name:
the operation needs a clear scientific meaning, documented units where relevant,
and behavior that callers can test.

**Sources:** Python's [history documentation](https://docs.python.org/3/license.html),
CWI's [account of Python's origin](https://www.cwi.nl/en/news/25-years-of-python-at-cwi/),
and Van Rossum (1996), foreword to *Programming Python*.
:::

```{code-cell} python
class Fraction:
    """A reduced fraction of two integers with arithmetic operations."""

    def __init__(self, numerator, denominator):
        """Initialize an integer fraction with a positive denominator."""
        if (
            isinstance(numerator, bool)
            or isinstance(denominator, bool)
            or not isinstance(numerator, int)
            or not isinstance(denominator, int)
        ):
            raise ValueError("numerator and denominator must be integers")
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        self.num = numerator
        self.den = denominator
        self._reduce()

    def _reduce(self):
        """Reduce to lowest terms using GCD (Euclidean algorithm)."""
        # Euclidean algorithm: repeatedly replace larger number
        # with remainder when divided by smaller number
        a, b = abs(self.num), abs(self.den)
        while b:  # Continue until remainder is 0
            a, b = b, a % b  # GCD(a,b) = GCD(b, a mod b)
        self.num //= a
        self.den //= a

    def __str__(self):
        """Human-readable string for print()."""
        return f"{self.num}/{self.den}"

    def __repr__(self):
        """Unambiguous string for debugging."""
        return f"Fraction({self.num}, {self.den})"

    def __float__(self):
        """Convert to float."""
        return self.num / self.den

    def __add__(self, other):
        """Add two fractions: a/b + c/d = (ad+bc)/bd"""
        if not isinstance(other, Fraction):
            return NotImplemented  # Let Python try other.__radd__
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Fraction(new_num, new_den)

    def __eq__(self, other):
        """Check equality: a/b == c/d if ad == bc"""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self.num * other.den == other.num * self.den

# Using special methods
f1 = Fraction(1, 2)
f2 = Fraction(1, 3)

print(f"f1 = {f1}")  # Calls __str__
print(f"f1 + f2 = {f1 + f2}")  # Calls __add__
print(f"f1 as float: {float(f1)}")  # Calls __float__
print(f"f1 == Fraction(2,4): {f1 == Fraction(2, 4)}")  # Calls __eq__
```

### Essential Special Methods

```{code-cell} python
class DataSet:
    """Collection that acts like a built-in container."""

    def __init__(self, values=None):
        """Initialize with optional values (makes a defensive copy)."""
        self.values = list(values) if values is not None else []

    def __len__(self):
        """Support len(dataset)."""
        return len(self.values)

    def __getitem__(self, index):
        """Support dataset[index]."""
        return self.values[index]

    def __setitem__(self, index, value):
        """Support dataset[index] = value."""
        self.values[index] = value

    def __contains__(self, value):
        """Support 'value in dataset'."""
        return value in self.values

    def __iter__(self):
        """Support for loops."""
        return iter(self.values)

    def __bool__(self):
        """Support if dataset: (True if not empty)."""
        return len(self.values) > 0

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"DataSet({self.values})"

# Acts like a built-in container
data = DataSet([10, 20, 30, 40, 50])

print(f"Length: {len(data)}")
print(f"First: {data[0]}")
print(f"Contains 30: {30 in data}")
print(f"Is non-empty: {bool(data)}")

data[1] = 25
for value in data:
    print(value, end=" ")
```

::::{note} 🔍 Check Your Understanding

Which special method would you implement to make your object work with the `abs()` function?

:::{tip} Answer
:class: dropdown

You would implement `__abs__()`. Python's built-in `abs()` function calls the object's `__abs__()` method if it exists. For example:

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        # Return magnitude for abs()
        return (self.x**2 + self.y**2)**0.5

v = Vector2D(3, 4)
print(abs(v))  # Prints 5.0
```

This pattern extends to many built-ins: `len()` calls `__len__()`, `str()` calls `__str__()`, etc. Understanding this connection helps you make objects that feel native to Python.
:::
::::

:::{tip} 💡 Computational Thinking Box: Protocol-Based Design

**PATTERN: Duck Typing Through Special Methods**
_"If it walks like a duck and quacks like a duck, it's a duck"_

Python's built-ins and many idiomatic APIs use capabilities expressed through
protocols. Your own code can still use explicit type checks when an interface
requires a particular scientific representation. An object that implements the
right protocol can participate in the corresponding operation:

**Iterable and iterator protocols:**

- An *iterable* implements `__iter__()` and returns an iterator.
- An *iterator* implements `__next__()` as well as `__iter__()`.
- A `for` loop asks an iterable for an iterator, then repeatedly calls
  `__next__()` on that iterator.

**Container Protocol:**

- `__len__()` and `__getitem__()` $\to$ works with `len()`, indexing

**Numeric Protocol:**

- `__add__()`, `__mul__()`, etc. $\to$ works with math operators

**Context Manager Protocol:**

- `__enter__()` and `__exit__()` $\to$ works with 'with' statement

**NumPy interoperability:**

- `__array__()` can provide an explicit conversion to a NumPy array
- `__array_ufunc__()` and `__array_function__()` can define selected NumPy
  operations for a custom array type

This is why your custom objects can work with built-in functions! A DataSet with `__len__` works with `len()`. A Vector with `__add__` works with `+`. This protocol-based design is central to Python's flexibility and why scientific libraries integrate so well.

**Real-world example:** A sequence may be accepted by `np.asarray`, but merely
adding `.shape`, `.dtype`, and `__getitem__` does not make a custom object
compatible with every NumPy function. Libraries such as PyTorch implement
their own documented interoperability protocols.
:::

---

(deep-dive-objects-or-functions)=
## Deep Dive: Choosing Objects or Functions

Now that you understand HOW to create classes with all their powerful features - properties for validation, special methods for integration, inheritance for code reuse (Chapter 10) - you need wisdom about WHEN to use them. Not every problem needs objects. Creating unnecessary classes can make code harder to understand, not easier. The art of programming lies in choosing the right tool for the right job.

:::{important} OOP Is a Tool, Not a Requirement

Learning OOP does **not** mean you should use classes everywhere. Many scientific computations are better expressed as pure functions:

- **Kepler's third law:** `period = orbital_period(semi_major_axis)` — no state needed
- **Unit conversion:** `kelvin = celsius_to_kelvin(temp)` — stateless transformation
- **Array operations:** `mean = np.mean(data)` — let NumPy handle it

**Use classes when:**

- You have **state that changes over time** (particle positions, running statistics)
- You need to **enforce invariants** (radius > 0, probability $\in$ [0,1])
- **Data and behavior are inseparable** (a measurement *knows* its uncertainty)

**Use functions when:**

- The operation is **stateless** (input $\to$ output, no memory)
- The logic is **generic** (works on any data, not tied to an entity)
- A class would just wrap a single method

**A useful prompt, not a rule:** If your class has only `__init__` and one
method, ask whether a function would make the purpose clearer. Small value
objects and adapters can still be worthwhile when they give data a stable,
tested interface. Conversely, if you're passing the same five variables to
every function, they might want to be an object.
:::

Here's how to decide. Note: In Chapter 10, we'll explore the "is-a" relationship (inheritance) versus "has-a" relationship (composition) in detail. For now, focus on single classes.

### Use Objects When:

1. **Managing State Over Time**

```{code-cell} python
class RunningStatistics:
    """Maintains statistics as data arrives."""

    def __init__(self):
        """Initialize empty statistics."""
        self.count = 0
        self._mean = 0.0
        self._M2 = 0.0

    def add_value(self, x):
        """Add new value to statistics.

        Contract: MUTATES internal state (count, _mean, _M2); returns None.
        """
        self.count += 1
        delta = x - self._mean
        self._mean += delta / self.count
        self._M2 += delta * (x - self._mean)

    @property
    def mean(self):
        """Current mean."""
        return self._mean if self.count > 0 else None

    @property
    def variance(self):
        """Current sample variance, or None until two values exist."""
        if self.count < 2:
            return None
        return self._M2 / (self.count - 1)
```

:::{important} Design decision: preserve sufficient running state

This class stores the running mean and the accumulated squared deviation rather
than `sum` and `sum_sq`. That is Welford's stable streaming update from Chapter
3. It makes the object useful both as an OOP example and as a more reliable
way to accumulate a sample variance. Returning `None` before two values makes
the unavailable statistic explicit rather than silently calling it zero.
:::

```{code-cell} python
# Object maintains state between calls
stats = RunningStatistics()
for value in [1, 2, 3, 4, 5]:
    stats.add_value(value)
    variance_text = "n/a" if stats.variance is None else f"{stats.variance:.1f}"
    print(f"After {value}: mean={stats.mean:.1f}, sample var={variance_text}")
```

2. **Modeling Real Entities**

```{code-cell} python
class Galaxy:
    """Model a galaxy with properties."""

    def __init__(self, name, distance_mpc, redshift):
        """Initialize galaxy with observed properties."""
        self.name = name
        self.distance_mpc = distance_mpc  # Megaparsecs
        self.redshift = redshift

    def recession_velocity(self):
        """Approximate low-redshift recession velocity in km/s."""
        c = 3e5  # km/s
        return c * self.redshift

    def lookback_time_gyr(self):
        """Estimate low-redshift lookback time in Gyr using a stated H0."""
        if self.redshift < 0:
            raise ValueError(
                "This low-redshift lookback approximation is not defined for a blueshifted object"
            )
        H0 = 70  # km/s/Mpc
        return self.redshift * 1000 / H0

m31 = Galaxy("Andromeda", 0.78, -0.001)  # Blueshifted!
print(f"{m31.name}: v={m31.recession_velocity():.0f} km/s")

# A deliberately illustrative low-redshift object, consistent with H0 = 70 km/s/Mpc.
example_galaxy = Galaxy("Illustrative low-redshift galaxy", 43.0, 0.01)
print(f"Lookback estimate: {example_galaxy.lookback_time_gyr():.2f} Gyr")
```

:::{important} Modeling boundary: a small-redshift estimate is not cosmology

The `Galaxy` methods use $v \approx cz$ and $t \approx z/H_0$, which are
low-redshift approximations with an adopted value of $H_0$. They are useful for
showing how behavior can belong to a data model, not for precision distances or
lookback times. Use an explicitly chosen cosmological model for that work.
:::

### Use Functions When:

1. **Simple Transformations**

```{code-cell} python
# No need for a class here
import math

def celsius_to_kelvin(celsius):
    """Convert Celsius to a finite Kelvin temperature above absolute zero."""
    kelvin = celsius + 273.15
    if not math.isfinite(kelvin) or kelvin < 0:
        raise ValueError("temperature must be finite and not below absolute zero")
    return kelvin

def orbital_period_years_solar_mass(semi_major_axis_au):
    """Return P in years for a negligible companion orbiting one solar mass."""
    if not math.isfinite(semi_major_axis_au) or semi_major_axis_au <= 0:
        raise ValueError("semi-major axis must be finite and positive")
    return semi_major_axis_au ** 1.5

# Simple functions are clearer than unnecessary classes
temp_k = celsius_to_kelvin(25)
period = orbital_period_years_solar_mass(1.0)  # Earth, to this approximation
print(f"Temperature: {temp_k} K")
print(f"Period: {period} years")
```

2. **Stateless Operations**

```{code-cell} python
# These don't need to remember anything between calls
def mean(values):
    """Calculate mean."""
    return sum(values) / len(values)

def population_standard_deviation(values):
    """Calculate population standard deviation for a non-empty sequence."""
    if not values:
        raise ValueError("values must not be empty")
    m = mean(values)
    variance = sum((x - m)**2 for x in values) / len(values)
    return variance**0.5

data = [1, 2, 3, 4, 5]
print(f"Mean: {mean(data)}")
print(f"Population std: {population_standard_deviation(data):.2f}")
```

:::{important} 🌟 Why This Matters: Why `ndarray` Is an Object
:class: dropdown

An `ndarray` is not only a collection of values. It also has shape, dtype,
strides, and a memory representation. That makes it a useful example of a
scientific object: selected operations can be methods because they act on that
array's representation, while many operations remain ordinary NumPy functions.

This is not a binary choice between an object-oriented API and a functional API:
NumPy deliberately supports both styles.

```python
# ILLUSTRATIVE NumPy API contrast; requires `import numpy as np` to run.
array = np.array([1, 2, 3])
mean = array.mean()
reshaped = array.reshape(3, 1)

# Functional forms are also part of NumPy's public interface.
same_mean = np.mean(array)
same_shape = np.reshape(array, (3, 1))
```

The design lesson is not “methods are faster” or “objects replace functions.”
It is that an abstraction should expose the data and operations a reader needs
without hiding its important representation. For large numerical workloads,
measure the stated operation on the stated array and backend rather than infer
performance from API style alone.
:::

:::{note} 🌟 The More You Know: How Astropy Coordinated an Astronomy Ecosystem
:class: dropdown

By the early 2010s, astronomy Python had many independently developed packages.
That variety created real coordination costs: common functionality, interfaces,
documentation, tests, and maintenance effort could be distributed across
projects. An early-2011 mailing-list conversation about the proliferation of
general astronomy packages led to a planning wiki where more than 100 people
voted for a shared package effort.

The formal beginning of the Astropy Project was a planning meeting at the
Harvard Center for Astrophysics in fall 2011—not a single package merger at a
Python in Astronomy conference. The project combined code already developed by
several contributors with common development practices and an ecosystem of
affiliated packages. Its purpose was coordination and interoperability, not a
claim that every astronomical concept should become a class.

The following contrast is schematic rather than an archival program. It shows
why stable interfaces can matter when scientific objects carry a coordinate
frame, metadata, or units:

```python
# SCHEMATIC: representative separate-package workflow, not archival code.
import pyfits
import pywcs
import coords

data = pyfits.getdata('image.fits')  # Returns numpy array
header = pyfits.getheader('image.fits')  # Returns header object
wcs = pywcs.WCS(header)  # Different coordinate object
# Convert pixel to sky - returns plain numpy array, no units!
sky = wcs.wcs_pix2sky([[100, 200]], 1)
# Now convert to different coordinate system - different package!
galactic = coords.Position((sky[0][0], sky[0][1])).galactic()
```

Astropy can instead supply coordinated interfaces:

```python
# Requires Astropy and an actual FITS file.
from astropy.io import fits
from astropy.wcs import WCS

with fits.open('image.fits') as hdul:
    wcs = WCS(hdul[0].header)

# A celestial WCS can return a SkyCoord with frame information.
sky = wcs.pixel_to_world(100, 200)
galactic = sky.galactic
```

Objects can help model astronomical concepts: a coordinate may carry a frame,
epoch, and distance; a table can carry column metadata and masks; and an Astropy
`Quantity` carries units through supported operations. Astropy does not make
every number unit-bearing automatically, and its interfaces still need tests at
the boundaries where data enter or leave a calculation.

The transferable lesson is community design: a shared scientific interface can
make it easier to reuse code, compare results, and maintain tools together.
That is a stronger and more realistic reason to care about representation than
claiming that one abstraction alone produced a scientific discovery.

**Sources:** Astropy's [project history](https://www.astropy.org/history.html),
the [Astropy Project overview](https://www.astropy.org/about), and Robitaille
et al. (2013), [*Astropy: A Community Python Package for Astronomy*](https://arxiv.org/abs/1307.6212).
:::

(reference-debugging-objects)=
## Reference: Debugging Small Scientific Objects

Understanding how to inspect and debug objects is crucial. Python provides powerful introspection tools to examine objects at runtime:

```{code-cell} python
class Instrument:
    """Scientific instrument for debugging demo."""

    def __init__(self, name, wavelength_nm):
        """Initialize instrument with name and wavelength."""
        self.name = name
        self.wavelength_nm = wavelength_nm
        self._calibrated = False

    def calibrate(self):
        """Calibrate instrument."""
        self._calibrated = True
        return f"{self.name} calibrated"

# Create instrument
spectrometer = Instrument("HARPS", 500)

# Introspection tools
print(f"Type: {type(spectrometer)}")
print(f"Class name: {spectrometer.__class__.__name__}")
print(f"Is Instrument?: {isinstance(spectrometer, Instrument)}")

# Check attributes
print(f"\nHas 'calibrate'?: {hasattr(spectrometer, 'calibrate')}")
print(f"Wavelength: {getattr(spectrometer, 'wavelength_nm', 'N/A')}")

# List all attributes (filtering out special ones)
attrs = [a for a in dir(spectrometer) if not a.startswith('_')]
print(f"\nPublic attributes: {attrs}")

# Instance __dict__ vs dir()
# __dict__ shows instance attributes only
# dir() shows everything the object can access
print(f"\nInstance __dict__: {vars(spectrometer)}")
print(f"dir() has {len(dir(spectrometer))} items (includes inherited)")
print(f"__dict__ has {len(vars(spectrometer))} items (instance only)")
```

### Type Hints with Classes (Optional)

Python supports type hints to document expected types, making code clearer:

```{code-cell} python
from typing import Optional, List

class ObservationLog:
    """Demonstrates type hints with classes."""

    def __init__(self, observer: str, target: str) -> None:
        """Initialize observation log with type hints."""
        self.observer: str = observer
        self.target: str = target
        self.entries: List[str] = []
        self.completion_time: Optional[float] = None

    def add_entry(self, entry: str) -> None:
        """Add log entry."""
        self.entries.append(entry)

    def get_entry_count(self) -> int:
        """Return number of entries."""
        return len(self.entries)

    def mark_complete(self, time_hours: float) -> None:
        """Mark observation complete."""
        self.completion_time = time_hours

# Type hints help IDEs and documentation
log = ObservationLog("J. Smith", "M31")
log.add_entry("Target acquired")
log.add_entry("Exposure started")
log.mark_complete(2.5)

print(f"Observer: {log.observer}")
print(f"Entries: {log.get_entry_count()}")
print(f"Duration: {log.completion_time} hours")
```

::::{note} 🛠️ Debug This!

This code has a subtle but critical bug. Can you find it?

```python
class Observatory:
    def __init__(self, name, telescopes=[]):  # Bug here!
        self.name = name
        self.telescopes = telescopes

    def add_telescope(self, telescope):
        """Add a telescope to this observatory."""
        self.telescopes.append(telescope)

# Test the code
keck = Observatory("Keck")
keck.add_telescope("Keck I")

vlt = Observatory("VLT")
vlt.add_telescope("Antu")

print(f"Keck telescopes: {keck.telescopes}")
print(f"VLT telescopes: {vlt.telescopes}")  # Unexpected output!
```

:::{tip} Solution
:class: dropdown

The bug is the mutable default argument `telescopes=[]`. All instances share the same list! When you add a telescope to one observatory, it appears in all of them.

**Fix:**
```python
def __init__(self, name, telescopes=None):
    self.name = name
    self.telescopes = telescopes if telescopes is not None else []
```

This bug can make observatories that should be independent share telescopes.
Use `None` as the default for a mutable argument, then create a new object in
the method.
:::
::::

## Main Takeaways

You've just made a fundamental leap in how you think about programming. Object-Oriented Programming isn't just a different syntax—it's a different mental model. Instead of thinking "what operations do I need to perform on this data?", you now think "what *is* this thing and what can it *do*?" This shift from procedural to object-oriented thinking mirrors how we naturally conceptualize scientific systems. A particle isn't just three numbers for position; it's an entity with mass, velocity, and behaviors like moving and colliding. This conceptual alignment makes complex programs more intuitive and maintainable.

The power of OOP becomes clear when managing complexity. That simple Particle class with five attributes and three methods might seem like overkill compared to a dictionary. But when a simulation has many particles that need consistent updates, validation, and state tracking, a carefully designed class can make local contracts easier to inspect and test. Properties can validate a controlled update, methods can make the intended state transition explicit, and special methods can integrate an object with Python syntax. None of those mechanisms alone establishes system-level correctness: interfaces, units, models, and independent evidence still need their own checks.

The historical journey from SIMULA to modern Python reveals how OOP emerged from practical needs. Norwegian scientists needed to simulate factories and harbors, leading them to bundle data with behavior—the birth of objects. This paradigm spread through Smalltalk, C++, Java, and Python. When you write `__add__` to define addition for an object, you are participating in a visible Python protocol; scientific libraries can choose compatible protocols when doing so serves a real interface.

But perhaps the most important lesson is knowing when NOT to use objects. Not every function needs to become a method. Not every data structure needs to become a class. Simple calculations should stay as functions. Stateless transformations don't need objects. The art lies in recognizing when you're modeling entities with state and behavior (use classes) versus performing operations on data (use functions). An array's shape, dtype, and memory layout make an object interface useful, while Astropy shows how a community can coordinate scientific representations and interfaces.

Looking ahead, everything in Python's scientific stack builds on these concepts. NumPy arrays are objects with methods like `.mean()` and `.reshape()`. Every Matplotlib plot is an object maintaining state about axes, data, and styling. When you write `array.sum()` or `figure.savefig()`, you're using the same patterns you just learned. More importantly, you can now create your own scientific classes that integrate seamlessly with these tools. You're not just learning to use objects—you're learning to think in objects, and that's a superpower for scientific computing that will serve you throughout your career.

---

**What's Next:** You now have the conceptual tools to understand *why* NumPy arrays are objects with methods, *how* properties can expose local constraints, and *why* special methods like `__getitem__` enable slicing syntax. In Chapter 7, you'll see these OOP patterns in action at scale through arrays and broadcasting. The classes you learned to build here are the foundation; NumPy is where you learn to *leverage* related ideas for real scientific work.

## Definitions

**attribute** - A variable that belongs to an object. Instance attributes are unique to each object; class attributes are shared by all instances

**class** - A blueprint or template for creating objects. Defines what attributes and methods objects will have

**class attribute** - Data shared by all instances of a class, defined directly in the class body

**constructor** - The `__init__` method that initializes new objects when they're created

**duck typing** - A style in which an operation relies on supported behavior or a protocol rather than only a declared class; code may still use explicit type checks when needed

**encapsulation** - The bundling of data and methods that operate on that data within a single unit (class)

**instance** - A specific object created from a class. Each instance has its own set of instance attributes

**instance attribute** - Data unique to each object, defined with `self.attribute`

**method** - A function defined inside a class that operates on instances of that class

**object** - A specific instance of a class containing data (attributes) and behavior (methods)

**object-oriented programming** - A programming paradigm that organizes code around objects (data) and methods (behavior)

**property** - A special attribute that executes code when accessed or set, created with the `@property` decorator

**self** - The first parameter of instance methods, referring to the specific object being operated on

**setter** - A property method that validates and sets attribute values, defined with `@attribute.setter`

**special method** - Methods with double underscores (like `__init__`, `__str__`) that define object behavior for built-in operations

**static method** - A method that doesn't receive self or cls, defined with `@staticmethod`

## Key Takeaways

✓ **Classes combine data and behavior** – Objects bundle related attributes and methods, helping keep coordinated state and operations inspectable

✓ **The self parameter connects methods to objects** – It's automatically passed to methods and refers to the specific instance being operated on

✓ **Properties provide smart attributes** – Use `@property` for computed values and declared local validation, while still testing the wider scientific interface

✓ **Special methods make objects Pythonic** – Implementing `__str__`, `__len__`, `__add__` lets your objects work naturally with built-in functions and operators

✓ **Instance attributes belong to objects, class attributes are shared** – Choose instance for object-specific data, class for constants and shared state

✓ **Not everything needs to be a class** – Use objects for stateful entities with behavior, functions for simple calculations and transformations

✓ **Properties can expose local unit checks** – Validation in setters can catch a declared local constraint, but system-level unit interfaces require independent verification

✓ **Everything in Python is an object** – Even functions and modules are objects, making Python's object model consistent and powerful

✓ **Duck typing enables flexibility** – Protocols let operations depend on supported capabilities; explicit type checks remain appropriate when an interface requires them

✓ **OOP emerged from practical simulation needs** – SIMULA's factory simulations birthed the paradigm that now powers scientific computing

## Reference: Class Syntax, Protocols, and Debugging

### Class Definition Syntax

| Element | Syntax | Example |
|---------|--------|---------|
| Define class | `class Name:` | `class Particle:` |
| Constructor | `def __init__(self):` | `def __init__(self, mass):` |
| Instance attribute | `self.attr = value` | `self.mass = 1.67e-24` |
| Class attribute | `attr = value` | `SPEED_OF_LIGHT = 3e10` |
| Instance method | `def method(self):` | `def velocity(self):` |
| Property getter | `@property` plus a getter | `@property` + `def energy(self):` |
| Property setter | `@attr.setter` plus a setter | `@energy.setter` + `def energy(self, value):` |
| Class method | `@classmethod` | `@classmethod` + `def from_values(cls, values):` |
| Static method | `@staticmethod` | `@staticmethod` + `def validate(data):` |

### Essential Special Methods

| Method | Purpose | Called By |
|--------|---------|-----------|
| `__init__` | Initialize object | `MyClass()` |
| `__str__` | Human-readable string | `str(obj)`, `print(obj)` |
| `__repr__` | Developer string | `repr(obj)` |
| `__len__` | Get length | `len(obj)` |
| `__getitem__` | Get by index | `obj[i]` |
| `__setitem__` | Set by index | `obj[i] = val` |
| `__contains__` | Check membership | `x in obj` |
| `__iter__` | Make iterable | `for x in obj` |
| `__add__` | Addition | `obj1 + obj2` |
| `__eq__` | Equality test | `obj1 == obj2` |
| `__bool__` | Truth value | `if obj:`, `bool(obj)` |
| `__call__` | Make callable | `obj()` |
| `__abs__` | Absolute value | `abs(obj)` |
| `__float__` | Convert to float | `float(obj)` |

### When to Use Classes vs Functions

| Use Classes When | Use Functions When |
|-----------------|-------------------|
| Managing state over time | Simple transformations |
| Modeling real entities | Stateless operations |
| Operations belong to data | One-way data flow |
| Need data validation | No state to maintain |
| Complex initialization | Simple input $\to$ output |
| Multiple related methods | Single operation |

### Debugging Object Tools

| Function | Purpose | Example |
|----------|---------|---------|
| `type(obj)` | Get object's class | `type(particle)` |
| `isinstance(obj, cls)` | Check if object is instance | `isinstance(p, Particle)` |
| `hasattr(obj, 'attr')` | Check if attribute exists | `hasattr(p, 'mass')` |
| `getattr(obj, 'attr')` | Get attribute safely | `getattr(p, 'mass', 0)` |
| `setattr(obj, 'attr', val)` | Set attribute | `setattr(p, 'mass', 1.0)` |
| `dir(obj)` | List all accessible attributes | `dir(particle)` |
| `vars(obj)` or `obj.__dict__` | Get instance attributes only | `vars(particle)` |
| `help(obj)` | Get documentation | `help(Particle)` |

## Recap and next connection

Part II begins with [Chapter 7: NumPy Fundamentals](../04-scientific-computing/07-numpy-fundamentals.md).
There, arrays provide a different kind of abstraction: many numerical values,
their shape, and operations over them. Carry forward the same habits—name
assumptions, protect invariants, and test a known case.

## References

1. **Mars Exploration Rover Spirit Recovery (2004)**
   - NASA JPL. (2004). *Mars Exploration Rover Mission: Spirit Anomaly Report*. Jet Propulsion Laboratory.
   - Reeves, G., & Neilson, T. (2005). "The Mars Rover Spirit FLASH Anomaly." *IEEE Aerospace Conference Proceedings*.

2. **SIMULA and OOP Origins (1960s)**
   - Nygaard, K., & Dahl, O. J. (1978). "The development of the SIMULA languages." *ACM SIGPLAN Notices*, 13(8), 245-272.
   - Holmevik, J. R. (1994). "Compiling SIMULA: A Historical Study of Technological Genesis." *IEEE Annals of the History of Computing*, 16(4), 25-37.

3. **Therac-25 Radiation Accidents (1985-1987)**
   - Leveson, N.G. & Turner, C.S. (1993). "An Investigation of the Therac-25 Accidents." *IEEE Computer*, 26(7), 18-41.

4. **Hubble Space Telescope Mirror Error (1990)**
   - Allen, L. (1990). *The Hubble Space Telescope Optical Systems Failure Report*. NASA-TM-103443.
   - Chaisson, E. (1994). *The Hubble Wars*. New York: HarperCollins. ISBN 0-06-017114-6.

5. **Mars Climate Orbiter Loss (1999)**
   - Stephenson, A. G. et al. (1999). *Mars Climate Orbiter Mishap Investigation Board Report*. NASA.
   - Oberg, J. (1999). "Why the Mars Probe Went Off Course." *IEEE Spectrum*, 36(12), 34-39.

6. **NumPy Design Decisions (2005)**
   - Oliphant, T. E. (2006). *A guide to NumPy* (Vol. 1). USA: Trelgol Publishing.
   - Van Der Walt, S., Colbert, S. C., & Varoquaux, G. (2011). "The NumPy array: a structure for efficient numerical computation." *Computing in Science & Engineering*, 13(2), 22-30.

7. **Astropy Unification (2011-2013)**
   - Robitaille, T., et al. (2013). "Astropy: A community Python package for astronomy." *Astronomy & Astrophysics*, 558, A33.
   - Greenfield, P. (2011). "What Python Can Do for Astronomy." *Proceedings of the 20th Annual Python in Science Conference*.

8. **Python Language Design**
   - Van Rossum, G. (1996). Foreword for "Programming Python" (1st ed.). O'Reilly Media.
   - Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual*. CreateSpace.
   - Martelli, A. (2000). "The Python 'Duck Typing' Principle." comp.lang.python newsgroup archives.

9. **Object-Oriented Design Principles**
   - Kay, A. (1993). "The early history of Smalltalk." *ACM SIGPLAN Notices*, 28(3), 69-95.
   - Kay, A. (2003). Email correspondence to Stefan Ram on the definition of object-oriented programming.

10. **Python OOP Resources**
    - Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media.
    - Ramalho, L. (2015). *Fluent Python*. O'Reilly Media.
    - Beazley, D., & Jones, B. K. (2013). *Python Cookbook* (3rd ed.). O'Reilly Media.
