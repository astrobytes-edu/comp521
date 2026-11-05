"""Reproducible figures for Lectures 1–2: probability and propagation.

Canonical examples: Jaxstro SciML guide, Sections 1.2–1.7 and Exercise 5.
All data are synthetic. Dimensionless X=M/M_sun, Y=L/L_sun=X**4 is a
local teaching model, not a stellar-evolution calculation. Additional Gaussian,
uniform-input, matrix, and discontinuous examples are explicitly illustrative.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import platform
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import numpy as np

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SEED = 20261105
SAMPLE_SIZE = 200_000
NAVY, TEAL, GOLD = "#20365b", "#087e81", "#d59831"
PALE, GRAY = "#eef5fa", "#697685"
J = np.array([[1.2, 0.5], [0.2, 0.8]], dtype=np.float64)
SIGMA = np.array([[1.0, 0.6], [0.6, 1.0]], dtype=np.float64)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 22,
    "axes.titlesize": 23, "axes.labelsize": 22,
    "xtick.labelsize": 19, "ytick.labelsize": 19,
    "legend.fontsize": 18, "axes.spines.top": False,
    "axes.spines.right": False, "axes.labelcolor": NAVY,
    "text.color": NAVY, "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.edgecolor": "#b5c2cf", "axes.titlepad": 14,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "lines.linewidth": 2.8,
})


def normal_pdf(x, mu=0.0, sigma=1.0):
    x = np.asarray(x, dtype=np.float64)
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    values = np.asarray(x, dtype=np.float64)
    result = np.array([0.5 * (1 + math.erf((float(v) - mu) / (sigma * np.sqrt(2))))
                       for v in values.ravel()]).reshape(values.shape)
    return result.item() if result.ndim == 0 else result


def normal_quantile(p, mu=0.0, sigma=1.0):
    """Bisection for interior teaching quantiles, without a SciPy dependency."""
    if not 0 < p < 1:
        raise ValueError("Quantile probability must be strictly between 0 and 1.")
    lo, hi = mu - 12 * sigma, mu + 12 * sigma
    for _ in range(70):
        mid = (lo + hi) / 2
        if normal_cdf(mid, mu, sigma) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def raw_normal_moment(order, mu=1.0, sigma=0.05):
    moments = [1.0, float(mu)]
    for n in range(2, order + 1):
        moments.append(mu * moments[-1] + (n - 1) * sigma**2 * moments[-2])
    return moments[order]


def quartic_density(y, mu=1.0, sigma=0.05):
    """Exact X**4 density for an untruncated normal, including both branches."""
    y = np.asarray(y, dtype=np.float64)
    result = np.zeros_like(y)
    positive = y > 0
    r = y[positive] ** 0.25
    result[positive] = (normal_pdf(r, mu, sigma) + normal_pdf(-r, mu, sigma)) / (4 * r**3)
    return result


def style(ax, xlabel=None, ylabel=None):
    ax.grid(alpha=0.16, color=NAVY)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def panels(title, n=2, size=(10.4, 5.2)):
    fig, axes = plt.subplots(1, n, figsize=size, layout="constrained")
    fig.suptitle(title, fontsize=24, fontweight="bold")
    return fig, np.atleast_1d(axes)


def pdf_cdf():
    fig, (ax, bx) = panels("Density gives probability through area")
    x = np.linspace(0.80, 1.20, 1501)
    p = normal_pdf(x, 1, .05)
    inside = (x >= .95) & (x <= 1.05)
    ax.plot(x, p, color=TEAL)
    ax.fill_between(x, 0, p, where=inside, color=TEAL, alpha=.23)
    ax.set_title("PDF: shaded area = 0.683")
    ax.set_ylim(0, 9.3)
    ax.set_xticks([.9, 1., 1.1])
    style(ax, r"Mass ratio $x=M/M_\odot$", r"Density $p_X(x)$")
    f = normal_cdf(x, 1, .05)
    bx.plot(x, f, color=TEAL)
    for bound in (.95, 1.05):
        probability = normal_cdf(bound, 1, .05)
        bx.plot([bound, bound], [0, probability], color=TEAL, ls=":", lw=1.7)
        bx.plot([.8, bound], [probability, probability], color=TEAL, ls=":", lw=1.7)
        bx.scatter([bound], [probability], s=48, color=TEAL, zorder=5)
    bx.axhline(.5, color=GOLD, ls="--", lw=2)
    bx.axvline(1., color=GOLD, ls="--", lw=2)
    bx.scatter([1.], [.5], s=65, color=GOLD, zorder=5)
    bx.set_title("CDF: median at $F_X=0.5$")
    bx.set_ylim(-.03, 1.03)
    bx.set_xticks([.9, 1., 1.1])
    bx.set_yticks([0, .5, 1])
    style(bx, r"Mass ratio $x=M/M_\odot$", r"Cumulative probability $F_X(x)$")
    return fig


def mean_standard_error():
    fig, (ax, bx) = panels("Individual spread and precision of a mean differ")
    x = np.linspace(.80, 1.20, 1001)
    ax.plot(x, normal_pdf(x, 1, .05), color=TEAL)
    ax.fill_between(x, 0, normal_pdf(x, 1, .05), color=TEAL, alpha=.15)
    ax.set_title(r"One draw: $\sigma_X=0.05$")
    ax.set_xticks([.9, 1., 1.1])
    style(ax, r"Mass ratio $X=M/M_\odot$", "Probability density")
    x = np.linspace(.97, 1.03, 1001)
    for n, color in [(25, GOLD), (100, NAVY)]:
        se = .05 / np.sqrt(n)
        bx.plot(x, normal_pdf(x, 1, se), color=color, label=f"N={n}: SE={se:g}")
    bx.set_title("Sample mean: narrower spread")
    bx.set_xticks([.98, 1., 1.02])
    bx.annotate("N=25\nSE=0.01", xy=(.987, float(normal_pdf(.987, 1, .01))),
                xytext=(.972, 52), color=GOLD, fontsize=18,
                arrowprops={"arrowstyle":"->", "color":GOLD, "lw":1.7})
    bx.annotate("N=100\nSE=0.005", xy=(1.004, float(normal_pdf(1.004, 1, .005))),
                xytext=(1.009, 72), color=NAVY, fontsize=18,
                arrowprops={"arrowstyle":"->", "color":NAVY, "lw":1.7})
    style(bx, r"Mean mass ratio $\bar{X}$", "Probability density")
    return fig


def joint_conditional():
    fig, (ax, bx) = panels("Conditioning changes the distribution we use")
    rho = .7
    a = np.linspace(-3, 3, 301)
    xx, yy = np.meshgrid(a, a)
    density = np.exp(-(xx**2 - 2*rho*xx*yy + yy**2)/(2*(1-rho**2))) / (2*np.pi*np.sqrt(1-rho**2))
    ax.contourf(xx, yy, density, levels=12, cmap="Blues")
    ax.contour(xx, yy, density, levels=[.03, .07, .13, .20], colors=TEAL, linewidths=1.4)
    ax.axvline(1., color=GOLD, lw=3)
    ax.set_title(r"Synthetic joint: $\rho=0.7$")
    ax.set_aspect("equal")
    ax.set_xticks([-2, 0, 2]); ax.set_yticks([-2, 0, 2])
    style(ax, r"Standardized input $x$", r"Standardized input $y$")
    yy = np.linspace(-3, 3, 1001)
    bx.plot(yy, normal_pdf(yy), color=NAVY, label="Marginal of X or Y")
    bx.plot(yy, normal_pdf(yy, rho, np.sqrt(1-rho**2)), color=GOLD, label="Y given X=1")
    bx.axvline(rho, color=GOLD, ls=":", lw=2)
    bx.set_title("Marginal and conditional")
    bx.legend(frameon=False, fontsize=17, loc="upper left")
    style(bx, r"Standardized value $y$", "Probability density")
    return fig


def change_of_variables():
    fig, (ax, bx) = panels("A nonlinear map changes density, not probability")
    x = np.linspace(.8, 1.2, 1001)
    px = np.full_like(x, 2.5)
    ax.plot(x, px, color=TEAL)
    ax.fill_between(x, 0, px, where=(x >= .95) & (x <= 1.05), color=GOLD, alpha=.45)
    ax.set_xlim(.76, 1.24); ax.set_ylim(0, 3.2)
    ax.set_xticks([.8, 1., 1.2])
    ax.set_title(r"$X\sim U(0.8,1.2)$")
    style(ax, r"Input mass ratio $x$", r"Density $p_X(x)$")
    y = x**4
    py = 2.5 / (4 * y**.75)
    bx.plot(y, py, color=TEAL)
    bx.fill_between(y, 0, py, where=(y >= .95**4) & (y <= 1.05**4), color=GOLD, alpha=.45)
    bx.set_xlim(.35, 2.15); bx.set_ylim(0, 1.5)
    bx.set_xticks([.5, 1., 1.5, 2.])
    bx.set_title(r"$Y=X^4$: shaded area 0.25")
    style(bx, r"Output luminosity ratio $y$", r"Density $p_Y(y)$")
    return fig


def jacobian_grid():
    fig, (ax, bx) = panels("The Jacobian maps local directions and areas")
    for axis, transform in [(ax, np.eye(2)), (bx, J)]:
        for t in np.arange(-2, 2.1, .5):
            for direction in [0, 1]:
                line = np.array([[-2, 2], [t, t]])
                if direction:
                    line = line[::-1]
                out = transform @ line
                axis.plot(out[0], out[1], color="#b7cad7", lw=1.1)
        square = np.array([[0,0], [1,0], [1,1], [0,1]]) @ transform.T
        axis.add_patch(Polygon(square, color=TEAL, alpha=.32, ec=TEAL, lw=2.5))
        axis.axhline(0, color=GRAY, lw=1.2); axis.axvline(0, color=GRAY, lw=1.2)
        axis.set_xlim(-3,3); axis.set_ylim(-3,3); axis.set_aspect("equal")
        axis.set_xticks([-2,0,2]); axis.set_yticks([-2,0,2])
    ax.set_title("Input unit square: area 1")
    bx.set_title(r"Mapped area: $|\det J|=0.86$")
    style(ax, r"Input $x_1$", r"Input $x_2$")
    style(bx, r"Output $y_1$", r"Output $y_2$")
    return fig


def quartic_tangent():
    fig, ax = plt.subplots(figsize=(8.4,5.1), layout="constrained")
    x = np.linspace(.8,1.2,801)
    ax.axvspan(.95,1.05,color=PALE,label=r"Input range $\mu\pm\sigma$")
    ax.plot(x,x**4,color=TEAL,label=r"Nonlinear model $f(x)=x^4$")
    ax.plot(x,1+4*(x-1),color=GOLD,ls="--",label="Tangent at mean input")
    ax.scatter([1],[1],color=NAVY,s=70,zorder=5)
    ax.annotate(r"$f'(1)=4$",xy=(1.06,1.24),xytext=(1.07,.57),
                fontsize=23,arrowprops={"arrowstyle":"->","color":NAVY})
    ax.set_title("Linear propagation uses the local slope",fontweight="bold")
    ax.set_xlim(.8,1.2); ax.set_ylim(.1,2.2)
    ax.set_xticks([.8,.9,1.,1.1,1.2]); ax.legend(frameon=False,fontsize=16,loc="upper left")
    style(ax,r"Input mass ratio $x=M/M_\odot$",r"Output luminosity ratio $y=L/L_\odot$")
    return fig


def pushforward():
    rng=np.random.default_rng(SEED)
    masses=rng.normal(1,.05,SAMPLE_SIZE)
    luminosities=masses**4
    fig,ax=plt.subplots(figsize=(8.4,5.2),layout="constrained")
    ax.hist(luminosities,bins=100,range=(.25,2.5),density=True,
            color=TEAL,alpha=.25,label="Monte Carlo pushforward")
    y=np.linspace(.25,2.5,2001)
    ax.plot(y,quartic_density(y),color=TEAL,label="Exact transformed density")
    ax.plot(y,normal_pdf(y,1,.2),color=GOLD,ls="--",label="First-order Gaussian")
    ax.axvline(1,color=GRAY,lw=1.7,ls=":")
    ax.axvline(raw_normal_moment(4),color=NAVY,lw=1.7)
    ax.set_xlim(.35,2.); ax.set_ylim(0,2.5)
    ax.set_title("Symmetric mass uncertainty becomes skewed light",fontweight="bold")
    ax.legend(frameon=False,fontsize=16,loc="upper right")
    ax.text(.97,.52,"Exact mean: 1.01502\nLinearized mean: 1.00000",
            transform=ax.transAxes,ha="right",va="top",fontsize=18,color=NAVY)
    style(ax,r"Luminosity ratio $y=L/L_\odot$","Probability density")
    return fig


def add_covariance_contours(ax,covariance,color):
    values,vectors=np.linalg.eigh(covariance)
    angle=np.degrees(np.arctan2(vectors[1,-1],vectors[0,-1]))
    for radius,alpha in [(2.,.12),(1.,.22)]:
        ellipse=Ellipse((0,0),2*radius*np.sqrt(values[-1]),2*radius*np.sqrt(values[0]),
                        angle=angle,facecolor=color,edgecolor=color,alpha=alpha,lw=2.5)
        ax.add_patch(ellipse)
    theta=np.linspace(0,2*np.pi,361)
    circle=np.array([np.cos(theta),np.sin(theta)])
    for radius in [1,2]:
        points=vectors @ (np.sqrt(values)[:,None]*circle)*radius
        ax.plot(points[0],points[1],color=color,lw=2)


def covariance_map():
    fig,(ax,bx)=panels(r"Forward propagation: $\Sigma_Y=J\Sigma_XJ^{\mathrm{T}}$")
    output=J@SIGMA@J.T
    add_covariance_contours(ax,SIGMA,TEAL)
    add_covariance_contours(bx,output,GOLD)
    ax.set_title("Input Gaussian contours")
    bx.set_title("Output Gaussian contours")
    for axis in [ax,bx]:
        axis.set_xlim(-4,4);axis.set_ylim(-4,4);axis.set_aspect("equal")
        axis.set_xticks([-3,0,3]);axis.set_yticks([-3,0,3])
        axis.axhline(0,color=GRAY,lw=1);axis.axvline(0,color=GRAY,lw=1)
    style(ax,r"Input $x_1$",r"Input $x_2$")
    style(bx,r"Output $y_1$",r"Output $y_2$")
    return fig


def phase_boundary():
    rng=np.random.default_rng(SEED+1)
    samples=rng.normal(-.05,.1,SAMPLE_SIZE)
    outputs=samples+.8*(samples>=0)
    fig,(ax,bx)=panels("Synthetic threshold: one local slope misses a branch")
    left=np.linspace(-.4,0,401,endpoint=False);right=np.linspace(0,.3,301)
    ax.axvspan(-.15,.05,color=PALE)
    ax.plot(left,left,color=TEAL);ax.plot(right,right+.8,color=TEAL)
    ax.scatter([0],[0],s=55,fc="white",ec=TEAL,lw=2,zorder=5)
    ax.scatter([0],[.8],s=55,color=TEAL,zorder=5)
    x=np.linspace(-.4,.3,801)
    ax.plot(x,x,color=GOLD,ls="--",label="Smooth/local linear map")
    ax.axvline(0,color=GRAY,ls=":",lw=1.8)
    ax.set_title("Synthetic jump at x=0")
    ax.set_xlim(-.4,.3);ax.set_ylim(-.45,1.15)
    ax.set_xticks([-.3,0,.3]);ax.legend(frameon=False,fontsize=15,loc="upper left")
    style(ax,"Synthetic input x","Synthetic output y")
    bx.hist(outputs,bins=100,range=(-.45,1.15),density=True,color=TEAL,alpha=.35,label="Full sample propagation")
    y=np.linspace(-.45,1.15,1001)
    bx.plot(y,normal_pdf(y,-.05,.1),color=GOLD,ls="--",label="Local linear prediction")
    bx.set_title("Full versus local propagation")
    bx.set_xlim(-.45,1.15);bx.set_xticks([-.3,0,.5,1.])
    bx.legend(frameon=False,fontsize=15,loc="upper right")
    style(bx,"Synthetic output y","Probability density")
    return fig


def shared_shifts():
    rng=np.random.default_rng(SEED+2)
    n=24
    eps=rng.normal(0,.2,(3,n))
    # Selected possible shared offsets illustrate the predictive ensemble.
    offsets=np.array([-.15,0.,.15],dtype=np.float64)
    colors=[TEAL,GOLD,NAVY]
    fig,(ax,bx)=panels("Shared physics moves an entire possible data set")
    for k,color in enumerate(colors):
        x=np.arange(1,n+1)
        ax.scatter(x,eps[k],s=34,color=color,alpha=.75)
        bx.scatter(x,eps[k]+offsets[k],s=34,color=color,alpha=.75)
        bx.axhline(offsets[k],color=color,lw=2,ls="--")
    for axis in [ax,bx]:
        axis.set_ylim(-.7,.7);axis.set_xlim(0,n+1)
        axis.set_xticks([1,12,24]);axis.set_yticks([-.5,0,.5])
        axis.axhline(0,color=GRAY,lw=1)
        style(axis,"Star index i","Synthetic observable")
    ax.set_title(r"Independent scatter: $\epsilon_i$")
    bx.set_title(r"Shared offset: $Y_i=\theta+\epsilon_i$")
    return fig


def shared_floor():
    fig,ax=plt.subplots(figsize=(8.4,5.1),layout="constrained")
    n=np.geomspace(1,1000,1001)
    correct=np.sqrt(.1**2+.2**2/n)
    naive=np.sqrt((.1**2+.2**2)/n)
    ax.plot(n,correct,color=TEAL,label=r"Shared: $\sqrt{0.1^2+0.2^2/N}$")
    ax.plot(n,naive,color=GOLD,ls="--",label="Incorrectly independent")
    ax.axhline(.1,color=NAVY,ls=":",lw=2,label="Unconstrained shared floor: 0.1")
    ax.scatter([100],[np.sqrt(.0104)],s=70,color=TEAL,zorder=5)
    ax.annotate("N=100: SD=0.102",xy=(100,np.sqrt(.0104)),xytext=(9,.15),
                fontsize=21,arrowprops={"arrowstyle":"->","color":NAVY})
    ax.set_xscale("log");ax.set_xlim(1,1000);ax.set_ylim(0,.25)
    ax.set_xticks([1,10,100,1000],labels=["1","10","100","1000"])
    ax.set_title("A shared uncertainty sets a predictive floor",fontweight="bold",fontsize=22)
    ax.legend(frameon=False,fontsize=16,loc="upper right")
    style(ax,"Number of stars N",r"Predictive SD of the mean $\bar{Y}$")
    return fig


FIGURES = {
    "pdf-cdf.png":pdf_cdf,
    "mean-standard-error.png":mean_standard_error,
    "joint-conditional.png":joint_conditional,
    "change-of-variables.png":change_of_variables,
    "jacobian-grid.png":jacobian_grid,
    "quartic-tangent.png":quartic_tangent,
    "pushforward.png":pushforward,
    "covariance-map.png":covariance_map,
    "phase-boundary.png":phase_boundary,
    "shared-shifts.png":shared_shifts,
    "shared-floor.png":shared_floor,
}


def save_figure(name,fig):
    if name not in FIGURES:
        raise ValueError(f"Unknown figure: {name}")
    ASSETS.mkdir(parents=True,exist_ok=True)
    fig.savefig(ASSETS/name,dpi=180,bbox_inches="tight")
    return ASSETS/name


def numerical_checks(write=True):
    """Focused analytic checks plus bounded seeded Monte Carlo comparisons."""
    rng=np.random.default_rng(SEED)
    x=rng.normal(1,.05,SAMPLE_SIZE).astype(np.float64)
    y=x**4
    exact_mean=raw_normal_moment(4)
    exact_var=raw_normal_moment(8)-exact_mean**2
    exact_sd=math.sqrt(exact_var)
    mc_mean=float(np.mean(y));mc_sd=float(np.std(y,ddof=1))
    mc_se=mc_sd/math.sqrt(SAMPLE_SIZE)
    mean_z=(mc_mean-exact_mean)/mc_se
    assert x.dtype==np.float64
    assert abs(exact_mean-1.01501875)<1e-13
    assert abs(mean_z)<5, "Seeded MC mean is outside five estimated standard errors."
    mass=np.linspace(.5,1.5,10001)
    normal_area=float(np.trapezoid(normal_pdf(mass,1,.05),mass))
    assert abs(normal_area-1)<1e-12
    probs=[.025,.16,.5,.84,.975]
    quantile_residual=max(abs(normal_cdf(normal_quantile(p,1,.05),1,.05)-p) for p in probs)
    assert quantile_residual<1e-13
    # Positive uniform input gives an exactly monotone density transformation.
    positive=np.linspace(.8,1.2,20001)
    transformed=positive**4
    change_area=float(np.trapezoid(2.5/(4*transformed**.75),transformed))
    assert abs(change_area-1)<2e-8
    det=float(np.linalg.det(J));assert abs(det-.86)<1e-14
    out_cov=J@SIGMA@J.T
    assert np.allclose(out_cov,[[2.41,1.276],[1.276,.872]],rtol=0,atol=1e-14)
    rng_cov=np.random.default_rng(SEED+3)
    inputs=rng_cov.multivariate_normal([0,0],SIGMA,SAMPLE_SIZE)
    outputs=inputs@J.T
    sample_cov=np.cov(outputs,rowvar=False,ddof=1)
    cov_se=np.sqrt((out_cov**2+np.outer(np.diag(out_cov),np.diag(out_cov)))/(SAMPLE_SIZE-1))
    cov_z=(sample_cov-out_cov)/cov_se
    assert np.max(np.abs(cov_z))<5
    correct_floor=math.sqrt(.1**2+.2**2/100)
    naive_floor=math.sqrt((.1**2+.2**2)/100)
    assert abs(correct_floor-.10198039027185571)<1e-14
    within10=math.ceil(.2**2/(.1**2*(1.1**2-1)))
    assert within10==20
    # Exact Gaussian fourth central moment of Y supplies the MC SD uncertainty.
    central4=sum(math.comb(4,k)*(-exact_mean)**(4-k)*raw_normal_moment(4*k) for k in range(5))
    variance_se=math.sqrt((central4-exact_var**2)/SAMPLE_SIZE)
    sd_se=variance_se/(2*exact_sd)
    sd_z=(mc_sd-exact_sd)/sd_se
    assert abs(sd_z)<5
    report={
        "status":"pass", "seed":SEED,"sample_size":SAMPLE_SIZE,"dtype":"float64",
        "environment":{"python":platform.python_version(),"executable":"course .venv/bin/python",
                       "numpy":np.__version__,"matplotlib":matplotlib.__version__},
        "sources":["Jaxstro SciML guide Sections 1.2–1.7", "Lecture 1 Exercise 5"],
        "quartic":{"input_mean":1.0,"input_sd":.05,"exact_mean":exact_mean,"exact_sd":exact_sd,
                   "delta1_mean":1.0,"delta1_sd":.2,"delta2_mean":1.015,
                   "mc_mean":mc_mean,"mc_sd":mc_sd,"mc_mean_standard_error":mc_se,
                   "mc_mean_error_in_standard_errors":mean_z,
                   "mc_sd_standard_error_approx":sd_se,"mc_sd_error_in_standard_errors":sd_z,
                   "density_uses_both_inverse_branches":True},
        "normal_pdf_cdf":{"integral":normal_area,"quantile_roundtrip_max_abs_error":quantile_residual,
                          "probability_between_0.95_and_1.05":normal_cdf(1.05,1,.05)-normal_cdf(.95,1,.05)},
        "positive_uniform_change_of_variables":{"input_interval":[.8,1.2],"transformed_density_integral":change_area,
                                                 "matched_input_interval":[.95,1.05],"matched_probability":.25},
        "linear_map":{"J":J.tolist(),"determinant":det,"input_covariance":SIGMA.tolist(),
                      "output_covariance":out_cov.tolist(),"sample_covariance":sample_cov.tolist(),
                      "covariance_entry_standard_errors":cov_se.tolist(),"entry_error_in_standard_errors":cov_z.tolist()},
        "source_covariance_exercise":{"sigma1":2,"sigma2":3,"rho":-.5,"sum_variance":7,"difference_variance":19},
        "shared_floor":{"sigma_theta":.1,"sigma_epsilon":.2,"N100_correct_sd":correct_floor,
                        "N100_naive_sd":naive_floor,"minimum_N_within_10_percent_of_floor":within10,
                        "interpretation":"Predictive ensemble with unconstrained shared offset; not posterior uncertainty after calibration."},
        "limits":["Synthetic teaching calculations, not stellar-model validation.",
                  "Gaussian mass approximation has nonphysical negative support 20 standard deviations below its mean.",
                  "Linear covariance propagation is exact only for the displayed linear map; nonlinear use is a local approximation.",
                  "The phase-boundary example is a synthetic discontinuity, not a physical stellar-mass threshold.",
                  "Covariance contours have Mahalanobis radii 1 and 2; no 68 percent claim is made.",
                  "Five-standard-error Monte Carlo checks are engineering diagnostics for this frozen illustrative seed, not scientific qualification."]}
    if write:
        (ROOT/"numerical-checks.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


def main():
    report=numerical_checks()
    for name,make in FIGURES.items():
        fig=make();save_figure(name,fig);plt.close(fig)
    print(f"PASS: {len(FIGURES)} figures; MC mean {report['quartic']['mc_mean']:.8f} ± "
          f"{report['quartic']['mc_mean_standard_error']:.2g}; exact {report['quartic']['exact_mean']:.8f}.")


if __name__=="__main__":
    main()
