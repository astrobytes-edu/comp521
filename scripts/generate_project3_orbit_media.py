"""Generate the Project 3 orbit illustrations and check their geometry.

From the course root:
    MPLCONFIGDIR=/private/tmp/comp521-mpl .venv/bin/python scripts/generate_project3_orbit_media.py
    .venv/bin/python scripts/generate_project3_orbit_media.py --check

The film uses the same illustrative eccentricity, 0.55, as the existing
auxiliary-circle figure. SciPy supplies reference positions for the media;
this is not the project's student Newton implementation.
"""

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
ECCENTRICITY = 0.55
BLUE, ORANGE, PURPLE = "#0072B2", "#D55E00", "#6B4C9A"
GRAY, INK = "#72797E", "#182C38"


def eccentric_anomaly(mean, eccentricity=ECCENTRICITY):
    """Reference solution for an illustration, with angles in radians."""
    if eccentricity == 0:
        return float(mean)
    return brentq(
        lambda angle: angle - eccentricity * np.sin(angle) - mean,
        mean - eccentricity,
        mean + eccentricity,
        xtol=5e-15,
        rtol=4 * np.finfo(float).eps,
    )


def position(mean, eccentricity=ECCENTRICITY):
    angle = eccentric_anomaly(mean, eccentricity)
    return np.array([
        np.cos(angle) - eccentricity,
        np.sqrt(1 - eccentricity**2) * np.sin(angle),
    ])


def check_geometry():
    mean = np.linspace(0, 2 * np.pi, 721)
    for eccentricity in (0.0, ECCENTRICITY):
        angle = np.array([eccentric_anomaly(m, eccentricity) for m in mean])
        residual = np.max(np.abs(angle - eccentricity * np.sin(angle) - mean))
        assert residual < 2e-14, residual
        xy = np.array([position(m, eccentricity) for m in mean])
        radius = np.linalg.norm(xy, axis=1)
        np.testing.assert_allclose(radius, 1 - eccentricity * np.cos(angle), atol=2e-14, rtol=0)
        # Equal increments in the clock must correspond to equal swept areas.
        area = np.sqrt(1 - eccentricity**2) / 2 * (angle - eccentricity * np.sin(angle))
        np.testing.assert_allclose(np.diff(area), np.diff(mean) * np.sqrt(1 - eccentricity**2) / 2,
                                   atol=2e-14, rtol=0)
        if eccentricity == 0:
            true = np.unwrap(np.arctan2(xy[:, 1], xy[:, 0]))
            np.testing.assert_allclose(angle, mean, atol=2e-14, rtol=0)
            np.testing.assert_allclose(true, mean, atol=2e-14, rtol=0)
            np.testing.assert_allclose(radius, 1, atol=2e-14, rtol=0)
        print(f"e={eccentricity:g}: max Kepler residual {residual:.3g}; equal-area and radius checks passed")

    # Independently check motion against the analytic peri/apastron speed ratio.
    step = 1e-5
    peri_speed = np.linalg.norm(position(step) - position(-step)) / (2 * step)
    apa_speed = np.linalg.norm(position(np.pi + step) - position(np.pi - step)) / (2 * step)
    expected = (1 + ECCENTRICITY) / (1 - ECCENTRICITY)
    np.testing.assert_allclose(peri_speed / apa_speed, expected, rtol=1e-8, atol=0)
    print(f"Equal-time motion: peri/apastron speed ratio {peri_speed / apa_speed:.9f}; expected {expected:.9f}")

    # The new illustrations use the existing film's E = pi/3 snapshot.
    from scipy.integrate import quad
    e, chosen_e = ECCENTRICITY, np.pi / 3
    chosen_m = chosen_e - e * np.sin(chosen_e)
    xy = position(chosen_m)
    radius = np.linalg.norm(xy)
    true = np.arctan2(xy[1], xy[0])
    np.testing.assert_allclose(eccentric_anomaly(chosen_m), chosen_e, atol=2e-14, rtol=0)
    np.testing.assert_allclose([np.cos(true), np.sin(true)],
        [(np.cos(chosen_e) - e) / radius,
         np.sqrt(1 - e**2) * np.sin(chosen_e) / radius], atol=2e-14, rtol=0)

    # Independently integrate the area swept by the star-to-planet vector.
    def area_integrand(angle):
        x, y = np.cos(angle) - e, np.sqrt(1 - e**2) * np.sin(angle)
        dx, dy = -np.sin(angle), np.sqrt(1 - e**2) * np.cos(angle)
        return (x * dy - y * dx) / 2

    swept_area = quad(area_integrand, 0, chosen_e)[0]
    np.testing.assert_allclose(swept_area / (np.pi * np.sqrt(1 - e**2)),
                              chosen_m / (2 * np.pi), atol=2e-14, rtol=0)
    for turns in (-2, -1, 0, 1, 2):
        shifted = chosen_m + turns * 2 * np.pi
        np.testing.assert_allclose(eccentric_anomaly(shifted),
                                  chosen_e + turns * 2 * np.pi, atol=2e-14, rtol=0)
        np.testing.assert_allclose(position(shifted), xy, atol=2e-14, rtol=0)

    # The inclined drawing retains the page's 65-degree illustrative tilt
    # and Project 3's omega = 90 degrees. Rotation must preserve radius.
    inclination, omega = np.deg2rad(65), np.pi / 2
    u = true + omega
    rotated = radius * np.array([np.cos(u), np.sin(u) * np.cos(inclination),
                                 np.sin(u) * np.sin(inclination)])
    np.testing.assert_allclose(np.linalg.norm(rotated), radius, atol=2e-14, rtol=0)
    # Positive orbital motion at the ascending node must cross toward +Z.
    node_r = (1 - e**2) / (1 + e * np.cos(-omega))
    node_behind = node_r * np.sin(-1e-6) * np.sin(inclination)
    node_ahead = node_r * np.sin(1e-6) * np.sin(inclination)
    assert node_behind < 0 < node_ahead
    print(f"Shared snapshot: M={np.degrees(chosen_m):.6f} deg; "
          f"E={np.degrees(chosen_e):.6f} deg; nu={np.degrees(true):.6f} deg; "
          f"r/a={radius:.6f}; swept-area, branch, rotation, and node checks passed")


def illustration_style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.size": 11.5,
        "text.color": INK,
        "font.family": "DejaVu Sans",
        "svg.fonttype": "path",
        "svg.hashsalt": "comp521-project3",
    })
    return plt


def parameter_figure():
    plt = illustration_style()
    from matplotlib.patches import Arc
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.2), layout="constrained")
    fig.get_layout_engine().set(w_pad=0.12, h_pad=0.12, wspace=0.10, hspace=0.08)
    angles = np.linspace(0, 2 * np.pi, 601)

    def orbit(ax, a, e, omega=0, **style):
        xy = a * np.array([np.cos(angles) - e, np.sqrt(1 - e**2) * np.sin(angles)])
        rotation = np.array([[np.cos(omega), -np.sin(omega)], [np.sin(omega), np.cos(omega)]])
        ax.plot(*(rotation @ xy), **style)

    for ax in axes.flat:
        ax.set_aspect("equal")
        ax.set(xlim=(-2.0, 1.6), ylim=(-1.95, 1.15))
        ax.axis("off")
        ax.scatter(0, 0, color=ORANGE, s=58, zorder=5)

    def heading(ax, text):
        ax.set_title(text, loc="left", fontsize=14, weight="normal", pad=38)

    def legend(ax, columns=2):
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.015), ncol=columns,
                  frameon=False, fontsize=10.5, borderaxespad=0, handlelength=1.8,
                  handletextpad=0.6, columnspacing=1.25)

    def note(ax, text):
        ax.text(0.5, 0.035, text, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=11, color=INK)

    ax = axes[0, 0]
    heading(ax, r"Size · $a$")
    orbit(ax, 0.65, 0.4, color=GRAY, lw=2, ls="--", label="smaller a")
    orbit(ax, 1, 0.4, color=BLUE, lw=2.8, label="larger a")
    ax.annotate("", (-1.4, -1.15), (0.6, -1.15), arrowprops={"arrowstyle": "<->", "color": INK})
    ax.text(-0.4, -1.38, r"Full width = $2a$", ha="center")
    note(ax, r"$a$ is half the longest width")
    legend(ax)

    ax = axes[0, 1]
    heading(ax, r"Shape · $e$")
    orbit(ax, 1, 0, color=GRAY, lw=2, ls="--", label="e = 0: circle")
    orbit(ax, 1, ECCENTRICITY, color=BLUE, lw=2.8, label="e = 0.55: ellipse")
    ax.scatter([-1 - ECCENTRICITY, 1 - ECCENTRICITY], [0, 0], color=BLUE, s=30)
    ax.annotate("Apastron\nfarthest", (-1.55, 0), (-1.55, -1.32), ha="center",
                va="center", fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": GRAY, "lw": 1})
    ax.annotate("Periastron\nclosest", (0.45, 0), (1.12, -1.32), ha="center",
                va="center", fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": GRAY, "lw": 1,
                            "connectionstyle": "angle,angleA=90,angleB=0,rad=8"})
    note(ax, r"Same $a$; star at a focus")
    legend(ax)

    ax = axes[1, 0]
    heading(ax, r"Tilt · $i$")
    ax.plot(np.cos(angles), np.sin(angles), color=GRAY, lw=2, ls="--", label="0°: face-on")
    ax.plot(np.cos(angles), np.sin(angles) * np.cos(np.pi / 3), color=BLUE, lw=2.8, label="60°: tilted")
    ax.plot([-1, 1], [0, 0], color=PURPLE, lw=2.8, label="90°: edge-on")
    ax.text(0, -1.36, "Circular orbit, seen on the sky", ha="center", fontsize=11)
    note(ax, "The apparent track becomes flatter")
    legend(ax, columns=3)

    ax = axes[1, 1]
    heading(ax, r"Orientation · $\omega$")
    orbit(ax, 1, ECCENTRICITY, color=GRAY, lw=2, ls="--", label="ω = 0°")
    orbit(ax, 1, ECCENTRICITY, np.pi / 2, color=BLUE, lw=2.8, label="ω = 90°")
    ax.annotate("", (1.32, 0), (0, 0),
                arrowprops={"arrowstyle": "->", "color": INK, "lw": 1})
    ax.annotate("Node\ndirection", (1.2, 0), (1.2, 0.58), ha="center", va="center",
                fontsize=10.5, arrowprops={"arrowstyle": "-", "color": GRAY,
                                         "lw": 1, "shrinkA": 5, "shrinkB": 5})
    ax.plot([0, 0], [0, 0.45], color=BLUE, lw=1.5)
    ax.scatter([0.45, 0], [0, 0.45], color=[GRAY, BLUE], s=40, zorder=6)
    ax.add_patch(Arc((0, 0), 0.56, 0.56, theta1=0, theta2=90, color=PURPLE, lw=2))
    ax.text(0.13, 0.10, r"$\omega$", color=PURPLE, fontsize=11.5,
            ha="center", va="center")
    note(ax, "View in the orbital plane")
    legend(ax)

    destination = ROOT / "08-assessments/projects/figures/project3-orbit-parameters"
    for suffix in ("svg", "png"):
        fig.savefig(destination.with_suffix(f".{suffix}"), dpi=170, facecolor="white")
        print(destination.with_suffix(f".{suffix}").relative_to(ROOT))
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check geometry without regenerating assets")
    args = parser.parse_args()
    check_geometry()
    if not args.check:
        parameter_figure()
