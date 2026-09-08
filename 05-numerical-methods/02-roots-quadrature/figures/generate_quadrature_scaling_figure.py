"""Regenerate the quadrature convergence figure used in the Block 2 reading."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT = Path(__file__).with_name("2_5_simpson_vs_trapezoid_scaling.webp")
INK = "#1F2937"
GRID = "#CBD5E1"
TRAPEZOID = "#A13D72"
SIMPSON = "#1F78A8"


def trapezoid_exp(panel_count: int) -> float:
    """Approximate the dimensionless integral of exp(x) on [0, 1]."""
    x = np.linspace(0.0, 1.0, panel_count + 1)
    h = 1.0 / panel_count
    values = np.exp(x)
    return float(h * (0.5 * values[0] + values[1:-1].sum() + 0.5 * values[-1]))


def simpson_exp(panel_count: int) -> float:
    """Approximate the dimensionless integral of exp(x) on [0, 1]."""
    if panel_count % 2 != 0:
        raise ValueError("panel_count must be even for Simpson's rule.")
    x = np.linspace(0.0, 1.0, panel_count + 1)
    h = 1.0 / panel_count
    values = np.exp(x)
    return float(
        h
        * (
            values[0]
            + 4.0 * values[1:-1:2].sum()
            + 2.0 * values[2:-1:2].sum()
            + values[-1]
        )
        / 3.0
    )


def panels_for_target(rule, target: float) -> int:
    """Return the first power-of-two panel count meeting a stated error target."""
    exact = np.e - 1.0
    for panel_count in 2 ** np.arange(1, 21):
        if abs(rule(int(panel_count)) - exact) <= target:
            return int(panel_count)
    raise RuntimeError("target was not reached by the search range.")


def style_axis(axis: plt.Axes) -> None:
    """Apply shared readable axis styling."""
    axis.set_facecolor("#F8FAFC")
    axis.grid(True, which="major", color=GRID, linewidth=0.8)
    axis.grid(True, which="minor", color=GRID, linewidth=0.4, alpha=0.45)
    axis.spines[["top", "right"]].set_visible(False)
    axis.tick_params(labelsize=12, colors=INK)


def main() -> None:
    """Create the checked convergence and efficiency comparison figure."""
    panel_counts = 2 ** np.arange(1, 12)
    exact = np.e - 1.0
    trapezoid_errors = np.array([abs(trapezoid_exp(int(n)) - exact) for n in panel_counts])
    simpson_errors = np.array([abs(simpson_exp(int(n)) - exact) for n in panel_counts])

    figure, (error_axis, cost_axis) = plt.subplots(1, 2, figsize=(14, 6.5), layout="constrained")
    for axis in (error_axis, cost_axis):
        style_axis(axis)

    error_axis.loglog(
        panel_counts,
        trapezoid_errors,
        color=TRAPEZOID,
        linestyle="--",
        marker="o",
        markeredgecolor=INK,
        markeredgewidth=0.6,
        linewidth=2.4,
        label="trapezoid",
    )
    error_axis.loglog(
        panel_counts,
        simpson_errors,
        color=SIMPSON,
        linestyle="-",
        marker="s",
        markeredgecolor=INK,
        markeredgewidth=0.6,
        linewidth=2.4,
        label="Simpson",
    )
    error_axis.loglog(
        panel_counts,
        trapezoid_errors[0] * (panel_counts / panel_counts[0]) ** -2,
        color=INK,
        linestyle=":",
        linewidth=1.5,
        label=r"reference $n^{-2}$",
    )
    error_axis.loglog(
        panel_counts,
        simpson_errors[0] * (panel_counts / panel_counts[0]) ** -4,
        color=INK,
        linestyle="-.",
        linewidth=1.5,
        label=r"reference $n^{-4}$",
    )
    error_axis.axhline(np.finfo(float).eps, color="#B91C1C", linestyle="--", linewidth=1.4, label="machine epsilon")
    error_axis.set_xlabel("number of panels $n$ [dimensionless]", fontsize=13)
    error_axis.set_ylabel("absolute error [dimensionless]", fontsize=13)
    error_axis.set_title(r"Error for $\int_0^1 e^x\,dx$", color=INK, fontsize=17, fontweight="bold")
    error_axis.annotate(
        "slope −2",
        xy=(64, trapezoid_errors[5]),
        xytext=(13, 2.0e-5),
        color=TRAPEZOID,
        fontsize=12,
        arrowprops={"arrowstyle": "->", "color": TRAPEZOID, "lw": 1.2},
    )
    error_axis.annotate(
        "slope −4",
        xy=(128, simpson_errors[6]),
        xytext=(145, 2.0e-9),
        color=SIMPSON,
        fontsize=12,
        arrowprops={"arrowstyle": "->", "color": SIMPSON, "lw": 1.2},
    )
    error_axis.legend(fontsize=10, frameon=True, facecolor="white", edgecolor=GRID)

    targets = np.array([1.0e-2, 1.0e-4, 1.0e-6, 1.0e-8])
    trapezoid_panels = np.array([panels_for_target(trapezoid_exp, target) for target in targets])
    simpson_panels = np.array([panels_for_target(simpson_exp, target) for target in targets])
    cost_axis.loglog(
        targets,
        trapezoid_panels,
        color=TRAPEZOID,
        linestyle="--",
        marker="o",
        markeredgecolor=INK,
        markeredgewidth=0.6,
        linewidth=2.4,
        label="trapezoid",
    )
    cost_axis.loglog(
        targets,
        simpson_panels,
        color=SIMPSON,
        linestyle="-",
        marker="s",
        markeredgecolor=INK,
        markeredgewidth=0.6,
        linewidth=2.4,
        label="Simpson",
    )
    cost_axis.invert_xaxis()
    cost_axis.set_xlabel("target absolute error [dimensionless]", fontsize=13)
    cost_axis.set_ylabel("number of panels $n$ [dimensionless]", fontsize=13)
    cost_axis.set_title("Panels needed for a target", color=INK, fontsize=17, fontweight="bold")
    cost_axis.legend(fontsize=11, frameon=True, facecolor="white", edgecolor=GRID)

    figure.savefig(OUTPUT, format="webp", dpi=200, facecolor="white")
    plt.close(figure)


if __name__ == "__main__":
    main()
