#!/usr/bin/env python3
"""Keep volatile course details out of the landing page.

The schedule and Projects pages are the authoritative sources for dates and
project sequence. This check prevents the landing page from silently restoring a
second, stale roadmap.
"""

from pathlib import Path
import sys


HOME = Path("index.md")
REQUIRED = (
    "provisional through **Thu Sep 24**",
    "01-course-info/syllabus.md",
    "01-course-info/schedule.md",
    "01-course-info/projects.md",
    "01-course-info/ai-policy.md",
    "02-getting-started/index.md",
)
FORBIDDEN = (
    "| Weeks | Project | Focus | Due |",
    "The thread running through everything",
    "Complete data science pipeline",
    "Monday, August 24",
)


def main() -> int:
    text = HOME.read_text()
    problems = [f"missing required text: {item!r}" for item in REQUIRED if item not in text]
    problems.extend(f"stale duplicate content: {item!r}" for item in FORBIDDEN if item in text)
    if problems:
        print("Landing-page contract failed:")
        print("\n".join(f"- {problem}" for problem in problems))
        return 1
    print("Landing-page contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
