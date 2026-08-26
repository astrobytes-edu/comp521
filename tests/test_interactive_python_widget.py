import unittest
from pathlib import Path


WIDGET = Path(__file__).resolve().parents[1] / "plugins" / "interactive-python" / "widget.mjs"
PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "interactive-python" / "interactive-python.mjs"


class InteractivePythonWidgetTests(unittest.TestCase):
    def test_matplotlib_is_loaded_only_for_plotting_experiments(self):
        source = WIDGET.read_text()

        self.assertIn("const usesMatplotlib", source)
        self.assertIn('"matplotlib"]', source)
        self.assertIn("if (usesMatplotlib)", source)
        self.assertIn('const figures = usesMatplotlib ?', source)

    def test_plugin_registers_the_lecture_widgets(self):
        source = PLUGIN.read_text()

        self.assertIn('name: "notebook-state"', source)
        self.assertIn('name: "projector-controls"', source)
        self.assertIn("directives: [interactivePython, notebookState, projectorControls]", source)


if __name__ == "__main__":
    unittest.main()
