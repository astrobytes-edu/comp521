"""
Generate pedagogical figures for HMC module (Part 4)

Modern minimalist design with clean aesthetics and readable fonts.

Requirements:
    conda activate astro
    pip install numpy matplotlib scipy
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import multivariate_normal
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

# Modern minimalist color scheme
COLORS = {
    'primary': '#2E3440',      # Dark blue-gray (text, lines)
    'secondary': '#4C566A',    # Medium gray
    'accent1': '#5E81AC',      # Muted blue (primary data)
    'accent2': '#88C0D0',      # Light blue (secondary data)
    'accent3': '#8FBCBB',      # Teal (tertiary)
    'success': '#A3BE8C',      # Muted green
    'warning': '#EBCB8B',      # Muted yellow
    'error': '#BF616A',        # Muted red
    'background': '#ECEFF4',   # Very light gray
    'white': '#FFFFFF',
    'grid': '#D8DEE9',         # Light gray grid
}

# Set publication-quality defaults - CLEAN and MINIMAL
plt.rcParams.update({
    'font.size': 13,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'axes.labelsize': 14,
    'axes.titlesize': 15,
    'axes.titleweight': 'normal',
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.2,
    'grid.color': COLORS['grid'],
    'axes.facecolor': 'white',
    'axes.edgecolor': COLORS['secondary'],
    'axes.linewidth': 1.2,
    'axes.labelcolor': COLORS['primary'],
    'text.color': COLORS['primary'],
    'xtick.color': COLORS['primary'],
    'ytick.color': COLORS['primary'],
    'legend.framealpha': 0.95,
    'legend.edgecolor': COLORS['secondary'],
})


# ============================================================================
# MCMC Implementations (unchanged)
# ============================================================================

def log_posterior_2d(theta, Sigma_inv):
    """Log of 2D correlated Gaussian."""
    return -0.5 * theta @ Sigma_inv @ theta


def grad_log_posterior_2d(theta, Sigma_inv):
    """Gradient of log-posterior."""
    return -Sigma_inv @ theta


def metropolis_hastings(log_posterior, theta_init, proposal_std, n_samples,
                       Sigma_inv, seed=42):
    """Metropolis-Hastings with Gaussian random walk."""
    np.random.seed(seed)
    d = len(theta_init)
    samples = np.zeros((n_samples, d))
    theta = theta_init.copy()
    n_accept = 0

    for i in range(n_samples):
        theta_prop = theta + proposal_std * np.random.randn(d)
        log_alpha = (log_posterior(theta_prop, Sigma_inv) -
                    log_posterior(theta, Sigma_inv))

        if np.log(np.random.rand()) < log_alpha:
            theta = theta_prop
            n_accept += 1

        samples[i] = theta

    acceptance_rate = n_accept / n_samples
    return samples, acceptance_rate


def leapfrog(theta, p, epsilon, L, grad_log_post, Sigma_inv, M_inv):
    """Leapfrog integrator for HMC."""
    theta = theta.copy()
    p = p.copy()

    p = p + 0.5 * epsilon * grad_log_post(theta, Sigma_inv)

    for _ in range(L):
        theta = theta + epsilon * M_inv @ p
        p = p + epsilon * grad_log_post(theta, Sigma_inv)

    p = p - 0.5 * epsilon * grad_log_post(theta, Sigma_inv)
    p = -p

    return theta, p


def hamiltonian(theta, p, log_post, Sigma_inv, M_inv):
    """Compute Hamiltonian H = U + K."""
    U = -log_post(theta, Sigma_inv)
    K = 0.5 * p @ M_inv @ p
    return U + K


def hmc(log_posterior, grad_log_post, theta_init, epsilon, L, n_samples,
        Sigma_inv, M=None, seed=42):
    """Hamiltonian Monte Carlo sampler."""
    np.random.seed(seed)
    d = len(theta_init)

    if M is None:
        M = np.eye(d)
    M_inv = np.linalg.inv(M)

    samples = np.zeros((n_samples, d))
    theta = theta_init.copy()
    n_accept = 0
    trajectories = []

    for i in range(n_samples):
        p = np.random.multivariate_normal(np.zeros(d), M)
        p_old = p.copy()
        theta_old = theta.copy()

        theta_traj = [theta.copy()]
        theta, p = leapfrog(theta, p, epsilon, L, grad_log_post, Sigma_inv, M_inv)
        theta_traj.append(theta.copy())

        if i < 10:
            trajectories.append(np.array(theta_traj))

        H_old = hamiltonian(theta_old, p_old, log_posterior, Sigma_inv, M_inv)
        H_new = hamiltonian(theta, p, log_posterior, Sigma_inv, M_inv)

        if np.log(np.random.rand()) < -(H_new - H_old):
            n_accept += 1
        else:
            theta = theta_old

        samples[i] = theta

    acceptance_rate = n_accept / n_samples
    return samples, acceptance_rate, trajectories


def estimate_ess(samples, max_lag=None):
    """Estimate effective sample size using autocorrelation."""
    n = len(samples)
    if max_lag is None:
        max_lag = min(n // 2, 1000)

    samples_centered = samples - np.mean(samples)
    acf = np.correlate(samples_centered, samples_centered, mode='full')
    acf = acf[len(acf)//2:]

    if acf[0] == 0:
        return 1.0

    acf = acf / acf[0]

    tau_int = 0.5
    for lag in range(1, min(max_lag, len(acf))):
        if acf[lag] < 0:
            break
        tau_int += acf[lag]

    ess = n / (2 * tau_int)
    return max(1, ess)


# ============================================================================
# FIGURE 1: Four-panel M-H vs HMC comparison (REDESIGNED)
# ============================================================================

def create_figure1_mh_vs_hmc():
    """Clean, minimalist four-panel comparison."""

    # Setup
    rho = 0.95
    Sigma = np.array([[1, rho], [rho, 1]])
    Sigma_inv = np.linalg.inv(Sigma)

    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    pos = np.dstack((X, Y))
    rv = multivariate_normal([0, 0], Sigma)
    Z = rv.pdf(pos)

    print("Running Metropolis-Hastings (10,000 samples)...")
    theta_init = np.array([2.0, 2.0])
    samples_mh, accept_mh = metropolis_hastings(
        log_posterior_2d, theta_init, proposal_std=0.5,
        n_samples=10000, Sigma_inv=Sigma_inv
    )

    print("Running HMC (1,000 samples)...")
    samples_hmc, accept_hmc, trajectories = hmc(
        log_posterior_2d, grad_log_posterior_2d, theta_init,
        epsilon=0.15, L=20, n_samples=1000, Sigma_inv=Sigma_inv
    )

    print(f"M-H acceptance rate: {accept_mh:.1%}")
    print(f"HMC acceptance rate: {accept_hmc:.1%}")

    # Create figure
    fig = plt.figure(figsize=(15, 12))
    gs = GridSpec(2, 2, hspace=0.25, wspace=0.25)

    # Panel 1: True posterior (clean contours only)
    ax1 = fig.add_subplot(gs[0, 0])
    levels = np.linspace(Z.max()*0.05, Z.max()*0.95, 10)
    ax1.contour(X, Y, Z, levels=levels, colors=COLORS['primary'],
                alpha=0.6, linewidths=1.5)
    ax1.set_xlabel(r'$\theta_1$', fontsize=15)
    ax1.set_ylabel(r'$\theta_2$', fontsize=15)
    ax1.set_title('Target Distribution (ρ = 0.95)', fontsize=16, pad=12)
    ax1.set_aspect('equal')
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)

    # Panel 2: Metropolis-Hastings (minimal scatter)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.contour(X, Y, Z, levels=levels, colors=COLORS['secondary'],
                alpha=0.3, linewidths=1)

    n_burnin = 2000
    # Show every 10th sample to reduce clutter
    ax2.scatter(samples_mh[n_burnin::10, 0], samples_mh[n_burnin::10, 1],
                c=COLORS['accent1'], s=2, alpha=0.3, label='Samples')

    # First 200 steps as line
    ax2.plot(samples_mh[:200, 0], samples_mh[:200, 1],
             color=COLORS['error'], alpha=0.4, lw=1, label='Early trajectory')

    ax2.scatter(samples_mh[0, 0], samples_mh[0, 1],
                c=COLORS['error'], s=150, marker='*',
                edgecolors=COLORS['primary'], linewidths=2,
                zorder=10, label='Start')

    ax2.set_xlabel(r'$\theta_1$', fontsize=15)
    ax2.set_ylabel(r'$\theta_2$', fontsize=15)
    ax2.set_title(f'Metropolis-Hastings: {accept_mh:.1%} acceptance',
                  fontsize=16, pad=12)
    ax2.set_aspect('equal')
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-3, 3)
    ax2.legend(loc='upper left', fontsize=11, framealpha=0.9)

    # Panel 3: HMC (show trajectories clearly)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.contour(X, Y, Z, levels=levels, colors=COLORS['secondary'],
                alpha=0.3, linewidths=1)

    # Plot first 5 trajectories with distinct colors
    for i, traj in enumerate(trajectories[:5]):
        alpha_val = 0.8 - i * 0.1
        ax3.plot(traj[:, 0], traj[:, 1], '-',
                color=COLORS['accent1'], alpha=alpha_val, lw=2.5)
        ax3.scatter(traj[0, 0], traj[0, 1],
                   color=COLORS['accent1'], s=60, alpha=0.7,
                   edgecolors=COLORS['primary'], linewidths=1)

    # All samples (light)
    ax3.scatter(samples_hmc[::2, 0], samples_hmc[::2, 1],
                c=COLORS['accent2'], s=4, alpha=0.4)

    ax3.scatter(samples_hmc[0, 0], samples_hmc[0, 1],
                c=COLORS['error'], s=150, marker='*',
                edgecolors=COLORS['primary'], linewidths=2,
                zorder=10, label='Start')

    ax3.set_xlabel(r'$\theta_1$', fontsize=15)
    ax3.set_ylabel(r'$\theta_2$', fontsize=15)
    ax3.set_title(f'HMC (L=20): {accept_hmc:.1%} acceptance',
                  fontsize=16, pad=12)
    ax3.set_aspect('equal')
    ax3.set_xlim(-3, 3)
    ax3.set_ylim(-3, 3)
    ax3.text(0.03, 0.97, '5 sample trajectories shown',
             transform=ax3.transAxes, va='top', fontsize=11,
             bbox=dict(boxstyle='round,pad=0.5',
                      facecolor='white', edgecolor=COLORS['secondary'],
                      alpha=0.9))

    # Panel 4: Marginal distributions (clean histograms)
    ax4 = fig.add_subplot(gs[1, 1])

    bins = np.linspace(-3, 3, 40)
    ax4.hist(samples_mh[n_burnin:, 0], bins=bins,
             alpha=0.6, color=COLORS['error'], density=True,
             label='M-H', edgecolor=COLORS['primary'], linewidth=0.5)
    ax4.hist(samples_hmc[:, 0], bins=bins,
             alpha=0.6, color=COLORS['accent1'], density=True,
             label='HMC', edgecolor=COLORS['primary'], linewidth=0.5)

    # True marginal
    x_true = np.linspace(-3, 3, 200)
    ax4.plot(x_true, multivariate_normal.pdf(x_true, 0, 1),
             color=COLORS['primary'], lw=3, label='True distribution',
             linestyle='--')

    ax4.set_xlabel(r'$\theta_1$', fontsize=15)
    ax4.set_ylabel('Density', fontsize=15)
    ax4.set_title('Marginal Distributions', fontsize=16, pad=12)
    ax4.legend(fontsize=12, loc='upper left')
    ax4.set_xlim(-3, 3)

    # Add summary statistics
    textstr = (f'M-H: 10,000 samples\n'
               f'HMC: 1,000 samples\n'
               f'(10× fewer needed)')
    ax4.text(0.98, 0.65, textstr, transform=ax4.transAxes,
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round,pad=0.7',
                      facecolor='white', edgecolor=COLORS['secondary'],
                      alpha=0.9),
             fontsize=12)

    plt.suptitle('Metropolis-Hastings vs Hamiltonian Monte Carlo',
                 fontsize=18, fontweight='bold', y=0.995)

    filename = '04-mod5-part4-fig1-mh-vs-hmc.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filename}")
    plt.close()


# ============================================================================
# FIGURE 2: Grid search (REDESIGNED - cleaner)
# ============================================================================

def create_figure2_parameter_grid():
    """Clean parameter grid with better color scheme."""

    rho = 0.95
    Sigma = np.array([[1, rho], [rho, 1]])
    Sigma_inv = np.linalg.inv(Sigma)
    theta_init = np.array([2.0, 2.0])

    epsilons = np.linspace(0.01, 0.5, 15)
    Ls = np.arange(5, 101, 5)
    n_samples = 2000

    ESS_grid = np.zeros((len(Ls), len(epsilons)))
    accept_grid = np.zeros((len(Ls), len(epsilons)))

    print("Running grid search over (epsilon, L)...")
    print(f"Grid size: {len(epsilons)} × {len(Ls)} = {len(epsilons)*len(Ls)} runs")

    for i, L in enumerate(Ls):
        for j, eps in enumerate(epsilons):
            samples, accept, _ = hmc(
                log_posterior_2d, grad_log_posterior_2d, theta_init,
                epsilon=eps, L=int(L), n_samples=n_samples,
                Sigma_inv=Sigma_inv, seed=42+i*len(epsilons)+j
            )

            ess = estimate_ess(samples[:, 0])
            ESS_grid[i, j] = ess
            accept_grid[i, j] = accept

        print(f"  Completed L={L:.0f} ({i+1}/{len(Ls)})")

    # Create figure - single panel for clarity
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Use grayscale for ESS with blue accent for optimal
    im = ax.contourf(epsilons, Ls, ESS_grid, levels=20,
                     cmap='Greys', alpha=0.7)

    # ESS contours
    contours_ess = ax.contour(epsilons, Ls, ESS_grid, levels=8,
                              colors=COLORS['primary'], linewidths=1.5,
                              alpha=0.5)
    ax.clabel(contours_ess, inline=True, fontsize=10, fmt='%d')

    # Acceptance rate contours (key ones only)
    accept_contours = ax.contour(epsilons, Ls, accept_grid,
                                 levels=[0.5, 0.65, 0.80, 0.95],
                                 colors=COLORS['accent1'],
                                 linewidths=2.5, linestyles='--', alpha=0.8)
    ax.clabel(accept_contours, inline=True, fontsize=11,
              fmt='accept=%.2f', inline_spacing=10)

    # Highlight optimal region
    optimal_threshold = 0.8 * np.max(ESS_grid)
    optimal_region = ESS_grid > optimal_threshold
    if np.any(optimal_region):
        ax.contour(epsilons, Ls, optimal_region, levels=[0.5],
                   colors=COLORS['success'], linewidths=4,
                   linestyles='solid', alpha=0.9)

    ax.set_xlabel('Step Size (ε)', fontsize=16)
    ax.set_ylabel('Trajectory Length (L)', fontsize=16)
    ax.set_title('HMC Parameter Tuning: ESS and Acceptance Rate',
                 fontsize=18, pad=15)

    cbar = plt.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label('Effective Sample Size (ESS)', fontsize=14)
    cbar.ax.tick_params(labelsize=12)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=COLORS['primary'], lw=1.5,
               label='ESS values'),
        Line2D([0], [0], color=COLORS['accent1'], lw=2.5,
               linestyle='--', label='Acceptance rate'),
        Line2D([0], [0], color=COLORS['success'], lw=4,
               label='Optimal region (ESS > 80% max)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right',
              fontsize=12, framealpha=0.95)

    # Clean annotation
    textstr = ('Sweet spot: ε ≈ 0.1-0.2, L ≈ 20-40\n'
               'Target: 65-80% acceptance\n'
               'Maximize ESS for efficiency')
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.8',
                     facecolor='white', edgecolor=COLORS['secondary'],
                     alpha=0.95),
            fontsize=12)

    filename = '04-mod5-part4-fig2-parameter-grid.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filename}")
    plt.close()


# ============================================================================
# FIGURE 3: U-turn criterion (REDESIGNED)
# ============================================================================

def create_figure3_uturn_criterion():
    """Clean U-turn visualization."""

    rho = 0.9
    Sigma = np.array([[1, rho], [rho, 1]])
    Sigma_inv = np.linalg.inv(Sigma)

    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    pos = np.dstack((X, Y))
    rv = multivariate_normal([0, 0], Sigma)
    Z = rv.pdf(pos)

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))

    # Simulate trajectory
    theta_init = np.array([1.5, 1.5])
    p_init = np.array([-1.0, 0.5])
    epsilon = 0.15
    max_steps = 80

    theta = theta_init.copy()
    p = p_init.copy()
    M = np.eye(2)
    M_inv = np.linalg.inv(M)

    trajectory = [theta.copy()]
    momenta = [p.copy()]

    for step in range(max_steps):
        p = p + 0.5 * epsilon * grad_log_posterior_2d(theta, Sigma_inv)
        theta = theta + epsilon * M_inv @ p
        p = p + 0.5 * epsilon * grad_log_posterior_2d(theta, Sigma_inv)
        trajectory.append(theta.copy())
        momenta.append(p.copy())

    trajectory = np.array(trajectory)
    momenta = np.array(momenta)

    uturn_detected = []
    for i in range(len(trajectory)):
        displacement = trajectory[i] - trajectory[0]
        momentum_i = momenta[i]
        dot_product = np.dot(displacement, momentum_i)
        uturn_detected.append(dot_product < 0)

    first_uturn = next((i for i, u in enumerate(uturn_detected) if u), len(trajectory))

    snapshots = [
        (first_uturn // 2, 'Before U-turn'),
        (first_uturn, 'U-turn Detected'),
        (min(first_uturn + 20, len(trajectory)-1), 'After U-turn'),
    ]

    for ax, (time_idx, title) in zip(axes, snapshots):
        # Clean background contours
        levels = np.linspace(Z.max()*0.1, Z.max()*0.9, 8)
        ax.contour(X, Y, Z, levels=levels, colors=COLORS['secondary'],
                   alpha=0.25, linewidths=1)

        # Trajectory (gradient by time)
        traj_subset = trajectory[:time_idx+1]
        colors_time = np.linspace(0.3, 1, len(traj_subset))

        for i in range(len(traj_subset)-1):
            ax.plot(traj_subset[i:i+2, 0], traj_subset[i:i+2, 1],
                   color=COLORS['accent1'], linewidth=2.5,
                   alpha=colors_time[i])

        # Start and current points
        ax.scatter(trajectory[0, 0], trajectory[0, 1],
                  c=COLORS['success'], s=200, marker='o',
                  edgecolors=COLORS['primary'], linewidths=2.5,
                  zorder=10, label='Start')

        ax.scatter(trajectory[time_idx, 0], trajectory[time_idx, 1],
                  c=COLORS['error'], s=200, marker='s',
                  edgecolors=COLORS['primary'], linewidths=2.5,
                  zorder=10, label='Current')

        # Displacement vector
        displacement = trajectory[time_idx] - trajectory[0]
        ax.arrow(trajectory[0, 0], trajectory[0, 1],
                displacement[0]*0.9, displacement[1]*0.9,
                head_width=0.18, head_length=0.12,
                fc=COLORS['primary'], ec=COLORS['primary'],
                linewidth=2.5, alpha=0.7, zorder=5)

        # Momentum vector
        momentum_current = momenta[time_idx]
        momentum_scale = 0.5
        ax.arrow(trajectory[time_idx, 0], trajectory[time_idx, 1],
                momentum_current[0]*momentum_scale,
                momentum_current[1]*momentum_scale,
                head_width=0.18, head_length=0.12,
                fc=COLORS['warning'], ec=COLORS['warning'],
                linewidth=2.5, alpha=0.8, zorder=5)

        # Compute criterion
        dot_prod = np.dot(displacement, momentum_current)
        angle = np.arccos(np.clip(dot_prod / (np.linalg.norm(displacement) *
                                   np.linalg.norm(momentum_current) + 1e-10),
                                   -1, 1))
        angle_deg = np.degrees(angle)

        uturn = dot_prod < 0

        # Clean criterion box
        criterion_text = f'Dot product: {dot_prod:.2f}\n'
        criterion_text += f'Angle: {angle_deg:.0f}°\n'
        criterion_text += f'U-turn: {"YES" if uturn else "NO"}'

        box_color = COLORS['error'] if uturn else COLORS['success']
        ax.text(0.05, 0.97, criterion_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=12, family='monospace',
               bbox=dict(boxstyle='round,pad=0.6',
                        facecolor=box_color, edgecolor=COLORS['primary'],
                        alpha=0.3, linewidth=2))

        ax.set_xlabel(r'$\theta_1$', fontsize=14)
        ax.set_ylabel(r'$\theta_2$', fontsize=14)
        ax.set_title(f'{title} (step {time_idx})', fontsize=15,
                     fontweight='bold', pad=10)
        ax.set_aspect('equal')
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)

        # Minimal legend
        if ax == axes[0]:
            ax.legend(loc='lower right', fontsize=11, framealpha=0.9)

    # Clean title
    plt.suptitle('NUTS U-turn Detection: When to Stop',
                 fontsize=18, fontweight='bold', y=1.00)

    # Simplified explanation
    explanation = (r'$(θ_t - θ_0) · p_t < 0$ means trajectory is doubling back → stop to avoid waste')
    fig.text(0.5, -0.01, explanation, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.7',
                     facecolor='white', edgecolor=COLORS['secondary'],
                     alpha=0.9),
            fontsize=13)

    filename = '04-mod5-part4-fig3-uturn-criterion.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filename}")
    plt.close()


# ============================================================================
# BONUS FIGURE: Energy conservation (REDESIGNED)
# ============================================================================

def create_bonus_figure_energy_conservation():
    """Clean energy diagnostic."""

    rho = 0.95
    Sigma = np.array([[1, rho], [rho, 1]])
    Sigma_inv = np.linalg.inv(Sigma)
    theta_init = np.array([2.0, 2.0])

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    epsilons_test = [0.05, 0.15, 0.3, 0.6]
    L = 20
    n_samples = 500

    for idx, eps in enumerate(epsilons_test):
        np.random.seed(42)
        theta = theta_init.copy()
        M = np.eye(2)
        M_inv = np.linalg.inv(M)

        delta_H_values = []

        for i in range(n_samples):
            p = np.random.multivariate_normal(np.zeros(2), M)
            p_old = p.copy()
            theta_old = theta.copy()

            theta_new, p_new = leapfrog(theta, p, eps, L,
                                       grad_log_posterior_2d, Sigma_inv, M_inv)

            H_old = hamiltonian(theta_old, p_old, log_posterior_2d, Sigma_inv, M_inv)
            H_new = hamiltonian(theta_new, p_new, log_posterior_2d, Sigma_inv, M_inv)
            delta_H = H_new - H_old
            delta_H_values.append(delta_H)

            if np.log(np.random.rand()) < -delta_H:
                theta = theta_new
            else:
                theta = theta_old

        delta_H_values = np.array(delta_H_values)

        ax = axes[idx // 2, idx % 2]

        # Clean histogram
        ax.hist(delta_H_values, bins=40, alpha=0.7,
                color=COLORS['accent1'], edgecolor=COLORS['primary'],
                linewidth=1)

        # Reference lines
        ax.axvline(0, color=COLORS['primary'], linestyle='--',
                   linewidth=2.5, label='ΔH = 0', zorder=10)
        ax.axvline(np.mean(delta_H_values), color=COLORS['error'],
                   linestyle='--', linewidth=2,
                   label=f'Mean = {np.mean(delta_H_values):.3f}')

        # Quality assessment
        mean_abs = np.mean(np.abs(delta_H_values))
        if mean_abs < 0.1:
            quality = 'Excellent'
            box_color = COLORS['success']
        elif mean_abs < 0.5:
            quality = 'Good'
            box_color = COLORS['warning']
        else:
            quality = 'Poor'
            box_color = COLORS['error']

        stats_text = f'ε = {eps:.2f}, L = {L}\n'
        stats_text += f'Mean |ΔH|: {mean_abs:.3f}\n'
        stats_text += f'Std(ΔH): {np.std(delta_H_values):.3f}\n'
        stats_text += f'Quality: {quality}'

        ax.text(0.97, 0.97, stats_text, transform=ax.transAxes,
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.7',
                        facecolor=box_color, edgecolor=COLORS['primary'],
                        alpha=0.25, linewidth=2),
               fontsize=12, family='monospace')

        ax.set_xlabel(r'$\Delta H = H(\theta^*, p^*) - H(\theta, p)$',
                      fontsize=13)
        ax.set_ylabel('Frequency', fontsize=13)
        ax.set_title(f'Step Size ε = {eps:.2f}', fontsize=14, pad=10)
        ax.legend(fontsize=11)

    plt.suptitle('HMC Diagnostic: Hamiltonian Conservation',
                 fontsize=18, fontweight='bold')

    explanation = ('Small |ΔH| → good leapfrog integration → high acceptance\n'
                  'Large |ΔH| → poor integration → rejections')
    fig.text(0.5, -0.01, explanation, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.7',
                     facecolor='white', edgecolor=COLORS['secondary'],
                     alpha=0.9),
            fontsize=13)

    filename = '04-mod5-part4-bonus-energy-conservation.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filename}")
    plt.close()


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Generating HMC Pedagogical Figures (Modern Minimalist Design)")
    print("=" * 70)
    print()

    print("Figure 1: M-H vs HMC comparison...")
    create_figure1_mh_vs_hmc()
    print()

    print("Figure 2: Parameter grid search...")
    create_figure2_parameter_grid()
    print()

    print("Figure 3: U-turn criterion...")
    create_figure3_uturn_criterion()
    print()

    print("Bonus: Energy conservation diagnostic...")
    create_bonus_figure_energy_conservation()
    print()

    print("=" * 70)
    print("All figures generated successfully!")
    print("=" * 70)
