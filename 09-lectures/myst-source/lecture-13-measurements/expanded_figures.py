"""Figures for the transit fitting and covariance derivations in Lecture 13."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

OUT = Path(__file__).resolve().parent / 'assets'
INK, TEAL, BLUE, GOLD, RED = '#20394d', '#087e81', '#486d9f', '#d59831', '#b54844'
plt.rcParams.update({'font.size': 20, 'axes.titlesize': 22, 'axes.labelsize': 21,
    'xtick.labelsize': 18, 'ytick.labelsize': 18, 'text.color': INK,
    'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def save(name):
    plt.savefig(OUT / name, dpi=150, bbox_inches='tight')
    plt.close()

# Four measurements and three candidate depths; timing and baseline are fixed.
t = np.array([0.,1.,2.,3.]); y = np.array([1.,.98,.99,1.]); template = np.array([0.,1.,1.,0.])
fig, ax = plt.subplots(figsize=(8.5,4.5))
for depth,color,label in ((.005,BLUE,'0.5% depth'),(.015,TEAL,'1.5% depth'),(.025,GOLD,'2.5% depth')):
    ax.step(t, 1-depth*template, where='mid', color=color, lw=3, label=label)
ax.scatter(t, y, c=INK, s=100, marker='o', edgecolors='white', linewidths=1.5, zorder=5, label='Measurements')
ax.set(xlabel='Observation index', ylabel='Normalized flux', xticks=t, ylim=(.968,1.006))
ax.legend(frameon=False, fontsize=16, ncol=2, loc='lower right'); ax.grid(alpha=.15)
save('candidate-transit-depths.png')

# The residual uses y minus the prediction at each measurement time.
fit = 1-.015*template; residual = y-fit
fig, axes = plt.subplots(2, 1, figsize=(9,6.1), sharex=True, gridspec_kw={'height_ratios':[2,1]})
axes[0].step(t,fit,where='mid',color=TEAL,lw=3,label='Best-fitting model')
axes[0].scatter(t,y,c=INK,s=85,zorder=4,label='Measurements')
for ti, yi, mi in zip(t,y,fit): axes[0].plot([ti,ti],[yi,mi],color=RED,lw=2.5)
axes[0].set(ylabel='Normalized flux',ylim=(.974,1.006)); axes[0].legend(frameon=False,fontsize=16,loc='lower right')
axes[1].axhline(0,color=INK,lw=1); axes[1].scatter(t,residual,c=RED,s=75,zorder=3)
axes[1].vlines(t,0,residual,color=RED,lw=2); axes[1].set(xlabel='Observation index',ylabel='Residual',ylim=(-.008,.008),xticks=t)
for ax in axes: ax.grid(alpha=.13)
fig.tight_layout()
save('transit-fit-residuals.png')

# The paired observations on the slide: means zero, covariance 4/3, r=4/sqrt(20).
x = np.array([-1.5,-.5,.5,1.5]); yy = np.array([-1.,-1.,1.,1.])
fig, ax=plt.subplots(figsize=(7,5))
ax.scatter(x,yy,color=TEAL,s=125,edgecolors='white',linewidths=1.5,zorder=5)
for i,(xx,yv) in enumerate(zip(x,yy),1): ax.annotate(str(i),(xx,yv),xytext=(9,8),textcoords='offset points',fontsize=19,color=INK)
ax.axvline(0,color=INK,lw=1,alpha=.45); ax.axhline(0,color=INK,lw=1,alpha=.45)
ax.set(xlabel='X deviation from mean',ylabel='Y deviation from mean',xlim=(-2,2),ylim=(-1.7,1.7)); ax.grid(alpha=.15)
save('correlation-pairs.png')

# Analytical covariance ellipse: x/y covariance [[4,3],[3,9]].
C=np.array([[4.,3.],[3.,9.]])
values,vectors=np.linalg.eigh(C); order=np.argsort(values)[::-1]; values=values[order]; vectors=vectors[:,order]
angle=np.degrees(np.arctan2(vectors[1,0],vectors[0,0]))
fig, ax=plt.subplots(figsize=(7,5.7))
ax.add_patch(Ellipse((0,0),2*np.sqrt(values[0]),2*np.sqrt(values[1]),angle=angle,facecolor='#d7eeec',edgecolor=TEAL,lw=3))
ax.axvline(0,color=INK,lw=1,alpha=.5); ax.axhline(0,color=INK,lw=1,alpha=.5)
ax.set(xlim=(-5.5,5.5),ylim=(-6.5,6.5),xlabel='X deviation',ylabel='Y deviation')
ax.set_aspect('equal'); ax.grid(alpha=.15)
save('covariance-ellipse.png')

# Compare standard deviations of combinations at rho=0.5 and rho=0.
fig, ax=plt.subplots(figsize=(9,4.8))
ys=np.array([2,1]); correlated=np.sqrt([19,7]); independent=np.sqrt(13)
ax.errorbar([0,0],ys,xerr=correlated,fmt='o',color=TEAL,lw=3,capsize=6,markersize=8,label='Correlation = 0.5')
ax.errorbar([0,0],ys-.19,xerr=[independent,independent],fmt='o',color=BLUE,lw=2,capsize=6,markersize=6,label='Correlation = 0')
ax.set(xlim=(-5.4,5.4),ylim=(.45,2.45),yticks=[1,2],yticklabels=['Difference X − Y','Sum X + Y'],xlabel='Deviation from combination mean')
ax.legend(frameon=False,fontsize=13,loc='upper center',bbox_to_anchor=(.5,1.18),ncol=2); ax.grid(axis='x',alpha=.15)
save('sum-difference-uncertainty.png')
print('Created five lecture figures.')
