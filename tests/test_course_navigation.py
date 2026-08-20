from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("path", "required"),
    [
        (
            "01-course-info/this-week.md",
            ('title: "This Week"', "schedule.md", "projects.md"),
        ),
        (
            "01-course-info/technology-submission.md",
            (
                'title: "Course Technology & Submission Path"',
                "02-getting-started/index.md",
                "projects.md",
            ),
        ),
        (
            "07-practice-labs/index.md",
            ('title: "Practice Labs"', "ungraded"),
        ),
        (
            "08-assessments/index.md",
            (
                'title: "Assessments"',
                "projects.md",
                "growth-reflections.md",
                "grading.md",
            ),
        ),
    ],
)
def test_new_course_route_has_its_required_contract(path, required):
    text = (ROOT / path).read_text()
    for fragment in required:
        assert fragment in text
