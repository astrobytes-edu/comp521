import unittest
from pathlib import Path


WIDGET = Path(__file__).resolve().parents[1] / "plugins" / "interactive-lecture" / "widget.mjs"
LECTURE_STYLES = Path(__file__).resolve().parents[1] / "assets" / "lecture-projector.css"
LECTURE_ONE = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-01-run-calculate-inspect.md"
LECTURE_TWO = Path(__file__).resolve().parents[1] / "03-python" / "bootcamp-02-procedures-decisions.md"


class InteractiveLectureWidgetTests(unittest.TestCase):
    def test_widget_is_self_contained_and_preserves_the_course_base_path(self):
        source = WIDGET.read_text()

        self.assertNotIn('from "./runtime.mjs"', source)
        self.assertIn('document.querySelector("base")?.href || new URL("./", location.href)', source)
        self.assertIn('new URL(`jupyterlite/lab/index.html#/tree/', source)

    def test_lecture_one_mermaid_classes_do_not_use_reserved_end_keyword(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("classDef outcome", lecture)
        self.assertNotIn("classDef end", lecture)
        self.assertNotIn("class evidence,claim end", lecture)

    def test_lecture_one_examples_are_self_contained_and_standard_library_first(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("radius_km = 4.2", lecture)
        self.assertIn('importlib.util.find_spec("math")', lecture)
        self.assertIn("import math\n\npredicted_flux_erg_s_cm2", lecture)
        self.assertIn("import random", lecture)
        self.assertNotIn("import numpy as np", lecture)

    def test_lecture_one_explains_and_indexes_its_function_calls(self):
        lecture = LECTURE_ONE.read_text()

        self.assertIn("## How to read a function call", lecture)
        self.assertIn("## Reference · calls for ordinary Python work", lecture)
        self.assertIn("## Reference · environment and provenance calls", lecture)
        self.assertIn("## Reference · numerical calls and their arguments", lecture)
        self.assertIn("## Reference · stable and complex-number helpers", lecture)

    def test_lecture_one_links_to_official_docs_for_every_standard_library_module(self):
        lecture = LECTURE_ONE.read_text()

        for module in ("math", "sys", "pathlib", "random", "importlib", "cmath"):
            self.assertIn(f"https://docs.python.org/3/library/{module}.html", lecture)
        self.assertIn("https://docs.python.org/3/library/functions.html", lecture)

    def test_projector_code_uses_a_larger_readable_scale(self):
        styles = LECTURE_STYLES.read_text()

        self.assertIn("calc(1.25rem * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(2vw * var(--lecture-font-scale, 1))", styles)
        self.assertIn("calc(1.8rem * var(--lecture-font-scale, 1))", styles)

    def test_lecture_two_scaffolds_core_python_before_a_bounded_numpy_preview(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## I · Procedures and decisions",
            "## II · Store related observations deliberately",
            "## III · Package a calculation as a function",
            "## IV · First contact with NumPy",
        ):
            self.assertIn(heading, lecture)

        self.assertNotIn("## Exit check", lecture)

        self.assertIn(":::{projector-controls}", lecture)
        self.assertIn(":::{interactive-python}", lecture)
        self.assertIn("import numpy as np", lecture)
        self.assertIn("Week 2", lecture)
        self.assertIn("not yet learning", lecture)
        self.assertIn("03-python-control-flow.md", lecture)
        self.assertIn("04-python-data-structures.md", lecture)
        self.assertIn("05-python-functions-modules.md", lecture)
        self.assertIn("07-numpy-fundamentals.md", lecture)

        for heading in (
            "## More than two outcomes · `elif`",
            "## Combine conditions deliberately",
            "## Short-circuiting protects a calculation",
            "## `while` repeats until a stated condition changes",
            "## `for` loops: one procedure for every observation",
        ):
            self.assertIn(heading, lecture)

        self.assertLess(
            lecture.index("## Why programs need control flow"),
            lecture.index("## A Boolean expression chooses a branch"),
        )
        self.assertLess(
            lecture.index("## Loops apply one procedure repeatedly"),
            lecture.index("## `while` repeats until a stated condition changes"),
        )
        self.assertLess(
            lecture.index("## `while` repeats until a stated condition changes"),
            lecture.index("## `for` loops: one procedure for every observation"),
        )
        self.assertLess(
            lecture.index("## Write the rule before the code"),
            lecture.index("## A Boolean expression chooses a branch"),
        )
        self.assertLess(
            lecture.index("## `while` repeats until a stated condition changes"),
            lecture.index("## III · Package a calculation as a function"),
        )

    def test_lecture_two_has_worked_self_study_checks_and_a_numerically_sound_test(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("math.isclose(", lecture)
        self.assertNotIn("assert transit_depth(1.0, 10.0) == 0.01", lecture)
        self.assertIn("Example `or` policy", lecture)
        self.assertIn("**Read it:** `0.984` reaches the `0.990` branch.", lecture)
        self.assertIn("**Expected result:** no error; the body is skipped.", lecture)
        self.assertIn("**Expected result:** `stopped at step 3: residual = 0.010`.", lecture)
        self.assertIn("**Call contract:**", lecture)
        self.assertIn("`np.ones_like(time_days)` creates ones with the same shape", lecture)

    def test_lecture_two_uses_a_science_facing_elif_example_and_bounds_transit_domain(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("observation-triage example", lecture)
        self.assertNotIn("01-course-info/grading.md", lecture)
        self.assertIn("strong low-flux candidate", lecture)
        self.assertIn("radius_planet_cm > radius_star_cm", lecture)
        self.assertIn("full-overlap, uniform-brightness geometry", lecture)
        self.assertIn("Run this definition first", lecture)
        self.assertIn("strict software-test tolerance", lecture)

    def test_lecture_two_states_why_conditionals_and_loops_matter_before_syntax(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("A **conditional** is a fork in a procedure", lecture)
        self.assertIn("A `for` loop is the right default when a collection supplies", lecture)
        self.assertIn("A `while` loop is for work whose number of repeats is not known", lecture)

    def test_lecture_two_keeps_first_use_references_and_function_anatomy(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## Reference · conditionals and Boolean logic",
            "## Reference · loop patterns",
            "## Reference · collections and mutation",
            "## Anatomy of a function",
            "## Reference · functions and tests",
            "## Reference · NumPy essentials",
        ):
            self.assertIn(heading, lecture)

        self.assertLess(
            lecture.index("## Short-circuiting protects a calculation"),
            lecture.index("## Reference · conditionals and Boolean logic"),
        )
        self.assertLess(
            lecture.index("## Trace the loop; do not guess"),
            lecture.index("## Reference · loop patterns"),
        )
        self.assertLess(
            lecture.index("## Mutability is a bookkeeping choice"),
            lecture.index("## Reference · collections and mutation"),
        )
        self.assertLess(
            lecture.index("## Anatomy of a function"),
            lecture.index("## Reference · functions and tests"),
        )
        self.assertLess(
            lecture.index("## Run · make one simple numerical grid"),
            lecture.index("## Reference · NumPy essentials"),
        )

    def test_lecture_two_test_sequence_is_honest_and_fails_when_invalid_inputs_are_accepted(self):
        lecture = LECTURE_TWO.read_text()

        self.assertNotIn("Continuing from the preceding slide", lecture)
        self.assertIn("## Run the definition, then run its tests", lecture)
        self.assertIn('raise AssertionError("transit_depth accepted invalid geometry")', lecture)

    def test_lecture_two_covers_the_remaining_core_control_flow_data_and_function_topics(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## Stop, skip, or finish a loop deliberately",
            "## Nested loops: one procedure across two dimensions",
            "## List comprehensions: compact a simple loop",
            "## Tuples and sets express different relationships",
            "## Copying nested data needs an explicit decision",
            "## `return` makes a result reusable; `print` only displays it",
            "## Defaults and scope keep function behavior predictable",
            "## Never use a mutable object as a default argument",
            "## Modules are reusable boundaries",
            "## From a function contract to evidence",
        ):
            self.assertIn(heading, lecture)

        self.assertIn("break", lecture)
        self.assertIn("continue", lecture)
        self.assertIn("for ... else", lecture)
        self.assertIn("copy.deepcopy", lecture)
        self.assertIn("import math", lecture)
        self.assertIn("mutable default", lecture)

    def test_lecture_two_uses_one_consistent_transit_ratio_domain(self):
        lecture = LECTURE_TWO.read_text()

        self.assertIn("0 < Rp <= Rstar", lecture)
        self.assertIn("0.0 < radius_ratio <= 1.0", lecture)
        self.assertNotIn("0.0 < radius_ratio < 1.0", lecture)
        self.assertLess(
            lecture.index("## From a function contract to evidence"),
            lecture.index("## Run the definition, then run its tests"),
        )


if __name__ == "__main__":
    unittest.main()
