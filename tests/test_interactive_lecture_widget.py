import unittest
from pathlib import Path


WIDGET = Path(__file__).resolve().parents[1] / "plugins" / "interactive-lecture" / "widget.mjs"
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

    def test_lecture_two_scaffolds_core_python_before_a_bounded_numpy_preview(self):
        lecture = LECTURE_TWO.read_text()

        for heading in (
            "## I · Procedures and decisions",
            "## II · Store related observations deliberately",
            "## III · Package a calculation as a function",
            "## IV · First contact with NumPy",
            "## Exit check",
        ):
            self.assertIn(heading, lecture)

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
        ):
            self.assertIn(heading, lecture)

        self.assertLess(
            lecture.index("## Write the rule before the code"),
            lecture.index("## A Boolean expression chooses a branch"),
        )
        self.assertLess(
            lecture.index("## `while` repeats until a stated condition changes"),
            lecture.index("## III · Package a calculation as a function"),
        )


if __name__ == "__main__":
    unittest.main()
