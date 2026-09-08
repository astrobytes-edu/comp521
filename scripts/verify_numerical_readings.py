"""Execute reading examples and check the audit's mathematical counterexamples.

Outputs are written to a temporary review directory; course text is not edited.
Run: .venv/bin/python -B scripts/verify_numerical_readings.py
"""
from pathlib import Path
import ast
import contextlib
import io
import json
import os
import re
import tempfile

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/comp521-audit-mpl")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.mkdtemp(prefix="comp521-reading-verification-"))

def main():
    spaces, results, failures = {}, [], []
    for path in sorted((ROOT / "05-numerical-methods").rglob("*.md")):
        source = path.read_text()
        ns = {"__name__": "__reading_review__"}
        spaces[path.name] = ns
        cells = re.findall(r"^```\{code-cell\} python\n(.*?)^```", source, re.M | re.S)
        for number, cell in enumerate(cells, 1):
            code = re.sub(r"^:[^\n]*\n", "", cell, flags=re.M)
            stream = io.StringIO()
            status = "pass"
            try:
                with contextlib.redirect_stdout(stream):
                    exec(compile(code, str(path), "exec"), ns)
                for fignum in plt.get_fignums():
                    plt.figure(fignum).savefig(OUT / f"{path.stem}-{number}-{fignum}.png", dpi=100)
            except Exception as exc:
                status = f"{type(exc).__name__}: {exc}"
                failures.append((str(path), number, status))
            finally:
                plt.close("all")
            results.append(dict(file=str(path.relative_to(ROOT)), cell=number, status=status, output=stream.getvalue()))
        # Syntax-check static examples and load isolated function definitions.
        for code in re.findall(r"^```python\n(.*?)^```", source, re.M | re.S):
            try:
                tree = ast.parse(code)
                if all(isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom)) for n in tree.body) and not any(x in code for x in ("jax", "from integrate")):
                    exec(compile(tree, str(path), "exec"), ns)
            except Exception as exc:
                failures.append((str(path), "static", str(exc)))
        for asset in re.findall(r"^:::.*\{figure\} ([^\n]+)", source, re.M):
            if not (path.parent / asset).is_file():
                failures.append((str(path), "figure", asset))
        if re.search(r'!\[.*\]\(.*\)\{#', source):
            failures.append((str(path), "figure", "literal attribute syntax"))
    (OUT / "cell-results.json").write_text(json.dumps(results, indent=2))
    print(f"{len(results)} executable cells: {sum(r['status']=='pass' for r in results)} passed")
    if failures:
        print(json.dumps(failures, indent=2))
        raise SystemExit(1)

    errors = spaces['02-mod1-part2-numerical-errors.md']
    assert errors['good_error'] < errors['bad_error'] / 100
    assert errors['absolute_relative_error'](2e-8, 1e-8, zero_scale=1e5)['relative_error'] == 1.0
    assert np.isnan(errors['absolute_relative_error'](1., 0.)['relative_error'])
    fd = spaces['01-mod1-part1-finite-differences.md']['finite_diff']
    for h in (np.nan, np.inf, 0., -1.):
        expect_error(lambda: fd(lambda x: 1., 1., h), ValueError)
    taylor = spaces['03-mod1-part3-taylor-series.md']
    assert taylor['finite_difference_call_count'](10, 'forward') == 11
    assert taylor['finite_difference_call_count'](10, 'central') == 20
    root = spaces['01-mod2-part1-root-finding.md']
    assert np.allclose(root['root_half_ranges'], [.002, .04], rtol=1e-14, atol=0)
    for scale in (1., 1e-12, 1e-200):
        assert abs(root['bisection'](lambda x: scale*(x-.9), 0., 1.)-.9) <= 1e-10
    expect_error(lambda: root['bisection'](lambda x: 1e-200*(x+1), 0., 1.), ValueError)
    expect_error(lambda: root['bisection'](lambda x: np.nan, 0., 1.), ValueError)
    assert root['find_brackets'](lambda x: x-.5, 0., 1.) == [(.5,.5)]
    quadrature = spaces['02-mod2-part2-quadrature.md']
    for name, expected in [('smooth', 4), ('kink', 2), ('split', 4)]:
        values = quadrature['reference_errors'][name]
        assert np.all(np.abs(np.log2(values[:-1]/values[1:])-expected) < .05)
    budget = spaces['03-mod2-synthesis.md']
    assert np.all(budget['actual_errors'] < budget['position_bounds'])
    assert np.all(budget['actual_errors'] > 1000*budget['computed_residuals'])
    assert np.all(np.diff(budget['actual_errors']) < 0)
    assert quadrature['estimated_error'] < 1e-20
    assert abs(quadrature['corrected']-.5) > .49
    for n in (8, 64, 128):
        value = quadrature['rectangle'](np.sin, 0., np.pi/2, n)
        assert 0 < 1-value <= np.pi**2/(8*n)
    # A quadratic isolates the disputed trapezoid coefficient exactly.
    h, m = .1, .5
    trap=h*((m-h/2)**2+(m+h/2)**2)/2
    exact=((m+h/2)**3-(m-h/2)**3)/3
    assert np.isclose((trap-h*m*m)/(2*h**3),1/8,rtol=1e-12)
    assert np.isclose((exact-trap)/(2*h**3),-1/12,rtol=1e-12)
    ode = spaces['02-module3-part2-runge-kutta.md']
    coarse_t, coarse_y = ode['euler_sho'](200, 1)
    fine_t, fine_y = ode['euler_sho'](400, 1)
    coarse = ode['sho_diagnostics'](coarse_t, coarse_y)[-1][-1]
    fine = ode['sho_diagnostics'](fine_t, fine_y)[-1][-1]
    observed = np.log2(coarse/fine)
    assert abs(observed-1) < .12
    print(f'Euler fixed-duration state order: {observed:.3f}')
    exact = np.column_stack((np.cos(fine_t), -np.sin(fine_t)))
    assert np.max(ode['sho_diagnostics'](fine_t, exact)[-1]) == 0
    expect_error(lambda: ode['sho_diagnostics']([0,1], [[1,0]]), ValueError)
    times, values, trials = ode['adaptive_euler_decay'](1e-3, 1e-5)
    assert trials[0,3] == 0 and trials[0,0] == trials[1,0]
    assert np.all(trials[trials[:,3].astype(bool),2] <= 1)
    assert times[-1] == 4.0 and np.all(np.diff(times) > 0)
    tight_times, tight_values, _ = ode['adaptive_euler_decay'](1e-4, 1e-5)
    assert abs(tight_values[-1]-np.exp(-4)) < abs(values[-1]-np.exp(-4))
    decay = spaces['05-mod3-synthesis.md']
    for bad_step in (0, -1, np.inf, np.nan):
        expect_error(lambda: decay['euler_decay_trace'](bad_step), ValueError)
    assert np.min(decay['euler_decay_trace'](1.5)[1]) < 0
    assert abs(decay['euler_decay_trace'](1.5)[1][-1]) < 1
    assert abs(decay['euler_decay_trace'](3.)[1][-1]) > 1
    foundation = spaces['04-mod1-synthesis.md']
    assert all(np.any(e <= foundation['absolute_target']) for e in foundation['errors_probe'].values())
    estimate = foundation['derivative_estimate'](foundation['perturbed_function'], .7, 1e-5, 'central')
    offset = estimate-foundation['reference_probe']
    assert np.isclose(offset, foundation['perturbation_derivative'], rtol=.01, atol=0)
    # Guard the student implementation boundary in public executable examples.
    for path in (ROOT/'05-numerical-methods').rglob('*.md'):
        for code in re.findall(r"^```(?:\{code-cell\} )?python\n(.*?)^```", path.read_text(), re.M|re.S):
            assert not re.search(r"def (?:rk[24](?:_step)?|oscillator_step)\s*\(", code), path
    stability=spaces['04-module3-part4-stability.md']
    assert not stability['stability_test'](lambda y,lam,h: np.nan,-1.,[.1])[0][1]
    value=stability['backward_euler_step'](np.array([1.]),0.,.01,lambda y,t:-1000*y,lambda y,t:np.array([[-1000.]]))
    assert np.allclose(value,[1/11],rtol=1e-12,atol=0.)
    print('Audit counterexamples, derivative investigation, Euler adaptation, physical decay, and student-code boundary: passed')
    print('Evidence:', OUT)

def expect_error(call, kind):
    try: call()
    except kind: return
    raise AssertionError(f'Expected {kind.__name__}')

if __name__ == '__main__': main()
