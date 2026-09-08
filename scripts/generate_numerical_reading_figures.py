"""Reproduce the numerical-reading revision figures from stated calculations.

Run from the course root with .venv/bin/python scripts/generate_numerical_reading_figures.py.
No network access or optional plotting packages are needed.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1] / "05-numerical-methods"
F = ROOT / "01-foundations/figures"
Q = ROOT / "02-roots-quadrature/figures"
O = ROOT / "03-odes/figures"
plt.rcParams.update({"font.size": 12, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "white"})
BLUE, ORANGE, GREEN, PURPLE = "#0072B2", "#D55E00", "#009E73", "#CC79A7"

def save(fig, path):
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    print(path.relative_to(ROOT))

def floating_figures():
    # Approximate lengths are scale examples, not measurements of named objects.
    names = ['Solar radius', 'Earth orbit (1 AU)', 'Outer solar system (30 AU)',
             'Cloud scale (10 pc)', 'Galactic scale (1 kpc)', 'Intergalactic scale (1 Mpc)']
    lengths = np.array([6.957e10, 1.496e13, 30*1.496e13, 10*3.086e18,
                        1e3*3.086e18, 1e6*3.086e18])
    y = np.arange(len(names))
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), layout='constrained')
    for ax, values, label, color in zip(
        axes, (lengths, np.spacing(lengths)),
        ('Approximate length (cm)', 'Adjacent binary64 spacing at that length (cm)'),
        (BLUE, ORANGE),
    ):
        ax.scatter(values, y, color=color, s=55)
        ax.set(xscale='log', yticks=y, yticklabels=names, xlabel=label)
        ax.grid(axis='x', alpha=.2)
    fig.suptitle('All these lengths are representable; their absolute spacings differ')
    save(fig, F/'2_3_astronomical_scales.webp')
    fig, axes = plt.subplots(3, 1, figsize=(9, 6), layout="constrained")
    for ax, base in zip(axes, (1e-21, 1.0, 1e16)):
        spacing = np.spacing(base)
        offsets = np.arange(5)
        values = base + offsets * spacing
        ax.plot(offsets, np.zeros(5), "o", color=BLUE, ms=9)
        ax.set(xlim=(-.5,4.5), ylim=(-.5,.5), yticks=[], xticks=offsets,
               title=f"Base = {base:.0e}; adjacent spacing = {spacing:.3e}",
               xlabel="Offset above base / adjacent-float spacing")
        assert np.all(np.diff(values)>0)
        ax.spines['left'].set_visible(False)
    save(fig,F/'2_5_floating_point_spacing.webp')
    fig, ax = plt.subplots(figsize=(9,4), layout="constrained")
    labels=['0.1','0.2','0.3','0.5']
    with localcontext() as ctx:
        ctx.prec=80
        errors=[float(Decimal.from_float(float(x))-Decimal(x)) for x in labels]
    ax.bar(labels,np.array(errors)*1e18,color=[BLUE,ORANGE,GREEN,PURPLE])
    ax.axhline(0,color='black',lw=.7)
    ax.set(xlabel='Intended decimal value',ylabel=r'Stored minus intended value ($10^{-18}$)',ylim=(-15,15),
           title='Exact decimal reference; binary64 stored value')
    for x,y in zip(labels,np.array(errors)*1e18):
        ax.annotate(f'{y:.3f}',(x,y),xytext=(0,5 if y>=0 else -17),textcoords='offset points',ha='center')
    save(fig,F/'2_6_decimal_binary_mismatch.webp')
    fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
    x=np.linspace(-3,3,301); allowance=.1+.1*np.abs(x)
    ax.fill_between(x,-allowance,allowance,color=BLUE,alpha=.2,label='Accepted residual')
    ax.plot(x,allowance,color=BLUE);ax.plot(x,-allowance,color=BLUE)
    ax.axhline(.1,color=ORANGE,ls='--',label='Absolute allowance = 0.1 cm')
    ax.axhline(-.1,color=ORANGE,ls='--')
    ax.set(xlabel='Reference (cm)',ylabel='Computed − reference (cm)',title='atol = 0.1 cm; rtol = 0.1')
    ax.legend();save(fig,F/'tolerance-acceptance.png')

def error_landscape():
    # A normalized explanatory model, not a fit or a universal optimal h.
    h = np.logspace(-9, -1, 501)
    eps = np.finfo(float).eps
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), layout='constrained')
    for ax, order, color in zip(axes, (1, 2), (BLUE, ORANGE)):
        truncation = h**order
        rounding = eps/h
        total = truncation+rounding
        optimum = (eps/order)**(1/(order+1))
        ax.loglog(h, truncation, '--', color=color, label=f'Truncation h^{order}')
        ax.loglog(h, rounding, ':', color='gray', label='Amplification eps/h')
        ax.loglog(h, total, color=color, label='Model sum')
        ax.plot(optimum, optimum**order+eps/optimum, 'o', color='black')
        ax.set(xlabel='h (dimensionless)', ylabel='model absolute error',
               title=f'p = {order}; model minimum h = {optimum:.2g}', ylim=(1e-12, 2e-1))
        ax.grid(alpha=.2)
        ax.legend(fontsize=9)
    fig.suptitle('Illustrative coefficients A = B = 1; binary64 epsilon')
    save(fig, F/'1_2_error_landscape.webp')


def rk_stage_geometry():
    # These are hand-calculated stage locations for x'=x, x(0)=1, h=0.5.
    # This draws a mathematical example, not an RK solver.
    t = np.linspace(0, .54, 300)
    points = [(0, 1, 'k1', BLUE), (.25, 1.25, 'k2', ORANGE),
              (.25, 1.3125, 'k3', GREEN), (.5, 1.65625, 'k4', PURPLE)]
    fig, ax = plt.subplots(figsize=(9, 5), layout='constrained')
    ax.plot(t, np.exp(t), color='black', label='Exact trajectory exp(t)')
    offsets = [(15, 12), (-60, -25), (18, 15), (-100, 35)]
    for (time, state, label, color), offset in zip(points, offsets):
        segment=np.array([max(0,time-.035), time+.035])
        ax.plot(segment, state+state*(segment-time), color=color, lw=2)
        ax.plot(time,state,'o',color=color)
        ax.annotate(f'{label}: state = {state:g}',(time,state),xytext=offset,
                    textcoords='offset points',color=color,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=.85, pad=1.5))
    ax.axvline(.25,color='gray',lw=.7,ls=':')
    ax.set(xlabel='t (dimensionless)', ylabel='x (dimensionless)',
           title='Same midpoint time, different predicted states', xlim=(-.03,.58), ylim=(.96,1.82))
    ax.legend(loc='upper left')
    save(fig, O/'rk-stage-geometry.png')


def taylor_figures():
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    x=np.linspace(-1,1,401);positive=np.linspace(.015,1,200)
    axes[0].plot(x,np.exp(x),color='black',label=r'$e^x$')
    for degree,color in ((1,BLUE),(2,ORANGE),(4,GREEN)):
        poly=lambda z:sum(z**k/math.factorial(k) for k in range(degree+1))
        axes[0].plot(x,poly(x),color=color,label=f'Degree {degree}')
        error=np.abs(np.exp(positive)-poly(positive))
        bound=np.e*positive**(degree+1)/math.factorial(degree+1)
        axes[1].loglog(positive,error,color=color,label=f'Degree {degree}')
        axes[1].loglog(positive,bound,color=color,ls='--')
    axes[0].set(xlabel='x (dimensionless)',ylabel='Function / polynomial value')
    axes[1].set(xlabel='h > 0 (dimensionless)',ylabel='Absolute error / bound',title='Solid: error; dashed: bound')
    for ax in axes:ax.legend();ax.grid(alpha=.2)
    save(fig,F/'taylor-polynomial-remainder.png')
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained');h=np.logspace(-16,-1,160);x=1.
    values=[(np.sin(x+h)-np.sin(x))/h,(np.sin(x+h)-np.sin(x-h))/(2*h),
            (-np.sin(x+2*h)+8*np.sin(x+h)-8*np.sin(x-h)+np.sin(x-2*h))/(12*h)]
    for value,label,color in zip(values,['Forward, order 1','Central, order 2','Central, order 4'],[BLUE,ORANGE,GREEN]):
        error=np.abs(value-np.cos(x));error[error==0]=np.nan
        ax.loglog(h,error,label=label,color=color)
    ax.set(xlabel='h (dimensionless)',ylabel='Absolute derivative error',title=r'$f(x)=\sin x$, $x=1$: refinement eventually amplifies rounding')
    ax.legend();ax.grid(alpha=.2);save(fig,F/'1_4_error_scaling.webp')

def quadrature_figures():
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    n=6;h=np.pi/(2*n);dense=np.linspace(0,np.pi/2,300)
    for ax,offset,name,color,marker in zip(axes,[0,1,.5],['Left','Right','Midpoint'],[BLUE,ORANGE,GREEN],['o','s','^']):
        nodes=(np.arange(n)+offset)*h
        for i,y in enumerate(np.sin(nodes)):
            ax.add_patch(Rectangle((i*h,0),h,y,facecolor=color,edgecolor=color,alpha=.25))
        ax.plot(dense,np.sin(dense),color='#243746');ax.plot(nodes,np.sin(nodes),marker, color=color)
        ax.set(xlabel='x (rad)',ylim=(0,1.06),title=f'{name}: {h*np.sin(nodes).sum():.4f}')
    axes[0].set_ylabel('sin x (dimensionless)');save(fig,Q/'rectangle-variants.png')
    fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
    x=np.linspace(0,1,1001);nodes=np.linspace(0,1,5)
    ax.plot(x,np.sin(4*np.pi*x)**2,color=BLUE,label=r'$\sin^2(4\pi x)$')
    ax.plot(nodes,np.sin(4*np.pi*nodes)**2,'o',color=ORANGE,ms=8,label='Initial Simpson samples')
    ax.fill_between(x,0,np.sin(4*np.pi*x)**2,color=BLUE,alpha=.12)
    ax.set(xlabel='x (dimensionless)',ylabel='f(x)',title='True area = 1/2; initial error estimate ≈ 0')
    ax.legend();save(fig,Q/'adaptive-unresolved-wave.png')
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    a,b=0.,1.;widths=[];residuals=[]
    for i in range(24):
        c=(a+b)/2;widths.append((b-a)/2);residuals.append(abs(c-.9))
        if c<.9:a=c
        else:b=c
    i=np.arange(24)
    axes[0].semilogy(i,widths,'o-',color=BLUE,label='Both scales')
    axes[1].semilogy(i,residuals,'o-',color=BLUE,label='f(x) = x − 0.9')
    axes[1].semilogy(i,np.array(residuals)*1e-12,'s-',color=ORANGE,label='f(x) = 10⁻¹²(x − 0.9)')
    axes[0].set(ylabel='Bracket half-width (x units)',xlabel='Bisection index')
    axes[1].set(ylabel='Absolute residual (function units)',xlabel='Bisection index')
    for ax in axes:ax.grid(alpha=.2);ax.legend()
    save(fig,Q/'root-residual-width.png')

def adaptive_diagram():
    fig,ax=plt.subplots(figsize=(10,4.5),layout='constrained');ax.set(xlim=(0,10),ylim=(0,4.5));ax.axis('off')
    boxes=[(1.4,2.3,'Choose step / panel'),(4.6,2.3,'Compare coarse and fine\napproximations'),(8,2.3,'Estimate meets\nlocal allowance?'),(8,.6,'Accept estimate;\ncontinue'),(4.6,4,'Refine and retry')]
    for x,y,t in boxes:ax.text(x,y,t,ha='center',va='center',bbox=dict(boxstyle='round,pad=.6',fc='#e9f3f8',ec=BLUE),fontsize=12)
    for xy,xytext in [((3.1,2.3),(2.7,2.3)),((6.8,2.3),(6.1,2.3)),((8,1.1),(8,1.8)),((5.9,4),(8,2.8)),((4.6,2.9),(4.6,3.5))]:
        ax.annotate('',xy=xy,xytext=xytext,arrowprops=dict(arrowstyle='->',color=BLUE,lw=1.8))
    ax.text(8.15,1.4,'Yes');ax.text(6.8,3.5,'No')
    ax.text(.2,.25,'A small estimate can miss unresolved structure.\nCheck assumptions and independent refinement.',fontsize=11,va='bottom')
    save(fig,F/'2_4_adaptive_step_control.webp')

def ode_figures():
    h=.02;n=round(10*2*np.pi/h);t=np.arange(n+1)*h
    z=(1-1j*h)**np.arange(n+1);energy=np.abs(z)**2/2
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    axes[0].plot(z.real,z.imag,color=ORANGE);theta=np.linspace(0,2*np.pi,200)
    axes[0].plot(np.cos(theta),-np.sin(theta),'--',color=BLUE)
    axes[0].set(xlabel='q',ylabel='p',aspect='equal',title='Euler oscillator phase plane')
    axes[1].plot(t/(2*np.pi),energy/energy[0],color=ORANGE)
    axes[1].set(xlabel='Time / period',ylabel='Energy / initial energy',title=f'h = {h}; final ratio = {energy[-1]/energy[0]:.3f}')
    save(fig,O/'3_2_energy_drift.webp')
    h=.2;n=1000;t=np.arange(n+1)*h;q,p=1.,0.;E=[];K=[]
    for _ in range(n+1):
        E.append((q*q+p*p)/2);K.append((p*p+(1-h*h/4)*q*q)/2)
        ph=p-h*q/2;q=q+h*ph;p=ph-h*q/2
    amp=abs(sum((1j*h)**k/math.factorial(k) for k in range(5)))**2
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
    axes[0].plot(t/(2*np.pi),amp**np.arange(n+1)-1,color=BLUE,label='RK4')
    axes[0].plot(t/(2*np.pi),np.array(E)/E[0]-1,color=ORANGE,label='Leapfrog')
    axes[1].plot(t/(2*np.pi),np.array(K)-K[0],color=GREEN)
    axes[0].set(xlabel='Time / period',ylabel='Relative physical energy error',title='Oscillator, h = 0.2');axes[0].legend()
    axes[1].set(xlabel='Time / period',ylabel=r'$K_h(t)-K_h(0)$',title='Special exact invariant: rounding residual')
    save(fig,O/'3_6_modified_hamiltonian.webp')
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    x=np.linspace(-3.5,1,300);y=np.linspace(-3.5,3.5,300);X,Y=np.meshgrid(x,y);z=X+1j*Y
    for ax,fun,name in zip(axes,[lambda z:1+z,lambda z:1+z+z*z/2+z**3/6+z**4/24,lambda z:1/(1-z)],['Forward Euler','Classical RK4','Backward Euler']):
        mag=np.abs(fun(z));ax.contourf(X,Y,mag,levels=[0,1],colors=[BLUE],alpha=.25)
        ax.contour(X,Y,mag,levels=[1],colors=[BLUE]);ax.axvline(0,color='gray',lw=.7);ax.axhline(0,color='gray',lw=.7)
        ax.set(title=name,xlabel='Re(hλ)',ylabel='Im(hλ)',aspect='equal')
    save(fig,O/'stability-regions.png')

if __name__=='__main__':
    floating_figures();error_landscape();rk_stage_geometry();taylor_figures();quadrature_figures();adaptive_diagram();ode_figures()
