---
title: "Light Curves and Normalized Flux"
subtitle: "Scientific Background | Astronomy & observables"
---

# Light Curves and Normalized Flux

A **light curve** is a record of measured brightness as a function of time.
For a transit, the key pattern is a small decrease relative to the star's usual
brightness, followed by a return toward that baseline.

## Flux is the observable

In this course, **flux** means the light power received per unit collecting
area. A detector estimates that received light at a sequence of times. The
value can depend on the instrument, observing conditions, and chosen units, so
we often compare each measurement with an out-of-transit baseline $F_0$.

$$
\text{normalized flux} = \frac{F}{F_0}.
$$

Normalized flux is dimensionless. A value near $1$ represents the chosen
baseline; a value below $1$ represents a dimmer measurement. It does **not**
mean the star has stopped emitting light.

## Transit depth

The **transit depth** is the fractional decrease from the baseline:

$$
\delta = 1 - \frac{F}{F_0}.
$$

For example, normalized flux $0.990$ has depth $0.010$, meaning a one-percent
decrease relative to the defined baseline.

## Reading a light curve responsibly

A dip alone is not a finished conclusion. Before calling it evidence for a
planet, ask:

- Is the baseline defined and visible?
- Does the dip recur at a consistent time interval?
- How large is the measurement uncertainty and instrumental variation?
- Could stellar activity or another source produce a similar pattern?

Project 1 begins before those observational complications. It uses a known
geometric model to practice how computational assumptions become visible,
testable output.
