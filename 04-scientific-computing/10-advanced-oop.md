---
title: "Chapter 10: Advanced OOP Patterns - Architecting Scientific Software"
subtitle: "COMP 536 | Scientific Computing Core"
author: "Anna Rosen"
---


## Learning Objectives

By the end of this chapter, you will be able to:

- Design abstract base classes that enforce scientific interfaces and invariants
- Implement advanced inheritance with mixins and multiple inheritance for code reuse
- Apply metaprogramming techniques including descriptors and metaclasses for domain-specific behavior
- Use design patterns (Factory, Observer, Strategy) to solve recurring architectural problems
- Implement dataclasses to reduce boilerplate in data-heavy scientific classes
- Create asynchronous code for concurrent instrument control and data acquisition
- Optimize memory and performance using `__slots__`, caching, and profiling techniques
- Recognize these patterns in NumPy, SciPy, Matplotlib, and other scientific libraries

## Prerequisites Check

Before starting this chapter, verify you can:

- ✓ Create classes with methods, properties, and special methods (Chapter 6)
- ✓ Use NumPy arrays and vectorized operations (Chapters 7-8)
- ✓ Create Matplotlib figures and subplots (Chapter 8)
- ✓ Work with decorators like `@property` (Chapter 6)
- ✓ Understand array broadcasting and ufuncs (Chapter 7)

Quick diagnostic:

```python
# Can you identify the OOP patterns in this NumPy/Matplotlib code?
import numpy as np
import matplotlib.pyplot as plt

# Pattern 1: Factory
arr = np.array([1, 2, 3])  # What pattern?

# Pattern 2: Context Manager
with plt.style.context('dark_background'):  # What pattern?
    fig, ax = plt.subplots()  # Pattern 3: ?

# Pattern 4: Method chaining
result = arr.reshape(3, 1).mean(axis=0)  # What pattern?
```

If you recognized factory, context manager, factory again, and fluent interface patterns, you're ready to understand how they work internally!

## Chapter Overview

You've mastered NumPy's powerful arrays and created stunning visualizations with Matplotlib. You've noticed that NumPy arrays somehow work with every mathematical operator, that Matplotlib figures manage complex state across multiple method calls, and that both libraries seem to magically know how to work together. How does `np.array([1,2,3]) + np.array([4,5,6])` know to add element-wise? Why can you pass NumPy arrays directly to Matplotlib functions? How do these libraries coordinate thousands of classes and millions of lines of code while remaining so elegant to use? The answer lies in advanced object-oriented patterns - the architectural principles that make scientific Python possible.

This chapter reveals the design patterns hidden throughout the scientific Python ecosystem you've been using. You'll discover that NumPy's universal functions (ufuncs) rely on abstract base classes to ensure every array type supports the same operations. Matplotlib's figure and axes use mixins to compose dozens of plotting capabilities without code duplication. Unit-aware libraries use descriptors and metaclasses to catch unit errors at assignment time, not after your simulation crashes. These aren't academic exercises - they're the exact patterns that power the tools enabling modern scientific discoveries, from detecting gravitational waves to analyzing particle collisions.

Most importantly, you'll develop the architectural thinking needed to contribute to these packages or build your own research-grade software. You'll understand why certain design decisions were made, recognize patterns when reading source code, and know when to apply these techniques in your own work. By the end, you'll see NumPy, Matplotlib, and other scientific libraries not as black boxes but as masterclasses in software architecture, and you'll have the skills to architect systems at the same level. This isn't just about learning advanced Python - it's about joining the community of developers who build the tools that enable scientific discovery.

## 10.1 Abstract Base Classes: Defining Scientific Interfaces

:::{margin}
**Abstract Base Class (ABC)**
A class that cannot be instantiated and defines methods that subclasses must implement.
:::

:::{margin}
**Interface**
A contract specifying what methods a class must provide, ensuring compatibility between components.
:::

Now that you've used NumPy and Matplotlib extensively, you've encountered abstract base classes without realizing it. Every time NumPy performs an operation on different array types, it's using ABCs to ensure compatibility. Let's understand how this works.

```python
from abc import ABC, abstractmethod
import numpy as np

# First, see the problem ABCs solve in scientific computing
class BadSensorArray:
    def read_counts(self):
        return np.array([100, 200, 300])  # raw counts

class BadDetectorArray:
    def get_flux(self):  # Different method name!
        return np.array([50, 60, 70])  # flux in erg/s/cm^2

# Without ABCs, incompatible interfaces cause runtime errors
# You've seen this problem when different data sources use different formats
```

Now let's solve this with ABCs, using CGS units throughout:

```python
from abc import ABC, abstractmethod

class ScientificDetector(ABC):
    """Abstract base defining detector interface in CGS units."""

    @abstractmethod
    def read_frame(self) -> np.ndarray:
        """Read one frame of data in erg/s/cm^2."""
        pass

    @abstractmethod
    def get_noise(self) -> float:
        """Return noise in erg/s/cm^2."""
        pass

    @abstractmethod
    def get_area_cm2(self) -> float:
        """Return detector area in cm^2."""
        pass

    # Concrete methods provide shared functionality
    def photons_to_flux(self, counts, wavelength_cm):
        """Convert photon counts to flux in erg/s/cm^2.

        E = hnu = hc/lambda where:
        h = 6.626e-27 erg*s (Planck in CGS)
        c = 2.998e10 cm/s (speed of light in CGS)
        """
        h = 6.626e-27  # erg*s
        c = 2.998e10   # cm/s
        energy_per_photon = h * c / wavelength_cm
        return counts * energy_per_photon

# Now implementations MUST follow the interface
class CCDDetector(ScientificDetector):
    """CCD implementation with CGS units."""

    def __init__(self, area_cm2=4.0, gain=1.0):
        self.area = area_cm2  # typically 2x2 cm for CCDs
        self.gain = gain
        self.read_noise = 5.0  # electrons

    def read_frame(self) -> np.ndarray:
        """Read CCD frame, return flux in erg/s/cm^2."""
        # Simulate Poisson photon noise
        photons = np.random.poisson(1000, size=(1024, 1024))
        # Convert to flux at 550nm (5.5e-5 cm)
        return self.photons_to_flux(photons, 5.5e-5)

    def get_noise(self) -> float:
        """RMS noise in erg/s/cm^2."""
        # Convert read noise to flux
        return self.photons_to_flux(self.read_noise, 5.5e-5)

    def get_area_cm2(self) -> float:
        """CCD area in cm^2."""
        return self.area

class InfraredArray(ScientificDetector):
    """IR array implementation with CGS units."""

    def __init__(self, area_cm2=1.0):
        self.area = area_cm2  # smaller pixels for IR
        self.dark_current = 0.1  # e-/s at 77K

    def read_frame(self) -> np.ndarray:
        """Read IR frame at 2.2 microns."""
        # IR arrays have different noise characteristics
        signal = np.random.randn(256, 256) * 10 + 100
        # Convert to flux at 2.2 microns (2.2e-4 cm)
        return self.photons_to_flux(signal, 2.2e-4)

    def get_noise(self) -> float:
        """Dark current noise in erg/s/cm^2."""
        return self.photons_to_flux(self.dark_current, 2.2e-4)

    def get_area_cm2(self) -> float:
        return self.area

# Process any detector uniformly
def calculate_sensitivity(detector: ScientificDetector) -> float:
    """Calculate sensitivity for any detector in erg/s/cm^2."""
    signal = detector.read_frame()
    noise = detector.get_noise()
    area = detector.get_area_cm2()

    # Signal-to-noise ratio calculation
    snr = np.mean(signal) / noise if noise > 0 else 0
    sensitivity = noise * 3 / area  # 3-sigma detection limit

    return sensitivity

# Works with ANY detector implementing the interface!
ccd = CCDDetector(area_cm2=4.0)
ir = InfraredArray(area_cm2=1.0)

print(f"CCD sensitivity: {calculate_sensitivity(ccd):.2e} erg/s/cm^3")
print(f"IR sensitivity: {calculate_sensitivity(ir):.2e} erg/s/cm^3")
```

:::{note} The More You Know: How ABCs Enabled Multi-Site Scientific Collaboration

In large-scale scientific projects, abstract base classes solve a critical coordination problem. When multiple research sites produce data with completely different hardware, data formats, and recording systems, early integration attempts often fail - code written for one instrument crashes with another's data.

The breakthrough comes when teams define abstract interfaces that each data source must implement:

```python
class DataStation(ABC):
    @abstractmethod
    def get_measurement(self, time, parameter):
        """Return measurement value at specified time."""
        pass

    @abstractmethod
    def get_calibration(self, data):
        """Apply site-specific calibration."""
        pass
```

Each site team can implement these methods however they need. Some implementations might be 5,000 lines handling complex multi-sensor arrays. Simple single-sensor stations might be just 500 lines. But the processing pipeline doesn't care - it just calls `get_measurement()` and trusts each station to handle the details.

This abstraction proves critical when problems are discovered. If one station's calibration is drifting, developers only fix that station's implementation. The rest of the pipeline, processing vast amounts of data, continues running without modification.

It's the same pattern you're learning, applied to enable scientific discoveries through collaboration across incompatible systems!
:::

### Advanced ABC Patterns with NumPy Integration

```python
from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

class SpectralAnalyzer(ABC):
    """Advanced ABC using NumPy arrays and CGS units."""

    @property
    @abstractmethod
    def wavelength_range_cm(self) -> Tuple[float, float]:
        """Wavelength coverage in cm."""
        pass

    @abstractmethod
    def find_peaks(self, flux: np.ndarray,
                   threshold_sigma: float = 3.0) -> np.ndarray:
        """Find emission peaks in flux [erg/s/cm^2/cm].

        Returns wavelengths in cm of detected peaks.
        """
        pass

    def flux_to_photons(self, flux_cgs, wavelength_cm):
        """Convert flux to photon rate using CGS units.

        flux: erg/s/cm^2/cm
        returns: photons/s/cm^2/cm
        """
        h = 6.626e-27  # erg*s
        c = 2.998e10   # cm/s
        return flux_cgs * wavelength_cm / (h * c)

class OpticalSpectrograph(SpectralAnalyzer):
    """Optical spectrograph with CGS units."""

    @property
    def wavelength_range_cm(self):
        # 380-750 nm in cm
        return (3.8e-5, 7.5e-5)

    def find_peaks(self, flux, threshold_sigma=3.0):
        """Find emission peaks using median filtering."""
        # Simple peak finding with NumPy
        median = np.median(flux)
        std = np.std(flux)
        peaks = np.where(flux > median + threshold_sigma * std)[0]

        # Convert indices to wavelengths in cm
        wave_start, wave_end = self.wavelength_range_cm
        wavelengths = np.linspace(wave_start, wave_end, len(flux))

        return wavelengths[peaks]

# Using the abstract interface with NumPy
spectrograph = OpticalSpectrograph()
mock_flux = np.random.randn(1000) * 1e-12 + 5e-12  # erg/s/cm^2/cm
lines = spectrograph.find_peaks(mock_flux)
print(f"Found {len(lines)} emission peaks")
print(f"Wavelength range: {spectrograph.wavelength_range_cm} cm")
```

:::{note} Check Your Understanding
:class: dropdown

Why does NumPy's `np.asarray()` work with so many different input types (lists, tuples, other arrays)? How do ABCs enable this?

**Answer:**

NumPy uses the Array API protocol (similar to an ABC) that defines what methods an object needs to be "array-like". Any object implementing `__array__()` or `__array_interface__` can be converted to a NumPy array.

This is why you can do:
- `np.asarray([1,2,3])` - lists work
- `np.asarray((1,2,3))` - tuples work
- `np.asarray(pandas_series)` - Pandas objects work

Each of these types implements the array protocol differently, but NumPy doesn't care about the implementation - just that the required methods exist. This is ABC-based design enabling the entire scientific Python ecosystem to interoperate!
:::

## 10.2 Multiple Inheritance and Mixins

:::{margin}
**Mixin**
A class providing specific functionality to be inherited by other classes, not meant to stand alone.
:::

:::{margin}
**Diamond Problem**
When a class inherits from two classes that share a common base, creating ambiguity in method resolution.
:::

You've seen matplotlib axes that can plot lines, scatter points, histograms, images, and dozens of other visualizations. How does one class have so many capabilities without becoming a 10,000-line monster? The answer is mixins.

```python
# First, understand the diamond problem you've seen in NumPy
class Array:
    def sum(self): return "Array.sum"

class MaskedArray(Array):
    def sum(self): return "MaskedArray.sum"

class SparseArray(Array):
    def sum(self): return "SparseArray.sum"

class MaskedSparseArray(MaskedArray, SparseArray):
    pass  # Which sum() method?

# Method Resolution Order (MRO) solves this
msa = MaskedSparseArray()
print(f"Calls: {msa.sum()}")  # MaskedArray.sum (first parent)
print(f"MRO: {[c.__name__ for c in MaskedSparseArray.__mro__]}")
```

Now let's build an instrument control system using mixins with proper CGS units:

```python
import time
import numpy as np

# Mixins provide specific, reusable functionality
class PositioningMixin:
    """Add positioning capability."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_position = 0.0  # cm
        self.y_position = 0.0  # cm

    def move_to(self, x_cm, y_cm):
        """Move to coordinates in cm."""
        self.x_position = x_cm
        self.y_position = y_cm

    def get_distance_from_origin(self):
        """Calculate distance from origin in cm."""
        return np.sqrt(self.x_position**2 + self.y_position**2)

class PhotometryMixin:
    """Add photometric capability with CGS flux units."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_width_cm = 1e-5  # 100 nm default

    def counts_to_flux(self, counts, exposure_s, area_cm2):
        """Convert counts to flux in erg/s/cm^2/Hz.

        Assumes optical wavelength 550 nm = 5.5e-5 cm
        """
        wavelength_cm = 5.5e-5
        c = 2.998e10  # cm/s
        h = 6.626e-27  # erg*s

        # Photon energy
        energy_per_photon = h * c / wavelength_cm

        # Flux in erg/s/cm^2
        flux = counts * energy_per_photon / (exposure_s * area_cm2)

        # Convert to per Hz (nu = c/lambda)
        freq_hz = c / wavelength_cm
        bandwidth_hz = c * self.filter_width_cm / wavelength_cm**2

        return flux / bandwidth_hz

class SpectroscopyMixin:
    """Add spectroscopic capability."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolution = 1000  # R = lambda/Deltalambda

    def velocity_shift_cm_per_s(self, obs_wavelength_cm,
                                rest_wavelength_cm):
        """Calculate velocity shift in cm/s using Doppler formula.

        v = c * (lambda_obs - lambda_rest) / lambda_rest
        """
        c = 2.998e10  # cm/s
        return c * (obs_wavelength_cm - rest_wavelength_cm) / rest_wavelength_cm

# Base instrument class
class Instrument:
    """Base instrument with aperture in cm."""

    def __init__(self, name, aperture_cm):
        super().__init__()  # Important for mixin chain!
        self.name = name
        self.aperture_cm = aperture_cm

    def collecting_area(self):
        """Collecting area in cm^2."""
        return np.pi * (self.aperture_cm / 2)**2

# Combine mixins to create specialized instruments
class ImagingInstrument(Instrument, PositioningMixin, PhotometryMixin):
    """Imaging instrument with positioning and photometry."""
    pass

class SpectroscopicInstrument(Instrument, PositioningMixin, SpectroscopyMixin):
    """Instrument with spectrograph."""
    pass

class MultiModeInstrument(Instrument, PositioningMixin,
                          PhotometryMixin, SpectroscopyMixin):
    """Instrument with all capabilities."""
    pass

# Create instruments with different capabilities
imaging = ImagingInstrument("Imager", 10)  # 10 cm aperture
imaging.move_to(x_cm=5.0, y_cm=10.0)

# Photometry-specific methods available
flux = imaging.counts_to_flux(counts=10000, exposure_s=30,
                              area_cm2=imaging.collecting_area())
print(f"Flux: {flux:.2e} erg/s/cm^2/Hz")

# Spectroscopic instrument has different methods
spectro = SpectroscopicInstrument("Spectrograph", 20)  # 20 cm
velocity = spectro.velocity_shift_cm_per_s(
    obs_wavelength_cm=6.565e-5,  # observed
    rest_wavelength_cm=6.563e-5  # rest
)
print(f"Velocity: {velocity/1e5:.1f} km/s")  # Convert to km/s for display
```

:::{note} The More You Know: How Mixins Orchestrate Large-Scale Physics Experiments

At major physics laboratories, massive detectors produce different data types from millions of events per second. Original monolithic code often becomes unmaintainable. Every detector class can exceed 10,000 lines with massive duplication.

The solution is refactoring to mixins. The problem: detectors share some capabilities but not others. Some need particle tracking. Others specialize in different phenomena. All need precise timing. Traditional inheritance would create bizarre hierarchies or duplicate code.

The elegant solution uses mixins:

```python
class ParticleTrackingMixin:
    def reconstruct_momentum(self, hits):
        """Track particles through detector, return momentum."""
        # Complex reconstruction algorithm
        pass

class CalorimeterMixin:
    def measure_energy(self, cells):
        """Measure energy deposition."""
        # Energy measurement algorithm
        pass

class PrecisionTimingMixin:
    def get_event_time(self, time_ns):
        """Identify precise event timing."""
        pass

# Each detector picks its capabilities
class DetectorTypeA(Detector, ParticleTrackingMixin, CalorimeterMixin,
                    PrecisionTimingMixin, JetReconstructionMixin):
    pass

class DetectorTypeB(Detector, CalorimeterMixin, PrecisionTimingMixin,
                    SpecialAnalysisMixin):  # Different capabilities
    pass
```

This design proves its worth during discoveries. When unusual signatures appear, new analysis mixins can be created and added to detectors in days instead of months.

When you use mixins, you're using patterns that enable major scientific discoveries!
:::

:::{tip} Computational Thinking Box: Composition vs Inheritance

**PATTERN: Choosing Between Inheritance, Mixins, and Composition**

After using NumPy and Matplotlib, you've seen all three patterns:

**Inheritance (IS-A)**: "MaskedArray IS-A ndarray"
```python
class ma.MaskedArray(np.ndarray):  # NumPy's actual design
    pass
```

**Mixin (CAN-DO)**: "Axes CAN-DO plotting methods"
```python
class Axes(Artist, _AxesBase):  # Matplotlib's actual design
    # Inherits from mixins providing different capabilities
    pass
```

**Composition (HAS-A)**: "Figure HAS-A list of Axes"
```python
class Figure:
    def __init__(self):
        self.axes = []  # Composition - Figure contains Axes
```

**Decision Framework**:

- Use inheritance for true specialization (rare)
- Use mixins for orthogonal capabilities (common)
- Use composition for complex relationships (very common)
- When in doubt, prefer composition

Real NumPy example: Structured arrays use composition (array HAS-A dtype), not inheritance!
:::

## 10.3 Dataclasses: Modern Python for Scientific Data

:::{margin}
**Dataclass**
A decorator that automatically generates special methods for classes primarily storing data.
:::

Python 3.7 introduced dataclasses, which eliminate boilerplate for data-heavy scientific classes. You've been writing `__init__`, `__repr__`, and `__eq__` manually - dataclasses generate them automatically.

```python
from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np

# Before dataclasses - lots of boilerplate
class OldStyleMeasurement:
    def __init__(self, target: str, x_pos: float, y_pos: float,
                 exposure_s: float, temperature: float,
                 flux_cgs: Optional[float] = None):
        self.target = target
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.exposure_s = exposure_s
        self.temperature = temperature
        self.flux_cgs = flux_cgs

    def __repr__(self):
        return (f"OldStyleMeasurement(target={self.target}, "
                f"x_pos={self.x_pos}, ...)")

    def __eq__(self, other):
        return (self.target == other.target and
                self.x_pos == other.x_pos and ...)

# With dataclasses - automatic and clean!
@dataclass
class Measurement:
    """Scientific measurement with automatic methods."""
    target: str
    x_pos: float
    y_pos: float
    exposure_s: float
    temperature: float
    flux_cgs: Optional[float] = None  # erg/s/cm^2

    def __post_init__(self):
        """Validate after auto-generated __init__."""
        if self.exposure_s <= 0:
            raise ValueError(f"Exposure {self.exposure_s} must be positive")
        if self.temperature < 0:
            raise ValueError(f"Temperature {self.temperature} below 0 K")

    def signal_to_noise(self) -> float:
        """Estimate SNR based on exposure time."""
        # Simple SNR estimate: SNR ~ sqrt(exposure)
        return np.sqrt(self.exposure_s)

# Automatic __init__, __repr__, __eq__ and more!
meas = Measurement(
    target="Sample A",
    x_pos=10.5,
    y_pos=20.3,
    exposure_s=300,
    temperature=293.0,
    flux_cgs=1.5e-12
)

print(meas)  # Nice automatic __repr__
print(f"Estimated SNR: {meas.signal_to_noise():.1f}")
```

### Advanced Dataclass Features for Scientific Computing

```python
from __future__ import annotations  # Enables forward references
from dataclasses import dataclass, field, asdict
import numpy as np
from typing import ClassVar, Optional

@dataclass
class SpectralLine:
    """Spectral line with CGS units and validation."""

    # Class variable (shared by all instances)
    c_cgs: ClassVar[float] = 2.998e10  # cm/s

    # Instance variables with types
    wavelength_cm: float
    flux_cgs: float  # erg/s/cm^2
    width_cm: float
    name: str = "Unknown"

    # Computed field with default_factory
    measurements: List[float] = field(default_factory=list)

    # Field with metadata
    snr: float = field(default=0.0, metadata={"unit": "dimensionless"})

    def __post_init__(self):
        """Calculate SNR after initialization."""
        if self.flux_cgs > 0 and self.width_cm > 0:
            # Simple SNR estimate
            self.snr = self.flux_cgs / (self.width_cm * 1e-13)

    @property
    def velocity_width_km_s(self) -> float:
        """Line width in velocity space (km/s)."""
        return (self.width_cm / self.wavelength_cm) * self.c_cgs / 1e5

    @property
    def frequency_hz(self) -> float:
        """Frequency in Hz."""
        return self.c_cgs / self.wavelength_cm

# Create spectral line
line = SpectralLine(
    wavelength_cm=6.563e-5,
    flux_cgs=1e-13,
    width_cm=1e-7,
    name="H-alpha"
)

print(f"H-alpha: {line.frequency_hz:.2e} Hz")
print(f"Velocity width: {line.velocity_width_km_s:.1f} km/s")
print(f"SNR: {line.snr:.1f}")

# Convert to dictionary (useful for saving)
line_dict = asdict(line)
print(f"As dict: {line_dict}")

# Frozen (immutable) dataclass for constants
@dataclass(frozen=True)
class PhysicalConstants:
    """Immutable physical constants in CGS."""
    c: float = 2.998e10      # cm/s
    h: float = 6.626e-27     # erg*s
    k: float = 1.381e-16     # erg/K
    m_e: float = 9.109e-28   # g
    m_p: float = 1.673e-24   # g

    def photon_energy(self, wavelength_cm: float) -> float:
        """Photon energy in ergs."""
        return self.h * self.c / wavelength_cm

# Constants are immutable
constants = PhysicalConstants()
# constants.c = 3e10  # This would raise FrozenInstanceError
print(f"Photon at 550nm: {constants.photon_energy(5.5e-5):.2e} erg")
```

:::{important} Why This Matters: Dataclasses in Scientific Python

Dataclasses dramatically reduce boilerplate in scientific code. Here's a real comparison:

```python
# Traditional class - lots of boilerplate
class DataPoint:
    def __init__(self, name, x, y, value, uncertainty):
        self.name = name
        self.x = x
        self.y = y
        self.value = value
        self.uncertainty = uncertainty

    def __repr__(self):
        return (f"DataPoint(name={self.name!r}, x={self.x}, "
                f"y={self.y}, value={self.value}, "
                f"uncertainty={self.uncertainty})")

    def __eq__(self, other):
        if not isinstance(other, DataPoint):
            return NotImplemented
        return (self.name == other.name and
                self.x == other.x and
                self.y == other.y and
                self.value == other.value and
                self.uncertainty == other.uncertainty)

# With dataclass - clean and automatic!
@dataclass
class DataPoint:
    name: str
    x: float
    y: float
    value: float
    uncertainty: float
    # __init__, __repr__, __eq__ all generated automatically!
```

Benefits in scientific computing:

- Type hints make scientific APIs self-documenting
- `asdict()` simplifies data export to JSON/HDF5
- `frozen=True` ensures immutability for coordinate systems
- Less code means fewer bugs in data structures

Many modern scientific Python packages are adopting dataclasses for their clarity and reduced maintenance burden. You're learning patterns that represent the future direction of scientific Python!
:::

## 10.4 Asynchronous Programming for Instrument Control

:::{margin}
**Async/Await**
Python's syntax for asynchronous programming, allowing concurrent operations without threads.
:::

:::{margin}
**Coroutine**
A function that can pause and resume execution, enabling cooperative multitasking.
:::

Modern scientific facilities control multiple instruments simultaneously. While one sensor reads out (30 seconds), you can move a stage (10 seconds) and configure another instrument (5 seconds). Async programming enables this parallelism.

```python
import asyncio
import time
import numpy as np

# Synchronous version - everything waits
def sync_measure(target: str) -> dict:
    """Traditional blocking measurement."""
    print(f"Starting measurement of {target}")

    # Each step blocks
    print("Moving stage...")
    time.sleep(2)  # Simulate 2 second move

    print("Acquiring data...")
    time.sleep(3)  # Simulate 3 second acquisition

    print("Processing...")
    time.sleep(1)  # Simulate 1 second processing

    return {"target": target, "counts": 1000}

# Time the synchronous version
start = time.perf_counter()
result = sync_measure("Sample A")
sync_time = time.perf_counter() - start
print(f"Synchronous time: {sync_time:.1f}s\n")
```

Now the asynchronous version:

```python
# Asynchronous version - operations can overlap
async def move_stage(x_cm: float, y_cm: float):
    """Async stage movement."""
    print(f"Moving to x={x_cm:.1f}, y={y_cm:.1f}")
    await asyncio.sleep(2)  # Non-blocking sleep
    print("Move complete")
    return True

async def acquire_data(integration_s: float):
    """Async data acquisition."""
    print(f"Starting {integration_s}s acquisition")
    await asyncio.sleep(3)  # Simulated acquisition

    # Generate mock data in CGS units
    counts = np.random.poisson(1000, size=(100, 100))
    flux_cgs = counts * 3.6e-12  # erg/s/cm^2

    print("Acquisition complete")
    return flux_cgs

async def configure_detector(gain: int):
    """Async detector configuration."""
    print(f"Configuring detector gain={gain}")
    await asyncio.sleep(1)
    print("Detector ready")
    return gain

async def async_measure(target: str, x: float, y: float):
    """Parallel measurement with multiple operations."""
    print(f"Starting async measurement of {target}")

    # Launch operations concurrently!
    tasks = [
        move_stage(x, y),
        acquire_data(30.0),
        configure_detector(100)
    ]

    # Wait for all to complete
    results = await asyncio.gather(*tasks)

    return {
        "target": target,
        "positioned": results[0],
        "flux": results[1].mean(),
        "gain": results[2]
    }

# Run async version
async def main():
    start = time.perf_counter()
    result = await async_measure("Sample A", 10.0, 20.0)
    async_time = time.perf_counter() - start

    print(f"\nAsync time: {async_time:.1f}s")
    print(f"Speedup: {sync_time/async_time:.1f}x")
    print(f"Mean flux: {result['flux']:.2e} erg/s/cm^2")

# Note: In Jupyter, use await directly
# In scripts, use asyncio.run(main())
await main()
```

### Real-World Async Instrument Control

```python
from dataclasses import dataclass
from typing import List, Optional
import asyncio

# Note: In Jupyter notebooks, use 'await' directly in cells
# In Python scripts, use asyncio.run(main())
# Some Jupyter versions may require nest_asyncio:
# import nest_asyncio
# nest_asyncio.apply()

@dataclass
class InstrumentState:
    """Current instrument state."""
    x_pos: float = 0.0
    y_pos: float = 0.0
    filter: str = "open"
    focus_mm: float = 0.0
    temperature_k: float = 293.0

class AsyncInstrument:
    """Async instrument controller with realistic operations."""

    def __init__(self, name: str):
        self.name = name
        self.state = InstrumentState()
        self.is_active = False

    async def move_to(self, x: float, y: float) -> float:
        """Move to position, return time taken."""
        # Calculate move time based on distance
        distance = np.sqrt((x - self.state.x_pos)**2 +
                          (y - self.state.y_pos)**2)
        move_time = min(distance / 10.0, 30.0)  # 10 cm/s, max 30s

        print(f"{self.name}: Moving {distance:.1f} cm ({move_time:.1f}s)")
        await asyncio.sleep(move_time)

        self.state.x_pos = x
        self.state.y_pos = y
        self.is_active = True

        return move_time

    async def change_filter(self, filter_name: str):
        """Change filter wheel."""
        if filter_name != self.state.filter:
            print(f"{self.name}: Changing to {filter_name} filter")
            await asyncio.sleep(5.0)  # Filter wheel rotation
            self.state.filter = filter_name

    async def auto_focus(self) -> float:
        """Autofocus routine, return FWHM in arcsec."""
        print(f"{self.name}: Starting autofocus")

        best_focus = 0.0
        best_fwhm = float('inf')

        # Simulate focus sweep
        for focus in np.linspace(-2, 2, 5):
            await asyncio.sleep(1.0)  # Move focus

            # Simulate FWHM measurement
            fwhm = abs(focus) + np.random.random() + 0.8
            if fwhm < best_fwhm:
                best_fwhm = fwhm
                best_focus = focus

        self.state.focus_mm = best_focus
        print(f"{self.name}: Focus complete, FWHM={best_fwhm:.2f}")
        return best_fwhm

# Async measurement sequence
async def measure_samples(instrument: AsyncInstrument,
                          samples: List[tuple]):
    """Measure multiple samples efficiently."""

    for name, x, y, filter_name in samples:
        print(f"\n--- Measuring {name} ---")

        # Parallel operations where possible
        tasks = [
            instrument.move_to(x, y),
            instrument.change_filter(filter_name)
        ]

        # Move and filter change happen in parallel
        await asyncio.gather(*tasks)

        # Focus if needed (every 5 samples)
        if np.random.random() < 0.2:
            await instrument.auto_focus()

        # Simulate acquisition
        print(f"Acquiring {name} with {filter_name}")
        await asyncio.sleep(10.0)

        print(f"Completed {name}")

# Run measurement sequence
async def experiment_session():
    instrument = AsyncInstrument("Main Detector")

    samples = [
        ("Sample A", 10.0, 20.0, "blue"),
        ("Sample B", 50.0, 30.0, "red"),
        ("Sample C", 100.0, 50.0, "green"),
    ]

    start = time.perf_counter()
    await measure_samples(instrument, samples)
    total_time = time.perf_counter() - start

    print(f"\nTotal measurement time: {total_time:.1f}s")

await experiment_session()
```

:::{warning} Common Bug Alert: Mixing Sync and Async

```python
# WRONG - Blocking call in async function
async def bad_async():
    print("Starting")
    time.sleep(1)  # BLOCKS the event loop!
    print("Done")

# CORRECT - Use async sleep
async def good_async():
    print("Starting")
    await asyncio.sleep(1)  # Non-blocking
    print("Done")

# WRONG - Forgetting await
async def forgot_await():
    result = acquire_data(30)  # Returns coroutine object!
    # print(result)  # <coroutine object...>

# CORRECT - Use await
async def remembered_await():
    result = await acquire_data(30)  # Actually runs
    print(f"Got flux: {result.mean():.2e}")
```

Always use `await` with async functions and never use blocking calls in async code!
:::

## 10.5 Metaclasses and Descriptors

:::{margin}
**Metaclass**
A class whose instances are classes themselves, controlling class creation.
:::

:::{margin}
**Descriptor**
An object that customizes attribute access through `__get__` and `__set__` methods.
:::

Now that you've seen how NumPy dtypes work and how unit-aware libraries prevent disasters, let's understand the metaclasses and descriptors that make them possible.

```python
# Descriptors for unit-safe computations
class UnitProperty:
    """Descriptor ensuring CGS units are maintained."""

    def __init__(self, unit_name: str, cgs_conversion: float = 1.0,
                 min_val: Optional[float] = None):
        self.unit_name = unit_name
        self.cgs_conversion = cgs_conversion
        self.min_val = min_val

    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to class."""
        self.name = f"_{name}"
        self.public_name = name

    def __get__(self, obj, objtype=None):
        """Get value in CGS units."""
        if obj is None:
            return self
        return getattr(obj, self.name, None)

    def __set__(self, obj, value):
        """Set value with validation and conversion."""
        # Handle tuple of (value, unit)
        if isinstance(value, tuple):
            val, unit = value
            if unit != self.unit_name:
                # Convert to CGS
                if unit == "km" and self.unit_name == "cm":
                    val *= 1e5
                elif unit == "m" and self.unit_name == "cm":
                    val *= 100
                else:
                    raise ValueError(f"Cannot convert {unit} to {self.unit_name}")
        else:
            val = value

        # Validate
        if self.min_val is not None and val < self.min_val:
            raise ValueError(f"{self.public_name} = {val} below minimum {self.min_val}")

        setattr(obj, self.name, val)

class PhysicalObject:
    """Object with unit-safe properties."""

    # Descriptors enforce CGS units
    distance = UnitProperty("cm", min_val=0)
    mass = UnitProperty("g", min_val=0)
    radius = UnitProperty("cm", min_val=0)
    temperature = UnitProperty("K", min_val=0)

    def __init__(self, name: str):
        self.name = name

    @property
    def escape_velocity_cm_s(self) -> float:
        """Escape velocity in cm/s."""
        if self.mass and self.radius:
            G = 6.674e-8  # cm^3/g/s^2
            return np.sqrt(2 * G * self.mass / self.radius)
        return 0.0

# Unit-safe usage
earth = PhysicalObject("Earth")
earth.distance = (1.496e8, "km")  # Converts to cm automatically
earth.mass = 5.972e27  # grams
earth.radius = (6371, "km")  # Converts to cm

print(f"Earth distance: {earth.distance:.2e} cm")
print(f"Earth radius: {earth.radius:.2e} cm")
print(f"Escape velocity: {earth.escape_velocity_cm_s/1e5:.1f} km/s")
```

### Metaclasses for Automatic Registration

```python
# Metaclass for instrument registry (like many scientific libraries)
class InstrumentMeta(type):
    """Metaclass that auto-registers instruments."""

    _registry = {}

    def __new__(mcs, name, bases, namespace):
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)

        # Register if it has instrument_code
        if 'instrument_code' in namespace:
            code = namespace['instrument_code']
            mcs._registry[code] = cls
            print(f"Registered {name} as '{code}'")

        return cls

    @classmethod
    def create(mcs, code: str, **kwargs):
        """Factory method using registry."""
        if code not in mcs._registry:
            available = list(mcs._registry.keys())
            raise ValueError(f"Unknown instrument '{code}'. "
                           f"Available: {available}")
        return mcs._registry[code](**kwargs)

    @classmethod
    def list_instruments(mcs):
        """List all registered instruments."""
        return list(mcs._registry.keys())

class Instrument(metaclass=InstrumentMeta):
    """Base class with metaclass."""

    def __init__(self, **config):
        self.config = config

# Classes auto-register on definition!
class Spectrometer(Instrument):
    """UV-Vis Spectrometer."""
    instrument_code = "UV-VIS"

    def __init__(self, mode="absorbance", **config):
        super().__init__(**config)
        self.mode = mode  # absorbance or fluorescence

class MassSpec(Instrument):
    """Mass Spectrometer."""
    instrument_code = "MS"

    def __init__(self, ionization="ESI", **config):
        super().__init__(**config)
        self.ionization = ionization

class NMR(Instrument):
    """NMR Spectrometer."""
    instrument_code = "NMR"

    def __init__(self, frequency_mhz=400, **config):
        super().__init__(**config)
        self.frequency = frequency_mhz

# Use the registry
print(f"Available: {InstrumentMeta.list_instruments()}")

# Create instruments by code
ms = InstrumentMeta.create("MS", ionization="MALDI")
nmr = InstrumentMeta.create("NMR")

print(f"Created {ms.__class__.__name__} with {ms.ionization} ionization")
print(f"NMR frequency: {nmr.frequency} MHz")
```

:::{note} Check Your Understanding
:class: dropdown

How do NumPy arrays know which operations they support? How can `arr + 1` and `arr + another_array` both work?

**Answer:**

NumPy uses a combination of metaclasses and descriptors:

1. **Metaclass Registration**: When you create array subclasses, NumPy's metaclass registers which operations they support

2. **Descriptor Protocol**: Operations like `+` call `__add__`, which uses descriptors to check if the operation is valid

3. **Dynamic Dispatch**: Based on the types involved, NumPy dispatches to the appropriate implementation

This is why:
- `np.array([1,2,3]) + 1` broadcasts the scalar
- `np.array([1,2,3]) + np.array([4,5,6])` adds element-wise
- `np.array([1,2,3]) + "string"` raises TypeError

The same patterns you just learned power NumPy's flexibility!
:::

## 10.6 Design Patterns from Scientific Computing

:::{margin}
**Design Pattern**
A reusable solution to a commonly occurring problem in software design.
:::

You've used these patterns throughout NumPy and Matplotlib. Now let's understand how they work.

### Factory Pattern: Creating the Right Object

```python
# How NumPy's array creation works (simplified)
class ArrayFactory:
    """Factory pattern like np.array()."""

    @staticmethod
    def create(data, dtype=None):
        """Create appropriate array type based on input."""

        # Determine appropriate array type
        if hasattr(data, '__array__'):
            # Object provides array interface
            return np.asarray(data)

        elif isinstance(data, (list, tuple)):
            # Python sequence
            if dtype == 'object':
                return ObjectArray(data)
            else:
                return NumericArray(data)

        elif isinstance(data, str):
            # String array
            return StringArray(data)

        else:
            raise TypeError(f"Cannot create array from {type(data)}")

class NumericArray:
    def __init__(self, data):
        self.data = list(data)
        print(f"Created numeric array: {self.data}")

class ObjectArray:
    def __init__(self, data):
        self.data = data
        print(f"Created object array: {self.data}")

class StringArray:
    def __init__(self, data):
        self.data = data
        print(f"Created string array: {self.data}")

# Factory creates appropriate type
arr1 = ArrayFactory.create([1, 2, 3])
arr2 = ArrayFactory.create(['a', 'b'], dtype='object')
arr3 = ArrayFactory.create("hello")
```

### Strategy Pattern: Swappable Algorithms

```python
from abc import ABC, abstractmethod

# How scipy.optimize works (simplified)
class OptimizationStrategy(ABC):
    """Abstract strategy for optimization."""

    @abstractmethod
    def minimize(self, func, x0):
        """Minimize function starting from x0."""
        pass

class GradientDescent(OptimizationStrategy):
    """Gradient descent optimization."""

    def minimize(self, func, x0):
        x = x0
        learning_rate = 0.01

        for i in range(100):
            # Numerical gradient
            eps = 1e-8
            grad = (func(x + eps) - func(x - eps)) / (2 * eps)
            x = x - learning_rate * grad

            if abs(grad) < 1e-6:
                break

        return x

class NelderMead(OptimizationStrategy):
    """Simplex optimization (gradient-free)."""

    def minimize(self, func, x0):
        # Simplified Nelder-Mead
        x = x0
        step = 0.1

        for i in range(100):
            # Try points around current
            if func(x + step) < func(x):
                x = x + step
            elif func(x - step) < func(x):
                x = x - step
            else:
                step *= 0.5

        return x

class Optimizer:
    """Context using strategy pattern."""

    def __init__(self, strategy: OptimizationStrategy):
        self.strategy = strategy

    def minimize(self, func, x0):
        """Minimize using selected strategy."""
        return self.strategy.minimize(func, x0)

# Test with rosenbrock function
def rosenbrock(x):
    """Rosenbrock function minimum at x=1."""
    return (1 - x)**2 + 100 * (0 - x**2)**2

# Try different strategies
opt1 = Optimizer(GradientDescent())
result1 = opt1.minimize(rosenbrock, x0=0.5)
print(f"Gradient descent: x = {result1:.4f}")

opt2 = Optimizer(NelderMead())
result2 = opt2.minimize(rosenbrock, x0=0.5)
print(f"Nelder-Mead: x = {result2:.4f}")
```

:::{important} Why This Matters: Design Patterns in SciPy

SciPy uses these exact patterns. When you write:

```python
from scipy import optimize
result = optimize.minimize(func, x0, method='BFGS')
```

You're using:

- **Factory Pattern**: `minimize` creates the right optimizer
- **Strategy Pattern**: 'BFGS' selects the algorithm
- **Template Method**: Each optimizer follows the same interface

This design lets you swap between 20+ optimization algorithms by changing one parameter!
:::

## 10.7 Performance Optimization Techniques

:::{margin}
**\_\_slots\_\_**
Class attribute that restricts instance attributes to a fixed set, saving memory.
:::

Understanding performance helps you write efficient code for large-scale scientific data processing.

```python
import sys
import time
from functools import lru_cache

# Memory optimization with __slots__
class RegularDataPoint:
    """Normal class - flexible but memory-hungry."""

    def __init__(self, x, y, value, uncertainty):
        self.x = x  # position
        self.y = y  # position
        self.value = value  # measurement
        self.uncertainty = uncertainty  # error

class OptimizedDataPoint:
    """Using __slots__ for memory efficiency."""

    __slots__ = ['x', 'y', 'value', 'uncertainty', '_derived_cache']

    def __init__(self, x, y, value, uncertainty):
        self.x = x
        self.y = y
        self.value = value
        self.uncertainty = uncertainty
        self._derived_cache = None

    @property
    def snr(self):
        """Signal-to-noise ratio (cached)."""
        if self._derived_cache is None:
            if self.uncertainty > 0:
                self._derived_cache = self.value / self.uncertainty
            else:
                self._derived_cache = float('inf')
        return self._derived_cache

# Compare memory usage
regular = RegularDataPoint(10.0, 20.0, 1.5e-12, 1e-13)
optimized = OptimizedDataPoint(10.0, 20.0, 1.5e-12, 1e-13)

print(f"Regular: {sys.getsizeof(regular.__dict__)} bytes")
print(f"Optimized: {sys.getsizeof(optimized)} bytes")

# For large datasets, the difference matters!
n_points = 100000  # Subset for demo
regular_mem = n_points * sys.getsizeof(regular.__dict__)
optimized_mem = n_points * 56  # Approximate slotted size

print(f"\n{n_points:,} points:")
print(f"Regular: {regular_mem/1e6:.1f} MB")
print(f"Optimized: {optimized_mem/1e6:.1f} MB")
print(f"Savings: {(regular_mem-optimized_mem)/1e6:.1f} MB")
```

### Method Caching for Expensive Computations

```python
# LRU cache for expensive calculations
class Spectrum:
    """Spectrum with expensive computations."""

    def __init__(self, wavelengths_cm, fluxes_cgs):
        self.wavelengths = wavelengths_cm  # cm
        self.fluxes = fluxes_cgs  # erg/s/cm^2/cm

    @lru_cache(maxsize=128)
    def find_shift(self, template_lines_cm):
        """Find wavelength shift by template matching (expensive)."""
        print("Computing shift...")  # Shows when cache misses

        # Simplified cross-correlation
        best_shift = 0.0
        best_corr = -float('inf')

        for shift in np.linspace(-1e-6, 1e-6, 100):
            # Shift template lines
            shifted = [line + shift for line in template_lines_cm]

            # Simple correlation metric
            corr = sum(1 for line in shifted
                      if any(abs(line - w) < 1e-7
                            for w in self.wavelengths))

            if corr > best_corr:
                best_corr = corr
                best_shift = shift

        return best_shift

    def velocity_km_s(self, template_lines_cm):
        """Velocity from cached shift."""
        shift = self.find_shift(template_lines_cm)
        c_km_s = 2.998e5
        # v = c * Deltalambda/lambda
        return c_km_s * shift / template_lines_cm[0]

# Test caching
wavelengths = np.linspace(4e-5, 7e-5, 1000)  # 400-700 nm in cm
fluxes = np.random.randn(1000) * 1e-13

spectrum = Spectrum(wavelengths, fluxes)

# Reference lines in cm
ref_lines = tuple([4.861e-5, 6.563e-5])

# First call - computes
shift1 = spectrum.find_shift(ref_lines)
print(f"Shift: {shift1:.4e} cm")

# Second call - cached!
shift2 = spectrum.find_shift(ref_lines)
print(f"Cached: {shift2:.4e} cm")

# Cache info
print(f"Cache stats: {spectrum.find_shift.cache_info()}")
```

:::{tip} Computational Thinking Box: Profile Before Optimizing

**PATTERN: Measure, Don't Guess**

Large scientific pipelines process massive amounts of data nightly. Teams profile their pipelines and often find surprising bottlenecks:

```python
import cProfile
import pstats

def process_data(data):
    # Complex processing
    pass

# Profile the code
cProfile.run('process_data(data)', 'profile.stats')

# Analyze results
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 time consumers
```

Typical surprising results:

- 60% time in coordinate transformations (not core algorithms!)
- 20% in file I/O
- Only 10% in the actual analysis algorithm

One coordinate optimization can give 3x speedup for the entire pipeline!

**Lesson**: Always profile before optimizing. The bottleneck is rarely where you think.
:::

## 10.8 Practice Exercises

### Exercise 1: Build a Multi-Instrument Laboratory System

Create a complete laboratory system using ABCs, mixins, and async:

```python
"""
Part A: Abstract base and mixins (10 minutes)
Design flexible instrument system with CGS units
"""

from abc import ABC, abstractmethod
import asyncio
import numpy as np
from dataclasses import dataclass
from typing import Optional

# Abstract base for all instruments
class LabInstrument(ABC):
    """Base class for laboratory instruments."""

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize instrument."""
        pass

    @abstractmethod
    async def acquire(self, integration_s: float) -> np.ndarray:
        """Acquire data for given time."""
        pass

    @abstractmethod
    def get_sensitivity_cgs(self) -> float:
        """Return sensitivity in erg/s/cm^2."""
        pass

# Mixins for capabilities
class TemperatureControlMixin:
    """Temperature control for cooled instruments."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temperature_k = 293  # Room temp
        self.target_temp_k = 150  # Target for CCDs

    async def cool_down(self):
        """Cool to operating temperature."""
        print(f"Cooling from {self.temperature_k}K to {self.target_temp_k}K")

        while self.temperature_k > self.target_temp_k:
            await asyncio.sleep(0.1)  # Simulate cooling
            self.temperature_k -= 10

        print(f"Reached {self.temperature_k}K")
        return True

class CalibrationMixin:
    """Calibration capability."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dark_frame = None
        self.flat_frame = None

    async def take_dark(self, integration_s: float):
        """Take dark frame."""
        print(f"Taking {integration_s}s dark")
        await asyncio.sleep(integration_s)
        self.dark_frame = np.random.randn(100, 100) * 10

    async def take_flat(self):
        """Take flat field."""
        print("Taking flat field")
        await asyncio.sleep(1)
        self.flat_frame = np.ones((100, 100)) + np.random.randn(100, 100) * 0.01

# Concrete implementations
class CCDCamera(LabInstrument, TemperatureControlMixin,
                CalibrationMixin):
    """CCD camera with cooling and calibration."""

    def __init__(self, name: str, pixel_size_cm: float = 1.5e-3):
        super().__init__()
        self.name = name
        self.pixel_size = pixel_size_cm  # 15 microns typical
        self.initialized = False

    async def initialize(self) -> bool:
        """Initialize CCD with cooling."""
        print(f"Initializing {self.name}")

        # Cool down first
        await self.cool_down()

        # Take calibration frames
        await asyncio.gather(
            self.take_dark(1.0),
            self.take_flat()
        )

        self.initialized = True
        return True

    async def acquire(self, integration_s: float) -> np.ndarray:
        """Acquire CCD frame."""
        if not self.initialized:
            raise RuntimeError("CCD not initialized")

        print(f"Exposing for {integration_s}s")
        await asyncio.sleep(integration_s)

        # Simulate data with Poisson noise
        signal = np.random.poisson(1000 * integration_s, (100, 100))

        # Apply calibration if available
        if self.dark_frame is not None:
            signal = signal - self.dark_frame
        if self.flat_frame is not None:
            signal = signal / self.flat_frame

        # Convert to flux in erg/s/cm^2
        # Assume 550nm, QE=0.9
        h = 6.626e-27  # erg*s
        c = 2.998e10   # cm/s
        wavelength = 5.5e-5  # cm

        photon_energy = h * c / wavelength
        area_per_pixel = self.pixel_size**2

        flux_cgs = signal * photon_energy / (integration_s * area_per_pixel)

        return flux_cgs

    def get_sensitivity_cgs(self) -> float:
        """3-sigma sensitivity in erg/s/cm^2."""
        # Depends on temperature
        read_noise = 5 if self.temperature_k < 200 else 20

        # Convert to flux
        h = 6.626e-27
        c = 2.998e10
        photon_energy = h * c / 5.5e-5

        return 3 * read_noise * photon_energy / self.pixel_size**2

# Test the system
async def test_lab():
    ccd = CCDCamera("Main CCD", pixel_size_cm=1.5e-3)

    # Initialize (cooling + calibration)
    await ccd.initialize()

    # Take science frame
    data = await ccd.acquire(30.0)

    print(f"Mean flux: {data.mean():.2e} erg/s/cm^2")
    print(f"Sensitivity: {ccd.get_sensitivity_cgs():.2e} erg/s/cm^2")

await test_lab()
```

```python
"""
Part B: Complete laboratory with async control (15 minutes)
Multiple instruments operating in parallel
"""

@dataclass
class MeasurementRequest:
    """Request for measurement with units."""
    sample: str
    x_pos: float
    y_pos: float
    exposures_s: list
    filters: list
    priority: int = 5

class Laboratory:
    """Complete laboratory with multiple instruments."""

    def __init__(self, name: str):
        self.name = name
        self.instruments = {}
        self.queue = []
        self.completed = []

    def add_instrument(self, name: str, instrument: LabInstrument):
        """Register instrument."""
        self.instruments[name] = instrument

    async def initialize_all(self):
        """Initialize all instruments in parallel."""
        print(f"Initializing {self.name} laboratory")

        tasks = [
            inst.initialize()
            for inst in self.instruments.values()
        ]

        results = await asyncio.gather(*tasks)

        if all(results):
            print("All instruments ready")
        else:
            print("Some instruments failed initialization")

    async def measure(self, request: MeasurementRequest):
        """Execute measurement request."""
        print(f"\nMeasuring {request.sample}")

        results = {}

        for exp_time, filter_name in zip(request.exposures_s,
                                         request.filters):
            print(f"  {filter_name}: {exp_time}s")

            # Use primary CCD
            ccd = self.instruments.get('ccd')
            if ccd:
                data = await ccd.acquire(exp_time)
                results[filter_name] = {
                    'data': data,
                    'mean_flux': data.mean(),
                    'peak_flux': data.max()
                }

        self.completed.append((request.sample, results))
        return results

    async def process_queue(self):
        """Process measurement queue."""
        while self.queue:
            request = self.queue.pop(0)
            await self.measure(request)

    def add_request(self, request: MeasurementRequest):
        """Add to queue sorted by priority."""
        self.queue.append(request)
        self.queue.sort(key=lambda r: r.priority, reverse=True)

# Create and run laboratory
async def full_lab_demo():
    # Create laboratory
    lab = Laboratory("Main Lab")

    # Add instruments
    lab.add_instrument('ccd', CCDCamera("Primary CCD"))

    # Initialize everything
    await lab.initialize_all()

    # Queue measurements
    lab.add_request(MeasurementRequest(
        sample="Sample A",
        x_pos=10.0,
        y_pos=20.0,
        exposures_s=[30, 60, 60],
        filters=['blue', 'green', 'red'],
        priority=10
    ))

    lab.add_request(MeasurementRequest(
        sample="Calibration Standard",
        x_pos=0.0,
        y_pos=0.0,
        exposures_s=[5, 5],
        filters=['green', 'red'],
        priority=15  # Higher priority
    ))

    # Process queue (high priority first)
    await lab.process_queue()

    # Summary
    print(f"\nCompleted {len(lab.completed)} measurements")
    for sample, results in lab.completed:
        print(f"  {sample}: {list(results.keys())}")

await full_lab_demo()
```

### Exercise 2: Design Pattern Implementation

Implement key design patterns for scientific software:

```python
"""
Implement Factory, Strategy, and Observer patterns
for a data reduction pipeline
"""

from abc import ABC, abstractmethod
from typing import List, Callable
import numpy as np

# Strategy pattern for reduction algorithms
class ReductionStrategy(ABC):
    """Abstract strategy for data reduction."""

    @abstractmethod
    def reduce(self, data: np.ndarray) -> np.ndarray:
        """Reduce data using specific algorithm."""
        pass

class MedianCombine(ReductionStrategy):
    """Median combination strategy."""

    def reduce(self, data: np.ndarray) -> np.ndarray:
        """Median combine along first axis."""
        return np.median(data, axis=0)

class SigmaClipping(ReductionStrategy):
    """Sigma-clipped mean strategy."""

    def __init__(self, sigma: float = 3.0):
        self.sigma = sigma

    def reduce(self, data: np.ndarray) -> np.ndarray:
        """Sigma-clipped mean combination."""
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)

        # Mask outliers
        mask = np.abs(data - mean) < self.sigma * std

        # Recalculate with mask
        masked_data = np.where(mask, data, np.nan)
        return np.nanmean(masked_data, axis=0)

# Observer pattern for pipeline monitoring
class PipelineObserver(ABC):
    """Abstract observer for pipeline events."""

    @abstractmethod
    def update(self, event: str, data: dict):
        """Called when pipeline state changes."""
        pass

class LogObserver(PipelineObserver):
    """Logs pipeline events."""

    def update(self, event: str, data: dict):
        """Log the event."""
        print(f"[LOG] {event}: {data}")

class QualityObserver(PipelineObserver):
    """Monitors data quality."""

    def __init__(self):
        self.quality_metrics = []

    def update(self, event: str, data: dict):
        """Check quality metrics."""
        if event == "reduction_complete":
            result = data.get('result')
            if result is not None:
                snr = np.mean(result) / np.std(result)
                self.quality_metrics.append(snr)

                if snr < 10:
                    print(f"[QUALITY WARNING] Low SNR: {snr:.1f}")

# Factory pattern for pipeline creation
class PipelineFactory:
    """Factory for creating appropriate pipelines."""

    @staticmethod
    def create_pipeline(data_type: str) -> 'ReductionPipeline':
        """Create pipeline based on data type."""

        if data_type == "imaging":
            pipeline = ReductionPipeline()
            pipeline.set_strategy(MedianCombine())
            pipeline.attach(LogObserver())
            return pipeline

        elif data_type == "spectroscopy":
            pipeline = ReductionPipeline()
            pipeline.set_strategy(SigmaClipping(sigma=2.5))
            pipeline.attach(LogObserver())
            pipeline.attach(QualityObserver())
            return pipeline

        elif data_type == "photometry":
            pipeline = ReductionPipeline()
            pipeline.set_strategy(SigmaClipping(sigma=3.0))
            pipeline.attach(QualityObserver())
            return pipeline

        else:
            raise ValueError(f"Unknown data type: {data_type}")

# Main pipeline using all patterns
class ReductionPipeline:
    """Data reduction pipeline with patterns."""

    def __init__(self):
        self.strategy: Optional[ReductionStrategy] = None
        self.observers: List[PipelineObserver] = []

    def set_strategy(self, strategy: ReductionStrategy):
        """Set reduction strategy."""
        self.strategy = strategy
        self.notify("strategy_changed",
                   {"strategy": strategy.__class__.__name__})

    def attach(self, observer: PipelineObserver):
        """Attach observer."""
        self.observers.append(observer)

    def notify(self, event: str, data: dict):
        """Notify all observers."""
        for observer in self.observers:
            observer.update(event, data)

    def process(self, frames: np.ndarray) -> np.ndarray:
        """Process frames using current strategy."""
        if not self.strategy:
            raise RuntimeError("No reduction strategy set")

        self.notify("reduction_started", {"n_frames": len(frames)})

        # Apply strategy
        result = self.strategy.reduce(frames)

        self.notify("reduction_complete", {
            "result_shape": result.shape,
            "result": result
        })

        return result

# Demonstrate all patterns together
print("=== Design Patterns Demo ===\n")

# Create different pipelines using factory
imaging_pipeline = PipelineFactory.create_pipeline("imaging")
spectro_pipeline = PipelineFactory.create_pipeline("spectroscopy")

# Generate mock data
frames = np.random.randn(10, 100, 100) * 100 + 1000

# Process with different pipelines
print("Imaging Pipeline:")
imaging_result = imaging_pipeline.process(frames)

print("\nSpectroscopy Pipeline:")
spectro_result = spectro_pipeline.process(frames)

# Change strategy at runtime
print("\nChanging strategy at runtime:")
imaging_pipeline.set_strategy(SigmaClipping(sigma=2.0))
new_result = imaging_pipeline.process(frames)

print("\n Patterns demonstrated:")
print("  - Factory: Created specialized pipelines")
print("  - Strategy: Swappable reduction algorithms")
print("  - Observer: Monitoring and logging")
```

### Exercise 3: Performance Optimization Challenge

```python
"""
Debug This! Can you find and fix the performance issue?
"""

# Inefficient implementation
class SlowObject:
    def __init__(self, name, parameter):
        self.name = name
        self.parameter = parameter

    def distance_from_origin(self):
        """Calculate distance (SLOW!)."""
        # This recalculates every time!
        return np.sqrt(self.parameter**2)

    def computed_property(self):
        """Computed property (calls distance repeatedly)."""
        d = self.distance_from_origin()

        # Unnecessary loop!
        for i in range(1000):
            d = d * (1 + self.parameter * 0.001)

        return d

# Test slow version
import time

objects = [SlowObject(f"Object{i}", 0.01 * i)
           for i in range(100)]

start = time.perf_counter()
for obj in objects:
    for _ in range(10):  # Multiple calls
        d = obj.computed_property()
slow_time = time.perf_counter() - start

print(f"Slow version: {slow_time*1000:.1f} ms")

# SOLUTION: Optimized implementation
from functools import lru_cache

class FastObject:
    __slots__ = ['name', 'parameter', '_distance_cache']

    def __init__(self, name, parameter):
        self.name = name
        self.parameter = parameter
        self._distance_cache = None

    @property
    def distance_from_origin(self):
        """Cached distance calculation."""
        if self._distance_cache is None:
            self._distance_cache = np.sqrt(self.parameter**2)
        return self._distance_cache

    @lru_cache(maxsize=1)
    def computed_property(self):
        """Cached computed property."""
        d = self.distance_from_origin

        # Vectorized calculation instead of loop
        correction = (1 + self.parameter) ** 1.0

        return d * correction

# Test fast version
objects_fast = [FastObject(f"Object{i}", 0.01 * i)
                for i in range(100)]

start = time.perf_counter()
for obj in objects_fast:
    for _ in range(10):
        d = obj.computed_property()
fast_time = time.perf_counter() - start

print(f"Fast version: {fast_time*1000:.1f} ms")
print(f"Speedup: {slow_time/fast_time:.1f}x")

print("\n Performance issues found and fixed:")
print("  1. Recalculating distance every call")
print("  2. Unnecessary loop in computed_property")
print("  3. No caching of expensive calculations")
print("  4. Using dict instead of __slots__")
```

## Main Takeaways

You've completed a transformative journey from using scientific Python packages to understanding their architectural foundations. The abstract base classes, mixins, design patterns, and optimization techniques you've mastered aren't just advanced features - they're the pillars supporting every major scientific Python package you use. When NumPy seamlessly handles different array types, when Matplotlib coordinates thousands of plot elements, when unit-aware libraries prevent conversion disasters, they're using exactly the patterns you now understand. You've moved beyond being a consumer of these tools to understanding how they're built, why they work, and how to contribute at the same level.

The progression through this chapter mirrors your growth as a computational scientist. You started by understanding how ABCs enabled incompatible instruments to coordinate into unified systems. You discovered how mixins let complex experiments process vast amounts of data without code duplication. You learned how async programming enables modern facilities to control dozens of instruments simultaneously. These aren't just programming techniques - they're the engineering principles that enable modern scientific discovery. Every major scientific project relies on software architected with these patterns.

The practical skills you've developed prepare you for real research challenges. Dataclasses eliminate the boilerplate that clutters scientific code, letting you focus on science instead of syntax. Async programming enables you to build instrument control systems that maximize precious experiment time. Descriptors and metaclasses let you build domain-specific languages that make unit errors impossible. Performance optimization techniques ensure your code scales from prototype to production, from analyzing one sample to processing entire datasets. You now have the tools to build software that not only works but scales to the demands of modern science.

Looking forward, you're equipped to recognize these patterns throughout the scientific Python ecosystem and apply them in your own work. When you see NumPy's factory functions creating appropriate array types, you understand the factory pattern at work. When SciPy swaps optimization algorithms, you recognize the strategy pattern. When Matplotlib manages complex figure state, you see context managers and mixins in action. More importantly, you know when to apply these patterns in your own code - using ABCs when defining interfaces for collaboration, mixins when composing behaviors, async when controlling hardware, and optimization techniques when processing large datasets. You've transformed from someone who writes scripts to someone who architects systems, ready to build the next generation of tools that will enable tomorrow's discoveries.

## Definitions

**Abstract Base Class (ABC)**: A class that cannot be instantiated and defines methods that subclasses must implement, enforcing interfaces.

**Async/Await**: Python's syntax for asynchronous programming, allowing concurrent operations without threads.

**Context Manager**: An object implementing `__enter__` and `__exit__` methods for guaranteed resource cleanup with `with` statements.

**Coroutine**: A function that can pause and resume execution, enabling cooperative multitasking with `async def`.

**Dataclass**: A decorator that automatically generates special methods for classes primarily storing data.

**Descriptor**: An object implementing `__get__`, `__set__`, or `__delete__` to customize attribute access behavior.

**Design Pattern**: A reusable solution to a commonly occurring problem in software design.

**Diamond Problem**: Ambiguity in method resolution when a class inherits from two classes sharing a common base.

**Factory Pattern**: A design pattern that creates objects without specifying their exact classes.

**Generator**: A function that returns an iterator, yielding values one at a time to conserve memory.

**Interface**: A contract specifying what methods a class must provide, ensuring compatibility between components.

**Metaclass**: A class whose instances are classes themselves, controlling class creation and behavior.

**Method Resolution Order (MRO)**: The order Python searches through classes when looking for methods in inheritance hierarchies.

**Mixin**: A class providing specific functionality to be inherited by other classes, not meant to stand alone.

**Observer Pattern**: A design pattern where objects notify registered observers of state changes.

**Protocol**: A structural type system defining what methods/attributes an object must have for duck typing.

**Strategy Pattern**: A design pattern that defines a family of algorithms and makes them interchangeable.

**Type Hint**: Optional annotations indicating expected types for variables, parameters, and return values.

**\_\_slots\_\_**: Class attribute that restricts instance attributes to a fixed set, saving memory.

## Key Takeaways

- **Abstract base classes enforce interfaces across teams** - ABCs enable incompatible instruments and data sources to work together seamlessly

- **Mixins compose behaviors without code duplication** - Large experiments use mixins to give different detectors different capabilities efficiently

- **Dataclasses eliminate boilerplate in data-heavy code** - Modern scientific packages use dataclasses to reduce code by 30% while improving type safety

- **Async programming enables parallel instrument control** - Modern facilities use async to control multiple instruments simultaneously, maximizing efficiency

- **Descriptors and metaclasses enable domain-specific behavior** - Unit-aware systems use these to catch unit errors at assignment time, preventing disasters

- **Design patterns solve recurring architectural problems** - SciPy's 20+ optimization algorithms use the Strategy pattern, letting you swap algorithms with one parameter

- **\_\_slots\_\_ saves 40-50% memory for large datasets** - Critical for processing billion-element catalogs or massive nightly data

- **Caching dramatically improves performance** - The `@lru_cache` decorator can provide 10-1000x speedups for expensive calculations

- **Type hints make scientific code self-documenting** - Modern packages use type hints to catch errors early and improve IDE support

- **Profile before optimizing** - Real pipelines often find 60% of time in coordinate transforms, not core algorithms as expected

## Quick Reference Tables

### Design Patterns in Scientific Python

| Pattern | Problem Solved | NumPy/SciPy Example | Your Use Case |
|---------|---------------|---------------------|---------------|
| Factory | Create right object type | `np.array()` creates appropriate array | Different detector types |
| Strategy | Swap algorithms | `scipy.optimize.minimize(method=...)` | Reduction algorithms |
| Observer | Event notification | Matplotlib figure updates | Pipeline monitoring |
| Singleton | Single instance | NumPy's random state | Hardware controllers |
| Template | Algorithm skeleton | All SciPy optimizers | Analysis pipelines |

### Performance Optimization Techniques

| Technique | When to Use | Typical Improvement | Example |
|-----------|------------|-------------------|---------|
| `__slots__` | Many small objects | 40-50% memory | Large catalogs |
| `@lru_cache` | Repeated calculations | 10-1000x speed | Shift finding |
| Async | I/O or hardware control | 2-10x throughput | Instrument control |
| Vectorization | Numerical operations | 10-100x speed | Array operations |
| Dataclasses | Data containers | 30% less code | Measurements |

### Async Best Practices

| Pattern | Use Case | Example |
|---------|----------|---------|
| `asyncio.gather()` | Run tasks in parallel | Multiple acquisitions |
| `asyncio.create_task()` | Fire and forget | Background monitoring |
| `async with` | Async context managers | Instrument connections |
| `asyncio.Queue` | Producer-consumer | Data pipeline |
| `asyncio.sleep()` | Non-blocking delay | Hardware timing |

### Memory Comparison (per object)

| Implementation | Memory Usage | 1M Objects |
|---------------|--------------|------------|
| Regular class | ~296 bytes | 296 MB |
| With `__slots__` | ~56 bytes | 56 MB |
| Namedtuple | ~72 bytes | 72 MB |
| Dataclass | ~296 bytes | 296 MB |
| Dataclass + slots | ~56 bytes | 56 MB |

## References

1. van Rossum, G., & Warsaw, B. (2001). **PEP 3119 – Introducing Abstract Base Classes**. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-3119/ - The original proposal that introduced ABCs to Python.

2. Smith, E. (2018). **PEP 557 – Data Classes**. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0557/ - The proposal that introduced dataclasses to Python 3.7.

3. van Rossum, G., Lehtosalo, J., & Langa, Ł. (2014). **PEP 484 – Type Hints**. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0484/ - Introduction of type hints to Python.

4. Levkivskyi, I. (2019). **PEP 563 – Postponed Evaluation of Annotations**. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0563/ - The `from __future__ import annotations` feature.

5. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). **Design Patterns: Elements of Reusable Object-Oriented Software**. Addison-Wesley. - The classic "Gang of Four" book defining design patterns including Factory, Observer, and Strategy.

6. Selivanov, Y. (2015). **PEP 492 – Coroutines with async and await syntax**. Python Enhancement Proposals. https://www.python.org/dev/peps/pep-0492/ - Introduction of async/await to Python.

7. Ramalho, L. (2022). **Fluent Python** (2nd ed.). O'Reilly Media. - Comprehensive coverage of Python's advanced OOP features including metaclasses and descriptors.

8. Beazley, D., & Jones, B. K. (2013). **Python Cookbook** (3rd ed.). O'Reilly Media. - Practical recipes for advanced Python patterns and optimization techniques.

9. Harris, C. R., et al. (2020). **Array programming with NumPy**. *Nature*, 585(7825), 357-362. - NumPy's design philosophy and architecture.

10. Virtanen, P., et al. (2020). **SciPy 1.0: fundamental algorithms for scientific computing in Python**. *Nature Methods*, 17(3), 261-272. - SciPy's architectural decisions including the Strategy pattern for optimization.

11. Langa, Ł. (2021). **asyncio — Asynchronous I/O**. Python Documentation. https://docs.python.org/3/library/asyncio.html - Official Python asyncio documentation.

12. Martin, R. C. (2017). **Clean Architecture: A Craftsman's Guide to Software Structure and Design**. Prentice Hall. - Principles of software architecture applicable to scientific computing.

13. McKinney, W. (2017). **Python for Data Analysis** (2nd ed.). O'Reilly Media. - Practical patterns for scientific data processing.

14. Nygaard, K., & Dahl, O. J. (1978). **The development of the SIMULA languages**. *ACM SIGPLAN Notices*, 13(8), 245-272. - Historical origin of object-oriented programming concepts.

15. Python Software Foundation. (2024). **Abstract Base Classes for Containers**. https://docs.python.org/3/library/collections.abc.html - Documentation for Python's built-in ABCs.

16. Beazley, D. (2016). **Python Concurrency From the Ground Up**. PyCon 2015. https://www.youtube.com/watch?v=MCs5OvhV9S4 - Deep dive into Python's concurrency models including asyncio.

## Next Chapter Preview

In Chapter 11, you'll learn Pandas fundamentals for data manipulation and analysis. You'll discover how to work with DataFrames and Series, perform grouping and aggregation operations, merge and join datasets, and handle time series data. The patterns you've learned here - especially dataclasses, design patterns, and performance optimization - will help you understand how Pandas implements its elegant API for handling tabular scientific data. You'll see how Pandas uses many of the same architectural patterns to provide a powerful, intuitive interface for data analysis!
