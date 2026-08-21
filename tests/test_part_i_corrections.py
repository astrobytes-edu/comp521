"""Executable regression checks for corrected Part I teaching examples."""

from __future__ import annotations

import copy
import math
import re
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]


def code_block_after(path: str, marker: str) -> str:
    """Return the first Python fence after a visible Markdown marker."""
    text = (ROOT / path).read_text()
    remainder = text[text.index(marker) :]
    match = re.search(r"```(?:\{code-cell\} )?python\n(.*?)\n```", remainder, re.DOTALL)
    assert match, f"no Python block after {marker!r} in {path}"
    return match.group(1)


def code_block_containing(path: str, marker: str) -> str:
    """Return the Python fence that contains a distinctive source marker."""
    text = (ROOT / path).read_text()
    blocks = re.findall(r"```(?:\{code-cell\} )?python\n(.*?)\n```", text, re.DOTALL)
    for block in blocks:
        if marker in block:
            return block
    raise AssertionError(f"no Python block containing {marker!r} in {path}")


def test_complete_chapter_1_script_compiles_and_imports_cleanly():
    script = code_block_after("03-python/01-python-environment.md", "Complete calculation.py Script")
    assert "\n\timport numpy" not in script
    namespace = {"__name__": "imported_example"}
    exec(compile(script, "calculation.py", "exec"), namespace)
    assert namespace["schwarzschild_radius"](10 * namespace["M_sun"]) == pytest.approx(29_533.39, rel=1e-5)


def test_chapter_1_notebook_state_activity_is_markdown_authored_with_lite_execution():
    chapter = (ROOT / "03-python/01-python-environment.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch01-notebook-state.md").read_text()
    assert "## Try this chapter" in chapter
    assert "Browser Python lab · Notebook State Detective" in chapter
    assert "jupyterlite/ch01-notebook-state.html" in chapter
    assert "activity is optional" in chapter
    assert "```{code-cell} python" in activity
    assert "name: xpython" in activity
    assert "# Cell 4: inspect whether stored and current state agree" in activity
    assert "Restart Kernel and Run All Cells" in activity
    assert "Success condition" in activity
    assert "calculate_result.__defaults__" not in activity
    assert "does **not** tell" in activity


def test_chapter_1_notebook_state_activity_exposes_stale_derived_state_only_out_of_order():
    activity = (ROOT / "tools/jupyterlite/activities/ch01-notebook-state.md").read_text()
    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 4

    out_of_order: dict[str, object] = {}
    for index in (0, 2, 1, 3):
        exec(compile(cells[index], f"cell-{index + 1}", "exec"), out_of_order)

    assert out_of_order["recorded_param_a"] == 70.0
    assert out_of_order["param_a"] == 67.4
    assert out_of_order["result"] != pytest.approx(out_of_order["calculate_result"](1000))

    clean: dict[str, object] = {}
    for index, cell in enumerate(cells):
        exec(compile(cell, f"cell-{index + 1}", "exec"), clean)

    assert clean["recorded_param_a"] == clean["param_a"] == 67.4
    assert clean["result"] == pytest.approx(clean["calculate_result"](1000))


def test_chapter_1_separates_core_route_from_reference_and_avoids_false_validation():
    chapter = (ROOT / "03-python/01-python-environment.md").read_text()
    assert "hide_outline: true" in chapter
    assert "## Reference: diagnosing imports and interpreter mismatches" in chapter
    assert "## Core check: investigate a discrepant run" in chapter
    assert "## Reference: environments, paths, and random generators" in chapter
    assert "report_numerical_context" in chapter
    assert "validate_computation_environment" not in chapter
    assert "safe_calculation" not in chapter


def test_chapter_1_notebook_state_launcher_preserves_the_notebook_path():
    launcher = (ROOT / "tools/jupyterlite/launchers/ch01-notebook-state.html").read_text()
    assert "lab/index.html?path=ch01-notebook-state.ipynb" in launcher
    assert "window.location.replace" in launcher


def test_stable_quadratic_example_handles_named_boundary_cases():
    code = code_block_after("03-python/02-python-calculator.md", "quadratic formula")
    namespace: dict[str, object] = {}
    exec(code, namespace)
    roots = namespace["quadratic_roots_stable"]
    assert sorted(roots(1, 0, -1)) == pytest.approx([-1, 1])
    assert roots(1, 0, 0) == (0.0, 0.0)
    assert roots(1, 0, 1) == (None, None)
    with pytest.raises(ValueError):
        roots(0, 1, 1)


def test_logsumexp_example_is_finite_when_direct_exponentiation_underflows():
    code = code_block_after("03-python/02-python-calculator.md", "For products of many positive factors")
    namespace = {"math": math}
    exec(code, namespace)
    assert namespace["logsumexp"]([-1000.0, -1001.0]) == pytest.approx(-999.6867383124818)
    assert namespace["logsumexp"]([-math.inf, -math.inf]) == -math.inf


def test_chapter_2_calibrates_comparisons_and_avoids_generic_validation_claims():
    chapter = (ROOT / "03-python/02-python-calculator.md").read_text()
    assert "rel_tol=0.0" in chapter
    assert "measurement_resolution_m_s" in chapter
    assert "A passing numerical comparison tests that stated" in chapter
    assert "validate_magnitude" not in chapter
    assert "schwarzschild_radius_robust" not in chapter
    assert "m^(5/2)/s^2 (not a velocity)" in chapter
    assert "Small-angle approximation" in chapter
    assert "Modeling boundary: a Fourier peak is not a discovery" in chapter


def test_chapter_2_stable_function_examples_make_the_difference_visible():
    chapter = (ROOT / "03-python/02-python-calculator.md").read_text()
    assert "x = 1e-16" in chapter
    assert "y = 1e-16" in chapter
    assert math.exp(1e-16) - 1 == 0.0
    assert math.expm1(1e-16) == pytest.approx(1e-16)
    assert math.log(1 + 1e-16) == 0.0
    assert math.log1p(1e-16) == pytest.approx(1e-16)


def test_chapter_2_checked_schwarzschild_script_uses_a_meaningful_scaling_check():
    code = code_block_after(
        "03-python/02-python-calculator.md",
        "## Reference preview: from a checked calculation to reusable code",
    )
    namespace = {"__name__": "imported_example"}
    exec(compile(code, "schwarzschild_radius.py", "exec"), namespace)
    radius = namespace["schwarzschild_radius_checked"]
    solar_mass_kg = 1.989e30
    assert radius(solar_mass_kg) == pytest.approx(2_952.075, rel=1e-5)
    assert radius(2 * solar_mass_kg) == pytest.approx(2 * radius(solar_mass_kg), rel=1e-15)
    with pytest.raises(ValueError):
        radius(0.0)


def test_chapter_2_numerical_claim_inspector_is_markdown_authored_and_discriminating():
    chapter = (ROOT / "03-python/02-python-calculator.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch02-numerical-claim-inspector.md").read_text()
    launcher = (ROOT / "tools/jupyterlite/launchers/ch02-numerical-claim-inspector.html").read_text()
    assert "## Try this chapter" in chapter
    assert "Browser Python lab · Numerical Claim Inspector" in chapter
    assert "jupyterlite/ch02-numerical-claim-inspector.html" in chapter
    assert "activity is optional" in chapter
    assert "name: xpython" in activity
    assert "Success condition" in activity
    assert "does\n**not** provide" in activity
    assert "lab/index.html?path=ch02-numerical-claim-inspector.ipynb" in launcher

    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 3
    namespace: dict[str, object] = {}
    for index, cell in enumerate(cells, start=1):
        exec(compile(cell, f"chapter-2-activity-cell-{index}", "exec"), namespace)

    direct, stable = namespace["inspect_angle"](1e-8)
    assert direct == 0.0
    assert stable > 0.0
    assert namespace["within_resolution"](1e-4, 1e-3)
    assert not namespace["within_resolution"](1e-4, 1e-5)


def test_chapter_3_calibrates_toy_stellar_and_schwarzschild_examples():
    text = (ROOT / "03-python/03-python-control-flow.md").read_text()
    assert "classify_stellar_fate_toy" in text
    assert "not a remnant" in text
    assert "rs_au = 1.97e-8 * M" in text
    assert "difference of two large aggregate terms" in text


def test_chapter_3_bounded_convergence_reports_its_stopping_contract():
    code = code_block_after("03-python/03-python-control-flow.md", "Predict before running")
    namespace: dict[str, object] = {}
    exec(compile(code, "bounded_convergence.py", "exec"), namespace)
    bounded_relaxation = namespace["bounded_relaxation"]

    _, status, iterations = bounded_relaxation(100.0, 1.0, 0.1, 0.01, 5)
    assert (status, iterations) == ("max_iterations_reached", 5)

    _, status, iterations = bounded_relaxation(100.0, 1.0, 0.1, 0.01, 100)
    assert status == "converged"
    assert iterations < 100

    with pytest.raises(ValueError):
        bounded_relaxation(100.0, 1.0, 0.0, 0.01, 5)
    with pytest.raises(ValueError):
        bounded_relaxation(100.0, 1.0, 0.1, 0.0, 5)


def test_chapter_3_keeps_advanced_syntax_and_reference_with_explicit_limits():
    text = (ROOT / "03-python/03-python-control-flow.md").read_text()
    assert "### The Walrus Operator: Assignment Expressions" in text
    assert "### The Ternary Operator: Compact Conditionals" in text
    assert "### Loop Control: `break`, `continue`, and `else`" in text
    assert "## Deep Dive: advanced control flow patterns" in text
    assert "## Reference: quick tables and debugging tools" in text
    assert "| `:=` | Walrus operator" in text
    assert "zip(times, positions, strict=True)" in text
    assert "zip(star_masses, star_positions, strict=True)" in text
    assert "zip(redshifts, luminosities, strict=True)" in text
    assert 'RETURN failure("no acceptable step within MAX_ATTEMPTS")' in text
    assert "Never use **==** with floating-point numbers!" not in text
    assert "List comprehensions are faster than loops" not in text


def test_chapter_3_bounded_convergence_activity_is_markdown_authored_and_discriminating():
    chapter = (ROOT / "03-python/03-python-control-flow.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch03-bounded-convergence-inspector.md").read_text()
    launcher = (ROOT / "tools/jupyterlite/launchers/ch03-bounded-convergence-inspector.html").read_text()
    assert "## Try this chapter" in chapter
    assert "Browser Python lab · Bounded Convergence Inspector" in chapter
    assert "jupyterlite/ch03-bounded-convergence-inspector.html" in chapter
    assert "activity is optional" in chapter
    assert "name: xpython" in activity
    assert "Success condition" in activity
    assert "does\n**not** select" in activity
    assert "lab/index.html?path=ch03-bounded-convergence-inspector.ipynb" in launcher

    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 3
    namespace: dict[str, object] = {}
    for index, cell in enumerate(cells, start=1):
        exec(compile(cell, f"chapter-3-activity-cell-{index}", "exec"), namespace)

    bounded_relaxation = namespace["bounded_relaxation"]
    _, short_status, _ = bounded_relaxation(100.0, 1.0, 0.1, 0.01, 5)
    _, long_status, _ = bounded_relaxation(100.0, 1.0, 0.1, 0.01, 100)
    assert short_status == "max_iterations_reached"
    assert long_status == "converged"


def test_chapter_4_calibrates_collection_performance_and_eos_analogy():
    text = (ROOT / "03-python/04-python-data-structures.md").read_text()
    assert "average-case hash lookup" in text
    assert "not a substitute for profiling the real workload" in text
    assert "a lookup is not a neighbor algorithm" in text
    assert "object; ownership-dependent" in text
    assert "header only!" not in text
    assert "1000$\\times$ speedup" not in text
    assert "## Deep Dive: Memory, Caches, and Benchmarks" in text
    assert "## Reference: Structures, Operations, and Modules" in text
    assert "## Try this chapter" in text
    assert "Browser Python lab · Aliasing and Lookup Inspector" in text


def test_chapter_4_aliasing_activity_is_markdown_authored_and_discriminating():
    chapter = (ROOT / "03-python/04-python-data-structures.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch04-aliasing-and-lookup-inspector.md").read_text()
    launcher = (ROOT / "tools/jupyterlite/launchers/ch04-aliasing-and-lookup-inspector.html").read_text()
    assert "jupyterlite/ch04-aliasing-and-lookup-inspector.html" in chapter
    assert "activity is optional" in chapter
    assert "name: xpython" in activity
    assert "Success condition" in activity
    assert "does **not** select" in activity
    assert "lab/index.html?path=ch04-aliasing-and-lookup-inspector.ipynb" in launcher

    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 3
    namespace: dict[str, object] = {}
    for index, cell in enumerate(cells, start=1):
        exec(compile(cell, f"chapter-4-activity-cell-{index}", "exec"), namespace)

    initial = [[20.0, 20.0], [20.0, 50.0]]
    for mode, expected_original_center in (("assignment", 35.0), ("shallow", 35.0), ("deep", 50.0)):
        original = copy.deepcopy(initial)
        working = namespace["copy_grid"](original, mode)
        working[1][1] = 35.0
        assert original[1][1] == expected_original_center


def test_trapezoid_example_labels_its_approximation_and_executes():
    code = code_block_after("03-python/05-python-functions-modules.md", "### Documentation Levels")
    namespace: dict[str, object] = {}
    exec(code, namespace)
    assert namespace["result"] == pytest.approx(2.75)
    integrate = namespace["integrate_trapezoid"]
    with pytest.raises(ValueError, match="at least two"):
        integrate([0.0], [0.0])
    with pytest.raises(ValueError, match="strictly increasing"):
        integrate([0.0, 0.0], [0.0, 0.0])
    text = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    assert "trapezoidal *approximation*" in text
    assert "Local input checks" in text
    assert "# PSEUDOCODE: set_mode" in text


def test_chapter_5_exposes_a_contract_first_route_and_calibrated_extensions():
    text = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    kinetic_code = code_block_after("03-python/05-python-functions-modules.md", "### Kinetic Energy in CGS Units")
    namespace: dict[str, object] = {}
    exec(kinetic_code, namespace)
    kinetic_energy = namespace["kinetic_energy_cgs"]
    assert kinetic_energy(2.0, 3.0) == pytest.approx(9.0)
    with pytest.raises(ValueError, match="nonnegative"):
        kinetic_energy(-1.0, 1.0)
    with pytest.raises(ValueError, match="finite"):
        kinetic_energy(1.0, math.inf)
    assert "hide_outline: true" in text
    assert "## Try this chapter" in text
    assert "## Deep Dive: Closures, Higher-Order Functions, and Functional Interfaces" in text
    assert "## Deep Dive: Measure and Cache a Stated Workload" in text
    assert "## Reference: Function Signatures, Imports, and Typing" in text
    assert "Python's built-in\n# map() does not itself promise GPU execution" in text
    assert "Loop ({repetitions} equivalent calls)" in text
    assert "Function Call Overhead" in text


def test_chapter_5_historical_stories_are_sourced_and_calibrated():
    text = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    range_check_code = code_block_after(
        "03-python/05-python-functions-modules.md",
        "This executable Python models only the range precondition.",
    )
    namespace: dict[str, object] = {}
    exec(range_check_code, namespace)
    checked_int16 = namespace["checked_int16"]
    assert checked_int16(32_767) == 32_767
    with pytest.raises(OverflowError):
        checked_int16(32_768)
    assert "CERN analysis scripts" not in text
    assert "NASA trajectory calculations" not in text
    assert "Weather prediction models" not in text
    assert "https://escholarship.org/uc/item/5dr206s3" in text
    assert "https://discovery.larc.nasa.gov/pdf_files/MCO_report_2.pdf" in text
    assert "https://ligo.org/science-summaries/gw150914cbc/" in text
    assert "https://www.esa.int/esapub/bulletin/bullet87/inbrie87.htm" in text
    assert "# SCHEMATIC: this is not source code from the LIGO analyses." in text
    assert "Python integers do\nnot themselves overflow at 16 bits." in text
    assert "does not make parallel execution literally impossible" in text


def test_chapter_5_reference_and_framework_claims_are_calibrated():
    text = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    assert "round(3.14, ndigits=2)" in text
    assert "round(3.14, digits=2)" not in text
    assert round(3.14, ndigits=2) == pytest.approx(3.14)
    assert "Google's NumPy replacement" not in text
    assert "Testing** is trivial" not in text
    assert "A climate model that tried to update global temperature" not in text
    assert "Real example that caused wrong results" not in text
    assert "stateful-computations.html" in text


def test_chapter_5_function_contract_activity_is_markdown_authored_and_discriminating():
    chapter = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch05-function-contract-inspector.md").read_text()
    launcher = (ROOT / "tools/jupyterlite/launchers/ch05-function-contract-inspector.html").read_text()
    assert "Browser Python lab · Function Contract Inspector" in chapter
    assert "jupyterlite/ch05-function-contract-inspector.html" in chapter
    assert "activity is optional" in chapter
    assert "name: xpython" in activity
    assert "Success condition" in activity
    assert "does **not**" in activity
    assert "lab/index.html?path=ch05-function-contract-inspector.ipynb" in launcher

    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 3
    namespace: dict[str, object] = {}
    for index, cell in enumerate(cells, start=1):
        exec(compile(cell, f"chapter-5-activity-cell-{index}", "exec"), namespace)

    assert namespace["kinetic_energy_cgs"](2.0, 3.0) == pytest.approx(9.0)
    assert namespace["record_checked"](1.0) == [1.0]
    with pytest.raises(ValueError):
        namespace["kinetic_energy_cgs"](-1.0, 1.0)


def test_temperature_class_enforces_construction_and_assignment_invariant():
    code = code_block_after("03-python/06-oop-fundamentals.md", "### Properties for Unit Safety")
    namespace: dict[str, object] = {}
    exec(code, namespace)
    temperature = namespace["Temperature"](0)
    assert temperature.celsius == pytest.approx(-273.15)
    with pytest.raises(ValueError):
        namespace["Temperature"](-1)
    with pytest.raises(ValueError):
        temperature.celsius = -274
    for nonfinite in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="finite"):
            namespace["Temperature"](nonfinite)


def test_chapter_6_temperature_microexperiment_is_markdown_authored_with_lite_execution():
    chapter = (ROOT / "03-python/06-oop-fundamentals.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch06-temperature-invariant.md").read_text()
    assert "Predict → run → explain → revise: constructor validation" in chapter
    assert "Browser Python lab · Temperature invariant" in chapter
    assert "jupyterlite/ch06-temperature-invariant.html" in chapter
    assert ":::{lecture-code}" not in chapter
    assert "activity source is Markdown" in chapter
    assert "jupyter:\n  lite: true" not in chapter
    assert "```{code-cell} python" in activity
    assert "name: xpython" in activity
    assert "07-numpy-fundamentals.md" in chapter
    assert "__array_ufunc__" in chapter
    assert "# PSEUDOCODE: this deliberately omits the device's real state model" in chapter


def test_temperature_microexperiment_launcher_preserves_the_notebook_path():
    launcher = (ROOT / "tools/jupyterlite/launchers/ch06-temperature-invariant.html").read_text()
    assert "lab/index.html?path=ch06-temperature-invariant.ipynb" in launcher
    assert "window.location.replace" in launcher


def test_chapter_6_nested_check_closes_before_method_types_section():
    chapter = (ROOT / "03-python/06-oop-fundamentals.md").read_text()
    before, after = chapter.split("### Method Types: Instance, Class, and Static", maxsplit=1)
    assert before.rstrip().endswith("::::")
    assert "::::{note} 🔍 Check Your Understanding" in before[-1_500:]
    assert after.lstrip().startswith("```{code-cell} python")


def test_chapter_6_hardens_object_contracts_and_case_studies():
    text = (ROOT / "03-python/06-oop-fundamentals.md").read_text()
    particle_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "Now let's see the same problem with OOP:"
    )
    particle_namespace: dict[str, object] = {}
    exec(particle_code, particle_namespace)
    particle = particle_namespace["Particle"](1.0, 0.0, 0.0, 10.0, 5.0)
    initial_energy = particle.kinetic_energy()
    particle.update_position(0.1)
    assert particle.kinetic_energy() == pytest.approx(initial_energy)

    vector_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "Now let's advance to more complex mathematical methods:"
    )
    vector_namespace: dict[str, object] = {}
    exec(vector_code, vector_namespace)
    vector = vector_namespace["Vector2D"]
    with pytest.raises(ValueError, match="undefined"):
        vector(0, 0).angle_with(vector(1, 0))
    with pytest.raises(ValueError, match="normalize"):
        vector(0, 0).normalize()

    statistics_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "1. **Managing State Over Time**"
    )
    statistics_namespace: dict[str, object] = {}
    exec(statistics_code, statistics_namespace)
    statistics = statistics_namespace["RunningStatistics"]()
    assert statistics.mean is None
    assert statistics.variance is None
    statistics.add_value(1.0)
    assert statistics.variance is None
    statistics.add_value(3.0)
    assert statistics.mean == pytest.approx(2.0)
    assert statistics.variance == pytest.approx(2.0)

    impulse_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "for the actual failure analysis."
    )
    impulse_namespace: dict[str, object] = {}
    exec(impulse_code, impulse_namespace)
    impulse = impulse_namespace["NavigationImpulse"](1.0)
    assert impulse.impulse_pound_force_seconds == pytest.approx(0.224809)
    impulse.impulse_pound_force_seconds = 0.224809
    assert impulse.impulse_newton_seconds == pytest.approx(1.0)

    assert "## Try this chapter" in text
    assert "Browser Python lab · Temperature invariant" in text
    assert "## Deep Dive: Python Protocols and Special Methods" in text
    assert "## Deep Dive: Choosing Objects or Functions" in text
    assert "## Reference: Debugging Small Scientific Objects" in text
    assert "## Reference: Class Syntax, Protocols, and Debugging" in text
    assert "Deep dive / reference" not in text
    assert "thrust_newtons" not in text
    assert "sky_brightness_category" not in text
    assert "https://llis.nasa.gov/lesson/1483" in text
    assert "https://www.astropy.org/history.html" in text
    assert "Python doesn't check types" not in text


def test_chapter_6_validation_examples_reject_nonfinite_values_and_state_their_bounds():
    text = (ROOT / "03-python/06-oop-fundamentals.md").read_text()

    circle_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "Properties can enforce **declared invariants**"
    )
    circle_namespace: dict[str, object] = {}
    exec(circle_code, circle_namespace)
    circle = circle_namespace["Circle"]
    for invalid_radius in (math.nan, math.inf, -math.inf, 0, True):
        with pytest.raises(ValueError, match="finite positive"):
            circle(invalid_radius)

    processor_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "### Method Types: Instance, Class, and Static"
    )
    processor_namespace: dict[str, object] = {}
    exec(processor_code, processor_namespace)
    processor = processor_namespace["DataProcessor"]
    assert processor.validate_data([1, 2.0])
    assert not processor.validate_data([])
    assert not processor.validate_data([math.nan])
    with pytest.raises(ValueError, match="non-empty"):
        processor([])
    with pytest.raises(ValueError, match="absolute zero"):
        processor.celsius_to_kelvin(-274)

    impulse_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "for the actual failure analysis."
    )
    impulse_namespace: dict[str, object] = {}
    exec(impulse_code, impulse_namespace)
    with pytest.raises(ValueError, match="finite"):
        impulse_namespace["NavigationImpulse"](math.nan)

    galaxy_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "2. **Modeling Real Entities**"
    )
    galaxy_namespace: dict[str, object] = {}
    exec(galaxy_code, galaxy_namespace)
    with pytest.raises(ValueError, match="blueshifted"):
        galaxy_namespace["m31"].lookback_time_gyr()
    assert galaxy_namespace["example_galaxy"].lookback_time_gyr() > 0

    function_code = code_block_after(
        "03-python/06-oop-fundamentals.md", "1. **Simple Transformations**"
    )
    function_namespace: dict[str, object] = {}
    exec(function_code, function_namespace)
    with pytest.raises(ValueError, match="absolute zero"):
        function_namespace["celsius_to_kelvin"](-274)
    with pytest.raises(ValueError, match="positive"):
        function_namespace["orbital_period_years_solar_mass"](0)

    assert "another_coord" not in text
    assert "m31.separation(m33)" in text
    assert "The root cause was a lack of validation" not in text
    assert "Reject one modeled unsafe configuration" in text
    assert "exact message is Python-version dependent" in text
    assert "`@staticmethod` + `def validate(data):`" in text


def test_temperature_microexperiment_rejects_nonfinite_values():
    activity = (ROOT / "tools/jupyterlite/activities/ch06-temperature-invariant.md").read_text()
    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    namespace: dict[str, object] = {}
    exec(cells[0], namespace)
    for nonfinite in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="finite"):
            namespace["Temperature"](nonfinite)


def test_chapter_7_preserves_a_core_route_and_makes_its_lab_discoverable():
    chapter = (ROOT / "04-scientific-computing/07-numpy-fundamentals.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch07-shape-mask-view-inspector.md").read_text()
    launcher = (ROOT / "tools/jupyterlite/launchers/ch07-shape-mask-view-inspector.html").read_text()

    assert chapter.index("## Why this chapter matters") < chapter.index("## Learning objectives")
    assert "## Try this chapter" in chapter
    assert "Browser Python lab · Shape, Mask, and View Inspector" in chapter
    assert "jupyterlite/ch07-shape-mask-view-inspector.html" in chapter
    assert "activity is optional" in chapter
    assert "## Deep Dive: Sampling Models and Their Assumptions" in chapter
    assert "## Deep Dive: Numerical Grids and Sampled Signals" in chapter
    assert "## Deep Dive: Measuring Array Performance and Memory" in chapter
    assert "## Reference: Array Operations and Numerical Utilities" in chapter
    assert "Deep dive / reference" not in chapter

    assert "name: xpython" in activity
    assert "Success condition" in activity
    assert "does\n**not** decide" in activity
    assert "lab/index.html?path=ch07-shape-mask-view-inspector.ipynb" in launcher

    cells = re.findall(r"```\{code-cell\} python\n(.*?)\n```", activity, re.DOTALL)
    assert len(cells) == 3
    namespace: dict[str, object] = {}
    for index, cell in enumerate(cells, start=1):
        exec(compile(cell, f"chapter-7-activity-cell-{index}", "exec"), namespace)

    assert namespace["corrected"].shape == (2, 3)
    assert namespace["bright_values"].shape == (2,)
    assert np.shares_memory(namespace["basic_slice"], namespace["flux_grid"])
    assert not np.shares_memory(namespace["fancy_columns"], namespace["flux_grid"])
    assert namespace["flux_grid"][0, 1] == -99.0


def test_chapter_7_signal_grid_and_covariance_examples_state_correct_contracts():
    chapter = (ROOT / "04-scientific-computing/07-numpy-fundamentals.md").read_text()

    fft_code = code_block_containing(
        "04-scientific-computing/07-numpy-fundamentals.md",
        "`rfft` and `rfftfreq` retain the non-negative frequencies",
    )
    fft_namespace: dict[str, object] = {}
    exec(fft_code, fft_namespace)
    assert fft_namespace["t"][1] - fft_namespace["t"][0] == pytest.approx(1 / 500)
    assert fft_namespace["peak_freqs"] == pytest.approx([5.0, 10.0, 50.0])
    assert fft_namespace["single_sided_amplitude"][5] == pytest.approx(1.0, abs=0.04)
    assert "NumPy's forward FFT is unnormalized" in chapter
    assert "not automatically a physical amplitude" in chapter
    assert "not yet a calibrated power measurement" in chapter

    calculus_code = code_block_containing(
        "04-scientific-computing/07-numpy-fundamentals.md",
        "Check both approximations first with a smooth signal whose answer is known",
    )
    calculus_namespace = {"np": np}
    exec(calculus_code, calculus_namespace)
    assert calculus_namespace["integrated_flux"] == pytest.approx(
        calculus_namespace["exact_integral"], abs=0.01
    )
    assert "Differentiation also amplifies measurement noise" in chapter

    grid_code = code_block_containing(
        "04-scientific-computing/07-numpy-fundamentals.md",
        "This is a 2D teaching model in normalized units",
    )
    grid_namespace = {"np": np}
    exec(grid_code, grid_namespace)
    assert grid_namespace["Fx"].shape == (50, 50)
    assert grid_namespace["Fy"].shape == (50, 50)
    assert "softening length changes the force" in chapter
    assert "Approximate integrated density" in chapter
    assert "density.sum():.2f" not in chapter

    covariance_code = code_block_containing(
        "04-scientific-computing/07-numpy-fundamentals.md",
        "Simulate a deliberately simplified stellar-property relationship",
    )
    covariance_namespace = {"np": np}
    exec(covariance_code, covariance_namespace)
    assert covariance_namespace["covariance_manual"] == pytest.approx(
        covariance_namespace["cov_matrix"][0, 1]
    )
    assert "Kelvin to Celsius adds a constant and therefore leaves covariance" in chapter
    assert "There is no universal cutoff" in chapter
    assert "L proportional to R^2 T^4" in chapter
    assert "illustrative display threshold (|r| > 0.5; not a strength test)" in chapter
    assert "Strong correlations (|r| > 0.5)" not in chapter


def test_chapter_7_handles_dtype_views_missingness_and_candidate_counts_honestly():
    chapter = (ROOT / "04-scientific-computing/07-numpy-fundamentals.md").read_text()
    transit_code = code_block_containing(
        "04-scientific-computing/07-numpy-fundamentals.md",
        "Candidate flagging using boolean masking",
    )
    transit_namespace = {"np": np}
    exec(transit_code, transit_namespace)

    assert len(transit_namespace["candidate_starts"]) == 9
    assert "a boolean threshold is not an exoplanet discovery" in chapter
    assert "Do not make every scientific array floating-point by reflex" in chapter
    assert "Filling is a modeling choice, not generic data cleaning" in chapter
    assert "Use `np.shares_memory` or `np.may_share_memory`" in chapter
    assert "| `.reshape()` | When possible | May copy for non-contiguous input |" in chapter
    assert "Random values from memory" not in chapter
    assert "- Nested loops: seconds" not in chapter
    assert "- NumPy with optimized BLAS: milliseconds" not in chapter
    assert "Real impact (measure it)" in chapter


def test_chapter_8_scales_uncertainty_and_pixel_examples_state_valid_contracts():
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    plt.show = lambda: None

    chapter_path = "04-scientific-computing/08-matplotlib-fundamentals.md"
    chapter = (ROOT / chapter_path).read_text()

    scale_code = code_block_containing(chapter_path, "Never take abs(data) to force this")
    scale_namespace = {"np": np, "plt": plt}
    exec(scale_code, scale_namespace)
    assert scale_namespace["axes"][4, 1].get_title() == "Log-Log: not valid"
    assert "np.abs(data)" not in chapter
    assert "Modeling boundary: scales and transformations" in chapter

    uncertainty_code = code_block_after(chapter_path, "### Error Bars: Proper Uncertainty Visualization")
    uncertainty_namespace = {"np": np, "plt": plt}
    exec(uncertainty_code, uncertainty_namespace)
    assert uncertainty_namespace["weights"] == pytest.approx(1 / uncertainty_namespace["y_err"])
    assert uncertainty_namespace["model_sigma"].min() > 0
    assert "inverse-standard-deviation weights" in chapter
    assert "1sigma confidence" not in chapter

    pixel_code = code_block_containing(chapter_path, "The 1% dip is deliberately exaggerated")
    pixel_namespace = {"np": np, "plt": plt}
    exec(pixel_code, pixel_namespace)
    assert pixel_namespace["relative_flux"][22] < 1
    assert "not a Kepler detection pipeline" in chapter
    assert "Approximate RA/Dec Display (not WCS)" in chapter
    assert "projection': wcs" in chapter

    assert "good_cmaps = ['viridis', 'plasma', 'cividis', 'magma']" in chapter
    assert "Deep dive / reference" not in chapter
    assert "## Reference: installation and scale-aware performance choices" in chapter
    assert "| PDF | Publication (vector) | `bbox_inches='tight'`" in chapter
    assert "Synthetic density (arbitrary units)" in chapter
    assert "statistically quantified discrepancy" in chapter
    assert "# `df` is a table with numeric 'ra' and 'dec' columns" in chapter
    plt.close("all")


def test_chapter_9_tests_behavior_without_claiming_scientific_validation():
    chapter_path = "04-scientific-computing/09-robust-computing.md"
    chapter = (ROOT / chapter_path).read_text()

    mars_code = code_block_after(chapter_path, "The immediate unit mismatch")
    mars_namespace: dict[str, object] = {}
    exec(mars_code, mars_namespace)
    combine_impulses = mars_namespace["combine_impulses_to_delta_v"]
    assert combine_impulses(4.4482216152605, "N s", 1.0, "lbf s", 2.0) == pytest.approx(4.4482216152605)
    with pytest.raises(ValueError, match="Unknown impulse unit"):
        combine_impulses(1.0, "m/s", 1.0, "N s", 1.0)

    validation_code = code_block_containing(chapter_path, "return wavelength, flux")
    validation_namespace = {"np": np}
    exec(validation_code, validation_namespace)
    process_spectrum = validation_namespace["process_spectrum"]
    wavelength, flux = process_spectrum([6500.0, 6501.0], [1.0, 0.9])
    assert np.array_equal(wavelength, [6500.0, 6501.0])
    assert np.array_equal(flux, [1.0, 0.9])
    with pytest.raises(ValueError, match="strictly increasing"):
        process_spectrum([6501.0, 6500.0], [1.0, 0.9])
    with pytest.raises(ValueError, match="Invalid redshift"):
        process_spectrum([6500.0, 6501.0], [1.0, 0.9], z=np.nan)

    orbit_code = code_block_containing(chapter_path, "def integrate_relative_orbit_leapfrog")
    orbit_namespace = {"np": np}
    exec(orbit_code, orbit_namespace)
    gravitational_constant = 6.67430e-11
    solar_mass_kg = 1.989e30
    earth_mass_kg = 5.972e24
    orbital_radius_m = 1.496e11
    circular_speed_m_s = math.sqrt(
        gravitational_constant * (solar_mass_kg + earth_mass_kg) / orbital_radius_m
    )
    orbit = orbit_namespace["integrate_relative_orbit_leapfrog"](
        [orbital_radius_m, 0.0, 0.0],
        [0.0, circular_speed_m_s, 0.0],
        solar_mass_kg,
        earth_mass_kg,
        86_400.0,
        101,
        max_relative_energy_error=1e-5,
    )
    assert orbit.shape == (102, 3)
    assert np.isfinite(orbit).all()

    cosmology_code = code_block_containing(chapter_path, "luminosity_distance_matter_lambda")
    cosmology_namespace = {"np": np}
    exec(cosmology_code, cosmology_namespace)
    distance = cosmology_namespace["luminosity_distance_matter_lambda"](1100)
    assert np.isfinite(distance) and distance > 0

    refinement_code = code_block_containing(chapter_path, "def euler_exponential")
    refinement_namespace: dict[str, object] = {}
    exec(refinement_code, refinement_namespace)
    assert abs(refinement_namespace["euler_exponential"](0.05) - math.e) < abs(
        refinement_namespace["euler_exponential"](0.1) - math.e
    )

    assert "## Reference: definitions and quick checks" in chapter
    assert "passive numerical stability issue" not in chapter
    assert "This scalar calculation ignores vector direction" in chapter
    assert "not a validated cosmology" in chapter
    assert "deterministic random behavior" in chapter
    assert "Binary search debugging" not in chapter
    assert "n_raw_saturated = np.sum(image >= saturation_level)" in chapter
    assert "Flat frame must be finite and strictly positive" in chapter
