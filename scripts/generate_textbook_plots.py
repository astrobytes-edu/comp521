"""Generate the small set of reproducible Python plots used in the textbook."""

from __future__ import annotations

from html import escape
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRECTORY = ROOT / "assets" / "textbook-figures"

plt.rcParams.update(
    {
        "font.family": "Arial",
        "svg.fonttype": "none",
        "svg.hashsalt": "comp521-textbook-plots",
    }
)

INK = "#0F172A"
BODY = "#334155"
GRID = "#CBD5E1"
COLORS = {
    "constant": "#64748B",
    "logarithmic": "#0F766E",
    "linear": "#2563EB",
    "n_log_n": "#D97706",
    "quadratic": "#DC2626",
}


def add_svg_accessibility_metadata(path: Path, title: str, description: str) -> None:
    """Add native SVG metadata alongside the MyST figure alt text."""
    svg = path.read_text()
    root_start = svg.index("<svg")
    root_end = svg.index(">", root_start) + 1
    metadata = f"\n  <title>{escape(title)}</title>\n  <desc>{escape(description)}</desc>"
    accessible_svg = svg[:root_end] + metadata + svg[root_end:]
    path.write_text("\n".join(line.rstrip() for line in accessible_svg.splitlines()) + "\n")


def save_svg(figure: plt.Figure, filename: str, title: str, description: str) -> None:
    """Write editable SVG output with visual and nonvisual descriptions."""
    output = ASSET_DIRECTORY / filename
    figure.savefig(
        output,
        format="svg",
        facecolor="white",
        metadata={"Date": None},
    )
    plt.close(figure)
    add_svg_accessibility_metadata(output, title, description)


def configure_axis(axis: plt.Axes) -> None:
    """Apply the restrained textbook plot treatment."""
    axis.set_facecolor("#F8FAFC")
    axis.grid(True, which="major", color=GRID, linewidth=0.8, alpha=0.8)
    axis.grid(True, which="minor", color=GRID, linewidth=0.45, alpha=0.35)
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color(BODY)
    axis.tick_params(colors=BODY, labelsize=14)
    axis.xaxis.label.set_color(BODY)
    axis.yaxis.label.set_color(BODY)


def make_operation_count_plot() -> None:
    """Show an asymptotic work model, explicitly not a runtime benchmark."""
    n = np.logspace(1, 6, 500)
    figure, axis = plt.subplots(figsize=(8.4, 5.35), layout="constrained")
    configure_axis(axis)

    axis.loglog(n, np.ones_like(n), color=COLORS["constant"], linewidth=2.4, label=r"$O(1)$")
    axis.loglog(n, np.log2(n), color=COLORS["logarithmic"], linewidth=2.4, label=r"$O(\log n)$")
    axis.loglog(n, n, color=COLORS["linear"], linewidth=2.7, label=r"$O(n)$")
    axis.loglog(n, n * np.log2(n), color=COLORS["n_log_n"], linewidth=2.7, label=r"$O(n\log n)$")
    axis.loglog(n, n**2, color=COLORS["quadratic"], linewidth=2.9, label=r"$O(n^2)$")

    axis.set_xlim(10, 3e6)
    axis.set_ylim(0.5, 3e12)
    axis.set_xlabel("input size n", fontsize=16)
    axis.set_ylabel("illustrative operation count", fontsize=16)
    axis.set_title("How does the work grow?", color=INK, fontweight="bold", fontsize=25, loc="left", pad=16)
    axis.text(
        0.0,
        1.01,
        "A growth model, not timing data from one machine",
        transform=axis.transAxes,
        color=BODY,
        fontsize=16,
    )
    axis.scatter([1e6], [1e12], color=COLORS["quadratic"], s=28, zorder=5)
    axis.text(
        0.61,
        0.90,
        r"At $n = 10^6$, $O(n^2)$ means" + "\n" + r"$10^{12}$ pair checks",
        transform=axis.transAxes,
        color=INK,
        fontsize=14,
        ha="left",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": GRID, "alpha": 0.96},
    )
    legend = axis.legend(loc="upper left", ncol=2, frameon=True, fontsize=14)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor(GRID)

    save_svg(
        figure,
        "ch04-representation-scaling.svg",
        "Illustrative asymptotic operation counts",
        "A log-log plot compares constant, logarithmic, linear, n log n, and quadratic operation-count models as input size grows from ten to one million. An annotation notes that a quadratic all-pairs calculation has one trillion pair checks at one million inputs. The plot is an asymptotic work model, not a benchmark.",
    )


def make_cancellation_plot() -> None:
    """Show when direct subtraction disagrees with a stable identity."""
    x = np.logspace(-12, -1, 500)
    direct = 1 - np.cos(x)
    stable = 2 * np.sin(x / 2) ** 2
    disagreement = np.abs(direct - stable) / stable
    visible_disagreement = np.maximum(disagreement, np.finfo(float).eps)

    figure, axis = plt.subplots(figsize=(8.4, 5.35), layout="constrained")
    configure_axis(axis)
    axis.semilogx(x, visible_disagreement, color=COLORS["quadratic"], linewidth=2.8)
    axis.set_yscale("log")
    axis.set_xlim(1e-12, 1e-1)
    axis.set_ylim(1e-16, 2)
    axis.set_xlabel("angle x (radians)", fontsize=16)
    axis.set_ylabel("relative disagreement with stable identity", fontsize=16)
    axis.set_title("Cancellation loses small results", color=INK, fontweight="bold", fontsize=25, loc="left", pad=16)
    axis.text(
        0.0,
        1.01,
        r"Direct: $1 - \cos(x)$  |  Stable: $2\sin^2(x/2)$",
        transform=axis.transAxes,
        color=BODY,
        fontsize=16,
    )
    x_example = 1e-8
    axis.axvline(x_example, color=BODY, linewidth=1.1, linestyle="--", alpha=0.55)
    axis.annotate(
        r"At $x = 10^{-8}$, direct subtraction" + "\n" + "rounds to zero; the stable form retains scale",
        xy=(x_example, 1.0),
        xytext=(2e-10, 1e-6),
        color=INK,
        fontsize=14,
        ha="left",
        arrowprops={"arrowstyle": "-", "color": BODY, "lw": 1.2},
    )

    save_svg(
        figure,
        "ch02-cancellation-stability.svg",
        "Direct subtraction versus a stable identity for one minus cosine",
        "A logarithmic plot shows the relative disagreement between direct computation of one minus cosine of x and the algebraically equivalent stable identity two sine squared of x over two. The disagreement reaches 100 percent for very small angles, including x equal to ten to the minus eight radians, where direct subtraction rounds to zero.",
    )


def make_visual_evidence_plot() -> None:
    """Contrast the same measurements as marks and as an inspectable claim."""
    rng = np.random.default_rng(521)
    hours = np.linspace(0.0, 5.0, 16)
    uncertainty = np.full_like(hours, 0.0017)
    transit = 0.010 * np.exp(-0.5 * ((hours - 2.55) / 0.38) ** 2)
    relative_flux = 1.0 - transit + rng.normal(0.0, uncertainty)

    figure, axes = plt.subplots(2, 1, figsize=(8.4, 8.2), layout="constrained")
    for axis in axes:
        configure_axis(axis)
        axis.set_xlim(-0.15, 5.15)
        axis.set_ylim(0.984, 1.006)

    axes[0].scatter(hours, relative_flux, color=COLORS["linear"], s=48, zorder=3)
    axes[0].set_title("Marks without a claim", color=INK, fontsize=18, fontweight="bold", loc="left")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].spines[["left", "bottom"]].set_visible(False)
    axes[0].grid(False)
    axes[0].text(
        0.06,
        0.08,
        "What quantity?\nWhat scale?\nHow uncertain?",
        transform=axes[0].transAxes,
        color=BODY,
        fontsize=14,
        va="bottom",
    )

    axes[1].errorbar(
        hours,
        relative_flux,
        yerr=uncertainty,
        fmt="o",
        color=COLORS["linear"],
        ecolor="#94A3B8",
        elinewidth=1.4,
        capsize=3,
        markersize=5.5,
        zorder=3,
    )
    axes[1].axhline(1.0, color=BODY, linewidth=1.1, linestyle="--", alpha=0.7)
    axes[1].set_title("Inspectable measurement", color=INK, fontsize=18, fontweight="bold", loc="left")
    axes[1].set_xlabel("time since start [h]", fontsize=15)
    axes[1].set_ylabel("relative flux [normalized]", fontsize=15)
    axes[1].annotate(
        "candidate dip",
        xy=(2.67, relative_flux[8]),
        xytext=(3.25, 0.9885),
        color=INK,
        fontsize=13,
        arrowprops={"arrowstyle": "-", "color": BODY, "lw": 1.1},
    )
    figure.suptitle(
        "Same data, different evidence",
        color=INK,
        fontsize=22,
        fontweight="bold",
        x=0.06,
        ha="left",
    )

    save_svg(
        figure,
        "ch08-evidence-ready-plot.svg",
        "The same synthetic flux measurements as unlabeled marks and as an inspectable plot",
        "Two panels show the same synthetic relative-flux measurements. The left panel shows unlabeled blue marks. The right panel supplies time in hours, normalized relative flux, uncertainty bars, a reference level, and an annotation that calls the visible dip a candidate rather than a conclusion.",
    )


def make_normalization_plot() -> None:
    """Show why normalization is part of the meaning of a 2D figure."""
    coordinates = np.linspace(-4.0, 4.0, 180)
    x, y = np.meshgrid(coordinates, coordinates)
    bright_core = np.exp(-(x**2 + y**2) / 0.55)
    faint_companion = 0.035 * np.exp(-((x - 2.0) ** 2 + (y + 1.2) ** 2) / 0.18)
    diffuse_background = 0.004 * np.exp(-(x**2 + y**2) / 8.0)
    intensity = bright_core + faint_companion + diffuse_background

    figure, axes = plt.subplots(2, 1, figsize=(8.4, 9.0), layout="constrained")
    for axis in axes:
        axis.set_facecolor("#F8FAFC")
        axis.set_xticks([])
        axis.set_yticks([])
        for spine in axis.spines.values():
            spine.set_color(GRID)

    linear_image = axes[0].imshow(intensity, cmap="viridis", origin="lower")
    axes[0].set_title("Linear normalization", color=INK, fontsize=18, fontweight="bold", loc="left")
    axes[0].text(
        0.05,
        0.06,
        "bright core dominates",
        transform=axes[0].transAxes,
        color="white",
        fontsize=13,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": INK, "edgecolor": "none", "alpha": 0.82},
    )
    linear_colorbar = figure.colorbar(linear_image, ax=axes[0], fraction=0.046, pad=0.03)
    linear_colorbar.set_label("synthetic intensity [arbitrary units]", color=BODY, fontsize=13)
    linear_colorbar.ax.tick_params(labelsize=11, colors=BODY)

    log_image = axes[1].imshow(
        intensity,
        cmap="viridis",
        norm=LogNorm(vmin=intensity.min(), vmax=intensity.max()),
        origin="lower",
    )
    axes[1].set_title("Log normalization", color=INK, fontsize=18, fontweight="bold", loc="left")
    axes[1].text(
        0.05,
        0.06,
        "faint companion becomes visible",
        transform=axes[1].transAxes,
        color="white",
        fontsize=13,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": INK, "edgecolor": "none", "alpha": 0.82},
    )
    log_colorbar = figure.colorbar(log_image, ax=axes[1], fraction=0.046, pad=0.03)
    log_colorbar.set_label("synthetic intensity [arbitrary units]", color=BODY, fontsize=13)
    log_colorbar.ax.tick_params(labelsize=11, colors=BODY)
    figure.suptitle(
        "Normalization changes visible structure",
        color=INK,
        fontsize=22,
        fontweight="bold",
        x=0.06,
        ha="left",
    )

    save_svg(
        figure,
        "ch08-normalization-comparison.svg",
        "Linear and logarithmic normalization of the same synthetic two-dimensional intensity field",
        "Two panels use the same synthetic two-dimensional intensity field and the same perceptually uniform viridis colormap. Linear normalization emphasizes a bright central core, while logarithmic normalization also makes a faint companion feature visible. Both colorbars state that the intensity units are arbitrary.",
    )


def main() -> None:
    """Generate every Python-produced textbook plot deterministically."""
    make_cancellation_plot()
    make_operation_count_plot()
    make_visual_evidence_plot()
    make_normalization_plot()


if __name__ == "__main__":
    main()
