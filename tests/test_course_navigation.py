from pathlib import Path
import re

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


def test_myst_toc_uses_the_approved_top_level_libraries():
    config = (ROOT / "myst.yml").read_text()
    titles = re.findall(r"^    - title: (.+)$", config, flags=re.MULTILINE)
    assert titles[:7] == [
        "Course Info & Roadmap",
        "Scientific Computing with Python",
        "Readings",
        "Lectures",
        "Practice Labs",
        "Assessments",
        "Tools & Workflow",
    ]


@pytest.mark.parametrize(
    ("path", "number"),
    [
        ("03-python/01-python-environment.md", 1),
        ("03-python/02-python-calculator.md", 2),
        ("03-python/03-python-control-flow.md", 3),
        ("03-python/04-python-data-structures.md", 4),
        ("03-python/05-python-functions-modules.md", 5),
        ("03-python/06-oop-fundamentals.md", 6),
        ("04-scientific-computing/07-numpy-fundamentals.md", 7),
        ("04-scientific-computing/08-matplotlib-fundamentals.md", 8),
        ("04-scientific-computing/09-robust-computing.md", 9),
        ("04-scientific-computing/10-advanced-oop.md", 10),
        ("04-scientific-computing/11-pandas-fundamentals.md", 11),
        ("04-scientific-computing/12-data-acquisition-cleaning.md", 12),
    ],
)
def test_python_textbook_chapter_title_is_sequential(path, number):
    text = (ROOT / path).read_text()
    assert f'title: "Chapter {number}:' in text
