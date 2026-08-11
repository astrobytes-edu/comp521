"""
Visualization script for Module 5 Part 4: HMC vs Metropolis-Hastings
Generates figures comparing random walk M-H with HMC on the twisted Gaussian

Author: ASTR 596 Course Materials
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import multivariate_normal
import matplotlib.patches as mpatches

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.titlesize': 18,
    'lines.linewidth': 2
})

# Define twisted Gaussian parameters
rho = 0.95  # Strong correlation
cov_matrix = np.array([[1, rho], [rho, 1]])
mean = np.array([0, 0])

def log_posterior_twisted_gaussian(theta):
    """Log-posterior for twisted Gaussian."""
    return multivariate_normal.logpdf(theta, mean=mean, cov=cov_matrix)

def grad_log_posterior_twisted_gaussian(theta):
    """Gradient of log-posterior (finite differences)."""
    h = 1e-6
    d = len(theta)
    grad = np.zeros(d)
    for i in range(d):
        theta_plus = theta.copy()
        theta_minus = theta.copy()
        theta_plus[i] += h
        theta_minus[i] -= h
        grad[i] = (log_posterior_twisted_gaussian(theta_plus) - 
                   log_posterior_twisted_gaussian(theta_minus)) / (2*h)
    return grad

def metropolis_hastings_2d(n_samples, sigma_prop=0.1):
    """Random walk Metropolis-Hastings."""
    samples = np.zeros((n_samples, 2))
    theta = np.array([2.0, 2.0])  # Start far from mode
    n_accepted = 0
    
    for i in range(n_samples):
        # Propose
        theta_prop = theta + np.random.randn(2) * sigma_prop
        
        # Accept/reject
        log_ratio = (log_posterior_twisted_gaussian(theta_prop) - 
                     log_posterior_twisted_gaussian(theta))
        if np.log(np.random.rand()) < log_ratio:
            theta = theta_prop
            n_accepted += 1
        
        samples[i] = theta
    
    acceptance_rate = n_accepted / n_samples
    return samples, acceptance_rate

def leapfrog_step(theta, p, epsilon, grad_fn):
    """Single leapfrog step."""
    # Half-step momentum
    p = p + (epsilon/2) * grad_fn(theta)
    # Full-step position
    theta = theta + epsilon * p
    # Half-step momentum
    p = p + (epsilon/2) * grad_fn(theta)
    return theta, p

def hamiltonian_monte_carlo_2d(n_samples, epsilon=0.05, L=20):
    """Hamiltonian Monte Carlo."""
    samples = np.zeros((n_samples, 2))
    theta = np.array([2.0, 2.0])  # Start far from mode
    n_accepted = 0
    delta_H_history = []
    
    for i in range(n_samples):
        # Sample momentum
        p = np.random.randn(2)
        
        # Store initial state
        theta_old = theta.copy()
        p_old = p.copy()
        H_old = -log_posterior_twisted_gaussian(theta_old) + 0.5 * np.sum(p_old**2)
        
        # Leapfrog integration
        theta_new = theta_old.copy()
        p_new = p_old.copy()
        
        for _ in range(L):
            theta_new, p_new = leapfrog_step(theta_new, p_new, epsilon, 
                                             grad_log_posterior_twisted_gaussian)
        
        # Negate momentum
        p_new = -p_new
        
        # Compute Hamiltonian change
        H_new = -log_posterior_twisted_gaussian(theta_new) + 0.5 * np.sum(p_new**2)
        delta_H = H_new - H_old
        delta_H_history.append(delta_H)
        
        # Metropolis acceptance
        if np.random.rand() < np.exp(-delta_H):
            theta = theta_new
            n_accepted += 1
        
        samples[i] = theta
    
    acceptance_rate = n_accepted / n_samples
    return samples, acceptance_rate, np.array(delta_H_history)

def compute_autocorrelation(chain, max_lag=100):
    """Compute autocorrelation function."""
    n = len(chain)
    mean = np.mean(chain)
    var = np.var(chain)
    
    acf = np.zeros(max_lag)
    for lag in range(max_lag):
        if lag < n:
            c = np.mean((chain[:n-lag] - mean) * (chain[lag:] - mean))
            acf[lag] = c / var
    
    return acf

def effective_sample_size(chain, max_lag=100):
    """Compute effective sample size."""
    acf = compute_autocorrelation(chain, max_lag)
    # Sum until ACF becomes negligible
    tau = 1 + 2 * np.sum(acf[1:][acf[1:] > 0.05])
    ess = len(chain) / tau
    return ess, tau

# Generate samples
print("Generating Metropolis-Hastings samples...")
mh_samples, mh_accept = metropolis_hastings_2d(10000, sigma_prop=0.15)
print(f"M-H Acceptance rate: {mh_accept:.1%}")

print("Generating HMC samples...")
hmc_samples, hmc_accept, delta_H = hamiltonian_monte_carlo_2d(2000, epsilon=0.05, L=20)
print(f"HMC Acceptance rate: {hmc_accept:.1%}")

# Compute ESS
mh_ess_1, mh_tau_1 = effective_sample_size(mh_samples[:, 0])
mh_ess_2, mh_tau_2 = effective_sample_size(mh_samples[:, 1])
hmc_ess_1, hmc_tau_1 = effective_sample_size(hmc_samples[:, 0])
hmc_ess_2, hmc_tau_2 = effective_sample_size(hmc_samples[:, 1])

print(f"\nM-H ESS (θ₁): {mh_ess_1:.0f}, τ: {mh_tau_1:.1f}")
print(f"M-H ESS (θ₂): {mh_ess_2:.0f}, τ: {mh_tau_2:.1f}")
print(f"HMC ESS (θ₁): {hmc_ess_1:.0f}, τ: {hmc_tau_1:.1f}")
print(f"HMC ESS (θ₂): {hmc_ess_2:.0f}, τ: {hmc_tau_2:.1f}")

# ==============================================================================
# FIGURE 1: 2D Posterior with Trajectories
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Create grid for contour
x = np.linspace(-3, 3, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
Z = multivariate_normal.pdf(pos, mean=mean, cov=cov_matrix)

# M-H trajectories
ax1.contour(X, Y, Z, levels=10, colors='gray', alpha=0.4, linewidths=1)
ax1.contourf(X, Y, Z, levels=20, cmap='Blues', alpha=0.6)

# Plot every 10th sample to avoid clutter
skip = 10
ax1.plot(mh_samples[::skip, 0], mh_samples[::skip, 1], 'o-', 
         color='red', markersize=3, alpha=0.5, linewidth=0.5, label='M-H trajectory')
ax1.plot(mh_samples[0, 0], mh_samples[0, 1], 'g*', markersize=15, 
         label='Start', markeredgecolor='black')
ax1.set_xlabel('θ₁', fontsize=14)
ax1.set_ylabel('θ₂', fontsize=14)
ax1.set_title('Metropolis-Hastings (Random Walk)\n' + 
              f'Acceptance: {mh_accept:.1%}, ESS: {mh_ess_1:.0f}, τ: {mh_tau_1:.1f}',
              fontsize=14, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-3, 3)
ax1.set_ylim(-3, 3)

# HMC trajectories
ax2.contour(X, Y, Z, levels=10, colors='gray', alpha=0.4, linewidths=1)
ax2.contourf(X, Y, Z, levels=20, cmap='Blues', alpha=0.6)

# Plot every 2nd sample (HMC takes bigger steps)
skip = 2
ax2.plot(hmc_samples[::skip, 0], hmc_samples[::skip, 1], 'o-', 
         color='orange', markersize=3, alpha=0.6, linewidth=0.5, label='HMC trajectory')
ax2.plot(hmc_samples[0, 0], hmc_samples[0, 1], 'g*', markersize=15, 
         label='Start', markeredgecolor='black')
ax2.set_xlabel('θ₁', fontsize=14)
ax2.set_ylabel('θ₂', fontsize=14)
ax2.set_title('Hamiltonian Monte Carlo (Ballistic)\n' + 
              f'Acceptance: {hmc_accept:.1%}, ESS: {hmc_ess_1:.0f}, τ: {hmc_tau_1:.1f}',
              fontsize=14, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-3, 3)
ax2.set_ylim(-3, 3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/fig1_trajectories_comparison.png', dpi=300, bbox_inches='tight')
print("\nSaved: fig1_trajectories_comparison.png")

# ==============================================================================
# FIGURE 2: Trace Plots Comparison
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# M-H trace plots
axes[0, 0].plot(mh_samples[:2000, 0], linewidth=0.8, color='darkred', alpha=0.7)
axes[0, 0].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 0].set_ylabel('θ₁', fontsize=13)
axes[0, 0].set_title('Metropolis-Hastings: θ₁ Trace', fontsize=13, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

axes[1, 0].plot(mh_samples[:2000, 1], linewidth=0.8, color='darkred', alpha=0.7)
axes[1, 0].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
axes[1, 0].set_xlabel('Iteration', fontsize=13)
axes[1, 0].set_ylabel('θ₂', fontsize=13)
axes[1, 0].set_title('Metropolis-Hastings: θ₂ Trace', fontsize=13, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# HMC trace plots
axes[0, 1].plot(hmc_samples[:2000, 0], linewidth=0.8, color='darkorange', alpha=0.7)
axes[0, 1].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 1].set_ylabel('θ₁', fontsize=13)
axes[0, 1].set_title('HMC: θ₁ Trace (looks like noise = good!)', 
                     fontsize=13, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 1].plot(hmc_samples[:2000, 1], linewidth=0.8, color='darkorange', alpha=0.7)
axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
axes[1, 1].set_xlabel('Iteration', fontsize=13)
axes[1, 1].set_ylabel('θ₂', fontsize=13)
axes[1, 1].set_title('HMC: θ₂ Trace (looks like noise = good!)', 
                     fontsize=13, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/fig2_trace_plots_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: fig2_trace_plots_comparison.png")

# ==============================================================================
# FIGURE 3: Autocorrelation Functions
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# M-H ACF
max_lag = 100
mh_acf_1 = compute_autocorrelation(mh_samples[:, 0], max_lag)
mh_acf_2 = compute_autocorrelation(mh_samples[:, 1], max_lag)

ax1.plot(mh_acf_1, 'o-', color='darkred', label='θ₁', markersize=4, linewidth=2)
ax1.plot(mh_acf_2, 's-', color='darkblue', label='θ₂', markersize=4, linewidth=2)
ax1.axhline(0, color='black', linestyle='--', linewidth=1)
ax1.axhline(0.05, color='gray', linestyle=':', linewidth=1, 
            label='Negligible threshold')
ax1.set_xlabel('Lag', fontsize=13)
ax1.set_ylabel('Autocorrelation', fontsize=13)
ax1.set_title(f'Metropolis-Hastings ACF\nτ₁ ≈ {mh_tau_1:.0f}, τ₂ ≈ {mh_tau_2:.0f}', 
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(-0.1, 1.05)

# HMC ACF
hmc_acf_1 = compute_autocorrelation(hmc_samples[:, 0], max_lag)
hmc_acf_2 = compute_autocorrelation(hmc_samples[:, 1], max_lag)

ax2.plot(hmc_acf_1, 'o-', color='darkorange', label='θ₁', markersize=4, linewidth=2)
ax2.plot(hmc_acf_2, 's-', color='purple', label='θ₂', markersize=4, linewidth=2)
ax2.axhline(0, color='black', linestyle='--', linewidth=1)
ax2.axhline(0.05, color='gray', linestyle=':', linewidth=1, 
            label='Negligible threshold')
ax2.set_xlabel('Lag', fontsize=13)
ax2.set_ylabel('Autocorrelation', fontsize=13)
ax2.set_title(f'HMC ACF (Much faster decay!)\nτ₁ ≈ {hmc_tau_1:.0f}, τ₂ ≈ {hmc_tau_2:.0f}', 
              fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(-0.1, 1.05)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/fig3_autocorrelation_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: fig3_autocorrelation_comparison.png")

# ==============================================================================
# FIGURE 4: HMC Energy Conservation
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Delta H over iterations
ax1.plot(delta_H, linewidth=0.8, color='teal', alpha=0.7)
ax1.axhline(0, color='red', linestyle='--', linewidth=2, label='Perfect conservation')
ax1.axhline(1, color='orange', linestyle=':', linewidth=2, alpha=0.7, 
            label='ΔH = 1 (high acceptance threshold)')
ax1.axhline(-1, color='orange', linestyle=':', linewidth=2, alpha=0.7)
ax1.set_ylabel('ΔH (Energy Error)', fontsize=13)
ax1.set_title('HMC Energy Conservation Check\n' + 
              f'Mean |ΔH|: {np.mean(np.abs(delta_H)):.3f}, ' + 
              f'Std(ΔH): {np.std(delta_H):.3f}',
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Histogram of Delta H
ax2.hist(delta_H, bins=50, color='teal', alpha=0.7, edgecolor='black', density=True)
ax2.axvline(0, color='red', linestyle='--', linewidth=2, label='ΔH = 0')
ax2.set_xlabel('ΔH', fontsize=13)
ax2.set_ylabel('Density', fontsize=13)
ax2.set_title('Distribution of Energy Errors\n(Should be concentrated near 0)', 
              fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/fig4_hmc_energy_conservation.png', dpi=300, bbox_inches='tight')
print("Saved: fig4_hmc_energy_conservation.png")

# ==============================================================================
# FIGURE 5: Corner Plot Style Comparison
# ==============================================================================

fig = plt.figure(figsize=(16, 7))

# M-H corner plot
ax1 = plt.subplot(1, 2, 1)
# Use burn-in
burnin = 1000
ax1.hexbin(mh_samples[burnin:, 0], mh_samples[burnin:, 1], 
           gridsize=30, cmap='Reds', alpha=0.7)
ax1.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=1)
ax1.set_xlabel('θ₁', fontsize=13)
ax1.set_ylabel('θ₂', fontsize=13)
ax1.set_title(f'M-H: {len(mh_samples)-burnin} samples\nESS ~ {mh_ess_1:.0f} (efficiency: {mh_ess_1/(len(mh_samples)-burnin):.1%})', 
              fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-3, 3)
ax1.set_ylim(-3, 3)

# HMC corner plot
ax2 = plt.subplot(1, 2, 2)
burnin_hmc = 200
ax2.hexbin(hmc_samples[burnin_hmc:, 0], hmc_samples[burnin_hmc:, 1], 
           gridsize=30, cmap='Oranges', alpha=0.7)
ax2.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=1)
ax2.set_xlabel('θ₁', fontsize=13)
ax2.set_ylabel('θ₂', fontsize=13)
ax2.set_title(f'HMC: {len(hmc_samples)-burnin_hmc} samples\nESS ~ {hmc_ess_1:.0f} (efficiency: {hmc_ess_1/(len(hmc_samples)-burnin_hmc):.1%})', 
              fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-3, 3)
ax2.set_ylim(-3, 3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/fig5_corner_plot_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: fig5_corner_plot_comparison.png")

print("\n" + "="*60)
print("All figures generated successfully!")
print("="*60)
print("\nFigure Summary:")
print("  1. fig1_trajectories_comparison.png - 2D posterior with M-H vs HMC paths")
print("  2. fig2_trace_plots_comparison.png - Time series showing mixing quality")
print("  3. fig3_autocorrelation_comparison.png - ACF decay comparison")
print("  4. fig4_hmc_energy_conservation.png - HMC energy diagnostic")
print("  5. fig5_corner_plot_comparison.png - Density estimates comparison")
print("\nKey Results:")
print(f"  M-H: τ ~ {mh_tau_1:.0f}, ESS ~ {mh_ess_1:.0f}, Acceptance: {mh_accept:.1%}")
print(f"  HMC: τ ~ {hmc_tau_1:.0f}, ESS ~ {hmc_ess_1:.0f}, Acceptance: {hmc_accept:.1%}")
print(f"  Efficiency gain: {(hmc_ess_1/hmc_tau_1)/(mh_ess_1/mh_tau_1):.0f}× better!")
