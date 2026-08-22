from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]


PART_I_II_CHAPTERS = (
    "03-python/01-python-environment.md",
    "03-python/02-python-calculator.md",
    "03-python/03-python-control-flow.md",
    "03-python/04-python-data-structures.md",
    "03-python/05-python-functions-modules.md",
    "03-python/06-oop-fundamentals.md",
    "04-scientific-computing/07-numpy-fundamentals.md",
    "04-scientific-computing/08-matplotlib-fundamentals.md",
    "04-scientific-computing/09-robust-computing.md",
    "04-scientific-computing/10-advanced-oop.md",
)


@pytest.mark.parametrize("path", PART_I_II_CHAPTERS)
def test_completed_chapter_exposes_reader_contract(path):
    text = (ROOT / path).read_text()
    for heading in (
        "## Prerequisites",
        "## Learning objectives",
    ):
        assert heading in text
    assert text.count("## Learning objectives") == 1
    assert text.count("## Prerequisites") == 1


@pytest.mark.parametrize("path", PART_I_II_CHAPTERS)
def test_completed_chapters_use_no_warning_directives(path):
    text = (ROOT / path).read_text()
    assert not re.search(r"^:{3,}\{warning\}", text, flags=re.MULTILINE)
    assert not re.search(r"^:{3,}\{[^}]+\} .*⚠️", text, flags=re.MULTILINE)


def test_part_i_and_ii_guides_are_course_agnostic_and_truthful():
    part_i = (ROOT / "03-python/index.md").read_text()
    part_ii = (ROOT / "04-scientific-computing/index.md").read_text()
    assert "Project 1" not in part_i
    assert "assignments and projects" not in part_ii
    assert "11-pandas-fundamentals.md" not in part_ii
    assert "Chapter 6 completes the first\npass" in part_i
    assert "[Part I Recap — Trustworthy Scientific Programming](synthesis.md)" in part_i
    assert "[Part II Recap — Inspectable Scientific Evidence](synthesis.md)" in part_ii


def test_part_recaps_and_tentative_part_iii_navigation_are_explicit():
    part_i_recap = (ROOT / "03-python/synthesis.md").read_text()
    part_ii_recap = (ROOT / "04-scientific-computing/synthesis.md").read_text()
    part_iii = (ROOT / "04-scientific-computing/part-3-data-workflows.md").read_text()
    navigation = (ROOT / "myst.yml").read_text()

    assert 'title: "Part I Recap — Trustworthy Scientific Programming"' in part_i_recap
    assert 'title: "Part II Recap — Inspectable Scientific Evidence"' in part_ii_recap
    assert "A return route, not another chapter" in part_i_recap
    assert "A return route, not another chapter" in part_ii_recap
    assert "not a completed reading route" in part_iii
    assert "Part III · Real Data Workflows (in development)" in navigation
    assert "Early reference · Chapter 11" in navigation
    assert "Scope note · Chapter 12" in navigation
    assert "04-scientific-computing/synthesis.md" in navigation


def test_deferred_part_iii_is_honest_about_its_status():
    part_iii = (ROOT / "04-scientific-computing/part-3-data-workflows.md").read_text()
    chapter_12 = (ROOT / "04-scientific-computing/12-data-acquisition-cleaning.md").read_text()
    assert "in development" in part_iii.lower()
    assert "in development" in chapter_12.lower()


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


def test_myst_toc_uses_the_release_one_textbook_part_labels():
    config = (ROOT / "myst.yml").read_text()
    assert "title: Part I · Foundations for Scientific Programming" in config
    assert "title: Part II · Arrays, Visualization, and Reliable Computing" in config


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
