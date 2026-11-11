"""Executed teaching figures: fitting a fading signal and choosing an optimizer.

All data are synthetic. The dimensionless model f=A exp(-t/tau) represents
exponential relaxation of an excess signal, not a complete stellar calculation.
The guide's scalar quadratic, anisotropic bowl, and quartic exercise provide
independent analytic checks. No scientific package capability is measured here.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import platform

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / "_build/mpl-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
NAVY, TEAL, GOLD = "#20365b", "#087e81", "#d59831"
PALE, GRAY = "#eef5fa", "#697685"
SEED = 20261110
TIMES = np.linspace(0.0, 6.0, 16, dtype=np.float64)
SIGMA = np.float64(0.08)
TRUE = np.log(np.array([1.8, 2.4], dtype=np.float64))
START = np.log(np.array([0.7, 0.7], dtype=np.float64))
H_BOWL = np.diag([1.0, 50.0])
BOWL_START = np.array([1.0, 1.0])
COUNTS = np.array([1., 2., 2., 4., 6.])

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 22,
    "axes.titlesize": 23, "axes.labelsize": 22,
    "xtick.labelsize": 19, "ytick.labelsize": 19,
    "legend.fontsize": 17, "axes.spines.top": False,
    "axes.spines.right": False, "axes.labelcolor": NAVY,
    "text.color": NAVY, "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.edgecolor": "#b5c2cf", "axes.titlepad": 14,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "lines.linewidth": 2.8,
})


def model(theta, t=TIMES):
    """Dimensionless A=exp(a), tau=exp(b), t=time/t0, f=excess flux/F0."""
    a, b = theta
    return np.exp(a) * np.exp(-np.asarray(t) / np.exp(b))


DATA = model(TRUE) + SIGMA * np.random.default_rng(SEED).normal(size=TIMES.size)


def residual(theta):
    """Whitened model-minus-data residual; fixed independent sigma=0.08."""
    return (model(theta) - DATA) / SIGMA


def jacobian(theta):
    """Jacobian of whitened residuals with respect to log A and log tau."""
    f = model(theta)
    return np.column_stack((f, f * TIMES / np.exp(theta[1]))) / SIGMA


def loss(theta):
    q = residual(theta)
    # No complex conjugation: this preserves the analytic extension used by checks.
    return 0.5 * (q @ q)


def gradient(theta):
    return jacobian(theta).T @ residual(theta)


def hessian(theta):
    q, j = residual(theta), jacobian(theta)
    f, z = model(theta), TIMES / np.exp(theta[1])
    correction = np.array([[np.sum(q*f/SIGMA), np.sum(q*z*f/SIGMA)],
                           [np.sum(q*z*f/SIGMA), np.sum(q*(z*z-z)*f/SIGMA)]])
    return j.T @ j + correction


def lm_proposal(theta, nu):
    """Damped linear least squares solved by SVD-backed augmented least squares."""
    if nu <= 0:
        raise ValueError("Damping must be positive.")
    q, j = residual(theta), jacobian(theta)
    augmented_j = np.vstack((j, np.sqrt(nu) * np.eye(2)))
    augmented_rhs = np.concatenate((-q, np.zeros(2)))
    return np.linalg.lstsq(augmented_j, augmented_rhs, rcond=None)[0]


def fit_lm(theta0=START, nu0=1.0, max_attempts=80, gradient_tol=1e-6):
    """Finite-work teaching LM: accept actual decreases and adapt damping.

    This is a small inspectable algorithm, not a replacement for a production
    least-squares solver. Attempts, damping, and numerical stopping are bounded;
    no physical bounds or priors are added to this unconstrained log-parameter fit.
    """
    theta = np.array(theta0, dtype=np.float64, copy=True)
    nu = float(nu0)
    history = []
    reason = "attempt limit"
    for attempt in range(1, max_attempts + 1):
        g = gradient(theta)
        if np.linalg.norm(g, ord=np.inf) < gradient_tol:
            reason = "small gradient"
            break
        before = float(loss(theta))
        step = lm_proposal(theta, nu)
        candidate = theta + step
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            proposed = float(loss(candidate))
        accepted = bool(np.isfinite(proposed) and proposed < before)
        old_theta = theta.copy()
        old_nu = nu
        if accepted:
            theta = candidate
            nu = max(nu / 3.0, 1e-12)
        else:
            nu = min(nu * 5.0, 1e12)
        history.append({"attempt": attempt, "nu": old_nu,
                        "theta_before": old_theta.tolist(), "step": step.tolist(),
                        "trial_theta": candidate.tolist(), "trial_loss": proposed if np.isfinite(proposed) else None,
                        "loss_before": before, "accepted": accepted,
                        "loss_after": float(loss(theta))})
        if accepted and np.linalg.norm(step) < 1e-10 * (1 + np.linalg.norm(theta)):
            reason = "small accepted step"
            break
        if not accepted and nu >= 1e12:
            reason = "damping limit"
            break
    return {"theta": theta, "parameters": np.exp(theta), "loss": float(loss(theta)),
            "gradient_inf_norm": float(np.linalg.norm(gradient(theta), ord=np.inf)),
            "history": history, "reason": reason, "attempts": len(history),
            "accepted": sum(h["accepted"] for h in history),
            "rejected": sum(not h["accepted"] for h in history)}


def style(ax, xlabel=None, ylabel=None):
    ax.grid(alpha=.16, color=NAVY)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def panels(title, n=2, size=(10.4, 5.3)):
    fig, axes = plt.subplots(1, n, figsize=size, layout="constrained")
    fig.suptitle(title, fontsize=24, fontweight="bold")
    return fig, np.atleast_1d(axes)


def single(title, size=(8.4, 5.1)):
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    ax.set_title(title, fontsize=23, fontweight="bold")
    return fig, ax


def fading_data():
    fig, ax = single("Synthetic fading observations")
    t = np.linspace(0, 6, 501)
    ax.plot(t, model(TRUE, t), color=TEAL, label="Generating model")
    ax.errorbar(TIMES, DATA, yerr=SIGMA, fmt="o", color=NAVY, capsize=4,
                ms=6, label=r"Synthetic data: $\sigma=0.08$")
    ax.set_ylim(0, 2.1); ax.set_xlim(-.15, 6.15)
    ax.legend(frameon=False, fontsize=17)
    style(ax, r"Scaled time $t=\mathrm{time}/t_0$", r"Excess flux $y=F/F_0$")
    return fig


def residuals():
    fig, (ax, bx) = panels("Residuals say how a particular model misses the data")
    t = np.linspace(0, 6, 501)
    ax.plot(t, model(START, t), color=GOLD, label="Initial model")
    ax.errorbar(TIMES, DATA, yerr=SIGMA, fmt="o", color=NAVY, capsize=3, ms=5)
    ax.set_title(r"Initial $A=0.7$, $\tau=0.7$")
    ax.legend(frameon=False, fontsize=17)
    style(ax, "Scaled time t", "Scaled excess flux")
    q = residual(START)
    bx.axhline(0, color=GRAY, lw=1.5)
    bx.vlines(TIMES, 0, q, color=GOLD, lw=2)
    bx.scatter(TIMES, q, color=GOLD, s=48)
    bx.set_title("Standardized residuals")
    style(bx, "Scaled time t", r"Standardized residual $q_i$")
    return fig


def whitening():
    fig, (ax, bx) = panels("Whitening accounts for scales and correlations")
    covariance = np.array([[1., .7], [.7, 2.]])
    c = np.linalg.cholesky(covariance)
    angle = np.linspace(0, 2*np.pi, 501)
    circle = np.array([np.cos(angle), np.sin(angle)])
    for radius in [1., 2.]:
        raw = c @ (radius * circle)
        white = np.linalg.solve(c, raw)
        ax.plot(raw[0], raw[1], color=NAVY)
        bx.plot(white[0], white[1], color=TEAL)
    ax.set_title("Correlated residuals")
    bx.set_title("Whitened residuals")
    for axis in [ax, bx]:
        axis.set_xlim(-3,3); axis.set_ylim(-3,3); axis.set_aspect("equal")
        axis.set_xticks([-2,0,2]); axis.set_yticks([-2,0,2])
    style(ax, r"Residual $r_1$", r"Residual $r_2$")
    style(bx, r"Whitened $q_1$", r"Whitened $q_2$")
    return fig


def poisson_counts():
    fig, (ax, bx) = panels("The noise model changes the fitted count rate")
    ax.bar(np.arange(1,6), COUNTS, color=TEAL, width=.65)
    ax.set_xticks(np.arange(1,6)); ax.set_yticks([0,2,4,6])
    ax.set_title("Observed positive counts")
    style(ax, "Observation index", "Observed count n")
    mu = np.linspace(.5, 6.0, 1201)
    mle = float(COUNTS.mean())
    neyman = float(COUNTS.size / np.sum(1/COUNTS))
    poisson = COUNTS.size*mu - COUNTS.sum()*np.log(mu)
    neyman_loss = .5*np.sum((mu[:,None]-COUNTS)**2/COUNTS, axis=1)
    poisson -= COUNTS.size*mle-COUNTS.sum()*np.log(mle)
    neyman_loss -= .5*np.sum((neyman-COUNTS)**2/COUNTS)
    bx.plot(mu, poisson, color=TEAL, label=f"Poisson: min at {mle:g}")
    bx.plot(mu, neyman_loss, color=GOLD, ls="--", label=f"Neyman: min at {neyman:.3f}")
    bx.axvline(mle,color=TEAL,lw=1.5,ls=":");bx.axvline(neyman,color=GOLD,lw=1.5,ls=":")
    bx.set_ylim(-.3,15);bx.set_xlim(.5,6)
    bx.legend(frameon=False,fontsize=16)
    bx.set_title("Different weighting")
    style(bx,r"Common predicted count $\mu$","Loss minus its minimum")
    return fig


def derivative():
    fig,ax=single("A derivative gives the local change in loss")
    theta=np.linspace(-1.4,2.5,701)
    ax.plot(theta,8*(theta-1)**2,color=TEAL,label=r"$\mathcal{L}=8(\theta-1)^2$")
    tangent_theta=np.linspace(-1.35,-.35,101)
    ax.plot(tangent_theta,32-32*(tangent_theta+1),color=GOLD,ls="--",label="Local tangent")
    ax.scatter([-1,1],[32,0],s=70,color=NAVY,zorder=5)
    ax.annotate(r"$\mathcal{L}'(-1)=-32$",xy=(-.8,25.6),xytext=(.1,35),fontsize=23,
                arrowprops={"arrowstyle":"->","color":NAVY})
    ax.set_ylim(-2,50);ax.set_xlim(-1.4,2.5)
    ax.legend(frameon=False,fontsize=18,loc="upper right")
    style(ax,r"Parameter $\theta$",r"Loss $\mathcal{L}$")
    return fig


def gd_step_sizes():
    fig,axes=plt.subplots(1,4,figsize=(14,4.5),layout="constrained")
    fig.suptitle("Step size changes the error multiplier",fontsize=24,fontweight="bold")
    k=np.arange(13)
    for ax,eta,title,color in zip(axes.ravel(),[.03,.09,.125,.14],
            ["Monotone","Damped oscillation","Two-point cycle","Divergence"],
            [TEAL,NAVY,GOLD,GRAY]):
        theta=1-2*(1-16*eta)**k
        ax.plot(k,theta,"o-",color=color,ms=4)
        ax.axhline(1,color=GRAY,lw=1,ls=":")
        ax.set_title(rf"$\eta={eta:g}$" + "\n" + title,fontsize=20)
        ax.set_xticks([0,6,12])
        style(ax,"Iteration k",r"$\theta_k$")
    return fig


def bowl_contours(ax,limit=1.25):
    x=np.linspace(-limit,limit,301);xx,yy=np.meshgrid(x,x)
    zz=.5*(xx**2+50*yy**2)
    ax.contour(xx,yy,zz,levels=[.1,.5,2,8,20,35],colors=TEAL,linewidths=1.4,alpha=.8)
    ax.set_xlim(-limit,limit);ax.set_ylim(-limit,limit);ax.set_aspect("equal")
    ax.axhline(0,color=GRAY,lw=.8);ax.axvline(0,color=GRAY,lw=.8)
    style(ax,r"Error coordinate $e_1$",r"Error coordinate $e_2$")


def bowl_gd(n=350):
    eta=2/51
    path=[BOWL_START.copy()]
    for _ in range(n):path.append(path[-1]-eta*(H_BOWL@path[-1]))
    return np.array(path)


def curvature_bowl():
    fig,ax=single("Equal loss contours reveal unequal curvature",size=(7.2,5.4))
    bowl_contours(ax)
    ax.scatter([0],[0],color=NAVY,s=60,zorder=5)
    return fig


def conditioning_paths():
    fig,(ax,bx)=panels("Conditioning controls gradient-descent speed")
    bowl_contours(ax)
    path=bowl_gd(350)
    ax.plot(path[:31,0],path[:31,1],"o-",color=GOLD,ms=3,lw=1.8)
    ax.scatter([1],[1],color=NAVY,s=60,zorder=6)
    ax.set_title("First 30 gradient steps")
    relative=np.linalg.norm(path,axis=1)/np.linalg.norm(path[0])
    bx.semilogy(np.arange(len(path)),relative,color=NAVY)
    bx.axhline(1e-6,color=GOLD,ls=":",lw=2)
    bx.set_title(r"Best fixed step: $\eta=2/51$")
    style(bx,"Iteration k","Relative parameter error")
    return fig


def scaling():
    fig,(ax,bx)=panels("Rescaling changes geometry without adding data")
    x=np.linspace(-2.5,2.5,301);xx,yy=np.meshgrid(x,x)
    ax.contour(xx,yy,.5*(xx**2+50*yy**2),levels=[.25,.5,1,2],colors=TEAL,linewidths=2)
    bx.contour(xx,yy,.5*(xx**2+yy**2),levels=[.25,.5,1,2],colors=GOLD,linewidths=2)
    for axis in [ax,bx]:
        axis.set_aspect("equal");axis.set_xlim(-2.3,2.3);axis.set_ylim(-2.3,2.3)
        axis.set_xticks([-2,0,2]);axis.set_yticks([-2,0,2])
    ax.set_title(r"Original: $\kappa=50$")
    bx.set_title(r"Rescaled: $\kappa=1$")
    style(ax,r"$e_1$",r"$e_2$");style(bx,r"$z_1$",r"$z_2$")
    return fig


def heavy_ball(n=120):
    root=math.sqrt(50)
    eta=4/(root+1)**2;beta=((root-1)/(root+1))**2
    theta=BOWL_START.copy();velocity=np.zeros(2)
    path=[theta.copy()]
    for _ in range(n):
        velocity=beta*velocity-eta*(H_BOWL@theta)
        theta=theta+velocity;path.append(theta.copy())
    return np.array(path),eta,beta


def momentum():
    fig,ax=single("Heavy-ball momentum can accelerate this quadratic")
    gd=bowl_gd(120);hb,eta,beta=heavy_ball(120)
    ax.semilogy(np.arange(121),np.linalg.norm(gd,axis=1)/np.linalg.norm(gd[0]),color=NAVY,label="Fixed-step gradient descent")
    ax.semilogy(np.arange(121),np.linalg.norm(hb,axis=1)/np.linalg.norm(hb[0]),color=GOLD,label="Tuned heavy-ball")
    ax.set_ylim(1e-13,10)
    ax.legend(frameon=False,fontsize=18)
    ax.text(.97,.5,"Fixed quadratic\nInitial update = 0",transform=ax.transAxes,ha="right",fontsize=19)
    style(ax,"Iteration k","Relative parameter error")
    return fig


def newton_model():
    fig,ax=single("On a quadratic, the local model is exact")
    theta=np.linspace(-1.3,2.3,701)
    q=32-32*(theta+1)+.5*16*(theta+1)**2
    ax.plot(theta,8*(theta-1)**2,color=TEAL,lw=4,label="Actual loss")
    ax.plot(theta,q,color=GOLD,ls="--",lw=2.4,label="Second-order model at -1")
    ax.scatter([-1,1],[32,0],color=NAVY,s=80,zorder=5)
    ax.annotate("One Newton step",xy=(1,1),xytext=(-.2,21),fontsize=23,
                arrowprops={"arrowstyle":"->","color":NAVY})
    ax.set_ylim(-2,45);ax.legend(frameon=False,fontsize=18)
    style(ax,r"Parameter $\theta$",r"Loss $\mathcal{L}$")
    return fig


def newton_failure():
    fig,ax=single("Negative curvature can make Newton move uphill")
    x=np.linspace(-1.35,1.35,801);f=lambda z:z**4-2*z**2
    x0=.25;g=4*x0**3-4*x0;h=12*x0**2-4;trial=x0-g/h
    ax.plot(x,f(x),color=TEAL)
    local=np.linspace(-.35,.8,301)
    ax.plot(local,f(x0)+g*(local-x0)+.5*h*(local-x0)**2,color=GOLD,ls="--",label="Concave local quadratic")
    ax.scatter([x0,trial],[f(x0),f(trial)],s=80,color=NAVY,zorder=5)
    ax.annotate("Newton trial: higher loss",xy=(trial,f(trial)),xytext=(-1.2,.55),fontsize=21,
                arrowprops={"arrowstyle":"->","color":NAVY})
    ax.set_xlim(-1.35,1.35);ax.set_ylim(-1.2,.85)
    ax.legend(frameon=False,fontsize=17,loc="lower center")
    style(ax,"Parameter x",r"Loss $x^4-2x^2$")
    return fig


def loss_grid(a,b,t=TIMES,data=DATA):
    aa,bb=np.meshgrid(a,b)
    pred=np.exp(aa[...,None])*np.exp(-t/np.exp(bb[...,None]))
    return .5*np.sum(((pred-data)/SIGMA)**2,axis=-1)


def optimization_hero():
    """One existing fit, shown in observation and parameter coordinates.

    The line joins accepted LM states only, mapped back to amplitude and
    timescale. Contours are the actual fixed-noise Gaussian loss, not a stylized
    optimization landscape or an uncertainty band.
    """
    fit = fit_lm()
    accepted = [np.asarray(h["trial_theta"], dtype=np.float64)
                for h in fit["history"] if h["accepted"]]
    path = np.vstack([START, *accepted])
    assert np.array_equal(path[-1], fit["theta"])
    assert np.all(np.diff([float(loss(theta)) for theta in path]) < 0)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.6, 4.0), layout="constrained",
                                gridspec_kw={"width_ratios": [1.12, 1.0]})
    t = np.linspace(0, 6, 501)
    ax.errorbar(TIMES, DATA, yerr=SIGMA, fmt="o", color=NAVY, capsize=3,
                ms=5.5, label="Synthetic data", zorder=4)
    ax.plot(t, model(START, t), color=GOLD, ls="--", label="Initial model")
    ax.plot(t, model(fit["theta"], t), color=TEAL, lw=3.4, label="Fitted model")
    ax.set(xlim=(-.12, 6.1), ylim=(-.03, 2.03), xticks=[0, 3, 6], yticks=[0, 1, 2])
    ax.set_title("Compare with data", fontsize=21,
                 fontweight="bold", loc="left")
    ax.legend(frameon=False, fontsize=17, loc="upper right", handlelength=1.5,
              borderpad=.2, labelspacing=.35)
    style(ax, r"Scaled time $t$", r"Scaled excess flux $y$")

    a = np.linspace(-.6, .88, 201)
    b = np.linspace(-.6, 1.22, 221)
    values = loss_grid(a, b)
    amplitude, timescale = np.exp(a), np.exp(b)
    physical_path = np.exp(path)
    levels = np.geomspace(fit["loss"] * 1.001, 1500, 16)
    bx.contourf(amplitude, timescale, values, levels=levels, cmap="Blues_r", norm=LogNorm(),
                extend="both", alpha=.9)
    bx.contour(amplitude, timescale, values, levels=[8, 15, 40, 120, 400, 900],
               colors=TEAL, linewidths=1.1, alpha=.65)
    bx.plot(physical_path[:, 0], physical_path[:, 1], "o-", color=GOLD, ms=4, lw=2.6, zorder=5)
    bx.scatter(*np.exp(START), s=65, color=GOLD, edgecolors="white", linewidths=1.2, zorder=6)
    bx.scatter(*fit["parameters"], s=160, marker="*", color="white", edgecolors=NAVY,
               linewidths=1.1, zorder=7)
    bx.annotate("Start", xy=np.exp(START), xytext=(.77, .61), fontsize=19, color=NAVY)
    bx.annotate("Fit", xy=fit["parameters"], xytext=(1.91, 2.63), fontsize=19, color=NAVY)
    bx.set(xlim=(amplitude[0], amplitude[-1]), ylim=(timescale[0], timescale[-1]),
           xticks=[.7, 1.2, 1.8, 2.4], yticks=[.7, 1.5, 2.4, 3.2])
    bx.set_title("Search parameter space", fontsize=21,
                 fontweight="bold", loc="left")
    style(bx, r"Initial brightness $A$", r"Fading timescale $\tau$")
    bx.grid(False)
    for axis in (ax, bx):
        axis.tick_params(labelsize=18)
    return fig


def lm_damping():
    fig,(ax,bx)=panels("Damping changes the proposed step, then we test it")
    a=np.linspace(-.8,1.35,160);b=np.linspace(-.9,3.6,190)
    zz=loss_grid(a,b)
    ax.contourf(a,b,np.maximum(zz,6.8),levels=np.geomspace(6.8,8000,15),cmap="Blues",norm=LogNorm())
    ax.contour(a,b,zz,levels=[8,20,100,500,2000],colors=TEAL,linewidths=.8,alpha=.5)
    nus=[1.,100.,1000.];colors=[GOLD,TEAL,NAVY]
    trial_losses=[]
    for nu,color in zip(nus,colors):
        step=lm_proposal(START,nu);trial=START+step;value=float(loss(trial));trial_losses.append(value)
        ax.annotate("",xy=trial,xytext=START,arrowprops={"arrowstyle":"->","color":color,"lw":3})
        ax.scatter(*trial,color=color,s=60,zorder=5)
    ax.scatter(*START,color=NAVY,s=80,zorder=6)
    ax.scatter(*fit_lm()["theta"],color="white",edgecolor=NAVY,s=75,zorder=6)
    ax.set_xlim(a[0],a[-1]);ax.set_ylim(b[0],b[-1])
    ax.set_title("Trials from one start")
    style(ax,r"Log amplitude $a$",r"Log time scale $b$")
    labels=["nu=1\nreject","nu=100\naccept","nu=1000\naccept"]
    bx.bar(np.arange(3),trial_losses,color=colors,width=.65)
    bx.axhline(float(loss(START)),color=GRAY,lw=2,ls="--",label="Initial loss")
    bx.set_yscale("log");bx.set_xticks(np.arange(3),labels=labels,fontsize=17)
    bx.set_title("Evaluate actual trial loss")
    bx.legend(frameon=False,fontsize=17)
    style(bx,None,"Loss on logarithmic scale")
    return fig


def lm_trace():
    fit=fit_lm();hist=fit['history'];k=np.array([h['attempt'] for h in hist])
    fig,(ax,bx)=panels("Accepted states and rejected trials are different")
    ax.step(np.r_[0,k],np.r_[float(loss(START)),[h['loss_after'] for h in hist]],where="post",color=NAVY,label="Accepted-state loss")
    for accepted,color,marker,label in [(True,TEAL,"o","Accepted trial"),(False,GOLD,"x","Rejected trial")]:
        selected=[h for h in hist if h['accepted']==accepted and h['trial_loss'] is not None]
        ax.scatter([h['attempt'] for h in selected],[h['trial_loss'] for h in selected],color=color,marker=marker,s=65,label=label,zorder=5)
    ax.set_yscale("log");ax.set_title("Loss at each attempt")
    ax.legend(frameon=False,fontsize=15)
    style(ax,"Attempt index","Loss")
    bx.semilogy(k,[h['nu'] for h in hist],"o-",color=TEAL,ms=5)
    bx.set_title("Adapt damping")
    style(bx,"Attempt index",r"Damping $\nu$")
    return fig


def fit_result():
    fit=fit_lm();theta=fit['theta'];t=np.linspace(0,6,501)
    fig,(ax,bx)=panels("Check the fit and its residuals")
    ax.plot(t,model(TRUE,t),color=GRAY,ls="--",label="Generating curve")
    ax.plot(t,model(theta,t),color=TEAL,label="Fitted curve")
    ax.errorbar(TIMES,DATA,yerr=SIGMA,fmt="o",color=NAVY,capsize=3,ms=5)
    ax.set_title(f"A={fit['parameters'][0]:.3f}, tau={fit['parameters'][1]:.3f}")
    ax.legend(frameon=False,fontsize=17)
    style(ax,"Scaled time t","Scaled excess flux")
    q=residual(theta)
    bx.axhspan(-1,1,color=PALE);bx.axhline(0,color=GRAY,lw=1.3)
    bx.vlines(TIMES,0,q,color=TEAL,lw=2);bx.scatter(TIMES,q,color=TEAL,s=50)
    bx.set_title(r"$q_i=(f_i-d_i)/0.08$")
    style(bx,"Scaled time t","Standardized residual")
    return fig


def identifiability():
    fig,(ax,bx)=panels("Rescaling cannot supply missing information")
    a=np.linspace(-.6,1.2,160);b=np.linspace(-.4,1.4,160)
    zeros=np.zeros(16);data0=np.full(16,1.8)
    for axis,t,data,title in [(ax,zeros,data0,"All observations at t=0: rank 1"),
                              (bx,TIMES,DATA,"Several times: rank 2")]:
        zz=loss_grid(a,b,t,data)
        axis.contour(a,b,zz,levels=[2,8,20,50,150,400,1000],colors=TEAL,linewidths=1.6)
        axis.set_title(title,fontsize=21)
        axis.set_xlim(a[0],a[-1]);axis.set_ylim(b[0],b[-1]);axis.set_aspect("equal")
        style(axis,r"Log amplitude $a$",r"Log time scale $b$")
    return fig


def regularization():
    fig,ax=single("A penalty changes the objective and its minimizer")
    z=np.linspace(-1,3.5,701);data=.5*(z-2)**2;prior=.5*z**2;total=data+prior
    ax.plot(z,data,color=TEAL,label=r"Data: $\frac{1}{2}(z-2)^2$")
    ax.plot(z,prior,color=GOLD,label=r"Prior penalty: $\frac{1}{2} z^2$")
    ax.plot(z,total,color=NAVY,label="Sum")
    ax.scatter([2,1],[0,1],s=70,color=[TEAL,NAVY],zorder=5)
    ax.set_ylim(-.2,7.0);ax.legend(frameon=False,fontsize=17,loc="upper left")
    style(ax,"Standardized parameter z","Objective value")
    return fig


def counts_observations():
    """The same five positive observations, shown without a second visual task."""
    fig,ax=plt.subplots(figsize=(10,4.6),layout="constrained")
    ax.bar(np.arange(1,6),COUNTS,color=TEAL,width=.62)
    for i,n in enumerate(COUNTS,start=1):
        ax.text(i,n+.14,f"{int(n)}",ha="center",va="bottom",fontsize=22,color=NAVY)
    ax.set_xlim(.4,5.6);ax.set_ylim(0,6.8)
    ax.set_xticks(np.arange(1,6));ax.set_yticks([0,2,4,6])
    ax.tick_params(labelsize=20)
    style(ax,"Observation index",r"Observed count $n_i$")
    return fig


def counts_losses():
    """The unchanged Poisson and Neyman objectives, each shifted to minimum zero."""
    fig,ax=plt.subplots(figsize=(10,4.6),layout="constrained")
    mu=np.linspace(.5,6.0,1201)
    mle=float(COUNTS.mean());neyman=float(COUNTS.size/np.sum(1/COUNTS))
    poisson=COUNTS.size*mu-COUNTS.sum()*np.log(mu)
    neyman_loss=.5*np.sum((mu[:,None]-COUNTS)**2/COUNTS,axis=1)
    poisson-=COUNTS.size*mle-COUNTS.sum()*np.log(mle)
    neyman_loss-=.5*np.sum((neyman-COUNTS)**2/COUNTS)
    ax.plot(mu,poisson,color=TEAL,label=f"Poisson: minimum at {mle:g}")
    ax.plot(mu,neyman_loss,color=GOLD,ls="--",label=f"Neyman: minimum at {neyman:.3f}")
    ax.axvline(mle,color=TEAL,lw=1.5,ls=":",ymax=.60)
    ax.axvline(neyman,color=GOLD,lw=1.5,ls=":",ymax=.60)
    ax.scatter([mle,neyman],[0,0],s=65,color=[TEAL,GOLD],zorder=5)
    ax.set_xlim(.5,6.0);ax.set_ylim(-.3,15)
    ax.set_xticks([1,2,3,4,5,6]);ax.tick_params(labelsize=20)
    ax.legend(frameon=False,fontsize=20,loc="upper center")
    style(ax,r"Common predicted count $\mu$","Loss minus its minimum")
    return fig


def stationary_points():
    """The guide's unchanged quartic: minima at ±1 and a local maximum at zero."""
    fig,ax=plt.subplots(figsize=(10,4.6),layout="constrained")
    x=np.linspace(-1.5,1.5,901)
    ax.plot(x,x**4-2*x**2,color=TEAL)
    ax.axhline(0,color=GRAY,lw=1.1)
    ax.scatter([-1,1],[-1,-1],s=85,color=NAVY,zorder=5)
    ax.scatter([0],[0],s=85,color=GOLD,zorder=5)
    for point in [-1,1]:
        ax.annotate("minimum",xy=(point,-1),xytext=(point,-.60),ha="center",fontsize=22,
                    arrowprops={"arrowstyle":"->","color":NAVY})
    ax.annotate("local maximum",xy=(0,0),xytext=(0,.48),ha="center",fontsize=22,
                arrowprops={"arrowstyle":"->","color":GOLD})
    ax.set_xlim(-1.5,1.5);ax.set_ylim(-1.23,.84)
    ax.set_xticks([-1,0,1]);ax.set_yticks([-1,-.5,0,.5]);ax.tick_params(labelsize=20)
    style(ax,"Parameter x",r"Loss $\mathcal{L}(x)=x^4-2x^2$")
    return fig


FIGURES={
    'optimization-hero.png':optimization_hero,
    'fading-data.png':fading_data,'residuals.png':residuals,'whitening.png':whitening,
    'poisson-counts.png':poisson_counts,'derivative.png':derivative,'gd-step-sizes.png':gd_step_sizes,
    'curvature-bowl.png':curvature_bowl,'conditioning-paths.png':conditioning_paths,
    'scaling.png':scaling,'momentum.png':momentum,'newton-model.png':newton_model,
    'newton-failure.png':newton_failure,'lm-damping.png':lm_damping,'lm-trace.png':lm_trace,
    'fit-result.png':fit_result,'identifiability.png':identifiability,'regularization.png':regularization,
    'counts-observations.png':counts_observations,'counts-losses.png':counts_losses,
    'stationary-points.png':stationary_points}


def save_figure(name,fig):
    if name not in FIGURES:raise ValueError(f'Unknown figure: {name}')
    ASSETS.mkdir(parents=True,exist_ok=True)
    fig.savefig(ASSETS/name,dpi=180,bbox_inches="tight")
    return ASSETS/name


def numerical_checks(write=True):
    fit=fit_lm()
    reference=least_squares(residual,START,jac=jacobian,method='trf',
                            xtol=1e-13,ftol=1e-13,gtol=1e-12)
    assert fit['reason'] not in ['attempt limit','damping limit'],fit['reason']
    assert np.max(np.abs(fit['theta']-reference.x))<1e-6
    assert abs(fit['loss']-float(loss(reference.x)))<1e-9
    assert all(h['loss_after']<=h['loss_before'] for h in fit['history'])
    assert all(np.array_equal(h['theta_before'],h['trial_theta']) is False for h in fit['history'])
    theta=np.log(np.array([1.2,1.6]));eps=1e-30
    cs_j=np.column_stack([np.imag(residual(theta.astype(complex)+eps*1j*np.eye(2)[j]))/eps for j in range(2)])
    cs_g=np.array([np.imag(loss(theta.astype(complex)+eps*1j*np.eye(2)[j]))/eps for j in range(2)])
    cs_h=np.column_stack([np.imag(gradient(theta.astype(complex)+eps*1j*np.eye(2)[j]))/eps for j in range(2)])
    jerr=float(np.max(np.abs(cs_j-jacobian(theta))))
    gerr=float(np.max(np.abs(cs_g-gradient(theta))))
    herr=float(np.max(np.abs(cs_h-hessian(theta))))
    assert jerr<1e-10 and gerr<1e-8 and herr<1e-7
    # The scalar recurrence is independent of the loop implementation.
    scalar={}
    for eta in [.03,.09,.125,.14,1/16]:
        values=[-1.]
        for _ in range(12):values.append(values[-1]-eta*16*(values[-1]-1))
        exact=1-2*(1-16*eta)**np.arange(13)
        assert np.allclose(values,exact,rtol=1e-13,atol=1e-13)
        scalar[str(eta)]={'error_multiplier':1-16*eta,'theta_after_12':float(values[-1])}
    bowl=bowl_gd(350);rho=49/51
    assert np.allclose(np.linalg.norm(bowl,axis=1)/np.linalg.norm(bowl[0]),rho**np.arange(351),rtol=1e-12,atol=1e-14)
    needed=math.ceil(math.log(1e-6)/math.log(rho));assert needed==346
    scaled_h=np.diag([1,1/math.sqrt(50)])@H_BOWL@np.diag([1,1/math.sqrt(50)])
    assert np.allclose(scaled_h,np.eye(2),atol=1e-14)
    newton_step=np.linalg.solve(H_BOWL,-H_BOWL@BOWL_START)
    assert np.array_equal(BOWL_START+newton_step,np.zeros(2))
    hb,hb_eta,hb_beta=heavy_ball(120)
    assert np.linalg.norm(hb[-1])<np.linalg.norm(bowl[120])
    x0=.25;g=4*x0**3-4*x0;h=12*x0**2-4;trial=x0-g/h
    f=lambda x:x**4-2*x**2
    assert g*(trial-x0)>0 and f(trial)>f(x0)
    covariance=np.array([[1.,.7],[.7,2.]]);c=np.linalg.cholesky(covariance);r=np.array([1.,-2.])
    q=np.linalg.solve(c,r);whiten_loss=.5*float(q@q)
    assert abs(whiten_loss-.5*float(r@np.linalg.solve(covariance,r)))<1e-14
    poisson_mle=float(COUNTS.mean());neyman_mle=float(COUNTS.size/np.sum(1/COUNTS))
    assert poisson_mle==3 and abs(neyman_mle-2.0689655172413794)<1e-14
    fit_j=jacobian(fit['theta']);hgn=fit_j.T@fit_j;hfull=hessian(fit['theta'])
    jzero=np.column_stack([np.full(16,1.8),np.zeros(16)])/SIGMA
    assert np.linalg.matrix_rank(jzero)==1 and np.linalg.matrix_rank(fit_j)==2
    receipt={
      'status':'pass','dtype':'float64','seed':SEED,
      'environment':{'python':platform.python_version(),'numpy':np.__version__,
                     'matplotlib':matplotlib.__version__,'executable':'course .venv/bin/python'},
      'model':{'interpretation':'Synthetic scaled excess-flux relaxation, not a full stellar model.',
               't_definition':'time/t0','y_definition':'excess flux/F0','A_true':1.8,'tau_true':2.4,
               'sigma':float(SIGMA),'times':TIMES.tolist(),'data':DATA.tolist(),
               'initial_parameters':[.7,.7],'initial_loss':float(loss(START))},
      'lm':{'fit_log_parameters':fit['theta'].tolist(),'fit_parameters':fit['parameters'].tolist(),
            'loss':fit['loss'],'chi_squared':2*fit['loss'],'nominal_degrees_of_freedom':14,
            'attempts':fit['attempts'],'accepted':fit['accepted'],'rejected':fit['rejected'],
            'reason':fit['reason'],'final_gradient_inf_norm':fit['gradient_inf_norm'],
            'initial_nu':1.,'max_attempts':80,'gradient_tolerance':1e-6,
            'step_method':'augmented numpy.linalg.lstsq with positive identity damping',
            'history':fit['history'],'scipy_reference_parameters':np.exp(reference.x).tolist(),
            'max_log_parameter_difference_from_scipy':float(np.max(np.abs(fit['theta']-reference.x))),
            'loss_difference_from_scipy':abs(fit['loss']-float(loss(reference.x))),
            'gauss_newton':hgn.tolist(),'full_hessian':hfull.tolist(),
            'relative_hessian_frobenius_difference':float(np.linalg.norm(hfull-hgn)/np.linalg.norm(hfull))},
      'complex_step_checks':{'test_log_parameters':theta.tolist(),'step':eps,
             'jacobian_max_absolute_error':jerr,'gradient_max_absolute_error':gerr,
             'hessian_max_absolute_error':herr},
      'scalar_gd':scalar,
      'quadratic_bowl':{'H':H_BOWL.tolist(),'condition_number':50,'optimal_gd_step':2/51,
             'error_contraction_factor':rho,'iterations_for_million_fold_error_reduction':needed,
             'scaled_condition_number':float(np.linalg.cond(scaled_h)),
             'newton_endpoint':(BOWL_START+newton_step).tolist(),
             'heavy_ball_eta':hb_eta,'heavy_ball_beta':hb_beta,
             'heavy_ball_relative_error_after_120':float(np.linalg.norm(hb[-1])/np.linalg.norm(hb[0]))},
      'newton_uphill':{'start':x0,'gradient':g,'hessian':h,'trial':trial,
             'loss_before':f(x0),'loss_after':f(trial),'gradient_dot_step':g*(trial-x0)},
      'whitening':{'covariance':covariance.tolist(),'whitened_loss':whiten_loss},
      'poisson':{'counts':COUNTS.tolist(),'poisson_mle':poisson_mle,'neyman_mle':neyman_mle,
             'limit':'All counts positive. This fixed example illustrates changed weighting, not an ensemble bias study; Neyman expression is undefined for zero counts.'},
      'identifiability':{'t_zero_rank':1,'full_time_rank':2,
             'full_time_singular_values':np.linalg.svd(fit_j,compute_uv=False).tolist()},
      'regularization':{'data_only_minimizer':2.,'prior_precision':1.,
             'penalty_definition':'0.5*z**2','regularized_minimizer':1.},
      'limits':['Engineering checks of fixed teaching examples, not scientific or optimizer benchmarking.',
                'Gaussian synthetic noise and scaled coordinates are specified assumptions.',
                'A successful local fit does not establish global optimality, physical validity, or identifiability.',
                'Heavy-ball parameters are tuned for this SPD quadratic; they are not universal acceleration settings.',
                'Contours in the whitening figure are Mahalanobis radii, not one-dimensional 68 percent intervals.']}
    if write:(ROOT/'numerical-checks.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    return receipt


def main():
    r=numerical_checks()
    for name,make in FIGURES.items():
        fig=make();save_figure(name,fig);plt.close(fig)
    print(f"PASS: {len(FIGURES)} figures; LM {r['lm']['attempts']} attempts "
          f"({r['lm']['accepted']} accepted/{r['lm']['rejected']} rejected); "
          f"A,tau={r['lm']['fit_parameters']}; loss={r['lm']['loss']:.10g}.")


if __name__=='__main__':main()
