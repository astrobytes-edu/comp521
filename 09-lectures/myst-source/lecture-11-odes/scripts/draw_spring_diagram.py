"""Draw the spring apparatus schematics with LaTeX labels; geometry is illustrative."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
root=Path(__file__).resolve().parents[1]
plt.rcParams.update({'svg.fonttype':'path','svg.hashsalt':'comp521-spring','mathtext.fontset':'cm','font.family':'DejaVu Sans'})
def draw(path,small=False):
 fig,ax=plt.subplots(figsize=(6,1.7 if small else 3.7))
 ax.set_xlim(0,10);ax.set_ylim(-.5,2.3 if small else 5);ax.axis('off');fig.subplots_adjust(left=.02,right=.98,bottom=.03,top=.98)
 y=1.15 if small else 2.5
 ax.plot([.7,.7],[y-.6,y+.6],color='#394c5d',lw=4)
 for yy in np.linspace(y-.6,y+.6,7):ax.plot([.3,.7],[yy-.2,yy],color='#394c5d',lw=2)
 xx=[.7,1.2];yy=[y,y]
 for i in range(13):xx.append(1.4+i*.37);yy.append(y+(.24 if i%2==0 else -.24))
 xx.extend([6.4,6.8]);yy.extend([y,y]);ax.plot(xx,yy,color='#2f6f6f',lw=3)
 ax.add_patch(Rectangle((6.8,y-.5),1.4,1,facecolor='#e7f0f3',edgecolor='#394c5d',lw=2))
 ax.text(7.5,y,r'$m$',fontsize=32 if small else 27,ha='center',va='center',color='#26364c')
 ax.plot([5.5,5.5],[y-.8,y+.9],ls='--',lw=1.8,color='#596272')
 ax.annotate('',xy=(7.5,y-.75),xytext=(5.5,y-.75),arrowprops={'arrowstyle':'<->','color':'#2c5f9e','lw':2})
 ax.text(6.5,y-1.12,r'$x(t)$',ha='center',fontsize=30 if small else 25,color='#2c5f9e')
 if not small:
  ax.text(3.7,y+.65,r'$k$',ha='center',fontsize=27,color='#2f6f6f')
  ax.text(5.5,y+1.1,r'$x=0$',ha='center',fontsize=23,color='#596272')
  ax.text(4.6,y+1.65,'Equilibrium',ha='center',fontsize=19,color='#394c5d')
  ax.annotate('',xy=(6,y+1.05),xytext=(8.8,y+1.05),arrowprops={'arrowstyle':'->','color':'#a24728','lw':3})
  ax.text(8.2,y+1.4,r'$F=-kx$',ha='center',fontsize=24,color='#a24728')
 fig.savefig(path,format='svg',metadata={'Date':None,'Title':'Mass on a linear spring','Description':'A mass attached to a fixed wall by a spring. Displacement is measured from equilibrium; the restoring force opposes displacement.'});plt.close(fig)
 path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
draw(root/'assets/spring-mass.svg');draw(root/'assets/spring-mass-intro.svg',True)
