"""Executable regression checks for corrected Part I teaching examples."""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def code_block_after(path: str, marker: str) -> str:
    """Return the first Python fence after a visible Markdown marker."""
    text = (ROOT / path).read_text()
    remainder = text[text.index(marker) :]
    match = re.search(r"```(?:\{code-cell\} )?python\n(.*?)\n```", remainder, re.DOTALL)
    assert match, f"no Python block after {marker!r} in {path}"
    return match.group(1)


def test_complete_chapter_1_script_compiles_and_imports_cleanly():
    script = code_block_after("03-python/01-python-environment.md", "Complete calculation.py Script")
    assert "\n\timport numpy" not in script
    namespace = {"__name__": "imported_example"}
    exec(compile(script, "calculation.py", "exec"), namespace)
    assert namespace["schwarzschild_radius"](10 * namespace["M_sun"]) == pytest.approx(29_533.39, rel=1e-5)


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


def test_chapter_3_calibrates_toy_stellar_and_schwarzschild_examples():
    text = (ROOT / "03-python/03-python-control-flow.md").read_text()
    assert "classify_stellar_fate_toy" in text
    assert "not a remnant" in text
    assert "rs_au = 1.97e-8 * M" in text
    assert "difference of two large aggregate terms" in text


def test_chapter_4_calibrates_collection_performance_and_eos_analogy():
    text = (ROOT / "03-python/04-python-data-structures.md").read_text()
    assert "average-case hash lookup" in text
    assert "not a substitute for profiling the real workload" in text
    assert "not ordinary Python-dictionary lookup as a physical model" in text


def test_trapezoid_example_labels_its_approximation_and_executes():
    code = code_block_after("03-python/05-python-functions-modules.md", "### Documentation Levels")
    namespace: dict[str, object] = {}
    exec(code, namespace)
    assert namespace["result"] == pytest.approx(2.75)
    text = (ROOT / "03-python/05-python-functions-modules.md").read_text()
    assert "trapezoidal *approximation*" in text
    assert "Local input checks" in text
    assert "# PSEUDOCODE: set_mode" in text


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


def test_chapter_6_temperature_microexperiment_is_markdown_authored_with_lite_execution():
    chapter = (ROOT / "03-python/06-oop-fundamentals.md").read_text()
    activity = (ROOT / "tools/jupyterlite/activities/ch06-temperature-invariant.md").read_text()
    assert "Predict → run → explain → revise: constructor validation" in chapter
    assert ":starter: ch06-temperature-invariant.ipynb" in chapter
    assert "repository source" in chapter
    assert "jupyter:\n  lite: true" not in chapter
    assert "```{code-cell} python" in activity
    assert "name: xpython" in activity
    assert "07-numpy-fundamentals.md" in chapter
    assert "__array_ufunc__" in chapter
    assert "# PSEUDOCODE: this deliberately omits the device's real state model" in chapter


def test_chapter_6_nested_check_closes_before_method_types_section():
    chapter = (ROOT / "03-python/06-oop-fundamentals.md").read_text()
    before, after = chapter.split("### Method Types: Instance, Class, and Static", maxsplit=1)
    assert before.rstrip().endswith("::::")
    assert "::::{note} 🔍 Check Your Understanding" in before[-1_500:]
    assert after.lstrip().startswith("```{code-cell} python")
