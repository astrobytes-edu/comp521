---
title: "The Uniform-Source Transit Model"
subtitle: "Scientific Background | Models & approximations"
---

# The Uniform-Source Transit Model

The first transit model treats the star as a uniformly bright circular disk and
the planet as an opaque circular disk. It asks a geometric question: **what
fraction of the visible stellar disk remains uncovered?**

## The complete-overlap starting point

Let

$$
p = \frac{R_p}{R_\star},
$$

where $R_p$ is planet radius and $R_\star$ is stellar radius. Because this is a
ratio of lengths measured in the same units, $p$ has no units. If the smaller
planet disk lies entirely in front of the stellar disk, the blocked fraction is
the area ratio:

$$
\delta = \frac{\pi R_p^2}{\pi R_\star^2} = p^2.
$$

The normalized flux is therefore

$$
\frac{F}{F_0} = 1 - p^2.
$$

If $p=0.10$, then $\delta=0.01$ and the normalized flux is $0.99$. If $p$ is
doubled to $0.20$, depth becomes $0.04$: area scales with the square of a
length.

## What Project 1 adds

The complete-overlap result is only one limiting case. A complete model also
needs the projected center separation

$$
z = \frac{d}{R_\star},
$$

where $d$ is the projected distance between disk centers. Different values of
$p$ and $z$ produce no overlap, partial overlap, full overlap, or complete
stellar coverage. Project 1 turns those geometric branches into a testable
function.

## Limits of the model

This is a deliberately useful approximation, not a claim that stars are flat,
uniform disks. It omits, among other effects:

- limb darkening: stellar edges can appear dimmer than the center;
- measurement noise and instrumental systematics;
- starspots and other stellar variability; and
- orbital details that determine the timing of $z$.

Those omissions tell us the scope of a conclusion: the model teaches geometry
and computational validation; it does not by itself fit a real observed
exoplanet system.
