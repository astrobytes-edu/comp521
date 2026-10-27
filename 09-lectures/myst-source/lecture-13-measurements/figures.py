"""Reproducible illustrative figures for Lecture 13; no observational data."""
from math import comb
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / 'assets'
OUT.mkdir(exist_ok=True)
INK = '#20394d'
TEAL = '#087e81'
GOLD = '#d59831'
BLUE = '#486d9f'
RED = '#b54844'
plt.rcParams.update({'font.size': 17, 'axes.titlesize': 20, 'axes.labelsize': 18,
                     'xtick.labelsize': 15, 'ytick.labelsize': 15,
                     'text.color': INK, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def save(name):
    plt.savefig(OUT / name, dpi=150, bbox_inches='tight')
    plt.close()

# A schematic box-shaped transit, not a fit to observations.
rng = np.random.default_rng(521)
t = np.linspace(-2, 2, 55)
model = 1.0 - 0.018 * (np.abs(t) < 0.47)
y = model + rng.normal(0, 0.003, t.size)
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.scatter(t, y, color=TEAL, s=30, alpha=.85, label='Synthetic measurements')
ax.step(t, model, color=GOLD, lw=3, where='mid', label='Illustrative model')
ax.set(xlabel='Time relative to transit (arbitrary units)', ylabel='Normalized flux', ylim=(.970, 1.013))
ax.legend(frameon=False, loc='lower left', fontsize=14)
ax.grid(alpha=.15)
save('synthetic-transit.png')

# Exact binomial probabilities and Gaussian approximation for K/100.
n = 100
k = np.arange(n + 1)
p = np.array([comb(n, int(i)) / 2**n for i in k])
x = k / n
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar(x, p, width=.0085, color=TEAL, alpha=.8, label='Exact binomial probability')
z = np.linspace(.3, .7, 600)
normal_per_bin = np.exp(-.5*((z-.5)/.05)**2) / (np.sqrt(2*np.pi)*.05) / n
ax.plot(z, normal_per_bin, color=GOLD, lw=3.5, label='Gaussian density × bin width')
ax.axvline(.5, color=INK, lw=1, ls='--', alpha=.65)
ax.set(xlim=(.30,.70), xlabel='Fraction of 1s in a sample of 100', ylabel='Probability per 0.01 bin')
ax.legend(frameon=False, fontsize=13, loc='upper left')
ax.grid(axis='y', alpha=.15)
save('clt-sample-means.png')

# Orthogonal projection in equal-unit, normalized-band feature coordinates.
fig, ax = plt.subplots(figsize=(7, 5.8))
ax.plot([0, 1.45], [0, 1.45], color=BLUE, lw=2.5, label='Equal-band direction')
ax.annotate('', xy=(.9, 1.1), xytext=(0, 0), arrowprops={'arrowstyle':'->','lw':3,'color':TEAL})
ax.annotate('', xy=(1., 1.), xytext=(0, 0), arrowprops={'arrowstyle':'->','lw':3,'color':GOLD})
ax.annotate('', xy=(.9, 1.1), xytext=(1., 1.), arrowprops={'arrowstyle':'->','lw':3,'color':RED})
ax.scatter([.9,1.], [1.1,1.], color=[TEAL,GOLD], s=75, zorder=3)
ax.annotate('original (0.9, 1.1)', (.9,1.1), xytext=(-175,25), textcoords='offset points', color=TEAL)
ax.annotate('projection (1.0, 1.0)', (1.,1.), xytext=(18,-28), textcoords='offset points', color='#9b6617')
ax.annotate('difference', (.95,1.05), xytext=(15,30), textcoords='offset points', color=RED)
ax.set(xlim=(0,1.45), ylim=(0,1.45), xlabel='Normalized flux: band A', ylabel='Normalized flux: band B')
ax.set_aspect('equal'); ax.grid(alpha=.15)
save('band-projection.png')

# Two measurements: plotted bars represent exactly one stated standard deviation.
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.errorbar([.980,1.000], [2,1], xerr=[.010,.020], fmt='o', markersize=10, capsize=6, color=TEAL, lw=2.5)
ax.axvline(.984, color=GOLD, lw=3, label='Weighted mean = 0.984')
ax.axvline(.990, color=BLUE, lw=2, ls='--', label='Unweighted mean = 0.990')
ax.set(yticks=[1,2], yticklabels=['Measurement 2','Measurement 1'], xlabel='Normalized brightness', xlim=(.955,1.035), ylim=(.5,2.5))
ax.legend(frameon=False, fontsize=14, loc='lower right'); ax.grid(axis='x', alpha=.15)
save('weighted-measurements.png')

# Three deterministic pair patterns show covariance rather than observational data.
base = np.array([-2., -1., 0., 1., 2.])
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharex=True, sharey=True)
for ax, yy, title, color in zip(axes, [base, -base, base**2 - 2], ['Positive', 'Negative', 'Zero, but dependent'], [TEAL, BLUE, GOLD]):
    ax.scatter(base, yy, s=70, color=color)
    ax.axhline(0, color=INK, lw=1, alpha=.35); ax.axvline(0, color=INK, lw=1, alpha=.35)
    ax.set_title(title); ax.set_xlabel('X (centered)'); ax.grid(alpha=.12)
axes[0].set_ylabel('Y (centered)')
fig.tight_layout()
save('covariance-patterns.png')
