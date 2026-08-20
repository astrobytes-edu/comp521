import unittest
from pathlib import Path

from scripts.check_interactive_lectures import validate_text


class InteractiveLectureValidatorTests(unittest.TestCase):
    def test_rejects_duplicate_prompt_ids(self):
        text = """:::{lecture-write}
:id: same
:prompt: First
:::
:::{lecture-checkpoint}
:id: same
:prompt: Second
:::
"""
        self.assertEqual(
            validate_text(text, "lesson.md"),
            ["lesson.md:5: duplicate lecture prompt id 'same'"],
        )

    def test_rejects_media_without_accessibility_assets(self):
        text = """:::{lecture-media}
:id: orbit
:mp4: orbit.mp4
:::
"""
        self.assertEqual(
            validate_text(text, "lesson.md"),
            ["lesson.md:1: lecture-media requires webm, poster, captions, transcript, and fallback"],
        )

    def test_accepts_complete_panel_contract(self):
        text = """:::{lecture-panel}
:id: depth
:src: transit-geometry-dashboard
:fallback: The blocked fraction is p squared.
:::
"""
        self.assertEqual(validate_text(text, "lesson.md"), [])

    def test_rejects_youtube_only_media(self):
        text = """:::{lecture-media}
:id: transit-motion
:youtube_id: abc123
:::
"""
        self.assertEqual(
            validate_text(text, "lesson.md"),
            ["lesson.md:1: lecture-media requires webm, poster, captions, transcript, and fallback"],
        )

    def test_rejects_prediction_without_options(self):
        text = """:::{lecture-predict}
:id: prediction
:prompt: Make a claim.
:::
"""
        self.assertEqual(
            validate_text(text, "lesson.md"),
            ["lesson.md:1: lecture-predict requires options"],
        )

    def test_rejects_code_activity_without_fallback(self):
        text = """:::{lecture-code}
:id: experiment
:starter: transit-depth.ipynb
:::
"""
        self.assertEqual(
            validate_text(text, "lesson.md"),
            ["lesson.md:1: lecture-code requires starter and fallback"],
        )

    def test_accepts_v2_semantic_activity_contract(self):
        text = """:::{interactive-lecture}
:title: Test lecture
:::
:::{lecture-scene}
:id: setup
:::
:::{lecture-predict}
:id: prediction
:prompt: Predict.
:options: doubles|quadruples|unchanged
:::
:::{lecture-figure}
:id: figure
:model: transit-depth
:fallback: Depth is p squared.
:::
:::{lecture-reveal}
:id: reasoning
:::
:::{lecture-code}
:id: code
:starter: transit-depth.ipynb
:fallback: Run the supplied model.
:::
:::{lecture-checkpoint}
:id: checkpoint
:prompt: Explain.
:::
:::{presenter-note}
:scene: setup
:ask: Ask for a prediction.
:wait: 45 seconds
:::
"""
        self.assertEqual(validate_text(text, "lesson.md"), [])

    def test_smoke_fixture_satisfies_the_source_contract(self):
        fixture = Path("tests/fixtures/interactive-lecture-smoke.md").read_text()
        self.assertEqual(validate_text(fixture, "fixture.md"), [])

    def test_transit_pilot_has_no_lecture_contract_errors(self):
        pilot = Path("03-python/interactive-lab-transit-depth.md").read_text()
        self.assertEqual(validate_text(pilot, "03-python/interactive-lab-transit-depth.md"), [])


if __name__ == "__main__":
    unittest.main()
