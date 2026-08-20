import unittest
from pathlib import Path


WIDGET = Path(__file__).resolve().parents[1] / "plugins" / "interactive-lecture" / "widget.mjs"


class InteractiveLectureWidgetTests(unittest.TestCase):
    def test_widget_is_self_contained_and_preserves_the_course_base_path(self):
        source = WIDGET.read_text()

        self.assertNotIn('from "./runtime.mjs"', source)
        self.assertIn('document.querySelector("base")?.href || new URL("./", location.href)', source)
        self.assertIn('new URL(`jupyterlite/lab/index.html?', source)


if __name__ == "__main__":
    unittest.main()
