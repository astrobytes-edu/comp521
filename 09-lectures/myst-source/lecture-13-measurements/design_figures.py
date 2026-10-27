"""Figures for the Lecture 13 visual explanations."""
from math import comb, pi, sqrt
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / 'assets'
INK, TEAL, BLUE, GOLD, RED = '#20394d', '#087e81', '#486d9f', '#d59831', '#b54844'
plt.rcParams.update({'font.size': 17, 'axes.labelsize': 18, 'axes.titlesize': 19,
    'xtick.labelsize': 14, 'ytick.labelsize': 14, 'text.color': INK,
    'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def save(name):
    plt.savefig(OUT / name, dpi=150, bbox_inches='tight')
    plt.close()

# The direction of the scientific reasoning, not a numerical calculation.
fig, ax = plt.subplots(figsize=(12,4.2)); ax.set_xlim(0,14); ax.set_ylim(0,4.6); ax.axis('off')
for x,y,label,color in [(0.2,2.7,'Physical\nparameters','#eaf4f3'),(3.6,2.7,'Forward\nmodel','#eef0f8'),(7.0,2.7,'Predicted\nflux','#fff5e5'),(10.4,2.7,'Compare','#eaf4f3'),(10.4,.35,'Observed\nflux','#eef0f8')]:
    ax.add_patch(FancyBboxPatch((x,y),2.65,1.2,boxstyle='round,pad=0.06,rounding_size=.12',facecolor=color,edgecolor=TEAL,lw=2))
    ax.text(x+1.325,y+.6,label,ha='center',va='center',fontsize=18,weight='semibold')
for a,b in [(2.95,3.45),(6.35,6.85),(9.75,10.25)]:
    ax.add_patch(FancyArrowPatch((a,3.3),(b,3.3),arrowstyle='-|>',mutation_scale=20,lw=2.5,color=TEAL))
ax.add_patch(FancyArrowPatch((11.725,1.65),(11.725,2.55),arrowstyle='-|>',mutation_scale=20,lw=2.5,color=GOLD))
ax.text(5.4,.85,'Adjust parameters to improve the match',ha='center',fontsize=17,color=INK)
save('forward-inverse-flow.png')

# Gaussian is an example density; shaded area is an interval probability.
x=np.linspace(-3.3,3.3,900); y=np.exp(-x*x/2)/sqrt(2*pi)
fig,ax=plt.subplots(figsize=(8,4.6)); ax.plot(x,y,color=BLUE,lw=3.5)
mask=(x>=-.8)&(x<=1.2); ax.fill_between(x[mask],y[mask],color=TEAL,alpha=.35)
ax.axvline(-.8,color=TEAL,ls='--',lw=2); ax.axvline(1.2,color=TEAL,ls='--',lw=2)
ax.set(xlabel='Measurement',ylabel='Probability density',xticks=[-.8,1.2],xticklabels=['a','b'],ylim=(0,.45))
ax.text(.2,.10,'interval probability',ha='center',color='#075f62',fontsize=17); ax.grid(axis='y',alpha=.12)
save('density-interval.png')

# Exact binomial distributions of sample means; each panel has its own y-axis scale.
fig,axes=plt.subplots(1,3,figsize=(12,4),sharex=True)
for ax,n in zip(axes,(1,4,100)):
    k=np.arange(n+1); p=np.array([comb(n,int(i))/2**n for i in k]); x=k/n
    ax.bar(x,p,width=.65/n if n>1 else .1,color=TEAL,alpha=.84)
    ax.set_xlim(-.06,1.06); ax.set_title(f'{n} outcome' if n==1 else f'{n} outcomes')
    ax.set_xlabel('Sample mean'); ax.set_xticks([0,.5,1]); ax.grid(axis='y',alpha=.12)
axes[0].set_ylabel('Probability'); fig.tight_layout()
save('clt-three-samples.png')

# Shared drift adds to both otherwise distinct measurements.
t=np.arange(8); common=np.array([-.3,-.1,.05,.34,.22,-.02,-.23,.02]); x=common+np.array([.04,-.03,.03,.02,-.04,.05,-.03,-.04]); y=common+np.array([-.04,.03,-.03,-.02,.04,-.05,.03,.04])
fig,ax=plt.subplots(figsize=(9,4.5)); ax.plot(t,x,'o-',color=TEAL,lw=2.5,label='Measurement X'); ax.plot(t,y,'s-',color=BLUE,lw=2.5,label='Measurement Y')
ax.set(xlabel='Observation time',ylabel='Deviation from baseline',xticks=t); ax.axhline(0,color=INK,lw=1,alpha=.4); ax.grid(alpha=.15); ax.legend(frameon=False,ncol=2,fontsize=14)
save('shared-drift.png')

# Relative likelihoods for the same two observations used in the deck.
mu=np.linspace(.945,1.035,700); q1=np.exp(-.5*((mu-.980)/.010)**2); q2=np.exp(-.5*((mu-1.000)/.020)**2)
qjoint=q1*q2; qjoint/=qjoint.max()
fig,ax=plt.subplots(figsize=(9,4.5)); ax.plot(mu,q1,color=BLUE,lw=2.3,label='Measurement 1'); ax.plot(mu,q2,color=GOLD,lw=2.3,label='Measurement 2'); ax.plot(mu,qjoint,color=TEAL,lw=4,label='Joint likelihood')
ax.axvline(.984,color=TEAL,ls='--',lw=1.8); ax.set(xlabel='Candidate brightness',ylabel='Relative likelihood',ylim=(0,1.12))
ax.legend(frameon=False,ncol=3,fontsize=15,loc='lower center',bbox_to_anchor=(.5,1.02)); ax.grid(alpha=.15)
save('likelihood-comparison.png')

# Each row of a matrix makes one linear combination of two inputs.
fig,ax=plt.subplots(figsize=(9,4.6)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
for x,y,label,color in [(1,4,'input 1',TEAL),(1,1,'input 2',BLUE),(8,4,'output 1',TEAL),(8,1,'output 2',BLUE)]:
    ax.add_patch(FancyBboxPatch((x,y),1.6,.8,boxstyle='round,pad=0.1',facecolor='#eff7f6' if color==TEAL else '#edf1f8',edgecolor=color,lw=2))
    ax.text(x+.8,y+.4,label,ha='center',va='center',fontsize=18)
for x1,y1,x2,y2,color in [(2.75,4.4,7.85,4.4,TEAL),(2.75,1.4,7.85,4.4,BLUE),(2.75,4.4,7.85,1.4,TEAL),(2.75,1.4,7.85,1.4,BLUE)]:
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,lw=2,color=color,alpha=.8))
ax.text(5.3,5.7,'Rows of the matrix give the weights',ha='center',fontsize=18)
save('matrix-combines-inputs.png')
print('Created six visual-explanation figures.')
