"""Lecture 13 diagrams: incoming light and uniform/limb-darkened models."""
from pathlib import Path
import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / 'assets'
INK, TEAL, BLUE, GOLD = '#20394d', '#087e81', '#486d9f', '#d59831'
plt.rcParams.update({'font.size': 17, 'axes.labelsize': 19, 'xtick.labelsize': 16,
                     'ytick.labelsize': 16, 'text.color': INK, 'axes.labelcolor': INK,
                     'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def annulus_fraction(r, z, p):
    if z == 0:
        return float(r <= p)
    if z + r <= p:
        return 1.0
    if z > r + p or z < r - p:
        return 0.0
    if r == 0:
        return 0.0
    return np.arccos(np.clip((r*r + z*z - p*p)/(2*r*z), -1, 1))/np.pi

def model_flux(z, p=.1, u=.6):
    def integrand(r):
        intensity = 1 - u*(1 - np.sqrt(max(0, 1-r*r)))
        return intensity * 2*np.pi*r*annulus_fraction(r, z, p)
    points = sorted(v for v in (abs(z-p), z+p) if 0 < v < 1)
    blocked = quad(integrand, 0, 1, points=points, epsabs=1e-10)[0]
    return 1-blocked/(np.pi*(1-u/3))

def make_figures():
    fig, ax = plt.subplots(figsize=(11,3.9)); ax.set_xlim(0,11); ax.set_ylim(0,4); ax.axis('off')
    ax.add_patch(Circle((1,2.1), .67, color='#f6c766'))
    ax.text(1,.85,'Star',ha='center',weight='bold')
    ax.add_patch(FancyBboxPatch((4,1.25),2.3,1.6,boxstyle='round,pad=.08',fc='#eaf4f3',ec=TEAL,lw=2))
    ax.text(5.15,2.05,'Telescope\ncollects light',ha='center',va='center',weight='bold')
    ax.add_patch(FancyBboxPatch((8,1.25),2.4,1.6,boxstyle='round,pad=.08',fc='#eef0f8',ec=BLUE,lw=2))
    ax.text(9.2,2.05,'Detector\nrecords counts',ha='center',va='center',weight='bold',fontsize=15)
    for a,b in [((1.8,2.1),(3.85,2.1)),((6.45,2.1),(7.85,2.1))]:
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=24,lw=3,color=GOLD))
    ax.text(2.85,2.6,'light',ha='center',fontsize=16)
    fig.savefig(OUT/'flux-to-detector.png',dpi=150,bbox_inches='tight'); plt.close(fig)

    fig,ax=plt.subplots(figsize=(6.3,5.2)); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Circle((0,0),1,fc='#f6c766',ec=GOLD,lw=2.5))
    ax.add_patch(Circle((.76,.34),.27,fc='#20394d',ec='white',lw=2))
    ax.scatter([0,.76],[0,.34],color=['#a76522','white'],s=25,zorder=4)
    ax.annotate('',xy=(.76,.34),xytext=(0,0),arrowprops=dict(arrowstyle='<->',color=BLUE,lw=2.5))
    ax.text(.34,.28,'z',color=BLUE,fontsize=23,weight='bold')
    ax.annotate('stellar disk',xy=(-.72,-.7),xytext=(-1.55,-1.25),color=INK,fontsize=16,
                arrowprops=dict(arrowstyle='-',color=INK))
    ax.annotate('planet',xy=(.9,.48),xytext=(1.05,1),color=INK,fontsize=16,
                arrowprops=dict(arrowstyle='-',color=INK))
    ax.set(xlim=(-1.7,1.7),ylim=(-1.45,1.35))
    fig.savefig(OUT/'transit-geometry.png',dpi=150,bbox_inches='tight');plt.close(fig)

    side=450; coords=np.linspace(-1,1,side); xx,yy=np.meshgrid(coords,coords)
    radius=np.hypot(xx,yy); mu=np.sqrt(np.maximum(0,1-radius**2)); brightness=1-.6*(1-mu)
    rgba=np.zeros((side,side,4)); rgba[:,:,:3]=np.stack((np.ones_like(mu),.78*brightness,.28*brightness),axis=-1)
    rgba[:,:,0]=.86+.14*brightness; rgba[:,:,3]=(radius<=1).astype(float)
    fig,ax=plt.subplots(figsize=(5.3,5.3));ax.imshow(rgba,extent=(-1,1,-1,1),origin='lower')
    ax.add_patch(Circle((.67,0),.12,fc=INK,ec='white',lw=1.5));ax.axis('off')
    fig.savefig(OUT/'limb-darkened-disk.png',dpi=150,bbox_inches='tight');plt.close(fig)

    time=np.linspace(-.065,.065,180); z=10*np.abs(np.sin(2*np.pi*time/3))
    uniform=np.array([model_flux(v,u=0) for v in z]); limb=np.array([model_flux(v,u=.6) for v in z])
    fig,ax=plt.subplots(figsize=(9.6,4.6))
    ax.plot(time,uniform,color=BLUE,lw=3,label='Uniform star')
    ax.plot(time,limb,color=TEAL,lw=3,label='Limb-darkened star')
    ax.set(xlabel='Time from mid-transit (days)',ylabel='Normalized flux',ylim=(.986,1.002))
    ax.spines[['top','right']].set_visible(False); ax.grid(alpha=.16)
    ax.legend(frameon=False,fontsize=15,loc='upper center',ncol=2); fig.tight_layout()
    fig.savefig(OUT/'transit-model-comparison.png',dpi=150,bbox_inches='tight'); plt.close(fig)

if __name__ == '__main__':
    make_figures()
